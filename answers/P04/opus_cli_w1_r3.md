---
pytanie: P04
system: 'Claude opus przez Claude Code CLI (subskrypcja), czysty model — bez MCP i
  CLAUDE.md, W1: WebSearch + WebFetch'
model_alias: opus
model_id: claude-haiku-5-5,claude-opus-5-5
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
data_odpowiedzi: '2026-10-18'
czas_s: 55.0
tokeny:
  input_tokens: 6
  cache_creation_input_tokens: 4716
  cache_read_input_tokens: 9061
  output_tokens: 3788
  output_tokens_details:
    thinking_tokens: 1390
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 4716
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 2240
    cache_read_input_tokens: 5364
    cache_creation_input_tokens: 789
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 789
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.1298233
blad: null
---

**Krótko:** nie jest to postanowienie ani orzeczenie sądu, tylko **decyzja administracyjna** MSWiA. Dlatego co do zasady mówi się o jej **ostateczności**, a nie o prawomocności w rozumieniu procedury cywilnej. MSWiA w ogóle nie nadaje decyzji klauzuli. Na wniosek strony wydaje **zaświadczenie**, że decyzja jest ostateczna i prawomocna.

## 1. Charakter aktu
Zgodnie z art. 1 ust. 1 ustawy z 24 marca 1920 r. o nabywaniu nieruchomości przez cudzoziemców (t.j. Dz.U. z 2017 r. poz. 2278 ze zm.) zezwolenie na nabycie nieruchomości wydaje w drodze **decyzji administracyjnej** minister właściwy do spraw wewnętrznych. Postępowanie toczy się według k.p.a., więc pojęcie „klauzuli prawomocności” z art. 363 i 364 k.p.c. tu nie ma zastosowania.

## 2. Ostateczność (art. 16 § 1 k.p.a.)
- Decyzję wydaje minister, więc nie przysługuje od niej odwołanie. Strona może złożyć **wniosek o ponowne rozpatrzenie sprawy** w terminie 14 dni (art. 127 § 3 w zw. z art. 129 § 2 k.p.a.).
- Decyzja staje się ostateczna:
  - po bezskutecznym upływie 14 dni od doręczenia,
  - wcześniej, jeśli strona zrzeknie się prawa do złożenia wniosku. Decyzja jest ostateczna z dniem doręczenia organowi oświadczenia o zrzeczeniu (art. 127a w zw. z art. 127 § 3 k.p.a.). Przy kilku stronach zrzec się muszą wszystkie.
- Wniosek o ponowne rozpatrzenie nie jest obowiązkowy. Stronie od razu przysługuje skarga do WSA (art. 52 § 3 p.p.s.a.).

## 3. Prawomocność (art. 16 § 3 k.p.a.)
Po nowelizacji k.p.a. z 2017 r. decyzja administracyjna może być też **prawomocna**: jest nią decyzja, od której nie przysługuje skarga do sądu administracyjnego. Dotyczy to sytuacji, gdy upłynie 30-dniowy termin na skargę do WSA (art. 53 § 1 p.p.s.a.) albo gdy zakończy się kontrola sądowa. Dlatego MSWiA w swoich formułach pisze, że decyzja jest „ostateczna i prawomocna”.

## 4. Praktyka MSWiA i u notariusza
- MSWiA wprost informuje, że **nie wydaje odpisu decyzji opatrzonego klauzulą**. Na wniosek strony potwierdza, że decyzja jest ostateczna i prawomocna, wydając **zaświadczenie administracyjne** (art. 217 k.p.a.). Opłata skarbowa wynosi 17 zł, a do wniosku trzeba dołączyć oryginał potwierdzenia wpłaty.
- Do aktu notarialnego przedstawia się zwykle decyzję razem z tym zaświadczeniem. Warto wcześniej zapytać notariusza, czy wystarczy mu potwierdzenie ostateczności, czy oczekuje także potwierdzenia prawomocności. W tym drugim przypadku trzeba odczekać termin na skargę albo uzyskać zrzeczenie się prawa do wniosku i nie wnieść skargi.
- Według źródeł z praktyki zezwolenie jest ważne przez **2 lata**. Przed aktem warto sprawdzić w treści decyzji i ustawy, od kiedy biegnie ten termin.
- Umowa zawarta bez wymaganego zezwolenia jest **nieważna** (art. 6 ust. 1 ustawy).

## 5. Uwaga dotycząca obywatela Ukrainy
Specustawa ukraińska (ustawa z 12 marca 2022 r.) nie wprowadziła ogólnego zwolnienia z obowiązku uzyskania zezwolenia. Warto jednak sprawdzić, czy zezwolenie jest w ogóle potrzebne. Art. 8 ustawy przewiduje wyłączenia, m.in. dla:
- nabycia samodzielnego lokalu mieszkalnego (poza strefą nadgraniczną),
- cudzoziemca zamieszkałego w Polsce co najmniej 5 lat od udzielenia mu zezwolenia na pobyt stały lub rezydenta długoterminowego UE.

**Źródła:**
- [MSWiA – Najczęściej zadawane pytania (gov.pl)](https://www.gov.pl/web/mswia/najczesciej-zadawane-pytania)
- [Zasady nabywania nieruchomości przez cudzoziemców (e-prawnik.pl)](https://e-prawnik.pl/artykuly/zasady-nabywania-nieruchomosci-przez-cudzoziemcow.html)
- [Zezwolenie na zakup nieruchomości przez cudzoziemca w Polsce (totalmoney.pl)](https://www.totalmoney.pl/artykuly/zezwolenie-na-zakup-nieruchomosci-przez-cudzoziemca-w-polsce)
- [Nabycie nieruchomości przez cudzoziemca – ważne informacje (poradnikprzedsiebiorcy.pl)](https://poradnikprzedsiebiorcy.pl/-nabycie-nieruchomosci-przez-cudzoziemca-wazne-informacje)
