"""Zgodność dwóch sędziów tieru „pytania”: karty (sędzia 1) vs JSON drugiego sędziego w oceny/_sedziowie/.

Liczy zgodność i κ Cohena per kryterium, macierz etykiety hallucinated, zgodność wg dostawcy ocenianego
systemu oraz kolejkę kart do przeglądu człowieka (rozbieżność w A6 albo w etykiecie). Wypisuje tylko liczby
i identyfikatory kart. Użycie: python porownaj_sedziow.py <sedzia> [--kolejka plik.md]
"""
import collections
import glob
import json
import os
import re
import sys

OC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cards")  # repo lawbenchmark
sedzia = sys.argv[1]
kolejka = sys.argv[sys.argv.index("--kolejka") + 1] if "--kolejka" in sys.argv else None


def num(x):
    x = str(x).strip().replace("**", "").replace(",", ".").replace("−", "-")
    if re.match(r"n/?d", x, re.I):
        return "nd"
    t = x.split("/")[0].strip()
    if t == "½":
        return 0.5
    t = re.sub(r"^(\d)½$", r"\1.5", t)
    try:
        return float(t)
    except ValueError:
        return None


def karta(f):
    s = open(f).read()
    d = {"R": [], "K": [], "dowod_A6": ""}
    for line in s.splitlines():
        m = re.match(r"\|\s*\**([A-Za-z0-9\-]+)[^|]*\|\s*([^|]*)\|(.*)", line)
        if not m:
            continue
        k, v = m.group(1), num(m.group(2))
        if k in ("A-R", "A2", "A3", "A5", "A6", "A8"):
            d[k.replace("-", "_")] = v
            if k == "A6":
                d["dowod_A6"] = m.group(3).strip(" |")[:600]
        elif re.match(r"^R\d+$", k):
            d["R"].append(v)
        elif re.match(r"^K\d+$", k):
            d["K"].append(1 if (v not in (None, "nd") and v < 0) else 0)
        elif k in ("B1", "B2"):
            d[k] = v
    # 2026-10-25: etykieta z OSTATNIEJ linii „**Δ” (karty mają historię zmian); przy zapisie „tak → nie” bierzemy wartość po strzałce
    linie_d = [l for l in s.splitlines() if l.startswith("**Δ")]
    h = re.search(r"hallucinated:\s*\**\s*(?:(?:tak|nie)\s*→\s*\**)?(tak|nie)", linie_d[-1], re.I) if linie_d else None
    d["hal"] = bool(h and h.group(1).lower() == "tak")
    return d


def kappa(pairs):
    n = len(pairs)
    if not n:
        return 0, 0, 0
    po = sum(a == b for a, b in pairs) / n
    ca, cb = collections.Counter(a for a, _ in pairs), collections.Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return po, ((po - pe) / (1 - pe) if pe < 1 else 1.0), n


nz = lambda v: "nd" if v in ("nd", "n/d", None) else float(v)
rows = []
for jf in sorted(glob.glob(f"{OC}/../judges/*.{sedzia}.json")):
    j = json.load(open(jf))
    if j.get("blad_parsowania"):
        continue
    m = j["_meta"]
    rows.append((m["pytanie"], m["system"], karta(f"{OC}/{m['pytanie']}_{m['system']}.md"), j))
print("kart porównanych:", len(rows))
print("\n| Kryterium | zgodność | κ Cohena | n |\n|---|---|---|---|")
for crit, key in [("A-R", "A_R"), ("A2", "A2"), ("A3", "A3"), ("A5", "A5"), ("A6", "A6"), ("A8", "A8"), ("B1", "B1"), ("B2", "B2")]:
    po, k, n = kappa([(nz(c.get(key)), nz(j.get(key))) for _, _, c, j in rows])
    print(f"| {crit} | {po*100:.0f} % | {k:.2f} | {n} |")
po, k, n = kappa([(c["hal"], bool(j.get("hallucinated"))) for _, _, c, j in rows])
print(f"| hallucinated | {po*100:.0f} % | {k:.2f} | {n} |")
rp, kp = [], []
for _, _, c, j in rows:
    if len(c["R"]) == len(j.get("R", [])):
        rp += [(float(a), float(b)) for a, b in zip(c["R"], j["R"]) if a is not None]
    if len(c["K"]) == len(j.get("K", [])):
        kp += [(a, int(b)) for a, b in zip(c["K"], j["K"])]
for nm, pp in (("R (elementy rubryki)", rp), ("K (kary)", kp)):
    po, k, n = kappa(pp)
    print(f"| {nm} | {po*100:.0f} % | {k:.2f} | {n} |")
cm = collections.Counter((c["hal"], bool(j.get("hallucinated"))) for _, _, c, j in rows)
print(f"\nhallucinated: obaj tak {cm[(True, True)]} | obaj nie {cm[(False, False)]} | tylko sędzia 1 {cm[(True, False)]} | tylko sędzia 2 {cm[(False, True)]}")
dost = lambda s: "OpenAI" if ("codex" in s or "chatgpt" in s) else ("Anthropic" if any(x in s for x in ("opus", "sonnet", "haiku", "fable")) else "Google")
print("\n| Dostawca ocenianego | n | A6 zgodność | hallucinated: sędzia 1 | sędzia 2 |\n|---|---|---|---|---|")
for dd in ("OpenAI", "Anthropic", "Google"):
    sub = [(c, j) for _, s, c, j in rows if dost(s) == dd]
    po, _, n = kappa([(nz(c.get("A6")), nz(j.get("A6"))) for c, j in sub])
    print(f"| {dd} | {n} | {po*100:.0f} % | {sum(c['hal'] for c, _ in sub)} | {sum(bool(j.get('hallucinated')) for _, j in sub)} |")
roz = [(p, s, c, j) for p, s, c, j in rows if c["hal"] != bool(j.get("hallucinated")) or nz(c.get("A6")) != nz(j.get("A6"))]
print(f"\nkolejka do człowieka (A6 lub etykieta różne): {len(roz)} z {len(rows)}; w tym różna etykieta: {sum(c['hal'] != bool(j.get('hallucinated')) for _, _, c, j in roz)}")
if kolejka:
    with open(kolejka, "w") as fh:
        fh.write(f"# Kolejka do przeglądu — rozbieżność sędziów w A6 lub etykiecie hallucinated\n\nSędzia 1: karta (Claude). Sędzia 2: {sedzia}. Kart: {len(roz)} z {len(rows)}.\n")
        for p, s, c, j in sorted(roz, key=lambda r: (r[2]["hal"] == bool(r[3].get("hallucinated")), r[0], r[1])):
            pw = "; ".join(f"{x.get('powolanie','')[:90]} → {x.get('werdykt','')}" for x in j.get("powolania", []) if x.get("werdykt") not in ("zgodne", None))
            fh.write(f"\n## {p} · {s}\n\n- **Sędzia 1:** A6 {c.get('A6')}, hallucinated {'tak' if c['hal'] else 'nie'}. {c['dowod_A6']}\n- **Sędzia 2:** A6 {j.get('A6')} {j.get('A6_typ')}, hallucinated {'tak' if j.get('hallucinated') else 'nie'}. {j.get('uzasadnienie','')}\n- **Powołania zakwestionowane przez sędziego 2:** {pw or 'brak'}\n- **Decyzja Adama:** \n")
    print("kolejka zapisana:", kolejka)
