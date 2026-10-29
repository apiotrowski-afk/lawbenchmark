# -*- coding: utf-8 -*-
"""Buduje statyczną stronę lawbenchmark.pl do katalogu site/ z danych repozytorium.

Źródła: reports/benchmark-02/src/dane.py (tabele liczone z kart), data/questions.jsonl (pytania), karty w cards/
(studia przypadku), PDF-y raportów. Strony (układ z 29.10.2026 po recenzji Astry — adresy zależne od edycji
pod /benchmark/02/, metodologia wspólna osobno, bez stron modeli i FAQ do czasu własnej analizy):
  /                          wyniki, klasy błędów, przykłady (skrót metodologii z odesłaniem)
  /metodologia               pełny opis oceny według specyfikacji (1.0.4; punktacja jak w 1.0.1)
  /benchmark/02/pytania      lista 10 pytań z wynikami per pytanie
  /benchmark/02/pytania/pNN  pytanie, pułapka, klucz, 16 wyników, klasy błędów
  /raporty                   raport Benchmark 02 i artykuł metodologiczny (streszczenia własne, DOI, BibTeX)
  /dane                      zbiór danych, kod, odtworzenie wyników, licencje (JSON-LD Dataset)
  /en                        krótka strona po angielsku (ustalenia, ograniczenia, odnośniki)
Firebase: cleanUrls + trailingSlash:false → katalog/index.html jest dostępny pod adresem bez ukośnika na końcu.
Użycie (z katalogu repo): python3 -I tools/build_site.py. Nic nie wysyła; wdrożenie: tools/deploy_hosting.py.
"""
import html
import importlib.util
import json
import os
import re
import shutil
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(REPO, "reports", "benchmark-02", "src")
SITE = os.path.join(REPO, "site")
BAZA = "https://lawbenchmark.pl"
DATA_KART, WERSJA_RAPORTU, DATA_RAPORTU = "25.10.2026", "1.1", "29.10.2026"
DATA_STRONY = "2026-10-29"          # lastmod nowych stron; strona główna ma własną datę niżej
REPO_URL = "https://github.com/apiotrowski-afk/lawbenchmark"   # publiczne repozytorium (odnośniki do kart, distribution w JSON-LD)
GA_ID = "G-JK6TSG2WN8"                        # identyfikator pomiaru GA4 (G-…); None = brak banera i brak analityki
HF_URL = "https://huggingface.co/datasets/LexAlphaLab/lawbenchmark-b02"   # zbiór na Hugging Face (bramka z automatyczną akceptacją)

sys.path.insert(0, SRC)
os.chdir(SRC)
spec = importlib.util.spec_from_file_location("dane", os.path.join(SRC, "dane.py"))
dane = importlib.util.module_from_spec(spec); spec.loader.exec_module(dane)
T, L = dane.TABELE, dane.LICZBY
E = html.escape


def pl(x, m=2):
    """Liczba z przecinkiem dziesiętnym, bez zbędnych zer (0,8 → '0,80' przy m=2; 170.698 → '170,70')."""
    return f"{x:.{m}f}".replace(".", ",")


def tabela_md(klucz):
    """Wiersze tabeli Markdown z dane.py jako listy komórek (bez nagłówka i separatora)."""
    return [[x.strip() for x in w.strip("|").split("|")] for w in T[klucz].strip().splitlines()[2:]]


# ---------- dane z tabeli wyników ----------
WIERSZE = []
for c in tabela_md("WYNIKI"):
    WIERSZE.append({"model": c[0], "war": c[1], "A": c[2], "B": c[3], "hal": int(c[4]), "pu": int(c[5]),
                    "koszt": c[6], "koszt_pu": c[7], "spr": c[8]})
MODELE = []
for r in WIERSZE:
    if r["model"] not in MODELE:
        MODELE.append(r["model"])
PARA = {m: {r["war"]: r for r in WIERSZE if r["model"] == m} for m in MODELE}
KLASY = tabela_md("KLASY")
PYT = dane.PYT
PYTANIA_T = {c[0]: c for c in tabela_md("PYTANIA")}
KLUCZE_T = {c[0]: c for c in tabela_md("KLUCZE")}
ANEKS_A = {c[0]: c[1:] for c in tabela_md("ANEKS_B_A")}   # "Sol W0" → [A% per pytanie]
ANEKS_H = {c[0]: c[1:] for c in tabela_md("ANEKS_B_H")}   # "Sol W0" → [✓ / – / klasy]
SEDZIOWIE_T = tabela_md("SEDZIOWIE")
ZRODLA_T = tabela_md("ZRODLA_W1")
KROTKA = {"GPT-6.1 Sol": "Sol", "GPT-6 Astra": "Astra", "GPT-5.6 Terra": "Terra", "Claude Opus 5.5": "Opus",
          "Claude Sonnet 5.5": "Sonnet", "Claude Haiku 5.5": "Haiku", "Gemini 3.8 Flash": "Flash", "Gemini 4 Argon": "Argon"}
SYSTEM_PLIK = {(n, w): s for s, n, _, w in dane.SYSTEMY}   # (model, warunek) → id systemu w nazwach plików

PYTANIA = {}
with open(os.path.join(REPO, "data", "questions.jsonl"), encoding="utf-8") as f:
    for linia in f:
        d = json.loads(linia); PYTANIA[d["id"]] = d

TYTUL = {"P01": "Próg wykroczenia przeciwko mieniu a płaca minimalna",
         "P04": "Zezwolenie na nabycie nieruchomości przez cudzoziemca: ostateczność czy prawomocność",
         "P05": "Doręczenia pism sądowych osobie fizycznej przez Portal Informacyjny",
         "P06": "Zażalenie na odrzucenie zażalenia przez sąd apelacyjny",
         "P07": "Zasadnicze powody rozstrzygnięcia a wniosek o uzasadnienie",
         "P08": "Głos wygenerowany przez AI a definicja deepfake w AI Act",
         "P09": "Ogólny zapis o „wszelkich polach eksploatacji” w umowie zlecenia",
         "P10": "Ogólny zapis o polach eksploatacji: wersja pytania z sugestią, że wystarcza",
         "P12": "Klauzula wykonalności przeciwko małżonkowi dłużnika",
         "P13": "Wstrzymanie wykonania nakazu z weksla a zabezpieczenie"}
TYP_OPIS = {"zamkniete": "zamknięte (tak / nie / zależy od…)", "obliczenie": "obliczenie (wynik liczbowy)",
            "weryfikacja": "weryfikacja cudzego twierdzenia"}
KL_OPIS = {"T": "treść, której w źródle nie ma", "W": "brzmienie z innej daty podane jako obowiązujące",
           "F": "źródło lub jednostka redakcyjna nie istnieje", "S": "zniekształcony identyfikator (sygnatura, numer)"}


# ---------- wykres par: wiersze HTML pogrupowane według dostawcy, kolumna „W0 → W1” (makieta Claude Design, 29.10.2026) ----------
# Kolory warunków stałe na całej stronie: W0 = obrys neutralny, W1 = wypełniony kolor marki. Kierunek zmiany podany tekstem,
# bez osobnego kodu oceny (bez przerywanej linii; rada Astry 29.10).
DOSTAWCA = {n: p for _, n, p, _ in dane.SYSTEMY}


def wykres_par(klucz, tytul, pod, wiecej, mniej):
    ticks = "".join(f'<span style="left:{i * 10}%">{i}</span>' for i in range(0, 11, 2))
    out = [f'<figure class="pw"><figcaption><b>{E(tytul)}</b><span>{E(pod)} · <i class="lg-w0"></i>bez narzędzi · <i class="lg-w1"></i>z wyszukiwaniem</span></figcaption>',
           f'<div class="pw-os" aria-hidden="true"><span>liczba odpowiedzi</span><div class="pw-ticks">{ticks}</div><span>W0 → W1</span></div>']
    for prov in dict.fromkeys(DOSTAWCA[m] for m in MODELE):
        out.append(f'<div class="pw-gr"><span class="pw-dost">{E(prov)}</span>')
        for m in [m for m in MODELE if DOSTAWCA[m] == prov]:
            a, b = PARA[m]["W0"][klucz], PARA[m]["W1"][klucz]
            if a == b:
                tag, tor = "bez zmian", f'<span class="pw-same" style="left:{a * 10}%"><i></i></span>'
            else:
                tag, lo, hi = (wiecej if b > a else mniej), min(a, b), max(a, b)
                tor = (f'<span class="pw-line" style="left:{lo * 10}%;width:{(hi - lo) * 10}%"></span>'
                       f'<span class="pw-w0" style="left:{a * 10}%"></span><span class="pw-w1" style="left:{b * 10}%"></span>')
            opis = f"{m}: {a} z 10 bez narzędzi, {b} z 10 z wyszukiwaniem"
            out.append(f'<div class="pw-r" data-m="{E(m)}"><span class="pw-m">{E(m)}</span><div class="pw-tor" role="img" aria-label="{E(opis)}">{tor}</div>'
                       f'<span class="pw-d"><b>{a} → {b}</b><small>{E(tag)}</small></span></div>')
        out.append("</div>")
    out.append("</figure>")
    return "".join(out)


WYKRES = ('<div class="wyk2">'
          + wykres_par("pu", "Poprawnie ugruntowane (z 10)", "więcej = lepiej", "więcej", "mniej")
          + wykres_par("hal", "Odpowiedzi z halucynacją (z 10)", "mniej = lepiej", "więcej", "mniej")
          + "</div>")
LEGENDA_W = ('<div class="legenda"><span><i class="lg-w0"></i>W0 · bez narzędzi</span><span><i class="lg-w1"></i>W1 · z wyszukiwaniem w internecie</span>'
             '<span><i class="lg-same"><i></i></i>ten sam wynik w obu warunkach</span><span>Kolejność według dostawców, nie według wyniku.</span></div>')

# ---------- tabela szczegółowa: tbody na model, kolumna „Model” przyklejona przy przewijaniu na telefonie ----------
tab = ['<table class="pary"><thead><tr><th>Model</th><th>Warunek</th><th class="num">Poprawnie ugruntowane <small>z 10</small></th>'
       '<th class="num">Halucynacje <small>z 10</small></th><th class="num">Blok A <small>%</small></th><th class="num">Blok B <small>%</small></th>'
       '<th class="num">Koszt serii <small>USD</small></th><th class="num">USD / poprawnie ugruntowaną</th><th class="num">Sprawdzone powołania</th></tr></thead>']
def _f(s):
    try:
        return float(str(s).replace(",", ".").replace("≥", "").strip())
    except ValueError:
        return -1.0
for idx, m in enumerate(MODELE):
    w1r = PARA[m]["W1"]
    tab.append(f'<tbody data-m="{E(m)}" data-idx="{idx}" data-pu="{w1r["pu"]}" data-hal="{w1r["hal"]}" data-a="{_f(w1r["A"])}">')
    for k, war in enumerate(("W0", "W1")):
        r = PARA[m][war]
        glowa = f'<th scope="rowgroup" rowspan="2" class="model">{E(m)}</th>' if k == 0 else ""
        tab.append(f'<tr>{glowa}<td><span class="war {war.lower()}">{war}</span></td>'
                   f'<td class="num ok"><span class="cb"><i style="width:{r["pu"] * 6}px"></i>{r["pu"]}</span></td><td class="num bad"><span class="cb"><i style="width:{r["hal"] * 6}px"></i>{r["hal"]}</span></td><td class="num">{E(r["A"])}</td><td class="num">{E(r["B"])}</td>'
                   f'<td class="num">{E(r["koszt"])}</td><td class="num">{E(r["koszt_pu"])}</td><td class="num">{E(r["spr"])}</td></tr>')
    tab.append("</tbody>")
tab.append("</table>")
TABELA = ('<div class="sortuj" role="group" aria-label="Sortowanie tabeli"><span class="eyb">Sortuj według wyniku z wyszukiwaniem (W1)</span>'
          '<button type="button" data-sort="idx" aria-pressed="true">kolejność raportu</button><button type="button" data-sort="pu" aria-pressed="false">poprawnie ugruntowane</button>'
          '<button type="button" data-sort="hal" aria-pressed="false">najmniej halucynacji</button><button type="button" data-sort="a" aria-pressed="false">blok A</button></div>'
          + '<div class="scroll">' + "\n".join(tab) + '</div>')

KLASA_ODP = {lit: [] for lit in KL_OPIS}
for m in MODELE:
    for w in ("W0", "W1"):
        for i, pid in enumerate(PYT):
            v = ANEKS_H[f"{KROTKA[m]} {w}"][i]
            if v not in ("✓", "–", "blokada"):
                for lit in v.split(","):
                    KLASA_ODP[lit.strip()].append((pid, m, w))
KLASY_HTML = ['<div class="kb">']
for k in KLASY:
    lit = k[0][0]
    if lit not in KL_OPIS:
        continue
    w0, w1, raz = int(k[1]), int(k[2]), int(k[3])
    lst = KLASA_ODP[lit]
    assert len(lst) == raz, (lit, len(lst), raz)
    chipy = "".join(f'<a class="chip" href="/benchmark/02/pytania/{pid.lower()}#wyniki">{pid} · {E(KROTKA[m])} · {w}</a>' for pid, m, w in sorted(lst))
    KLASY_HTML.append(
        f'<details class="kb-d"><summary class="kb-r"><div class="kb-n"><span class="znak">{lit}</span><div><b>{E(KL_OPIS[lit])}</b><span class="m">klasa {lit} · razem {raz} odpowiedzi</span></div></div>'
        f'<div class="kb-b"><div class="kb-l"><span>W0</span><span class="kb-t"><i class="w0" style="width:{w0 / 80 * 100:.1f}%"></i></span><b>{w0}/80</b></div>'
        f'<div class="kb-l"><span>W1</span><span class="kb-t"><i class="w1" style="width:{w1 / 80 * 100:.1f}%"></i></span><b>{w1}/80</b></div></div></summary>'
        f'<div class="kb-lst"><span class="eyb">{raz} odpowiedzi z klasą {lit} · pytanie · model · warunek</span><div class="chips">{chipy}</div></div></details>')
KLASY_HTML.append("</div>")
KLASY_HTML = "".join(KLASY_HTML)
KLASA = {k[0][0]: (int(k[1]), int(k[2])) for k in KLASY if k[0][0] in KL_OPIS}

# ---------- pliki ----------
os.makedirs(os.path.join(SITE, "reports"), exist_ok=True)
for _plik in ("og.png", "favicon.png", "apple-touch-icon.png"):  # grafiki z tools/render_assets.py (Playwright, krój strony)
    shutil.copy2(os.path.join(REPO, "assets", _plik), os.path.join(SITE, _plik))
for src, dst in [("reports/benchmark-02/lexalpha_lab_benchmark_02.pdf", "reports/lexalpha_lab_benchmark_02.pdf"),
                 ("reports/paper-v1.2/Piotrowski_2026_correctly_grounded_v1.2.pdf", "reports/Piotrowski_2026_correctly_grounded_v1.2.pdf")]:
    shutil.copy2(os.path.join(REPO, src), os.path.join(SITE, dst))

BIBTEX = """@techreport{piotrowski2026benchmark02,
  author = {Piotrowski, Adam and Koman, Andrzej},
  title  = {LexAlpha Lab · Benchmark 02 · pytania prawne},
  institution = {LexAlpha Lab, KTZR},
  year = {2026}, month = {10}, note = {wersja 1.1, 29 października 2026},
  url = {https://lawbenchmark.pl/}
}"""
BIBTEX_ART = """@techreport{piotrowski2026correctly,
  author = {Piotrowski, Adam},
  title  = {"Hallucination" Is Not Enough: Why Legal LLM Benchmarks Should Measure "Correctly Grounded"},
  institution = {LexAlpha Lab, KTZR},
  year = {2026}, month = {10}, note = {v1.2, 26 October 2026},
  doi = {10.5281/zenodo.23674794}
}"""

