"""Nowele aktów źródłowych kluczy B02 według wykazu ELI (wydanie danych 1.0.3; propozycja z issue #4).

Dla każdego klucza bierze akty wskazane jako „Dz.U. RRRR poz. N”, odczytuje z API ELI listę „Nowelizacje po tekście
jednolitym” i dla każdej noweli datę ogłoszenia oraz datę wejścia w życie aktu zmieniającego. Wypisuje proponowane pola:
- nowele_sprawdzone_do: dzień odczytu wykazu ELI;
- nowele_po_tj: lista nowel (akt, ogłoszenie, wejście w życie aktu — poszczególne przepisy mogą wchodzić w innych terminach);
- klucz_aktualny_do: dzień przed najwcześniejszym wejściem w życie noweli PO dacie stanu prawnego klucza, a gdy takiej
  nie ma — dzień odczytu. Nowela nie musi dotyczyć jednostek z klucza; pole wskazuje, od kiedy klucz wymaga przejrzenia.

Użycie: python tools/nowele_kluczy.py [--zapisz]   (bez --zapisz tylko wypisuje; z --zapisz dopisuje blok na końcu YAML)
"""
import datetime
import glob
import json
import re
import sys
import time
import urllib.request

import yaml

API = "https://api.sejm.gov.pl/eli/acts/DU"
DZIS = datetime.date.today()
ZAPISZ = "--zapisz" in sys.argv


def pobierz(url):
    for proba in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except Exception:  # noqa: BLE001 — API bywa chwilowo niedostępne
            time.sleep(2 * (proba + 1))
    raise RuntimeError(f"API ELI nie odpowiada: {url}")


for plik in sorted(glob.glob("keys/P*.yaml")):
    tekst = open(plik, encoding="utf-8").read()
    d = yaml.safe_load(tekst)
    stan = datetime.date.fromisoformat(str(d.get("data_stanu_prawnego")))
    znacznik = "\n# --- nowele (tools/nowele_kluczy.py)"
    tresc_klucza = tekst.split(znacznik)[0]  # bez bloku z poprzedniego uruchomienia (inaczej nowele trafiłyby do aktów źródłowych)
    akty = sorted(set(re.findall(r"Dz\.U\. (\d{4}) poz\. (\d+)", tresc_klucza)))
    nowele = []
    for rok, poz in akty:
        ref = pobierz(f"{API}/{rok}/{poz}/references")
        tj = pobierz(f"{API}/{rok}/{poz}")
        kandydaci = {n["act"]["ELI"]: n["act"] for n in ref.get("Nowelizacje po tekście jednolitym", [])}
        # wykaz przy t.j. bywa niepełny (np. starsze t.j.): dokładamy akty zmieniające akt bazowy ogłoszone po t.j.
        for baza in ref.get("Tekst jednolity dla aktu", []):
            b_ = baza["act"]
            for n in pobierz(f"{API}/{b_['year']}/{b_['pos']}/references").get("Akty zmieniające", []):
                a = n["act"]
                if a.get("promulgation") and tj.get("promulgation") and a["promulgation"] > tj["promulgation"]:
                    kandydaci.setdefault(a["ELI"], a)
        for a in kandydaci.values():
            meta = pobierz(f"{API}/{a['year']}/{a['pos']}")
            nowele.append({"akt_zrodlowy": f"Dz.U. {rok} poz. {poz}", "nowela": a["displayAddress"], "tytul": a["title"],
                           "ogloszono": a.get("promulgation"), "wejscie_w_zycie_aktu": meta.get("entryIntoForce")})
    nowele.sort(key=lambda n: (n["akt_zrodlowy"], n["ogloszono"] or ""))
    po_stanie = [datetime.date.fromisoformat(n["wejscie_w_zycie_aktu"]) for n in nowele
                 if n["wejscie_w_zycie_aktu"] and datetime.date.fromisoformat(n["wejscie_w_zycie_aktu"]) > stan]
    aktualny_do = (min(po_stanie) - datetime.timedelta(days=1)) if po_stanie else DZIS
    blok = {"nowele_sprawdzone_do": DZIS.isoformat(), "klucz_aktualny_do": aktualny_do.isoformat(),
            "nowele_po_tj": nowele or [], "nowele_zrodlo": "API ELI: „Nowelizacje po tekście jednolitym” oraz akty zmieniające akt bazowy ogłoszone po t.j. (tools/nowele_kluczy.py); data wejścia w życie dotyczy aktu zmieniającego, poszczególne przepisy mogą wchodzić w innych terminach"}
    if not akty:
        blok = {"nowele_sprawdzone_do": None, "klucz_aktualny_do": None, "nowele_po_tj": [],
                "nowele_zrodlo": "akty spoza Dziennika Ustaw (EUR-Lex); wykazu ELI nie stosuje się"}
    print(f"== {plik}: akty {len(akty)}, nowel {len(nowele)}, klucz_aktualny_do {blok['klucz_aktualny_do']}")
    for n in nowele:
        print(f"   {n['akt_zrodlowy']} ← {n['nowela']} (ogł. {n['ogloszono']}, w życie aktu {n['wejscie_w_zycie_aktu']})")
    if ZAPISZ:
        if "nowele_sprawdzone_do:" in tekst:
            tekst = tekst[:tekst.index("\n# --- nowele (tools/nowele_kluczy.py)")]
        dopisek = "\n# --- nowele (tools/nowele_kluczy.py) ---\n" + yaml.safe_dump(blok, allow_unicode=True, sort_keys=False, width=120)
        open(plik, "w", encoding="utf-8").write(tekst.rstrip("\n") + "\n" + dopisek)
