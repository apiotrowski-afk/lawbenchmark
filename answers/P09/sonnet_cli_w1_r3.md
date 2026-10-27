---
pytanie: P09
system: 'Claude claude-sonnet-5-5 przez Claude Code CLI (subskrypcja), czysty model
  — bez MCP i CLAUDE.md, W1: WebSearch + WebFetch'
model_alias: claude-sonnet-5-5
model_id: claude-haiku-5-5,claude-sonnet-5-5
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
czas_s: 42.3
tokeny:
  input_tokens: 2
  cache_creation_input_tokens: 860
  cache_read_input_tokens: 1437
  output_tokens: 5610
  output_tokens_details:
    thinking_tokens: 3174
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 860
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 5610
    cache_read_input_tokens: 1437
    cache_creation_input_tokens: 860
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 860
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.059986
blad: null
---

Tak, tak to się przyjmuje w doktrynie i orzecznictwie. Sam zapis, że zleceniobiorca „przenosi prawa na wszelkich polach eksploatacji”, jest ryzykowny i może nie wywołać skutku, o który chodzi zleceniodawcy.

## Podstawy prawne

- **Art. 41 ust. 2 pr. aut.** stanowi, że umowa o przeniesienie autorskich praw majątkowych obejmuje pola eksploatacji *wyraźnie w niej wymienione*. Ustawa wymaga więc wyliczenia pól, a nie ogólnego odesłania do wszystkich.
- **Art. 50 pr. aut.** zawiera przykładowy katalog pól eksploatacji. Obejmuje on utrwalanie i zwielokrotnianie, obrót egzemplarzami, publiczne wykonanie, wyświetlanie i nadawanie. Obejmuje też publiczne udostępnianie w taki sposób, aby każdy miał dostęp w miejscu i czasie przez siebie wybranym, czyli internet.
- **Art. 53 pr. aut.** wymaga formy pisemnej pod rygorem nieważności dla przeniesienia praw. Dla licencji wyłącznej taki sam wymóg wynika z art. 67 ust. 5. Forma pisemna oznacza podpis własnoręczny albo kwalifikowany podpis elektroniczny (art. 78¹ KC). Wymiana e-maili ani forma dokumentowa nie wystarczą.
- **Art. 41 ust. 3 pr. aut.** przewiduje nieważność postanowienia dotyczącego wszystkich utworów przyszłych danego twórcy. Umowa musi więc oznaczać utwory, np. przez odniesienie do materiałów wytworzonych w wykonaniu danej umowy.
- **Art. 41 ust. 4 pr. aut.** dotyczy pól nieznanych w chwili zawarcia umowy. Zapis „wszelkie pola, także przyszłe” jest w tym zakresie bezskuteczny.
- **Art. 46 pr. aut.** oraz **art. 2 pr. aut.** dotyczą opracowań, czyli utworów zależnych. Zezwolenie na wykonywanie praw zależnych, np. na przeróbki, remiksy, montaż i adaptacje do innych formatów, trzeba zapisać osobno.
- **Art. 43 pr. aut.** zawiera domniemanie odpłatności. Wynagrodzenie za przeniesienie praw warto wyodrębnić w umowie. Przy rażącej dysproporcji zleceniobiorca może żądać podwyższenia wynagrodzenia (art. 44 pr. aut.).
- **Prawa osobiste** (art. 16 pr. aut.) są niezbywalne. Można za to uregulować zezwolenie na dokonywanie zmian, zobowiązanie do niewykonywania autorskich praw osobistych oraz sposób oznaczania autorstwa, np. brak oznaczenia przy publikacji.

## Skutki ogólnego zapisu

Pola, które nie zostały wymienione, nie przechodzą na zleceniodawcę. Zleceniobiorca pozostaje wtedy uprawniony na tych polach. Zleceniodawca może się wtedy bronić tylko koncepcją licencji dorozumianej, ograniczonej do celu umowy. To jest niepewne i trudne do wykazania.

## Jak zredagować zapis w umowie na social media

1. **Wymień pola eksploatacji konkretnie:**
   - utrwalanie i zwielokrotnianie dowolną techniką, w tym cyfrową;
   - wprowadzanie do pamięci komputera i do sieci;
   - publiczne udostępnianie w internecie, w tym w serwisach społecznościowych (np. Facebook, Instagram, TikTok, YouTube, LinkedIn) oraz na stronach www zleceniodawcy;
   - publiczne odtwarzanie, wyświetlanie i nadawanie;
   - użycie w reklamie, promocji i marketingu (w tym płatnych kampaniach);
   - obrót oryginałem lub egzemplarzami, jeśli jest potrzebny.
2. **Dodaj prawa zależne** (art. 46 pr. aut.). Wskaż zezwolenie na opracowywanie, przeróbki, skracanie, montaż i adaptację oraz na rozporządzanie i korzystanie z opracowań.
3. **Zapisz moment przejścia praw**, np. z chwilą zapłaty albo odbioru materiałów. Ustal też, co dzieje się z prawami do wersji roboczych.
4. **Określ zakres terytorialny i czasowy** (np. bez ograniczeń) oraz **prawo zależne i prawo własności nośników**.
5. **Uregulowanie wizerunku i elementów cudzych** (art. 81 pr. aut.): zgody osób występujących w materiałach, muzyka, czcionki, zdjęcia stockowe i licencje na nie, a także materiały generowane narzędziami AI. Zleceniobiorca powinien oświadczyć, że materiały są wolne od praw osób trzecich, i odpowiadać za wady prawne (art. 55¹ pr. aut. w zw. z art. 556 KC w zw. z art. 750 KC).
6. **Zastrzeż prawo do dalszych rozporządzeń** i do udzielania sublicencji. Jeśli prawa nie mają być przeniesione, tylko licencjonowane, wybierz licencję wyłączną na wskazanych polach.

## Uwagi praktyczne

- Przeniesienie praw jest skuteczne tylko dla materiałów, które spełniają przesłanki utworu (art. 1 pr. aut.). Przy prostych postach, hasłach i zdjęciach produktowych bywa to wątpliwe, więc warto zabezpieczyć się również zobowiązaniem do niedochodzenia roszczeń.
- Jeśli zleceniobiorca działa jako osoba fizyczna, nadal stosuje się zasady zlecenia (art. 734 KC i nast.). Prawa autorskie to osobna sprawa od samej umowy zlecenia i muszą być uregulowane wyraźnie.
- Nie podaję sygnatur orzeczeń, bo nie weryfikowałem ich w tej odpowiedzi. Linia SN i sądów apelacyjnych jest stabilna co do wymogu wyraźnego wymienienia pól. Przed powołaniem się na orzeczenie w piśmie lub opinii sprawdziłbym aktualne sygnatury w bazie orzeczeń.

Mogę przygotować projekt klauzuli o przeniesieniu praw dostosowany do social media, w wariancie z przeniesieniem praw albo z licencją wyłączną.
