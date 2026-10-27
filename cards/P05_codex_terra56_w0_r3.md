# Karta oceny — P05 · OpenAI gpt-5.6-terra przez Codex CLI (rozumowanie: medium), W0 bez wyszukiwania — r3

- Pytanie: P05 (katalog nr 38), klucz w wersji 2 (2026-10-10)
- Data odpowiedzi systemu: 2026-10-10 · czas 34.2 s · warunki: model gpt-5.6-terra, wysiłek rozumowania medium, Codex CLI (sandbox read-only, pusty katalog, sesja nietrwała), aplikacje ChatGPT wyłączone (features.apps=false); narzędzia: brak, wyszukiwanie: brak (W0), liczba wyszukań 0; wstęp: „Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne. Odpowiedz bezpośrednio w wiadomości — nie twórz plików i nie uruchamiaj poleceń.”; tokeny: wejście 9502 (z pamięci podręcznej 6912), wyjście 1003, rozumowanie 516
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 0/2 | 0: rdzeń odwrotny do klucza — pierwszy akapit: „osoba fizyczna występująca we własnym imieniu nie jest obowiązana odbierać pism sądowych przez Portal Informacyjny”, dalej „Doręczenia przez Portal Informacyjny dotyczą przede wszystkim profesjonalnych pełnomocników”; o wyborze doręczeń portalowych przez stronę (art. 131¹ᵃ § 1 od 1.06.2026) nic — pułapka aktualności zadziałała |
| A2 | 0/1 | 0: art. 131¹ᵃ § 1 powołany w brzmieniu sprzed 1.06.2026 (tylko pełnomocnicy), brak § 1¹ i § 2 art. 131¹ᵃ (moment doręczenia podany z art. 131¹ § 2) |
| A3 | n/d | system nie cytuje dosłownie |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 0/1 | [2026-10-11 A6 binarne: ½→0, A6_typ: [W], A6_pochodzenie: art. 131¹ᵃ § 1 k.p.c.: pamięć — W podtrzymane (krąg adresatów z § 1 w brzmieniu do 31.05.2026 podany jako obowiązujący), wg reguły binarnej to 0; bieg W0 bez narzędzi] **A6_zakres: rdzeń** [2026-10-25 uzupełnione, do przeglądu Adama: W w art. 131¹ᵃ § 1 k.p.c. (krąg adresatów sprzed 1.06.2026) dotyczy podstawy wymaganej i głównej konkluzji o doręczeniu osobie fizycznej] · A6_typ: [W]. Sprawdzone 3 z 3 (ISAP DU/2026/468): (1) **art. 131¹ᵃ § 1 — W**: „Doręczenia przez Portal Informacyjny dotyczą przede wszystkim profesjonalnych pełnomocników (adwokatów, radców prawnych, rzeczników patentowych oraz Prokuratorii Generalnej RP) … Podstawa: art. 131¹a § 1 k.p.c.” — krąg adresatów odpowiada realnemu brzmieniu § 1 obowiązującemu do 31.05.2026 (odnośnik 28 t.j.); od 1.06.2026 § 1 obejmuje „także stronę, która dokonała wyboru takiego sposobu doręczania” oraz komornika i stałego mediatora (odnośnik 29) → dawna wersja podana jako obecna; dopisek „jeżeli sąd dysponuje odpowiednimi warunkami technicznymi” nie ma odpowiednika w żadnej z dwóch wersji (w ustawie: „w razie niemożności doręczenia za pośrednictwem systemu teleinformatycznego”) — bez osobnej klasy, do decyzji Adama; (2) art. 131¹ § 1 ✓ („jeżeli adresat wniósł pismo za pośrednictwem systemu teleinformatycznego albo dokonał wyboru wnoszenia pism”); (3) art. 131¹ § 2 ✓ (chwila z elektronicznego potwierdzenia odbioru; brak potwierdzenia — 14 dni od umieszczenia pisma w systemie; system pisze „wskazaną przez system jako zapoznanie się” — nieścisłość bez klasy). Orzeczeń nie powołano (SAOS: 0 sprawdzeń). Najgorszy przypadek: W → ½ |
| A8 | 1/1 | każdy akapit dotyczy doręczeń elektronicznych osobie fizycznej (portal, system teleinformatyczny z art. 131¹ — ścieżka dopuszczona w kluczu, skutek dla terminów); bez dygresji |
| R1 | 0/1 | osoba fizyczna może otrzymywać doręczenia przez portal, jeżeli wybierze ten sposób — ✗ (wybór opisany tylko dla systemu teleinformatycznego z art. 131¹; portal „służy przede wszystkim dostępowi do informacji i akt”) |
| R2 | 0/1 | sposób złożenia oświadczenia o wyborze (przez portal, jeden z trzech podpisów) — ✗ (brak) |
| R3 | 0/1 | moment doręczenia, w tym reguła 14 dni — ✗: moment i 14 dni podane dla doręczenia przez system teleinformatyczny („art. 131¹ § 2 k.p.c.”, „od umieszczenia pisma w systemie”), nie dla portalu. Do decyzji Adama: karty P05_codex_astra6_w0_r3 i P05_chatgpt_codex_w0_r3 dostały 1, ale tam reguła dotyczyła portalu (w części o pełnomocniku); mechanizm jest ten sam, przy łagodnym czytaniu 1 |
| R4 | 0/1 | możliwość rezygnacji — ✗ (brak) |
| K1 | −1 | twierdzi, że osobie fizycznej bez pełnomocnika nie można doręczać przez portal — „Doręczenia przez Portal Informacyjny dotyczą przede wszystkim profesjonalnych pełnomocników”, „Portal Informacyjny służy przede wszystkim dostępowi do informacji i akt, a nie automatycznie elektronicznej komunikacji procesowej z każdą stroną”, „Samo założenie konta i wgląd do akt w portalu nie oznacza jeszcze skutecznego doręczenia”. Do decyzji Adama: sformułowania są miękkie („przede wszystkim”, „co do zasady”), a zdanie końcowe o stronie „niekorzystającej formalnie z elektronicznego trybu” jest samo w sobie prawdziwe; karę naliczono jak w kartach Astra i ChatGPT-Codex W0 r3, bo drogi wyboru portalu przez stronę odpowiedź nie zna |
| K2 | 0 | stosuje art. 139 k.p.c. (awizo) do doręczenia portalowego — nie dotyczy |
| **A** | **0 / 9 = 0.0 %** | punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d); suma 1½ − K 1 = ½ [2026-10-11: było ½ / 9 = 5.6 %, Δ −27.7; A6 ½→0] |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 0/2 | 0: na pytanie „jak wygląda doręczenie przez portal” prawnik dostaje odpowiedź, że portal jest dla pełnomocników; nie dowie się o oświadczeniu o wyborze, podpisach ani rezygnacji, a przy stronie, która portal wybrała, nie ma kroku kontrolnego (sprawdzenie oświadczenia, dokumentu potwierdzającego doręczenie) i grozi przeoczenie biegu terminu |
| B2 kalibracja | 1/1 | 1 (`kalibracja_oczekiwana: kategoryczna`): teza postawiona wprost w pierwszym zdaniu i w podsumowaniu („W konsekwencji: …”); „co do zasady” jej nie rozmywa; nieaktualny stan prawny płaci w bloku A |
| **B** | **1 / 3 = 33.3 %** | |

**Δ = A % − B % = −33.3** · hallucinated: tak (A6_typ W; 2026-10-11 A6 binarne, było: nie; A6_zakres: rdzeń [2026-10-25 uzupełnione]) · bez weryfikacji źródła: tak (brak narzędzi)

## Pochodzenie (opisowe)

P1 ślady narzędzi: brak (W0: bez narzędzi i bez wyszukiwania) · P2 nie badano · P3 źródła deklarowane w tekście: k.p.c. (art. 131¹ᵃ § 1, art. 131¹ § 1 i § 2), bez linków · P4 wiedza z wag modelu; art. 131¹ᵃ § 1 w stanie sprzed 1.06.2026. Warunki biegu z nagłówka odpowiedzi: model gpt-5.6-terra, wysiłek rozumowania medium, Codex CLI, sandbox read-only (pusty katalog, sesja nietrwała), aplikacje ChatGPT wyłączone, liczba_wyszukan 0, inne_narzedzia 0, zdarzenia [], blad null; wstęp jak w metryce karty

Specyfikacja oceny: v1.0 (2026-10-11) — karta oceniona lub przeliczona według README w tej wersji.
