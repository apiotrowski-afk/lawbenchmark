---
pytanie: P01
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
czas_s: 34.8
tokeny:
  input_tokens: 4
  cache_creation_input_tokens: 4271
  cache_read_input_tokens: 2253
  output_tokens: 2207
  output_tokens_details:
    thinking_tokens: 753
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 4271
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 1912
    cache_read_input_tokens: 2253
    cache_creation_input_tokens: 2018
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 2018
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.0914218
blad: null
---

Próg w 2026 r. wynosi **800 zł** i nie zmienił się w związku ze wzrostem płacy minimalnej. Od 1 października 2023 r. jest to stała kwota zapisana w ustawie, niezależna od minimalnego wynagrodzenia.

**Jak się zmieniał próg**
- Do 9 listopada 2018 r. granicą była **1/4 minimalnego wynagrodzenia**, więc kwota rosła co roku.
- Od 9 listopada 2018 r. była to stała kwota **500 zł**.
- Od 1 października 2023 r. jest to **800 zł**. Wprowadziła to nowelizacja z 7 lipca 2022 r. (Dz.U. 2022 poz. 2600). Miała wejść w życie 14 marca 2023 r., ale termin przesunięto.

Wzrost płacy minimalnej w 2026 r. nie ma więc wpływu na ten próg. Do jego zmiany potrzebna jest nowelizacja ustawy. Nie znalazłem żadnego projektu, który by go zmieniał w 2026 r., ale przed opinią warto to sprawdzić w RCL i na stronach Sejmu.

**Gdzie obowiązuje próg 800 zł** (Kodeks wykroczeń, t.j. Dz.U. 2025 poz. 734):
- art. 119 § 1: kradzież lub przywłaszczenie cudzej rzeczy ruchomej,
- art. 120 § 1: kradzież lub wyrąb drzewa z lasu,
- art. 122 § 1: paserstwo,
- art. 124 § 1: niszczenie lub uszkadzanie cudzej rzeczy.

Powyżej tej kwoty czyn jest przestępstwem, np. z art. 278, 284, 288 lub 291–292 Kodeksu karnego.

**Wyjątki**
- Przy kradzieży z włamaniem (art. 279 k.k.) i kradzieży szczególnie zuchwałej (art. 278a k.k.) liczy się przestępstwo bez względu na wartość. Dotyczy to też kradzieży broni, amunicji i materiałów wybuchowych.
- Czyn ciągły: jeśli łączna wartość mienia przekracza 800 zł, czyny popełnione w ramach czynu ciągłego są przestępstwem (art. 12 § 2 k.k. w zw. z art. 10a k.w.). Brzmienie tych przepisów warto sprawdzić w aktualnym tekście jednolitym.

Źródła:
- [Lexlege – art. 119 Kodeksu wykroczeń](https://www.lexlege.pl/kw/art-119/)
- [Lexlege – Kodeks wykroczeń, rozdział XIV](https://lexlege.pl/kw/rozdzial-xiv-wykroczenia-przeciwko-mieniu/453)
- [Infor – Próg kwotowy między wykroczeniem a przestępstwem](https://www.infor.pl/prawo/nowosci-prawne/5751898,prog-kwotowy-miedzy-wykroczeniem-a-przestepstwem.html)
- [Infor – Kradzież: przestępstwo czy wykroczenie](https://www.infor.pl/prawo/wykroczenia/odpowiedzialnosc-za-wykroczenia/5667992,kradziez-przestepstwo-czy-wykroczenie.html)
- [Interia – Podniesienie do 800 zł granicy wykroczenia](https://biznes.interia.pl/finanse/news-podniesienie-do-800-zl-granicy-wykroczenia-za-kradziez-to-za,nId,6441782)
- [Rulecalc – art. 278 KK / art. 119 KW](https://rulecalc.com/pl/sady/kradziez-kwota)
