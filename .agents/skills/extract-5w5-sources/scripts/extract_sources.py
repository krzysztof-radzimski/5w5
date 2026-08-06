#!/usr/bin/env python3
"""Extract validated source material for a 5w5 passage."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


BOOK_ALIASES: dict[str, tuple[str, ...]] = {
    "Rdz": ("Genesis", "Gen"),
    "Wj": ("Exodus", "Exod", "Ex"),
    "Kpł": ("Leviticus", "Lev"),
    "Lb": ("Numbers", "Num"),
    "Pwt": ("Deuteronomy", "Deut"),
    "Joz": ("Joshua", "Josh"),
    "Sdz": ("Judges", "Judg"),
    "Rt": ("Ruth",),
    "1Sm": ("1 Samuel", "1 Sam"),
    "2Sm": ("2 Samuel", "2 Sam"),
    "1Krl": ("1 Kings", "1 Kgs"),
    "2Krl": ("2 Kings", "2 Kgs"),
    "1Krn": ("1 Chronicles", "1 Chron", "1 Chr"),
    "2Krn": ("2 Chronicles", "2 Chron", "2 Chr"),
    "Ezd": ("Ezra",),
    "Neh": ("Nehemiah", "Neh"),
    "Est": ("Esther", "Esth"),
    "Hi": ("Job",),
    "Ps": ("Psalms", "Psalm", "Ps"),
    "Prz": ("Proverbs", "Prov"),
    "Kaz": ("Ecclesiastes", "Eccl"),
    "Pnp": ("Song of Songs", "Song of Solomon", "Song"),
    "Iz": ("Isaiah", "Isa"),
    "Jr": ("Jeremiah", "Jer"),
    "Lm": ("Lamentations", "Lam"),
    "Ez": ("Ezekiel", "Ezek"),
    "Dn": ("Daniel", "Dan"),
    "Oz": ("Hosea", "Hos"),
    "Jl": ("Joel",),
    "Am": ("Amos",),
    "Ab": ("Obadiah", "Obad"),
    "Jo": ("Jonah",),
    "Mi": ("Micah", "Mic"),
    "Na": ("Nahum",),
    "Ha": ("Habakkuk", "Hab"),
    "So": ("Zephaniah", "Zeph"),
    "Ag": ("Haggai", "Hag"),
    "Za": ("Zechariah", "Zech"),
    "Ml": ("Malachi", "Mal"),
    "Mt": ("Matthew", "Matt"),
    "Mk": ("Mark",),
    "Łk": ("Luke", "Lk"),
    "J": ("John",),
    "Dz": ("Acts",),
    "Rz": ("Romans", "Rom"),
    "1Kor": ("1 Corinthians", "1 Cor"),
    "2Kor": ("2 Corinthians", "2 Cor"),
    "Ga": ("Galatians", "Gal"),
    "Ef": ("Ephesians", "Eph"),
    "Flp": ("Philippians", "Phil"),
    "Kol": ("Colossians", "Col"),
    "1Tes": ("1 Thessalonians", "1 Thess", "1 Thes"),
    "2Tes": ("2 Thessalonians", "2 Thess", "2 Thes"),
    "1Tm": ("1 Timothy", "1 Tim"),
    "2Tm": ("2 Timothy", "2 Tim"),
    "Tt": ("Titus",),
    "Flm": ("Philemon", "Phlm"),
    "Hbr": ("Hebrews", "Heb"),
    "Jk": ("James", "Jas"),
    "1P": ("1 Peter", "1 Pet"),
    "2P": ("2 Peter", "2 Pet"),
    "1J": ("1 John",),
    "2J": ("2 John",),
    "3J": ("3 John",),
    "Jud": ("Jude",),
    "Obj": ("Revelation", "Rev"),
}


@dataclass(frozen=True)
class Passage:
    book: str
    start_chapter: int
    start_verse: int | None
    end_chapter: int
    end_verse: int | None

    @property
    def folder_reference(self) -> str:
        if self.start_verse is None:
            return f"{self.book} {self.start_chapter}"
        start = f"{self.start_chapter},{self.start_verse}"
        if self.start_chapter == self.end_chapter:
            if self.start_verse == self.end_verse:
                return f"{self.book} {start}"
            return f"{self.book} {start}-{self.end_verse}"
        return f"{self.book} {start}-{self.end_chapter},{self.end_verse}"

    @property
    def display_reference(self) -> str:
        return self.folder_reference.replace("-", "–")


@dataclass(frozen=True)
class CommentarySection:
    start_line: int
    end_line: int
    level: int
    heading: str
    reference: str
    span: int
    start_ordinal: int
    end_ordinal: int


PASSAGE_RE = re.compile(
    r"^\s*(?P<book>\S+)\s+(?P<sc>\d+)"
    r"(?:[,:](?P<sv>\d+)"
    r"(?:\s*[-–—]\s*(?:(?P<ec>\d+)[,:])?(?P<ev>\d+))?"
    r")?\s*$"
)
HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")


class ExtractionError(RuntimeError):
    """Expected input or source-data error."""


def parse_passage(raw: str) -> Passage:
    match = PASSAGE_RE.match(raw)
    if not match:
        raise ExtractionError(
            "Nieprawidłowy odnośnik. Użyj np. '2Tm 2,20-26' albo "
            "'2Tm 1,15-2,7'."
        )

    book = match.group("book")
    start_chapter = int(match.group("sc"))
    start_verse = int(match.group("sv")) if match.group("sv") else None
    end_chapter = int(match.group("ec")) if match.group("ec") else start_chapter
    end_verse = int(match.group("ev")) if match.group("ev") else start_verse
    return Passage(book, start_chapter, start_verse, end_chapter, end_verse)


def load_bible(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise ExtractionError(f"Nie znaleziono pliku Biblii: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ExtractionError(f"Nieprawidłowy JSON w {path}: {exc}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("books"), dict):
        raise ExtractionError(f"Plik {path} nie zawiera obiektu .books.")
    return data


def numeric_keys(mapping: dict[str, Any], label: str) -> list[int]:
    try:
        return sorted(int(key) for key in mapping)
    except (TypeError, ValueError) as exc:
        raise ExtractionError(f"{label} zawiera klucz, który nie jest liczbą.") from exc


def validate_and_collect(
    bible: dict[str, Any], passage: Passage
) -> tuple[Passage, list[tuple[int, int, str]], dict[tuple[int, int], int]]:
    books = bible["books"]
    if passage.book not in books:
        available = ", ".join(sorted(books))
        raise ExtractionError(
            f"Nie znaleziono księgi '{passage.book}'. Dostępne skróty: {available}"
        )

    chapters = books[passage.book].get("chapters")
    if not isinstance(chapters, dict):
        raise ExtractionError(f"Księga {passage.book} nie zawiera rozdziałów.")

    chapter_numbers = numeric_keys(chapters, f"Rozdziały księgi {passage.book}")
    for chapter in range(passage.start_chapter, passage.end_chapter + 1):
        if chapter not in chapter_numbers:
            raise ExtractionError(f"Nie znaleziono {passage.book} {chapter}.")

    if passage.start_chapter > passage.end_chapter:
        raise ExtractionError("Początek zakresu znajduje się po jego końcu.")

    if passage.start_verse is None:
        if passage.start_chapter != passage.end_chapter:
            raise ExtractionError("Zakres wielu rozdziałów musi wskazywać wersety.")
        verse_numbers = numeric_keys(
            chapters[str(passage.start_chapter)],
            f"Wersety {passage.book} {passage.start_chapter}",
        )
        normalized = Passage(
            passage.book,
            passage.start_chapter,
            verse_numbers[0],
            passage.start_chapter,
            verse_numbers[-1],
        )
    else:
        normalized = passage

    assert normalized.start_verse is not None
    assert normalized.end_verse is not None
    if (normalized.start_chapter, normalized.start_verse) > (
        normalized.end_chapter,
        normalized.end_verse,
    ):
        raise ExtractionError("Początek zakresu znajduje się po jego końcu.")

    ordinal_by_verse: dict[tuple[int, int], int] = {}
    ordinal = 0
    for chapter in chapter_numbers:
        verse_map = chapters[str(chapter)]
        if not isinstance(verse_map, dict):
            raise ExtractionError(f"Rozdział {passage.book} {chapter} nie jest obiektem.")
        for verse in numeric_keys(verse_map, f"Wersety {passage.book} {chapter}"):
            ordinal_by_verse[(chapter, verse)] = ordinal
            ordinal += 1

    start_key = (normalized.start_chapter, normalized.start_verse)
    end_key = (normalized.end_chapter, normalized.end_verse)
    if start_key not in ordinal_by_verse:
        raise ExtractionError(
            f"Nie znaleziono wersetu {passage.book} "
            f"{normalized.start_chapter},{normalized.start_verse}."
        )
    if end_key not in ordinal_by_verse:
        raise ExtractionError(
            f"Nie znaleziono wersetu {passage.book} "
            f"{normalized.end_chapter},{normalized.end_verse}."
        )

    all_verses: list[tuple[int, int, str]] = []
    for chapter in range(normalized.start_chapter, normalized.end_chapter + 1):
        verse_map = chapters[str(chapter)]
        verse_numbers = numeric_keys(verse_map, f"Wersety {passage.book} {chapter}")
        first_verse = (
            normalized.start_verse
            if chapter == normalized.start_chapter
            else verse_numbers[0]
        )
        last_verse = (
            normalized.end_verse
            if chapter == normalized.end_chapter
            else verse_numbers[-1]
        )
        for verse in range(first_verse, last_verse + 1):
            if str(verse) not in verse_map:
                raise ExtractionError(
                    f"Zakres zawiera brakujący werset {passage.book} {chapter},{verse}."
                )
            text = verse_map[str(verse)]
            if not isinstance(text, str):
                raise ExtractionError(
                    f"Tekst {passage.book} {chapter},{verse} nie jest napisem."
                )
            all_verses.append((chapter, verse, text))
    return normalized, all_verses, ordinal_by_verse


def format_bible_markdown(
    passage: Passage, verses: list[tuple[int, int, str]]
) -> str:
    lines = [f"# {passage.display_reference}", "", "*EIB, przekład dosłowny*", ""]
    show_chapters = passage.start_chapter != passage.end_chapter
    current_chapter: int | None = None
    for chapter, verse, verse_text in verses:
        if show_chapters and chapter != current_chapter:
            if current_chapter is not None:
                lines.append("")
            lines.extend([f"## Rozdział {chapter}", ""])
            current_chapter = chapter
        lines.append(f"**{verse}** {verse_text}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def alias_regex(book: str, extra_alias: str | None) -> re.Pattern[str]:
    aliases = {book, *BOOK_ALIASES.get(book, ())}
    if extra_alias:
        aliases.add(extra_alias)
    escaped = []
    for alias in sorted(aliases, key=len, reverse=True):
        escaped.append(re.escape(alias).replace(r"\ ", r"\s+"))
    names = "|".join(escaped)
    return re.compile(
        rf"(?<!\w)(?:{names})\s+"
        r"(?P<sc>\d+):(?P<sv>\d+)"
        r"(?:\s*[-–—]\s*(?:(?P<ec>\d+):)?(?P<ev>\d+))?",
        re.IGNORECASE,
    )


def locate_commentary_sections(
    path: Path,
    passage: Passage,
    ordinal_by_verse: dict[tuple[int, int], int],
    extra_alias: str | None,
) -> tuple[list[CommentarySection], list[str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    except FileNotFoundError as exc:
        raise ExtractionError(f"Nie znaleziono komentarza: {path}") from exc

    reference_re = alias_regex(passage.book, extra_alias)
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line.rstrip("\r\n"))
        if match:
            headings.append((index, len(match.group("marks")), match.group("title")))

    assert passage.start_verse is not None
    assert passage.end_verse is not None
    target_start = ordinal_by_verse[(passage.start_chapter, passage.start_verse)]
    target_end = ordinal_by_verse[(passage.end_chapter, passage.end_verse)]
    candidates: list[CommentarySection] = []

    for heading_index, (line_index, level, title) in enumerate(headings):
        for ref_match in reference_re.finditer(title):
            start = (int(ref_match.group("sc")), int(ref_match.group("sv")))
            end_chapter = (
                int(ref_match.group("ec"))
                if ref_match.group("ec")
                else start[0]
            )
            end_verse = (
                int(ref_match.group("ev"))
                if ref_match.group("ev")
                else start[1]
            )
            end = (end_chapter, end_verse)
            if start not in ordinal_by_verse or end not in ordinal_by_verse:
                continue
            section_start = ordinal_by_verse[start]
            section_end = ordinal_by_verse[end]
            if section_end < target_start or section_start > target_end:
                continue
            next_boundary = len(lines)
            for next_line, next_level, _ in headings[heading_index + 1 :]:
                if next_level <= level:
                    next_boundary = next_line
                    break
            candidates.append(
                CommentarySection(
                    start_line=line_index + 1,
                    end_line=next_boundary,
                    level=level,
                    heading=line.rstrip("\r\n"),
                    reference=ref_match.group(0),
                    span=section_end - section_start,
                    start_ordinal=section_start,
                    end_ordinal=section_end,
                )
            )

    if not candidates:
        aliases = ", ".join(sorted({passage.book, *BOOK_ALIASES.get(passage.book, ())}))
        raise ExtractionError(
            "Nie znaleziono nagłówka komentarza obejmującego cały fragment. "
            f"Sprawdzone nazwy księgi: {aliases}. "
            "W razie potrzeby użyj --commentary-alias."
        )

    containing = [
        item
        for item in candidates
        if item.start_ordinal <= target_start and item.end_ordinal >= target_end
    ]
    if containing:
        selected = min(
            containing, key=lambda item: (item.span, -item.level, item.start_line)
        )
        return [selected], lines

    selected_by_line: dict[int, CommentarySection] = {}
    for ordinal_position in range(target_start, target_end + 1):
        covering = [
            item
            for item in candidates
            if item.start_ordinal <= ordinal_position <= item.end_ordinal
        ]
        if not covering:
            verse_by_ordinal = {value: key for key, value in ordinal_by_verse.items()}
            chapter, verse = verse_by_ordinal[ordinal_position]
            raise ExtractionError(
                "Nagłówki komentarza nie obejmują wersetu "
                f"{passage.book} {chapter},{verse}."
            )
        best = min(covering, key=lambda item: (item.span, -item.level, item.start_line))
        selected_by_line[best.start_line] = best
    return sorted(selected_by_line.values(), key=lambda item: item.start_line), lines


def format_commentary_markdown(
    passage: Passage,
    sections: list[CommentarySection],
    source_lines: list[str],
) -> str:
    excerpts = [
        "".join(source_lines[item.start_line - 1 : item.end_line]).rstrip()
        for item in sections
    ]
    references = ", ".join(f"`{item.reference}`" for item in sections)
    line_ranges = ", ".join(
        f"{item.start_line}–{item.end_line}" for item in sections
    )
    preface = (
        f"# Wyciąg z Commentary.md — {passage.display_reference}\n\n"
        "> Automatycznie wydobyta najmniejsza sekcja lub zestaw sekcji komentarza "
        f"obejmujących fragment: {references} (wiersze {line_ranges} głównego "
        "`Commentary.md`). Przed użyciem w opracowaniu "
        "należy ograniczyć ją do materiału bezpośrednio związanego z fragmentem.\n\n"
    )
    return preface + "\n\n---\n\n".join(excerpts) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Wydobądź Bible.md i roboczy Commentary.md dla fragmentu 5w5."
    )
    parser.add_argument("passage", help="Np. '2Tm 2,20-26' lub '2Tm 1,15-2,7'.")
    parser.add_argument("--bible", type=Path, default=Path("Bible.json"))
    parser.add_argument("--commentary", type=Path, default=Path("Commentary.md"))
    parser.add_argument("--output-root", type=Path, default=Path("."))
    parser.add_argument(
        "--commentary-alias",
        help="Dodatkowa nazwa księgi używana w nagłówkach komentarza.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Sprawdź źródła i pokaż plan bez zapisywania plików.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Zastąp istniejące Bible.md i Commentary.md.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        requested = parse_passage(args.passage)
        bible = load_bible(args.bible)
        passage, verses, ordinal_by_verse = validate_and_collect(bible, requested)
        sections, commentary_lines = locate_commentary_sections(
            args.commentary,
            passage,
            ordinal_by_verse,
            args.commentary_alias,
        )

        destination = args.output_root / passage.book / passage.folder_reference
        bible_path = destination / "Bible.md"
        commentary_path = destination / "Commentary.md"
        print(f"Fragment: {passage.display_reference}")
        print(f"Wersety: {len(verses)}")
        print("Komentarz:")
        for section in sections:
            print(
                f"- {section.reference}, wiersze "
                f"{section.start_line}–{section.end_line}"
            )
        print(f"Katalog: {destination}")

        if args.dry_run:
            print("Tryb podglądu: nie zapisano plików.")
            return 0

        collisions = [path for path in (bible_path, commentary_path) if path.exists()]
        if collisions and not args.force:
            names = ", ".join(str(path) for path in collisions)
            raise ExtractionError(
                f"Pliki już istnieją: {names}. Przeczytaj je przed użyciem --force."
            )

        destination.mkdir(parents=True, exist_ok=True)
        bible_path.write_text(format_bible_markdown(passage, verses), encoding="utf-8")
        commentary_path.write_text(
            format_commentary_markdown(passage, sections, commentary_lines),
            encoding="utf-8",
        )
        print(f"Zapisano: {bible_path}")
        print(f"Zapisano: {commentary_path}")
        return 0
    except ExtractionError as exc:
        print(f"Błąd: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
