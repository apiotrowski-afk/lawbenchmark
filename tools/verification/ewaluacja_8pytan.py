#!/usr/bin/env python3
"""Ewaluacja testu meta-sędziego na pytaniach, na których nie był strojony (2026-10-23).

Łączy: raporty faktów (raporty/<P>_<system>.json), błędy z kart (bledy_z_kart.py → _bledy_z_kart_*.json)
i — jeśli jest — raport weryfikatora poparcia (JSON z poparcie.py). Liczy per pytanie i zbiorczo:
  - zasięg: powołania, sprawdzone, nieobsługiwane, nie istnieje / nie znaleziono, tekst_niedostepny / brak_dowodu;
  - czułość kroku faktów (F/W/S) i weryfikatora poparcia (T, orzeczenia, ogólniki B9) wobec błędów z kart;
  - fałszywe alarmy na powołaniach „✓” z kart i na powołaniach, których karta nie wymienia;
  - błędy z kart, których krok faktów w ogóle nie wyodrębnił (regex powołań).
Reguły zamrożone (fakty.py / poparcie.py) — skrypt tylko liczy.

Użycie: python -I ewaluacja_8pytan.py P01 P04 … --karty raporty/_bledy_z_kart_8pytan_2026-10-23.json [--poparcie plik.json] [--md wyjscie.md]
"""
from __future__ import annotations

import argparse
import json
import re
import os
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAPORTY = HERE.parents[1] / "verification" / "reports"
SYSTEMY = ["chatgpt_codex_w0_r3", "chatgpt_codex_web_r3", "codex_astra6_w0_r3", "codex_astra6_web_r3",
           "codex_terra56_w0_r3", "codex_terra56_web_r3", "haiku_cli_w0_r3", "haiku_cli_w1_r3",
           "sonnet_cli_w0_r3", "sonnet_cli_w1_r3", "opus_cli_w0_r3", "opus_cli_w1_r3",
           "gemini38flash_vertex_w0_r3", "gemini38flash_vertex_w1_r3",
           "argon4_high_vertex_w0_r3", "argon4_high_vertex_w1_r3"]

ERR_P = {"nie_znaleziono", "nie_znaleziono_akt_domniemany", "niedoslowny", "niedoslowny_zgodny_z_wersja_wczesniejsza",
         "niedoslowny_blizszy_wersji_wczesniejszej", "uchylony", "slowa_wersji_wczesniejszej"}
ERR_O = {"nie_znaleziono", "inna_data", "inny_sad"}
WYKRYCIE = {"nie_na_temat", "przeczy"}
WYKRYCIE_OGOLNIK = {"przeczy", "mieszane"}
# oczekiwane źródło wykrycia wg klasy błędu z karty
OCZEKIWANE = {"F": "fakty", "W": "fakty", "S": "fakty", "T": "poparcie"}

_SUP = {ord(c): d for c, d in zip("¹²³⁴⁵⁶⁷⁸⁹⁰", "1234567890")}
_SUP.update({ord(c): d for c, d in zip("ᵃᵇᶜᵈᵉ", "abcde")})
AKT_KOD = {"KPC": "KPC", "KC": "KC", "KK": "KK", "KW": "KW", "KPA": "KPA", "KPK": "KPK", "KRO": "KRO", "KKS": "KKS",
           "PPSA": "PPSA", "PrAut": "PrAut", "u.k.s.c.": "u.k.s.c.", "u.k.w.h.": "u.k.w.h.", "AI Act": "AI Act", "RODO": "RODO",
           "u.k.k.": "u.k.k.", "u.n.n.c.": "UNNC"}     # UNNC: legal-cite feat/unnc (decyzja Adama nr 3, 2026-10-24)
# decyzja Adama nr 6 (2026-10-24): kanoniczny plik poparcia biegu 24.10 to wersja przemapowana „b” (A2b); oryginał zachowany
POPARCIE_KANONICZNE_2026_10_24 = RAPORTY / "_poparcie_8pytan_2026-10-24b.json"


def nn(s: str | None) -> str:
    return (s or "").translate(_SUP).replace("^", "").replace(" ", "").lower()


