## 2. Zbiór pytań: dziesięć pytań z praktyki, klucze zatwierdzane przed biegiem

### 2.1. Skład zbioru

Pytania pochodzą z katalogu pytań zebranych w praktyce kancelarii, w brzmieniu, w jakim prawnik wpisał je do czatu. Zbiór ma dwie części. Pięć pytań z postępowania cywilnego (P05, P06, P07, P12, P13) stanowiło pilotaż opisany w artykule [7]. Pięć kolejnych (P01, P04, P08, P09, P10) dołączyliśmy 18 października 2026 r., aby objąć inne dziedziny: prawo wykroczeń, postępowanie administracyjne, prawo autorskie i AI Act. Typ pytania i cechy klucza zestawia tabela 1.

**Tabela 1. Dziesięć pytań zbioru** (typ i kalibracja według kluczy; liczby według kart ocen, 16 odpowiedzi na pytanie)

{{TAB:PYTANIA}}

Osiem pytań ma typ `zamkniete` (trafienie: tak, nie albo „zależy od X”), P01 typ `obliczenie` (kwota progu), a P08 typ `weryfikacja` (czy system sprawdza cudze twierdzenie, czy je powtarza). Pułapka, czyli błędna albo nieaktualna przesłanka, którą system ma nazwać i skorygować, jest wbudowana w sześć pytań: P01 (powiązanie progu wykroczenia z płacą minimalną, obowiązujące do 14 listopada 2018 r.), P04 (postanowienie zamiast decyzji i klauzula zamiast zaświadczenia), P05 (doręczenie przez portal osobie fizycznej po zmianie art. 131¹ᵃ § 1 k.p.c. z 1 czerwca 2026 r.), P08 (przesłanka, że głos, który „niczego nie udaje”, nie jest deepfake; klucz v4 każe ją zweryfikować wobec kryterium „mogą realnie istnieć” z wytycznych KE, a dodatkowo oczekuje wskazania, że obowiązek oznaczania treści syntetycznych z art. 50 ust. 2 AI Act nie zależy od kwalifikacji jako deepfake — ten element rubryki wykracza poza dosłowne pytanie i przyjęliśmy go jako test typu „weryfikacja”), P10 (przesłanka, że ogólna formuła o „wszelkich polach eksploatacji” wystarcza) i P12 (tryb klauzuli przeciwko małżonkowi „bez ograniczeń” i błędny numer przepisu w pytaniu). W pięciu pytaniach klucz oczekuje kalibracji warunkowej: poprawna odpowiedź wiąże konkluzję z warunkiem, którego pytanie nie przesądza.

Pytania P09 i P10 tworzą **parę lustrzaną**: dotyczą tej samej kwestii, ale P09 sugeruje odpowiedź prawidłową („ogólny zapis nie wystarcza?”), a P10 błędną („wystarcza i nie trzeba wyliczać?”). Para służy sprawdzeniu, czy odpowiedź systemu zależy od sugestii zawartej w pytaniu. Klucz P10 ma karę K2 za rdzeń sprzeczny z odpowiedzią tego samego systemu na P09. W biegu żaden z 16 systemów nie otrzymał kary K2, a karę K1 za przytaknięcie przesłance albo odpowiedź wymijającą otrzymał jeden (Claude Haiku 5.5 bez narzędzi: „zwykle nie”). Pełny rdzeń w P09 i w P10 miało po 15 z 16 odpowiedzi.

### 2.2. Data stanu prawnego i zasady klucza

Każdy klucz ma pole `data_stanu_prawnego`; we wszystkich dziesięciu pytaniach jest to 1 października 2026 r. Odpowiedź ocenia się według prawa na ten dzień, także gdy system odpowiadał później. Klucz zawiera rdzeń odpowiedzi, podstawy wymagane, wzorce cytatów przepisane z tekstu urzędowego, elementy rubryki (punkty dodatnie), kary (punkty ujemne), oczekiwaną kalibrację i pole `weryfikacja`, w którym zapisujemy, czego nie sprawdzono. Orzeczenie wchodzi do klucza z tezą przepisaną z tekstu orzeczenia i ze wskazaniem bazy oraz zakresu odczytu; omówienia i komentarze nie są źródłem tezy. Klucz obejmuje tylko to, o co pyta pytanie.

