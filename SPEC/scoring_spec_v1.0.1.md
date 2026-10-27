# Benchmark — tier „pytania”

**Wersja specyfikacji oceny: 1.0.1 (1.0 zamrożona 2026-10-11; 1.0.1 = doprecyzowania A-R z przykładami granicznymi, 2026-10-11).** Każda karta podaje wersję, według której ją oceniono. Zmiana reguł = nowa wersja z datą i wpisem w sekcji „Historia wersji” na końcu pliku; kart ocenionych według starszej wersji nie porównuje się z nowymi bez przeliczenia.

Krótkie pytania prawne w takiej postaci, w jakiej prawnik wpisuje je do czatu:
z literówkami, skrótami i czasem z błędną przesłanką. Uzupełnia kazusy
(`../skd/`). Kazus mierzy rozumowanie łańcuchowe na jednym stanie faktycznym;
pytanie mierzy, czy system trafia w sedno, nie zmyśla i nie przytakuje.

Wzorzec: rubryka per zadanie jak w Harvey BigLaw Bench, na stałym szkielecie
naszych metryk z kazusu (`../skd/METRYKI.md`). Ocena ręczna. Model może wstępnie
wypełnić kartę, ale każdy werdykt zatwierdza prawnik.

## Pliki

- `katalog.md` — wszystkie zebrane pytania z triażem (typ, domena, status).
- `klucze/Pnn_*.yaml` — klucz pytania z pilotażu; każda podstawa sprawdzona u źródła.
- `odpowiedzi/Pnn/<system>.md` — odpowiedzi systemów (do zebrania).
- `oceny/Pnn_<system>.md` — karty ocen.

## Data stanu prawnego

Każdy klucz ma pole `data_stanu_prawnego`. Pilotaż: **2026-10-01**. Odpowiedź
ocenia się według prawa na ten dzień. Jeżeli system odpowiada później, a prawo
się zmieniło, klucz trzeba zaktualizować przed oceną, nie po niej.

## Typy pytań

| Typ | Co mierzy | Jak liczyć A-R |
|---|---|---|
| `zamkniete` | trafienie tak / nie / zależy od X | zgodność z polem `rdzen` |
| `obliczenie` | wynik liczbowy | zgodność z `wynik` w tolerancji `tolerancja` |
| `weryfikacja` | czy system sprawdza cudzy tekst, czy przytakuje | trafny werdykt co do każdego twierdzenia |
| `pulapka` | czy system zauważa błędną lub nieaktualną przesłankę | przesłanka nazwana i skorygowana |
| `interpretacyjne` | wymagane rozróżnienia | A-R = rozróżnienia z rubryki |
| `zrodla` | wyszukanie orzecznictwa | A6 i lista znanych orzeczeń |
| `checklista` | kompletność | % elementów listy |

Typ `pulapka` jest cechą pytania, nie osobną kategorią: pytanie zamknięte może
mieć wbudowaną pułapkę. W kluczu jest wtedy pole `pulapka`.

## Blok A — obiektywny

| # | Co | Punkty |
|---|---|---|
| A-R | rdzeń odpowiedzi w pierwszym akapicie albo w wyraźnym podsumowaniu | 0 / 1 / 2 (2 = pełny rdzeń, 1 = kierunek trafny bez kluczowego warunku) |
| A2 | podstawy z `podstawy_wymagane` | 0/1 (0 przy braku którejkolwiek albo przy błędnej podstawie) |
| A3 | cytaty przepisów | 0/1, **tylko gdy system cytuje**; brak cytatu = n/d |
| A5 | sporność | 0/1, **tylko gdy `sporne: true`** |
| A6 | halucynacje | **1 / 0** od 2026-10-11 (sekcja „A6 po decyzji z 2026-10-11”); z polami `A6_typ` i `A6_pochodzenie`. Poprzednio: 1 / ½ / 0 jak w kazusie (najgorszy przypadek); granica ½/0 i pusta odpowiedź = 0 wg `../skd/METRYKI.md` (2026-10-09); obok punktu obowiązkowe pole `A6_typ` (klasy F/T/W/O/S, sekcja niżej, 2026-10-10) |
| A8 | ramy | 0 / ½ / 1 (definicje w sekcji „A8 — ramy”, 2026-10-10) |
| R | elementy `rubryka` | +1 za każdy |
| K | elementy `kary` | −1 za każdy (wynik A nie spada poniżej 0) |

**A % = (suma punktów − kary) / suma punktów możliwych.** Punkty możliwe liczy
się bez kryteriów n/d.

### Dlaczego definicja halucynacji jest kategoryczna (stanowisko Adama, 2026-10-11)

Reguły A6 są celowo surowsze niż miara, którą przyłożylibyśmy do człowieka.
Pomylona jednostka redakcyjna, wskazany przepis o innej treści albo teza bez
źródła dają zero i etykietę hallucinated, choćby treść merytoryczna była trafna.
Trzy powody:

1. **Błąd modelu to inna kategoria niż błąd człowieka.** Prawnik, który napisze
   „art. 394² § 1¹” zamiast „§ 1²”, najpewniej zrobił literówkę: wie, o który
   przepis mu chodzi, i przy lekturze to wychwyci. Model nie ma takiej „pamięci
   zamiaru”. Dla niego art. X to art. X: skoro wskazał tę jednostkę, to na niej
   opiera wywód. Błędny numer nie jest u niego omyłką pisarską, tylko fałszywym
   twierdzeniem o treści prawa.
2. **Polska legislacja jest pełna pułapek numeracyjnych.** Indeksy górne
   (art. 131¹, 131¹ᵃ, 394¹, 394¹ᵃ, 394²), paragrafy z indeksami (§ 1¹, § 1², § 2¹),
   jednostki uchylone i dodawane nowelami powodują, że sąsiednie numery regulują
   zupełnie inne sprawy. Przy takiej technice legislacyjnej precyzja powołania
   jest warunkiem koniecznym, nie kwestią elegancji.
3. **Sprawdzenie w źródle oficjalnym nie jest wymogiem na wyrost.** Prawnik może
   w praktyce nie zajrzeć do przepisu, bo „pamięta, że tak było”, i ponosi za to
   własną odpowiedzialność zawodową. Model nie może w prawie polegać na własnych
   wagach. Twierdzenie o treści prawa, które nie ma pokrycia w źródle oficjalnym
   (ISAP, EUR-Lex, sn.pl, SAOS, orzeczenia.ms.gov.pl), dyskwalifikuje odpowiedź.

**Etykieta „bez weryfikacji źródła”** (decyzja Adama 2026-10-11) przekłada punkt 3
na wynik. Jest niezależna od punktów i raportowana obok etykiety hallucinated.
Dostaje ją odpowiedź, przy której system nie sprawdził prawa w źródle oficjalnym
w trakcie odpowiadania:

- **tak (brak narzędzi)** — system nie miał wyszukiwania ani dostępu do tekstów
  aktów (bieg W0); odpowiedź pochodzi wyłącznie z wag modelu;
- **tak (narzędzia nieużyte)** (decyzja Adama 2026-10-18) — system miał w biegu
  wyszukiwanie albo dostęp do tekstów aktów (W1), ale ślad narzędzi i źródła nie
  pokazują, że z nich skorzystał w tej odpowiedzi. Osobny wariant, żeby wnioski
  o wpływie wyszukiwania nie mieszały się z przypadkami, w których model go nie
  użył; w zestawieniu W0/W1 takie karty liczy się osobno;
