# Meta-sędzia — projekt (2026-10-19, do akceptacji Adama)

Cel: kolejne ogniwo oceny (nie zastępuje Adama). Daje wstępną kartę i listę spraw do decyzji człowieka.

## Symulacja na istniejących ocenach (bez nowych wywołań)

Etykieta hallucinated, zgodność z kartami Adama (r3, karty z kompletem 4 sędziów):

| Układ | P05–P13 (n 96) κ | P01–P10 (n 79) κ | nadmiar / brak (nowe) |
|---|---|---|---|
| Argon sam | 0.98 | 0.92 | 0 / 3 |
| Sol sam | 0.89 | 0.82 | 6 / 1 |
| Pro sam | 0.74 | 0.77 | 0 / 9 |
| Flash sam | 0.79 | 0.55 | 1 / 17 |
| Argon lub Pro („dowolny”) | 0.89 | **0.95** | 0 / 2 |
| Argon lub Flash | 0.96 | 0.90 | 1 / 3 |
| większość Argon + Sol + Pro | 0.96 | 0.92 | 0 / 3 |

Zastrzeżenia:
- P05–P13: rozbieżności były rozstrzygane przez Adama po obejrzeniu argumentów sędziów → zgodność zawyżona.
  Czystym testem są P01–P10 (karty zamknięte przed biegiem sędziów, z wyjątkiem 7 spraw Sola z 19.10).
- Wybór układu na podstawie tych samych danych = dopasowanie. Reguła ma być zamrożona przed kolejnym zbiorem.
- **Argon przeoczył 2 z 4 halucynacji we własnych odpowiedziach** (Argon W0 P08 „jedynie” w art. 50 ust. 2;
  Argon W1 P09 dwa wyroki SN nie na temat), które Pro i Sol wykryły — sygnał preferencji rodziny (B3).
  Pozostałe przeoczenia: Flash W0 P04 (art. 127a), Haiku W1 P10.

Wniosek: sam panel modeli daje mało (Argon ≈ panel). Pozostałe błędy to treść przepisu, wersja,
historia zmian, orzeczenie „nie na temat” — wymagają sprawdzenia w źródle, nie kolejnego głosu.

## Proponowana architektura

1. **Krok faktów (kod, bez LLM).** Z odpowiedzi wyciągnąć powołania (przepisy, sygnatury, daty, Dz.U.).
   Przepisy → legal-cite (tekst w wersji na datę stanu prawnego + wersje wcześniejsze dla W).
   Orzeczenia → SAOS, a gdy brak — baza LexAlpha (odczyt). Wynik: raport faktów
   {powołanie, istnieje, fragment urzędowy, wersja/publikator, data, „nie znaleziono”}.
2. **Panel 2 sędziów z różnych rodzin:** Argon (high) + Sol, oba dostają odpowiedź, klucz, README i raport faktów.
   Sędzia nie ocenia odpowiedzi swojej rodziny bez drugiego głosu (Argon/Flash → decyduje Sol; GPT → decyduje Argon).
3. **Agregacja per kryterium:** A6 = 0, gdy którykolwiek sędzia wskaże błąd **potwierdzony w raporcie faktów**;
   błąd bez potwierdzenia → „do decyzji człowieka”. Punkty liczbowe: zgodne → przyjęte; różne → niższa wartość
   + flaga. Etykiety F/T/W/S z raportu faktów, nie z modelu.
4. **Wyjście:** karta wstępna + lista „do decyzji Adama” (tylko rozbieżności i niepotwierdzone zarzuty).

## Walidacja

- Zamrozić reguły agregacji na P05–P13 + P01–P10 (dzisiejszy stan), test na **nowym zbiorze pytań**
  (np. kolejne 5 pytań z katalogu) — dopiero to jest uczciwa miara.
- Miary: κ dla hallucinated i A-R względem Adama, liczba spraw do decyzji człowieka (cel: < 25 % kart),
  koszt na kartę, czas.

## Koszt (szacunek do sprawdzenia)

Krok faktów: ~0 (kod, API publiczne). Dwa sędziowie na kartę: Argon high ~0.05–0.15 USD (Vertex),
Sol — subskrypcja (limit konta ChatGPT jest wąskim gardłem; alternatywa: Pro na Vertex).

## Etap A–C (2026-10-24, plan zatwierdzony przez Adama) — co zmieniono w kodzie

