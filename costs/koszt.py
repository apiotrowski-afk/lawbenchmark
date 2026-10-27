"""Metryka kosztu benchmarku LexAlpha (pomocnicza; decyzja A. Piotrowskiego 2026-10-18).

Czyta front matter odpowiedzi (pytania/odpowiedzi/<P>/<system>.md), cennik (cennik_2026-10-18.yaml)
i karty ocen (pytania/oceny/<P>_<system>.md). Liczy koszt równoważny API każdej odpowiedzi z rozbiciem
na wejście, cache, wyjście, rozumowanie i narzędzia, a potem tabelę system × (odpowiedzi, koszt łączny,
średni, mediana czasu, poprawnie ugruntowane = A6 1/1 i A-R 2/2, koszt na poprawnie ugruntowaną).

Zasady:
- brak danych -> None (w raporcie „n/d”), nigdy 0;
- koszt niepełny (np. nieznana liczba wyszukań Claude CLI, brak tokenów url_context Vertex) ->
  flaga dolna_granica i znak „≥” w raporcie;
- Claude CLI: koszt główny = pole koszt_usd_rownowaznik (obejmuje pomocniczego Haiku); równolegle
  wyliczenie z tokenów głównego modelu i rozbieżność;
- nic nie jest zapisywane poza koszt_<data>.md, koszt_<data>.csv i koszt_<data>_odpowiedzi.csv.

Użycie: python3 -I koszt.py [--cennik ścieżka] [--tylko P05,P06]
"""
import csv
import os
import re
import statistics
import sys

import yaml

BENCH = os.path.dirname(os.path.abspath(__file__))
ODP = os.path.join(BENCH, "pytania", "odpowiedzi")
OCENY = os.path.join(BENCH, "pytania", "oceny")


def arg(nazwa, domyslna=None):
    return sys.argv[sys.argv.index(nazwa) + 1] if nazwa in sys.argv else domyslna


CENNIK_PLIK = arg("--cennik", os.path.join(BENCH, "cennik_2026-10-18.yaml"))
DATA = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(CENNIK_PLIK)).group(1)
PYTANIA = (arg("--tylko") or "P01,P04,P05,P06,P07,P08,P09,P10,P12,P13").split(",")

# system -> (model w cenniku, rodzina, wariant wyszukiwania)
SYSTEMY = {
    "chatgpt_codex_w0_r3": ("gpt-6.1-sol", "codex", "W0"),
    "chatgpt_codex_web_r3": ("gpt-6.1-sol", "codex", "W1"),
    "codex_astra6_w0_r3": ("gpt-6-astra", "codex", "W0"),
    "codex_astra6_web_r3": ("gpt-6-astra", "codex", "W1"),
    "codex_terra56_w0_r3": ("gpt-5.6-terra", "codex", "W0"),
    "codex_terra56_web_r3": ("gpt-5.6-terra", "codex", "W1"),
    "haiku_cli_w0_r3": ("claude-haiku-5-5", "claude_cli", "W0"),
    "haiku_cli_w1_r3": ("claude-haiku-5-5", "claude_cli", "W1"),
    "sonnet_cli_w0_r3": ("claude-sonnet-5-5", "claude_cli", "W0"),
    "sonnet_cli_w1_r3": ("claude-sonnet-5-5", "claude_cli", "W1"),
    "opus_cli_w0_r3": ("claude-opus-5-5", "claude_cli", "W0"),
    "opus_cli_w1_r3": ("claude-opus-5-5", "claude_cli", "W1"),
    "gemini38flash_vertex_w0_r3": ("gemini-3.8-flash", "vertex", "W0"),
    "gemini38flash_vertex_w1_r3": ("gemini-3.8-flash", "vertex", "W1"),
    "argon4_high_vertex_w0_r3": ("gemini-4-argon", "vertex", "W0"),
    "argon4_high_vertex_w1_r3": ("gemini-4-argon", "vertex", "W1"),
}
ROZLICZENIE = {"codex": "równoważnik (subskrypcja ChatGPT/Codex)",
               "claude_cli": "równoważnik (subskrypcja Claude Code)",
               "vertex": "faktyczny (Vertex, global)"}
