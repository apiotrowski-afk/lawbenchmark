"""Skład raportu „LexAlpha Lab · Benchmark 02 · pytania prawne” w identyfikacji Benchmarku 01
(na podstawie benchmark/skd/raport/zrodla/build.py).

Wejście: raport02_*.md (tekst) i dane.py (tabele i liczby liczone z kart, kluczy, ocen sędziów i pliku kosztu).
Wyjście: ../lexalpha_lab_benchmark_02.html (do przeglądania), lexalpha_lab_benchmark_02_print.html (do druku)
oraz ../lexalpha_lab_benchmark_02.pdf (WeasyPrint, fonty systemowe).
Użycie: python3 -I build.py
Skrypt nic nie publikuje i nie wysyła.
"""
import base64
import html
import os
import re
import sys

import markdown

SP = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SP)
sys.path.insert(0, SP)
import dane  # noqa: E402  (liczy wszystko przy imporcie i sprawdza zgodność z zestawienie_tier.py)

DATA = "wersja 1.1 · 29.10.2026"
RUNHEAD = "LEXALPHA LAB &nbsp;/&nbsp; BENCHMARK 02 · PYTANIA PRAWNE"
L = dane.LICZBY


def md(s):
    return markdown.markdown(s, extensions=["tables"])


PLIKI = ["raport02_front.md", "raport02_rozdz_2-4.md", "raport02_rozdz_5.md", "raport02_rozdz_6-7.md", "raport02_rozdz_8-9_aneksy.md"]
doc = "\n\n".join(open(f"{SP}/{p}", encoding="utf-8").read() for p in PLIKI)

# tabele z dane.py
def wstaw(m):
    k = m.group(1)
    assert k in dane.TABELE, k
    return dane.TABELE[k]
doc = re.sub(r"\{\{TAB:([A-Z_0-9]+)\}\}", wstaw, doc)
# liczby z dane.LICZBY w tekście: {{USD:klucz}} → kwota z dwoma miejscami po przecinku (przeliczana przy każdej budowie)
doc = re.sub(r"\{\{USD:([a-z_0-9]+)\}\}", lambda m: dane.pl(dane.LICZBY[m.group(1)], 2), doc)
assert "{{" not in doc

tytul = re.match(r"# (.+)", doc).group(1)
doc = doc[doc.find("\n"):]
AUT = re.search(r"\*\*Autorzy:\*\*\s*(.+)", doc)
AUTORZY = AUT.group(1).strip() if AUT else ""
doc = re.sub(r"\*\*Autorzy:\*\*.*\n", "", doc)
KOMENTARZ_AUT = ""  # współautor potwierdzony przez Adama 2026-10-25
LOGO_W = "data:image/png;base64," + base64.b64encode(open(f"{SP}/lx_logo_white.png", "rb").read()).decode()
LOGO_D = "data:image/png;base64," + base64.b64encode(open(f"{SP}/lx_logo_dark.png", "rb").read()).decode()

sekcje = re.split(r"\n(?=## )", doc.strip())
LEADY = {
    "1.": "Cel raportu, związek z Benchmarkiem 01 i z artykułem „Correctly grounded”, status zbioru.",
    "2.": "Dziesięć pytań, pułapki, para lustrzana, data stanu prawnego i zmiany kluczy po lekturze źródeł.",
    "3.": "Osiem modeli, warunki W0 i W1, ustawienia biegu; systemy kancelarii poza benchmarkiem.",
    "4.": "Bloki A i B, halucynacja zero-jedynkowa z klasami F/T/W/S, poprawne ugruntowanie, reguły graniczne z datami.",
    "5.": "160 odpowiedzi: wyniki, wpływ wyszukiwania, koszt, klasy błędów i przykłady z kart.",
    "6.": "Pięciu sędziów-modeli wobec kart prawnika: κ, wyszukiwania, czego nie widzą, preferencja rodziny, panel.",
    "7.": "Kod sprawdzający powołania w źródłach urzędowych, weryfikator poparcia i raport dla sędziego w trzech wariantach.",
    "8.": "Granice interpretacji wyników i niespójności danych wykryte przy składaniu raportu.",
    "9.": "Pięć wniosków i kroki przed zbiorem testowym.",
    "Aneks A": "Pytania w brzmieniu z biegu i rdzenie kluczy w skrócie.",
    "Aneks B": "Wynik każdej ze 160 odpowiedzi i ścieżki do materiału źródłowego.",
    "Aneks C": "Zgodność sędziów według pytania i ustawienia sędziów.",
    "Aneks D": "Pojęcia, nazwy robocze i ich odpowiedniki w artykule angielskim, identyfikatory systemów.",
}


