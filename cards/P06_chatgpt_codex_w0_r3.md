# Karta oceny — P06 · OpenAI gpt-6.1-sol przez Codex CLI (rozumowanie: medium), W0 bez wyszukiwania — powtórzenie r3

- Pytanie: P06 (katalog nr 22), klucz w wersji 3 (2026-10-10, element „rozwidlenie”)
- Data odpowiedzi systemu: 2026-10-10 · czas 63.4 s · warunki: gpt-6.1-sol, wysiłek rozumowania medium, Codex CLI (sandbox read-only, pusty katalog, sesja nietrwała); wyszukiwarka: brak (W0); liczba wyszukań: 0
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 1/2 | [2026-10-11 przykład graniczny A-R: 0→1 — konkluzja „tak, zażalenie do innego składu SA (poziome)” bez rozróżnienia jest trafna dla gałęzi poziomej klucza; brak rozróżnienia płaci w R1, K i B2 (karta wzorcowa przykładu 2)] 0: pierwszy akapit daje jedną gałąź jako zasadę — „Tak — … co do zasady przysługuje zażalenie do innego składu tego samego sądu apelacyjnego (tzw. zażalenie poziome)”; zależność od rodzaju odrzuconego zażalenia zasygnalizowana dopiero w przedostatnim akapicie („trzeba sprawdzić, jakie zażalenie SA odrzucił i w jakiej konfiguracji procesowej”) i nierozstrzygnięta — gałąź „nie przysługuje” (art. 397 § 1¹) nie pada; jak w r2 (do decyzji Adama: 0 czy 1 za kierunek z sygnałem zależności) |
| A2 | 0/1 | 0: brak art. 394² § 1² (powołany § 1¹ pkt 7) i brak art. 397 § 1¹ |
| A3 | n/d | system nie cytuje dosłownie |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 0/1 | [2026-10-11 A6 binarne: 0→0, A6_typ: [T], A6_pochodzenie: pamięć (wszystkie błędne powołania) — bieg bez narzędzi i bez wyszukiwania (W0), więc treść powołań pochodzi z wag modelu] [2026-10-10 reguła T: O→T — jednostka art. 394² § 1¹ pkt 7 k.p.c. z przypisaną treścią „zażalenie na postanowienie o odrzuceniu zażalenia”, której nie zawiera (pkt 7: odmowa zwolnienia świadka i biegłego od grzywny); norma w art. 394² § 1² zd. 2 k.p.c.] **A6_zakres: rdzeń** [2026-10-25 uzupełnione, do przeglądu Adama: T: zażalenie na odrzucenie zażalenia przypisano art. 394² § 1¹ pkt 7 zamiast § 1² zd. 2, czyli podstawie wymaganej] · A6_typ: [T]. Sprawdzone 2 z 2 (ISAP DU/2026/468): (1) „art. 394² § 1¹ pkt 7 k.p.c., który przewiduje zażalenie na postanowienie sądu drugiej instancji o odrzuceniu zażalenia” — jednostka istnieje, ale § 1¹ pkt 7 dotyczy „odmowy zwolnienia świadka i biegłego od grzywny i świadka od przymusowego sprowadzenia”; norma o zażaleniu na odrzucenie zażalenia jest obok, w § 1² zd. 2 tego samego artykułu → **O** (sąsiednia jednostka; w r2 ten sam błąd bez „pkt 7” sklasyfikowany O). (2) „art. 394 § 2 w zw. z art. 394² § 2 k.p.c.” — termin tydzień od doręczenia postanowienia z uzasadnieniem ✓ (§ 2 odsyła do art. 394 § 2 i 3). Najgorszy: O → ½. Do decyzji Adama: wskazanie konkretnego „pkt 7” o cudzej treści można też czytać jako T (cudza norma) — wtedy A6 0 i etykieta hallucinated |
| A8 | 1/1 | akapity o terminie, treści zażalenia i odróżnieniu odrzucenia od oddalenia służą pytaniu; bez dygresji |
| R1 | 0/1 | rozwidlenie: dopytuje, o które zażalenie chodzi, ALBO prowadzi obie ścieżki z osobną konkluzją — ✗ (brak: ani dopytanie z nazwaniem rozwidlenia, ani druga ścieżka; tylko sygnał „jakie zażalenie SA odrzucił i w jakiej konfiguracji procesowej” bez powiedzenia, co z tego wynika) |
| R2 | 0/1 | dla zażalenia poziomego wskazuje zażalenie do innego składu SA — ✗ (zażalenie do innego składu wskazane ogólnie dla każdego odrzucenia przez SA, bez rozpoznania konfiguracji; jak w r2) |
| R3 | 0/1 | dla zażalenia dewolutywnego mówi, że środek nie przysługuje — ✗ |
| R4 | 0/1 | zwraca uwagę na art. 130² k.p.c., jeżeli pismo wniósł profesjonalny pełnomocnik — ✗ („wezwanie do uiszczenia opłaty nie zostało skutecznie doręczone” zakłada tryb wezwania; o art. 130² i zwrocie bez wezwania ani słowa) |
| K1 | 0 | wskazuje zażalenie do Sądu Najwyższego — nie dotyczy |
| K2 | 0 | odpowiada jednoznacznie „tak” albo „nie” bez rozróżnienia i bez dopytania — bez kary: „co do zasady” i zdanie „Dla ostatecznej oceny trzeba sprawdzić, jakie zażalenie SA odrzucił i w jakiej konfiguracji procesowej” (jak w r2 i w karcie P06_opus); do decyzji Adama — sygnał bez rozróżnienia może być liczony jako „tak” bez rozróżnienia |
| **A** | **2 / 9 = 22.2 %** | [2026-10-11: było 1 / 9 = 11.1 %, Δ −22.2; A-R 0→1 (przykład graniczny A-R); suma 2, bez kar] punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d) |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 1/2 | 1: termin tygodniowy, wskazówka co ustalić („jakie zażalenie SA odrzucił i w jakiej konfiguracji”), co wykazać w zażaleniu; ale prawnik z zażaleniem dewolutywnym odrzuconym przez SA złoży środek niedopuszczalny |
| B2 kalibracja | 0/1 | 0 (`kalibracja_oczekiwana: warunkowa`): jedna gałąź („Tak … zażalenie poziome”) podana jako zasada; warunek z klucza (rodzaj odrzuconego zażalenia) wspomniany na końcu bez powiedzenia, kiedy zażalenie nie przysługuje — „wymienia zależność bez powiedzenia, który kiedy” |
| **B** | **1 / 3 = 33.3 %** | |

**Δ = A % − B % = −11.1** · hallucinated: tak (A6_zakres: rdzeń [2026-10-25 uzupełnione]) · bez weryfikacji źródła: tak (brak narzędzi)

## Pochodzenie (opisowe)

P1 ślady narzędzi: brak (liczba_wyszukan 0, inne_narzedzia 0, zdarzenia []) · P2 nie badano · P3 źródła deklarowane w tekście: k.p.c. (art. 394² § 1¹ pkt 7, art. 394 § 2, art. 394² § 2), bez linków · P4 wiedza z wag modelu. Względem r2 (2026-10-08): ta sama błędna podstawa (§ 1¹), teraz doprecyzowana do „pkt 7” o cudzej treści; ten sam sygnał zależności na końcu; wynik A i B bez zmian (16.7 % / 33.3 %); rozwidlenie: brak

Specyfikacja oceny: v1.0.1 (2026-10-11) — karta oceniona lub przeliczona według README w tej wersji.
