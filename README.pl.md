# LawBenchmark.pl — benchmark modeli językowych w polskim prawie

Projekt **LexAlpha Lab** (KTZR, Gdańsk). Repozytorium zawiera dane, klucze oceny, karty wzorcowe, oceny sędziów-modeli i skrypty stojące za raportami LexAlpha Lab, tak aby każdy mógł sprawdzić ocenę i powtórzyć ją na własnych systemach.

[English version](README.md)

## Co tu jest

**Benchmark 02 · pytania prawne** (raport z 27 października 2026 r.): 10 krótkich pytań prawnych w postaci, w jakiej prawnik wpisuje je do czatu (literówki zachowane, sześć pytań z wbudowaną pułapką), zadanych 8 modelom trzech dostawców w dwóch warunkach — bez narzędzi (W0) i z wyszukiwaniem w internecie (W1): 160 odpowiedzi. Każde powołanie przepisu i orzeczenia sprawdzono w źródle urzędowym (ISAP, ELI, SAOS, sn.pl) na dzień stanu prawnego 1 października 2026 r.

| Katalog | Zawartość |
|---|---|
| `SPEC/` | Specyfikacja oceny v1.0.1 z rejestrem datowanych decyzji (dokument wewnętrzny, bez zmian) |
| `keys/` | Klucze 10 pytań: rdzeń, rubryka, kary, podstawy wymagane, źródła sprawdzone |
| `answers/<P>/` | 16 odpowiedzi na pytanie (8 modeli × W0/W1), tak jak zwrócił je system, ze śladem narzędzi tam, gdzie narzędzie go zapisuje |
| `cards/` | 160 kart wzorcowych: punkty A/B, klasy błędów F/T/W/S, etykieta „halucynacja”, każde powołanie sprawdzone, data wersji |
| `judges/` | Oceny pięciu sędziów-modeli (Gemini 4 Argon, GPT-6.1 Sol, Gemini 3.1 Pro, Gemini 3.8 Flash, GPT-6 Astra) i wariantów „sędzia z raportem weryfikacji” (`*meta*`) |
| `verification/` | Raporty warstwy weryfikacji: krok faktów (kod) i weryfikator poparcia (model), per karta i zbiorcze |
| `costs/` | Cennik z 18 października 2026 r. i koszt na odpowiedź (równoważnik API) |
| `reports/` | Raport Benchmark 02 (PDF, HTML, źródła Markdown, `dane.py` liczący każdą liczbę z kart) i artykuł metodologiczny v1.2 |
| `probes/` | Sondy, do których odsyła raport (P07, 24 zapytania) |
| `tools/` | Skrypty: biegi systemów, biegi sędziów, porównanie sędziów z kartami, warstwa weryfikacji |

Nazwy modeli: pliki używają nazw roboczych (`chatgpt_codex` = GPT-6.1 Sol, `codex_astra6` = GPT-6 Astra, `codex_terra56` = GPT-5.6 Terra, `opus_cli`/`sonnet_cli`/`haiku_cli` = Claude Opus/Sonnet/Haiku 5.5 przez Claude Code, `gemini38flash_vertex` = Gemini 3.8 Flash, `argon4_high_vertex` = Gemini 4 Argon; `w0` = bez narzędzi, `w1`/`web` = wyszukiwanie). Pełna tabela w aneksie D raportu. Specyfikacja w `SPEC/` odwołuje się do pierwotnego układu katalogów (`klucze/`, `odpowiedzi/`, `oceny/`) — tu odpowiadają im `keys/`, `answers/`, `cards/`.

## Jak działa ocena (w skrócie)

- **Blok A (obiektywny)**: rdzeń, podstawy wymagane, powołania; **A6** jest zero-jedynkowe: jedno twierdzenie o źródle prawa niezgodne z tekstem urzędowym (klasy: F — źródło nie istnieje, T — prawdziwe źródło z treścią, której w nim nie ma, W — brzmienie z innej daty, S — sygnatura z tezą z innej sprawy) daje A6 = 0 i etykietę „halucynacja”.
- **Blok B (ocenny)**: kalibracja, kompletność, użyteczność.
- **Poprawnie ugruntowana** = pełny rdzeń + A6 = 1 + co najmniej jedno sprawdzone powołanie.
- Karty wypełniał wstępnie model (Claude) ze sprawdzeniem każdego powołania u źródła, potem sprawdzał je jeden prawnik. Reguły doprecyzowywano w trakcie pracy; każda zmiana ma datę w `SPEC/`.

To zbiór kalibracyjny, nie ranking: 10 pytań, jedna seria, jeden prawnik. Przed cytowaniem liczb przeczytaj rozdział 8 raportu.

## Jak powtórzyć

- Tabele raportu: `python3 -I reports/benchmark-02/src/dane.py` (czyta `cards/`, `keys/`, `judges/`, `costs/`).
- Sędziowie wobec kart: `python3 -I tools/porownaj_sedziow.py`.
- Bieg systemu na pytaniach: `tools/eval_*.py` (wymaga CLI dostawcy albo dostępu do Vertex AI; repozytorium nie zawiera żadnych kluczy ani haseł).
- Warstwa weryfikacji (`tools/verification/`) potrzebuje [legal-cite-pl](https://github.com/apiotrowski-afk/legal-cite-pl) do odczytu ISAP/ELI.

Skrypty są opublikowane w postaci użytej; ścieżki zamieniono na względne, nic poza tym nie zmieniano.

## Cytowanie

Piotrowski A., Koman A. (2026). *LexAlpha Lab · Benchmark 02 · pytania prawne*. Wersja 1.0, 27 października 2026 r. — `reports/benchmark-02/`

Piotrowski A. (2026). *"Hallucination" Is Not Enough: Why Legal LLM Benchmarks Should Measure "Correctly Grounded"*. LexAlpha Lab, v1.2, 26 października 2026 r. doi:10.5281/zenodo.23674794 — `reports/paper-v1.2/`

## Licencja

Dane, klucze, karty, raporty i teksty: [CC BY 4.0](LICENSE-CC-BY-4.0.txt). Kod w `tools/` i `reports/*/src/*.py`: [MIT](LICENSE). Odpowiedzi modeli są udostępnione do celów oceny; cytowane w nich przepisy i orzeczenia są dokumentami urzędowymi (art. 4 pr.aut.).

Kontakt: Adam Piotrowski, a.piotrowski@ktzr.pl · https://lawbenchmark.pl
