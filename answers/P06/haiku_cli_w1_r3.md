---
pytanie: P06
system: 'Claude claude-haiku-5-5 przez Claude Code CLI (subskrypcja), czysty model
  — bez MCP i CLAUDE.md, W1: WebSearch + WebFetch'
model_alias: claude-haiku-5-5
model_id: claude-haiku-5-5
prompt_systemowy: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po
  polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne. Możesz korzystać
  z wyszukiwania w internecie; jeśli z niego korzystasz, na końcu podaj adresy źródeł.
narzedzia:
- WebSearch
- WebFetch
wyszukiwanie: true
temperatura: domyślna CLI (nieustawialna)
kontekst_dodatkowy: sekcja środowiska Claude Code (katalog tymczasowy, data, platforma,
  e-mail konta) — nie da się wyłączyć
data_odpowiedzi: '2026-10-17'
czas_s: 38.3
tokeny:
  input_tokens: 4
  cache_creation_input_tokens: 6493
  cache_read_input_tokens: 3669
  output_tokens: 5900
  output_tokens_details:
    thinking_tokens: 4174
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 6493
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 3962
    cache_read_input_tokens: 2232
    cache_creation_input_tokens: 5698
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 5698
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.029943489999999996
blad: null
---

**Krótka odpowiedź:** co do zasady **nie**. Od postanowienia sądu apelacyjnego odrzucającego zażalenie z powodu nieuiszczenia opłaty nie przysługuje zażalenie do Sądu Najwyższego. Jest jednak kilka innych środków, które warto rozważyć.

**1. Zażalenie do SN (art. 394¹ k.p.c.)**
Przepis ten przewiduje zażalenie do SN na postanowienie sądu drugiej instancji odrzucające skargę kasacyjną oraz na postanowienie odrzucające skargę o stwierdzenie niezgodności z prawem prawomocnego orzeczenia. Katalog jest zamknięty i nie obejmuje odrzucenia zażalenia z powodu braku opłaty. Orzecznictwo SN (np. sygn. V CZ 48/16) przyjmuje, że zażalenie na postanowienie o odrzuceniu zażalenia jest niedopuszczalne.

**2. Wniosek o kontrolę z art. 380 k.p.c.**
W sprawie V CZ 48/16 SN wskazał, że zażalenie na takie postanowienie może zostać potraktowane jako wniosek o kontrolę postanowienia w trybie art. 380 k.p.c. Ta droga jest jednak wąska i jej przesłanki (zwłaszcza odnoszące się do postanowień niezaskarżalnych) trzeba sprawdzić w aktualnym tekście i orzecznictwie. Nie podaję tu terminu, bo nie udało mi się go zweryfikować.

**3. Skarga konstytucyjna (art. 79 ust. 1 Konstytucji RP)**
Jest to środek najczęściej wykorzystywany w takiej sytuacji, ale wymaga wyczerpania dostępnych środków prawnych, dlatego punkt 2 należy rozważyć przed nią. Termin wynosi 3 miesiące od doręczenia prawomocnego orzeczenia (art. 53 ust. 1 ustawy o TK).

**4. Weryfikacja podstaw odrzucenia**
Warto sprawdzić, czy:
- wezwanie do uiszczenia opłaty zostało prawidłowo doręczone i czy termin w nim wskazany był prawidłowo obliczony,
- opłata w ogóle była należna (podstawa: ustawa o kosztach sądowych w sprawach cywilnych) albo czy nie zachodzi zwolnienie lub przypadek, w którym można złożyć wniosek o zwolnienie z kosztów (art. 102 uksc),
- nie zachodzi nieważność postępowania (art. 379 k.p.c.), jeśli strona została pozbawiona możliwości obrony.

**Zastrzeżenie:** Nie udało mi się zweryfikować pełnego aktualnego brzmienia art. 394¹, art. 380 i przepisów o opłatach. Przed przygotowaniem pisma proszę sprawdzić je w ISAP oraz w aktualnym orzecznictwie SN, zwłaszcza w sprawach o opłatę od zażalenia.

Sources:
- [SN V CZ 48/16](https://www.sn.pl/sites/orzecznictwo/Orzeczenia3/V%20CZ%2048-16.pdf)
- [Zażalenie do Sądu Najwyższego (art. 394[1] k.p.c.) – Standardy Prawa](https://standardyprawa.pl/standardy/22062)
- [art. 394¹ k.p.c. – Lexlege](https://lexlege.pl/kpc/art-394-1/)
- [SN III CZ 468/22](https://www.sn.pl/sites/orzecznictwo/Orzeczenia3/III%20CZ%20468-22.pdf)
- [Zażalenie (art. 394 – 398 k.p.c.) – Standardy Prawa](https://standardyprawa.pl/standardy/10597)
- [Zażalenie na postanowienie o odrzuceniu apelacji – e-prawnik.pl](https://e-prawnik.pl/porady-prawne/czy-odrzucenie-apelacji-mozna-skarzyc-zazaleniem.html)
