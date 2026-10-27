#!/usr/bin/env python3
"""Krok 3 meta-sędziego: „karta meta” (plan zatwierdzony przez Adama Piotrowskiego 2026-10-24, ETAP C).

Dla każdej karty (P, system) buduje prompt sędziego IDENTYCZNY z eval_sedzia_gemini.py / eval_sedzia_codex.py
(ta sama stała INSTR wycinana z eval_sedzia_codex.py, te same wycinki README, klucz, odpowiedź, format JSON karty)
i dokłada sekcję „RAPORT FAKTÓW (sprawdzone kodem i weryfikatorem poparcia)”: powołania z klasą A6, brzmieniem na
datę stanu prawnego, wersjami wcześniejszymi, statusem orzeczenia (data/sąd/tezy z kotwicą) i statusami weryfikacji.
Instrukcja v2 (24.10): klasy F/T/W/S z raportu wiążące, ✓ NIE zamyka sprawy — sędzia sam porównuje treść z brzmieniem; „niedostępne” ≠ błąd.

Sędziowie: argon4meta = gemini-4-argon (Vertex, projekt ktzr-asystent, --myslenie high, wyszukiwanie Google jak w
eval_sedzia_gemini.py); sol61meta = gpt-6.1-sol przez Codex CLI (jak eval_sedzia_codex.py).
Wynik: pytania/oceny/_sedziowie/<P>_<system>.<sedzia>.json (format jak inni sędziowie + pole `raport_faktow_uzyty`).
Istniejących plików sędziów NIE nadpisuje.

Użycie:
  python3 -I karta_meta.py argon4meta --tylko P05,P06 [--systemy a,b] --poparcie raporty/_poparcie_<etykieta>.json
      [--rownolegle 3] [--budzet 6.0] [--limit 64] [--szacunek]
  python3 -I karta_meta.py sol61meta --tylko P05 --poparcie ... [--rownolegle 2]
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fakty  # noqa: E402
from poparcie import readme_regula  # noqa: E402  (reguła README wycinana programowo, nie przepisywana)

REPO = os.path.expanduser("./pytania")
NARZEDZIA = os.path.expanduser("~/ktzr-narzedzia")
RAPORTY = HERE / "raporty"
SEDZIOWIE = {"argon4meta": {"model": "gemini-4-argon", "droga": "vertex", "myslenie": "high"},
             # v2 instrukcji (24.10): raport może dodać błąd, nie może go odjąć — osobne id, żeby nie nadpisać wyników v1
             "argon4meta2": {"model": "gemini-4-argon", "droga": "vertex", "myslenie": "high"},
             "sol61meta2": {"model": "gpt-6.1-sol", "droga": "codex"},
             # v3 prezentacji raportu (25.10): brak „✓”, gdy brzmienia na datę stanu prawnego nie ustalono
             "argon4meta3": {"model": "gemini-4-argon", "droga": "vertex", "myslenie": "high"},
             "sol61meta3": {"model": "gpt-6.1-sol", "droga": "codex"},
             "sol61meta": {"model": "gpt-6.1-sol", "droga": "codex"}}
CENY = {"gemini-4-argon": {"we": 2.00, "wy": 10.00}}      # USD / 1 mln tokenów (cennik 2026-10-18; rozumowanie jak wyjście)

LIMIT_BRZMIENIE = 600
LIMIT_KOTWICA = 260

# ───────────────────────── prompt bazowy (identyczny z eval_sedzia_*) ─────────────────────────

readme = open(f"{REPO}/README.md").read()
reguly = (readme[readme.index("## Blok A — obiektywny"):readme.index("## Warunki biegu (prompt)")]
          + "\n" + readme[readme.index("## Przykłady graniczne"):readme.index("## Status zbioru")])
WERSJA = readme.split("Wersja specyfikacji oceny: ")[1].split(" ")[0] if "Wersja specyfikacji oceny: " in readme else "?"
# decyzja Adama nr 2 (2026-10-24): reguła o kręgu adresatów / zakresie normy — dosłownie z README, także w instrukcji karty meta
REGULA_KRAG = readme_regula(readme)
if REGULA_KRAG not in reguly:
    raise SystemExit("README: reguła o kręgu adresatów nie mieści się w wycinku README dla sędziego — rozszerz `reguly`")
_src = open(os.path.join(NARZEDZIA, "eval_sedzia_codex.py")).read()
INSTR = _src[_src.index('INSTR = """') + len('INSTR = """'):_src.index('"""\n\n\ndef tresc_odpowiedzi')]