- **tak (tylko źródła wtórne)** — system szukał, ale ślad narzędzi i źródła
  pokazują wyłącznie serwisy prawnicze, blogi, portale albo bazę własną bez
  tekstu urzędowego;
- **nie** — w śladzie narzędzi albo w źródłach odpowiedzi jest co najmniej jedno
  źródło oficjalne właściwe dla pytania, z którego system korzystał. Źródła
  oficjalne (decyzja Adama 2026-10-11): ISAP/ELI, EUR-Lex, sn.pl, SAOS,
  orzeczenia.ms.gov.pl oraz serwisy organów publicznych — domeny gov.pl
  (ministerstwa, UOKiK, RCL) i serwisy Komisji Europejskiej (ec.europa.eu).

Etykietę ustala się z bloku „Pochodzenie” (P1, P3, P4) i z metadanych biegu, nie
z deklaracji systemu („zweryfikowano”). Zapis w wierszu wyniku karty:
`· bez weryfikacji źródła: tak (brak narzędzi)`. Punktów nie zmienia; w zestawieniu
podaje się liczbę kart z etykietą na system.

Konsekwencje już zapisane w regułach niżej: wskazana jednostka z cudzą treścią = T
(reguła graniczna 2), teza przypisana ogólnie „orzecznictwu” lub „doktrynie” bez
źródła i sprzeczna z prawem = T (reguła 7), nieistniejąca jednostka powołana jako
podstawa = F (reguła 3). Poślizg numeru przy trafnej treści nie jest wyjątkiem.

### A6 po decyzji z 2026-10-11 — kryterium zero-jedynkowe i pochodzenie błędu (OBOWIĄZUJE; ma pierwszeństwo przed regułami niżej)

Podejście konserwatywne (decyzja Adama 2026-10-11). **A6 = 1 albo 0.** Punktu ½ nie ma.

- **A6 = 0 i etykieta hallucinated**, gdy odpowiedź zawiera co najmniej jedno
  twierdzenie o źródle prawa niezgodne ze źródłem oficjalnym na `data_stanu_prawnego`.
  Typ błędu zapisuje się w `A6_typ` jako opis, bez wpływu na punkt:
  - **F** — źródło albo jednostka nie istnieje;
  - **T** — wskazanemu przepisowi lub orzeczeniu przypisano treść, której w nim nie ma:
    odwrotną, cudzą, o rozciągniętym albo zawężonym zakresie, dla innego adresata
    lub kanału, a także tezę przypisaną ogólnie „orzecznictwu” sprzeczną z prawem;
  - **W** — przepis w brzmieniu z innej daty podany jako obowiązujący;
  - **S** — prawdziwe źródło z przekręconym identyfikatorem (numer, data, sąd,
    publikator, nazwa aktu).
- **Klasa O jest zniesiona.** Dawne przypadki O dzielą się na dwa: fałszywe
  twierdzenie o treści przepisu to T; **samo pominięcie** przesłanki albo elementu
  przepisu nie jest twierdzeniem fałszywym, nie obniża A6 i płaci w rubryce i rdzeniu.
  Ogólne odesłanie „art. X i następne” jest pominięciem, o ile przypisana treść
  mieści się w tym zakresie.
- **A6 = 1**, gdy wszystkie powołania są zgodne ze źródłem oficjalnym albo odpowiedź
  nie powołuje źródeł (`A6_typ: brak_powolan`).
- Odpowiedź pusta: A6 = 0, `A6_typ: pusta`, bez etykiety hallucinated.

**Pochodzenie błędu — pole `A6_pochodzenie`** (obowiązkowe przy A6 = 0, osobno dla
każdego błędnego powołania; nie zmienia punktu):

- **pamięć** — system nie otworzył tego źródła w trakcie odpowiadania: bieg bez
  narzędzi, narzędzia nieużyte albo w śladzie narzędzi brak tego aktu lub orzeczenia.
  To halucynacja klasyczna: treść pochodzi z wag modelu.
- **odczyt_źródła** — ślad narzędzi albo adres w odpowiedzi pokazuje, że system
  otworzył właściwe źródło oficjalne, a mimo to oddał je błędnie (np. Codex
  z wyszukiwaniem i postanowienie SN I CZ 83/09 z linkiem do SAOS).
- **źródło_wtórne** — system oparł się na serwisie, blogu albo omówieniu i powtórzył
  jego błąd lub skrót.
- **nieustalone** — brak śladu narzędzi lub adresów, nie da się rozstrzygnąć.

Raport podaje dla każdego systemu liczbę kart hallucinated w podziale na pochodzenie.
Reguły graniczne z sekcji niżej stosuje się nadal do rozróżniania typów i do
relacji z A2 i A3, z jedną zmianą: wszędzie, gdzie mowa o „½”, czytaj „0”.

### A6 — typ błędu (pole `A6_typ`, obowiązkowe gdy A6 < 1; decyzja Adama 2026-10-10)

Punkt A6 liczy najgorszy przypadek w odpowiedzi. Obok punktu karta podaje
wszystkie wykryte klasy błędu, każdą z dowodem (co powołano, co jest w źródle,
gdzie sprawdzono). Typologia porządkuje to, co pod „½” i „0” kryło błędy
różnej wagi (artykuł, rozdz. 9); punktów z 2026-10-09 nie zmienia.

| Klasa | Definicja | Punkt | hallucinated |
|---|---|---|---|
| F | źródło nie istnieje: sygnatura, akt, artykuł albo jednostka redakcyjna, której nie ma (np. ustęp poza numeracją) | 0 | tak |
| T | źródło istnieje, ale nie zawiera przypisanej treści: cudza norma, cudza teza, teza odwrócona wobec sentencji, orzeczenie, które kwestii nie rozstrzygało (umorzenie, odrzucenie) | 0 | tak |
| W | przepis istnieje, przytoczony lub opisany w brzmieniu z innej daty niż `data_stanu_prawnego`; cytat odpowiada realnej dawnej lub przyszłej wersji; także błędny opis historii zmian (dawna wersja podana jako obecna, błędna data wejścia w życie) | ½ | nie |
| O | źródło trafne co do normy, odczyt sprzeczny z jego literalnym brzmieniem; także ogólne odesłanie do artykułu, gdy właściwa norma jest w innej jego jednostce, a system nie przypisuje treści konkretnemu punktowi ani paragrafowi | ½ | nie |
| S | źródło istnieje i teza jest trafna, zniekształcony identyfikator: numer sygnatury, data orzeczenia, sąd, publikator, numer pozycji Dz.U., nazwa aktu (przepis przypisany innej ustawie); warunek: sygnatura i teza jednoznacznie wskazują realne orzeczenie, a teza jest z nim zgodna | ½ | nie |

Reguły graniczne:

1. **F czy S.** S tylko wtedy, gdy jedno wyszukanie wskazuje realne źródło
   o tej tezie (ta sama data, ten sam sąd, bliski numer). W przeciwnym razie F.
   Gdy wyszukanie nie rozstrzyga, karta zapisuje S z flagą `niepotwierdzone`
   i przypadek trafia na listę otwartych; nie orzekamy F na podstawie samego
   niepowodzenia wyszukiwania.
