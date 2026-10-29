# -*- coding: utf-8 -*-
"""Warstwa maszynowa repozytorium: data/*.jsonl z kluczy (YAML), odpowiedzi i kart (Markdown), ocen sędziów i raportów warstwy (JSON).

Format po przeglądzie LegalBench, SWE-bench, LiveBench, BIG-bench, LawBench i LEXam (28.10.2026): jeden obiekt = jedna pozycja,
nazwy pól po angielsku, treść po polsku, pytania osobno od odpowiedzi, odpowiedzi osobno od ocen, kanaryjski ciąg w każdym rekordzie.
Markdown w cards/ i answers/ pozostaje źródłem czytelnym dla człowieka; ten skrypt go tylko odczytuje.
Kontrola: liczby (A %, B %, halucynacje, poprawnie ugruntowane) muszą zgadzać się z reports/benchmark-02/src/dane.py.
Użycie (z katalogu repo): python3 -I tools/export_jsonl.py
"""
import glob
import importlib.util
import json
import os
import re
import sys

import yaml

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(REPO, "reports", "benchmark-02", "src")
OUT = os.path.join(REPO, "data")
CANARY = open(os.path.join(REPO, "CANARY.txt"), encoding="utf-8").read().strip()
CARD_VERSION = "2026-10-25"

os.chdir(SRC); sys.path.insert(0, SRC)
spec = importlib.util.spec_from_file_location("dane", os.path.join(SRC, "dane.py"))
dane = importlib.util.module_from_spec(spec); spec.loader.exec_module(dane)
os.chdir(REPO)
SYS = {s: {"system": s, "model": n, "provider": prov, "condition": w} for s, n, prov, w in dane.SYSTEMY}
os.makedirs(OUT, exist_ok=True)


def _typ(v):
    return ("null" if v is None else "bool" if isinstance(v, bool) else "num" if isinstance(v, (int, float)) else
            "str" if isinstance(v, str) else "list" if isinstance(v, list) else "obj")


def _sciezki(v, p, out):
    out.setdefault(p, set()).add(_typ(v))
    if isinstance(v, dict):
        for k, x in v.items():
            _sciezki(x, f"{p}.{k}", out)
    elif isinstance(v, list):
        for x in v:
            _sciezki(x, p + "[]", out)


def pola_mieszane(rekordy):
    """Pola głównego poziomu, w których ta sama ścieżka ma w różnych rekordach różne typy (np. tekst albo obiekt).
    Pyarrow (Hugging Face datasets) nie wczyta takiej kolumny; od 29.10.2026 zapisujemy je jako tekst JSON (bez utraty treści)."""
    out = {}
    for r in rekordy:
        for k, v in r.items():
            _sciezki(v, k, out)
    return sorted({p.split(".")[0].split("[")[0] for p, t in out.items() if len(t - {"null"}) > 1})


POLA_JSON = {}  # plik → pola zapisane jako tekst JSON (opis w data/README.md)


def zapisz(nazwa, rekordy):
    mieszane = pola_mieszane(rekordy)
    POLA_JSON[nazwa] = mieszane
    with open(os.path.join(OUT, nazwa), "w", encoding="utf-8") as f:
        for r in rekordy:
            for k in mieszane:
                if r.get(k) is not None:
                    r[k] = json.dumps(r[k], ensure_ascii=False)
            r["canary"] = CANARY
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{nazwa}: {len(rekordy)} rekordów" + (f"; pola jako tekst JSON: {', '.join(mieszane)}" if mieszane else ""))


