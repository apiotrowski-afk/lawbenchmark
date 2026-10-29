# -*- coding: utf-8 -*-
"""Zgłoszenie adresów do IndexNow (Bing, Yandex, Seznam i inni) dla lawbenchmark.pl.

Klucz: plik `site/<klucz>.txt` (treść = klucz), musi być wdrożony na hostingu przed zgłoszeniem.
Użycie (z katalogu repo): python3 -I tools/indexnow.py [url ...]   — bez argumentów bierze adresy z site/sitemap.xml.
Loguje tylko kody odpowiedzi i liczbę adresów.
"""
import glob
import json
import os
import re
import sys
import urllib.request

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
HOST = "lawbenchmark.pl"
klucze = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(REPO, "site", "*.txt"))
          if re.fullmatch(r"[a-f0-9]{32}\.txt", os.path.basename(p))]
if len(klucze) != 1:
    sys.exit(f"Oczekiwano jednego pliku klucza w site/, jest {len(klucze)}")
klucz = klucze[0]

adresy = sys.argv[1:] or re.findall(r"<loc>(.*?)</loc>", open(os.path.join(REPO, "site", "sitemap.xml"), encoding="utf-8").read())
# kontrola: plik klucza widoczny publicznie
try:
    widoczny = urllib.request.urlopen(f"https://{HOST}/{klucz}.txt", timeout=20).read().decode().strip() == klucz
except Exception as e:
    widoczny = False
if not widoczny:
    sys.exit("Plik klucza nie jest dostępny na hostingu — najpierw wdrożenie (tools/deploy_hosting.py).")

dane = json.dumps({"host": HOST, "key": klucz, "keyLocation": f"https://{HOST}/{klucz}.txt", "urlList": adresy}).encode()
r = urllib.request.Request("https://api.indexnow.org/IndexNow", data=dane, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
try:
    with urllib.request.urlopen(r, timeout=30) as o:
        print("IndexNow:", o.status, "adresów:", len(adresy))
except urllib.error.HTTPError as e:
    print("IndexNow BŁĄD:", e.code, e.read().decode()[:200])