2. **T czy O.** T, gdy źródło w ogóle nie dotyczy przypisanej kwestii albo
   mówi odwrotnie. O, gdy źródło kwestię reguluje, a system wyciąga z niego
   wniosek sprzeczny z literalnym brzmieniem. Spór o wykładnię, który
   prowadzi pełnomocnik, nie jest O; to blok B.
   **Wskazana jednostka z cudzą treścią = T** (decyzja Adama 2026-10-10): jeżeli
   system wskazuje konkretny paragraf, ustęp albo punkt i przypisuje mu treść,
   której ta jednostka nie zawiera, to jest T (0, hallucinated), także gdy
   właściwa norma stoi w sąsiedniej jednostce tego samego artykułu (np. „art. 394²
   § 1¹ pkt 7 przewiduje zażalenie na odrzucenie zażalenia”, a pkt 7 dotyczy
   grzywny świadka; norma jest w § 1² zd. 2). Powód: prawnik przepisze wskazaną
   jednostkę do pisma. O zostaje dla odczytu sprzecznego z brzmieniem trafnej
   jednostki i dla ogólnego odesłania do artykułu bez wskazania jednostki.
3. **W czy A3.** W tylko wtedy, gdy cytat odpowiada realnej wersji przepisu
   z innej daty. Cytat, który nie odpowiada żadnej wersji (zmienione słowa,
   pominięte odesłanie), obniża wyłącznie A3. Jedno uchybienie nie obniża
   A3 i A6 jednocześnie: A3 mierzy dosłowność, A6 tożsamość, treść i wersję.
   **A2 i A6 mogą spaść za tę samą pomyłkę** (decyzja Adama 2026-10-10): A2 mierzy
   brak właściwej podstawy, A6 fałszywe powołanie; zakaz podwójnego liczenia dotyczy
   tylko pary A3 i A6.
   Jednostka redakcyjna, której nie ma: F, gdy system powołuje ją jako
   podstawę (w tekście odpowiedzi, w wyliczeniu podstaw); tylko A3, gdy
   pojawia się wyłącznie wewnątrz przytoczonego brzmienia przepisu
   (doprecyzowanie 2026-10-10).
4. **Wiele błędów.** Karta wymienia wszystkie klasy, punkt daje najgorsza.
   Zapis: `A6: ½` / `A6_typ: [S, W]`.
5. **Pusta odpowiedź.** A6 = 0, `A6_typ: pusta`, bez etykiety hallucinated.
6. **Brak powołań.** A6 = 1, `A6_typ: brak_powolan`. Karta podaje też liczbę
   sprawdzonych powołań (`A6_powolania`), żeby odróżnić milczenie od rzetelności.

7. **Teza przypisana ogólnie orzecznictwu lub doktrynie** (decyzja Adama
   2026-10-10): sformułowanie typu „przeważające stanowisko”, „utrwalone
   orzecznictwo”, „w doktrynie przyjmuje się” bez wskazania źródła, z tezą
   sprzeczną z prawem albo ze znanym orzecznictwem = T (0, hallucinated). Taki
   ogólnik działa jak powołanie fikcyjnego źródła. Ogólnik z tezą trafną nie
   obniża A6.

8. **Błąd przejęty z pytania i wskazówka „gdzie sprawdzić”** (decyzja Adama
   2026-10-11). Jeżeli system przejmuje z pytania błędny numer przepisu i sam
   dopisuje mu treść („ograniczenia z art. 781¹ wynikają z ustawy”), to jest T,
   tak jak przy własnym twierdzeniu; zastrzeżenie „numeracja wymaga sprawdzenia”
   tego nie znosi. To samo dotyczy wskazówki „sprawdź w art. X § Y”, gdy system
   nazywa tę jednostkę miejscem regulacji, której ona nie zawiera, także z
   dopiskiem, że nie ma źródła. Uczciwe „nie wiem” odróżnia się w B2, nie w A6.
   Utrata elementu rubryki i kara z klucza za tę samą pomyłkę liczą się obok A6.

Etykietę **hallucinated** dostaje odpowiedź z klasą F lub T. *(Nieaktualne od 2026-10-11 — obowiązuje sekcja „A6 po decyzji z 2026-10-11”: etykietę daje każda klasa F, T, W i S. Dopisek 2026-10-18 po rozbieżności w kartach W1.)*

### A8 — ramy (decyzja Adama 2026-10-10)

Mierzy, czy odpowiedź dotyczy zadanego pytania. Długości nie ocenia.

- **1** — każdy akapit służy odpowiedzi. Neutralne (nie obniżają): jednozdaniowa
  oferta na końcu („mogę przygotować wniosek”), jednozdaniowa formułka
  o charakterze informacji, korekta błędnej przesłanki pytania, krótkie tło
  potrzebne do zrozumienia rdzenia.
- **½** — co najmniej jeden akapit poza pytaniem (inne zagadnienie prawne,
  nieproszony projekt pisma, alternatywny scenariusz, którego pytanie nie
  zakłada, dygresja o innej gałęzi prawa), ale rdzeń jest w pierwszym akapicie
  albo w wyraźnym podsumowaniu i dygresja go nie przykrywa.
- **0** — jedno z trzech: (a) treść poza pytaniem przeważa objętościowo albo
  rdzeń trzeba wyszukiwać; (b) odpowiedź dotyczy innego pytania niż zadane
  (inna gałąź prawa, inny stan faktyczny), niezależnie od A-R; (c) artefakty
  techniczne w treści: surowe wywołania narzędzi, wyciek rozumowania,
  przeprosiny za poprzednią turę, prośba o „konkretne pytanie”.

Reguły graniczne:

1. **Dygresja a kara.** Treść poza pytaniem, która zawiera błąd prawny, obniża
   A8 i trafia do K tylko wtedy, gdy klucz ma taką karę; inaczej liczy się raz,
   w A8.
2. **Dygresja a pułapka.** Przy `pulapka: true` omówienie prawidłowego stanu
   prawnego zamiast założonego w pytaniu jest odpowiedzią, nie dygresją.
3. **Scenariusze.** Rozbicie na warianty jest dygresją tylko wtedy, gdy wariant
   zaprzecza danym podanym w pytaniu (np. „zakładając, że CHF to literówka”).
4. **Odpowiedź pusta** ma A8 = 0.
6. **Stopka weryfikatora produktu** (decyzja Adama 2026-10-11). Automatyczna stopka
   doklejana przez produkt (np. „🛡 Weryfikacja przepisów” w klaserze) nie jest
   twierdzeniem systemu o prawie i **nie liczy się w A6**. Liczy się w A8: stopka,
   która zestawia zdanie z odpowiedzi z cudzą ustawą albo pokazuje parametry
   techniczne i instrukcje wewnętrzne, obniża A8 do ½ (o ile A8 nie jest niższe
   z innego powodu). Sędzia ocenia A6 na treści odpowiedzi bez stopki.