SEKCJA_RAPORTU = """

=== RAPORT FAKTÓW (sprawdzone kodem i weryfikatorem poparcia) ===
Poniższy raport powstał poza Tobą: krok faktów (kod: legal-cite / ELI dla przepisów, SAOS i baza orzeczeń dla
orzeczeń) sprawdził istnienie i brzmienie każdego powołania na datę stanu prawnego z klucza, a weryfikator poparcia
(model widzący wyłącznie twierdzenie odpowiedzi i tekst źródła, z cytatami sprawdzonymi kodem) ocenił, czy źródło
mówi to, co odpowiedź mu przypisuje. Klasy A6 w raporcie: ✓ zgodne; F — źródło/jednostka nie istnieje; T — źródło
istnieje, ale nie zawiera przypisanej treści; W — brzmienie z innej daty podane jako obowiązujące; S — błędne
oznaczenie (data/sąd/sygnatura) przy trafnej treści.

INSTRUKCJA (wersja 2, decyzja Adama 2026-10-24 — raport może dodać błąd, nie może go odjąć):
1. Klasy F / T / W / S z raportu PRZYJMUJESZ: A6 = 0 z tą klasą w A6_typ. Odstąpić od nich możesz tylko z cytatem ze
   źródła oficjalnego w polu "powolania" (pole "zrodlo") i jednym zdaniem w "uzasadnienie".
2. Klasa ✓ w raporcie potwierdza WYŁĄCZNIE, że źródło istnieje, ma podane brzmienie na datę stanu prawnego i że cytat
   odpowiedzi jest dosłowny. NIE potwierdza, że odpowiedź trafnie oddaje treść normy. Sam porównaj to, co odpowiedź
   przypisuje źródłu, z brzmieniem z raportu: adresat, zakres, skutek, termin, forma. Gdy odpowiedź przypisuje źródłu
   treść, której w brzmieniu nie ma, albo zawęża lub rozszerza jego zakres — daj A6 = 0 (T; przy brzmieniu z innej daty
   W) i przytocz brzmienie z raportu jako cytat w "powolania". Bez takiego porównania „✓” nie zamyka sprawy.
   Krąg adresatów i zakres normy oceniaj według reguły README (dosłownie; raport podaje też „wersje wcześniejsze
   o innym brzmieniu” z datami — porównaj z nimi wyliczony w odpowiedzi krąg lub zakres):
{regula_krag}
3. A3 (dosłowność cytatów) oprzyj na porównaniach z raportu.
4. Pozostałe kryteria (A-R, A2, A5, A8, R, K, B1, B2) oceń jak zwykle, według reguł i klucza.
5. Gdy raport podaje status weryfikacji zamiast klasy („akt nieustalony”, „sygnatura niejednoznaczna”, „tekst
   niedostępny”, „SAOS niedostępny”, „brak dowodu”, „nie znaleziono”, „nieobsługiwany”), NIE WOLNO z tego wnioskować
   błędu odpowiedzi — wpisz takie powołanie w polu "niesprawdzone" (chyba że sam sprawdzisz je w źródle oficjalnym
   i podasz cytat).

{raport}
=== KONIEC RAPORTU FAKTÓW ===
"""


def tresc_odpowiedzi(pid: str, system: str) -> str:
    s = open(f"{REPO}/odpowiedzi/{pid}/{system}.md").read()
    return s.split("---", 2)[2].strip() if s.startswith("---") else s


def trim(s, n):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


# ───────────────────────── raport faktów → tekst ─────────────────────────

# v3 (decyzja Adama 2026-10-25): „✓” tylko przy brzmieniu na datę POTWIERDZONYM; przy „nieustalone” zamiast klasy
# status do samodzielnej oceny aktualności. Ustawiane w main() dla sędziów *meta3.
PREZENTACJA_V3 = False


