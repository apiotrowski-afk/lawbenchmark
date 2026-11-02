# LawBenchmark.pl — benchmark modeli językowych w polskim prawie

Projekt **LexAlpha Lab** (KTZR, Gdańsk). Repozytorium zawiera dane, klucze oceny, karty wzorcowe, oceny sędziów-modeli i skrypty stojące za raportami LexAlpha Lab, tak aby każdy mógł sprawdzić ocenę i powtórzyć ją na własnych systemach. [English version](README.md).

- **Raport** *Benchmark 02 · pytania prawne* (PDF): [reports/benchmark-02/lexalpha_lab_benchmark_02.pdf](reports/benchmark-02/lexalpha_lab_benchmark_02.pdf) · strona: https://lawbenchmark.pl
- **Zbiór danych** (JSONL, to samo co `data/`): https://huggingface.co/datasets/LexAlphaLab/lawbenchmark-b02
- **Artykuł metodologiczny** *"Hallucination" Is Not Enough* (po angielsku): doi:10.5281/zenodo.23674794 · [PDF](reports/paper-v1.2/Piotrowski_2026_correctly_grounded_v1.2.pdf)
- **Wersje** (tag repo ↔ raport ↔ rewizja zbioru ↔ DOI): [CHANGELOG.md](CHANGELOG.md) · cytowanie: [CITATION.cff](CITATION.cff)

## Co zmierzono

**Benchmark 02 · pytania prawne** (raport z 27 października 2026 r., v1.1 z 29 października): 10 krótkich pytań prawnych w postaci, w jakiej prawnik wpisuje je do czatu (literówki zachowane, sześć pytań z wbudowaną pułapką), zadanych 8 modelom trzech dostawców w dwóch warunkach — bez narzędzi (W0) i z wyszukiwaniem w internecie (W1): 160 odpowiedzi. Każde powołanie przepisu i orzeczenia sprawdzono w źródle urzędowym (ISAP, ELI, SAOS, sn.pl) na dzień stanu prawnego 1 października 2026 r. Te same odpowiedzi oceniło pięciu sędziów-modeli; na ośmiu pytaniach przetestowano warstwę weryfikacji (krok faktów w kodzie, weryfikator poparcia w modelu).

To zbiór kalibracyjny, nie ranking: 10 pytań, jedna seria, jeden prawnik. Przed cytowaniem liczb przeczytaj rozdział 8 raportu.

## Jak odtworzyć liczby

```bash
python3 -I reports/benchmark-02/src/dane.py   # każda liczba raportu → reports/benchmark-02/src/dane.json
git diff --stat reports/benchmark-02/src/dane.json   # pusto = identyczne z opublikowanym zrzutem
python3 -I tools/export_jsonl.py              # odbudowuje data/*.jsonl i sprawdza sumy z dane.py
python3 -I tools/porownaj_sedziow.py argon4v101   # jeden bieg sędziego wobec kart (κ, macierz pomyłek)
```

