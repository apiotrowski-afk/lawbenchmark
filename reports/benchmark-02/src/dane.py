"""Dane do raportu „LexAlpha Lab · Benchmark 02 · pytania prawne” (wersja 1.0 z 27.10.2026; karty w stanie z 25.10.2026).

Czyta wyłącznie pliki benchmarku: karty ocen (pytania/oceny/<P>_<system>.md), klucze (pytania/klucze/*.yaml),
koszt na odpowiedź (benchmark/koszt_2026-10-18_odpowiedzi.csv, cennik z 2026-10-18), oceny sędziów-modeli
(pytania/oceny/_sedziowie/*.json). Wynik: tabele markdown w słowniku TABELE i liczby w słowniku LICZBY,
używane przez build.py. Nic nie zapisuje poza dane.json obok skryptu.

Zasady parsowania:
- etykieta hallucinated karty: OSTATNIA linia zaczynająca się od „**Δ”, wzorzec
  hallucinated:\\s*\\**\\s*(?:(?:tak|nie)\\s*→\\s*\\**)?(tak|nie);
- A %, B %: wiersze sum „| **A** |” i „| **B** |” (jak tools/zestawienie_tier.py);
- poprawnie ugruntowana: A6 = 1/1 i A-R = 2/2 (README, „Koszt”);
- A6_typ i A6_zakres: wartość bieżąca z wiersza A6 (przy zapisie „X → Y” bierzemy Y);
- kontrola: średnie A %, B % i liczba hallucinated per system muszą się zgadzać z wyjściem
  zestawienie_tier.py --tylko <10 pytań>; przy niezgodności skrypt przerywa.
Użycie: python3 -I dane.py
"""
import collections
import csv
import glob
import json
import os
import re
import subprocess

import yaml

BENCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")  # katalog repo lawbenchmark
OC = f"{BENCH}/cards"
SD = f"{BENCH}/judges"
KL = f"{BENCH}/keys"
SP = os.path.dirname(os.path.abspath(__file__))
PYT = ["P01", "P04", "P05", "P06", "P07", "P08", "P09", "P10", "P12", "P13"]
PILOT = {"P05", "P06", "P07", "P12", "P13"}          # zbiór pilotażowy (karty zamykane po obejrzeniu sędziów)
ROZSZ = {"P01", "P04", "P08", "P09", "P10"}          # rozszerzenie 18.10 (karty zamknięte przed sędziami)
P8 = {"P01", "P04", "P05", "P06", "P07", "P08", "P12", "P13"}  # pytania testowe warstwy weryfikacji

# system → (model w artykule, rodzina, warunek)
SYSTEMY = [
    ("chatgpt_codex_w0_r3", "GPT-6.1 Sol", "OpenAI", "W0"), ("chatgpt_codex_web_r3", "GPT-6.1 Sol", "OpenAI", "W1"),
    ("codex_astra6_w0_r3", "GPT-6 Astra", "OpenAI", "W0"), ("codex_astra6_web_r3", "GPT-6 Astra", "OpenAI", "W1"),
    ("codex_terra56_w0_r3", "GPT-5.6 Terra", "OpenAI", "W0"), ("codex_terra56_web_r3", "GPT-5.6 Terra", "OpenAI", "W1"),
    ("opus_cli_w0_r3", "Claude Opus 5.5", "Anthropic", "W0"), ("opus_cli_w1_r3", "Claude Opus 5.5", "Anthropic", "W1"),
    ("sonnet_cli_w0_r3", "Claude Sonnet 5.5", "Anthropic", "W0"), ("sonnet_cli_w1_r3", "Claude Sonnet 5.5", "Anthropic", "W1"),
    ("haiku_cli_w0_r3", "Claude Haiku 5.5", "Anthropic", "W0"), ("haiku_cli_w1_r3", "Claude Haiku 5.5", "Anthropic", "W1"),
    ("gemini38flash_vertex_w0_r3", "Gemini 3.8 Flash", "Google", "W0"), ("gemini38flash_vertex_w1_r3", "Gemini 3.8 Flash", "Google", "W1"),
    ("argon4_high_vertex_w0_r3", "Gemini 4 Argon", "Google", "W0"), ("argon4_high_vertex_w1_r3", "Gemini 4 Argon", "Google", "W1"),
]
NAZWA = {s: n for s, n, _, _ in SYSTEMY}
RODZ = {s: r for s, _, r, _ in SYSTEMY}
WAR = {s: w for s, _, _, w in SYSTEMY}
MODELE = list(dict.fromkeys(n for _, n, _, _ in SYSTEMY))
SEDZIOWIE = [("argon4v101", "Gemini 4 Argon"), ("sol61v101", "GPT-6.1 Sol"), ("gemini31v101", "Gemini 3.1 Pro"),
             ("gemini38flashv101", "Gemini 3.8 Flash"), ("astra6v101", "GPT-6 Astra")]
RE_H = re.compile(r"hallucinated:\s*\**\s*(?:(?:tak|nie)\s*→\s*\**)?(tak|nie)", re.I)


def pl(x, cyfry=1):
    """Liczba w zapisie polskim (przecinek dziesiętny)."""
    return f"{x:.{cyfry}f}".replace(".", ",")


def pkt(w):
    m = re.match(r"\s*([\d½.]+)\s*/\s*\d", w)
    return float(m.group(1).replace("½", "0.5")) if m else None


