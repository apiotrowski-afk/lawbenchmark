# Karta oceny — P13 · OpenAI gpt-6.1-sol przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie na żywo — r3

- Pytanie: P13 (katalog nr 15), klucz w wersji 1 (2026-10-10, zatwierdzony; kalibracja kategoryczna)
- Data odpowiedzi systemu: 2026-10-10 · czas 46.7 s · warunki: gpt-6.1-sol, wysiłek rozumowania medium, Codex CLI (sandbox read-only, pusty katalog, sesja nietrwała, aplikacje ChatGPT wyłączone); wstęp neutralny z `eval_codex.py` (wariant web); wyszukiwarka: web_search Codexa; liczba wyszukań: 8
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 2/2 | 2: „**Nie — samo wstrzymanie wykonania nakazu zapłaty z weksla na podstawie art. 492 § 3 k.p.c. nie blokuje wszczęcia postępowania zabezpieczającego na podstawie tego nakazu.**” + dwie funkcje nakazu (tytuł zabezpieczenia z § 1 od wydania, bez klauzuli; natychmiastowa wykonalność z § 3) |
| A2 | 1/1 | „**art. 492 § 1 k.p.c.**”, „**art. 492 § 3 k.p.c.**” |
| A3 | n/d | system nie cytuje dosłownie; brzmienie z „warrantem i rewersem” nie pada |
| A5 | n/d | pytanie niesporne (`sporne: false` potwierdzone przez Adama) |
| A6 | 0/1 | [2026-10-11 A6 binarne: 0→0, A6_typ: [T], A6_pochodzenie: postanowienie SN I CZ 83/09: odczyt_źródła — rozstrzygnięcie Adama bez zmian; odpowiedź podaje adres saos.org.pl/judgments/90795, system miał pełny tekst orzeczenia i mimo to przypisał mu tezę, której w nim nie ma.] [2026-10-11 decyzja Adama: 1→0, A6_typ: [T] — postanowieniu SN I CZ 83/09 (SAOS 90795) przypisano tezę „wstrzymanie wykonania nakazu z weksla nie pozbawia go cech tytułu zabezpieczenia”, której w nim nie ma: teza orzeczenia dotyczy niedopuszczalności zażalenia na wstrzymanie wykonania postanowienia o zabezpieczeniu (art. 396), sprawa o rozwiązanie sp. z o.o.; o nakazie tylko dwie wzmianki poboczne; system miał pełny tekst (link do SAOS) — nadinterpretacja; rozbieżność wykryta przez drugiego sędziego (Astra 6)] [2026-10-10 reguła T: nie dotyczy — karta nie ma klasy O (A6_typ: brak błędów); zastrzeżenie dotyczy orzeczenia I CZ 83/09, nie jednostki przepisu, więc reguła o wskazanej jednostce nie ma zastosowania] **A6_zakres: rdzeń** [2026-10-25 uzupełnione, do przeglądu Adama: T: postanowieniu SN I CZ 83/09 przypisano tezę będącą główną konkluzją (wstrzymanie nie pozbawia cech tytułu zabezpieczenia); rozstrzygnięte 2026-10-25: T (treść przypisana błędnie, nie samo oznaczenie) służy głównej konkluzji = rdzeń; reguła nr 2 dotyczy tylko S] · A6_typ: brak błędów (jedno powołanie z zastrzeżeniem, niżej) · A6_powolania: sprawdzone 7 z 7. k.p.c. (ISAP DU/2026/468): art. 492 § 1 ✓ („z chwilą wydania stanowi tytuł zabezpieczenia, wykonalny bez nadawania mu klauzuli”), § 2 ✓ (powód wskazuje sposób; ograniczenie na wniosek pozwanego; art. 742 odpowiednio), § 3 ✓ (bez warrantu i rewersu — brzmienie aktualne), art. 731 ✓ („nie może zmierzać do zaspokojenia roszczenia”), art. 742 ✓ (przez odesłanie z § 2), Dz.U. 2026 poz. 468 ✓. Postanowienie SN z 4.09.2009, I CZ 83/09 ✓ istnieje (SAOS 90795, link z odpowiedzi trafny; data i sygnatura zgodne). **Zastrzeżenie:** sentencja dotyczy zażalenia na postanowienie z art. 396 k.p.c. w sprawie o rozwiązanie spółki, nie nakazu z weksla; w uzasadnieniu SN stwierdza jednak, że „nakaz zapłaty wydany w postępowaniu nakazowym stanowi z mocy prawa tytuł zabezpieczający” i że wcześniejsza ocena dopuszczalności zażalenia na wstrzymanie wykonania nakazu z weksla (III CZP 147/93, III CZP 58/03) „nie odnosiła się do wstrzymania wykonalności nakazu zapłaty jako tytułu zabezpieczającego” — rozróżnienie jest, ale jako obiter w innym kontekście; zdanie „wstrzymanie wykonania nakazu z weksla nie pozbawia go cech tytułu zabezpieczenia” to wniosek systemu z tego fragmentu, nie wypowiedź SN. Odpowiedź powołuje wprost „uzasadnienie postanowienia”, więc wstępnie bez klasy błędu; **do decyzji Adama** (alternatywa: O → ½ za nadinterpretację). Klucz nie zna I CZ 83/09 (jedyne znane orzeczenie: SO Szczecin VIII Gz 43/16) |
| A8 | 1/1 | każdy akapit służy odpowiedzi; uwaga o sprawdzeniu sentencji postanowienia o wstrzymaniu — praktyczna, w ramach pytania |
| R1 | 1/1 | „nie” + dwie funkcje — „Nakaz pełni dwie odrębne funkcje: **Tytułu zabezpieczenia** … Podstawy egzekucji … Wstrzymanie na podstawie **art. 492 § 3 k.p.c.** dotyczy tej funkcji” |
| R2 | 1/1 | tytuł zabezpieczenia od wydania, bez klauzuli — „już od chwili wydania, bez konieczności nadania klauzuli wykonalności (**art. 492 § 1 k.p.c.**)”; „Nie potrzebuje odrębnego postanowienia o udzieleniu zabezpieczenia” |
| R3 | 1/1 | środki obrony pozwanego — „osobnego wniosku dotyczącego zabezpieczenia, w szczególności o jego ograniczenie na podstawie **art. 492 § 2 k.p.c.**, z odpowiednim zastosowaniem art. 742 k.p.c.” (bez depozytu z § 1 zd. 2, ale rubryka dopuszcza alternatywę) |
| R4 | 0/1 | skutek wstrzymania = zawieszenie egzekucji (art. 820 § 2), nie upadek zabezpieczenia — ✗ druga połowa jest („dotyczy tej funkcji”, zabezpieczenie „pozostaje dopuszczalne”), pierwszej brak: ani art. 820 § 2, ani zawieszenia egzekucji na wniosek dłużnika; do decyzji Adama, czy zaliczyć łagodnie |
| K1 | 0 | nie twierdzi, że wstrzymanie wyłącza zabezpieczenie |
| K2 | 0 | nie wymaga klauzuli ani osobnego postanowienia — wprost przeciwnie |
| K3 | 0 | nie cytuje brzmienia z warrantem i rewersem |
| **A** | **7 / 9 = 77.8 %** | [2026-10-11: było 8 / 9 = 88.9 %] |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 2/2 | [2026-10-17 decyzja Adama: zostaje 2 wg obecnej reguły; przypadek odnotowany do następnej wersji specyfikacji — orzeczenie z cudzą tezą, które prawnik przeniesie do pisma, a obecna reguła B1 („kwota, termin, organ, forma”) go nie obejmuje; README, plan pkt 10] 2: dla powoda — droga do komornika ze wskazaniem sposobu (zajęcie rachunku), granica z art. 731; dla pozwanego — osobny wniosek o ograniczenie; wskazówka, by sprawdzić zakres sentencji postanowienia o wstrzymaniu |
| B2 kalibracja | 1/1 | 1 (`kategoryczna`): „Nie —” wprost w pierwszym zdaniu; zastrzeżenie o treści sentencji dotyczy faktu nieznanego z pytania, nie rozmywa tezy |
| **B** | **3 / 3 = 100.0 %** | |

