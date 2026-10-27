# Karta oceny — P07 · OpenAI gpt-6.1-sol przez Codex CLI (rozumowanie: medium), W0 bez wyszukiwania — powtórzenie r3

- Pytanie: P07 (katalog nr 24), klucz w wersji 2 (2026-10-10)
- Data odpowiedzi systemu: 2026-10-10 · czas 44.0 s · warunki: gpt-6.1-sol, wysiłek rozumowania medium, Codex CLI (sandbox read-only, pusty katalog, sesja nietrwała); wyszukiwarka: brak (W0); liczba wyszukań: 0
- Data stanu prawnego klucza: 2026-10-01
- Oceniający: Claude (wstępnie, do weryfikacji przez A. Piotrowskiego)

## Blok A

| # | Pkt | Dowód |
|---|---|---|
| A-R | 2/2 | 2: pierwszy akapit — „Tak — wskazanie przez sąd zasadniczych powodów rozstrzygnięcia na podstawie art. 357 § 5 k.p.c. nie wyłącza możliwości złożenia wniosku o sporządzenie i doręczenie uzasadnienia postanowienia, jeżeli postanowienie podlega zaskarżeniu”; pełny rdzeń z warunkiem zaskarżalności |
| A2 | 1/1 | 1: art. 357 § 5, art. 357 § 1 („w terminie tygodnia od ogłoszenia”) i § 2¹ („w terminie tygodnia od doręczenia postanowienia”) |
| A3 | n/d | system nie cytuje dosłownie (cudzysłów tylko przy nazwie instytucji i przy formule wniosku) |
| A5 | n/d | pytanie niesporne (`sporne: false`) |
| A6 | 1/1 | A6_typ: — (bez błędów). Sprawdzone 3 z 3 (ISAP DU/2026/468): art. 357 § 1 ✓ (posiedzenie jawne, żądanie w terminie tygodniowym od ogłoszenia, tylko gdy podlega zaskarżeniu); art. 357 § 2¹ ✓ (posiedzenie niejawne, tydzień od doręczenia); art. 357 § 5 ✓ („nawet niepodlegające zaskarżeniu” i zd. 2 o odróżnieniu od uzasadnienia — oddane jako „nie zastępuje formalnego uzasadnienia”). Twierdzenie „samo ich podanie nie tworzy … prawa do żądania uzasadnienia” zgodne z § 1 i § 2¹ (uzasadnienie tylko gdy postanowienie podlega zaskarżeniu) |
| A8 | 1/1 | każdy akapit służy pytaniu; jednozdaniowa formuła wniosku i jednozdaniowe zastrzeżenie o przepisie szczególnym — neutralne (jak w r2) |
| R1 | 1/1 | odpowiada „tak” i wyjaśnia, że zasadnicze powody nie są uzasadnieniem — „zwięzłe wyjaśnienie decyzji sądu, które nie zastępuje formalnego uzasadnienia” |
| R2 | 1/1 | wskazuje warunek: postanowienie musi podlegać zaskarżeniu — „jeżeli postanowienie podlega zaskarżeniu”, „Jeżeli postanowienie jest zaskarżalne, wniosek należy złożyć” |
| R3 | 1/1 | podaje termin tygodniowy i jego początek — „po ogłoszeniu na posiedzeniu jawnym — w terminie tygodnia od ogłoszenia (art. 357 § 1)”, „po wydaniu na posiedzeniu niejawnym — w terminie tygodnia od doręczenia postanowienia (art. 357 § 2¹)” |
| R4 | 0/1 | wspomina o opłacie od wniosku albo o wyjątkach z § 2³–§ 2⁴ lub § 6 — ✗ (brak opłaty z art. 25b u.k.s.c. i brak wyjątków) |
| K1 | 0 | twierdzi, że wskazanie zasadniczych powodów zastępuje uzasadnienie albo zamyka drogę do wniosku — nie dotyczy (przeciwnie: „nie zastępuje wniosku”) |
| K2 | 0 | podaje termin dwóch tygodni — nie dotyczy (wszędzie „tydzień”) |
| **A** | **8 / 9 = 88.9 %** | punkty możliwe: A-R 2 + A2 1 + A6 1 + A8 1 + R 4 = 9 (A3, A5 n/d) |

## Blok B

| # | Pkt | Uzasadnienie |
|---|---|---|
| B1 przydatność | 2/2 | 2: warunek, termin i jego początek w obu wariantach, gotowa formuła wniosku, trafna przestroga „Nie należy więc czekać na dodatkowe wyjaśnienia sądu … nie powoduje rozpoczęcia nowego terminu” |
| B2 kalibracja | 1/1 | 1 (`kalibracja_oczekiwana: kategoryczna`): teza wprost („Tak — …”), pewność adekwatna do jasnego przepisu; zastrzeżenie o przepisie szczególnym nie rozmywa tezy |
| **B** | **3 / 3 = 100.0 %** | |

**Δ = A % − B % = −11.1** · hallucinated: nie · bez weryfikacji źródła: tak (brak narzędzi)

## Pochodzenie (opisowe)

P1 ślady narzędzi: brak (liczba_wyszukan 0, inne_narzedzia 0, zdarzenia []) · P2 nie badano · P3 źródła deklarowane w tekście: k.p.c. (art. 357 § 1, § 2¹, § 5), bez linków · P4 wiedza z wag modelu; brzmienie § 5 zd. 2 oddane trafnie. Względem r2 (2026-10-08): ten sam wynik (A 88.9 %, B 100 %), ta sama luka (R4: opłata, wyjątki)

Specyfikacja oceny: v1.0 (2026-10-11) — karta oceniona lub przeliczona według README w tej wersji.
