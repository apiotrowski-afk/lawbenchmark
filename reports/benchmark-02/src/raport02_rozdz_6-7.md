## 6. Sędziowie-modele

### 6.1. Procedura

Kartę każdej odpowiedzi wypełniał najpierw model Claude ze sprawdzeniem powołań w źródłach urzędowych, a sprawdzał i zatwierdzał ją prawnik (rozdział 4.1). Sprawdzone karty są w tym rozdziale punktem odniesienia. Te same odpowiedzi oceniało niezależnie pięciu sędziów-modeli: Gemini 4 Argon (rozumowanie high), Gemini 3.1 Pro i Gemini 3.8 Flash na Vertex AI (region global, temperatura 0, z Google Search) oraz GPT-6.1 Sol i GPT-6 Astra przez Codex CLI (wyszukiwanie na żywo, rozumowanie medium, tryb tylko do odczytu). Czterech sędziów (Gemini 4 Argon, Gemini 3.8 Flash, GPT-6.1 Sol, GPT-6 Astra) jest zarazem ocenianymi modelami; w części kart sędzia ocenia więc własną odpowiedź albo odpowiedź modelu własnej rodziny.

Każdy sędzia dostawał w jednym poleceniu trzy elementy: reguły oceny (bloki A i B wraz z przykładami granicznymi), pełny klucz pytania oraz tekst odpowiedzi bez nazwy systemu. Nie widział karty ani ocen innych sędziów. Polecenie wymagało sprawdzenia każdego powołanego przepisu i orzeczenia w źródle urzędowym przez wyszukiwanie (ISAP i ELI, EUR-Lex, SAOS, sn.pl), porównania numeru jednostki i treści dosłownie, nieoceniania z pamięci i wpisania do osobnego pola „niesprawdzone” każdego powołania, którego nie udało się sprawdzić. Sędzia oddawał kartę w tym samym układzie co karta wzorcowa. Zgodność mierzymy κ Cohena dla etykiety hallucinated; etykietę karty czytamy z ostatniej linii wyniku karty („**Δ = …”), aby uwzględnić zmiany naniesione po decyzjach.

Zbiór dzieli się na dwie części o różnej wartości dowodowej. Karty pytań pilotażowych (P05, P06, P07, P12, P13) prawnik sprawdzał po obejrzeniu ocen sędziów, a sporne punkty rozstrzygał często na korzyść argumentu sędziego; zgodność na tej części jest zawyżona. Karty pytań rozszerzenia (P01, P04, P08, P09, P10) sprawdzono przed uruchomieniem sędziów, z wyjątkiem siedmiu rozbieżności GPT-6.1 Sol rozstrzygniętych 19 października 2026 r.; ta część jest właściwym testem. Sędziowie na pytaniach rozszerzenia zaczynali przed dopisaniem do specyfikacji reguł B9–B12 i znali je tylko z kluczy. GPT-6 Astra ocenił z powodu limitu konta 43 karty pilotażu i 6 kart rozszerzenia, dlatego jego wyników nie interpretujemy.

### 6.2. Zgodność z kartą prawnika

**Tabela 8. Zgodność etykiety hallucinated sędziów-modeli z kartami** (16 systemów z tabeli 4; fałszywy alarm: sędzia „tak”, karta „nie”; pominięcie: karta „tak”, sędzia „nie”)

{{TAB:SEDZIOWIE}}

Na pytaniach rozszerzenia najwyższą zgodność osiągnął Gemini 4 Argon (κ 0,90, n = 79; jedna karta bez oceny). GPT-6.1 Sol i Gemini 3.1 Pro mają tę samą κ 0,80, ale błędy w przeciwnych kierunkach: GPT-6.1 Sol zgłosił 7 halucynacji, których karty nie przyjęły, i pominął jedną; Gemini 3.1 Pro nie zgłosił żadnego fałszywego alarmu i pominął 8 halucynacji. Gemini 3.8 Flash pominął 16 z 42 halucynacji zapisanych w kartach (κ 0,58). Sześć z siedmiu fałszywych alarmów GPT-6.1 Sol wynikało z definicji surowszej niż przyjęta w specyfikacji: pięć kart P08 (zawężenie definicji deepfake wbrew wytycznym Komisji, które specyfikacja od 19 października traktuje jako błąd wykładni w rdzeniu, nie jako T) i karta P09 Gemini 4 Argon W0 („musi” w zaleceniu redakcyjnym); w żadnym z tych przypadków sędzia nie podał błędnie treści prawa. Siódmy to karta P10 Claude Opus 5.5 W1, której etykietę zmieniono na „nie” po zawężeniu reguły B9 23 października. Na pytaniach pilotażowych κ jest wyższa niż na rozszerzeniu u Gemini 4 Argon (0,97), GPT-6.1 Sol (0,84) i Gemini 3.8 Flash (0,82), a niższa u Gemini 3.1 Pro (0,71: 5 fałszywych alarmów i 6 pominięć); kierunek zawyżenia nie jest więc jednakowy dla wszystkich sędziów. Macierze pomyłek i przedziały 95 % dla każdej κ podaje aneks E; na rozszerzeniu tylko przedziały Gemini 4 Argon (0,80–0,97) i Gemini 3.8 Flash (0,40–0,70) się nie pokrywają.

