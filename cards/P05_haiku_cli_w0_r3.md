# Karta oceny — P05 · Claude claude-haiku-5-5 przez Claude Code CLI (czysty model, bez narzędzi), W0 bez wyszukiwania — r3

- Pytanie: P05 (katalog nr 38), klucz w wersji 2 (2026-10-10)
- Data odpowiedzi systemu: 2026-10-10 · czas 20.3 s · warunki: model claude-haiku-5-5 (model_id claude-haiku-5-5), Claude Code CLI (subskrypcja), bez narzędzi, MCP i CLAUDE.md, temperatura: domyślna CLI (nieustawialna), narzędzia: brak, wyszukiwanie: brak (W0); prompt_systemowy: „Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne.”; kontekst dodatkowy: sekcja środowiska Claude Code (katalog tymczasowy, data, platforma, e-mail konta); tokeny: wejście 2 (+814 zapis do pamięci podręcznej), wyjście 4053, w tym rozumowanie 2451
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 0/2 | 0: odpowiedź opisuje inny mechanizm niż rdzeń klucza — „Doręczenie elektroniczne osobie fizycznej odbywa się głównie w systemie **e-Doręczeń** (adres do doręczeń elektronicznych, ADE) albo przez inny system teleinformatyczny, np. ePUAP”; Portal Informacyjny, art. 131¹ᵃ k.p.c., zmiana od 1.06.2026 i wybór tego sposobu przez stronę nie padają; do decyzji Adama — 1, jeżeli za trafny kierunek uznać samo „osobie fizycznej można doręczać elektronicznie” z regułą 14 dni |
| A2 | 0/1 | 0: brak art. 131¹ᵃ § 1, § 1¹ i § 2 k.p.c.; powołano art. 131, 132–146, 136, 139, 168 k.p.c. i ustawę o doręczeniach elektronicznych |
| A3 | n/d | system nie cytuje dosłownie |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 0/1 | [2026-10-11 A6 binarne: ½→0, A6_typ: [T], A6_pochodzenie: art. 131 k.p.c.: pamięć — dawne S przeliczone na T: wskazanemu art. 131 przypisano treść cudzą („doręczenia elektroniczne”, norma w art. 131¹ § 1), a błędny numer u modelu jest twierdzeniem o treści przepisu, nie omyłką; bieg W0 bez narzędzi] **A6_zakres: rdzeń** [2026-10-25 uzupełnione, do przeglądu Adama: T: art. 131 k.p.c. przypisano „doręczenia elektroniczne”, na których opiera się główna (błędna) konkluzja o drodze doręczeń dla osoby fizycznej] · A6_typ: [S]. Sprawdzone 7 z 7 (ISAP DU/2026/468 k.p.c.; DU/2026/3 t.j. ustawy o doręczeniach elektronicznych). **S**: „art. 131 (doręczenia elektroniczne)” k.p.c. — art. 131 dotyczy doręczeń przez operatora pocztowego, osoby zatrudnione w sądzie, sądową służbę doręczeniową i komornika; „doręczenie elektroniczne” definiuje art. 131¹ § 1 (zgubiony indeks, treść zgodna z art. 131¹); do decyzji Adama — T (0, hallucinated) przy ścisłym odczycie reguły 2 („źródło nie dotyczy przypisanej kwestii”), bo system nie wskazał paragrafu, tylko cały artykuł o innej treści. ✓: art. 132–146 („ogólne zasady doręczeń, w tym doręczenie zastępcze i awizo” — art. 138 i 139 w tym zakresie); ustawa z 18.11.2020 o doręczeniach elektronicznych (istnieje, data zgodna; reguluje ADE i skutki doręczenia); „art. 136 i nast.” jako doręczenie tradycyjne (art. 136 to obowiązek zawiadamiania o zmianie adresu, dalsze artykuły o doręczeniu właściwym i zastępczym — odesłanie luźne, bez klasy); 14 dni „z ustawy o doręczeniach elektronicznych” (art. 41 ust. 1 pkt 3 i art. 42 ust. 2: doręczenie w dniu następującym po upływie 14 dni od wpłynięcia na ADE podmiotu niepublicznego); „por. też art. 139” (awizo, dwukrotne 7 dni); art. 168 i nast. (przywrócenie terminu). Bez klasy, do decyzji Adama: twierdzenie, że sądy w sprawach cywilnych doręczają osobom fizycznym przez e-Doręczenia albo ePUAP, nie ma powołanego przepisu i jest błędem merytorycznym rozliczonym w A-R i A2 (w karcie P05_bielik_11b_v3_q8_chmura przypisanie ustawie o doręczeniach elektronicznych regulacji Portalu Informacyjnego dało T; tu system o Portalu Informacyjnym nie pisze, ustawie przypisuje tylko e-Doręczenia). Orzeczeń nie powołano (SAOS: 0 sprawdzeń). Brzmienia art. 131¹ᵃ sprzed 1.06.2026 system nie przytacza — nie W |
| A8 | 1/1 | każdy akapit dotyczy doręczeń elektronicznych osobie fizycznej (krąg adresatów, przebieg, moment doręczenia, skutki dla terminów); końcowe zdanie z pytaniem o rodzaj postępowania to jednozdaniowa oferta |
| R1 | 0/1 | osoba fizyczna może otrzymywać doręczenia przez portal, jeżeli wybierze ten sposób — ✗ (jest „gdy mają ADE lub konto na systemie, z którego sąd korzysta, i nie wnoszą sprzeciwu”: inny system i model braku sprzeciwu zamiast wyboru) |
| R2 | 0/1 | sposób złożenia oświadczenia o wyborze (przez portal, jeden z trzech podpisów) — ✗ brak |
| R3 | 1/1 | moment doręczenia z regułą 14 dni — „doręczenie jest skuteczne z chwilą odbioru”, „z **upływem 14 dni** od dnia udostępnienia pisma w systemie”; treść zgodna z art. 131¹ᵃ § 2, podstawa wskazana błędnie (rozliczone w A2); do decyzji Adama — 0, jeżeli punkt wymaga odniesienia do portalu |
| R4 | 0/1 | możliwość rezygnacji — ✗ brak |
| K1 | 0 | osobie fizycznej bez pełnomocnika nie można doręczać przez portal — nie dotyczy (takiej tezy nie ma) |
| K2 | 0 | stosuje art. 139 k.p.c. (awizo) do doręczenia portalowego — bez kary wstępnie: art. 139 pada tylko porównawczo („por. też art. 139 KPC”, „Skutki nieodebrania są takie same jak przy awizo”); do decyzji Adama — −1, jeżeli porównanie uznać za zastosowanie (wtedy A 1,5 / 9 = 16.7 %) |
| **A** | **2 / 9 = 22.2 %** | punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d); bez kar [2026-10-11: było 2,5 / 9 = 27.8 %, Δ −38.9; A6 ½→0] |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 1/2 | 1: prawnik dostaje trafne ostrzeżenie o fikcji doręczenia po 14 dniach i o biegu terminów od tej chwili, ale zostaje skierowany do e-Doręczeń i ADE zamiast do Portalu Informacyjnego i oświadczenia o wyborze (błąd co do systemu i formy zmienia działanie — najwyżej 1); do decyzji Adama — 0, jeżeli błędny system przesądza |
| B2 kalibracja | 1/1 | 1 (`kalibracja_oczekiwana: kategoryczna`): tezy postawione wprost („Sąd doręcza im pisma elektronicznie głównie wtedy, gdy…”, „doręczenie uznaje się za dokonane z upływem 14 dni”); jedno zdanie o sprawdzeniu aktualnego tekstu nie rozmywa tezy; błąd płaci w bloku A |
| **B** | **2 / 3 = 66.7 %** | |

