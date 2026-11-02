# LawBenchmark.pl — LLM benchmark on Polish law

A project of **LexAlpha Lab** (KTZR, Gdańsk). This repository holds the data, scoring keys, reference cards, judge outputs and scripts behind the LexAlpha Lab benchmark reports, so that anyone can inspect the scoring and re-run the evaluation on their own systems. [Polish version of this file](README.pl.md).

- **Report** *Benchmark 02 · pytania prawne* (PDF, Polish): [reports/benchmark-02/lexalpha_lab_benchmark_02.pdf](reports/benchmark-02/lexalpha_lab_benchmark_02.pdf) · site: https://lawbenchmark.pl
- **Dataset** (JSONL, same content as `data/`): https://huggingface.co/datasets/LexAlphaLab/lawbenchmark-b02
- **Methodology paper** *"Hallucination" Is Not Enough* (English): doi:10.5281/zenodo.23674794 · [PDF](reports/paper-v1.2/Piotrowski_2026_correctly_grounded_v1.2.pdf)
- **Versions** (repo tag ↔ report ↔ dataset revision ↔ DOI): [CHANGELOG.md](CHANGELOG.md) · cite with [CITATION.cff](CITATION.cff)

## What was measured

**Benchmark 02 · legal questions** (report of 27 October 2026, v1.1 of 29 October): 10 short legal questions typed the way a lawyer types them into a chat window (typos kept, six questions with a built-in trap), answered by 8 models of 3 providers in two conditions — without tools (W0) and with web search (W1): 160 answers. Every cited provision and ruling was checked against the official source (ISAP, ELI, SAOS, sn.pl) as of the legal-state date 1 October 2026. Five model judges scored the same answers; a verification layer (citation check in code, support check by a model) was tested on eight of the questions.

This is a calibration set, not a ranking: 10 questions, one run per system, one reviewing lawyer. Read the report's chapter 8 before quoting numbers.

## Reproduce the numbers

```bash
python3 -I reports/benchmark-02/src/dane.py   # every number of the report → reports/benchmark-02/src/dane.json
git diff --stat reports/benchmark-02/src/dane.json   # empty = identical to the published snapshot
python3 -I tools/export_jsonl.py              # rebuilds data/*.jsonl and checks the totals against dane.py
python3 -I tools/porownaj_sedziow.py argon4v101   # one judge run vs the cards (κ, confusion matrix)
```