# ---------- wspólny szkielet ----------
CSS = """
/* Układ: witryna danych, nie dokument. Tekst bezszeryfowy (IBM Plex Sans), nagłówki szeryfowe (Literata) tylko dla h1/h2,
   liczby w IBM Plex Mono. Jeden kolor marki (kobalt), dwa kolory semantyczne (ugruntowane / halucynacja). Chłodne neutralne. */
:root{--brand:#1d4f8f;--brand-ink:#163d6e;--ok:#0f7a6c;--bad:#b23b2a;--bg:#f4f6f9;--surface:#ffffff;--ink:#141c26;--muted:#56626f;--line:#d9e0e8;--soft:#e9eef4;--okbg:#e4f3f0;--badbg:#f8e7e3;--on-brand:#ffffff;
  --serif:"Literata",Georgia,"Times New Roman",serif;--sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--brand:#8fb8ea;--brand-ink:#b7d2f3;--ok:#4fb8aa;--bad:#e3806f;--bg:#0f151c;--surface:#171f29;--ink:#e8edf2;--muted:#9aa6b3;--line:#2a3542;--soft:#1e2833;--okbg:#153530;--badbg:#3c221d;--on-brand:#0f151c;color-scheme:dark}}
:root[data-theme="dark"]{--brand:#8fb8ea;--brand-ink:#b7d2f3;--ok:#4fb8aa;--bad:#e3806f;--bg:#0f151c;--surface:#171f29;--ink:#e8edf2;--muted:#9aa6b3;--line:#2a3542;--soft:#1e2833;--okbg:#153530;--badbg:#3c221d;--on-brand:#0f151c;color-scheme:dark}
*{box-sizing:border-box;min-width:0} html{scroll-behavior:smooth;scroll-padding-top:70px} body{overflow-x:hidden}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--sans)}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2{font-family:var(--serif);font-weight:600;letter-spacing:-.01em;text-wrap:balance} h3{font-family:var(--sans)}
a{color:var(--brand);text-decoration-thickness:1px;text-underline-offset:2px} a:focus-visible,button:focus-visible{outline:2px solid var(--brand);outline-offset:2px}
code{font:0.9em var(--mono);background:var(--soft);padding:1px 5px;border-radius:3px;overflow-wrap:anywhere}
.num,.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
/* nawigacja */
nav{position:sticky;top:env(safe-area-inset-top,0px);background:color-mix(in srgb,var(--bg) 90%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);z-index:5}
nav .wrap{display:flex;align-items:center;gap:18px;height:58px;font:500 14px var(--sans)}
nav .logo{color:var(--ink);text-decoration:none;display:flex;flex-direction:column;line-height:1.1} nav .logo b{font-family:var(--serif);font-size:18px;font-weight:600;letter-spacing:-.01em}
nav .logo small{color:var(--muted);font:500 11px var(--sans);letter-spacing:.04em;text-transform:uppercase;margin-top:2px} nav .sp{flex:1}
nav a:not(.logo){color:var(--muted);text-decoration:none;padding:6px 0;border-bottom:2px solid transparent} nav a:not(.logo):hover{color:var(--ink)} nav a.tu{color:var(--ink);border-bottom-color:var(--brand)}
@media (max-width:860px){nav .wrap:first-child a:not(.logo){display:none}}
nav .wrap.nav-m{display:none} @media (max-width:860px){nav .wrap.nav-m{display:flex;height:auto;gap:18px;overflow-x:auto;white-space:nowrap;padding-block:0 8px;font:500 14px var(--sans);scrollbar-width:none} nav .nav-m::-webkit-scrollbar{display:none} nav .nav-m a{flex:none;color:var(--muted);text-decoration:none;padding:4px 0;border-bottom:2px solid transparent} nav .nav-m a.tu{color:var(--ink);border-bottom-color:var(--brand)} html{scroll-padding-top:110px}}
nav button{background:none;border:1px solid var(--line);color:var(--muted);border-radius:6px;padding:4px 10px;font:inherit;cursor:pointer}
.okr{font:13px var(--sans);color:var(--muted);padding-top:16px} .okr a{color:var(--muted)} .okr span{margin:0 7px}
/* hero strony głównej */
.hero{padding:48px 0 28px;border-bottom:1px solid var(--line);background:var(--surface)}
.hero .wrap{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:40px;align-items:start} @media (max-width:900px){.hero .wrap{grid-template-columns:1fr;gap:24px}}
.hero h1{font-size:clamp(30px,4.2vw,44px);line-height:1.12;margin:0 0 14px;max-width:16em}
.hero p.lead{font-size:18px;color:var(--muted);max-width:34em;margin:0 0 18px}
.zakres{display:flex;flex-wrap:wrap;gap:6px 18px;font:500 14px var(--sans);color:var(--muted);margin:0 0 14px} .zakres b{color:var(--ink);font-weight:600}
.meta{font:14px var(--sans);color:var(--muted);margin:0 0 18px}
.btn{display:inline-block;border-radius:6px;padding:9px 14px;font:600 14px var(--sans);text-decoration:none;margin:0 8px 8px 0;border:1px solid var(--line);color:var(--ink);background:var(--surface)}
.btn.p{background:var(--brand);color:var(--on-brand);border-color:var(--brand)} .btn:hover{border-color:var(--brand)}
.uwaga{font:14px/1.55 var(--sans);color:var(--muted);max-width:44em;border-left:3px solid var(--line);padding-left:12px;margin-top:10px}
.stat{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.stat div{background:var(--surface);padding:14px 16px} .stat .l{display:block;font:500 12px var(--sans);letter-spacing:.03em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.stat .v{font:600 30px/1 var(--sans);font-variant-numeric:tabular-nums;letter-spacing:-.01em} .stat .v small{font-size:15px;color:var(--muted);margin-left:4px} .stat .v .ok{color:var(--ok)} .stat .v .bad{color:var(--bad)}
.stat .d{display:block;font:14px/1.4 var(--sans);color:var(--muted);margin-top:6px}
/* panel wyników w hero */
.hw{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:20px 22px;display:flex;flex-direction:column;gap:18px}
.hw figcaption{font:500 12px var(--sans);letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.hw-m{display:flex;flex-direction:column;gap:8px} .hw-t{font:600 16px var(--sans)}
.hw-r{display:grid;grid-template-columns:112px minmax(0,1fr) 34px;gap:10px;align-items:center;font:14px var(--sans);color:var(--muted)}
.hw-r b{font:600 20px var(--sans);font-variant-numeric:tabular-nums;color:var(--ink);text-align:right}
.hw-tor{height:14px;background:var(--soft);border-radius:4px;overflow:hidden} .hw-tor i{display:block;height:14px;border-radius:4px} .hw-tor i.w0{background:var(--muted)} .hw-tor i.w1{background:var(--brand)}
.hw-s{display:flex;flex-wrap:wrap;gap:6px 16px;border-top:1px solid var(--line);padding-top:14px;font:13.5px var(--sans);color:var(--muted)} .hw-s b{color:var(--ink);font-weight:600}
.leg16{font:13px var(--sans);color:var(--muted);margin:4px 0 0} .leg16 i{display:inline-block;width:11px;height:11px;border-radius:2px;vertical-align:-1px;margin:0 5px 0 10px} .leg16 i:first-child{margin-left:0}
/* nagłówki podstron */
.pod-hero{padding:30px 0 10px;border-bottom:1px solid var(--line);background:var(--surface);margin-bottom:8px}
.pod-hero h1{font-size:clamp(26px,3.4vw,38px);line-height:1.15;margin:0 0 10px;max-width:24em}
.pod-hero p.lead{font-size:17px;color:var(--muted);max-width:46em;margin:0 0 10px}
.pod-hero .meta{margin-bottom:14px}
/* sekcje */
section{padding:36px 0 6px} h2{font-size:26px;line-height:1.2;margin:0 0 6px} .pod{color:var(--muted);margin:0 0 18px;max-width:46em}
article section{padding:26px 0 4px} article h2{font-size:24px;margin-top:6px} article h3{font:600 17px/1.3 var(--sans);margin:20px 0 6px}
article p,article li{max-width:46em;font-size:16.5px} article ul,article ol{padding-left:22px} article li{margin:4px 0}
h2 a.kot,h3 a.kot{color:var(--line);text-decoration:none;font-weight:400;margin-left:8px} h2:hover a.kot,h3:hover a.kot{color:var(--muted)}
.meto{display:grid;grid-template-columns:220px minmax(0,1fr);gap:40px;align-items:start} @media (max-width:900px){.meto{grid-template-columns:1fr}}
.meto aside{position:sticky;top:76px;font:13.5px/1.45 var(--sans);border-left:1px solid var(--line);padding-left:14px} .meto aside a{display:block;color:var(--muted);text-decoration:none;padding:4px 0} .meto aside a:hover{color:var(--ink)}
.meto aside .n{font:500 11px var(--sans);letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin:0 0 6px} @media (max-width:900px){.meto aside{display:none}}
.spis{font:14px var(--sans);display:flex;flex-wrap:wrap;gap:4px 16px;margin:12px 0 4px} .spis a{text-decoration:none} @media (min-width:901px){.spis{display:none}}
.dwa{display:grid;grid-template-columns:1fr 1fr;gap:16px} @media (max-width:760px){.dwa{grid-template-columns:1fr}}
.blok{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:18px 20px}
.blok h3{margin:0 0 6px;font:600 18px var(--sans)} .blok p{margin:0;color:var(--muted);font-size:15.5px}
.blok.ok{border-top:3px solid var(--ok)} .blok.bad{border-top:3px solid var(--bad)} .blok.ok h3{color:var(--ok)} .blok.bad h3{color:var(--bad)}
.teza{font:500 19px/1.45 var(--serif);margin:18px 0 0;max-width:40em}
.wyk{gap:12px} .wykres{width:100%;height:auto;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:10px}
.legenda{display:flex;gap:8px 22px;flex-wrap:wrap;align-items:center;font:14px var(--sans);color:var(--muted);margin:12px 0 0}
.legenda i{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;margin-right:6px;border:2px solid var(--muted)} .legenda i.f{background:var(--muted)}
table.pary,table.t{width:100%;border-collapse:collapse;font:14px/1.35 var(--sans);background:var(--surface);border:1px solid var(--line);border-radius:8px;overflow:hidden;font-variant-numeric:tabular-nums}
.pary th,.pary td,.t th,.t td{padding:9px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top} .pary th,.t th{background:var(--soft);font-weight:600;font-size:13px} th small{font-weight:500;color:var(--muted)}
.pary th,.pary td{white-space:nowrap} .t.zw td,.t.zw th{white-space:nowrap}
.pary .num,.t .num{text-align:right;font-family:var(--mono);white-space:nowrap} .pary tr.p0 td{border-bottom:0} .pary td.model,.t td.model{font-weight:600} .pary tr.p1 td{padding-top:2px}
.war{display:inline-block;font:600 11px var(--sans);padding:2px 6px;border-radius:4px;border:1px solid var(--line);color:var(--muted)} .war.w1{background:var(--brand);color:var(--on-brand);border-color:var(--brand)}
.ok{color:var(--ok)} .bad{color:var(--bad)} td.ok,td.bad{font-weight:600}
.scroll{overflow-x:auto;margin:0 -16px;padding:0 16px}
.pary th.model{position:sticky;left:0;z-index:1;background:var(--surface);font:600 14px var(--sans);vertical-align:top;border-right:1px solid var(--line)}
.pary thead th:first-child{position:sticky;left:0;z-index:2;background:var(--soft)} .pary tbody:nth-child(odd) td,.pary tbody:nth-child(odd) th.model{background:var(--bg)}
.pary tbody tr:first-child td{border-bottom:0} .przesun{display:none;font:14px var(--sans);color:var(--muted);margin:0 0 8px} @media (max-width:760px){.przesun{display:block}}
/* wykres par */
.wyk2{display:grid;grid-template-columns:1fr 1fr;gap:20px} @media (max-width:960px){.wyk2{grid-template-columns:1fr}}
.pw{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:16px 18px}
.pw figcaption{display:flex;flex-direction:column;gap:2px;margin-bottom:10px} .pw figcaption b{font:600 16px var(--sans)} .pw figcaption span{font:14px var(--sans);color:var(--muted)}
.pw-os,.pw-r{display:grid;grid-template-columns:132px minmax(0,1fr) 128px;gap:12px;align-items:center}
@media (max-width:520px){.pw-os,.pw-r{grid-template-columns:92px minmax(0,1fr) 96px;gap:8px} .pw-m{font-size:13px!important}}
.pw-os{font:12px var(--mono);color:var(--muted)} .pw-ticks{position:relative;height:16px;margin:0 9px} .pw-ticks span{position:absolute;transform:translateX(-50%)}
.pw-gr{border-top:1px solid var(--line);margin-top:6px;padding-top:2px} .pw-dost{display:block;font:500 11px var(--sans);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:5px 0 2px}
.pw-r{min-height:38px} .pw-m{font:500 14px var(--sans)}
.pw-tor{position:relative;height:28px;margin:0 9px;background-image:linear-gradient(to right,var(--line) 1px,transparent 1px);background-size:20% 100%;border-right:1px solid var(--line)}
.pw-line{position:absolute;top:50%;height:0;border-top:2px solid var(--muted);opacity:.5}
.pw-w0,.pw-w1,.pw-same{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:50%;box-sizing:border-box}
.pw-w0{width:14px;height:14px;border:2.5px solid var(--muted);background:var(--surface)} .pw-w1{width:14px;height:14px;background:var(--brand)}
.pw-same{width:18px;height:18px;border:2.5px solid var(--muted);background:var(--surface);display:grid;place-items:center} .pw-same i{width:8px;height:8px;border-radius:50%;background:var(--brand)}
.pw-d{display:flex;flex-direction:column;line-height:1.25} .pw-d b{font:600 14px var(--mono)} .pw-d small{font:13px var(--sans);color:var(--muted)}
.lg-w0,.lg-w1,.lg-same{display:inline-block;width:13px;height:13px;border-radius:50%;vertical-align:-2px;margin-right:7px;box-sizing:border-box}
.lg-w0{border:2.5px solid var(--muted);background:var(--surface)} .lg-w1{background:var(--brand)}
.legenda i.lg-w0{border:2.5px solid var(--muted);background:var(--surface);width:13px;height:13px} .legenda i.lg-w1{border:0;background:var(--brand);width:13px;height:13px}
.legenda i.lg-same{width:17px;height:17px;border:2.5px solid var(--muted);background:var(--surface);display:inline-grid;place-items:center} .legenda i.lg-same i{width:7px;height:7px;margin:0;border:0;background:var(--brand)} .lg-same{width:17px;height:17px;border:2.5px solid var(--muted);background:var(--surface);display:inline-grid;place-items:center;vertical-align:-4px} .lg-same i{width:7px;height:7px;border-radius:50%;background:var(--brand)}
.stat.wyn{grid-template-columns:repeat(2,minmax(0,1fr));max-width:760px;margin:0 0 14px} @media (max-width:520px){.stat.wyn{grid-template-columns:1fr}}
.wer{font:14px/1.55 var(--sans);color:var(--ink);max-width:52em;margin:0 0 22px;padding:12px 16px;background:var(--soft);border-radius:8px}
/* klasy błędu: paski */
.kb{border-top:1px solid var(--line)} .kb-r{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:12px 28px;align-items:center;padding:16px 0;border-bottom:1px solid var(--line)} @media (max-width:760px){.kb-r{grid-template-columns:1fr}}
.kb-n{display:flex;gap:14px;align-items:center} .kb-n b{display:block;font:600 15.5px var(--sans)} .kb-n .m{display:block;font:14px var(--sans);color:var(--muted)}
.kb-b{display:flex;flex-direction:column;gap:8px} .kb-l{display:grid;grid-template-columns:28px minmax(0,1fr) 56px;gap:10px;align-items:center;font:14px var(--sans);color:var(--muted)} .kb-l b{font:600 14px var(--mono);color:var(--ink);text-align:right}
.kb-t{height:12px;background:var(--soft);border-radius:3px;overflow:hidden} .kb-t i{display:block;height:12px;border-radius:3px} .kb-t i.w0{background:var(--muted)} .kb-t i.w1{background:var(--brand)}
/* przykłady z kart */
.prz{display:flex;flex-direction:column;gap:14px;margin:0 0 36px} .prz .eyb{font:500 12px var(--sans);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.prz h3{margin:0;font:600 22px/1.25 var(--serif)} .pbox{background:var(--soft);border-radius:8px;padding:14px 18px;max-width:52em;font-size:16px}
.prz .dw{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:16px}
.kp{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:18px 20px;display:flex;flex-direction:column;gap:12px}
.kp .wn{display:flex;align-items:center;gap:8px;font:600 14px var(--sans)} .kp blockquote{margin:0;font:400 18px/1.5 var(--serif)}
.chips{display:flex;flex-wrap:wrap;gap:6px} .chip{font:500 13.5px var(--sans);padding:4px 10px;border-radius:999px;background:var(--soft);color:var(--ink)} .chip.ok{background:var(--okbg);color:var(--ok)} .chip.bad{background:var(--badbg);color:var(--bad)}
.prz .wniosek{margin:0;max-width:52em}
.klasy{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px} .klasa{display:flex;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:14px}
.znak{flex:none;width:36px;height:36px;border:2px solid var(--ink);border-radius:6px;display:grid;place-items:center;font:600 16px var(--mono)}
.klasa b{display:block;font:600 14.5px var(--sans)} .klasa .m b{display:inline;font-size:13px} .klasa .m{display:block;font:14px var(--sans);color:var(--muted);margin-top:4px}
.przyp{display:grid;grid-template-columns:1fr 1fr;gap:16px} @media (max-width:760px){.przyp{grid-template-columns:1fr}}
.przyp .blok h3{font-size:16px} .przyp .blok p{color:var(--ink)} .q{border-left:3px solid var(--line);padding:2px 0 2px 12px;margin:10px 0;color:var(--muted);font-style:italic;font-family:var(--serif)}
.ocena{font:14px var(--sans);color:var(--muted);margin-top:8px}
.lista{columns:2;column-gap:40px;max-width:1000px} @media (max-width:760px){.lista{columns:1}} .lista p{break-inside:avoid;margin:0 0 12px;font-size:15.5px} .lista b{font-family:var(--sans)}
pre{white-space:pre-wrap;word-break:break-word;background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:12px 14px;font:13px/1.45 var(--mono);overflow-x:auto}
blockquote.pyt{margin:14px 0;padding:14px 18px;background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--brand);border-radius:6px;font:400 18px/1.5 var(--serif)}
.fakty{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden;font:14px var(--sans);margin:14px 0}
.fakty div{background:var(--surface);padding:10px 12px;font-family:var(--mono)} .fakty b{display:block;font:500 12px var(--sans);color:var(--muted);margin-bottom:3px}
/* siatka 8 modeli × 2 warunki */
.s16{display:block;width:100%;max-width:300px;height:auto} .s16 text{font:500 9px var(--sans);fill:var(--muted)}
.siatka-pyt{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px} .siatka-pyt a{display:block;color:inherit;text-decoration:none;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:14px 16px} .siatka-pyt .s16{max-width:230px;margin:10px 0 2px}
.siatka-pyt a:hover{border-color:var(--brand)} .siatka-pyt .id{font:500 11px var(--sans);letter-spacing:.04em;text-transform:uppercase;color:var(--muted)} .siatka-pyt h2{margin:3px 0 6px;font:600 16px/1.3 var(--sans)}
.siatka-pyt .st{display:block;font:14px/1.5 var(--sans);color:var(--muted)} .siatka-pyt .st b{color:var(--ink);font-family:var(--mono);font-weight:500}
.kl{display:inline-block;font:600 12px var(--mono);padding:1px 6px;border-radius:4px;border:1px solid var(--line);margin-right:3px} .kl.ok{border-color:var(--ok);color:var(--ok);background:var(--okbg)} .kl.bl{border-color:var(--bad);color:var(--bad);background:var(--badbg)}
/* stopka */
footer{margin-top:56px;border-top:1px solid var(--line);background:var(--surface);padding:28px 0 44px;font:14px/1.55 var(--sans);color:var(--muted)}
footer .kol{display:grid;grid-template-columns:2fr 1fr 1fr;gap:28px} @media (max-width:760px){footer .kol{grid-template-columns:1fr}}
footer h4{margin:0 0 8px;font:500 11px var(--sans);letter-spacing:.05em;text-transform:uppercase;color:var(--muted)} footer a{color:var(--ink)} footer p{margin:0 0 8px}
footer .marki{display:flex;gap:18px;flex-wrap:wrap;margin:10px 0 0;font-weight:500} footer .marki a{text-decoration:none;border:1px solid var(--line);border-radius:6px;padding:6px 10px}
.rz{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line)} @media (max-width:760px){.rz{grid-template-columns:1fr}}
.rz div{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:6px 24px;padding:18px 0;border-bottom:1px solid var(--line)} .rz div:nth-child(odd){padding-right:28px} .rz div:nth-child(even){padding-left:28px;border-left:1px solid var(--line)}
@media (max-width:760px){.rz div{grid-template-columns:1fr} .rz div:nth-child(odd),.rz div:nth-child(even){padding-left:0;padding-right:0;border-left:0}}
.rz b{font:600 16px var(--sans)} .rz span{font-size:15px;color:var(--muted)}
.mat{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border-top:1px solid var(--line);border-left:1px solid var(--line)} @media (max-width:900px){.mat{grid-template-columns:1fr 1fr}} @media (max-width:560px){.mat{grid-template-columns:1fr}}
.mat a{display:flex;flex-direction:column;gap:6px;padding:20px 20px 22px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);color:var(--ink);text-decoration:none;background:var(--surface)}
.mat a:hover{background:var(--panel)} .mat b{font:600 17px/1.3 var(--sans)} .mat a > span:last-child{font-size:14.5px;color:var(--muted)} .mat .eyb{margin:0}
.sortuj{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:0 0 12px} .sortuj .eyb{margin:0 8px 0 0}
.sortuj button{font:500 13px var(--sans);color:var(--muted);background:transparent;border:1px solid var(--line);border-radius:999px;padding:5px 12px;cursor:pointer}
.sortuj button:hover{color:var(--ink);border-color:var(--ink)} .sortuj button[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.pary tbody.hl td,.pary tbody.hl th.model{background:color-mix(in srgb,var(--brand) 9%,var(--surface))!important} .pw-r.hl{background:color-mix(in srgb,var(--brand) 9%,transparent)} .pw-r{transition:background .12s}
.kb-d{border-bottom:1px solid var(--line)} .kb-d summary{list-style:none;cursor:pointer;border-bottom:0} .kb-d summary::-webkit-details-marker{display:none}
.kb-d summary .kb-n::after{content:"+";font:500 18px var(--mono);color:var(--muted);margin-left:auto;padding-left:12px} .kb-d[open] summary .kb-n::after{content:"−"} .kb-d summary:hover .kb-n b{text-decoration:underline}
.kb-n{flex:1} .kb-lst{padding:0 0 18px} .kb-lst .chips{gap:6px} .kb-lst .chip{text-decoration:none;color:var(--ink);background:var(--soft)} .kb-lst .chip:hover{background:var(--ink);color:var(--bg)}
.siatka-pyt a[hidden]{display:none} .s16 a rect{cursor:pointer} .s16 a:hover rect{stroke:var(--ink);stroke-width:2}
.zgoda{position:fixed;left:0;right:0;bottom:0;z-index:20;background:var(--surface);border-top:1px solid var(--line);box-shadow:0 -6px 24px rgba(0,0,0,.08);
padding:16px max(16px,env(safe-area-inset-right,0px)) calc(16px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:center}
.zgoda[hidden]{display:none} [hidden]{display:none!important}
.zgoda p{margin:0;max-width:46em;font-size:14.5px} .zgoda div{display:flex;gap:8px} .zgoda .btn{margin:0}
/* ===== STYL v3 (29.10.2026): oprawa „instrumentu” zamiast dokumentu. Wzorce: legalbenchmarks.ai (grotesk, powietrze, pigułki),
   vals.ai (rama kolumny, etykiety monospace, tabela jako rdzeń). Szeryf tylko w H1; reszta Hanken Grotesk; etykiety IBM Plex Mono. ===== */
:root{--bg:#ffffff;--surface:#ffffff;--ink:#17171a;--muted:#5d5f66;--line:#e3e3e6;--soft:#f4f4f5;--panel:#fafafa;--brand:#1d4f8f;--on-brand:#ffffff;
  --sans:"Hanken Grotesk",system-ui,-apple-system,"Segoe UI",sans-serif;--frame:#e3e3e6}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0d0e10;--surface:#111215;--ink:#ececef;--muted:#a3a4ab;--line:#26272b;--soft:#18191c;--panel:#141518;--brand:#8fb8ea;--on-brand:#0d0e10;--frame:#26272b;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0d0e10;--surface:#111215;--ink:#ececef;--muted:#a3a4ab;--line:#26272b;--soft:#18191c;--panel:#141518;--brand:#8fb8ea;--on-brand:#0d0e10;--frame:#26272b;color-scheme:dark}
body{font:16px/1.6 var(--sans);background:var(--bg)}
@media (min-width:1214px){body{background-image:linear-gradient(to right,transparent calc(50% - 591px),var(--frame) calc(50% - 591px),var(--frame) calc(50% - 590px),transparent calc(50% - 590px),transparent calc(50% + 590px),var(--frame) calc(50% + 590px),var(--frame) calc(50% + 591px),transparent calc(50% + 591px))}}
h1{font-family:var(--serif);font-weight:600;letter-spacing:-.015em}
h2,h3{font-family:var(--sans);font-weight:600;letter-spacing:-.015em} h2{font-size:28px;line-height:1.2} article h2{font-size:24px}
.eyb{display:block;font:500 11.5px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
.tag{display:inline-block;font:500 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--ink);border:1px solid var(--line);padding:3px 8px;margin:0 0 14px}
.tag i{display:inline-block;width:7px;height:7px;background:var(--brand);margin-right:7px;vertical-align:1px}
nav{background:color-mix(in srgb,var(--bg) 92%,transparent)} nav .logo b{font-family:var(--sans);font-weight:700;font-size:17px;letter-spacing:-.02em}
nav .logo small{font:500 10.5px var(--mono);letter-spacing:.07em} nav a:not(.logo){font-weight:500}
nav button{border-radius:999px}
.okr{font:500 11.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;padding-top:22px} .okr a{text-decoration:none}
.meta{font:12.5px/1.6 var(--mono);color:var(--muted)}
.hero{background:transparent;border-bottom:0;padding:64px 0 48px} .hero h1{font-size:clamp(32px,4.4vw,50px);font-weight:500;line-height:1.08}
.hero p.lead{font-size:19px;line-height:1.55;color:var(--ink);opacity:.86}
.pod-hero{background:transparent;border-bottom:0;padding:28px 0 6px;margin:0} .pod-hero h1{font-weight:500}
.btn{border-radius:999px;padding:10px 18px;font:600 14px var(--sans);border:1px solid var(--line);background:transparent}
.btn.p{background:var(--ink);color:var(--bg);border-color:var(--ink)} .btn:hover{border-color:var(--ink)}
.uwaga{border-left:0;padding-left:0;font:13.5px/1.6 var(--sans)}
.wer{background:transparent;border-top:1px solid var(--line);border-bottom:1px solid var(--line);border-radius:0;padding:14px 0}
body > section > .wrap{border-top:1px solid var(--line);padding-top:44px} body > section{padding:0 0 44px}
body > section h2{margin-bottom:8px} .pod{font-size:16.5px;max-width:44em}
.blok{border:0;border-top:1px solid var(--line);border-radius:0;padding:16px 0 0;background:transparent}
.blok.ok,.blok.bad{border-top:2px solid var(--line)} .blok.ok{border-top-color:var(--ok)} .blok.bad{border-top-color:var(--bad)} .blok h3{font-size:17px}
.teza{font:500 19px/1.5 var(--sans);letter-spacing:-.01em}
.hw,.pw,.kp,.siatka-pyt a,.klasa,.fakty,table.pary,table.t,blockquote.pyt,.wykres,pre{border-radius:0}
.hw{background:var(--panel);padding:0;gap:0} .hw figcaption{padding:12px 18px;border-bottom:1px solid var(--line);font:500 11.5px var(--mono);letter-spacing:.07em}
.hw-m{padding:16px 18px 4px} .hw-s{margin:12px 0 0;padding:12px 18px;font:12.5px var(--mono)} .hw-r b{font-family:var(--sans)}
.hw-tor,.kb-t,.pw-tor{border-radius:0} .hw-tor i,.kb-t i{border-radius:0}
.pw{background:var(--panel)} .pw figcaption b{font-size:15px} .pw-dost{font-family:var(--mono)}
table.pary,table.t{border:1px solid var(--line)} .pary th,.t th{background:var(--panel);font:500 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.pary th small,.t th small{font:inherit;text-transform:none;letter-spacing:0}
.pary th.model{font:600 14px var(--sans);text-transform:none;letter-spacing:0;color:var(--ink);background:var(--surface)} .pary tbody:nth-child(odd) th.model,.pary tbody:nth-child(odd) td{background:var(--panel)}
.cb{display:inline-flex;align-items:center;gap:8px;justify-content:flex-end;width:100%} .cb i{display:inline-block;height:8px;background:currentColor;opacity:.85;vertical-align:middle}
.war{border-radius:0;font-family:var(--mono)}
.kb{border-top:1px solid var(--line)} .znak{border-radius:0;border-width:1.5px}
.kp{background:var(--panel)} .pbox{background:transparent;border-left:2px solid var(--brand);border-radius:0;padding:4px 0 4px 16px}
.chip{border-radius:0;font-family:var(--mono);font-size:12px;letter-spacing:.02em}
.prz h3{font-family:var(--sans);font-weight:600}
blockquote.pyt{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--brand)}
.siatka-pyt a{background:var(--panel)} .siatka-pyt h2{font-family:var(--sans)}
footer{background:transparent} footer h4{font-family:var(--mono)} footer .marki a{border-radius:999px}
.meto aside{font-family:var(--sans)} .meto aside .n{font-family:var(--mono)}
/* ===== poprawki po uwagach ChatGPT (29.10.2026): czytelność drobnego tekstu, panel, wykresy, hierarchia tabeli ===== */
.eyb{font-size:12.5px;letter-spacing:.06em;color:color-mix(in srgb,var(--muted) 70%,var(--ink))} .tag{font-size:12px}
.meta{font:14px/1.6 var(--sans);color:color-mix(in srgb,var(--muted) 75%,var(--ink))}
.hero h1{font-size:clamp(30px,3.8vw,44px)} .hero .wrap{grid-template-columns:minmax(0,6fr) minmax(0,5fr)} @media (max-width:900px){.hero .wrap{grid-template-columns:1fr}}
.hw figcaption{font-size:12.5px} .hw-r{font-size:15px;color:var(--ink)} .hw-r b small{font:500 13px var(--sans);color:var(--muted);margin-left:2px} .hw-r{grid-template-columns:120px minmax(0,1fr) 62px}
.hw-4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--line);margin-top:14px} @media (max-width:520px){.hw-4{grid-template-columns:1fr 1fr}}
.hw-4 div{padding:14px 18px;border-right:1px solid var(--line);display:flex;flex-direction:column;gap:2px} .hw-4 div:last-child{border-right:0} @media (max-width:520px){.hw-4 div:nth-child(2){border-right:0} .hw-4 div:nth-child(-n+2){border-bottom:1px solid var(--line)}}
.hw-4 b{font:600 22px/1.1 var(--sans);font-variant-numeric:tabular-nums} .hw-4 span{font-size:13px;color:var(--muted);line-height:1.35}
.pw figcaption span{font-size:14px;color:var(--ink);opacity:.8} .pw figcaption i{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;margin:0 5px 0 2px;box-sizing:border-box}
.pw figcaption i.lg-w0{border:2px solid var(--muted);background:var(--surface)} .pw figcaption i.lg-w1{background:var(--brand)}
.pw-os{font-size:12.5px;color:var(--ink);opacity:.75} .pw-tor{background-image:linear-gradient(to right,color-mix(in srgb,var(--muted) 35%,transparent) 1px,transparent 1px)}
.legenda{font-size:14px;color:var(--ink);opacity:.85;margin:0 0 12px}
.pary td{font-size:13px;color:var(--muted)} .pary td:nth-child(2),.pary td:nth-child(3),.pary tr:not(:first-child) td:nth-child(1),.pary tr:not(:first-child) td:nth-child(2){font-size:15px;font-weight:600}
.pary tr:first-child td:nth-child(3),.pary tr:first-child td:nth-child(4),.pary tr:not(:first-child) td:nth-child(2),.pary tr:not(:first-child) td:nth-child(3){font-size:15px;font-weight:600}
.pary thead th:nth-child(1),.pary thead th:nth-child(3),.pary thead th:nth-child(4){color:var(--ink)} .pary tbody{border-bottom:2px solid var(--line)} .pary tbody tr:first-child td{border-bottom:1px dashed var(--line)}
.mat a.wyr{box-shadow:inset 0 3px 0 var(--brand)} .mat a.wyr b{color:var(--brand)}
"""
SKRYPT = """<script>
(function(){var r=document.documentElement,b=document.getElementById('motyw');try{var z=localStorage.getItem('motyw');if(z)r.setAttribute('data-theme',z);}catch(e){}
b.addEventListener('click',function(){var c=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');var n=c==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('motyw',n);}catch(e){}});})();
(function(){var t=document.querySelector('table.pary');var g=document.querySelector('.sortuj:not([data-filtr])');
if(t&&g){g.addEventListener('click',function(e){var k=e.target.closest('button');if(!k)return;var s=k.dataset.sort;
var tb=[].slice.call(t.tBodies);tb.sort(function(a,b){var x=parseFloat(a.dataset[s]),y=parseFloat(b.dataset[s]);return s==='hal'||s==='idx'?x-y:y-x;});
tb.forEach(function(x){t.appendChild(x);});if(window.gtag)gtag('event','sortowanie_tabeli',{kryterium:s});[].forEach.call(g.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===k?'true':'false');});});}
var w=document.querySelectorAll('[data-m]');[].forEach.call(w,function(el){el.addEventListener('mouseenter',function(){var m=el.dataset.m;[].forEach.call(w,function(x){x.classList.toggle('hl',x.dataset.m===m);});});
el.addEventListener('mouseleave',function(){[].forEach.call(w,function(x){x.classList.remove('hl');});});});
var f=document.querySelector('.sortuj[data-filtr]');if(f){var l=document.querySelector(f.dataset.filtr);f.addEventListener('click',function(e){var k=e.target.closest('button');if(!k)return;var v=k.dataset.f;
[].forEach.call(l.children,function(a){if(v==='*'){a.hidden=false;return;}var p=v.split('=');a.hidden=a.dataset[p[0]]!==p[1];});if(window.gtag)gtag('event','filtr_pytan',{filtr:v});
[].forEach.call(f.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===k?'true':'false');});});}
[].forEach.call(document.querySelectorAll('details.kb-d'),function(d){d.addEventListener('toggle',function(){if(d.open&&window.gtag)gtag('event','klasa_bledu',{klasa:(d.querySelector('.znak')||{}).textContent});});});})();
</script>"""
NAV = [("/#wyniki", "Wyniki"), ("/benchmark/02/pytania", "Pytania"), ("/benchmark/01", "Kazus"), ("/metodologia", "Metodologia"), ("/raporty", "Raporty"), ("/dane", "Dane"), ("/wspolpraca", "Współpraca"), ("/en", "EN")]
STOPKA_PL = ('<div class="kol"><div><h4>O projekcie</h4><p><b>LawBenchmark.pl</b> prowadzi <b>LexAlpha Lab</b>, wspólna inicjatywa badawcza kancelarii '
             '<a href="https://www.ktzr.pl/">KTZR</a> (Gdańsk) i spółki <a href="https://lexalpha.pl/">LexAlpha Sp. z o.o.</a> (Warszawa). '
             'Autorzy: Adam Piotrowski (radca prawny, partner KTZR), Andrzej Koman (CEO LexAlpha). Badanie finansowane ze środków własnych obu podmiotów; żaden dostawca modeli nie uczestniczył w jego przygotowaniu. '
             'Benchmark 02 nie obejmuje produktów LexAlpha ani KTZR; wyników produktów ocenianych w pilotażu Benchmark 01 nie publikujemy. Benchmark nie jest poradą prawną.</p>'
             '<div class="marki"><a href="https://www.ktzr.pl/">ktzr.pl</a><a href="https://lexalpha.pl/">lexalpha.pl</a><a href="https://github.com/apiotrowski-afk/lawbenchmark">GitHub</a></div></div>'
             '<div><h4>Strony</h4><p><a href="/#wyniki">Wyniki</a><br><a href="/benchmark/02/pytania">Dziesięć pytań</a><br><a href="/benchmark/01">Kazus SKD (pilotaż)</a><br><a href="/metodologia">Metodologia</a><br><a href="/raporty">Raporty</a><br><a href="/dane">Dane i kod</a><br><a href="/wspolpraca">Współpraca</a><br><a href="/dolacz">Dołącz do nas</a><br><a href="/en">English</a></p></div>'
             '<div><h4>Licencja i kontakt</h4><p>Teksty, klucze i karty: CC BY 4.0. Kod: MIT. Cytuj jako „LexAlpha Lab, LawBenchmark.pl”.</p><p>a.piotrowski@ktzr.pl</p>'
             '<p><a href="/prywatnosc">Prywatność i cookies</a>' + (' · <a href="#" data-ustawienia-cookie>Ustawienia cookies</a>' if GA_ID else '') + '</p></div></div>')