def lead_for(n):
    for k, v in LEADY.items():
        if n.startswith(k):
            return v
    return None


def koloruj(h):
    """Macierze aneksu B: ✓ zielone, – żółte, klasy błędu i blokada czerwone."""
    def tab(m):
        t = m.group(0)
        if "<th>P01</th>" not in t or "<th>System</th>" not in t:
            return t
        def cell(c):
            v = c.group(1).strip()
            if v == "✓":
                cls = "ok"
            elif v == "–":
                cls = "half"
            elif v == "blokada" or re.fullmatch(r"[FTWS](,[FTWS])*", v):
                cls = "bad"
            else:
                cls = None
            return f'<td class="c {cls}">{v}</td>' if cls else f'<td class="c">{v}</td>'
        return re.sub(r"<td>([^<]*)</td>", lambda c: cell(c) if not re.match(r"[A-Z][a-z]+ W[01]", c.group(1)) else c.group(0), t)
    return re.sub(r"<table>.*?</table>", tab, h, flags=re.S)


def znaczniki(h):
    return re.sub(r"\[do uzupełnienia[^\]]*\]", lambda m: f'<mark class="todo">{m.group(0)}</mark>', h, flags=re.I)


def runhead(prawy):
    return f'<div class="runhead"><span class="rh-l"><img src="{LOGO_D}" alt="LexAlpha">{RUNHEAD}</span><span>{html.escape(prawy.upper())}</span></div>'


body = []
for s in sekcje:
    naglowek, _, tresc = s.partition("\n")
    naglowek = naglowek.lstrip("# ").strip()
    m = re.match(r"(\d+)\.\s+(.*)", naglowek)
    aneks = naglowek.startswith("Aneks") or naglowek.startswith("Literatura") or naglowek.startswith("Źródła")
    if m:
        eyebrow = f"{int(m.group(1)):02d} / {m.group(2)}"; tyt = m.group(2)
        krotki = re.sub(r"[:(].*$", "", m.group(2)).strip()
    elif naglowek.startswith("Aneks"):
        eyebrow = naglowek.split(".")[0]; tyt = naglowek.split(". ", 1)[-1]; krotki = eyebrow
    else:
        eyebrow = tyt = krotki = naglowek
    lead = lead_for(naglowek)
    inner = znaczniki(koloruj(md(tresc)))
    inner = re.sub(r"(<p><strong>Tabela [A-Z]?\.?\d+\..*?</strong>.*?</p>\s*<table>.*?</table>)", r'<div class="card tabela">\1</div>', inner, flags=re.S)
    # tabele poza układem dwukolumnowym: WeasyPrint 68 pada na długiej tabeli column-span:all łamanej między stronami
    inner = re.sub(r'(<div class="card tabela">.*?</table></div>)', r'</div>\1<div class="kol">', inner, flags=re.S)
    if naglowek == "Abstrakt":
        body.append(f'<section class="rozdzial abstrakt">{runhead("Abstrakt")}<h2 class="tytul-art">{html.escape(tytul)}</h2>'
                    f'<p class="autorzy">{html.escape(AUTORZY)}{KOMENTARZ_AUT} · {DATA}</p><div class="abstrakt-blok"><p class="eyebrow">ABSTRAKT</p>{inner}</div></section>')
        continue
    klasy = "rozdzial" + (" aneks" if aneks else "") + (" literatura" if naglowek in ("Literatura",) or naglowek.startswith("Źródła") else "") \
        + (" ciag" if naglowek.startswith("Źródła") else "")
    body.append(f'<section class="{klasy}">{runhead(krotki)}<p class="eyebrow">{html.escape(eyebrow.upper())}</p><h2>{html.escape(tyt)}</h2>'
                + (f'<p class="lead">{html.escape(lead)}</p>' if lead else "") + f'<div class="kol">{inner}</div></section>')