Wartości te różnią się od podanych w zestawieniu z 19 października 2026 r. (Gemini 4 Argon 0,92, GPT-6.1 Sol 0,82, Gemini 3.1 Pro 0,78, Gemini 3.8 Flash 0,56), bo po tej dacie zmieniły się etykiety części kart, między innymi po zawężeniu reguły B9 23 października. Raport podaje wartości na kartach w stanie z dnia składania; generator κ jest częścią skryptu składającego raport (trafi do repozytorium, aneks B).

### 6.3. Wyszukiwania i deklaracje o weryfikacji

Wszyscy sędziowie mieli wyszukiwarkę i polecenie sprawdzenia każdego powołania. Na pytaniach rozszerzenia Gemini 4 Argon wykonał średnio 12,2 wyszukania na kartę, a GPT-6.1 Sol 11,2; obaj wyszukiwali przy każdej karcie. Gemini 3.1 Pro wykonał 4,3 wyszukania na kartę i przy 25 z 80 kart nie wyszukał niczego, Gemini 3.8 Flash 4,7 i przy 9 kartach żadnego. Najwięcej wyszukiwał sędzia najzgodniejszy z kartami. Gemini 3.1 Pro, który wyszukiwał najmniej, ma jednak tę samą κ co GPT-6.1 Sol, bo jego błędy to wyłącznie pominięcia, a błędy GPT-6.1 Sol to głównie fałszywe alarmy. Wśród czterech sędziów mniejsza liczba pominięć współwystępowała z wyszukiwaniem przy każdej karcie: dwaj sędziowie wyszukujący przy każdej karcie pominęli łącznie 4 halucynacje zapisane w kartach, dwaj pozostali 24. Badanie nie pozwala oddzielić wpływu wyszukiwania od innych różnic między modelami.

Drugą miarą jest rzetelność deklaracji o weryfikacji: czy model wskazuje powołania, których nie sprawdził. Pole „niesprawdzone” wypełniał praktycznie tylko GPT-6.1 Sol (0,36 powołania na kartę na rozszerzeniu); u Gemini 4 Argon, Gemini 3.1 Pro i Gemini 3.8 Flash średnia wynosi 0,00–0,01. Sędzia, który po zerze wyszukań raportuje wszystkie powołania jako sprawdzone, oddaje werdykt nieodróżnialny od zweryfikowanego. Wcześniejszy przykład z pilotażu: przy uchwale III CZP 50/22 GPT-6.1 Sol i GPT-6 Astra wpisały „niesprawdzone”, bo nie dotarły do uzasadnienia, a oba Gemini — „w pełni zgodne”, bez śladu lektury uzasadnienia. Statystyki wyszukań istnieją tylko dlatego, że wywołania narzędzi były rejestrowane: dla sędziów Gemini zapisywaliśmy zapytania i źródła, dla sędziów Codex tylko liczbę wyszukań (od 25 października 2026 r. także zapytania i źródła).

### 6.4. Czego sędziowie nie widzą