def fakty_art(powolanie: str) -> tuple[str, str | None]:
    m = re.match(r"art\.\s*(\S+?)(?:\s+(?:ust\.|§)\s*(\S+))?(?:\s+pkt|\s|$)", powolanie)
    return (nn(m.group(1)), nn(m.group(2)) if m.group(2) else None) if m else ("", None)


def match_prov(ent: dict, b: dict) -> str | None:
    """Dopasowanie wpisu raportu faktów do błędu z karty: zwraca „pełne” / „po artykule” / None."""
    a, u = fakty_art(ent["powolanie"])
    if a != nn(b.get("art")):
        return None
    kod = (ent.get("akt") or {}).get("kod_legal_cite")
    if b.get("akt") and kod and AKT_KOD.get(b["akt"]) and AKT_KOD[b["akt"]] != kod:
        return None
    bu = nn(b.get("jednostka")) if b.get("jednostka") else None
    if bu and u and bu != u:
        return None
    return "pełne" if (bu == u or not bu) else "po artykule"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pytania", nargs="+")
    ap.add_argument("--karty", required=True)
    ap.add_argument("--poparcie", help=f"JSON weryfikatora poparcia; bez podania: {POPARCIE_KANONICZNE_2026_10_24.name} (kanoniczny, decyzja nr 6)")
    ap.add_argument("--md")
    ap.add_argument("--json")
    ap.add_argument("--flagi-klasowe", action="store_true",
                    help="flagi kroku faktów liczone jako błąd tylko, gdy mapują się na klasę A6 (B1): nie_znaleziono, uchylony, cytat zgodny/bliższy wersji wcześniejszej; orzeczenia: inna_data, inny_sad")
    ap.add_argument("--raporty", help="katalog raportów faktów (domyślnie meta_sedzia/raporty; do porównania przed/po: (archiwum wewnętrzne, poza repozytorium)…)")
    args = ap.parse_args()
    global RAPORTY, ERR_P, ERR_O
    if args.raporty:
        RAPORTY = Path(args.raporty)
    if args.flagi_klasowe:
        ERR_P = {"nie_znaleziono", "uchylony", "niedoslowny_zgodny_z_wersja_wczesniejsza", "niedoslowny_blizszy_wersji_wczesniejszej"}
        ERR_O = {"inna_data", "inny_sad"}
    karty = json.loads(Path(args.karty).read_text())
    if not args.poparcie and POPARCIE_KANONICZNE_2026_10_24.exists():
        args.poparcie = str(POPARCIE_KANONICZNE_2026_10_24)
    pop = json.loads(Path(args.poparcie).read_text()) if args.poparcie else None
    pop_by = {}
    pop_og = {}
    if pop:
        for z in pop["powolania"]:
            pop_by.setdefault((z["P"], z["system"]), []).append(z)
        for g in pop["ogolniki"]:
            pop_og.setdefault((g["P"], g["system"]), []).append(g)

    per_p = {}
    bledy_rows, fa_rows, brak_rows = [], [], []
    for p in args.pytania:
        st = {"karty": 0, "przepisy": 0, "orzeczenia": 0, "sprawdzone_p": 0, "sprawdzone_o": 0, "nieobslugiwane": 0,
              "nie_istnieje": 0, "blad_weryfikacji": 0, "orz_nie_znaleziono": 0, "orz_poza": 0,
              "pop_ocenione": 0, "pop_tekst_niedostepny": 0, "pop_brak_dowodu": 0, "pop_brak_twierdzenia": 0,
              "bledy": [], "fa_fakty_ok": 0, "fa_fakty_inne": 0, "fa_pop_ok": 0, "fa_pop_inne": 0, "ok_n": 0,
              "og_alarm_inne": 0, "og_n": 0, "kart_do_reki": 0, "hal_tak": 0}
        per_p[p] = st
        for s in SYSTEMY:
            f = RAPORTY / f"{p}_{s}.json"
            k = karty.get(f"{p}|{s}")
            if not f.exists() or not k:
                continue
            r = json.loads(f.read_text())
            st["karty"] += 1
            st["kart_do_reki"] += bool(k["do_recznego_sprawdzenia"])
            st["hal_tak"] += k["hallucinated"] == "tak"
            przepisy, orzeczenia = r["przepisy"], r["orzeczenia"]
            st["przepisy"] += len(przepisy)
            st["orzeczenia"] += len(orzeczenia)
            for e in przepisy:
                stt = e["weryfikacja"]["status"]
                st["sprawdzone_p"] += stt == "istnieje"
                st["nieobslugiwane"] += stt.startswith("nieobsługiwany")
                st["nie_istnieje"] += stt == "nie istnieje"
                st["blad_weryfikacji"] += stt.startswith("błąd")
            for o in orzeczenia:
                stt = o["weryfikacja"]["status"]
                st["sprawdzone_o"] += stt.startswith("znaleziono")
                st["orz_nie_znaleziono"] += stt.startswith("nie znaleziono")
                st["orz_poza"] += stt.startswith("poza")
            pz = pop_by.get((p, s), [])
            for z in pz:
                et = z["wynik"]["etykieta"]
                st["pop_brak_twierdzenia"] += et == "brak_twierdzenia"
                st["pop_tekst_niedostepny"] += et == "tekst_niedostepny"
                st["pop_brak_dowodu"] += et == "brak_dowodu"
                st["pop_ocenione"] += et not in ("brak_twierdzenia", "tekst_niedostepny", "brak_dowodu")
            uzyte_p, uzyte_o = set(), set()
            # ── błędy z karty ──
            for b in k["bledy"]:
                row = {"P": p, "system": s, "klasa": b["klasa"], "rodzaj": b["rodzaj"], "powolanie": b.get("napis") or b.get("opis"),
                       "akt": b.get("akt"), "wpisy": 0, "fakty_flagi": [], "fakty": False, "poparcie": [], "pop": False,
                       "oczekiwane": OCZEKIWANE.get(b["klasa"], "?")}
                if b["rodzaj"] == "przepis":
                    ents = [(e, match_prov(e, b)) for e in przepisy]
                    ents = [(e, m) for e, m in ents if m]
                    if any(m == "pełne" for _, m in ents):
                        ents = [(e, m) for e, m in ents if m == "pełne"]
                    row["wpisy"] = len(ents)
                    for e, _ in ents:
                        uzyte_p.add(e["id"])
                        row["fakty_flagi"] += sorted(set(e["flagi"]) & ERR_P)
                        if e["weryfikacja"]["status"] != "istnieje" and not (set(e["flagi"]) & ERR_P):
                            row["fakty_flagi"].append(f"status: {e['weryfikacja']['status']}")
                        for z in pz:
                            if z["rodzaj"] == "przepis" and z["id"] == e["id"]:
                                row["poparcie"].append(z["wynik"]["etykieta"])
                elif b["rodzaj"] == "orzeczenie":
                    ents = [o for o in orzeczenia if re.sub(r"\s+", " ", o["sygnatura"]) == b["sygnatura"]]
                    row["wpisy"] = len(ents)
                    for o in ents:
                        uzyte_o.add(o["sygnatura"])
                        row["fakty_flagi"] += sorted(set(o["flagi"]) & ERR_O)
                        if not o["weryfikacja"]["status"].startswith("znaleziono"):
                            row["fakty_flagi"].append(f"status: {o['weryfikacja']['status']}")
                        for z in pz:
                            if z["rodzaj"] == "orzeczenie" and z["powolanie"] == o["sygnatura"]:
                                row["poparcie"].append(z["wynik"]["etykieta"])
                row["fakty"] = any(f in ERR_P | ERR_O for f in row["fakty_flagi"])
                row["pop"] = any(e in WYKRYCIE for e in row["poparcie"])
                row["wykryte"] = row["fakty"] or row["pop"]
                if b["rodzaj"] in ("przepis", "orzeczenie") and row["wpisy"] == 0:
                    brak_rows.append(row)
                bledy_rows.append(row)
                st["bledy"].append(row)
            # ogólniki B9
            for g in k["ogolniki_b9"]:
                ogs = pop_og.get((p, s), [])
                row = {"P": p, "system": s, "klasa": g["klasa"], "rodzaj": "ogólnik B9", "powolanie": g["opis"], "wpisy": len(ogs),
                       "fakty_flagi": [], "fakty": False, "poparcie": [x["wynik"]["etykieta"] for x in ogs],
                       "pop": any(x["wynik"]["etykieta"] in WYKRYCIE_OGOLNIK for x in ogs), "oczekiwane": "poparcie (B9)"}
                row["wykryte"] = row["pop"]
                bledy_rows.append(row)
                st["bledy"].append(row)
            # ── fałszywe alarmy ──
            ok_p = [c for c in k["poprawne"] if c["rodzaj"] == "przepis"]
            ok_o = {c["sygnatura"] for c in k["poprawne"] if c["rodzaj"] == "orzeczenie"}
            st["ok_n"] += len(k["poprawne"])

            def is_ok(e):
                return any(match_prov(e, c) for c in ok_p)

            for e in przepisy:
                if e["id"] in uzyte_p:
                    continue
                fl = sorted(set(e["flagi"]) & ERR_P)
                if fl:
                    ok = is_ok(e)
                    st["fa_fakty_ok" if ok else "fa_fakty_inne"] += 1
                    fa_rows.append({"P": p, "system": s, "zrodlo": "fakty", "rodzaj": "przepis", "powolanie": e["powolanie"],
                                    "karta": "✓" if ok else "nie wymienia", "sygnal": ", ".join(fl), "akt": e["akt"]["ustalenie"]})
                for z in pz:
                    if z["rodzaj"] == "przepis" and z["id"] == e["id"] and z["wynik"]["etykieta"] in WYKRYCIE:
                        ok = is_ok(e)
                        st["fa_pop_ok" if ok else "fa_pop_inne"] += 1
                        fa_rows.append({"P": p, "system": s, "zrodlo": "poparcie", "rodzaj": "przepis", "powolanie": e["powolanie"],
                                        "karta": "✓" if ok else "nie wymienia", "sygnal": z["wynik"]["etykieta"],
                                        "uzasadnienie": (z["wynik"].get("uzasadnienie") or "")[:220], "twierdzenie": (z.get("twierdzenie") or "")[:160]})
            for o in orzeczenia:
                if o["sygnatura"] in uzyte_o:
                    continue
                fl = sorted(set(o["flagi"]) & ERR_O)
                ok = o["sygnatura"] in ok_o
                if fl:
                    st["fa_fakty_ok" if ok else "fa_fakty_inne"] += 1
                    fa_rows.append({"P": p, "system": s, "zrodlo": "fakty", "rodzaj": "orzeczenie", "powolanie": o["sygnatura"],
                                    "karta": "✓" if ok else "nie wymienia", "sygnal": ", ".join(fl),
                                    "akt": f"podany {o['sad_podany']} {o['data_podana']}; w źródle {o['weryfikacja'].get('sad_wyroku')} {o['weryfikacja'].get('data_wyroku')}"})
                for z in pz:
                    if z["rodzaj"] == "orzeczenie" and z["powolanie"] == o["sygnatura"] and z["wynik"]["etykieta"] in WYKRYCIE:
                        st["fa_pop_ok" if ok else "fa_pop_inne"] += 1
                        fa_rows.append({"P": p, "system": s, "zrodlo": "poparcie", "rodzaj": "orzeczenie", "powolanie": o["sygnatura"],
                                        "karta": "✓" if ok else "nie wymienia", "sygnal": z["wynik"]["etykieta"],
                                        "uzasadnienie": (z["wynik"].get("uzasadnienie") or "")[:220], "twierdzenie": (z.get("twierdzenie") or "")[:160]})
            ogs = pop_og.get((p, s), [])
            st["og_n"] += len(ogs)
            if not k["ogolniki_b9"]:
                st["og_alarm_inne"] += sum(x["wynik"]["etykieta"] in WYKRYCIE_OGOLNIK for x in ogs)

    # ───────── raport ─────────
    L = []
    L.append("| P | karty | hal. tak | powołania (przep./orz.) | sprawdzone | nieobsł. | nie istnieje / błąd | orz. nie znal. / poza | "
             "poparcie: ocenione / tekst_niedostepny / brak_dowodu / wzmianki | błędy kart (z powołaniem) | wykryte F/W/S (fakty) | wykryte T (poparcie) | B9 | nie wyodrębnione | FA fakty (✓ / inne) | FA poparcie (✓ / inne) | ✓ w kartach | kart do ręki |")
    L.append("|" + "---|" * 18)
    tot = {}
    for p, st in per_p.items():
        bl = [b for b in st["bledy"] if b["rodzaj"] in ("przepis", "orzeczenie")]
        fws = [b for b in bl if b["klasa"] in "FWS"]
        t = [b for b in bl if b["klasa"] == "T"]
        b9 = [b for b in st["bledy"] if b["rodzaj"] == "ogólnik B9"]
        niew = [b for b in bl if b["wpisy"] == 0]
        vals = dict(karty=st["karty"], hal=st["hal_tak"], pw=st["przepisy"], ow=st["orzeczenia"], sp=st["sprawdzone_p"], so=st["sprawdzone_o"],
                    nieob=st["nieobslugiwane"], nie=st["nie_istnieje"], bl=st["blad_weryfikacji"], onz=st["orz_nie_znaleziono"], opz=st["orz_poza"],
                    po=st["pop_ocenione"], ptn=st["pop_tekst_niedostepny"], pbd=st["pop_brak_dowodu"], pbt=st["pop_brak_twierdzenia"],
                    nbl=len(bl), fws_n=len(fws), fws_w=sum(b["fakty"] for b in fws), t_n=len(t), t_w=sum(b["pop"] for b in t),
                    t_wf=sum(b["fakty"] and not b["pop"] for b in t), b9_n=len(b9), b9_w=sum(b["pop"] for b in b9), niew=len(niew),
                    fafo=st["fa_fakty_ok"], fafi=st["fa_fakty_inne"], fapo=st["fa_pop_ok"], fapi=st["fa_pop_inne"], ok=st["ok_n"], reka=st["kart_do_reki"])
        for kk, v in vals.items():
            tot[kk] = tot.get(kk, 0) + v
        L.append(f"| {p} | {vals['karty']} | {vals['hal']} | {vals['pw']} / {vals['ow']} | {vals['sp']} / {vals['so']} | {vals['nieob']} | {vals['nie']} / {vals['bl']} | "
                 f"{vals['onz']} / {vals['opz']} | {vals['po']} / {vals['ptn']} / {vals['pbd']} / {vals['pbt']} | {vals['nbl']} | {vals['fws_w']}/{vals['fws_n']} | "
                 f"{vals['t_w']}/{vals['t_n']} (+{vals['t_wf']} tylko fakty) | {vals['b9_w']}/{vals['b9_n']} | {vals['niew']} | {vals['fafo']} / {vals['fafi']} | {vals['fapo']} / {vals['fapi']} | {vals['ok']} | {vals['reka']} |")
    v = tot
    L.append(f"| **razem** | {v['karty']} | {v['hal']} | {v['pw']} / {v['ow']} | {v['sp']} / {v['so']} | {v['nieob']} | {v['nie']} / {v['bl']} | {v['onz']} / {v['opz']} | "
             f"{v['po']} / {v['ptn']} / {v['pbd']} / {v['pbt']} | {v['nbl']} | {v['fws_w']}/{v['fws_n']} | {v['t_w']}/{v['t_n']} (+{v['t_wf']} tylko fakty) | {v['b9_w']}/{v['b9_n']} | {v['niew']} | "
             f"{v['fafo']} / {v['fafi']} | {v['fapo']} / {v['fapi']} | {v['ok']} | {v['reka']} |")
    L.append("")
    allbl = [b for b in bledy_rows if b["rodzaj"] in ("przepis", "orzeczenie")]
    wyk = sum(b["wykryte"] for b in allbl)
    L.append(f"Zbiorczo: błędy z kart z powołaniem {len(allbl)}, wykryte (fakty lub poparcie) {wyk} = {wyk / max(1, len(allbl)):.0%}; "
             f"w tym nie wyodrębnione przez regex {v['niew']}. Fałszywe alarmy na ✓: fakty {v['fafo']} / {v['ok']} ✓ = {v['fafo'] / max(1, v['ok']):.1%}, "
             f"poparcie {v['fapo']} / {v['ok']} ✓ = {v['fapo'] / max(1, v['ok']):.1%}. Dla porównania P09/P10 (strojenie): czułość 65 %, FA 1 %.")
    L.append("")
    L.append("## Błędy z kart — szczegóły\n")
    L.append("| P | system | klasa | rodzaj | powołanie | wpisy w raporcie faktów | flagi faktów | etykiety poparcia | wykryte |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for b in bledy_rows:
        L.append(f"| {b['P']} | {b['system']} | {b['klasa']} | {b['rodzaj']} | {b['powolanie']} | {b['wpisy']} | {', '.join(b['fakty_flagi']) or '—'} | "
                 f"{', '.join(str(x or 'status') for x in b['poparcie']) or '—'} | {'tak' if b['wykryte'] else 'nie'} |")
    L.append("")
    L.append("## Fałszywe alarmy (powołanie bez błędu w karcie)\n")
    L.append("| P | system | źródło | rodzaj | powołanie | karta | sygnał | szczegół |")
    L.append("|---|---|---|---|---|---|---|---|")
    for x in fa_rows:
        L.append(f"| {x['P']} | {x['system']} | {x['zrodlo']} | {x['rodzaj']} | {x['powolanie']} | {x['karta']} | {x['sygnal']} | "
                 f"{x.get('akt') or ''}{(' tw.: ' + x['twierdzenie'] + ' — ' + x['uzasadnienie']) if x.get('uzasadnienie') else ''} |")
    # ───────── klasy A6 (B1, 2026-10-24): czułość per klasa i fałszywe alarmy per klasa ─────────
    if pop and any("klasa_A6" in z for z in pop["powolania"]):
        L += klasy_a6_sekcja(args.pytania, karty, pop_by)
    txt = "\n".join(L)
    print(txt)
    if args.md:
        Path(args.md).write_text(txt + "\n")
    if args.json:
        Path(args.json).write_text(json.dumps({"per_p": {p: {k: v for k, v in st.items() if k != "bledy"} for p, st in per_p.items()},
                                               "bledy": bledy_rows, "falszywe": fa_rows}, ensure_ascii=False, indent=1))


def klasy_a6_sekcja(pytania, karty, pop_by) -> list[str]:
    """Czułość i fałszywe alarmy wg KLASY A6 (✓/F/T/W/S) z weryfikatora poparcia wobec błędów z kart.
    Wykrycie „ta sama klasa” = któryś wpis dopasowany do błędu karty ma tę klasę; „dowolny błąd” = klasę F/T/W/S."""
    KL = ["F", "T", "W", "S"]
    sens = {k: {"n": 0, "ta_sama": 0, "dowolna": 0, "status": 0, "brak_wpisu": 0} for k in KL}
    fa = {k: 0 for k in KL}
    fa_inne = {k: 0 for k in KL}
    ok_n = 0
    statusy = {}
    szczegoly = []
    for p in pytania:
        for s in SYSTEMY:
            f = RAPORTY / f"{p}_{s}.json"
            k = karty.get(f"{p}|{s}")
            if not f.exists() or not k:
                continue
            r = json.loads(f.read_text())
            by_id = {("przepis", str(e["id"])): e for e in r["przepisy"]}
            by_id.update({("orzeczenie", f"o{i}"): o for i, o in enumerate(r["orzeczenia"])})
            rows = pop_by.get((p, s), [])
            for z in rows:
                if z.get("status_weryfikacji"):
                    statusy[z["status_weryfikacji"]] = statusy.get(z["status_weryfikacji"], 0) + 1
            uzyte = set()
            for b in k["bledy"]:
                if b["rodzaj"] not in ("przepis", "orzeczenie") or b["klasa"] not in KL:
                    continue
                dop = []
                for z in rows:
                    e = by_id.get((z["rodzaj"], str(z["id"])))
                    if not e:
                        continue
                    if b["rodzaj"] == "przepis" and z["rodzaj"] == "przepis":
                        m = match_prov(e, b)
                        if m:
                            dop.append((z, m))
                    elif b["rodzaj"] == "orzeczenie" and z["rodzaj"] == "orzeczenie" and re.sub(r"\s+", " ", e["sygnatura"]) == b.get("sygnatura"):
                        dop.append((z, "pełne"))
                if any(m == "pełne" for _, m in dop):
                    dop = [(z, m) for z, m in dop if m == "pełne"]
                # człony łańcucha: liczy się klasa powołania głównego
                klasy = set()
                for z, _ in dop:
                    uzyte.add((z["rodzaj"], str(z["id"])))
                    kl = z.get("klasa_A6")
                    if not kl and z.get("status_weryfikacji") == "w_zwiazku":
                        g = next((y for y in rows if y["rodzaj"] == "przepis" and str(y["id"]) == str(z.get("powolanie_glowne_id"))), None)
                        kl = g.get("klasa_A6") if g else None
                    if kl:
                        klasy.add(kl)
                st = sens[b["klasa"]]
                st["n"] += 1
                if not dop:
                    st["brak_wpisu"] += 1
                elif b["klasa"] in klasy:
                    st["ta_sama"] += 1
                    st["dowolna"] += 1
                elif klasy & set(KL):
                    st["dowolna"] += 1
                elif not klasy:
                    st["status"] += 1
                szczegoly.append((p, s, b["klasa"], b.get("napis") or b.get("opis"), sorted(klasy) or ["—"],
                                  sorted({z.get("status_weryfikacji") or "" for z, _ in dop} - {""}) or ["—"]))
            ok_p = [c for c in k["poprawne"] if c["rodzaj"] == "przepis"]
            ok_o = {c["sygnatura"] for c in k["poprawne"] if c["rodzaj"] == "orzeczenie"}
            ok_n += len(k["poprawne"])
            for z in rows:
                kl = z.get("klasa_A6")
                if kl not in KL or (z["rodzaj"], str(z["id"])) in uzyte:
                    continue
                e = by_id.get((z["rodzaj"], str(z["id"])))
                if not e:
                    continue
                ok = any(match_prov(e, c) for c in ok_p) if z["rodzaj"] == "przepis" else e["sygnatura"] in ok_o
                (fa if ok else fa_inne)[kl] += 1
    L = ["", "## Klasy A6 (B1) — czułość per klasa i fałszywe alarmy per klasa", "",
         "| klasa karty | n | wykryte: ta sama klasa | wykryte: dowolna klasa błędu | tylko status weryfikacji | brak wpisu (nie wyodrębnione) | czułość (ta sama / dowolna) |",
         "|---|---|---|---|---|---|---|"]
    for kcl in KL:
        st = sens[kcl]
        L.append(f"| {kcl} | {st['n']} | {st['ta_sama']} | {st['dowolna']} | {st['status']} | {st['brak_wpisu']} | "
                 f"{st['ta_sama'] / max(1, st['n']):.0%} / {st['dowolna'] / max(1, st['n']):.0%} |")
    n_all = sum(sens[k]["n"] for k in KL)
    L.append(f"| **razem** | {n_all} | {sum(sens[k]['ta_sama'] for k in KL)} | {sum(sens[k]['dowolna'] for k in KL)} | "
             f"{sum(sens[k]['status'] for k in KL)} | {sum(sens[k]['brak_wpisu'] for k in KL)} | "
             f"{sum(sens[k]['ta_sama'] for k in KL) / max(1, n_all):.0%} / {sum(sens[k]['dowolna'] for k in KL) / max(1, n_all):.0%} |")
    L += ["", "| klasa nadana | fałszywe alarmy na ✓ z kart | na powołaniach, których karta nie wymienia | odsetek FA na ✓ |", "|---|---|---|---|"]
    for kcl in KL:
        L.append(f"| {kcl} | {fa[kcl]} | {fa_inne[kcl]} | {fa[kcl] / max(1, ok_n):.1%} |")
    L.append(f"| **razem** | {sum(fa.values())} | {sum(fa_inne.values())} | {sum(fa.values()) / max(1, ok_n):.1%} (✓ w kartach: {ok_n}) |")
    L.append("")
    L.append("Statusy weryfikacji (nie liczone jako błąd): " + ", ".join(f"{k} {v}" for k, v in sorted(statusy.items(), key=lambda x: -x[1])))
    L += ["", "### Błędy z kart — klasa karty vs klasa weryfikatora", "", "| P | system | klasa karty | powołanie | klasy weryfikatora | statusy |", "|---|---|---|---|---|---|"]
    for p, s, kcl, pw, kls, sts in szczegoly:
        L.append(f"| {p} | {s} | {kcl} | {pw} | {', '.join(kls)} | {', '.join(sts)} |")
    return L


if __name__ == "__main__":
    main()
