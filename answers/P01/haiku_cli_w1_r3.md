---
pytanie: P01
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
data_odpowiedzi: '2026-10-18'
czas_s: 43.3
tokeny:
  input_tokens: 6
  cache_creation_input_tokens: 9514
  cache_read_input_tokens: 9229
  output_tokens: 4028
  output_tokens_details:
    thinking_tokens: 2430
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 9514
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 1761
    cache_read_input_tokens: 6979
    cache_creation_input_tokens: 2535
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 2535
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.04152939
blad: null
---

**Odpowiedź krótko:** próg wartości rzeczy dla wykroczenia kradzieży (art. 119 § 1 k.w.) wynosi obecnie **800 zł**. Nie zmienił się w 2026 r. i nie zależy od wysokości płacy minimalnej.

**Podstawa i zmiany:**
- Art. 119 § 1 k.w. stanowi, że kradzież lub przywłaszczenie cudzej rzeczy ruchomej o wartości nieprzekraczającej 800 zł jest wykroczeniem, zagrożonym aresztem, ograniczeniem wolności albo grzywną.
- Próg wzrósł z 500 zł do 800 zł na podstawie ustawy z 7 lipca 2022 r. o zmianie ustawy – Kodeks karny (art. 4 pkt 5). Obowiązuje od 1 października 2023 r.
- Wcześniej (do 2018 r.) próg był powiązany z ¼ najniższego wynagrodzenia. Nowelizacja z 2018 r. przeszła na kwotę stałą, dlatego od tej pory podwyżki płacy minimalnej nie zmieniają progu. Co do daty tej zmiany źródła są niespójne, więc przed wykorzystaniem warto ją zweryfikować w tekście ustawy.

**Wyjątki:** kradzież szczególnie zuchwała lub z włamaniem jest przestępstwem niezależnie od wartości. Nie stosuje się też progu, gdy przedmiotem jest broń lub materiały wybuchowe, albo gdy sprawca stosuje gwałt.

**Powyżej 800 zł** czyn kwalifikuje się jako kradzież z art. 278 § 1 k.k. Wartość ustala się według wartości rynkowej w chwili czynu, a nie ceny na metce.

**Kara:** maksymalna grzywna za wykroczenie wynosi 5000 zł (art. 24 § 2 k.w.), a areszt do 30 dni.

Przed wykorzystaniem w piśmie procesowym sprawdź aktualny tekst ustawy w Dzienniku Ustaw, bo źródła w sieci nie zawsze są aktualne.

Sources:
- [Art. 119 k.w. – Lexlege](https://www.lexlege.pl/kw/art-119/)
- [Art. 119. Kradzież lub przywłaszczenie rzeczy – Standardy Prawa](https://standardyprawa.pl/akt/3/art/652)
- [Kradzież przestępstwo czy wykroczenie – Infor](https://www.infor.pl/prawo/wykroczenia/odpowiedzialnosc-za-wykroczenia/5667992,kradziez-przestepstwo-czy-wykroczenie.html)
- [Próg kwotowy między wykroczeniem a przestępstwem – Infor](https://www.infor.pl/prawo/nowosci-prawne/5751898,prog-kwotowy-miedzy-wykroczeniem-a-przestepstwem.html)
- [Kradzież jako przestępstwo – jednak nie od 400 zł, nowy próg jest wyższy – Bezprawnik](https://bezprawnik.pl/kradziez-jako-przestepstwo-jednak-nie-od-400-zl-nowy-prog-jest-wyzszy)
- [Wyrok SN V KK 137/24](https://www.sn.pl/sites/orzecznictwo/Orzeczenia3/V%20KK%20137-24.pdf)