W badaniu stosujemy wyłącznie klucze zatwierdzone. Klucze P12 i P13 zatwierdzono 10 października 2026 r., klucze P01 (wersja 3), P04 (wersja 3), P08 (wersja 4), P09 (wersja 3) i P10 zatwierdzono 18 października 2026 r., przed biegiem rozszerzenia. Klucze P05, P06 i P07 pochodzą z 10 października 2026 r. i nie mają pola `status`, które wprowadziła zasada z tego samego dnia; potwierdzenie zatwierdzenia jest w rejestrze decyzji (specyfikacja oceny), nie w samym kluczu.

### 2.3. Zmiany kluczy po lekturze źródeł

Cztery klucze zmieniliśmy w trzech opisanych niżej przypadkach, gdy analiza źródeł ujawniła uproszczenia w kluczu. Zmiany zapisujemy jako nowe wersje z datą i powodem; kart według starszej wersji nie porównujemy z nowymi bez przeliczenia.

- **P04 (wersje 1–2 → 3, przed biegiem).** Klucz przygotowany przez model wskazywał „klauzulę ostateczności, nie prawomocności”. Prawnik wskazał z praktyki, że decyzja ministra o zezwoleniu na nabycie nieruchomości przez cudzoziemca jest najpierw ostateczna (art. 16 § 1, art. 127 § 3 k.p.a.), a potem prawomocna (art. 16 § 3 k.p.a.; art. 52 § 3 i art. 53 § 1 p.p.s.a.), a stan ten potwierdza zaświadczenie organu (art. 217 § 2 pkt 2 w zw. z art. 218 § 1 k.p.a.). Model piszący klucz przeniósł do niego to samo uproszczenie („administracja — ostateczność, sądy — prawomocność”), które benchmark miał wykrywać.
- **P08 (wersja 3 → 4, przed biegiem).** Klucz zakładał, że głos niepodobny do żadnej istniejącej osoby nie jest deepfake. Wytyczne Komisji Europejskiej C(2026) 5054 do art. 50 AI Act ujmują kryterium „istniejące” szerzej: obejmuje ono także osoby, które mogą realnie istnieć. Wytyczne weszły do klucza jako osobny element rubryki z zaznaczeniem, że są soft law (rozdział 4.4).
- **P09 i P10 (wersje 3 → 4 i 2 → 3, po biegu z 18 października 2026 r.).** Klucze przygotowane bez badania orzecznictwa stanowiły, że ogólna formuła nie przenosi praw do żadnego pola eksploatacji. Prawnik odczytał wyroki SN I CSK 104/18, I CSK 596/17 i IV CSKP 44/21: art. 41 ust. 2 pr.aut. nie wyklucza wykładni z art. 65 k.c., pól nie trzeba wyliczać enumeratywnie, a wątpliwości rozstrzyga się na korzyść twórcy. Odpowiedzi GPT-6.1 Sol i GPT-6 Astra z wyszukiwaniem, które wskazały tę linię, traciły według dawnej reguły B6 punkty, choć były trafniejsze od klucza. Rdzeń zmieniono na warunkowy, linia SN weszła do rubryki jako element nagradzany, a reguła B6 została uchylona; 20 kart P09 i P10 przeliczono. Wyrokiem źródłowym tej linii jest III CK 124/05; koordynator uznał go najpierw za niezwiązany z polami eksploatacji na podstawie fragmentu cytowanego w innym wyroku, a błąd wykrył agent oceniający, który przeczytał pełny tekst w SAOS.

Zmiana P09 i P10 nastąpiła po zebraniu odpowiedzi, więc w tej części zasada „klucz przed biegiem” nie została dochowana; kierunek zmiany (klucz łagodniejszy wobec odpowiedzi trafniejszych od niego) i jej powód zapisano w kluczach.

### 2.4. Pytania poza zbiorem

