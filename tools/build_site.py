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
DATA_KART, WERSJA_RAPORTU, DATA_RAPORTU = "25.10.2026", "1.0", "27.10.2026"
DATA_STRONY = "2026-10-29"          # lastmod nowych stron; strona główna ma własną datę niżej
REPO_URL = "https://github.com/apiotrowski-afk/lawbenchmark"   # publiczne repozytorium (odnośniki do kart, distribution w JSON-LD)
HF_URL = None                       # karta zbioru na Hugging Face — po publikacji

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


# ---------- wykres par (dumbbell), dwa panele ----------
def panel(klucz, tytul, kolor):
    szer, lewy, wysz_w = 300, 150, 30
    wys = 70 + len(MODELE) * wysz_w
    out = [f'<text x="16" y="22" class="pt">{E(tytul)}</text>']
    for i in range(0, 11, 2):
        x = lewy + i / 10 * szer
        out.append(f'<line x1="{x:.0f}" y1="34" x2="{x:.0f}" y2="{40 + len(MODELE) * wysz_w}" class="siatka"/>'
                   f'<text x="{x:.0f}" y="{52 + len(MODELE) * wysz_w}" class="os" text-anchor="middle">{i}</text>')
    for j, m in enumerate(MODELE):
        y = 50 + j * wysz_w
        a, b = PARA[m]["W0"][klucz], PARA[m]["W1"][klucz]
        xa, xb = lewy + a / 10 * szer, lewy + b / 10 * szer
        out.append(f'<text x="{lewy - 10}" y="{y + 4}" class="et" text-anchor="end">{E(m)}</text>')
        if a == b:
            out.append(f'<circle cx="{xb:.0f}" cy="{y}" r="7" style="fill:{kolor}"/><circle cx="{xb:.0f}" cy="{y}" r="3" class="w0" style="stroke:{kolor}"/>')
            out.append(f'<text x="{xb:.0f}" y="{y - 11}" class="lb" text-anchor="middle" style="fill:{kolor}">{b}</text>')
            out.append(f'<text x="{xb + 12:.0f}" y="{y + 4}" class="os">bez zmiany</text>')
            continue
        out.append(f'<line x1="{xa:.0f}" y1="{y}" x2="{xb:.0f}" y2="{y}" class="lacz"/>')
        out.append(f'<circle cx="{xa:.0f}" cy="{y}" r="6" class="w0" style="stroke:{kolor}"/>')
        out.append(f'<circle cx="{xb:.0f}" cy="{y}" r="6" style="fill:{kolor}"/>')
        ya = y + 20 if abs(a - b) <= 1 else y - 11
        out.append(f'<text x="{xa:.0f}" y="{ya}" class="lb" text-anchor="middle">{a}</text>')
        out.append(f'<text x="{xb:.0f}" y="{y - 11}" class="lb" text-anchor="middle" style="fill:{kolor}">{b}</text>')
    return (f'<svg viewBox="0 0 540 {wys}" role="img" aria-label="{E(tytul)}" class="wykres">'
            '<style>.pt{font:600 14px Inter,system-ui,sans-serif;fill:var(--ink)} .et{font:500 13px Inter,system-ui,sans-serif;fill:var(--ink)}'
            ' .os{font:12px Inter,system-ui,sans-serif;fill:var(--muted)} .lb{font:600 12px Inter,system-ui,sans-serif;fill:var(--muted);font-variant-numeric:tabular-nums}'
            ' .siatka{stroke:var(--line);stroke-width:1} .lacz{stroke:var(--muted);stroke-width:2;opacity:.6} .w0{fill:var(--surface);stroke-width:2.5}</style>'
            + "\n".join(out) + '</svg>')


WYKRES = ('<div class="dwa wyk">' + panel("pu", "Poprawnie ugruntowane (z 10) — więcej = lepiej", "var(--ok)")
          + panel("hal", "Odpowiedzi z halucynacją (z 10) — mniej = lepiej", "var(--bad)") + '</div>')

# ---------- tabela par i karty mobilne (strona główna) ----------
tab = ['<table class="pary"><thead><tr><th>Model</th><th>Warunek</th><th class="num">Poprawnie ugruntowane <small>z 10</small></th>'
       '<th class="num">Halucynacje <small>z 10</small></th><th class="num">Blok A <small>%</small></th><th class="num">Blok B <small>%</small></th>'
       '<th class="num">Koszt serii <small>USD</small></th><th class="num">USD / poprawnie ugruntowaną</th><th class="num">Sprawdzone powołania</th></tr></thead><tbody>']
