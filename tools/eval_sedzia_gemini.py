"""Drugi sędzia (inny dostawca) dla kart tieru „pytania”: Gemini przez Vertex AI z wyszukiwaniem Google.

Ten sam prompt i format wyniku co eval_sedzia_codex.py (import INSTR i reguł stamtąd nie jest możliwy bez
uruchomienia biegu, więc tekst instrukcji jest wspólny przez plik README + stała poniżej). Ocena ślepa:
sędzia dostaje reguły, klucz i samą treść odpowiedzi. Zapis: oceny/_sedziowie/Pnn_<system>.<sedzia>.json
Użycie: python eval_sedzia_gemini.py <sedzia> [--model gemini-3.1-pro-preview] --systemy a,b --tylko P05,P06 [--rownolegle 4] [--myslenie high] [--readme plik]
"""
import concurrent.futures as cf
import glob
import json
import os
import re
import sys
import time

from google import genai
from google.genai import types

REPO = os.path.expanduser("./pytania")
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
sedzia = sys.argv[1]
model = arg("--model", "gemini-3.1-pro-preview")
systemy = arg("--systemy").split(",")
pytania = arg("--tylko").split(",")
rown = int(arg("--rownolegle", "4"))

# --readme <plik>: reguły z zamrożonej wersji README (np. z gita), żeby nowy sędzia oceniał według tych samych
# reguł co wcześniejsi (2026-10-17: Argon jako sędzia na README z e336d22, bez przykładów granicznych z 17.10)
readme = open(arg("--readme", f"{REPO}/README.md")).read()
reguly = (readme[readme.index("## Blok A — obiektywny"):readme.index("## Warunki biegu (prompt)")]
          + "\n" + readme[readme.index("## Przykłady graniczne"):readme.index("## Status zbioru")])
WERSJA = readme.split("Wersja specyfikacji oceny: ")[1].split(" ")[0]
# instrukcja identyczna jak dla sędziego Codex — wycinana z jego pliku, żeby oba biegi miały jeden tekst
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval_sedzia_codex.py")).read()
INSTR = _src[_src.index('INSTR = """') + len('INSTR = """'):_src.index('"""\n\n\ndef tresc_odpowiedzi')]

klient = genai.Client(vertexai=True, project="ktzr-asystent", location="global",
                      http_options=types.HttpOptions(timeout=1_200_000))  # 20 min na zapytanie: 17.10 Argon zawisł bez limitu
# --myslenie low|medium|high: wymuszony poziom rozumowania (Gemini 4 Argon bez tego sam rezygnuje z rozumowania)
myslenie = arg("--myslenie")
cfg = types.GenerateContentConfig(temperature=0.0, tools=[types.Tool(google_search=types.GoogleSearch())],
                                  thinking_config=types.ThinkingConfig(thinking_level=myslenie) if myslenie else None)


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
    try:
        r = klient.models.generate_content(model=model, contents=prompt, config=cfg)
        odp = r.text or ""
        gm = r.candidates[0].grounding_metadata if r.candidates else None
        zap = list(getattr(gm, "web_search_queries", None) or [])
        zr = [getattr(getattr(c, "web", None), "uri", None) or getattr(getattr(c, "web", None), "title", None)
              for c in (getattr(gm, "grounding_chunks", None) or [])]
        tok = {"wejscie": r.usage_metadata.prompt_token_count, "wyjscie": r.usage_metadata.candidates_token_count}
    except Exception as e:
        return pid, system, f"BŁĄD {type(e).__name__}: {str(e)[:80]} (nie zapisano)", round(time.time() - t0)
    if not odp.strip():
        return pid, system, "BŁĄD pusta odpowiedź (nie zapisano)", round(time.time() - t0)
    m = re.search(r"\{.*\}", odp, re.S)
    try:
        d = json.loads(m.group(0))
    except Exception:
        d = {"blad_parsowania": True, "surowe": odp[:4000]}
    d["_meta"] = {"sedzia": sedzia, "model": model, "pytanie": pid, "system": system, "wyszukan": len(zap),
                  "zapytania": zap[:20], "zrodla_sedziego": [z for z in zr if z][:25], "tokeny": tok,
                  "czas_s": round(time.time() - t0), "data": time.strftime("%Y-%m-%d"), "slepa": True,
                  "specyfikacja": WERSJA, "temperatura": 0.0, "region": "global",
                  "poziom_rozumowania": myslenie or "domyślny modelu", "readme": arg("--readme", "bieżące")}
    os.makedirs(os.path.dirname(cel), exist_ok=True)
    json.dump(d, open(cel, "w"), ensure_ascii=False, indent=1)
    return pid, system, "BŁĄD parsowania" if d.get("blad_parsowania") else "ok", d["_meta"]["czas_s"]


zad = [(p, s) for s in systemy for p in pytania if os.path.exists(f"{REPO}/odpowiedzi/{p}/{s}.md")]
with cf.ThreadPoolExecutor(rown) as ex:
    for pid, system, st, czas in ex.map(lambda z: jeden(*z), zad):
        print(f"{pid} {system:32} {czas:5}s  {st}", flush=True)