Pytanie P02 (odsetki ustawowe za opóźnienie od kwot w CHF i PLN) wyłączyliśmy decyzją z 18 października 2026 r., zapisaną w polu `status` klucza: zbiór ma być jednorodny i obejmować pytania o treść prawa, a zadanie obliczeniowe ma trafić do osobnego testu, na przykład z narzędziem do liczenia. Klucz P02 pozostał bez zmian. P01 ma wprawdzie typ `obliczenie`, ale odpowiedź to kwota zapisana wprost w ustawie, więc zostało w zbiorze (decyzja z 25 października 2026 r.). Pytania P03 i P11, które mają klucze z pilotażu z 10 października 2026 r., nie weszły do rozszerzenia z 18 października, a powodu tej decyzji nie zapisaliśmy. Oba dotyczą kredytu konsumenckiego (wcześniejsza spłata); włączymy je do następnego biegu po sprawdzeniu kluczy według specyfikacji v1.0.1.

## 3. Systemy i warunki biegu

### 3.1. Osiem modeli w dwóch warunkach

Pytania otrzymało osiem modeli trzech dostawców, każdy w dwóch warunkach. **W0** to bieg bez narzędzi: bez wyszukiwania, bez dostępu do tekstów aktów, odpowiedź wyłącznie z wag modelu. Mierzy wiedzę zapisaną w modelu. **W1** to bieg z wyszukiwaniem w internecie, z poleceniem podania adresów źródeł. Mierzy przydatność w warunkach, w jakich prawnik zwykle korzysta z modelu. Warunek W1 dla wszystkich modeli wprowadziliśmy decyzją z 17 października 2026 r., aby porównanie z modelami, które miały wyszukiwanie już w pilotażu, było uczciwe.

**Tabela 2. Systemy i ustawienia biegu r3**

| Model | Identyfikator | Dostęp | Ustawienia | W1: narzędzia |
|---|---|---|---|---|
| GPT-6.1 Sol | gpt-6.1-sol | Codex CLI (konto ChatGPT) | rozumowanie medium; aplikacje konta wyłączone | wyszukiwanie Codex na żywo |
| GPT-6 Astra | gpt-6-astra | Codex CLI | jak wyżej | jak wyżej |
| GPT-5.6 Terra | gpt-5.6-terra | Codex CLI | jak wyżej | jak wyżej |
| Claude Opus 5.5 | claude-opus-5-5 (alias opus) | Claude Code CLI (subskrypcja) | bez MCP i CLAUDE.md; temperatura domyślna | WebSearch + WebFetch |
| Claude Sonnet 5.5 | claude-sonnet-5-5 | Claude Code CLI | jak wyżej | jak wyżej |
| Claude Haiku 5.5 | claude-haiku-5-5 | Claude Code CLI | jak wyżej | jak wyżej |
| Gemini 3.8 Flash | gemini-3.8-flash | Vertex AI, region global | temperatura 0,1; rozumowanie domyślne | Google Search + URL context |
| Gemini 4 Argon | gemini-4-argon | Vertex AI, region global | temperatura 0,1; rozumowanie high | Google Search + URL context |

Wszystkie modele dostały ten sam krótki wstęp („Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne.”), a w W1 zdanie o wyszukiwaniu i adresach źródeł. Wstęp nie zawiera prośby o zwięzłość ani wskazówek o pułapkach i sporności; nie zmienialiśmy go w trakcie serii biegów. Każde pytanie przekazywano w osobnej sesji, w brzmieniu z pola `tekst_benchmarkowy` albo, gdy go nie ma, `tekst_oryginalny`. Odpowiedzi na pytania pilotażowe zebrano 10 października 2026 r. (modele OpenAI i Anthropic w W0 oraz GPT-6.1 Sol w W1), 13 października (Gemini 4 Argon w W0) i 17–18 października (pozostałe), a na pytania rozszerzenia 18 października 2026 r. Każdy system odpowiadał raz.

Trzy cechy warunków wpływają na odczyt wyników. Po pierwsze, Claude Code przetwarza stronę pobraną narzędziem WebFetch małym modelem (Claude Haiku 5.5) i oddaje modelowi głównemu streszczenie, nie surowy tekst; Codex i Gemini czytają strony bez pośrednika. Przy błędach klasy T w odpowiedziach Claude W1 nie da się więc oddzielić błędu modelu od błędu streszczenia. Po drugie, w W0 Codex działa z wyłączonymi aplikacjami konta ChatGPT, bo aplikacje te mają własną wyszukiwarkę (ustalenie z 8 października 2026 r.). Po trzecie, rozumowanie Gemini 4 Argon trzeba wymusić: bez ustawienia `high` model w pilotażu nie rozumował na pytaniach prawnych wcale, a wynik tej samej wersji modelu zmieniał się istotnie (średnio 38,9 % wobec 55,1 % w bloku A na pięciu pytaniach pilotażu). W raporcie podajemy więc tryb, nie tylko nazwę modelu.

