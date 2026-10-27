## 5. Wyniki modeli

### 5.1. Wyniki zbiorcze

Tabela 4 zestawia wyniki szesnastu biegów (osiem modeli w dwóch warunkach) na dziesięciu pytaniach. Kolumny A %, B % i „Halucynacje” pochodzą z generatora zestawień czytającego karty ocen, liczba odpowiedzi poprawnie ugruntowanych z tych samych kart, a koszt z zestawienia kosztów na odpowiedź (cennik z 18 października 2026 r.).

**Tabela 4. Wyniki ośmiu modeli w warunkach W0 i W1** (10 odpowiedzi w każdym wierszu; poprawnie ugruntowana: A6 = 1 i A-R = 2; „≥” = dolna granica kosztu; „sprawdzone powołania” = suma z wierszy A6 kart)

{{TAB:WYNIKI}}

Ze 160 odpowiedzi 91 zawierało co najmniej jedną halucynację: 51 z 80 w W0 i 40 z 80 w W1. Poprawnie ugruntowanych było 46: 19 w W0 i 27 w W1. Rozpiętość między modelami jest duża: od 0 do 7 odpowiedzi poprawnie ugruntowanych na 10. GPT-6.1 Sol i GPT-6 Astra miały w obu warunkach najwyżej po jednej odpowiedzi z halucynacją i po 6–7 odpowiedzi poprawnie ugruntowanych. Claude Sonnet 5.5 i Claude Haiku 5.5 nie dały ani jednej odpowiedzi poprawnie ugruntowanej, ani bez narzędzi, ani z wyszukiwaniem.

Wysoki wynik w bloku A nie wyklucza halucynacji. Claude Opus 5.5 w W1 ma najwyższą średnią A % w zestawieniu (86,0 %) i jednocześnie pięć odpowiedzi z halucynacją. Claude Sonnet 5.5 w W1 ma B % 90,0 i dziewięć odpowiedzi z halucynacją na dziesięć. Profil „trafny rdzeń, wadliwe powołanie” jest w tym zbiorze częsty: z 93 odpowiedzi z pełnym rdzeniem (A-R = 2) 47 zawierało co najmniej jedno powołanie niezgodne ze źródłem urzędowym, więc poprawnie ugruntowanych zostało 46 (aneks B).

### 5.2. Wyszukiwanie: co zmienia, a czego nie

**Tabela 5. Ten sam model bez narzędzi i z wyszukiwaniem**

{{TAB:PARY}}

Średni wynik bloku A wzrósł z wyszukiwaniem u wszystkich ośmiu modeli, o 7,3 pp (GPT-6 Astra) do 31,0 pp (GPT-5.6 Terra i Claude Opus 5.5). Liczba odpowiedzi z halucynacją spadła wyraźnie u trzech modeli: Claude Opus 5.5 (z 9 do 5), Gemini 3.8 Flash (z 8 do 5) i GPT-5.6 Terra (z 6 do 4). U Claude Sonnet 5.5 i Gemini 4 Argon nie zmieniła się, u Claude Haiku 5.5 spadła o jedną. Liczba odpowiedzi poprawnie ugruntowanych wzrosła o 4 u Claude Opus 5.5, o 2 u Gemini 3.8 Flash, o 1 u modeli OpenAI, nie zmieniła się u Claude Sonnet 5.5 i Claude Haiku 5.5, a u Gemini 4 Argon spadła z 2 do 1. W badanej serii średni wynik A był więc wyższy w W1 u wszystkich modeli, a liczba odpowiedzi z halucynacją zmniejszyła się u pięciu; blok A obejmuje także A6, więc obie miary nie są niezależne.

