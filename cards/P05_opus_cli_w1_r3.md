# Karta oceny — P05 · Claude opus przez Claude Code CLI (subskrypcja), czysty model — bez MCP i CLAUDE.md, W1: WebSearch + WebFetch — r3 W1

- Pytanie: P05 (katalog nr 38), klucz w wersji 2 (2026-10-10; kalibracja kategoryczna)
- Data odpowiedzi systemu: 2026-10-17 · czas 99.0 s · warunki: model_id `claude-haiku-5-5,claude-opus-5-5` (alias opus), Claude Code CLI (subskrypcja), bez MCP i CLAUDE.md; narzędzia: WebSearch + WebFetch (W1); prompt systemowy z dopiskiem o wyszukiwaniu i adresach źródeł; liczniki `server_tool_use`: web_search_requests 0, web_fetch_requests 0 (narzędzia Claude Code działają po stronie klienta, liczniki ich nie obejmują); ślad narzędzi niezachowany
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 2/2 | 2: pierwszy akapit — „sąd doręcza pisma przez Portal Informacyjny … tylko wtedy, gdy sama wybrała ten sposób w danej sprawie … nowelizacja k.p.c. obowiązująca od 1 czerwca 2026 r.”; oświadczenie przez portal z jednym z trzech podpisów (sekcja 3), chwila z dokumentu potwierdzającego i 14 dni (sekcja 5); pułapka aktualności ominięta |
| A2 | 1/1 | wszystkie trzy podstawy wymagane: „art. 131¹ᵃ § 1 k.p.c.” (sekcja 2), „art. 131¹ᵃ § 1¹ k.p.c.” (sekcja 3), „art. 131¹ᵃ § 2 k.p.c.” (sekcja 5) |
| A3 | n/d | system nie cytuje dosłownie (parafrazy) |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 0/1 | A6_typ: [W] · **A6_zakres: poboczne** [2026-10-25 uzupełnione, do przeglądu Adama: jedyne W to art. 133a k.p.k. w dygresji o postępowaniu karnym; konkluzja i podstawy z art. 131¹ᵃ § 1, § 1¹, § 2 k.p.c. trafne] · A6_pochodzenie: art. 133a k.p.k.: pamięć — wśród ośmiu adresów źródeł nie ma k.p.k., a sam system pisze „Według dostępnych mi informacji … Nie sprawdziłem”. Sprawdzone 16 z 16. k.p.c. (legal-cite: t.j. Dz.U. 2026 poz. 468, nieurzędowy odczyt PDF z api.sejm.gov.pl, brzmienie od 1.06.2026): art. 131¹ᵃ § 1 ✓ (krąg profesjonalistów, „a także stronie, która dokonała wyboru”; pominięcie organu emerytalnego to pominięcie, nie błąd), § 1¹ ✓ (wybór przez portal z podpisem kwalifikowanym, zaufanym albo osobistym; rezygnacja także na piśmie; skutek z chwilą zawiadomienia sądu), § 2 ✓ (chwila z dokumentu potwierdzającego; „Przepisu art. 134 § 1 nie stosuje się”; 14 dni od umieszczenia w portalu), § 3 ✓ (odstąpienie ze względu na charakter pisma, uwierzytelniony odpis orzeczenia, tytuł wykonawczy; „może” zamiast „zarządza” to parafraza), § 4 ✓ (delegacja do rozporządzenia MS); art. 131 § 1 ✓ (operator pocztowy, sądowa służba doręczeniowa, komornik); art. 134 § 1 ✓; art. 165 § 2 ✓ (nadanie w placówce = wniesienie; wniosek, że nie stosuje się go do rezygnacji, to wywód z § 1¹ zd. 3, nie przypisanie treści przepisowi); art. 131¹ § 1–2¹ ✓ (system teleinformatyczny, 14 dni, rezygnacja z § 2¹); art. 131² ✓ uchylony (przez art. 1 pkt 12 ustawy z 5.08.2025); art. 168 i nast. ✓; Dz.U. 2026 poz. 468 ✓ t.j.; ustawa z 5.08.2025, Dz.U. 2025 poz. 1172 ✓ (ISAP: art. 16 pkt 3 — art. 1 pkt 11 lit. a i b, czyli § 1 i § 1¹, od 1.06.2026 ✓; reszta ustawy od 1.03.2026, ale art. 1 pkt 11 lit. c, czyli zmiana § 2 zd. 3 art. 131¹ᵃ, weszła w życie 14 dni po ogłoszeniu, ok. 10.09.2025 — zdanie „pozostałe zmiany dotyczące portalu 1 marca 2026 r.” jest więc nieścisłe; **do decyzji Adama**, czy to drugie W, „błędna data wejścia w życie”; wstępnie nie, bo zdanie ogólne i dla większości zmian prawdziwe; punktu nie zmienia). **W**: „W postępowaniu karnym obowiązuje osobna regulacja (art. 133a k.p.k.). … obejmuje ona prokuratorów, obrońców, profesjonalnych pełnomocników i Prokuratorię Generalną, a nie strony będące osobami fizycznymi” — to realne brzmienie art. 133a § 1 k.p.k. sprzed 1.06.2026; t.j. Dz.U. 2026 poz. 490 (ISAP, PDF), odnośniki 42–43: od 1.06.2026 § 1 obejmuje też „stronie, która dokonała wyboru takiego sposobu doręczania”, a § 1a reguluje oświadczenie o wyborze. Zastrzeżenie „Nie sprawdziłem, czy nowelizacja z 2025 r. zmieniła to także w k.p.k.” nie znosi fałszywego zdania „a nie strony” (README, reguła 8: uczciwe „nie wiem” liczy się w B2); **do decyzji Adama**, czy zdanie z takim zastrzeżeniem traktować jako twierdzenie. Rozporządzenie MS: tylko podstawa z § 4 ✓, bez daty i pozycji |
| A8 | 1/1 | każdy akapit służy odpowiedzi; pytanie nie ogranicza się do procedury cywilnej, więc punkt o k.p.k. jest w zakresie (błąd w nim płaci w A6); odróżnienie od art. 131¹ i e-Doręczeń to krótkie tło; uwaga o przywróceniu terminu i zastrzeżenie końcowe — neutralne |
| R1 | 1/1 | osoba fizyczna może otrzymywać doręczenia przez portal, jeżeli wybierze — „na wniosek stronie, która wybrała ten sposób doręczeń. Dotyczy to także osoby fizycznej działającej bez pełnomocnika” |
| R2 | 1/1 | sposób złożenia oświadczenia — „Wybór składa się przez portal … podpisać kwalifikowanym podpisem elektronicznym, podpisem zaufanym albo podpisem osobistym” |
| R3 | 1/1 | moment doręczenia i 14 dni — „w chwili wskazanej w dokumencie potwierdzającym doręczenie”; „pismo uznaje się za doręczone po 14 dniach od dnia umieszczenia go w portalu” |
| R4 | 1/1 | rezygnacja na piśmie, skutek od zawiadomienia sądu — „Rezygnację można złożyć przez portal … albo na piśmie. Rezygnacja zaczyna działać dopiero z chwilą zawiadomienia sądu” |
| K1 | 0 | nie twierdzi, że osobie fizycznej bez pełnomocnika nie można doręczać przez portal — przeciwnie |
| K2 | 0 | nie stosuje art. 139 k.p.c. (awizo) |
| **A** | **8 / 9 = 88.9 %** | punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d); suma 8, bez kar |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 2/2 | 2: krąg adresatów, tryb wyboru i rezygnacji z podpisami, katalog pism, chwila doręczenia i fikcja 14 dni, skutek dla terminów („Fikcja doręczenia otwiera bieg terminów”), przywrócenie terminu; błąd co do k.p.k. dotyczy procedury pobocznej i płaci w A6 |
| B2 kalibracja | 1/1 | 1 (`kategoryczna`): teza wprost w pierwszym zdaniu; zastrzeżenia (rozporządzenie, k.p.k., porównanie z ISAP) dotyczą spraw pobocznych i nie rozmywają tezy |
| **B** | **3 / 3 = 100.0 %** | |