**A. Wejście (`fakty.py`, bez strojenia promptów).**
- A1 indeks literowy: `131¹ᵃ`, `131¹a`, `$131^{1a}$ § $1^1$`, `394^1a`, `<sup>1a</sup>` → legal-cite `art. 131[1a] § 1[1] KPC`.
- A2 akt domniemany z klucza tylko, gdy zdanie nie nazywa innego aktu (a przy zdaniu bez aktu — także akapit) i gdy
  jednostka istnieje w akcie domniemanym; inaczej status „akt nieustalony — do sprawdzenia ręcznie” (flaga
  `akt_nieustalony`, nie zarzut). Nazwy opisowe („ustawy o nabywaniu nieruchomości…”, „rozporządzenia 2016/679”,
  RODO, ustawy nowelizujące/covidowe) rozpoznawane.
- A3 sygnatura w kilku sądach: wybór po sądzie/mieście i dacie z odpowiedzi; bez nich i przy > 1 sądzie — status
  „sygnatura niejednoznaczna (N wyroków: …)” bez oceny poparcia i bez flagi błędu. W `poparcie.py` rekordy LexAlpha
  filtrowane po sądzie wybranym w kroku faktów.
- A4 SAOS: 3 próby z odstępem; awaria (HTTP ≠ 200, JSON, timeout) → flaga `saos_niedostepny` (informacja), tekst
  z LexAlpha; brak wyroku przy działającym SAOS → `nie_znaleziono`. Pamięć SAOS w `poparcie.py` zapisuje tylko
  odpowiedzi serwera (dawne `{"id": null}` z czasu awarii są ignorowane).
- A5 role powołań: `główne` / `w_zwiazku` / `zakres` (+ `powolanie_glowne_id`); twierdzenie i ocena poparcia tylko
  dla głównego, brzmienia członów dołączają do źródła.
- Dodatkowo: baza LexAlpha w `fakty.py` wyłącznie przez bramkę `tools/lexalpha_ro.query` (wcześniej psycopg
  bezpośrednio); jednostka „nie istnieje” dziś, ale obecna w na_dzien(data stanu) → istnieje; obecna tylko w wersjach
  wcześniejszych → flaga `uchylony` (kandydat W, nie F — README „jednostka uchylona … = W”).

**B. Ramy (`poparcie.py`).** Wyjście per powołanie: `klasa_A6` ∈ {✓, F, T, W, S} albo `status_weryfikacji`
(brak_dowodu, tekst_niedostepny, akt_nieustalony, sygnatura_niejednoznaczna, nie_znaleziono, nieobslugiwany,
w_zwiazku, brak_twierdzenia, niepewne) + `A6_zakres` (rdzeń: podstawy_wymagane / orzeczenie z klucza / zbieżność
z rubryką; inaczej poboczne) + `uzasadnienie_etykieta` (dawna etykieta). Mapowanie (stała `KLASA_Z_ETYKIETY`):
F = jednostka nie istnieje przy akcie wprost (krok faktów); W = uchylona/usunięta na datę, cytat zgodny z wersją
wcześniejszą (krok faktów) albo `popiera_wersja_wczesniejsza` sędziego (rdzeń tylko w brzmieniu wcześniejszym,
cytat verbatim w tym brzmieniu); S = orzeczenie pod inną datą/sądem przy treści popartej; T = `nie_na_temat`,
`przeczy`, `tylko_zreferowane` (wskazana jednostka z cudzą treścią, inny adresat, rozciągnięty zakres);
✓ = `popiera_wprost`, `popiera_czesciowo` (w tym sąsiednia jednostka z istotą treści), `poza_brzmieniem`.
Orzeczenie nieznalezione = status, nie F (README reguła 1). Prompt sędziego = stały prefiks z dosłownymi
fragmentami README (sekcje „A6 po decyzji…” + „A6 — typ błędu”, „Przykłady graniczne”, „Reguły z przeglądu kart” +
„Zakres halucynacji”, wycinane po nagłówkach) w cache kontekstu Vertex + część zmienna. Kotwice verbatim bez zmian.

**C. Karta meta (`karta_meta.py`).** Prompt = INSTR z `eval_sedzia_codex.py` + te same wycinki README + klucz +
odpowiedź + sekcja „RAPORT FAKTÓW” (klasy, brzmienia, wersje, orzeczenia z kotwicami, statusy; instrukcja: A6/A6_typ/A3
z raportu, reszta jak zwykle, status ≠ błąd). Sędziowie argon4meta (gemini-4-argon high, Vertex, wyszukiwanie)
i sol61meta (gpt-6.1-sol, Codex). Pliki `_sedziowie/<P>_<system>.{argon4meta,sol61meta}.json` + `raport_faktow_uzyty`.
Pomiar: `ewaluacja_8pytan.py` (sekcja klas A6), `zgodnosc_meta.py` (κ bez raportu vs z raportem).