def karta(p, s):
    t = open(f"{OC}/{p}_{s}.md", encoding="utf-8").read()
    A = re.search(r"\|\s*\*\*A\*\*\s*\|\s*\*\*[^=]*=\s*([\d.]+)\s*%", t)
    B = re.search(r"\|\s*\*\*B\*\*\s*\|\s*\*\*[^=]*=\s*([\d.]+)\s*%", t)
    delta = [l for l in t.splitlines() if l.startswith("**Δ")]
    H = RE_H.search(delta[-1]) if delta else None
    a6 = re.findall(r"^\| A6 \|([^|]*)\|([^\n]*)", t, re.M)
    ar = re.findall(r"^\| A-R \|([^|]*)\|", t, re.M)
    assert len(a6) == 1 and len(ar) == 1, (p, s)
    wiersz = a6[0][1]
    m = re.search(r"A6_typ:\s*\**\s*(\[[^\]]*\])(?:\s*→\s*(\[[^\]]*\]))?", wiersz)
    typ = set(re.findall(r"\b([FTWS])\b", (m.group(2) or m.group(1)))) if m else set()
    mz = re.search(r"A6_zakres:\s*\**\s*(rdzeń|poboczne)(?:\**\s*→\s*\**(rdzeń|poboczne))?", wiersz)
    zr = re.search(r"bez weryfikacji źródła:\s*(tak \((?:brak narzędzi|tylko źródła wtórne|narzędzia nieużyte)\)|nie)", t)
    sp = re.search(r"[Ss]prawdzon[eo]\s+(?:powoła[nń]\w*\s+)?(\d+)\s+z\s+(\d+)", wiersz)
    mp = re.search(r"A6_pochodzenie:([^\]]*)", wiersz)
    poch = next((r for r in ["odczyt_źródła", "źródło_wtórne", "pamięć", "nieustalone"] if mp and r in mp.group(1)), None)
    k = [pkt(v) if pkt(v) is not None else (-1.0 if "−1" in v or "-1" in v else 0.0)
         for v in re.findall(r"^\| K\d+ \|([^|]*)\|", t, re.M)]
    return {"p": p, "s": s, "A": float(A.group(1)), "B": float(B.group(1)),
            "hal": bool(H and H.group(1).lower() == "tak"), "a6": pkt(a6[0][0]), "blokada": "blokada" in a6[0][0],
            "ar": pkt(ar[0]), "typ": sorted(typ), "zakres": (mz.group(2) or mz.group(1)) if mz else None,
            "zrodlo": zr.group(1) if zr else "?", "spr": (int(sp.group(1)), int(sp.group(2))) if sp else (0, 0),
            "poch": poch, "kary": sum(1 for x in k if x and x < 0)}


K = {(p, s): karta(p, s) for p in PYT for s, *_ in SYSTEMY}
for k in K.values():
    k["pu"] = (k["a6"] == 1 and k["ar"] == 2)
    k["spojnosc"] = (k["hal"] == (k["a6"] == 0)) or k["blokada"]

# --- kontrola z generatorem zestawienie_tier.py ---
gen = subprocess.run(["python3", "-I", f"{BENCH}/tools/zestawienie_tier.py",
                      "--tylko", ",".join(PYT)], capture_output=True, text=True, check=True).stdout
GEN = {}
for l in gen.splitlines():
    c = [x.strip() for x in l.strip("|").split("|")]
    if len(c) > 5 and c[0] in NAZWA:
        GEN[c[0]] = {"A": float(c[2].strip("*")), "B": float(c[3]), "hal": int(c[4].split()[0]), "spr": c[5]}
for s in NAZWA:
    xs = [K[(p, s)] for p in PYT]
    a = round(sum(x["A"] for x in xs) / 10, 1); b = round(sum(x["B"] for x in xs) / 10, 1); h = sum(x["hal"] for x in xs)
    assert (a, b, h) == (GEN[s]["A"], GEN[s]["B"], GEN[s]["hal"]), (s, a, b, h, GEN[s])

# --- koszt (koszt_2026-10-18_odpowiedzi.csv; koszt nie zależy od kart) ---
KOSZT = {(r["pytanie"], r["system"]): (float(r["koszt_usd"]), r["dolna_granica"] == "True", r["data_odpowiedzi"])
         for r in csv.DictReader(open(f"{BENCH}/costs/koszt_2026-10-18_odpowiedzi.csv", encoding="utf-8"))}
assert all((p, s) in KOSZT for p in PYT for s in NAZWA)


def sysstat(s):
    xs = [K[(p, s)] for p in PYT]
    koszt = sum(KOSZT[(p, s)][0] for p in PYT); dg = any(KOSZT[(p, s)][1] for p in PYT)
    pu = sum(x["pu"] for x in xs)
    zr = collections.Counter(x["zrodlo"] for x in xs)
    return {"A": sum(x["A"] for x in xs) / 10, "B": sum(x["B"] for x in xs) / 10, "hal": sum(x["hal"] for x in xs),
            "pu": pu, "koszt": koszt, "dg": dg, "usd_pu": koszt / pu if pu else None,
            "spr": (sum(x["spr"][0] for x in xs), sum(x["spr"][1] for x in xs)), "zr": zr,
            "blok": sum(x["blokada"] for x in xs),
            "rdzen": sum(1 for x in xs if x["hal"] and x["zakres"] == "rdzeń"),
            "pob": sum(1 for x in xs if x["hal"] and x["zakres"] == "poboczne"),
            "poch": collections.Counter(x["poch"] for x in xs if x["hal"])}


