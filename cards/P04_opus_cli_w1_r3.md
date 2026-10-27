# Karta oceny — P04 · Claude opus przez Claude Code CLI (subskrypcja), czysty model — bez MCP i CLAUDE.md, W1: WebSearch + WebFetch — r3 W1 (rozszerzenie 2026-10-18)

- Pytanie: P04 (katalog nr 25), klucz w wersji 3 (2026-10-18, zatwierdzony; kalibracja kategoryczna; podwójna pułapka — decyzja zamiast postanowienia, zaświadczenie zamiast klauzuli; decyzja może być ostateczna i prawomocna)
- Data odpowiedzi systemu: 2026-10-18 · czas 55.0 s · warunki: model_id `claude-haiku-5-5,claude-opus-5-5` (alias opus), Claude Code CLI (subskrypcja), bez MCP i CLAUDE.md; narzędzia: WebSearch + WebFetch (W1); prompt systemowy z dopiskiem o wyszukiwaniu i adresach źródeł; liczniki `server_tool_use`: web_search_requests 0, web_fetch_requests 0 (narzędzia Claude Code działają po stronie klienta, liczniki ich nie obejmują); ślad narzędzi niezachowany
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 1/2 | 1 [2026-10-18 decyzja Adama nr 12: „zasadniczo ostateczność, ewentualnie też prawomocność” = 1 — zatwierdzone; alternatywa 2 odrzucona] (było: wstępnie) wg reguły klucza („zasadniczo ostateczność, ewentualnie też prawomocność” = 1): pierwszy akapit — „nie jest to postanowienie … tylko **decyzja administracyjna** MSWiA. Dlatego **co do zasady mówi się o jej ostateczności, a nie o prawomocności** w rozumieniu procedury cywilnej. MSWiA w ogóle nie nadaje decyzji klauzuli. Na wniosek strony wydaje **zaświadczenie**, że decyzja jest ostateczna i prawomocna”; obie pułapki skorygowane, dalej pełny mechanizm (14 dni, art. 16 § 3, 30 dni na skargę do WSA, art. 52 § 3 p.p.s.a.). Rdzeń jest w odpowiedzi w całości, ale teza wiodąca „co do zasady ostateczność, a nie prawomocność” odpowiada wariantowi z reguły klucza. **Do decyzji Adama** — alternatywa 2, jeżeli zastrzeżenie „w rozumieniu procedury cywilnej” i zaświadczenie „ostateczna i prawomocna” w tym samym akapicie uznać za pełny rdzeń (przykład graniczny A-R 1: rdzeń gdziekolwiek w odpowiedzi; wtedy A 9 / 9 = 100.0 %, Δ 0.0) |
| A2 | 1/1 | art. 1 ust. 1 u.n.n.c. ✓, art. 16 § 1 ✓ i § 3 k.p.a. ✓, art. 217 k.p.a. ✓ — powołany bez „§ 2 pkt 2”; ogólne odesłanie do artykułu przy trafnej treści (zaświadczenie na wniosek strony), tak jak w rubryce klucza („art. 217 k.p.a.”). [2026-10-18 decyzja Adama nr 10: „art. 217” bez „§ 2 pkt 2” = 1 — zatwierdzone; alternatywa 0 odrzucona] |
| A3 | n/d | system nie cytuje przepisów dosłownie; „ostateczna i prawomocna” w cudzysłowie to formuła MSWiA, nie przepis |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 1/1 | A6_typ: brak błędów · **Sprawdzone 18 z 18**, wszystkie zgodne. u.n.n.c. (api.sejm.gov.pl DU/2017/2278, t.j., pdftotext; nowela 2026/1099 w życie 19.11.2026 — po dacie stanu prawnego): art. 1 ust. 1 ✓ (zezwolenie „w drodze decyzji administracyjnej, przez ministra właściwego do spraw wewnętrznych”), Dz.U. 2017 poz. 2278 ✓, art. 3 ust. 2 ✓ (ważność 2 lata „od dnia wydania” — w odpowiedzi bez numeru, z zaleceniem sprawdzenia początku biegu), art. 6 ust. 1 ✓ (nabycie wbrew ustawie nieważne), art. 8 ust. 1 pkt 1 w zw. z ust. 3 ✓ (samodzielny lokal mieszkalny; zwolnień nie stosuje się w strefie nadgranicznej), art. 8 ust. 1 pkt 2 ✓ (5 lat od zezwolenia na pobyt stały lub rezydenta długoterminowego UE). k.p.a. (api.sejm.gov.pl DU/2025/1691, t.j., pdftotext): art. 16 § 1 ✓, art. 127 § 3 ✓ (od decyzji ministra wniosek o ponowne rozpatrzenie), art. 129 § 2 ✓ (14 dni), art. 127a ✓ (zrzeczenie się; § 2 „przez ostatnią ze stron”; przepis mówi „ostateczna i prawomocna” — podanie tylko „ostateczna” to pominięcie, nie fałsz), art. 16 § 3 ✓ i „po nowelizacji k.p.a. z 2017 r.” ✓ (§ 3 dodany przez art. 1 pkt 6 ustawy Dz.U. 2017 poz. 935; t.j. Dz.U. 2016 poz. 23 kończy art. 16 na § 2), art. 217 ✓. p.p.s.a. (api.sejm.gov.pl DU/2026/143, t.j.): art. 52 § 3 ✓ (skarga bez wniosku o ponowne rozpatrzenie), art. 53 § 1 ✓ (30 dni). k.p.c. (legal-cite: t.j. DU/2024/1568 = Dz.U. 2026 poz. 468): art. 363 § 1 ✓, art. 364 § 1 ✓ (stwierdzenie prawomocności przez sąd — „nie ma zastosowania” w k.p.a. trafne). Praktyka MSWiA (gov.pl/web/mswia/najczesciej-zadawane-pytania, odczyt curl): „nie wydaje odpisu decyzji opatrzonego klauzulą” ✓, zaświadczenie o ostateczności i prawomocności na wniosek ✓, opłata skarbowa 17 zł ✓. Specustawa ukraińska z 12.03.2022 (Dz.U. 2022 poz. 583) ✓ — data trafna, brak zwolnienia z wymogu zezwolenia (w tekście ustawy brak przepisu o nabywaniu nieruchomości) |
| A8 | 1/1 | każdy akapit służy odpowiedzi; praktyka u notariusza to skutek odpowiedzi dla pytającego; ważność zezwolenia i nieważność umowy — dwa jednozdaniowe punkty tła; uwaga o obywatelu Ukrainy i art. 8 odpowiada na element pytania (obywatelstwo; K2) |
| R1 | 1/1 | koryguje formę — „nie jest to postanowienie ani orzeczenie sądu, tylko **decyzja administracyjna** MSWiA” (art. 1 ust. 1) |
| R2 | 1/1 | zaświadczenie organu, nie klauzula — „MSWiA w ogóle nie nadaje decyzji klauzuli. Na wniosek strony wydaje **zaświadczenie**”; „**zaświadczenie administracyjne** (art. 217 k.p.a.)” |
| R3 | 1/1 | oba przymioty i zaświadczenie o prawomocności — sekcje 2 i 3 rozróżniają ostateczność (art. 16 § 1) i prawomocność (art. 16 § 3); „potwierdza, że decyzja jest ostateczna i prawomocna, wydając zaświadczenie” |
| R4 | 1/1 | mechanizm — „upłynie 30-dniowy termin na skargę do WSA (art. 53 § 1 p.p.s.a.)”; „Wniosek o ponowne rozpatrzenie nie jest obowiązkowy. Stronie od razu przysługuje skarga do WSA (art. 52 § 3 p.p.s.a.)” |
| K1 | 0 | nie zaleca wniosku do sądu o klauzulę — wprost wyklucza („pojęcie »klauzuli prawomocności« z art. 363 i 364 k.p.c. tu nie ma zastosowania”) |
| K2 | 0 | nie twierdzi, że obywatel Ukrainy nie potrzebuje zezwolenia — „Specustawa ukraińska … nie wprowadziła ogólnego zwolnienia” |
| K3 | 0 | nie wyklucza prawomocności i nie mówi „wyłącznie ostateczność” — przeciwnie, sekcja 3 „decyzja administracyjna może być też **prawomocna**” (reguła klucza: samo „co do zasady” płaci w A-R) |
| **A** | **8 / 9 = 88.9 %** | punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d); suma 1 + 1 + 1 + 1 + 4 = 8; bez kar |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 2/2 | 2: prawnik wie, do kogo i o co wystąpić (zaświadczenie MSWiA, art. 217 k.p.a., opłata 17 zł), kiedy decyzja jest ostateczna i prawomocna (14 i 30 dni, zrzeczenie), co sprawdzić u notariusza i czy zezwolenie jest w ogóle potrzebne (art. 8); bez błędu co do kwoty, terminu, organu ani formy |
| B2 kalibracja | 1/1 | 1 (`kategoryczna`): tezy postawione wprost; „co do zasady” dotyczy rozróżnienia pojęć, nie rozmywa wskazówki co do zaświadczenia |
| **B** | **3 / 3 = 100.0 %** | |

