#!/usr/bin/env python3
"""Automatyczny ekstraktor błędów A6 z kart ocen (pytania/oceny/<P>_<system>.md) — meta-sędzia, test 2026-10-23.

Zastępuje ręcznie spisane listy WZORZEC_T / WZORZEC_B9 / WZORZEC_INNE (poparcie.py) i A6 (porownaj_fakty.py).
Z wiersza „| A6 |” karty wyciąga:
  - powołania oznaczone jako błąd z klasą F/T/W/S (wzorce: „**T**”, „**T nr 1**”, „**T (2)**”, „**T — art. 41 ust. 1 pr.aut.**”,
    „**art. 50 ust. 1 — T**”, „1 → 0: … = W”, dawne „**O nr 1**” przeliczone na T w nagłówku wiersza),
    a także z wiersza „**Δ …” („hallucinated: tak (T — art. 24 § 2 k.w.; …)”);
  - ogólniki B9 (fraza „ogólnik” / „reguła 7” z klasą T albo z decyzją B9) — bez powołania;
  - powołania zweryfikowane „✓” jako poprawne;
  - etykietę hallucinated z wiersza „**Δ”.
Karta niejednoznaczna (liczba wyciągniętych błędów ≠ liczba klas w A6_typ, marker bez powołania, klasa O bez przeliczenia)
→ pole „do_recznego_sprawdzenia” z powodem. Ekstraktor NIE zgaduje: brak powołania zostaje brakiem.

Użycie:
  python -I bledy_z_kart.py P09 P10 [--systemy a,b] [--json wyjscie.json] [--sprawdz-p09p10]
  --sprawdz-p09p10: porównanie z ręcznymi listami (porownaj_fakty.A6, poparcie.WZORZEC_*), wypisuje różnice.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
OCENY = HERE.parent / "pytania" / "oceny"

SYSTEMY_R3 = [
    "chatgpt_codex_w0_r3", "chatgpt_codex_web_r3", "codex_astra6_w0_r3", "codex_astra6_web_r3",
    "codex_terra56_w0_r3", "codex_terra56_web_r3", "haiku_cli_w0_r3", "haiku_cli_w1_r3",
    "sonnet_cli_w0_r3", "sonnet_cli_w1_r3", "opus_cli_w0_r3", "opus_cli_w1_r3",
    "gemini38flash_vertex_w0_r3", "gemini38flash_vertex_w1_r3",
    "argon4_high_vertex_w0_r3", "argon4_high_vertex_w1_r3",
]

SUP = "¹²³⁴⁵⁶⁷⁸⁹⁰"
SUP_LET = "ᵃᵇᶜᵈᵉ"
_SUP_MAP = {ord(c): str("1234567890"["¹²³⁴⁵⁶⁷⁸⁹⁰".index(c)]) for c in SUP}
_SUP_MAP.update({ord(c): "abcde"[SUP_LET.index(c)] for c in SUP_LET})

# ───────────────────────── akty (skróty w kartach → kod) ─────────────────────────
AKTY = [
    (r"k\.?\s?p\.?\s?c\.|KPC\b|Kodeks\w* postępowania cywilnego", "KPC"),
    (r"k\.?\s?p\.?\s?k\.|KPK\b|Kodeks\w* postępowania karnego", "KPK"),
    (r"k\.?\s?p\.?\s?a\.|KPA\b|Kodeks\w* postępowania administracyjnego", "KPA"),
    (r"p\.?\s?p\.?\s?s\.?\s?a\.|PPSA\b", "PPSA"),
    (r"k\.?\s?k\.?\s?s\.|KKS\b", "KKS"),
    (r"k\.?\s?r\.?\s?o\.|KRO\b|Kodeks\w* rodzinn\w*", "KRO"),
    (r"k\.c\.|KC\b|Kodeks\w* cywiln\w*", "KC"),
    (r"k\.k\.|KK\b|Kodeks\w* karn\w*", "KK"),
    (r"k\.w\.|KW\b|Kodeks\w* wykroczeń", "KW"),
    (r"k\.p\.|KP\b|Kodeks\w* pracy", "KP"),
    (r"pr\.\s?aut\.|PrAut\b|PAut\b|u\.?p\.?a\.?p\.?p\.|prawa autorskiego|prawie autorskim", "PrAut"),
    (r"u\.k\.s\.c\.|ustaw\w* o kosztach sądowych", "u.k.s.c."),
    (r"u\.k\.w\.h\.|ustaw\w* o księgach wieczystych", "u.k.w.h."),
    (r"u\.k\.k\.|ustaw\w* o kredycie konsumenckim", "u.k.k."),
    (r"u\.TK\b|ustaw\w* o (?:organizacji i trybie postępowania przed )?Trybunale", "u.TK"),
    (r"AI Act|AIA\b|rozporządzeni\w* (?:\(UE\) )?2024/1689", "AI Act"),
    (r"RODO", "RODO"),
    (r"p\.u\.s\.p\.", "p.u.s.p."),
    (r"ustaw\w* (?:z \d{1,2}\.\d{1,2}\.\d{4} )?o nabywaniu nieruchomości", "u.n.n.c."),
    (r"ustaw\w* o doręczeniach elektronicznych|u\.d\.e\.", "u.d.e."),
    (r"ustaw\w*(?: z [^,;)]{0,30})? o [a-ząćęłńóśźż]+(?: [a-ząćęłńóśźż]+){0,5}", "ustawa (inna)"),
]
AKT_RE = re.compile(r"\s*(?:" + "|".join(f"(?P<a{i}>{p})" for i, (p, _) in enumerate(AKTY)) + r")")

NUM = rf"\d+[a-z]?(?:[{SUP}]+[{SUP_LET}]?)?(?:\^\d+)?"
CIT_RE = re.compile(
    rf"art\.\s*(?P<art>{NUM})"
    rf"(?:\s*(?P<kind>§|ust\.)\s*(?P<unit>{NUM})(?:\s*[–-]\s*(?P<unit2>{NUM}))?)?"
    rf"(?:\s*(?:pkt|lit\.)\s*(?P<pkt>\w+))?"
    rf"(?:\s*zd\.\s*\d)?")
SIG_RE = re.compile(
    r"\b([IVX]{1,4})\s+(CSKP|CSK|CKN|CK|CZP|CNP|CZ|CO|CR|ACa|ACz|AGa|AGz|APa|AUa|Ca|Cz|Ga|Gz|GC|C|Nc|Ns|PK|UK|KK|KZP|KO|OSK|FSK|GSK|SA/[A-Z][a-z]{1,2})\s+(\d{1,5})/(\d{2,4})\b")

# bold-markery klas. (1) „T”, „T nr 1”, „T (2)”, „T — art. …”, „S-niepotwierdzone”, „W i T”;
# (2) „art. 50 ust. 1 — T”, „historia progu — W i T”, „… — F”
MARK1 = re.compile(r"^([FTWSO])(?:[-–]niepotwierdzone)?(?:\s+i\s+([FTWSO]))?(?:\s*(?:nr\s*\d+|\(\d+\)))?\s*(?:[—–:-]\s*(.*))?$", re.S)
MARK2 = re.compile(r"^(.*?)\s*[—–-]\s*([FTWSO])(?:\s+i\s+([FTWSO]))?(?:[-–]niepotwierdzone)?(?:\s*\(.*\))?$", re.S)
# decyzja Adama w nagłówku wiersza: „1 → 0: założenie … = W, poboczne”
DECYZJA = re.compile(r"[01½]\s*→\s*0:\s*(.+?)\s*=\s*([FTWS])\b"
                     r"|(art\.[^;\]]{0,90}?przypisano[^;\]]{0,120}?),?\s+to\s+([FTWS])\b")
# wiersz Δ: „(T — art. 24 § 2 k.w.; zakres poboczne)”, „W — art. 278a k.k.; T — art. 278 § 1 k.k.”
DELTA_ERR = re.compile(r"(?<![\w])([FTWS])\s*[—–-]\s*([^;)\]]+)")
SENTINEL = re.compile(r"Zgodne\b|✓:|Bez klasy|Orzeczeń (?:z sygnaturą )?nie powołano|Do decyzji Adama|Pozostałe|Uwagi bez wpływu|"
                      r"Niesprawdzone|Ogólnik|Najgorszy przypadek|Soft law|Orzeczenia \(|Historia progu ✓|\[20\d\d-\d\d-\d\d")

OGOLNIK = re.compile(r"ogólnik|reguł[aę] 7|B9", re.I)


def norm_num(s: str) -> str:
    """„131¹ᵃ” → „1311a”, „394²” → „3942”, „1^2” → „12”."""
    s = (s or "").translate(_SUP_MAP).replace("^", "")
    return s.lower().strip()


def act_code(text: str) -> str | None:
    m = AKT_RE.match(text)
    if not m:
        return None
    for i, (_, kod) in enumerate(AKTY):
        if m.group(f"a{i}"):
            return kod
    return None


def citations(text: str) -> list[dict]:
    out = []
    for m in CIT_RE.finditer(text):
        if re.search(r"(?:Dz\.\s?U\.|poz\.\s*\d+|ustaw\w* z \d{1,2}\.\d{1,2}\.\d{4})[^.;]{0,25}$", text[max(0, m.start() - 45):m.start()]):
            continue   # jednostka aktu zmieniającego w opisie historii („…, Dz.U. 2018 poz. 2077, art. 1 pkt 7”)
        after = text[m.end():m.end() + 90]
        kod = act_code(after)
        units = [m.group("unit")] if m.group("unit") else [None]
        if m.group("unit2") and m.group("unit") and m.group("unit").isascii() and m.group("unit").isdigit() and m.group("unit2").isascii() and m.group("unit2").isdigit():
            a, b = int(m.group("unit")), int(m.group("unit2"))
            if 0 < b - a <= 5:
                units = [str(u) for u in range(a, b + 1)]   # „§ 1–2” → § 1 i § 2
        for u in units:
            out.append({"rodzaj": "przepis", "napis": m.group(0).strip(), "art": norm_num(m.group("art")),
                        "jednostka": norm_num(u) if u else None,
                        "kind": m.group("kind"), "pkt": m.group("pkt"), "akt": kod, "start": m.start(), "end": m.end()})
    for m in SIG_RE.finditer(text):
        out.append({"rodzaj": "orzeczenie", "napis": m.group(0), "sygnatura": re.sub(r"\s+", " ", m.group(0)),
                    "start": m.start(), "end": m.end()})
    out.sort(key=lambda c: c["start"])
    return out


def first_quote_cits(seg: str) -> list[dict]:
    """Powołania z pierwszego cytatu „…” segmentu (tam zwykle stoi błędne powołanie); gdy brak cytatu — pierwsze powołanie."""
    seg2 = seg.lstrip(" :—–-")
    m = re.match(r"„([^”]{1,400})”", seg2)
    if m:
        c = citations(m.group(1))
        if c:
            return c[:3]
    c = citations(seg)
    return c[:1]


def a6_typ(row: str) -> tuple[list[str] | None, str]:
    """Pierwsza (aktualna) lista A6_typ w wierszu; „brak…”/„—” → []. Zwraca (klasy, surowy napis)."""
    m = re.search(r"A6_typ:\s*(\[[^\]]*\]|brak[^.;·]*|—|pusta|brak_powolan)((?:\s*→\s*(?:\[[^\]]*\]|brak[^.;·(]*))*)", row)
    if not m:
        return None, ""
    raw = m.group(1)
    if m.group(2):   # „[W, T] → [T]” — liczy się ostatni człon
        raw = re.findall(r"\[[^\]]*\]|brak[^.;·(]*", m.group(2))[-1].strip()
    if not raw.startswith("["):
        return [], raw
    kl = [re.sub(r"[-–]niepotwierdzone", "", x.strip()) for x in raw.strip("[]").split(",") if x.strip()]
    return kl, raw


def parse_card(path: Path) -> dict:
    text = path.read_text()
    row = next((ln for ln in text.splitlines() if ln.startswith("| A6 |")), None)
    delta = next((ln for ln in text.splitlines() if ln.startswith("**Δ")), "")
    res = {"plik": path.name, "a6_pkt": None, "a6_typ": None, "hallucinated": None, "bledy": [], "poprawne": [],
           "ogolniki_b9": [], "do_recznego_sprawdzenia": []}
    if not row:
        res["do_recznego_sprawdzenia"].append("brak wiersza A6")
        return res
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    res["a6_pkt"] = cells[1] if len(cells) > 1 else None
    body = cells[2] if len(cells) > 2 else ""
    typ, typ_raw = a6_typ(body)
    res["a6_typ"] = typ
    mh = re.search(r"hallucinated:\s*(tak|nie)", delta)
    res["hallucinated"] = mh.group(1) if mh else None
    if not mh:
        res["do_recznego_sprawdzenia"].append("brak etykiety hallucinated w wierszu Δ")

    # ── markery błędów (bold) ──
    marks = []
    for m in re.finditer(r"\*\*([^*]{1,160})\*\*", body):
        c = m.group(1).strip()
        m1 = MARK1.match(c)
        m2 = MARK2.match(c) if not m1 else None
        if m1:
            klasy = [k for k in (m1.group(1), m1.group(2)) if k]
            marks.append({"klasy": klasy, "w_markerze": m1.group(3) or "", "start": m.start(), "end": m.end()})
        elif m2 and (citations(m2.group(1)) or re.search(r"historia|ustawa|nowel|data", m2.group(1), re.I)):
            klasy = [k for k in (m2.group(2), m2.group(3)) if k]
            marks.append({"klasy": klasy, "w_markerze": m2.group(1), "start": m.start(), "end": m.end()})
    for m in DECYZJA.finditer(body):
        kl, opis = (m.group(2), m.group(1)) if m.group(2) else (m.group(4), m.group(3))
        marks.append({"klasy": [kl], "w_markerze": opis, "start": m.start(), "end": m.end(), "decyzja": True})
    marks.sort(key=lambda x: x["start"])

    zniesione = [(m.group(1), c) for m in re.finditer(r"\b([FTWS]) za ([^—;·()]*?) zniesion", body) for c in citations(m.group(2))]

    # ── segmenty i powołania ──
    for i, mk in enumerate(marks):
        seg_end = marks[i + 1]["start"] if i + 1 < len(marks) else len(body)
        seg = body[mk["end"]:seg_end]
        ms = SENTINEL.search(seg)
        if ms:
            seg = seg[:ms.start()]
        # pierwszy ✓ po pierwszym powołaniu kończy segment (dalej idą powołania zgodne)
        mc = re.search(r"✓", seg)
        if mc:
            c0 = citations(seg[:mc.start()])
            if c0:
                seg = seg[:mc.start()]
        cits = citations(mk["w_markerze"])[:3] if mk["w_markerze"] else []
        zrodlo = "marker"
        if not cits and not mk.get("decyzja"):
            przed = body[max(0, mk["start"] - 60):mk["start"]]
            cp = citations(przed)
            if cp and re.fullmatch(r"[\s—–:(-]*", przed[cp[-1]["end"]:]):
                cits, zrodlo = [cp[-1]], "przed markerem"
        if not cits and not mk.get("decyzja"):
            cits = first_quote_cits(seg)
            zrodlo = "segment"
        for kl in mk["klasy"]:
            if any(kl == zk and any(c.get("art") == zc["art"] and c.get("jednostka") in (None, zc["jednostka"]) for c in cits)
                   for zk, zc in zniesione):
                res["do_recznego_sprawdzenia"].append(f"klasa {kl} ({cits[0]['napis']}) zniesiona decyzją — pominięta")
                continue
            if kl != "O" and typ and kl not in typ and len(set(typ)) == 1:
                res["do_recznego_sprawdzenia"].append(f"klasa {kl} markera spoza A6_typ {typ} — przyjęto {typ[0]}")
                kl = typ[0]
            if kl == "O":
                # dawne O: liczy się tylko, gdy nagłówek przeliczył je na T (A6_typ aktualne bez O)
                if typ and "O" not in typ and "T" in typ:
                    kl = "T"
                    res["do_recznego_sprawdzenia"].append(f"klasa O przeliczona na T ({trim(mk['w_markerze'] or seg, 60)})")
                else:
                    continue
            if cits:
                for c in cits:
                    res["bledy"].append({"klasa": kl, **{k: v for k, v in c.items() if k not in ("start", "end")}, "zrodlo": zrodlo})
            else:
                opis = trim(mk["w_markerze"] or seg, 100)
                if OGOLNIK.search(mk["w_markerze"] + " " + seg[:200]):
                    res["ogolniki_b9"].append({"klasa": kl, "opis": opis})
                else:
                    res["bledy"].append({"klasa": kl, "rodzaj": "bez_powolania", "napis": None, "opis": opis, "zrodlo": zrodlo})
                    res["do_recznego_sprawdzenia"].append(f"marker {kl} bez powołania: {opis}")

    # ── ogólniki B9 oznaczone w nagłówku (decyzja B9) — tylko gdy liczba klas w A6_typ przewyższa wyciągnięte błędy ──
    if (re.search(r"decyzja Adama nr 1 \(B9\)|dodane T za ogólnik|ogólnik[^.]{0,80}sprzeczn", body) and not res["ogolniki_b9"]
            and typ and len(typ) > len(res["bledy"])):
        res["ogolniki_b9"].append({"klasa": "T", "opis": "ogólnik B9 wg nagłówka wiersza A6"})
    # A6 = 1/1 (np. B9 wycofane 2026-10-23): markery w wierszu są historyczne — nie liczą się jako błędy karty
    if res["a6_pkt"] and res["a6_pkt"].startswith("1/") and (res["bledy"] or res["ogolniki_b9"]):
        res["historyczne"] = res["bledy"] + res["ogolniki_b9"]
        res["bledy"], res["ogolniki_b9"] = [], []
        res["do_recznego_sprawdzenia"].append("A6 1/1, a w wierszu markery błędów — potraktowane jako historyczne")

    # ── klasy zniesione decyzją („W za art. 41 ust. 2 zniesione — tylko A3”) ──
    if re.search(r"\bT za (?:ogólnik|tezę o)", body) and typ and len(typ) > len(res["bledy"]) and not res["ogolniki_b9"]:
        res["ogolniki_b9"].append({"klasa": "T", "opis": "ogólnik B9 wg nagłówka wiersza A6 („T za ogólnik”)"})

    # ── uzupełnienie z wiersza Δ ──
    mpar = re.search(r"hallucinated:\s*tak\s*(\(.*)", delta)
    if mpar:
        for m in DELTA_ERR.finditer(mpar.group(1)[:600]):
            kl, opis = m.group(1), m.group(2).strip()
            cits = citations(opis)
            if not cits:
                continue
            for c in cits[:3]:
                key = (kl, c.get("art"), c.get("jednostka"), c.get("sygnatura"))
                if any((b["klasa"], b.get("art"), b.get("jednostka"), b.get("sygnatura")) == key for b in res["bledy"]):
                    continue
                # marker tej klasy bez powołania → uzupełnienie
                puste = next((b for b in res["bledy"] if b["klasa"] == kl and b["rodzaj"] == "bez_powolania"), None)
                if puste:
                    puste.update({k: v for k, v in c.items() if k not in ("start", "end")}, zrodlo="Δ")
                    res["do_recznego_sprawdzenia"] = [x for x in res["do_recznego_sprawdzenia"] if not x.startswith(f"marker {kl} bez")]
                else:
                    res["bledy"].append({"klasa": kl, **{k: v for k, v in c.items() if k not in ("start", "end")}, "zrodlo": "Δ"})

    # Δ: błędy bez powołania (orzeczenie bez sygnatury, data noweli) — gdy klas w A6_typ jest więcej niż wyciągniętych błędów
    if mpar and typ and len(typ) > len(res["bledy"]) + len(res["ogolniki_b9"]):
        for m in DELTA_ERR.finditer(mpar.group(1)[:600]):
            kl, opis = m.group(1), m.group(2).strip()
            if not citations(opis) and kl in typ and not any(b["klasa"] == kl for b in res["bledy"]):
                res["bledy"].append({"klasa": kl, "rodzaj": "bez_powolania", "napis": None, "opis": trim(opis, 100), "zrodlo": "Δ"})
                res["do_recznego_sprawdzenia"].append(f"błąd {kl} bez powołania (Δ): {trim(opis, 60)}")
    # powtórzenia (ten sam błąd opisany dwa razy)
    uniq, seen = [], set()
    for b in res["bledy"]:
        k = (b["klasa"], b.get("art"), b.get("jednostka"), b.get("sygnatura"), b.get("opis"))
        if k not in seen:
            seen.add(k); uniq.append(b)
    res["bledy"] = uniq

    # ── powołania zgodne (✓) ──
    err_spans = [(mk["start"], (marks[i + 1]["start"] if i + 1 < len(marks) else len(body))) for i, mk in enumerate(marks)]
    cits_all = citations(body)
    for i, c in enumerate(cits_all):
        nxt = cits_all[i + 1]["start"] if i + 1 < len(cits_all) else len(body)
        window = body[c["end"]:min(nxt, c["end"] + 160)]
        before = body[max(0, c["start"] - 3):c["start"]]
        ok = "✓" in window or "✓" in before
        if not ok:
            continue
        if any(b.get("art") == c.get("art") and (b.get("jednostka") in (None, c.get("jednostka"))) and b["klasa"] in "FTWS"
               for b in res["bledy"] if b["rodzaj"] == "przepis") and c["rodzaj"] == "przepis":
            continue   # ten sam przepis jest w błędach — nie liczymy go jako ✓
        if any(b.get("sygnatura") == c.get("sygnatura") for b in res["bledy"] if b["rodzaj"] == "orzeczenie") and c["rodzaj"] == "orzeczenie":
            continue
        res["poprawne"].append({k: v for k, v in c.items() if k not in ("start", "end")})

    # ── kontrola spójności ──
    n_bl = len({(b["klasa"], b.get("napis") or b.get("opis")) for b in res["bledy"]}) + len(res["ogolniki_b9"])
    if typ is None:
        res["do_recznego_sprawdzenia"].append("brak pola A6_typ")
    elif typ and len(typ) != n_bl:
        res["do_recznego_sprawdzenia"].append(f"A6_typ {typ_raw} ma {len(typ)} klas, wyciągnięto {n_bl} błędów")
    elif not typ and n_bl:
        res["do_recznego_sprawdzenia"].append(f"A6_typ „{typ_raw}”, a wyciągnięto {n_bl} błędów")
    if res["hallucinated"] == "tak" and res["a6_pkt"] and res["a6_pkt"].startswith("1/"):
        res["do_recznego_sprawdzenia"].append("hallucinated: tak przy A6 1/1")
    return res


def trim(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


# ───────────────────────── kontrola na P09/P10 ─────────────────────────

def check_p09p10(cards: dict) -> list[str]:
    sys.path.insert(0, str(HERE))
    src = (HERE / "porownaj_fakty.py").read_text()
    ns: dict = {}
    exec(re.search(r"A6 = \[.*?\n\]", src, re.S).group(0), ns)   # tylko stała A6 (bez uruchamiania main)
    manual = ns["A6"]
    out = ["# Kontrola ekstraktora na P09/P10 (ręczna lista porownaj_fakty.A6 = 30 pozycji)", ""]
    found, missing, extra = 0, [], []
    seen_auto = set()
    for (p, s, kl, rodz, pat) in manual:
        card = cards.get((p, s))
        if not card:
            missing.append(f"{p} {s}: brak karty"); continue
        hit = None
        if pat[0] == "g":
            hit = next((g for g in card["ogolniki_b9"]), None)
        elif pat[0] == "o":
            hit = next((b for b in card["bledy"] if b.get("sygnatura") == pat[1]), None)
        else:
            arts = [norm_num(a) for a in pat[1].split("|")]
            hit = next((b for b in card["bledy"] if b.get("art") in arts and (pat[2] is None or b.get("jednostka") == pat[2])
                        and b["klasa"] == kl), None)
        if hit:
            found += 1
            seen_auto.add((p, s, id(hit)))
        else:
            missing.append(f"{p} {s} {kl} {rodz} {pat[1:]}: NIE odtworzone; auto: "
                           + "; ".join(f"{b['klasa']} {b.get('napis') or b.get('opis')}" for b in card["bledy"]) + f"; B9: {len(card['ogolniki_b9'])}")
    for (p, s), card in sorted(cards.items()):
        if p not in ("P09", "P10"):
            continue
        for b in card["bledy"]:
            if (p, s, id(b)) not in seen_auto:
                extra.append(f"{p} {s}: nadmiarowe {b['klasa']} {b.get('napis') or b.get('opis')} (źródło {b['zrodlo']})")
        for g in card["ogolniki_b9"]:
            if not any(rp == p and rs == s and pat[0] == "g" for (rp, rs, _, _, pat) in manual):
                extra.append(f"{p} {s}: nadmiarowy ogólnik B9 „{g['opis']}”")
    out.append(f"Odtworzone: {found}/{len(manual)}; brakujące: {len(missing)}; nadmiarowe: {len(extra)}")
    out += [""] + [f"- {x}" for x in missing] + [""] + [f"- {x}" for x in extra]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pytania", nargs="+")
    ap.add_argument("--systemy", default=",".join(SYSTEMY_R3))
    ap.add_argument("--json")
    ap.add_argument("--sprawdz-p09p10", action="store_true")
    args = ap.parse_args()
    cards = {}
    for p in args.pytania:
        for s in args.systemy.split(","):
            f = OCENY / f"{p}_{s}.md"
            if f.exists():
                cards[(p, s)] = parse_card(f)
    n_err = sum(len(c["bledy"]) for c in cards.values())
    n_ok = sum(len(c["poprawne"]) for c in cards.values())
    n_amb = sum(1 for c in cards.values() if c["do_recznego_sprawdzenia"])
    print(f"karty: {len(cards)}; błędy z powołaniem/bez: {n_err}; ogólniki B9: {sum(len(c['ogolniki_b9']) for c in cards.values())}; "
          f"✓: {n_ok}; kart do ręcznego sprawdzenia: {n_amb}")
    for (p, s), c in sorted(cards.items()):
        bl = "; ".join(f"{b['klasa']} {b.get('napis') or b.get('opis')}" + (f" [{b['akt']}]" if b.get('akt') else "") for b in c["bledy"])
        print(f"{p} {s:28} A6 {c['a6_pkt']} typ {c['a6_typ']} hal {c['hallucinated']} | {bl or '—'} | B9 {len(c['ogolniki_b9'])} | ✓ {len(c['poprawne'])}"
              + (f" | ?? {' / '.join(c['do_recznego_sprawdzenia'])}" if c["do_recznego_sprawdzenia"] else ""))
    if args.sprawdz_p09p10:
        print("\n".join(check_p09p10(cards)))
    if args.json:
        Path(args.json).write_text(json.dumps({f"{p}|{s}": c for (p, s), c in cards.items()}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
