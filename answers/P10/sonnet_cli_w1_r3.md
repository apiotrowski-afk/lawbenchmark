---
pytanie: P10
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
czas_s: 36.1
tokeny:
  input_tokens: 2
  cache_creation_input_tokens: 855
  cache_read_input_tokens: 1437
  output_tokens: 4723
  output_tokens_details:
    thinking_tokens: 2117
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 855
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 4723
    cache_read_input_tokens: 1437
    cache_creation_input_tokens: 855
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 855
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.051203499999999985
blad: null
---

**Nie, to ryzykowne.** Samo sformułowanie „przenosi na wszelkie pola eksploatacji” jest niewystarczające, a w praktyce sądowej i doktrynie uznaje się je za nieskuteczne albo przynajmniej bardzo ryzykowne.

## Podstawa prawna
- **Art. 41 ust. 2 pr. aut. wym.** stanowi, że umowa o przeniesienie praw majątkowych (lub o korzystanie z utworu) obejmuje pola eksploatacji **wyraźnie w niej wymienione**. Klauzula generalna „wszelkie pola” nie spełnia tego wymogu.
- **Art. 50 pr. aut. wym.** zawiera przykładowy katalog pól eksploatacji. Można z niego korzystać przy redagowaniu umowy, ale samo odesłanie do „pól z art. 50” też nie wystarcza. Pola należy wymienić w umowie.
- **Art. 53 pr. aut. wym.** wymaga formy pisemnej pod rygorem nieważności (w polskim prawie to forma dokumentowa nie wystarcza, potrzebny jest podpis, w tym kwalifikowany podpis elektroniczny).
- **Art. 41 ust. 3 pr. aut. wym.** zakazuje umowy obejmującej wszystkie utwory przyszłe danego twórcy. Utwory przyszłe muszą być oznaczone co najmniej rodzajowo, np. „materiały graficzne i wideo tworzone w ramach zlecenia nr…”.
- **Art. 41 ust. 4 pr. aut. wym.** stanowi, że umowa jest nieważna w części dotyczącej pól eksploatacji nieznanych w chwili jej zawarcia. Nie da się więc skutecznie objąć „przyszłych technologii”.
- **Art. 46 pr. aut. wym.** dotyczy praw zależnych. Zezwolenie na wykonywanie praw zależnych (opracowania, przeróbki, remiksy, adaptacje) trzeba w umowie wskazać odrębnie.
- **Art. 43 pr. aut. wym.** stanowi, że przeniesienie praw jest co do zasady odpłatne. Przy zleceniu warto więc wskazać, że wynagrodzenie obejmuje przeniesienie praw.

## Konsekwencje błędnego zapisu
Jeśli pola nie zostaną wymienione, zleceniodawca może nie nabyć praw w oczekiwanym zakresie. Sądy tłumaczą wątpliwości na korzyść twórcy. Wada może dotyczyć całego przeniesienia albo tylko pól niewymienionych, co zależy od brzmienia umowy. W efekcie klient może korzystać z materiałów tylko w zakresie wynikającym z celu umowy, a jego dalsze wykorzystanie (np. reklama płatna czy druk) bywa sporne.

## Co warto wpisać przy social media
1. **Utrwalanie i zwielokrotnianie** dowolną techniką (cyfrowo, w pamięci urządzeń, na serwerach).
2. **Publiczne udostępnianie w taki sposób, aby każdy miał dostęp w miejscu i czasie przez siebie wybranym**, w tym w internecie, w mediach społecznościowych (z wymienieniem platform) i na stronach www.
3. **Wprowadzanie do obrotu** i **najem/użyczenie** (jeśli dotyczy).
4. **Publiczne wyświetlanie, odtwarzanie, nadawanie i reemitowanie**, w tym w reklamie, także płatnej (ads, boosting).
5. **Wykorzystanie w materiałach reklamowych i marketingowych** oraz **druk** (np. plakaty, ulotki, materiały eventowe).
6. **Prawa zależne**: tłumaczenie, adaptowanie, przeróbki, zmiana formatu, kadrowanie, montaż, łączenie z innymi utworami. Do tego **zezwolenie na wykonywanie i rozporządzanie** nimi.
7. **Prawo do udzielania dalszych licencji (sublicencji)** i **prawo do przenoszenia praw** na osoby trzecie, np. agencję czy podmioty z grupy kapitałowej.
8. **Zakres terytorialny i czasowy**. Przy przeniesieniu praw czas jest co do zasady nieograniczony, ale warto to wpisać.
9. **Moment przejścia praw**, np. z chwilą odbioru lub zapłaty. Warto doprecyzować, czy chodzi o każdy utwór osobno.
10. **Przeniesienie własności nośników** (art. 56 pr. aut. wym. w zw. z art. 49).

## Kwestie dodatkowe
- **Prawa osobiste** (art. 16) są niezbywalne. Można za to uregulować zgodę na wykonywanie zależnych praw osobistych (np. nieoznaczanie autorstwa, zgoda na dokonywanie zmian) oraz zobowiązanie do niewykonywania tych praw. Taka konstrukcja jest dopuszczalna w ograniczonym zakresie.
- **Oświadczenia zleceniobiorcy**: że jest wyłącznym twórcą, że utwory nie naruszają praw osób trzecich (zdjęcia, muzyka, czcionki, wizerunek), oraz klauzula o odpowiedzialności z tytułu rękojmi za prawa.
- **Wizerunek i muzyka**: zgoda na rozpowszechnianie wizerunku (art. 81 pr. aut. wym.) nie wynika z przeniesienia praw autorskich, więc trzeba ją uregulować odrębnie. Licencje na muzykę i stocki także.
- **Wynagrodzenie**: warto wskazać, że obejmuje wszystkie pola eksploatacji i przeniesienie praw. Dla twórcy może to być podstawa roszczenia z art. 44 pr. aut. wym. (dodatkowe wynagrodzenie) lub art. 436 KC, a jego wyłączenie jest ograniczone.
- **Rażąca dysproporcja** wynagrodzenia i korzyści zleceniodawcy może uzasadniać roszczenie na podstawie art. 44 pr. aut. wym.
- Jeśli zleceniobiorca działa w ramach działalności gospodarczej, a nie jako osoba fizyczna, przepisy o przeniesieniu praw stosuje się tak samo. Różni się tylko opodatkowanie, np. brak 50% KUP.

## Rekomendacja
Zamiast klauzuli ogólnej zastosuj **wyliczenie pól eksploatacji** w katalogu dopasowanym do charakteru zlecenia, z dopiskiem, że lista jest wyczerpująca (bo nie można jej otworzyć na „inne”). Jeśli chcesz, mogę przygotować wzór klauzuli dla social media.

Nie korzystałem z wyszukiwania w internecie. Odpowiedź opiera się na treści ustawy z 4.02.1994 r. o prawie autorskim i prawach pokrewnych. Numerację ustępów (zwłaszcza art. 41 ust. 3–4) warto zweryfikować w aktualnym tekście jednolitym przed użyciem w opinii.