S = {s: sysstat(s) for s in NAZWA}
usd = lambda x, dg=False: "n/d" if x is None else ("≥ " if dg else "") + pl(x, 3)

TABELE, LICZBY = {}, {}

# Tabela wyników W0/W1
w = ["| Model | Warunek | A % | B % | Halucynacje (z 10) | Poprawnie ugruntowane (z 10) | Koszt łączny USD | USD na poprawnie ugruntowaną | Sprawdzone powołania |",
     "|---|---|---|---|---|---|---|---|---|"]
for s, n, r, wa in SYSTEMY:
    x = S[s]
    w.append(f"| {n} | {wa} | {pl(x['A'])} | {pl(x['B'])} | {x['hal']} | {x['pu']} | {usd(x['koszt'], x['dg'])} | "
             f"{usd(x['usd_pu'], x['dg'])} | {x['spr'][0]} z {x['spr'][1]} |")
TABELE["WYNIKI"] = "\n".join(w)

# Pary W0 → W1
w = ["| Model | A % W0 → W1 | B % W0 → W1 | Halucynacje W0 → W1 | Poprawnie ugruntowane W0 → W1 | USD na poprawnie ugruntowaną W0 → W1 |",
     "|---|---|---|---|---|---|"]
for m in MODELE:
    s0 = next(s for s in NAZWA if NAZWA[s] == m and WAR[s] == "W0"); s1 = next(s for s in NAZWA if NAZWA[s] == m and WAR[s] == "W1")
    a, b = S[s0], S[s1]
    w.append(f"| {m} | {pl(a['A'])} → {pl(b['A'])} | {pl(a['B'])} → {pl(b['B'])} | {a['hal']} → {b['hal']} | {a['pu']} → {b['pu']} | "
             f"{usd(a['usd_pu'], a['dg'])} → {usd(b['usd_pu'], b['dg'])} |")
TABELE["PARY"] = "\n".join(w)

# Sumy
for wa in ("W0", "W1"):
    ss = [s for s in NAZWA if WAR[s] == wa]
    LICZBY[f"hal_{wa}"] = sum(S[s]["hal"] for s in ss); LICZBY[f"pu_{wa}"] = sum(S[s]["pu"] for s in ss)
    LICZBY[f"koszt_{wa}"] = sum(S[s]["koszt"] for s in ss)
LICZBY["hal"] = LICZBY["hal_W0"] + LICZBY["hal_W1"]; LICZBY["pu"] = LICZBY["pu_W0"] + LICZBY["pu_W1"]
LICZBY["koszt"] = LICZBY["koszt_W0"] + LICZBY["koszt_W1"]
LICZBY["pu_min"] = min(S[s]["pu"] for s in NAZWA); LICZBY["pu_max"] = max(S[s]["pu"] for s in NAZWA)
LICZBY["spojnosc_bledy"] = [f"{k['p']}_{k['s']}" for k in K.values() if not k["spojnosc"]]
LICZBY["blokady"] = [f"{k['p']}_{k['s']}" for k in K.values() if k["blokada"]]

# Klasy błędów (liczba odpowiedzi z daną klasą) wg warunku
w = ["| Klasa | W0 (80 odpowiedzi) | W1 (80 odpowiedzi) | Razem |", "|---|---|---|---|"]
opis = {"T": "T — treść, której w źródle nie ma", "W": "W — brzmienie z innej daty", "F": "F — źródło lub jednostka nie istnieje",
        "S": "S — zniekształcony identyfikator"}
for c in "TWFS":
    a = sum(1 for k in K.values() if k["hal"] and c in k["typ"] and WAR[k["s"]] == "W0")
    b = sum(1 for k in K.values() if k["hal"] and c in k["typ"] and WAR[k["s"]] == "W1")
    w.append(f"| {opis[c]} | {a} | {b} | {a + b} |"); LICZBY[f"klasa_{c}"] = a + b
w.append(f"| odpowiedzi z halucynacją | {LICZBY['hal_W0']} | {LICZBY['hal_W1']} | {LICZBY['hal']} |")
TABELE["KLASY"] = "\n".join(w)

# Zakres (tylko rozszerzenie — pole istnieje tylko tam)
hz = [k for k in K.values() if k["hal"]]
LICZBY["zakres_rdzen"] = sum(1 for k in hz if k["zakres"] == "rdzeń"); LICZBY["zakres_pob"] = sum(1 for k in hz if k["zakres"] == "poboczne")
LICZBY["zakres_brak"] = sum(1 for k in hz if k["zakres"] is None)
LICZBY["zakres_brak_pilot"] = sum(1 for k in hz if k["zakres"] is None and k["p"] in PILOT)
LICZBY["hal_rozsz"] = sum(1 for k in hz if k["p"] in ROZSZ); LICZBY["hal_pilot"] = sum(1 for k in hz if k["p"] in PILOT)

# Zasięg i pochodzenie w W1
w = ["| Model (W1) | źródło urzędowe użyte | tylko źródła wtórne | narzędzia nieużyte | „brak narzędzi” w karcie W1 | halucynacje: pamięć / odczyt źródła / źródło wtórne / nieustalone |",
     "|---|---|---|---|---|---|"]
for s in [s for s in NAZWA if WAR[s] == "W1"]:
    z = S[s]["zr"]; po = S[s]["poch"]
    w.append(f"| {NAZWA[s]} | {z['nie']} | {z['tak (tylko źródła wtórne)']} | {z['tak (narzędzia nieużyte)']} | {z['tak (brak narzędzi)']} | "
             f"{po['pamięć']} / {po['odczyt_źródła']} / {po['źródło_wtórne']} / {po['nieustalone'] + po[None]} |")
