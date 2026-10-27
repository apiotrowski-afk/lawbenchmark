---
pytanie: P13
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
czas_s: 91.0
tokeny:
  input_tokens: 6
  cache_creation_input_tokens: 5344
  cache_read_input_tokens: 9215
  output_tokens: 5235
  output_tokens_details:
    thinking_tokens: 2373
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 5344
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 3673
    cache_read_input_tokens: 5513
    cache_creation_input_tokens: 1268
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 1268
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.16406919999999997
blad: null
---

**Nie. Wstrzymanie wykonania nakazu zapłaty z weksla nie odbiera mu charakteru tytułu zabezpieczenia.** Wierzyciel nadal może na jego podstawie złożyć do komornika wniosek o wykonanie zabezpieczenia, bez klauzuli wykonalności.

**Podstawy i argumentacja**

1. **Dwa odrębne skutki nakazu (art. 492 k.p.c.):**
   - **§ 1:** nakaz zapłaty jest tytułem zabezpieczenia od chwili wydania i można go wykonać bez nadawania klauzuli wykonalności. Dotyczy to każdego nakazu w postępowaniu nakazowym.
   - **§ 3:** nakaz wydany na podstawie weksla (a także warrantu, rewersu lub czeku) staje się natychmiast wykonalny po upływie terminu do zaspokojenia roszczenia. To skutek dodatkowy, który dotyczy egzekucji. Sąd może wstrzymać wykonanie nakazu na wniosek pozwanego.

   Wstrzymanie z § 3 zdanie drugie dotyczy tylko tego dodatkowego skutku, czyli wykonania nakazu jako tytułu egzekucyjnego. Skutek z § 1 pozostaje nietknięty. W praktyce sytuacja wierzyciela wraca do tej, jaką ma przy zwykłym nakazie zapłaty, np. z faktur: może się zabezpieczyć, ale nie może egzekwować.

2. **Orzecznictwo.** Sąd Okręgowy w Szczecinie (postanowienie z 2 marca 2016 r., VIII Gz 43/16) wskazał, że wstrzymanie wykonania nakazu zapłaty wydanego np. na podstawie weksla „nie pozbawia takiego nakazu zapłaty cech tytułu zabezpieczającego”. Sąd uzasadnił to tak:
   - tytuł zabezpieczenia „nie podlega wykonaniu w sposób porównywalny z wykonaniem tytułu wykonawczego”;
   - wstrzymanie wykonania tytułu wykonawczego prowadzi do zawieszenia egzekucji (art. 820 k.p.c.). Zajęcie jednak zostaje w mocy nawet po zawieszeniu (art. 821 k.p.c.), a zabezpieczenie roszczenia pieniężnego polega właśnie na zajęciu. Nie ma więc czego „wstrzymywać”.

   Ten sam pogląd przyjmuje D. Zawistowski w komentarzu do art. 492 k.p.c. w „Postępowanie zabezpieczające. Komentarz. Wybór orzeczeń” (2007).

   Sąd dopuścił jeden wyjątek: wstrzymanie mogłoby mieć znaczenie przy szczególnych tytułach zabezpieczenia, które wykonuje się tak jak tytuły wykonawcze (art. 753, 753¹, 754 k.p.c.). Przy roszczeniu z weksla to nie występuje.

**Wnioski praktyczne dla wierzyciela**
- Wniosek do komornika składa się o **wykonanie zabezpieczenia**, a nie o wszczęcie egzekucji. Dołącza się nakaz zapłaty bez klauzuli (art. 492 § 1 w zw. z art. 743 § 1 k.p.c.).
- Dostępne są sposoby zabezpieczenia roszczeń pieniężnych z art. 747 k.p.c., m.in.:
  - zajęcie rachunku bankowego, wierzytelności, wynagrodzenia lub ruchomości;
  - hipoteka przymusowa (art. 747 pkt 2 k.p.c., art. 109 ust. 2 ustawy o księgach wieczystych i hipotece);
  - zakaz zbywania nieruchomości bez księgi wieczystej.
- Jeśli egzekucja była już wszczęta, po wstrzymaniu wykonania nakazu ulega zawieszeniu (art. 820 k.p.c.). Dokonane zajęcia co do zasady pozostają w mocy (art. 821 § 1 k.p.c.). Sąd może je jednak uchylić, jeśli dłużnik złoży odpowiednie zabezpieczenie (art. 821 § 2 k.p.c.).
- Warto przeczytać sentencję i uzasadnienie postanowienia o wstrzymaniu. Ustawa nie przewiduje „wstrzymania nakazu jako tytułu zabezpieczenia”, ale gdyby sąd ujął to szerzej, trzeba ocenić, czy zaskarżyć postanowienie. Zażalenie na postanowienie w przedmiocie wstrzymania wykonania przysługuje: uchwała SN z 24 września 2003 r., III CZP 58/03. Po nowelizacji z 2019 r. warto sprawdzić, czy przysługuje zażalenie poziome, czy do sądu II instancji.

**Czym może się bronić dłużnik**
Dłużnik nie zablokuje zabezpieczenia samym wstrzymaniem wykonania nakazu. Może natomiast wnosić o:
- ograniczenie zabezpieczenia (art. 492 § 2 k.p.c.);
- uchylenie lub zmianę zabezpieczenia (art. 742 k.p.c.).

Zastrzeżenie: obecnego brzmienia art. 492 k.p.c., w tym numeracji paragrafów po nowelizacji z 2019 r., nie sprawdziłem w Dzienniku Ustaw. Przed użyciem w piśmie warto je potwierdzić w ISAP lub w systemie informacji prawnej.

**Źródła:**
- [SO w Szczecinie, VIII Gz 43/16 – dlajurysty.pl](https://dlajurysty.pl/orzeczenia/pokaz/405970/VIII-Gz-43-16)
- [Art. 492 k.p.c. – standardyprawa.pl](https://standardyprawa.pl/akt/76/art/13396)
- [Art. 492 k.p.c. – analiza, standardyprawa.pl](https://standardyprawa.pl/akt/76/art/13396/analiza/2104)
- [Nakaz zapłaty z weksla a zabezpieczenie – e-prawnik.pl](https://e-prawnik.pl/porady-prawne/nakaz-zaplaty-z-weksla-a-zabezpieczenie.html)
- [Wstrzymanie wykonania nakazu zapłaty – argumenty prawne RPO](https://test-brpo.brpo.gov.pl/sites/default/files/Wstrzymanie%20wykonania%20nakazu%20zap%C5%82aty%20w%20toku%20tocz%C4%85cego%20si%C4%99%20post%C4%99powania%20o%20zap%C5%82at%C4%99%20-%20argumenty%20prawne%20RPO.pdf)
- [Orzeczenie SN – saos.org.pl](https://www.saos.org.pl/judgments/96058)
