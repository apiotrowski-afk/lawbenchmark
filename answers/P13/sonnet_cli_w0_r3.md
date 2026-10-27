---
pytanie: P13
system: Claude claude-sonnet-5-5 przez Claude Code CLI (subskrypcja), czysty model
  — bez narzędzi, MCP i CLAUDE.md, W0
model_alias: claude-sonnet-5-5
model_id: claude-haiku-5-5,claude-sonnet-5-5
prompt_systemowy: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po
  polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne.
narzedzia: []
wyszukiwanie: false
temperatura: domyślna CLI (nieustawialna)
kontekst_dodatkowy: sekcja środowiska Claude Code (katalog tymczasowy, data, platforma,
  e-mail konta) — nie da się wyłączyć
data_odpowiedzi: '2026-10-10'
czas_s: 57.3
tokeny:
  input_tokens: 2
  cache_creation_input_tokens: 857
  cache_read_input_tokens: 0
  output_tokens: 8854
  output_tokens_details:
    thinking_tokens: 7557
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 857
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 8854
    cache_read_input_tokens: 0
    cache_creation_input_tokens: 857
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 857
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.09228650000000001
blad: null
---

**Co do zasady tak.** Wstrzymanie wykonania nakazu zapłaty obejmuje również egzekucję zabezpieczającą prowadzoną na podstawie tego nakazu.

**Uzasadnienie**

1. Nieprawomocny nakaz zapłaty w postępowaniu nakazowym nie jest tytułem egzekucyjnym do zaspokojenia, lecz tytułem zabezpieczenia (art. 492 § 1 KPC). Jedyne „wykonanie" nakazu, które w tym stadium wchodzi w grę, to jego wykonanie w trybie zabezpieczenia.
2. Wstrzymanie wykonania nakazu (art. 493 § 4 KPC) dotyczy więc właśnie tego trybu. Wstrzymanie jest ograniczeniem możności wykonywania nakazu jako tytułu zabezpieczenia, a nie dodatkową instytucją obok niego. Gdyby wierzyciel mimo wstrzymania mógł prowadzić egzekucję zabezpieczającą, postanowienie sądu byłoby pozbawione sensu.
3. W praktyce oznacza to, że:
   - wierzyciel nie może skutecznie wszcząć egzekucji zabezpieczającej na podstawie takiego nakazu (komornik nie powinien podejmować czynności, a wniosek podlega zwrotowi lub oddaleniu),
   - jeżeli egzekucja została już wszczęta, podlega wstrzymaniu lub zawieszeniu. Dłużnik może przedstawić komornikowi postanowienie o wstrzymaniu wykonania, a w razie potrzeby wnieść o zawieszenie postępowania (art. 820 i n. KPC w zw. z art. 492 § 1 KPC).

**Zastrzeżenia, które warto sprawdzić w aktach**

- **Zakres wstrzymania.** Sąd może wstrzymać wykonanie w całości lub w części albo uzależnić wstrzymanie od warunków, np. od złożenia kaucji. Trzeba sprawdzić sentencję postanowienia, czy nie ogranicza się tylko do części roszczenia lub czy nie wskazuje wprost zabezpieczenia.
- **Odrębny wniosek o zabezpieczenie.** Wstrzymanie wykonania nakazu nie wyłącza formalnie możliwości złożenia przez powoda wniosku o udzielenie zabezpieczenia na zasadach ogólnych (art. 730 i n. KPC). Powód musi wówczas uprawdopodobnić roszczenie i interes prawny w zabezpieczeniu (art. 730¹ KPC). Sąd weźmie pod uwagę okoliczności, które legły u podstaw wstrzymania, więc uwzględnienie takiego wniosku jest mało prawdopodobne. Pozwany może się mu sprzeciwić, powołując się na te same argumenty.
- **Utrata skuteczności wstrzymania.** Wstrzymanie wygasa lub może zostać uchylone po rozpoznaniu zarzutów, po zmianie okoliczności albo w razie uchylenia postanowienia w zażaleniu. Trzeba to monitorować.

Numerację paragrafów (zwłaszcza art. 492 i 493 KPC po nowelizacjach) proszę zweryfikować w aktualnym tekście ustawy, bo cytuję ją z pamięci. Przy pisemnej opinii warto też sprawdzić najnowsze orzecznictwo sądów apelacyjnych dotyczące relacji art. 493 § 4 KPC do zabezpieczenia z art. 730 i n. KPC.
