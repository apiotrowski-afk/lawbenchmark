"""Zestawienie tieru „pytania” z kart ocen: średnie A % i B %, liczba kart hallucinated i pochodzenie błędu.

Czyta wyłącznie karty (oceny/Pnn_<system>.md): wiersze sum A i B, etykietę z wiersza wyniku oraz pole
A6_pochodzenie z wiersza A6 (karta liczona wg najcięższego dowodu: odczyt_źródła > źródło_wtórne > pamięć >
nieustalone). Wypisuje tabele markdown. Użycie: python zestawienie_tier.py [--tylko P05,P06,...]
"""
import collections
import glob
import os
import re
import sys

OC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cards")  # repo lawbenchmark
tylko = set(sys.argv[sys.argv.index("--tylko") + 1].split(",")) if "--tylko" in sys.argv else None
RANGA = ["odczyt_źródła", "źródło_wtórne", "pamięć", "nieustalone"]


def karta(f):
    s = open(f).read()
    A = re.search(r"\|\s*\*\*A\*\*\s*\|\s*\*\*[^=]*=\s*([\d.]+)\s*%", s)
    B = re.search(r"\|\s*\*\*B\*\*\s*\|\s*\*\*[^=]*=\s*([\d.]+)\s*%", s)
    # etykieta z wiersza wyniku; obsługuje adnotacje zmian „nie → tak”
    H = re.search(r"Δ = A % − B %[^\n]*?hallucinated:\s*\**\s*(?:(?:tak|nie)\s*→\s*\**)?(tak|nie)", s, re.I)
    a6 = re.search(r"^\| A6 \|[^\n]*", s, re.M)
    poch = None
    if a6:
        m = re.search(r"A6_pochodzenie:([^\]]*)", a6.group(0))
        if m:
            poch = next((r for r in RANGA if r in m.group(1)), "nieustalone")
    zr = re.search(r"bez weryfikacji źródła:\s*(tak \((?:brak narzędzi|tylko źródła wtórne|narzędzia nieużyte)\)|nie)", s)
    # zasięg weryfikacji: „sprawdzone X z Y” z wiersza A6 (ile powołań faktycznie sprawdzono w źródle)
    sp = re.search(r"[Ss]prawdzon[eo]\s+(?:powoła[nń]\w*\s+)?(\d+)\s+z\s+(\d+)", a6.group(0)) if a6 else None
    pokr = (int(sp.group(1)), int(sp.group(2))) if sp else (0, 0)
    return (float(A.group(1)), float(B.group(1)), bool(H and H.group(1).lower() == "tak"), poch, zr.group(1) if zr else "?", pokr)


dane = collections.defaultdict(dict)
for f in sorted(glob.glob(f"{OC}/P*_*.md")):
    b = os.path.basename(f)[:-3]
    pid, system = b.split("_", 1)
    if tylko and pid not in tylko:
        continue
    dane[system][pid] = karta(f)


def tabela(systemy, nazwy=None):
    wiersze = []
    for s in systemy:
        k = dane.get(s)
        if not k:
            continue
        x = list(k.values())
        n = len(x)
        c = collections.Counter(p for _, _, h, p, _, _ in x if h)
        bez = sum(1 for _, _, _, _, z, _ in x if z.startswith("tak"))
        spr = sum(k[0] for *_, k in x); wsz = sum(k[1] for *_, k in x)
        wiersze.append((sum(a for a, *_ in x) / n, (nazwy or {}).get(s, s), n, sum(b for _, b, *_ in x) / n,
                        sum(1 for _, _, h, *_ in x if h), c, bez, (spr, wsz)))
    wiersze.sort(key=lambda w: -w[0])
    out = ["| System | kart | śr. A % | śr. B % | hallucinated | sprawdzone powołania | z pamięci | odczyt źródła | źródło wtórne | nieustalone | bez weryfikacji źródła |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for a, nm, n, b, h, c, bez, (spr, wsz) in wiersze:
        out.append(f"| {nm} | {n} | **{a:.1f}** | {b:.1f} | {h} z {n} | {spr} z {wsz} | {c['pamięć']} | {c['odczyt_źródła']} | {c['źródło_wtórne']} | {c['nieustalone'] + c[None]} | {bez} z {n} |")
    return "\n".join(out)


if __name__ == "__main__":
    print(tabela(sorted(dane)))