**Δ = A % − B % = -22.2** · hallucinated: tak (T — I CZ 83/09, decyzja Adama 2026-10-11; A6_zakres: rdzeń [2026-10-25 uzupełnione]) · bez weryfikacji źródła: nie — ślad web_search i linki: eli.gov.pl / api.sejm.gov.pl DU/2026/468 (k.p.c.), saos.org.pl/judgments/90795

## Pochodzenie (opisowe)

P1 ślady narzędzi: 8 zdarzeń web_search (4 z pustym zapytaniem); zapytania: „wstrzymanie wykonania nakazu zapłaty weksel nie pozbawia tytułu zabezpieczenia 492 3”, eli.gov.pl/api/acts/DU/2026/468/text.html, „"I ACz 390/13" data 2013” (szukane orzeczenie SA nie trafiło do odpowiedzi; zamiast niego powołano I CZ 83/09), api.sejm.gov.pl DU/2026/468/text.pdf · P2 nie badano · P3 źródła deklarowane w tekście: api.sejm.gov.pl DU/2026/468 (t.j. k.p.c., aktualny), saos.org.pl/judgments/90795 (I CZ 83/09 — identyfikator trafny) · P4 źródła urzędowe (ISAP, SAOS). Pierwszy bieg P13 dla tego systemu; bez porównania

Specyfikacja oceny: v1.0 (2026-10-11) — karta oceniona lub przeliczona według README w tej wersji.