def raport_faktow_tekst(pid: str, system: str, rap: dict, pop_rows: list[dict], atomy_orz: dict) -> str:
    L = [f"Data stanu prawnego (klucz): {rap['meta']['data_stanu_prawnego']}. Powołania: przepisy {len(rap['przepisy'])}, "
         f"orzeczenia {len(rap['orzeczenia'])}. Źródła: {rap['meta']['zrodla']['przepisy']}; orzeczenia: {rap['meta']['zrodla']['orzeczenia']}."]
    by_id = {(z["rodzaj"], str(z["id"])): z for z in pop_rows}
    L.append("\nPRZEPISY:")
    for e in rap["przepisy"]:
        z = by_id.get(("przepis", str(e["id"])), {})
        w = e.get("weryfikacja", {})
        kl = z.get("klasa_A6")
        stt = z.get("status_weryfikacji")
        rola = e.get("rola", "główne")
        czesci = [f"{e['id']}. {e['powolanie']} [akt: {e['akt']['ustalenie']}]"]
        if rola != "główne":
            czesci.append(f"powołanie {rola} — ocena łącznie z powołaniem nr {e.get('powolanie_glowne_id')}; istnienie: {w.get('status')}")
        elif kl and PREZENTACJA_V3 and kl == "✓" and w.get("status") == "istnieje" and not str(
                (w.get("brzmienie_na_dzien") or {}).get("ustalenie") or "").startswith("potwierdzone"):
            bnd = w.get("brzmienie_na_dzien") or {}
            czesci.append(f"STATUS: BRZMIENIE NA {rap['meta']['data_stanu_prawnego']} NIEUSTALONE — jednostka istnieje, a treść "
                          f"przypisana przez odpowiedź zgadza się z brzmieniem na dziś; aktualności na datę stanu prawnego NIE "
                          f"sprawdzono. To nie jest ani potwierdzenie (✓), ani błąd. Oceń sam, czy opisany w odpowiedzi stan prawa "
                          f"obowiązywał w dniu {rap['meta']['data_stanu_prawnego']}"
                          + (f" (źródło brzmienia: {trim(bnd.get('zrodlo') or '', 260)})" if bnd.get("zrodlo") else ""))
        elif kl:
            czesci.append(f"KLASA A6: {kl} (etykieta weryfikatora: {z.get('uzasadnienie_etykieta')}; rozstrzygnięcie: {z.get('klasa_zrodlo')})")
            czesci.append(f"A6_zakres: {z.get('A6_zakres')} ({z.get('A6_zakres_powod')})")
        else:
            czesci.append(f"STATUS WERYFIKACJI (nie jest błędem): {stt or w.get('status')}" + (f" — {w.get('powod')}" if w.get("powod") else ""))
        if w.get("status") == "istnieje":
            bnd = w.get("brzmienie_na_dzien") or {}
            czesci.append(f"istnieje; brzmienie na datę stanu prawnego: {bnd.get('ustalenie') or 'na dziś (na_dzien nie ustalono)'}"
                          + (f"; {w.get('znacznik')}" if w.get("znacznik") else ""))
            if w.get("uchylony_na_dzien"):
                czesci.append("UWAGA: jednostka uchylona na datę stanu prawnego")
        elif w.get("status"):
            czesci.append(f"istnienie: {w['status']}")
        wn = e.get("wersje_na_dzien") or []
        inne = [x["na_dzien"] for x in wn if x.get("status") == "inne brzmienie"]
        if inne:
            czesci.append(f"wersje wcześniejsze o innym brzmieniu: na dzień {', '.join(inne)}")
            # decyzja nr 2 (2026-10-24): najnowsze wcześniejsze brzmienie w skrócie — do porównania kręgu/zakresu
            x0 = next(x for x in wn if x.get("status") == "inne brzmienie")
            if x0.get("fragment") and rola == "główne":
                czesci.append(f"brzmienie wcześniejsze (na dzień {x0['na_dzien']}, fragment): „{trim(x0['fragment'], LIMIT_BRZMIENIE)}”")
        cp = e.get("cytat_porownanie") or {}
        if e.get("cytat"):
            czesci.append(f"cytat w odpowiedzi: {cp.get('wynik')}" + (f" (pokrycie dwuwyrazów {cp.get('pokrycie_dwuwyrazow')})" if cp.get("pokrycie_dwuwyrazow") is not None else ""))
        fl = [f for f in e.get("flagi", []) if f not in ("brzmienie_na_dzien_nieustalone",)]
        if fl:
            czesci.append(f"flagi kroku faktów: {', '.join(fl)}")
        if z.get("twierdzenie"):
            czesci.append(f"twierdzenie odpowiedzi (wg weryfikatora): „{trim(z['twierdzenie'], 240)}”")
        wy = z.get("wynik") or {}
        if wy.get("uzasadnienie"):
            czesci.append(f"uzasadnienie weryfikatora: {trim(wy['uzasadnienie'], 300)}")
        if wy.get("cytat") and wy.get("cytat_zweryfikowany"):
            czesci.append(f"kotwica (verbatim ze źródła): „{trim(wy['cytat'], LIMIT_KOTWICA)}”")
        if w.get("fragment_urzedowy") and rola == "główne":
            czesci.append(f"brzmienie jednostki (fragment): „{trim(w['fragment_urzedowy'], LIMIT_BRZMIENIE)}”")
        L.append("- " + "\n    · ".join(czesci))
    L.append("\nORZECZENIA:" if rap["orzeczenia"] else "\nORZECZENIA: brak sygnatur w odpowiedzi.")
    for i, o in enumerate(rap["orzeczenia"]):
        z = by_id.get(("orzeczenie", f"o{i}"), {})
        w = o.get("weryfikacja", {})
        czesci = [f"{o['sygnatura']} — podane w odpowiedzi: sąd {o.get('sad_podany') or '—'} ({o.get('sad_zrodlo') or '—'}), data {o.get('data_podana') or '—'}"]
        czesci.append(f"wynik wyszukania: {w.get('status')}" + (f"; w źródle: {w.get('sad_wyroku')}, {w.get('data_wyroku')}" if w.get("sad_wyroku") else ""))
        if z.get("klasa_A6"):
            czesci.append(f"KLASA A6: {z['klasa_A6']} (etykieta weryfikatora: {z.get('uzasadnienie_etykieta')}; rozstrzygnięcie: {z.get('klasa_zrodlo')}); A6_zakres: {z.get('A6_zakres')}")
            kt = (z.get("wynik") or {}).get("kandydat_trafiony")
            if kt:   # decyzja nr 4: właściwy wyrok spośród kandydatów pod tą sygnaturą
                czesci.append(f"właściwy wyrok pod tą sygnaturą (wg weryfikatora): {kt.get('sad')}, {str(kt.get('data') or '')[:10]} ({kt.get('zrodlo')})")
        else:
            czesci.append(f"STATUS WERYFIKACJI (nie jest błędem): {z.get('status_weryfikacji') or w.get('status')}")
        if o.get("flagi"):
            czesci.append(f"flagi: {', '.join(o['flagi'])}")
        if z.get("twierdzenie"):
            czesci.append(f"twierdzenie odpowiedzi (wg weryfikatora): „{trim(z['twierdzenie'], 240)}”")
        wy = z.get("wynik") or {}
        if wy.get("uzasadnienie"):
            czesci.append(f"uzasadnienie weryfikatora: {trim(wy['uzasadnienie'], 300)}")
        at = atomy_orz.get(o["sygnatura"])
        if at:
            tezy = [a for a in at.get("atomy", []) if a.get("status_cytatu") == "verbatim"][:4]
            for a in tezy:
                czesci.append(f"teza {a['nr']} ({a.get('tryb')}): {trim(a.get('teza'), 200)} — kotwica: „{trim(a.get('cytat'), LIMIT_KOTWICA)}”")
        L.append("- " + "\n    · ".join(czesci))
    if rap.get("publikatory"):
        L.append("\nPUBLIKATORY: " + "; ".join(f"{p['napis']} — {p.get('ocena', '')}" for p in rap["publikatory"]))
    return "\n".join(L)


