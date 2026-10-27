---
pytanie: P08
system: 'OpenAI gpt-6.1-sol przez Codex CLI (rozumowanie: medium), W0 bez wyszukiwania'
model: gpt-6.1-sol
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-18'
czas_s: 29.3
tokeny:
  input_tokens: 10619
  cached_input_tokens: 0
  cache_write_input_tokens: 0
  output_tokens: 990
  reasoning_output_tokens: 291
wstep: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na
  gruncie prawa polskiego i unijnego, podając podstawy prawne. Odpowiedz bezpośrednio
  w wiadomości — nie twórz plików i nie uruchamiaj poleceń.
sandbox: read-only, pusty katalog, sesja nietrwała
aplikacje_chatgpt: wyłączone (features.apps=false)
liczba_wyszukan: 0
inne_narzedzia: 0
zdarzenia: []
blad: null
---

## Pytanie

Treścią typu deepfake nie będzie głos wygenerowany przez AI, który niczego nie udaje i w żaden sposób nie wprowadza w błąd.  czy to prawda na gruncie AI Act?

## Odpowiedź

**Co do zasady tak, ale zdanie wymaga doprecyzowania: sam brak zamiaru wprowadzenia w błąd nie wyklucza kwalifikacji jako deepfake.**

Zgodnie z **art. 3 pkt 60 rozporządzenia (UE) 2024/1689 (AI Act)** treści typu deepfake to wygenerowane lub zmanipulowane przez AI obrazy, treści dźwiękowe lub wideo, które przypominają istniejące osoby, przedmioty, miejsca, inne podmioty lub zdarzenia i które odbiorca mógłby niesłusznie uznać za autentyczne lub prawdziwe.

W konsekwencji:

- **Syntetyczny głos fikcyjnego lektora**, który nie podszywa się pod konkretną osobę ani nie pozoruje autentycznego nagrania osoby lub zdarzenia, co do zasady nie będzie deepfake’em. Samo naturalne brzmienie głosu nie przesądza o takiej kwalifikacji.
- **Nie trzeba wykazywać zamiaru oszukania ani rzeczywistego wprowadzenia kogokolwiek w błąd.** Istotne jest, czy odbiorca *mógłby* niesłusznie uznać treść za autentyczną lub prawdziwą.
- **Brak imitowania konkretnej osoby nie zawsze wystarcza** — przykładowo nagranie z fikcyjnymi głosami może pozorować rzeczywiste zdarzenie.
- Samo oznaczenie nagrania jako wygenerowanego przez AI nie oznacza automatycznie, że przestaje ono być deepfake’em. **Art. 50 ust. 4** przewiduje właśnie obowiązek ujawniania sztucznego pochodzenia takich treści przez podmioty stosujące systemy AI.

**Brak kwalifikacji jako deepfake nie oznacza też braku obowiązków wynikających z AI Act.** Art. 50 ust. 2 nakłada na dostawców systemów generujących syntetyczne treści, w tym dźwiękowe, obowiązek zapewnienia oznaczania wyników w formacie nadającym się do odczytu maszynowego i ich wykrywalności jako sztucznie wygenerowanych lub zmanipulowanych, z przewidzianymi w tym przepisie wyjątkami.

Bezpieczniejsze sformułowanie brzmi:

> „Głos wygenerowany przez AI nie jest deepfake’em wyłącznie dlatego, że jest syntetyczny. Co do zasady nie będzie nim, jeżeli nie imituje istniejącej osoby ani nie pozoruje autentycznej treści lub zdarzenia, które odbiorca mógłby niesłusznie uznać za prawdziwe”.

Podstawa prawna: [art. 3 pkt 60 i art. 50 ust. 2 i 4 AI Act](https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:32024R1689). Obowiązki z art. 50 stosuje się od **2 sierpnia 2026 r.** (art. 113).