Wystarczy Python 3 z PyYAML. PDF raportu: `reports/benchmark-02/src/build.py` (WeasyPrint). Nowy bieg systemu albo sędziego: `tools/eval_*.py` (CLI dostawcy albo dostęp do Vertex AI; repozytorium nie zawiera żadnych kluczy ani haseł). Warstwa weryfikacji (`tools/verification/`) potrzebuje [legal-cite-pl](https://github.com/apiotrowski-afk/legal-cite-pl).

## Jak płyną dane

```
keys/ + answers/  ──►  cards/ (prawnik)    ─┐
                  ──►  judges/ (5 modeli)   ├──►  tools/export_jsonl.py  ──►  data/*.jsonl  (= Hugging Face)
                  ──►  verification/        ┘
cards/ + keys/ + judges/ + costs/ + verification/runs/  ──►  dane.py  ──►  dane.json  ──►  build.py  ──►  raport PDF
```

| Katalog | Zawartość |
|---|---|
| `SPEC/` | Specyfikacja oceny v1.0.4 z rejestrem datowanych decyzji (zasady punktacji bez zmian od 1.0.1, którą podają karty; w postaci użytej) i pusty szablon karty |
| `keys/` | Klucze 10 pytań: rdzeń, rubryka, kary, podstawy wymagane, źródła sprawdzone |
| `answers/<P>/` | 16 odpowiedzi na pytanie (8 modeli × W0/W1), tak jak zwrócił je system, ze śladem narzędzi tam, gdzie narzędzie go zapisuje |
| `cards/` | 160 kart wzorcowych: punkty A/B, klasy błędów F/T/W/S, etykieta „halucynacja”, każde powołanie sprawdzone |
| `judges/` | 1 319 ocen pięciu sędziów-modeli w 12 biegach, w tym warianty „sędzia z raportem weryfikacji” — indeks: [judges/README.md](judges/README.md) |
| `verification/` | `reports/` 320 raportów kroku faktów (po jednym na odpowiedź); `runs/` 15 biegów zbiorczych warstwy — przewodnik: [verification/README.md](verification/README.md) |
| `costs/` | Cennik z 18 października 2026 r., koszt na odpowiedź (równoważnik API), `koszt.py` |
| `reports/` | Raport Benchmark 02 (PDF, źródła Markdown, `dane.py`, `dane.json`) i artykuł metodologiczny v1.2 |
| `probes/` | Sonda, do której odsyła raport (P07, 24 zapytania) |
| `cases/skd-01/` | **Benchmark 01** (pilotaż, fikcyjny kazus o terminie zawitym sankcji kredytu darmowego): kazus, klucz, metryki, 17 odpowiedzi z kartami ocenionymi ręcznie; poza zbiorem 160 odpowiedzi |
| `data/` | Warstwa maszynowa: sześć plików JSONL z kartą zbioru — [data/README.md](data/README.md) |
| `tools/` | Skrypty: biegi systemów i sędziów, porównanie sędziów z kartami, warstwa weryfikacji, eksport JSONL |

Nazwy modeli: pliki używają nazw roboczych (`chatgpt_codex` = GPT-6.1 Sol, `codex_astra6` = GPT-6 Astra, `codex_terra56` = GPT-5.6 Terra, `opus_cli`/`sonnet_cli`/`haiku_cli` = Claude Opus/Sonnet/Haiku 5.5 przez Claude Code, `gemini38flash_vertex` = Gemini 3.8 Flash, `argon4_high_vertex` = Gemini 4 Argon; `w0` = bez narzędzi, `w1`/`web` = wyszukiwanie). Pełna tabela w aneksie D raportu. Specyfikacja w `SPEC/` odwołuje się do pierwotnego układu katalogów (`klucze/`, `odpowiedzi/`, `oceny/`) — tu odpowiadają im `keys/`, `answers/`, `cards/`.

Każdy klucz, karta, odpowiedź, ocena sędziego, raport warstwy i rekord JSONL zawiera ciąg kanaryjski z [CANARY.txt](CANARY.txt) (konwencja BIG-bench): **ten benchmark nie jest danymi treningowymi.** Pozostałe 40 pytań puli pozostaje nieopublikowane, by ograniczyć kontaminację.

## Jak działa ocena (w skrócie)

- **Blok A (obiektywny)**: rdzeń, podstawy wymagane, powołania; **A6** jest zero-jedynkowe: jedno twierdzenie o źródle prawa niezgodne z tekstem urzędowym (klasy: F — źródło nie istnieje, T — prawdziwe źródło z treścią, której w nim nie ma, W — brzmienie z innej daty, S — prawdziwe źródło z przekręconym identyfikatorem: numer, data, sąd, publikator, nazwa aktu) daje A6 = 0 i etykietę „halucynacja”.
- **Blok B (ocenny)**: kalibracja, kompletność, użyteczność.
- **Poprawnie ugruntowana** = pełny rdzeń + A6 = 1 + co najmniej jedno sprawdzone powołanie.
- Karty wypełniał wstępnie model (Claude) ze sprawdzeniem każdego powołania u źródła, potem sprawdzał je jeden prawnik. Reguły doprecyzowywano w trakcie pracy; każda zmiana ma datę w `SPEC/`.

Skrypty są opublikowane w postaci użytej, ze ścieżkami dostosowanymi do układu tego repozytorium (1.0.2); komentarze i logi po polsku.

## Cytowanie

Piotrowski A., Koman A. (2026). *LexAlpha Lab · Benchmark 02 · pytania prawne*. Wersja 1.1, 29 października 2026 r. — `reports/benchmark-02/`

Piotrowski A. (2026). *"Hallucination" Is Not Enough: Why Legal LLM Benchmarks Should Measure "Correctly Grounded"*. LexAlpha Lab, v1.2, 26 października 2026 r. doi:10.5281/zenodo.23674794 — `reports/paper-v1.2/`

## Licencja

- **Materiał własny** — specyfikacja oceny, pytania w brzmieniu benchmarkowym, klucze, karty wzorcowe, instrukcje dla sędziów, raporty warstwy weryfikacji, raporty i wszystkie teksty w tym repozytorium: [CC BY 4.0](LICENSE-CC-BY-4.0.txt). Oznaczenie autorstwa: „LexAlpha Lab, LawBenchmark.pl”.
- **Kod** (`tools/`, `reports/*/src/*.py`, `costs/koszt.py`): [MIT](LICENSE).
- **Odpowiedzi modeli** (`answers/`, `cases/skd-01/answers/`, `probes/`, `data/answers.jsonl` oraz cytaty w kartach i ocenach sędziów) to wyniki systemów osób trzecich, przytoczone dosłownie w celu oceny, krytyki i badań. Nie rościmy sobie do nich praw ani ich nie relicencjonujemy; korzystanie z samych modeli regulują warunki ich dostawców.
- **Przepisy i orzeczenia** cytowane w odpowiedziach i kluczach to dokumenty urzędowe, niechronione prawem autorskim (art. 4 pr.aut.).
- Ciąg kanaryjski w [CANARY.txt](CANARY.txt) to metodologiczna prośba o nieużywanie tych plików do treningu, żeby kolejne pomiary pozostały miarodajne; sama licencja CC BY 4.0 takiego użycia nie zakazuje.

Kontakt: Adam Piotrowski, a.piotrowski@ktzr.pl · https://lawbenchmark.pl
