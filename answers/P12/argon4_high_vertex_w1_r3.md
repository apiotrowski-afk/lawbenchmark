---
pytanie: P12
system: 'Gemini gemini-4-argon (Vertex AI, czysty model — bez narzędzi KTZR, W1: Google
  Search + URL context)'
model: gemini-4-argon
projekt: ktzr-asystent
region: global
temperatura: 0.1
poziom_rozumowania: high
prompt_systemowy: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po
  polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne. Możesz korzystać
  z wyszukiwania w internecie; jeśli z niego korzystasz, na końcu podaj adresy źródeł.
narzedzia:
- google_search
- url_context
wyszukiwanie: true
zapytania:
- '"787" "787^1" kpc klauzula na małżonka działalność gospodarcza'
- klauzula wykonalności przeciwko małżonkowi 787 kpc 787 1 kpc
- '"787" kpc "prowadzący działalność gospodarczą" tytuł egzekucyjny'
- '"787(1)" OR "787 1" kpc nakaz zapłaty działalność gospodarcza'
- '"787 1" kpc uchwała Sądu Najwyższego przedsiębiorstwo majątek wspólny'
- '"787" kpc zgoda małżonka działalność gospodarcza'
zrodla:
- dauerman.com.pl
- ms.gov.pl
- poradnikprzedsiebiorcy.pl
- inforlex.pl
- msbadwokat.pl
- saos.org.pl
- codozasady.pl
- krakow.sa.gov.pl
- i-rs.pl
- poradnikprzedsiebiorcy.pl
- kancelariamikucki.pl
- mckancelaria.pl
- krosno.sr.gov.pl
- blochkancelaria.pl
- kbpp.pl
data_odpowiedzi: '2026-10-18'
czas_s: 189.7
tokeny:
  wejscie: 505
  wyjscie: 3943
  rozumowanie: 7288
blad: null
---

Na wstępie należy uporządkować podstawę prawną: ograniczenie odpowiedzialności małżonka dłużnika wyłącznie do **przedsiębiorstwa** wchodzącego w skład majątku wspólnego wynika z **art. 787¹ k.p.c.** (w pytaniu omyłkowo wskazano art. 781¹ k.p.c.), natomiast „zwykły” (szerszy) tryb nadania klauzuli wykonalności przeciwko małżonkowi reguluje **art. 787 k.p.c.** (ograniczenie odpowiedzialności do **całego majątku objętego wspólnością majątkową**).

Odpowiedź na pytanie, czy można pominąć ograniczenie z art. 787¹ k.p.c. i wnieść o klauzulę na cały majątek wspólny w trybie art. 787 k.p.c., **zależy wyłącznie od tego, czy wierzyciel dysponuje dokumentem potwierdzającym zgodę małżonka dłużnika na zaciągnięcie zobowiązania**, a **nie** od tego, jak dłużnik został opisany w nakazie zapłaty (NZ) i klauzuli wykonalności.

---

### 1. Dlaczego brak wzmianki o działalności gospodarczej w NZ i wpisanie PESEL nie zmieniają sytuacji wierzyciela?

1. **Status JDG w procesie cywilnym:** Osoba fizyczna prowadząca jednoosobową działalność gospodarczą nie posiada odrębnej od tej osoby podmiotowości prawnej. Stroną procesową i dłużnikiem jest zawsze osoba fizyczna, dlatego sądy prawidłowo oznaczają ją w nakazie zapłaty samym imieniem i nazwiskiem (bez dopisku „prowadzący działalność gospodarczą pod firmą...”), a w klauzuli wykonalności – zgodnie z art. 783 § 1 k.p.c. – wpisują jej numer PESEL.
2. **Brak „automatycznej” klauzuli przy długach prywatnych:** Sam fakt, że z treści nakazu zapłaty oraz klauzuli nie wynika gospodarczy charakter sprawy (przez co tytuł wygląda jak wydany w sprawie „prywatnej/konsumenckiej”), **nie daje wierzycielowi prawa do łatwiejszego uzyskania klauzuli przeciwko małżonkowi**. Jest wręcz odwrotnie: od nowelizacji KRO i KPC z 2005 r. przy długach niezwiązanych z prowadzeniem przedsiębiorstwa uzyskanie klauzuli na małżonka bez jego udokumentowanej zgody jest **całkowicie niemożliwe**.

---

### 2. Kiedy można wnieść o klauzulę w trybie art. 787 k.p.c. (bez ograniczenia do przedsiębiorstwa)?

Warto pamiętać, że nawet w trybie „normalnym” (art. 787 k.p.c.) klauzula na małżonka nigdy nie jest nadawana „bez żadnych ograniczeń” – sąd zawsze ogranicza odpowiedzialność małżonka do **majątku objętego wspólnością majątkową** (małżonek nie odpowiada swoim majątkiem osobistym). Jest to jednak zakres znacznie szerszy niż w art. 787¹ k.p.c., ponieważ pozwala prowadzić egzekucję np. z prywatnej nieruchomości czy ruchomości należących do majątku wspólnego małżonków, a nie tylko ze składników firmy.

