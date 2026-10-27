# Karta oceny — P01 · OpenAI gpt-5.6-terra przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie na żywo — r3 W1 (rozszerzenie 2026-10-18)

- Pytanie: P01 (katalog nr 49), klucz w wersji 3 (2026-10-18, zatwierdzony; kalibracja kategoryczna; typ obliczenie, pułapka)
- Data odpowiedzi systemu: 2026-10-18 · czas 26.2 s · warunki: gpt-5.6-terra, wysiłek rozumowania medium, Codex CLI (sandbox read-only, pusty katalog, sesja nietrwała, aplikacje ChatGPT wyłączone); wstęp neutralny z `eval_codex.py` (wariant web); wyszukiwarka: web_search Codexa; liczba wyszukań: 8
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 0/2 | 0: „W 2026 r. próg wynosi **1 201,50 zł**”; „Tak, próg wzrósł wraz z płacą minimalną … ustawowy próg to jej **1/4**” — zła kwota i przytaknięcie pułapce (powiązanie z płacą minimalną) |
| A2 | 0/1 | art. 119 § 1 k.w. powołany, ale z fałszywą treścią („odwołuje się do 1/4 minimalnego wynagrodzenia”) — błędna podstawa; A2 i A6 mogą spaść za tę samą pomyłkę (reguła graniczna 3). **Do decyzji Adama** — alternatywa 1, jeżeli A2 liczyć tylko z obecności właściwej jednostki, a fałszywą treść wyłącznie w A6 (wynik A bez zmian: 2 − 2 = 0 → 0 %) |
| A3 | n/d | system nie cytuje dosłownie |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 0/1 | A6_typ: [W] · A6_zakres: rdzeń · A6_pochodzenie: pamięć (niżej) · A6_powolania: sprawdzone 6 z 6 (4 błędne, 2 zgodne). k.w. (legal-cite: t.j. DU/2023/2119, brzmienie identyczne w Dz.U. 2025 poz. 734): **art. 119 § 1 — W**, **art. 120 § 1 — W**, **art. 122 § 1 — W**, **art. 124 § 1 — W**: system twierdzi, że „w każdym z tych przypadków ustawodawca odwołuje się do 1/4 minimalnego wynagrodzenia”; obowiązujące brzmienie każdej z czterech jednostek: „nie przekracza 800 złotych”; „1/4 minimalnego wynagrodzenia” to realne dawne brzmienie (k.w. t.j. DU/2015/1094, ELI PDF, pdftotext: art. 119 § 1, 120 § 1, 122 § 1, 124 § 1 — „nie przekracza 1/4 minimalnego wynagrodzenia”; zastąpione kwotą 500 zł w 2018 r., potem 800 zł od 1.10.2023, DU/2022/2600) — przepis w brzmieniu z innej daty podany jako obowiązujący. Rozporządzenie RM z 11.09.2025, Dz.U. 2025 poz. 1242 ✓ (ELI PDF: „od dnia 1 stycznia 2026 r. … 4806 zł”). Odesłanie do k.w. t.j. Dz.U. 2025 poz. 734 jako źródła ✓ co do aktu (ISAP DocDetails, HTTP 200), ale akt ten zawiera 800 zł — błąd mieści się w W powyżej. Poza powołaniami: „w 2025 r. … 4 666 zł” ✓ (Dz.U. 2024 poz. 1362, ELI PDF). Zakres **rdzeń**: błąd dotyczy podstawy wymaganej (art. 119 § 1) i głównej konkluzji (kwota, wpływ płacy minimalnej). **Do decyzji Adama** — klasa T zamiast W, skoro system przypisuje „1/4” wprost tekstowi jednolitemu z 2025 r., który podaje jako źródło (bez wpływu na punkt i etykietę). Orzeczeń nie powołano |
| A8 | 1/1 | każdy akapit służy odpowiedzi (kwota, płaca minimalna, podstawa, granica wykroczenie/przestępstwo); błąd płaci w A-R, A6 i K, nie w ramach (przykład graniczny A8 nr 2) |
| R1 | 0/1 | kwota 800 zł — ✗ („1 201,50 zł”) |
| R2 | 0/1 | płaca minimalna nie wpływa — ✗, odwrotnie: „próg wzrósł wraz z płacą minimalną” |
| R3 | 0/1 | kwota stała od 1.10.2023 albo wcześniej 500 zł — ✗ |
| R4 | 0/1 | ten sam próg 800 zł przy art. 120 § 1, 122 § 1, 124 § 1 — system wymienia wszystkie trzy przepisy jako objęte tym samym progiem, ale progiem „1/4 minimalnego wynagrodzenia”, nie 800 zł; element wymaga kwoty 800 zł — ✗ |
| K1 | −1 | wiąże próg z płacą minimalną jako stan obecny — „ustawowy próg to jej 1/4” |
| K2 | −1 | podaje inną kwotę jako obowiązującą — „1 201,50 zł” |
| **A** | **0 / 9 = 0.0 %** | punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d); punkty 1 (A8) − kary 2 (K1, K2) = −1 → 0 (wynik nie spada poniżej 0) |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 0/2 | 0: prawnik dostaje złą kwotę (1 201,50 zł zamiast 800 zł) i fałszywy mechanizm ustalania progu; czyny o wartości 800,01–1 201,50 zł zakwalifikowałby jako wykroczenia zamiast przestępstw — błąd zmienia działanie (kwalifikacja czynu, właściwy tryb) |
| B2 kalibracja | 1/1 | 1 (`kategoryczna`): teza wprost w pierwszym zdaniu; błędna, ale pewna odpowiedź przy `kategoryczna` ma B2 = 1 (błąd płaci w bloku A) |
| **B** | **1 / 3 = 33.3 %** | |

