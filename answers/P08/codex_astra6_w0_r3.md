---
pytanie: P08
system: 'OpenAI gpt-6-astra przez Codex CLI (rozumowanie: medium), W0 bez wyszukiwania'
model: gpt-6-astra
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-18'
czas_s: 25.0
tokeny:
  input_tokens: 10553
  cached_input_tokens: 0
  cache_write_input_tokens: 0
  output_tokens: 842
  reasoning_output_tokens: 161
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

**Co do zasady tak, ale stwierdzenie wymaga doprecyzowania: sam fakt wygenerowania głosu przez AI nie oznacza, że jest on deepfake’em w rozumieniu AI Act.**

Zgodnie z **art. 3 pkt 60 rozporządzenia (UE) 2024/1689 (AI Act)** deepfake oznacza wygenerowane lub zmanipulowane przez AI obrazy, treści dźwiękowe lub treści wideo, które:
- przypominają istniejące osoby, przedmioty, miejsca, podmioty lub zdarzenia oraz
- mogłyby zostać przez odbiorcę niesłusznie uznane za autentyczne lub prawdziwe.

**Zwykły syntetyczny głos lektora, który nie imituje konkretnej osoby ani nie przedstawia fikcyjnego nagrania jako rzeczywistego, co do zasady nie będzie więc deepfake’em.** Nie wystarczy jednak stwierdzić, że twórca „niczego nie udaje” lub nie zamierza nikogo oszukać. Definicja nie wymaga zamiaru wprowadzenia w błąd ani dowodu, że ktoś rzeczywiście został oszukany — istotna jest możliwość błędnego odbioru treści jako autentycznej lub prawdziwej. Znaczenie ma zatem także kontekst wykorzystania głosu, np. przedstawienie go jako nagrania rzeczywistej rozmowy lub zdarzenia.

Trzeba również odróżnić **kwalifikację jako deepfake od obowiązków oznaczania treści syntetycznych**:
- **Art. 50 ust. 4 AI Act** nakłada na podmioty stosujące systemy AI obowiązek ujawnienia sztucznego wygenerowania lub zmanipulowania treści stanowiących deepfake, z przewidzianymi w tym przepisie wyjątkami i szczególnymi zasadami. Samo dodanie oznaczenia „wygenerowane przez AI” nie wyłącza automatycznie kwalifikacji jako deepfake.
- **Art. 50 ust. 2 AI Act** przewiduje szerszy obowiązek po stronie **dostawców** systemów generujących syntetyczne treści, w tym dźwięk: zapewnienie oznakowania wyników w formacie nadającym się do odczytu maszynowego i możliwości wykrycia ich sztucznego pochodzenia, z zastrzeżeniami określonymi w tym przepisie. Obowiązek ten może obejmować również głos, który nie jest deepfake’em.

Najbezpieczniejsze sformułowanie brzmi: **„Głos wygenerowany przez AI nie jest automatycznie deepfake’em. Nie będzie nim, jeżeli nie spełnia przesłanek z art. 3 pkt 60 AI Act, w szczególności nie może być niesłusznie odebrany jako autentyczne lub prawdziwe nagranie istniejącej osoby albo zdarzenia. Nie wyklucza to obowiązków oznaczania treści syntetycznych”.**
