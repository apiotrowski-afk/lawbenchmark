# -*- coding: utf-8 -*-
"""Buduje statyczną stronę lawbenchmark.pl do katalogu site/ z danych repozytorium.

Źródła: reports/benchmark-02/src/dane.py (tabele liczone z kart), karty w cards/ (studia przypadku), PDF-y raportów.
Układ (ustalony 28.10.2026 po przeglądzie stron benchmarkowych): nagłówek z kotwicami → hero z paskiem zakresu →
„jak czytać wyniki” → wykres par W0/W1 (SVG rysowany tutaj, bez bibliotek) → tabela par (na telefonie karty) →
klasy błędów → dwa studia przypadku → metodologia, ograniczenia, dane, cytowanie. Tryb ciemny: systemowy + przełącznik.
Użycie (z katalogu repo): python3 -I tools/build_site.py. Nic nie wysyła; wdrożenie: tools/deploy_hosting.py.
"""
import html
import importlib.util
import os
import re
import shutil
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(REPO, "reports", "benchmark-02", "src")
SITE = os.path.join(REPO, "site")
DATA_KART, WERSJA_RAPORTU, DATA_RAPORTU = "25.10.2026", "1.0", "27.10.2026"

sys.path.insert(0, SRC)
os.chdir(SRC)
spec = importlib.util.spec_from_file_location("dane", os.path.join(SRC, "dane.py"))
dane = importlib.util.module_from_spec(spec); spec.loader.exec_module(dane)
T, L = dane.TABELE, dane.LICZBY
E = html.escape

# ---------- dane z tabeli wyników ----------
WIERSZE = []
for w in T["WYNIKI"].strip().splitlines()[2:]:
    c = [x.strip() for x in w.strip("|").split("|")]
    WIERSZE.append({"model": c[0], "war": c[1], "A": c[2], "B": c[3], "hal": int(c[4]), "pu": int(c[5]),
                    "koszt": c[6], "koszt_pu": c[7], "spr": c[8]})
MODELE = []
for r in WIERSZE:
    if r["model"] not in MODELE:
        MODELE.append(r["model"])
PARA = {m: {r["war"]: r for r in WIERSZE if r["model"] == m} for m in MODELE}
KLASY = [[x.strip() for x in w.strip("|").split("|")] for w in T["KLASY"].strip().splitlines()[2:]]


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
            continue
        out.append(f'<line x1="{xa:.0f}" y1="{y}" x2="{xb:.0f}" y2="{y}" class="lacz"/>')
        out.append(f'<circle cx="{xa:.0f}" cy="{y}" r="6" class="w0" style="stroke:{kolor}"/>')
        out.append(f'<circle cx="{xb:.0f}" cy="{y}" r="6" style="fill:{kolor}"/>')
        ya = y + 20 if abs(a - b) <= 1 else y - 11  # bliskie wartości: etykieta W0 pod linią
        out.append(f'<text x="{xa:.0f}" y="{ya}" class="lb" text-anchor="middle">{a}</text>')
        out.append(f'<text x="{xb:.0f}" y="{y - 11}" class="lb" text-anchor="middle" style="fill:{kolor}">{b}</text>')
    return (f'<svg viewBox="0 0 470 {wys}" role="img" aria-label="{E(tytul)}" class="wykres">'
            '<style>.pt{font:600 14px Inter,system-ui,sans-serif;fill:var(--ink)} .et{font:500 13px Inter,system-ui,sans-serif;fill:var(--ink)}'
            ' .os{font:12px Inter,system-ui,sans-serif;fill:var(--muted)} .lb{font:600 12px Inter,system-ui,sans-serif;fill:var(--muted);font-variant-numeric:tabular-nums}'
            ' .siatka{stroke:var(--line);stroke-width:1} .lacz{stroke:var(--muted);stroke-width:2;opacity:.6} .w0{fill:var(--surface);stroke-width:2.5}</style>'
            + "\n".join(out) + '</svg>')


WYKRES = ('<div class="dwa wyk">' + panel("pu", "Poprawnie ugruntowane (z 10) — więcej = lepiej", "var(--ok)")
          + panel("hal", "Odpowiedzi z halucynacją (z 10) — mniej = lepiej", "var(--bad)") + '</div>')