Dostęp do wyszukiwarki nie oznacza, że model z niej korzysta. W W1 w 50 z 80 odpowiedzi ślad narzędzi albo adresy w odpowiedzi pokazują co najmniej jedno źródło urzędowe właściwe dla pytania; 18 odpowiedzi opierało się wyłącznie na źródłach wtórnych (serwisy prawnicze, blogi, portale), a w 12 model nie użył narzędzi, choć je miał (12 kart ma etykietę „narzędzia nieużyte”; historia poprawki etykiety P12 Gemini 3.8 Flash w rozdziale 8.2). Tabela 6 pokazuje, że zależy to od modelu: GPT-6.1 Sol i GPT-6 Astra sięgnęły po źródło urzędowe w każdej odpowiedzi, modele Claude w 3–4 odpowiedziach na 10.

**Tabela 6. Źródła w odpowiedziach W1 i pochodzenie halucynacji** (etykieta „bez weryfikacji źródła” i pole `A6_pochodzenie` z kart)

{{TAB:ZRODLA_W1}}

Z 40 odpowiedzi W1 z halucynacją 21 ma błąd z pamięci: model miał wyszukiwarkę, ale błędnego źródła nie otworzył. W 7 model otworzył właściwe źródło urzędowe i mimo to oddał je błędnie (pochodzenie „odczyt źródła”), w 4 powtórzył błąd ze źródła wtórnego, w 8 pochodzenia nie dało się ustalić: w 5 odpowiedziach modeli Claude, bo Claude Code nie zachowuje śladu narzędzi, i w 3 odpowiedziach modeli Gemini (2 Gemini 3.8 Flash, 1 Gemini 4 Argon), w których ślad nie wskazywał źródła błędu. W W0 wszystkie 51 halucynacji ma z definicji pochodzenie „pamięć”.

### 5.3. Koszt na odpowiedź poprawnie ugruntowaną

Łączny koszt równoważny API 160 odpowiedzi wyniósł co najmniej 15,78 USD: 3,96 USD w W0 i co najmniej 11,81 USD w W1. Najniższy koszt serii dziesięciu odpowiedzi w przeliczeniu na jedną odpowiedź poprawnie ugruntowaną wyniósł 0,042 USD (GPT-6.1 Sol w W0), kolejne 0,058 USD (Gemini 3.8 Flash w W0) i 0,069 USD (GPT-5.6 Terra w W0); najwyższy co najmniej 2,085 USD (Gemini 4 Argon w W1, jedna taka odpowiedź na dziesięć). Wskaźnik dzieli koszt całej serii przez liczbę odpowiedzi poprawnie ugruntowanych, nie jest ceną pojedynczej odpowiedzi. Bieg z wyszukiwaniem kosztował od 1,4 raza (Claude Sonnet 5.5) do 7,7 raza (Claude Haiku 5.5) więcej niż bieg bez narzędzi, przy zmianie liczby odpowiedzi poprawnie ugruntowanych od −1 do +4. Dla modeli bez odpowiedzi poprawnie ugruntowanej metryka ma wartość „n/d”. Mediana czasu odpowiedzi wynosiła od 21,0 s (Claude Haiku 5.5 w W0) do 169 s (Gemini 4 Argon w W1).

Koszt jest równoważnikiem, a nie wydatkiem kancelarii w przypadku Claude Code i Codex, które działały z subskrypcji; dla Vertex AI jest kosztem faktycznym, w cenach promocyjnych obowiązujących 18 października 2026 r. Wartości W1 Claude i Gemini są dolną granicą (rozdział 4.4). Pełny koszt badania, razem z sędziami i warstwą weryfikacji, podaje rozdział 7.7.

### 5.4. Zasięg weryfikacji

