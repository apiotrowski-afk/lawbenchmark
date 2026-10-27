---
pytanie: P07
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
czas_s: 49.7
tokeny:
  input_tokens: 6
  cache_creation_input_tokens: 7928
  cache_read_input_tokens: 10588
  output_tokens: 6193
  output_tokens_details:
    thinking_tokens: 4041
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 7928
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 3349
    cache_read_input_tokens: 6870
    cache_creation_input_tokens: 2495
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 2495
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.03354918
blad: null
---

**Krótka odpowiedź:** tak, co do zasady wniosek o pisemne uzasadnienie można złożyć po ogłoszeniu zasadniczych powodów rozstrzygnięcia. Nie udało mi się jednak zweryfikować brzmienia art. 357 § 5 k.p.c., więc termin i zakres przed złożeniem wniosku trzeba sprawdzić w aktualnym tekście ustawy.

**Co udało się ustalić:**

- **Art. 328 § 1 k.p.c. (wyrok):** pisemne uzasadnienie sporządza się na wniosek strony zgłoszony w terminie **tygodnia od ogłoszenia wyroku**. Gdy wyrok doręcza się z urzędu, termin liczy się od doręczenia (§ 2).
- **Art. 328 § 3 k.p.c.:** we wniosku trzeba wskazać, czy uzasadnienie ma dotyczyć całości wyroku, czy jego części.
- **Art. 328 § 4 k.p.c.:** sąd odrzuca wniosek niedopuszczalny, spóźniony, nieopłacony lub z brakami nieusuniętymi mimo wezwania.
- **Art. 357 § 5 k.p.c.:** w źródłach pojawia się w kontekście „zwięzłego wskazania zasadniczych powodów rozstrzygnięcia" i konieczności wniosku o uzasadnienie. Z tego, co znalazłem, wygląda na to, że dotyczy **postanowień** (art. 357 reguluje uzasadnienie postanowień), a nie wyroków. Nie mam jednak pewności co do brzmienia ani terminu.
- **Art. 130¹ § 2 k.p.c.:** wniosek o uzasadnienie jest wymagany także przy zarzutach dotyczących uchybień w postanowieniu.

**Dlaczego termin jest kluczowy:**

- Przy **wyroku** termin na wniosek wynosi tydzień od ogłoszenia (art. 328 § 1). Jego przekroczenie oznacza odrzucenie wniosku.
- Termin na **apelację** (art. 369 § 1 k.p.c.) biegnie od doręczenia wyroku z uzasadnieniem, więc bez wniosku nie rozpocznie się.
- Przy **postanowieniu** zażalenie przysługuje w terminie tygodnia od doręczenia postanowienia z uzasadnieniem (art. 394 § 2 k.p.c.).

**Zalecenia:**

1. Sprawdź aktualny tekst art. 357 i 328 k.p.c. w ISAP (isap.sejm.gov.pl). Ustal, czy rozstrzygnięcie jest wyrokiem czy postanowieniem, bo od tego zależy właściwy przepis i termin.
2. Złóż wniosek najpóźniej w tygodniu od ogłoszenia, a najlepiej wcześniej, i w treści wskaż zakres uzasadnienia (art. 328 § 3). Przy wątpliwościach co do terminu przyjmij najkrótszy.
3. Zweryfikuj termin z komentarzem do k.p.c. (np. Piotrowski, Marcinkiewicz) lub orzecznictwem.

Źródła:
- [Standardy Prawa – art. 328 k.p.c.](https://standardyprawa.pl/akt/76/art/13109)
- [Standardy Prawa – uzasadnienie postanowienia i jego doręczenie (art. 357 k.p.c.)](https://standardyprawa.pl/standardy/23554)
- [Standardy Prawa – wniosek o uzasadnienie wyroku (art. 328 k.p.c.)](https://standardyprawa.pl/standardy/9307)
- [Standardy Prawa – termin tygodniowy do zażalenia (art. 394 § 2 k.p.c.)](https://standardyprawa.pl/standardy/16800)
- [Rulecalc – art. 328 KPC, termin tygodniowy](https://rulecalc.com/pl/podatki/kpc-uzasadnienie-wyroku-tydzien)
