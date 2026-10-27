# Karta oceny — P06 · OpenAI gpt-6-astra przez Codex CLI (rozumowanie: medium), W0 bez wyszukiwania — r3

- Pytanie: P06 (katalog nr 22), klucz w wersji 3 (2026-10-10, element „rozwidlenie”)
- Data odpowiedzi systemu: 2026-10-10 · czas 58.6 s · warunki: model gpt-6-astra, wysiłek rozumowania medium, Codex CLI (sandbox read-only, pusty katalog, sesja nietrwała), aplikacje ChatGPT wyłączone (features.apps=false); narzędzia: brak, wyszukiwanie: brak (W0), liczba wyszukań 0; wstęp: „Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne. Odpowiedz bezpośrednio w wiadomości — nie twórz plików i nie uruchamiaj poleceń.”; tokeny: wejście 10521 (z pamięci podręcznej 8832), wyjście 2047, rozumowanie 1514
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 1/2 | 1: kierunek trafny dla jednej gałęzi, warunek nazwany, ale nierozstrzygnięty — pierwszy akapit: „Co do zasady – nie, jeżeli chodzi o … postanowienie sądu apelacyjnego działającego jako sąd drugiej instancji, którym odrzucono zażalenie”; na końcu dopytanie nazywające rozwidlenie („czy SA odrzucił zażalenie na postanowienie SO, czy na własne postanowienie?”); brak konkluzji dla zażalenia poziomego (zażalenie do innego składu SA, art. 394² § 1² zd. 2) — README „Dopytanie”: kierunek trafny, warunek nierozstrzygnięty = 1 |
| A2 | 0/1 | 0: brak art. 394² § 1² (art. 394² powołany ogólnie i z tezą, że nie daje środka) i brak art. 397 § 1¹ |
| A3 | n/d | system nie cytuje dosłownie |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 0/1 | [2026-10-11 A6 binarne: ½→0, A6_typ: [W], A6_pochodzenie: art. 394¹ § 2 k.p.c.: pamięć — W podtrzymane (uchylony § 2 opisany w dawnym brzmieniu jako obowiązujący), wg reguły binarnej to 0; przemilczenie art. 394² § 1² zd. 2 jest pominięciem i nie liczy się w A6; bieg W0 bez narzędzi] **A6_zakres: rdzeń** [2026-10-25 uzupełnione, do przeglądu Adama: W: uchylony art. 394¹ § 2 jako droga do SN dotyczy samego pytania o dostępny środek zaskarżenia (kara K1 klucza); niepewne, bo odpowiedź tej drogi nie przesądza („trzeba ocenić odrębnie”)] · A6_typ: [W]. Sprawdzone 3 z 3 (ISAP DU/2026/468): (1) art. 394¹ᵃ § 1 pkt 12 ✓ („odrzucenie zażalenia”; zażalenie do innego składu sądu pierwszej instancji — „dotyczy postanowień sądu pierwszej instancji” trafne); (2) art. 394² ✓ co do tożsamości (zażalenie do innego składu sądu drugiej instancji); zdanie „nie ustanawia ogólnej zaskarżalności postanowienia tego sądu o odrzuceniu zażalenia” jest literalnie prawdziwe (§ 1² zd. 2 dotyczy tylko odrzucenia zażaleń z § 1 i § 1¹), ale przemilcza § 1² zd. 2 — bez klasy, do decyzji Adama (przy kwalifikacji O punkt bez zmian: ½); (3) **art. 394¹ § 2 — W**: „Ewentualne zażalenie do Sądu Najwyższego trzeba ocenić odrębnie według art. 394¹ § 2 k.p.c.: … dopuszczalność skargi kasacyjnej …, czy postanowienie kończy postępowanie w sprawie, oraz ustawowe wyłączenia” — w t.j. DU/2026/468 „§ 2. (uchylony)”; opis odpowiada realnemu dawnemu brzmieniu (t.j. DU/2019/1460: „W sprawach, w których przysługuje skarga kasacyjna, zażalenie przysługuje także na postanowienie sądu drugiej instancji kończące postępowanie w sprawie, z wyjątkiem postanowień, o których mowa w art. 398¹, a także postanowień wydanych w wyniku rozpoznania zażalenia na postanowienie sądu pierwszej instancji”) → dawna wersja podana jako obecna. Do decyzji Adama: uchylony paragraf powołany jako obowiązująca podstawa można też czytać jako F (jednostka, której nie ma) — wtedy A6 0 i hallucinated: tak; przyjęto W, bo jednostka mieści się w numeracji, a opis zgadza się z realną dawną wersją. Orzeczeń nie powołano (SAOS: 0 sprawdzeń). Najgorszy przypadek: W → ½ |
| A8 | 1/1 | każdy akapit służy pytaniu o zaskarżalność (trzy możliwe podstawy, znaczenie braku opłaty, dopytanie); jednozdaniowe zastrzeżenie o postępowaniu karnym — neutralne |
| R1 | 1/1 | rozwidlenie: dopytanie z nazwaniem rozwidlenia ALBO obie ścieżki — ✓ strategia (a): „czego dotyczyło pierwotne zażalenie i czy SA odrzucił zażalenie na postanowienie SO, czy na własne postanowienie?” (nazwane obie konfiguracje: dewolutywna i pozioma) |
| R2 | 0/1 | dla zażalenia poziomego wskazuje zażalenie do innego składu SA — ✗ (brak; przeciwnie, art. 394² „nie ustanawia ogólnej zaskarżalności”) |
| R3 | 1/1 | dla zażalenia dewolutywnego mówi, że środek nie przysługuje — „Co do zasady – nie, jeżeli chodzi o … postanowienie sądu apelacyjnego działającego jako sąd drugiej instancji, którym odrzucono zażalenie”. Do decyzji Adama: „nie” nie jest wprost przypisane gałęzi „zażalenie na postanowienie SO” (pada dla SA jako sądu II instancji w ogóle, a gałąź nazwana dopiero w dopytaniu); przy ścisłym czytaniu 0 |
| R4 | 0/1 | zwraca uwagę na art. 130² k.p.c., jeżeli pismo wniósł profesjonalny pełnomocnik — ✗ (jest tylko „czy wymagane było wezwanie do zapłaty”; art. 130², zwrotu bez wezwania i dopłaty w tygodniu brak) |
| K1 | 0 | wskazuje zażalenie do Sądu Najwyższego — bez kary: odpowiedź nie twierdzi, że zażalenie do SN przysługuje („Ewentualne … trzeba ocenić odrębnie”, „Sam fakt wydania postanowienia przez SA nie wystarcza”). Do decyzji Adama: otwiera tę drogę jako realną na podstawie uchylonego § 2 (policzone w A6 jako W); przy uznaniu tego za „wskazanie” −1 |
| K2 | 0 | odpowiada jednoznacznie „tak” albo „nie” bez rozróżnienia i bez dopytania — nie dotyczy (jest dopytanie z nazwanym rozwidleniem) |
| **A** | **4 / 9 = 44.4 %** | punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d); bez kar [2026-10-11: było 4½ / 9 = 50.0 %, Δ −16.7; A6 ½→0] |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 1/2 | 1: prawnik wie, co ustalić (czy odrzucono zażalenie na postanowienie SO, czy na własne postanowienie SA) i że art. 394¹ᵃ nie pomoże; nie dowie się jednak, że przy zażaleniu poziomym ma zażalenie do innego składu SA (art. 394² § 1² zd. 2), a wątek SN odsyła do uchylonego przepisu |
| B2 kalibracja | 1/1 | 1 (`kalibracja_oczekiwana: warunkowa`): konkluzja „co do zasady – nie” ograniczona zastrzeżeniem i związana z warunkiem z klucza przez dopytanie („Do jednoznacznej odpowiedzi potrzebuję informacji…”); żadna gałąź nie jest podana jako pewna. Do decyzji Adama: druga gałąź nie ma konkluzji, więc „który kiedy” jest powiedziane tylko w połowie |
| **B** | **2 / 3 = 66.7 %** | |

**Δ = A % − B % = −22.3** · hallucinated: tak (A6_typ W; 2026-10-11 A6 binarne, było: nie; A6_zakres: rdzeń [2026-10-25 uzupełnione]) · bez weryfikacji źródła: tak (brak narzędzi)

## Pochodzenie (opisowe)

P1 ślady narzędzi: brak (W0: bez narzędzi i bez wyszukiwania) · P2 nie badano · P3 źródła deklarowane w tekście: k.p.c. (art. 394¹ᵃ § 1 pkt 12, art. 394², art. 394¹ § 2), bez linków · P4 wiedza z wag modelu; art. 394¹ § 2 w stanie sprzed uchylenia (brzmienie jak w t.j. DU/2019/1460). Rozwidlenie: a (dopytanie). Warunki biegu z nagłówka odpowiedzi: model gpt-6-astra, wysiłek rozumowania medium, Codex CLI, sandbox read-only (pusty katalog, sesja nietrwała), aplikacje ChatGPT wyłączone, liczba_wyszukan 0, inne_narzedzia 0, zdarzenia [], blad null; wstęp jak w metryce karty

Specyfikacja oceny: v1.0.1 (2026-10-11) — karta oceniona lub przeliczona według README w tej wersji.