STOPKA_EN = ('<div class="kol"><div><h4>About</h4><p><b>LawBenchmark.pl</b> is run by <b>LexAlpha Lab</b>, a joint research initiative of the law firm '
             '<a href="https://www.ktzr.pl/">KTZR</a> (Gdańsk, Poland) and <a href="https://lexalpha.pl/">LexAlpha Sp. z o.o.</a> (Warsaw). '
             'Authors: Adam Piotrowski (attorney-at-law, partner at KTZR), Andrzej Koman (CEO, LexAlpha). Funded by the two organisations; no model provider took part. '
             'Benchmark 02 does not include products of LexAlpha or KTZR; results of products scored in the Benchmark 01 pilot are not published. Not legal advice.</p>'
             '<div class="marki"><a href="https://www.ktzr.pl/">ktzr.pl</a><a href="https://lexalpha.pl/">lexalpha.pl</a><a href="https://github.com/apiotrowski-afk/lawbenchmark">GitHub</a></div></div>'
             '<div><h4>Pages</h4><p><a href="/">Results (Polish)</a><br><a href="/metodologia">Methodology (Polish)</a><br><a href="/dane">Data and code</a><br><a href="/wspolpraca">Collaboration (Polish)</a></p></div>'
             '<div><h4>Licence and contact</h4><p>Texts, keys and cards: CC BY 4.0. Code: MIT. Cite as "LexAlpha Lab, LawBenchmark.pl".</p><p>a.piotrowski@ktzr.pl</p></div></div>')

# ---------- zgoda na pliki cookie i Google Analytics 4 (tryb podstawowy: gtag ładowany WYŁĄCZNIE po zgodzie) ----------
ZGODA_HTML = ("" if not GA_ID else f"""<div class="zgoda" id="zgoda" role="dialog" aria-live="polite" aria-label="Pliki cookie" hidden>
<p>Za Twoją zgodą używamy plików cookie Google Analytics, żeby wiedzieć, które strony i materiały są czytane. Bez zgody nie ładujemy żadnego skryptu analitycznego. <a href="/prywatnosc">Prywatność i cookies</a></p>
<div><button type="button" class="btn p" data-zgoda="tak">Akceptuję</button><button type="button" class="btn p" data-zgoda="nie">Odrzucam</button></div>
</div>
<script>
(function(){{var ID="{GA_ID}",K="zgoda_analityka",b=document.getElementById('zgoda');
function czytaj(){{try{{return localStorage.getItem(K);}}catch(e){{return null;}}}}
function zapisz(v){{try{{localStorage.setItem(K,v);}}catch(e){{}}}}
function laduj(){{if(window.__ga)return;window.__ga=1;window.dataLayer=window.dataLayer||[];window.gtag=function(){{dataLayer.push(arguments);}};
gtag('js',new Date());gtag('config',ID);var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+ID;document.head.appendChild(s);}}
function usunCookie(){{document.cookie.split(';').forEach(function(c){{var n=c.split('=')[0].trim();if(n.indexOf('_ga')===0){{['','.lawbenchmark.pl','lawbenchmark.pl'].forEach(function(d){{document.cookie=n+'=; Max-Age=0; path=/'+(d?'; domain='+d:'');}});}}}});}}
var z=czytaj();if(z==='tak')laduj();else if(z!=='nie')b.hidden=false;
b.addEventListener('click',function(e){{var k=e.target.closest('[data-zgoda]');if(!k)return;var v=k.dataset.zgoda;var bylo=czytaj();zapisz(v);b.hidden=true;
if(v==='tak')laduj();else{{usunCookie();if(bylo==='tak')location.reload();}}}});
document.addEventListener('click',function(e){{if(e.target.closest('[data-ustawienia-cookie]')){{e.preventDefault();b.hidden=false;}}}});}})();
</script>""")

STRONY = []   # (ścieżka URL bez domeny, lastmod) — do mapy witryny


def kot(id_, tekst, poziom=2):
    return f'<h{poziom} id="{id_}">{tekst}<a class="kot" href="#{id_}" aria-label="odnośnik do sekcji">#</a></h{poziom}>'


def okruszki(sciezka):
    """Widoczne okruszki i BreadcrumbList z tej samej listy (strona główna → … → bieżąca)."""
    if not sciezka:
        return "", ""
    html_ = '<div class="wrap okr"><a href="/">LawBenchmark.pl</a>' + "".join(
        f'<span>›</span>' + (f'<a href="{E(u)}">{E(n)}</a>' if u else E(n)) for n, u in sciezka) + "</div>"
    lista = [{"@type": "ListItem", "position": 1, "name": "LawBenchmark.pl", "item": BAZA + "/"}]
    for i, (n, u) in enumerate(sciezka, start=2):
        el = {"@type": "ListItem", "position": i, "name": n}
        if u:
            el["item"] = BAZA + u
        lista.append(el)
    return html_, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lista}


def strona(sciezka, tytul, opis, tresc, *, lang="pl", okr=None, ld=None, lastmod=DATA_STRONY, og_opis=None, hreflang=None, tu=None):
    """Składa pełny dokument i zapisuje go pod site/<sciezka>/index.html (albo site/index.html dla '')."""
    url = BAZA + (sciezka or "/")
    okr_html, okr_ld = okruszki(okr or [])
    ld_lista = [x for x in ([okr_ld] if okr_ld else []) + (ld or []) if x]
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld_lista)
    hl = ""
    if hreflang:
        hl = "".join(f'<link rel="alternate" hreflang="{k}" href="{BAZA}{v}">\n' for k, v in hreflang.items())
    nav_html = "".join(f'<a href="{E(u)}"{" class=\"tu\"" if u == tu else ""}>{E(n)}</a>' for u, n in NAV)
    stopka = STOPKA_EN if lang == "en" else STOPKA_PL
    zgoda_html = ZGODA_HTML if GA_ID else ""
    dok = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(tytul)}</title>
<meta name="description" content="{E(opis)}">
<link rel="canonical" href="{url}">
{hl}<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:title" content="{E(tytul)}">
<meta property="og:description" content="{E(og_opis or opis)}">
<meta property="og:type" content="{"website" if not sciezka else "article"}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="LawBenchmark.pl">
<meta property="og:image" content="https://lawbenchmark.pl/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="LawBenchmark.pl: odpowiedzi z halucynacją 51 i 40 z 80, poprawnie ugruntowane 19 i 27 z 80, bez narzędzi i z wyszukiwaniem">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Literata:opsz,wght@7..72,500;7..72,600&display=swap" rel="stylesheet">
<style>{CSS}</style>
{ld_html}</head>
<body>
<nav><div class="wrap"><a class="logo" href="/"><b>LawBenchmark.pl</b><small>LexAlpha Lab · KTZR i LexAlpha</small></a><span class="sp"></span>
{nav_html}
<button id="motyw" aria-label="Przełącz motyw">◐</button></div>
<div class="wrap nav-m" aria-label="Menu">{nav_html}</div></nav>
{okr_html}
{tresc}
<footer><div class="wrap">{stopka}</div></footer>
{zgoda_html}
{SKRYPT}
</body>
</html>
"""
    kat = os.path.join(SITE, sciezka.strip("/")) if sciezka else SITE
    os.makedirs(kat, exist_ok=True)
    open(os.path.join(kat, "index.html"), "w", encoding="utf-8").write(dok)
    STRONY.append((sciezka or "/", lastmod))
    return dok


spr_n, spr_m = L["spr"]
spr_n_fmt = f"{spr_n:,}".replace(",", "\u202f")
spr_m_fmt = f"{spr_m:,}".replace(",", "\u202f")

# =====================================================================
# 1. Strona główna
# =====================================================================
GLOWNA = f"""
<header class="hero"><div class="wrap"><div>
<span class="eyb">Benchmark 02 · prawo polskie · aktualizacja {DATA_RAPORTU}</span>
<span class="tag"><i></i>Zbiór kalibracyjny</span>
<h1>Jak modele językowe odpowiadają na pytania z polskiego prawa?</h1>
<p class="lead">W badanej serii halucynacje oznaczono w {L["hal_W0"]} z 80 odpowiedzi bez narzędzi i w {L["hal_W1"]} z 80 z wyszukiwaniem w internecie; poprawnie ugruntowanych było odpowiednio {L["pu_W0"]} i {L["pu_W1"]}.</p>
<a class="btn p" href="#wyniki">Zobacz wyniki</a><a class="btn" href="/reports/lexalpha_lab_benchmark_02.pdf">Raport PDF · 44 str.</a><a href="/reports/Piotrowski_2026_correctly_grounded_v1.2.pdf" style="font:500 14px var(--sans);display:inline-block;padding:9px 4px">Artykuł metodologiczny (EN)</a>
<p class="uwaga">Wyniki dotyczą jednej serii dziesięciu pytań; karty sprawdzał jeden prawnik. To nie jest ogólny ranking modeli ani produktów. <a href="/metodologia#ograniczenia">Ograniczenia badania</a></p>
<div class="meta" style="margin-top:14px">O badaniu: Benchmark 02 · raport {WERSJA_RAPORTU} z {DATA_RAPORTU} · karty z {DATA_KART} · stan prawny 1.10.2026 · specyfikacja oceny 1.0.4</div>
</div>
<figure class="hw" aria-label="Wyniki łączne Benchmarku 02">
<figcaption>Benchmark 02 · 80 odpowiedzi w każdym warunku</figcaption>
<div class="hw-m"><span class="hw-t bad">Odpowiedzi z halucynacją</span>
<div class="hw-r"><span>bez narzędzi</span><span class="hw-tor"><i class="w0" style="width:{L["hal_W0"]/80*100:.1f}%"></i></span><b>{L["hal_W0"]}<small>/80</small></b></div>
<div class="hw-r"><span>z wyszukiwaniem</span><span class="hw-tor"><i class="w1" style="width:{L["hal_W1"]/80*100:.1f}%"></i></span><b>{L["hal_W1"]}<small>/80</small></b></div></div>
<div class="hw-m"><span class="hw-t ok">Poprawnie ugruntowane</span>
<div class="hw-r"><span>bez narzędzi</span><span class="hw-tor"><i class="w0" style="width:{L["pu_W0"]/80*100:.1f}%"></i></span><b>{L["pu_W0"]}<small>/80</small></b></div>
<div class="hw-r"><span>z wyszukiwaniem</span><span class="hw-tor"><i class="w1" style="width:{L["pu_W1"]/80*100:.1f}%"></i></span><b>{L["pu_W1"]}<small>/80</small></b></div></div>
<div class="hw-4"><div><b>10</b><span>pytań z praktyki</span></div><div><b>8</b><span>modeli, 3 dostawców</span></div><div><b>160</b><span>odpowiedzi z kartą</span></div><div><b>{spr_n_fmt}</b><span>sprawdzonych powołań z {spr_m_fmt}</span></div></div>
</figure>
</div></header>

<section id="czytanie"><div class="wrap">
<span class="eyb">Definicje</span>
<h2>Jak czytać wyniki</h2>
<div class="dwa">
<div class="blok ok"><h3>Poprawnie ugruntowane ↑</h3><p>Odpowiedź ma pełny rdzeń (trafia w sedno pytania) i ani jednego twierdzenia o źródle prawa niezgodnego z tekstem urzędowym, a co najmniej jedno powołanie zostało sprawdzone u źródła.</p></div>
<div class="blok bad"><h3>Z halucynacją ↓</h3><p>Odpowiedź zawiera co najmniej jedno twierdzenie o przepisie lub orzeczeniu niezgodne z tekstem urzędowym na dzień stanu prawnego, także wtedy, gdy sam wniosek jest trafny.</p></div>
</div>
<p class="teza">Brak halucynacji nie wystarcza: odpowiedź bez błędnych powołań, ale z niepełnym rdzeniem albo bez żadnego sprawdzonego źródła, nie jest poprawnie ugruntowana. <a href="/metodologia#ugruntowanie">Definicje i mianowniki</a>.</p>
</div></section>

<section id="wyniki"><div class="wrap">
<span class="eyb">Wyniki</span>
<h2>Wyniki: bez narzędzi (W0) i z wyszukiwaniem (W1)</h2>
<p class="pod">Każdy model odpowiadał na te same dziesięć pytań dwa razy: bez narzędzi (W0) i z wyszukiwaniem w internecie narzędziem dostawcy (W1).</p>
<p class="wer"><b>Jak powstała ocena.</b> Model przygotowuje kartę każdej odpowiedzi i szuka każdego powołania w źródle urzędowym; prawnik sprawdza każdą kartę i zatwierdza albo zmienia ocenę. Sprawdzono {spr_n_fmt} z {spr_m_fmt} powołań. <a href="/metodologia#procedura">Procedura</a></p>
{LEGENDA_W}
{WYKRES}
<h2 style="margin-top:36px;font-size:22px">Wyniki szczegółowe</h2>
<p class="pod">Dla jednego modelu w jednym warunku jedna odpowiedź to 10 punktów procentowych; różnice 1–2 odpowiedzi nie wystarczają do ustalenia stabilnej kolejności modeli. Blok A to kryteria sprawdzane wobec klucza i źródła (rdzeń, podstawy prawne, powołania), blok B to kryteria ocenne. Koszt serii dziesięciu odpowiedzi według cenników z 18.10.2026 jako równoważnik API; „≥” to dolne oszacowanie. Wyniki per pytanie: <a href="/benchmark/02/pytania">dziesięć pytań</a>.</p>
<p class="przesun">Tabelę można przesuwać w bok; kolumna z nazwą modelu zostaje na miejscu.</p>
{TABELA}
</div></section>

<section id="bledy"><div class="wrap">
<span class="eyb">Klasy błędu</span>
<h2>Cztery klasy błędu</h2>
<p class="pod">Najczęściej oznaczano klasę T: przypisanie istniejącemu przepisowi lub orzeczeniu treści, której źródło nie potwierdza ({KLASA["T"][0]} z 80 odpowiedzi bez narzędzi, {KLASA["T"][1]} z 80 z wyszukiwaniem). Klasa W, brzmienie przepisu z innej daty podane jako obowiązujące, wystąpiła w {KLASA["W"][0]} i {KLASA["W"][1]} odpowiedziach. Ma znaczenie, bo przepisy zmieniają się nowelizacjami, a do pisma trafia brzmienie obowiązujące w dniu sprawy. Zmyślone źródło (F) i przekręcony identyfikator (S) są rzadkie.</p>
<div class="legenda" style="margin:0 0 6px"><span><i class="lg-w0" style="border-radius:3px;background:var(--muted);border:0"></i>W0 · bez narzędzi</span><span><i class="lg-w1" style="border-radius:3px"></i>W1 · z wyszukiwaniem</span><span>odpowiedzi z co najmniej jednym błędem danej klasy, na 80 w każdym warunku</span></div>
{KLASY_HTML}
<p class="uwaga" style="margin-top:14px">Jedna odpowiedź może mieć kilka klas, więc liczby się nie sumują. Łącznie {L["hal_W0"]} odpowiedzi z halucynacją bez narzędzi i {L["hal_W1"]} z wyszukiwaniem. <a href="/metodologia#halucynacja">Definicje klas</a></p>
</div></section>

<section id="przyklady"><div class="wrap">
<span class="eyb">Przykłady z kart</span>
<h2>Dwa przykłady z kart</h2>
<p class="pod">Oba przykłady to ten sam model, GPT-5.6 Terra, w obu warunkach: w P01 wyszukiwanie zaszkodziło, w P05 pomogło. Każda ze 160 odpowiedzi ma podobną kartę z punktami, dowodem ze źródła i klasą błędu.</p>

<div class="prz">
<span class="eyb"><a href="/benchmark/02/pytania/p01">P01</a> · próg wykroczenia przeciwko mieniu · GPT-5.6 Terra</span>
<h3>Z wyszukiwaniem gorzej: przytaknięcie pułapce</h3>
<div class="pbox"><b>Pytanie</b> zakłada, że próg między wykroczeniem a przestępstwem przeciwko mieniu nadal rośnie z płacą minimalną. <b>Pułapka:</b> od 1.10.2023 to stała kwota 800 zł (art. 119 § 1 k.w.).</div>
<div class="dw">
<div class="kp"><span class="wn"><i class="lg-w0"></i>W0 · bez narzędzi</span>
<blockquote>„W 2026 r. granica … wynosi co do zasady 800 zł. Nie zmieniła się ona wraz ze wzrostem płacy minimalnej.”</blockquote>
<div class="chips"><span class="chip ok">Kwota trafna</span><span class="chip">Klasa W w historii progu (element rubryki)</span><span class="chip">5 z 5 powołań sprawdzonych</span></div></div>
<div class="kp"><span class="wn"><i class="lg-w1"></i>W1 · z wyszukiwaniem</span>
<blockquote>„W 2026 r. próg wynosi 1 201,50 zł. Tak, próg wzrósł wraz z płacą minimalną … ustawowy próg to jej 1/4.”</blockquote>
<div class="chips"><span class="chip bad">Przytaknięcie pułapce</span><span class="chip">Klasa W w rdzeniu</span><span class="chip">4 z 6 powołań błędne: art. 119, 120, 122 i 124 § 1 k.w. w dawnym brzmieniu</span></div></div>
</div>
<p class="wniosek"><b>W tej parze</b> wyszukiwanie nie zastąpiło sprawdzenia brzmienia przepisu na datę: model z dostępem do sieci podał brzmienie sprzed 1.10.2023 jako obowiązujące.</p>
</div>