karty = []
for m in MODELE:
    for k, war in enumerate(("W0", "W1")):
        r = PARA[m][war]
        tab.append(f'<tr class="{"p0" if k == 0 else "p1"}"><td class="model">{E(m) if k == 0 else ""}</td><td><span class="war {war.lower()}">{war}</span></td>'
                   f'<td class="num ok">{r["pu"]}</td><td class="num bad">{r["hal"]}</td><td class="num">{E(r["A"])}</td><td class="num">{E(r["B"])}</td>'
                   f'<td class="num">{E(r["koszt"])}</td><td class="num">{E(r["koszt_pu"])}</td><td class="num">{E(r["spr"])}</td></tr>')
    w0, w1 = PARA[m]["W0"], PARA[m]["W1"]
    karty.append(f'''<div class="karta"><h3>{E(m)}</h3>
<div class="kw"><span class="war w0">W0</span><span><b class="ok">{w0["pu"]}</b> ugruntowane</span><span><b class="bad">{w0["hal"]}</b> z halucynacją</span><span class="m">A {E(w0["A"])} % · {E(w0["koszt"])} USD</span></div>
<div class="kw"><span class="war w1">W1</span><span><b class="ok">{w1["pu"]}</b> ugruntowane</span><span><b class="bad">{w1["hal"]}</b> z halucynacją</span><span class="m">A {E(w1["A"])} % · {E(w1["koszt"])} USD</span></div></div>''')
tab.append("</tbody></table>")
TABELA, KARTY = "\n".join(tab), "\n".join(karty)

KLASY_HTML = "".join(f'<div class="klasa"><span class="znak">{E(k[0][0])}</span><div><b>{E(KL_OPIS[k[0][0]])}</b>'
                     f'<span class="m">razem <b>{E(k[3])}</b> odpowiedzi · W0 {E(k[1])} · W1 {E(k[2])}</span></div></div>'
                     for k in KLASY if k[0][0] in KL_OPIS)

# ---------- pliki ----------
os.makedirs(os.path.join(SITE, "reports"), exist_ok=True)
for src, dst in [("reports/benchmark-02/lexalpha_lab_benchmark_02.pdf", "reports/lexalpha_lab_benchmark_02.pdf"),
                 ("reports/paper-v1.2/Piotrowski_2026_correctly_grounded_v1.2.pdf", "reports/Piotrowski_2026_correctly_grounded_v1.2.pdf")]:
    shutil.copy2(os.path.join(REPO, src), os.path.join(SITE, dst))

