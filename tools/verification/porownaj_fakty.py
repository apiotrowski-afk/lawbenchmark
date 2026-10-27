"""Porównanie raportów faktów (meta_sedzia/raporty) z kartami P09/P10 r3 — czułość i fałszywe alarmy.
Lista błędów spisana ręcznie z pól A6/A3 kart (stan 2026-10-19)."""
import json
import re
import sys
from pathlib import Path

R = Path("tools/verification/raporty")
SYS = ["chatgpt_codex_w0_r3", "chatgpt_codex_web_r3", "codex_astra6_w0_r3", "codex_astra6_web_r3",
       "codex_terra56_w0_r3", "codex_terra56_web_r3", "haiku_cli_w0_r3", "haiku_cli_w1_r3",
       "sonnet_cli_w0_r3", "sonnet_cli_w1_r3", "opus_cli_w0_r3", "opus_cli_w1_r3",
       "gemini38flash_vertex_w0_r3", "gemini38flash_vertex_w1_r3",
       "argon4_high_vertex_w0_r3", "argon4_high_vertex_w1_r3"]

# (P, system, klasa, rodzaj, wzorzec: ("p", art, jednostka|None, akt_substr|None) / ("o", sygnatura) / ("g",))
A6 = [
    ("P09", "haiku_cli_w0_r3", "T", "przepis", ("p", "65", None, "autorskie")),
    ("P09", "haiku_cli_w1_r3", "T", "przepis", ("p", "41", "1", None)),
    ("P09", "haiku_cli_w1_r3", "T", "przepis", ("p", "65", None, "autorskie")),
    ("P09", "haiku_cli_w1_r3", "T", "przepis", ("p", "43|44", None, None)),
    ("P09", "sonnet_cli_w0_r3", "T", "przepis", ("p", "41", "4", None)),
    ("P09", "sonnet_cli_w0_r3", "T", "przepis", ("p", "50", None, None)),
    ("P09", "sonnet_cli_w1_r3", "F", "przepis", ("p", "55¹", None, None)),
    ("P09", "sonnet_cli_w1_r3", "W", "przepis", ("p", "44", None, None)),
    ("P09", "opus_cli_w0_r3", "W", "przepis", ("p", "44", None, None)),
    ("P09", "opus_cli_w1_r3", "T", "przepis", ("p", "64", None, None)),
    ("P09", "opus_cli_w1_r3", "T", "przepis", ("p", "41", "5", None)),
    ("P09", "opus_cli_w1_r3", "T", "ogólnik B9", ("g",)),
    ("P09", "gemini38flash_vertex_w0_r3", "T", "ogólnik B9", ("g",)),
    ("P09", "gemini38flash_vertex_w1_r3", "T", "orzeczenie", ("o", "III CK 400/03")),
    ("P09", "argon4_high_vertex_w1_r3", "T", "orzeczenie", ("o", "I CSK 237/10")),
    ("P09", "argon4_high_vertex_w1_r3", "T", "orzeczenie", ("o", "V CSK 373/10")),
    ("P10", "codex_terra56_web_r3", "W", "przepis", ("p", "78", "2", "cywilny")),
    ("P10", "haiku_cli_w0_r3", "F", "przepis", ("p", "53", "1", None)),
    ("P10", "haiku_cli_w0_r3", "T", "przepis", ("p", "65", None, "autorskie")),
    ("P10", "haiku_cli_w1_r3", "T", "przepis", ("p", "41", "3", None)),
    ("P10", "sonnet_cli_w0_r3", "F", "przepis", ("p", "65", "1", None)),
    ("P10", "sonnet_cli_w1_r3", "T", "przepis", ("p", "436", None, None)),
    ("P10", "sonnet_cli_w1_r3", "T", "przepis", ("p", "56|49", None, None)),
    ("P10", "sonnet_cli_w1_r3", "T", "przepis", ("p", "41", "3", None)),
    ("P10", "sonnet_cli_w1_r3", "W", "przepis", ("p", "44", None, None)),
    ("P10", "opus_cli_w0_r3", "W", "przepis", ("p", "44", None, None)),
    ("P10", "opus_cli_w1_r3", "T", "ogólnik B9", ("g",)),
    ("P10", "gemini38flash_vertex_w0_r3", "T", "ogólnik B9", ("g",)),
    ("P10", "argon4_high_vertex_w0_r3", "T", "orzeczenie", ("o", "II CSKP 526/22")),
    ("P10", "argon4_high_vertex_w1_r3", "S", "orzeczenie", ("o", "I ACa 1188/12")),
]
# A3 = 0 (cytat art. 41 ust. 2 niezgodny z obowiązującym brzmieniem)
A3 = [(p, s, ("p", "41", "2", None)) for p, s in [
    ("P09", "opus_cli_w1_r3"), ("P09", "gemini38flash_vertex_w0_r3"), ("P09", "gemini38flash_vertex_w1_r3"),
    ("P09", "argon4_high_vertex_w0_r3"), ("P10", "gemini38flash_vertex_w0_r3"),
    ("P10", "gemini38flash_vertex_w1_r3"), ("P10", "argon4_high_vertex_w0_r3")]]

ERR_P = {"nie_znaleziono", "nie_znaleziono_akt_domniemany", "niedoslowny", "niedoslowny_zgodny_z_wersja_wczesniejsza",
         "niedoslowny_blizszy_wersji_wczesniejszej", "uchylony", "slowa_wersji_wczesniejszej"}
ERR_O = {"nie_znaleziono", "inna_data", "inny_sad"}


