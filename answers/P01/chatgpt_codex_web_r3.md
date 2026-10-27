---
pytanie: P01
system: 'OpenAI gpt-6.1-sol przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie
  na żywo'
model: gpt-6.1-sol
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-18'
czas_s: 30.1
tokeny:
  input_tokens: 70211
  cached_input_tokens: 52864
  cache_write_input_tokens: 0
  output_tokens: 623
  reasoning_output_tokens: 21
wstep: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na
  gruncie prawa polskiego i unijnego, podając podstawy prawne. Odpowiedz bezpośrednio
  w wiadomości — nie twórz plików i nie uruchamiaj poleceń. Możesz korzystać z wyszukiwania
  w internecie; jeśli z niego korzystasz, na końcu podaj adresy źródeł.
sandbox: read-only, pusty katalog, sesja nietrwała
aplikacje_chatgpt: wyłączone (features.apps=false)
liczba_wyszukan: 6
inne_narzedzia: 0
zdarzenia:
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: site.isap.sejm.gov.pl kodeks wykroczeń art. 119 800 złotych 2026 ...
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: https://eli.gov.pl/api/acts/DU/2025/734/text.html
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: site.gov.pl 800 kradzież 2026 wykroczenie ...
  polecenie: null
  narzedzie: null
blad: null
---

## Pytanie

Ile wynosi w tym roku wartość mienia przy wykroczeniu max ? Czy zmieniła się w zw. ze wzrostem płacy minmalnej ?

## Odpowiedź

**W 2026 r. próg wynosi 800 zł włącznie** — jeżeli chodzi o zwykłą kradzież lub przywłaszczenie cudzej rzeczy ruchomej. Wynika to z **art. 119 § 1 Kodeksu wykroczeń**. Powyżej 800 zł czyn co do zasady stanowi przestępstwo.

**Wzrost płacy minimalnej nie zmienił tego progu.** Obecnie jest on określony kwotowo. Dawne powiązanie z ¼ minimalnego wynagrodzenia zniesiono 15 listopada 2018 r.; próg 800 zł obowiązuje od 1 października 2023 r.

Nie jest to jednak uniwersalna granica dla wszystkich czynów przeciwko mieniu — np. kradzież z włamaniem może stanowić przestępstwo również przy wartości poniżej 800 zł (art. 279 § 1 k.k. w zw. z art. 130 k.w.).

Źródła: [Kodeks wykroczeń — art. 119 i 130](https://api.sejm.gov.pl/eli/acts/DU/2025/734/text.pdf), [ustawa znosząca powiązanie z płacą minimalną](https://api.sejm.gov.pl/eli/acts/DU/2018/2077/text.html).
