# Instrukcje dla agentów

## Cel projektu

Twórz w języku polskim krótkie opracowania fragmentów Biblii o wysokiej jakości egzegetycznej i teologicznej. Opracowanie ma dać się przeczytać w około pięć minut i ma informować, objaśniać oraz prowadzić do odpowiedzi na tekst. Nie może przyjmować formy kazania, homilii ani rozbudowanego rozważania dewocyjnego.

## Źródła prawdy

1. `Bible.json` jest źródłem tekstu biblijnego. Zawiera przekład dosłowny EIB. Cytowany tekst musi być skopiowany wiernie, bez poprawiania, uwspółcześniania ani parafrazowania.
2. `Commentary.md` jest źródłem prawdy dla egzegezy, kontekstu historyczno-literackiego, struktury i głównych wniosków teologicznych.
3. Cały tekst Biblii z `Bible.json` może służyć do sprawdzania kontekstu księgi i odwołań kanonicznych w części „Teologia biblijna”. Nie wolno jednak budować wniosków sprzecznych z analizą zawartą w `Commentary.md`.
4. Nie korzystaj z internetu ani z dodatkowych komentarzy, chyba że użytkownik wyraźnie o to poprosi. Dodatkowe źródło nigdy nie zastępuje ani nie koryguje po cichu źródeł projektu.
5. Jeżeli `Commentary.md` nie obejmuje wskazanego fragmentu albo nie zawiera danych koniecznych do rzetelnego opracowania, nie uzupełniaj luk domysłami. Wskaż użytkownikowi dokładnie, jakiego materiału brakuje.

## Schemat `Bible.json`

Tekst wersetu znajduje się pod ścieżką:

```text
.books[SKRÓT].chapters[ROZDZIAŁ][WERSET]
```

Przykład dla 2 Tm 2,20:

```text
.books["2Tm"].chapters["2"]["20"]
```

Skrót księgi zawsze ustalaj na podstawie klucza w `.books` lub pola `bsname`. Przed rozpoczęciem pracy sprawdź, czy księga, rozdział oraz wszystkie wersety wskazanego zakresu istnieją.

## Struktura katalogów i plików

Dla każdego opracowania utwórz katalog księgi, a w nim katalog fragmentu:

```text
<SKRÓT KSIĘGI>/
└── <SKRÓT KSIĘGI> <ROZDZIAŁ>,<ZAKRES>/
    ├── Bible.md
    ├── Commentary.md
    └── 5w5.md
```

Przykład:

```text
2Tm/
└── 2Tm 2,20-26/
    ├── Bible.md
    ├── Commentary.md
    └── 5w5.md
```

W nazwach katalogów używaj skrótu z `Bible.json`, przecinka między rozdziałem a wersetem oraz zwykłego łącznika `-` w zakresie wersetów. Dla zakresu między rozdziałami stosuj zapis np. `2Tm 1,15-2,7`. W nazwach plików i katalogów nigdy nie używaj dwukropka.

Nie nadpisuj bez sprawdzenia istniejącego opracowania ani ręcznych zmian użytkownika. Jeśli katalog już istnieje, najpierw przeczytaj jego zawartość i zmieniaj wyłącznie to, czego dotyczy polecenie.

## Zawartość plików źródłowych fragmentu

### `Bible.md`

- Dodaj nagłówek z pełnym odnośnikiem do fragmentu i informacją: „EIB, przekład dosłowny”.
- Umieść wszystkie wskazane wersety we właściwej kolejności.
- Wyraźnie oznacz numery wersetów.
- Zachowaj dokładne brzmienie i interpunkcję z `Bible.json`.
- Nie dodawaj komentarzy, poprawek ani objaśnień.

### `Commentary.md`

- Skopiuj z głównego `Commentary.md` materiał bezpośrednio dotyczący wskazanego fragmentu.
- Zachowaj oryginalne brzmienie, język, nagłówki i oznaczenia wersetów; jest to wyciąg źródłowy, nie streszczenie ani tłumaczenie.
- Uwzględnij potrzebny kontekst z sekcji takich jak `Form/Structure/Setting`, `Comment` i `Explanation`, ale pomiń materiał niezwiązany z fragmentem.
- Na początku podaj zakres fragmentu i zaznacz, że jest to wyciąg z głównego `Commentary.md`.
- Nie przedstawiaj pominięć jako pełnej treści komentarza. W miejscach cięć możesz użyć wyraźnego oznaczenia `[…]`.

## Obowiązkowa struktura `5w5.md`

Plik ma mieć dokładnie pięć głównych części:

Wewnątrz `5w5.md` — w tytule, strukturze i wszystkich odwołaniach biblijnych — oddzielaj rozdział od wersetu dwukropkiem, np. `2Tm 2:20`, `2Tm 2:20–26` oraz `2Tm 1:15–2:7`. Ta zasada dotyczy treści pliku, nie nazw plików ani katalogów.

```markdown
# <ODNOŚNIK> — 5w5

## 1. Kontekst

## 2. Struktura

## 3. GMF + ORPS

**GMF:** ...

**ORPS:** ...

## 4. Teologia biblijna

## 5. Zastosowanie
```

### 1. Kontekst

Umieść fragment w toku argumentacji księgi oraz w jego sytuacji historycznej i literackiej. Podaj tylko informacje potrzebne do zrozumienia badanego tekstu. Wyjaśnij, co poprzedza fragment, do czego on prowadzi i jaki problem lub potrzebę pierwotnych odbiorców podejmuje.

### 2. Struktura

