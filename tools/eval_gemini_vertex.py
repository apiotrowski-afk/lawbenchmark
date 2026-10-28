"""Bieg czystego Gemini przez Vertex AI na tierze „pytania” — model bez narzędzi KTZR.

Bez bazy kancelarii, bez narzędzi, bez wyszukiwania (W0). Ten sam wstęp co Codex i modele lokalne
(eval_lokalne.py / eval_codex.py), jako system_instruction. Projekt GCP z GOOGLE_CLOUD_PROJECT, region europe-west4.
Każde pytanie = osobne wywołanie z pustą historią. Wypisuje tylko czasy i liczniki tokenów.
Użycie: python eval_gemini_vertex.py <etykieta> [--model gemini-2.5-pro] [--region europe-west4|global] [--tylko P05,P06] [--temp 0.1] [--myslenie high]
"""
import glob
import os
import sys
import time

import yaml
from google import genai
from google.genai import types

REPO = os.path.expanduser("./pytania")
WSTEP = ("Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, "
         "na gruncie prawa polskiego i unijnego, podając podstawy prawne.")
PROJEKT = os.environ.get("GOOGLE_CLOUD_PROJECT", "twoj-projekt-gcp")

etykieta = sys.argv[1]
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
model = arg("--model", "gemini-2.5-pro")
temp = float(arg("--temp", "0.1"))
# Gemini 3.x jest dostępne tylko w regionie „global”; pytania benchmarkowe nie zawierają danych klientów
REGION = arg("--region", "europe-west4")
tylko = set(arg("--tylko").split(",")) if arg("--tylko") else None

pytania = []
for f in sorted(glob.glob(f"{REPO}/klucze/P*.yaml")):
    k = yaml.safe_load(open(f))
    if not tylko or k["id"] in tylko:
        pytania.append((k["id"], (k.get("tekst_benchmarkowy") or k["tekst_oryginalny"]).strip()))

klient = genai.Client(vertexai=True, project=PROJEKT, location=REGION,
                      http_options=types.HttpOptions(timeout=600_000))  # 10 min na zapytanie: 17.10 Argon zawisł bez limitu
# --myslenie low|medium|high: wymuszony poziom rozumowania (Gemini 4 Argon domyślnie sam decyduje i na pytaniach
# prawnych nie rozumował wcale); bez tej opcji zachowanie domyślne modelu
myslenie = arg("--myslenie")
# --web (2026-10-17, decyzja Adama: W1 dla wszystkich): Google Search + URL context (czytanie całych stron, jak
# WebFetch u Claude i pobieranie stron u Codex); to samo zdanie we wstępie co Codex --web
web = "--web" in sys.argv
if web:
    WSTEP = WSTEP + (" Możesz korzystać z wyszukiwania w internecie; jeśli z niego korzystasz, "
                     "na końcu podaj adresy źródeł.")
narz = [types.Tool(google_search=types.GoogleSearch()), types.Tool(url_context=types.UrlContext())] if web else None
cfg = types.GenerateContentConfig(system_instruction=WSTEP, temperature=temp, tools=narz,
                                  thinking_config=types.ThinkingConfig(thinking_level=myslenie) if myslenie else None)

for pid, tekst in pytania:
    t0 = time.time()
    blad, odp, tok, zap, zr = None, "", {}, [], []
    try:
        r = klient.models.generate_content(model=model, contents=tekst, config=cfg)
        odp = r.text or ""
        gm = r.candidates[0].grounding_metadata if r.candidates else None
        zap = list(getattr(gm, "web_search_queries", None) or [])
        # uri to przekierowanie vertexaisearch — domenę źródła niesie title
        zr = [getattr(getattr(c, "web", None), "title", None) or getattr(getattr(c, "web", None), "uri", None)
              for c in (getattr(gm, "grounding_chunks", None) or [])]
        zr = [z for z in zr if z][:25]
        u = r.usage_metadata
        tok = {"wejscie": u.prompt_token_count, "wyjscie": u.candidates_token_count,
               "rozumowanie": getattr(u, "thoughts_token_count", None),
               # tokeny treści z narzędzi (url_context, grounding) — potrzebne do kosztu W1 (koszt.py)
               "narzedzia": getattr(u, "tool_use_prompt_token_count", None),
               "cache": getattr(u, "cached_content_token_count", None),
               "razem": getattr(u, "total_token_count", None)}
        if not odp:
            blad = f"pusta odpowiedź (finish_reason={r.candidates[0].finish_reason if r.candidates else '?'})"
    except Exception as e:
        blad = f"{type(e).__name__}: {str(e)[:200]}"
    czas = round(time.time() - t0, 1)
    kat = f"{REPO}/odpowiedzi/{pid}"
    os.makedirs(kat, exist_ok=True)
    meta = {"pytanie": pid, "system": f"Gemini {model} (Vertex AI, czysty model — bez narzędzi KTZR, " + ("W1: Google Search + URL context)" if web else "W0 bez wyszukiwania)"),
            "model": model, "projekt": PROJEKT, "region": REGION, "temperatura": temp,
            "poziom_rozumowania": myslenie or "domyślny modelu",
            "prompt_systemowy": WSTEP, "narzedzia": ["google_search", "url_context"] if web else [], "wyszukiwanie": web,
            "zapytania": zap, "zrodla": zr,
            "data_odpowiedzi": time.strftime("%Y-%m-%d"), "czas_s": czas, "tokeny": tok, "blad": blad}
    with open(f"{kat}/{etykieta}.md", "w") as fh:
        fh.write("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\n" + odp + "\n")
    print(f"{pid:6} {czas:6.1f}s  tok_out={tok.get('wyjscie')}  {'BŁĄD ' + blad if blad else 'ok'}")