<div class="prz">
<span class="eyb"><a href="/benchmark/02/pytania/p05">P05</a> · doręczenia przez Portal Informacyjny · GPT-5.6 Terra</span>
<h3>Z wyszukiwaniem lepiej: znaleziona nowela</h3>
<div class="pbox"><b>Pytanie</b> dotyczy doręczeń osobie fizycznej przez Portal Informacyjny. <b>Pułapka aktualności:</b> od 1.06.2026 sąd doręcza przez portal także stronie, która wybrała ten sposób (art. 131¹ᵃ § 1 k.p.c.); wcześniej tylko pełnomocnikom zawodowym.</div>
<div class="dw">
<div class="kp"><span class="wn"><i class="lg-w0"></i>W0 · bez narzędzi</span>
<blockquote>„Co do zasady osoba fizyczna występująca we własnym imieniu nie jest obowiązana odbierać pism sądowych przez Portal Informacyjny.”</blockquote>
<div class="chips"><span class="chip bad">Rdzeń odwrotny do klucza</span><span class="chip">Klasa W w rdzeniu: art. 131¹ᵃ § 1 w brzmieniu sprzed 1.06.2026</span><span class="chip">Blok A 0 %</span></div></div>
<div class="kp"><span class="wn"><i class="lg-w1"></i>W1 · z wyszukiwaniem</span>
<blockquote>„Tak — od 1 czerwca 2026 r. osoba fizyczna może otrzymywać pisma sądowe przez Portal Informacyjny, ale wyłącznie po dobrowolnym wyborze tej formy doręczeń.”</blockquote>
<div class="chips"><span class="chip ok">Poprawnie ugruntowana</span><span class="chip">11 z 11 powołań zgodnych</span><span class="chip">Blok A 100 %</span></div></div>
</div>
<p class="wniosek"><b>W tej parze</b> wyszukiwanie dało dostęp do noweli, której model nie znał z pamięci. Inny przypadek, w którym trafna odpowiedź „tak” opiera się na złym przepisie: <a href="/benchmark/02/pytania/p07#przyklad">P07, Claude Haiku 5.5</a>.</p>
</div>
</div></section>

<section id="metodologia"><div class="wrap">
<span class="eyb">Metoda</span>
<h2>Jak powstaje wynik</h2>
<p class="pod">Każda liczba na tej stronie wynika z karty oceny jednej odpowiedzi. <a href="/metodologia">Pełna metodologia</a></p>
<div class="rz">
<div><b>Pytania z praktyki</b><span>Dziesięć pytań w brzmieniu wpisanym do czatu, z literówkami. Sześć ma wbudowaną błędną albo nieaktualną przesłankę.</span></div>
<div><b>Klucz ustalony przed badaniem</b><span>Rdzeń odpowiedzi, przepisy wymagane i elementy punktowane, każda podstawa sprawdzona w tekście urzędowym na 1.10.2026.</span></div>
<div><b>Każde powołanie u źródła</b><span>Przepisy w ISAP i ELI, orzeczenia w SAOS i na stronach sądów. Jeden błąd klasy F, T, W albo S daje etykietę „halucynacja”.</span></div>
<div><b>Karta sprawdzana przez prawnika</b><span>Model przygotowuje kartę z dowodami, prawnik ją zatwierdza albo zmienia. Pięciu sędziów-modeli ocenia to samo dla porównania.</span></div>
<div><b>Bez udziału dostawców modeli</b><span>Żaden dostawca nie przygotowywał ani nie finansował badania. Produktów LexAlpha i KTZR nie ma w Benchmarku 02.</span></div>
<div><b>Ograniczenia na wierzchu</b><span>Dziesięć pytań, jedna seria, jeden prawnik. 160 odpowiedzi to nie 160 niezależnych obserwacji. <a href="/metodologia#ograniczenia">Ograniczenia</a></span></div>
</div>
</div></section>

<section id="dane"><div class="wrap">
<span class="eyb">Materiały</span>
<h2>Raporty, dane i kod</h2>
<p class="pod">Wszystko, co stoi za liczbami, jest publiczne: pytania z kluczami, odpowiedzi, karty, oceny sędziów i skrypty.</p>
<div class="mat">
<a href="/reports/lexalpha_lab_benchmark_02.pdf"><span class="eyb">Raport · PL · PDF</span><b>Benchmark 02 · pytania prawne</b><span>Wersja {WERSJA_RAPORTU} z {DATA_RAPORTU}, 44 strony: wyniki, klasy błędów, sędziowie-modele, ograniczenia.</span></a>
<a href="{HF_URL}" class="wyr"><span class="eyb">Zbiór danych · Hugging Face · od 29.10.2026</span><b>LexAlphaLab/lawbenchmark-b02</b><span>Sześć tabel jako zbiór testowy: karty, odpowiedzi, pytania, klucze, oceny sędziów, weryfikacja.</span></a>
<a href="https://doi.org/10.5281/zenodo.23674794"><span class="eyb">Artykuł · EN · DOI</span><b>„Hallucination” Is Not Enough</b><span>Dlaczego benchmarki prawnicze powinny mierzyć odpowiedzi poprawnie ugruntowane. Working paper v1.2.</span></a>
<a href="{REPO_URL}"><span class="eyb">Kod i źródła · GitHub</span><b>apiotrowski-afk/lawbenchmark</b><span>Specyfikacja oceny, karty w Markdown, skrypty liczące każdą liczbę raportu. CC BY 4.0 i MIT.</span></a>
<a href="/benchmark/01"><span class="eyb">Pilotaż · kazus</span><b>Benchmark 01 · kazus SKD</b><span>Jeden fikcyjny kazus o terminie z art. 45 ust. 5 u.k.k. i 17 odpowiedzi modeli ogólnych.</span></a>
<a href="/raporty#benchmark-02"><span class="eyb">Cytowanie</span><b>Jak cytować</b><span>Opisy bibliograficzne i BibTeX raportu, artykułu i zbioru danych.</span></a>
</div>
</div></section>
"""
LD_ORG = {"@context": "https://schema.org", "@type": "ResearchProject", "name": "LawBenchmark.pl", "alternateName": "LexAlpha Lab Benchmark",
          "url": BAZA + "/", "inLanguage": "pl",
          "parentOrganization": {"@type": "Organization", "name": "KTZR", "url": "https://www.ktzr.pl/"},
          "description": "Benchmark modeli językowych w polskim prawie: poprawność, halucynacje i oparcie w źródłach urzędowych."}
strona("", "LawBenchmark.pl — modele językowe a polskie prawo",
       "Jak modele językowe odpowiadają na pytania z polskiego prawa: poprawność, halucynacje i oparcie w źródłach urzędowych, bez narzędzi i z wyszukiwaniem. Projekt LexAlpha Lab.",
       GLOWNA, ld=[LD_ORG], lastmod=DATA_STRONY, og_opis="Benchmark 02: 8 modeli, 10 pytań, 160 odpowiedzi, każde powołanie sprawdzone w źródle urzędowym.",
       hreflang={"pl": "/", "en": "/en", "x-default": "/"})

# =====================================================================
# 2. Metodologia
# =====================================================================
SEDZ_HTML = ['<div class="scroll"><table class="t zw"><thead><tr><th>Sędzia</th><th>Zbiór pytań</th><th class="num">n kart</th><th class="num">Zgodność</th><th class="num">κ</th>'
             '<th class="num">Fałszywe alarmy</th><th class="num">Pominięcia</th><th class="num">Wyszukań na kartę</th></tr></thead><tbody>']
for c in SEDZIOWIE_T:
    SEDZ_HTML.append(f'<tr><td class="model">{E(c[0])}</td><td>{E(c[1])}</td><td class="num">{E(c[2])}</td><td class="num">{E(c[3])}</td><td class="num">{E(c[4])}</td>'
                     f'<td class="num">{E(c[5])}</td><td class="num">{E(c[6])}</td><td class="num">{E(c[7])}</td></tr>')
SEDZ_HTML.append("</tbody></table></div>")
SEDZ_HTML = "\n".join(SEDZ_HTML)

ZR_HTML = ['<div class="scroll"><table class="t zw"><thead><tr><th>Model (W1)</th><th class="num">Źródło urzędowe użyte</th><th class="num">Tylko źródła wtórne</th><th class="num">Narzędzia nieużyte</th>'
           '<th>Halucynacje wg pochodzenia<br><small>pamięć / odczyt źródła / źródło wtórne / nieustalone</small></th></tr></thead><tbody>']
for c in ZRODLA_T:
    ZR_HTML.append(f'<tr><td class="model">{E(c[0])}</td><td class="num">{E(c[1])}</td><td class="num">{E(c[2])}</td><td class="num">{E(c[3])}</td><td>{E(c[5])}</td></tr>')
ZR_HTML.append("</tbody></table></div>")
ZR_HTML = "\n".join(ZR_HTML)

METODOLOGIA = f"""
<header class="pod-hero"><div class="wrap">
<h1>Metodologia oceny</h1>
<p class="lead">Jak powstaje każda liczba na tej stronie: pytania, klucze, warunki badania, kryteria oceny, definicja halucynacji i odpowiedzi poprawnie ugruntowanej, sędziowie-modele, warstwa weryfikacji, koszt, ograniczenia.</p>
<div class="meta">Specyfikacja oceny v1.0.4 z 29.10.2026 (zasady punktacji niezmienione od 1.0.1 z 11.10.2026) · stan prawny 1.10.2026 · pełny tekst specyfikacji z rejestrem decyzji w <a href="/dane">repozytorium</a></div>
<div class="spis">
<a href="#konstrukt">Co mierzymy</a><a href="#pytania">Pytania</a><a href="#klucze">Klucze</a><a href="#warunki">Warunki badania</a><a href="#karta">Karta oceny</a><a href="#halucynacja">Halucynacja i klasy błędu</a>
<a href="#ugruntowanie">Poprawnie ugruntowane</a><a href="#procedura">Jak powstaje karta</a><a href="#sedziowie">Sędziowie-modele</a><a href="#weryfikacja">Warstwa weryfikacji</a><a href="#koszt">Koszt</a>
<a href="#ograniczenia">Ograniczenia</a><a href="#wersje">Wersjonowanie</a><a href="#kontaminacja">Kontaminacja</a><a href="#autorzy">Autorzy i finansowanie</a>
</div>
</div></header>
<article><div class="wrap meto">
<aside aria-label="Spis treści"><p class="n">Na tej stronie</p>
<a href="#konstrukt">Co mierzymy</a><a href="#pytania">Pytania</a><a href="#klucze">Klucze</a><a href="#warunki">Warunki badania</a><a href="#karta">Kryteria oceny</a><a href="#halucynacja">Halucynacja i klasy błędu</a>
<a href="#ugruntowanie">Poprawnie ugruntowane</a><a href="#procedura">Karta oceny</a><a href="#sedziowie">Sędziowie-modele</a><a href="#weryfikacja">Warstwa weryfikacji</a><a href="#koszt">Koszt</a>
<a href="#ograniczenia">Ograniczenia</a><a href="#wersje">Wersjonowanie</a><a href="#kontaminacja">Kontaminacja</a><a href="#autorzy">Autorzy i finansowanie</a></aside>
<div>
<section>{kot("konstrukt", "Co mierzy benchmark modeli AI")}
<p>Za benchmarkiem stoi praktyczne pytanie: ile pracy sprawdzającej zostaje prawnikowi po otrzymaniu odpowiedzi modelu. Benchmark tego pytania nie rozstrzyga. Mierzy dwie rzeczy, które da się sprawdzić: zgodność odpowiedzi z kluczem ustalonym przed badaniem oraz prawdziwość zawartych w niej twierdzeń o źródłach prawa wobec tekstu urzędowego na dzień stanu prawnego. Żadna etykieta na tej stronie nie oznacza, że odpowiedź nadaje się do pisma bez kontroli.</p>
<p>Stąd dwie osie oceny. Pierwsza, <b>halucynacja</b>, odpowiada na pytanie, czy twierdzenia o źródłach prawa są prawdziwe. Druga, <b>ugruntowanie</b>, odpowiada na pytanie, czy powołania w odpowiedzi dało się potwierdzić w źródle urzędowym, a w warunku z wyszukiwaniem także, czy system takie źródło otworzył. Miara główna łączy obie osie: odsetek odpowiedzi <a href="#ugruntowanie">poprawnie ugruntowanych</a>.</p>
<p>Benchmark 02 jest zbiorem kalibracyjnym. Dziesięć pytań, jedna seria i jeden sprawdzający prawnik wystarczają, by pokazać kryteria i ich skutki na prawdziwych odpowiedziach, nie by ustalić ranking produktów. Reguły oceny zmieniano w trakcie pracy po lekturze odpowiedzi; każda zmiana ma datę w rejestrze decyzji.</p>
</section>

<section>{kot("pytania", "Pytania")}
<p>Pytania pochodzą z praktyki kancelarii i mają postać, w jakiej prawnik wpisuje je do czatu: z literówkami, skrótami, czasem z błędną przesłanką. Błędy językowe i błędne przesłanki zachowano celowo, by sprawdzić, jak systemy reagują na takie pytania.</p>
<p>Każde pytanie ma typ, który decyduje o sposobie liczenia rdzenia odpowiedzi:</p>
<ul>
<li><b>zamknięte</b> — trafienie „tak”, „nie” albo „zależy od X”; w Benchmarku 02 osiem z dziesięciu pytań;</li>
<li><b>obliczenie</b> — wynik liczbowy w zadanej tolerancji (P01);</li>
<li><b>weryfikacja</b> — czy system sprawdza cudze twierdzenie, czy mu przytakuje (P08).</li>
</ul>
<p>Sześć pytań ma wbudowaną <b>pułapkę</b>: błędną albo nieaktualną przesłankę, którą system powinien nazwać i skorygować. Przykład: pytanie P01 zakłada, że próg wykroczenia rośnie z płacą minimalną, a od 1.10.2023 jest kwotą stałą. Pytanie P05 działa odwrotnie: odpowiedź, która jeszcze w maju 2026 r. była prawidłowa, na dzień stanu prawnego jest nieaktualna. Para P09 i P10 to <b>para z przeciwnymi sugestiami</b> (w specyfikacji: „lustro”): to samo zagadnienie, raz z sugestią „nie wystarcza”, raz „wystarcza”. Mierzy, czy system zmienia odpowiedź pod wpływem oczekiwań pytającego.</p>
<p>Każde pytanie ma <b>tekst oryginalny</b> (dokładnie tak, jak wpisał prawnik) i, gdy oryginał nie wystarcza do jednoznacznego klucza, <b>tekst benchmarkowy</b> uzupełniony przed badaniem o brakujące dane. W badaniu użyto tekstu benchmarkowego, jeśli istnieje: dotyczy to P01, P04 i P09 (P10 jako wersja z odwróconą sugestią ma tylko tekst benchmarkowy); pozostałe sześć pytań zadano w brzmieniu oryginalnym. Strona każdego pytania pokazuje obie wersje. Pełne brzmienia i klucze: <a href="/benchmark/02/pytania">dziesięć pytań</a>.</p>
<p>Pula liczy 50 pytań. Opublikowano 10; pozostałe 40 zostają nieujawnione, by kolejne edycje mogły użyć pytań, których modele nie widziały.</p>
</section>

<section>{kot("klucze", "Jak ustalamy prawidłową odpowiedź: klucze")}
<p>Klucz pytania jest ustalany przed zebraniem odpowiedzi i zawiera: <b>rdzeń</b> odpowiedzi, <b>rubrykę</b> (elementy premiowane), <b>kary</b> (błędy, za które odejmuje się punkt), <b>podstawy wymagane</b> (przepisy, bez których odpowiedź nie jest kompletna) i oczekiwaną <b>kalibrację</b> (kategoryczna albo warunkowa, z warunkiem). Zasady klucza:</p>
<ol>
<li>Każda podstawa ma źródło: ISAP, ELI, EUR-Lex, SAOS albo sn.pl. Cytaty przepisów są przepisane z tekstu urzędowego, nie z bazy pomocniczej ani z pamięci.</li>
<li>Orzeczenie w kluczu ma sygnaturę, sąd, datę, tezę przepisaną z tekstu orzeczenia i źródło z zakresem odczytu. Omówienia i komentarze nie są źródłem tezy.</li>
<li>Klucz obejmuje tylko to, o co pyta pytanie. Zagadnienie sąsiednie nie wchodzi do rubryki ani kar, choćby było praktycznie ważne.</li>
<li>Klucza nie zmienia się po poznaniu odpowiedzi systemów. Zmiana wymaga nowej wersji z datą i powodem.</li>
<li>Do badania idą tylko klucze zatwierdzone przez prawnika; pole „weryfikacja” mówi wprost, czego nie sprawdzono.</li>
</ol>
<p>Stan prawny każdego klucza to <b>1 października 2026 r.</b> Odpowiedzi ocenia się według prawa na ten dzień. Dwa klucze (P09, P10) zmieniono po zebraniu odpowiedzi, gdy orzecznictwo Sądu Najwyższego okazało się bardziej zniuansowane niż klucz; rdzeń stał się warunkowy, a zmiana jest opisana w raporcie i w rejestrze decyzji. Jest to odstępstwo od zasady 4 i podajemy je jawnie. Warunkowość rdzenia P09 i P10 wynika z wykładni umowy (art. 65 k.c.) przyjętej w orzecznictwie Sądu Najwyższego, nie z rozbieżności między orzeczeniami; dlatego pytania nie są oznaczone jako sporne i kryterium A5 ich nie dotyczy.</p>
<p>Dokumenty niewiążące (wytyczne Komisji Europejskiej, kodeksy praktyk) wchodzą do klucza jako osobny element rubryki, nigdy jako kara: brak odwołania nie jest błędem, a halucynacją jest dopiero przypisanie im mocy wiążącej albo treści, której w nich nie ma.</p>
</section>

<section>{kot("warunki", "Warunki badania")}
<p>Każdy model odpowiadał na te same dziesięć pytań w dwóch warunkach:</p>
<ul>
<li><b>W0</b> — bez narzędzi: ten sam krótki, neutralny wstęp i pytanie. Odpowiedź pochodzi wyłącznie z wag modelu.</li>
<li><b>W1</b> — z wyszukiwaniem w internecie narzędziem dostawcy: dla OpenAI wyszukiwanie Codex CLI, dla Anthropic WebSearch i WebFetch w Claude Code, dla Google <code>google_search</code> i <code>url_context</code> w Vertex AI. Wstęp dodaje jedno zdanie o podawaniu adresów źródeł.</li>
</ul>
<p>Wstęp nie zawiera prośby o zwięzłość ani wskazówek o pułapkach czy sporności i nie zmienia się w trakcie serii. Jedna seria, jedna odpowiedź na pytanie; odpowiedź zapisuje się w postaci, w jakiej zwrócił ją system, razem ze śladem narzędzi tam, gdzie narzędzie go zapisuje.</p>
<div class="scroll"><table class="t"><thead><tr><th>Dostawca</th><th>Model</th><th>Identyfikator</th><th>Wywołanie</th><th>Ustawienia</th></tr></thead><tbody>
<tr><td>OpenAI</td><td>GPT-6.1 Sol</td><td><code>gpt-6.1-sol</code></td><td rowspan="3">Codex CLI (konto ChatGPT)</td><td rowspan="3">rozumowanie: medium; W1: wyszukiwanie Codex</td></tr>
<tr><td>OpenAI</td><td>GPT-6 Astra</td><td><code>gpt-6-astra</code></td></tr>
<tr><td>OpenAI</td><td>GPT-5.6 Terra</td><td><code>gpt-5.6-terra</code></td></tr>
<tr><td>Anthropic</td><td>Claude Opus 5.5</td><td><code>claude-opus-5-5</code></td><td rowspan="3">Claude Code CLI (subskrypcja), bez MCP i CLAUDE.md</td><td rowspan="3">temperatura domyślna CLI; W1: WebSearch + WebFetch (strony streszcza model pomocniczy Haiku)</td></tr>
<tr><td>Anthropic</td><td>Claude Sonnet 5.5</td><td><code>claude-sonnet-5-5</code></td></tr>
<tr><td>Anthropic</td><td>Claude Haiku 5.5</td><td><code>claude-haiku-5-5</code></td></tr>
<tr><td>Google</td><td>Gemini 3.8 Flash</td><td><code>gemini-3.8-flash</code></td><td rowspan="2">Vertex AI, region <code>global</code></td><td rowspan="2">poziom rozumowania domyślny modelu; W1: <code>google_search</code> + <code>url_context</code></td></tr>
<tr><td>Google</td><td>Gemini 4 Argon</td><td><code>gemini-4-argon</code></td></tr>
</tbody></table></div>
<p>Odpowiedzi zebrano 10, 13, 17 i 18 października 2026 r.; każda ma datę, identyfikator modelu i ustawienia w metadanych. Własne produkty kancelarii nie biorą udziału w benchmarku.</p>
</section>

<section>{kot("karta", "Kryteria oceny")}
<p>Każda odpowiedź ma kartę z punktem za każde kryterium i dowodem ze źródła. Karta dzieli się na blok A (kryteria sprawdzane wobec klucza i tekstu urzędowego) i blok B (kryteria ocenne); wyniki obu bloków podajemy osobno i nie uśredniamy ich. Także w bloku A część ocen wymaga rozstrzygnięcia prawnika: istnienie źródła i brzmienie przepisu porównuje się wprost, ale to, czy przypisana źródłu treść mieści się w jego tekście, ocenia prawnik wobec źródła i klucza.</p>
{kot("blok-a", "Blok A — kryteria sprawdzane wobec klucza i źródła", 3)}
<div class="scroll"><table class="t"><thead><tr><th>Kryterium</th><th>Co mierzy</th><th>Punkty</th></tr></thead><tbody>
<tr><td><b>A-R</b></td><td>rdzeń odpowiedzi: czy odpowiedź trafia w sedno pytania (może paść w dowolnym miejscu odpowiedzi)</td><td>0 / 1 / 2 — 2 = pełny rdzeń, 1 = kierunek trafny bez kluczowego warunku (np. jedna gałąź pytania warunkowego)</td></tr>
<tr><td><b>A2</b></td><td>podstawy wymagane z klucza</td><td>0 / 1 — 0 przy braku którejkolwiek albo przy błędnej podstawie</td></tr>
<tr><td><b>A3</b></td><td>cytaty przepisów zgodne z tekstem urzędowym</td><td>0 / 1, tylko gdy system cytuje; inaczej nie dotyczy</td></tr>
<tr><td><b>A5</b></td><td>nazwanie sporności</td><td>0 / 1, tylko przy pytaniu oznaczonym jako sporne (w Benchmarku 02 brak)</td></tr>
<tr><td><b>A6</b></td><td>halucynacje: zgodność każdego twierdzenia o źródle prawa z tekstem urzędowym</td><td>1 / 0 — zero-jedynkowe, z klasą i pochodzeniem błędu (sekcja niżej)</td></tr>
<tr><td><b>A8</b></td><td>ramy: czy odpowiedź dotyczy zadanego pytania (długości nie ocenia)</td><td>1 / ½ / 0 — ½ przy dygresji poza pytanie, 0 gdy treść poza pytaniem przeważa, odpowiedź dotyczy innego pytania albo zawiera artefakty techniczne</td></tr>
<tr><td><b>R</b></td><td>elementy rubryki klucza</td><td>+1 za każdy</td></tr>
<tr><td><b>K</b></td><td>kary z klucza</td><td>−1 za każdą; wynik bloku nie spada poniżej 0</td></tr>
</tbody></table></div>
<p><b>A % = (suma punktów − kary) / suma punktów możliwych</b>; punkty możliwe liczy się bez kryteriów „nie dotyczy”. Przy pułapce omówienie prawidłowego stanu prawnego zamiast założonego w pytaniu jest odpowiedzią, nie dygresją. Milczące przyjęcie błędnego numeru przepisu z pytania kosztuje element rubryki, jeśli klucz go ma; karę płaci dopiero utrwalenie błędu.</p>
{kot("blok-b", "Blok B — kryteria ocenne", 3)}
<ul>
<li><b>B1, przydatność</b> (0–2): czy prawnik wie, co zrobić dalej. Błąd w praktycznej wskazówce, który zmienia działanie (kwota opłaty, termin, organ, forma), obniża B1 do najwyżej 1, także gdy system nie powołał przepisu.</li>
<li><b>B2, sposób sformułowania konkluzji</b> (0–1; do 29.10.2026 pod nazwą „kalibracja”): zgodność formy konkluzji z kluczem. Przy kluczu kategorycznym punkt dostaje odpowiedź, która stawia tezę wprost; rozmycie jasnej tezy („zależy od interpretacji”, „warto skonsultować”) bez wskazania, od czego, kosztuje punkt. Przy kluczu warunkowym punkt dostaje odpowiedź, która wiąże konkluzję z warunkiem; system może też dopytać, o ile nazwie rozwidlenie.</li>
</ul>
<p>B2 mierzy formę konkluzji wobec klucza, nie trafność ani rzeczywistą pewność modelu, stąd zmiana nazwy po recenzji zewnętrznej: błędna, lecz kategoryczna odpowiedź przy kluczu kategorycznym ma B2 = 1, a sam błąd obniża wynik bloku A. Blok B nie dubluje bloku A; profil „A niskie, B wysokie” ma być widoczny, nie wygładzony. Formułki „nie stanowi porady prawnej” nie wpływają na ocenę.</p>
</section>

