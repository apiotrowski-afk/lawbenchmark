---
pytanie: P12
system: 'OpenAI gpt-6.1-sol przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie
  na żywo'
model: gpt-6.1-sol
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-10'
czas_s: 56.2
tokeny:
  input_tokens: 100563
  cached_input_tokens: 62976
  cache_write_input_tokens: 0
  output_tokens: 1693
  reasoning_output_tokens: 72
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
  zapytanie: art 787 7871 kpc małżonek przedsiębiorstwo zgoda małżonka klauzula wykonalności
    ...
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: site.eli.gov.pl kodeks rodzinny opiekuńczy 2026 41 ...
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: '"7761" "Tytuł wykonawczy wystawiony" "wynagrodzenia" ...'
  polecenie: null
  narzedzie: null
blad: null
---

## Pytanie

Klauzula wykonalności na małżonka, pozew był związany z działalnością gospodarczą, ale w NZ nie ma nic na temat "prowadzący działalnosc" w klauzuli jest PESEL i nie ma żadnej wzmianki nt. dzialalności, czy można wnosić o klauzulę na małżonka w "normalnym trybie'? tj. czy można wnieść o egzkeucję "bez ograniczeń", które wynikają z 781[1] k.p.c. ?

## Odpowiedź

**Można wystąpić o klauzulę przeciwko małżonkowi na podstawie art. 787 k.p.c. także przy długu związanym z działalnością gospodarczą — ale trzeba wykazać dokumentem zgodę małżonka na czynność prawną, z której wynika dług. Sam brak wzmianki o działalności w nakazie zapłaty i klauzuli nie pozwala uzyskać szerszej egzekucji.**

Zakładam, że „NZ” oznacza nakaz zapłaty, wydany wyłącznie przeciwko jednemu z małżonków, prowadzącemu jednoosobową działalność.

W pytaniu zapewne chodzi o **art. 787¹ k.p.c.**, a nie art. 781¹ k.p.c. Ten ostatni dotyczy terminu rozpoznania wniosku klauzulowego.

Rozróżnienie jest następujące:

- **Art. 787 k.p.c. w zw. z art. 41 § 1 k.r.o.** pozwala uzyskać klauzulę przeciwko małżonkowi **z ograniczeniem odpowiedzialności do całego majątku objętego wspólnością majątkową**. Wierzyciel musi wykazać dokumentem urzędowym lub prywatnym, że wierzytelność powstała z czynności prawnej dokonanej za zgodą małżonka. Gospodarczy charakter długu nie wyklucza tej podstawy.
- **Art. 787¹ k.p.c. w zw. z art. 41 § 2 k.r.o.** pozwala uzyskać klauzulę **z ograniczeniem odpowiedzialności do przedsiębiorstwa wchodzącego w skład majątku wspólnego**. Nie wymaga wykazania zgody małżonka, lecz wymaga udokumentowania związku wierzytelności z prowadzeniem przedsiębiorstwa. [K.p.c.](https://eli.gov.pl/eli/DU/2026/468/ogl), [k.r.o.](https://eli.gov.pl/eli/DU/2026/236/ogl).

**PESEL i brak dopisku „prowadzący działalność gospodarczą” nie rozstrzygają o wyborze podstawy.** Przedsiębiorca prowadzący jednoosobową działalność jest tą samą osobą fizyczną. Istotne są źródło wierzytelności i dokumenty potwierdzające przesłanki rozszerzenia klauzuli, a nie samo oznaczenie pozwanego w nakazie.

Jeżeli macie np. podpisaną przez małżonka zgodę na zawarcie umowy, z której wynika zasądzona należność, można żądać klauzuli na podstawie art. 787 k.p.c. **Sama wiedza małżonka o działalności, tolerowanie jej czy korzystanie z dochodów nie zastępują udokumentowanej zgody na czynność będącą źródłem długu.** SN w uchwale z 18 marca 2011 r., III CZP 117/10, wykluczył ustalanie tej zgody na podstawie domniemania faktycznego w postępowaniu klauzulowym. [Uchwała SN](https://www.sn.pl/sites/orzecznictwo/Orzeczenia1/III%20CZP%20117-10.pdf).

Zatem odpowiedź na „bez ograniczeń” zależy od znaczenia tego sformułowania:

- **Poza przedsiębiorstwem, do pozostałego majątku wspólnego — tak**, jeżeli spełnione są przesłanki art. 787 k.p.c.
- **Do majątku osobistego drugiego małżonka — nie**, na podstawie samego rozszerzenia klauzuli z art. 787 lub 787¹ k.p.c. Potrzebna byłaby odrębna podstawa jego osobistej odpowiedzialności i odpowiedni tytuł przeciwko niemu.

Praktycznie wniosek z art. 787 k.p.c. powinien żądać nadania klauzuli przeciwko małżonkowi **„z ograniczeniem jego odpowiedzialności do majątku objętego wspólnością majątkową”**, a nie klauzuli „bez ograniczeń”. Jeżeli nie ma dokumentu wykazującego zgodę, opisany brak wzmianki o działalności nie pozwoli obejść ograniczenia z art. 787¹ k.p.c.

Powyższe dotyczy obecnego reżimu odpowiedzialności; przy zobowiązaniu powstałym przed 20 stycznia 2005 r. trzeba sprawdzić przepisy przejściowe. W opisanej krajowej sprawie prawo UE nie zmienia tego rozróżnienia.

Źródła: [Kodeks postępowania cywilnego](https://eli.gov.pl/eli/DU/2026/468/ogl), [Kodeks rodzinny i opiekuńczy](https://eli.gov.pl/eli/DU/2026/236/ogl), [SN, III CZP 117/10](https://www.sn.pl/sites/orzecznictwo/Orzeczenia1/III%20CZP%20117-10.pdf), [ustawa nowelizująca z 17 czerwca 2004 r.](https://eli.gov.pl/api/acts/DU/2004/1691/text.html).
