---
pytanie: P08
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
czas_s: 67.7
tokeny:
  input_tokens: 6
  cache_creation_input_tokens: 4523
  cache_read_input_tokens: 8513
  output_tokens: 4141
  output_tokens_details:
    thinking_tokens: 958
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 4523
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 2990
    cache_read_input_tokens: 4813
    cache_creation_input_tokens: 1147
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 1147
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.13557039999999998
blad: null
---

**Odpowiedź krótka:** co do zasady tak. Takie nagranie nie spełnia definicji deepfake'a z art. 3 pkt 60 AI Act. Trzeba jednak pamiętać o trzech zastrzeżeniach, a brak statusu deepfake'a nie zwalnia z innych obowiązków przejrzystości z art. 50.

## 1. Definicja deepfake'a (art. 3 pkt 60 rozporządzenia 2024/1689)

Deepfake to wygenerowane lub zmanipulowane przez AI obrazy, treści audio lub wideo, które:
- (a) **przypominają istniejące osoby, przedmioty, miejsca, podmioty lub zdarzenia**, oraz
- (b) **mogłyby niesłusznie zostać uznane przez odbiorcę za autentyczne lub prawdziwe**.

Oba warunki muszą być spełnione łącznie. Jeśli głos AI nie naśladuje żadnej konkretnej osoby i nie stwarza fałszywego wrażenia autentyczności (np. wyraźnie syntetyczny lektor lub głos postaci w grze), to nie jest deepfake. Nie stosuje się wtedy obowiązku ujawnienia z **art. 50 ust. 4** (obowiązek podmiotu stosującego, czyli deployera).

## 2. Zastrzeżenia

**a) Liczy się odbiór, a nie intencja.** Przesłanka „mogłyby niesłusznie zostać uznane za autentyczne” ma charakter obiektywny. Ocenia się, jak treść może odebrać odbiorca, a nie czy twórca chciał kogoś zwieść. Sformułowanie „niczego nie udaje” jest więc bezpieczne tylko wtedy, gdy wynika to z samej treści i kontekstu jej użycia, a nie tylko z zamiaru twórcy.

**b) Wytyczne Komisji czytają definicję szerzej.** Według dostępnych omówień wytyczne Komisji dotyczące przejrzystości (art. 50), przyjęte 20 lipca 2026 r., obejmują pojęciem deepfake'a także treści przedstawiające coś, co „mogłoby istnieć”. Chodzi o realistyczny, wiarygodny scenariusz, nawet jeśli dana osoba lub zdarzenie nigdy nie istniały. Realistyczny głos „nieistniejącej osoby”, przedstawiony np. jako wypowiedź prawdziwego eksperta, klienta czy świadka, może więc zostać uznany za deepfake. Z drugiej strony wytyczne podkreślają znaczenie kontekstu i oczekiwań odbiorców: jeśli odbiorca nie oczekuje, że treść jest autentyczna, to nie jest ona deepfake'iem. Wytyczne nie są wiążące, ale organy nadzoru rynku i Urząd ds. AI będą się nimi zapewne kierować. Zastrzegam, że nie zweryfikowałem tekstu wytycznych bezpośrednio u źródła, tylko na podstawie opracowań kancelaryjnych.

**c) Art. 50 ust. 4 zd. 3.** Przy treściach w oczywisty sposób artystycznych, twórczych, satyrycznych lub fikcyjnych obowiązek ujawnienia jest ograniczony, ale nie znika całkowicie. To jednak dotyczy treści, które już są deepfake'ami.

## 3. Obowiązki niezależne od tego, czy treść jest deepfake'iem

- **Art. 50 ust. 2:** dostawca systemu AI generującego syntetyczny dźwięk musi zapewnić, że wyniki są oznakowane w formacie nadającym się do odczytu maszynowego i wykrywalne jako wygenerowane przez AI. Dotyczy to **każdego** syntetycznego audio, nie tylko deepfake'ów. Wyjątki obejmują m.in. funkcję wspomagającą standardową edycję oraz brak istotnej zmiany danych wejściowych. Według dostępnych źródeł, po zmianach w ramach Digital Omnibus systemy wprowadzone do obrotu przed 2 sierpnia 2026 r. mają czas na wdrożenie znakowania do **2 grudnia 2026 r.** Pozostałe obowiązki z art. 50 stosuje się od 2 sierpnia 2026 r. (art. 113).
- **Art. 50 ust. 1:** jeśli głos AI służy do bezpośredniej interakcji z ludźmi (np. voicebot, asystent głosowy), dostawca musi zaprojektować system tak, by użytkownik wiedział, że rozmawia z AI. Wyjątkiem jest sytuacja, gdy jest to oczywiste.
- Poza AI Act w grę mogą wchodzić m.in. ochrona dóbr osobistych (art. 23–24 k.c.), RODO (głos jako dana osobowa, a w pewnych zastosowaniach dana biometryczna) oraz przepisy o nieuczciwych praktykach rynkowych.

## Wniosek

Teza jest prawdziwa, jeśli głos nie przypomina istniejącej osoby (ani, według wytycznych, realistycznie „możliwej” osoby lub zdarzenia) i w danym kontekście nie mógłby zostać uznany za autentyczny. Oceniamy to obiektywnie, z perspektywy odbiorcy. Nawet wtedy dostawca musi znakować wynik zgodnie z art. 50 ust. 2, a przy interakcji z człowiekiem stosuje się też art. 50 ust. 1. Przed opinią dla klienta warto sprawdzić aktualne brzmienie wytycznych Komisji i rozporządzenia Digital Omnibus w Dzienniku Urzędowym UE. Źródła różnią się co do dat i numeru tego aktu.

**Źródła:**
- [Mayer Brown – EU AI Act News: Digital Omnibus, Transparency Guidelines](https://www.mayerbrown.com/en/insights/publications/2026/07/eu-ai-act-news-digital-omnibus-on-ai-new-guidance-on-risk-classification-gpai-and-transparency-obligations)
- [artificialintelligenceact.eu – Practical Guide to Article 50](https://artificialintelligenceact.eu/transparency-rules-article-50/)
- [Gibson Dunn – EU AI Act Omnibus Agreement](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)
- [CSA – Article 50 Watermarking Grace Period Ends December 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article50-watermarking-deadline/)
- [CSA – Article 50 Transparency Obligations Take Effect](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article-50-transparency-20260729/)
- [Travers Smith – EU AI Act transparency rules take effect 2 August 2026](https://www.traverssmith.com/knowledge/knowledge-container/is-it-a-bot-eu-ai-act-transparency-rules-take-effect-2-august-2026/)
- [Usercentrics – Digital Omnibus Now in Force](https://usercentrics.com/knowledge-hub/eu-ai-act-high-risk-delay-article-50-transparency-consent/)
- [Technology.org – AI Act Deadlines After the Digital Omnibus](https://www.technology.org/2026/10/13/eu-ai-act-deadlines-after-the-digital-omnibus-what-applies-from-december-2026-to-august-2028/)
- [Hello Growth – Digital Omnibus AI Act: what changes in 2026](https://hellogrowth.ai/en/blog/eu-ai-act-2026-omnibus-labelling-ai-content)
