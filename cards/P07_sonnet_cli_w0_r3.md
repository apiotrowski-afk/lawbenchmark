# Karta oceny — P07 · Claude Sonnet przez Claude Code CLI (czysty model, bez narzędzi), W0 bez wyszukiwania — r3

- Pytanie: P07 (katalog nr 24), klucz w wersji 2 (2026-10-10)
- Data odpowiedzi systemu: 2026-10-10 · czas 42.9 s · warunki: model_id `claude-haiku-5-5,claude-sonnet-5-5` (alias claude-sonnet-5-5), Claude Code CLI (subskrypcja), bez narzędzi, MCP i CLAUDE.md; wyszukiwarka: brak (W0); liczba wyszukań: 0; tokeny: wyjście 5654, w tym rozumowanie 4336
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 1/2 | 1: kierunek trafny w pierwszym zdaniu — „**Tak, wniosek o uzasadnienie można złożyć, mimo że sąd ustnie podał zasadnicze powody rozstrzygnięcia.**”, z terminem tygodnia od ogłoszenia albo doręczenia; brak kluczowego warunku rdzenia: postanowienie musi podlegać zaskarżeniu (nie pada); odpowiedź osadzona w ustnych motywach wyroku (art. 326 § 3), nie w art. 357 § 5 zd. 2, o który pytano; do decyzji Adama (1 czy 2) |
| A2 | 0/1 | 0: art. 357 § 5 pada tylko w zastrzeżeniu („nie mogę zweryfikować aktualnego brzmienia art. 357 § 5 k.p.c.”), bez treści; termin oparty na art. 357 § 2 zamiast § 1 albo § 2¹ |
| A3 | n/d | system nie cytuje dosłownie przepisów |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 0/1 | [2026-10-11 A6 binarne: 0→0, A6_typ: [T, W], A6_pochodzenie: pamięć (wszystkie błędne powołania) — bieg bez narzędzi i bez wyszukiwania (W0), więc treść powołań pochodzi z wag modelu] **A6_zakres: rdzeń** [2026-10-25 uzupełnione, do przeglądu Adama: T: termin wniosku przypisano art. 357 § 2 zamiast § 1 albo § 2¹, czyli podstawie wymaganej i elementowi rubryki (termin)] · A6_typ: [T, W]. Sprawdzone 9 z 9 (ISAP DU/2026/468, DU/2025/1228; wersja dawna k.p.c.: DU/2018/1360). **T nr 1**: „Wniosek o uzasadnienie składa się w terminie tygodnia od ogłoszenia postanowienia lub od jego doręczenia … (art. 357 § 2 k.p.c.)” — § 2 dotyczy doręczenia z urzędu postanowień wydanych na posiedzeniu niejawnym i pouczenia strony; terminy są w § 1 (od ogłoszenia) i § 2¹ (od doręczenia); także w t.j. 2018 § 2 terminu nie zawierał (wskazana jednostka z cudzą treścią, norma w sąsiednich jednostkach). **T nr 2** (do decyzji Adama: T, F czy S): „Wniosek podlega opłacie 100 zł … (art. 328 § 1 zd. 2 k.p.c.)” — art. 328 § 1 ma jedno zdanie i o opłacie nie mówi; w t.j. 2018 zd. 2 dotyczyło odrzucenia wniosku spóźnionego; opłata 100 zł jest w art. 25b ust. 1 u.k.s.c. (teza trafna, przepis przypisany innej ustawie — przy kwalifikacji S: ½, ale T nr 1 i tak daje 0). **W**: „Jeżeli wyroku nie ogłoszono, termin liczy się od doręczenia sentencji (art. 328 § 1 k.p.c.)” — brzmienie § 1 sprzed noweli z 2019 r. (t.j. 2018: „od dnia doręczenia sentencji”); dziś § 2: „gdy wyrok doręcza się z urzędu … od dnia doręczenia wyroku”. Zgodne: art. 326 § 3 ✓ (po ogłoszeniu wyroku podaje się ustnie zasadnicze powody rozstrzygnięcia); art. 327¹ ✓ (treść uzasadnienia wyroku); art. 328 § 1 ✓ co do tygodnia od ogłoszenia; art. 369 § 1 ✓ (apelacja w dwa tygodnie od doręczenia wyroku z uzasadnieniem); art. 394 § 2 ✓ (zażalenie w tydzień od doręczenia postanowienia z uzasadnieniem); art. 168 § 1 ✓; art. 169 § 1 i 2 ✓ (tydzień od ustania przyczyny; w ustawie „uprawdopodobnić”, nie „wykazać”). Bez powołania (poza A6, liczone w B1): „termin na zaskarżenie biegnie wtedy od doręczenia orzeczenia bez uzasadnienia” — nieaktualne co do wyroku (art. 369 § 2 uchylony; apelacja wymaga wniosku o uzasadnienie). Orzeczeń nie powołano (SAOS: 0 sprawdzeń). Najgorszy przypadek: T → 0 |
| A8 | ½/1 | ½: pytanie dotyczy postanowienia i art. 357 § 5; punkt „**Wyrok:**” (termin, opłata, art. 328) i oparcie sekcji 1 na art. 326 § 3 i 327¹ to scenariusz, którego pytanie nie zakłada, plus akapit o przywróceniu terminu (art. 168–169); rdzeń jest w pierwszym zdaniu i dygresje go nie przykrywają; zastrzeżenie końcowe z pytaniem „wyrok czy postanowienie” neutralne |
| R1 | 1/1 | „tak” i zasadnicze powody nie są uzasadnieniem — „Tak, wniosek o uzasadnienie można złożyć”; „Nie jest uzasadnieniem w rozumieniu art. 327¹ k.p.c. i nie wyłącza prawa strony do żądania uzasadnienia pisemnego”; do decyzji Adama: wywód dotyczy ustnych motywów przy wyroku „analogicznie przy postanowieniu”, a nie odróżnienia z art. 357 § 5 zd. 2 |
| R2 | 0/1 | warunek: postanowienie musi podlegać zaskarżeniu — ✗ brak |
| R3 | 1/1 | termin tygodniowy i jego początek — „w terminie tygodnia od ogłoszenia postanowienia lub od jego doręczenia, jeżeli było doręczane bez ogłoszenia” (błędny paragraf liczony w A2 i A6) |
| R4 | 0/1 | opłata od wniosku albo wyjątki z § 2³–§ 2⁴ lub § 6 — ✗ wstępnie: opłata 100 zł podana tylko przy wyroku i z błędną podstawą, przy postanowieniu brak (art. 25b ust. 1–2 u.k.s.c.: 100 albo 30 zł); zdanie „Uzasadnienie z urzędu dotyczy postanowień wymienionych w tym przepisie” nie mówi, że doręczenie z urzędu zwalnia z wniosku; do decyzji Adama, czy wzmianka o opłacie od wniosku wystarcza (wtedy 1) |
| K1 | 0 | wskazanie zasadniczych powodów zastępuje uzasadnienie albo zamyka drogę do wniosku — nie dotyczy (przeciwnie) |
| K2 | 0 | termin dwóch tygodni na wniosek — nie dotyczy („7 dni”, „tygodnia”; dwa tygodnie nie padają) |
| **A** | **3½ / 9 = 38.9 %** | punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d); bez kar |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 1/2 | 1: prawnik wie, że wniosek trzeba złożyć w tydzień i że wysłuchanie motywów nie zwalnia z terminu; ale nie dowie się, że przy postanowieniu niezaskarżalnym wniosek jest bezprzedmiotowy, dostanie błędny paragraf (art. 357 § 2) i nieaktualną wskazówkę o biegu terminu do zaskarżenia bez wniosku o uzasadnienie (zmienia działanie — B1 najwyżej 1) |
| B2 kalibracja | 1/1 | 1 (`kalibracja_oczekiwana: kategoryczna`): teza wprost („Tak, wniosek o uzasadnienie można złożyć”); końcowe zastrzeżenie o braku weryfikacji brzmienia art. 357 § 5 to formułka, tezy nie rozmywa (do decyzji Adama) |
| **B** | **2 / 3 = 66.7 %** | |