**Δ = A % − B % = −11.1** · hallucinated: nie · bez weryfikacji źródła: nie — w źródłach odpowiedzi strona MSWiA (gov.pl, serwis organu publicznego — README: źródło oficjalne), z której pochodzą: brak klauzuli, zaświadczenie, opłata 17 zł; pozostałe trzy adresy to serwisy wtórne (e-prawnik.pl, totalmoney.pl, poradnikprzedsiebiorcy.pl)

## Pochodzenie (opisowe)

P1 ślady narzędzi: niezachowane; liczniki `server_tool_use` 0/0 nie obejmują narzędzi klienckich Claude Code; `model_id` zawiera `claude-haiku-5-5`, co pasuje do WebFetch: w Claude Code ten tool streszcza pobraną stronę małym modelem (Haiku), więc Opus dostaje streszczenie, a nie tekst źródła · P2 nie badano · P3 źródła deklarowane w tekście: gov.pl/web/mswia/najczesciej-zadawane-pytania (HTTP 200, treść zgodna z odpowiedzią), e-prawnik.pl, totalmoney.pl, poradnikprzedsiebiorcy.pl; ustawy podane bez adresów ELI/ISAP · P4 źródło urzędowe (serwis MSWiA) dla praktyki; przepisy k.p.a./p.p.s.a./u.n.n.c. bez śladu odczytu tekstu aktu, ale wszystkie trafne. Profil: obie pułapki skorygowane, wiodące „co do zasady ostateczność” złagodzone przez praktykę MSWiA w tym samym akapicie. Karta W0 tego modelu dla P04 jeszcze niewypełniona — bez porównania

Weryfikacja: api.sejm.gov.pl (pdftotext): DU/2017/2278, DU/2025/1691, DU/2016/23, DU/2017/935, DU/2026/143, DU/2022/583; legal-cite: k.p.c. art. 363 § 1, 364 § 1; gov.pl MSWiA FAQ (curl, odczyt HTML). legal-cite nie obsługuje u.n.n.c., k.p.a. ani p.p.s.a. (zgodnie z polem `weryfikacja` klucza).

Specyfikacja oceny: v1.0.1 (2026-10-11) z przykładami granicznymi z 2026-10-17 oraz zasadami soft law, A6_zakres, blokady dostawcy i regułami B1–B7 z 2026-10-18 — karta wypełniona wstępnie 2026-10-18.