Halucynacje przeoczone przez co najmniej dwóch sędziów na pytaniach rozszerzenia należą prawie wyłącznie do trzech grup: brzmienie albo zakres przepisu inne niż w dniu stanu prawnego (błędna historia progu w P01, stan prawa „na 2024 r.” zamiast 2026 r., art. 44 pr.aut. w starym brzmieniu, zawężające „jedynie” w art. 50 ust. 2 AI Act, art. 127a k.p.a.), prawdziwa sygnatura z tezą z innej sprawy (klasa T) oraz ogólnik „SN przyjmuje…” bez sygnatury (reguła B9). Wykrycie większości z nich wymaga informacji spoza odpowiedzi, klucza i reguł; wyjątkiem jest ogólnik sprzeczny z wyrokiem zapisanym w kluczu, który da się wychwycić z samego klucza. Potrzebny jest tekst urzędowy na datę stanu prawnego, pełny tekst orzeczenia albo znajomość linii orzeczniczej. Wyszukiwarka zwracała je zawodnie: tekst jednolity bieżący stawiała przed wcześniejszymi, zamiast orzeczeń podawała omówienia, a nie sygnalizowała, że wyroku nie ma. Sędzia, który nie dotrze do źródła, korzysta z tej samej pamięci co model, który napisał odpowiedź; ocenia wtedy wiarygodność twierdzenia, nie jego prawdziwość.

### 6.5. Pominięcia według dostawcy ocenianego modelu

**Tabela 9. Pominięte halucynacje według dostawcy ocenianego modelu** (wszystkie 10 pytań; mianownik: karty z halucynacją ocenione przez sędziego)

{{TAB:RODZINA}}

Gemini 3.8 Flash pominął 45 % halucynacji w odpowiedziach modeli Google, wobec 12 % w odpowiedziach modeli Anthropic i 15 % OpenAI; Gemini 3.1 Pro odpowiednio 24 %, 12 % i 8 %. U Gemini 4 Argon różnica jest mała w liczbach bezwzględnych (2 z 24 wobec 1 z 44); jedna z dwóch pominiętych halucynacji w odpowiedziach Google jest w odpowiedzi samego Gemini 4 Argon (W0 P08: „jedynie” w art. 50 ust. 2 AI Act), druga w odpowiedzi Gemini 3.8 Flash (W0 P04: art. 127a k.p.a.). Projekt meta-sędziego z 19 października wymienia jeszcze przeoczenie w karcie P09 Gemini 4 Argon W1, ale ocena Gemini 4 Argon dla tej karty nie ma pliku i nie weszła do tabeli (rozdział 8). Wynik ma znane zastrzeżenie: odpowiedzi Google mają w tym zbiorze dużo błędów klasy W, które wszyscy sędziowie wykrywają gorzej, więc część różnicy może wynikać z rodzaju błędu, nie z rodziny modelu. Liczba kart na rodzinę (12–49) nie pozwala tych przyczyn rozdzielić.

### 6.6. Panel sędziów

Na 79 kartach rozszerzenia ocenionych przez czterech sędziów Gemini 4 Argon sam ma κ 0,90. Reguła „halucynacja, gdy zgłosi ją Gemini 4 Argon albo Gemini 3.1 Pro” daje κ 0,92 (1 fałszywy alarm, 2 pominięcia), większość z trzech (Gemini 4 Argon, GPT-6.1 Sol, Gemini 3.1 Pro) 0,90, a reguła „którykolwiek z czterech” 0,82 (7 fałszywych alarmów, 0 pominięć). Reguły dobieraliśmy na tych samych danych, więc nawet przyrost o 0,02 jest dopasowaniem, nie wynikiem. Łączenie ocen zmniejszało liczbę pominięć kosztem fałszywych alarmów; każdą halucynację z kart wykrył co najmniej jeden sędzia. Błędy pominięte przez dwóch lub więcej sędziów (rozdział 6.4) dotyczą faktów, których ci sędziowie nie sprawdzili w źródle. To samo zjawisko opisuje Kohli [3]: panel dziewięciu sędziów z siedmiu rodzin modeli dał informację odpowiadającą około dwóm niezależnym głosom, a najlepszy pojedynczy sędzia dorównał panelowi. Nasze dane wskazują prawdopodobną przyczynę skorelowanych błędów: niesprawdzone fakty.

### 6.7. Co wynika z rozdziału 6

