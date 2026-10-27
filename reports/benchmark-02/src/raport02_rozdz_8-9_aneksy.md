## 8. Ograniczenia

### 8.1. Zakres interpretacji wyników

1. **Jeden prawnik.** Wszystkie karty sprawdził jeden prawnik, Adam Piotrowski. Karty wypełniał wstępnie model Claude, a więc model z rodziny trzech ocenianych systemów. Nie mamy drugiego oceniającego, więc nie znamy zgodności człowiek–człowiek, do której należałoby odnieść κ sędziów-modeli. κ w rozdziałach 6 i 7 to zgodność modelu z kartą zamkniętą przez człowieka.
2. **Kolejność kart i sędziów w pilotażu.** Karty pytań pilotażowych sprawdzano po obejrzeniu ocen sędziów, a sporne punkty rozstrzygano często na korzyść argumentu sędziego. Zgodność na tej części, w tym κ „bez raportu” w porównaniu z kartą meta (rozdział 7.5), jest zawyżona. Kierunek zmian między wariantami raportu jest mimo to jednoznaczny.
3. **Zbiór kalibracyjny.** Reguły oceny zmienialiśmy po lekturze odpowiedzi (tabela 3), a klucze P09 i P10 zmieniono po zebraniu odpowiedzi (rozdział 2.3). Wyniki nie są pomiarem według zamrożonej specyfikacji.
4. **Mała próba.** Dziesięć pytań, w tym pięć z postępowania cywilnego, jedno uruchomienie każdego systemu; dla wyników ocenianych modeli z rozdziału 5 nie oszacowano przedziałów niepewności ani nie przeprowadzono formalnych porównań sparowanych (przedziały dla κ sędziów są w aneksie E). Różnice o jedną–dwie odpowiedzi między modelami mieszczą się w zmienności, której nie mierzyliśmy.
5. **Warunki biegu.** W W1 modele Claude czytały strony przez streszczenie wykonane przez Claude Haiku 5.5, a Claude Code nie zachowuje śladu narzędzi, więc 5 z 40 halucynacji w W1 ma pochodzenie nieustalone z tego powodu (3 dalsze dotyczą modeli Gemini, u których ślad nie wskazywał źródła błędu). Claude Code CLI dokleja do polecenia sekcję środowiska z danymi konta, której nie da się wyłączyć. Koszt W1 dla Claude i Gemini jest dolną granicą.
6. **Sędziowie.** Sędziowie na pytaniach rozszerzenia startowali przed dopisaniem do specyfikacji reguł B9–B12. GPT-6 Astra ocenił tylko część kart. Dla sędziów Codex do 25 października logowaliśmy tylko liczbę wyszukań, nie zapytania i źródła. Powtórzeń biegu sędziego nie badaliśmy.
7. **Warstwa weryfikacji.** Parser i prompty strojono na P09 i P10; test na ośmiu pytaniach jest pierwszym pomiarem poza strojeniem. Karty meta v2 Gemini 4 Argon pochodzą z dwóch wersji raportu („b” i „c”). Wariant v3 ma komplet kart GPT-6.1 Sol i 127 z 128 kart Gemini 4 Argon.
8. **Literatura.** Większość prac o sędziach-modelach, na które się powołujemy [3]–[6], to preprinty z 2026 r. bez recenzji; w przeglądzie literatury czytaliśmy ich streszczenia, nie pełne teksty.

### 8.2. Niespójności w danych wykryte przy składaniu raportu

Raport liczy wszystkie wartości z kart w stanie z 25 października 2026 r. Przy składaniu wykryliśmy rozbieżności między kartami a wcześniejszymi zestawieniami i zapisami; liczby w raporcie ich nie powielają, ale wymagają one poprawienia u źródła.

