---
pytanie: P13
system: Claude opus przez Claude Code CLI (subskrypcja), czysty model — bez narzędzi,
  MCP i CLAUDE.md, W0
model_alias: opus
model_id: claude-haiku-5-5,claude-opus-5-5
prompt_systemowy: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po
  polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne.
narzedzia: []
wyszukiwanie: false
temperatura: domyślna CLI (nieustawialna)
kontekst_dodatkowy: sekcja środowiska Claude Code (katalog tymczasowy, data, platforma,
  e-mail konta) — nie da się wyłączyć
data_odpowiedzi: '2026-10-10'
czas_s: 42.9
tokeny:
  input_tokens: 2
  cache_creation_input_tokens: 859
  cache_read_input_tokens: 0
  output_tokens: 4302
  output_tokens_details:
    thinking_tokens: 2524
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 859
    ephemeral_5m_input_tokens: 0
  inference_geo: not_available
  iterations:
  - input_tokens: 2
    output_tokens: 4302
    cache_read_input_tokens: 0
    cache_creation_input_tokens: 859
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 859
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.09323150000000001
blad: null
---

# Wstrzymanie wykonania nakazu zapłaty z weksla a zabezpieczenie

**Nie.** Wstrzymanie wykonania nakazu zapłaty na podstawie art. 492 § 3 k.p.c. nie odbiera nakazowi charakteru tytułu zabezpieczenia. Powód może nadal, na podstawie tego nakazu, wszcząć postępowanie zabezpieczające.

## Uzasadnienie

**1. Nakaz ma dwie funkcje, uregulowane osobno w art. 492 k.p.c.**
- **§ 1:** nakaz zapłaty od chwili wydania jest **tytułem zabezpieczenia**, wykonalnym bez klauzuli wykonalności. Ten skutek przysługuje każdemu nakazowi w postępowaniu nakazowym.
- **§ 2:** nakaz wydany na podstawie weksla (czeku, warrantu, rewersu) staje się **natychmiast wykonalny** po upływie terminu do zaspokojenia roszczenia. Po nadaniu klauzuli wykonalności jest więc tytułem wykonawczym i pozwala prowadzić egzekucję zmierzającą do zaspokojenia.

**2. Zakres wstrzymania z art. 492 § 3 k.p.c.**
Przepis pozwala sądowi, na wniosek pozwanego zgłoszony w zarzutach, wstrzymać wykonanie „nakazu zapłaty, o którym mowa w § 2”. Wstrzymanie dotyczy więc wyłącznie **natychmiastowej wykonalności** nakazu wekslowego, czyli egzekucji zmierzającej do zaspokojenia. Funkcji tytułu zabezpieczenia z § 1 nie obejmuje. W praktyce nakaz wekslowy wraca wtedy do pozycji „zwykłego” nakazu z postępowania nakazowego, który i tak jest tytułem zabezpieczenia.

**3. Wykładnia celowościowa i stanowisko doktryny**
Wstrzymanie wykonania ma chronić pozwanego przed nieodwracalnym zaspokojeniem wierzyciela przed rozpoznaniem zarzutów. Zabezpieczenie nie prowadzi do zaspokojenia, a jedynie utrwala stan majątkowy dłużnika. Taki jest pogląd dominujący w komentarzach do art. 492 k.p.c. i w praktyce sądowej.

## Konsekwencje praktyczne

- **Dla powoda (wierzyciela):** może złożyć wniosek do komornika o wykonanie zabezpieczenia na podstawie nakazu, bez klauzuli. Komornik stosuje sposoby zabezpieczenia właściwe dla tytułu zabezpieczenia z art. 492 § 1 k.p.c. (art. 747 pkt 1–2 k.p.c. odpowiednio), np. zajęcie ruchomości, wynagrodzenia, rachunku bankowego czy innych wierzytelności. Możliwy jest także wpis hipoteki przymusowej na podstawie tytułu zabezpieczenia (art. 110 ustawy o księgach wieczystych i hipotece). Zajęte środki nie są wydawane wierzycielowi, lecz pozostają zablokowane.
- **Dla pozwanego (dłużnika):** sam wniosek o wstrzymanie wykonania nie chroni przed zabezpieczeniem. Pozwany może:
  - wnosić o **uchylenie lub ograniczenie zabezpieczenia** (z odpowiednim zastosowaniem art. 742 k.p.c.; należy zweryfikować aktualne orzecznictwo co do dopuszczalności tej drogi wobec zabezpieczenia z mocy samego nakazu);
  - złożyć kwotę do depozytu sądowego lub wskazać inny, mniej uciążliwy sposób zabezpieczenia;
  - pamiętać, że uchylenie nakazu i oddalenie powództwa w wyniku zarzutów prowadzi do **upadku zabezpieczenia** (art. 744 k.p.c.). Pozwany może wtedy dochodzić naprawienia szkody (art. 746 k.p.c.).

## Zastrzeżenie

Przed użyciem tej analizy w piśmie procesowym proszę sprawdzić aktualne brzmienie art. 492, 492¹, 742–747 k.p.c. w wersji obowiązującej na dzień czynności, uwzględniając nowelizacje od 2019 r. Warto też sprawdzić bieżące orzecznictwo SN i sądów apelacyjnych w LEX/Legalis. Nie podaję sygnatur z pamięci, żeby nie wprowadzić Pana w błąd.

Mogę przygotować projekt wniosku do komornika o wykonanie zabezpieczenia albo projekt wniosku pozwanego o ograniczenie zabezpieczenia, zależnie od tego, kogo Pan reprezentuje.
