#!/usr/bin/env python3
"""Przemapowanie klas A6 w raporcie poparcia po zmianie kroku faktów BEZ ponownego wołania sędziego (0 USD).

Użyte 2026-10-24: po biegu poparcia (7,9 USD) doprecyzowano regułę aktu domniemanego (A2: brak aktu domyślnego,
gdy podstawy_wymagane klucza nazywają kilka aktów — P04: u.n.n.c. + k.p.a.). Nowy krok faktów zmienia tylko STATUSY
(więcej „akt nieustalony”), nie treść źródeł, więc oceny sędziego dla pozostałych powołań pozostają ważne.
Dopasowanie wpisów: (rodzaj, powołanie, kontekst, rola). Wpis, który w nowym raporcie ma inny status weryfikacji
(nieustalony / nieobsługiwany / nie istnieje) → klasa z kroku faktów, ocena sędziego zachowana w `wynik`.
Wpisy nowe (bez odpowiednika) → status `nieocenione_po_przemapowaniu`.

Użycie: python -I przemapuj_poparcie.py --poparcie raporty/_poparcie_X.json --raporty <katalog nowych raportów> --wyjscie raporty/_poparcie_Xb.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import poparcie  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--poparcie", required=True)
    ap.add_argument("--raporty", required=True)
    ap.add_argument("--wyjscie", required=True)
    args = ap.parse_args()
    pop = json.loads(Path(args.poparcie).read_text())
    rap_dir = Path(args.raporty)
    zmiany = {"status_zmieniony": 0, "bez_zmian": 0, "bez_odpowiednika": 0, "nowe_wpisy": 0}
    nowe_rows = []
    klucze = {}
    for (p, s) in {(z["P"], z["system"]) for z in pop["powolania"]}:
        f = rap_dir / f"{p}_{s}.json"
        if not f.exists():
            continue
        r = json.loads(f.read_text())
        klucze.setdefault(p, poparcie.fakty.load_key(p))
        stare = [z for z in pop["powolania"] if (z["P"], z["system"]) == (p, s)]
        idx = {}
        for z in stare:
            k = (z["rodzaj"], z["powolanie"], z.get("kontekst"), z.get("rola"))
            idx.setdefault(k, []).append(z)
        uzyte = set()
        for e in r["przepisy"]:
            k = ("przepis", e["powolanie"], e["kontekst"], e.get("rola", "główne"))
            kand = [z for z in idx.get(k, []) if id(z) not in uzyte]
            if not kand:
                # bez odpowiednika (np. zmiana napisu aktu): wpis nowy ze statusem z kroku faktów
                zmiany["nowe_wpisy"] += 1
                kl, stt, zr = poparcie.klasa_a6("przepis", e, {"etykieta": None})
                nowe_rows.append({"P": p, "system": s, "rodzaj": "przepis", "id": e["id"], "powolanie": e["powolanie"],
                                  "cytowanie": e.get("cytowanie_legal_cite"), "akt_ustalenie": e["akt"]["ustalenie"],
                                  "rola": e.get("rola", "główne"), "powolanie_glowne_id": e.get("powolanie_glowne_id"),
                                  "status_faktow": e["weryfikacja"].get("status"), "flagi_faktow": e.get("flagi", []),
                                  "kontekst": e["kontekst"], "twierdzenie": None, "wzmianka": True,
                                  "wynik": {"etykieta": None, "flagi": ["nieocenione_po_przemapowaniu"]},
                                  "klasa_A6": kl, "status_weryfikacji": stt or "nieocenione_po_przemapowaniu", "klasa_zrodlo": zr,
                                  "uzasadnienie_etykieta": None, "A6_zakres": None, "A6_zakres_powod": "przemapowanie"})
                continue
            z = kand[0]
            uzyte.add(id(z))
            z["id"] = e["id"]
            z["powolanie_glowne_id"] = e.get("powolanie_glowne_id")
            z["akt_ustalenie"] = e["akt"]["ustalenie"]
            z["status_faktow"] = e["weryfikacja"].get("status")
            z["flagi_faktow"] = e.get("flagi", [])
            kl, stt, zr = poparcie.klasa_a6("przepis", e, z.get("wynik") or {"etykieta": None})
            if (kl, stt) != (z.get("klasa_A6"), z.get("status_weryfikacji")):
                z["przemapowanie"] = {"z": [z.get("klasa_A6"), z.get("status_weryfikacji")], "na": [kl, stt]}
                z["klasa_A6"], z["status_weryfikacji"], z["klasa_zrodlo"] = kl, stt, zr
                zmiany["status_zmieniony"] += 1
            else:
                zmiany["bez_zmian"] += 1
            nowe_rows.append(z)
        for i, o in enumerate(r["orzeczenia"]):
            k = ("orzeczenie", o["sygnatura"], o["kontekst"], None)
            kand = [z for z in idx.get(k, []) if id(z) not in uzyte]
            if not kand:
                zmiany["nowe_wpisy"] += 1
                continue
            z = kand[0]
            uzyte.add(id(z))
            z["id"] = f"o{i}"
            z["status_faktow"] = o["weryfikacja"]["status"]
            z["flagi_faktow"] = o.get("flagi", [])
            kl, stt, zr = poparcie.klasa_a6("orzeczenie", o, z.get("wynik") or {"etykieta": None})
            if (kl, stt) != (z.get("klasa_A6"), z.get("status_weryfikacji")):
                z["przemapowanie"] = {"z": [z.get("klasa_A6"), z.get("status_weryfikacji")], "na": [kl, stt]}
                z["klasa_A6"], z["status_weryfikacji"], z["klasa_zrodlo"] = kl, stt, zr
                zmiany["status_zmieniony"] += 1
            else:
                zmiany["bez_zmian"] += 1
            nowe_rows.append(z)
        zmiany["bez_odpowiednika"] += sum(1 for z in stare if id(z) not in uzyte)
    pop["powolania"] = nowe_rows
    pop["meta"]["przemapowanie"] = {"raporty": str(rap_dir), "zmiany": zmiany, "z_pliku": Path(args.poparcie).name}
    pop["meta"]["klasy_A6"] = {k: sum(1 for z in nowe_rows if z.get("klasa_A6") == k) for k in ("✓", "F", "T", "W", "S")}
    pop["meta"]["statusy_weryfikacji"] = {k: sum(1 for z in nowe_rows if z.get("status_weryfikacji") == k)
                                          for k in sorted({z.get("status_weryfikacji") for z in nowe_rows if z.get("status_weryfikacji")})}
    Path(args.wyjscie).write_text(json.dumps(pop, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({"zmiany": zmiany, "klasy": pop["meta"]["klasy_A6"], "statusy": pop["meta"]["statusy_weryfikacji"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