pl = dane.pl
TILES = [
    ("160", "odpowiedzi: 10 pytań × 8 modeli × 2 warunki (W0 bez narzędzi, W1 z wyszukiwaniem)"),
    (str(L["hal"]), f"odpowiedzi z co najmniej jedną halucynacją ({L['hal_W0']} w W0, {L['hal_W1']} w W1)"),
    (f"{L['pu_min']}–{L['pu_max']} z 10", f"odpowiedzi poprawnie ugruntowanych na model ({L['pu']} ze 160)"),
    (f"κ {pl(L['kappa_argon4v101_rozsz'], 2)}", "najlepszy sędzia-model (Gemini 4 Argon) na kartach sprawdzonych przed sędziami, n = 79"),
    (f"≥ {pl(L['koszt_pelny'], 2)} USD", f"pełny koszt badania: odpowiedzi ≥ {pl(L['koszt'], 2)}, sędziowie ≥ {pl(L['koszt_sedziowie'], 2)}, warstwa weryfikacji {pl(L['koszt_weryfikacja'], 2)} (bez Codex z subskrypcji)"),
]
tiles = "".join(f'<div class="tile"><b>{html.escape(b)}</b><span>{html.escape(s)}</span></div>' for b, s in TILES)

cover = f"""
<section class="cover">
  <div class="cover-head"><img class="logo" src="{LOGO_W}" alt="LexAlpha"><div><div class="cover-brand">L E X A L P H A &nbsp;L A B</div><div class="cover-kicker">PAŹDZIERNIK 2026 &nbsp;/&nbsp; BENCHMARK 02 &nbsp;·&nbsp; PYTANIA PRAWNE</div></div></div>
  <h1>Czy odpowiedzi modeli AI są poprawnie ugruntowane w polskim prawie?</h1>
  <div class="bar"></div>
  <p class="cover-sub">Benchmark 02: dziesięć krótkich pytań prawnych, osiem modeli, bez narzędzi i z wyszukiwaniem.</p>
  <p class="cover-sub2">Każde powołanie przepisu i orzeczenia sprawdzone w źródle urzędowym na dzień stanu prawnego 1.10.2026. Te same odpowiedzi ocenione przez pięciu sędziów-modeli i przez warstwę weryfikacji powołań. Zbiór kalibracyjny: dziesięć pytań, jedna seria, reguły oceny zapisane z datą.</p>
  <div class="grupy">
    <div class="grupa"><div class="grupa-h">OpenAI</div><b>GPT-6.1 Sol</b><b>GPT-6 Astra</b><b>GPT-5.6 Terra</b><span>Codex CLI, rozumowanie medium</span></div>
    <div class="grupa"><div class="grupa-h">Anthropic</div><b>Claude Opus 5.5</b><b>Claude Sonnet 5.5</b><b>Claude Haiku 5.5</b><span>Claude Code CLI</span></div>
    <div class="grupa"><div class="grupa-h">Google</div><b>Gemini 4 Argon</b><b>Gemini 3.8 Flash</b><span>Vertex AI; sędziowie także Gemini 3.1 Pro</span></div>
  </div>
  <div class="tiles">{tiles}</div>
  <div class="cover-line">BLOK A · RZETELNOŚĆ &nbsp;/&nbsp; BLOK B · PRZYDATNOŚĆ &nbsp;/&nbsp; KLASY BŁĘDU F · T · W · S</div>
  <div class="cover-aut">{html.escape(AUTORZY)}{KOMENTARZ_AUT}</div>
  <div class="cover-foot"><span>LEXALPHA LAB &nbsp;/&nbsp; 10 PYTAŃ • 8 MODELI • 2 WARUNKI</span><span>{DATA.upper()}</span></div>
</section>"""

