---
pytanie: P12
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
data_odpowiedzi: '2026-10-17'
czas_s: 72.3
tokeny:
  input_tokens: 4
  cache_creation_input_tokens: 4888
  cache_read_input_tokens: 3795
  output_tokens: 5825
  output_tokens_details:
    thinking_tokens: 3361
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 4888
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 3605
    cache_read_input_tokens: 2358
    cache_creation_input_tokens: 3967
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 3967
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.16941669999999998
blad: null
---

**Krótko:** tak, możesz złożyć zwykły wniosek o klauzulę z art. 787 k.p.c., choć nakaz zapłaty nie wspomina o działalności gospodarczej. Nie dostaniesz jednak klauzuli „bez ograniczeń”. Klauzula przeciwko małżonkowi, który nie jest dłużnikiem osobistym, zawsze ogranicza jego odpowiedzialność do jakiejś części majątku. Różnica polega tylko na tym, czy jest to cały majątek wspólny (art. 787), czy tylko przedsiębiorstwo (art. 787¹).

Zakładam, że chodzi o art. **787¹** k.p.c. (klauzula na małżonka przedsiębiorcy), a nie o art. 781¹.

## 1. Dwie drogi do wyboru

| | **Art. 787 k.p.c. („tryb normalny”)** | **Art. 787¹ k.p.c.** |
|---|---|---|
| Zakres odpowiedzialności małżonka | cały majątek wspólny | tylko przedsiębiorstwo wchodzące w skład majątku wspólnego |
| Co musisz wykazać | dokumentem urzędowym lub prywatnym, że wierzytelność powstała z czynności prawnej dokonanej **za zgodą małżonka** dłużnika (art. 41 § 1 k.r.o.) | dokumentem urzędowym lub prywatnym, że wierzytelność powstała **w związku z prowadzeniem przedsiębiorstwa** (art. 41 § 2 k.r.o.) |
| Majątek osobisty małżonka | wyłączony | wyłączony |

Wybór drogi należy do wierzyciela. Art. 787¹ nie wyłącza art. 787 tylko dlatego, że dług ma związek z działalnością. Jeśli masz dokument potwierdzający zgodę małżonka, możesz od razu żądać klauzuli z art. 787. Taka klauzula obejmuje cały majątek wspólny, a nie tylko przedsiębiorstwo.

## 2. To, czego brakuje w nakazie zapłaty, nie przesądza sprawy

- Sąd w postępowaniu klauzulowym bada tytuł egzekucyjny w sposób formalny, ale przesłanki z art. 787 i 787¹ ustala na podstawie **dokumentów dołączonych do wniosku**, a nie samej treści tytułu.
- Tytuł wydany przeciwko osobie fizycznej oznaczonej PESEL-em jest prawidłowym tytułem przeciwko dłużnikowi. Dopisek „prowadzący działalność gospodarczą pod firmą…” jest tylko dodatkowym opisem.
- Nawet przy art. 787¹ tytuł nie musi wspominać o działalności. Związek z przedsiębiorstwem wykazujesz dokumentami, na przykład:
  - umową lub fakturami wystawionymi na firmę z NIP,
  - wydrukiem z CEIDG,
  - korespondencją handlową,
  - odpisem pozwu i załączników.

## 3. Wniosek z art. 787: praktyka

- Potrzebny jest **dokument potwierdzający zgodę małżonka**: jego podpis na umowie, odrębne oświadczenie o zgodzie, poręczenie, wekslowe „za zgodą małżonka”, ewentualnie korespondencja, z której zgoda jasno wynika. Sama okoliczność, że dług ma związek z firmą, **nie wystarczy**.
- Sąd musi też mieć dowód **istnienia małżeństwa** (odpis aktu małżeństwa) oraz wspólności ustawowej w chwili powstania zobowiązania.
- Jeśli nie masz dokumentu o zgodzie, art. 787 odpada. Zostaje art. 787¹, ale tylko wtedy, gdy przedsiębiorstwo wchodzi w skład majątku wspólnego.
- Warto rozważyć **żądanie ewentualne**: głównie klauzula z art. 787, a ewentualnie z art. 787¹. Sąd rozpozna wtedy oba żądania w jednym postępowaniu.

## 4. Na co uważać

- Małżonek, który dostał klauzulę, nie staje się dłużnikiem osobistym. Jest **dłużnikiem egzekwowanym** w granicach ograniczenia wpisanego w klauzuli (wyrok SN z 6.12.2012 r., III CSK 43/12). Może się bronić zażaleniem na klauzulę oraz środkami z prawa egzekucyjnego. Komornik nie może prowadzić egzekucji z jego majątku osobistego.
- Do egzekucji z wynagrodzenia za pracę dłużnika, jego dochodów z innej działalności zarobkowej i jego majątku osobistego **klauzula przeciwko małżonkowi nie jest potrzebna** (art. 41 § 2 k.r.o.).
- Zgoda z art. 41 § 1 k.r.o. powinna dotyczyć **czynności prawnej, z której powstał dług**. Późniejsza wiedza małżonka o długu czy tolerowanie go zwykle nie wystarczą.

Brzmienie art. 787¹ podaję za komentarzami dostępnymi w sieci. Przed złożeniem wniosku warto je porównać z aktualnym tekstem ustawy w ISAP.

**Źródła:**
- [Postępowanie klauzulowe (art. 781 – art. 787[2] k.p.c.) – standardyprawa.pl](https://standardyprawa.pl/standardy/3569)
- [Małżeńskie prawo egzekucyjne – standardyprawa.pl](https://standardyprawa.pl/standardy/25199)
- [Odpowiedzialność małżonka za długi (art. 30 i 41 k.r.o.) – standardyprawa.pl](https://standardyprawa.pl/standardy/9309)
- [Małżeńskie stosunki majątkowe – standardyprawa.pl](https://standardyprawa.pl/standardy/9593)
- [Odpowiedzialność za długi małżonka-przedsiębiorcy – poradnikprzedsiebiorcy.pl](https://poradnikprzedsiebiorcy.pl/-odpowiedzialnosc-za-dlugi-malzonka-przedsiebiorcy)
- [Egzekucja z majątku wspólnego – pro.rp.pl](https://pro.rp.pl/prawo-w-firmie/art15412571-egzekucja-z-majatku-wspolnego)