- Na kartach sprawdzonych przed sędziami najlepszy sędzia-model osiąga κ 0,90 w etykiecie halucynacji; najsłabszy 0,58. Wybór sędziego zmienia wynik benchmarku bardziej niż wybór reguły panelu.
- Pominięcia sędziów skupiają się na błędach wymagających źródła na datę: dawnego brzmienia, tezy z innej sprawy, linii orzeczniczej; przy błędach widocznych z odpowiedzi, klucza i reguł pominięć było niewiele (analiza przypadków, rozdział 6.4).
- W zbadanych konfiguracjach zwiększenie liczby sędziów nie dawało wyższej κ niż najlepszy pojedynczy sędzia; różnice między sędziami szły w parze z tym, jak weryfikowali powołania. Karta sędziego powinna podawać liczbę wyszukań, listę niesprawdzonych powołań oraz zapytania i zwrócone źródła z wersją i datą; bez takiego dziennika czytelnik nie odróżni werdyktu sprawdzonego od niesprawdzonego.
- Powtórzeń biegu tego samego sędziego nie badaliśmy, więc o stabilności werdyktów nic nie twierdzimy.

## 7. Warstwa weryfikacji

### 7.1. Dwa kroki przed sędzią

Ponieważ sędziom brakowało źródła, zbudowaliśmy sprawdzenie, które wykonuje się przed oceną i niezależnie od sędziego. Nazywamy je **warstwą weryfikacji** (w artykule angielskim *verification layer*). Ma dwa kroki.

- **Krok faktów** (sam kod, bez modelu). Kod wyodrębnia z odpowiedzi powołania. Dla przepisu pobiera z legal-cite brzmienie jednostki na datę stanu prawnego klucza oraz brzmienia wcześniejsze (co 6, 12, 24, 60, 120 i 180 miesięcy), aby wykryć klasę W. Dla orzeczenia szuka sygnatury w SAOS, a gdy wyroku tam nie ma — w bazie orzeczeń LexAlpha, wyłącznie do odczytu przez bramkę. Cytaty porównuje z tekstem dosłownie.
- **Weryfikator poparcia** (model z ograniczonym wejściem). Model dostaje tylko twierdzenie, które odpowiedź przypisuje jednemu źródłu, i tekst tego źródła. Rozstrzyga, czy źródło popiera twierdzenie. Etykietę „popiera” może dać tylko z dosłownym cytatem ze źródła, którego obecność sprawdza potem kod.

Wynikiem jest **raport weryfikacji**: dla każdego powołania klasa (✓, F, T, W, S) albo status weryfikacji („tekst niedostępny”, „brzmienie na datę nieustalone”, „sygnatura niejednoznaczna”, „akt nieustalony” i inne) wraz z brzmieniem urzędowym, jego wersją i datą. Status nie jest błędem modelu: nieudane sprawdzenie nie dowodzi, że model się pomylił, i obu wyników nie wolno oznaczać tą samą etykietą. Podział pracy odpowiada ramie „legal warrant” Taranukhina i Shwartz [2]: istnienie, jurysdykcję i aktualność źródła da się sprawdzić kodem, poparcie twierdzenia przez źródło wymaga czytania.

### 7.2. Wyniki na pytaniach strojenia i na pytaniach testowych

Na dwóch pytaniach, na których warstwę budowaliśmy (P09 i P10, 32 odpowiedzi), krok faktów wykrył wszystkie błędy F (3 z 3), W (5 z 5) i S (1 z 1) zapisane w kartach oraz 7 z 7 cytatów niedosłownych, przy jednym fałszywym alarmie; nie wykrył żadnego z 15 błędów T merytorycznych, bo ich wykrycie wymaga czytania. Weryfikator poparcia w drugiej wersji wykrył 9 z 13 przepisów z cudzą treścią, 3 z 3 orzeczeń nie na temat i 1 z 4 ogólników B9 (razem 13 z 20, 65 %), przy 4 fałszywych alarmach na 355 ocen (1 %). Te liczby mogą być zawyżone, bo mechanizm rozpoznawania powołań i instrukcję dla modelu dostosowywaliśmy na tych samych danych.

Właściwy test objął osiem pytań, na których warstwy wcześniej nie strojono (P01, P04, P05, P06, P07, P08, P12, P13; 128 odpowiedzi; dalej: pytania testowe), z zamrożonymi instrukcjami. Pierwsza kolumna tabeli 10 to ten test; dwie następne pokazują wyniki po poprawkach wprowadzonych na podstawie analizy błędów z tych samych pytań, więc są wynikami eksploracyjnymi, nie testem na nietkniętym zbiorze. Punktem odniesienia jest lista 147 błędów z powołaniem zapisanych w kartach i 665 powołań, które karty uznały za poprawne. Tabela 10 pokazuje trzy kolejne biegi.

