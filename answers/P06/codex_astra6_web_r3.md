---
pytanie: P06
system: 'OpenAI gpt-6-astra przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie
  na żywo'
model: gpt-6-astra
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-17'
czas_s: 53.9
tokeny:
  input_tokens: 142277
  cached_input_tokens: 115328
  cache_write_input_tokens: 0
  output_tokens: 1244
  reasoning_output_tokens: 13
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
  zapytanie: '"3942" "odrzucenie zażalenia" sąd drugiej instancji ...'
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: site.sn.pl "odrzuceniu zażalenia" "3942" "2024" ...
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: https://eli.gov.pl/api/acts/DU/2024/1568/text.html
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: '"art. 394" "§ 1²" "nieopłacone" "2026" ...'
  polecenie: null
  narzedzie: null
blad: null
---

## Pytanie

Postanowienie o odrzuceniu zażalenia (SA) - brak opłaty, czy przysługuje zażalenie ?

## Odpowiedź

**Co do zasady nie — jeżeli chodzi o postępowanie cywilne i SA działający jako sąd drugiej instancji.** Na jego postanowienie o odrzuceniu zażalenia z powodu nieuiszczenia opłaty nie przysługuje kolejne zażalenie. Sam powód odrzucenia nie zmienia zasad zaskarżalności.

Podstawy prawne:

- **Art. 394² § 1 i § 1¹ k.p.c.** określają katalog postanowień sądu drugiej instancji zaskarżalnych do innego składu tego sądu. Katalog obejmuje odrzucenie **apelacji**, ale nie odrzucenie **zażalenia**.
- **Art. 394¹a § 1 pkt 12 k.p.c.** przewiduje zażalenie na odrzucenie zażalenia, jednak dotyczy postanowień **sądu pierwszej instancji**.
- **Art. 394¹ § 1 i § 1¹ k.p.c.** nie przewidują w opisanej sytuacji zażalenia do Sądu Najwyższego. [K.p.c.](https://eli.gov.pl/api/acts/DU/2024/1568/text.html)

Taką wykładnię wspiera **uchwała SN z 23 czerwca 2022 r., III CZP 50/22**: SN wykluczył zażalenie na odrzucenie zażalenia przez sąd drugiej instancji. Uchwała dotyczyła postępowania upadłościowego, ale jej argumentacja odnosi się do konstrukcji art. 394² k.p.c. [Uchwała SN](https://www.sn.pl/sites/orzecznictwo/orzeczenia3/iii%20czp%2050-22-1.pdf)

**Praktycznie:** jeżeli termin do uiszczenia opłaty został uchybiony bez winy strony, można rozważyć **wniosek o przywrócenie terminu** — art. 168 § 1 oraz art. 169 § 1–3 k.p.c. Należy go złożyć w ciągu tygodnia od ustania przyczyny uchybienia, uprawdopodobnić brak winy i jednocześnie uiścić opłatę. To odrębny środek, a nie zażalenie na odrzucenie. [K.p.c.](https://eli.gov.pl/api/acts/DU/2024/1568/text.html)

Do ostatecznej oceny potrzebne są **data postanowienia i informacja, czego dotyczyło odrzucone zażalenie** — zwłaszcza czy było skierowane do SA, innego składu SA czy SN.

Źródła: [Kodeks postępowania cywilnego — ELI](https://eli.gov.pl/api/acts/DU/2024/1568/text.html), [SN, III CZP 50/22 — pełny tekst](https://www.sn.pl/sites/orzecznictwo/orzeczenia3/iii%20czp%2050-22-1.pdf).