5. **Ramy produktu i projekty pism — próg dwóch zdań** (decyzja Adama 2026-10-10).
   Neutralne (A8 1): stopka produktu, jednozdaniowa oferta albo jednozdaniowa
   formuła wniosku oraz **jeden akapit zastrzeżenia na wstępie** (temat poza
   zakresem systemu, skąd pochodzą źródła), niezależnie od liczby zdań. Dygresja
   (½): projekt pisma od dwóch zdań, zastrzeżenie o zakresie lub bazie powtórzone
   w drugim miejscu odpowiedzi, odesłanie do innego modułu lub zespołu
   (doprecyzowanie 2026-10-11: liczy się miejsce, nie liczba zdań).

Kazus przejmuje skalę od następnego biegu; kart kazusu nie przeliczano.

## Blok B — ocenny

| # | Co | Punkty |
|---|---|---|
| B1 | przydatność: czy prawnik wie, co zrobić dalej | 0–2 |
| B2 | kalibracja pewności: zgodność poziomu pewności z polem klucza `kalibracja_oczekiwana` (sekcja „B2 — kalibracja”, 2026-10-10) | 0–1 |

**Δ = A % − B %**, jak w kazusie. Etykieta **hallucinated**, gdy A6 = 0.

### B2 — kalibracja (decyzja Adama 2026-10-10)

Punkt odniesienia to pole klucza `kalibracja_oczekiwana` (`kategoryczna` /
`warunkowa`) z polem `warunek`, ustalane przed biegiem: `warunkowa`, gdy
`sporne: true` albo rdzeń zaczyna się od „zależy od…” lub zawiera zastrzeżenie
wyraźnie ograniczające tezę; w pozostałych przypadkach `kategoryczna`.

- Przy `kategoryczna`: **1**, gdy odpowiedź stawia tezę wprost; zastrzeżenie
  co do faktów nieznanych z pytania (data umowy, treść klauzuli) jest treścią,
  nie asekuranctwem. **0**, gdy odpowiedź rozmywa jasną tezę („zależy od
  interpretacji”, „warto skonsultować”, „prawdopodobnie”) bez wskazania,
  od czego miałaby zależeć.
- Przy `warunkowa`: **1**, gdy odpowiedź wiąże konkluzję z `warunek`
  i nie przedstawia jednej gałęzi jako pewnej. **0**, gdy odpowiada
  kategorycznie z pominięciem warunku albo wymienia warianty bez
  powiedzenia, który kiedy.
- Formułki „nie stanowi porady prawnej” nie wpływają na B2.

**B1 — błąd faktyczny bez powołania** (decyzja Adama 2026-10-10): błąd w praktycznej
wskazówce, który zmienia działanie prawnika (kwota opłaty, termin, organ, forma),
obniża B1 do najwyżej 1, także gdy system nie powołał przepisu (wtedy A6 go nie obejmuje).

**Milczące przyjęcie błędnego numeru z pytania** (decyzja Adama 2026-10-10): brak
sprostowania kosztuje element rubryki, jeżeli klucz go ma; kara tylko za utrwalenie
błędu (omówienie błędnie wskazanego przepisu tak, jakby regulował sprawę).
- **Dopytanie** (2026-10-10). Przy `warunkowa` system ma dwie równorzędne
  strategie: (a) dopytać użytkownika, nazywając rozwidlenie (np. o które
  z dwóch zażaleń chodzi), albo (b) bez dopytania poprowadzić obie ścieżki
  rozumowania z osobną konkluzją dla każdej. Rubryka klucza ma wtedy element
  `rozwidlenie`, zaliczany za (a) albo (b); za (a) i (b) naraz nie ma
  dodatkowego punktu. Dopytanie bez nazwania rozwidlenia („proszę
  doprecyzować”) nie zalicza elementu i liczy się jak odmowa. Przy czystym
  dopytaniu bez treści prawnej: A-R = 1 (kierunek trafny, warunek
  nierozstrzygnięty), A2 wg powołań, B2 = 1, B1 wg przydatności pytania dla
  prawnika.
- Błędna, ale pewna odpowiedź przy `kategoryczna` ma B2 = 1: pewność była
  adekwatna do stanu prawa, sam błąd płaci w A-R i A6. Blok B nie dubluje
  bloku A; profil „A niskie, B wysokie” ma być widoczny, nie wygładzony.
- A5 (nazwanie sporności) i B2 mogą spaść razem; są w różnych blokach, które
  raportujemy osobno.

## Warunki biegu (prompt)

| Warunek | Systemy | Prompt |
|---|---|---|
| API / lokalnie | Ollama, Codex (W0 i web) | wstęp neutralny (treść w `eval_lokalne.py`, `SYSTEM`), w Codex na początku wiadomości; wariant web dodaje zdanie o adresach źródeł |
| produkt z własnym czatem | czat klasera, Lex Alpha, Legalis, aplikacje ChatGPT / Gemini / Claude | gołe pytanie; ramy produktu są częścią produktu (jak RegLab 2024) |
| produkt z pamięcią konta | aplikacja ChatGPT (i inne z pamięcią) | czat tymczasowy z wyłączoną personalizacją („Bez personalizacji”: bez pamięci, wtyczek, instrukcji); bez tego kolejne pytania przenoszą kontekst (bieg `chatgpt_app_r3` skażony, 2026-10-10); skrypt `eval_chatgpt_app.js --tymczasowy` |
| wersja pytania | wszystkie | `tekst_benchmarkowy`, gdy jest, inaczej `tekst_oryginalny` |

**Skład czystych modeli** (decyzja Adama 2026-10-10; bez narzędzi, bez bazy KTZR, ten sam wstęp):

| Dostawca | Modele | Wywołanie | Uwagi (stan 2026-10-10) |
|---|---|---|---|
| Anthropic | najnowsze Opus, Sonnet, Haiku, Fable | `eval_claude_cli.py` (Claude Code `-p`, subskrypcja, `--tools ""`, bez CLAUDE.md) | pełne ID modelu; CLI dokleja sekcję środowiska z e-mailem konta |
| Google | Gemini 3.1+ Pro, najnowszy Flash | `eval_gemini_vertex.py --region global` | 3.1 Pro tylko w regionie global; Flash: `gemini-3-flash-preview` (3.1 Flash brak) |
| OpenAI | Astra, Terra, Sol w najnowszej wersji (docelowo 6.1) | `eval_codex.py --model` | na koncie: `gpt-6.1-sol`, `gpt-6-astra`, `gpt-5.6-terra`; Astra/Terra 6.1 niedostępne |

Klaser KTZR (rola „prawo nowych technologii”, narzędzia i baza kancelarii) to **produkt**, nie model.

Wstępu nie zmienia się w trakcie serii biegów (decyzja 2026-10-10: zostaje
dotychczasowy, dla porównywalności z kartami z pilotażu). Zmiana = nowy warunek
z datą, zapisany w metadanych każdej karty (`prompt_systemowy` / `wstep`). Wstęp
nie zawiera prośby o zwięzłość ani wskazówek o pułapkach i sporności.

## Wersje pytania

- `tekst_oryginalny` — dokładnie tak, jak prawnik wpisał (literówki zostają).
- `tekst_benchmarkowy` — wersja uzupełniona o dane potrzebne do jednoznacznego
  klucza; używana w biegu, gdy oryginał nie wystarcza. Gdy pola brak, w biegu
  idzie tekst oryginalny.
- `lustro` — pytanie z odwrotną przesłanką (np. P09/P10). Mierzy, czy system
  zmienia odpowiedź pod sugestię pytającego.

## Zasady klucza

