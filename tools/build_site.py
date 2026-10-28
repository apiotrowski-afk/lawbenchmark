# -*- coding: utf-8 -*-
"""Buduje statyczną stronę lawbenchmark.pl do katalogu site/ z danych repozytorium.

Źródła: reports/benchmark-02/src/dane.py (tabela wyników liczona z kart), PDF-y raportów.
Użycie (z katalogu repo): python3 -I tools/build_site.py
Nic nie wysyła; wdrożenie robi GitHub Actions (.github/workflows/deploy.yml).
"""
import html
import importlib.util
import os
import shutil
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(REPO, "reports", "benchmark-02", "src")
SITE = os.path.join(REPO, "site")

sys.path.insert(0, SRC)
os.chdir(SRC)  # dane.py uruchamia zestawienie_tier.py względem repo
spec = importlib.util.spec_from_file_location("dane", os.path.join(SRC, "dane.py"))
dane = importlib.util.module_from_spec(spec); spec.loader.exec_module(dane)
T, L = dane.TABELE, dane.LICZBY


def md_tabela_do_html(md):
    wiersze = [w for w in md.strip().splitlines() if w.startswith("|")]
    naglowek = [c.strip() for c in wiersze[0].strip("|").split("|")]
    out = ["<table><thead><tr>" + "".join(f"<th>{html.escape(c)}</th>" for c in naglowek) + "</tr></thead><tbody>"]
    for w in wiersze[2:]:
        kom = [c.strip() for c in w.strip("|").split("|")]
        out.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in kom) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


os.makedirs(os.path.join(SITE, "reports"), exist_ok=True)
for src, dst in [("reports/benchmark-02/lexalpha_lab_benchmark_02.pdf", "reports/lexalpha_lab_benchmark_02.pdf"),
                 ("reports/paper-v1.2/Piotrowski_2026_correctly_grounded_v1.2.pdf", "reports/Piotrowski_2026_correctly_grounded_v1.2.pdf")]:
    shutil.copy2(os.path.join(REPO, src), os.path.join(SITE, dst))

tabela = md_tabela_do_html(T["WYNIKI"])
n_pu = L["pu"]; n_hal = L["hal"]

