---
pytanie: P05
system: Claude opus przez Claude Code CLI (subskrypcja), czysty model — bez narzędzi,
  MCP i CLAUDE.md, W0
model_alias: opus
model_id: claude-haiku-5-5,claude-opus-5-5
prompt_systemowy: Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po
  polsku, na gruncie prawa polskiego i unijnego, podając podstawy prawne.
narzedzia: []
wyszukiwanie: false
temperatura: domyślna CLI (nieustawialna)
kontekst_dodatkowy: sekcja środowiska Claude Code (katalog tymczasowy, data, platforma,
  e-mail konta) — nie da się wyłączyć
data_odpowiedzi: '2026-10-10'
czas_s: 39.1
tokeny:
  input_tokens: 2
  cache_creation_input_tokens: 814
  cache_read_input_tokens: 0
  output_tokens: 3725
  output_tokens_details:
    thinking_tokens: 1683
  server_tool_use:
    web_search_requests: 0
    web_fetch_requests: 0
  service_tier: standard
  cache_creation:
    ephemeral_1h_input_tokens: 814
    ephemeral_5m_input_tokens: 0
  inference_geo: not_available
  iterations:
  - input_tokens: 2
    output_tokens: 3725
    cache_read_input_tokens: 0
    cache_creation_input_tokens: 814
    cache_creation:
      ephemeral_5m_input_tokens: 0
      ephemeral_1h_input_tokens: 814
    type: message
  speed: standard
  fallback_credit: null
koszt_usd_rownowaznik: 0.08123409999999999
blad: null
---

# Doręczanie pism sądowych osobie fizycznej przez Portal Informacyjny (postępowanie cywilne)

> **Zastrzeżenie:** przepisy o Portalu Informacyjnym kilkakrotnie nowelizowano (m.in. ustawą z 7 lipca 2023 r., Dz.U. 2023 poz. 1860). Przed wykorzystaniem w sprawie sprawdź w ISAP lub LEX aktualną numerację paragrafów art. 131¹ k.p.c. i rozporządzenia wykonawczego.

## 1. Zasada: dla osoby fizycznej to doręczenie fakultatywne

Obowiązkowe doręczenie przez portal (art. 131¹ k.p.c.) dotyczy podmiotów profesjonalnych: adwokatów, radców prawnych, rzeczników patentowych, Prokuratorii Generalnej RP, komorników i prokuratorów.

Osobie fizycznej działającej samodzielnie sąd doręcza przez portal tylko wtedy, gdy **sama wybrała ten sposób doręczeń**. Bez takiego wyboru stosuje się tryb tradycyjny: pocztę, doręczenie przez sąd lub przez komornika (art. 131 i nast. k.p.c.).

Jeśli osoba fizyczna ma profesjonalnego pełnomocnika, pisma doręcza się pełnomocnikowi (art. 133 § 3 k.p.c.), a więc przez portal obowiązkowo.

## 2. Warunki skorzystania z portalu

1. **Konto na Portalu Informacyjnym Sądów Powszechnych** (portal.wroclaw.sa.gov.pl, obecnie jeden portal dla wszystkich sądów powszechnych). Konto wymaga weryfikacji tożsamości, w praktyce przez login.gov.pl (profil zaufany, e-dowód, bankowość elektroniczna) albo osobiście w sądzie.
2. **Dostęp do konkretnej sprawy.** Konto musi być powiązane ze sprawą, w której osoba jest stroną lub uczestnikiem.
3. **Oświadczenie o wyborze doręczeń przez portal**, złożone w sprawie, np. w piśmie procesowym lub przez funkcję portalu.

Wybór można co do zasady odwołać. Pisma doręcza się wtedy ponownie w trybie tradycyjnym.

## 3. Jak przebiega doręczenie

- Sąd umieszcza pismo na portalu, w zakładce danej sprawy.
- System wysyła powiadomienie e-mailem (ewentualnie SMS-em). **Powiadomienie ma charakter wyłącznie informacyjny** i nie wpływa na datę doręczenia ani na bieg terminów.
- Doręczenie potwierdza elektroniczne potwierdzenie odbioru, generowane przez system.

## 4. Chwila doręczenia (art. 131¹ k.p.c.)

| Sytuacja | Data doręczenia |
|---|---|
| Adresat otworzył (odebrał) pismo na portalu | data wskazana w elektronicznym potwierdzeniu odbioru, czyli dzień otwarcia |
| Adresat nie otworzył pisma | **fikcja doręczenia** z upływem **14 dni** od dnia umieszczenia pisma na portalu |

**Wniosek praktyczny:** od tej daty biegną terminy procesowe, np. na apelację czy zażalenie. Osoba, która wybrała portal i go nie sprawdza, ryzykuje uprawomocnienie się orzeczenia.

## 5. Wyjątki: kiedy sąd doręczy tradycyjnie mimo wyboru portalu

- charakter pisma uniemożliwia doręczenie elektroniczne (np. oryginały dokumentów, niektóre załączniki);
- występuje przeszkoda techniczna po stronie systemu sądowego.

Jeśli trwała awaria portalu uniemożliwiła odbiór, właściwym środkiem jest **wniosek o przywrócenie terminu** (art. 168–172 k.p.c.). Należy wtedy wykazać brak winy, np. komunikatem o awarii publikowanym na portalu.

## 6. Wskazówki praktyczne dla kancelarii

- Ustalając początek biegu terminu u klienta-osoby fizycznej, sprawdź w aktach (lub w potwierdzeniu z portalu), czy klient złożył oświadczenie o wyborze portalu.
- W razie sporu o datę doręczenia rozstrzyga **elektroniczne potwierdzenie odbioru** w aktach, a nie data e-maila z powiadomieniem.
- Klientom korzystającym z portalu warto zalecić logowanie częściej niż co 14 dni.
- **e-Doręczenia** (ustawa z 18 listopada 2020 r. o doręczeniach elektronicznych) to odrębny system. Nie zastępuje on doręczeń sądowych w postępowaniu cywilnym, które regulują przepisy k.p.c.

## Podstawy prawne

- art. 131, art. 131¹, art. 133 § 3 k.p.c.;
- art. 168–172 k.p.c. (przywrócenie terminu);
- rozporządzenie Ministra Sprawiedliwości w sprawie trybu i sposobu dokonywania doręczeń elektronicznych przez portal informacyjny (wydane na podstawie delegacji z art. 131¹ k.p.c.; zweryfikuj aktualną wersję i publikator).

Jeśli chodzi o postępowanie karne, sądowoadministracyjne lub egzekucyjne, przygotuję odrębne omówienie, bo tam obowiązują inne regulacje.