**Tabela 10. Warstwa weryfikacji na pytaniach testowych** (czułość wobec listy błędów z kart; „dowolna klasa” — błąd wykryty, choćby z inną klasą; „ta sama klasa” — z klasą z karty; źródła: raporty biegów warstwy z 23.10 i 24.10 w repozytorium)

| Miara | 23.10 (prompty zamrożone) | 24.10 (naprawy wejścia, plik „b”) | 24.10 (decyzje nr 2–4, plik „c”) |
|---|---|---|---|
| czułość, dowolna klasa | 84 / 147 (57 %) | 87 / 147 (59 %) | 94 / 147 (64 %) |
| czułość, ta sama klasa | n/d | 66 / 147 (45 %) | 74 / 147 (50 %) |
| T, dowolna klasa | 39 / 83 (47 %) | 49 / 83 (59 %) | 50 / 83 (60 %) |
| W: ta sama / dowolna klasa | n/d / 15 z 44 (sam krok faktów) | 17 / 28 z 44 (39 / 64 %) | 24 / 32 z 44 (55 / 73 %) |
| S: ta sama / dowolna klasa | n/d / 7 z 14 (sam krok faktów) | 0 / 4 z 14 | 2 / 6 z 14 |
| F: ta sama / dowolna klasa | n/d / 3 z 6 (sam krok faktów) | 0 / 6 z 6 | 0 / 6 z 6 |
| fałszywe alarmy na 665 ✓ | 8,0 % weryfikator + 4,1 % krok faktów | 1,8 % | 1,8 % |
| koszt biegu (Vertex) | 8,09 USD | 7,87 USD | 7,09 USD |

*Uwaga do kolumny 23.10: łączna czułość 84 ze 147 to suma wykryć kroku faktów i weryfikatora poparcia liczona na całym zbiorze; raport z tego biegu nie podaje tej sumy w podziale na klasy W, S i F, dlatego dla tych klas podajemy wyłącznie wykrycia kroku faktów (łącznie z T: 64), które nie sumują się do 84.*

### 7.3. Większość strat to wejście, nie ocena

Różnica między 65 % na pytaniach strojenia a 57 % na pytaniach testowych łączy dwie różne miary (czułość weryfikatora poparcia na 20 błędach treściowych wobec czułości całej warstwy na 147 błędach), więc nie jest ścisłym spadkiem; wzrost fałszywych alarmów z 1 % do 8 % wynikał głównie z przetwarzania wejścia, nie z oceny modelu. Cztery przyczyny dało się usunąć bez zmiany promptów:

- parser powołań nie rozpoznawał litery w indeksie górnym (art. 131¹ᵃ, 394¹ᵃ k.p.c.) i szukał sąsiedniego artykułu — 22 fałszywe alarmy przed naprawą, 1 po niej;
- akt domyślny z klucza podstawiano za inny akt nazwany w odpowiedzi (k.p.a., AI Act, k.w. zamiast ustawy o nabywaniu nieruchomości przez cudzoziemców, RODO, prawa autorskiego) — 37 alarmów przed naprawą, po niej 0 i 38 statusów „akt nieustalony”;
- ta sama sygnatura w różnych sądach: kod brał cudzy wyrok (np. VIII Gz 43/16) — 14 alarmów przed naprawą, 6 po niej;
- łańcuch „art. X w zw. z art. Y” liczony jako kilka twierdzeń — 21 alarmów przed naprawą, po niej 0 i 120 statusów „w związku”.

Po naprawach fałszywe alarmy spadły do 1,8 %, a czułość wykrywania błędów klasy T wzrosła z 47 % do 59 %. Część pozostałych pominięć wynikała z różnic w stosowaniu definicji, nie z kodu. Najważniejsza dotyczyła zawężenia kręgu adresatów albo zakresu normy: weryfikator czytał je jako pominięcie, karta jako W albo T. Decyzja z 24 października 2026 r. (rozdział 4.5) i jej wprowadzenie do promptu weryfikatora podniosły czułość „ta sama klasa” na klasie W z 39 % do 55 %, kosztem jednego nowego fałszywego alarmu i jednej zmiany klasy z W na T.

