---
pytanie: P12
system: 'Gemini gemini-3.8-flash (Vertex AI, czysty model — bez narzędzi KTZR, W1:
  Google Search + URL context)'
model: gemini-3.8-flash
projekt: ktzr-asystent
region: global
temperatura: 0.1
poziom_rozumowania: domyślny modelu
prompt_systemowy: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po
  polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne. Możesz korzystać
  z wyszukiwania w internecie; jeśli z niego korzystasz, na końcu podaj adresy źródeł.
narzedzia:
- google_search
- url_context
wyszukiwanie: true
zapytania: []
zrodla: []
data_odpowiedzi: '2026-10-17'
czas_s: 19.1
tokeny:
  wejscie: 212
  wyjscie: 1632
  rozumowanie: 842
blad: null
---

W pytaniu pojawiła się drobna literówka w numeracji artykułu – chodzi o **art. 787[1] k.p.c.** (dotyczący zobowiązań z prowadzenia przedsiębiorstwa), zestawiony z „podstawowym” trybem z **art. 787 k.p.c.** (klauzula na cały majątek wspólny).

Oto szczegółowa analiza prawna tego zagadnienia:

---

### 1. Dwa różne tryby nadania klauzuli na małżonka (art. 787 vs art. 787[1] k.p.c.)

W polskim procesie cywilnym i prawie rodzinnym (art. 41 k.r.o.) funkcjonują dwa odrębne tryby nadania klauzuli wykonalności przeciwko małżonkowi dłużnika:

1. **Tryb „zwykły” – art. 787 k.p.c. (odpowiedzialność z całego majątku wspólnego):**
   * **Wymóg:** Wierzyciel musi wykazać dokumentem urzędowym lub prywatnym, że wierzytelność powstała z czynności prawnej dokonanej **za zgodą małżonka dłużnika**.
   * **Zakres egzekucji:** Sąd nadaje klauzulę z ograniczeniem odpowiedzialności małżonka do majątku objętego wspólnością majątkową (całego majątku wspólnego).

2. **Tryb „przedsiębiorstwa” – art. 787[1] k.p.c. (odpowiedzialność ograniczona do przedsiębiorstwa):**
   * **Wymóg:** Nie jest wymagana zgoda małżonka dłużnika. Wierzyciel musi jedynie wykazać dokumentem urzędowym lub prywatnym, że wierzytelność **powstała w związku z prowadzeniem przedsiębiorstwa**.
   * **Zakres egzekucji:** Sąd ogranicza odpowiedzialność małżonka **wyłącznie do przedsiębiorstwa wchodzącego w skład majątku wspólnego**.

---

### 2. Czy brak wzmianki o działalności w nakazie zapłaty (tytule) pozwala pominąć art. 787[1] k.p.c.?

**Krótka odpowiedź:** Sam brak dopisku o działalności gospodarczej (oraz wskazanie jedynie numeru PESEL) w sentencji nakazu zapłaty **nie uprawnia automatycznie** do uzyskania klauzuli na podstawie art. 787 k.p.c. (na cały majątek wspólny), **jeśli nie posiada Pan/Pani pisemnej zgody małżonka na zaciągnięcie tego zobowiązania**.

#### Dlaczego?
* **Osoba fizyczna prowadząca JDG nie ma odrębnej podmiotowości prawnej:** Osoba fizyczna wpisana do CEIDG odpowiada zawsze swoim majątkiem osobistym i wspólnym jako człowiek (posługujący się PESEL). Brak firmy (nazwy działalności) czy NIP w tytule egzekucyjnym nie zmienia charakteru prawnego dłużnika ani źródła wierzytelności.
* **Kluczowy warunek art. 787 k.p.c. to ZGODA małżonka:** Aby uzyskać klauzulę w „normalnym trybie” (na cały majątek wspólny), sąd bezwzględnie bada, czy przedłożono **dokument urzędowy lub prywatny wykazujący zgodę małżonka** na dokonanie danej czynności prawnej (art. 787 k.p.c. w zw. z art. 41 § 1 k.r.o.). Jeśli nie dysponuje Pan/Pani taką zgodą (np. podpisem małżonka na umowie, osobnym oświadczeniem o wyrażeniu zgody), wniosek oparty na art. 787 k.p.c. zostanie przez sąd **oddalony**.

---

### 3. Jakie są scenariusze w tej sytuacji?

#### Scenariusz A: Wierzyciel POSIADA zgodę małżonka na piśmie
Jeśli małżonek dłużnika wyraził zgodę na zawarcie umowy / zaciągnięcie zobowiązania (nawet gospodarczego):
* **Tak, można, a wręcz należy wnosić na podstawie art. 787 k.p.c.**
* Przedkłada się tytuł wykonawczy, odpis aktu małżeństwa oraz dokument potwierdzający zgodę małżonka. 
* Ograniczenie z art. 787[1] k.p.c. nie ma wówczas zastosowania – egzekucja będzie mogła być skierowana do całego majątku wspólnego (np. rachunków bankowych, nieruchomości wspólnych).

#### Scenariusz B: Wierzyciel NIE POSIADA zgody małżonka (najczęstszy przypadek w obrocie B2B)
Jeżeli zgody małżonka nie ma, a dług wynikał z kontraktu handlowego dłużnika:
* **Nie można skutecznie uzyskać klauzuli w trybie art. 787 k.p.c.** – sąd bada istnienie dokumentu zgody z urzędu i oddali wniosek z powodu jego braku.
* Jedyną ścieżką rozszerzenia klauzuli na małżonka jest wówczas **art. 787[1] k.p.c.**, czyli wniosek o nadanie klauzuli z ograniczeniem do przedsiębiorstwa wchodzącego w skład majątku wspólnego.
* Fakt, że w nakazie jest tylko PESEL, w niczym nie przeszkadza w złożeniu wniosku z art. 787[1] k.p.c. – we wniosku klauzulowym wierzyciel po prostu wykazuje (np. fakturą, umową, odpisem z CEIDG z daty zawarcia umowy), że dochodzone roszczenie powstało w związku z przedsiębiorstwem dłużnika.

---

### Podsumowanie i rekomendacja

Brak wzmianki o „działalności gospodarczej” w tytule egzekucyjnym nie otwiera automatycznie drogi do egzekucji z całego majątku wspólnego. Wybór trybu zależy wyłącznie od tego, czy dysponują Państwo **dowodem zgody małżonka na zaciągnięcie zobowiązania**:

1. **Jest zgoda małżonka na piśmie:** Wniosek z **art. 787 k.p.c.** (odpowiedzialność z całego majątku wspólnego).
2. **Brak zgody małżonka:** Wyłącznie wniosek z **art. 787[1] k.p.c.** (odpowiedzialność ograniczona do przedsiębiorstwa) albo prowadzenie egzekucji wyłącznie z majątku osobistego dłużnika oraz składników wymienionych w art. 41 § 2 k.r.o. (m.in. dochodów z działalności, wynagrodzenia za pracę dłużnika – do czego klauzula na małżonka w ogóle nie jest potrzebna).