Karty podają, ile powołań sprawdzono w źródle urzędowym. Na 160 kartach sprawdzono 1 436 z 1 454 powołań (98,8 %); jedna karta (blokada dostawcy) nie ma powołań. Pozostałe 18 powołań w 11 kartach ma status „nie znaleziono”, „nieobsługiwany” albo „do sprawdzenia ręcznie” i nie wchodzi do błędów modelu. Wśród 46 odpowiedzi poprawnie ugruntowanych dwie mają po jednym takim powołaniu (P10 GPT-6.1 Sol W1, 7 z 8 sprawdzonych; P13 Gemini 4 Argon W0, 6 z 8); ich etykieta opiera się na powołaniach sprawdzonych. Liczba powołań na odpowiedź różni się między modelami ponad czterokrotnie: od 41 w dziesięciu odpowiedziach GPT-5.6 Terra w W0 do 189 w odpowiedziach Gemini 4 Argon w W1. Model, który powołuje więcej, ma więcej okazji do błędu przy regule „jedna zła jednostka = 0”; to argument za raportowaniem obok etykiety także udziału poprawnych powołań w odpowiedzi.

### 5.5. Klasy błędów

**Tabela 7. Klasy błędów w odpowiedziach z halucynacją** (liczba odpowiedzi zawierających daną klasę; jedna odpowiedź może mieć kilka klas; wartość bieżąca pola `A6_typ`)

{{TAB:KLASY}}

Najczęstszą klasą jest T: prawdziwy przepis lub wyrok z treścią, której w nim nie ma (66 z 91 odpowiedzi z halucynacją). Drugą jest W, brzmienie z innej daty podane jako obowiązujące (35). Zmyślone źródło (F, 8 odpowiedzi) i zniekształcony identyfikator (S, 9) są rzadkie. Wyszukiwanie zmniejszyło liczbę odpowiedzi z klasą T z 42 do 24, a liczby odpowiedzi z klasą W prawie nie zmieniło (18 i 17). Liczba odpowiedzi z błędem W była więc podobna w obu warunkach. W kartach W1 z błędem W model podawał treść z pamięci albo ze starszego tekstu znalezionego w sieci; udziału starszych tekstów w wynikach wyszukiwania nie mierzyliśmy.

Pole `A6_zakres` wypełniono w kartach pięciu pytań rozszerzenia. Z 42 odpowiedzi z halucynacją na tych pytaniach 22 mają błąd w rdzeniu, a 20 tylko w uwadze pobocznej przy trafnej konkluzji i jej podstawach. W 49 kartach z halucynacją na pytaniach pilotażowych pole uzupełniono 25 października 2026 r. (decyzja z tego dnia; wpis do przeglądu prawnika w każdej karcie): 35 ma błąd w rdzeniu, a 14 tylko w uwadze pobocznej. Łącznie na dziesięciu pytaniach 57 z 91 odpowiedzi z halucynacją ma błąd w rdzeniu, a 34 tylko w uwadze pobocznej. Dwie reguły przyjęte tego dnia rozstrzygnęły siedem przypadków granicznych: błąd w treści elementu rubryki to rdzeń także wtedy, gdy element zaliczono, a zniekształcony identyfikator orzeczenia przy zgodnej tezie to uwaga poboczna, chyba że orzeczenie należy do podstaw wymaganych. W 4 kartach pilotażu rozstrzygnięcie pozostaje oznaczone jako niepewne.

### 5.6. Typowe błędy: przykłady z kart

Przykłady wybraliśmy tak, aby każdy ilustrował inny mechanizm. Odesłanie w nawiasie wskazuje kartę `oceny/<pytanie>_<system>.md`.

