#!/usr/bin/env python3
"""Krok faktów meta-sędziego baza wewnętrzna (prototyp, projekt PROJEKT.md z 2026-10-19).

Dla odpowiedzi modelu (pytania/odpowiedzi/<P>/<system>.md) i klucza (pytania/klucze/<P>_*.yaml)
tworzy raport faktów: meta_sedzia/raporty/<P>_<system>.json + krótki .md.

Kod, bez LLM:
  1. ekstrakcja powołań regexem: przepisy (art./ust./§/pkt + akt), sygnatury orzeczeń,
     publikatory Dz.U., daty;
  2. przepisy → legal-cite (legal-cite (https://github.com/apiotrowski-afk/legal-cite-pl), NOWA wersja; nie kopia lokalna):
     istnienie jednostki, fragment urzędowy, źródło/wersja, porównanie cytatu,
     brzmienie z poprzedniego t.j. w HTML (jedyna wcześniejsza wersja, jaką legal-cite trzyma);
  3. orzeczenia → SAOS API, a gdy brak (albo brak w sądzie podanym przez model) → wewnętrzna baza orzeczeń
     (tylko odczyt). Bez oceny „popiera / nie popiera” — to robi sędzia-model.

Bezpieczeństwo: URL bazy i hasło nigdy nie trafiają do wyjścia (wyjątki logowane tylko nazwą typu).

Użycie:
  python3 -I fakty.py P09 P10 [--systemy a,b,c]
"""
from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import html as _html
import json
import re
import sys
import time
import os
import unicodedata
from pathlib import Path

# nowa wersja legal-cite — przed site-packages, żeby nie wziąć starej kopii
sys.path.insert(0, os.environ.get("LEGAL_CITE_PATH", "legal-cite-pl"))  # https://github.com/apiotrowski-afk/legal-cite-pl
from legal_cite import core as lc  # noqa: E402

import httpx  # noqa: E402
import yaml  # noqa: E402

BENCH = Path(__file__).resolve().parents[2]  # katalog repo lawbenchmark
PYTANIA = BENCH  # klucze w keys/, odpowiedzi w answers/, specyfikacja w SPEC/
RAPORTY = Path(__file__).resolve().parents[2] / "verification" / "reports"
ENV_FILE = Path(os.environ.get("BENCHMARK_ENV_FILE", "benchmark.env"))  # opcjonalny plik z adresem wewnętrznej bazy orzeczeń (poza repozytorium)

SYSTEMY_R3 = [
    "chatgpt_codex_w0_r3", "chatgpt_codex_web_r3", "codex_astra6_w0_r3", "codex_astra6_web_r3",
    "codex_terra56_w0_r3", "codex_terra56_web_r3", "haiku_cli_w0_r3", "haiku_cli_w1_r3",
    "sonnet_cli_w0_r3", "sonnet_cli_w1_r3", "opus_cli_w0_r3", "opus_cli_w1_r3",
    "gemini38flash_vertex_w0_r3", "gemini38flash_vertex_w1_r3",
    "argon4_high_vertex_w0_r3", "argon4_high_vertex_w1_r3",
]

LIMIT_FRAGMENT = 700      # przycięcie urzędowego fragmentu jednostki
LIMIT_KONTEKST = 450      # przycięcie zdania kontekstu
POCZATEK_WYROKU = 600     # znaki początku tekstu orzeczenia

# liczniki zapytań (raport końcowy)
LICZNIKI = {"legal_cite": 0, "eli_meta": 0, "saos_search": 0, "saos_judgment": 0, "lexalpha": 0}


# ───────────────────────── tekst odpowiedzi ─────────────────────────

def body_of_answer(raw: str) -> str:
    """Treść odpowiedzi bez nagłówka YAML (zapytania wyszukiwarki nie są powołaniami)."""
    m = re.search(r"^## Odpowiedź\s*$", raw, re.M)
    if m:
        return raw[m.end():]
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            return raw[end + 4:]
    return raw


def clean_markdown(t: str) -> str:
    """Usuwa wyróżnienia markdown (** _ `), które rozbijają wzorce powołań.
    2026-10-24 (A1): zapisy techniczne indeksu górnego sprowadzane do „N^X”: LaTeX „$131^{1a}$ § $1^1$”,
    „394^{2}”, HTML „<sup>1a</sup>” — dalej NUM i _norm_sup czytają „^1a” jak „¹ᵃ”."""
    t = re.sub(r"\$(\d+[a-z]?)\^\{?(\d+[a-z]?)\}?\$", r"\1^\2", t)      # $131^{1a}$ → 131^1a
    t = re.sub(r"\$(\d+[a-z]?)\$", r"\1", t)                              # $1$ → 1
    t = re.sub(r"(\d)\^\{(\d+[a-z]?)\}", r"\1^\2", t)                     # 394^{2} → 394^2
    t = re.sub(r"(\d)<sup>\s*(\d+[a-z]?)\s*</sup>", r"\1^\2", t)         # 131<sup>1a</sup> → 131^1a
    t = t.replace("**", "").replace("`", "")
    t = re.sub(r"(?<=\S)\*|\*(?=\S)", "", t)
    t = re.sub(r"(?<![\w/])_(?=\w)|(?<=\w)_(?![\w/])", "", t)
    t = t.replace(" ", " ")
    return t


def norm(s: str) -> str:
    """Normalizacja do porównań: NFKC, małe litery, tylko litery i cyfry."""
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[^\w]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


STOP = set("""
oraz albo lub jako jest są być było może mogą także także tylko jeżeli jeśli który która które
których którym tego tych tym temu przez przy nad pod jego jej ich więc zatem czyli również
bardzo nawet jednak gdyż ponieważ dlatego takie taki taka tak nie się sobie swoje swoich
umowa umowy umowie umową prawa prawo praw autorskich autorskie autorskiego ustawy ustawa
artykuł przepis przepisu przepisy zgodnie podstawie wskazuje stanowi zakres zakresie
""".split())

# słowa dziedzinowe pomijane w sygnale „słowa wersji wcześniejszej” (występują wszędzie)
DOMENA = {"utwor", "korzy", "twórc", "autor", "umowa", "umowy", "prawa", "przen", "licen",
          "eksplo", "pola", "polac", "majat", "mająt"}


def stems(text: str, n: int = 5, minlen: int = 5) -> set[str]:
    out = set()
    for w in re.findall(r"[a-ząćęłńóśźż]+", text.lower()):
        if len(w) >= minlen and w not in STOP:
            out.add(w[:n])
    return out


ABBR = r"(?:art|ust|pkt|lit|r|nr|poz|zm|t\.j|tj|ok|m\.in|np|tzw|zob|por|sygn|akt|dz|u|k|c|p|ww|wym|zw|dot|ds|pr|aut|ul|tys|zł|godz|s|n|in|ust|al|cyt|red|wyd|op|cit|itd|itp|tj|j)"


def sentence_span(text: str, pos: int, end: int) -> tuple[int, int]:
    """Granice zdania wokół [pos, end) — w obrębie wiersza; nie tnie na skrótach (art., ust., r.)."""
    ls = text.rfind("\n", 0, pos) + 1
    le = text.find("\n", end)
    le = len(text) if le == -1 else le
    line = text[ls:le]
    cuts = [0]
    for m in re.finditer(r"[.!?…](?=\s+[„\"(A-ZŁŚŻŹĆŃÓ])", line):
        before = line[max(0, m.start() - 6):m.start()]
        if re.search(rf"(?:^|[\s(.]){ABBR}$", before, re.I) or re.search(r"\d$", before):
            continue
        cuts.append(m.end())
    cuts.append(len(line))
    rel_p, rel_e = pos - ls, end - ls
    s = max(c for c in cuts if c <= rel_p)
    e = min(c for c in cuts if c >= rel_e)
    return ls + s, ls + e