- Zestawienie W0/W1 z 19.10 (aktualizacja z 23.10) podaje dla Claude Opus 5.5 W1 4 odpowiedzi poprawnie ugruntowane, ale koszt na odpowiedź ≥ 0,489 USD, co odpowiada trzem (1,467 / 3). Na obecnych kartach: 4 odpowiedzi i ≥ 0,367 USD.
- Wcześniejsza notatka robocza (A18) podaje dla Claude Opus 5.5 halucynacje 9 → 6 i odpowiedzi poprawnie ugruntowane 0 → 3; po decyzji z 23.10 (B9) karty dają 9 → 5 i 0 → 4. Wpis A14 („wyszukiwanie dokłada najwyżej 1–2 poprawnie ugruntowane odpowiedzi”) jest nieaktualny: u Claude Opus 5.5 przyrost wynosi 4.
- Zestawienie z 19.10 podaje κ sędziów na rozszerzeniu 0,92 / 0,82 / 0,78 / 0,56; na obecnych kartach 0,90 / 0,80 / 0,80 / 0,58 (rozdział 6.2). Artykuł v1.2 (opublikowany 26.10) podaje obie serie: na kartach w stanie pierwotnym i na obecnych. Zdanie z notatki roboczej (B11) i z artykułu, że kolejność sędziów według wyszukań jest taka sama jak według κ, nie jest ścisłe: Gemini 3.1 Pro wyszukiwał mniej niż Gemini 3.8 Flash (4,3 wobec 4,7), a ma wyższą κ.
- Karta `P12_gemini38flash_vertex_w1_r3` miała etykietę „bez weryfikacji źródła: tak (brak narzędzi)”, choć bieg W1 miał narzędzia, a model ich nie użył. Decyzją z 25.10 etykietę poprawiono na „narzędzia nieużyte” według reguły z 18.10. Dziennik z 18.10 podaje 9 kart „narzędzia nieużyte”, po tej poprawce jest ich 12.
- Pole `A6_zakres` było tylko w kartach pytań rozszerzenia. W 49 kartach z halucynacją na pytaniach pilotażowych go brakowało, w tym w kartach wskazanych w specyfikacji jako wzory zakresu (`P05_sonnet_cli_w1_r3`, `P12_argon4_high_vertex_w1_r3`, `P07_sonnet_cli_w1_r3`). Uzupełniono je 25.10 (35 rdzeń, 14 poboczne); 7 przypadków granicznych rozstrzygnęły dwie reguły z tego dnia, 4 pozostają do przeglądu prawnika.
- Karta `P07_opus_cli_w0_r3` zawiera nadal klasę O (zniesioną 11.10) w adnotacji historycznej; punkt i etykieta wynikają z klasy T.
- Klucze P05, P06 i P07 nie mają pola `status`, wymaganego zasadą 7 specyfikacji.
- P01 ma w kluczu typ `obliczenie`, jak wyłączone P02, którego powodem wyłączenia był charakter obliczeniowy. Decyzją z 25.10 uznaliśmy to za spójne: odpowiedź P01 to kwota zapisana wprost w ustawie (800 zł w art. 119 § 1 k.w.), więc pytanie sprawdza treść prawa, a nie rachunek.
- Brak pliku oceny Gemini 4 Argon dla karty `P09_argon4_high_vertex_w1_r3`, choć projekt meta-sędziego i notatka robocza (B8) liczą tę kartę jako przeoczenie Argona.
- Skrypty porównujące sędziów z kartami czytały etykietę karty z pierwszego wystąpienia wzorca i nie obsługiwały zapisu „nie → tak”; poprawione 25.10 (odczyt z ostatniej linii „**Δ”). Na 327 kartach w katalogu ocen (160 raportu i karty systemów spoza niego) stary i nowy odczyt dają ten sam wynik (0 rozbieżności), ale przy kolejnych zmianach kart może dać inny.
- Karta P06 Claude Opus 5.5 W1 nie ma oceny Gemini 4 Argon w wariancie v3: Vertex AI dwa razy nie odpowiedział w 20 minut; karta nie została zapisana i nie weszła do tabeli 11.
- Karty P05 GPT-6.1 Sol W0 i P05 GPT-6 Astra W0 miały na końcu wiersza A6 nieaktualny dopisek „A6_typ: [W]” po decyzji z 13.10 (A6 = 1, etykieta „nie”); usunięty 26.10. Na liczby raportu nie wpływał, bo klasy liczymy tylko w odpowiedziach z halucynacją.