BIBTEX = """@techreport{piotrowski2026benchmark02,
  author = {Piotrowski, Adam and Koman, Andrzej},
  title  = {LexAlpha Lab · Benchmark 02 · pytania prawne},
  institution = {LexAlpha Lab, KTZR},
  year = {2026}, month = {10}, note = {wersja 1.0, 27 października 2026},
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
:root{--brand:#1f4e79;--ok:#13766d;--bad:#b44739;--bg:#f7f8fa;--surface:#ffffff;--ink:#17212b;--muted:#5b6670;--line:#dce2e8;--soft:#eef2f6}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--brand:#8ab9e2;--ok:#4fb3a9;--bad:#e07a6c;--bg:#111820;--surface:#19232e;--ink:#e6edf3;--muted:#9aa7b4;--line:#2a3643;--soft:#1f2b37}}
:root[data-theme="dark"]{--brand:#8ab9e2;--ok:#4fb3a9;--bad:#e07a6c;--bg:#111820;--surface:#19232e;--ink:#e6edf3;--muted:#9aa7b4;--line:#2a3643;--soft:#1f2b37}
*{box-sizing:border-box;min-width:0} html{scroll-behavior:smooth} body{overflow-x:hidden}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 "Source Serif 4",Georgia,serif}
.wrap{max-width:1200px;margin:0 auto;padding:0 16px} .tekst{max-width:780px}
nav{position:sticky;top:0;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);z-index:5}
nav .wrap{display:flex;align-items:center;gap:18px;height:56px;font:500 14px Inter,system-ui,sans-serif}
nav .logo{font-weight:600;color:var(--ink);text-decoration:none;letter-spacing:.01em} nav .logo small{color:var(--muted);font-weight:500;margin-left:8px}
nav a{color:var(--muted);text-decoration:none} nav a:hover,nav a.tu{color:var(--ink)} nav .sp{flex:1}
@media (max-width:760px){nav a:not(.logo){display:none}}
nav button{background:none;border:1px solid var(--line);color:var(--muted);border-radius:6px;padding:4px 10px;font:inherit;cursor:pointer}
.okr{font:13px Inter,system-ui,sans-serif;color:var(--muted);padding:18px 0 0} .okr a{color:var(--muted)} .okr span{margin:0 6px}
.hero{padding:56px 0 40px} .hero h1{font:600 clamp(30px,4.6vw,46px)/1.12 "Source Serif 4",Georgia,serif;margin:0 0 14px;max-width:820px}
.hero p.lead{font-size:20px;color:var(--muted);max-width:720px;margin:0 0 22px}
.pod-hero{padding:28px 0 8px} .pod-hero h1{font:600 clamp(26px,3.6vw,38px)/1.15 "Source Serif 4",Georgia,serif;margin:0 0 10px;max-width:860px}
.pod-hero p.lead{font-size:19px;color:var(--muted);max-width:760px;margin:0 0 10px}
.zakres{display:flex;flex-wrap:wrap;gap:8px 22px;font:500 15px Inter,system-ui,sans-serif;color:var(--ink);margin-bottom:10px} .zakres b{font-weight:600}
.meta{font:13px Inter,system-ui,sans-serif;color:var(--muted);margin-bottom:22px}
.btn{display:inline-block;border-radius:6px;padding:10px 16px;font:600 14px Inter,system-ui,sans-serif;text-decoration:none;margin:0 10px 10px 0}
.btn.p{background:var(--brand);color:#fff} .btn.s{border:1px solid var(--line);color:var(--ink);background:var(--surface)}
.uwaga{font:14px Inter,system-ui,sans-serif;color:var(--muted);max-width:720px;border-left:3px solid var(--line);padding-left:12px;margin-top:8px}
section{padding:40px 0 8px} h2{font:600 28px/1.2 "Source Serif 4",Georgia,serif;margin:0 0 6px} .pod{color:var(--muted);margin:0 0 20px;max-width:720px}
article section{padding:28px 0 4px} article h2{font-size:26px;margin-top:8px} article h3{font:600 19px/1.3 Inter,system-ui,sans-serif;margin:22px 0 6px}
article p,article li{max-width:780px} article ul,article ol{padding-left:22px} article li{margin:4px 0}
h2 a.kot,h3 a.kot{color:var(--line);text-decoration:none;font-weight:400;margin-left:8px} h2:hover a.kot,h3:hover a.kot{color:var(--muted)}
.dwa{display:grid;grid-template-columns:1fr 1fr;gap:16px} @media (max-width:760px){.dwa{grid-template-columns:1fr}}
.blok{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px 20px}
.blok h3{margin:0 0 6px;font:600 20px Inter,system-ui,sans-serif} .blok p{margin:0;color:var(--muted);font-size:16px}
.blok.ok h3{color:var(--ok)} .blok.bad h3{color:var(--bad)}
.teza{font:600 20px/1.4 "Source Serif 4",Georgia,serif;margin:18px 0 0;max-width:820px}
.wyk{gap:12px} .wykres{width:100%;height:auto;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px}
.legenda{display:flex;gap:20px;flex-wrap:wrap;font:13px Inter,system-ui,sans-serif;color:var(--muted);margin:10px 0 0}
.legenda i{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;margin-right:6px;border:2px solid var(--muted)} .legenda i.f{background:var(--muted)}
table.pary,table.t{width:100%;border-collapse:collapse;font:14px/1.35 Inter,system-ui,sans-serif;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden;font-variant-numeric:tabular-nums}
.pary th,.pary td,.t th,.t td{padding:9px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top} .pary th,.t th{background:var(--soft);font-weight:600} th small{font-weight:500;color:var(--muted)}
.pary th,.pary td{white-space:nowrap} .t.zw td,.t.zw th{white-space:nowrap}
.pary .num,.t .num{text-align:right} .pary tr.p0 td{border-bottom:0} .pary td.model,.t td.model{font-weight:600} .pary tr.p1 td{padding-top:2px}
.war{display:inline-block;font:600 11px Inter,system-ui,sans-serif;padding:2px 6px;border-radius:4px;border:1px solid var(--line);color:var(--muted)} .war.w1{background:var(--brand);color:#fff;border-color:var(--brand)}
.ok{color:var(--ok)} .bad{color:var(--bad)} td.ok,td.bad{font-weight:600}
.scroll{overflow-x:auto;margin:0 -16px;padding:0 16px} .karty{display:none}
@media (max-width:760px){.scroll.pary-s{display:none} .karty{display:grid;gap:12px} .karta{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.karta h3{margin:0 0 8px;font:600 17px Inter,system-ui,sans-serif} .kw{display:grid;grid-template-columns:auto 1fr 1fr;gap:4px 10px;align-items:center;font:14px Inter,system-ui,sans-serif;padding:6px 0;border-top:1px solid var(--line)}
.kw .m{grid-column:2/4;color:var(--muted);font-size:13px}}
.klasy{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px} .klasa{display:flex;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px}
.znak{flex:none;width:36px;height:36px;border:2px solid var(--ink);border-radius:8px;display:grid;place-items:center;font:600 16px Inter,system-ui,sans-serif}
.klasa b{display:block;font:600 15px Inter,system-ui,sans-serif} .klasa .m b{display:inline;font-size:13px} .klasa .m{display:block;font:13px Inter,system-ui,sans-serif;color:var(--muted);margin-top:4px}
.przyp{display:grid;grid-template-columns:1fr 1fr;gap:16px} @media (max-width:760px){.przyp{grid-template-columns:1fr}}
.przyp .blok h3{font-size:17px} .przyp .blok p{color:var(--ink)} .q{border-left:3px solid var(--line);padding:2px 0 2px 12px;margin:10px 0;color:var(--muted);font-style:italic}
.ocena{font:13px Inter,system-ui,sans-serif;color:var(--muted);margin-top:8px}
.lista{columns:2;column-gap:40px;max-width:1000px} @media (max-width:760px){.lista{columns:1}} .lista p{break-inside:avoid;margin:0 0 12px} .lista b{font-family:Inter,system-ui,sans-serif;font-size:15px}
pre{white-space:pre-wrap;word-break:break-word;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:12px 14px;font:13px/1.45 ui-monospace,Menlo,Consolas,monospace;overflow-x:auto}
code{font:0.92em ui-monospace,Menlo,Consolas,monospace;background:var(--soft);padding:1px 5px;border-radius:4px}
blockquote.pyt{margin:14px 0;padding:14px 18px;background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--brand);border-radius:8px;font-size:18px}
.fakty{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;font:14px Inter,system-ui,sans-serif;margin:14px 0}
.fakty div{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:10px 12px} .fakty b{display:block;font-size:13px;color:var(--muted);font-weight:500;margin-bottom:2px}
.siatka-pyt{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:12px} .siatka-pyt a{display:block;color:inherit;text-decoration:none;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.siatka-pyt a:hover{border-color:var(--brand)} .siatka-pyt .id{font:600 12px Inter,system-ui,sans-serif;color:var(--muted)} .siatka-pyt h2{margin:2px 0 6px;font:600 17px/1.3 Inter,system-ui,sans-serif}
.siatka-pyt .st{font:13px Inter,system-ui,sans-serif;color:var(--muted)} .siatka-pyt .st b{color:var(--ink)}
.kl{display:inline-block;font:600 12px Inter,system-ui,sans-serif;padding:1px 6px;border-radius:4px;border:1px solid var(--line);margin-right:3px} .kl.ok{border-color:var(--ok)} .kl.bl{border-color:var(--bad);color:var(--bad)}
.spis{font:14px Inter,system-ui,sans-serif;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 18px;margin:16px 0 8px;max-width:780px} .spis a{display:inline-block;margin:3px 14px 3px 0;text-decoration:none}
footer{margin-top:48px;border-top:1px solid var(--line);padding:24px 0 40px;font:14px/1.5 Inter,system-ui,sans-serif;color:var(--muted)} a{color:var(--brand)}
"""
SKRYPT = """<script>
(function(){var r=document.documentElement,b=document.getElementById('motyw');try{var z=localStorage.getItem('motyw');if(z)r.setAttribute('data-theme',z);}catch(e){}
b.addEventListener('click',function(){var c=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');var n=c==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('motyw',n);}catch(e){}});})();
</script>"""
NAV = [("/#wyniki", "Wyniki"), ("/benchmark/02/pytania", "Pytania"), ("/metodologia", "Metodologia"), ("/raporty", "Raporty"), ("/dane", "Dane"), ("/en", "EN")]
STOPKA_PL = ('LawBenchmark.pl jest projektem <b>LexAlpha Lab</b>, laboratorium badawczego kancelarii <a href="https://www.ktzr.pl/">KTZR</a> (Gdańsk). '
             'Autorzy: Adam Piotrowski (radca prawny, KTZR), Andrzej Koman (COO LexAlpha). Badanie finansowane ze środków własnych kancelarii; żaden dostawca modeli nie uczestniczył w jego przygotowaniu. '
             'Treści na licencji CC BY 4.0. Benchmark nie jest poradą prawną.')
