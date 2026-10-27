# Karta oceny — P06 · OpenAI gpt-5.6-terra przez Codex CLI (rozumowanie: medium), W0 bez wyszukiwania — r3

- Pytanie: P06 (katalog nr 22), klucz w wersji 3 (2026-10-10, element „rozwidlenie”)
- Data odpowiedzi systemu: 2026-10-10 · czas 95.4 s · warunki: model gpt-5.6-terra, wysiłek rozumowania medium, Codex CLI (sandbox read-only, pusty katalog, sesja nietrwała), aplikacje ChatGPT wyłączone (features.apps=false); narzędzia: brak, wyszukiwanie: brak (W0), liczba wyszukań 0; wstęp: „Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne. Odpowiedz bezpośrednio w wiadomości — nie twórz plików i nie uruchamiaj poleceń.”; tokeny: wejście 9515 (z pamięci podręcznej 8960), wyjście 2522, rozumowanie 2243
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 1/2 | [2026-10-11 przykład graniczny A-R: 0→1 — konkluzja „tak, zażalenie do innego składu SA (poziome)” bez rozróżnienia jest trafna dla gałęzi poziomej klucza; brak rozróżnienia płaci w R1, K i B2] 0: jedna gałąź podana jako zasada, bez warunku — „Tak. Na postanowienie Sądu Apelacyjnego o odrzuceniu zażalenia z powodu nieuiszczenia opłaty przysługuje co do zasady zażalenie poziome”; gałąź „nie przysługuje” (SA jako sąd II instancji, art. 397 § 1¹) nie pada, zależność od rodzaju odrzuconego zażalenia nie jest zasygnalizowana (jak w kartach z kategorycznym „tak”: P06_gemini_r3, P06_chatgpt_codex_w0_r3 — 0; do decyzji Adama: 1 za kierunek trafny dla gałęzi poziomej) |
| A2 | 0/1 | 0: brak art. 394² § 1² i brak art. 397 § 1¹; w ich miejscu „art. 394² § 1 pkt 12” |
| A3 | n/d | system nie cytuje przepisu dosłownie; dwuwyrazowe „odrzucenie zażalenia” w cudzysłowie przy błędnej jednostce liczone w A6 (reguła 3: bez podwójnego liczenia A3 i A6) |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 0/1 | [2026-10-11 A6 binarne: 0→0, A6_typ: [F], A6_pochodzenie: pamięć (wszystkie błędne powołania) — bieg bez narzędzi i bez wyszukiwania (W0), więc treść powołań pochodzi z wag modelu] **A6_zakres: rdzeń** [2026-10-25 uzupełnione, do przeglądu Adama: F: nieistniejący art. 394² § 1 pkt 12 powołany jako podstawa głównej konkluzji o zażaleniu na odrzucenie zażalenia] · A6_typ: [F]. Sprawdzone 2 z 2 (ISAP DU/2026/468): (1) **„art. 394² § 1 pkt 12 k.p.c. („odrzucenie zażalenia”)” — F**: art. 394² § 1 nie ma punktów (jedno zdanie: odrzucenie apelacji, odrzucenie skargi o wznowienie, umorzenie postępowania apelacyjnego), a wyliczenie w § 1¹ kończy się na pkt 7 — punktu 12 w art. 394² nie ma; „12) odrzucenie zażalenia” to art. 394¹ᵃ § 1 pkt 12 (zażalenie do innego składu sądu **pierwszej** instancji), a norma o zażaleniu na odrzucenie zażalenia poziomego w SA jest w art. 394² § 1² zd. 2. Jednostka powołana jako podstawa → F (reguła 3 zd. ostatnie). Do decyzji Adama: alternatywnie T (wskazana jednostka z cudzą treścią) albo S (pomylony numer artykułu: 394¹ᵃ → 394²) — S odrzucono, bo art. 394¹ᵃ § 1 pkt 12 nie daje zażalenia na postanowienie SA, więc teza nie zgadza się z realnym źródłem; przy F i T punkt ten sam (0, hallucinated); (2) „art. 394 § 2 k.p.c. w zw. z art. 394² k.p.c.” ✓ — tydzień od doręczenia postanowienia z uzasadnieniem (art. 394² § 2 odsyła do art. 394 § 2 i 3). Orzeczeń nie powołano (SAOS: 0 sprawdzeń). Najgorszy przypadek: F → 0 |
| A8 | 1/1 | cztery akapity, wszystkie o zaskarżalności postanowienia i sposobie wniesienia zażalenia; bez dygresji |
| R1 | 0/1 | rozwidlenie: dopytanie z nazwaniem rozwidlenia ALBO obie ścieżki — ✗ (ani dopytania, ani dwóch ścieżek) |
| R2 | 0/1 | dla zażalenia poziomego wskazuje zażalenie do innego składu SA — ✗: zażalenie „do innego składu tego samego Sądu Apelacyjnego” wskazane ogólnie dla każdego odrzucenia przez SA, bez rozpoznania konfiguracji (tak liczone w P06_gemini_r3 i P06_chatgpt_codex_w0_r3). Do decyzji Adama: przy łagodnym czytaniu 1, bo dla gałęzi poziomej wskazanie jest trafne |
| R3 | 0/1 | dla zażalenia dewolutywnego mówi, że środek nie przysługuje — ✗ (brak) |
| R4 | 0/1 | art. 130² k.p.c. przy profesjonalnym pełnomocniku — ✗ (jest tylko „sąd nie powinien był odrzucać środka bez uprzedniego wezwania do zapłaty”; art. 130², zwrotu bez wezwania i dopłaty w tygodniu brak) |
| K1 | 0 | wskazuje zażalenie do Sądu Najwyższego — nie dotyczy |
| K2 | −1 | odpowiada jednoznacznie „tak” albo „nie” bez rozróżnienia i bez dopytania — „Tak. … przysługuje co do zasady zażalenie poziome”; rozróżnienia ani dopytania brak. Do decyzji Adama: jedyny sygnał to „co do zasady” (w P06_chatgpt_codex_w0_r3 kary nie naliczono, ale tam było też zdanie „trzeba sprawdzić, jakie zażalenie SA odrzucił”); bez kary A = 1 / 9 = 11.1 % |
| **A** | **1 / 9 = 11.1 %** | [2026-10-11: było 0 / 9 = 0.0 %, Δ −33.3; A-R 0→1 (przykład graniczny A-R); suma 2 − K 1 = 1] punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d); suma 1 − K 1 = 0 |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 1/2 | 1: dla zażalenia poziomego wskazówka praktyczna trafna (inny skład SA, tydzień od doręczenia z uzasadnieniem, opłata, co zarzucać), ale z podstawą nie do przepisania („art. 394² § 1 pkt 12”); prawnik, któremu SA odrzucił zażalenie na postanowienie SO, złoży środek niedopuszczalny. Do decyzji Adama (0, jeżeli to przesądza) |
| B2 kalibracja | 0/1 | 0 (`kalibracja_oczekiwana: warunkowa`): odpowiedź kategoryczna („Tak … przysługuje”), warunek z klucza (rodzaj odrzuconego zażalenia) pominięty; „co do zasady” nie mówi, od czego wyjątek zależy |
| **B** | **1 / 3 = 33.3 %** | |

**Δ = A % − B % = −22.2** · hallucinated: tak (A6_typ F; A6_zakres: rdzeń [2026-10-25 uzupełnione]) · bez weryfikacji źródła: tak (brak narzędzi)

## Pochodzenie (opisowe)

P1 ślady narzędzi: brak (W0: bez narzędzi i bez wyszukiwania) · P2 nie badano · P3 źródła deklarowane w tekście: k.p.c. (art. 394² § 1 pkt 12, art. 394 § 2 w zw. z art. 394²), bez linków · P4 wiedza z wag modelu; numer punktu przeniesiony z art. 394¹ᵃ § 1 do art. 394². Rozwidlenie: brak. Warunki biegu z nagłówka odpowiedzi: model gpt-5.6-terra, wysiłek rozumowania medium, Codex CLI, sandbox read-only (pusty katalog, sesja nietrwała), aplikacje ChatGPT wyłączone, liczba_wyszukan 0, inne_narzedzia 0, zdarzenia [], blad null; wstęp jak w metryce karty

Specyfikacja oceny: v1.0.1 (2026-10-11) — karta oceniona lub przeliczona według README w tej wersji.