Przedstaw syntetyczny podział fragmentu. Każdy element powinien zawierać zakres wersetów oraz krótkie określenie funkcji danej części w argumentacji. Nie powtarzaj całego tekstu biblijnego i nie rozbudowuj tej sekcji w komentarz werset po wersecie.

### 3. GMF + ORPS

- **GMF (główna myśl fragmentu):** jedno pełne, możliwie precyzyjne zdanie streszczające nadrzędne twierdzenie autora i funkcję fragmentu. Ma wynikać ze struktury oraz uwzględniać najważniejsze relacje logiczne tekstu.
- **ORPS (oczekiwana reakcja pierwotnego słuchacza):** jedno pełne zdanie określające, jak pierwotni adresaci mieli odpowiedzieć na przesłanie fragmentu — w przekonaniach, postawie lub działaniu.

Nie mieszaj ORPS ze współczesnym zastosowaniem. Najpierw ustal zamysł autora wobec pierwotnych odbiorców, dopiero potem przejdź do dzisiejszych czytelników.

### 4. Teologia biblijna

Pokaż, jak przesłanie fragmentu wpisuje się w rozwój i całość przesłania Biblii. Wskaż najważniejsze powiązania kanoniczne, miejsce tekstu w historii zbawienia oraz — jeśli wynika to z fragmentu i komentarza — jego związek z osobą i dziełem Chrystusa. Unikaj luźnych skojarzeń, listy odnośników bez objaśnienia oraz narzucania tekstowi obcej kategorii teologicznej.

### 5. Zastosowanie

Wyprowadź z GMF i ORPS konkretną, współczesną reakcję. Zachowaj ten sam kierunek przesłania, który tekst miał wobec pierwotnych odbiorców, uwzględniając różnice między ich sytuacją a naszą. Zastosowanie może dotyczyć przekonań, postaw i działań, ale nie może zmieniać się w apel kaznodziejski, osobiste świadectwo ani serię retorycznych pytań.

## Styl i objętość

- Pisz poprawną, naturalną i precyzyjną polszczyzną.
- Utrzymuj wysoki poziom egzegetyczny i teologiczny, lecz wyjaśniaj terminy, które nie są powszechnie zrozumiałe.
- Preferuj zwarte akapity, jasne związki logiczne i konkretne sformułowania.
- Unikaj tonu kaznodziejskiego, ozdobników, anegdot, ilustracji, modlitw, rozbudowanego wstępu i osobnego zakończenia.
- Odróżniaj to, co tekst mówi, od wniosków interpretacyjnych. Nie przedstawiaj przypuszczeń jako pewników.
- Nie powielaj obszernych cytatów z `Bible.md` ani `Commentary.md` w `5w5.md`.
- Celuj w około 650–850 słów w `5w5.md` (bez nagłówków), tak aby gęsty tekst teologiczny można było przeczytać w około pięć minut. Nie przekraczaj 900 słów bez wyraźnego polecenia użytkownika.

## Kolejność pracy

1. Znormalizuj odnośnik i potwierdź zakres w `Bible.json`.
2. Przeczytaj tekst fragmentu wraz z bezpośrednim kontekstem przed nim i po nim.
3. Znajdź w głównym `Commentary.md` sekcję obejmującą fragment i przeczytaj ją w całości, także jej omówienie struktury i podsumowanie.
4. Utwórz katalog fragmentu oraz `Bible.md`.
5. Przygotuj wierny wyciąg w lokalnym `Commentary.md`.
6. Ustal strukturę, GMF i ORPS, a następnie napisz pozostałe części `5w5.md`.
7. Przeprowadź kontrolę jakości przed zakończeniem.

## Automatyczne wydobywanie źródeł

Przy tworzeniu katalogu fragmentu użyj lokalnego skillu `extract-5w5-sources` z `.agents/skills/extract-5w5-sources/`. Najpierw uruchom skrypt w trybie `--dry-run`, a dopiero po sprawdzeniu odnośnika i dopasowanej sekcji komentarza pozwól mu zapisać `Bible.md` oraz roboczy `Commentary.md`.

Automatycznie wydobyty komentarz jest najmniejszą pełną sekcją lub zestawem sekcji oznaczonych nagłówkami, które obejmują wskazany fragment. Nie jest jeszcze gotowym wyciągiem końcowym: przeczytaj go i usuń materiał niezwiązany bezpośrednio z opracowywanymi wersetami, zgodnie z zasadami dla `Commentary.md`.

## Kontrola jakości

Przed oddaniem opracowania sprawdź:

- czy odnośnik, nazwy katalogów i zakres wersetów są zgodne;
- czy wszystkie odnośniki biblijne wewnątrz `5w5.md` używają dwukropka między rozdziałem a wersetem, a nazwy katalogów używają przecinka;
- czy w `Bible.md` nie brakuje żadnego wersetu i czy tekst jest identyczny z `Bible.json`;
- czy lokalny `Commentary.md` zawiera wyłącznie adekwatny materiał i jasno oznacza skróty;
- czy `5w5.md` ma dokładnie pięć wymaganych części;
- czy struktura opisuje tok fragmentu, a nie tylko jego tematy;
- czy GMF jest jednym zdaniem i obejmuje główny punkt całego fragmentu;
- czy ORPS dotyczy pierwotnych odbiorców, a zastosowanie odbiorców współczesnych;
- czy teologia biblijna wynika z tekstu i uwzględnia szerszy kontekst kanoniczny;
- czy żadna istotna teza egzegetyczna nie przeczy `Commentary.md` ani nie została zmyślona;
- czy tekst mieści się w zakładanym czasie lektury i nie ma charakteru kaznodziejskiego.