<section>{kot("halucynacja", "Halucynacja i klasy błędu")}
<p><b>Halucynacją</b> jest każde twierdzenie o źródle prawa niezgodne ze źródłem urzędowym na dzień stanu prawnego. Jedno takie twierdzenie daje A6 = 0 i etykietę „halucynacja” dla całej odpowiedzi, także wtedy, gdy sam wniosek jest trafny. Etykieta „bez halucynacji” oznacza brak <i>wykrytej</i> halucynacji: sprawdzono {spr_n} z {spr_m} powołań, a powołania niesprawdzone nie obniżały oceny (jedna karta ma niesprawdzone powołanie przy etykiecie „poprawnie ugruntowana”; raport, rozdz. 8).</p>
<p>Karta zapisuje obok punktu wszystkie wykryte klasy błędu, każdą z dowodem (co powołano, co jest w źródle, gdzie sprawdzono):</p>
<div class="klasy">
<div class="klasa"><span class="znak">F</span><div><b>{E(KL_OPIS["F"])}</b><span class="m">zmyślony artykuł, paragraf, wyrok albo akt</span></div></div>
<div class="klasa"><span class="znak">T</span><div><b>{E(KL_OPIS["T"])}</b><span class="m">treść odwrotna, cudza, o rozciągniętym albo zawężonym zakresie, dla innego adresata lub kanału; także teza przypisana ogólnie „orzecznictwu”, sprzeczna z prawem</span></div></div>
<div class="klasa"><span class="znak">W</span><div><b>{E(KL_OPIS["W"])}</b><span class="m">dawne albo przyszłe brzmienie przepisu podane jako aktualne</span></div></div>
<div class="klasa"><span class="znak">S</span><div><b>{E(KL_OPIS["S"])}</b><span class="m">prawdziwe źródło z przekręconym numerem, datą, sądem, publikatorem lub nazwą aktu</span></div></div>
</div>
<p>W Benchmarku 02 klasa T wystąpiła w {L["klasa_T"]} odpowiedziach, W w {L["klasa_W"]}, F w {L["klasa_F"]}, S w {L["klasa_S"]}. Jedna odpowiedź może mieć kilka klas, więc liczby nie sumują się do {L["hal"]} odpowiedzi z halucynacją.</p>
<p>Samo <b>pominięcie</b> przesłanki albo elementu przepisu nie jest twierdzeniem fałszywym: nie obniża A6, odejmuje punkty w rubryce i rdzeniu. Granica z klasą T: odpowiedź, która opisuje art. 787 k.p.c. niepełnie, ale nie twierdzi, że przepis obejmuje tylko to, co opisała, popełnia pominięcie; odpowiedź, która stwierdza, że przepis stosuje się wyłącznie w sytuacji, do której się nie ogranicza, przypisuje mu zawężony zakres i dostaje klasę T. Odpowiedź bez żadnych powołań ma A6 = 1. Odpowiedź pusta ma A6 = 0 bez etykiety. Gdy tekst zablokował filtr dostawcy (np. Vertex <code>RECITATION</code>), odpowiedź trafia do osobnej kategorii „blokada dostawcy”: ani halucynacja, ani odpowiedź prawidłowa (w Benchmarku 02 jeden przypadek, P07 Gemini 4 Argon W1).</p>
<p>Przy każdym błędzie karta zapisuje dwie rzeczy więcej:</p>
<ul>
<li><b>pochodzenie</b> — <i>pamięć</i> (brak potwierdzonego odczytu źródła: warunek bez narzędzi, narzędzia nieużyte albo brak tego aktu w śladzie narzędzi; nazwa kategorii wyraża hipotezę, że treść pochodzi z wag modelu), <i>odczyt źródła</i> (ślad pokazuje otwarcie właściwego źródła urzędowego, a treść i tak jest błędna), <i>źródło wtórne</i> (błąd powtarza błąd lub skrót serwisu, który system otworzył), <i>nieustalone</i>;</li>
<li><b>zakres</b> — <i>rdzeń</i>, gdy błąd dotyczy sedna pytania, podstaw wymaganych albo elementu rubryki; <i>poboczne</i>, gdy występuje w części pobocznej (dygresja, analogia, tło) przy poprawnej konkluzji. W Benchmarku 02: {L["zakres_rdzen"]} odpowiedzi z błędem w rdzeniu, {L["zakres_pob"]} z błędem tylko pobocznym.</li>
</ul>
<p>W warunku W1 karta odnotowuje także, czy system w ogóle użył źródła urzędowego:</p>
{ZR_HTML}
</section>

<section>{kot("ugruntowanie", "Odpowiedź poprawnie ugruntowana")}
<p>Odpowiedź jest <b>poprawnie ugruntowana</b>, gdy spełnia trzy warunki naraz: pełny rdzeń (A-R = 2), brak wykrytej halucynacji (A6 = 1) i co najmniej jedno powołanie, które oceniający potwierdził w źródle urzędowym. Sprawdzenia dokonuje oceniający, nie system: etykieta mówi, że powołania w odpowiedzi są prawdziwe i da się je potwierdzić, a nie, że model je przeczytał. W warunku bez narzędzi model źródła nie otwierał; czy w warunku z wyszukiwaniem otworzył źródło urzędowe, pokazuje osobna tabela w sekcji o halucynacjach. Odpowiedź bez błędnych powołań, ale z niepełnym rdzeniem albo bez żadnego potwierdzonego powołania, nie jest poprawnie ugruntowana; odpowiedź z trafnym wnioskiem i jednym fałszywym powołaniem też nie.</p>
<p>Mianowniki: każdy model ma 10 odpowiedzi w warunku; 80 odpowiedzi w warunku; 160 odpowiedzi łącznie. W Benchmarku 02 poprawnie ugruntowanych było {L["pu_W0"]} z 80 w W0 i {L["pu_W1"]} z 80 w W1; z halucynacją {L["hal_W0"]} i {L["hal_W1"]}. Reszta to odpowiedzi bez wykrytej halucynacji, lecz z niepełnym rdzeniem albo bez potwierdzonego powołania, oraz jedna blokada dostawcy (P07, Gemini 4 Argon, W1), która pozostaje w mianowniku 80. 160 odpowiedzi to nie 160 niezależnych obserwacji: te same dziesięć pytań powtarza się u każdego modelu, więc wynik zależy od doboru pytań. Przed cytowaniem liczb: rozdział 8 raportu.</p>
<p>Sprawdzono {spr_n} z {spr_m} powołań we wszystkich odpowiedziach; karta podaje „sprawdzone n z m”.</p>
</section>

<section>{kot("procedura", "Jak sprawdzamy odpowiedzi: karta oceny")}
<ol>
<li>Model (Claude) wypełnia kartę wstępnie: wyszukuje każde powołanie w ISAP, ELI, SAOS, sn.pl albo portalu sądu, porównuje treść z odpowiedzią, proponuje punkty i klasy błędów z dowodami.</li>
<li>Prawnik sprawdza każdą kartę i zatwierdza albo zmienia werdykt. Decyzje graniczne trafiają do rejestru decyzji w specyfikacji z datą, by kolejne karty były oceniane tak samo.</li>
<li>Karta zapisuje wersję specyfikacji, według której ją oceniono, datę i historię zmian. Kart ocenionych według starszej wersji nie porównuje się z nowymi bez przeliczenia.</li>
</ol>
<p>Model wypełniający karty należy do tej samej rodziny co trzy oceniane systemy. Także wśród sędziów-modeli część ocenia odpowiedzi własnej rodziny, a w kilku kartach własne (raport, rozdz. 6). Dlatego każdą kartę sprawdza człowiek, a na tych samych kartach liczymy zgodność z pięcioma sędziami-modelami z trzech rodzin.</p>
</section>

<section>{kot("sedziowie", "Sędziowie-modele i zgodność z kartami")}
<p>Te same odpowiedzi oceniło osobno pięć modeli z dostępem do wyszukiwania, w oddzielnych wywołaniach, według specyfikacji 1.0.1. Dla każdego sędziego liczymy zgodność z kartami i κ Cohena dla etykiety „halucynacja”, osobno dla zbioru pilotażowego (P05–P07, P12, P13) i rozszerzenia (P01, P04, P08–P10), zawsze na kartach, które dany sędzia ocenił (kolumna n). Cztery modele oceniły 147–160 kart; GPT-6 Astra oceniła 49 kart, więc jej κ nie jest porównywalna z pozostałymi. <i>Fałszywy alarm</i> to halucynacja orzeczona przez sędziego tam, gdzie karta jej nie ma; <i>pominięcie</i> odwrotnie.</p>
{SEDZ_HTML}
<p>κ nie dowodzi, że karty są prawdziwe; mówi, na ile inny oceniający dochodzi do tych samych wniosków. Na rozszerzeniu κ czterech sędziów mieści się między 0,58 a 0,90 (79–80 kart), na pilotażu między 0,71 a 0,97 (68–80 kart). Przedziały ufności z bootstrapu po pytaniach i macierze TP/FP/FN/TN są w aneksie E raportu. Sędziowie, którzy mało korzystali z wyszukiwarki, są najmniej zgodni z kartami, a prawie żaden nie przyznaje, czego nie sprawdził. Raport bada też wariant „sędzia z raportem weryfikacji” (karta meta v3), w którym sędzia dostaje raport warstwy weryfikacji jako pomoc, nie werdykt. Zmiana zgodności z kartami: GPT-6.1 Sol κ {pl(L["meta"]["sol61_meta3"]["kb"])} → {pl(L["meta"]["sol61_meta3"]["km"])} na {L["meta"]["sol61_meta3"]["n"]} wspólnych kartach, Gemini 4 Argon {pl(L["meta"]["argon4_meta3"]["kb"])} → {pl(L["meta"]["argon4_meta3"]["km"])} na {L["meta"]["argon4_meta3"]["n"]}; u Argona strata przypada na klasę W, której kod nie umie ustalić.</p>
</section>

<section>{kot("weryfikacja", "Warstwa weryfikacji")}
<p>Obok sędziów działa warstwa weryfikacji w dwóch krokach. <b>Krok faktów</b> to kod: wyciąga powołania z odpowiedzi, próbuje ustalić brzmienie jednostki na dzień stanu prawnego z ISAP/ELI (biblioteka legal-cite-pl) i orzeczenie z SAOS, sprawdza istnienie, identyfikator i brzmienie; przypadki, których nie umie rozstrzygnąć, oznacza jako nieustalone. <b>Ocena poparcia</b> to model, który dostaje tezę z odpowiedzi i tekst źródła i ocenia, czy źródło tę tezę wspiera. Wynik trafia do sędziego jako raport pomocniczy, nigdy jako werdykt wiążący.</p>
<p>Na ośmiu pytaniach poza zbiorem strojenia warstwa wykryła 84 ze 147 błędów z kart (57 %). Większość pominięć to różnice definicji (zawężony zakres normy, który karta liczy jako T) i klasa W: między tekstami jednolitymi k.p.c. weszło w życie zbyt wiele nowelizacji, by kod ustalił brzmienie na dzień. Odsetek fałszywych alarmów, wyniki przed naprawami wejścia i po nich oraz mianowniki podaje rozdział 7 raportu; kod i raporty dla poszczególnych kart są w repozytorium.</p>
</section>

<section>{kot("koszt", "Koszt")}
<p>Dla każdej odpowiedzi liczymy <b>koszt równoważny API</b>: ile kosztowałoby to samo zużycie tokenów i narzędzi według publicznego cennika dostawcy z 18.10.2026. Systemy uruchamiane z subskrypcji (Claude Code, Codex) nie generują tych kwot naprawdę; Vertex AI to koszt faktyczny. Koszt nie wpływa na punkty i nie wchodzi do rankingu jakości.</p>
<p>Metryka pomocnicza: <b>USD na odpowiedź poprawnie ugruntowaną</b>, czyli koszt serii podzielony przez liczbę takich odpowiedzi; przy wskaźniku zawsze pokazujemy koszt serii, liczbę odpowiedzi i oznaczenie dolnej granicy. System bez ani jednej takiej odpowiedzi ma „n/d”, nie „∞”. Przy dziesięciu pytaniach i części kosztów znanych tylko jako dolna granica wskaźnik nie jest oceną opłacalności produktu. Ograniczenia: tokeny z cache liczone tak, jak raportuje narzędzie; Claude Code nie zapisuje liczby wyszukań (w W1 opłata „n/d”, koszt to dolna granica „≥”); skrypt Vertex nie zapisywał tokenów treści z <code>url_context</code>. Pełny koszt badania (odpowiedzi, sędziowie, warstwa weryfikacji) to co najmniej {pl(L["koszt_pelny"])} USD według cennika, bez kosztu pracy prawnika.</p>
</section>

<section>{kot("ograniczenia", "Ograniczenia")}
<ul>
<li><b>Mała próba.</b> Dziesięć pytań, pięć z postępowania cywilnego. Wynik zależy od doboru pytań; 160 odpowiedzi to nie 160 niezależnych obserwacji.</li>
<li><b>Jedna seria.</b> Każdy system uruchomiono raz na pytanie. Nie znamy wariancji między uruchomieniami tego samego modelu; wyniki W0 i W1 pochodzą z różnych dni.</li>
<li><b>Jeden prawnik.</b> Karty sprawdzała jedna osoba. Nie ma zgodności człowiek–człowiek jako punktu odniesienia dla κ sędziów-modeli.</li>
<li><b>Karty wstępnie wypełniał model</b> z rodziny jednego z ocenianych dostawców.</li>
<li><b>Reguły doprecyzowywano w trakcie.</b> Trzy zmiany definicji A6 między 9 a 11.10.2026, kolejne doprecyzowania do 25.10; dwa klucze zmieniono po zebraniu odpowiedzi.</li>
<li><b>Konfiguracje dostawców różnią się</b> (CLI z subskrypcji, API, różne narzędzia wyszukiwania), a część kosztów jest dolną granicą.</li>
<li><b>Pytania są publiczne</b> od października 2026 r., więc kolejne pomiary na tym samym zbiorze mogą być skażone ekspozycją.</li>
<li><b>Skład modeli.</b> Claude Fable 5.1, najnowszy model Anthropic, nie wszedł do serii z 17–18.10.2026: ma tylko pięć odpowiedzi z pilotażu w W0, bez kompletu W1, więc raport go nie obejmuje. Jest zaplanowany na następną serię w obu warunkach. Skład to migawka z października 2026 r.; nowsze wersje modeli nie są w nim ujęte.</li>
</ul>
<p>Z tych powodów wyniki należy czytać jako ilustrację kryteriów, nie ranking. Plan kolejnych edycji: nowe, nieujawnione pytania; klucze zatwierdzone przed zebraniem odpowiedzi i zamrożona specyfikacja; co najmniej trzy biegi na system z przedziałami ufności; drugi prawnik na próbce kart; weryfikacja powołań jako osobny krok przed sędziowaniem.</p>
</section>

<section>{kot("wersje", "Wersjonowanie i identyfikatory")}
<ul>
<li><b>Specyfikacja oceny:</b> 1.0 z 11.10.2026 (po trzech zmianach definicji A6 w dniach 9–11.10); 1.0.1 z tego samego dnia dodaje przykłady graniczne, a karty P06 i P12 przeliczono; 1.0.2 (18.10.2026): koszt, reguły z przeglądu kart rozszerzenia, pole „zakres” halucynacji, blokada dostawcy, soft law; 1.0.3 (25.10.2026): doprecyzowanie pola „zakres”, uzupełnione w kartach pilotażu; 1.0.4 (29.10.2026): nowa nazwa kryterium B2. Od 1.0.1 zasady punktacji nie zmieniły się, dlatego karty podają wersję 1.0.1.</li>
<li><b>Klucze:</b> każdy ma numer wersji, datę i status zatwierdzenia; w Benchmarku 02 wersje od v1 do v4. Zmiany po zebraniu odpowiedzi (P09 v4, P10 v3, 18.10.2026) są opisane.</li>
<li><b>Odpowiedzi:</b> identyfikator <code>Pnn_&lt;system&gt;_&lt;warunek&gt;_r3</code>, data, identyfikator modelu, ustawienia i ślad narzędzi w metadanych.</li>
<li><b>Karty:</b> wersja specyfikacji, data i historia zmian w każdej karcie; stan kart użyty w raporcie: {DATA_KART}.</li>
<li><b>Raport:</b> Benchmark 02 wersja {WERSJA_RAPORTU} z {DATA_RAPORTU}; zmiany w <code>CHANGELOG.md</code> repozytorium.</li>
</ul>
</section>

<section>{kot("kontaminacja", "Kontaminacja i kanarek")}
<p>Każdy klucz, karta, odpowiedź, ocena sędziego i rekord danych zawiera ciąg kanaryjski (konwencja BIG-bench) z prośbą, by nie używać tych plików do treningu modeli. Kanarek pozwala wykryć część przypadków ekspozycji, ale jego niewykrycie nie dowodzi braku kontaminacji. Dlatego opublikowany zbiór traktujemy jako potencjalnie skażony od dnia publikacji, a kolejne edycje opieramy na pytaniach wcześniej nieujawnionych.</p>
</section>