**D. Bieg 2026-10-24 (wynik: `raporty/_meta_8pytan_2026-10-24.md`).** Zmiany techniczne w trakcie biegu: (1) `gemini-4-argon`
nie obsługuje jawnego cache kontekstu Vertex, a niejawny praktycznie nie trafia (85 tys. z 2,2 mln tokenów) → sędzia poparcia
ocenia PAKIET ≤ 10 powołań jednej odpowiedzi w jednym wywołaniu (`PAKIET_MAX`, `judge_batch`; każde powołanie wobec własnego
źródła, kotwice sprawdzane per powołanie; brakująca ocena → dopytanie pojedyncze); (2) A2b: akt domyślny z klucza tylko,
gdy `podstawy_wymagane` nazywają jeden akt (P04: u.n.n.c. + k.p.a. → brak aktu domyślnego, status `akt_nieustalony`),
bez rezerwowego domysłu z odpowiedzi; statusy przeliczone post hoc `przemapuj_poparcie.py` (13 wpisów P04, 0 USD).
Koszt biegu: poparcie 7,87 USD, karta meta Argon (64 karty) 6,57 USD, testy 0,26 USD — razem 14,70 USD; Sol 61 kart do limitu konta.
Wynik w skrócie: FA na ✓ 12 % → 1,8 %, czułość T 47 → 59 %, ogólna 57 → 59 %; karta meta z raportem wiążącym obniża κ
hallucinated (Argon 0,96 → 0,85, Sol 0,88 → 0,83) — raport zdejmuje nadmiar, ale blokuje własne wykrycia sędziego.

## E. Decyzje Adama 2026-10-24 (nr 2, 3, 4, 6) — co zmieniono w kodzie (bieg kontrolny „c”)

**Nr 2 — krąg adresatów / zakres normy (`poparcie.py`, `karta_meta.py`, `fakty.py`).** Reguła README „Zawężony lub rozszerzony
krąg adresatów / zakres normy” trafia do promptu weryfikatora i do instrukcji karty meta v2 DOSŁOWNIE, wycinana programowo
(`poparcie.readme_regula`: od „- **Tytuł**” do następnego punktu listy; start przerywany, gdy README jej nie ma albo wyciąg
sekcji `readme_fragmenty` jej nie obejmuje). W prompcie sędziego nowy krok „KRĄG ADRESATÓW / ZAKRES NORMY”: wyliczenie
w twierdzeniu porównywane z brzmieniem na datę i z każdym atomem „brzmienie WCZEŚNIEJSZE” (z `wersje_na_dzien` kroku faktów):
zgodne z datą → ✓; zgodne tylko z wcześniejszym → `popiera_wersja_wczesniejsza` (W) mimo zmiękczeń; z żadnym → `nie_na_temat`
(T); samo niewspomnienie → `popiera_czesciowo`. Sędzia zwraca pole `krag_zakres` (true, gdy ocena z takiego porównania);
przy `krag_zakres` W zostaje, nawet gdy cytat z wersji wcześniejszej występuje też w brzmieniu na datę (dawny krąg bywa
podzbiorem nowego — flaga `krag_zakres_cytat_wspolny_z_brzmieniem_na_date`). Krok faktów: wcześniejsze brzmienia co
6/12/24/60/120/180 miesięcy (`MIESIACE_WSTECZ`) zamiast 2/5/10/15 lat — zmiana sprzed kilku miesięcy (art. 131¹ᵃ § 1 k.p.c.,
1.06.2026) wypadała między „dziś” a „−2 lata”. Karta meta: raport pokazuje najnowsze wcześniejsze brzmienie (fragment).

**Nr 3 — u.n.n.c. (`legal-cite (https://github.com/apiotrowski-afk/legal-cite-pl)`, gałąź `feat/unnc`; `fakty.py`).** `PL_ACTS`: `UNNC`, `u.n.n.c.`, „ustawy
o nabywaniu nieruchomości przez cudzoziemców” → DU/1920/178 (akt pierwotny, jak pozostałe wpisy; t.j. DU/2017/2278 HTML,
nowela DU/2026/1099 w życie 19.11.2026 — raportowana jako oczekująca). Poprawka `_cut_ustep`: nagłówek „Art. 1.” nie jest
ustępem 1 (bez niej „art. 1 ust. 1 UNNC” oddawał samo „1.”). Test `testy/unnc.py`. `fakty.py` mapuje „u.n.n.c.”, „ustawy
o nabywaniu…”, „ustawy z 1920 r.”, „ustawy z dnia 24 marca 1920 r.” na `UNNC`; `fakty.py` importuje legal-cite z
`legal-cite (https://github.com/apiotrowski-afk/legal-cite-pl)` (sys.path przed site-packages — bez zmian). Klucz P04 pozostaje wieloaktowy (u.n.n.c. + k.p.a.), więc
bare „art. 8” nadal = `akt_nieustalony` (A2b).