# ---------- questions.jsonl + keys.jsonl ----------
pytania, klucze = [], []
for f in sorted(glob.glob("keys/P*.yaml")):
    d = yaml.safe_load(open(f, encoding="utf-8"))
    pytania.append({"id": d["id"], "catalog_no": d.get("katalog_nr"), "text_original": d.get("tekst_oryginalny"),
                    "text_benchmark": d.get("tekst_benchmarkowy"), "type": d.get("typ"), "domain": d.get("domena"),
                    "trap": bool(d.get("pulapka")), "trap_description": d.get("pulapka_opis"), "mirror_of": d.get("lustro"),
                    "disputed": bool(d.get("sporne")), "expected_calibration": d.get("kalibracja_oczekiwana"),
                    "calibration_condition": d.get("warunek"), "legal_state_date": str(d.get("data_stanu_prawnego")),
                    "key_version": d.get("wersja_klucza"), "key_date": str(d.get("data_klucza")), "key_status": d.get("status"),
                    "language": "pl", "key_file": f})
    klucze.append({"id": d["id"], "key_version": d.get("wersja_klucza"), "key_date": str(d.get("data_klucza")),
                   "core": d.get("rdzen"), "result": d.get("wynik"), "tolerance": d.get("tolerancja"),
                   "accepted_variants": d.get("akceptowane_warianty"), "required_bases": d.get("podstawy_wymagane"),
                   "admissible_bases": d.get("podstawy_dopuszczalne"), "citation_patterns": d.get("wzorce_cytatow"),
                   "rubric": d.get("rubryka"), "penalties": d.get("kary"), "key_sources": d.get("zrodla_klucza"),
                   "verification": d.get("weryfikacja"), "scoring_rules_2026_10_18": d.get("reguly_oceny_20261018")})
zapisz("questions.jsonl", pytania); zapisz("keys.jsonl", klucze)