Needs only Python 3 with PyYAML. The report PDF: `reports/benchmark-02/src/build.py` (WeasyPrint). Running a system or a judge anew: `tools/eval_*.py` (provider CLI or Vertex AI access; no credentials are stored here). The verification layer (`tools/verification/`) needs [legal-cite-pl](https://github.com/apiotrowski-afk/legal-cite-pl).

## How the data flow

```
keys/ + answers/  ──►  cards/ (lawyer)  ─┐
                  ──►  judges/ (5 models) ├──►  tools/export_jsonl.py  ──►  data/*.jsonl  (= Hugging Face)
                  ──►  verification/      ┘
cards/ + keys/ + judges/ + costs/ + verification/runs/  ──►  dane.py  ──►  dane.json  ──►  build.py  ──►  report PDF
```

| Directory | Content |
|---|---|
| `SPEC/` | Scoring specification v1.0.4 with the register of dated decisions (scoring rules unchanged since 1.0.1, the version cited on the cards; Polish, as used) and the empty card template |
| `keys/` | Scoring keys of the 10 questions: core answer, rubric, penalties, required legal bases, sources checked |
| `answers/<P>/` | 16 answers per question (8 models × W0/W1), as returned, with tool traces where the tool records them |
| `cards/` | 160 reference cards: scores A/B, error classes F/T/W/S, label "hallucinated", every citation checked |
| `judges/` | 1 319 outputs of five model judges in 12 runs, incl. the "judge with verification report" variants — index: [judges/README.md](judges/README.md) |
| `verification/` | `reports/` 320 citation-check reports (one per answer); `runs/` 15 aggregate runs of the layer — guide: [verification/README.md](verification/README.md) |
| `costs/` | Price list of 18 October 2026, cost per answer (API-equivalent), `koszt.py` |
| `reports/` | Benchmark 02 report (PDF, Markdown sources, `dane.py`, `dane.json`) and the methodology paper v1.2 |
| `probes/` | Follow-up probe referenced in the report (P07, 24 queries) |
| `cases/skd-01/` | **Benchmark 01** (pilot, fictional case on the time limit of the free-credit sanction): case, key, metrics, 17 answers with cards scored by hand; not part of the 160 answers |
| `data/` | Machine-readable layer: six JSONL files with the dataset card — [data/README.md](data/README.md) |
| `tools/` | Scripts: running the systems and the judges, comparing judges with the cards, the verification layer, the JSONL export |

Model names: the files use working names (`chatgpt_codex` = GPT-6.1 Sol, `codex_astra6` = GPT-6 Astra, `codex_terra56` = GPT-5.6 Terra, `opus_cli`/`sonnet_cli`/`haiku_cli` = Claude Opus/Sonnet/Haiku 5.5 via Claude Code, `gemini38flash_vertex` = Gemini 3.8 Flash, `argon4_high_vertex` = Gemini 4 Argon; `w0` = no tools, `w1`/`web` = web search). The full mapping is in appendix D of the report.

Every key, card, answer, judge output, verification report and JSONL record carries the canary string from [CANARY.txt](CANARY.txt) (BIG-bench convention): **this benchmark is not training data.** The remaining 40 questions of the pool stay unpublished to limit contamination.

## How the scoring works (short)

- **Block A (objective)**: core answer, required legal bases, citations; **A6** is binary: one claim about a source of law that disagrees with the official text (classes: F — source does not exist, T — real source, content not there, W — wording from another date, S — real source with a distorted identifier: number, date, court, publisher, act name) sets A6 to 0 and labels the answer "hallucinated".
- **Block B (judgement)**: calibration, completeness, usefulness.
- **Correctly grounded** = full core + A6 = 1 + at least one checked citation.
- Cards were filled in by a model (Claude) checking every citation at the source, then reviewed by one lawyer. Rules were refined during the work; every change is dated in `SPEC/`.

Scripts are published as used, with paths adapted to this repository's layout (1.0.2); comments and logs are in Polish.

## Citation

Piotrowski A., Koman A. (2026). *LexAlpha Lab · Benchmark 02 · pytania prawne*. Version 1.1, 29 October 2026. — `reports/benchmark-02/`

Piotrowski A. (2026). *"Hallucination" Is Not Enough: Why Legal LLM Benchmarks Should Measure "Correctly Grounded"*. LexAlpha Lab, v1.2, 26 October 2026. doi:10.5281/zenodo.23674794 — `reports/paper-v1.2/`

## Licence

- **Our own material** — scoring specification, questions as formulated for the benchmark, keys, reference cards, judge prompts, verification reports, reports and all texts in this repository: [CC BY 4.0](LICENSE-CC-BY-4.0.txt). Attribution: "LexAlpha Lab, LawBenchmark.pl".
- **Code** (`tools/`, `reports/*/src/*.py`, `costs/koszt.py`): [MIT](LICENSE).
- **Model answers** (`answers/`, `cases/skd-01/answers/`, `probes/`, `data/answers.jsonl`, and quotations inside cards and judgments) are outputs of third-party systems reproduced verbatim for evaluation, criticism and research. We do not claim copyright in them and do not relicense them; use of the underlying models is governed by their providers' terms.
- **Statutes and court rulings** quoted in answers and keys are official documents and are not protected by copyright under Polish law (art. 4 pr.aut.).
- The canary string in [CANARY.txt](CANARY.txt) is a methodological request not to use these files as training data, so that future evaluations stay meaningful; CC BY 4.0 itself does not restrict that use.

Contact: Adam Piotrowski, a.piotrowski@ktzr.pl · https://lawbenchmark.pl