STOPKA_EN = ('LawBenchmark.pl is a project of <b>LexAlpha Lab</b>, the research unit of the law firm <a href="https://www.ktzr.pl/">KTZR</a> (Gdańsk, Poland). '
             'Authors: Adam Piotrowski (attorney-at-law, KTZR), Andrzej Koman (COO, LexAlpha). Funded by the firm; no model provider took part. Content under CC BY 4.0. Not legal advice.')
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
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<style>{CSS}</style>
{ld_html}</head>
<body>
<nav><div class="wrap"><a class="logo" href="/">LawBenchmark.pl <small>LexAlpha Lab</small></a><span class="sp"></span>
{nav_html}
<button id="motyw" aria-label="Przełącz motyw">◐</button></div></nav>
{okr_html}
{tresc}
<footer><div class="wrap">{stopka}</div></footer>
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
spr_n_fmt = f"{spr_n:,}".replace(",", "\u00a0")

# =====================================================================
# 1. Strona główna
# =====================================================================
GLOWNA = f"""
<header class="hero"><div class="wrap">
<h1>Jak modele językowe odpowiadają na pytania z polskiego prawa?</h1>
<p class="lead">Badamy poprawność odpowiedzi, halucynacje i oparcie w źródłach urzędowych — bez narzędzi oraz z wyszukiwaniem w internecie.</p>
<div class="zakres"><span><b>10</b> pytań</span><span><b>8</b> modeli, 3 dostawców</span><span><b>2</b> warunki: W0 / W1</span><span><b>160</b> odpowiedzi</span><span><b>1 454</b> powołań, <b>{spr_n_fmt}</b> sprawdzonych u źródła</span></div>
<div class="meta">Benchmark 02 · raport wersja {WERSJA_RAPORTU} z {DATA_RAPORTU} · karty wzorcowe w stanie z {DATA_KART} · stan prawny 1.10.2026 · specyfikacja oceny v1.0.4 (punktacja jak w 1.0.1)</div>
<a class="btn p" href="#wyniki">Zobacz wyniki</a><a class="btn s" href="/benchmark/02/pytania">Dziesięć pytań</a><a class="btn s" href="/metodologia">Metodologia</a><a class="btn s" href="/reports/lexalpha_lab_benchmark_02.pdf">Raport (PDF, 44 str.)</a>
<p class="uwaga">Wyniki dotyczą tego zestawu pytań i tych konfiguracji: dziesięć pytań, jedna seria, karty sprawdzał jeden prawnik. Nie stanowią ogólnego rankingu produktów.</p>
</div></header>

<section id="czytanie"><div class="wrap">
<h2>Jak czytać wyniki</h2>
<div class="dwa">
<div class="blok ok"><h3>Poprawnie ugruntowane ↑</h3><p>Odpowiedź ma pełny rdzeń (trafia w sedno pytania) i ani jednego twierdzenia o źródle prawa niezgodnego z tekstem urzędowym, a co najmniej jedno powołanie zostało sprawdzone u źródła.</p></div>
<div class="blok bad"><h3>Z halucynacją ↓</h3><p>Odpowiedź zawiera co najmniej jedno twierdzenie o przepisie lub orzeczeniu niezgodne z tekstem urzędowym na dzień stanu prawnego — także wtedy, gdy sam wniosek jest trafny.</p></div>
</div>
<p class="teza">Brak halucynacji nie wystarcza: odpowiedź bez błędnych powołań, ale z niepełnym rdzeniem albo bez żadnego sprawdzonego źródła, nie jest poprawnie ugruntowana. <a href="/metodologia#ugruntowanie">Definicje i mianowniki</a>.</p>
</div></section>

<section id="wyniki"><div class="wrap">
<h2>Wyniki: bez narzędzi (W0) i z wyszukiwaniem (W1)</h2>
<p class="pod">Każdy model odpowiadał na te same dziesięć pytań dwa razy. Jedna odpowiedź to 10 punktów procentowych; linia łączy oba warunki tego samego modelu i pokazuje także pogorszenie.</p>
{WYKRES}
<div class="legenda"><span><i></i>W0 — bez narzędzi</span><span><i class="f"></i>W1 — z wyszukiwaniem w internecie</span><span>Jeden punkt z dopiskiem „bez zmiany” = ten sam wynik w obu warunkach.</span><span>Kolejność modeli jak w raporcie (dostawcami), nie według wyniku.</span></div>
<h2 style="margin-top:36px;font-size:22px">Wyniki szczegółowe</h2>
<p class="pod">Blok A — kryteria obiektywne (rdzeń, podstawy prawne, powołania), blok B — ocenne (kalibracja, kompletność, użyteczność). Koszt serii dziesięciu odpowiedzi według cenników z 18.10.2026 jako równoważnik API; „≥” — dolne oszacowanie, bo narzędzie nie zapisuje części zużycia. Wyniki per pytanie: <a href="/benchmark/02/pytania">dziesięć pytań</a>.</p>
<div class="scroll pary-s">{TABELA}</div>
<div class="karty">{KARTY}</div>
</div></section>

<section id="bledy"><div class="wrap">
<h2>Cztery klasy błędu</h2>
<p class="pod">Najczęstszym błędem nie jest zmyślone źródło. Jest nim prawdziwy przepis lub wyrok z treścią, której w nim nie ma, a zaraz potem dawne brzmienie przepisu podane jako obowiązujące — tego wyszukiwanie prawie nie zmienia.</p>
<div class="klasy">{KLASY_HTML}</div>
<p class="uwaga" style="margin-top:14px">Liczby to odpowiedzi z co najmniej jednym błędem danej klasy na 80 odpowiedzi w każdym warunku; jedna odpowiedź może mieć kilka klas. Łącznie {L["hal_W0"]} odpowiedzi z halucynacją w W0 i {L["hal_W1"]} w W1. <a href="/metodologia#halucynacja">Definicje klas</a>.</p>
</div></section>

<section id="przyklady"><div class="wrap">
<h2>Dwa przykłady z kart</h2>
<p class="pod">Każda ze 160 odpowiedzi ma kartę: punkt za każde kryterium, dowód ze źródła i klasa błędu. Dwa przypadki pokazują, czego nie widać w samych liczbach.</p>
<div class="przyp">
<div class="blok"><h3><a href="/benchmark/02/pytania/p01">P01</a> · próg wykroczenia · GPT-5.6 Terra, ten sam model w W0 i W1</h3>
<p><b>Pytanie</b> zakłada, że próg między wykroczeniem a przestępstwem przeciwko mieniu nadal rośnie z płacą minimalną (pułapka: od 1.10.2023 to stała kwota 800 zł, art. 119 § 1 k.w.).</p>
<div class="q">W0: „W 2026 r. granica … wynosi co do zasady 800 zł. Nie zmieniła się ona wraz ze wzrostem płacy minimalnej.”</div>
<div class="q">W1: „W 2026 r. próg wynosi 1 201,50 zł. Tak, próg wzrósł wraz z płacą minimalną … ustawowy próg to jej 1/4.”</div>
<p class="ocena">W0: kwota trafna, halucynacja klasy <b>W</b> w wątku pobocznym (historia progu). W1, z dostępem do sieci: przytaknięcie pułapce, zła kwota, art. 119 § 1 k.w. powołany z fałszywą treścią — klasa <b>W</b> w rdzeniu, 4 z 6 powołań błędne. Wyszukiwanie nie zastąpiło sprawdzenia brzmienia na datę.</p></div>
<div class="blok"><h3><a href="/benchmark/02/pytania/p07">P07</a> · zasadnicze powody rozstrzygnięcia · Claude Haiku 5.5, W0</h3>
<p><b>Pytanie</b> dotyczy postanowienia i zażalenia (art. 357 k.p.c.). Odpowiedź brzmi „tak” — i jest trafna co do kierunku.</p>
<div class="q">„…tydzień od ogłoszenia wyroku. Jeżeli strona nie była obecna przy ogłoszeniu, termin może liczyć się od doręczenia.”</div>
<p class="ocena">Cała odpowiedź dotyczy wyroku i apelacji zamiast postanowienia i zażalenia; art. 357 § 5 k.p.c. powołany z błędną treścią (klasy <b>T</b> i <b>F</b>). Ocena samego „tak/nie” uznałaby ją za prawidłową. Sonda z 24 zapytaniami pokazała, że wzorzec zależy od sformułowania pytania (raport, rozdz. 5.6).</p></div>
</div>
</div></section>

<section id="metodologia"><div class="wrap">
<h2>Metodologia w skrócie</h2>
<div class="lista">
<p><b>Pytania.</b> Dziesięć krótkich pytań zebranych w praktyce kancelarii, w brzmieniu wpisanym do czatu (literówki zachowane), z czterech dziedzin prawa i AI Act; sześć ma wbudowaną pułapkę — błędną lub nieaktualną przesłankę, którą system powinien skorygować.</p>
<p><b>Klucze.</b> Każde pytanie ma klucz: rdzeń odpowiedzi, rubrykę, kary, podstawy wymagane; każda podstawa sprawdzona u źródła na dzień 1.10.2026. Zmiany kluczy są datowane.</p>
<p><b>Modele i warunki.</b> Trzej dostawcy, osiem modeli, dwa warunki: W0 bez narzędzi, W1 z wyszukiwaniem w internecie narzędziem dostawcy. Jedna seria, jedna odpowiedź na pytanie.</p>
<p><b>Karty.</b> Kartę wypełnia najpierw model ze sprawdzeniem każdego powołania w ISAP, ELI, SAOS, sn.pl i portalach sądów, a sprawdza prawnik. Jeden błąd klasy F, T, W lub S daje etykietę „halucynacja”.</p>
<p><b>Ograniczenia.</b> Mała próba, jedno uruchomienie każdego systemu, jeden sprawdzający prawnik, reguły doprecyzowywane w trakcie pracy. 160 odpowiedzi to nie 160 niezależnych pytań.</p>
<p><b>Pełny opis:</b> <a href="/metodologia">metodologia według specyfikacji oceny</a> — kryteria, klasy błędów, sędziowie-modele, warstwa weryfikacji, koszt, wersjonowanie.</p>
</div>
</div></section>

<section id="dane"><div class="wrap">
<h2>Dane, kod i cytowanie</h2>
<p class="pod">Specyfikacja oceny, dziesięć pytań z kluczami, 160 odpowiedzi i kart, oceny sędziów, raporty warstwy weryfikacji, koszty i skrypty liczące każdą liczbę raportu: <a href="/dane">zbiór danych i kod</a>. Raport i artykuł metodologiczny: <a href="/raporty">raporty</a>.</p>
<p>Piotrowski A., Koman A. (2026). <i>LexAlpha Lab · Benchmark 02 · pytania prawne</i>. Wersja {WERSJA_RAPORTU}, {DATA_RAPORTU}. <a href="/reports/lexalpha_lab_benchmark_02.pdf">PDF</a><br>
Piotrowski A. (2026). <i>„Hallucination” Is Not Enough: Why Legal LLM Benchmarks Should Measure „Correctly Grounded”</i>. LexAlpha Lab, v1.2, 26.10.2026. <a href="https://doi.org/10.5281/zenodo.23674794">doi:10.5281/zenodo.23674794</a> · <a href="https://papers.ssrn.com/abstract=7672779">SSRN</a></p>
<pre>{E(BIBTEX)}</pre>
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
<article><div class="wrap">

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
<p>Benchmark prowadzi LexAlpha Lab, laboratorium badawcze kancelarii KTZR w Gdańsku. Autorzy: Adam Piotrowski (radca prawny; projekt metodologii, klucze, karty, raport) i Andrzej Koman (COO LexAlpha). Badanie jest finansowane ze środków własnych kancelarii. Żaden dostawca modeli nie uczestniczył w przygotowaniu badania ani go nie finansował; autorzy nie przekazywali dostawcom wyników przed publikacją. Kancelaria korzysta w pracy z narzędzi wymienionych dostawców na warunkach komercyjnych i rozwija własne narzędzia prawnicze, których w benchmarku nie ocenia.</p>
</section>

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


LISTA = ['<div class="siatka-pyt">']
for pid in PYT:
    q, t, st = PYTANIA[pid], PYTANIA_T[pid], statystyka(pid)
    LISTA.append(f'<a href="/benchmark/02/pytania/{pid.lower()}"><span class="id">{pid} · {E(t[1])} · {"pułapka" if q["trap"] else "bez pułapki"}</span><h2>{E(TYTUL[pid])}</h2>'
                 f'<span class="st">halucynacje <b>{st["W0"]["hal"]}</b> → <b>{st["W1"]["hal"]}</b> z 8 · poprawnie ugruntowane <b>{st["W0"]["pu"]}</b> → <b>{st["W1"]["pu"]}</b> z 8 · śr. A {E(t[8])} %</span></a>')
LISTA.append("</div>")
PYT_LISTA = f"""
<header class="pod-hero"><div class="wrap">
<h1>Dziesięć pytań Benchmarku 02</h1>
<p class="lead">Pytania użyte w badaniu wraz z wersjami oryginalnymi z praktyki (w trzech pytaniach przed badaniem uzupełniono brakujące dane), z pułapką tam, gdzie ją zastawiono, kluczem odpowiedzi i wynikami ośmiu modeli w dwóch warunkach.</p>
<div class="meta">Stan prawny 1.10.2026 · klucze zatwierdzone w wersjach z 10–18.10.2026 · liczby „W0 → W1” to wynik bez narzędzi i z wyszukiwaniem, z ośmiu modeli</div>
</div></header>
<section><div class="wrap">
{"".join(LISTA)}
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
<p class="legenda" style="display:block"><span class="kl ok">✓</span> poprawnie ugruntowana · <span class="kl">–</span> bez halucynacji, ale rdzeń niepełny albo brak sprawdzonego źródła · <span class="kl bl">T</span> <span class="kl bl">W</span> <span class="kl bl">F</span> <span class="kl bl">S</span> klasy błędu w odpowiedzi z halucynacją (<a href="/metodologia#halucynacja">definicje</a>) · <span class="kl">blokada</span> tekst zablokowany przez filtr dostawcy, bez etykiety · blok A = kryteria sprawdzane wobec klucza i źródła (<a href="/metodologia#karta">kryteria oceny</a>)</p>
<p class="uwaga">Liczby dotyczą jednej odpowiedzi każdego modelu na to pytanie w każdym warunku. Nie mówią nic o wariancji między uruchomieniami ani o innych pytaniach z tej dziedziny.</p>
</section>
<p style="display:flex;justify-content:space-between;font:14px Inter,system-ui,sans-serif;margin-top:24px"><span>{poprz}</span><a href="/benchmark/02/pytania">wszystkie pytania</a><span>{nast}</span></p>
</div></article>
"""
    strona(f"/benchmark/02/pytania/{pid.lower()}", f"{TYTUL[pid]} — {pid} · LawBenchmark.pl",
           f"Pytanie {pid} Benchmarku 02 ({t[1]}): brzmienie, {'pułapka, ' if q['trap'] else ''}klucz odpowiedzi i wyniki ośmiu modeli językowych bez narzędzi i z wyszukiwaniem.",
           PYT_STRONA, okr=[("Benchmark 02", None), ("Pytania", "/benchmark/02/pytania"), (pid, None)], tu="/benchmark/02/pytania")

# =====================================================================
# 4. Raporty
# =====================================================================
LD_RAPORT = {"@context": "https://schema.org", "@type": "Report", "name": "LexAlpha Lab · Benchmark 02 · pytania prawne", "version": WERSJA_RAPORTU,
             "datePublished": "2026-10-27", "inLanguage": "pl", "url": f"{BAZA}/reports/lexalpha_lab_benchmark_02.pdf", "encodingFormat": "application/pdf",
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
<p><b>Piotrowski A., Koman A.</b> (2026). <i>LexAlpha Lab · Benchmark 02 · pytania prawne.</i> Wersja {WERSJA_RAPORTU}, {DATA_RAPORTU}, 44 strony. <a class="btn s" href="/reports/lexalpha_lab_benchmark_02.pdf">PDF</a></p>
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
<tr><td><code>data/</code></td><td>warstwa maszynowa: <code>questions</code>, <code>keys</code>, <code>answers</code>, <code>cards</code>, <code>judgments</code>, <code>verification</code> jako JSONL (pola po angielsku, treść po polsku) z kartą zbioru</td><td class="num">6 plików</td></tr>
<tr><td><code>reports/</code></td><td>raport Benchmark 02 (PDF, HTML, źródła Markdown, <code>dane.py</code>) i artykuł v1.2</td><td class="num">2</td></tr>
<tr><td><code>tools/</code></td><td>skrypty biegów systemów i sędziów, porównanie sędziów z kartami, warstwa weryfikacji, eksport JSONL, budowa tej strony</td><td class="num">—</td></tr>
</tbody></table></div>
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
# 6. EN
# =====================================================================
EN_ROWS = "".join(f'<tr><td class="model">{E(m)}</td><td class="num ok">{PARA[m]["W0"]["pu"]}</td><td class="num ok">{PARA[m]["W1"]["pu"]}</td>'
                  f'<td class="num bad">{PARA[m]["W0"]["hal"]}</td><td class="num bad">{PARA[m]["W1"]["hal"]}</td></tr>' for m in MODELE)
EN = f"""
<header class="hero"><div class="wrap">
<h1>How do language models answer questions about Polish law?</h1>
<p class="lead">LawBenchmark.pl measures correctness, hallucinations and grounding in official legal sources, with and without web search. A project of LexAlpha Lab, the research unit of the law firm KTZR (Gdańsk, Poland).</p>
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
mapa.append(f'<url><loc>{BAZA}/reports/lexalpha_lab_benchmark_02.pdf</loc><lastmod>2026-10-27</lastmod></url>')
mapa.append(f'<url><loc>{BAZA}/reports/Piotrowski_2026_correctly_grounded_v1.2.pdf</loc><lastmod>2026-10-26</lastmod></url>')
mapa.append("</urlset>")
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(mapa) + "\n")
print("site/ OK;", len(STRONY), "stron;", len(WIERSZE), "wierszy wyników")
