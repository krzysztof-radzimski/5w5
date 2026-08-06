---
name: extract-5w5-sources
description: Wydobywa i waliduje tekst wskazanego fragmentu z projektowego Bible.json oraz odnajduje najmniejszą sekcję lub zestaw sekcji głównego Commentary.md obejmujących ten fragment. Używaj przy tworzeniu lub odtwarzaniu katalogu źródłowego opracowania 5w5, generowaniu Bible.md, przygotowywaniu lokalnego Commentary.md albo sprawdzaniu poprawności odnośnika biblijnego.
---

# Wydobywanie źródeł 5w5

## Procedura

1. Pracuj z katalogu głównego repozytorium zawierającego `Bible.json` i `Commentary.md`.
2. Uruchom najpierw podgląd:

   ```bash
   python3 .agents/skills/extract-5w5-sources/scripts/extract_sources.py "2Tm 2,20-26" --dry-run
   ```

3. Sprawdź znormalizowany odnośnik, liczbę wersetów i wskazaną sekcję komentarza.
4. Jeśli dopasowanie jest poprawne, wygeneruj pliki:

   ```bash
   python3 .agents/skills/extract-5w5-sources/scripts/extract_sources.py "2Tm 2,20-26"
   ```

5. Przeczytaj wygenerowane pliki i porównaj `Bible.md` z zakresem w `Bible.json`.
6. Potraktuj lokalny `Commentary.md` jako wyciąg roboczy. Skróć go do materiału bezpośrednio dotyczącego fragmentu, zachowując oryginalne brzmienie, nagłówki i oznaczenia `[…]` w miejscach cięć.
7. Dopiero po kontroli źródeł przygotuj `5w5.md` zgodnie z głównym `AGENTS.md`.

## Zachowanie skryptu

Skrypt `scripts/extract_sources.py`:

- przyjmuje zapis z przecinkiem lub dwukropkiem, np. `2Tm 2,20-26` albo `2Tm 2:20-26`;
- obsługuje pojedynczy werset, cały rozdział i zakres między rozdziałami;
- sprawdza księgę, rozdziały i każdy werset w `Bible.json`;
- sortuje rozdziały i wersety numerycznie, niezależnie od kolejności kluczy JSON;
- tworzy katalog `<KSIĘGA>/<FRAGMENT>/` oraz `Bible.md` i `Commentary.md`;
- wybiera najmniejszy nagłówek Markdown w głównym komentarzu, którego zakres obejmuje cały fragment, albo najmniejszy zestaw sekcji, gdy fragment przekracza ich granicę;
- nie tworzy `5w5.md` i nie interpretuje komentarza;
- odmawia nadpisania istniejących plików bez opcji `--force`.

Użyj `--commentary-alias`, jeśli komentarz stosuje nazwę księgi, której skrypt nie rozpoznaje automatycznie:

```bash
python3 .agents/skills/extract-5w5-sources/scripts/extract_sources.py \
  "2Tm 2,20-26" --commentary-alias "2 Tim"
```

Użyj `--output-root`, aby przeprowadzić bezpieczny test poza docelowym katalogiem. Użyj `--force` wyłącznie po przeczytaniu istniejących plików i potwierdzeniu, że mają zostać zastąpione.

## Granice automatyzacji

Automatyczne dopasowanie działa na zakresach zapisanych w nagłówkach `Commentary.md`. Wydobyta sekcja lub sekcje mogą obejmować więcej wersetów niż żądany fragment, gdy komentarz omawia je wspólnie. Nie uznawaj całego automatycznie wydobytego materiału za gotowy wyciąg końcowy: dokonaj ręcznej selekcji zgodnie z `AGENTS.md`.

Jeśli nie znaleziono sekcji obejmującej fragment, nie zgaduj i nie wybieraj sekcji tylko na podstawie podobnych słów. Sprawdź alias księgi i nagłówki komentarza. Jeśli odpowiedniego materiału rzeczywiście brakuje, zgłoś użytkownikowi konieczność uzupełnienia głównego `Commentary.md`.