def trim(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


# ───────────────────────── akty ─────────────────────────

# (wzorzec, kod legal-cite albo None = nieobsługiwany, nazwa)
_ACTS: list[tuple[str, str | None, str]] = [
    (r"k\.?\s?p\.?\s?c\.?|KPC\b|Kodeksu postępowania cywilnego|kodeksu postępowania cywilnego", "KPC", "Kodeks postępowania cywilnego"),
    (r"k\.?\s?p\.?\s?k\.?|KPK\b|Kodeksu postępowania karnego", "KPK", "Kodeks postępowania karnego"),
    (r"k\.?\s?p\.?\s?a\.?|KPA\b|Kodeksu postępowania administracyjnego", "KPA", "Kodeks postępowania administracyjnego"),
    (r"p\.?\s?p\.?\s?s\.?\s?a\.?|PPSA\b|ustawy\s+[–-]\s+Prawo o postępowaniu przed sądami administracyjnymi", "PPSA", "Prawo o postępowaniu przed sądami administracyjnymi"),
    (r"k\.?\s?k\.?\s?s\.?|KKS\b|Kodeksu karnego skarbowego", "KKS", "Kodeks karny skarbowy"),
    (r"k\.?\s?s\.?\s?h\.?|KSH\b|Kodeksu spółek handlowych", "KSH", "Kodeks spółek handlowych"),
    (r"k\.?\s?r\.?\s?o\.?|KRO\b|Kodeksu rodzinnego i opiekuńczego", "KRO", "Kodeks rodzinny i opiekuńczy"),
    (r"k\.c\.|KC\b|kc\b|Kodeksu cywilnego|kodeksu cywilnego|Kodeks cywilny|KC", "KC", "Kodeks cywilny"),
    (r"k\.k\.|KK\b|Kodeksu karnego|kodeksu karnego", "KK", "Kodeks karny"),
    (r"k\.w\.|KW\b|Kodeksu wykroczeń|kodeksu wykroczeń", "KW", "Kodeks wykroczeń"),
    (r"k\.p\.|KP\b|Kodeksu pracy|kodeksu pracy", "KP", "Kodeks pracy"),
    (r"pr\.?\s?aut\.?|PrAut\b|PAut\b|p\.?\s?a\.?\s?p\.?\s?p\.?|u\.?\s?p\.?\s?a\.?\s?p\.?\s?p\.?|upapp\b|"
     r"[Uu]stawy o prawie autorskim(?: i prawach pokrewnych)?|[Pp]rawa autorskiego", "PrAut", "Prawo autorskie i prawa pokrewne"),
    (r"u\.k\.k\.|UKK\b|ustawy o kredycie konsumenckim", "u.k.k.", "Ustawa o kredycie konsumenckim"),
    (r"u\.o\.k\.k\.", None, "Ustawa o ochronie konkurencji i konsumentów"),
    # 2026-10-24 (decyzja Adama nr 3): u.n.n.c. w legal-cite (gałąź feat/unnc, kod UNNC); nazwy opisowe — także
    # „ustawy z 1920 r.” / „ustawy z dnia 24 marca 1920 r.” bez tytułu (zapis skrócony w odpowiedziach P04)
    (r"u\.n\.n\.c\.|UNNC\b|ustawy o nabywaniu nieruchomości przez cudzoziemców|"
     r"ustaw\w*\s+z\s+(?:dnia\s+)?(?:24\s+marca\s+|24\.03\.)?1920\s*r?\.?(?!\s+o\s)", "UNNC", "Ustawa o nabywaniu nieruchomości przez cudzoziemców"),
    (r"u\.k\.w\.h\.|ustawy o księgach wieczystych i hipotece", "u.k.w.h.", "Ustawa o księgach wieczystych i hipotece"),
    (r"u\.ś\.u\.d\.e\.|ustawy o świadczeniu usług drogą elektroniczną", "u.ś.u.d.e.", "Ustawa o świadczeniu usług drogą elektroniczną"),
    (r"u\.z\.n\.k\.|ustawy o zwalczaniu nieuczciwej konkurencji", "u.z.n.k.", "Ustawa o zwalczaniu nieuczciwej konkurencji"),
    (r"u\.p\.k\.|ustawy o prawach konsumenta", "u.p.k.", "Ustawa o prawach konsumenta"),
    (r"u\.k\.s\.c\.|ustawy o kosztach sądowych w sprawach cywilnych", "u.k.s.c.", "Ustawa o kosztach sądowych w sprawach cywilnych"),
    (r"u\.r\.p\.|ustawy o radcach prawnych", "u.r.p.", "Ustawa o radcach prawnych"),
    (r"ustawy o cudzoziemcach", "u.c.", "Ustawa o cudzoziemcach"),
    (r"ustawy o ochronie danych osobowych|u\.o\.d\.o\.", "UODO", "Ustawa o ochronie danych osobowych"),
    (r"ustawy o informatyzacji[\w\s]{0,80}?publiczne", None, "Ustawa o informatyzacji działalności podmiotów realizujących zadania publiczne"),
    (r"ustawy o doręczeniach elektronicznych|u\.d\.e\.", None, "Ustawa o doręczeniach elektronicznych"),
    (r"RODO|GDPR", "RODO", "Rozporządzenie 2016/679 (RODO)"),
    (r"AI Act|AIA\b|Aktu o sztucznej inteligencji|aktu o sztucznej inteligencji", "AI Act", "Rozporządzenie 2024/1689 (AI Act)"),
    (r"DSA\b", "DSA", "Rozporządzenie 2022/2065 (DSA)"),
    (r"Konstytucji(?: RP)?", None, "Konstytucja RP"),
    # 2026-10-24 (A2): opisowe nazwy aktów zmieniających/epizodycznych — rozpoznawane, żeby nie podstawiać aktu domniemanego
    (r"ustaw\w*\s+(?:nowelizując\w*|zmieniając\w*|covidow\w*|epizodyczn\w*|antycovidow\w*)", None, "Ustawa nowelizująca / epizodyczna (akt zmieniający)"),
    (r"(?:unijn\w*\s+)?[Dd]yrektyw\w*\s+(?:DSM|InfoSoc|Omnibus|o prawie autorskim[\w\s]{0,40}?jednolitym rynku cyfrowym)", None, "Dyrektywa (nazwa skrócona)"),
    # ogólne nazwy aktów spoza listy — nieobsługiwane, bez zgadywania
    (r"ustaw\w*\s+(?:z\s+dnia\s+\d{1,2}\s+\w+\s+\d{4}\s*r\.\s+)?o\s+[a-ząćęłńóśźż]+(?:\s+[a-ząćęłńóśźż]+){0,6}", None, "Ustawa spoza listy legal-cite"),
    (r"(?:tej\s+)?ustawy(?![\w])(?!\s+(?:o|z)\s)", "DOMYSLNY", "ta ustawa (akt domniemany)"),
    (r"[Kk]odeksu\s+[a-ząćęłńóśźż]+(?:\s+[a-ząćęłńóśźż]+){0,3}", None, "Kodeks spoza listy legal-cite"),
]
_EU_REG = {"2016/679": "RODO", "2024/1689": "AI Act", "2022/2065": "DSA", "2022/868": "DGA",
           "2022/1925": "DMA"}
_EU_DIR = {"2008/48": "CCD", "2022/2555": "NIS2"}

# data ustawy słownie („z dnia 24 marca 1920 r.”) albo liczbowo („z 24.03.1920 r.”, „z 24.03.1920”) — 2026-10-24 (A2)
_USTAWY_O = r"ustaw\w*\s+(?:z\s+(?:dnia\s+)?(?:\d{1,2}\s+\w+\s+\d{4}|\d{1,2}\.\d{1,2}\.\d{4})\s*(?:r\.)?\s+)?o\s+"
_ACTS = [(re.sub(r"\[Uu\]stawy o |ustawy o ", lambda _m: _USTAWY_O, p), k, n) for p, k, n in _ACTS]

ACT_RE = re.compile(
    r"\s*\(?,?\s*(?:"
    + "|".join(f"(?P<a{i}>{p})" for i, (p, _, _) in enumerate(_ACTS))
    + r"|(?P<reg>(?:unijn\w*\s+|wspólnotow\w*\s+)?rozporządzeni\w*(?:\s+Parlamentu Europejskiego i Rady)?\s+\(?(?:UE|WE)?\)?\s*(?:nr\s*)?(?P<regnr>\d{2,4}/\d{1,4}))"
    + r"|(?P<dir>(?:unijn\w*\s+|wspólnotow\w*\s+)?dyrektyw\w*(?:\s+Parlamentu Europejskiego i Rady)?\s+(?:\((?:UE|WE)\)\s*)?(?:nr\s*)?(?P<dirnr>\d{2,4}/\d{1,4})(?:/W?E)?)"
    + r")(?![\w])", re.I
)


UNKNOWN_ACT_RE = re.compile(
    r"\s*\(?\s*((?:unijn\w*\s+)?(?:[Dd]yrektyw|[Rr]ozporządze|[Kk]onwencj|[Tt]raktat|TFUE\b|TUE\b|Karty\b|[Kk]odeks|[A-ZŁŚŻ]{2,}\b)[^\s,;.)]*(?:\s+[^\s,;.)]+){0,3})")


def match_act(text: str, pos: int) -> tuple[dict | None, int]:
    """Akt bezpośrednio po powołaniu (dopuszcza nawias/przecinek). Zwraca (akt, koniec).
    Akt nierozpoznany (np. skrót spoza listy) → kod None: nieobsługiwany, bez zgadywania."""
    m = ACT_RE.match(text, pos)
    if not m:
        mu = UNKNOWN_ACT_RE.match(text, pos)
        if mu and not re.match(r"\s*\(?\s*(?:ust|pkt|lit|art)\b", text[pos:pos + 12], re.I):
            return {"kod": None, "nazwa": f"akt nierozpoznany: {mu.group(1)}", "napis": mu.group(1)}, mu.end()
        return None, pos
    if m.group("reg"):
        nr = m.group("regnr")
        kod = _EU_REG.get(nr)
        return {"kod": kod, "nazwa": f"Rozporządzenie {nr}", "napis": m.group(0).strip(" (,")}, m.end()
    if m.group("dir"):
        nr = m.group("dirnr")
        kod = _EU_DIR.get(nr)
        return {"kod": kod, "nazwa": f"Dyrektywa {nr}", "napis": m.group(0).strip(" (,")}, m.end()
    for i, (_, kod, nazwa) in enumerate(_ACTS):
        if m.group(f"a{i}"):
            napis = m.group(f"a{i}")
            if nazwa.endswith("spoza listy legal-cite"):
                nazwa = napis
                k2 = lc._resolve(napis, lc.PL_ACTS) or lc._resolve(napis, lc.EU_ACTS)
                if k2:
                    kod = k2
                    nazwa = (lc.PL_ACTS.get(k2) or lc.EU_ACTS.get(k2))["name"]
            return {"kod": kod, "nazwa": nazwa, "napis": napis}, m.end()
    return None, pos


def acts_in_text(text: str) -> list[dict]:
    """Wszystkie nazwy/skróty aktów w tekście (zdanie, akapit) — do reguły aktu domniemanego (A2, 2026-10-24).
    Pomija „tej ustawy” (DOMYSLNY) — to odesłanie, nie nazwa innego aktu."""
    out = []
    for m in ACT_RE.finditer(text):
        a, _ = match_act(text, m.start())
        if a and a.get("kod") != "DOMYSLNY":
            out.append(a)
    return out


def act_identity(a: dict | None) -> str:
    """Tożsamość aktu do porównań: kod legal-cite, a bez kodu — znormalizowana nazwa."""
    if not a:
        return ""
    return (a.get("kod") or norm(a.get("nazwa") or a.get("napis") or "")).lower()


def other_acts(text: str, default: dict | None) -> list[str]:
    """Nazwy aktów w tekście innych niż akt domniemany (bez powtórzeń)."""
    seen, out = set(), []
    did = act_identity(default)
    for a in acts_in_text(text):
        ident = act_identity(a)
        if ident and ident != did and ident not in seen:
            seen.add(ident)
            out.append(a.get("napis") or a.get("nazwa"))
    return out


# ───────────────────────── powołania przepisów ─────────────────────────

SUP = "¹²³⁴⁵⁶⁷⁸⁹⁰"
SUP_LIT = "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻ"   # litera w indeksie górnym (art. 131¹ᵃ, 394¹ᵃ k.p.c.) — brak jej kosztował 16 powołań w teście 24.10
# litera indeksu także jako zwykła mała litera tuż po cyfrze w indeksie („131¹a” — 4 odpowiedzi w P05), ale nie
# gdy zaczyna wyraz („art. 131¹ a także…”): bez spacji i bez kolejnej litery po niej
NUM = rf"\d+[a-z]{{0,3}}(?:\s?[{SUP}]+(?:[{SUP_LIT}]|[a-z](?![a-ząćęłńóśźż]))?|\^\d+[a-z]?|\[\d+[a-z]?\])?"
_SUP_TR = str.maketrans(SUP + SUP_LIT, "1234567890" + "abcdefghijklmnoprstuvwxyz")


def _norm_sup(art: str) -> str:
    """„131¹ᵃ” / „131¹a” / „131^1a” → „131[1a]” (zapis legal-cite); „98 § 1¹” obsługuje wołający; bez indeksu — bez zmian."""
    art = art.replace(" ", "")
    m = re.fullmatch(rf"(\d+[a-z]{{0,3}})([{SUP}]+)([{SUP_LIT}]|[a-z])?", art)
    if m:
        return f"{m.group(1)}[{m.group(2).translate(_SUP_TR)}{(m.group(3) or '').translate(_SUP_TR)}]"
    m = re.fullmatch(r"(\d+[a-z]{0,3})\^(\d+[a-z]?)", art)
    if m:
        return f"{m.group(1)}[{m.group(2)}]"
    return art


def norm_unit_label(s: str) -> str:
    """Do porównań numerów jednostek: „1¹”, „1^1”, „1[1]” → „11”; „131¹ᵃ” → „1311a”."""
    s = (s or "").replace(" ", "").translate(_SUP_TR)
    return re.sub(r"[\^\[\]]", "", s).lower()
ART_START = re.compile(rf"\b[Aa]rt(?:\.|ykuł\w*)\s*({NUM})(?![\d/])")
TOK_UNIT = re.compile(rf"\s*(ust\.|§)\s*({NUM})")
TOK_PKT = re.compile(rf"\s*(pkt|lit\.)\s*([\w{SUP}]+(?:\s*[–-]\s*\w+)?)\)?")
TOK_CONN = re.compile(r"\s*(,|i|oraz|lub|albo|[–—-]|do)\s+|\s*[–—-]\s*")
TOK_ZW = re.compile(r"\s*(?:,\s*)?(?:w zw\. z|w związku z)\s+")
TOK_ART = re.compile(rf"\s*(?:art\.|Art\.)\s*({NUM})(?![\d/])")
TOK_NUM = re.compile(rf"({NUM})(?![\d/.]\d)")


def _int(s: str) -> int | None:
    return int(s) if s.isascii() and s.isdigit() else None


def parse_provision_group(text: str, start: int) -> tuple[list[dict], int]:
    """Parsuje łańcuch od „art. N”: ustępy/paragrafy, punkty, wyliczenia, zakresy, „w zw. z”,
    akt po łańcuchu. Zwraca (pozycje, koniec)."""
    m = ART_START.match(text, start)
    # rola (A5, 2026-10-24): „główne” — powołanie niosące twierdzenie; „w_zwiazku” — po „w zw. z”; „zakres” — człon
    # rozwinięcia „art. 111–117” / „§ 1–2”. Powołania niegłówne nie dostają osobnej oceny poparcia (jedno twierdzenie,
    # jedno powołanie główne; ich brzmienie dołącza do źródła powołania głównego).
    items: list[dict] = [{"art": m.group(1), "kind": None, "unit": None, "pkt": None, "akt": None, "rola": "główne"}]
    w_zw = False
    pre = text[max(0, start - 90):start]
    if re.search(r"\(\s*$", pre):
        cut = pre.rstrip()[:-1].rstrip()
        for mm in ACT_RE.finditer(cut):
            if mm.end() == len(cut):
                a, _ = match_act(cut, mm.start())
                if a:
                    items[0]["akt_przed"] = a
    pos, level, pending = m.end(), "art", [0]
    while True:
        mu = TOK_UNIT.match(text, pos)
        if mu and level in ("art", "unit", "pkt"):
            cur = items[-1]
            if cur["unit"] is None and level == "art":
                cur["kind"], cur["unit"] = ("§" if mu.group(1) == "§" else "ust."), mu.group(2)
            else:
                items.append({**cur, "kind": "§" if mu.group(1) == "§" else "ust.", "unit": mu.group(2), "pkt": None,
                              "rola": "w_zwiazku" if w_zw else "główne"})
                pending.append(len(items) - 1)
            pos, level = mu.end(), "unit"
            continue
        mp = TOK_PKT.match(text, pos)
        if mp:
            items[-1]["pkt"] = (items[-1]["pkt"] + "," if items[-1]["pkt"] else "") + mp.group(2)
            pos, level = mp.end(), "pkt"
            continue
        mz = TOK_ZW.match(text, pos)
        if mz:
            ma = TOK_ART.match(text, mz.end())
            if ma:
                w_zw = True
                items.append({"art": ma.group(1), "kind": None, "unit": None, "pkt": None, "akt": None, "rola": "w_zwiazku"})
                pending.append(len(items) - 1)
                pos, level = ma.end(), "art"
                continue
        akt, aend = match_act(text, pos)
        if akt:
            for i in pending:
                if items[i]["akt"] is None:
                    items[i]["akt"] = akt
            pending = []
            pos = aend
            # po akcie łańcuch może trwać („… pr.aut. w zw. z art. 49”)
            mz = TOK_ZW.match(text, pos)
            if mz and TOK_ART.match(text, mz.end()):
                continue
            break
        mc = TOK_CONN.match(text, pos)
        if mc:
            conn = mc.group(1) or "–"
            after = mc.end()
            rola_conn = "w_zwiazku" if w_zw else "główne"
            ma = TOK_ART.match(text, after)
            if ma:
                items.append({"art": ma.group(1), "kind": None, "unit": None, "pkt": None, "akt": None, "rola": rola_conn})
                pending.append(len(items) - 1)
                pos, level = ma.end(), "art"
                continue
            mu2 = TOK_UNIT.match(text, after)
            if mu2:
                pos = after - 0
                # obsłużone w następnym obiegu jako jednostka
                items.append({**items[-1], "kind": "§" if mu2.group(1) == "§" else "ust.", "unit": mu2.group(2), "pkt": None,
                              "rola": rola_conn})
                pending.append(len(items) - 1)
                pos, level = mu2.end(), "unit"
                continue
            mn = TOK_NUM.match(text, after)
            if mn and level in ("art", "unit") and not re.match(r"\s*(?:r\.|roku|zł|%|dni|lat)", text[mn.end():mn.end() + 6]):
                n_new = mn.group(1)
                cur = items[-1]
                if level == "unit" and _int(n_new) and _int(cur["unit"] or "") and _int(n_new) > 15 and _int(n_new) > _int(cur["unit"]):
                    level = "art"   # „art. 41 ust. 4, 43–44, 65” — dalej numery artykułów
                if level == "unit":
                    a, b = _int(cur["unit"] or ""), _int(n_new)
                    zakres = conn in "–—-" and a and b and 0 < b - a <= 6
                    rng = range(a + 1, b + 1) if zakres else [n_new]
                    for u in rng:
                        items.append({**cur, "unit": str(u), "pkt": None, "rola": "zakres" if zakres else rola_conn})
                        pending.append(len(items) - 1)
                else:
                    a, b = _int(cur["art"]), _int(n_new)
                    zakres = conn in "–—-" and a and b and 0 < b - a <= 6
                    rng = range(a + 1, b + 1) if zakres else [n_new]
                    for u in rng:
                        items.append({"art": str(u), "kind": None, "unit": None, "pkt": None, "akt": None,
                                      "rola": "zakres" if zakres else rola_conn})
                        pending.append(len(items) - 1)
                pos = mn.end()
                continue
        break
    if items[0].get("akt_przed"):
        for it in items:
            if not it["akt"]:
                it["akt_przed"] = items[0]["akt_przed"]
    return items, pos


def find_quotes(text: str, a: int, b: int) -> list[tuple[int, int, str]]:
    out = []
    for m in re.finditer(r"„([^”\"\n]{3,1500})[”\"]|\"([^\"\n]{3,1500})\"|“([^”\n]{3,1500})”|«([^»\n]{3,1500})»", text[a:b]):
        q = next(g for g in m.groups() if g)
        out.append((a + m.start(), a + m.end(), q))
    return out


def extract_provisions(text: str) -> list[dict]:
    res = []
    pos = 0
    while True:
        m = ART_START.search(text, pos)
        if not m:
            break
        items, end = parse_provision_group(text, m.start())
        s, e = sentence_span(text, m.start(), end)
        ctx = text[s:e]
        # zdanie kończy się dwukropkiem → cytat zwykle w następnym wierszu
        win_end = e
        if ctx.rstrip().endswith(":") or text[end:end + 25].lstrip().startswith(":"):
            nxt = text.find("\n", e)
            while nxt != -1 and nxt + 1 < len(text) and text[nxt + 1:text.find("\n", nxt + 1) if text.find("\n", nxt + 1) != -1 else len(text)].strip() == "":
                nxt = text.find("\n", nxt + 1)
            if nxt != -1:
                nl = text.find("\n", nxt + 1)
                win_end = len(text) if nl == -1 else nl
        res.append({"start": m.start(), "end": end, "napis": text[m.start():end].strip(), "items": items,
                    "ctx_span": (s, e), "win_span": (s, win_end)})
        pos = max(end, m.end())
    # przypisanie cytatów: każdy cytat (≥ 6 słów) do najbliższego powołania w tym samym oknie
    for g in res:
        g["quote"] = None
    all_quotes = {}
    for gi, g in enumerate(res):
        for (qa, qb, q) in find_quotes(text, *g["win_span"]):
            if len(q.split()) < 6:
                continue
            if qa <= g["start"] < qb:   # powołanie wewnątrz cytatu
                continue
            if re.search(r"\bart\.", q):
                continue
            if qa >= g["end"]:
                gap = text[g["end"]:qa]
                lead = text[max(0, qa - 12):qa]
                if re.search(r"\bnp\.|klauzul|zapis|formuł|sformułowa|przykład|wpis", gap + lead, re.I):
                    continue
                if not (len(gap) <= 25 or (len(gap) <= 140 and re.search(
                        r":|stanowi|brzmi|przewiduje|zgodnie z którym|wynika|mówi|cyt\.", gap))):
                    continue
                d = len(gap)
            else:
                gap = text[qb:g["start"]]
                if len(gap) > 4:   # „…” (art. N) — cytat tuż przed powołaniem
                    continue
                d = len(gap)
            if (qa, qb) not in all_quotes or d < all_quotes[(qa, qb)][1]:
                all_quotes[(qa, qb)] = (gi, d, q)
    for (qa, qb), (gi, d, q) in all_quotes.items():
        res[gi]["quote"] = q
    return res


# ───────────────────────── legal-cite ─────────────────────────

_lc_cache: dict[str, dict] = {}


def _parse_lc_output(out: str) -> dict:
    parts = out.split("\n\n")
    header = parts[0]
    body = parts[1] if len(parts) > 1 else ""
    notes = [p for p in parts[2:] if not p.startswith("[dla modelu]")]
    akt_line = next((ln for ln in out.splitlines() if ln.startswith("Aktualność:")), None)
    head_lines = [ln for ln in header.splitlines()[1:] if not ln.startswith("Aktualność:")]
    return {"zrodlo": trim(" ".join(head_lines), 600), "aktualnosc": akt_line[len("Aktualność:"):].strip() if akt_line else None,
            "tekst": body.strip(), "uwagi": [trim(n, 300) for n in notes]}


DEFAULT_DATA_STANU: str | None = None      # ustawiane przez wołającego (poparcie.py), gdy nie podaje daty wprost
LATA_WSTECZ = (2, 5, 10, 15)                   # (historyczne) wcześniejsze brzmienia do klasy W (na_dzien = data − N lat)
# 2026-10-24 (decyzja Adama nr 2 — krąg adresatów / zakres z brzmienia z innej daty = W): krok co 6 miesięcy na początku,
# bo zmiana sprzed kilku miesięcy (art. 131¹ᵃ § 1 k.p.c., 1.06.2026 przy dacie stanu 1.10.2026) wypadała między
# „dziś” a „−2 lata”, a legal-cite na dzień −2 lata oddawał tekst sprzed dodania jednostki
MIESIACE_WSTECZ = (6, 12, 24, 60, 120, 180)


def data_wstecz(d0: dt.date, miesiace: int) -> str:
    """Data o N miesięcy wcześniejsza (ten sam dzień miesiąca; przy braku dnia — ostatni dzień miesiąca)."""
    y, m = divmod(d0.year * 12 + (d0.month - 1) - miesiace, 12)
    m += 1
    for dzien in (d0.day, 30, 29, 28):
        try:
            return dt.date(y, m, dzien).isoformat()
        except ValueError:
            continue
    return dt.date(y, m, 1).isoformat()


def _extract_unit(text: str, kind: str | None, unit: str | None) -> str | None:
    """Z tekstu całego artykułu wycina ustęp/paragraf (gdy legal-cite na_dzien podaje cały artykuł).
    Znaczniki jednostek („§ 2.”, „2.”) stoją po nagłówku „Art. N.”, po końcu zdania albo na początku wiersza,
    a po nich jest spacja i wielka litera, cudzysłów, nawias albo „(uchylony)”."""
    if not unit:
        return text
    # 2026-10-24: znaczniki z indeksem górnym („§ 1¹.”) też są jednostkami (art. 131¹ᵃ § 1¹ k.p.c.)
    marker = re.compile(rf"(?:^|(?<=\.\s)|(?<=\n))(§\s*)?(\d+[a-z]?[{SUP}]*)\.\s+(?=[A-ZŁŚŻŹĆĄĘÓŃ„(\[])", re.M)
    hits = [(m.start(), bool(m.group(1)), m.group(2)) for m in marker.finditer(text)]
    want_par = kind == "§"
    for i, (pos, is_par, num) in enumerate(hits):
        if norm_unit_label(num) == norm_unit_label(unit) and is_par == want_par:
            end = len(text)
            for pos2, is_par2, _ in hits[i + 1:]:
                if is_par2 == want_par:
                    end = pos2
                    break
            return text[pos:end].strip()
    return None


async def wording_on_date(citation: str, date: str) -> dict:
    """Brzmienie jednostki na wskazany dzień (legal-cite na_dzien, tylko akty PL)."""
    LICZNIKI["legal_cite"] += 1
    try:
        from legal_cite.na_dzien import verify_article_na_dzien
        out = await verify_article_na_dzien(citation, date)
    except Exception as e:
        return {"status": "błąd", "blad": type(e).__name__, "na_dzien": date}
    if out.startswith("❌"):
        return {"status": "nie istnieje" if "nie znaleziony" in out else "błąd", "komunikat": trim(out[2:], 300), "na_dzien": date}
    p = _parse_lc_output(out)
    m = re.search(r"ustalenie=([a-z_]+)", out)
    tekst = p["tekst"]
    if "podaję cały artykuł" in out:
        parsed = lc.parse_citation(citation)
        kind = "§" if parsed and "§" in citation else "ust."
        cut = _extract_unit(tekst, kind, parsed.get("ustep") if parsed else None)
        if cut:
            tekst = cut
    return {"status": "istnieje", "na_dzien": date, "tekst_pelny": tekst, "ustalenie": m.group(1) if m else None,
            "zrodlo": p["zrodlo"], "znacznik": "urzędowy HTML" if out.startswith("📜") else "nieurzędowy odczyt PDF"}


async def verify_provision(citation: str, code: str, data_stanu: str | None = None) -> dict:
    """Wynik legal-cite: brzmienie dzisiejsze + brzmienie NA DATĘ STANU PRAWNEGO (na_dzien) + wcześniejsze
    brzmienia (data − 2/5/10 lat) do wykrywania klasy W. Pamięć podręczna w obrębie biegu."""
    data_stanu = data_stanu or DEFAULT_DATA_STANU
    ckey = (citation, data_stanu)
    if ckey in _lc_cache:
        return _lc_cache[ckey]
    LICZNIKI["legal_cite"] += 1
    try:
        out = await lc.verify_article(citation)
    except Exception as e:  # sieć, ELI
        res = {"status": "błąd weryfikacji", "blad": type(e).__name__}
        _lc_cache[ckey] = res
        return res
    if out.startswith("❌"):
        if "Nieznany kod aktu" in out:
            res = {"status": "nieobsługiwany akt — do sprawdzenia ręcznie"}
        elif "nie znaleziony" in out:
            res = {"status": "nie istnieje", "komunikat": trim(out[2:], 300)}
            # 2026-10-24: jednostki nie ma w dzisiejszym tekście — sprawdź, czy była na datę stanu prawnego
            # (istnieje) albo wcześniej (uchylona/usunięta → kandydat W, nie F; README: „jednostka uchylona … = W, nie F”)
            if data_stanu and code in lc.PL_ACTS:
                nd = await wording_on_date(citation, data_stanu)
                if nd.get("tekst_pelny"):
                    res = {"status": "istnieje", "znacznik": nd.get("znacznik"), "zrodlo": nd.get("zrodlo"),
                           "aktualnosc": "jednostki brak w dzisiejszym tekście; brzmienie z na_dzien", "uwagi": [],
                           "tekst_pelny": nd["tekst_pelny"], "uchylony": False, "na_dzien": nd,
                           "tekst_na_dzien": nd["tekst_pelny"], "wersje": {"status": "wersje wcześniejsze: nie sprawdzono (jednostka z na_dzien)"},
                           "wersje_wczesniejsze": []}
                    _lc_cache[ckey] = res
                    return res
                try:
                    d0 = dt.date.fromisoformat(data_stanu[:10])
                except ValueError:
                    d0 = None
                for mies in (MIESIACE_WSTECZ if d0 else ()):
                    d = data_wstecz(d0, mies)
                    w = await wording_on_date(citation, d)
                    if w.get("tekst_pelny"):
                        res["istniala_wczesniej"] = {"na_dzien": d, "fragment": trim(w["tekst_pelny"], LIMIT_FRAGMENT),
                                                     "ustalenie": w.get("ustalenie")}
                        break
        else:
            res = {"status": "błąd weryfikacji", "komunikat": trim(out[2:], 400)}
        _lc_cache[ckey] = res
        return res
    p = _parse_lc_output(out)
    tekst = p["tekst"]
    uchylony = bool(re.fullmatch(r"\s*(?:Art\.\s*\S+\s*)?(?:§\s*\S+|\d+\w*\.)?\s*\((?:uchylony|uchylona|uchylone|pominięty)\)\.?\s*", tekst))
    res = {"status": "istnieje", "znacznik": "urzędowy HTML" if out.startswith("📜") else "nieurzędowy odczyt PDF / tekst skonsolidowany",
           "zrodlo": p["zrodlo"], "aktualnosc": p["aktualnosc"], "uwagi": p["uwagi"], "tekst_pelny": tekst,
           "uchylony": uchylony}
    res["wersje"] = previous_version(citation, code, tekst)
    # brzmienie na datę stanu prawnego i wersje wcześniejsze (tylko akty PL — na_dzien nie obsługuje UE)
    if data_stanu and code in lc.PL_ACTS:
        nd = await wording_on_date(citation, data_stanu)
        res["na_dzien"] = nd
        if nd.get("tekst_pelny"):
            res["tekst_na_dzien"] = nd["tekst_pelny"]
            res["uchylony_na_dzien"] = bool(re.fullmatch(
                r"\s*(?:§\s*\S+|\d+\w*\.)?\s*\((?:uchylony|uchylona|uchylone|pominięty)\)\.?\s*", nd["tekst_pelny"]))
        baza = norm(res.get("tekst_na_dzien") or tekst).replace(" ", "")
        wcz, widziane = [], {baza}
        try:
            d0 = dt.date.fromisoformat(data_stanu[:10])
        except ValueError:
            d0 = None
        for mies in (MIESIACE_WSTECZ if d0 else ()):
            d = data_wstecz(d0, mies)
            w = await wording_on_date(citation, d)
            t = w.get("tekst_pelny")
            if not t:
                wcz.append({"na_dzien": d, "status": w.get("status"), "komunikat": w.get("komunikat")})
                continue
            k = norm(t).replace(" ", "")
            if k in widziane:
                continue
            widziane.add(k)
            wcz.append({"na_dzien": d, "status": "inne brzmienie", "ustalenie": w.get("ustalenie"), "tekst_pelny": t})
        res["wersje_wczesniejsze"] = wcz
    _lc_cache[ckey] = res
    return res


def previous_version(citation: str, code: str, current: str) -> dict:
    """Brzmienie z poprzedniego tekstu jednolitego w HTML — jedyna wcześniejsza wersja,
    którą legal-cite pobiera (do kontroli odczytu PDF). Brzmienia z dowolnej daty: nieobsługiwane."""
    if code not in lc.PL_ACTS:
        return {"status": "wersje wcześniejsze: nieobsługiwane (akt UE — legal-cite podaje tylko najnowszą wersję skonsolidowaną)"}
    info = lc.PL_ACTS[code]
    key = lc._klucz_pl(info)
    tj = (lc._tj_cache.get(key) or (None, []))[1]
    raw = lc._html_cache.get(key)
    zr = lc._zrodlo.get(key)
    if not tj or not raw or not zr:
        return {"status": "wersje wcześniejsze: nieobsługiwane (brak starszego t.j. w pamięci legal-cite)"}
    if tj[0].get("html"):
        return {"status": f"wersje wcześniejsze: nieobsługiwane (najnowszy t.j. {tj[0]['id']} jest w HTML; legal-cite nie pobiera starszych)"}
    parsed = lc.parse_citation(citation)
    try:
        old = lc.extract_pl_article_html(key, raw, parsed["art"], parsed["ustep"]) if parsed else None
    except Exception as e:
        return {"status": f"wersje wcześniejsze: nie odczytano ({type(e).__name__})"}
    tj_id, tj_data = zr[0], zr[1]
    if not old:
        return {"status": f"brak jednostki w t.j. {tj_id} (HTML, {tj_data}) — dodana później albo inny podział",
                "tj": tj_id, "data": tj_data}
    if norm(old).replace(" ", "") == norm(current).replace(" ", ""):
        return {"status": f"bez zmian względem t.j. {tj_id} (HTML, {tj_data})", "tj": tj_id, "data": tj_data}
    return {"status": f"inne brzmienie w t.j. {tj_id} (HTML, {tj_data})", "tj": tj_id, "data": tj_data,
            "tekst_pelny": old}


def compare_quote(quote: str | None, official: str | None, older) -> dict:
    """older: jedno wcześniejsze brzmienie albo lista — porównanie z każdym, zapisane najlepsze."""
    if isinstance(older, list):
        best = None
        for o in older:
            r = compare_quote(quote, official, o)
            if best is None or r.get("zgodny_z_wersja_wczesniejsza") or (
                    r.get("pokrycie_dwuwyrazow_wczesniejszy", 0) > best.get("pokrycie_dwuwyrazow_wczesniejszy", 0)):
                best = r
            if r.get("zgodny_z_wersja_wczesniejsza"):
                break
        return best if best is not None else compare_quote(quote, official, None)
    if not quote:
        return {"wynik": "brak cytatu"}
    if not official:
        return {"wynik": "nie porównano (brak tekstu urzędowego)"}
    frags = [f for f in re.split(r"\(?\s*(?:…|\.\.\.|\[\s*…\s*\]|\[\.\.\.\])\s*\)?", quote) if len(norm(f).split()) >= 3]
    if not frags:
        return {"wynik": "brak cytatu (za krótki)"}
    off = norm(official)
    ok = all(norm(f) in off for f in frags)
    qn = norm(quote).split()
    big = list(zip(qn, qn[1:]))
    offw = off.split()
    obig = set(zip(offw, offw[1:]))
    cov = round(sum(1 for b in big if b in obig) / max(1, len(big)), 2)
    res = {"wynik": "dosłowny" if ok else "niedosłowny", "pokrycie_dwuwyrazow": cov}
    if not ok and older:
        ow = norm(older).split()
        obig_old = set(zip(ow, ow[1:]))
        cov_old = round(sum(1 for b in big if b in obig_old) / max(1, len(big)), 2)
        res["pokrycie_dwuwyrazow_wczesniejszy"] = cov_old
        if cov_old >= cov + 0.1:
            res["blizszy_wersji_wczesniejszej"] = True
            res["wynik"] = "niedosłowny — bliższy wcześniejszemu t.j."
        o = norm(older)
        if all(norm(f) in o for f in frags):
            res["zgodny_z_wersja_wczesniejsza"] = True
            res["wynik"] = "niedosłowny — dosłowny względem wcześniejszego t.j."
    return res


# ───────────────────────── publikatory i daty ─────────────────────────

MIESIACE = {m: i for i, m in enumerate(["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca",
                                         "sierpnia", "września", "października", "listopada", "grudnia"], 1)}
DATE_RE = re.compile(
    r"\b(\d{1,2})\s+(stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|września|października|listopada|grudnia)\s+(\d{4})"
    r"|\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b|\b(\d{4})-(\d{2})-(\d{2})\b")
DZU_RE = re.compile(r"Dz\.\s?U\.\s*(?:z\s*)?(?:(\d{4})\s*r\.?\s*,?\s*)?(?:Nr\s*(\d+)\s*,?\s*)?poz\.\s*(\d+)", re.I)


def parse_date(m: re.Match) -> str | None:
    try:
        if m.group(1):
            return dt.date(int(m.group(3)), MIESIACE[m.group(2)], int(m.group(1))).isoformat()
        if m.group(4):
            return dt.date(int(m.group(6)), int(m.group(5)), int(m.group(4))).isoformat()
        return dt.date(int(m.group(7)), int(m.group(8)), int(m.group(9))).isoformat()
    except ValueError:
        return None


_eli_tj: dict[str, dict] = {}


async def eli_act_meta(code: str) -> dict:
    """Wykaz t.j. i aktów zmieniających z ELI (jedno zapytanie na akt)."""
    if code in _eli_tj:
        return _eli_tj[code]
    info = lc.PL_ACTS[code]
    LICZNIKI["eli_meta"] += 1
    try:
        async with httpx.AsyncClient(timeout=25, follow_redirects=True) as c:
            meta = (await c.get(f"https://api.sejm.gov.pl/eli/acts/{info['pub']}/{info['year']}/{info['pos']}")).json()
        refs = meta.get("references") or {}
        _eli_tj[code] = {"tj": [e["id"] for e in refs.get("Inf. o tekście jednolitym", [])],
                         "zmieniajace": {e["id"]: e.get("date") for e in refs.get("Akty zmieniające", [])},
                         "pierwotny": f"{info['pub']}/{info['year']}/{info['pos']}"}
    except Exception as e:
        _eli_tj[code] = {"blad": type(e).__name__}
    return _eli_tj[code]


async def check_publikatory(text: str, acts_used: set[str], data_stanu: str) -> list[dict]:
    out = []
    for m in DZU_RE.finditer(text):
        year, nr, poz = m.group(1), m.group(2), m.group(3)
        s, e = sentence_span(text, m.start(), m.end())
        ent = {"napis": m.group(0), "kontekst": trim(text[s:e], 250), "flagi": []}
        if not year:
            ent["ocena"] = "nie rozpoznano roku — do sprawdzenia ręcznie"
            out.append(ent)
            continue
        ident = f"DU/{year}/{poz}"
        found = False
        for code in sorted(acts_used):
            if code not in lc.PL_ACTS:
                continue
            meta = await eli_act_meta(code)
            if "blad" in meta:
                continue
            tjs = meta["tj"]
            if ident in tjs:
                przed = [t for t in tjs if int(t.split("/")[1]) <= int(data_stanu[:4])]
                najnowszy = max(przed, key=lambda t: (int(t.split("/")[1]), int(t.split("/")[2]))) if przed else None
                ent["ocena"] = f"tekst jednolity: {lc.PL_ACTS[code]['name']}; najnowszy t.j. przed datą stanu prawnego: {najnowszy}"
                if najnowszy and ident != najnowszy:
                    ent["flagi"].append("nieaktualny_tj")
                found = True
            elif ident in meta["zmieniajace"]:
                ent["ocena"] = f"akt zmieniający {lc.PL_ACTS[code]['name']} (w życie {meta['zmieniajace'][ident]})"
                found = True
            elif ident == meta["pierwotny"]:
                ent["ocena"] = f"tekst pierwotny: {lc.PL_ACTS[code]['name']}"
                found = True
            if found:
                break
        if not found:
            ent["ocena"] = "nie powiązano z powołanym aktem — do sprawdzenia ręcznie"
        out.append(ent)
    return out


# ───────────────────────── orzeczenia ─────────────────────────

SIG_RE = re.compile(
    r"\b([IVX]{1,4})\s+(CSKP|CSK|CKN|CK|CZP|CNP|CSPP|CO|CZ|CR|ACa|ACz|AGa|AGz|APa|AUa|Ca|Cz|Ga|Gz|GC|C|Nc|Ns|PK|PSK|PSKP|UK|USK|KK|KZP|KO|Ka|Kz|NSNc|NSNk|NSNp|NZP|NSK|OSK|FSK|GSK|SA/[A-Z][a-z]{1,2})\s+(\d{1,5})/(\d{2,4})\b"
    r"|\b(C[‑–-]\d{1,4}/\d{2})\b"
    r"|\b(SK|K|P|U|Kp)\s+(\d{1,4})/(\d{2})\b(?=[^\n]{0,0})")
SN_TYPES = {"CSKP", "CSK", "CKN", "CK", "CZP", "CNP", "CSPP", "CO", "CZ", "CR", "PK", "PSK", "PSKP", "UK",
            "USK", "KK", "KZP", "KO", "NSNc", "NSNk", "NSNp", "NZP", "NSK"}
SA_TYPES = {"ACa", "ACz", "AGa", "AGz", "APa", "AUa"}

COURT_RE = re.compile(
    r"(?P<sn>\bSN\b|Sąd\w*\s+Najwyższ\w*)"
    # 2026-10-24: przy skrócie (SA/SO) „w/we” nieobowiązkowe — „SO Szczecin”, „SA Gdańsk” (P13); pełna nazwa nadal z „w”
    r"|(?P<sa>\bSA\b(?:\s+(?:w|we))?|Sąd\w*\s+Apelacyjn\w*\s+(?:w|we))\s+(?P<sacity>[A-ZŁŚŻŹ][a-ząćęłńóśźż]+(?:\s+[A-ZŁŚŻ][a-ząćęłńóśźż]+)?)"
    r"|(?P<so>\bSO\b(?:\s+(?:w|we))?|Sąd\w*\s+Okręgow\w*\s+(?:w|we))\s+(?P<socity>[A-ZŁŚŻŹ][a-ząćęłńóśźż]+)"
    r"|(?P<nsa>\bNSA\b|Naczeln\w*\s+Sąd\w*\s+Administracyjn\w*)"
    r"|(?P<wsa>\bWSA\b|Wojewódzk\w*\s+Sąd\w*\s+Administracyjn\w*)\s+(?:w|we)\s+(?P<wsacity>[A-ZŁŚŻŹ][a-ząćęłńóśźż]+)"
    r"|(?P<tsue>\bTSUE\b|Trybunał\w*\s+Sprawiedliwości)"
    r"|(?P<tk>\bTK\b|Trybunał\w*\s+Konstytucyjn\w*)")


def court_from_match(m: re.Match) -> str:
    if m.group("sn"):
        return "Sąd Najwyższy"
    if m.group("sa"):
        return f"Sąd Apelacyjny w {m.group('sacity')}"
    if m.group("so"):
        return f"Sąd Okręgowy w {m.group('socity')}"
    if m.group("nsa"):
        return "Naczelny Sąd Administracyjny"
    if m.group("wsa"):
        return f"Wojewódzki Sąd Administracyjny w {m.group('wsacity')}"
    if m.group("tsue"):
        return "TSUE"
    return "Trybunał Konstytucyjny"


def court_key(c: str | None) -> str:
    """Klucz porównania sądu: typ + rdzeń miasta (Łodzi/Łódź → łod)."""
    if not c:
        return ""
    c = c.lower()
    typ = ("sn" if "najwy" in c else "sa" if "apelac" in c else "so" if "okręg" in c else
           "nsa" if "naczel" in c else "wsa" if "wojew" in c else c[:6])
    city = re.search(r"\b(?:w|we)\s+(\w+)", c)
    city_s = unicodedata.normalize("NFKD", city.group(1))[:3] if city else ""
    city_s = "".join(ch for ch in city_s if not unicodedata.combining(ch))
    return f"{typ}:{city_s}"


def extract_judgments(text: str) -> list[dict]:
    res = []
    prev_end = 0
    for m in SIG_RE.finditer(text):
        if m.group(5):
            sig, typ = m.group(5).replace("‑", "-").replace("–", "-"), "TSUE"
        elif m.group(1):
            sig, typ = f"{m.group(1)} {m.group(2)} {m.group(3)}/{m.group(4)}", m.group(2)
        else:
            # sygnatury TK tylko z kontekstem „TK”/„Trybunał”
            if not re.search(r"TK|Trybuna", text[max(0, m.start() - 80):m.start()]):
                continue
            sig, typ = f"{m.group(6)} {m.group(7)}/{m.group(8)}", "TK"
        ls = text.rfind("\n", 0, m.start()) + 1
        back_from = max(ls, prev_end, m.start() - 220)
        before = text[back_from:m.start()]
        after = text[m.end():m.end() + 60].split("\n")[0]
        courts = list(COURT_RE.finditer(before))
        court = court_from_match(courts[-1]) if courts else None
        if not court:
            # 2026-10-24 (decyzja Adama nr 4): sąd podany tuż PO sygnaturze („VIII Gz 43/16, SO Szczecin”) — potrzebny
            # do porównania z kandydatami przy sygnaturze niejednoznacznej
            ca = COURT_RE.search(after)
            if ca and ca.start() < 12:
                court = court_from_match(ca)
        dates = [(d, parse_date(d)) for d in DATE_RE.finditer(before)]
        date = dates[-1][1] if dates else None
        if not date:
            da = DATE_RE.search(after)
            if da and da.start() < 30:
                date = parse_date(da)
        if not court:
            court = ("Sąd Najwyższy" if typ in SN_TYPES else "TSUE" if typ == "TSUE" else
                     "Sąd Apelacyjny (miasto niepodane)" if typ in SA_TYPES else None)
            court_src = "z typu sygnatury" if court else None
        else:
            court_src = "z tekstu"
        s, e = sentence_span(text, m.start(), m.end())
        res.append({"sygnatura": sig, "typ": typ, "sad_podany": court, "sad_zrodlo": court_src,
                    "data_podana": date, "kontekst": trim(text[s:e], LIMIT_KONTEKST),
                    # do słów kluczowych: cały akapit/punkt listy (teza bywa w zdaniu obok sygnatury)
                    "_ctx": text[ls:(text.find("\n", m.end()) if text.find("\n", m.end()) != -1 else len(text))]})
        prev_end = m.end()
    return res


def _strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", _html.unescape(s)).strip()


SAOS_PROBY = 3          # A4 (2026-10-24): awaria SAOS (HTTP ≠ 200, JSONDecodeError, timeout) ≠ „nie znaleziono”
SAOS_ODSTEP_S = 4.0


async def saos_search(client: httpx.AsyncClient, sig: str) -> list[dict] | None:
    """Wyroki o sygnaturze w SAOS. Zwraca listę (może być pusta = „nie znaleziono”) albo None = SAOS niedostępny
    po SAOS_PROBY próbach. Awaria jest informacją o źródle, nie o odpowiedzi modelu."""
    LICZNIKI["saos_search"] += 1
    items = None
    for proba in range(SAOS_PROBY):
        try:
            r = await client.get("https://www.saos.org.pl/api/search/judgments",
                                 params={"caseNumber": sig, "pageSize": 20})
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            items = r.json().get("items", [])
            break
        except Exception as e:
            LICZNIKI["saos_awarie"] = LICZNIKI.get("saos_awarie", 0) + 1
            print(f"  [SAOS] {sig}: {type(e).__name__} (próba {proba + 1}/{SAOS_PROBY})", file=sys.stderr, flush=True)
            if proba + 1 < SAOS_PROBY:
                await asyncio.sleep(SAOS_ODSTEP_S * (proba + 1))
    if items is None:
        return None
    out = []
    for it in items:
        nums = [c.get("caseNumber", "") for c in it.get("courtCases", [])]
        if not any(re.sub(r"\s+", " ", n).strip().lower() == sig.lower() for n in nums):
            continue
        court = None
        if it.get("courtType") == "SUPREME":
            court = "Sąd Najwyższy"
        else:
            court = ((it.get("division") or {}).get("court") or {}).get("name") or it.get("courtType")
        out.append({"zrodlo": "SAOS", "id": it.get("id"), "sad": court, "data": it.get("judgmentDate"),
                    "rodzaj": it.get("judgmentType")})
    return out


async def saos_text(client: httpx.AsyncClient, jid) -> str:
    LICZNIKI["saos_judgment"] += 1
    for proba in range(SAOS_PROBY):
        try:
            r = await client.get(f"https://www.saos.org.pl/api/judgments/{jid}")
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            return _strip_html(r.json().get("data", {}).get("textContent", ""))
        except Exception:
            if proba + 1 < SAOS_PROBY:
                await asyncio.sleep(SAOS_ODSTEP_S * (proba + 1))
    return ""


BRAMKA_BAZY = os.environ.get("INTERNAL_DB_GATEWAY_PATH", "")  # bramka wewnętrznej bazy orzeczeń, poza repozytorium


class WewnetrznaBazaDB:
    """Wewnętrzna baza orzeczeń WYŁĄCZNIE przez bramkę bramka_ro_poza_repo.query (parser SQL, read-only, ROLLBACK, maskowanie URL).
    2026-10-24: wcześniej moduł łączył się bezpośrednio przez psycopg — niezgodnie z regułą „tylko bramka”.
    URL nigdy nie jest wypisywany; wyjątki logowane typem."""

    def __init__(self):
        self.conn = None          # True = bramka dostępna i potwierdziła read-only
        self.error = None
        try:
            sys.path.insert(0, BRAMKA_BAZY)
            from bramka_ro_poza_repo import query, BramkaRoError
            self._query, self._err = query, BramkaRoError
            ro = query("SELECT current_setting('transaction_read_only'), current_setting('default_transaction_read_only')",
                       None, as_dict=False)
            if ro and tuple(ro[0]) == ("on", "on"):
                self.conn = True
            else:
                self.error = "bramka nie potwierdziła read-only"
        except Exception as e:  # bez treści wyjątku — bramka maskuje, ale i tak logujemy tylko typ
            self.conn, self.error = None, type(e).__name__

    def find(self, sig: str) -> list[dict]:
        if not self.conn:
            return []
        LICZNIKI["lexalpha"] += 1
        try:
            rows = self._query('SELECT id, "signatureMain", "decisionDate", court, "textRaw" FROM "Judgment" '
                               'WHERE "signatureMain" = %s LIMIT 20', (sig,), as_dict=False, timeout_ms=120_000)
        except Exception as e:
            self.error = type(e).__name__
            return []
        seen, out = set(), []
        for rid, s, d, court, txt in sorted(rows, key=lambda r: -len(r[4] or "")):
            k = (court, d.date().isoformat() if d else None)
            if k in seen:
                continue
            seen.add(k)
            out.append({"zrodlo": "baza wewnętrzna", "id": rid, "sad": court, "data": k[1], "_tekst": txt or ""})
        return out


def keyword_fragments(claim: str, text: str, sig: str) -> list[dict]:
    """Fragmenty tekstu orzeczenia z największą liczbą słów kluczowych z twierdzenia modelu
    (proste dopasowanie rdzeni 6-znakowych; bez oceny)."""
    claim = claim.replace(sig, " ")
    claim = DATE_RE.sub(" ", claim)
    keys = {w[:6] for w in re.findall(r"[a-ząćęłńóśźż]+", claim.lower())
            if len(w) >= 6 and w not in STOP and w[:6] not in {"sądu n", "wyroku", "najwyż", "wyrok"}}
    if not keys or not text:
        return []
    chunks = re.split(r"(?<=[.;])\s+", text)
    scored = []
    for i, ch in enumerate(chunks):
        ws = {w[:6] for w in re.findall(r"[a-ząćęłńóśźż]+", ch.lower()) if len(w) >= 6}
        hit = keys & ws
        if len(hit) >= 2:
            scored.append((len(hit), i, sorted(hit)))
    scored.sort(key=lambda x: (-x[0], x[1]))
    out = []
    for n, i, hit in scored[:3]:
        frag = " ".join(chunks[max(0, i - 0):i + 2])
        out.append({"trafienia": n, "slowa": hit, "fragment": trim(frag, 400)})
    return out


async def verify_judgment(client, db: WewnetrznaBazaDB, j: dict) -> dict:
    sig = j["sygnatura"]
    if j["typ"] == "TSUE":
        return {"status": "poza źródłami (TSUE: SAOS/baza wewnętrzna nie obejmują) — do sprawdzenia ręcznie", "flagi": ["poza_zrodlami"]}
    saos = await saos_search(client, sig)
    saos_down = saos is None                       # A4: awaria źródła, nie brak wyroku
    cands = list(saos or [])
    flagi = ["saos_niedostepny"] if saos_down else []
    gdzie = ["SAOS"] if cands else []
    want = court_key(j["sad_podany"]) if j["sad_podany"] and "niepodane" not in j["sad_podany"] else ""
    if saos_down or not cands or (want and not any(court_key(c["sad"]) == want for c in cands)):
        db_c = db.find(sig)
        if db_c:
            gdzie.append("baza wewnętrzna")
            cands += db_c
    if not cands:
        if saos_down:
            st = "SAOS niedostępny; nie znaleziono w bazie wewnętrznej" if db.conn else "SAOS niedostępny; wewnętrzna baza orzeczeń niedostępna"
            return {"status": st, "flagi": flagi}      # bez flagi nie_znaleziono — źródło zawiodło, nie model
        st = "nie znaleziono (SAOS, baza wewnętrzna)" if db.conn else "nie znaleziono (SAOS; wewnętrzna baza orzeczeń niedostępna)"
        return {"status": st, "flagi": ["nie_znaleziono"]}
    # ── wybór orzeczenia (A3, 2026-10-24): po sądzie/mieście i dacie podanych przez model ──
    typ_want = want.split(":")[0] if want else ("sa" if j["typ"] in SA_TYPES else "sn" if j["typ"] in SN_TYPES else "")
    miasto_podane = bool(want and ":" in want and want.split(":")[1])
    pool = [c for c in cands if court_key(c["sad"]) == want] if miasto_podane else []
    if not pool and typ_want:
        pool = [c for c in cands if court_key(c["sad"]).split(":")[0] == typ_want]
        if miasto_podane and pool:
            flagi.append("inny_sad")
    if not pool:
        pool = cands
        if want:
            flagi.append("inny_sad")
    if j["data_podana"]:
        z_data = [c for c in pool if c["data"] and c["data"][:10] == j["data_podana"]]
        if z_data:
            pool = z_data
    sady = {court_key(c["sad"]) for c in pool}
    if len(sady) > 1:
        # kilka różnych sądów pod tą samą sygnaturą, a model nie podał sądu/miasta ani daty rozstrzygającej
        for c in cands:
            c.pop("_tekst", None)
        # 2026-10-24 (decyzja Adama nr 4): lista ODRĘBNYCH wyroków-kandydatów (sąd, data; ten sam wyrok w SAOS
        # i baza wewnętrzna liczony raz, SAOS pierwszy) — weryfikator poparcia ocenia twierdzenie wobec każdego, gdy ≤ 4
        odrebne, widz = [], set()
        for c in sorted(pool, key=lambda c: c["zrodlo"] != "SAOS"):
            k = (court_key(c["sad"]), (c.get("data") or "")[:10])
            if k in widz:
                continue
            widz.add(k)
            odrebne.append({kk: c.get(kk) for kk in ("zrodlo", "id", "sad", "data")})
        opis = "; ".join(f"{c['sad'] or '?'} {c['data'][:10] if c.get('data') else '?'} ({c['zrodlo']})" for c in odrebne)
        return {"status": f"sygnatura niejednoznaczna ({len(odrebne)} wyroków: {opis})",
                "kandydaci": [{k: c.get(k) for k in ("zrodlo", "id", "sad", "data")} for c in cands],
                "kandydaci_odrebni": odrebne,
                "data_podana": j["data_podana"], "sad_podany": j["sad_podany"],
                "flagi": flagi + ["sygnatura_niejednoznaczna"]}
    # ten sam sąd: pierwszeństwo SAOS (tekst urzędowy), potem najdłuższy tekst z baza wewnętrzna (kolejność z find)
    pool.sort(key=lambda c: c["zrodlo"] != "SAOS")
    best = pool[0]
    if j["data_podana"] and best["data"] and best["data"][:10] != j["data_podana"]:
        flagi.append("inna_data")
    tekst = best.pop("_tekst", None)
    if tekst is None and best["zrodlo"] == "SAOS":
        tekst = await saos_text(client, best["id"])
    for c in cands:
        c.pop("_tekst", None)
    status = f"znaleziono ({', '.join(gdzie)})" + ("; SAOS niedostępny" if saos_down else "")
    return {"status": status, "wybrane": best,
            "kandydaci": [{k: c.get(k) for k in ("zrodlo", "id", "sad", "data")} for c in cands],
            "data_wyroku": best["data"][:10] if best.get("data") else None,
            "data_podana": j["data_podana"], "sad_wyroku": best["sad"], "sad_podany": j["sad_podany"],
            "poczatek_tekstu": trim(tekst or "", POCZATEK_WYROKU),
            "fragmenty_kluczowe": keyword_fragments(j["_ctx"], tekst or "", sig),
            "flagi": flagi}


# ───────────────────────── raport ─────────────────────────

def load_key(p: str) -> dict:
    files = sorted(f for f in (PYTANIA / "keys").glob(f"{p}_*.yaml"))
    if not files:
        raise SystemExit(f"brak klucza dla {p}")
    return yaml.safe_load(files[0].read_text())


def key_default_act(key: dict) -> dict | None:
    """Akt domyślny z klucza (A2, 2026-10-24): TYLKO gdy wszystkie akty w `podstawy_wymagane` (także akty spoza
    legal-cite, np. u.n.n.c.) to jeden akt; przy kilku aktach w podstawach wymaganych domyślnego aktu nie ma — bare
    „art. 8” w P04 mogło znaczyć u.n.n.c. albo k.p.a. (11 fałszywych T w biegu 24.10). Przy jednym akcie w podstawach
    wymaganych ten akt jest domyślny; gdy podstaw wymaganych brak — najczęstszy akt z podstaw dopuszczalnych."""
    def akty_z(f):
        txt = " ".join(str(x) for x in (key.get(f) or []))
        out = []
        for g in (extract_provisions(clean_markdown(txt)) if txt else []):
            for it in g["items"]:
                a = it["akt"] or it.get("akt_przed")
                if a and a.get("kod") != "DOMYSLNY":
                    out.append(a)
        return out
    wym = akty_z("podstawy_wymagane")
    if wym:
        idents = {act_identity(a) for a in wym}
        if len(idents) > 1:
            return None
        return next((a for a in wym if a.get("kod")), wym[0])
    return doc_default_act(extract_provisions(clean_markdown(" ".join(str(x) for x in (key.get("podstawy_dopuszczalne") or [])))))


def doc_default_act(groups: list[dict]) -> dict | None:
    cnt: dict[str, tuple[int, dict]] = {}
    for g in groups:
        for it in g["items"]:
            a = it["akt"]
            if a and a.get("kod") and a["kod"] != "DOMYSLNY":
                k = a["nazwa"]
                cnt[k] = (cnt.get(k, (0, a))[0] + 1, a)
    if not cnt:
        return None
    return max(cnt.values(), key=lambda x: x[0])[1]


def lc_citation(it: dict, code: str) -> str:
    unit = f" {it['kind']} {_norm_sup(it['unit'])}" if it["unit"] else ""
    return f"art. {_norm_sup(it['art'])}{unit} {code}"


async def build_report(p: str, system: str, db: WewnetrznaBazaDB, client: httpx.AsyncClient) -> dict:
    t0 = time.monotonic()
    key = load_key(p)
    data_stanu = str(key.get("data_stanu_prawnego"))
    path = PYTANIA / "answers" / p / f"{system}.md"
    text = clean_markdown(body_of_answer(path.read_text()))

    groups = extract_provisions(text)
    default = key_default_act(key)      # A2 (2026-10-24): bez rezerwowego domysłu z odpowiedzi (doc_default_act)
    przepisy, seen = [], set()
    acts_used: set[str] = set()
    for gi, g in enumerate(groups):
        s, e = g["ctx_span"]
        ctx = text[s:e]
        ls = text.rfind("\n", 0, g["start"]) + 1
        le = text.find("\n", g["end"])
        akapit = text[ls:(len(text) if le == -1 else le)]
        glowne_id = None
        for it in g["items"]:
            wprost = it["akt"] or it.get("akt_przed")
            if wprost and wprost.get("kod") == "DOMYSLNY":
                wprost = None
            # A2 (2026-10-24): akt domniemany z klucza tylko, gdy w zdaniu nie ma innego aktu, a gdy zdanie nie nazywa
            # żadnego aktu — także w akapicie; inaczej „akt nieustalony — do sprawdzenia ręcznie” (status, nie zarzut)
            nieustalony_powod = None
            if not wprost and default:
                inne_zd = other_acts(ctx, default)
                if inne_zd:
                    nieustalony_powod = f"w zdaniu inny akt: {', '.join(inne_zd[:3])}"
                elif not acts_in_text(ctx):
                    inne_ak = other_acts(akapit, default)
                    if inne_ak:
                        nieustalony_powod = f"w akapicie inny akt: {', '.join(inne_ak[:3])}"
            akt = wprost or (default if not nieustalony_powod else None)
            akt_src = ("wprost" if wprost else f"nieustalony ({nieustalony_powod})" if nieustalony_powod
                       else "domniemany (akt z podstaw klucza)" if default else "brak")
            jedn = f"art. {it['art']}" + (f" {it['kind']} {it['unit']}" if it["unit"] else "") + (f" pkt {it['pkt']}" if it["pkt"] else "")
            dedup = (jedn, akt["nazwa"] if akt else None, g["quote"] or "", ctx)
            if dedup in seen:
                continue
            seen.add(dedup)
            rola = it.get("rola", "główne")
            ent = {"id": len(przepisy) + 1, "powolanie": jedn + (f" {akt['napis']}" if akt and wprost else ""),
                   "akt": {"nazwa": akt["nazwa"] if akt else None, "kod_legal_cite": akt["kod"] if akt else None,
                           "ustalenie": akt_src},
                   "rola": rola, "grupa": gi + 1, "napis_grupy": g["napis"],
                   "kontekst": trim(ctx, LIMIT_KONTEKST), "cytat": g["quote"] if len(g["items"]) == 1 or it is g["items"][0] else None,
                   "flagi": []}
            if rola == "główne" or glowne_id is None:
                glowne_id = ent["id"]
            ent["powolanie_glowne_id"] = glowne_id
            if nieustalony_powod:
                ent["weryfikacja"] = {"status": "akt nieustalony — do sprawdzenia ręcznie", "powod": nieustalony_powod}
                ent["wersje"] = "wersje wcześniejsze: nieobsługiwane"
                ent["cytat_porownanie"] = {"wynik": "nie porównano"}
                ent["flagi"].append("akt_nieustalony")
                przepisy.append(ent)
                continue
            if not akt and not default:
                # bez aktu w zdaniu, a klucz nie daje jednego aktu domyślnego (kilka aktów w podstawach wymaganych)
                ent["weryfikacja"] = {"status": "akt nieustalony — do sprawdzenia ręcznie",
                                      "powod": "brak nazwy aktu przy powołaniu; klucz nazywa kilka aktów w podstawach wymaganych"}
                ent["akt"]["ustalenie"] = "nieustalony (brak aktu; klucz wieloaktowy)"
                ent["wersje"] = "wersje wcześniejsze: nieobsługiwane"
                ent["cytat_porownanie"] = {"wynik": "nie porównano"}
                ent["flagi"].append("akt_nieustalony")
                przepisy.append(ent)
                continue
            if not akt or not akt["kod"] or not (lc._resolve(akt["kod"], lc.PL_ACTS) or lc._resolve(akt["kod"], lc.EU_ACTS)):
                ent["weryfikacja"] = {"status": "nieobsługiwany — do sprawdzenia ręcznie"}
                ent["wersje"] = "wersje wcześniejsze: nieobsługiwane"
                ent["cytat_porownanie"] = {"wynik": "nie porównano"}
                ent["flagi"].append("nieobslugiwany")
                przepisy.append(ent)
                continue
            code = lc._resolve(akt["kod"], lc.PL_ACTS) or lc._resolve(akt["kod"], lc.EU_ACTS)
            acts_used.add(code)
            cit = lc_citation(it, code)
            ent["cytowanie_legal_cite"] = cit
            v = await verify_provision(cit, code, data_stanu)
            if v["status"] == "nie istnieje" and not wprost and not v.get("istniala_wczesniej"):
                # jednostki nie ma w akcie domniemanym → nie wiemy, o jaki akt chodziło (status, nie „nie istnieje”)
                ent["akt"]["ustalenie"] = "nieustalony (jednostki nie ma w akcie domniemanym)"
                ent["weryfikacja"] = {"status": "akt nieustalony — do sprawdzenia ręcznie",
                                      "powod": f"art. {it['art']} nie istnieje w akcie domniemanym ({akt['nazwa']})"}
                ent["wersje"] = "wersje wcześniejsze: nieobsługiwane"
                ent["cytat_porownanie"] = {"wynik": "nie porównano"}
                ent["flagi"].append("akt_nieustalony")
                przepisy.append(ent)
                continue
            w = {k: v[k] for k in ("status", "znacznik", "zrodlo", "aktualnosc", "komunikat", "uwagi", "uchylony") if k in v}
            # podstawa porównania: brzmienie NA DATĘ STANU PRAWNEGO (gdy legal-cite je ustaliło), inaczej dzisiejsze
            current = v.get("tekst_na_dzien") or v.get("tekst_pelny")
            if v.get("na_dzien"):
                nd = v["na_dzien"]
                w["brzmienie_na_dzien"] = {k: nd[k] for k in ("na_dzien", "status", "ustalenie", "zrodlo", "znacznik") if k in nd}
                if v.get("uchylony_na_dzien"):
                    w["uchylony_na_dzien"] = True
                if nd.get("ustalenie") == "nieustalone":
                    ent["flagi"].append("brzmienie_na_dzien_nieustalone")
            if current:
                w["fragment_urzedowy"] = trim(current, LIMIT_FRAGMENT)
            ent["weryfikacja"] = w
            olders = []
            ver = v.get("wersje")
            if ver:
                ent["wersje"] = {k: ver[k] for k in ("status", "tj", "data") if k in ver}
                if ver.get("tekst_pelny"):
                    olders.append(ver["tekst_pelny"])
                    ent["wersje"]["fragment_wczesniejszy"] = trim(ver["tekst_pelny"], LIMIT_FRAGMENT)
            else:
                ent["wersje"] = "wersje wcześniejsze: nieobsługiwane"
            if v.get("wersje_wczesniejsze") is not None:
                ent["wersje_na_dzien"] = [{k: x[k] for k in ("na_dzien", "status", "ustalenie", "komunikat") if k in x}
                                          | ({"fragment": trim(x["tekst_pelny"], LIMIT_FRAGMENT)} if x.get("tekst_pelny") else {})
                                          for x in v["wersje_wczesniejsze"]]
                olders += [x["tekst_pelny"] for x in v["wersje_wczesniejsze"] if x.get("tekst_pelny")]
            older = olders or None
            ent["cytat_porownanie"] = compare_quote(ent["cytat"], current, older)
            # sygnały pomocnicze (bez rozstrzygania): zbieżność słów kontekstu z tekstem urzędowym
            # i słowa występujące tylko w wersji wcześniejszej
            if current:
                cs = stems(re.sub(re.escape(g["napis"]), " ", ctx))
                ent["sygnaly"] = {"zbieznosc_kontekstu": round(len(cs & stems(current)) / max(1, len(cs)), 2)}
                if older:
                    only_old = set().union(*(stems(o) for o in (older if isinstance(older, list) else [older]))) - stems(current) - DOMENA
                    hits = sorted(cs & only_old)
                    if hits:
                        ent["sygnaly"]["slowa_wersji_wczesniejszej"] = hits
                        # 2026-10-23: dwa luźne, pospolite słowa („wady prawne … osób trzecich” przy art. 556 k.c.)
                        # to za mało — flaga przy ≥ 3 słowach albo gdy 2 słowa stoją obok siebie („rażącej dysproporcji”)
                        seq = [w[:5] for w in re.findall(r"[a-ząćęłńóśźż]+", ctx.lower()) if len(w) >= 5 and w not in STOP]
                        idx = [i for i, st in enumerate(seq) if st in only_old]
                        sasiednie = any(b - a == 1 for a, b in zip(idx, idx[1:]))
                        if len(hits) >= 3 or (len(hits) == 2 and sasiednie):
                            ent["flagi"].append("slowa_wersji_wczesniejszej")
                        else:
                            ent["sygnaly"]["slowa_wersji_wczesniejszej_slabe"] = True
            st = v["status"]
            if st == "nie istnieje":
                if v.get("istniala_wczesniej"):
                    # jednostka była w akcie przed datą stanu prawnego → uchylona/usunięta: kandydat W, nie F
                    ent["weryfikacja"]["istniala_wczesniej"] = v["istniala_wczesniej"]
                    ent["weryfikacja"]["status"] = f"nie istnieje na datę stanu prawnego (istniała na dzień {v['istniala_wczesniej']['na_dzien']})"
                    ent["flagi"].append("uchylony")
                else:
                    ent["flagi"].append("nie_znaleziono")      # akt wprost — jednostki nie ma (kandydat F)
            elif st.startswith("błąd"):
                ent["flagi"].append("blad_weryfikacji")
            elif st.startswith("nieobsługiwany"):
                ent["flagi"].append("nieobslugiwany")
            if v.get("uchylony_na_dzien") or (v.get("uchylony") and "tekst_na_dzien" not in v):
                ent["flagi"].append("uchylony")
            cw = ent["cytat_porownanie"]["wynik"]
            if cw.startswith("niedosłowny"):
                ent["flagi"].append("niedoslowny_zgodny_z_wersja_wczesniejsza"
                                    if ent["cytat_porownanie"].get("zgodny_z_wersja_wczesniejsza") else
                                    "niedoslowny_blizszy_wersji_wczesniejszej"
                                    if ent["cytat_porownanie"].get("blizszy_wersji_wczesniejszej") else "niedoslowny")
            przepisy.append(ent)

    orzeczenia = []
    for j in extract_judgments(text):
        dup = next((o for o in orzeczenia if o["sygnatura"] == j["sygnatura"]
                    and (o["sad_podany"], o["data_podana"]) == (j["sad_podany"], j["data_podana"])), None)
        if dup:
            dup["wzmianki"] = dup.get("wzmianki", 1) + 1
            continue
        v = await verify_judgment(client, db, j)
        j.pop("_ctx")
        orzeczenia.append({**j, "weryfikacja": v, "flagi": v.get("flagi", [])})

    publikatory = await check_publikatory(text, acts_used, data_stanu)
    daty = []
    for m in DATE_RE.finditer(text):
        d = parse_date(m)
        if d:
            s, e = sentence_span(text, m.start(), m.end())
            daty.append({"data": d, "napis": m.group(0), "kontekst": trim(text[s:e], 200)})

    flag_count: dict[str, int] = {}
    for coll in (przepisy, orzeczenia, publikatory):
        for x in coll:
            for f in x["flagi"]:
                flag_count[f] = flag_count.get(f, 0) + 1
    # pełne teksty tylko w pamięci, do raportu idą fragmenty
    return {
        "meta": {"pytanie": p, "system": system, "plik_odpowiedzi": str(path.relative_to(BENCH)),
                 "data_stanu_prawnego": data_stanu, "wygenerowano": dt.datetime.now().isoformat(timespec="seconds"),
                 "czas_s": round(time.monotonic() - t0, 1),
                 "zrodla": {"przepisy": "legal-cite (legal-cite (https://github.com/apiotrowski-afk/legal-cite-pl)) — najnowszy t.j./wersja skonsolidowana na dziś; "
                                         "wcześniejsze brzmienie tylko z poprzedniego t.j. w HTML",
                            "orzeczenia": "SAOS API; gdy brak — wewnętrzna baza orzeczeń (odczyt)"},
                 "uwaga": "raport faktów bez oceny merytorycznej; flagi to sygnały do sprawdzenia, nie rozstrzygnięcia"},
        "podsumowanie": {"przepisy": len(przepisy), "orzeczenia": len(orzeczenia), "publikatory": len(publikatory),
                         "daty": len(daty), "flagi": flag_count},
        "przepisy": przepisy, "orzeczenia": orzeczenia, "publikatory": publikatory, "daty": daty,
    }


def report_md(r: dict) -> str:
    m, s = r["meta"], r["podsumowanie"]
    L = [f"# Raport faktów — {m['pytanie']} · {m['system']}", "",
         f"Data stanu prawnego (klucz): {m['data_stanu_prawnego']} · wygenerowano {m['wygenerowano']} · {m['czas_s']} s",
         f"Powołania: przepisy {s['przepisy']}, orzeczenia {s['orzeczenia']}, publikatory {s['publikatory']}, daty {s['daty']}",
         f"Flagi: {', '.join(f'{k} {v}' for k, v in sorted(s['flagi'].items())) or 'brak'}", "",
         "## Przepisy", "", "| # | powołanie | akt | istnieje | cytat | wersje | flagi |", "|---|---|---|---|---|---|---|"]
    for p in r["przepisy"]:
        wer = p["wersje"] if isinstance(p["wersje"], str) else p["wersje"].get("status", "")
        rola = f" [{p['rola']} → #{p['powolanie_glowne_id']}]" if p.get("rola", "główne") != "główne" else ""
        L.append(f"| {p['id']} | {p['powolanie']}{rola} | {p['akt']['nazwa'] or '—'}{' (domn.)' if p['akt']['ustalenie'].startswith('domn') else ''} "
                 f"| {p['weryfikacja']['status']} | {p['cytat_porownanie']['wynik']} | {trim(wer, 70)} | {', '.join(p['flagi']) or '—'} |")
    L += ["", "## Orzeczenia", "", "| sygnatura | sąd podany | data podana | wynik | sąd w źródle | data w źródle | flagi |",
          "|---|---|---|---|---|---|---|"]
    for o in r["orzeczenia"]:
        v = o["weryfikacja"]
        L.append(f"| {o['sygnatura']} | {o['sad_podany'] or '—'} | {o['data_podana'] or '—'} | {v['status']} "
                 f"| {v.get('sad_wyroku') or '—'} | {v.get('data_wyroku') or '—'} | {', '.join(o['flagi']) or '—'} |")
    if r["publikatory"]:
        L += ["", "## Publikatory", ""]
        for p in r["publikatory"]:
            L.append(f"- {p['napis']} — {p.get('ocena', '')}{' · flagi: ' + ', '.join(p['flagi']) if p['flagi'] else ''}")
    L += ["", "Szczegóły (fragmenty urzędowe, początki orzeczeń, fragmenty ze słowami kluczowymi): plik JSON obok.", ""]
    return "\n".join(L)


async def main_async(args):
    RAPORTY.mkdir(exist_ok=True)
    systems = args.systemy.split(",") if args.systemy else SYSTEMY_R3
    db = WewnetrznaBazaDB()
    if not db.conn:
        print(f"[fakty] wewnętrzna baza orzeczeń niedostępna ({db.error}) — orzeczenia tylko z SAOS", file=sys.stderr)
    out_dir = Path(args.katalog) if args.katalog else RAPORTY
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    async with httpx.AsyncClient(timeout=30, follow_redirects=True,
                                 headers={"User-Agent": "ktzr-lexalpha-fakty/0.1"}) as client:
        for p in args.pytania:
            for s in systems:
                if not (PYTANIA / "answers" / p / f"{s}.md").exists():
                    print(f"[fakty] brak odpowiedzi {p}/{s}", file=sys.stderr)
                    continue
                r = await build_report(p, s, db, client)
                (out_dir / f"{p}_{s}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1))
                (out_dir / f"{p}_{s}.md").write_text(report_md(r))
                print(f"[fakty] {p} {s}: przepisy {r['podsumowanie']['przepisy']}, orzeczenia "
                      f"{r['podsumowanie']['orzeczenia']}, flagi {r['podsumowanie']['flagi']} ({r['meta']['czas_s']} s)")
    print(f"[fakty] razem {round(time.monotonic() - t0, 1)} s; zapytania: {LICZNIKI}")


def main():
    ap = argparse.ArgumentParser(description="Krok faktów meta-sędziego (prototyp)")
    ap.add_argument("pytania", nargs="+", help="np. P09 P10")
    ap.add_argument("--systemy", help="lista systemów po przecinku (domyślnie 16 systemów r3)")
    ap.add_argument("--katalog", help="katalog wyjściowy raportów (domyślnie meta_sedzia/raporty)")
    asyncio.run(main_async(ap.parse_args()))


if __name__ == "__main__":
    main()
