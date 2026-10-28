# -*- coding: utf-8 -*-
"""Wdrożenie katalogu site/ na Firebase Hosting przez REST API (bez firebase-tools), tokenem z `gcloud auth print-access-token`.

Kroki API: versions.create → versions.populateFiles → upload brakujących plików (gzip, SHA-256) → versions.patch FINALIZED
→ releases.create. Użycie (z katalogu repo): python3 -I tools/deploy_hosting.py [--projekt lawbenchmark-pl] [--site lawbenchmark-pl]
Wymaga ważnego tokenu CLI (hook sprawdza przed startem). Nic nie usuwa; poprzednie wersje zostają w historii hostingu.
"""
import gzip
import hashlib
import json
import os
import subprocess
import sys
import urllib.request

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SITE_DIR = os.path.join(REPO, "site")
PROJEKT = sys.argv[sys.argv.index("--projekt") + 1] if "--projekt" in sys.argv else "lawbenchmark-pl"
SITE = sys.argv[sys.argv.index("--site") + 1] if "--site" in sys.argv else "lawbenchmark-pl"
API = "https://firebasehosting.googleapis.com/v1beta1"

tok = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, check=True).stdout.strip()
H = {"Authorization": f"Bearer {tok}", "x-goog-user-project": PROJEKT, "Content-Type": "application/json"}


def api(metoda, sciezka, dane=None):
    body = json.dumps(dane).encode() if dane is not None else None
    r = urllib.request.Request(API + sciezka, data=body, headers=H, method=metoda)
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        print("BŁĄD", e.code, e.read().decode()[:600]); raise


konfig = json.load(open(os.path.join(REPO, "firebase.json"), encoding="utf-8"))["hosting"]
wersja = api("POST", f"/sites/{SITE}/versions", {"config": {
    "cleanUrls": konfig.get("cleanUrls", False), "trailingSlashBehavior": "REMOVE" if konfig.get("trailingSlash") is False else "ADD",
    "headers": [{"glob": h["source"], "headers": {x["key"]: x["value"] for x in h["headers"]}} for h in konfig.get("headers", [])]}})
wid = wersja["name"]
print("wersja:", wid.split("/")[-1])

pliki, gz = {}, {}
for root, _, fs in os.walk(SITE_DIR):
    for f in fs:
        p = os.path.join(root, f); rel = "/" + os.path.relpath(p, SITE_DIR).replace(os.sep, "/")
        dane_gz = gzip.compress(open(p, "rb").read(), mtime=0)
        h = hashlib.sha256(dane_gz).hexdigest(); pliki[rel] = h; gz[h] = dane_gz
odp = api("POST", f"/{wid}:populateFiles", {"files": pliki})
do_wyslania = odp.get("uploadRequiredHashes", []); url = odp["uploadUrl"]
print(f"plików: {len(pliki)}, do wysłania: {len(do_wyslania)}")
for h in do_wyslania:
    r = urllib.request.Request(f"{url}/{h}", data=gz[h], headers={"Authorization": f"Bearer {tok}", "x-goog-user-project": PROJEKT,
                                                                   "Content-Type": "application/octet-stream"}, method="POST")
    urllib.request.urlopen(r).read()
api("PATCH", f"/{wid}?updateMask=status", {"status": "FINALIZED"})
rel = api("POST", f"/sites/{SITE}/releases?versionName={wid}", {"message": "deploy_hosting.py"})
print("wydanie:", rel["name"].split("/")[-1], "→ https://" + SITE + ".web.app")