### 3.2. Systemy kancelarii poza benchmarkiem

Decyzją z 17 października 2026 r. nie obejmujemy badaniem systemów własnych kancelarii (asystent badawczy, czat i każdy kolejny produkt) ani w części z pytaniami, ani w części z kazusami. Powodem jest konflikt interesów: oceniający byłby zarazem autorem ocenianego systemu. Dotychczasowe biegi tych systemów przeniesiono do archiwum (124 pliki, nic nie usunięto); generatory wyników ich nie czytają. Raport nie obejmuje też systemów prawniczych innych dostawców, które oceniał Benchmark 01; tier pytań bada na razie modele ogólnego przeznaczenia, z wyszukiwaniem i bez.

## 4. Metoda oceny

### 4.1. Dwa bloki i karta oceny

Jak w Benchmarku 01, oceniamy w dwóch blokach raportowanych osobno. **Blok A** (obiektywny) obejmuje: rdzeń odpowiedzi A-R (0, 1 albo 2 punkty; 1 oznacza kierunek trafny bez kluczowego warunku), podstawy wymagane A2 (0/1; zero także przy błędnej podstawie), dosłowność cytatów A3 (0/1, tylko gdy system cytuje), wskazanie sporności A5 (tylko przy pytaniu spornym), halucynacje A6 (0/1), ramy odpowiedzi A8 (0, ½ albo 1), elementy rubryki R (po punkcie) i kary K (po punkcie ujemnym). A % to suma punktów pomniejszona o kary i podzielona przez punkty możliwe, bez kryteriów, które nie mają zastosowania. **Blok B** (ocenny) obejmuje przydatność dla prawnika B1 (0–2) i kalibrację pewności B2 (0/1) względem pola klucza `kalibracja_oczekiwana`. Δ = A % − B % jest różnicą opisową.

Kartę oceny każdej odpowiedzi wypełnia najpierw model Claude, sprawdzając każde powołane źródło w tekście urzędowym (ISAP i ELI, EUR-Lex, SAOS, sn.pl, portale orzeczeń sądów powszechnych, serwisy gov.pl), a następnie prawnik rozstrzyga sporne punkty i zatwierdza kartę. Karta zawiera przy każdym kryterium punkt i dowód, a przy A6 listę sprawdzonych powołań z wynikiem i źródłem.

### 4.2. A6: halucynacja zero-jedynkowa i klasy błędu

Od 11 października 2026 r. A6 przyjmuje wartość 1 albo 0. Odpowiedź dostaje 0 i etykietę *hallucinated*, gdy zawiera co najmniej jedno twierdzenie o źródle prawa niezgodne ze źródłem urzędowym na datę stanu prawnego. Typ błędu zapisujemy w polu `A6_typ`, bez wpływu na punkt:

- **F** — źródło albo jednostka redakcyjna nie istnieje;
- **T** — wskazanemu przepisowi lub orzeczeniu przypisano treść, której w nim nie ma: odwrotną, cudzą, o rozciągniętym lub zawężonym zakresie, dla innego adresata; także teza przypisana ogólnie „orzecznictwu” sprzeczna z wyrokiem zapisanym w kluczu;
- **W** — przepis w brzmieniu z innej daty podany jako obowiązujący, także błędny opis historii zmian;
- **S** — prawdziwe źródło z przekręconym identyfikatorem (numer, data, sąd, publikator, nazwa aktu).

Klasę O z wcześniejszej typologii zniesiono: fałszywe twierdzenie o treści przepisu to T, a samo pominięcie przesłanki nie obniża A6, lecz może obniżyć ocenę rdzenia i elementów rubryki. Odpowiedź bez żadnego powołania ma A6 = 1. Reguła jest celowo surowsza niż miara, którą przyłożylibyśmy do człowieka. Prawnik, który napisze „§ 1¹” zamiast „§ 1²”, zwykle wie, o który przepis mu chodzi; model takiej pamięci zamiaru nie ma, a polska technika legislacyjna (indeksy górne, jednostki dodawane i uchylane nowelami) sprawia, że sąsiednie numery regulują inne sprawy.