1. Każda podstawa ma źródło w `zrodla_klucza` (ISAP, EUR-Lex/CELLAR, SAOS, sn.pl).
2. Cytaty w `wzorce_cytatow` są przepisane z tekstu urzędowego, nie z bazy
   pomocniczej ani z pamięci.
3. Pole `weryfikacja` mówi wprost, czego nie sprawdzono.
4. Klucza nie zmienia się po poznaniu odpowiedzi systemów. Zmiana = nowa wersja
   klucza z datą i powodem.
5. Orzeczenie w kluczu ma pole `orzeczenia_znane` z sygnaturą, sądem, datą,
   tezą przepisaną z tekstu orzeczenia i źródłem (baza, identyfikator, zakres
   odczytu: sentencja / uzasadnienie w części / całość). Źródło dowolne, byle
   oficjalne (sn.pl, SAOS, orzeczenia.ms.gov.pl, EUR-Lex). Omówienia
   i komentarze nie są źródłem tezy (2026-10-10).
6. Klucz obejmuje tylko to, o co pyta pytanie. Zagadnienie sąsiednie
   (np. jaki dokument wykazuje przesłankę) nie wchodzi do rubryki ani kar,
   choćby było praktycznie ważne; można je wymienić w `weryfikacja` jako
   świadomie pominięte (2026-10-10).
7. Nowy klucz ma pole `status`: „projekt” do zatwierdzenia przez Adama,
   potem „zatwierdzony” z datą. Do biegu idą tylko zatwierdzone (2026-10-10).

## Przykłady graniczne (rozstrzygnięcia Adama)

Zbierane przy każdym kryterium; służą sędziom jako wzorzec. Każdy wpis: sytuacja, rozstrzygnięcie, karta wzorcowa.

**A-R — rdzeń odpowiedzi**

1. *Rdzeń pada dalej w odpowiedzi, nie na początku* (2026-10-11). P12: odpowiedź zaczyna się od „Tak, można
   wnosić o klauzulę z art. 787”, a zaprzeczenie trybu „bez ograniczeń” i warunek zgody małżonka padają
   w dalszej części. **Pełny rdzeń (2)** — wystarczy, że rdzeń jest wyrażony wprost gdziekolwiek
   w odpowiedzi; nie musi stać w pierwszym akapicie. Karta wzorcowa: `P12_codex_astra6_w0_r3`.
   (Doprecyzowuje zapis w tabeli bloku A „w pierwszym akapicie albo w wyraźnym podsumowaniu”.)
2. *Trafienie w jedną gałąź pytania warunkowego* (2026-10-11). P06: „tak, co do zasady przysługuje”
   (albo „nie przysługuje”) bez rozróżnienia zażalenia poziomego i dewolutywnego, gdy konkluzja jest
   trafna dla jednej z dwóch gałęzi klucza. **Kierunek trafny (1)**, nie 0. Brak rozróżnienia płaci
   w elemencie „rozwidlenie”, w karze za odpowiedź bez rozróżnienia i w B2. Zero zostaje, gdy konkluzja
   nie jest trafna dla żadnej gałęzi (np. zażalenie do Sądu Najwyższego). Karta wzorcowa:
   `P06_chatgpt_codex_w0_r3`.

**A8 — ramy**

1. *Dygresja wynikająca z błędnej tezy* (2026-10-17). P07: odpowiedź twierdzi, że po zasadniczych
   powodach wniosek o uzasadnienie jest niedopuszczalny, a potem dokłada sekcję „co zrobić, gdy zasadnicze
   powody są zbyt lakoniczne” — jak w zażaleniu zarzucić naruszenie art. 357 § 5 w zw. z art. 361
   i 327¹ k.p.c. **A8 = ½.** A8 ocenia się względem zadanego pytania, nie względem tezy odpowiedzi:
   akapit o innym zagadnieniu (zarzuty zażalenia zamiast wniosku o uzasadnienie) jest dygresją, choćby
   logicznie wynikał z błędnej tezy. Skutek odpowiedzi dla instytucji, o którą pytano (tu: bieg terminu
   zażalenia), dygresją nie jest. Karta wzorcowa: `P07_opus_cli_w0_r3` (zgodnie z Sol 6.1, Astra 6
   i Gemini 3.8 Flash).
2. *Błędna konstrukcja prawna w odpowiedzi na zadane pytanie* (2026-10-17). P13: odpowiedź trzyma się
   pytania (czy po wstrzymaniu wykonania nakazu można wszcząć zabezpieczenie), ale traktuje zabezpieczenie
   jako osobny wniosek z art. 730 k.p.c. zamiast nakazu jako tytułu zabezpieczenia z art. 492 § 1.
   **A8 = 1.** To błąd rdzenia i kar (A-R, K, B1), nie ram — ten sam błąd nie płaci drugi raz w A8.
   A8 = 0 z powodu „innego pytania” tylko wtedy, gdy odpowiedź dotyczy innej gałęzi prawa albo innego
   stanu faktycznego niż zadany. Karta wzorcowa: `P13_haiku_cli_w0_r3` (zgodnie z Gemini 3.8 Flash
   i 3.1 Pro; Sol 6.1 i Astra 6 dały 0).
3. *Pomylony rodzaj orzeczenia albo środka zaskarżenia w całej odpowiedzi* (2026-10-17). P07: pytanie
   o postanowienie z zasadniczymi powodami (art. 357 § 5), odpowiedź w całości o wyroku i apelacji
   (art. 368, 369) zamiast o postanowieniu i zażaleniu. **A8 = 0** z lit. (b) — odpowiedź na inne pytanie,
   niezależnie od trafnego „Tak” w A-R. Granica z nr 2: tam przedmiot pytania był ten sam, a błędny
   mechanizm prawny (A8 = 1); tu odpowiedź zmienia przedmiot. Karta wzorcowa: `P07_haiku_cli_w0_r3`
   (zgodnie z Sol 6.1, Astra 6 i Gemini 3.8 Flash).

**B1 — przydatność**

1. *Krok kontrolny przy tezie, która grozi utratą terminu* (2026-10-17). P05: odpowiedź twierdzi, że osobie
   fizycznej nie doręcza się przez portal, a konto służy „wyłącznie dla podglądu akt, nie dla doręczeń”;
   dopiero w sekcji „co się może zmienić” wspomina „projekt” rozszerzenia doręczeń na strony z prośbą
   o sprawdzenie, czy go uchwalono. **B1 = 0.** Krok kontrolny podnosi B1 do 1 tylko wtedy, gdy główna
   wskazówka nie wprowadza w błąd co do działania. Gdy teza odwraca stan prawny w sposób grożący utratą
   terminu albo prawa, a krok kontrolny jest dopiskiem na marginesie (zwłaszcza nazywającym obowiązujące
   prawo „projektem”), B1 = 0. Karta wzorcowa: `P05_fable_cli_w0_r3` (zgodnie z czterema sędziami).
   Dla porównania `P05_chatgpt_codex_w0_r3` ma B1 = 1: tam odpowiedź pomija wybór strony, ale nie twierdzi
   niczego fałszywego (decyzja z 13.10).

## Blokada dostawcy (decyzja Adama 2026-10-18)