M = 1_000_000


def front_matter(sciezka):
    tekst = open(sciezka, encoding="utf-8").read()
    if not tekst.startswith("---"):
        return None
    return yaml.safe_load(tekst.split("---", 2)[1]) or {}


def punkty(wiersz):
    # „2/2” -> 2.0, „½/1” -> 0.5, „n/d (blokada)” -> None
    m = re.match(r"\s*([\d½.]+)\s*/\s*\d", wiersz)
    if not m:
        return None
    return float(m.group(1).replace("½", "0.5"))


def karta(pid, system):
    sciezka = os.path.join(OCENY, f"{pid}_{system}.md")
    if not os.path.exists(sciezka):
        return None
    s = open(sciezka, encoding="utf-8").read()
    a6 = re.findall(r"^\| A6 \|([^|]*)\|", s, re.M)
    ar = re.findall(r"^\| A-R \|([^|]*)\|", s, re.M)
    if len(a6) != 1 or len(ar) != 1:
        # karta niejednoznaczna — nie zgadujemy
        return {"a6": None, "ar": None, "uwaga": f"wiersze A6={len(a6)}, A-R={len(ar)}"}
    return {"a6": punkty(a6[0]), "ar": punkty(ar[0]), "a6_surowe": a6[0].strip(), "uwaga": ""}


def koszt_codex(fm, c, narz):
    t = fm.get("tokeny") or {}
    wynik, uwagi, dolna = {}, [], False
    if "input_tokens" not in t or "output_tokens" not in t:
        return None, ["brak tokenów"], True
    wej, cache = t["input_tokens"], t.get("cached_input_tokens") or 0
    zapis = t.get("cache_write_input_tokens") or 0
    rozum = t.get("reasoning_output_tokens") or 0
    stawki = c
    prog = (c.get("dlugi_kontekst") or {}).get("prog_tokenow_wejscia")
    if prog and wej > prog:
        # Codex sumuje tokeny wielu wywołań; próg dotyczy pojedynczego wywołania — nie da się ustalić
        uwagi.append(f"wejście łącznie {wej} > {prog} (suma tur Codex; stawka krótkiego kontekstu — dolna granica)")
        dolna = True
    # cached_input_tokens i cache_write są częścią input_tokens (sprawdzone: cached <= input we wszystkich 60 plikach)
    wynik["k_wejscie"] = (wej - cache - zapis) * stawki["wejscie"] / M
    wynik["k_cache_odczyt"] = cache * stawki["wejscie_cache_odczyt"] / M
    wynik["k_cache_zapis"] = zapis * stawki["zapis_cache"] / M
    # rozumowanie jest częścią output_tokens i płaci się je jak wyjście
    wynik["k_wyjscie"] = (t["output_tokens"] - rozum) * stawki["wyjscie"] / M
    wynik["k_rozumowanie"] = rozum * stawki["wyjscie"] / M
    n = fm.get("liczba_wyszukan")
    if n is None:
        wynik["k_narzedzia"] = None
        dolna = True
        uwagi.append("brak liczby wyszukań")
    else:
        wynik["k_narzedzia"] = n * narz["openai_web_search"]["cena_za_wywolanie"]
    wynik["wyszukania"] = n
    return wynik, uwagi, dolna