# ───────────────────────── sędziowie ─────────────────────────

class Vertex:
    def __init__(self, model: str, myslenie: str):
        from google import genai
        from google.genai import types
        self.types = types
        self.model, self.myslenie = model, myslenie
        self.klient = genai.Client(vertexai=True, project="ktzr-asystent", location="global",
                                   http_options=types.HttpOptions(timeout=1_200_000))
        self.cfg = types.GenerateContentConfig(temperature=0.0, tools=[types.Tool(google_search=types.GoogleSearch())],
                                               thinking_config=types.ThinkingConfig(thinking_level=myslenie))
        self.lock = threading.Lock()
        self.tok = {"we": 0, "wy": 0, "rozum": 0, "wywolania": 0}

    def koszt(self) -> float:
        c = CENY.get(self.model, {"we": 0, "wy": 0})
        return round(self.tok["we"] / 1e6 * c["we"] + (self.tok["wy"] + self.tok["rozum"]) / 1e6 * c["wy"], 3)

    def ocen(self, prompt: str) -> tuple[str, dict]:
        r = self.klient.models.generate_content(model=self.model, contents=prompt, config=self.cfg)
        odp = r.text or ""
        gm = r.candidates[0].grounding_metadata if r.candidates else None
        zap = list(getattr(gm, "web_search_queries", None) or [])
        zr = [getattr(getattr(c, "web", None), "uri", None) or getattr(getattr(c, "web", None), "title", None)
              for c in (getattr(gm, "grounding_chunks", None) or [])]
        um = r.usage_metadata
        tok = {"wejscie": um.prompt_token_count or 0, "wyjscie": um.candidates_token_count or 0,
               "rozumowanie": getattr(um, "thoughts_token_count", 0) or 0}
        with self.lock:
            self.tok["we"] += tok["wejscie"]
            self.tok["wy"] += tok["wyjscie"]
            self.tok["rozum"] += tok["rozumowanie"]
            self.tok["wywolania"] += 1
        return odp, {"wyszukan": len(zap), "zapytania": zap[:20], "zrodla_sedziego": [z for z in zr if z][:25], "tokeny": tok}


