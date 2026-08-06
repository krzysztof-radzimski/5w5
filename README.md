<p align="center">
  <img src="assets/logo.svg" alt="Logo 5w5" width="160">
</p>

# 5w5

**Pięć najważniejszych punktów o fragmencie Biblii — do przeczytania w pięć minut.**

## Cel projektu

5w5 służy do tworzenia zwięzłych, polskojęzycznych opracowań fragmentów Biblii na wysokim poziomie egzegetycznym i teologicznym. Każde opracowanie pomaga uchwycić sens tekstu w jego pierwotnym kontekście, umieścić go w szerszym przesłaniu Biblii i wyprowadzić uzasadnione zastosowanie dla współczesnego czytelnika.

Opracowania nie są kazaniami ani rozważaniami dewocyjnymi. Mają realizować pięć ściśle określonych zadań:

1. **Kontekst** — umiejscowić fragment w sytuacji historycznej, literackiej i w toku argumentacji księgi.
2. **Struktura** — syntetycznie pokazać budowę i rozwój myśli fragmentu.
3. **GFM + ORPS** — sformułować główną myśl fragmentu oraz oczekiwaną reakcję pierwotnego słuchacza.
4. **Teologia biblijna** — wyjaśnić, jak fragment wpisuje się w szerszy kontekst i przesłanie Biblii.
5. **Zastosowanie** — wskazać, jak na przesłanie fragmentu powinni odpowiedzieć ludzie żyjący współcześnie.

Wynikowy tekst `5w5.md` ma być na tyle zwięzły, by można go było przeczytać w około pięć minut.

## Źródła

- [`Bible.json`](Bible.json) zawiera cały tekst Biblii w przekładzie dosłownym EIB. Jest źródłem dokładnego brzmienia fragmentu.
- [`Commentary.md`](Commentary.md) zawiera komentarz egzegetyczny i jest źródłem prawdy dla interpretacji. Plik będzie uzupełniany w miarę opracowywania kolejnych fragmentów.
- [`AGENTS.md`](AGENTS.md) opisuje szczegółowy sposób przygotowywania opracowań, wymagany format oraz kryteria jakości.

Jeżeli komentarz nie obejmuje wybranego tekstu w stopniu wystarczającym do rzetelnej pracy, materiał źródłowy powinien zostać najpierw uzupełniony. Braków nie należy zastępować domysłami.

## Struktura opracowania

Każdy fragment otrzymuje osobny katalog wewnątrz katalogu księgi. Skróty ksiąg pochodzą z `Bible.json`.

```text
2Tm/
└── 2Tm 2,20-26/
    ├── Bible.md
    ├── Commentary.md
    └── 5w5.md
```

- `Bible.md` — dokładny tekst wskazanego fragmentu z numerami wersetów;
- `Commentary.md` — adekwatny wyciąg ze źródłowego komentarza;
- `5w5.md` — właściwe opracowanie w pięciu częściach.

## Format pliku `5w5.md`

```markdown
# 2Tm 2,20–26 — 5w5

## 1. Kontekst

## 2. Struktura

## 3. GFM + ORPS

**GFM:** Główna myśl fragmentu w jednym zdaniu.

**ORPS:** Oczekiwana reakcja pierwotnego słuchacza w jednym zdaniu.

## 4. Teologia biblijna

## 5. Zastosowanie
```

**GFM** opisuje nadrzędne twierdzenie autora i funkcję badanego tekstu. **ORPS** określa odpowiedź, której autor oczekiwał od pierwszych adresatów. Dopiero część „Zastosowanie” przenosi ten kierunek odpowiedzi do sytuacji współczesnego czytelnika.

## Sposób użycia

Wskaż fragment, dla którego ma powstać opracowanie, na przykład:

```text
Przygotuj 5w5 dla 2Tm 2,20-26.
```

Przed napisaniem opracowania należy sprawdzić zakres wersetów w `Bible.json` i upewnić się, że `Commentary.md` zawiera odpowiadający mu materiał. Szczegółowy przebieg pracy i lista kontroli końcowej znajdują się w [`AGENTS.md`](AGENTS.md).

## Automatyczne wydobywanie źródeł

Repozytorium zawiera lokalny skill [`extract-5w5-sources`](.agents/skills/extract-5w5-sources/SKILL.md). Waliduje on odnośnik, pobiera wersety w prawidłowej kolejności i odnajduje najmniejszą sekcję lub zestaw sekcji komentarza obejmujących cały fragment.

Podgląd bez zapisywania plików:

```text
python3 .agents/skills/extract-5w5-sources/scripts/extract_sources.py "2Tm 2,20-26" --dry-run
```

Utworzenie `Bible.md` i roboczego `Commentary.md`:

```text
python3 .agents/skills/extract-5w5-sources/scripts/extract_sources.py "2Tm 2,20-26"
```

Roboczy wyciąg komentarza należy następnie ograniczyć do materiału bezpośrednio dotyczącego wskazanych wersetów. Skrypt celowo nie nadpisuje istniejących plików bez jawnej opcji `--force`.

## Standard jakości

Gotowe opracowanie powinno być:

- wierne tekstowi EIB i źródłowemu komentarzowi;
- zakorzenione w kontekście historycznym, literackim i kanonicznym;
- precyzyjne w oddzieleniu pierwotnego znaczenia od współczesnego zastosowania;
- zwarte, zrozumiałe i wolne od niepotrzebnego żargonu;
- analityczne i duszpastersko odpowiedzialne, ale nie kaznodziejskie;
- możliwe do przeczytania w około pięć minut.
