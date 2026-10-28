"""Bieg czystego modelu Claude przez Claude Code CLI (subskrypcja (konto kancelarii)) na tierze „pytania”.

Bez narzędzi (--tools ""), bez MCP (--strict-mcp-config), bez ustawień i CLAUDE.md (--setting-sources ""),
bez zapisu sesji; uruchamiane w pustym katalogu. Ten sam wstęp co Codex/Gemini jako --system-prompt.
Zastrzeżenie: Claude Code zawsze dokleja sekcję techniczną środowiska (katalog, data, e-mail konta) —
zapisane w metadanych. Wyszukiwanie: brak (W0). Wypisuje tylko czasy i liczniki.
Użycie: python eval_claude_cli.py <etykieta> [--model opus] [--tylko P05,P06]
"""
import glob
import json
import os
import subprocess
import sys
import tempfile
import time

import yaml

REPO = os.path.expanduser("./pytania")
WSTEP = ("Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, "
         "na gruncie prawa polskiego i unijnego, podając podstawy prawne.")
etykieta = sys.argv[1]
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
model = arg("--model", "opus")
# --web (2026-10-17, decyzja Adama: W1 dla wszystkich modeli): WebSearch + WebFetch, to samo zdanie we wstępie co Codex --web
web = "--web" in sys.argv
WSTEP_WEB = (" Możesz korzystać z wyszukiwania w internecie; jeśli z niego korzystasz, "
             "na końcu podaj adresy źródeł.")
if web:
    WSTEP = WSTEP + WSTEP_WEB
tylko = set(arg("--tylko").split(",")) if arg("--tylko") else None

pytania = []
for f in sorted(glob.glob(f"{REPO}/klucze/P*.yaml")):
    k = yaml.safe_load(open(f))
    if not tylko or k["id"] in tylko:
        pytania.append((k["id"], (k.get("tekst_benchmarkowy") or k["tekst_oryginalny"]).strip()))

for pid, tekst in pytania:
    t0 = time.time()
    blad, odp, info = None, "", {}
    with tempfile.TemporaryDirectory() as pusty:
        narz = ["--tools", "WebSearch,WebFetch", "--allowedTools", "WebSearch,WebFetch"] if web else ["--tools", ""]
        cmd = ["claude", "-p", "--model", model, *narz, "--setting-sources", "", "--strict-mcp-config",
               "--no-session-persistence", "--output-format", "json", "--system-prompt", WSTEP, tekst]
        try:
            p = subprocess.run(cmd, cwd=pusty, capture_output=True, text=True, timeout=900)
            d = json.loads(p.stdout)
            odp = d.get("result", "") or ""
            mu = d.get("modelUsage") or {}
            info = {"model_id": ",".join(mu.keys()) or None, "koszt_usd_rownowaznik": d.get("total_cost_usd"),
                    "tokeny": d.get("usage", {}), "tury": d.get("num_turns")}
            if d.get("is_error") or not odp:
                blad = f"is_error={d.get('is_error')} subtype={d.get('subtype')}"
        except Exception as e:
            blad = f"{type(e).__name__}: {str(e)[:200]}"
    czas = round(time.time() - t0, 1)
    kat = f"{REPO}/odpowiedzi/{pid}"
    os.makedirs(kat, exist_ok=True)
    meta = {"pytanie": pid, "system": f"Claude {model} przez Claude Code CLI (subskrypcja), czysty model — bez MCP i CLAUDE.md, " + ("W1: WebSearch + WebFetch" if web else "W0"),
            "model_alias": model, "model_id": info.get("model_id"), "prompt_systemowy": WSTEP,
            "narzedzia": ["WebSearch", "WebFetch"] if web else [], "wyszukiwanie": web, "temperatura": "domyślna CLI (nieustawialna)",
            "kontekst_dodatkowy": "sekcja środowiska Claude Code (katalog tymczasowy, data, platforma, e-mail konta) — nie da się wyłączyć",
            "data_odpowiedzi": time.strftime("%Y-%m-%d"), "czas_s": czas,
            "tokeny": info.get("tokeny"), "koszt_usd_rownowaznik": info.get("koszt_usd_rownowaznik"), "blad": blad}
    with open(f"{kat}/{etykieta}.md", "w") as fh:
        fh.write("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\n" + odp + "\n")
    print(f"{pid:6} {czas:6.1f}s  model={info.get('model_id')}  {'BŁĄD ' + blad if blad else 'ok'}")
