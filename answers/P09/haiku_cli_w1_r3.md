---
pytanie: P09
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
czas_s: 38.1
tokeny:
  input_tokens: 2
  cache_creation_input_tokens: 852
  cache_read_input_tokens: 1437
  output_tokens: 8194
  output_tokens_details:
    thinking_tokens: 6699
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 852
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 8194
    cache_read_input_tokens: 1437
    cache_creation_input_tokens: 852
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 852
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.00457827
blad: null
---

Tak, w zasadzie tak. Ogólny zapis „na wszelkie pola eksploatacji” zwykle nie wystarcza, choć nie zawsze prowadzi do pełnej nieskuteczności całej klauzuli.

**Podstawa: art. 41 ust. 1 ustawy o prawie autorskim i prawach pokrewnych**
Przeniesienie autorskich praw majątkowych obejmuje tylko pola eksploatacji wymienione w umowie. Pola muszą być więc wskazane, a nie tylko zbiorczo określone. Sformułowanie „wszelkie pola” nic nie wymienia, więc sąd może uznać, że nie objęło żadnego konkretnego pola albo objęło tylko te, które da się z umowy i jej celu wywieść.

**Dodatkowe reguły, które działają na niekorzyść takiego zapisu:**
- **Forma pisemna pod rygorem nieważności** (art. 53 PAut). Dotyczy samego przeniesienia, więc zapis ustny lub dorozumiany nie wystarczy.
- **Pola nieznane w chwili zawarcia umowy** nie mogą być objęte przeniesieniem (art. 41 ust. 4 PAut). W social mediach to ważne, bo nowe formaty i platformy pojawiają się szybko, a „wszelkie znane pola” nie obejmie ich skutecznie.
- **Wykładnia na korzyść twórcy** (art. 65 PAut). W razie wątpliwości postanowienia umowy interpretuje się w sposób korzystniejszy dla twórcy, czyli wąsko.
- **Terytorium i czas.** Jeśli umowa ich nie określa, stosuje się domyślne ograniczenia z art. 43–44 PAut. Warto to sprawdzić w aktualnym tekście ustawy.

**Specyfika umowy zlecenia**
Zlecenie (art. 734 KC) nie przenosi praw autorskich z mocy prawa. Zleceniodawca nie staje się automatycznie właścicielem praw do materiałów. Może co najwyżej korzystać z utworu w zakresie wynikającym z celu umowy, na podstawie dorozumianej licencji. Ten zakres bywa sporny, a w przypadku social mediów często obejmuje tylko publikację na wskazanych kontach, a nie dalsze wykorzystanie, przeróbki czy udostępnianie w kampaniach płatnych.

Pracownicze reguły z art. 12 PAut nie mają tu zastosowania, bo dotyczą pracowników, a nie zleceniobiorców.

**Co zrobić w umowie (praktyka)**
1. Wymienić pola wprost: utrwalanie i zwielokrotnianie, wprowadzanie do obrotu, publiczne udostępnianie w internecie i w mediach społecznościowych, korzystanie z opracowań (kadrowanie, montaż, przeróbki), ewentualnie sublicencjonowanie.
2. Określić terytorium (np. cały świat) i czas (np. bezterminowo albo na X lat).
3. Zachować formę pisemną pod rygorem nieważności.
4. Osobno uregulować prawa osobiste (np. oznaczenie autorstwa, art. 16 PAut). Są niezbywalne, więc można jedynie zobowiązać się do niewykonywania ich w określonym zakresie.
5. Rozważyć wynagrodzenie i ewentualnie klauzulę dostosowania, zwłaszcza w kontekście dyrektywy 2019/790 (art. 20–22). Status implementacji w Polsce warto zweryfikować, bo przepisy się zmieniały.

**Zastrzeżenie:** odpowiadam z wiedzy ogólnej, bez sprawdzania aktualnego tekstu ustawy ani orzecznictwa. Numery przepisów (zwłaszcza art. 41 ust. 4, 43–44, 65) i stan implementacji dyrektywy przed podpisaniem umowy warto potwierdzić w Dz.U. lub systemie prawniczym. Jeśli chcesz, mogę poszukać aktualnego orzecznictwa SN dotyczącego klauzul „na wszelkie pola”.
