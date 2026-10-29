# -*- coding: utf-8 -*-
"""Publikacja katalogu data/ jako zbioru danych na Hugging Face (karta = data/README.md).

Trzy kroki, każdy osobnym wywołaniem (z katalogu repo):
  python -I tools/publish_hf.py --repo ORG/NAZWA                # plan: co zostanie wysłane, nic nie wysyła
  python -I tools/publish_hf.py --repo ORG/NAZWA --wykonaj      # repo PRYWATNE + wysłanie plików (do przeglądu)
  python -I tools/publish_hf.py --repo ORG/NAZWA --publiczne    # publiczne + bramka z automatyczną akceptacją
Token: z wcześniejszego `hf auth login` albo `huggingface-cli login` (skrypt go nie czyta, nie zapisuje i nie wypisuje).
Wymaga: huggingface_hub (np. ~/.venvs/hf/bin/python). W karcie znacznik <repo_id> jest podmieniany na --repo w kopii roboczej.
"""
import argparse
import os
import shutil
import sys
import tempfile

from huggingface_hub import HfApi

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DATA = os.path.join(REPO, "data")
PLIKI = ["README.md", "questions.jsonl", "keys.jsonl", "answers.jsonl", "cards.jsonl", "judgments.jsonl", "verification.jsonl"]

ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True, help="identyfikator zbioru, np. LexAlphaLab/lawbenchmark-b02")
ap.add_argument("--wykonaj", action="store_true", help="utwórz repo prywatne i wyślij pliki")
ap.add_argument("--publiczne", action="store_true", help="zmień widoczność na publiczną i włącz bramkę (auto)")
a = ap.parse_args()

brak = [p for p in PLIKI if not os.path.exists(os.path.join(DATA, p))]
if brak:
    sys.exit(f"Brak plików w data/: {brak} (najpierw tools/export_jsonl.py)")
rozmiar = sum(os.path.getsize(os.path.join(DATA, p)) for p in PLIKI)
print(f"zbiór: {a.repo} · plików: {len(PLIKI)} · razem {rozmiar / 1e6:.1f} MB")

api = HfApi()
if a.publiczne:
    api.update_repo_settings(a.repo, repo_type="dataset", private=False, gated="auto")
    print(f"publiczne, bramka: automatyczna akceptacja → https://huggingface.co/datasets/{a.repo}")
    sys.exit(0)
if not a.wykonaj:
    for p in PLIKI:
        print(f"  {p:22s} {os.path.getsize(os.path.join(DATA, p)) / 1e3:9.1f} kB")
    print("plan: bez --wykonaj nic nie wysłano")
    sys.exit(0)

api.create_repo(a.repo, repo_type="dataset", private=True, exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    for p in PLIKI:
        shutil.copy2(os.path.join(DATA, p), os.path.join(tmp, p))
    karta = os.path.join(tmp, "README.md")
    t = open(karta, encoding="utf-8").read().replace("<repo_id>", a.repo)
    open(karta, "w", encoding="utf-8").write(t)
    info = api.upload_folder(folder_path=tmp, repo_id=a.repo, repo_type="dataset",
                             commit_message="LawBenchmark.pl Benchmark 02, data version 1.0.1 (29 October 2026)")
print(f"wysłano (repo PRYWATNE): {info.commit_url if hasattr(info, 'commit_url') else info}")
print(f"przejrzyj: https://huggingface.co/datasets/{a.repo} · potem: --publiczne")