TABELE["ZRODLA_W1"] = "\n".join(w)
for lab, key in (("nie", "w1_oficjalne"), ("tak (tylko źródła wtórne)", "w1_wtorne"), ("tak (narzędzia nieużyte)", "w1_nieuzyte"),
                 ("tak (brak narzędzi)", "w1_brak")):
    LICZBY[key] = sum(S[s]["zr"][lab] for s in NAZWA if WAR[s] == "W1")

# Pytania
klucze = {}
for f in sorted(glob.glob(f"{KL}/P*.yaml")):
    d = yaml.safe_load(open(f, encoding="utf-8"))
    klucze[d["id"]] = d
DOM = {"karne": "prawo wykroczeń", "adm": "postępowanie administracyjne", "proc": "postępowanie cywilne",
       "ai": "AI Act", "aut": "prawo autorskie", "kons": "prawo konsumenckie"}
w = ["| Pytanie | Dziedzina | Typ | Pułapka | Kalibracja | Halucynacje (z 16) | Poprawnie ugruntowane (z 16) | A-R = 2 (z 16) | śr. A % |",
     "|---|---|---|---|---|---|---|---|---|"]
for p in PYT:
    xs = [K[(p, s)] for s in NAZWA]; d = klucze[p]
    w.append(f"| {p} | {DOM.get(d['domena'], d['domena'])} | {d['typ']} | {'tak' if d.get('pulapka') else 'nie'} | {d['kalibracja_oczekiwana']} | "
             f"{sum(x['hal'] for x in xs)} | {sum(x['pu'] for x in xs)} | {sum(1 for x in xs if x['ar'] == 2)} | {pl(sum(x['A'] for x in xs) / 16)} |")
TABELE["PYTANIA"] = "\n".join(w)

# Aneks A — klucze w skrócie
w = ["| Pytanie | Wersja klucza (data) | Pytanie w brzmieniu z biegu | Rdzeń klucza (skrót) | Podstawy wymagane |", "|---|---|---|---|---|"]
for p in PYT:
    d = klucze[p]
    tekst = (d.get("tekst_benchmarkowy") or d.get("tekst_oryginalny") or "").strip().replace("|", "/").replace("\n", " ")
    rdzen = d["rdzen"].strip().replace("\n", " ").replace("|", "/")
    zd = re.split(r"(?<=[.;])\s+(?=[A-ZŁŚŻŹĆ„])", rdzen)
    skrot = " ".join(zd[:2])
    # P09/P10: streszczenie ręczne z warunkiem (uwaga 23 recenzji z 27.10) zamiast pierwszych dwóch zdań
    SKROT_RECZNY = {
        "P09": "Co do zasady nie wystarcza (art. 41 ust. 2 i 4, art. 53 pr.aut.). Według SN (I CSK 104/18, I CSK 596/17, IV CSKP 44/21) pola mogą być dookreślone w drodze wykładni z art. 65 k.c. z treści i celu umowy, w razie wątpliwości na korzyść twórcy — kalibracja warunkowa.",
        "P10": "Nie — co do zasady nie wystarcza; wykładnia z art. 65 k.c. może dookreślić pola, ale nie zwalnia z wyliczenia. Odpowiedź „wystarcza i nie trzeba wyliczać” pozostaje błędem (pułapka); sprzeczność z własną odpowiedzią na P09 jest karana.",
    }
    skrot = SKROT_RECZNY.get(p, skrot)
    w.append(f"| {p} | v{d.get('wersja_klucza')} ({d.get('data_klucza')}) | {tekst} | {skrot} | {'; '.join(d['podstawy_wymagane'])} |")
TABELE["KLUCZE"] = "\n".join(w)
LICZBY["P02_status"] = klucze.get("P02", {}).get("status", "poza repozytorium")  # P02 nie wchodzi do raportu ani do eksportu

# Aneks B — macierze
skr = {"chatgpt_codex_w0_r3": "Sol W0", "chatgpt_codex_web_r3": "Sol W1", "codex_astra6_w0_r3": "Astra W0", "codex_astra6_web_r3": "Astra W1",
       "codex_terra56_w0_r3": "Terra W0", "codex_terra56_web_r3": "Terra W1", "opus_cli_w0_r3": "Opus W0", "opus_cli_w1_r3": "Opus W1",
       "sonnet_cli_w0_r3": "Sonnet W0", "sonnet_cli_w1_r3": "Sonnet W1", "haiku_cli_w0_r3": "Haiku W0", "haiku_cli_w1_r3": "Haiku W1",
       "gemini38flash_vertex_w0_r3": "Flash W0", "gemini38flash_vertex_w1_r3": "Flash W1", "argon4_high_vertex_w0_r3": "Argon W0",
       "argon4_high_vertex_w1_r3": "Argon W1"}
hdr = "| System | " + " | ".join(PYT) + " |\n|---|" + "---|" * len(PYT)
w = [hdr]
for s in NAZWA:
    w.append(f"| {skr[s]} | " + " | ".join(pl(K[(p, s)]["A"], 0) for p in PYT) + " |")
TABELE["ANEKS_B_A"] = "\n".join(w)
w = [hdr]
for s in NAZWA:
    cel = []
    for p in PYT:
        k = K[(p, s)]
        cel.append("blokada" if k["blokada"] else ((",".join(k["typ"]) or "tak") if k["hal"] else ("✓" if k["pu"] else "–")))
    w.append(f"| {skr[s]} | " + " | ".join(cel) + " |")