<section>{kot("autorzy", "Autorzy, finansowanie, konflikt interesów")}
<p>Benchmark prowadzi <b>LexAlpha Lab</b>, wspólna inicjatywa badawcza kancelarii <a href="https://www.ktzr.pl/">KTZR</a> (Gdańsk) i spółki <a href="https://lexalpha.pl/">LexAlpha Sp. z o.o.</a> (Warszawa), która rozwija komercyjną platformę AI dla prawników. Autorzy: Adam Piotrowski (radca prawny, partner KTZR; projekt metodologii, klucze, karty, raport) i Andrzej Koman (CEO LexAlpha). Badanie jest finansowane ze środków własnych obu podmiotów.</p><p><b>Konflikt interesów.</b> LexAlpha Sp. z o.o. oferuje komercyjne narzędzia AI dla prawników, zbudowane na modelach językowych tych samych dostawców, których czyste modele ocenia benchmark; spółka ma więc interes gospodarczy związany z wynikami i sposobem ich przedstawiania, a jej CEO jest współautorem raportu. KTZR korzysta z narzędzi tych dostawców na warunkach komercyjnych. Benchmark 02 nie obejmuje własnych produktów obu podmiotów (decyzja z 17.10.2026). W pilotażu Benchmark 01 z września 2026 oceniono trzy moduły LexAlpha i dwa systemy prawnicze innych firm; ich wyników nie publikujemy. Wyłączenie ogranicza bezpośredni konflikt związany z oceną własnego produktu, ale nie usuwa powiązań ekonomicznych autorów. Dlatego oceniamy wyłącznie czyste modele w publicznie dostępnych konfiguracjach, a klucze, karty, odpowiedzi i kod są publiczne, by każdą ocenę można było sprawdzić niezależnie. Wyniki czystych modeli nie mówią nic o jakości produktów LexAlpha ani KTZR; produkt z własnym wyszukiwaniem i instrukcjami wymaga osobnego badania.</p><p><b>Role.</b> Pytania, klucze, kontrolę kart i decyzje o publikacji wykonywał Adam Piotrowski; Andrzej Koman współtworzył raport. Żaden dostawca modeli nie uczestniczył w przygotowaniu badania ani go nie finansował; autorzy nie przekazywali dostawcom wyników przed publikacją. Do 29.10.2026 strona opisywała LexAlpha Lab jako laboratorium kancelarii KTZR; obecny opis odzwierciedla udział obu podmiotów.</p>
</section>
</div>
</div></article>
"""
strona("/metodologia", "Jak oceniamy modele AI w polskim prawie — metodologia · LawBenchmark.pl",
       "Zasady Benchmarku 02: pytania, klucze odpowiedzi, ocena błędów w powołaniach przepisów i orzeczeń, weryfikacja źródeł, sędziowie-modele, warunki badania i ograniczenia.",
       METODOLOGIA, okr=[("Metodologia", None)], tu="/metodologia")

# =====================================================================
# 3. Pytania: lista i strony pytań
# =====================================================================
def klasy_komorka(x):
    if x == "✓":
        return '<span class="kl ok" title="poprawnie ugruntowana">✓</span>'
    if x == "–":
        return '<span class="kl" title="bez halucynacji, ale nie poprawnie ugruntowana">–</span>'
    if x == "blokada":
        return '<span class="kl" title="blokada dostawcy">blokada</span>'
    return "".join(f'<span class="kl bl" title="{E(KL_OPIS.get(k, k))}">{E(k)}</span>' for k in x.split(","))


def statystyka(pid):
    """Z aneksu B: halucynacje i poprawnie ugruntowane per warunek dla pytania."""
    i = PYT.index(pid)
    st = {"W0": {"hal": 0, "pu": 0, "klasy": {}}, "W1": {"hal": 0, "pu": 0, "klasy": {}}}
    for m in MODELE:
        for w in ("W0", "W1"):
            x = ANEKS_H[f"{KROTKA[m]} {w}"][i]
            if x == "✓":
                st[w]["pu"] += 1
            elif x not in ("–", "blokada"):
                st[w]["hal"] += 1
                for k in x.split(","):
                    st[w]["klasy"][k] = st[w]["klasy"].get(k, 0) + 1
    return st


def siatka16(pid, etykiety=True):
    link = etykiety and REPO_URL
    """Inline SVG: 8 modeli × 2 warunki; kolor = wynik odpowiedzi (ugruntowana / bez halucynacji / halucynacja / blokada)."""
    i = PYT.index(pid); k, g = 30, 22
    out = []
    for r, w in enumerate(("W0", "W1")):
        y = 12 + r * g
        out.append(f'<text x="0" y="{y + 4}">{w}</text>')
        for c, m in enumerate(MODELE):
            x = 26 + c * k; v = ANEKS_H[f"{KROTKA[m]} {w}"][i]
            href = f'{REPO_URL}/blob/main/cards/{pid}_{SYSTEM_PLIK[(m, w)]}.md' if link else ""
            if link:
                out.append(f'<a href="{href}" aria-label="karta: {E(m)} {w}">')
            tyt = f"{m} {w}: " + ("poprawnie ugruntowana" if v == "✓" else "bez halucynacji, nie ugruntowana" if v == "–" else "blokada dostawcy" if v == "blokada" else "halucynacja " + v)
            if v == "✓":
                out.append(f'<rect x="{x}" y="{y - 7}" width="18" height="14" rx="3" fill="var(--ok)"><title>{E(tyt)}</title></rect>')
            elif v == "–":
                out.append(f'<rect x="{x + 0.75}" y="{y - 6.25}" width="16.5" height="12.5" rx="3" fill="var(--surface)" stroke="var(--muted)" stroke-width="1.5"><title>{E(tyt)}</title></rect>')
            elif v == "blokada":
                out.append(f'<rect x="{x + 0.75}" y="{y - 6.25}" width="16.5" height="12.5" rx="3" fill="var(--soft)" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="3 2"><title>{E(tyt)}</title></rect>')
            else:
                out.append(f'<rect x="{x}" y="{y - 7}" width="18" height="14" rx="3" fill="var(--bad)"><title>{E(tyt)}</title></rect>')
            if link:
                out.append("</a>")
    if etykiety:
        for c, m in enumerate(MODELE):
            out.append(f'<text x="{26 + c * k + 9}" y="62" text-anchor="middle">{E(KROTKA[m])}</text>')
    return f'<svg class="s16" viewBox="0 0 270 {68 if etykiety else 46}" role="img" aria-label="Wyniki ośmiu modeli w dwóch warunkach dla {pid}">' + "".join(out) + "</svg>"


LEGENDA16 = ('<p class="legenda"><span><i style="background:var(--ok);border-color:var(--ok);border-radius:3px"></i>poprawnie ugruntowana</span>'
             '<span><i style="border-radius:3px"></i>bez halucynacji, nie ugruntowana</span><span><i style="background:var(--bad);border-color:var(--bad);border-radius:3px"></i>z halucynacją</span>'
             '<span><i style="border-style:dashed;border-radius:3px"></i>blokada dostawcy</span><span>Kolumny: modele w kolejności raportu; wiersze: W0 bez narzędzi, W1 z wyszukiwaniem.</span></p>')

PRZYKLAD_PYT = {"P07": f"""<section>{kot("przyklad", "Przykład z kart: Claude Haiku 5.5, bez narzędzi")}
<p>Odpowiedź brzmi „tak” i jest trafna co do kierunku, ale cała dotyczy wyroku i apelacji zamiast postanowienia i zażalenia.</p>
<blockquote class="pyt">„…tydzień od ogłoszenia wyroku. Jeżeli strona nie była obecna przy ogłoszeniu, termin może liczyć się od doręczenia.”</blockquote>
<p>Art. 357 § 5 k.p.c. powołany z treścią, której w nim nie ma (klasy T i F). Ocena samego „tak/nie” uznałaby tę odpowiedź za prawidłową. Sonda z 24 zapytaniami pokazała, że ten wzorzec zależy od sformułowania pytania (raport, rozdz. 5.6).</p>
</section>"""}

LISTA = ['<div class="siatka-pyt">']
for pid in PYT:
    q, t, st = PYTANIA[pid], PYTANIA_T[pid], statystyka(pid)
    LISTA.append(f'<a href="/benchmark/02/pytania/{pid.lower()}" data-trap="{"1" if q["trap"] else "0"}" data-dom="{"proc" if q["domain"] == "proc" else "inne"}"><div><span class="id">{pid} · {E(t[1])} · {"pułapka" if q["trap"] else "bez pułapki"}</span><h2>{E(TYTUL[pid])}</h2>'
                 f'{siatka16(pid, etykiety=False)}<span class="st">halucynacje <b>{st["W0"]["hal"]}</b> → <b>{st["W1"]["hal"]}</b> z&nbsp;8 · poprawnie ugruntowane <b>{st["W0"]["pu"]}</b> → <b>{st["W1"]["pu"]}</b> z&nbsp;8</span><span class="st">średni wynik bloku A: <b>{E(t[8])} %</b></span></div></a>')
LISTA.append("</div>")
PYT_LISTA = f"""
<header class="pod-hero"><div class="wrap">
<h1>Dziesięć pytań Benchmarku 02</h1>
<p class="lead">Pytania użyte w badaniu wraz z wersjami oryginalnymi z praktyki (w trzech pytaniach przed badaniem uzupełniono brakujące dane), z pułapką tam, gdzie ją zastawiono, kluczem odpowiedzi i wynikami ośmiu modeli w dwóch warunkach.</p>
<div class="meta">Stan prawny 1.10.2026 · klucze zatwierdzone w wersjach z 10–18.10.2026 · liczby „W0 → W1” to wynik bez narzędzi i z wyszukiwaniem, z ośmiu modeli</div>
</div></header>
<section><div class="wrap">
<div class="sortuj" role="group" aria-label="Filtr pytań" data-filtr=".siatka-pyt"><span class="eyb">Pokaż</span>
<button type="button" data-f="*" aria-pressed="true">wszystkie</button><button type="button" data-f="trap=1" aria-pressed="false">z pułapką</button><button type="button" data-f="trap=0" aria-pressed="false">bez pułapki</button>
<button type="button" data-f="dom=proc" aria-pressed="false">postępowanie cywilne</button><button type="button" data-f="dom=inne" aria-pressed="false">inne dziedziny</button></div>
{"".join(LISTA)}
{LEGENDA16}
<p class="uwaga" style="margin-top:18px">Pytania są publiczne od października 2026 r. razem z kluczami; kolejne pomiary na tym zbiorze mogą być skażone ekspozycją. Pozostałe 40 pytań puli pozostaje nieujawnione. <a href="/metodologia#kontaminacja">Kontaminacja i kanarek</a>.</p>
</div></section>
"""
LD_PYT_LISTA = {"@context": "https://schema.org", "@type": "ItemList", "name": "Pytania Benchmarku 02",
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f"{pid} · {TYTUL[pid]}", "url": f"{BAZA}/benchmark/02/pytania/{pid.lower()}"} for i, pid in enumerate(PYT)]}
strona("/benchmark/02/pytania", "Dziesięć pytań Benchmarku 02 — LawBenchmark.pl",
       "Dziesięć pytań z polskiego prawa zadanych ośmiu modelom językowym: brzmienie, pułapki, klucze odpowiedzi i wyniki bez narzędzi oraz z wyszukiwaniem.",
       PYT_LISTA, okr=[("Benchmark 02", None), ("Pytania", None)], ld=[LD_PYT_LISTA], tu="/benchmark/02/pytania")

for n, pid in enumerate(PYT):
    q, t, k, st = PYTANIA[pid], PYTANIA_T[pid], KLUCZE_T[pid], statystyka(pid)
    i = PYT.index(pid)
    tresc_pyt = q["text_benchmark"] or q["text_original"]
    wiersze = []
    for m in MODELE:
        for j, w in enumerate(("W0", "W1")):
            a = ANEKS_A[f"{KROTKA[m]} {w}"][i]; h = ANEKS_H[f"{KROTKA[m]} {w}"][i]
            sysid = SYSTEM_PLIK[(m, w)]
            karta = f'<a href="{REPO_URL}/blob/main/cards/{pid}_{sysid}.md">karta</a>' if REPO_URL else f'<span class="muted">{pid}_{sysid}</span>'
            wiersze.append(f'<tr class="{"p0" if j == 0 else "p1"}"><td class="model">{E(m) if j == 0 else ""}</td><td><span class="war {w.lower()}">{w}</span></td>'
                           f'<td class="num">{E(a)}</td><td>{klasy_komorka(h)}</td><td style="font:12px ui-monospace,Menlo,monospace;color:var(--muted)">{karta}</td></tr>')
    kl_w0 = ", ".join(f"{k} {v}" for k, v in sorted(st["W0"]["klasy"].items())) or "brak"
    kl_w1 = ", ".join(f"{k} {v}" for k, v in sorted(st["W1"]["klasy"].items())) or "brak"
    pulapka = (f'<h3>Pułapka</h3><p>{E(q["trap_description"])}</p>' if q["trap"] else
               '<h3>Pułapka</h3><p>Pytanie nie zawiera błędnej przesłanki. Mierzy trafienie w rdzeń i poprawność powołań.</p>')
    kalibracja = (f'<p><b>Oczekiwana kalibracja: warunkowa.</b> {E(q["calibration_condition"])}</p>' if q["expected_calibration"] == "warunkowa"
                  else '<p><b>Oczekiwana kalibracja: kategoryczna.</b> Punkt za kalibrację dostaje odpowiedź, która stawia tezę wprost; rozmycie jasnej tezy bez wskazania, od czego miałaby zależeć, kosztuje punkt.</p>')
    lustro = f'<p>Pytanie jest lustrem <a href="/benchmark/02/pytania/{q["mirror_of"].lower()}">{q["mirror_of"]}</a>: to samo zagadnienie z przeciwną sugestią w pytaniu. Sprzeczność między odpowiedziami tego samego systemu na obie wersje jest karana.</p>' if q["mirror_of"] else ""
    poprz = f'<a href="/benchmark/02/pytania/{PYT[n-1].lower()}">← {PYT[n-1]}</a>' if n > 0 else ""
    nast = f'<a href="/benchmark/02/pytania/{PYT[n+1].lower()}">{PYT[n+1]} →</a>' if n < len(PYT) - 1 else ""
    PYT_STRONA = f"""
<header class="pod-hero"><div class="wrap">
<h1>{pid} · {E(TYTUL[pid])}</h1>
<p class="lead">{E(t[1])} · pytanie {E(TYP_OPIS.get(q["type"], q["type"]))} · {"z pułapką" if q["trap"] else "bez pułapki"} · klucz v{q["key_version"]} z {E(q["key_date"])} · stan prawny 1.10.2026</p>
<div style="max-width:320px;margin:6px 0 4px">{siatka16(pid)}</div>
<p class="leg16"><i style="background:var(--ok)"></i>poprawnie ugruntowana<i style="border:1.5px solid var(--muted)"></i>bez halucynacji<i style="background:var(--bad)"></i>z halucynacją · wiersze: W0 bez narzędzi, W1 z wyszukiwaniem</p>
</div></header>
<article><div class="wrap">
<section>{kot("pytanie", "Pytanie w brzmieniu użytym w badaniu")}
<blockquote class="pyt">{E(tresc_pyt)}</blockquote>
{('<p class="uwaga">Tekst oryginalny prawnika: „' + E(q["text_original"]) + '”. Wersja benchmarkowa uzupełnia dane potrzebne do jednoznacznego klucza; literówki oryginału zostają.</p>') if q["text_benchmark"] and q["text_original"] and q["text_benchmark"].strip() != q["text_original"].strip() else '<p class="uwaga">Brzmienie oryginalne, tak jak prawnik wpisał je do czatu; literówki zachowane.</p>'}
{pulapka}
{lustro}
</section>
<section>{kot("klucz", "Prawidłowa odpowiedź według klucza")}
<p><b>Rdzeń odpowiedzi.</b> {E(k[3])}</p>
<p><b>Podstawy wymagane.</b> {E(k[4])}</p>
{kalibracja}
<p class="uwaga">Pełny klucz (rubryka, kary, wzorce cytatów ze źródła, orzeczenia znane) jest w repozytorium w pliku <code>{E(q["key_file"])}</code>. Każda podstawa została sprawdzona w tekście urzędowym na dzień stanu prawnego. <a href="/metodologia#klucze">Zasady klucza</a>.</p>
</section>
<section>{kot("wyniki", "Wyniki ośmiu modeli")}
<div class="fakty">
<div><b>Odpowiedzi z halucynacją (z 8)</b>W0: {st["W0"]["hal"]} · W1: {st["W1"]["hal"]}</div>
<div><b>Poprawnie ugruntowane (z 8)</b>W0: {st["W0"]["pu"]} · W1: {st["W1"]["pu"]}</div>
<div><b>Klasy błędów W0</b>{E(kl_w0)}</div>
<div><b>Klasy błędów W1</b>{E(kl_w1)}</div>
<div><b>Średni wynik bloku A (16 odpowiedzi)</b>{E(t[8])} %</div>
<div><b>Pełny rdzeń (A-R = 2)</b>{E(t[7])} z 16</div>
</div>
<div class="scroll"><table class="pary"><thead><tr><th>Model</th><th>Warunek</th><th class="num">Blok A <small>%</small></th><th>Wynik</th><th>Karta</th></tr></thead><tbody>
{"".join(wiersze)}
</tbody></table></div>
{LEGENDA16}
<p class="legenda" style="display:block"><span class="kl ok">✓</span> poprawnie ugruntowana · <span class="kl">–</span> bez halucynacji, ale rdzeń niepełny albo brak sprawdzonego źródła · <span class="kl bl">T</span> <span class="kl bl">W</span> <span class="kl bl">F</span> <span class="kl bl">S</span> klasy błędu w odpowiedzi z halucynacją (<a href="/metodologia#halucynacja">definicje</a>) · <span class="kl">blokada</span> tekst zablokowany przez filtr dostawcy, bez etykiety · blok A = kryteria sprawdzane wobec klucza i źródła (<a href="/metodologia#karta">kryteria oceny</a>)</p>
<p class="uwaga">Liczby dotyczą jednej odpowiedzi każdego modelu na to pytanie w każdym warunku. Nie mówią nic o wariancji między uruchomieniami ani o innych pytaniach z tej dziedziny.</p>
</section>
{PRZYKLAD_PYT.get(pid, "")}
<p style="display:flex;justify-content:space-between;font:14px var(--sans);margin-top:24px"><span>{poprz}</span><a href="/benchmark/02/pytania">wszystkie pytania</a><span>{nast}</span></p>
</div></article>
"""
    strona(f"/benchmark/02/pytania/{pid.lower()}", f"{TYTUL[pid]} — {pid} · LawBenchmark.pl",
           f"Pytanie {pid} Benchmarku 02 ({t[1]}): brzmienie, {'pułapka, ' if q['trap'] else ''}klucz odpowiedzi i wyniki ośmiu modeli językowych bez narzędzi i z wyszukiwaniem.",
           PYT_STRONA, okr=[("Benchmark 02", None), ("Pytania", "/benchmark/02/pytania"), (pid, None)], tu="/benchmark/02/pytania")

# =====================================================================
# 3b. Benchmark 01 — kazus SKD (pilotaż; decyzje Adama z 29.10.2026)
# =====================================================================
K01 = os.path.join(REPO, "cases", "skd-01")
W01 = json.load(open(os.path.join(K01, "wyniki.json"), encoding="utf-8"))["wyniki"]
KAZUS_TXT = re.sub(r"\n*<!--.*?-->\s*$", "", open(os.path.join(K01, "kazus_01_termin.md"), encoding="utf-8").read(), flags=re.S).strip()


def pct(x):
    return f"{x} %"


def wiersz01(r):
    hal = (f'<span class="kl bl">tak</span> {E(r["A6_klasy"])}' if r["halucynacja"] else '<span class="kl ok">nie</span>')
    pkt = lambda v: (f"{v:g}".replace(".", ","))
    return (f'<tr><td class="model">{E(r["model"])}<br><small>{E(r["dostawca"])} · {E(r["interfejs"])}</small></td><td>{E(r["warunek"])}</td>'
            f'<td class="num">{pkt(r["A_pkt"])}/8 · {r["A_pct"]} %</td><td class="num">{pkt(r["B_pkt"])}/7 · {r["B_pct"]} %</td><td class="num">{r["delta_pp"]:+d}</td>'
            f'<td>{hal}</td><td><a href="{REPO_URL}/blob/main/{r["plik_karty"]}">karta</a> · <a href="{REPO_URL}/blob/main/{r["plik_odpowiedzi"]}">odpowiedź</a></td></tr>')


GLOWA01 = ('<div class="scroll"><table class="t"><thead><tr><th>Model</th><th>Warunek</th><th class="num">Blok A</th><th class="num">Blok B</th>'
           '<th class="num">Δ A−B <small>pp</small></th><th>Halucynacja (wg karty)</th><th>Materiały</th></tr></thead><tbody>')
PRZ01 = sorted([r for r in W01 if r["status_oceny"].startswith("przejrzana")], key=lambda r: -r["A_pct"])
WST01 = sorted([r for r in W01 if not r["status_oceny"].startswith("przejrzana")], key=lambda r: (r["model"].split()[0], -r["A_pct"]))
TAB01_P = GLOWA01 + "".join(wiersz01(r) for r in PRZ01) + "</tbody></table></div>"
TAB01_W = GLOWA01 + "".join(wiersz01(r) for r in WST01) + "</tbody></table></div>"
n_hal_p = sum(1 for r in PRZ01 if r["halucynacja"])
n_hal_w = sum(1 for r in WST01 if r["halucynacja"])

BENCH01 = f"""
<header class="pod-hero"><div class="wrap">
<h1>Kazus SKD: termin na oświadczenie o sankcji kredytu darmowego</h1>
<p class="lead">Benchmark 01, pilotaż z września i października 2026 r. Jeden fikcyjny kazus procesowy i {len(W01)} odpowiedzi modeli ogólnych w różnych konfiguracjach, w tym powtórzenia, ocenione według metryki pilotażu, czyli jego własnych kryteriów i zasad punktacji.</p>
<div class="meta">Dzień oświadczenia konsumenta w kazusie: maj 2026 · statusy spraw w toku ustalone 13.09.2026 · karty z 13.09 i 8–9.10.2026 · metryka pilotażu A1–A8 i B1–B2</div>
</div></header>
<article><div class="wrap">
<p class="wer"><b>To pilotaż, nie część Benchmarku 02.</b> Kazus oceniano inną metryką i w różnych interfejsach, więc jego liczb nie należy porównywać z wynikami dziesięciu pytań. Pięć kart przejrzał prawnik we wrześniu 2026; {len(WST01)} kart z 8–9.10.2026 to oceny wstępne wypełnione przez model, oznaczone w tabeli i w każdej karcie. W pilotażu oceniono też pięć systemów prawniczych: trzy moduły LexAlpha, współorganizatora projektu, i dwa systemy innych firm. Ich wyniki pozostają poza tą publikacją.</p>

<section>{kot("kazus", "Kazus")}
<p>Stan faktyczny i polecenie w brzmieniu, w jakim trafiły do systemów (literówki zachowane). Kazus jest fikcyjny.</p>
<blockquote class="pyt" style="white-space:pre-wrap;font-size:16px">{E(KAZUS_TXT)}</blockquote>
</section>

<section>{kot("co-mierzy", "Co mierzy kazus")}
<p>Polecenie każe skupić się wyłącznie na terminie z art. 45 ust. 5 ustawy o kredycie konsumenckim, a kwestię kredytowanych kosztów uwzględnić tylko wtedy, gdy wpływa na termin. Ocena naliczania odsetek od kredytowanych kosztów może wpływać na istnienie zaległości, a przez to na skuteczność wypowiedzenia. Znaczenie wypowiedzenia dla początku terminu zależy z kolei od przyjętej wykładni „wykonania umowy” w art. 45 ust. 5 u.k.k. Zadanie wymaga rozpoznania tej zależności, a nie samego wykonania polecenia. Do tego dochodzą daty miarodajne dla poszczególnych zdarzeń, dosłowne cytaty przepisów i wskazanie zagadnień spornych.</p>
</section>

<section>{kot("metryka", "Metryka pilotażu")}
<div class="scroll"><table class="t"><thead><tr><th>Kryterium</th><th>Pytanie</th><th>Punkty</th></tr></thead><tbody>
<tr><td><b>A1</b></td><td>Czy dobrze ustalono datę, na jaką należy ustalić treść przepisów, osobno dla każdego zdarzenia?</td><td>0/1</td></tr>
<tr><td><b>A2</b></td><td>Czy wskazano przepisy mające zastosowanie, w tym art. 75 ust. 1 Prawa bankowego i art. 385¹ k.c.?</td><td>0/1</td></tr>
<tr><td><b>A3</b></td><td>Czy cytaty przepisów są dosłowne albo oznaczone jako fragment?</td><td>0/1</td></tr>
<tr><td><b>A4</b></td><td>Czy model zauważył, że dla terminu istotne są kredytowane koszty, i nazwał mechanizm wpływu?</td><td>0/1</td></tr>
<tr><td><b>A5</b></td><td>Czy uczciwie wskazano, które zagadnienia są sporne?</td><td>0/1</td></tr>
<tr><td><b>A6</b></td><td>Czy odpowiedź nie powołuje źródeł zmyślonych albo z cudzą treścią? Od 11.10.2026 zero-jedynkowo, z klasami F, T, W, S jak w Benchmarku 02.</td><td>0/1</td></tr>
<tr><td><b>A7</b></td><td>Czy model odpowiedział na wszystkie punkty polecenia, w wymaganym formacie?</td><td>0/1</td></tr>
<tr><td><b>A8</b></td><td>Czy model nie wykroczył poza ramy zadania?</td><td>0/1</td></tr>
<tr><td><b>B1</b></td><td>Analiza stanowiska konsumenta i banku, osobno: brak, streszczenie albo analiza argumentów.</td><td>0–2 na stronę</td></tr>
<tr><td><b>B2</b></td><td>Wskazanie, które stanowisko ma większe szanse: bez uzasadnienia, z uzasadnieniem powierzchownym albo z wywodem opartym na orzecznictwie i doktrynie.</td><td>0–3</td></tr>
</tbody></table></div>
<p>Blok A ma 8 punktów, więc jeden punkt to 12,5 punktu procentowego; blok B ma 7 punktów. Bloków nie sumujemy. Różnica Δ = A − B, liczona z zaokrąglonych procentów, pokazuje rozbieżność między argumentacją a spełnieniem kryteriów bloku A; jej przyczynę widać w karcie. Etykieta „halucynacja” wynika z A6 = 0. Klasy błędu: F, źródło nie istnieje; T, prawdziwe źródło z treścią, której w nim nie ma; W, brzmienie z innej daty; S, zniekształcony identyfikator. „S (niepotwierdzona)” oznacza, że sygnatury nie odnaleziono, ale nie przesądzono, czy to zniekształcenie, czy zmyślenie. Pełna metryka: plik <code>METRYKI.md</code> w repozytorium.</p>
</section>

<section>{kot("wyniki", "Wyniki")}
<h3>Karty przejrzane przez prawnika</h3>
<p>Odpowiedzi z aplikacji czatu dostawców, karty z 13.09.2026, przejrzane przez prawnika we wrześniu. Halucynację oznaczono w {n_hal_p} z {len(PRZ01)} odpowiedzi. Liczby różnią się od artykułu z września z dwóch powodów: 11.10.2026 karty przeliczono według zatwierdzonej przez prawnika reguły zero-jedynkowego A6, a 29.10.2026 prawnik uznał sygnaturę „wyrok SA w Warszawie z 10 maja 2022 r., V ACa 810/21” za nieistniejącą (klasa F): nie ma jej w SAOS, w wewnętrznej bazie orzeczeń ani na portalu orzeczeń SA w Warszawie. Historia zmian jest w każdej karcie.</p>
{TAB01_P}
<h3 style="margin-top:28px">Oceny wstępne, nieprzejrzane przez prawnika</h3>
<p>Odpowiedzi zebrane 8–9.10.2026 skryptami: GPT-6.1 Sol przez Codex CLI oraz modele otwarte przez Ollama. Karty wypełnił model (Claude); halucynację oznaczono w {n_hal_w} z {len(WST01)}. Wyniki mogą się zmienić po przeglądzie prawnika.</p>
{TAB01_W}
<p class="uwaga">Jedna odpowiedź na system i warunek. Warianty „powtórzenie” to druga próba tego samego modelu w tych samych warunkach, pokazana, żeby było widać zmienność między próbami. Odpowiedź GPT-6.1 Sol bez narzędzi z włączonymi aplikacjami konta ChatGPT pominęliśmy, bo aplikacje dawały dostęp do wyszukiwarki.</p>
</section>

