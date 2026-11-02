# judges/ — index of model-judge runs

One file per (answer, run): `judges/<question>_<system>_r3.<run>.json`. 1 319 files, 12 runs, 5 judge models. Judges scored blind (system name removed), under scoring specification 1.0.1 unless stated. Settings per judge: report *Benchmark 02*, appendix C, table C.2; agreement with the lawyer's cards: chapter 6 and appendix E. Same content in machine-readable form: `data/judgments.jsonl` (`judge_id`, `judge_variant`).

## Main runs (judge without verification report, "v101")

| Run id | Judge model | Questions | Files | Coverage | Used in |
|---|---|---|---|---|---|
| `argon4v101` | Gemini 4 Argon | all 10 | 147 / 160 | 13 answers missing (runs that returned no valid card) | ch. 6, appendix C–E, `dane.py` |
| `sol61v101` | GPT-6.1 Sol | all 10 | 160 / 160 | complete | ch. 6, appendix C–E, `dane.py` |
| `gemini31v101` | Gemini 3.1 Pro | all 10 | 159 / 160 | 1 answer missing | ch. 6, appendix C–E, `dane.py` |
| `gemini38flashv101` | Gemini 3.8 Flash | all 10 | 160 / 160 | complete | ch. 6, appendix C–E, `dane.py` |
| `astra6v101` | GPT-6 Astra | all 10 | 49 / 160 | partial (subscription usage limits; run stopped) | ch. 6 (reported with its n), `dane.py` |

## "Card meta" runs (judge given the verification-layer report)

Only on the eight test questions of the verification layer (P01, P04, P05, P06, P07, P08, P12, P13 = 128 answers); the first variant on four of them. Three instruction variants, described in report chapter 7.5:

| Run id | Judge model | Variant | Questions | Files | Used in |
|---|---|---|---|---|---|
| `argon4meta` | Gemini 4 Argon | v1 — report **binding** (judge's A6 classes follow the report) | P05, P06, P07, P13 | 64 | ch. 7.5, `dane.py` (META) |
| `argon4meta2` | Gemini 4 Argon | v2 — report **auxiliary** (judge decides) | 8 test questions | 125 | ch. 7.5–7.6, `dane.py` |
| `argon4meta3` | Gemini 4 Argon | v3 — ✓ only when the report confirms the wording | 8 test questions | 127 | ch. 7.5–7.6, `dane.py` |
| `sol61meta` | GPT-6.1 Sol | v1 | P05, P06, P07, P13 | 61 | ch. 7.5, `dane.py` |
| `sol61meta2` | GPT-6.1 Sol | v2 | 8 test questions | 119 | ch. 7.5–7.6, `dane.py` |
| `sol61meta3` | GPT-6.1 Sol | v3 | 8 test questions | 128 | ch. 7.5–7.6, `dane.py` |

Missing files within a variant are answers for which the run returned no valid card (timeouts, usage limits); nothing was removed by hand. The comparison "with report vs without" in `dane.py` uses only answers present in both runs.

## Historical run

| Run id | Judge model | Questions | Files | Note |
|---|---|---|---|---|
| `astra6` | GPT-6 Astra | P05, P06, P07, P12, P13 | 20 | 11 October 2026, under specification 1.0 (before 1.0.1). Kept as a record; marked `historical` in `data/judgments.jsonl`, not part of the main tables |

## How to re-run the comparison

`python3 -I tools/porownaj_sedziow.py <run id>` — agreement of the run with `cards/` (κ, confusion matrix, misses by provider of the evaluated model). Judge scripts: `tools/eval_sedzia_gemini.py` (Vertex AI), `tools/eval_sedzia_codex.py` (Codex CLI).