## 9. Wnioski i dalsze kroki

### 9.1. Wnioski

Pierwszy wniosek dotyczy miary. Na dziesięciu krótkich pytaniach z polskiego prawa 29 % odpowiedzi ośmiu modeli było poprawnie ugruntowanych, a 57 % zawierało co najmniej jedno twierdzenie o źródle prawa niezgodne z tekstem urzędowym. Z 93 odpowiedzi z pełnym rdzeniem połowa miała wadliwe powołanie. Ocena samego rdzenia uznałaby te odpowiedzi za prawidłowe; prawnik, który przeniósłby powołanie do pisma bez sprawdzenia, popełniłby błąd.

Drugi wniosek dotyczy rodzaju błędu. W badanym zbiorze najczęstszym błędem nie było zmyślone źródło, lecz przypisanie istniejącemu przepisowi lub orzeczeniu treści, której ono nie zawiera (klasa T, 66 odpowiedzi), i brzmienie z innej daty (klasa W, 35). Wyszukiwanie ogranicza pierwszy, prawie nie zmienia drugiego. Benchmark, który nie sprawdza brzmienia na datę stanu prawnego, pomija błąd najtrwalszy.

Trzeci wniosek dotyczy warunku W1. Dostęp do wyszukiwarki podnosi wynik bloku A u wszystkich modeli, ale liczba odpowiedzi poprawnie ugruntowanych rośnie o 4 u jednego modelu, o 1–2 u trzech, nie zmienia się u dwóch i spada o 1 u jednego; ilorazy wykazanych kosztów W1 i W0 wynoszą około 1,4–7,7, dla części modeli jako dolne oszacowania. Wynik W1 trzeba raportować razem z tym, czy model użył narzędzi i do jakiego źródła dotarł.

Czwarty wniosek dotyczy oceny. Sędzia-model z wyszukiwarką odtwarza kartę prawnika z κ do 0,90 na kartach sprawdzonych przed sędziami, ale pomija między innymi błędy aktualności brzmienia przepisu i treści orzeczenia: dawne brzmienie, tezę z innej sprawy, nieistniejącą linię orzeczniczą. Reguła łączenia sędziów w panel podniosła κ najwyżej o 0,02; w poszczególnych porównaniach raport weryfikacji zmieniał ją od −0,11 do +0,13, w zależności od sędziego i wariantu; porównania obejmowały różne podzbiory kart.

Piąty wniosek dotyczy warstwy weryfikacji. Kod sprawdzający powołania w źródłach urzędowych jest potrzebny, ale jego zasięg wyznaczają źródła: dla k.p.c. brzmienia na datę nie dało się ustalić w 931 z 941 powołań. Niepełne sprawdzenie nie powinno być pokazywane jako potwierdzenie poprawności; w badaniu wpływ raportu zależał od modelu oceniającego. Podobny wniosek dla całych systemów prawniczych z wyszukiwaniem formułują Butler i Butler: jakość wyszukiwania wyznacza górną granicę jakości odpowiedzi [6].

### 9.2. Dalsze kroki

