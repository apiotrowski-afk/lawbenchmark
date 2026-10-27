# Karta oceny — P04 · OpenAI gpt-5.6-terra przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie na żywo — r3 W1 (rozszerzenie 2026-10-18)

- Pytanie: P04 (katalog nr 25), klucz w wersji 3 (2026-10-18, zatwierdzony; kalibracja kategoryczna; podwójna pułapka — decyzja zamiast postanowienia, zaświadczenie zamiast klauzuli; decyzja może być ostateczna i prawomocna)
- Data odpowiedzi systemu: 2026-10-18 · czas 22.2 s · warunki: gpt-5.6-terra, wysiłek rozumowania medium, Codex CLI (sandbox read-only, pusty katalog, sesja nietrwała, aplikacje ChatGPT wyłączone); wstęp neutralny z `eval_codex.py` (wariant web); wyszukiwarka: web_search Codexa; liczba wyszukań: 4
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 1/2 | [2026-10-18 decyzja Adama B2: 0→1 — „Co do zasady … ostateczności”, a na końcu „można wnioskować o zaświadczenie obejmujące również prawomocność” — wariant „zasadniczo ostateczność, ewentualnie też prawomocność”] 0: pierwsze zdanie — „Co do zasady: **klauzulę/zaświadczenie o ostateczności**, nie prawomocności”; praktyczna konkluzja — „należy wystąpić do MSWiA o **zaświadczenie o ostateczności decyzji**”. Pierwsza pułapka skorygowana („w drodze decyzji administracyjnej, a nie postanowienia”), druga częściowo (zaświadczenie MSWiA, ale „klauzulę/zaświadczenie” jako równoważne). Na zadaną alternatywę „prawomocności czy ostateczności” system wybiera gałąź przeciwną do klucza (organ wydaje zaświadczenie o prawomocności) — kierunek nietrafny, tak jak w karcie W0 tego modelu. **Do decyzji Adama** — alternatywa 1 (jak w `P04_chatgpt_codex_w0_r3` i `P04_codex_astra6_web_r3`): korekta formy, przyznanie prawomocności decyzji (art. 16 § 3) i dopuszczenie zaświadczenia „obejmującego również prawomocność” jako kierunek trafny bez kluczowego warunku (wtedy A 4 / 9 = 44.4 %) |
| A2 | 0/1 | art. 1 ust. 1 u.n.n.c. ✓, art. 16 § 1 i § 3 k.p.a. ✓; brak art. 217 § 2 pkt 2 k.p.a. (podstawa wymagana) |
| A3 | n/d | system nie cytuje dosłownie |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 1/1 | A6_typ: brak błędów · A6_powolania: sprawdzone 5 z 5, wszystkie zgodne. u.n.n.c. (ELI PDF DU/2017/2278, t.j., pdftotext; legal-cite aktu nie obsługuje): art. 1 ust. 1 ✓ (zezwolenie „w drodze decyzji administracyjnej, przez ministra właściwego do spraw wewnętrznych”), art. 1 ust. 1a ✓ (sprzeciw MON i ministra właściwego do spraw rozwoju wsi „w drodze postanowienia”). k.p.a. (legal-cite: t.j. DU/2024/572, brzmienie identyczne w Dz.U. 2025 poz. 1691, bez nowel po t.j.): art. 16 § 1 ✓ (decyzja ostateczna — nie służy odwołanie ani wniosek o ponowne rozpatrzenie), art. 127 § 3 ✓ (od decyzji ministra wydanej w pierwszej instancji — wniosek o ponowne rozpatrzenie), art. 16 § 3 ✓ („Decyzje ostateczne, których nie można zaskarżyć do sądu, są prawomocne”). Teza „ostateczność” jako odpowiedź na pytanie nie jest twierdzeniem o treści przepisu (system nie przypisuje jej jednostce ani orzecznictwu) — płaci w A-R, R3 i B1, nie w A6. Linki: eli.gov.pl DU/2017/2278 (HTTP 200), eli.gov.pl DU/2024/572 (k.p.a. t.j. z 2024, starszy, HTTP 200; art. 16 w tym samym brzmieniu — bez klasy), biznes.gov.pl proc/209 „Nabycie nieruchomości przez cudzoziemca” (HTTP 200) |
| A8 | 1/1 | każdy akapit służy odpowiedzi; „Doprecyzowanie” o postanowieniu w sprawie sprzeciwu (art. 1 ust. 1a) to korekta przesłanki pytania (neutralne) |
| R1 | 1/1 | koryguje formę — „wydaje minister właściwy ds. wewnętrznych **w drodze decyzji administracyjnej**, a nie postanowienia (art. 1 ust. 1 …)” |
| R2 | 0/1 | zaświadczenie organu (art. 217 k.p.a.), nie klauzula — mowa o „zaświadczeniu” MSWiA, ale bez podstawy i bez korekty „klauzuli” (przeciwnie: „klauzulę/zaświadczenie” jako zamienniki). **Do decyzji Adama** — alternatywa 1, jeżeli wystarcza wskazanie zaświadczenia organu bez art. 217 i bez wyraźnego odrzucenia terminu „klauzula” (wtedy A 4 / 9 = 44.4 %) |
| R3 | 0/1 | rozróżnienie ostateczności i prawomocności ✓, możliwość prawomocności ✓ (art. 16 § 3), ale organ ma zaświadczać „co do zasady” ostateczność, „nie prawomocności” — element złożony, ✗ |
| R4 | 0/1 | mechanizm prawomocności — tylko ogólne „po bezskutecznym upływie terminu skargi do WSA albo po zakończeniu kontroli sądowej”; brak 30 dni i skargi bez wniosku o ponowne rozpatrzenie — ✗ |
| K1 | 0 | nie zaleca wniosku do sądu o klauzulę prawomocności |
| K2 | 0 | nie twierdzi, że obywatel Ukrainy nie potrzebuje zezwolenia |
| K3 | 0 | [2026-10-18 decyzja Adama B3: zostaje 0 — furtka „zaświadczenie obejmujące również prawomocność” — odpowiedź nie mówi „wyłącznie ostateczność” i nie wyklucza prawomocności definitywnie] „co do zasady … ostateczności, nie prawomocności”, ale na końcu: „można wnioskować o zaświadczenie obejmujące również prawomocność” — odpowiedź nie twierdzi, że potwierdza się **wyłącznie** ostateczność, i nie przeczy prawomocności decyzji (art. 16 § 3). Różnica wobec karty W0 tego modelu (tam K3 −1: odpowiedź wykluczała potwierdzenie prawomocności). **Do decyzji Adama** — alternatywa −1, jeżeli nagłówkowe „nie prawomocności” wystarcza do kary mimo furtki w ostatnim akapicie (wtedy A 2 / 9 = 22.2 %) |
| **A** | **4 / 9 = 44.4 %** | [2026-10-18: było 3 / 9 = 33.3 % — B2: A-R 0→1] punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d); punkty: A-R 1 + A2 0 + A6 1 + A8 1 + R1 1 = 4; bez kar |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 1/2 | 1: prawnik wie, że chodzi o decyzję MSWiA i zaświadczenie organu, a nie o klauzulę sądu; główna wskazówka co do przedmiotu wniosku (zaświadczenie o ostateczności zamiast o prawomocności) jest błędna — reguła B1 o błędzie w praktycznej wskazówce (forma/przedmiot): najwyżej 1; nie 0, bo odpowiedź dopuszcza zaświadczenie o prawomocności i nie grozi utratą terminu ani prawa (przykład graniczny B1 nr 1) |
| B2 kalibracja | 1/1 | 1 (`kategoryczna`): teza postawiona wprost w pierwszym zdaniu; „co do zasady” i furtka dla notariusza dotyczą faktu nieznanego z pytania (czego oczekuje notariusz), nie rozmywają tezy |
| **B** | **2 / 3 = 66.7 %** | |