TABELE["ANEKS_B_H"] = "\n".join(w)


# --- sędziowie ---
def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n; pa = sum(a for a, _ in pairs) / n; pb = sum(b for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def wczytaj(j):
    out = {}
    for (p, s) in K:
        f = f"{SD}/{p}_{s}.{j}.json"
        if not os.path.exists(f):
            continue
        try:
            x = json.load(open(f, encoding="utf-8"))
        except ValueError:
            continue
        if x.get("blad_parsowania") or x.get("hallucinated") is None:
            continue
        out[(p, s)] = x
    return out


SEDZ = {j: wczytaj(j) for j, _ in SEDZIOWIE}


def stat_sedziego(j, zbior):
    xs = {k: v for k, v in SEDZ[j].items() if k[0] in zbior}
    pairs = [(K[k]["hal"], bool(v["hallucinated"])) for k, v in xs.items()]
    if not pairs:
        return None
    wy = [v.get("_meta", {}).get("wyszukan") for v in xs.values()]
    wy = [x for x in wy if x is not None]
    ns = [len(v.get("niesprawdzone") or []) for v in xs.values()]
    return {"n": len(pairs), "zg": sum(a == b for a, b in pairs) / len(pairs) * 100, "k": kappa(pairs),
            "fa": sum(b and not a for a, b in pairs), "pom": sum(a and not b for a, b in pairs),
            "wy": sum(wy) / len(wy) if wy else None, "wy0": sum(1 for x in wy if x == 0), "ns": sum(ns) / len(ns)}


w = ["| Sędzia | Zbiór | n | Zgodność | κ | Fałszywe alarmy | Pominięcia | Wyszukań na kartę | Karty bez wyszukania | „Niesprawdzone” na kartę |",
     "|---|---|---|---|---|---|---|---|---|---|"]
for j, nm in SEDZIOWIE:
    for zb, lab in ((ROZSZ, "rozszerzenie (P01, P04, P08–P10)"), (PILOT, "pilotaż (P05–P07, P12, P13)")):
        x = stat_sedziego(j, zb)
        if not x:
            continue
        LICZBY[f"kappa_{j}_{'rozsz' if zb is ROZSZ else 'pilot'}"] = round(x["k"], 2)
        w.append(f"| {nm} | {lab} | {x['n']} | {pl(x['zg'], 0)} % | {pl(x['k'], 2)} | {x['fa']} | {x['pom']} | "
                 f"{pl(x['wy'], 1) if x['wy'] is not None else 'n/d'} | {x['wy0']} | {pl(x['ns'], 2)} |")
TABELE["SEDZIOWIE"] = "\n".join(w)

# zgodność etykiety per pytanie (zgodne / ocenione)
w = ["| Sędzia | " + " | ".join(PYT) + " |", "|---|" + "---|" * len(PYT)]
for j, nm in SEDZIOWIE:
    cel = []
    for p in PYT:
        ks = [k for k in SEDZ[j] if k[0] == p]
        cel.append(f"{sum(K[k]['hal'] == bool(SEDZ[j][k]['hallucinated']) for k in ks)}/{len(ks)}" if ks else "–")
    w.append(f"| {nm} | " + " | ".join(cel) + " |")
TABELE["SEDZ_PYT"] = "\n".join(w)

# preferencja rodziny: odsetek pominiętych halucynacji wg rodziny ocenianego modelu (wszystkie 10 pytań)
w = ["| Sędzia | Anthropic: pominięte / halucynacje w kartach | Google: pominięte / halucynacje | OpenAI: pominięte / halucynacje |", "|---|---|---|---|"]
for j, nm in SEDZIOWIE[:4]:
    cel = []
    for r in ("Anthropic", "Google", "OpenAI"):
        ks = [k for k in SEDZ[j] if RODZ[k[1]] == r and K[k]["hal"]]
        pom = sum(1 for k in ks if not SEDZ[j][k]["hallucinated"])
        cel.append(f"{pom} / {len(ks)} ({pl(pom / len(ks) * 100, 0)} %)" if ks else "n/d")
    w.append(f"| {nm} | " + " | ".join(cel) + " |")
TABELE["RODZINA"] = "\n".join(w)

# panel na rozszerzeniu: „którykolwiek z Argon/Sol/Pro/Flash” i większość
wspolne = [k for k in K if k[0] in ROZSZ and all(k in SEDZ[j] for j, _ in SEDZIOWIE[:4])]
any_ = [(K[k]["hal"], any(SEDZ[j][k]["hallucinated"] for j, _ in SEDZIOWIE[:4])) for k in wspolne]
maj3 = [(K[k]["hal"], sum(bool(SEDZ[j][k]["hallucinated"]) for j in ("argon4v101", "sol61v101", "gemini31v101")) >= 2) for k in wspolne]
LICZBY["panel_n"] = len(wspolne); LICZBY["panel_any_k"] = round(kappa(any_), 2); LICZBY["panel_maj3_k"] = round(kappa(maj3), 2)
LICZBY["panel_any_fa"] = sum(b and not a for a, b in any_); LICZBY["panel_any_pom"] = sum(a and not b for a, b in any_)
ap = [(K[k]["hal"], bool(SEDZ["argon4v101"][k]["hallucinated"]) or bool(SEDZ["gemini31v101"][k]["hallucinated"])) for k in wspolne]
LICZBY["panel_argon_lub_pro_k"] = round(kappa(ap), 2)
LICZBY["panel_argon_lub_pro_fa_pom"] = (sum(b and not a for a, b in ap), sum(a and not b for a, b in ap))
# P09/P10: para lustrzana — kara K2 (rdzeń P10 sprzeczny z P09 tego samego systemu) i K1 (przytaknięcie przesłance)
LICZBY["P10_K2"] = sum(1 for s in NAZWA if re.search(r"^\| K2 \|\s*−1", open(f"{OC}/P10_{s}.md", encoding="utf-8").read(), re.M))
LICZBY["P10_K1"] = sum(1 for s in NAZWA if re.search(r"^\| K1 \|\s*−1", open(f"{OC}/P10_{s}.md", encoding="utf-8").read(), re.M))
LICZBY["argon_sam_wspolne_k"] = round(kappa([(K[k]["hal"], bool(SEDZ["argon4v101"][k]["hallucinated"])) for k in wspolne]), 2)

# --- meta-sędzia: warianty karty meta na pytaniach testowych ---
META = {}
w = ["| Sędzia | Wariant | Pytania | n (karty wspólne z sędzią bez raportu) | κ bez raportu | κ z raportem | Fałszywe alarmy bez → z | Pominięcia bez → z |",
     "|---|---|---|---|---|---|---|---|"]
for rodz, baza, nm in (("argon4", "argon4v101", "Gemini 4 Argon"), ("sol61", "sol61v101", "GPT-6.1 Sol")):
    B0 = wczytaj(baza)
    for v, lab in (("meta", "raport wiążący (v1)"), ("meta2", "raport pomocniczy (v2)"), ("meta3", "v3: ✓ tylko przy brzmieniu potwierdzonym")):
        M = wczytaj(rodz + v)
        ks = sorted(k for k in M if k[0] in P8 and k in B0)
        pyt = sorted({k[0] for k in ks})
        META[(rodz, v)] = {"n": len(ks), "pliki": len([f for f in glob.glob(f"{SD}/*.{rodz}{v}.json")]), "pytania": pyt}
        if not ks:
            continue
        b = [(K[k]["hal"], bool(B0[k]["hallucinated"])) for k in ks]; m = [(K[k]["hal"], bool(M[k]["hallucinated"])) for k in ks]
        META[(rodz, v)].update(kb=round(kappa(b), 2), km=round(kappa(m), 2))
        w.append(f"| {nm} | {lab} | {', '.join(pyt)} | {len(ks)} | {pl(kappa(b), 2)} | {pl(kappa(m), 2)} | "
                 f"{sum(y and not x for x, y in b)} → {sum(y and not x for x, y in m)} | {sum(x and not y for x, y in b)} → {sum(x and not y for x, y in m)} |")
TABELE["META"] = "\n".join(w)
LICZBY["meta"] = {f"{a}_{b}": v for (a, b), v in META.items()}


# zasięg weryfikacji i pochodzenie (dopisane do LICZBY)
LICZBY["spr"] = (sum(S[s]["spr"][0] for s in NAZWA), sum(S[s]["spr"][1] for s in NAZWA))
LICZBY["karty_bez_spr"] = sum(1 for k in K.values() if k["spr"] == (0, 0))
LICZBY["poch_W1"] = dict(collections.Counter(k["poch"] or "nieustalone" for k in K.values() if k["hal"] and WAR[k["s"]] == "W1"))
LICZBY["poch_W0"] = dict(collections.Counter(k["poch"] or "nieustalone" for k in K.values() if k["hal"] and WAR[k["s"]] == "W0"))
LICZBY["dA"] = {m: round(S[[s for s in NAZWA if NAZWA[s] == m and WAR[s] == "W1"][0]]["A"] - S[[s for s in NAZWA if NAZWA[s] == m and WAR[s] == "W0"][0]]["A"], 1) for m in MODELE}
LICZBY["krotnosc_kosztu"] = {m: round(S[[s for s in NAZWA if NAZWA[s] == m and WAR[s] == "W1"][0]]["koszt"] / S[[s for s in NAZWA if NAZWA[s] == m and WAR[s] == "W0"][0]]["koszt"], 1) for m in MODELE}

# --- pełny koszt badania (decyzja Adama 2026-10-25: „pełen koszt”) ---
# Odpowiedzi: koszt_2026-10-18_odpowiedzi.csv. Sędziowie Vertex i karty meta Argon: tokeny z _meta plików sędziów
# (wszystkie pliki na 160 kartach, także z błędem parsowania — Vertex je nalicza) × cennik_2026-10-18.yaml;
# wyszukiwania (Grounding with Google Search) osobno, po 0,014 USD za zapytanie wg cennika (5000 zapytań/mies.
# bez opłaty — dlatego zapisy Vertex w raportach biegów ich nie zawierają). Sędziowie v1.0.1 nie zapisywali tokenów
# rozumowania → dolna granica. Codex (GPT-6.1 Sol, GPT-6 Astra): subskrypcja, tokeny niezapisane → n/d.
# Weryfikator poparcia: linie „Koszt USD” z raportów biegów (bez ceny katalogowej Argon).
CEN = yaml.safe_load(open(f"{BENCH}/costs/cennik_2026-10-18.yaml", encoding="utf-8"))
CENA_ZAP = CEN["narzedzia"]["vertex_google_search_grounding"]["cena_za_zapytanie"]


def koszt_sedziego(j):
    n = tok = zap = 0; usd_t = 0.0; bez_roz = 0
    for (p, s) in K:
        f = f"{SD}/{p}_{s}.{j}.json"
        if not os.path.exists(f):
            continue
        n += 1
        try:
            m = json.load(open(f, encoding="utf-8")).get("_meta", {})
        except ValueError:
            continue
        t = m.get("tokeny")
        if not t:
            continue
        c = CEN["modele"].get(m["model"]) or CEN["modele"][m["model"] + "-preview"]
        r = t.get("rozumowanie")
        bez_roz += r is None
        usd_t += (t["wejscie"] * c["wejscie"] + (t["wyjscie"] + (r or 0)) * c["wyjscie"]) / 1e6
        zap += m.get("wyszukan") or 0; tok += 1
    return {"n": n, "z_tokenami": tok, "usd_tokeny": usd_t, "zapytania": zap, "usd_zap": zap * CENA_ZAP,
            "dolna": bez_roz > 0}


POP_PLIKI = ["_poparcie_test_P05_1sys.md", "_poparcie_test_P05_cache.md", "_poparcie_P09P10_2026-10-19.md",
             "_poparcie_8pytan_2026-10-23.md", "_poparcie_8pytan_2026-10-24.md", "_poparcie_8pytan_2026-10-24c.md"]
RAP = f"{BENCH}/verification/reports"


def koszt_poparcia(plik):
    l = re.search(r"Koszt USD[^:]*:\s*gemini-3\.8-flash ([\d.]+), gemini-4-argon ([\d.]+)", open(f"{RAP}/{plik}", encoding="utf-8").read())
    return float(l.group(1)) + float(l.group(2))


POP = {f: koszt_poparcia(f) for f in POP_PLIKI}
DYM = float(re.search(r"Testy dymne: ([\d,]+) USD", open(f"{RAP}/_meta_8pytan_2026-10-24.md", encoding="utf-8").read()).group(1).replace(",", "."))

wiersze = []  # (grupa, pozycja, n, usd_tokeny, zapytania, usd_zap, dolna, uwaga)
wiersze.append(("Odpowiedzi", "160 odpowiedzi ośmiu modeli (W0 i W1)", 160, LICZBY["koszt"], None, 0.0, True,
                "równoważnik API; Vertex koszt faktyczny; W1 Claude i Gemini dolna granica"))
for j, nm in (("argon4v101", "Gemini 4 Argon"), ("gemini31v101", "Gemini 3.1 Pro"), ("gemini38flashv101", "Gemini 3.8 Flash")):
    x = koszt_sedziego(j)
    wiersze.append(("Sędziowie-modele", f"{nm}, specyfikacja v1.0.1", x["n"], x["usd_tokeny"], x["zapytania"], x["usd_zap"], x["dolna"],
                    "bez tokenów rozumowania (niezapisane)"))
for j, nm in (("sol61v101", "GPT-6.1 Sol"), ("astra6v101", "GPT-6 Astra")):
    x = koszt_sedziego(j)
    wiersze.append(("Sędziowie-modele", f"{nm}, specyfikacja v1.0.1", x["n"], None, None, None, False, "Codex z subskrypcji; tokeny niezapisane"))
wiersze.append(("Warstwa weryfikacji", "krok faktów (kod, źródła publiczne)", None, 0.0, None, 0.0, False, "bez modelu"))
wiersze.append(("Warstwa weryfikacji", f"weryfikator poparcia ({len(POP)} biegów: testy, strojenie P09–P10, test na 8 pytaniach, poprawki)", None,
                sum(POP.values()), None, 0.0, False, "z raportów biegów"))
for v, lab in (("meta", "v1"), ("meta2", "v2"), ("meta3", "v3")):
    x = koszt_sedziego("argon4" + v)
    if x["n"]:
        wiersze.append(("Warstwa weryfikacji", f"karta meta Gemini 4 Argon {lab}", x["n"], x["usd_tokeny"], x["zapytania"], x["usd_zap"], False, ""))
for v, lab in (("meta", "v1"), ("meta2", "v2"), ("meta3", "v3")):
    x = koszt_sedziego("sol61" + v)
    if x["n"]:
        wiersze.append(("Warstwa weryfikacji", f"karta meta GPT-6.1 Sol {lab}", x["n"], None, None, None, False, "Codex z subskrypcji"))
wiersze.append(("Warstwa weryfikacji", "testy wstępne poprawności działania", None, DYM, None, 0.0, False, "z raportu biegu 24.10"))

w = ["| Część | Pozycja | Karty | Tokeny USD | Wyszukania | Wyszukania USD | Razem USD |", "|---|---|---|---|---|---|---|"]
suma_t = suma_z = 0.0; dolna_all = False
for g, poz, n, ut, zp, uz, dg, uw in wiersze:
    if ut is None:
        w.append(f"| {g} | {poz} | {n if n is not None else '—'} | n/d | n/d | n/d | n/d ({uw}) |")
        continue
    suma_t += ut; suma_z += uz or 0; dolna_all |= dg
    razem = ut + (uz or 0)
    w.append(f"| {g} | {poz} | {n if n is not None else '—'} | {'≥ ' if dg else ''}{pl(ut, 2)} | {zp if zp is not None else '—'} | "
             f"{pl(uz or 0, 2)} | {'≥ ' if dg else ''}{pl(razem, 2)} |")
w.append(f"| **Razem** | | | **≥ {pl(suma_t, 2)}** | | **{pl(suma_z, 2)}** | **≥ {pl(suma_t + suma_z, 2)}** |")
TABELE["KOSZT_PELNY"] = "\n".join(w)
LICZBY["koszt_pelny"] = suma_t + suma_z
LICZBY["koszt_pelny_tokeny"] = suma_t
LICZBY["koszt_pelny_wyszukania"] = suma_z
LICZBY["koszt_sedziowie"] = sum(r[3] + (r[5] or 0) for r in wiersze if r[0] == "Sędziowie-modele" and r[3] is not None)
LICZBY["koszt_weryfikacja"] = sum(r[3] + (r[5] or 0) for r in wiersze if r[0] == "Warstwa weryfikacji" and r[3] is not None)
LICZBY["koszt_poparcie"] = sum(POP.values())


# --- macierze TP/FP/FN/TN i przedziały 95 % (bootstrap po pytaniach) — jak aneks D.5 artykułu v1.2 (2026-10-27) ---
import random
_B = 4000
_CI = {}


def _boot_ci(pairs_by_q):
    klucz = tuple(sorted((q, tuple(v)) for q, v in pairs_by_q.items()))
    if klucz not in _CI:
        random.seed(20261026)
        qs = list(pairs_by_q); vals = []
        for _ in range(_B):
            sample = [random.choice(qs) for _ in qs]
            pr = [p for q in sample for p in pairs_by_q[q]]
            k = kappa(pr)
            if k == k:
                vals.append(k)
        vals.sort(); _CI[klucz] = (vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))])
    return _CI[klucz]