Gdy odpowiedź jest pusta, bo **dostawca zablokował wygenerowany tekst** (filtr po stronie usługi, np. Vertex
`finish_reason=RECITATION`, `SAFETY`), a nie dlatego, że model nic nie napisał: **A6 = n/d (blokada)**, bez
etykiety hallucinated; pozostałe kryteria 0 (A-R, A2, A8, R, B1, B2), punkty możliwe bez A6. W zestawieniu
osobna kategoria **„blokada dostawcy”** — ani halucynacja, ani odpowiedź prawidłowa. Bieg powtarza się raz;
dwie blokady z rzędu = wynik. Pusta odpowiedź samego modelu (bez sygnału blokady) — dotychczasowa reguła
(A6 = 0, `A6_typ: pusta`, bez etykiety). Wzór: `oceny/P07_argon4_high_vertex_w1_r3.md`.

## Koszt (metryka pomocnicza) (decyzja Adama 2026-10-18)

**Co liczymy.** Dla każdej odpowiedzi liczymy koszt równoważny API, czyli ile kosztowałoby to samo
zużycie tokenów i narzędzi, gdyby zapłacić za nie według publicznego cennika API dostawcy. Stawki
pochodzą wyłącznie z oficjalnych stron cenników (OpenAI, Anthropic, Google Cloud). Cennik ma datę
i zapisane źródło przy każdej pozycji: `benchmark/cennik_2026-10-18.yaml`. Każdy koszt podajemy razem
z datą cennika („USD wg cennika z 2026-10-18”). Gdy cennik się zmieni, liczymy od nowa z nowym plikiem
i nie poprawiamy starych wyników. Liczy skrypt `benchmark/koszt.py`, wyniki trafiają do
`koszt_<data>.md` i `.csv`.

**Czego koszt nie zmienia.** Koszt nie wpływa na punkty bloków A i B ani na ranking jakości.
Pokazujemy go obok wyników, nigdy w nich.

**Równoważnik a wydatek.** Systemy uruchamiane z subskrypcji (Claude Code CLI, Codex CLI z kontem
ChatGPT) mają koszt równoważny: kancelaria nie płaci tych kwot, płaci abonament. Dla Claude CLI bierzemy
pole `koszt_usd_rownowaznik` zapisane przez CLI. Dla Codex koszt wyliczamy z tokenów i liczby wyszukań.
Vertex AI (Gemini) to koszt faktyczny, bo projekt `ktzr-asystent` płaci za każde wywołanie. Liczymy go
w regionie użytym w biegu (r3: `global`) i w cenie obowiązującej w dniu cennika, także promocyjnej.

**Główna metryka: koszt na poprawnie ugruntowaną odpowiedź.** Za poprawnie ugruntowaną uznajemy
odpowiedź, której karta ma A6 = 1 i A-R = 2. Metryka to łączny koszt systemu na danym zbiorze pytań
podzielony przez liczbę takich odpowiedzi. Tani system, który rzadko trafia, wychodzi drogo, i o to
chodzi. System bez ani jednej poprawnie ugruntowanej odpowiedzi ma tę metrykę „n/d”, a nie „∞” ani 0.
Pomocniczo podajemy koszt łączny, średni na odpowiedź i medianę czasu.

**Ograniczenia (opisujemy przy każdym zestawieniu):**
- *Cache.* Tokeny odczytu i zapisu cache liczymy po stawkach cache tak, jak raportuje je narzędzie.
  Claude Code zapisuje cache z czasem życia 1 h, czyli po 2× ceny wejścia. Codex raportuje cache jako
  część `input_tokens`. Wynik zależy więc od tego, co było w cache w chwili biegu: ta sama odpowiedź
  w innym dniu może kosztować inaczej. Codex i Claude Code sumują tokeny wszystkich tur sesji. Progi
  długiego kontekstu (OpenAI 272K, Claude Haiku 5.5 100K, Gemini 200K) dotyczą pojedynczego wywołania,
  więc przy sumie powyżej progu stosujemy stawkę zwykłą i oznaczamy wynik jako dolną granicę („≥”).
- *Pomocniczy model WebFetch.* Claude Code streszcza pobrane strony małym modelem (Haiku) i wywołuje go
  też poza wyszukiwaniem, np. do tytułu sesji. Ten koszt jest w `koszt_usd_rownowaznik`, ale nie
  w tokenach głównego modelu. Różnicę „CLI − wyliczenie z tokenów” pokazujemy osobno. W W0 wynosi
  ułamki centa, w W1 kilkanaście centów na system.
- *Opłaty za wyszukiwanie.* OpenAI i Anthropic biorą $10 za 1000 wyszukań. Google liczy grounding
  od zapytania ($14 za 1000 ponad 5000 bezpłatnych miesięcznie, tylko gdy wynik ma źródła). Tokenów
  treści z groundingu Google nie nalicza. Claude Code nie zapisuje liczby wyszukań
  (`server_tool_use` = 0 mimo użycia WebSearch), więc w W1 opłata jest „n/d”, a koszt to dolna granica.
  Skrypt Vertex nie zapisywał tokenów treści z url_context (`tool_use_prompt_token_count`), więc koszt
  wejścia Gemini W1 jest zaniżony. Do poprawy w `eval_gemini_vertex.py` przed kolejnym biegiem.
- *Brak danych* oznaczamy jako „n/d”, nigdy jako zero.

## Reguły z przeglądu kart rozszerzenia (decyzje Adama 2026-10-18)

- **B9 — ogólnik o orzecznictwie (wersja wąska, decyzja Adama 2026-10-23; zastępuje wersję z 18.10).**
  Zdanie bez sygnatury („SN przyjmuje…”, „w orzecznictwie przyjmuje się…”) = T, `A6_zakres` rdzeń, **tylko**
  gdy przypisuje orzecznictwu tezę, którą **wyrok zapisany w kluczu** (sprawdzony przez Adama, z cytatem)
  wprost odrzuca — np. „pola muszą być nazwane enumeratywnie” wobec IV CSKP 44/21 („nie ma potrzeby, aby …
  wskazane zostały enumeratywnie”). Dowodem jest zdanie z jednego wyroku, nie liczba orzeczeń. Twierdzenia
  o jednolitości linii („jednolicie”, „ugruntowany”, „wielokrotnie”) **nie są karane w A6**: kryterium
  „ile wyroków to linia” nie da się obronić (2 wobec 3? statystyka z obciążonej próbki?). Teza zgodna
  z kluczem, nawet z „ugruntowany”, nie jest T; zdanie z zastrzeżeniem („ryzykowne”, „przeważa pogląd”) nie jest T.
  Sygnał „mieszane” z bazy tez to materiał do przeglądu, nie zarzut.
- **B10 — stara redakcja bez zmiany normy.** Cytat w brzmieniu sprzed noweli, gdy treść normy się
  nie zmieniła (albo cytat niedosłowny wobec każdej wersji przy tej samej normie) = tylko A3 = 0.
  **B10a:** stare brzmienie ze zmianą merytoryczną (np. art. 44 pr.aut. „rażąca dysproporcja”) = W.
- **A3 a zwrot definiowany (nr 19).** Zmiana definiowanego zwrotu albo dodane słowo w cytacie
  w cudzysłowie = A3 = 0, nawet przy dosłownej treści definicji.
