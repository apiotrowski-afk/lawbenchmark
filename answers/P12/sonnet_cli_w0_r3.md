---
pytanie: P12
system: Claude claude-sonnet-5-5 przez Claude Code CLI (subskrypcja), czysty model
  — bez narzędzi, MCP i CLAUDE.md, W0
model_alias: claude-sonnet-5-5
model_id: claude-haiku-5-5,claude-sonnet-5-5
prompt_systemowy: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po
  polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne.
narzedzia: []
wyszukiwanie: false
temperatura: domyślna CLI (nieustawialna)
kontekst_dodatkowy: sekcja środowiska Claude Code (katalog tymczasowy, data, platforma,
  e-mail konta) — nie da się wyłączyć
data_odpowiedzi: '2026-10-10'
czas_s: 69.2
tokeny:
  input_tokens: 2
  cache_creation_input_tokens: 949
  cache_read_input_tokens: 0
  output_tokens: 10214
  output_tokens_details:
    thinking_tokens: 8117
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 949
    ephemeral_5m_input_tokens: 0
  inference_geo: global
  iterations:
  - input_tokens: 2
    output_tokens: 10214
    cache_read_input_tokens: 0
    cache_creation_input_tokens: 949
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 949
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.10620650000000001
blad: null
---

**Zastrzeżenie:** nie mam pewności co do numeracji przepisu, który Pan/Pani oznaczył(a) jako „781¹". Klauzulę wykonalności przeciwko małżonkowi dłużnika regulują art. 787 k.p.c. oraz art. 787¹ k.p.c. (do weryfikacji w aktualnym brzmieniu, bo art. 781 k.p.c. dotyczy czego innego). Poniżej opieram się na konstrukcji obu tych przepisów. Warto sprawdzić ich dokładne brzmienie przed złożeniem wniosku.

## 1. Krótka odpowiedź

Tak, można wnosić o klauzulę przeciwko małżonkowi w trybie ogólnym (art. 787 k.p.c.), a nie w trybie szczególnym dla długów związanych z działalnością gospodarczą. Nie oznacza to jednak egzekucji „bez ograniczeń":

- w trybie ogólnym klauzula zawsze jest nadawana z ograniczeniem odpowiedzialności małżonka do majątku objętego wspólnością majątkową (nie odpowiada on majątkiem osobistym),
- wierzyciel musi sprostać wymogom dowodowym, które w trybie szczególnym (działalność gospodarcza) są łagodniejsze albo inne.

## 2. Tryb ogólny (art. 787 k.p.c.)

Sąd nadaje klauzulę przeciwko małżonkowi dłużnika, jeżeli wierzyciel wykaże **dokumentem urzędowym albo dokumentem prywatnym z podpisem urzędowo poświadczonym**, że:

- dług powstał w czasie trwania wspólności ustawowej, oraz
- zachodzą przesłanki z art. 41 k.r.o., tj. dług powstał z czynności prawnej dokonanej za zgodą małżonka (art. 41 § 1 k.r.o.). Bez zgody egzekucja z majątku wspólnego jest ograniczona do składników wskazanych w art. 41 § 2 k.r.o. (m.in. wynagrodzenie za pracę, dochody z innej działalności zarobkowej, dochody z majątku odrębnego dłużnika).

Brak wzmianki o działalności gospodarczej w nakazie zapłaty ani w klauzuli nie stoi na przeszkodzie wnioskowi w tym trybie, bo przesłanki trybu ogólnego nie zależą od oznaczenia dłużnika jako przedsiębiorcy. Ograniczenie wynikające z trybu szczególnego dotyczy tylko sytuacji, w której wierzyciel z niego korzysta.

## 3. Czego tryb ogólny nie daje

Skoro w tytule nie ma oznaczenia dłużnika jako prowadzącego działalność, wierzyciel nie skorzysta z uproszczeń trybu szczególnego. Nie można też uzyskać klauzuli przeciwko małżonkowi „w całości" ani z odpowiedzialnością majątkiem osobistym. Nadanie klauzuli przeciwko małżonkowi nie czyni go dłużnikiem osobistym, bo nie jest stroną tytułu. Odpowiada on jedynie z majątku wspólnego.

## 4. Problem praktyczny: dowody

Kluczowa trudność to wymóg dokumentu urzędowego lub prywatnego z podpisem poświadczonym. Pozew związany z działalnością gospodarczą nie zastępuje tego dokumentu. Trzeba więc wykazać:

- datę powstania długu (np. umowa z poświadczonym podpisem, faktura nie wystarczy),
- istnienie wspólności ustawowej w tym czasie (np. odpis aktu małżeństwa, brak intercyzy),
- zgodę małżonka, jeśli wierzyciel chce objąć cały majątek wspólny.

Jeżeli takich dokumentów nie ma, sąd oddali wniosek (art. 787 k.p.c.). Wówczas pozostaje droga procesowa, czyli pozew o ustalenie lub o nadanie klauzuli w drodze powództwa (do rozważenia w oparciu o art. 189 k.p.c. oraz orzecznictwo SN dotyczące wąskiego zakresu takich powództw).

## 5. Środki zaskarżenia i ochrona małżonka

- Małżonek może zaskarżyć postanowienie o nadaniu klauzuli zażaleniem (art. 795 § 1 k.p.c.).
- Może też wnieść powództwo przeciwegzekucyjne (art. 840 k.p.c.), podnosząc m.in., że dług nie obciąża majątku wspólnego.
- W razie egzekucji z majątku objętego klauzulą ma on dodatkowo środki z art. 841 k.p.c. (powództwo ekscydencyjne), jeśli egzekucja dotknęła majątku osobistego.

## 6. Rekomendacja

1. Zweryfikować aktualne brzmienie art. 787 i 787¹ k.p.c. oraz art. 41 k.r.o.
2. Ocenić, czy dysponujemy dokumentami z pkt 4. Jeśli tak, wnosić o klauzulę w trybie ogólnym, z wyraźnym wskazaniem, że wniosek opiera się na art. 787 k.p.c. (a nie na przepisie dotyczącym długów z działalności gospodarczej).
3. Jeśli dokumentów brakuje, rozważyć powództwo o ustalenie albo zgromadzenie brakujących dowodów, zanim złożymy wniosek, aby uniknąć oddalenia i kosztów.

Mogę przygotować projekt wniosku o nadanie klauzuli przeciwko małżonkowi, jeśli prześle Pan/Pani nakaz zapłaty i posiadane dokumenty potwierdzające powstanie długu.