def _wiersz(nazwa, zbior, pairs_by_q):
    pr = [p for q in pairs_by_q for p in pairs_by_q[q]]; n = len(pr)
    tp = sum(a and b for a, b in pr); fp = sum((not a) and b for a, b in pr); fn = sum(a and (not b) for a, b in pr); tn = sum((not a) and (not b) for a, b in pr)
    lo, hi = _boot_ci(pairs_by_q)
    return f"| {nazwa} | {zbior} | {n} | {tp + fn} | {tp} | {fp} | {fn} | {pl(kappa(pr), 2)} | {pl(lo, 2)}–{pl(hi, 2)} |"


def _pary(J, keys):
    out = {}
    for k in keys:
        if k in J:
            out.setdefault(k[0], []).append((K[k]["hal"], bool(J[k]["hallucinated"])))
    return out


_NAZ = dict(SEDZIOWIE)
w = ["| Sędzia / reguła | Zbiór | n | hal. w kartach | TP | FP | FN | κ | przedział 95 % |",
     "|---|---|---|---|---|---|---|---|---|"]
k80 = [k for k in K if k[0] in ROZSZ]; kp = [k for k in K if k[0] in PILOT]
for j, nm in SEDZIOWIE:
    w.append(_wiersz(nm, "rozszerzenie", _pary(SEDZ[j], k80)))
    w.append(_wiersz(nm, "pilotaż", _pary(SEDZ[j], kp)))