- **Stary stan prawny w wagach i w wyszukiwarce (W).** W P01 reguła „¼ minimalnego wynagrodzenia”, obowiązująca do 14 listopada 2018 r., pojawiła się jako stan obecny w trzech niezależnych odpowiedziach: Claude Haiku 5.5 i Claude Sonnet 5.5 bez narzędzi oraz GPT-5.6 Terra z wyszukiwaniem. GPT-5.6 Terra bez narzędzi podał poprawnie 800 zł, a z wyszukiwaniem przypisał „¼ płacy minimalnej” art. 119 § 1, 120 § 1, 122 § 1 i 124 § 1 k.w.; jest to brzmienie z tekstu jednolitego z 2015 r. Wynik tej odpowiedzi w bloku A spadł z 78 % do 0 % (P01_codex_terra56_w0_r3, P01_codex_terra56_web_r3). Odpowiedź W1 zawierała regułę odpowiadającą dawnemu brzmieniu przepisu, podczas gdy odpowiedź W0 podawała aktualną kwotę; możliwym wyjaśnieniem jest wykorzystanie nieaktualnego źródła.
- **Przepis uchylony jako podstawa (W).** W P01 art. 278a k.k. powołano jako obowiązującą podstawę w czterech odpowiedziach (Claude Opus 5.5 w W0 i W1, Gemini 3.8 Flash i Gemini 4 Argon w W1); przepis w tej treści obowiązywał do 30 września 2023 r. (P01_opus_cli_w0_r3).
- **Brzmienie sprzed noweli ze zmianą merytoryczną (W, reguła B10a).** Art. 44 pr.aut. opisany jako „rażąca dysproporcja” wynagrodzenia — tak brzmiał przed nowelą z 26 lipca 2024 r. (Dz.U. 2024 poz. 1254); obecnie przepis mówi o wynagrodzeniu „niewspółmiernie niskim” (P10_opus_cli_w0_r3, błąd poboczny).
- **Krąg adresatów sprzed zmiany (W, reguła z 24 października 2026 r.).** W P05 opis art. 131¹ᵃ § 1 k.p.c. ograniczający doręczenia przez portal do profesjonalnych pełnomocników odpowiada brzmieniu sprzed 1 czerwca 2026 r. (P05_codex_terra56_w0_r3). W P07 art. 25b u.k.s.c. z opłatą 100 zł od każdego postanowienia odpowiada tekstowi jednolitemu z 2020 r.; obecnie 100 zł dotyczy tylko wyroku i postanowienia co do istoty (m.in. P07_codex_terra56_web_r3).
- **Prawdziwa sygnatura, cudza sprawa (T).** Wyrok SN II CSKP 526/22 powołany na tezę o polach eksploatacji, z datą 14 września 2022 r.; według bazy orzeczeń to wyrok z 12 stycznia 2023 r. w sprawie o zadośćuczynienie (P10_argon4_high_vertex_w0_r3, błąd poboczny). Wyrok SN III CK 400/03 dotyczy pól eksploatacji jako elementu przedmiotowo istotnego umowy, ale nie zawiera przypisanej mu tezy o bezskuteczności klauzuli ogólnej (P09_gemini38flash_vertex_w1_r3, błąd w rdzeniu).
- **Właściwe źródło otwarte, treść zmieniona (T, odczyt źródła).** GPT-6.1 Sol z wyszukiwaniem podał adres pełnego tekstu postanowienia SN I CZ 83/09 w SAOS i przypisał mu tezę, że SN „potwierdził” stanowisko w kwestii, do której wcześniejsza ocena według tekstu postanowienia *się nie odnosiła* (P13_chatgpt_codex_web_r3).
- **Właściwe źródło otwarte, zły numer (S, odczyt źródła).** Gemini 4 Argon z wyszukiwaniem otworzył wyrok SA w Łodzi I ACa 1157/12 z 27 lutego 2013 r. i trafnie oddał jego tezę, ale w tekście wpisał sygnaturę I ACa 1188/12, czyli innego wyroku tego sądu (P10_argon4_high_vertex_w1_r3). GPT-5.6 Terra z wyszukiwaniem podał właściwe rekordy SAOS z błędnym sądem: I ACz 390/13 (SA w Rzeszowie, nie w Szczecinie) i VIII Gz 43/16 (SO w Szczecinie, nie SA w Gdańsku) (P13_codex_terra56_web_r3).
- **Ogólnik o orzecznictwie sprzeczny z wyrokiem z klucza (T, reguła B9).** Claude Opus 5.5 w W1 (P09) i Gemini 3.8 Flash w W0 (P09 i P10) przypisały „orzecznictwu” tezę, że ogólna formuła nie przenosi praw do żadnego pola; linia SN (III CK 124/05, I CSK 596/17, IV CSKP 44/21) mówi odwrotnie. Po zawężeniu reguły B9 23 października 2026 r. jedna podobna teza (P10 Claude Opus 5.5 w W1) przestała być halucynacją, bo żaden wyrok z klucza jej wprost nie odrzuca.
- **Sąsiednia jednostka z cudzą treścią (T).** W P09 Claude Opus 5.5 w W1 powołał „art. 64” pr.aut. z treścią art. 52 ust. 1 (P09_opus_cli_w1_r3).
- **Blokada dostawcy.** Gemini 4 Argon z wyszukiwaniem na P07 dwukrotnie oddał pustą odpowiedź z sygnałem `RECITATION`: Vertex blokuje tekst, gdy model zbyt dosłownie przytacza znaleziony tekst. System z wyszukiwaniem może więc zamilknąć wtedy, gdy znalazł i cytuje przepis (P07_argon4_high_vertex_w1_r3).