<section>{kot("klucz", "Klucz w skrócie")}
<ul>
<li><b>Daty miarodajne:</b> abuzywność postanowień według chwili zawarcia umowy (czerwiec 2022, art. 385² k.c.); skuteczność wypowiedzenia według grudnia 2024; art. 45 ust. 5 u.k.k. z uzasadnieniem wyboru daty (przepis nie zmienił się od 2011 r.).</li>
<li><b>Przepisy wymagane:</b> art. 45 ust. 1 i 5 u.k.k., art. 75 ust. 1 Prawa bankowego, art. 385¹ § 1 k.c.</li>
<li><b>Sporne na dzień oświadczenia (maj 2026):</b> od czego biegnie termin z art. 45 ust. 5 u.k.k. (wykonanie przez kredytodawcę, przez obie strony czy wypowiedzenie; zagadnienie prawne III CZP 15/25 zawieszone); czy konsument mógł sam obniżyć raty bez orzeczenia o abuzywności; czy wypowiedzenie jest „wykonaniem” umowy.</li>
<li><b>Orzecznictwo:</b> wyrok TSUE C-744/24 z 23.04.2026 dotyczy oprocentowania kredytowanych kosztów i nie rozstrzyga o terminie; pytania prejudycjalne C-763/25 i C-828/25 dotyczące terminu były w toku według stanu z 13.09.2026.</li>
</ul>
<p class="uwaga">Klucz opisuje stan z 13.09.2026 i nie był później aktualizowany. Sprawy wówczas w toku mogły zostać rozstrzygnięte; kazus nie jest opisem obecnej linii orzeczniczej i nie jest poradą prawną.</p>
</section>