def tokeny_claude(t, c):
    """Wyliczenie kosztu głównego modelu Claude z pola tokeny (bez pomocniczego Haiku)."""
    stawki = c
    prompt = (t.get("input_tokens") or 0) + (t.get("cache_read_input_tokens") or 0) + (t.get("cache_creation_input_tokens") or 0)
    uwagi = []
    prog = (c.get("dlugi_kontekst") or {}).get("prog_tokenow_wejscia")
    if prog and prompt > prog:
        uwagi.append(f"prompt łącznie {prompt} > {prog} (suma tur; stawka podstawowa)")
    cc = t.get("cache_creation") or {}
    z1h = cc.get("ephemeral_1h_input_tokens")
    z5m = cc.get("ephemeral_5m_input_tokens")
    if z1h is None and z5m is None:
        # brak podziału — przyjmujemy 5 min (dolna stawka) i zaznaczamy
        z5m, z1h = t.get("cache_creation_input_tokens") or 0, 0
        uwagi.append("brak podziału zapisu cache 5m/1h — przyjęto 5m")
    rozum = (t.get("output_tokens_details") or {}).get("thinking_tokens") or 0
    w = {
        "k_wejscie": (t.get("input_tokens") or 0) * stawki["wejscie"] / M,
        "k_cache_odczyt": (t.get("cache_read_input_tokens") or 0) * stawki["wejscie_cache_odczyt"] / M,
        "k_cache_zapis": ((z5m or 0) * stawki["zapis_cache_5m"] + (z1h or 0) * stawki["zapis_cache_1h"]) / M,
        # thinking_tokens to część output_tokens (dokumentacja extended thinking)
        "k_wyjscie": ((t.get("output_tokens") or 0) - rozum) * stawki["wyjscie"] / M,
        "k_rozumowanie": rozum * stawki["wyjscie"] / M,
    }
    return w, uwagi


def koszt_claude(fm, c, narz, wariant):
    t = fm.get("tokeny") or {}
    if "output_tokens" not in t:
        return None, ["brak tokenów"], True
    w, uwagi = tokeny_claude(t, c)
    dolna = False
    z_tokenow = sum(w.values())
    w["koszt_z_tokenow"] = z_tokenow
    stu = t.get("server_tool_use") or {}
    ws = stu.get("web_search_requests") or 0
    if wariant == "W0":
        w["k_narzedzia"] = 0.0
        w["wyszukania"] = 0
    else:
        # WebSearch/WebFetch w Claude Code mijają licznik server_tool_use (zwykle 0 mimo użycia) — liczba nieznana
        w["wyszukania"] = None
        if ws:
            w["k_narzedzia"] = ws * narz["anthropic_web_search"]["cena_za_wywolanie"]
            uwagi.append(f"server_tool_use.web_search_requests={ws} (może być niepełne)")
        else:
            w["k_narzedzia"] = None
            uwagi.append("liczba wyszukań nieznana (server_tool_use = 0 mimo narzędzi klienta) — opłata za wyszukiwanie n/d")
        dolna = True
    cli = fm.get("koszt_usd_rownowaznik")
    w["koszt_cli"] = cli
    if cli is not None:
        w["k_pomocniczy"] = cli - z_tokenow
    else:
        w["k_pomocniczy"] = None
        uwagi.append("brak koszt_usd_rownowaznik — użyto wyliczenia z tokenów (bez pomocniczego Haiku)")
        dolna = True
    return w, uwagi, dolna


def koszt_vertex(fm, c, narz, wariant):
    t = fm.get("tokeny") or {}
    if t.get("wejscie") is None or t.get("wyjscie") is None:
        return None, ["brak tokenów"], True
    uwagi, dolna = [], False
    rozum = t.get("rozumowanie")
    if rozum is None:
        uwagi.append("brak tokenów rozumowania")
        dolna = True
    w = {
        # od 2026-10-19 skrypt Vertex zapisuje tokeny treści narzędzi (url_context) — wejście płatne stawką wejścia
        "k_wejscie": (t["wejscie"] + (t.get("narzedzia") or 0)) * c["wejscie"] / M,
        "k_cache_odczyt": 0.0,
        "k_cache_zapis": 0.0,
        # Vertex: candidates_token_count nie obejmuje thoughts; oba płatne stawką „response and reasoning”
        "k_wyjscie": t["wyjscie"] * c["wyjscie"] / M,
        "k_rozumowanie": (rozum or 0) * c["wyjscie"] / M,
    }
    if wariant == "W0":
        w["k_narzedzia"], w["wyszukania"] = 0.0, 0
    else:
        zap = len(fm.get("zapytania") or [])
        w["wyszukania"] = zap
        if fm.get("zrodla"):
            w["k_narzedzia"] = zap * narz["vertex_google_search_grounding"]["cena_za_zapytanie"]
        else:
            # opłata tylko gdy grounding zwróci źródła
            w["k_narzedzia"] = 0.0
            uwagi.append(f"{zap} zapytań bez zwróconych źródeł — grounding nienaliczany")
        if t.get("narzedzia") is None:
            uwagi.append("tokeny treści url_context (tool_use_prompt_token_count) niezapisane — koszt wejścia zaniżony")
            dolna = True
    if fm.get("blad"):
        uwagi.append(f"błąd: {str(fm['blad'])[:60]} (Vertex nalicza odpowiedzi 200 — przyjęto naliczenie)")
    return w, uwagi, dolna


