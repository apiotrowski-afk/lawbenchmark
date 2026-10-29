# -*- coding: utf-8 -*-
"""Renderuje assets/og.png (1200×630, podgląd przy udostępnianiu) oraz favicon.png i apple-touch-icon.png krojami strony.
Uruchamiany po stronie Windows (Playwright): python _lb_og.py <katalog_wyjściowy>; liczby w OG wpisane ręcznie z dane.py (Benchmark 02: 51/40 halucynacji, 19/27 ugruntowanych na 80) — przy zmianie wyników przeliczyć."""
import asyncio, sys
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = sys.argv[1]
FONTS = '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Literata:opsz,wght@7..72,600&display=swap" rel="stylesheet">'
OG = """<!doctype html><html><head><meta charset="utf-8">""" + FONTS + """<style>
html,body{margin:0}body{width:1200px;height:630px;background:#ffffff;color:#141c26;font-family:'IBM Plex Sans',sans-serif;box-sizing:border-box;padding:64px 72px;display:grid;grid-template-columns:1.15fr 1fr;gap:56px;align-items:center;border-top:14px solid #1d4f8f}
h1{font-family:'Literata',Georgia,serif;font-weight:600;font-size:54px;line-height:1.1;margin:0 0 22px;letter-spacing:-.01em}
.l{font-size:22px;color:#56626f;margin:0 0 36px}.m{font-size:20px;color:#56626f}.m b{color:#1d4f8f;font-weight:600}
.p{background:#f4f6f9;border-radius:14px;padding:30px 32px;display:flex;flex-direction:column;gap:26px}
.t{font-weight:600;font-size:22px;margin-bottom:10px}.t.bad{color:#b23b2a}.t.ok{color:#0f7a6c}
.r{display:grid;grid-template-columns:150px 1fr 44px;gap:14px;align-items:center;font-size:18px;color:#56626f;margin-top:8px}
.r b{font-size:28px;color:#141c26;text-align:right;font-weight:600}.tor{height:18px;background:#e2e8ef;border-radius:5px;overflow:hidden}.tor i{display:block;height:18px;border-radius:5px}
.w0{background:#56626f}.w1{background:#1d4f8f}</style></head><body>
<div><h1>Jak modele językowe odpowiadają na pytania z polskiego prawa?</h1>
<p class="l">8 modeli · 10 pytań · 160 odpowiedzi · każde powołanie sprawdzone w źródle urzędowym</p>
<p class="m"><b>LawBenchmark.pl</b> · LexAlpha Lab (KTZR i LexAlpha)</p></div>
<div class="p"><div><div class="t bad">Odpowiedzi z halucynacją</div>
<div class="r"><span>bez narzędzi</span><span class="tor"><i class="w0" style="width:63.75%"></i></span><b>51</b></div>
<div class="r"><span>z wyszukiwaniem</span><span class="tor"><i class="w1" style="width:50%"></i></span><b>40</b></div></div>
<div><div class="t ok">Poprawnie ugruntowane</div>
<div class="r"><span>bez narzędzi</span><span class="tor"><i class="w0" style="width:23.75%"></i></span><b>19</b></div>
<div class="r"><span>z wyszukiwaniem</span><span class="tor"><i class="w1" style="width:33.75%"></i></span><b>27</b></div></div>
<div style="font-size:17px;color:#56626f">na 80 odpowiedzi w każdym warunku · Benchmark 02, październik 2026</div></div>
</body></html>"""
IKONA = """<!doctype html><html><head><meta charset="utf-8">""" + FONTS + """<style>html,body{margin:0}body{width:SZpx;height:SZpx;display:grid;place-items:center;background:#1d4f8f;border-radius:RADpx}
span{font-family:'Literata',Georgia,serif;font-weight:600;color:#fff;font-size:FSpx;letter-spacing:-.04em;line-height:1}</style></head><body><span>LB</span></body></html>"""
async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        await pg.set_content(OG); await pg.wait_for_load_state("networkidle"); await pg.wait_for_timeout(600)
        print("fonty OG:", await pg.evaluate("document.fonts.check('600 54px Literata') && document.fonts.check('600 22px \"IBM Plex Sans\"')"))
        await pg.screenshot(path=OUT + r"\og.png")
        for nazwa, sz in (("favicon.png", 64), ("apple-touch-icon.png", 180)):
            pg2 = await b.new_page(viewport={"width": sz, "height": sz})
            await pg2.set_content(IKONA.replace("SZ", str(sz)).replace("RAD", "0").replace("FS", str(int(sz * 0.5))))
            await pg2.wait_for_load_state("networkidle"); await pg2.wait_for_timeout(400)
            await pg2.screenshot(path=OUT + "\\" + nazwa)
        await b.close()
asyncio.run(m())