**Δ = A % − B % = −44.5** · hallucinated: tak (A6_typ T; 2026-10-11 A6 binarne, było: nie; A6_zakres: rdzeń [2026-10-25 uzupełnione]) · bez weryfikacji źródła: tak (brak narzędzi)

## Pochodzenie (opisowe)

P1 ślady narzędzi: brak (narzedzia: [], wyszukiwanie: false; web_search_requests 0, web_fetch_requests 0) · P2 nie badano; noweli z 5.08.2025 (Dz.U. 2025 poz. 1172, w życie 1.06.2026) odpowiedź nie zna · P3 źródła deklarowane w tekście: k.p.c. (art. 131, 132–146, 136, 139, 168), ustawa z 18.11.2020 o doręczeniach elektronicznych; bez orzeczeń i linków · P4 wiedza z wag modelu. Warunki biegu z nagłówka odpowiedzi: model_alias i model_id claude-haiku-5-5, Claude Code CLI (subskrypcja), temperatura domyślna CLI (nieustawialna), kontekst dodatkowy: sekcja środowiska Claude Code, czas 20.3 s, koszt równoważny 0.0024 USD, prompt_systemowy jak w metryce karty

Specyfikacja oceny: v1.0 (2026-10-11) — karta oceniona lub przeliczona według README w tej wersji.