- Nowy zbiór pytań testowych z kluczami zatwierdzonymi przed biegiem, ocena według zamrożonej wersji specyfikacji, bez zmian reguł w trakcie.
- Co najmniej trzy biegi na system, przedziały ufności i porównania parami na tych samych pytaniach.
- Drugi prawnik na próbce około 30 kart jako punkt odniesienia dla κ sędziów-modeli.
- Miara pomocnicza obok etykiety: udział poprawnych powołań w odpowiedzi; tabela krzyżowa dwóch osi (halucynacja × ugruntowanie) dla każdego systemu.
- Przegląd pola `A6_zakres` uzupełnionego 25.10 w kartach pilotażu (zwłaszcza 4 rozstrzygnięć niepewnych w P06 i P07) i pozostałe poprawki z rozdziału 8.2.
- Powtórzenie kart v2 Gemini 4 Argon na jednym raporcie (dziś z dwóch wersji „b” i „c”) i próba wariantu, w którym status „brzmienie nieustalone” wymusza na sędzim cytat ze źródła przed uznaniem powołania.
- Logowanie każdego wywołania narzędzia sędziego (zapytanie, zwrócone źródło, wersja i data źródła) — od 25 października 2026 r. także dla sędziów Codex.
- Bieg kontrolny modeli Claude przez API z narzędziem pobierającym pełną treść strony, aby oddzielić błąd modelu od błędu streszczenia.
- Zapis liczby wyszukań w biegach Claude Code i tokenów treści URL context w biegach Vertex, aby koszt W1 nie był dolną granicą.
- Rozstrzygnięcie, czy B1 ma obejmować orzeczenie z tezą, której w nim nie ma, przytoczone jako argument do pisma (plan wersji 1.1, pkt 10).

## Aneks A. Pytania i klucze w skrócie

Tabela zawiera pytanie w brzmieniu przekazanym systemom (z zachowaniem literówek) i pierwsze dwa zdania rdzenia klucza; dla P09 i P10, których rdzeń zmieniono po biegu na warunkowy (rozdział 2.3), podajemy streszczenie z warunkiem. Pełne klucze, z rubryką, karami, wzorcami cytatów i źródłami, trafią do repozytorium LexAlpha Lab na GitHub (aneks B, „Materiał źródłowy”).

**Tabela A.1. Klucze dziesięciu pytań** (wersja i data klucza; data stanu prawnego we wszystkich: 1.10.2026)

{{TAB:KLUCZE}}

## Aneks B. Wyniki: pytanie × system

**Tabela B.1. Wynik bloku A (A %) każdej odpowiedzi**

{{TAB:ANEKS_B_A}}

**Tabela B.2. Halucynacje i poprawne ugruntowanie** (litery: klasy błędu z pola `A6_typ`; ✓: odpowiedź poprawnie ugruntowana; –: bez halucynacji, rdzeń niepełny; blokada: blokada dostawcy)

{{TAB:ANEKS_B_H}}