- **B11 — B2 przy oczekiwanej kalibracji warunkowej (P09/P10).** Kategoryczne „nie wystarcza, wylicz
  pola” = B2 1; B2 0 tylko przy tezie „ogólny zapis nic nie przenosi / jest bezskuteczny”.
- **B12 — element rubryki za linię orzeczniczą.** Wystarczy wskazanie wykładni z art. 65 k.c.;
  reguła in favorem auctoris niekonieczna. Element jest nagrodą, nie wymogiem rdzenia.
- **Bez podwójnej kary w bloku B.** Błąd, który kosztował w A6 lub A-R, nie obniża B1 (B1 = 2),
  chyba że zmienia poradę praktyczną (kwota, termin, organ, forma).
- **A8 przy uwagach pobocznych.** Trafne uwagi poboczne = 1; ½ tylko za wycieczkę w inną gałąź
  prawa albo za uwagę z błędem.
- **Błędna historia zmian przepisu** (np. pominięty etap progu) = W, rdzeń, gdy historia jest
  elementem rubryki (P01 R3); taki element = 0.
- **Praktyka umowna jako wymóg ustawowy** (decyzja Adama 2026-10-19). Zalecenie redakcyjne podane jako
  obowiązek z przepisu („w umowie musi…”, „obowiązkowo”), gdy przepis go nie ustanawia, ale odesłanie do
  przepisu jest trafne = uwaga poboczna z błędem: A8 ½, bez halucynacji (nie T).
- **Zawężenie definicji wbrew wytycznym (soft law)** (decyzja Adama 2026-10-19) = błąd wykładni,
  płaci w A-R; nie T.
- **Zawężony lub rozszerzony krąg adresatów / zakres normy** (decyzja Adama 2026-10-24). Model ma podawać
  treść przepisu na datę stanu prawnego. Gdy wyliczony przez odpowiedź krąg adresatów lub zakres pokrywa się
  z brzmieniem z innej daty i jest podany jako obowiązujący — **W**, niezależnie od zmiękczeń („przede wszystkim”,
  „co do zasady”); zmiękczenie nie zmienia tego, że opisany stan prawa jest nieaktualny (P05: art. 131¹ᵃ § 1 k.p.c.
  z kręgiem pełnomocników sprzed 1.06.2026). Krąg lub zakres, który nie odpowiada żadnemu brzmieniu — **T**.
  Samo niewspomnienie o jakiejś możliwości, bez opisu kręgu/zakresu, to pominięcie: płaci w A-R lub R, nie w A6.
- **Sąsiednia jednostka tego samego artykułu** (decyzja Adama 2026-10-22). Powołanie jednostki, która
  zawiera istotę przypisanej treści, gdy brakująca jednostka obok niesie tylko skutek lub doprecyzowanie
  (np. art. 78¹ § 1 k.c. zamiast § 1–2 przy podpisie kwalifikowanym), = nieścisłość bez T. T dopiero wtedy,
  gdy powołana jednostka nie zawiera nic z przypisanej treści (np. „art. 64” pr.aut. z treścią art. 52 ust. 1).
  Jednostka uchylona z jej dawną, prawdziwą treścią (art. 78 § 2 k.c.) = W, nie F.
- **Źródło oficjalne:** każda domena gov.pl (np. parp.gov.pl), zgodnie z definicją wyżej.

## Zakres halucynacji: rdzeń czy poboczne (decyzja Adama 2026-10-18)

A6 zostaje zero-jedynkowe i surowe (jedna zła jednostka gdziekolwiek → 0 i etykieta hallucinated). Każda
karta z A6 = 0 dostaje dodatkowo pole **`A6_zakres`**:

- **rdzeń** — błędne twierdzenie dotyczy sedna pytania: służy głównej konkluzji odpowiedzi, dotyczy
  `podstawy_wymagane` albo elementu `rubryka` klucza;
- **poboczne** — błąd w uwadze ubocznej, analogii, tle albo dygresji, przy poprawnej głównej konkluzji
  i jej podstawach.

Gdy w odpowiedzi są błędy obu rodzajów — **rdzeń**. Zestawienie podaje trzy liczby: halucynacje ogółem,
halucynacje w rdzeniu, halucynacje tylko poboczne. Wzory: rdzeń — `P05_sonnet_cli_w1_r3` (reguła 14 dni),
poboczne — `P12_argon4_high_vertex_w1_r3` (PESEL z art. 783 § 1), `P07_sonnet_cli_w1_r3` (pogląd SA
przypisany SN przy trafnym rdzeniu).

Doprecyzowanie (decyzje Adama 2026-10-25, przy uzupełnianiu pola w kartach pilotażu). Pole mówi o **miejscu**
błędu, nie o jego skutku dla punktów:

1. **Błąd w treści elementu rubryki = rdzeń, także gdy element zaliczono.** Przykład: element „wspomina
   o opłacie od wniosku” zaliczony, ale kwota z dawnego brzmienia art. 25b u.k.s.c. (`P07_codex_terra56_web_r3`).
   Zakres nie zależy od punktacji bloku B.
2. **Zniekształcony identyfikator (S) przy zgodnej tezie = poboczne**, także gdy orzeczenie wspiera główną
   konkluzję — chyba że orzeczenie jest w `podstawy_wymagane` klucza (wtedy rdzeń). Przykład:
   `P13_gemini38flash_vertex_w1_r3` (VIII Cz 83/16 zamiast VIII Gz 43/16). Reguła nie obejmuje klasy T:
   orzeczenie z przypisaną błędną tezą, która służy głównej konkluzji, to rdzeń (`P13_chatgpt_codex_web_r3`).

## Soft law w kluczach (decyzja Adama 2026-10-18)

Wytyczne Komisji, kodeksy praktyk, opinie organów i podobne dokumenty niewiążące (**soft law**) wchodzą
do klucza jako **osobny element rubryki** („odwołuje się do … z zaznaczeniem, że to soft law”), **nigdy jako
kara**. Brak odwołania nie jest błędem — odpowiedź traci tylko ten element. Wnikliwa analiza powinna jednak
do takich dokumentów sięgnąć i uwzględnić ich specyfikę (niewiążący charakter, status: projekt / zatwierdzona
treść / formalnie przyjęte, data). W A6: halucynacją jest przypisanie soft law mocy wiążącej albo treści,
której w nim nie ma; nieścisłość co do daty lub etapu przyjęcia, gdy same źródła publiczne są niezgodne,
halucynacją nie jest. Wzór: `klucze/P08_deepfake_glos_AI_Act.yaml` (v4, R6; wytyczne KE C(2026) 5054).

## Systemy KTZR poza benchmarkiem (decyzja Adama 2026-10-17)

**Benchmarku nie robimy na własnym stacku KTZR** (klaser, czat KTZR, Prawnik SKD i każdy kolejny
produkt kancelarii) — ani w tierze „pytania”, ani w kazusach. Dotychczasowe biegi przeniesione do
`benchmark/_archiwum/ktzr_stack_2026-10-17/` (124 pliki, opis w README archiwum). Nowych biegów
własnych systemów nie dokładamy; skrypt `tools/bench_kazus01_ktzr.py` zostaje tylko jako zapis.

## Status zbioru: kalibracyjny (decyzja Adama 2026-10-11)