Zależnie od posiadanych dokumentów występują dwie sytuacje:

#### Sytuacja A: Wierzyciel POSIADA dokument wykazujący zgodę małżonka dłużnika
Jeżeli wierzyciel dysponuje dokumentem urzędowym lub prywatnym (np. podpisem małżonka pod umową, osobnym pisemnym oświadczeniem małżonka o wyrażeniu zgody na zaciągnięcie zobowiązania), **może złożyć wniosek w trybie art. 787 k.p.c. (w zw. z art. 41 § 1 k.r.o.) o nadanie klauzuli z ograniczeniem do całego majątku wspólnego**.
* Gospodarczy charakter pozwu nie stanowi tu żadnej przeszkody – art. 787 k.p.c. ma zastosowanie do każdej czynności prawnej dokonanej za zgodą małżonka, również tej związanej z prowadzeniem działalności gospodarczej.

#### Sytuacja B: Wierzyciel NIE POSIADA dokumentu wykazującego zgodę małżonka dłużnika
Jeżeli wierzyciel nie ma pisemnej zgody małżonka (dokumentu prywatnego lub urzędowego), **wniosek złożony w trybie art. 787 k.p.c. zostanie przez sąd oddalony**.
* Zgodnie z uchwałą Sądu Najwyższego z dnia 18 marca 2011 r. (**III CZP 117/10**), w postępowaniu klauzulowym z art. 787 k.p.c. niedopuszczalne jest stosowanie domniemań faktycznych co do zgody małżonka – musi ona wynikać wprost z przedłożonego dokumentu.
* W takiej sytuacji jedyną szansą na uzyskanie jakiejkolwiek klauzuli przeciwko małżonkowi jest właśnie tryb **art. 787¹ k.p.c. (w zw. z art. 41 § 2 *in fine* k.r.o.)**, czyli z ograniczeniem odpowiedzialności małżonka do przedsiębiorstwa wchodzącego w skład majątku wspólnego.
* **Ważne:** Brak wzmianki o działalności gospodarczej w nakazie zapłaty oraz obecność numeru PESEL w klauzuli **nie przeszkadzają** w uzyskaniu klauzuli z art. 787¹ k.p.c. Fakt, że wierzytelność powstała w związku z prowadzeniem przedsiębiorstwa, wykazuje się we wniosku klauzulowym za pomocą dokumentów (np. umowy, faktur VAT, zamówień oraz wydruku z CEIDG dłużnika).

---

### 3. Jak sięgnąć do majątku wspólnego „poza przedsiębiorstwem”, gdy brak pisemnej zgody małżonka?

Jeżeli w Państwa sprawie wierzyciel nie posiada pisemnej zgody małżonka, a zależy mu na zaspokojeniu się ze składników majątku wspólnego niewchodzących w skład przedsiębiorstwa (np. wspólny dom/mieszkanie małżonków), istnieją trzy rozwiązania praktyczne:

1. **Wykorzystanie obecnego tytułu wykonawczego przeciwko samemu dłużnikowi (bez klauzuli na małżonka):**
   * **Art. 776¹ § 1 k.p.c.:** Tytuł wykonawczy wystawiony wyłącznie przeciwko dłużnikowi pozwala prowadzić egzekucję nie tylko z jego majątku osobistego, ale także z pobranego przez niego wynagrodzenia za pracę oraz **dochodów uzyskanych z innej działalności zarobkowej** (w tym z działalności gospodarczej), które formalnie wchodzą do majątku wspólnego.
   * **Art. 891² § 1 k.p.c.:** Tytuł przeciwko samemu dłużnikowi pozwala na zajęcie i egzekucję z **rachunku wspólnego** dłużnika i jego małżonka.
   * **Art. 845 § 2⁴ k.p.c. oraz art. 923¹ § 1 k.p.c.:** Tytuł przeciwko samemu dłużnikowi stanowi podstawę do **zajęcia** ruchomości oraz nieruchomości wchodzących w skład majątku wspólnego (choć do dalszych czynności egzekucyjnych po zajęciu wymagana już będzie klauzula przeciwko małżonkowi).

2. **Powództwo o ustanowienie przymusowej rozdzielności majątkowej (art. 52 § 1a k.r.o.):**
   * Jest to podstawowy instrument pozwalający „obejść” brak zgody z art. 787 k.p.c. oraz ograniczenie do przedsiębiorstwa z art. 787¹ k.p.c.
   * Wierzyciel jednego z małżonków może żądać ustanowienia przez sąd rozdzielności majątkowej, jeżeli uprawdopodobni, że zaspokojenie wierzytelności stwierdzonej tytułem wykonawczym wymaga dokonania podziału majątku wspólnego małżonków (np. egzekucja z majątku osobistego dłużnika i jego przedsiębiorstwa okazała się bezskuteczna).
   * Po prawomocnym ustanowieniu rozdzielności majątkowej małżonkowie stają się współwłaścicielami w częściach ułamkowych (z reguły po 1/2), a wierzyciel – na podstawie dotychczasowego tytułu wykonawczego z numerem PESEL dłużnika, **bez żadnej klauzuli na małżonka** – może skierować egzekucję bezpośrednio do udziału dłużnika (1/2) np. we wspólnej nieruchomości.