**Δ = A % − B % = −22.2** [2026-10-18: było −33.3 — B2] · hallucinated: nie · bez weryfikacji źródła: nie — linki w odpowiedzi: eli.gov.pl DU/2017/2278 (u.n.n.c.), eli.gov.pl DU/2024/572 (k.p.a.), biznes.gov.pl (procedura MSWiA)

## Pochodzenie (opisowe)

P1 ślady narzędzi: 4 zdarzenia web_search (2 z pustym zapytaniem); zapytania: „site:gov.pl nabywanie nieruchomości przez cudzoziemców zezwolenie decyzja administracyjna ostateczność …”, „site:eli.gov.pl Kodeks postępowania administracyjnego art. 16 § 1 decyzje ostateczne prawomocne …” · P2 nie badano · P3 źródła deklarowane w tekście: eli.gov.pl DU/2017/2278 (t.j. u.n.n.c., aktualny), eli.gov.pl DU/2024/572 (t.j. k.p.a. z 2024, starszy; aktualny t.j. Dz.U. 2025 poz. 1691), biznes.gov.pl proc/209 — wszystkie HTTP 200 · P4 źródła urzędowe (ELI, serwis gov.pl). Profil błędu: brak halucynacji, konkluzja zgodna z „typowym błędem” z klucza v3 (ostateczność zamiast prawomocności), złagodzona furtką na zaświadczenie o prawomocności. Porównanie z W0 tego modelu (`P04_codex_terra56_w0_r3`, A 11.1 %, hallucinated T — art. 3 ust. 1 zamiast art. 1 ust. 1 u.n.n.c.): wyszukiwanie usunęło błędną jednostkę (teraz trafny art. 1 ust. 1 i 1a), konkluzja co do ostateczności bez zmian

Specyfikacja oceny: v1.0.1 (2026-10-11) z przykładami granicznymi z 2026-10-17 oraz zasadami soft law i A6_zakres z 2026-10-18 — karta wypełniona wstępnie 2026-10-18.
