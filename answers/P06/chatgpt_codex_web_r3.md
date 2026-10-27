---
pytanie: P06
system: 'OpenAI gpt-6.1-sol przez Codex CLI (rozumowanie: medium), wariant A: wyszukiwanie
  na żywo'
model: gpt-6.1-sol
wysilek_rozumowania: medium
data_odpowiedzi: '2026-10-10'
czas_s: 84.9
tokeny:
  input_tokens: 339257
  cached_input_tokens: 271104
  cache_write_input_tokens: 0
  output_tokens: 1629
  reasoning_output_tokens: 110
wstep: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, na
  gruncie prawa polskiego i unijnego, podając podstawy prawne. Odpowiedz bezpośrednio
  w wiadomości — nie twórz plików i nie uruchamiaj poleceń. Możesz korzystać z wyszukiwania
  w internecie; jeśli z niego korzystasz, na końcu podaj adresy źródeł.
sandbox: read-only, pusty katalog, sesja nietrwała
aplikacje_chatgpt: wyłączone (features.apps=false)
liczba_wyszukan: 16
inne_narzedzia: 0
zdarzenia:
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: art. 3942 odrzucenie zażalenia sąd drugiej instancji zażalenie brak opłaty
    2026 ...
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
  zapytanie: '"3942" "odrzucenie zażalenia" "§ 1" ...'
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU20240001568/U/D20241568Lj.pdf
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: site.sn.pl "III CZP 50/22" "nie przysługuje" ...
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: '''Art. 3942.'''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: '"3942" "Na postanowienie przysługuje zażalenie" "2025" ...'
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: ''
  polecenie: null
  narzedzie: null
- typ: web_search
  zapytanie: '""Na postanowienie przysługuje zażalenie do innego składu sądu drugiej
    instancji""  ...'
  polecenie: null
  narzedzie: null
blad: null
---

## Pytanie

Postanowienie o odrzuceniu zażalenia (SA) - brak opłaty, czy przysługuje zażalenie ?

## Odpowiedź

**Tak — jeżeli SA odrzucił zażalenie poziome na własne postanowienie. Jeżeli odrzucił zażalenie na postanowienie sądu I instancji, co do zasady nie.** Zakładam, że chodzi o postępowanie cywilne.

Rozróżnienie wynika z **art. 394² § 1² k.p.c.**: odrzucenie jako nieopłaconego zażalenia wymienionego w § 1 lub § 1¹ tego artykułu podlega zażaleniu do **innego składu sądu drugiej instancji**. Dotyczy to np. zażalenia na postanowienie SA o odrzuceniu apelacji albo odmowie zwolnienia od kosztów sądowych. Termin wynosi **tydzień od doręczenia postanowienia z uzasadnieniem** — art. 394 § 2 w zw. z art. 394² § 2 k.p.c. [K.p.c.](https://eli.gov.pl/api/acts/DU/2024/1568/text/U/D20241568Lj.pdf)

Natomiast odrzucenie przez SA zażalenia skierowanego przeciwko postanowieniu sądu I instancji nie jest objęte tym przepisem. Sama przyczyna odrzucenia — brak opłaty — nie tworzy prawa do kolejnego zażalenia. Zamknięty charakter katalogu podkreślono również w uchwale SN z 23 czerwca 2022 r., **III CZP 50/22**, wydanej na tle postępowania upadłościowego. [Uchwała SN](https://www.sn.pl/sites/orzecznictwo/orzeczenia3/iii%20czp%2050-22-1.pdf)

**Na jakie postanowienie wniesiono odrzucone zażalenie i kiedy SA wydał postanowienie o jego odrzuceniu?** Te informacje pozwolą wskazać jednoznaczną odpowiedź dla sprawy.

Źródła: [tekst k.p.c.](https://eli.gov.pl/api/acts/DU/2024/1568/text/U/D20241568Lj.pdf), [uchwała III CZP 50/22](https://www.sn.pl/sites/orzecznictwo/orzeczenia3/iii%20czp%2050-22-1.pdf).