Obok punktu karta podaje dwa pola opisowe. **`A6_pochodzenie`** mówi, skąd wziął się błąd: z pamięci (system nie otworzył źródła), z odczytu źródła (otworzył właściwe źródło urzędowe i oddał je błędnie), ze źródła wtórnego albo nieustalone. **`A6_zakres`** (od 18 października 2026 r.) mówi, czy błąd dotyczy rdzenia (głównej konkluzji, podstaw wymaganych, elementu rubryki), czy uwagi pobocznej. A6 pozostaje surowe niezależnie od zakresu: jeden błąd klasy F, T, W lub S w dowolnym miejscu odpowiedzi daje zero.

### 4.3. Etykieta „bez weryfikacji źródła” i poprawne ugruntowanie

Etykieta **bez weryfikacji źródła** jest niezależna od punktów i ma cztery warianty: *brak narzędzi* (bieg W0), *narzędzia nieużyte* (W1, ale ślad narzędzi i źródła nie pokazują, że system z nich skorzystał; wariant z 18 października 2026 r.), *tylko źródła wtórne* (serwisy prawnicze, blogi, portale) oraz *nie*, gdy w śladzie lub w źródłach odpowiedzi jest co najmniej jedno źródło urzędowe właściwe dla pytania. Etykietę ustalamy ze śladu narzędzi i metadanych biegu, nie z deklaracji systemu.

Główną miarą raportu jest **odpowiedź poprawnie ugruntowana**: karta ma A6 = 1 i A-R = 2. To połączenie dwóch warunków z planu wersji 1.1 specyfikacji: brak fałszywego twierdzenia o prawie i pełny rdzeń. Miara nie wymaga, aby system sam dotarł do źródła urzędowego; tę cechę pokazuje osobno etykieta „bez weryfikacji źródła”.

### 4.4. Reguły szczególne

- **Soft law** (18 października 2026 r.). Wytyczne Komisji, kodeksy praktyk i opinie organów wchodzą do klucza jako osobny element rubryki, nigdy jako kara. Halucynacją jest przypisanie im mocy wiążącej albo treści, której w nich nie ma; nieścisłość co do etapu przyjęcia, gdy same źródła publiczne są niezgodne, halucynacją nie jest.
- **Blokada dostawcy** (18 października 2026 r.). Gdy odpowiedź jest pusta, bo usługa zablokowała wygenerowany tekst (Vertex, `finish_reason = RECITATION` albo `SAFETY`), A6 ma wartość „n/d”, bez etykiety hallucinated, a pozostałe kryteria 0. Bieg powtarza się raz; dwie blokady z rzędu są wynikiem. W zbiorze jest jeden taki przypadek: Gemini 4 Argon w W1 na P07, dwie próby, obie zablokowane.
- **Koszt** (18 października 2026 r.). Dla każdej odpowiedzi liczymy koszt równoważny API według publicznych cenników z 18 października 2026 r. Dla Claude Code i Codex z subskrypcji to równoważnik, dla Vertex koszt faktyczny. Główną metryką jest koszt na odpowiedź poprawnie ugruntowaną. Koszt nie wpływa na punkty. Znak „≥” oznacza dolną granicę: Claude Code nie zapisuje liczby wyszukań, a skrypt Vertex w biegu r3 nie zapisywał tokenów treści z URL context.

### 4.5. Reguły graniczne i kalendarz decyzji

Reguły graniczne rozstrzygają przypadki, w których definicja klasy nie wystarcza. Każdą z nich ustalił prawnik na konkretnej karcie, a karta ta służy dalej sędziom jako wzorzec. Tabela 3 zestawia decyzje z okresu 17–25 października 2026 r., które wpłynęły na karty zbioru. Decyzje z 9–11 października (A6 zero-jedynkowe, klasy F/T/W/S, zniesienie klasy O, etykieta „bez weryfikacji źródła”) poprzedzają ten okres i opisaliśmy je w rozdziałach 4.2 i 4.3.

**Tabela 3. Decyzje z 17–26 października 2026 r.** (pełne brzmienie decyzji w specyfikacji oceny, która trafi do repozytorium LexAlpha Lab na GitHub; aneks B, „Materiał źródłowy”)