# ---------- tabela par i karty mobilne ----------
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

KL_OPIS = {"T": "treść, której w źródle nie ma", "W": "brzmienie z innej daty podane jako obowiązujące",
           "F": "źródło lub jednostka redakcyjna nie istnieje", "S": "zniekształcony identyfikator (sygnatura, numer)"}
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

strona = f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LawBenchmark.pl — modele językowe a polskie prawo</title>
<meta name="description" content="Jak modele językowe odpowiadają na pytania z polskiego prawa: poprawność, halucynacje i oparcie w źródłach urzędowych, bez narzędzi i z wyszukiwaniem. Projekt LexAlpha Lab.">
<link rel="canonical" href="https://lawbenchmark.pl/">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:title" content="LawBenchmark.pl — modele językowe a polskie prawo">
<meta property="og:description" content="Benchmark 02: 8 modeli, 10 pytań, 160 odpowiedzi, każde powołanie sprawdzone w źródle urzędowym.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<style>
:root{{--brand:#1f4e79;--ok:#13766d;--bad:#b44739;--bg:#f7f8fa;--surface:#ffffff;--ink:#17212b;--muted:#5b6670;--line:#dce2e8;--soft:#eef2f6}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--brand:#8ab9e2;--ok:#4fb3a9;--bad:#e07a6c;--bg:#111820;--surface:#19232e;--ink:#e6edf3;--muted:#9aa7b4;--line:#2a3643;--soft:#1f2b37}}}}
:root[data-theme="dark"]{{--brand:#8ab9e2;--ok:#4fb3a9;--bad:#e07a6c;--bg:#111820;--surface:#19232e;--ink:#e6edf3;--muted:#9aa7b4;--line:#2a3643;--soft:#1f2b37}}
*{{box-sizing:border-box;min-width:0}} html{{scroll-behavior:smooth}} body{{overflow-x:hidden}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 "Source Serif 4",Georgia,serif}}
.wrap{{max-width:1200px;margin:0 auto;padding:0 16px}}
nav{{position:sticky;top:0;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);z-index:5}}
nav .wrap{{display:flex;align-items:center;gap:20px;height:56px;font:500 14px Inter,system-ui,sans-serif}}
nav .logo{{font-weight:600;color:var(--ink);text-decoration:none;letter-spacing:.01em}} nav .logo small{{color:var(--muted);font-weight:500;margin-left:8px}}
nav a{{color:var(--muted);text-decoration:none}} nav a:hover{{color:var(--ink)}} nav .sp{{flex:1}}
@media (max-width:760px){{nav a:not(.logo){{display:none}}}}
nav button{{background:none;border:1px solid var(--line);color:var(--muted);border-radius:6px;padding:4px 10px;font:inherit;cursor:pointer}}
.hero{{padding:56px 0 40px}} .hero h1{{font:600 clamp(30px,4.6vw,46px)/1.12 "Source Serif 4",Georgia,serif;margin:0 0 14px;max-width:820px}}
.hero p.lead{{font-size:20px;color:var(--muted);max-width:720px;margin:0 0 22px}}
.zakres{{display:flex;flex-wrap:wrap;gap:8px 22px;font:500 15px Inter,system-ui,sans-serif;color:var(--ink);margin-bottom:10px}} .zakres b{{font-weight:600}}
.meta{{font:13px Inter,system-ui,sans-serif;color:var(--muted);margin-bottom:22px}}
.btn{{display:inline-block;border-radius:6px;padding:10px 16px;font:600 14px Inter,system-ui,sans-serif;text-decoration:none;margin:0 10px 10px 0}}
.btn.p{{background:var(--brand);color:#fff}} .btn.s{{border:1px solid var(--line);color:var(--ink);background:var(--surface)}}
.uwaga{{font:14px Inter,system-ui,sans-serif;color:var(--muted);max-width:720px;border-left:3px solid var(--line);padding-left:12px;margin-top:8px}}
section{{padding:40px 0 8px}} h2{{font:600 28px/1.2 "Source Serif 4",Georgia,serif;margin:0 0 6px}} .pod{{color:var(--muted);margin:0 0 20px;max-width:720px}}
.dwa{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} @media (max-width:760px){{.dwa{{grid-template-columns:1fr}}}}
.blok{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px 20px}}
.blok h3{{margin:0 0 6px;font:600 20px Inter,system-ui,sans-serif}} .blok p{{margin:0;color:var(--muted);font-size:16px}}
.blok.ok h3{{color:var(--ok)}} .blok.bad h3{{color:var(--bad)}}
.teza{{font:600 20px/1.4 "Source Serif 4",Georgia,serif;margin:18px 0 0;max-width:820px}}
.wyk{{gap:12px}} .wykres{{width:100%;height:auto;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px}}
.legenda{{display:flex;gap:20px;flex-wrap:wrap;font:13px Inter,system-ui,sans-serif;color:var(--muted);margin:10px 0 0}}
.legenda i{{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;margin-right:6px;border:2px solid var(--muted)}} .legenda i.f{{background:var(--muted)}}
table.pary{{width:100%;border-collapse:collapse;font:14px/1.35 Inter,system-ui,sans-serif;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden;font-variant-numeric:tabular-nums}}
.pary th,.pary td{{padding:9px 10px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}} .pary th{{background:var(--soft);font-weight:600}} .pary th small{{font-weight:500;color:var(--muted)}}
.pary .num{{text-align:right}} .pary tr.p0 td{{border-bottom:0}} .pary td.model{{font-weight:600}} .pary tr.p1 td{{padding-top:2px}}
.war{{display:inline-block;font:600 11px Inter,system-ui,sans-serif;padding:2px 6px;border-radius:4px;border:1px solid var(--line);color:var(--muted)}} .war.w1{{background:var(--brand);color:#fff;border-color:var(--brand)}}
.ok{{color:var(--ok)}} .bad{{color:var(--bad)}} td.ok,td.bad{{font-weight:600}}
.scroll{{overflow-x:auto}} .karty{{display:none}}
@media (max-width:760px){{.scroll{{display:none}} .karty{{display:grid;gap:12px}} .karta{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px}}
.karta h3{{margin:0 0 8px;font:600 17px Inter,system-ui,sans-serif}} .kw{{display:grid;grid-template-columns:auto 1fr 1fr;gap:4px 10px;align-items:center;font:14px Inter,system-ui,sans-serif;padding:6px 0;border-top:1px solid var(--line)}}
.kw .m{{grid-column:2/4;color:var(--muted);font-size:13px}}}}
.klasy{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}} .klasa{{display:flex;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px}}
.znak{{flex:none;width:36px;height:36px;border:2px solid var(--ink);border-radius:8px;display:grid;place-items:center;font:600 16px Inter,system-ui,sans-serif}}
.klasa b{{display:block;font:600 15px Inter,system-ui,sans-serif}} .klasa .m b{{display:inline;font-size:13px}} .klasa .m{{display:block;font:13px Inter,system-ui,sans-serif;color:var(--muted);margin-top:4px}}
.przyp{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} @media (max-width:760px){{.przyp{{grid-template-columns:1fr}}}}
.przyp .blok h3{{font-size:17px}} .przyp .blok p{{color:var(--ink)}} .q{{border-left:3px solid var(--line);padding:2px 0 2px 12px;margin:10px 0;color:var(--muted);font-style:italic}}
.ocena{{font:13px Inter,system-ui,sans-serif;color:var(--muted);margin-top:8px}}
.lista{{columns:2;column-gap:40px;max-width:1000px}} @media (max-width:760px){{.lista{{columns:1}}}} .lista p{{break-inside:avoid;margin:0 0 12px}} .lista b{{font-family:Inter,system-ui,sans-serif;font-size:15px}}
pre{{white-space:pre-wrap;word-break:break-word;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:12px 14px;font:13px/1.45 ui-monospace,Menlo,Consolas,monospace;overflow-x:auto}}
footer{{margin-top:48px;border-top:1px solid var(--line);padding:24px 0 40px;font:14px/1.5 Inter,system-ui,sans-serif;color:var(--muted)}} a{{color:var(--brand)}}
</style>
</head>
<body>
<nav><div class="wrap"><a class="logo" href="#">LawBenchmark.pl <small>LexAlpha Lab</small></a><span class="sp"></span>
<a href="#wyniki">Wyniki</a><a href="#bledy">Błędy</a><a href="#przyklady">Przykłady</a><a href="#metodologia">Metodologia</a><a href="#dane">Dane</a>
<button id="motyw" aria-label="Przełącz motyw">◐</button></div></nav>

<header class="hero"><div class="wrap">
<h1>Jak modele językowe odpowiadają na pytania z polskiego prawa?</h1>
<p class="lead">Badamy poprawność odpowiedzi, halucynacje i oparcie w źródłach urzędowych — bez narzędzi oraz z wyszukiwaniem w internecie.</p>
<div class="zakres"><span><b>10</b> pytań</span><span><b>8</b> modeli, 3 dostawców</span><span><b>2</b> warunki: W0 / W1</span><span><b>160</b> odpowiedzi</span><span><b>1 454</b> powołań sprawdzonych u źródła</span></div>
<div class="meta">Benchmark 02 · raport wersja {WERSJA_RAPORTU} z {DATA_RAPORTU} · karty wzorcowe w stanie z {DATA_KART} · stan prawny 1.10.2026</div>
<a class="btn p" href="#wyniki">Zobacz wyniki</a><a class="btn s" href="reports/lexalpha_lab_benchmark_02.pdf">Raport (PDF, 44 str.)</a><a class="btn s" href="reports/Piotrowski_2026_correctly_grounded_v1.2.pdf">Artykuł metodologiczny (EN)</a>
<p class="uwaga">Wyniki dotyczą tego zestawu pytań i tych konfiguracji: dziesięć pytań, jedna seria, karty sprawdzał jeden prawnik. Nie stanowią ogólnego rankingu produktów.</p>
</div></header>

<section id="czytanie"><div class="wrap">
<h2>Jak czytać wyniki</h2>
<div class="dwa">
<div class="blok ok"><h3>Poprawnie ugruntowane ↑</h3><p>Odpowiedź ma pełny rdzeń (trafia w sedno pytania) i ani jednego twierdzenia o źródle prawa niezgodnego z tekstem urzędowym, a co najmniej jedno powołanie zostało sprawdzone u źródła.</p></div>
<div class="blok bad"><h3>Z halucynacją ↓</h3><p>Odpowiedź zawiera co najmniej jedno twierdzenie o przepisie lub orzeczeniu niezgodne z tekstem urzędowym na dzień stanu prawnego — także wtedy, gdy sam wniosek jest trafny.</p></div>
</div>
<p class="teza">Brak halucynacji nie wystarcza: odpowiedź bez błędnych powołań, ale z niepełnym rdzeniem albo bez żadnego sprawdzonego źródła, nie jest poprawnie ugruntowana.</p>
</div></section>

<section id="wyniki"><div class="wrap">
<h2>Wyniki: bez narzędzi (W0) i z wyszukiwaniem (W1)</h2>
<p class="pod">Każdy model odpowiadał na te same dziesięć pytań dwa razy. Jedna odpowiedź to 10 punktów procentowych; linia łączy oba warunki tego samego modelu i pokazuje także pogorszenie.</p>
{WYKRES}
<div class="legenda"><span><i></i>W0 — bez narzędzi</span><span><i class="f"></i>W1 — z wyszukiwaniem w internecie</span><span>Kolejność modeli jak w raporcie (dostawcami), nie według wyniku.</span></div>
<h2 style="margin-top:36px;font-size:22px">Wyniki szczegółowe</h2>
<p class="pod">Blok A — kryteria obiektywne (rdzeń, podstawy prawne, powołania), blok B — ocenne (kalibracja, kompletność, użyteczność). Koszt serii dziesięciu odpowiedzi według cenników z 18.10.2026 jako równoważnik API; „≥” — dolne oszacowanie, bo narzędzie nie zapisuje części zużycia.</p>
<div class="scroll">{TABELA}</div>
<div class="karty">{KARTY}</div>
</div></section>

<section id="bledy"><div class="wrap">
<h2>Cztery klasy błędu</h2>
<p class="pod">Najczęstszym błędem nie jest zmyślone źródło. Jest nim prawdziwy przepis lub wyrok z treścią, której w nim nie ma, a zaraz potem dawne brzmienie przepisu podane jako obowiązujące — tego wyszukiwanie prawie nie zmienia.</p>
<div class="klasy">{KLASY_HTML}</div>
<p class="uwaga" style="margin-top:14px">Liczby to odpowiedzi z co najmniej jednym błędem danej klasy na 80 odpowiedzi w każdym warunku; jedna odpowiedź może mieć kilka klas. Łącznie {L["hal_W0"]} odpowiedzi z halucynacją w W0 i {L["hal_W1"]} w W1.</p>
</div></section>

<section id="przyklady"><div class="wrap">
<h2>Dwa przykłady z kart</h2>
<p class="pod">Każda ze 160 odpowiedzi ma kartę: punkt za każde kryterium, dowód ze źródła i klasa błędu. Dwa przypadki pokazują, czego nie widać w samych liczbach.</p>
<div class="przyp">
<div class="blok"><h3>P01 · próg wykroczenia · GPT-5.6 Terra, ten sam model w W0 i W1</h3>
<p><b>Pytanie</b> zakłada, że próg między wykroczeniem a przestępstwem przeciwko mieniu nadal rośnie z płacą minimalną (pułapka: od 1.10.2023 to stała kwota 800 zł, art. 119 § 1 k.w.).</p>
<div class="q">W0: „W 2026 r. granica … wynosi co do zasady 800 zł. Nie zmieniła się ona wraz ze wzrostem płacy minimalnej.”</div>
<div class="q">W1: „W 2026 r. próg wynosi 1 201,50 zł. Tak, próg wzrósł wraz z płacą minimalną … ustawowy próg to jej 1/4.”</div>
<p class="ocena">W0: kwota trafna, halucynacja klasy <b>W</b> w wątku pobocznym (historia progu). W1, z dostępem do sieci: przytaknięcie pułapce, zła kwota, art. 119 § 1 k.w. powołany z fałszywą treścią — klasa <b>W</b> w rdzeniu, 4 z 6 powołań błędne. Wyszukiwanie nie zastąpiło sprawdzenia brzmienia na datę.</p></div>
<div class="blok"><h3>P07 · zasadnicze powody rozstrzygnięcia · Claude Haiku 5.5, W0</h3>
<p><b>Pytanie</b> dotyczy postanowienia i zażalenia (art. 357 k.p.c.). Odpowiedź brzmi „tak” — i jest trafna co do kierunku.</p>
<div class="q">„…tydzień od ogłoszenia wyroku. Jeżeli strona nie była obecna przy ogłoszeniu, termin może liczyć się od doręczenia.”</div>
<p class="ocena">Cała odpowiedź dotyczy wyroku i apelacji zamiast postanowienia i zażalenia; art. 357 § 5 k.p.c. powołany z błędną treścią (klasy <b>T</b> i <b>F</b>). Ocena samego „tak/nie” uznałaby ją za prawidłową. Sonda z 24 zapytaniami pokazała, że wzorzec zależy od sformułowania pytania (raport, rozdz. 5.6).</p></div>
</div>
</div></section>

<section id="metodologia"><div class="wrap">
<h2>Metodologia i ograniczenia</h2>
<div class="lista">
<p><b>Pytania.</b> Dziesięć krótkich pytań zebranych w praktyce kancelarii, w brzmieniu wpisanym do czatu (literówki zachowane), z czterech dziedzin prawa i AI Act; sześć ma wbudowaną pułapkę — błędną lub nieaktualną przesłankę, którą system powinien skorygować.</p>
<p><b>Klucze.</b> Każde pytanie ma klucz: rdzeń odpowiedzi, rubrykę, kary, podstawy wymagane; każda podstawa sprawdzona u źródła na dzień 1.10.2026. Zmiany kluczy są datowane; dwa klucze (P09, P10) zmieniono po biegu, gdy orzecznictwo SN okazało się bardziej zniuansowane niż klucz — opisujemy to w raporcie.</p>
<p><b>Modele i warunki.</b> GPT-6.1 Sol, GPT-6 Astra, GPT-5.6 Terra (Codex CLI); Claude Opus, Sonnet i Haiku 5.5 (Claude Code); Gemini 3.8 Flash i Gemini 4 Argon (Vertex AI). W0: ten sam krótki wstęp, bez narzędzi. W1: dodatkowo wyszukiwanie w internecie narzędziem dostawcy. Jedna seria, jedna odpowiedź na pytanie.</p>
<p><b>Karty.</b> Kartę wypełnia najpierw model (Claude) ze sprawdzeniem każdego powołania w ISAP, ELI, SAOS, sn.pl i portalach sądów, a sprawdza prawnik. Jeden błąd klasy F, T, W lub S daje etykietę „halucynacja”. Sprawdzono 1 436 z 1 454 powołań; niesprawdzone nie obniżały oceny.</p>
<p><b>Sędziowie-modele i warstwa weryfikacji.</b> Te same odpowiedzi ocenia pięciu sędziów-modeli z wyszukiwaniem oraz kod sprawdzający powołania u źródła z modelem oceniającym poparcie tezy; ich zgodność z kartami (κ Cohena 0,58–0,90) i wpływ raportu weryfikacji na sędziego są częścią raportu.</p>
<p><b>Ograniczenia.</b> Mała próba (10 pytań, 5 z postępowania cywilnego), jedno uruchomienie każdego systemu, jeden sprawdzający prawnik, karty wypełniane wstępnie przez model z rodziny ocenianych systemów, reguły doprecyzowywane w trakcie pracy. 160 odpowiedzi to nie 160 niezależnych pytań. Przed cytowaniem liczb: rozdział 8 raportu.</p>
</div>
</div></section>

<section id="dane"><div class="wrap">
<h2>Dane, kod i cytowanie</h2>
<p class="pod">Specyfikacja oceny z rejestrem decyzji, dziesięć pytań z pełnymi kluczami, 160 odpowiedzi i kart, oceny sędziów, raporty warstwy weryfikacji, koszty oraz skrypty liczące każdą liczbę raportu trafią wkrótce do publicznego repozytorium na GitHubie. Do tego czasu udostępniamy je na prośbę: <a href="mailto:a.piotrowski@ktzr.pl">a.piotrowski@ktzr.pl</a>.</p>
<p>Piotrowski A., Koman A. (2026). <i>LexAlpha Lab · Benchmark 02 · pytania prawne</i>. Wersja {WERSJA_RAPORTU}, {DATA_RAPORTU}. <a href="reports/lexalpha_lab_benchmark_02.pdf">PDF</a><br>
Piotrowski A. (2026). <i>„Hallucination” Is Not Enough: Why Legal LLM Benchmarks Should Measure „Correctly Grounded”</i>. LexAlpha Lab, v1.2, 26.10.2026. <a href="https://doi.org/10.5281/zenodo.23674794">doi:10.5281/zenodo.23674794</a> · <a href="https://papers.ssrn.com/abstract=7672779">SSRN</a></p>
<pre>{E(BIBTEX)}</pre>
</div></section>

<footer><div class="wrap">LawBenchmark.pl jest projektem <b>LexAlpha Lab</b>, laboratorium badawczego kancelarii <a href="https://www.ktzr.pl/">KTZR</a> (Gdańsk). Autorzy: Adam Piotrowski, Andrzej Koman. Badanie finansowane ze środków własnych kancelarii; żaden dostawca modeli nie uczestniczył w jego przygotowaniu. Treści na licencji CC BY 4.0. Benchmark nie jest poradą prawną.</div></footer>
<script>
(function(){{var r=document.documentElement,b=document.getElementById('motyw');try{{var z=localStorage.getItem('motyw');if(z)r.setAttribute('data-theme',z);}}catch(e){{}}
b.addEventListener('click',function(){{var c=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');var n=c==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{{localStorage.setItem('motyw',n);}}catch(e){{}}}});}})();
</script>
</body>
</html>
"""
open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(strona)
open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8").write("User-agent: *\nAllow: /\nSitemap: https://lawbenchmark.pl/sitemap.xml\n")
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    '<url><loc>https://lawbenchmark.pl/</loc><lastmod>2026-10-28</lastmod><changefreq>monthly</changefreq></url>\n'
    '<url><loc>https://lawbenchmark.pl/reports/lexalpha_lab_benchmark_02.pdf</loc><lastmod>2026-10-27</lastmod></url>\n'
    '<url><loc>https://lawbenchmark.pl/reports/Piotrowski_2026_correctly_grounded_v1.2.pdf</loc><lastmod>2026-10-26</lastmod></url>\n</urlset>\n')
print("site/index.html OK;", len(strona), "znaków;", len(WIERSZE), "wierszy wyników")