Dwie obserwacje dotyczą samych źródeł. SAOS był niedostępny przez cały bieg 23 października (błędy odpowiedzi i przekroczenia czasu), a kod nie odróżniał awarii od braku wyroku; po poprawce awaria jest osobnym statusem. W bazie orzeczeń LexAlpha tekst wyroku SN III CK 124/05 ma 10 238 znaków wobec 18 748 w SAOS i nie zawiera zdania o relacji art. 41 ust. 2 pr.aut. do art. 65 k.c., dla którego wyrok się cytuje; jest to inna, krótsza wersja redakcyjna. SAOS nie ma z kolei 5 z 8 badanych wyroków SN (III CK 400/03, II CSKP 526/22, IV CSKP 44/21, I CSK 596/17, I CSK 104/18). Ta sama sygnatura może więc mieć w dwóch bazach różne teksty, a weryfikator musi wiedzieć, którą wersję czyta. Od 21 października 2026 r. pierwszeństwo ma tekst z SAOS.

### 7.4. Granica źródła dla klasy W

Klasę W da się zmierzyć tylko tam, gdzie źródło urzędowe pozwala odtworzyć brzmienie na wskazaną datę. Dla Kodeksu postępowania cywilnego, który między tekstami jednolitymi ma kilkadziesiąt nowelizacji, legal-cite zwrócił „brzmienie na datę nieustalone” dla 931 z 941 powołań; podobnie dla u.k.s.c., k.p.k., p.p.s.a. i k.k.s. Klasa F jako ta sama klasa ma 0 % czułości, bo legal-cite odnajduje jednostkę pod sąsiednim numerem i błąd zostaje zaklasyfikowany jako T. Klasa S na orzeczeniach zamienia się w status, gdy sygnatura jest niejednoznaczna albo wyroku nie znaleziono; od 24 października weryfikator ocenia tezę wobec każdego z co najwyżej czterech kandydatów, co dało 2 trafne S z 14. Kryterium, którego nie da się zastosować, bo źródła nie można pobrać w wymaganej wersji, nie mierzy niczego. Dlatego obok wyników benchmarku należy podawać zasięg weryfikacji: ile powołań sprawdzono i w jakiej wersji źródła.

### 7.5. Raport dla sędziego: wiążący, pomocniczy, v3

Raport weryfikacji podaliśmy dwóm sędziom, Gemini 4 Argon i GPT-6.1 Sol, w trzech wariantach instrukcji (karta meta). W wariancie pierwszym raport był **wiążący**: klasy A6 sędzia miał opierać na raporcie. W drugim był **pomocniczy** (decyzja z 24 października 2026 r.: „raport może dodać błąd, nie może go odjąć”): klasa F, T, W albo S z raportu wiąże, a „✓” nie zwalnia sędziego z porównania treści przypisanej źródłu z brzmieniem z raportu. W trzecim (v3, 25 października 2026 r.) raport pokazuje „✓” tylko wtedy, gdy brzmienie na datę stanu prawnego zostało potwierdzone; w pozostałych przypadkach podaje status, który odsyła sędziego do własnej oceny.

**Tabela 11. Sędzia bez raportu i z raportem weryfikacji** (κ etykiety hallucinated wobec kart na kartach wspólnych z sędzią bez raportu; wiersze różnią się zbiorem kart, porównanie wariantów na jednym zbiorze w tekście niżej)

{{TAB:META}}

Raport wiążący obniżył zgodność obu sędziów (Gemini 4 Argon z 0,96 do 0,85, GPT-6.1 Sol z 0,88 do 0,83). Mechanizm widać na kartach: „✓” w raporcie oznaczał tylko, że przepis istnieje, ma podane brzmienie, a cytat jest dosłowny, a sędziowie traktowali go jak potwierdzenie całego powołania i przestawali sprawdzać, czy odpowiedź opisuje na przykład krąg adresatów przepisu sprzed nowelizacji. Raport zmienił etykietę zawsze z „tak” na „nie”; błędnie w kartach P05 GPT-5.6 Terra W0 (art. 131¹ᵃ § 1 k.p.c.: „tylko profesjonalni pełnomocnicy”), P05 Claude Sonnet 5.5 W1 (reguła doręczenia z uchwały III CZP 24/23 podana jako aktualna), P07 Gemini 3.8 Flash W1 (art. 25b ust. 1 u.k.s.c.) i P13 GPT-5.6 Terra W0 (art. 492 § 3 k.p.c.).

