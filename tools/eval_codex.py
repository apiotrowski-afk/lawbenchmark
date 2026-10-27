"""Bieg modelu OpenAI przez Codex CLI (logowanie kontem ChatGPT) na tierze „pytania” i kazusie SKD.

Każde zadanie = osobna nietrwała sesja (`--ephemeral`) w pustym katalogu, sandbox tylko do odczytu.
Wariant W0: wyszukiwanie wyłączone; wariant „web”: wyszukiwanie na żywo (model sam decyduje).
Ten sam wstęp co dla modeli lokalnych (eval_lokalne.py) — Codex nie ma osobnego promptu systemowego,
więc wstęp idzie na początek wiadomości. Zapis jak w pozostałych biegach. Wypisuje tylko czasy i liczniki.
Użycie: python eval_codex.py <etykieta> [--web] [--model M] [--tylko P01,KAZUS]
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

import yaml

REPO = os.path.expanduser("~/ktzr-hub/benchmark")
# codex jest z nvm — w powłoce nieinteraktywnej nie ma go na PATH; bierzemy najnowszy node
if not shutil.which("codex"):
    nvm = sorted(glob.glob(os.path.expanduser("~/.nvm/versions/node/*/bin")),
                 key=lambda s: [int(x) for x in s.split("/")[-2].lstrip("v").split(".")])
    if nvm:
        os.environ["PATH"] = nvm[-1] + os.pathsep + os.environ["PATH"]
    if not shutil.which("codex"):
        sys.exit("Codex: nie znaleziono programu codex (npm i -g @openai/codex)")
WSTEP = ("Jesteś asystentem prawnika w polskiej kancelarii. Odpowiadasz po polsku, "
         "na gruncie prawa polskiego i unijnego, podając podstawy prawne. "
         "Odpowiedz bezpośrednio w wiadomości — nie twórz plików i nie uruchamiaj poleceń.")
WSTEP_WEB = (" Możesz korzystać z wyszukiwania w internecie; jeśli z niego korzystasz, "
             "na końcu podaj adresy źródeł.")

etykieta = sys.argv[1]
web = "--web" in sys.argv
model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "gpt-6.1-sol"
wysilek = sys.argv[sys.argv.index("--wysilek") + 1] if "--wysilek" in sys.argv else "medium"
tylko = set(sys.argv[sys.argv.index("--tylko") + 1].split(",")) if "--tylko" in sys.argv else None

zadania = []
for f in sorted(glob.glob(f"{REPO}/pytania/klucze/P*.yaml")):
    k = yaml.safe_load(open(f))
    if not tylko or k["id"] in tylko:
        zadania.append((k["id"], (k.get("tekst_benchmarkowy") or k["tekst_oryginalny"]).strip()))
if not tylko or "KAZUS" in tylko:
    zadania.append(("KAZUS", open(f"{REPO}/skd/kazus_01_termin.md").read().strip()))


def bieg(tekst):
    with tempfile.TemporaryDirectory() as kat:
        wynik = os.path.join(kat, "_odp.md")
        cmd = ["codex", "exec", "--ephemeral", "--skip-git-repo-check", "-s", "read-only", "-C", kat,
               "--json", "-o", wynik, "-c", f'web_search="{"live" if web else "disabled"}"',
               # aplikacje konta ChatGPT (m.in. search_service.web_run) omijają web_search=disabled — wyłączone zawsze
               "-c", "features.apps=false"]
        cmd += ["-m", model, "-c", f'model_reasoning_effort="{wysilek}"']
        cmd.append("-")
        t0 = time.time()
        p = subprocess.run(cmd, input=WSTEP + (WSTEP_WEB if web else "") + "\n\n" + tekst,
                           capture_output=True, text=True, timeout=1800)
        czas = round(time.time() - t0, 1)
        odp = open(wynik).read() if os.path.exists(wynik) else ""
    zdarzenia, model_uzyty, tokeny = [], None, {}
    for linia in p.stdout.splitlines():
        try:
            e = json.loads(linia)
        except ValueError:
            continue
        typ = (e.get("item") or {}).get("type") or e.get("type")
        if typ in ("web_search", "command_execution", "mcp_tool_call", "file_change"):
            it = e.get("item") or {}
            zdarzenia.append({"typ": typ, "zapytanie": it.get("query"), "polecenie": it.get("command"),
                              "narzedzie": f'{it.get("server")}.{it.get("tool")}' if typ == "mcp_tool_call" else None})
        if e.get("type") == "turn.completed":
            tokeny = e.get("usage") or {}
        model_uzyty = model_uzyty or e.get("model")
    blad = None if p.returncode == 0 else f"kod {p.returncode}: {p.stderr.strip()[-300:]}"
    naglowek = {}
    for linia in (p.stderr + "\n" + p.stdout).splitlines():
        for klucz in ("model", "reasoning effort"):
            if linia.lower().startswith(klucz + ":"):
                naglowek.setdefault(klucz, linia.split(":", 1)[1].strip())
    return odp, czas, zdarzenia, tokeny, blad, naglowek


for pid, tekst in zadania:
    odp, czas, zdarzenia, tokeny, blad, naglowek = bieg(tekst)
    kat = f"{REPO}/skd/odpowiedzi/kazus_v3" if pid == "KAZUS" else f"{REPO}/pytania/odpowiedzi/{pid}"
    os.makedirs(kat, exist_ok=True)
    meta = {"pytanie": pid,
            "system": f"OpenAI {model} przez Codex CLI (rozumowanie: {wysilek}), "
                      + ("wariant A: wyszukiwanie na żywo" if web else "W0 bez wyszukiwania"),
            "model": model, "wysilek_rozumowania": wysilek,
            "data_odpowiedzi": time.strftime("%Y-%m-%d"), "czas_s": czas, "tokeny": tokeny,
            "wstep": WSTEP + (WSTEP_WEB if web else ""), "sandbox": "read-only, pusty katalog, sesja nietrwała",
            "aplikacje_chatgpt": "wyłączone (features.apps=false)",
            "liczba_wyszukan": sum(z["typ"] == "web_search" for z in zdarzenia),
            "inne_narzedzia": sum(z["typ"] != "web_search" for z in zdarzenia),
            "zdarzenia": zdarzenia, "blad": blad}
    with open(f"{kat}/{etykieta}.md", "w") as fh:
        fh.write("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\n")
        fh.write("## Pytanie\n\n" + tekst + "\n\n## Odpowiedź\n\n" + odp + "\n")
    print(f"{pid:6} {czas:7.1f}s  szuk={meta['liczba_wyszukan']} inne={meta['inne_narzedzia']}  "
          f"tok={tokeny.get('output_tokens', '?')}  {blad or 'ok'}", flush=True)