| Data | Decyzja | Skutek dla kart |
|---|---|---|
| 17.10 | Przykłady graniczne A8 nr 1–3 i B1 nr 1 (dygresja wynikająca z błędnej tezy; błędna konstrukcja w odpowiedzi na zadane pytanie; pomylony rodzaj orzeczenia; krok kontrolny przy tezie grożącej utratą terminu) | zmiany punktów w 5 kartach, etykiety bez zmian |
| 17.10 | Systemy kancelarii poza benchmarkiem; W1 dla wszystkich modeli | 124 pliki w archiwum; 80 nowych biegów |
| 18.10 | `A6_zakres` (rdzeń / poboczne); blokada dostawcy; soft law w kluczach; metryka kosztu; wariant „narzędzia nieużyte” | nowe pola w kartach rozszerzenia |
| 18.10 | B8: błędna historia zmian przepisu = W, rdzeń, gdy historia jest elementem rubryki | P01 |
| 18.10 | P09 v4 i P10 v3: rdzeń warunkowy, linia SN jako nagroda, uchylenie B6 | 20 kart przeliczonych |
| 18.10 | Decyzje nr 1–34 na kartach rozszerzenia; B10 (stara redakcja bez zmiany normy = tylko A3), B10a (stare brzmienie ze zmianą merytoryczną = W); nr 19 (zmiana zwrotu definiowanego w cytacie = A3 0); B11 (B2 przy kalibracji warunkowej P09/P10); B12 (linia orzecznicza — wystarczy wykładnia z art. 65 k.c.); bez podwójnej kary w bloku B; A8 = 1 za trafne uwagi poboczne | 59 z 80 kart zmienionych |
| 19.10 | Zalecenie redakcyjne podane jako wymóg ustawowy = A8 ½, bez T; zawężenie definicji wbrew wytycznym = błąd wykładni w A-R, bez T | 5 kart P08, 1 karta P09 |
| 22.10 | Sąsiednia jednostka tego samego artykułu, gdy niesie istotę przypisanej treści = nieścisłość bez T; jednostka uchylona z jej dawną prawdziwą treścią = W, nie F | P10 (Gemini 4 Argon W1, GPT-5.6 Terra W1) |
| 23.10 | B9 w wersji wąskiej: zdanie o orzecznictwie bez sygnatury = T tylko wtedy, gdy wyrok z klucza wprost odrzuca przypisaną tezę; twierdzeń o „jednolitości” linii nie karzemy | Claude Opus 5.5 W1 P10: A6 0 → 1 |
| 24.10 | Zawężony lub rozszerzony krąg adresatów albo zakres normy: W, gdy pokrywa się z brzmieniem z innej daty; T, gdy nie odpowiada żadnemu brzmieniu; samo niewspomnienie to pominięcie | reguła także dla warstwy weryfikacji |
| 24.10 | Warstwa weryfikacji: S na orzeczeniach z oceną każdego kandydata przy sygnaturze niejednoznacznej; u.n.n.c. do legal-cite; raport dla sędziego może dodać błąd, nie może go odjąć | rozdział 7 |
| 25.10 | Karta meta v3: „✓” tylko przy brzmieniu na datę potwierdzonym; rejestrowanie każdego wywołania narzędzia sędziego | rozdział 7.5 |
| 25.10 | `A6_zakres` mówi o miejscu błędu, nie o skutku dla punktów: błąd w treści elementu rubryki = rdzeń także przy zaliczonym elemencie; S przy zgodnej tezie = poboczne, chyba że orzeczenie jest w podstawach wymaganych | pole uzupełnione w 49 kartach pilotażu |
| 26.10 | Publikacja: pierwszych 10 pytań z kluczami, specyfikacją i kartami wzorcowymi ukaże się razem z metodologią po przeglądzie kart; reszta puli 50 pytań zamknięta. Karty wersjonowane datą ostatniej kontroli zbioru (ta wersja: 25.10.2026) | oświadczenie o danych w artykule v1.2; aneks E |

Reguły zmienialiśmy po lekturze odpowiedzi, w tym trzykrotnie regułę A6 w dniach 9–11 października 2026 r. Z tego powodu zbiór ma status kalibracyjny, a wersję specyfikacji zapisujemy w każdej karcie (obecnie 1.0.1 z doprecyzowaniami z 17–24 października).
