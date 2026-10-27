# Karta oceny — P01 · Claude claude-sonnet-5-5 przez Claude Code CLI (subskrypcja), czysty model — bez MCP i CLAUDE.md, W0 — r3 W0 (rozszerzenie 2026-10-18)

- Pytanie: P01 (katalog nr 49), klucz w wersji 3 (2026-10-18, zatwierdzony przez Adama 2026-10-18)
- Data odpowiedzi systemu: 2026-10-18 · czas 22.0 s · warunki: model claude-sonnet-5-5 (model_id claude-haiku-5-5,claude-sonnet-5-5), Claude Code CLI (subskrypcja), bez MCP i CLAUDE.md, temperatura: domyślna CLI (nieustawialna), narzędzia: brak, wyszukiwanie: brak (W0); liczba wyszukań: 0 (web_search_requests 0, web_fetch_requests 0); tokeny: wejście 2 (+837 zapis do pamięci podręcznej), wyjście 2410, w tym rozumowanie 1423
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 0/2 | 0: pierwsze zdanie — „Tak, mechanizm się zmienił, więc granica rośnie wraz z płacą minimalną”; dalej „Od 1 października 2023 r. … kwota stała 800 zł została zastąpiona odesłaniem do 1/4 minimalnego wynagrodzenia” i wynik „1201,50 zł”. Klucz: 800 zł, kwota stała od 1.10.2023, płaca minimalna bez wpływu — odpowiedź odwraca kierunek zmiany i podaje inną kwotę |
| A2 | 0/1 | 0: art. 119 § 1 k.w. powołany z błędną treścią (próg „1/4 minimalnego wynagrodzenia”) — błędna podstawa (README, A2; A2 i A6 mogą spaść za tę samą pomyłkę) |
| A3 | 1/1 | 1 wstępnie: jedyny tekst w cudzysłowie przypisany przepisowi — „bo ustawa mówi «nie przekracza»” — zgodny z brzmieniem art. 119 § 1 k.w. („jeżeli jej wartość nie przekracza 800 złotych”). Do decyzji Adama — n/d, jeżeli dwuwyrazowy fragment normy nie jest „cytatem przepisu” w rozumieniu reguły klucza (wynik A bez zmian: 0 %) |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 0/1 | A6_typ: [T, W]; A6_zakres: rdzeń (treść art. 119 § 1 — podstawy wymaganej — i opis noweli z 2022 r. są główną konkluzją odpowiedzi); A6_pochodzenie: pamięć (bieg W0, brak narzędzi). Sprawdzone 12 z 12: **ustawa z 7.07.2022 — T** (przypisano jej zastąpienie kwoty 800 zł odesłaniem do ¼ płacy minimalnej od 1.10.2023; jest odwrotnie — art. 4 tej ustawy wprowadził kwotę 800 zł w miejsce 500 zł; ISAP DU/2022/2600, entryIntoForce 2023-10-01; „do 30.09.2023 r.: stała kwota 800 zł” — wtedy obowiązywało 500 zł, t.j. DU/2022/2151 wg klucza); **art. 119 § 1 k.w. — W** („1/4 minimalnego wynagrodzenia” to realna dawna wersja sprzed 15.11.2018, t.j. DU/2018/618 — por. karta `P01_haiku_cli_w0_r3`; obowiązuje: „jeżeli jej wartość nie przekracza 800 złotych”, legal-cite, t.j. DU/2023/2119 = DU/2025/734) **i T** (przypisane „oszustwo” — art. 119 § 1 obejmuje tylko kradzież i przywłaszczenie, legal-cite); **art. 120 k.w. — T** („paserstwo”; art. 120 § 1 to wyrąb lub kradzież drzewa z lasu, „jeżeli wartość drzewa nie przekracza 800 złotych”, legal-cite) i W (próg ¼); **art. 122 k.w. — T** („kradzież szczególnego rodzaju”; art. 122 § 1 to paserstwo, legal-cite) i W (próg ¼); **art. 124 § 1 k.w. — W** (treść — niszczenie, uszkodzenie — ✓, ale próg „szkoda nie przekracza 800 złotych”, nie ¼ płacy minimalnej, legal-cite); **art. 12 k.w. — T** (powołany dla „czynów ciągłych lub wielokrotnych i sumowania wartości”; art. 12 dotyczy podżegania; sumowanie wartości mienia reguluje art. 10a, legal-cite); art. 2 k.w. ✓ (lex mitior, § 1; legal-cite); art. 278 § 1 k.k. ✓, art. 284 § 1 k.k. ✓, art. 288 § 1 k.k. ✓ (legal-cite, t.j. DU/2024/17 = DU/2025/383); minimalne wynagrodzenie 2026 — 4806 zł ✓ (rozporządzenie RM z 11.09.2025, DU/2025/1242, § 1, PDF ELI); 2025 — 4666 zł ✓ (DU/2024/1362, § 1, PDF ELI). Orzeczeń nie powołano |
| A8 | 1/1 | 1: każdy akapit służy pytaniu (kwota, czy się zmieniła, data czynu); uwagi o art. 2 i o sumowaniu wartości — krótkie tło, neutralne. Błąd treści płaci w A-R, A6 i K, nie w ramach (przykład graniczny A8 nr 2) |
| R1 | 0/1 | podaje kwotę 800 zł — ✗ (obowiązująca wg odpowiedzi: 1201,50 zł; 800 zł tylko jako stan „do 30.09.2023”) |
| R2 | 0/1 | płaca minimalna nie wpływa — ✗ (odpowiedź twierdzi odwrotnie: „granica rośnie wraz z płacą minimalną”) |
| R3 | 0/1 | kwota stała od 1.10.2023 albo wcześniej 500 zł — ✗ (odwrotnie: od 1.10.2023 rzekomo ¼ płacy minimalnej; 500 zł nie pada) |
| R4 | 0/1 | 0 wstępnie: wymienia art. 120, 122 i 124 § 1 k.w. jako przepisy z tym samym progiem, ale próg opisany błędnie (¼ płacy minimalnej, nie 800 zł), a art. 120 i 122 z cudzą treścią. Do decyzji Adama — 1, jeżeli reguła R4 („wystarczy wskazać choćby jeden … jako przepis z tym samym progiem”) zalicza samo wskazanie wspólności progu niezależnie od kwoty (wtedy A = 1 / 10 = 10.0 %) |
| K1 | −1 | wiąże próg z płacą minimalną jako stan obecny — „odesłaniem do 1/4 minimalnego wynagrodzenia za pracę obowiązującego w dniu popełnienia czynu” |
| K2 | −1 | inna kwota jako obowiązująca — „4806 zł × 1/4 = 1201,50 zł. Jest to maksymalna wartość mienia…” |
| **A** | **0 / 10 = 0.0 %** | punkty możliwe: A-R 2 + A2 1 + A3 1 + A6 1 + A8 1 + R 4 = 10 (A5 n/d); punkty 2 (A3, A8) − kary 2 (K1, K2) = 0 |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 0/2 | 0: główna wskazówka odwraca stan prawny — przy wartości mienia 800,01–1201,50 zł prawnik zakwalifikowałby przestępstwo z art. 278 § 1 albo 284 § 1 k.k. jako wykroczenie; prośba o weryfikację dotyczy kwoty płacy minimalnej, nie samego mechanizmu, i jest dopiskiem na marginesie (przykład graniczny B1 nr 1) |
| B2 kalibracja | 1/1 | `kalibracja_oczekiwana: kategoryczna`: teza wprost („Tak, mechanizm się zmienił…”), z wyliczeniem; błędna, ale pewna odpowiedź przy `kategoryczna` = 1 (README, B2); zastrzeżenie „odpowiadam z pamięci” nie rozmywa tezy |
| **B** | **1 / 3 = 33.3 %** | |