**Materiał źródłowy.** Standardy benchmarku (specyfikacja oceny z regułami i przykładami granicznymi), dziesięć pytań testowych wraz z odpowiedziami szesnastu systemów i pełnymi kluczami, karty ocen, oceny sędziów-modeli, raporty warstwy weryfikacji, zestawienia kosztów i skrypty generujące tabele tego raportu opublikujemy wkrótce po tym raporcie w repozytorium LexAlpha Lab na GitHub (https://github.com/apiotrowski-afk), po przeglądzie kart; do tego czasu materiały udostępniamy na prośbę. Karty są wersjonowane datą ostatniej kontroli zbioru; ten raport liczy wszystko na kartach w stanie z 25 października 2026 r.

## Aneks C. Sędziowie: zgodność i ustawienia

**Tabela C.1. Zgodność etykiety hallucinated z kartą według pytania** (zgodne / ocenione karty; 16 systemów)

{{TAB:SEDZ_PYT}}

**Tabela C.2. Ustawienia sędziów**

| Sędzia (identyfikator) | Model | Dostęp | Ustawienia | Zapis wyszukań |
|---|---|---|---|---|
| Gemini 4 Argon (argon4v101) | gemini-4-argon | Vertex AI, region global | rozumowanie high, temperatura 0, Google Search | zapytania i źródła (do 20 zapytań i 25 źródeł na kartę) |
| Gemini 3.1 Pro (gemini31v101) | gemini-3.1-pro-preview | Vertex AI, region global | temperatura 0, Google Search | jak wyżej |
| Gemini 3.8 Flash (gemini38flashv101) | gemini-3.8-flash | Vertex AI, region global | temperatura 0, Google Search | jak wyżej |
| GPT-6.1 Sol (sol61v101) | gpt-6.1-sol | Codex CLI | rozumowanie medium, wyszukiwanie na żywo, tryb tylko do odczytu | liczba wyszukań; od 25.10 także zapytania i źródła |
| GPT-6 Astra (astra6v101) | gpt-6-astra | Codex CLI | jak wyżej | jak wyżej |
| Karta meta: argon4meta, argon4meta2, argon4meta3 | gemini-4-argon | Vertex AI | jak argon4v101 + raport weryfikacji (v1 wiążący, v2 pomocniczy, v3) | jak wyżej |
| Karta meta: sol61meta, sol61meta2, sol61meta3 | gpt-6.1-sol | Codex CLI | jak sol61v101 + raport weryfikacji | jak wyżej |

Plik oceny sędziego zawiera punkty każdego kryterium, klasy błędu, etykietę hallucinated, listę sprawdzonych powołań ze źródłem i werdyktem, listę „niesprawdzone”, uzasadnienie oraz metadane: identyfikator sędziego, model, pytanie, system, liczbę wyszukań, tokeny, czas, datę, wersję specyfikacji i informację, że ocena była ślepa (bez nazwy systemu). Biegi sędziów v101 odbyły się w dniach 13–20 października 2026 r.

## Aneks D. Słownik pojęć

**Tabela D.1. Warunki, kryteria i etykiety**

| Pojęcie | Znaczenie w raporcie |
|---|---|
| W0 | bieg bez narzędzi: bez wyszukiwania i bez tekstów aktów; odpowiedź z wag modelu |
| W1 | bieg z wyszukiwaniem w internecie i poleceniem podania adresów źródeł |
| A-R | rdzeń odpowiedzi: 2 pełny, 1 kierunek trafny bez kluczowego warunku, 0 brak |
| A2, A3, A5, A8 | podstawy wymagane; dosłowność cytatów; sporność; ramy odpowiedzi |
| A6 | halucynacje: 1 albo 0; 0 przy co najmniej jednym twierdzeniu o źródle prawa niezgodnym ze źródłem urzędowym na datę stanu prawnego |
| R, K | elementy rubryki (+1) i kary (−1) z klucza |
| B1, B2 | przydatność dla prawnika (0–2) i kalibracja pewności (0–1) |
| Δ | A % − B %, różnica opisowa |
| F | źródło albo jednostka nie istnieje |
| T | źródło istnieje, ale nie zawiera przypisanej treści |
| W | przepis w brzmieniu z innej daty podany jako obowiązujący |
| S | prawdziwe źródło z przekręconym identyfikatorem |
| O | klasa zniesiona 11.10.2026 (odczyt sprzeczny z brzmieniem) |
| A6_pochodzenie | pamięć / odczyt źródła / źródło wtórne / nieustalone |
| A6_zakres | rdzeń (konkluzja, podstawy wymagane, element rubryki) / poboczne |
| bez weryfikacji źródła | tak (brak narzędzi) / tak (narzędzia nieużyte) / tak (tylko źródła wtórne) / nie |
| poprawnie ugruntowana | A6 = 1 i A-R = 2 |
| blokada dostawcy | pusta odpowiedź zablokowana przez usługę; A6 = n/d, osobna kategoria |
| fałszywy alarm (nadmiar) | sędzia: halucynacja; karta: brak |
| pominięcie (brak) | karta: halucynacja; sędzia: brak |
| zbiór pilotażowy | P05, P06, P07, P12, P13; karty sprawdzane po obejrzeniu sędziów |
| rozszerzenie | P01, P04, P08, P09, P10; karty sprawdzone przed sędziami |
| pytania testowe | osiem pytań, na których nie strojono warstwy weryfikacji: P01, P04–P08, P12, P13 |

**Tabela D.2. Nazwy robocze i nazwy w artykule angielskim**

| Nazwa w raporcie | Nazwa robocza w repozytorium | Nazwa w artykule v1.2 |
|---|---|---|
| poprawnie ugruntowana | poprawnie ugruntowana | correctly grounded |
| karta oceny (karta wzorcowa) | karta, `oceny/<P>_<system>.md` | scoring card (reference card) |
| sędzia-model | sędzia, `_sedziowie/*.json` | model judge |
| data stanu prawnego | `data_stanu_prawnego` | legal-state date |
| warstwa weryfikacji | meta-sędzia (krok faktów + poparcie) | verification layer |
| krok faktów | `fakty.py`, raport faktów | citation check |
| weryfikator poparcia | `poparcie.py` | support check |
| raport weryfikacji | raport faktów | verification report |
| karta meta | `karta_meta.py`, `*.argon4meta*.json`, `*.sol61meta*.json` | judge with the verification report |
| raport wiążący / pomocniczy | meta / meta2 | binding / asymmetric report |
| status weryfikacji | `status_weryfikacji` | verification status |
| tekst niedostępny | `tekst_niedostepny` | source text unavailable |
| brzmienie na datę nieustalone | `na_dzien` nieustalone | wording on the legal-state date undetermined |
| sygnatura niejednoznaczna | `sygnatura_niejednoznaczna` | ambiguous case number |
| akt nieustalony | `akt_nieustalony` | act not identified |
| zasięg weryfikacji | „sprawdzone X z Y” | verification coverage |

**Tabela D.3. Identyfikatory systemów**

| Model | W0 | W1 |
|---|---|---|
| GPT-6.1 Sol | chatgpt_codex_w0_r3 | chatgpt_codex_web_r3 |
| GPT-6 Astra | codex_astra6_w0_r3 | codex_astra6_web_r3 |
| GPT-5.6 Terra | codex_terra56_w0_r3 | codex_terra56_web_r3 |
| Claude Opus 5.5 | opus_cli_w0_r3 | opus_cli_w1_r3 |
| Claude Sonnet 5.5 | sonnet_cli_w0_r3 | sonnet_cli_w1_r3 |
| Claude Haiku 5.5 | haiku_cli_w0_r3 | haiku_cli_w1_r3 |
| Gemini 3.8 Flash | gemini38flash_vertex_w0_r3 | gemini38flash_vertex_w1_r3 |
| Gemini 4 Argon | argon4_high_vertex_w0_r3 | argon4_high_vertex_w1_r3 |

## Aneks E. Macierze pomyłek i przedziały niepewności dla każdej κ

Każda κ w rozdziałach 6 i 7 streszcza tabelę 2 × 2: zarówno karta wzorcowa, jak i ocena modelu wskazują halucynację (TP), tylko ocena modelu (FP, fałszywy alarm), tylko karta (FN, pominięcie), żadna (TN). Kartę z blokadą dostawcy (P07 Gemini 4 Argon W1) liczymy jak kartę bez halucynacji; wszyscy sędziowie, którzy ją ocenili, także nie przypisali jej halucynacji. Tabela E.1 podaje te cztery liczby dla każdego porównania wraz z liczbą halucynacji w kartach, zgodnością surową, κ i przedziałem 95 %. Przedział to bootstrap percentylowy po pytaniach: losujemy całe pytania ze wszystkimi ich kartami, ze zwracaniem, 4000 razy; uwzględnia to zależność między odpowiedziami na to samo pytanie. Przy czterech do ośmiu pytaniach przedziały są szerokie; ich szerokość odzwierciedla niepewność oszacowania przy małej liczbie pytań; przedział 1,00–1,00 znaczy tylko, że w żadnym pytaniu nie było niezgodności. Osobne przedziały nie testują różnicy między sędziami wprost, bo sędziowie oceniali te same odpowiedzi; porównanie sparowane wymagałoby większej liczby pytań. Liczbę halucynacji w kartach podajemy, bo κ od niej zależy: ta sama zgodność surowa daje niższą κ, gdy udział kart z halucynacją jest mały. Wszystkie wiersze liczone na kartach w stanie z 25.10.2026; zbiór pilotażowy obejmuje tu 16 systemów raportu (80 kart), inaczej niż 65 kart 13 systemów w artykule.

**Tabela E.1. Macierze pomyłek, κ i przedziały 95 %** (etykieta hallucinated; sędziowie w specyfikacji v1.0.1; karty meta na kartach wspólnych z sędzią bez raportu; TN = n − TP − FP − FN; zgodność = (TP + TN) / n; „karty v1/v2/v3” = karty ocenione w danym wariancie, „wspólne v2 i v3” = karty ocenione w obu)

{{TAB:MACIERZE}}

Trzy odczyty. Po pierwsze, na rozszerzeniu przedział Gemini 3.8 Flash nie pokrywa się z przedziałem Gemini 4 Argon; pozostałe różnice między sędziami mieszczą się w przedziałach. Po drugie, reguły paneli różnią się od samego Gemini 4 Argon od +0,02 („Argon albo Pro”) do −0,08 („którykolwiek z czterech”), a ich przedziały się pokrywają. Po trzecie, u GPT-6.1 Sol przedziały z raportem v2 i v3 się pokrywają, podobnie jak przedziały bez raportu i z raportem v2 (na krawędzi); kierunek zmiany jest spójny, ale jej wielkość przy ośmiu pytaniach pozostaje nierozstrzygnięta. Wniosek z rozdziału 7.5 o wariancie v3 jest z tego powodu hipotezą roboczą.

## Literatura

[1] Magesh, V., Surani, F., Dahl, M., Suzgun, M., Manning, C. D., Ho, D. E. (2025). *Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools*. *Journal of Empirical Legal Studies*, 22(2), s. 216–242, doi:10.1111/jels.12413; preprint arXiv:2405.20362 (2024). W tekście powołujemy: definicję halucynacji jako odpowiedzi niepoprawnej albo błędnie osadzonej w źródłach i pojęcie ugruntowania.

[2] Taranukhin, M., Shwartz, V. (2026). *Legal LLM Hallucination Should Be Evaluated as Failure of Legal Warrant*. AI4Law @ ICML 2026, arXiv:2609.17546. W tekście powołujemy: warunki „legal warrant” — źródło istnieje, dotyczy właściwej jurysdykcji, jest aktualne na datę analizy, ma przypisany status i popiera twierdzenie.

[3] Kohli, G. (2026). *Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels*. Preprint, arXiv:2605.29800. W tekście powołujemy: panel dziewięciu sędziów z siedmiu rodzin modeli odpowiada około dwóm niezależnym głosom; najlepszy pojedynczy sędzia dorównuje panelowi.

[4] Lee, D., Hwang, Y., Kang, T., Lee, M., Chae, Y., Jung, K. (2026). *Judging Against the Reference: Uncovering Knowledge-Driven Failures in LLM-Judges on QA Evaluation*. Preprint, arXiv:2601.07506. W tekście powołujemy: sędzia ignoruje referencję sprzeczną z własną wiedzą.

[5] Yang, H., Song, W., Kim, T., Song, J., Park, S., Jo, Y. (2026). *Agents' Overreliance on Unreliable Tools*. Preprint, arXiv:2609.05587. W tekście powołujemy: modele przejmują podrobione wyniki narzędzi, dla wyszukiwania w 68,0 % przypadków.

[6] Butler, A.-R., Butler, U. (2026). *Legal RAG Bench: an end-to-end benchmark for legal RAG*. Preprint, arXiv:2603.01710. W tekście powołujemy: jakość wyszukiwania wyznacza górną granicę jakości odpowiedzi systemu prawniczego z wyszukiwaniem.

[7] Piotrowski, A. (2026). *„Hallucination” Is Not Enough: Why Legal LLM Benchmarks Should Measure „Correctly Grounded”*. LexAlpha Lab, KTZR, wersja 1.2 z 26.10.2026, doi:10.5281/zenodo.23674794 (wszystkie wersje: doi:10.5281/zenodo.23438195; wersja 1.1 z 17.10.2026: doi:10.5281/zenodo.23438196); SSRN 7672779; https://www.ktzr.pl/legal-llm-benchmarks-correctly-grounded/.

[8] Piotrowski, A., Koman, A. (2026). *Benchmark systemów AI pracujących z polskim prawem. Propozycja formatu i pilotaż na kazusie terminu zawitego sankcji kredytu darmowego*. LexAlpha Lab, wersja z 1.10.2026 (Benchmark 01).

## Źródła prawne i orzeczenia powołane w raporcie

- Ustawa z dnia 20 maja 1971 r. — Kodeks wykroczeń, art. 119 § 1, 120 § 1, 122 § 1, 124 § 1 (t.j. Dz.U. 2025 poz. 734; brzmienie z t.j. Dz.U. 2015 poz. 1094 jako dawne).
- Ustawa z dnia 6 czerwca 1997 r. — Kodeks karny, art. 278a (uchylony z dniem 1.10.2023, Dz.U. 2022 poz. 2600).
- Ustawa z dnia 24 marca 1920 r. o nabywaniu nieruchomości przez cudzoziemców, art. 1 ust. 1 (t.j. Dz.U. 2017 poz. 2278).
- Ustawa z dnia 14 czerwca 1960 r. — Kodeks postępowania administracyjnego, art. 16 § 1 i § 3, 127 § 3, 217 § 2 pkt 2, 218 § 1; ustawa z dnia 30 sierpnia 2002 r. — Prawo o postępowaniu przed sądami administracyjnymi, art. 52 § 3, 53 § 1.
- Ustawa z dnia 17 listopada 1964 r. — Kodeks postępowania cywilnego, art. 131¹ᵃ (w brzmieniu od 1.06.2026), 357 § 5, 394² § 1², 397 § 1¹, 492 § 1 i § 3, 787, 787¹.
- Ustawa z dnia 28 lipca 2005 r. o kosztach sądowych w sprawach cywilnych, art. 25b (t.j. Dz.U. 2025 poz. 1228).
- Ustawa z dnia 4 lutego 1994 r. o prawie autorskim i prawach pokrewnych, art. 41 ust. 2 i 4, 44, 52, 53 (t.j. Dz.U. 2025 poz. 24; nowela Dz.U. 2024 poz. 1254).
- Rozporządzenie (UE) 2024/1689 (AI Act), art. 3 pkt 60, art. 50 ust. 2 i 4; Komisja Europejska, wytyczne C(2026) 5054 do art. 50 (soft law).
- Sąd Najwyższy: III CK 124/05 (14.09.2005), I CSK 596/17 (5.10.2018), I CSK 104/18 (22.03.2019), IV CSKP 44/21 (14.10.2021), III CK 400/03 (23.09.2004), II CSKP 526/22 (12.01.2023), I CZ 83/09, III CZP 24/23, III CZP 50/22.
- Sądy powszechne: SA w Łodzi I ACa 1157/12 (27.02.2013) i I ACa 1188/12; SA w Rzeszowie I ACz 390/13; SO w Szczecinie VIII Gz 43/16.
