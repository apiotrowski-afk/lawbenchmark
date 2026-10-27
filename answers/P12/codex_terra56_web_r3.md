---
pytanie: P12
system: 'OpenAI gpt-5.6-terra przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie
  na żywo'
model: gpt-5.6-terra
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-17'
czas_s: 45.0
tokeny:
  input_tokens: 141730
  cached_input_tokens: 109056
  cache_write_input_tokens: 0
  output_tokens: 2739
  reasoning_output_tokens: 1276
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
  zapytanie: art. 7811 k.p.c. małżonek klauzula wykonalności działalność gospodarcza
    PESEL ...
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
  zapytanie: Art. 7811 k.p.c. klauzula wykonalności przedsiębiorca ...
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: site:eli.gov.pl kodeks rodzinny opiekuńczy art. 41 odpowiedzialność małżonków
    ...
  polecenie: null
  narzedzie: null
blad: null
---

## Pytanie

Klauzula wykonalności na małżonka, pozew był związany z działalnością gospodarczą, ale w NZ nie ma nic na temat "prowadzący działalnosc" w klauzuli jest PESEL i nie ma żadnej wzmianki nt. dzialalności, czy można wnosić o klauzulę na małżonka w "normalnym trybie'? tj. czy można wnieść o egzkeucję "bez ograniczeń", które wynikają z 781[1] k.p.c. ?

## Odpowiedź

Nie. Sam fakt, że roszczenie wynikało z działalności gospodarczej dłużnika, nie pozwala uzyskać przeciwko jego małżonkowi tytułu „bez ograniczeń”.

W pierwszej kolejności: ograniczenie to wynika z art. **787¹ k.p.c.**, a nie z art. **781¹ k.p.c.** Art. 781¹ k.p.c. dotyczy wyłącznie instrukcyjnego, trzydniowego terminu rozpoznania wniosku o klauzulę.

Możliwe są dwa zasadniczo odmienne warianty:

- **art. 787 k.p.c.** – gdy wierzyciel wykaże dokumentem urzędowym albo prywatnym zgodę małżonka na konkretną czynność prawną, z której powstał dług. Klauzula obejmie małżonka, ale jego odpowiedzialność będzie ograniczona do całego majątku wspólnego.
- **art. 787¹ k.p.c.** – gdy wierzytelność powstała w związku z prowadzeniem przedsiębiorstwa, a przedsiębiorstwo wchodzi w skład majątku wspólnego. Klauzula przeciw małżonkowi jest wówczas obligatoryjnie ograniczona do przedsiębiorstwa wchodzącego w skład majątku wspólnego.

Brak wzmianki w nakazie zapłaty lub już nadanej klauzuli o prowadzeniu działalności ani sam PESEL dłużnika nie zamykają drogi z art. 787¹ k.p.c. Ta okoliczność może być wykazywana we wniosku klauzulowym dokumentami. Należy jednak wykazać nie tylko fakt wpisu dłużnika do CEIDG, lecz także:

1. związek **konkretnej** dochodzonej wierzytelności z przedsiębiorstwem (np. umową, zamówieniem, fakturą, protokołem odbioru, korespondencją, uznaniem długu);
2. że przedsiębiorstwo lub jego składniki należą do majątku wspólnego.

Sam wydruk CEIDG co do zasady dowodzi prowadzenia działalności, lecz niekoniecznie związku tej konkretnej należności z przedsiębiorstwem ani przynależności przedsiębiorstwa do majątku wspólnego.

Nie ma podstaw do pozywania małżonka „w zwykłym trybie” wyłącznie po to, by obejść ograniczenie z art. 787¹ k.p.c. Zgoda małżonka na czynność nie czyni go co do zasady osobistym współdłużnikiem; tworzy podstawę odpowiedzialności majątkiem wspólnym. Pozew przeciwko małżonkowi miałby sens tylko, gdy istnieje samodzielna materialnoprawna podstawa jego osobistej odpowiedzialności, np. był stroną umowy, poręczycielem, współdłużnikiem solidarnym albo przystąpił do długu.

Jeżeli zgody małżonka nie ma lub nie można jej wykazać, wierzyciel nadal może egzekwować od dłużnika jego majątek osobisty, wynagrodzenie, dochody z innej działalności zarobkowej oraz – dla długu związanego z przedsiębiorstwem – składniki przedsiębiorstwa (art. 41 § 2 k.r.o.). Klauzula na małżonka z art. 787¹ jest potrzebna dla egzekucji z tych składników wspólnych, które wchodzą w skład przedsiębiorstwa.

W sprawie czysto krajowej brak odrębnego zagadnienia prawa UE; rozstrzygają art. 41 k.r.o. oraz art. 787–787¹ k.p.c.

Źródła:

- [Kodeks postępowania cywilnego – tekst jednolity](https://eli.gov.pl/eli/DU/1964/296)
- [Art. 41 k.r.o. – oficjalny tekst](https://eli.gov.pl/api/acts/DU/2020/1359/text.html)
- [Postanowienie SO w Szczecinie, VIII Gz 140/18](https://pelnora.app/orzeczenia/sad-okregowy-w-szczecinie/VIII_Gz_140/18)