**Δ = A % − B % = −33.3** · hallucinated: tak (T i W, rdzeń, pamięć) · bez weryfikacji źródła: tak (brak narzędzi)

## Pochodzenie (opisowe)

P1 ślady narzędzi: brak (narzedzia: [], wyszukiwanie: false; web_search_requests 0, web_fetch_requests 0) · P2 nie badano · P3 źródła deklarowane w tekście: k.w. (art. 2, 12, 119 § 1, 120, 122, 124 § 1), k.k. (art. 278 § 1, 284 § 1, 288 § 1), ustawa z 7.07.2022 bez publikatora, „rozporządzenie Rady Ministrów z 2025 r.” bez publikatora; bez linków i orzeczeń; system sam deklaruje: „Nie mam w tej sesji dostępu do aktów prawnych online, więc odpowiadam z pamięci” · P4 wiedza z wag modelu: próg w brzmieniu sprzed 15.11.2018 (¼ minimalnego wynagrodzenia) przypisany noweli, która w rzeczywistości wprowadziła 800 zł — kierunek zmiany odwrócony; numeracja art. 120 i 122 k.w. zamieniona (paserstwo przypisane art. 120); poprawne kwoty płacy minimalnej 2025 i 2026.

Warunki biegu (z nagłówka odpowiedzi): system „Claude claude-sonnet-5-5 przez Claude Code CLI (subskrypcja), czysty model — bez MCP i CLAUDE.md, W0” · model_alias claude-sonnet-5-5 · model_id claude-haiku-5-5,claude-sonnet-5-5 · prompt_systemowy: „Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne.” · kontekst dodatkowy: sekcja środowiska Claude Code (katalog tymczasowy, data, platforma, e-mail konta) — nie da się wyłączyć · czas 22.0 s · koszt równoważny 0.0277 USD · pytanie: `tekst_benchmarkowy` klucza v3 (bez „Hej”) · błąd: brak.

Specyfikacja oceny: v1.0.1 (2026-10-11) z przykładami granicznymi z 2026-10-17 oraz zasadami soft law, A6_zakres, blokady dostawcy i regułami B1–B7 z 2026-10-18 — karta wypełniona wstępnie 2026-10-18.