Raport pomocniczy na ośmiu pytaniach testowych podniósł zgodność GPT-6.1 Sol z 0,84 do 0,97 (n = 119): zniknęło 7 z 8 fałszywych alarmów, pominięć nie przybyło. Zgodność Gemini 4 Argon spadła z 0,95 do 0,88 (n = 115). Trzy dodatkowe pominięcia Argona to błędy klasy W, które raport pokazał jako „✓”: w jednym brzmienia na datę nie dało się ustalić (P07 Gemini 3.8 Flash W1), w jednym raport powstał przed wprowadzeniem reguły o kręgu adresatów (P05 GPT-5.6 Terra W0), w jednym odpowiedź przyjęła błędny rok dla progu ustawowego, czego krok faktów nie sprawdza (P01 Gemini 4 Argon W0). Karty v2 dla P05, P06, P07 i P13 pochodzą z raportu „b”, a dla P01, P04, P08 i P12 z raportu „c”; czyste porównanie na jednym raporcie wymaga powtórzenia 64 kart Argona.

Wariant v3 ukończono 25 października 2026 r. na 128 kartach dla GPT-6.1 Sol i 127 dla Gemini 4 Argon (jedna karta bez odpowiedzi Vertex AI po dwóch próbach). Wariant miał pokazać, jak sędzia zachowa się, gdy zamiast „✓” zobaczy status; nie zakładaliśmy, że podniesie zgodność. Na 119 kartach wspólnych dla ocen bez raportu oraz wariantów v2 i v3 GPT-6.1 Sol ma κ 0,84 bez raportu, 0,97 z raportem v2 i 0,91 z raportem v3 (fałszywe alarmy 8 → 1 → 2, pominięcia 1 → 1 → 3); Gemini 4 Argon na 115 kartach wspólnych 0,95 bez raportu i 0,88 zarówno z v2, jak i z v3. Dwa nowe pominięcia GPT-6.1 Sol w v3 to karty klasy W (P05 Claude Sonnet 5.5 W1, P07 Gemini 3.8 Flash W1), które w v2 ten sam sędzia wykrył. W v3 raport pokazywał przy tych powołaniach status „brzmienie na datę nieustalone” zamiast „✓”; sędzia ocenił brzmienie sam i przyjął je za obowiązujące, a w P07 potraktował opłatę 100 zł z dawnego brzmienia jako pominięcie, nie jako W. W tych dwóch kartach sędzia w v3 pominął błąd wykryty w v2; jedną z możliwych przyczyn jest zmiana informacji w raporcie (status zamiast „✓”), po której sędzia oparł się na własnym odczycie odpowiedzi. Pełny bilans zmian na 119 kartach to jeden fałszywy alarm i dwa pominięcia więcej w v3 niż w v2. Najwyższą zgodność z kartami daje nadal v2 u sędziego surowszego. Wyjaśnienie mechanizmu traktujemy jako hipotezę roboczą: różnica między wariantami opiera się na kilku kartach jednego sędziego, bez powtórzeń biegu, i wymaga sprawdzenia na większej próbie oraz na większej liczbie sędziów. Przedziały 95 % z bootstrapu po pytaniach (aneks E) się pokrywają: u GPT-6.1 Sol 0,92–1,00 z raportem v2 i 0,85–0,98 z v3, a bez raportu 0,70–0,96; w badanej próbie κ była wyższa w v2 niż w v3, ale niepewności tej różnicy nie oszacowano (wymaga porównania sparowanego).

Wynik zgadza się z badaniem agentów, które przejmują podrobione wyniki narzędzi, dla wyszukiwania w 68 % przypadków [5]. Wymaga też zawężenia: gdy podana referencja przeczy wiedzy sędziego, sędziowie zwykle ją ignorują [4]. Efekt, który obserwujemy, dotyczy raportu zgodnego z tym, co sędzia i tak by przyjął: „✓” potwierdza powołanie, którego sędzia nie zamierzał badać. Reguła, którą z tego wyprowadzamy, brzmi: automatyczna weryfikacja może dodać błąd do oceny sędziego, nie może go usunąć, a powołanie może być pokazane jako poprawne tylko po zakończeniu każdego elementu sprawdzenia.

### 7.6. Koszt warstwy weryfikacji

