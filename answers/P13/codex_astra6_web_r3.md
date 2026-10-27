---
pytanie: P13
system: 'OpenAI gpt-6-astra przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie
  na żywo'
model: gpt-6-astra
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-17'
czas_s: 37.2
tokeny:
  input_tokens: 90259
  cached_input_tokens: 71296
  cache_write_input_tokens: 0
  output_tokens: 801
  reasoning_output_tokens: 8
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
  zapytanie: wstrzymanie wykonania nakazu zapłaty weksel nie pozbawia tytułu zabezpieczenia
    art 492 3
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: https://www.saos.org.pl/judgments/14498
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: '"I ACz 390/13" "2013" "Sąd"'
  polecenie: null
  narzedzie: null
blad: null
---

## Pytanie

Sąd wydał NZ w nakazowym z weksla i wstrzymał jego wykonanie. Czy obejmuje to też możliwość wszczęcia w oparciu o NZ post zabezpieczeającego ?

## Odpowiedź

**Nie — samo wstrzymanie wykonania nakazu zapłaty z weksla nie wyłącza możliwości wszczęcia na jego podstawie postępowania zabezpieczającego.** Zakładam, że sąd wstrzymał wykonanie na podstawie art. 492 § 3 k.p.c. i nie rozstrzygnął odrębnie o zabezpieczeniu.

Nakaz ma dwa niezależne skutki:

- **Jest tytułem zabezpieczenia już od chwili wydania**, bez potrzeby nadawania klauzuli wykonalności — art. 492 § 1 k.p.c.
- Nakaz wydany z weksla staje się ponadto natychmiast wykonalny po upływie terminu do zaspokojenia roszczenia. **Wstrzymanie na podstawie art. 492 § 3 k.p.c. dotyczy tej wykonalności**, czyli możliwości egzekucyjnego zaspokojenia wierzyciela. Nie usuwa skutku zabezpieczającego. [Art. 492 k.p.c.](https://lexlege.pl/kpc/art-492/)

Takie stanowisko wyraził wprost **SA w Rzeszowie w postanowieniu z 21 czerwca 2013 r., I ACz 390/13**: wstrzymanie wykonania nakazu nie pozbawia go cech tytułu zabezpieczającego. [Treść orzeczenia](https://www.saos.org.pl/judgments/14498)

**Praktycznie: wierzyciel nadal może wystąpić do komornika o wykonanie zabezpieczenia**, wskazując jego sposób, np. zajęcie rachunku bankowego. Samo postanowienie o wstrzymaniu wykonania NZ nie wystarczy, aby temu zapobiec.

Po stronie pozwanego należy zatem rozważyć **odrębny wniosek o ograniczenie zabezpieczenia na podstawie art. 492 § 2 k.p.c. albo o jego uchylenie lub zmianę przy odpowiednim zastosowaniu art. 742 k.p.c.**, zależnie od przesłanek. Dla konkretnej sprawy trzeba sprawdzić dokładną sentencję postanowienia: czy obejmuje jedynie wstrzymanie wykonania NZ, czy również rozstrzygnięcie dotyczące zabezpieczenia.

Źródła: [art. 492 k.p.c.](https://lexlege.pl/kpc/art-492/), [postanowienie SA w Rzeszowie, I ACz 390/13](https://www.saos.org.pl/judgments/14498).