CSS_COMMON = open(f"{SP}/styl.css", encoding="utf-8").read()
CSS_SCREEN = "@media (max-width:640px){.grupy{grid-template-columns:1fr}.tiles{grid-template-columns:1fr 1fr}.cover{padding:26px 20px}.cover h1{font-size:22pt}.tabela{overflow-x:auto}}"
CSS_PRINT = """
@page{size:A4;margin:18mm 14mm 18mm 14mm;
 @top-left{content:"LEXALPHA LAB  /  BENCHMARK 02 · PYTANIA PRAWNE";font:bold 7pt Arial,'Liberation Sans',sans-serif;letter-spacing:.14em;color:#4a535a;vertical-align:bottom;padding-bottom:6mm}
 @top-right{content:"WERSJA 1.1 · 29.10.2026";font:bold 7pt Arial,'Liberation Sans',sans-serif;letter-spacing:.1em;color:#4a535a;vertical-align:bottom;padding-bottom:6mm}
 @bottom-left{content:"LEXALPHA LAB  /  10 PYTAŃ • 8 MODELI • 2 WARUNKI";font:bold 7pt Arial,'Liberation Sans',sans-serif;letter-spacing:.12em;color:#4a535a;vertical-align:top;padding-top:5mm}
 @bottom-right{content:counter(page,decimal-leading-zero) " / " counter(pages,decimal-leading-zero);font:bold 7pt Arial,'Liberation Sans',sans-serif;letter-spacing:.1em;color:#4a535a;vertical-align:top;padding-top:5mm}}
@page:first{margin:0;@top-left{content:none}@top-right{content:none}@bottom-left{content:none}@bottom-right{content:none}}
.page{max-width:none;padding:0}
.cover{margin:0;border-radius:0;box-sizing:border-box;height:297mm;min-height:0;max-height:297mm;overflow:hidden;padding:16mm 18mm 12mm;display:flex;flex-direction:column;page-break-after:always}
.cover>*{flex-shrink:0}.cover-head{margin-bottom:9mm}.cover h1{font-size:25pt;max-width:32ch;margin-bottom:12px}.cover-sub{font-size:12.5pt}.cover-sub2{margin-bottom:12px;font-size:9.5pt}.cover .grupy{align-items:start;margin-bottom:7mm}.cover .grupa{padding:10px 12px 8px}.cover-foot{margin-top:auto}.cover .tiles{margin-bottom:6mm}.cover-line{margin-bottom:12px}.cover-aut{margin-bottom:10px}
.runhead{display:none}
.rozdzial{page-break-before:always}
.rozdzial.ciag{page-break-before:auto}
.rozdzial:not(.abstrakt):not(.aneks) .kol{column-count:2;column-gap:7mm}
.kol .tabela,.kol .card,.kol table{column-span:all}
.kol ul,.kol ol{padding-left:16px}
.kol li{page-break-inside:avoid}
.tabela table{page-break-inside:auto}.tabela tr{page-break-inside:avoid}
.card.tabela{page-break-inside:auto}
h2,h3,.eyebrow,.lead{page-break-after:avoid}
.tabela p{page-break-after:avoid}
"""


def dokument(css_extra, komentarz=""):
    return f"""<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LexAlpha Lab · Benchmark 02</title><style>{CSS_COMMON}{css_extra}</style></head>
<body>{komentarz}<div class="page">{cover}{''.join(body)}</div></body></html>"""


KOM = "<!-- LexAlpha Lab · Benchmark 02 · wersja 1.1 · 29.10.2026. Liczby liczone z kart ocen, kluczy, ocen sędziów i pliku kosztu. -->"
open(f"{OUT}/lexalpha_lab_benchmark_02.html", "w", encoding="utf-8").write(dokument(CSS_SCREEN, KOM))
open(f"{SP}/lexalpha_lab_benchmark_02_print.html", "w", encoding="utf-8").write(dokument(CSS_PRINT, KOM))
print("HTML OK:", len(body), "sekcji")

if "--bez-pdf" not in sys.argv:
    from weasyprint import HTML
    HTML(filename=f"{SP}/lexalpha_lab_benchmark_02_print.html", base_url=SP).write_pdf(f"{OUT}/lexalpha_lab_benchmark_02.pdf")
    print("PDF OK:", f"{OUT}/lexalpha_lab_benchmark_02.pdf")