_JJ = {j: SEDZ[j] for j in ["argon4v101", "sol61v101", "gemini31v101", "gemini38flashv101"]}
_wsp = [k for k in k80 if all(k in _JJ[j] for j in _JJ)]
def _panel(nazwa, fn):
    pb = {}
    for k in _wsp:
        v = {j: bool(_JJ[j][k]["hallucinated"]) for j in _JJ}
        pb.setdefault(k[0], []).append((K[k]["hal"], fn(v)))
    w.append(_wiersz(nazwa, "rozszerzenie, 4 sędziów", pb))
_panel("Gemini 4 Argon sam", lambda v: v["argon4v101"])
_panel("Argon albo Gemini 3.1 Pro", lambda v: v["argon4v101"] or v["gemini31v101"])
_panel("większość z: Argon, Sol, Pro", lambda v: sum([v["argon4v101"], v["sol61v101"], v["gemini31v101"]]) >= 2)
_panel("którykolwiek z czterech", lambda v: any(v.values()))
for rodz, baza, nm in (("argon4", "argon4v101", "Gemini 4 Argon"), ("sol61", "sol61v101", "GPT-6.1 Sol")):
    B0 = wczytaj(baza); M = {v: wczytaj(rodz + v) for v in ("meta", "meta2", "meta3")}
    lab = {"meta": "v1", "meta2": "v2", "meta3": "v3"}
    for v in ("meta", "meta2", "meta3"):
        ks = [k for k in M[v] if k[0] in P8 and k in B0]
        w.append(_wiersz(f"{nm}, bez raportu", f"karty {lab[v]}", _pary(B0, ks)))
        w.append(_wiersz(f"{nm}, z raportem {lab[v]}", f"karty {lab[v]}", _pary(M[v], ks)))
    ks = [k for k in M["meta2"] if k in M["meta3"] and k in B0 and k[0] in P8]
    for nazwa, J in ((f"{nm}, bez raportu", B0), (f"{nm}, z raportem v2", M["meta2"]), (f"{nm}, z raportem v3", M["meta3"])):
        w.append(_wiersz(nazwa, "wspólne v2 i v3", _pary(J, ks)))
TABELE["MACIERZE"] = "\n".join(w)

if __name__ == "__main__":
    json.dump({"LICZBY": LICZBY, "TABELE": TABELE}, open(f"{SP}/dane.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for k, v in LICZBY.items():
        print(k, "=", v)
    for k, v in TABELE.items():
        print(f"\n## {k}\n{v}")