3. **Odrębne powództwo przeciwko małżonkowi (gdy zgoda była wyrażona ustnie lub dorozumianie):**
   * Jeżeli małżonek dłużnika faktycznie wyraził zgodę na zaciągnięcie zobowiązania, ale wierzyciel nie ma na to dokumentu wymaganego w art. 787 k.p.c., zgodnie z uchwałą Sądu Najwyższego z dnia 11 kwietnia 2019 r. (**III CZP 106/18**) wierzyciel może wytoczyć przeciwko małżonkowi dłużnika powództwo o zapłatę na podstawie art. 41 § 1 k.r.o. (z ograniczeniem odpowiedzialności do majątku wspólnego w trybie art. 319 k.p.c.). W zwykłym procesie fakt udzielenia zgody można udowadniać wszelkimi środkami dowodowymi (np. zeznaniami świadków lub przesłuchaniem stron).

---

### Źródła
1. [arslege.pl - Art. 787 KPC](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHhylMmuIg42iYdtP1uln0J3SI6ixgKIaQlbuBKmDNyDcCcrt3u0xpyzYHzO3AzE8bM4zangL-lZaiyyTS3Fr1w68HgWSTax-sRMxl_jIwPtJyYCH8Jdr_KGVpo4psaA9HCqzZUIyb7HKCfbfjwYm1rjQBKAlYEqwThEMIDQnMH05c57spYZ4eAvstvInT0YscjynvWvgxNH_LTHmkzg5AifDXXvQ5pe4yMkxsw9Kkd2PSuV9wnsGfWmhoKGM9XD_wx_kjKHl1G0TqQlbIGVif7rUo=)
2. [poradnikprzedsiebiorcy.pl - Klauzula wykonalności przeciwko małżonkowi dłużnika (art. 787 i 787¹ KPC)](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHWruYpFH8qVzxXs6h2XLqVR58Mciq6q2YbikiQQr3V7alcEiToDblzExUNJ1dnPSyy-wcz0rbO-l6rFPe_UHhliD1UxZWuJ99YZL13IhApdRIX6TG7ucirWHRS-cJwe72Cw0XSqUSTxh50f9XUizolUq0szO6JWjqZnozNv3Y4eRIXA-8WcpwcFi_JiLCFmA==)
3. [krakow.sa.gov.pl - Orzecznictwo dot. art. 787 i 787¹ KPC oraz uchwały SN III CZP 117/10](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHGyjVI0BH3AqN3n3Xgnv5NZZHflhDQost2HUBpkVDWAzXM7RYkZwOIfJQwhYNc4exXH4VNH0LhLOo_yx-sEveRZ0du8nNOxRvDNIH83llLNtyHBA6AkzT2ZtsTU0Uvd3YOiLu93D2VmHw6itdFyCYk_wtJD4fiduNw96v-7buXs_ZiiR7_j-OgY64Lc1rhL3-09wDh7AzkEOEvZQ2P)
4. [blochkancelaria.pl - Uchwała SN z 11 kwietnia 2019 r., sygn. akt III CZP 106/18](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFepzMf1FtDBeFFspUfzTGd7JOyDtys28sR38I5oJMiLrrnVOOZQBNy_R-xFj4BCwqohlBD3mbJbryae-E0fX2pucHKuXSX75ifnT3vbh6QArkHH1KVpaHAwXYYEP7Mw4Um6Wp-ZKd-cjqV3WVXgAaB5mFq5D6kplT4rQ5CNXd22xaiWoyISzZgAGgvSeLp4yUILb8hI2s3odR7FJ4lZOnEwl8kwNUrZloBJup-2LDkTzbpCk7-1xnbiW1lBgbDJlVtseLX)
5. [mckancelaria.pl - Egzekucja przeciwko małżonkowi i przymusowa rozdzielność majątkowa](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEtimsAaJy98ZET3MTPj_El-Mr3wOciQgHO_Rrrln2pFekPHmHAqiJKjPTrY9PrIWgzFO0b5ZGFhvej-MgjkrwOcgyUqM113M1WdyFCMZYpu-TXjB8Qbd_lESuirfl7oU99U0kai6ZQjNAKNr50UOSnsGJjC5iSuF02uGJsgnBAqkA5WyJViGKPKkDyLvGuXA==)
6. [i-rs.pl - Egzekucja z majątku wspólnego małżonków (art. 776¹, 787, 787¹ KPC)](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHaYd26V10-Bwlq7ACUz-cxppoaqwrCxYtiE7ACS8cfIGdvyglB4FpKyZ2LI1GoOq-gCyHALNaWjE3qtyOAtLPTc8QpbGeYHehEiMpRKRTCiKGCZMJaci2I90VY-DHQBAN8dQUiIMMsnFQ5ONthxZ3FMFPW)