<section>{kot("dane", "Dane")}
<p>Kazus, klucz, metryka pilotażu, {len(W01)} odpowiedzi i kart oraz zestawienie <code>wyniki.json</code> są w repozytorium w katalogu <a href="{REPO_URL}/tree/main/cases/skd-01"><code>cases/skd-01/</code></a> na licencji jak reszta zbioru (<a href="/dane#licencje">licencje</a>). Każdy plik zawiera kanarek, czyli unikalny ciąg znaków, po którym można wykryć część przypadków użycia tych danych do trenowania modeli. Kazus jest teraz publiczny, więc nie nadaje się już do testowania nowych modeli.</p>
</section>
</div></article>
"""
LD_B01 = {"@context": "https://schema.org", "@type": "Dataset", "@id": f"{BAZA}/benchmark/01#dataset",
          "name": "LawBenchmark.pl Benchmark 01: kazus SKD (pilotaż)", "inLanguage": "pl", "datePublished": "2026-10-29",
          "description": f"Fikcyjny kazus o terminie na oświadczenie o sankcji kredytu darmowego (art. 45 ust. 5 u.k.k.), klucz, metryka pilotażu oraz {len(W01)} odpowiedzi modeli ogólnych z kartami ocen; 12 kart wstępnych.",
          "url": f"{BAZA}/benchmark/01", "isAccessibleForFree": True, "license": "https://creativecommons.org/licenses/by/4.0/",
          "creator": [{"@type": "Person", "name": "Adam Piotrowski"}, {"@type": "Person", "name": "Andrzej Koman"}],
          "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{REPO_URL}/blob/main/cases/skd-01/wyniki.json"}]}
strona("/benchmark/01", "Kazus SKD: termin na oświadczenie o sankcji kredytu darmowego — Benchmark 01 · LawBenchmark.pl",
       "Pilotaż: jak modele językowe analizują fikcyjny kazus o terminie z art. 45 ust. 5 u.k.k. Treść kazusu, metryka, wyniki 17 odpowiedzi modeli ogólnych, klucz i dane.",
       BENCH01, okr=[("Benchmark 01", None), ("Kazus SKD", None)], ld=[LD_B01], tu="/benchmark/01")

# =====================================================================
# 4. Raporty
# =====================================================================
LD_RAPORT = {"@context": "https://schema.org", "@type": "Report", "name": "LexAlpha Lab · Benchmark 02 · pytania prawne", "version": WERSJA_RAPORTU,
             "datePublished": "2026-10-29", "inLanguage": "pl", "url": f"{BAZA}/reports/lexalpha_lab_benchmark_02.pdf", "encodingFormat": "application/pdf",
             "author": [{"@type": "Person", "name": "Adam Piotrowski"}, {"@type": "Person", "name": "Andrzej Koman"}],
             "publisher": {"@type": "Organization", "name": "LexAlpha Lab, KTZR"}, "license": "https://creativecommons.org/licenses/by/4.0/"}
LD_ART = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": "\"Hallucination\" Is Not Enough: Why Legal LLM Benchmarks Should Measure \"Correctly Grounded\"",
          "version": "1.2", "datePublished": "2026-10-26", "inLanguage": "en", "identifier": "https://doi.org/10.5281/zenodo.23674794", "sameAs": ["https://doi.org/10.5281/zenodo.23674794", "https://papers.ssrn.com/abstract=7672779"],
          "author": {"@type": "Person", "name": "Adam Piotrowski"}, "publisher": {"@type": "Organization", "name": "LexAlpha Lab, KTZR"}, "license": "https://creativecommons.org/licenses/by/4.0/"}
RAPORTY = f"""
<header class="pod-hero"><div class="wrap">
<h1>Raporty</h1>
<p class="lead">Raport z Benchmarku 02 po polsku i artykuł metodologiczny po angielsku. Pliki PDF do pobrania; teksty źródłowe raportu i skrypt liczący każdą liczbę są w repozytorium.</p>
</div></header>
<article><div class="wrap">
<section>{kot("benchmark-02", "Benchmark 02 · pytania prawne (raport, PL)")}
<p><b>Piotrowski A., Koman A.</b> (2026). <i>LexAlpha Lab · Benchmark 02 · pytania prawne.</i> Wersja {WERSJA_RAPORTU}, {DATA_RAPORTU} (1.0: 27.10.2026; 1.1 dodaje odniesienie do badania UJ we wstępie i literaturze). <a class="btn s" href="/reports/lexalpha_lab_benchmark_02.pdf">PDF</a></p>
<p><b>Zakres.</b> Osiem modeli trzech dostawców (OpenAI, Anthropic, Google), dziesięć pytań z polskiego prawa, dwa warunki (bez narzędzi i z wyszukiwaniem w internecie), 160 odpowiedzi; {spr_n} z {spr_m} powołań sprawdzonych w źródle urzędowym na dzień 1.10.2026.</p>
<p><b>Główne ustalenia.</b> Odpowiedzi z halucynacją: {L["hal_W0"]} z 80 bez narzędzi, {L["hal_W1"]} z 80 z wyszukiwaniem; poprawnie ugruntowanych {L["pu_W0"]} i {L["pu_W1"]}. Najczęstsza klasa błędu to prawdziwy przepis albo orzeczenie z treścią, której w nim nie ma ({L["klasa_T"]} odpowiedzi), a za nią dawne brzmienie podane jako obowiązujące ({L["klasa_W"]}); zmyślone źródła są rzadkie ({L["klasa_F"]}), zniekształcone identyfikatory też ({L["klasa_S"]}); jedna odpowiedź może mieć kilka klas. W tej serii w W1 odnotowano mniej odpowiedzi z halucynacją u pięciu z ośmiu modeli, a u trzech tyle samo; koszt serii w W1 był od {pl(min(L["krotnosc_kosztu"].values()))} do {pl(max(L["krotnosc_kosztu"].values()))} razy wyższy niż w W0 (część kosztów W1 znana tylko jako dolna granica). Jedna seria z różnych dni nie pozwala oddzielić wpływu narzędzi od zmienności odpowiedzi. Czterech sędziów-modeli ocenianych na pełnym zbiorze osiąga κ od 0,58 do 0,90 z kartami (piąty, GPT-6 Astra, 0,95 na 43 kartach pilotażu); raport weryfikacji podany sędziemu jako pomoc poprawia surowego sędziego i pogarsza łagodnego.</p>
<p><b>Spis treści.</b> 1 Wstęp · 2 Zbiór pytań: dziesięć pytań z praktyki, klucze zatwierdzane przed biegiem (klucze P09 i P10 zmieniono po zebraniu odpowiedzi, zob. <a href="/metodologia#klucze">metodologia</a>) · 3 Systemy i warunki biegu · 4 Metoda oceny · 5 Wyniki modeli · 6 Sędziowie-modele · 7 Warstwa weryfikacji · 8 Ograniczenia · 9 Wnioski i dalsze kroki · aneksy A–E (pytania i klucze w skrócie, wyniki pytanie × system, sędziowie: zgodność i ustawienia, słownik pojęć, macierze pomyłek i przedziały niepewności dla każdej κ).</p>
<pre>{E(BIBTEX)}</pre>
</section>
<section>{kot("correctly-grounded", "„Hallucination” Is Not Enough (artykuł metodologiczny, EN)")}
<p><b>Piotrowski A.</b> (2026). <i>„Hallucination” Is Not Enough: Why Legal LLM Benchmarks Should Measure „Correctly Grounded”.</i> LexAlpha Lab, working paper v1.2, 26.10.2026, 37 stron (tekst nierecenzowany). <a href="https://doi.org/10.5281/zenodo.23674794">doi:10.5281/zenodo.23674794</a> · <a href="https://papers.ssrn.com/abstract=7672779">SSRN 7672779</a> · <a href="https://www.ktzr.pl/legal-llm-benchmarks-correctly-grounded/">pełny tekst na ktzr.pl</a> · <a class="btn s" href="/reports/Piotrowski_2026_correctly_grounded_v1.2.pdf">PDF</a></p>
<p><b>O czym jest.</b> Artykuł uzasadnia metrykę używaną na tej stronie. Etykieta „halucynacja” mierzy tylko, czy model powiedział coś nieprawdziwego o prawie; nie mówi, czy odpowiedź jest kompletna ani na czym ją oparł. Artykuł proponuje miarę „correctly grounded” (pełny rdzeń, brak fałszywych powołań, co najmniej jedno powołanie sprawdzone u źródła) i typologię błędów F/T/W/S z pochodzeniem błędu, a na kartach z pilotażu pokazuje, jak sędziowie-modele oceniają wiarygodność odpowiedzi zamiast jej prawdziwości i jak raport weryfikacji zmienia ich werdykty. Zawiera κ sędziów z macierzami i przedziałami ufności oraz pełną specyfikację oceny. Autor uzasadnia też, dlaczego taka miara jest potrzebna zwłaszcza w systemach prawa stanowionego.</p>
<pre>{E(BIBTEX_ART)}</pre>
</section>
<section>{kot("inne-badania", "Inne badania modeli językowych w polskim prawie")}
<p><b>Porębski A., Figura J.</b> (Uniwersytet Jagielloński). <i>Free LLMs Hallucinate and Rarely Signal Their Limitations in Solving Legal Problems</i>. W: <i>Progress in Polish Artificial Intelligence Research 6</i>, Wyd. Uniwersytetu Śląskiego, 2025, s. 294–300. <a href="https://doi.org/10.2139/ssrn.5188654">SSRN</a> · <a href="https://ruj.uj.edu.pl/entities/publication/d5ecab2b-1542-420f-8181-090c05e93a8b">pełny tekst (RUJ)</a> · <a href="https://doi.org/10.57903/UJ/2XPZKE">zbiór danych (RODBUK, 2026)</a>.</p>
<p>Najbliższe wcześniejsze badanie empiryczne: 12 poleceń po polsku z prawa konstytucyjnego, karnego i spadkowego, z założeniem prawdziwym albo fałszywym, zadanych w styczniu 2025 r. pięciokrotnie dwóm darmowym modelom (GPT-4o mini, Bielik-11B-v2); 120 odpowiedzi ocenionych przez dwóch oceniających, osobno sprawdzonych 369 powołanych orzeczeń. Główna część odpowiedzi trafna w 91 ze 120 przypadków; z 369 orzeczeń 16 zgodnych co do sądu i daty, 8 na temat pytania, 280 z sygnaturą istniejącą pod inną sprawą (liczby przeliczone z opublikowanych arkuszy). Autorzy nie wliczali powołań do oceny trafności; nasza miara „poprawnie ugruntowane” łączy obie osie w jedną etykietę. Wzorzec błędów jest zbieżny z naszym: identyfikator istnieje, sprawa albo treść jest cudza, czyste zmyślenie jest rzadsze.</p>
<p class="uwaga">Znasz inne opublikowane badanie modeli językowych na polskim prawie z jawną metodą oceny? Napisz: a.piotrowski@ktzr.pl.</p>
</section>
</div></article>
"""
strona("/raporty", "Raporty — LawBenchmark.pl",
       "Raport LexAlpha Lab Benchmark 02 (PL, PDF) i artykuł metodologiczny „Hallucination Is Not Enough” (EN, DOI): streszczenia, główne ustalenia, cytowanie.",
       RAPORTY, okr=[("Raporty", None)], ld=[LD_RAPORT, LD_ART], tu="/raporty")

# =====================================================================
# 5. Dane i kod
# =====================================================================
LD_DATASET = {"@context": "https://schema.org", "@type": "Dataset", "@id": f"{BAZA}/dane#benchmark-02",
              "name": "LawBenchmark.pl · Benchmark 02 · pytania prawne (dane)", "version": WERSJA_RAPORTU, "datePublished": "2026-10-27", "inLanguage": "pl",
              "description": "10 pytań z polskiego prawa z kluczami oceny, 160 odpowiedzi 8 modeli językowych (bez narzędzi i z wyszukiwaniem), 160 kart wzorcowych z klasami błędów F/T/W/S, 1 319 ocen pięciu sędziów-modeli i 2 184 rekordy warstwy weryfikacji powołań.",
              "url": f"{BAZA}/dane", "isAccessibleForFree": True, "license": "https://creativecommons.org/licenses/by/4.0/",
              "creator": [{"@type": "Person", "name": "Adam Piotrowski"}, {"@type": "Person", "name": "Andrzej Koman"}],
              "publisher": {"@type": "Organization", "name": "LexAlpha Lab, KTZR", "url": "https://www.ktzr.pl/"},
              "keywords": ["modele językowe", "polskie prawo", "halucynacje", "benchmark", "LLM", "legal AI", "Polish law"],
              "temporalCoverage": "2026-10-01", "spatialCoverage": {"@type": "Place", "name": "Polska"}}
if REPO_URL:
    LD_DATASET["distribution"] = [{"@type": "DataDownload", "encodingFormat": "application/jsonl", "contentUrl": f"{REPO_URL}/blob/main/data/{p}.jsonl"}
                                  for p in ("questions", "keys", "answers", "cards", "judgments", "verification")]
    LD_DATASET["sameAs"] = [REPO_URL] + ([HF_URL] if HF_URL else [])
repo_tekst = (f'Repozytorium: <a href="{REPO_URL}">{REPO_URL}</a>.' if REPO_URL else
              'Repozytorium: dostępne na prośbę do czasu upublicznienia.')
DANE = f"""
<header class="pod-hero"><div class="wrap">
<h1>Dane i kod</h1>
<p class="lead">Wszystko, co stoi za liczbami: specyfikacja oceny, klucze, odpowiedzi, karty, oceny sędziów, raporty warstwy weryfikacji, koszty i skrypty. Skrypty przeliczają tabele raportu i tej strony z zapisanych kart, ocen sędziów i danych kosztowych.</p>
<div class="meta">Benchmark 02, wersja danych {WERSJA_RAPORTU} ({DATA_RAPORTU}) · CC BY 4.0 (materiał własny) · MIT (kod) · {repo_tekst}</div>
</div></header>
<article><div class="wrap">
<section>{kot("zawartosc", "Co jest w zbiorze")}
<div class="scroll"><table class="t"><thead><tr><th>Katalog</th><th>Zawartość</th><th class="num">Rekordy</th></tr></thead><tbody>
<tr><td><code>SPEC/</code></td><td>specyfikacja oceny v1.0.4 (punktacja jak w 1.0.1) z rejestrem datowanych decyzji (dokument wewnętrzny w postaci użytej, po przeglądzie pod kątem danych osobowych i wewnętrznych identyfikatorów)</td><td class="num">1</td></tr>
<tr><td><code>keys/</code></td><td>klucze dziesięciu pytań: rdzeń, rubryka, kary, podstawy wymagane, źródła sprawdzone, wersja i status</td><td class="num">10</td></tr>
<tr><td><code>answers/</code></td><td>odpowiedzi systemów w postaci zwróconej, ze śladem narzędzi tam, gdzie narzędzie go zapisuje</td><td class="num">160</td></tr>
<tr><td><code>cards/</code></td><td>karty wzorcowe: punkty A/B, klasy błędów, pochodzenie i zakres, każde powołanie sprawdzone, data wersji</td><td class="num">160</td></tr>
<tr><td><code>judges/</code></td><td>oceny pięciu sędziów-modeli oraz wariantów „sędzia z raportem weryfikacji”</td><td class="num">1 319</td></tr>
<tr><td><code>verification/</code></td><td>raporty warstwy weryfikacji: krok faktów (kod) i weryfikator poparcia (model), per karta i zbiorcze</td><td class="num">2 184</td></tr>
<tr><td><code>costs/</code></td><td>cennik z 18.10.2026 ze źródłami i koszt na odpowiedź (równoważnik API)</td><td class="num">—</td></tr>
<tr><td><code>cases/skd-01/</code></td><td>Benchmark 01 (pilotaż): kazus SKD, klucz, metryka pilotażu, 17 odpowiedzi modeli ogólnych i ich karty, <code>wyniki.json</code>; 12 kart oznaczonych jako wstępne</td><td class="num">17</td></tr>
<tr><td><code>data/</code></td><td>warstwa maszynowa: <code>questions</code>, <code>keys</code>, <code>answers</code>, <code>cards</code>, <code>judgments</code>, <code>verification</code> jako JSONL (pola po angielsku, treść po polsku) z kartą zbioru</td><td class="num">6 plików</td></tr>
<tr><td><code>reports/</code></td><td>raport Benchmark 02 (PDF, HTML, źródła Markdown, <code>dane.py</code>) i artykuł v1.2</td><td class="num">2</td></tr>
<tr><td><code>tools/</code></td><td>skrypty biegów systemów i sędziów, porównanie sędziów z kartami, warstwa weryfikacji, eksport JSONL, budowa tej strony</td><td class="num">—</td></tr>
</tbody></table></div>
</section>
<section>{kot("hugging-face", "Zbiór na Hugging Face")}
<p>Ta sama warstwa maszynowa jest dostępna jako zbiór <a href="{HF_URL}">LexAlphaLab/lawbenchmark-b02</a> na Hugging Face: sześć tabel (karty, odpowiedzi, pytania, klucze, oceny sędziów, warstwa weryfikacji) jako zbiór testowy. Pobranie wymaga zaakceptowania krótkiej informacji z prośbą, by nie trenować modeli na tych danych; akceptacja jest automatyczna. Pliki w repozytorium GitHub są dostępne bez bramki.</p>
<pre>from datasets import load_dataset
cards = load_dataset("LexAlphaLab/lawbenchmark-b02", "cards", split="test")</pre>
</section>
<section>{kot("odtworzenie", "Jak odtworzyć wyniki")}
<ol>
<li>Tabele raportu i tej strony: <code>python3 -I reports/benchmark-02/src/dane.py</code> — czyta <code>cards/</code>, <code>keys/</code>, <code>judges/</code>, <code>costs/</code> i przelicza z nich każdą tabelę.</li>
<li>Warstwa JSONL: <code>python3 -I tools/export_jsonl.py</code> — odbudowuje <code>data/</code> ze źródeł i sprawdza sumy z <code>dane.py</code>.</li>
<li>Sędziowie wobec kart: <code>python3 -I tools/porownaj_sedziow.py argon4v101</code> (identyfikatory: <code>argon4v101</code>, <code>sol61v101</code>, <code>gemini31v101</code>, <code>gemini38flashv101</code>, <code>astra6v101</code>).</li>
<li>Własna seria odpowiedzi na pytaniach: <code>tools/eval_*.py</code> — wymaga CLI dostawcy albo dostępu do Vertex AI. Powtórzenie serii nie odtworzy odpowiedzi z badania: modele, ich konfiguracje i wyniki wyszukiwania zmieniają się w czasie.</li>
<li>Warstwa weryfikacji (<code>tools/verification/</code>) potrzebuje biblioteki <a href="https://github.com/apiotrowski-afk/legal-cite-pl">legal-cite-pl</a> do odczytu ISAP/ELI.</li>
</ol>
<p>Skrypty są w repozytorium w postaci użytej; ścieżki zamieniono na względne. Nazwy robocze systemów w plikach (np. <code>chatgpt_codex</code> = GPT-6.1 Sol, <code>argon4_high_vertex</code> = Gemini 4 Argon) są rozpisane w README repozytorium i w aneksie D raportu.</p>
</section>
<section>{kot("licencje", "Licencje i kanarek")}
<ul>
<li><b>Materiał własny</b> (specyfikacja, pytania w brzmieniu benchmarkowym, klucze, karty, instrukcje sędziów, raporty warstwy, raporty i teksty): <a href="https://creativecommons.org/licenses/by/4.0/deed.pl">CC BY 4.0</a>; oznaczenie autorstwa „LexAlpha Lab, LawBenchmark.pl”.</li>
<li><b>Kod</b>: MIT.</li>
<li><b>Odpowiedzi modeli</b> to wyniki systemów osób trzecich, przytoczone dosłownie w celu oceny, krytyki i badań; nie rościmy sobie do nich praw ani ich nie relicencjonujemy. Fragmenty cudzych opracowań, które model mógł powtórzyć w odpowiedzi, pozostają własnością ich autorów.</li>
<li><b>Przepisy i orzeczenia</b> cytowane w odpowiedziach i kluczach to urzędowe dokumenty i materiały, niechronione prawem autorskim (art. 4 pkt 2 pr.aut.); nie dotyczy to komentarzy i opracowań.</li>
<li><b>Kanarek</b>: każdy plik i rekord zawiera ciąg kanaryjski z prośbą o nieużywanie zbioru do treningu modeli. Licencja takiego użycia nie zakazuje; to prośba metodologiczna, by kolejne pomiary pozostały miarodajne.</li>
</ul>
</section>
<section>{kot("cytowanie", "Cytowanie zbioru")}
<p>Piotrowski A., Koman A. (2026). <i>LawBenchmark.pl · Benchmark 02 · pytania prawne (dane)</i>. Wersja {WERSJA_RAPORTU}, {DATA_RAPORTU}. LexAlpha Lab, KTZR. {BAZA}/dane</p>
<p>Raport i artykuł metodologiczny: <a href="/raporty">raporty</a>. Kontakt: <a href="mailto:a.piotrowski@ktzr.pl">a.piotrowski@ktzr.pl</a>.</p>
</section>
</div></article>
"""
strona("/dane", "Dane i kod — LawBenchmark.pl",
       "Zbiór danych Benchmarku 02: 10 pytań z kluczami, 160 odpowiedzi modeli, 160 kart z klasami błędów, oceny sędziów-modeli, warstwa weryfikacji, skrypty odtwarzające każdą liczbę. CC BY 4.0 / MIT.",
       DANE, okr=[("Dane i kod", None)], ld=[LD_DATASET], tu="/dane")

# =====================================================================
# 5b. Współpraca
# =====================================================================
WSPOLPRACA = f"""
<header class="pod-hero"><div class="wrap">
<h1>Współpraca</h1>
<p class="lead">Badamy jakość odpowiedzi systemów AI na pytania z polskiego prawa. Przyjmujemy zgłoszenia systemów do badania na pytaniach niepublicznych, propozycje współpracy naukowej, uwagi do metodologii i wyników oraz pytania mediów.</p>
<div class="spis" style="display:flex"><a href="#dostawcy">Dostawcy systemów</a><a href="#badacze">Uczelnie i badacze</a><a href="#praktyka">Kancelarie i działy prawne</a><a href="#media">Media i cytowanie</a><a href="#kontakt">Kontakt</a></div>
</div></header>
<article><div class="wrap">
<section>{kot("dostawcy", "Dostawcy i twórcy systemów prawniczych")}
<p>Dotyczy asystentów kancelaryjnych, systemów z własnym wyszukiwaniem (RAG) i innych narzędzi opartych na modelach językowych. Wyniki takich systemów nie trafiają do tabeli czystych modeli: dostęp do źródeł, korpus dokumentów i instrukcje systemowe zmieniają warunki, więc publikujemy je w osobnej kategorii z opisem konfiguracji.</p>
<h3>Badanie na pytaniach niepublicznych</h3>
<p>Oferujemy badanie wskazanej wersji systemu na 40 nieujawnionych pytaniach z puli 50, według opublikowanej specyfikacji oceny. Przed rozpoczęciem ustalamy na piśmie: konfigurację i wersję systemu, dostęp do narzędzi i źródeł, datę stanu prawnego, sposób wykonania odpowiedzi i ocenę według tej samej karty, którą stosujemy do czystych modeli.</p>
<h3>Warunki ustalane indywidualnie</h3>
<p>Finansowanie badania, termin na uwagi dostawcy do wyniku i sposób publikacji ustalamy indywidualnie, na piśmie, przed pierwszym wywołaniem systemu. Dwie zasady są stałe: wynik i jego opis nie zależą od tego, kto badanie finansuje, a każdy opublikowany raport podaje, kto je sfinansował, czy dostawca udostępnił system bezpłatnie i jakie warunki publikacji przyjęto. Dostawca otrzymuje wynik przed publikacją i może zgłosić błędy faktyczne i techniczne.</p>
<h3>Wersja systemu i powtórzenia</h3>
<p>Raport identyfikuje badaną wersję, konfigurację i datę wykonania. Powtórne badanie jest oznaczane jako kolejne i nie zastępuje wcześniejszego wyniku; prowadzimy rejestr wszystkich badań, także przerwanych i unieważnionych, z przyczyną. Awaria infrastruktury uzasadnia powtórzenie, słaba odpowiedź systemu nie.</p>
<h3>Ochrona pytań</h3>
<p>Nie przekazujemy dostawcy zestawu pytań ani kluczy do przygotowania systemu; pytania zadaje operator badania. Jeżeli pytania trafiają do systemu dostawcy przez jego interfejs, mogą być widoczne w jego logach: dlatego wymagamy zobowiązania do niewykorzystywania ich do treningu i strojenia oraz określenia okresu przechowywania, a gdy tego nie da się zapewnić, odnotowujemy to w raporcie. Zestaw niepubliczny nie jest tajny bezterminowo; po kilku badaniach część pytań wymieniamy. Stosujemy niepubliczne znaczniki kontrolne do wykrywania ujawnienia materiału; podejrzenia weryfikujemy przed sformułowaniem wniosków.</p>
<h3>Niezależność oceny</h3>
<p>Finansujący badanie nie wybiera ocenianych odpowiedzi, nie ustala punktacji i nie zatwierdza wniosków. Raport ujawnia powiązania autorów i oceniających z badanym dostawcą; przy istotnym powiązaniu oceniający jest wyłączony albo ocenę wykonuje osoba zewnętrzna. Własne produkty KTZR i LexAlpha pozostają poza publikowanymi wynikami (<a href="/metodologia#autorzy">konflikt interesów</a>).</p>
<p class="uwaga">Badanie nie jest certyfikacją, audytem ani rekomendacją zakupową. Wynik dotyczy wskazanej wersji i konfiguracji systemu w opisanych warunkach i nie potwierdza poprawności odpowiedzi w innych sprawach.</p>
</section>
<section>{kot("badacze", "Uczelnie i badacze")}
<h3>Niezależna druga ocena</h3>
<p>Zapraszamy prawników do niezależnego oceniania odpowiedzi według opublikowanej specyfikacji. Zakres próby i sposób liczenia zgodności między oceniającymi ustalamy przed oceną; κ liczymy z ocen sprzed uzgodnienia rozbieżności, a rozbieżności zachowujemy do analizy. Drugi oceniający nie jest „potwierdzeniem obiektywności”, tylko miarą tego, jak powtarzalna jest ocena.</p>
<h3>Replikacje i wspólne publikacje</h3>
<p>Możliwe obszary: replikacja na innych modelach lub datach, analiza błędów według klas F/T/W/S, rozwój metod oceny i weryfikacji powołań, porównanie z benchmarkami z innych porządków prawnych. Autorstwo publikacji ustalamy według rzeczywistego wkładu.</p>
<h3>Dane do ponownego wykorzystania</h3>
<p>Opublikowane pytania, klucze, karty, odpowiedzi i oceny sędziów są dostępne na licencji CC BY 4.0 (kod na MIT) i nie wymagają kontaktu z autorami: <a href="/dane">dane i kod</a>. Czterdzieści pytań niepublicznych i ich klucze pozostają poza otwartym zbiorem; udostępniamy je wyłącznie w ramach wspólnego badania, z zobowiązaniem do nieujawniania.</p>
</section>
<section>{kot("praktyka", "Kancelarie i działy prawne")}
<p>Wyniki pokazują, jakie rodzaje błędów popełniają czyste modele i jak zmienia je wyszukiwanie. Pomagają zaplanować własne sprawdzenie narzędzia na zadaniach wykonywanych w organizacji. Nie zastępują oceny konkretnego wdrożenia, jego źródeł, konfiguracji i nadzoru, a wynik modelu bazowego nie potwierdza jakości produktu, który z tego modelu korzysta. Żaden wynik nie zwalnia prawnika z kontroli odpowiedzi przed użyciem.</p>
<p>Przyjmujemy propozycje kategorii pytań i uwagi do kryteriów oceny. W pierwszym kontakcie nie przesyłaj danych klientów ani materiałów objętych tajemnicą zawodową.</p>
</section>
<section>{kot("media", "Media i cytowanie")}
<p>Przy cytowaniu podaj nazwę i wersję badania, datę, badaną konfigurację oraz odnośnik do wyników i metodologii; wzory cytowań są na stronie <a href="/raporty">raporty</a>. Wykresy i tabele możesz wykorzystać na licencji CC BY 4.0 z oznaczeniem „LexAlpha Lab, LawBenchmark.pl”. Udzielamy wyjaśnień o zakresie badania i przyjmujemy zgłoszenia błędów. Wyniku pojedynczego badania nie należy przedstawiać jako ogólnej oceny systemu we wszystkich zastosowaniach w prawie; bezpieczna konstrukcja brzmi: „w badaniu [wersja, data], przy [warunki], system X uzyskał [wynik] w zakresie [zadania]”.</p>
</section>
<section>{kot("kontakt", "Kontakt")}
<p>E-mail: <b>a.piotrowski@ktzr.pl</b>. W temacie wiadomości wpisz jedno z: „Badanie systemu”, „Współpraca naukowa”, „Uwagi do metodologii”, „Media”.</p>
<p class="uwaga">Korespondencję obsługuje Kancelaria Radców Prawnych KTZR (Gdańsk), która jest administratorem danych osobowych nadawców; informacja o przetwarzaniu danych: <a href="https://www.ktzr.pl/polityka-prywatnosci/">polityka prywatności KTZR</a>. Stronę ewentualnej umowy (KTZR albo LexAlpha Sp. z o.o.) ustalamy indywidualnie; „LexAlpha Lab” jest nazwą inicjatywy, nie podmiotem.</p>
</section>
</div></article>
"""
strona("/wspolpraca", "Współpraca — badanie systemów AI na pytaniach z polskiego prawa · LawBenchmark.pl",
       "Zasady współpracy z LawBenchmark.pl: badanie systemów prawniczych na 40 niepublicznych pytaniach (warunki ustalane indywidualnie, ochrona pytań, niezależność oceny), współpraca naukowa, wykorzystanie wyników w kancelariach, cytowanie.",
       WSPOLPRACA, okr=[("Współpraca", None)], tu="/wspolpraca")

# =====================================================================
# 5c. Dołącz do nas
# =====================================================================
DOLACZ = f"""
<header class="pod-hero"><div class="wrap">
<h1>Dołącz do nas</h1>
<p class="lead">LawBenchmark rozwija niewielki zespół prawników i inżynierów. Szukamy osób, które chcą oceniać odpowiedzi systemów AI według jawnych kryteriów, zgłaszać pytania z praktyki i budować narzędzia do sprawdzania powołań u źródła.</p>
</div></header>
<article><div class="wrap">
<section>{kot("kogo", "Kogo szukamy")}
<ul>
<li><b>Prawników oceniających</b> (radcowie prawni, adwokaci, aplikanci, doktoranci prawa): niezależna ocena odpowiedzi według opublikowanej specyfikacji, sprawdzanie każdego powołania w ISAP, ELI i SAOS. Każda ocena jest porównywana z kartą wzorcową, a zgodność między oceniającymi publikujemy.</li>
<li><b>Praktyków z pytaniami</b>: krótkie pytania w takiej postaci, w jakiej padają w pracy, z własną odpowiedzią i podstawą prawną. Z nich powstają klucze kolejnych edycji; pytania niepubliczne pozostają poza zbiorem otwartym.</li>
<li><b>Badaczy</b> (prawo, informatyka, językoznawstwo, statystyka): replikacje, analiza klas błędów, metody oceny i pomiaru zgodności, porównania z benchmarkami z innych porządków prawnych.</li>
<li><b>Inżynierów</b> (Python): warstwa weryfikacji powołań, biblioteka <a href="https://github.com/apiotrowski-afk/legal-cite-pl">legal-cite-pl</a>, skrypty biegów i oceny, strona. Kod jest otwarty (MIT).</li>
</ul>
</section>
<section>{kot("zasady", "Na jakich zasadach")}
<p>Udział jest dobrowolny; zakres, czas i ewentualne wynagrodzenie ustalamy indywidualnie. Współautorstwo raportów i publikacji wynika z rzeczywistego wkładu. Oceniający nie może oceniać systemu dostawcy, z którym jest powiązany; powiązania ujawniamy w raporcie. Przed oceną każdy dostaje specyfikację, przykłady graniczne i karty kalibracyjne; pierwsze karty omawiamy wspólnie.</p>
<p>Czego nie oczekuj: szybkich rozstrzygnięć. Sprawdzenie jednej odpowiedzi u źródła zajmuje od kilkunastu minut do godziny, a wynik liczy się dopiero wtedy, gdy każdy werdykt ma dowód z tekstu urzędowego.</p>
</section>
<section>{kot("jak", "Jak się zgłosić")}
<p>Napisz na <b>a.piotrowski@ktzr.pl</b> z tematem „Dołączam”. Podaj, w której roli chcesz pracować, dziedzinę prawa albo technologię, którą znasz, i ile czasu możesz poświęcić w miesiącu. Nie przesyłaj danych klientów ani materiałów objętych tajemnicą zawodową.</p>
<p class="uwaga">Korespondencję obsługuje Kancelaria Radców Prawnych KTZR (Gdańsk), administrator danych osobowych nadawców: <a href="https://www.ktzr.pl/polityka-prywatnosci/">polityka prywatności KTZR</a>. LawBenchmark prowadzi LexAlpha Lab, wspólna inicjatywa KTZR i <a href="https://lexalpha.pl/">LexAlpha Sp. z o.o.</a></p>
</section>
</div></article>
"""
strona("/dolacz", "Dołącz do nas — LawBenchmark.pl",
       "Zespół LawBenchmark szuka prawników do niezależnej oceny odpowiedzi systemów AI, praktyków z pytaniami z polskiego prawa, badaczy i inżynierów do warstwy weryfikacji powołań. Zasady udziału i kontakt.",
       DOLACZ, okr=[("Dołącz do nas", None)], tu="/dolacz")

# =====================================================================
# 5d. Prywatność i cookies
# =====================================================================
PRYWATNOSC = f"""
<header class="pod-hero"><div class="wrap">
<h1>Prywatność i pliki cookie</h1>
<p class="lead">Jakie dane zbiera ta strona, na jakiej podstawie i jak zmienić decyzję.</p>
<div class="meta">Obowiązuje od 29.10.2026</div>
</div></header>
<article><div class="wrap">
<section>{kot("administrator", "Administrator danych")}
<p>Administratorem danych osobowych przetwarzanych na stronie lawbenchmark.pl jest Kancelaria Radców Prawnych Żurawska Piotrowski i Wspólnicy sp.k. (KTZR) z siedzibą w Gdańsku. Kontakt w sprawach danych osobowych: a.piotrowski@ktzr.pl. Korespondencję przesyłaną na ten adres obsługujemy według <a href="https://www.ktzr.pl/polityka-prywatnosci/">polityki prywatności KTZR</a>.</p>
</section>
<section>{kot("analityka", "Google Analytics")}
<p>Strona korzysta z Google Analytics 4 wyłącznie za Twoją zgodą. Do czasu kliknięcia „Akceptuję” w okienku na dole strony nie ładujemy żadnego skryptu Google i nie zapisujemy plików cookie analityki. Po zgodzie Google Analytics zbiera informacje o odwiedzanych podstronach, kliknięciach (w tym pobraniach raportów i przejściach do repozytorium), przybliżonej lokalizacji, rodzaju urządzenia i przeglądarki oraz stronie, z której przyszedłeś. Google Analytics 4 nie zapisuje adresów IP. Używamy tych danych tylko w zbiorczych statystykach, żeby wiedzieć, które materiały są czytane.</p>
<ul>
<li><b>Podstawa prawna:</b> Twoja zgoda (art. 6 ust. 1 lit. a RODO) i zgoda na przechowywanie informacji w urządzeniu końcowym wymagana przepisami o komunikacji elektronicznej.</li>
<li><b>Pliki cookie:</b> <code>_ga</code> i <code>_ga_…</code>, ważne do dwóch lat.</li>
<li><b>Odbiorca:</b> Google Ireland Limited jako podmiot przetwarzający. Dane mogą trafiać do Google LLC w Stanach Zjednoczonych na podstawie unijno-amerykańskich ram ochrony danych (EU-US Data Privacy Framework).</li>
<li><b>Okres przechowywania:</b> dane zdarzeń w Google Analytics przez 14 miesięcy.</li>
</ul>
</section>
<section>{kot("zmiana", "Jak zmienić decyzję")}
<p>Zgodę możesz w każdej chwili wycofać albo udzielić jej ponownie przez link <a href="#" data-ustawienia-cookie>Ustawienia cookies</a> w stopce strony. Wycofanie zgody usuwa pliki cookie analityki i nie wpływa na zgodność z prawem przetwarzania przed jej wycofaniem. Twój wybór zapisujemy w pamięci przeglądarki, bez pliku cookie.</p>
</section>
<section>{kot("prawa", "Twoje prawa")}
<p>Masz prawo dostępu do danych, ich sprostowania, usunięcia i ograniczenia przetwarzania, a także prawo wniesienia skargi do Prezesa Urzędu Ochrony Danych Osobowych. Nie podejmujemy na podstawie tych danych żadnych zautomatyzowanych decyzji.</p>
</section>
</div></article>
"""
strona("/prywatnosc", "Prywatność i pliki cookie — LawBenchmark.pl",
       "Jakie dane zbiera lawbenchmark.pl: Google Analytics 4 wyłącznie za zgodą, pliki cookie, odbiorcy, okres przechowywania i prawa użytkownika.",
       PRYWATNOSC, okr=[("Prywatność i cookies", None)])

# =====================================================================
# 6. EN
# =====================================================================
EN_ROWS = "".join(f'<tr><td class="model">{E(m)}</td><td class="num ok">{PARA[m]["W0"]["pu"]}</td><td class="num ok">{PARA[m]["W1"]["pu"]}</td>'
                  f'<td class="num bad">{PARA[m]["W0"]["hal"]}</td><td class="num bad">{PARA[m]["W1"]["hal"]}</td></tr>' for m in MODELE)
EN = f"""
<header class="hero"><div class="wrap">
<h1>How do language models answer questions about Polish law?</h1>
<p class="lead">LawBenchmark.pl measures correctness, hallucinations and grounding in official legal sources, with and without web search. A project of LexAlpha Lab, a joint research initiative of the law firm <a href="https://www.ktzr.pl/">KTZR</a> (Gdańsk) and <a href="https://lexalpha.pl/">LexAlpha Sp. z o.o.</a> (Warsaw).</p>
<div class="zakres"><span><b>10</b> questions</span><span><b>8</b> models, 3 providers</span><span><b>2</b> conditions: no tools / web search</span><span><b>160</b> answers</span><span><b>{spr_n}</b> of {spr_m} citations checked at source</span></div>
<div class="meta">Benchmark 02 · report v{WERSJA_RAPORTU}, 27 October 2026 · law in force on 1 October 2026 · scoring specification 1.0.4 (scoring rules as in 1.0.1) · full site in Polish</div>
<a class="btn s" href="/reports/Piotrowski_2026_correctly_grounded_v1.2.pdf">Methodology working paper (PDF, EN)</a><a class="btn s" href="/reports/lexalpha_lab_benchmark_02.pdf">Benchmark 02 report (PDF, PL)</a>
</div></header>
<article><div class="wrap">
<section>{kot("design", "Design")}
<p>Ten short legal questions collected in practice, in the form a lawyer types into a chat (typos kept; in three questions missing facts were added before the study; six contain a false or outdated premise the model should correct). Eight models from OpenAI (GPT-6.1 Sol, GPT-6 Astra, GPT-5.6 Terra), Anthropic (Claude Opus, Sonnet, Haiku 5.5) and Google (Gemini 3.8 Flash, Gemini 4 Argon), each answering twice: without tools (W0) and with the provider's web search (W1). One run, one answer per question.</p>
<p>Every answer has a scoring card. An answer is labelled <b>hallucinated</b> if it contains at least one statement about a legal source that disagrees with the official text of the law in force on the reference date (1 October 2026), in one of four classes: F (the legal source or numbered provision does not exist), T (a real source attributed content absent from it), W (wording from another date presented as current), S (a real source with a distorted identifier). An answer is <b>correctly grounded</b> (a term defined by the authors) if it contains all essential elements specified in the answer key, has no detected hallucination, and has at least one citation that the assessor confirmed in an official source. A model filled in every card and a lawyer checked it. Five model judges from three providers evaluated the available answers separately; Cohen's κ with the cards ranged from 0.58 to 0.90 on the extension set (79–80 cards per judge) and from 0.71 to 0.97 on the pilot set (68–80 cards); the fifth judge evaluated 49 cards and is not comparable.</p>
</section>
<section>{kot("results", "Results")}
<div class="scroll"><table class="t zw"><thead><tr><th>Model</th><th class="num">Correctly grounded, no tools <small>of 10</small></th><th class="num">Correctly grounded, web search</th><th class="num">Hallucinated, no tools <small>of 10</small></th><th class="num">Hallucinated, web search</th></tr></thead><tbody>{EN_ROWS}</tbody></table></div>
<p>Across 80 answers per condition: {L["hal_W0"]} hallucinated without tools and {L["hal_W1"]} with web search; {L["pu_W0"]} and {L["pu_W1"]} correctly grounded. The most frequent error is a real provision or judgment attributed content absent from the source (class T, {L["klasa_T"]} answers), followed by outdated wording presented as current (W, {L["klasa_W"]}); fabricated sources are rare (F, {L["klasa_F"]}), as are distorted identifiers (S, {L["klasa_S"]}); one answer may carry several classes. In this series, five of eight models had fewer hallucinated answers with web search and three had the same number; the cost of a run with search was {min(L["krotnosc_kosztu"].values()):.1f} to {max(L["krotnosc_kosztu"].values()):.1f} times the cost without it (some search costs are lower bounds). A single run per condition does not separate the effect of the tools from run-to-run variation.</p>
</section>
<section>{kot("limitations", "Limitations")}
<p>Small sample (10 questions, 5 from civil procedure), one run per system, one reviewing lawyer, cards pre-filled by a model from one of the evaluated families, scoring rules refined during the work (every change is dated in the specification). The 160 answers are not 160 independent observations. Results illustrate the criteria; they are not a product ranking. The questions have been publicly available since October 2026, so later measurements on this set may be contaminated.</p>
</section>
<section>{kot("materials", "Materials and citation")}
<p>Methodology working paper (not peer-reviewed): Piotrowski A. (2026). <i>"Hallucination" Is Not Enough: Why Legal LLM Benchmarks Should Measure "Correctly Grounded"</i>. LexAlpha Lab, v1.2. <a href="https://doi.org/10.5281/zenodo.23674794">doi:10.5281/zenodo.23674794</a> · <a href="https://papers.ssrn.com/abstract=7672779">SSRN</a>.<br>
Technical report (Polish): Piotrowski A., Koman A. (2026). <i>LexAlpha Lab · Benchmark 02 · pytania prawne</i>, v{WERSJA_RAPORTU}. <a href="/reports/lexalpha_lab_benchmark_02.pdf">PDF</a>.<br>
Data and code (CC BY 4.0 / MIT): questions with scoring keys, 160 answers and cards, judge scores, verification reports, scripts — <a href="/dane">data page (Polish)</a>; repository: <a href="https://github.com/apiotrowski-afk/lawbenchmark">github.com/apiotrowski-afk/lawbenchmark</a>.</p>
<pre>{E(BIBTEX_ART)}</pre>
</section>
</div></article>
"""
strona("/en", "LawBenchmark.pl — language models and Polish law",
       "Benchmark of language models on Polish legal questions: correctness, hallucinations (classes F/T/W/S) and grounding in official sources, with and without web search. LexAlpha Lab, KTZR.",
       EN, lang="en", okr=[("English", None)], hreflang={"pl": "/", "en": "/en", "x-default": "/"}, tu="/en")

# =====================================================================
# robots, sitemap
# =====================================================================
ROBOTY_AI = ["Google-Extended", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Bingbot", "CCBot"]
open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8").write(
    "# lawbenchmark.pl: treść jest publiczna (CC BY 4.0) i może być indeksowana i cytowana; jawne wpisy dla robotów AI.\n"
    + "".join(f"User-agent: {r}\nAllow: /\n\n" for r in ROBOTY_AI)
    + "User-agent: *\nAllow: /\n\nSitemap: https://lawbenchmark.pl/sitemap.xml\n")
mapa = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for sc, lm in STRONY:
    mapa.append(f'<url><loc>{BAZA}{"" if sc == "/" else sc}{"/" if sc == "/" else ""}</loc><lastmod>{lm}</lastmod></url>')
mapa.append(f'<url><loc>{BAZA}/reports/lexalpha_lab_benchmark_02.pdf</loc><lastmod>2026-10-29</lastmod></url>')
mapa.append(f'<url><loc>{BAZA}/reports/Piotrowski_2026_correctly_grounded_v1.2.pdf</loc><lastmod>2026-10-26</lastmod></url>')
mapa.append("</urlset>")
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(mapa) + "\n")
print("site/ OK;", len(STRONY), "stron;", len(WIERSZE), "wierszy wyników")