**Δ = A % − B % = −11.1** · hallucinated: tak (A6_typ W — art. 133a k.p.k.; A6_zakres: poboczne [2026-10-25 uzupełnione]) · bez weryfikacji źródła: tak (tylko źródła wtórne) — osiem adresów: jklaw.pl, arslege.pl (2), lexlege.pl, kpmg.com, staskiewicz.eu, kirp.pl, adcasum.pl; Dz.U. 2026 poz. 468 i 2025 poz. 1172 wymienione bez adresu; ślad narzędzi niezachowany

## Pochodzenie (opisowe)

P1 ślady narzędzi: niezachowane; liczniki `server_tool_use` 0/0 nie obejmują narzędzi klienckich Claude Code; `model_id` zawiera `claude-haiku-5-5`, co pasuje do WebFetch: w Claude Code ten tool streszcza pobraną stronę małym modelem (Haiku), więc Opus dostaje streszczenie, a nie tekst źródła · P2 nie badano · P3 źródła deklarowane w tekście: osiem adresów serwisów kancelarii, komentarzy i samorządu (bez ISAP/ELI i gov.pl); dzienniki publikacyjne podane bez linków · P4 źródła wtórne; treść k.p.c. zgodna z brzmieniem od 1.06.2026, a błąd co do k.p.k. pochodzi z wag modelu (stan sprzed noweli). Względem W0 (`P05_opus_cli_w0_r3`): z wyszukiwaniem trafione art. 131¹ᵃ zamiast 131¹, trzy podpisy i data 1.06.2026 (A 55.6 → 88.9 %); nowy błąd w dopisku o k.p.k.

Weryfikacja: legal-cite (k.p.c., t.j. Dz.U. 2026 poz. 468, odczyt PDF — status „nieurzędowy odczyt”, aktualność po t.j. nieustalona: 6 nowel; klucz sprawdził nowele dla art. 131¹ᵃ); ISAP/api.sejm.gov.pl: DU/2025/1172 (art. 1 pkt 11, art. 16), DU/2026/490 (k.p.k. t.j., art. 133a z odnośnikami 41–46).

Specyfikacja oceny: v1.0.1 (2026-10-11) z przykładami granicznymi z 2026-10-17 — karta wypełniona wstępnie 2026-10-18.