**Δ = A % − B % = −33.3** · hallucinated: tak (W, rdzeń) · bez weryfikacji źródła: nie — ślad web_search z zapytaniem site:isap.sejm.gov.pl i linki w odpowiedzi do ISAP (rozporządzenie Dz.U. 2025 poz. 1242, k.w. t.j. Dz.U. 2025 poz. 734)

## Pochodzenie (opisowe)

P1 ślady narzędzi: 8 zdarzeń web_search (5 z pustym zapytaniem); zapytania: „site:isap.sejm.gov.pl rozporządzenie minimalne wynagrodzenie za pracę 2026 4806 …”, „Kodeks wykroczeń art. 119 § 1 jedna czwarta minimalnego wynagrodzenia tekst jednolity ISAP …”, pobranie api.sejm.gov.pl/eli/acts/DU/2025/734/text.html · P2 nie badano · P3 źródła deklarowane w tekście: isap.sejm.gov.pl WDU20250001242 (rozporządzenie o płacy minimalnej na 2026, HTTP 200), isap.sejm.gov.pl DocDetails WDU20250000734 (k.w. t.j., HTTP 200) · P4 źródła urzędowe (ISAP/ELI). **A6_pochodzenie: pamięć** — zapytanie z 1/4 minimalnego wynagrodzenia padło, zanim system otworzył tekst k.w.; pobrany adres api.sejm.gov.pl/eli/acts/DU/2025/734/text.html przy sprawdzeniu 2026-10-18 zwraca HTTP 200 z pustą treścią (0 bajtów; t.j. 2025/734 jest dostępny tylko w PDF), więc ślad nie pokazuje, że system przeczytał brzmienie art. 119; kwota płacy minimalnej pochodzi z odczytu rozporządzenia, ale mechanizm 1/4 z wag modelu. **Do decyzji Adama** — alternatywa `odczyt_źródła`, jeżeli samo otwarcie właściwego aktu w ELI (i link do ISAP w odpowiedzi) wystarcza, bez względu na to, czy strona zwróciła treść. Porównanie z W0 tego samego modelu (`P01_codex_terra56_w0_r3`): bez narzędzi system podał 800 zł (A 77.8 %, W poboczne w historii progu); z wyszukiwaniem — 1/4 płacy minimalnej i 1 201,50 zł. Wyszukiwanie pogorszyło odpowiedź: system szukał potwierdzenia błędnej przesłanki pytania (płaca minimalna), znalazł kwotę płacy minimalnej i dopisał do niej dawne brzmienie k.w.

Specyfikacja oceny: v1.0.1 (2026-10-11) z przykładami granicznymi z 2026-10-17 oraz zasadami soft law i A6_zakres z 2026-10-18 — karta wypełniona wstępnie 2026-10-18.