**Nr 4 — klasa S na orzeczeniach (`fakty.py`, `poparcie.py`).** Status „sygnatura niejednoznaczna (N wyroków)” liczy ODRĘBNE
wyroki (sąd, data; ten sam wyrok w SAOS i LexAlpha raz) i zapisuje `kandydaci_odrebni` z `id`. Reguła: N ≤ 4 → weryfikator
ocenia twierdzenie wobec KAŻDEGO kandydata osobno (atomy z kotwicami jak dotąd, po jednej jednostce pakietu na kandydata);
trafienie = `popiera_wprost`/`popiera_czesciowo` z cytatem zweryfikowanym (pierwszeństwo `popiera_wprost`). Trafiony kandydat
inny niż oznaczenie modelu (sąd/miasto lub data) → **S** ze wskazaniem właściwego wyroku (`kandydat_trafiony`); żaden → **T**;
model bez sądu i daty → ✓ (brak błędu oznaczenia; do przeglądu); N > 4, brak tekstów kandydatów albo brak twierdzenia →
status bez oceny. Sąd rozpoznawany także tuż po sygnaturze („VIII Gz 43/16, SO Szczecin”) i w skrócie bez „w” („SA Gdańsk”).

**Nr 6 — plik kanoniczny.** `ewaluacja_8pytan.py` bez `--poparcie` czyta `_poparcie_8pytan_2026-10-24b.json`
(`POPARCIE_KANONICZNE_2026_10_24`); oryginał `_poparcie_8pytan_2026-10-24.json` zachowany. Liczby biegu 24.10: FA poparcia na ✓
przed A2b 21 / 665 (3,2 %), po A2b 12 / 665 (1,8 %) — przemapowanie 13 wpisów P04 bez ponownego sędziego.

Pliki biegu „c”: raporty faktów nadpisane (poprzednie w `raporty/_archiwum_2026-10-24_przed_c/`), `_poparcie_8pytan_2026-10-24c.json/.md`,
`_ewaluacja_8pytan_2026-10-24c.md`. Karty meta NIE uruchamiane (osobna decyzja).

**Wynik biegu „c” (2026-10-24, 7,09 USD):** czułość „ta sama klasa” 66 → 74 / 147 (45 → 50 %), „dowolna” 87 → 94 (59 → 64 %); W 17 → 24,
S 0 → 2 (P13 codex_terra56_web, zgodne z kartą), T 49 → 48, F 0 → 0 (bez zmian: legal-cite znajduje jednostkę pod sąsiednim numerem);
FA na ✓ 12 → 12 (T 11 → 10, W 1 → 2), spoza kart 19 → 16; nieobsługiwany 22 → 9 (14 powołań u.n.n.c.: 13 ✓, 1 T), sygnatura
niejednoznaczna 5 → 2, akt_nieustalony 38 → 37. Reguła nr 2: 52 powołania z `krag_zakres`, 9 zmian klasy (+5 trafnych W, 1 nowy FA W,
1 strata W → T). Szczegóły: `raporty/_ewaluacja_8pytan_2026-10-24c.md`. Uwaga: kopia zapasowa raportów faktów pominęła P07 — odtworzone
starym `fakty.py` (`_archiwum_2026-10-24_przed_c/_UWAGA.md`).

## Nazwy w artykule v1.2 (2026-10-25)
W artykule („Correctly grounded”, §9) używamy nazw: **verification layer** = cała warstwa przed sędzią;
**citation check** = krok faktów (`fakty.py`, sam kod); **support check** = weryfikator poparcia (`poparcie.py`);
**verification report** = raport faktów podawany sędziemu (`karta_meta.py`, sekcja „RAPORT FAKTÓW”);
**verification status** = status weryfikacji (nigdy błąd modelu). Nazwy robocze w kodzie i dzienniku zostają.
Od 2026-10-25 sędziowie przez Codex zapisują zapytania i źródła (`codex_log_wyszukan.py`), nie tylko liczbę wyszukań;
karty `sol61meta3` sprzed tej zmiany (44 z 128) mają tylko liczbę.
