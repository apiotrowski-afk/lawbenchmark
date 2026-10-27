---
pytanie: P08
system: 'OpenAI gpt-6-astra przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie
  na żywo'
model: gpt-6-astra
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-18'
czas_s: 29.3
tokeny:
  input_tokens: 57161
  cached_input_tokens: 29824
  cache_write_input_tokens: 0
  output_tokens: 950
  reasoning_output_tokens: 19
wstep: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na
  gruncie prawa polskiego i unijnego, podając podstawy prawne. Odpowiedz bezpośrednio
  w wiadomości — nie twórz plików i nie uruchamiaj poleceń. Możesz korzystać z wyszukiwania
  w internecie; jeśli z niego korzystasz, na końcu podaj adresy źródeł.
sandbox: read-only, pusty katalog, sesja nietrwała
aplikacje_chatgpt: wyłączone (features.apps=false)
liczba_wyszukan: 4
inne_narzedzia: 0
zdarzenia:
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: site.eur-lex.europa.eu 2024/1689 art 3 60 deepfake dźwiękowe art 50
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act
  polecenie: null
  narzedzie: null
blad: null
---

## Pytanie

Treścią typu deepfake nie będzie głos wygenerowany przez AI, który niczego nie udaje i w żaden sposób nie wprowadza w błąd.  czy to prawda na gruncie AI Act?

## Odpowiedź

**Co do zasady tak, ale zdanie wymaga doprecyzowania: istotny jest brak możliwości wprowadzenia odbiorcy w błąd, a nie tylko brak zamiaru oszukania lub faktycznego oszukania kogokolwiek.**

Zgodnie z **art. 3 pkt 60 rozporządzenia (UE) 2024/1689 (AI Act)** kwalifikacja jako deepfake wymaga łącznie, aby treści:

- były wygenerowane lub zmanipulowane przez AI;
- przypominały istniejące osoby, przedmioty, miejsca, podmioty lub zdarzenia;
- mogły zostać niesłusznie uznane przez odbiorcę za autentyczne lub prawdziwe.

Samo wygenerowanie głosu przez AI zatem nie wystarcza. Przepis nie wymaga jednak wykazania zamiaru wprowadzenia w błąd ani rzeczywistego błędu konkretnej osoby. [Podstawa prawna: art. 3 pkt 60 AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=pl).

**„Niczego nie udaje” nie powinno być utożsamiane wyłącznie z brakiem naśladowania głosu konkretnej osoby.** Trzeba również ocenić, czy nagranie nie pozoruje autentycznej wypowiedzi lub zdarzenia. Znaczenie mają kontekst prezentacji i oczekiwania odbiorców. Przykładowo: jawnie syntetyczny głos odczytujący instrukcję, który nie pozoruje rzeczywistej wypowiedzi, zasadniczo nie będzie deepfake’em. Taka ocena odpowiada wskazówkom Komisji dotyczącym potencjału wprowadzenia w błąd i kontekstu użycia. [Wyjaśnienia Komisji Europejskiej](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act).

Można więc użyć precyzyjniejszego sformułowania:

> Głos wygenerowany przez AI nie jest automatycznie treścią deepfake. Nie będzie nią, jeżeli w danym kontekście nie może zostać niesłusznie uznany przez odbiorcę za autentyczny lub prawdziwy w rozumieniu art. 3 pkt 60 AI Act.

**Brak kwalifikacji jako deepfake nie oznacza braku obowiązków dotyczących oznaczania.** Art. 50 ust. 2 przewiduje, co do zasady, obowiązek dostawcy systemu zapewnienia maszynowo czytelnego oznaczania syntetycznych treści audio. Jest to odrębne od obowiązku ujawniania deepfake’ów przez podmiot stosujący system z art. 50 ust. 4. [Podstawa prawna: art. 50 AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=pl).

Źródła: [AI Act — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=pl); [Komisja Europejska — objaśnienia art. 50](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act).