Krok faktów nie ma kosztu poza zapytaniami do źródeł publicznych. Weryfikator poparcia kosztował 3,05 USD za 383 ocenione powołania na pytaniach strojenia (około 0,8 centa za powołanie) i 8,09 USD za 1 452 powołania na pytaniach testowych w biegu z 23 października (około 0,6 centa). Karta meta Gemini 4 Argon kosztuje około 0,10 USD (6,57 USD za 64 karty w wariancie v1), dwa do trzech razy więcej niż karta sędziego bez raportu, bo polecenie rośnie do około 19 tys. tokenów, a Gemini 4 Argon nie obsługuje jawnie zarządzanej pamięci podręcznej kontekstu na Vertex AI. Pełny cykl na ośmiu pytaniach testowych (krok faktów, weryfikator poparcia i karta meta Gemini 4 Argon) kosztował 14,70 USD. GPT-6.1 Sol działał z subskrypcji, a jego wąskim gardłem był limit konta, nie koszt.

### 7.7. Pełny koszt badania

Tabela 12 zbiera wycenę użycia modeli w tym badaniu według cenników z 18 października 2026 r. (dla Codex i Claude Code równoważnik API, nie wydatek): odpowiedzi ocenianych modeli, sędziów-modeli na kartach w specyfikacji v1.0.1 oraz warstwę weryfikacji ze wszystkimi biegami testowymi i strojeniem. Koszt sędziów i kart meta liczymy z tokenów zapisanych w plikach ocen i z cennika z 18 października 2026 r. Wyszukiwania Gemini (Grounding with Google Search) podajemy osobno w cenie katalogowej 0,014 USD za zapytanie. Cennik Vertex AI zwalnia z opłaty 5000 takich zapytań miesięcznie, dlatego zapisy kosztu w raportach biegów ich nie obejmują, a faktura była niższa niż suma w tabeli.

**Tabela 12. Pełny koszt badania** (USD, cennik z 18.10.2026; „≥” = dolna granica; „n/d” = Codex z subskrypcji bez zapisu tokenów)

{{TAB:KOSZT_PELNY}}

Pełny koszt wyniósł co najmniej {{USD:koszt_pelny}} USD, z czego {{USD:koszt_pelny_wyszukania}} USD przypada na wyszukiwania w cenie katalogowej. Odpowiedzi ocenianych modeli to co najmniej {{USD:koszt}} USD, sędziowie-modele Vertex co najmniej {{USD:koszt_sedziowie}} USD, a warstwa weryfikacji {{USD:koszt_weryfikacja}} USD. Ocena kosztowała więc kilka razy więcej niż wygenerowanie ocenianych odpowiedzi. U sędziów Gemini większą część kosztu stanowią wyszukiwania, a nie tokeny. Kwota jest dolną granicą z trzech powodów: sędziowie w specyfikacji v1.0.1 nie zapisywali tokenów rozumowania, W1 modeli Claude i Gemini nie ma pełnego zapisu narzędzi, a biegi Codex z subskrypcji nie zapisywały tokenów. Tabela nie obejmuje pracy prawnika ani modelu Claude, który wstępnie wypełniał karty.

### 7.8. Co wynika z rozdziału 7

- Kod umożliwia automatyczne sprawdzenie istnienia jednostki i dosłowności cytatu, ale wynik zależy od poprawnego rozpoznania powołania i dostępu do właściwego tekstu. Wykrywanie dawnego brzmienia, nieistniejących jednostek i błędnych oznaczeń orzeczeń ogranicza jakość źródeł urzędowych dostępnych w wymaganej wersji i jakość parsowania powołań.
- Cztery usterki przetwarzania wejścia (indeksy górne z literą, akty domyślne, te same sygnatury w różnych sądach, łańcuchy „w zw.”) odpowiadały za 94 fałszywe alarmy w pierwszym biegu i 7 po poprawkach; osobnym ograniczeniem są krótsze wersje tekstów orzeczeń. Te elementy techniczne wymagają tyle samo pracy projektowej co kryteria oceny.
- Zgodność sędziego z kartami różniła się między wariantami instrukcji i raportu; badanie nie oddziela wpływu samej instrukcji od treści raportu. Raport wiążący obniżył zgodność obu sędziów; raport pomocniczy podniósł zgodność sędziego surowszego (GPT-6.1 Sol), a u Gemini 4 Argon zwiększył liczbę pominięć tam, gdzie „✓” oznaczał sprawdzenie niepełne. Sędzia musi mieć polecenie samodzielnego sprawdzenia każdego powołania, także oznaczonego w raporcie jako poprawne.
