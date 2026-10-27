#!/usr/bin/env python3
"""Zgodność „karty meta” (sędzia z raportem faktów) z kartami Adama kontra zgodność TYCH SAMYCH sędziów bez raportu
(ETAP D.4, 2026-10-24). Parser kart i κ Cohena przepisane z tools/porownaj_sedziow.py (tamten skrypt
liczy przy imporcie, więc nie da się go zaimportować).

Dla par (sędzia bez raportu, sędzia z raportem) — domyślnie (argon4v101, argon4meta) i (sol61v101, sol61meta) —
liczy κ dla hallucinated, A6 i A-R na WSPÓLNYM zbiorze kart (te, które mają oba pliki sędziego i kartę), plus
macierze hallucinated, nadmiar/brak i listę kart rozbieżnych. Wypisuje tylko liczby i identyfikatory kart.

Użycie: python -I zgodnosc_meta.py [--pary argon4v101:argon4meta,sol61v101:sol61meta] [--tylko P01,P04,…] [--md plik]
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re

OC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cards")  # repo lawbenchmark


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
    d = {"R": [], "K": []}
    for line in s.splitlines():
        m = re.match(r"\|\s*\**([A-Za-z0-9\-]+)[^|]*\|\s*([^|]*)\|(.*)", line)
        if not m:
            continue
        k, v = m.group(1), num(m.group(2))
        if k in ("A-R", "A2", "A3", "A5", "A6", "A8"):
            d[k.replace("-", "_")] = v
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


def wczytaj(sedzia: str, tylko: set | None) -> dict:
    out = {}
    for jf in sorted(glob.glob(f"{OC}/../judges/*.{sedzia}.json")):
        j = json.load(open(jf))
        if j.get("blad_parsowania"):
            continue
        m = j["_meta"]
        if tylko and m["pytanie"] not in tylko:
            continue
        kf = f"{OC}/{m['pytanie']}_{m['system']}.md"
        if not os.path.exists(kf):
            continue
        out[(m["pytanie"], m["system"])] = (karta(kf), j)
    return out


def tabela(nazwa: str, rows: list[tuple[dict, dict]]) -> list[str]:
    L = [f"| {nazwa} | zgodność | κ | n |", "|---|---|---|---|"]
    for crit, key in [("hallucinated", "hal"), ("A6", "A6"), ("A-R", "A_R"), ("A2", "A2"), ("A3", "A3"), ("A8", "A8"), ("B1", "B1"), ("B2", "B2")]:
        if key == "hal":
            pairs = [(c["hal"], bool(j.get("hallucinated"))) for c, j in rows]
        else:
            pairs = [(nz(c.get(key)), nz(j.get(key))) for c, j in rows]
        po, k, n = kappa(pairs)
        L.append(f"| {crit} | {po * 100:.0f} % | {k:.2f} | {n} |")
    cm = collections.Counter((c["hal"], bool(j.get("hallucinated"))) for c, j in rows)
    L.append(f"\nhallucinated: obaj tak {cm[(True, True)]} · obaj nie {cm[(False, False)]} · tylko karta {cm[(True, False)]} (brak u sędziego) · tylko sędzia {cm[(False, True)]} (nadmiar)")
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pary", default="argon4v101:argon4meta,sol61v101:sol61meta")
    ap.add_argument("--tylko", default=None)
    ap.add_argument("--md", default=None)
    args = ap.parse_args()
    tylko = set(args.tylko.split(",")) if args.tylko else None
    L = ["# Zgodność z kartami Adama: sędzia bez raportu faktów vs sędzia z raportem (karta meta)", ""]
    for para in args.pary.split(","):
        bez, z = para.split(":")
        A, B = wczytaj(bez, tylko), wczytaj(z, tylko)
        wspolne = sorted(set(A) & set(B))
        L.append(f"## {bez} (bez raportu) vs {z} (z raportem) — wspólnych kart: {len(wspolne)} "
                 f"(bez raportu ogółem {len(A)}, z raportem ogółem {len(B)})\n")
        if not wspolne:
            L.append("brak wspólnych kart\n")
            continue
        rows_a = [A[k] for k in wspolne]
        rows_b = [B[k] for k in wspolne]
        L += tabela(f"{bez} — bez raportu", rows_a) + [""] + tabela(f"{z} — z raportem", rows_b) + [""]
        # zgodność sędzia-bez vs sędzia-z (czy raport zmienia werdykt)
        zm = [(k, A[k][1], B[k][1], A[k][0]) for k in wspolne if bool(A[k][1].get("hallucinated")) != bool(B[k][1].get("hallucinated"))]
        L.append(f"Karty, na których raport zmienił etykietę hallucinated: {len(zm)} z {len(wspolne)}")
        L.append("")
        L.append("| P | system | karta Adama | bez raportu | z raportem | A6_typ z raportem |")
        L.append("|---|---|---|---|---|---|")
        for k, ja, jb, c in zm:
            L.append(f"| {k[0]} | {k[1]} | {'tak' if c['hal'] else 'nie'} | {'tak' if ja.get('hallucinated') else 'nie'} | "
                     f"{'tak' if jb.get('hallucinated') else 'nie'} | {jb.get('A6_typ')} |")
        L.append("")
        # per pytanie: czy rozbieżności z kartą rosną czy maleją
        L.append("| P | n | bez raportu: zgodne hallucinated | z raportem: zgodne hallucinated | bez: zgodne A6 | z: zgodne A6 |")
        L.append("|---|---|---|---|---|---|")
        for p in sorted({k[0] for k in wspolne}):
            ks = [k for k in wspolne if k[0] == p]
            za = sum(A[k][0]["hal"] == bool(A[k][1].get("hallucinated")) for k in ks)
            zb = sum(B[k][0]["hal"] == bool(B[k][1].get("hallucinated")) for k in ks)
            a6a = sum(nz(A[k][0].get("A6")) == nz(A[k][1].get("A6")) for k in ks)
            a6b = sum(nz(B[k][0].get("A6")) == nz(B[k][1].get("A6")) for k in ks)
            L.append(f"| {p} | {len(ks)} | {za} | {zb} | {a6a} | {a6b} |")
        L.append("")
        # karty, gdzie sędzia z raportem nadal różni się od Adama w A6 (kolejka do człowieka)
        roz = [k for k in wspolne if B[k][0]["hal"] != bool(B[k][1].get("hallucinated"))]
        L.append(f"Karty meta ({z}) z etykietą hallucinated inną niż karta Adama (do decyzji człowieka): {len(roz)} — "
                 + ", ".join(f"{k[0]}/{k[1]}" for k in roz))
        L.append("")
    txt = "\n".join(L)
    print(txt)
    if args.md:
        open(args.md, "w").write(txt + "\n")


if __name__ == "__main__":
    main()