Pytania P01–P13 i wszystkie dotychczasowe biegi (pilotaż, r2, r3) służą do **ustalenia
kryteriów oceny**, nie do porównywania systemów. Reguły zmieniano po lekturze odpowiedzi
(trzy zmiany A6 w dniach 9–11.10), próba jest mała i bez przedziałów ufności, a karty
wypełniał sędzia z tej samej rodziny modeli co część ocenianych systemów. Wyników z tego
zbioru nie publikuje się jako rankingu; można je przytaczać jako ilustrację kryteriów.

Plan na wersję 1.1 (z przeglądu literatury o ewaluacji, 2026-10-11):

1. **Definicja konstruktu** — co mierzymy; propozycja: „czy prawnik może użyć odpowiedzi
   w piśmie bez samodzielnego sprawdzenia każdego powołania”.
2. **Miara pomocnicza obok A6** — udział poprawnych powołań w odpowiedzi (z „sprawdzone n z m”);
   etykieta hallucinated zostaje.
3. **Zbiór testowy** — nowe pytania z katalogu, klucze zatwierdzone przed biegiem, ocena
   według zamrożonej wersji bez zmian reguł w trakcie.
4. **Co najmniej trzy biegi na system**, przedziały ufności, porównania parami na tych
   samych pytaniach.
5. **Drugi prawnik na próbce ok. 30 kart** — zgodność człowiek–człowiek jako punkt
   odniesienia dla κ sędziów-modeli.
6. **Weryfikacja powołań jako osobny krok** przez legal-cite przed sędziowaniem; sędziowie
   z co najmniej dwóch rodzin modeli; kolejka rozbieżności do człowieka.
7. Wariant z prośbą o dosłowną treść przepisów — ewentualnie jako osobny test różnicy.
8. **Dwie osobne osie zamiast jednej etykiety z dodatkami** (wnioski Adama 2026-10-12). Oś pierwsza,
   *halucynacja*, odpowiada na pytanie, czy to, co system mówi o prawie, jest prawdziwe (za RegLab:
   nieprawdziwe twierdzenie o prawie): (a) źródło nie istnieje — dziś typ F; (b) źródło istnieje, treść
   trafna, błędne oznaczenie — S; (c) źródło i oznaczenie trafne, treść nieprawdziwa — T, z podtypami
   „treść odwrotna”, „treść cudza”, „zakres rozciągnięty lub zawężony”, „dawne brzmienie” (dzisiejsze W)
   oraz przypadki mieszane. Oś druga, *ugruntowanie*, odpowiada na pytanie, na czym system oparł odpowiedź:
   (1) na niczym poza wagami modelu; (2) na źródle urzędowym; (3) na źródle nieurzędowym, które cytuje
   albo streszcza przepis. Oś druga zastępuje dwa dzisiejsze pola: etykietę „bez weryfikacji źródła”
   i `A6_pochodzenie`. Raport pokazuje tabelę krzyżową obu osi dla każdego systemu. Na kartach z 12.10.2026
   (229): ugruntowanie urzędowe — 9 % odpowiedzi z halucynacją (5 z 53), źródła wtórne — 58 % (22 z 38),
   same wagi — 72 % (100 z 138).
9. **Etykieta wyniku odpowiedzi z dwóch osi** (decyzje Adama 2026-10-12). „Prawidłowa” wymaga obu
   warunków: braku halucynacji (A6 = 1) i pełnego rdzenia (A-R = 2). Ugruntowanie wtórne i brak
   ugruntowania to osobne etykiety. Pięć etykiet:
   - *prawidłowa i ugruntowana* — źródło urzędowe; jedyna, która spełnia konstrukt z pkt 1;
   - *prawidłowa, ugruntowana wtórnie* — serwis, blog albo omówienie zamiast tekstu urzędowego;
   - *prawidłowa, nieugruntowana* — same wagi modelu (odpowiednik „incomplete” w RegLab, ale liczony
     z faktycznego śladu narzędzi, nie z cytowań w tekście);
   - *bez halucynacji, niepełna* — brak fałszywych twierdzeń, ale rdzeń niepełny albo nietrafiony;
   - *halucynacja* — z typem a–c i poziomem ugruntowania zapisanym obok.
   Na kartach z 12.10.2026 (229): 47 prawidłowych i ugruntowanych, 10 ugruntowanych wtórnie,
   27 nieugruntowanych, 18 bez halucynacji niepełnych, 127 z halucynacją. Miara główna zbioru:
   odsetek odpowiedzi prawidłowych i ugruntowanych.

10. **B1 a orzeczenie z cudzą tezą** (do rozważenia, odnotowane przez Adama 2026-10-17; reguły 1.0.1
    nie zmieniono). Dziś B1 ogranicza do 1 tylko błąd w praktycznej wskazówce co do kwoty, terminu,
    organu albo formy. Nie obejmuje powołania orzeczenia z tezą, której w nim nie ma, choć prawnik
    przeniesie je do pisma i naraża się na zarzut przeciwnika albo sądu. Propozycja: dopisać do katalogu
    „orzeczenie albo przepis przytoczony jako argument, który prawnik może przenieść do pisma”. Karta
    wzorcowa: `P13_chatgpt_codex_web_r3` (I CZ 83/09; dziś B1 = 2, jednomyślnie). Wyniki i sondy
    z ręcznego przeglądu 2026-10-17: `oceny/_sedziowie/PRZEGLAD_RECZNY_2026-10-13.md`,
    `../_sondy/P07_haiku_2026-10-17/WYNIK.md`.

Odniesienia metodologiczne: MQM (Freitag i in. 2021), AIS (Rashkin i in.), ALCE (Gao i in. 2023),
FActScore (Min i in. 2023), halucynacje wewnętrzne/zewnętrzne (Maynez i in. 2020), model jako
sędzia (Zheng i in. 2023; Panickssery i in. 2024), statystyka ewaluacji (Miller 2024),
jakość benchmarków (Reuel i in. 2024; Bean i in. 2025), RegLab (Magesh i in. 2025).

## Historia wersji

- **2026-10-18 (noc, w ramach v1.0.1)** — sekcje „Koszt (metryka pomocnicza)” i „Reguły z przeglądu kart rozszerzenia” (B9–B12, nr 19, B1 bez podwójnej kary, A8, historia zmian przepisu, gov.pl); wariant etykiety „tak (narzędzia nieużyte)”. Archiwum poprzedniej wersji: `benchmark/_archiwum/README_przed_koszt_B9-B12_2026-10-18.md`.

- **1.0.1 (2026-10-11)** — sekcja „Przykłady graniczne”; A-R: rdzeń może paść w dowolnym miejscu
  odpowiedzi (P12); trafienie w jedną gałąź pytania warunkowego = 1 (P06). Przeliczone karty P06 i P12.

- **1.0 (2026-10-11)** — stan po decyzjach Adama z 9–11.10.2026: A6 zero-jedynkowe z typami F/T/W/S
  i polem `A6_pochodzenie`, klasa O zniesiona; etykiety hallucinated i „bez weryfikacji źródła”;
  A8 0/½/1 z regułami o ramach produktu, progu miejsca i stopce weryfikatora; B2 według
  `kalibracja_oczekiwana` z regułą dopytania; B1 maks. 1 przy błędzie faktycznym; reguły klucza 1–7;
  skład czystych modeli. Sekcje pisane przed 11.10 czytać łącznie z sekcją „A6 po decyzji z 2026-10-11”.
