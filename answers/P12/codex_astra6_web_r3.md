---
pytanie: P12
system: 'OpenAI gpt-6-astra przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie
  na żywo'
model: gpt-6-astra
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-17'
czas_s: 44.0
tokeny:
  input_tokens: 81048
  cached_input_tokens: 66304
  cache_write_input_tokens: 0
  output_tokens: 1328
  reasoning_output_tokens: 28
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
  zapytanie: art. 787 7871 7811 kpc małżonek przedsiębiorstwo zgoda ...
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: https://eli.gov.pl/api/acts/DU/2026/468/text.html
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: art 7811 kpc niezwłocznie trzy dni ...
  polecenie: null
  narzedzie: null
blad: null
---

## Pytanie

Klauzula wykonalności na małżonka, pozew był związany z działalnością gospodarczą, ale w NZ nie ma nic na temat "prowadzący działalnosc" w klauzuli jest PESEL i nie ma żadnej wzmianki nt. dzialalności, czy można wnosić o klauzulę na małżonka w "normalnym trybie'? tj. czy można wnieść o egzkeucję "bez ograniczeń", które wynikają z 781[1] k.p.c. ?

## Odpowiedź

**Można wnosić o klauzulę przeciwko małżonkowi na podstawie art. 787 k.p.c. także przy długu związanym z działalnością gospodarczą — ale trzeba wykazać dokumentem zgodę małżonka na czynność prawną będącą źródłem wierzytelności. Sam brak wzmianki o działalności w nakazie zapłaty lub klauzuli nie pozwala rozszerzyć egzekucji.**

Zakładam, że chodzi o **art. 787¹ k.p.c.**, ponieważ art. 781¹ k.p.c. dotyczy terminu rozpoznania wniosku o klauzulę.

W opisanej sytuacji należy rozróżnić dwie podstawy:

| Podstawa | Co trzeba wykazać dokumentem urzędowym lub prywatnym | Zakres odpowiedzialności małżonka |
|---|---|---|
| **Art. 787 k.p.c.** | Wierzytelność powstała z czynności prawnej dokonanej za zgodą małżonka dłużnika | Majątek objęty wspólnością majątkową — również składniki poza przedsiębiorstwem |
| **Art. 787¹ k.p.c.** | Wierzytelność powstała w związku z prowadzeniem przedsiębiorstwa | Przedsiębiorstwo wchodzące w skład majątku wspólnego |

Gospodarczy charakter długu **nie wyłącza zastosowania art. 787 k.p.c.** Jeżeli macie dokument wykazujący wymaganą zgodę, można żądać klauzuli z szerszym zakresem odpowiedzialności niż samo przedsiębiorstwo. Odpowiada to rozróżnieniu z art. 41 § 1 i 2 k.r.o. [K.p.c.](https://eli.gov.pl/api/acts/DU/2026/468/text.html), [art. 41 k.r.o.](https://eli.gov.pl/api/acts/DU/2023/2809/text.html).

**Brak dopisku „prowadzący działalność gospodarczą” i wskazanie samego PESEL nie zmieniają tej oceny.** Przy jednoosobowej działalności dłużnikiem jest osoba fizyczna. O podstawie rozszerzenia klauzuli decydują źródło wierzytelności i zgoda małżonka, a nie sposób opisania dłużnika w nakazie. Związek wierzytelności z przedsiębiorstwem może wynikać z dokumentów dotyczących zobowiązania, nawet jeśli nie wskazano go w sentencji nakazu. Takie rozróżnienie podstaw odpowiedzialności przedstawia również [SN w uzasadnieniu sprawy III CZP 106/18](https://www.sn.pl/sites/orzecznictwo/orzeczenia3/iii%20czp%20106-18.pdf).

Nie wystarczy natomiast argument, że małżonek wiedział o prowadzeniu firmy lub akceptował działalność. Potrzebny jest dokument wykazujący zgodę na czynność, z której wynika dochodzona wierzytelność. SN wykluczył zastępowanie tego wymagania domniemaniem faktycznym — uchwała z 18 marca 2011 r., III CZP 117/10. [Treść uchwały](https://www.saos.org.pl/judgments/94458).

**Praktycznie: jeżeli jest udokumentowana zgoda, wniosek należy oprzeć na art. 787 k.p.c., żądając ograniczenia odpowiedzialności małżonka do majątku objętego wspólnością majątkową.** Nie należy żądać klauzuli „bez ograniczeń”: także ten tryb nie otwiera egzekucji z majątku osobistego małżonka. Jeśli zgody nie można wykazać dokumentem, samo pominięcie działalności w nakazie nie daje podstaw do uzyskania szerszej klauzuli.

Źródła: [Kodeks postępowania cywilnego](https://eli.gov.pl/api/acts/DU/2026/468/text.html), [Kodeks rodzinny i opiekuńczy](https://eli.gov.pl/api/acts/DU/2023/2809/text.html), [SN, III CZP 117/10](https://www.saos.org.pl/judgments/94458), [SN, III CZP 106/18](https://www.sn.pl/sites/orzecznictwo/orzeczenia3/iii%20czp%20106-18.pdf).