**Δ = A % − B % = −27.8** · hallucinated: tak (A6_typ T; A6_zakres: rdzeń [2026-10-25 uzupełnione]) · bez weryfikacji źródła: tak (brak narzędzi)

## Pochodzenie (opisowe)

P1 ślady narzędzi: brak (W0; narzedzia [], wyszukiwanie false, web_search_requests 0, web_fetch_requests 0) · P2 nie badano · P3 źródła deklarowane w tekście: k.p.c. (art. 168 § 1, 169 § 1–2, 326 § 3, 327¹, 328 § 1, 357 § 2 i § 5, 369 § 1, 394 § 2); bez linków i bez orzeczeń; system odsyła do ISAP lub LEX/Legalis · P4 wiedza z wag modelu, w części ze stanu sprzed noweli z 2019 r. (art. 328 § 1 z „doręczeniem sentencji”, bieg terminu do zaskarżenia bez wniosku o uzasadnienie); treści art. 357 § 5 system nie przytacza.

Warunki biegu (z nagłówka odpowiedzi): system „Claude claude-sonnet-5-5 przez Claude Code CLI (subskrypcja), czysty model — bez narzędzi, MCP i CLAUDE.md, W0” · model_alias `claude-sonnet-5-5` · model_id `claude-haiku-5-5,claude-sonnet-5-5` · prompt_systemowy: „Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne.” · narzedzia: [] · wyszukiwanie: false · temperatura: domyślna CLI (nieustawialna) · kontekst_dodatkowy: sekcja środowiska Claude Code (katalog tymczasowy, data, platforma, e-mail konta) — nie da się wyłączyć.

Specyfikacja oceny: v1.0 (2026-10-11) — karta oceniona lub przeliczona według README w tej wersji.