def csv_wartosc(v):
    # CSV: n/d zamiast pustych pól, liczby zaokrąglone do 6 miejsc
    if v is None:
        return "n/d"
    if isinstance(v, float):
        return round(v, 6)
    return v


def fmt(x, nd="n/d", cyfry=4, dolna=False):
    if x is None:
        return nd
    return ("≥ " if dolna else "") + f"{x:.{cyfry}f}"


def main():
    cennik = yaml.safe_load(open(CENNIK_PLIK, encoding="utf-8"))
    modele, narz = cennik["modele"], cennik["narzedzia"]
    wiersze, braki = [], []
    for system, (model, rodzina, wariant) in SYSTEMY.items():
        for pid in PYTANIA:
            sciezka = os.path.join(ODP, pid, f"{system}.md")
            if not os.path.exists(sciezka):
                braki.append(f"brak odpowiedzi {pid}/{system}.md")
                continue
            fm = front_matter(sciezka)
            c = modele[model]
            if rodzina == "codex":
                w, uwagi, dolna = koszt_codex(fm, c, narz)
            elif rodzina == "claude_cli":
                w, uwagi, dolna = koszt_claude(fm, c, narz, wariant)
            else:
                w, uwagi, dolna = koszt_vertex(fm, c, narz, wariant)
            k = karta(pid, system)
            if k is None:
                braki.append(f"brak karty {pid}_{system}.md")
                k = {"a6": None, "ar": None, "uwaga": "brak karty"}
            if w is None:
                koszt = None
            elif rodzina == "claude_cli" and w.get("koszt_cli") is not None:
                koszt = w["koszt_cli"] + (w["k_narzedzia"] or 0)
            else:
                skl = [w[x] for x in ("k_wejscie", "k_cache_odczyt", "k_cache_zapis", "k_wyjscie", "k_rozumowanie")]
                koszt = sum(skl) + (w["k_narzedzia"] or 0)
            poprawna = None if (k["a6"] is None and k["ar"] is None and k["uwaga"]) else (k["a6"] == 1 and k["ar"] == 2)
            wiersze.append({
                "pytanie": pid, "system": system, "model": model, "wariant": wariant, "rozliczenie": ROZLICZENIE[rodzina],
                "data_odpowiedzi": fm.get("data_odpowiedzi"), "czas_s": fm.get("czas_s"),
                **{x: (w or {}).get(x) for x in ("k_wejscie", "k_cache_odczyt", "k_cache_zapis", "k_wyjscie",
                                                  "k_rozumowanie", "k_narzedzia", "wyszukania", "koszt_cli",
                                                  "koszt_z_tokenow", "k_pomocniczy")},
                "koszt_usd": koszt, "dolna_granica": dolna,
                "A6": k["a6"], "A-R": k["ar"], "poprawnie_ugruntowana": poprawna,
                "uwagi": "; ".join(uwagi + ([k["uwaga"]] if k.get("uwaga") else [])),
            })

    # --- zestawienie per system ---
    tabela = []
    for system, (model, rodzina, wariant) in SYSTEMY.items():
        ws = [w for w in wiersze if w["system"] == system]
        n = len(ws)
        koszty = [w["koszt_usd"] for w in ws]
        laczny = None if (not ws or any(k is None for k in koszty)) else sum(koszty)
        dolna = any(w["dolna_granica"] for w in ws)
        czasy = [w["czas_s"] for w in ws if w["czas_s"] is not None]
        popr = [w["poprawnie_ugruntowana"] for w in ws]
        n_popr = None if any(p is None for p in popr) else sum(1 for p in popr if p)
        wysz = [w["wyszukania"] for w in ws]
        tabela.append({
            "system": system, "model": model, "wariant": wariant, "rozliczenie": ROZLICZENIE[rodzina],
            "odpowiedzi": n, "koszt_laczny_usd": laczny,
            "koszt_sredni_usd": None if laczny is None or not n else laczny / n,
            "mediana_czasu_s": statistics.median(czasy) if czasy else None,
            "poprawnie_ugruntowane": n_popr,
            "koszt_na_poprawnie_ugruntowana_usd": None if (laczny is None or not n_popr) else laczny / n_popr,
            "wyszukania": None if any(x is None for x in wysz) else sum(wysz),
            "dolna_granica": dolna,
        })

    # --- zapis CSV ---
    with open(os.path.join(BENCH, f"koszt_{DATA}.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(tabela[0]))
        wr.writeheader()
        for t in tabela:
            wr.writerow({k: csv_wartosc(v) for k, v in t.items()})
    with open(os.path.join(BENCH, f"koszt_{DATA}_odpowiedzi.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(wiersze[0]))
        wr.writeheader()
        for w in wiersze:
            wr.writerow({k: csv_wartosc(v) for k, v in w.items()})

    # --- zapis MD ---
    L = [f"# Koszt równoważny API — benchmark LexAlpha, bieg r3 (cennik z {DATA})", "",
         f"Wygenerowano skryptem `benchmark/koszt.py` z `{os.path.basename(CENNIK_PLIK)}`, front matter odpowiedzi "
         f"i kart ocen. Pytania: {', '.join(PYTANIA)}. Metryka pomocnicza — nie wpływa na punkty ani ranking jakości.",
         "", "„Poprawnie ugruntowana” = karta z A6 = 1/1 i A-R = 2/2. „≥” = dolna granica (część kosztu nieznana, "
         "zob. uwagi). n/d = brak danych (nie zero).", "",
         "| System | Model | W | Rozliczenie | Odp. | Koszt łączny USD | Śr. na odp. USD | Mediana czasu s | "
         "Poprawnie ugruntowane | USD na poprawnie ugruntowaną | Wyszukania |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in tabela:
        L.append(f"| {t['system']} | {t['model']} | {t['wariant']} | {t['rozliczenie']} | {t['odpowiedzi']} | "
                 f"{fmt(t['koszt_laczny_usd'], dolna=t['dolna_granica'])} | {fmt(t['koszt_sredni_usd'], dolna=t['dolna_granica'])} | "
                 f"{fmt(t['mediana_czasu_s'], cyfry=1)} | {fmt(t['poprawnie_ugruntowane'], cyfry=0)} z {t['odpowiedzi']} | "
                 f"{fmt(t['koszt_na_poprawnie_ugruntowana_usd'], dolna=t['dolna_granica'])} | {fmt(t['wyszukania'], cyfry=0)} |")

    # rozbicie kosztu per system
    L += ["", "## Rozbicie kosztu (suma per system, USD)", "",
          "| System | Wejście | Cache odczyt | Cache zapis | Wyjście | Rozumowanie | Narzędzia | Pomocniczy model (CLI − tokeny) |",
          "|---|---|---|---|---|---|---|---|"]
    for system in SYSTEMY:
        ws = [w for w in wiersze if w["system"] == system]

        def s(pole):
            v = [w[pole] for w in ws]
            return None if any(x is None for x in v) else sum(v)
        pom = s("k_pomocniczy") if SYSTEMY[system][1] == "claude_cli" else None
        L.append(f"| {system} | {fmt(s('k_wejscie'))} | {fmt(s('k_cache_odczyt'))} | {fmt(s('k_cache_zapis'))} | "
                 f"{fmt(s('k_wyjscie'))} | {fmt(s('k_rozumowanie'))} | {fmt(s('k_narzedzia'))} | "
                 f"{fmt(pom) if SYSTEMY[system][1] == 'claude_cli' else '—'} |")

    # rozbieżności Claude CLI
    L += ["", "## Claude CLI: koszt_usd_rownowaznik vs wyliczenie z tokenów głównego modelu", "",
          "Różnica = koszt pomocniczego Haiku (model_id „claude-haiku-5-5,…”) i ewentualne inne składniki liczone przez CLI. "
          "Wyliczenie: zapis cache wg podziału 1h/5m z `cache_creation`, odczyt cache, wejście, wyjście (z rozumowaniem).", "",
          "| System | Σ CLI USD | Σ z tokenów USD | Różnica USD | Różnica % | min–max różnicy na odp. USD | odp. z różnicą < 0 |",
          "|---|---|---|---|---|---|---|"]
    for system, (model, rodzina, _) in SYSTEMY.items():
        if rodzina != "claude_cli":
            continue
        ws = [w for w in wiersze if w["system"] == system and w["koszt_cli"] is not None]
        if not ws:
            L.append(f"| {system} | n/d | n/d | n/d | n/d | n/d | n/d |")
            continue
        a, b = sum(w["koszt_cli"] for w in ws), sum(w["koszt_z_tokenow"] for w in ws)
        r = [w["k_pomocniczy"] for w in ws]
        L.append(f"| {system} | {a:.4f} | {b:.4f} | {a - b:.4f} | {(a - b) / b * 100:.1f} | {min(r):.4f} – {max(r):.4f} | "
                 f"{sum(1 for x in r if x < -1e-9)} |")

    L += ["", "## Uwagi do danych", "",
          "- Codex: tokeny to suma wszystkich wywołań w sesji; `cached_input_tokens` jest częścią `input_tokens`, "
          "`reasoning_output_tokens` częścią `output_tokens` (sprawdzone na 60 plikach). Opłata za web search = "
          "`liczba_wyszukan` × $0.01; liczba obejmuje też zdarzenia web_search z pustym zapytaniem (otwarcia stron).",
          "- Claude CLI W1: `server_tool_use.web_search_requests` = 0 we wszystkich odpowiedziach mimo WebSearch/WebFetch "
          "(narzędzia klienta Claude Code) — opłata za wyszukiwanie n/d, koszt to dolna granica.",
          "- Vertex W1: skrypt `eval_gemini_vertex.py` nie zapisuje `tool_use_prompt_token_count` (treść stron z url_context), "
          "więc koszt wejścia jest zaniżony; grounding wyceniony $14/1000 zapytań (cena ponad bezpłatne 5000/mies. — "
          "przy małym wolumenie faktyczna opłata może wynosić 0).",
          "- Gemini 4 Argon i Gemini 3.8 Flash: ceny promocyjne obowiązujące 2026-10-18 (Argon: 50 % kredytu zwrotnego do 2026-11-30).",
          ""]
    if braki:
        L += ["## Braki", ""] + [f"- {b}" for b in braki] + [""]
    L += ["## Odpowiedzi z uwagami", "", "| Pytanie | System | Koszt USD | Uwagi |", "|---|---|---|---|"]
    # uwagi powtarzalne (opisane wyżej w „Uwagach do danych”) pomijamy, zostają nietypowe
    typowe = ("liczba wyszukań nieznana", "tokeny treści url_context")
    for w in wiersze:
        nietypowe = [u for u in w["uwagi"].split("; ") if u and not u.startswith(typowe)]
        if nietypowe:
            L.append(f"| {w['pytanie']} | {w['system']} | {fmt(w['koszt_usd'], dolna=w['dolna_granica'])} | {'; '.join(nietypowe)} |")
    L.append("")
    open(os.path.join(BENCH, f"koszt_{DATA}.md"), "w", encoding="utf-8").write("\n".join(L))

    # log: tylko liczniki
    print(f"odpowiedzi: {len(wiersze)}, systemy: {len(tabela)}, braki: {len(braki)}, "
          f"z kosztem n/d: {sum(1 for w in wiersze if w['koszt_usd'] is None)}, "
          f"dolna granica: {sum(1 for w in wiersze if w['dolna_granica'])}")


if __name__ == "__main__":
    main()
