---
pytanie: P13
system: 'OpenAI gpt-5.6-terra przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie
  na żywo'
model: gpt-5.6-terra
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-17'
czas_s: 49.1
tokeny:
  input_tokens: 112014
  cached_input_tokens: 86784
  cache_write_input_tokens: 0
  output_tokens: 1559
  reasoning_output_tokens: 463
wstep: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na
  gruncie prawa polskiego i unijnego, podając podstawy prawne. Odpowiedz bezpośrednio
  w wiadomości — nie twórz plików i nie uruchamiaj poleceń. Możesz korzystać z wyszukiwania
  w internecie; jeśli z niego korzystasz, na końcu podaj adresy źródeł.
sandbox: read-only, pusty katalog, sesja nietrwała
aplikacje_chatgpt: wyłączone (features.apps=false)
liczba_wyszukan: 8
inne_narzedzia: 0
zdarzenia:
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: art. 492 § 3 k.p.c. wstrzymanie wykonania nakazu zapłaty postępowanie
    zabezpieczające orzecznictwo ...
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: '"Art. 492" "Kwota zabezpieczenia" kpc ...'
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: '"Nakaz zapłaty z weksla" "w dalszym ciągu wykonany jako tytuł zabezpieczający"
    ...'
  polecenie: null
  narzedzie: null
blad: null
---

## Pytanie

Sąd wydał NZ w nakazowym z weksla i wstrzymał jego wykonanie. Czy obejmuje to też możliwość wszczęcia w oparciu o NZ post zabezpieczeającego ?

## Odpowiedź

Co do zasady — tak. Samo wstrzymanie wykonania nakazu zapłaty wydanego z weksla na podstawie art. 492 § 3 k.p.c. nie pozbawia go funkcji tytułu zabezpieczenia. Wierzyciel może więc wszcząć (albo kontynuować) postępowanie zabezpieczające na podstawie tego nakazu.

Wynika to z rozróżnienia dwóch skutków nakazu:

- od chwili wydania nakaz stanowi z mocy art. 492 § 1 k.p.c. tytuł zabezpieczenia, wykonalny bez klauzuli wykonalności;
- nakaz z weksla po upływie terminu do spełnienia świadczenia staje się ponadto natychmiast wykonalny (art. 492 § 3 k.p.c.), co otwiera drogę do egzekucji świadczenia. Wstrzymanie dotyczy właśnie tej drugiej funkcji — jako podstawy egzekucji — a nie zabezpieczenia.

Takie stanowisko wyraźnie przyjął m.in. SA w Szczecinie w postanowieniu z 18.07.2013 r., I ACz 390/13, oraz SA w Gdańsku w postanowieniu VIII Gz 43/16: wstrzymanie wykonania z art. 492 § 3 k.p.c. nie odbiera nakazowi cech tytułu zabezpieczającego.

Jeżeli celem jest zablokowanie zabezpieczenia, należy sformułować odrębny wniosek o jego ograniczenie albo uchylenie — na podstawie art. 492 § 2 k.p.c. w zw. z art. 742 k.p.c. Wniosek powinien wprost obejmować zakaz wykonywania nakazu jako tytułu zabezpieczenia (ewentualnie zawieszenie już toczącego się postępowania zabezpieczającego), a nie tylko „wstrzymanie wykonania nakazu” z § 3. Ostatecznie decyduje oczywiście dokładna sentencja wydanego postanowienia: jeżeli sąd wyraźnie objął nią także zabezpieczenie, wszczęcie będzie niedopuszczalne w tym zakresie.

Źródła: [art. 492 k.p.c. — tekst jednolity](https://www.dziennikustaw.gov.pl/DU/2023/1550), [SA Szczecin, I ACz 390/13](https://www.saos.org.pl/judgments/14498), [SA Gdańsk, VIII Gz 43/16](https://www.saos.org.pl/judgments/213643), [SN, I CZ 83/09](https://www.sn.pl/sites/orzecznictwo/Orzeczenia1/I%20CZ%2083-09.pdf).