# ---------- answers.jsonl ----------
odpowiedzi = []
for p in dane.PYT:
    for s in SYS:
        t = open(f"answers/{p}/{s}.md", encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
        fm = yaml.safe_load(m.group(1)); body = m.group(2)
        odp = re.search(r"## Odpowiedź\n+(.*)", body, re.S)
        koszt = dane.KOSZT.get((p, s))
        odpowiedzi.append({"id": f"{p}_{s}", "question_id": p, **SYS[s], "model_id": fm.get("model"),
                           "reasoning_effort": fm.get("wysilek_rozumowania"), "run_date": str(fm.get("data_odpowiedzi")),
                           "duration_s": fm.get("czas_s"), "tokens": fm.get("tokeny"), "searches": fm.get("liczba_wyszukan"),
                           "other_tools": fm.get("inne_narzedzia"), "tool_events": fm.get("zdarzenia"), "error": fm.get("blad"),
                           "system_prompt": fm.get("wstep"), "cost_usd": koszt[0] if koszt else None,
                           "cost_is_lower_bound": koszt[1] if koszt else None, "text": odp.group(1).strip() if odp else body.strip(),
                           "answer_file": f"answers/{p}/{s}.md"})
zapisz("answers.jsonl", odpowiedzi)

# ---------- cards.jsonl ----------
RE_WIERSZ = re.compile(r"^\| ([A-Z][\w\- ]*?) \| ([^|]*) \| (.*?)\s*\|\s*$", re.M)
karty = []
for p in dane.PYT:
    for s in SYS:
        k = dane.K[(p, s)]
        t = open(f"cards/{p}_{s}.md", encoding="utf-8").read()
        kryteria = {}
        for nazwa, pkt, dowod in RE_WIERSZ.findall(t):
            if nazwa.startswith("**"):
                continue
            pkt = pkt.strip(); mm = re.match(r"([\d½.]+)\s*/\s*(\d+)", pkt)
            kryteria[nazwa.strip()] = {"score": float(mm.group(1).replace("½", "0.5")) if mm else None,
                                       "max": int(mm.group(2)) if mm else None, "raw": pkt, "evidence": dowod.strip()}
        naglowek = re.search(r"^# (.*)$", t, re.M)
        ocen = re.search(r"- Oceniający: (.*)", t)
        karty.append({"answer_id": f"{p}_{s}", "question_id": p, **SYS[s], "card_title": naglowek.group(1) if naglowek else None,
                      "A_pct": k["A"], "B_pct": k["B"], "hallucinated": k["hal"], "A6": k["a6"], "A6_classes": k["typ"],
                      "A6_scope": k["zakres"], "A6_origin": k["poch"], "correctly_grounded": bool(k["pu"]),
                      "core_score": k["ar"], "penalties_applied": k["kary"], "provider_block": k["blokada"],
                      "source_verification_label": k["zrodlo"], "citations_checked": k["spr"][0], "citations_total": k["spr"][1],
                      "criteria": kryteria, "reviewer": ocen.group(1).strip() if ocen else None,
                      "card_version": CARD_VERSION, "card_file": f"cards/{p}_{s}.md"})
zapisz("cards.jsonl", karty)

# ---------- judgments.jsonl ----------
sedzia_model = {"argon4v101": "Gemini 4 Argon", "gemini31v101": "Gemini 3.1 Pro", "gemini38flashv101": "Gemini 3.8 Flash",
                "sol61v101": "GPT-6.1 Sol", "astra6v101": "GPT-6 Astra", "argon4meta": "Gemini 4 Argon", "argon4meta2": "Gemini 4 Argon",
                "argon4meta3": "Gemini 4 Argon", "sol61meta": "GPT-6.1 Sol", "sol61meta2": "GPT-6.1 Sol", "sol61meta3": "GPT-6.1 Sol"}
wariant = {"meta": "v1 (binding report)", "meta2": "v2 (auxiliary report)", "meta3": "v3 (status instead of ✓)"}
oceny = []
for f in sorted(glob.glob("judges/P*.json")):
    m = re.match(r"judges/(P\d\d)_(.+?)\.(\w+)\.json$", f)
    d = json.load(open(f, encoding="utf-8")); j = m.group(3)
    mw = re.search(r"(meta\d?)$", j)
    oceny.append({"answer_id": f"{m.group(1)}_{m.group(2)}", "question_id": m.group(1), "judge_id": j, "judge_model": sedzia_model.get(j),
                  "judge_variant": wariant.get(mw.group(1), "without report") if mw else "without report",
                  "scores": {x: d.get(x) for x in ("A_R", "A2", "A3", "A5", "A6", "A8", "R", "K", "B1", "B2")},
                  "A6_classes": d.get("A6_typ"), "A6_origin": d.get("A6_pochodzenie"), "A6_scope": d.get("A6_zakres"),
                  "hallucinated": d.get("hallucinated"), "citations": d.get("powolania"), "unchecked": d.get("niesprawdzone"),
                  "rationale": d.get("uzasadnienie"), "verification_report_used": d.get("raport_faktow_uzyty"),
                  "meta": d.get("_meta"), "judgment_file": f})
zapisz("judgments.jsonl", oceny)

# ---------- verification.jsonl (krok faktów: jedna linia = jedno powołanie) ----------
wer = []
for f in sorted(glob.glob("verification/reports/P*.json")):
    m = re.match(r"verification/reports/(P\d\d)_(.+?)\.json$", f)
    d = json.load(open(f, encoding="utf-8"))
    for rodzaj, lista in (("provision", d.get("przepisy", [])), ("ruling", d.get("orzeczenia", [])),
                          ("publisher", d.get("publikatory", [])), ("date", d.get("daty", []))):
        for x in lista:
            wer.append({"answer_id": f"{m.group(1)}_{m.group(2)}", "question_id": m.group(1), "kind": rodzaj, "citation_id": x.get("id"),
                        "citation": x.get("powolanie") or x.get("sygnatura") or x.get("tekst"), "act": x.get("akt"), "role": x.get("rola"),
                        "quote": x.get("cytat"), "flags": x.get("flagi"), "verification": x.get("weryfikacja"), "versions": x.get("wersje"),
                        "versions_on_date": x.get("wersje_na_dzien"), "quote_comparison": x.get("cytat_porownanie"),
                        "generated_at": d.get("meta", {}).get("wygenerowano"), "report_file": f})
zapisz("verification.jsonl", wer)

# ---------- kontrola zgodności z dane.py ----------
pu = sum(1 for k in karty if k["correctly_grounded"]); hal = sum(1 for k in karty if k["hallucinated"])
assert (pu, hal) == (dane.LICZBY["pu"], dane.LICZBY["hal"]), (pu, hal)
print(f"kontrola: poprawnie ugruntowane {pu}, z halucynacją {hal} — zgodne z dane.py")