Dwa pytania pokazują granice rdzenia jako miary. W P04 żaden z 16 systemów nie dał pełnego rdzenia (średnio 43,0 % w bloku A): prawidłowa odpowiedź wymaga zestawienia k.p.a., p.p.s.a. i ustawy o nabywaniu nieruchomości przez cudzoziemców oraz znajomości instytucji zaświadczenia, a w pierwszym przeglądzie kart tego pytania (25 kart, w tym karty systemów spoza tego raportu) dominowała odpowiedź „ostateczność” albo „zasadniczo ostateczność, ewentualnie prawomocność” — także z wyszukiwaniem. W P07 Claude Haiku 5.5 odpowiedział trafnie „tak”, ale w całości o wyroku i apelacji zamiast o postanowieniu i zażaleniu. Sonda z 24 zapytaniami (18 z nich opisujemy) pokazała powtarzalny wzorzec zależny od sformułowania pytania: na oryginalne pytanie model 10 razy na 10 odpowiedział „tak” i 10 razy na 10 o wyroku; gdy pytanie wprost nazywało postanowienie, odpowiedział poprawnie 5 razy na 5; zapytany wprost o art. 357 § 5 k.p.c. trzy razy na trzy odpowiedział, że nie wie. Odpowiedź była trafna, lecz dotyczyła innej instytucji, czego ocena samego rdzenia nie wykrywa (zapis sondy trafi do repozytorium, aneks B).

### 5.7. Co wynika z rozdziału 5

- Na tym zbiorze 46 ze 160 odpowiedzi (29 %) jest poprawnie ugruntowanych. Halucynacja w rozumieniu przyjętym w raporcie dotyczy 91 odpowiedzi (57 %), przy czym na pytaniach rozszerzenia blisko połowa takich odpowiedzi (20 z 42) ma błąd tylko w uwadze pobocznej.
- Wyszukiwanie podnosi wynik bloku A u wszystkich modeli, ale liczba odpowiedzi poprawnie ugruntowanych rośnie o 4 tylko u jednego (Claude Opus 5.5), a u jednego spada (Gemini 4 Argon). Raportowanie wyniku W1 bez informacji, czy model użył narzędzi i jakiego źródła, miesza dwa różne zjawiska.
- Liczba odpowiedzi z błędem W była podobna w obu warunkach (18 w W0, 17 w W1), podczas gdy liczba odpowiedzi z klasą T spadła z 42 do 24. Kryterium aktualności brzmienia na datę chroni także przed „ugruntowaniem” w nieaktualnym źródle.
- Część błędów powstaje po otwarciu właściwego źródła (7 z 40 halucynacji w W1). Dostęp do źródeł na wejściu nie zastępuje kontroli powołań na wyjściu.