def art_unit(pow_: str):
    m = re.match(r"art\. (\S+?)(?: (?:ust\.|§) (\S+))?(?: pkt|\s|$)", pow_)
    return (m.group(1), m.group(2)) if m else (None, None)


def match_p(e, pat):
    _, art, unit, akt = pat
    a, u = art_unit(e["powolanie"])
    if not a or not re.fullmatch(art, a):
        return False
    if unit and u != unit:
        return False
    if akt and akt not in (e["akt"]["nazwa"] or "").lower():
        return False
    return True


def main():
    rows, fa, a3hits, used = [], [], [], set()
    for (p, s, kl, rodz, pat) in A6:
        r = json.loads((R / f"{p}_{s}.json").read_text())
        flags, how = set(), ""
        if pat[0] == "p":
            ents = [e for e in r["przepisy"] if match_p(e, pat)]
            for e in ents:
                flags |= set(e["flagi"]) & ERR_P
                if set(e["flagi"]) & ERR_P:
                    used.add((p, s, "p", e["id"]))
            how = f"{len(ents)} wpisów"
        elif pat[0] == "o":
            ents = [o for o in r["orzeczenia"] if o["sygnatura"] == pat[1]]
            for o in ents:
                flags |= set(o["flagi"]) & ERR_O
                if set(o["flagi"]) & ERR_O:
                    used.add((p, s, "o", o["sygnatura"]))
            how = f"{len(ents)} wpisów"
        rows.append((p, s, kl, rodz, pat, sorted(flags), how))
    for (p, s, pat) in A3:
        r = json.loads((R / f"{p}_{s}.json").read_text())
        ents = [e for e in r["przepisy"] if match_p(e, pat)]
        fl = set()
        for e in ents:
            f = {x for x in e["flagi"] if x.startswith("niedoslowny")}
            fl |= f
            if f:
                used.add((p, s, "p", e["id"]))
        pub = [x for x in r["publikatory"] if "nieaktualny_tj" in x["flagi"]]
        a3hits.append((p, s, sorted(fl), bool(pub)))
    for p in ("P09", "P10"):
        for s in SYS:
            r = json.loads((R / f"{p}_{s}.json").read_text())
            for e in r["przepisy"]:
                if set(e["flagi"]) & ERR_P and (p, s, "p", e["id"]) not in used:
                    # wpisy tego samego przepisu, którego błąd jest w karcie, też liczymy jako trafione
                    if any(rp == p and rs == s and pat[0] == "p" and match_p(e, pat) for (rp, rs, _, _, pat) in A6):
                        continue
                    fa.append((p, s, "przepis", e["powolanie"], sorted(set(e["flagi"]) & ERR_P), e["akt"]["ustalenie"]))
            for o in r["orzeczenia"]:
                if set(o["flagi"]) & ERR_O and (p, s, "o", o["sygnatura"]) not in used:
                    fa.append((p, s, "orzeczenie", o["sygnatura"], sorted(set(o["flagi"]) & ERR_O), ""))
    out = ["## Błędy A6 z kart (F/T/W/S) a flagi raportu faktów", "",
           "| P | system | klasa | rodzaj | powołanie | flagi raportu | wykryte |", "|---|---|---|---|---|---|---|"]
    for (p, s, kl, rodz, pat, fl, how) in rows:
        pw = {"p": lambda: f"art. {pat[1]}" + (f" ust./§ {pat[2]}" if pat[2] else ""), "o": lambda: pat[1], "g": lambda: "—"}[pat[0]]()
        out.append(f"| {p} | {s} | {kl} | {rodz} | {pw} | {', '.join(fl) or '—'} | {'tak' if fl else 'nie'} |")
    out += ["", "## A3 = 0 w kartach (cytat niezgodny z obowiązującym brzmieniem)", "",
            "| P | system | flaga cytatu | nieaktualny t.j. w publikatorze |", "|---|---|---|---|"]
    for p, s, fl, pub in a3hits:
        out.append(f"| {p} | {s} | {', '.join(fl) or '—'} | {'tak' if pub else 'nie'} |")
    out += ["", "## Flagi bez błędu w karcie (fałszywe alarmy)", "", "| P | system | rodzaj | powołanie | flagi | akt |", "|---|---|---|---|---|---|"]
    for x in fa:
        out.append(f"| {x[0]} | {x[1]} | {x[2]} | {x[3]} | {', '.join(x[4])} | {x[5]} |")
    # podsumowanie
    def stat(sel):
        sel = list(sel)
        return f"{sum(1 for x in sel if x[5])}/{len(sel)}"
    out += ["", "## Podsumowanie", "",
            f"- A6 razem: {stat(rows)}; F: {stat(x for x in rows if x[2]=='F')}; W: {stat(x for x in rows if x[2]=='W')}; "
            f"S: {stat(x for x in rows if x[2]=='S')}; T: {stat(x for x in rows if x[2]=='T')}",
            f"- A6 bez ogólników B9 (powołania z numerem/sygnaturą): {stat(x for x in rows if x[3] != 'ogólnik B9')}",
            f"- A3: flaga cytatu {sum(1 for x in a3hits if x[2])}/{len(a3hits)}; flaga t.j. {sum(1 for x in a3hits if x[3])}/{len(a3hits)}",
            f"- fałszywe alarmy: {len(fa)} (przepisy {sum(1 for x in fa if x[2]=='przepis')}, orzeczenia {sum(1 for x in fa if x[2]=='orzeczenie')})"]
    txt = "\n".join(out)
    print(txt)
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(txt + "\n")


main()
