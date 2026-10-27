---
pytanie: P08
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
zapytania:
- AI Act definicja deepfake art 3 rozporządzenie 2024 1689
- '"deep fake" "rozporządzenie 2024/1689" art 3'
zrodla:
- academicon.pl
- prostetorodo.pl
- skpipblog.pl
- kancelaria-skarbiec.pl
- parp.gov.pl
data_odpowiedzi: '2026-10-18'
czas_s: 23.6
tokeny:
  wejscie: 139
  wyjscie: 886
  rozumowanie: 1790
blad: null
---

**Tak, to stwierdzenie jest prawdziwe na gruncie unijnego Aktu o sztucznej inteligencji (AI Act)**.

### Podstawa prawna i analiza definicji

Kwestię tę reguluje **art. 3 pkt 60** Rozporządzenia Parlamentu Europejskiego i Rady (UE) 2024/1689 z dnia 13 czerwca 2024 r. w sprawie ustanowienia zharmonizowanych przepisów dotyczących sztucznej inteligencji (AI Act). Zgodnie z tą definicją legalną:

> *„deep fake” oznacza wygenerowane przez AI lub zmanipulowane przez AI obrazy, treści dźwiękowe lub treści wideo, które **przypominają istniejące osoby, obiekty, miejsca, podmioty lub zdarzenia** i które dla danej osoby **mogłyby niesłusznie sprawiać wrażenie autentycznych lub prawdziwych***.

Aby dana treść audio została zakwalifikowana jako deepfake, muszą zostać spełnione łącznie określone przesłanki:
1. **Generowanie lub manipulacja przez AI** (kryterium techniczne).
2. **Podobieństwo do realnego świata** – treść musi przypominać istniejącą osobę (np. sklonowany głos konkretnego aktora, polityka czy znajomego) bądź istniejące zdarzenie.
3. **Potencjał do wprowadzenia w błąd** – materiał musi obiektywnie stwarzać fałszywe pozory autentyczności (odbiorca mógłby niesłusznie uznać, że słyszy nagranie rzeczywistego człowieka lub realnego wydarzenia).

Jeżeli zatem głos został wygenerowany sztucznie od zera, **nie naśladuje głosu żadnej istniejącej osoby fizycznej** i **nie wprowadza w błąd** (nie udaje prawdziwego nagrania ani nikogo nie podszywa), to **nie stanowi treści typu *deepfake*** w rozumieniu AI Act. W konsekwencji podmiot stosujący taki głos nie podlega rygorowi z art. 50 ust. 4 AI Act (obowiązek wyraźnego oznaczania deepfake’ów wobec odbiorców).

---

### Istotne zastrzeżenie: Inne obowiązki wynikające z AI Act

Fakt, że syntetyczny głos nie jest *deepfake'em*, nie oznacza, że pozostaje zupełnie poza regulacją AI Act. Należy odróżnić pojęcie *deepfake* od pojęcia ogólnych *treści generowanych przez AI*:

1. **Obowiązek znakowania technicznego (art. 50 ust. 2 AI Act):** Dostawcy systemów AI generujących treści audio mają obowiązek zapewnić, aby wyniki były oznaczane w formacie nadającym się do odczytu maszynowego i wykrywalne jako sztucznie wygenerowane (np. poprzez metadane lub cyfrowe znaki wodne).
2. **Systemy wchodzące w bezpośrednią interakcję (art. 50 ust. 1 AI Act):** Jeżeli taki syntetyczny głos jest używany np. w voicebocie obsługującym infolinię do rozmowy z klientami, podmiot stosujący ma obowiązek poinformować człowieka, że wchodzi w interakcję z systemem AI (chyba że wynika to wprost z okoliczności i kontekstu użycia).
