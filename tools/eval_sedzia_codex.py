"""Drugi sędzia (inny dostawca) dla kart tieru „pytania”: model OpenAI przez Codex CLI z wyszukiwaniem.

Sędzia dostaje reguły oceny z README (bloki A i B), klucz pytania i SAMĄ treść odpowiedzi (bez nazwy
systemu i metadanych — ocena ślepa). Ma sprawdzić powołania w źródłach oficjalnych i zwrócić JSON.
Nie widzi karty pierwszego sędziego. Zapis: benchmark/pytania/oceny/_sedziowie/Pnn_<system>.<sedzia>.json
Użycie: python eval_sedzia_codex.py <sedzia> --model gpt-6-astra --systemy a,b,c --tylko P05,P06 [--rownolegle 3]
"""
import concurrent.futures as cf
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * (2 if os.path.basename(os.path.dirname(os.path.abspath(__file__))) == "verification" else 1))))  # katalog repo lawbenchmark
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
sedzia = sys.argv[1]
model = arg("--model", "gpt-6-astra")
systemy = arg("--systemy").split(",")
pytania = arg("--tylko").split(",")
rown = int(arg("--rownolegle", "3"))

readme = open(f"{REPO}/SPEC/scoring_spec_v1.0.1.md").read()
reguly = (readme[readme.index("## Blok A — obiektywny"):readme.index("## Warunki biegu (prompt)")]
          + "\n" + readme[readme.index("## Przykłady graniczne"):readme.index("## Status zbioru")])
WERSJA = (readme.split("Wersja specyfikacji oceny: ")[1].split(" ")[0]) if "Wersja specyfikacji oceny: " in readme else "?"

INSTR = """Jesteś sędzią w benchmarku prawniczym (prawo polskie). Oceniasz JEDNĄ odpowiedź systemu AI na pytanie prawne
według reguł i klucza poniżej. Nie wiesz, który system odpowiadał. Oceniaj wyłącznie według reguł i klucza.

OBOWIĄZEK: każde powołanie przepisu i orzeczenia z odpowiedzi sprawdź w źródle oficjalnym przez wyszukiwanie
(ISAP / api.sejm.gov.pl / eli.gov.pl dla aktów — k.p.c. to Dz.U. 2026 poz. 468, k.r.o. Dz.U. 2026 poz. 236,
u.k.s.c. Dz.U. 2025 poz. 1228; SAOS albo sn.pl dla orzeczeń). Porównaj literalnie numer jednostki i jej treść.
Nie oceniaj z pamięci. Jeśli czegoś nie da się sprawdzić, wpisz to w polu "niesprawdzone".

A6 jest ZERO-JEDYNKOWE (sekcja „A6 po decyzji z 2026-10-11” ma pierwszeństwo przed starszymi regułami): 0 i hallucinated=true,
gdy choć jedno twierdzenie o treści wskazanego przepisu lub orzeczenia jest niezgodne ze źródłem oficjalnym na datę stanu
prawnego (F, T, W albo S); samo pominięcie przesłanki albo wyjątku nie obniża A6 (test: czy dopisanie „co do zasady”
naprawia zdanie). Klasy O nie ma. Automatycznej stopki produktu („🛡 Weryfikacja przepisów”, wiersze „⚠ Niezweryfikowane”)
nie oceniaj w A6 — licz ją tylko w A8 (reguła 6). Stosuj „Przykłady graniczne” z końca reguł.

Zwróć WYŁĄCZNIE obiekt JSON (bez komentarza, bez bloków kodu) o polach:
{"A_R": 0|1|2, "A2": 0|1, "A3": 0|1|"nd", "A5": 0|1|"nd", "A6": 0|1, "A6_typ": ["F"|"T"|"W"|"S", ...],
 "A8": 0|0.5|1, "R": [0|1, ... w kolejności elementów pola rubryka z klucza], "K": [0|1, ... 1 = kara naliczona,
 w kolejności pola kary], "B1": 0|1|2, "B2": 0|1, "hallucinated": true|false,
 "powolania": [{"powolanie": "...", "zrodlo": "...", "werdykt": "zgodne|F|T|W|O|S|niesprawdzone"}],
 "niesprawdzone": ["..."], "uzasadnienie": "najwyżej 5 zdań o najważniejszych rozstrzygnięciach"}

=== REGUŁY OCENY (README) ===
%s

=== KLUCZ PYTANIA (YAML) ===
%s

=== ODPOWIEDŹ SYSTEMU DO OCENY ===
%s
"""


def tresc_odpowiedzi(pid, system):
    s = open(f"{REPO}/odpowiedzi/{pid}/{system}.md").read()
    return s.split("---", 2)[2].strip() if s.startswith("---") else s


def jeden(pid, system):
    cel = f"{REPO}/oceny/_sedziowie/{pid}_{system}.{sedzia}.json"
    if os.path.exists(cel):
        return pid, system, "pominięte (jest)", 0
    klucz = open(glob.glob(f"{REPO}/klucze/{pid}_*.yaml")[0]).read()
    prompt = INSTR % (reguly, klucz, tresc_odpowiedzi(pid, system))
    t0 = time.time()
    with tempfile.TemporaryDirectory() as kat:
        wynik = os.path.join(kat, "_odp.md")
        cmd = ["codex", "exec", "--ephemeral", "--skip-git-repo-check", "-s", "read-only", "-C", kat, "--json", "-o", wynik,
               "-c", 'web_search="live"', "-c", "features.apps=false", "-m", model, "-c", 'model_reasoning_effort="medium"', "-"]
        try:
            p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=1800)
            odp = open(wynik).read() if os.path.exists(wynik) else ""
        except Exception as e:
            return pid, system, f"BŁĄD {type(e).__name__}", round(time.time() - t0)
    if not odp.strip():  # limit konta lub błąd CLI — nie zapisuj pustego wyniku, bieg wznowi kartę później
        wyj = p.stderr + p.stdout
        powod = "limit konta" if ("usage limit" in wyj or "429" in wyj or "Too Many Requests" in wyj) else "pusta odpowiedź"
        return pid, system, f"BŁĄD {powod} (nie zapisano)", round(time.time() - t0)
    # 2026-10-25: zapisujemy treść wywołań (zapytania, źródła), nie tylko liczbę — zalecenie z artykułu v1.2
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from codex_log_wyszukan import wyszukania
    wysz = wyszukania(p.stdout)
    szuk = wysz["wyszukan"]
    m = re.search(r"\{.*\}", odp, re.S)
    try:
        d = json.loads(m.group(0))
    except Exception:
        d = {"blad_parsowania": True, "surowe": odp[:4000]}
    d["_meta"] = {"sedzia": sedzia, "model": model, "pytanie": pid, "system": system, "wyszukan": szuk, "zapytania": wysz["zapytania"], "zrodla_sedziego": wysz["zrodla_sedziego"],
                  "czas_s": round(time.time() - t0), "data": time.strftime("%Y-%m-%d"), "slepa": True, "specyfikacja": WERSJA}
    os.makedirs(os.path.dirname(cel), exist_ok=True)
    json.dump(d, open(cel, "w"), ensure_ascii=False, indent=1)
    return pid, system, "BŁĄD parsowania" if d.get("blad_parsowania") else "ok", d["_meta"]["czas_s"]


zad = [(p, s) for s in systemy for p in pytania if os.path.exists(f"{REPO}/answers/{p}/{s}.md")]
with cf.ThreadPoolExecutor(rown) as ex:
    for pid, system, st, czas in ex.map(lambda z: jeden(*z), zad):
        print(f"{pid} {system:32} {czas:5}s  {st}", flush=True)