def codex_ocen(model: str, prompt: str) -> tuple[str, dict, str | None]:
    """Codex CLI jak w eval_sedzia_codex.py. Zwraca (odpowiedź, meta, powód_błędu)."""
    with tempfile.TemporaryDirectory() as kat:
        wynik = os.path.join(kat, "_odp.md")
        cmd = ["codex", "exec", "--ephemeral", "--skip-git-repo-check", "-s", "read-only", "-C", kat, "--json", "-o", wynik,
               "-c", 'web_search="live"', "-c", "features.apps=false", "-m", model, "-c", 'model_reasoning_effort="medium"', "-"]
        try:
            p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=1800)
            odp = open(wynik).read() if os.path.exists(wynik) else ""
        except Exception as e:
            return "", {}, type(e).__name__
    if not odp.strip():
        wyj = p.stderr + p.stdout
        return "", {}, "limit konta" if ("usage limit" in wyj or "429" in wyj or "Too Many Requests" in wyj) else "pusta odpowiedź"
    # 2026-10-25: zapis treści wywołań wyszukiwania (zapytania, źródła), nie tylko liczby
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from codex_log_wyszukan import wyszukania
    return odp, wyszukania(p.stdout), None


# ───────────────────────── bieg ─────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sedzia", choices=list(SEDZIOWIE))
    ap.add_argument("--tylko", required=True, help="pytania po przecinku")
    ap.add_argument("--systemy", default=",".join(fakty.SYSTEMY_R3))
    ap.add_argument("--poparcie", required=True, help="JSON weryfikatora poparcia (_poparcie_<etykieta>.json)")
    ap.add_argument("--rownolegle", type=int, default=3)
    ap.add_argument("--budzet", type=float, default=None, help="USD; po przekroczeniu nowe karty nie startują (tylko Vertex)")
    ap.add_argument("--limit", type=int, default=None, help="najwyżej tyle kart w tym biegu")
    ap.add_argument("--szacunek", action="store_true", help="tylko policz prompty i tokeny (count_tokens), bez oceny")
    args = ap.parse_args()
    spec = SEDZIOWIE[args.sedzia]
    global PREZENTACJA_V3
    PREZENTACJA_V3 = args.sedzia.endswith("meta3")
    pytania = args.tylko.split(",")
    systemy = args.systemy.split(",")
    pop = json.loads(Path(args.poparcie).read_text())
    pop_by: dict[tuple, list] = {}
    for z in pop["powolania"]:
        pop_by.setdefault((z["P"], z["system"]), []).append(z)
    atomy_orz = {j["sygnatura"]: j for j in pop.get("atomy_orzeczen", [])}

    zad = []
    for p in pytania:
        for s in systemy:
            cel = f"{REPO}/oceny/_sedziowie/{p}_{s}.{args.sedzia}.json"
            if not os.path.exists(f"{REPO}/odpowiedzi/{p}/{s}.md") or not (RAPORTY / f"{p}_{s}.json").exists():
                continue
            if os.path.exists(cel):
                continue          # nie nadpisujemy
            zad.append((p, s, cel))
    if args.limit:
        zad = zad[:args.limit]
    print(f"kart do oceny ({args.sedzia}): {len(zad)}", flush=True)

    def prompt_dla(p, s):
        rap = json.loads((RAPORTY / f"{p}_{s}.json").read_text())
        klucz = open(glob.glob(f"{REPO}/klucze/{p}_*.yaml")[0]).read()
        raport = raport_faktow_tekst(p, s, rap, pop_by.get((p, s), []), atomy_orz)
        return INSTR % (reguly, klucz, tresc_odpowiedzi(p, s)) + SEKCJA_RAPORTU.format(raport=raport, regula_krag=REGULA_KRAG), raport

    vx = Vertex(spec["model"], spec.get("myslenie", "high")) if spec["droga"] == "vertex" else None
    if args.szacunek:
        tot = 0
        for p, s, _ in zad:
            pr, _ = prompt_dla(p, s)
            if vx:
                n = vx.klient.models.count_tokens(model=spec["model"], contents=pr).total_tokens
            else:
                n = len(pr) // 3
            tot += n
        print(f"prompty: {len(zad)}, tokeny wejścia razem ≈ {tot} (śr. {tot // max(1, len(zad))}); "
              f"szacunek Argon high: wejście {tot / 1e6 * 2:.2f} USD + wyjście/rozumowanie ~{len(zad) * 12_000 / 1e6 * 10:.2f} USD "
              f"(przy ~12 tys. tokenów wy+rozum na kartę) = {tot / 1e6 * 2 + len(zad) * 12_000 / 1e6 * 10:.2f} USD")
        return

    stop = threading.Event()
    stan = {"limit_konta": False}

    def jeden(z):
        p, s, cel = z
        if stop.is_set():
            return p, s, "pominięte (stop: budżet/limit konta)", 0
        if vx and args.budzet is not None and vx.koszt() >= args.budzet:
            stop.set()
            return p, s, f"pominięte (budżet {args.budzet} USD osiągnięty: {vx.koszt()})", 0
        prompt, raport = prompt_dla(p, s)
        t0 = time.time()
        meta_dod: dict = {}
        try:
            if vx:
                odp, meta_dod = vx.ocen(prompt)
            else:
                odp, meta_dod, powod = codex_ocen(spec["model"], prompt)
                if powod:
                    if powod == "limit konta":
                        stan["limit_konta"] = True
                        stop.set()
                    return p, s, f"BŁĄD {powod} (nie zapisano)", round(time.time() - t0)
        except Exception as e:
            return p, s, f"BŁĄD {type(e).__name__}: {str(e)[:80]} (nie zapisano)", round(time.time() - t0)
        if not odp.strip():
            return p, s, "BŁĄD pusta odpowiedź (nie zapisano)", round(time.time() - t0)
        m = re.search(r"\{.*\}", odp, re.S)
        try:
            d = json.loads(m.group(0))
        except Exception:
            d = {"blad_parsowania": True, "surowe": odp[:4000]}
        d["_meta"] = {"sedzia": args.sedzia, "model": spec["model"], "pytanie": p, "system": s, **meta_dod,
                      "czas_s": round(time.time() - t0), "data": time.strftime("%Y-%m-%d"), "slepa": True,
                      "specyfikacja": WERSJA, "temperatura": 0.0, "z_raportem_faktow": True,
                      "poparcie_plik": os.path.basename(args.poparcie),
                      **({"region": "global", "poziom_rozumowania": spec.get("myslenie"), "readme": "bieżące"} if vx else {})}
        d["raport_faktow_uzyty"] = raport
        os.makedirs(os.path.dirname(cel), exist_ok=True)
        if os.path.exists(cel):
            return p, s, "pominięte (plik powstał w międzyczasie)", d["_meta"]["czas_s"]
        json.dump(d, open(cel, "w"), ensure_ascii=False, indent=1)
        return p, s, "BŁĄD parsowania" if d.get("blad_parsowania") else "ok", d["_meta"]["czas_s"]

    t_start = time.time()
    ok = 0
    with cf.ThreadPoolExecutor(args.rownolegle) as ex:
        for p, s, st, czas in ex.map(jeden, zad):
            ok += st == "ok"
            dod = f"  koszt dotąd {vx.koszt()} USD" if vx else ""
            print(f"{p} {s:32} {czas:5}s  {st}{dod}", flush=True)
    print(f"gotowe: {ok}/{len(zad)} ok, {round(time.time() - t_start)} s" + (f", tokeny {vx.tok}, koszt {vx.koszt()} USD" if vx else "")
          + (" — LIMIT KONTA Codex: bieg przerwany, postęp zapisany w plikach" if stan["limit_konta"] else ""), flush=True)


if __name__ == "__main__":
    main()