strona = f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LawBenchmark.pl — benchmark modeli językowych w polskim prawie</title>
<meta name="description" content="Benchmark LLM na polskim prawie: krótkie pytania prawne, każde powołanie sprawdzone w źródle urzędowym. Projekt LexAlpha Lab (KTZR).">
<link rel="canonical" href="https://lawbenchmark.pl/">
<style>
:root{{--ink:#1a1a1a;--muted:#5c5c5c;--hue:#1f4e79;--light:#eef3f8;--bg:#ffffff;--line:#e2e6ea}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--ink:#ececec;--muted:#a8a8a8;--hue:#8fb3d9;--light:#1d2730;--bg:#121619;--line:#2a3238}}}}
:root[data-theme="dark"]{{--ink:#ececec;--muted:#a8a8a8;--hue:#8fb3d9;--light:#1d2730;--bg:#121619;--line:#2a3238}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.55 Georgia,"Times New Roman",serif}}
header,main,footer{{max-width:1040px;margin:0 auto;padding:0 16px}}
header{{padding-top:40px}}
.eyebrow{{font:600 13px/1 system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--hue)}}
h1{{font-size:clamp(28px,5vw,40px);line-height:1.15;margin:12px 0 8px}}
.lead{{font-size:19px;color:var(--muted);max-width:760px}}
.kpi{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:28px 0}}
.kpi div{{background:var(--light);border-radius:8px;padding:14px 16px}}
.kpi b{{display:block;font-size:30px;line-height:1;font-family:system-ui,sans-serif}}
.kpi span{{font-size:13px;color:var(--muted);font-family:system-ui,sans-serif}}
h2{{font-size:24px;margin:40px 0 10px}}
p{{max-width:760px}}
table{{border-collapse:collapse;width:100%;font:14px/1.4 system-ui,sans-serif;margin:16px 0}}
th,td{{padding:7px 8px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}}
th{{background:var(--light);font-weight:600}}
.scroll{{overflow-x:auto}}
.btn{{display:inline-block;background:var(--hue);color:#fff;text-decoration:none;padding:10px 16px;border-radius:6px;font:600 15px system-ui,sans-serif;margin:6px 8px 6px 0}}
a{{color:var(--hue)}}
footer{{margin-top:56px;padding:24px 16px 40px;border-top:1px solid var(--line);color:var(--muted);font:14px/1.5 system-ui,sans-serif}}
</style>
</head>
<body>
<header>
<div class="eyebrow">LawBenchmark.pl · projekt LexAlpha Lab</div>
<h1>Benchmark modeli językowych w polskim prawie</h1>
<p class="lead">Krótkie pytania prawne w takiej postaci, w jakiej prawnik wpisuje je do czatu. Każde powołanie przepisu i orzeczenia sprawdzone w źródle urzędowym na dzień stanu prawnego. Reguły oceny zapisane z datą, karty wzorcowe publiczne.</p>
<div class="kpi">
<div><b>8</b><span>modeli, 3 dostawców</span></div>
<div><b>10</b><span>pytań, 2 warunki (W0 / W1)</span></div>
<div><b>160</b><span>odpowiedzi ocenionych</span></div>
<div><b>{n_pu}</b><span>poprawnie ugruntowanych</span></div>
<div><b>{n_hal}</b><span>z co najmniej jedną halucynacją</span></div>
</div>
<a class="btn" href="reports/lexalpha_lab_benchmark_02.pdf">Raport Benchmark 02 (PDF)</a>
<a class="btn" href="reports/Piotrowski_2026_correctly_grounded_v1.2.pdf">Artykuł metodologiczny v1.2 (EN, PDF)</a>
</header>
<main>
<h2>Benchmark 02 · pytania prawne (27.10.2026)</h2>
<p>Osiem modeli trzech dostawców odpowiadało na dziesięć pytań z postępowania cywilnego, administracyjnego, prawa wykroczeń, prawa autorskiego i AI Act, każdy bez narzędzi (W0) i z wyszukiwaniem w internecie (W1). Odpowiedź jest <strong>poprawnie ugruntowana</strong>, gdy ma pełny rdzeń i ani jednego twierdzenia o źródle prawa niezgodnego z tekstem urzędowym. Zbiór kalibracyjny: dziesięć pytań, jedna seria, karty sprawdzał jeden prawnik — nie ranking.</p>
<div class="scroll">{tabela}</div>
<p>A % — blok obiektywny (rdzeń, podstawy, powołania), B % — blok ocenny. Koszt według cenników z 18.10.2026 (równoważnik API; „≥” — dolne oszacowanie). Pełne definicje, klasy błędów i zastrzeżenia: rozdziały 4 i 8 raportu.</p>
<h2>Jak oceniamy</h2>
<p>Kartę każdej odpowiedzi wypełnia model ze sprawdzeniem każdego powołania w ISAP, ELI, SAOS i bazach sądów, a sprawdza prawnik. Jedno twierdzenie niezgodne z tekstem urzędowym (zmyślone źródło, prawdziwy przepis z cudzą treścią, dawne brzmienie, sygnatura z tezą z innej sprawy) daje etykietę „halucynacja”. Te same odpowiedzi ocenia pięciu sędziów-modeli i warstwa weryfikacji powołań; ich zgodność z kartami jest częścią raportu.</p>
<h2>Dane i kod</h2>
<p>Specyfikacja oceny, pytania z pełnymi kluczami, odpowiedzi szesnastu systemów, karty ocen, oceny sędziów i skrypty trafią wkrótce do publicznego repozytorium na GitHubie. Do tego czasu materiały udostępniamy na prośbę: <a href="mailto:a.piotrowski@ktzr.pl">a.piotrowski@ktzr.pl</a>.</p>
</main>
<footer>LawBenchmark.pl jest projektem LexAlpha Lab, laboratorium badawczego kancelarii <a href="https://www.ktzr.pl/">KTZR</a> (Gdańsk). Treści na licencji CC BY 4.0. Benchmark nie jest poradą prawną i nie służy rankingowi produktów.</footer>
</body>
</html>
"""
open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(strona)
print("site/index.html OK;", len(strona), "znaków")
