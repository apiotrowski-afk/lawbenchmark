# LawBenchmark.pl — LLM benchmark on Polish law

A project of **LexAlpha Lab** (KTZR, Gdańsk). This repository holds the data, scoring keys, reference cards, judge outputs and scripts behind the LexAlpha Lab benchmark reports, so that anyone can inspect the scoring and re-run the evaluation on their own systems.

[Polish version of this file](README.pl.md)

## What is here

**Benchmark 02 · legal questions** (report of 27 October 2026): 10 short legal questions typed the way a lawyer types them into a chat window (typos kept, six questions with a built-in trap), answered by 8 models of 3 providers in two conditions — without tools (W0) and with web search (W1): 160 answers. Every cited provision and ruling was checked against the official source (ISAP, ELI, SAOS, sn.pl) as of the legal-state date 1 October 2026.

| Directory | Content |
|---|---|
| `SPEC/` | Scoring specification v1.0.1 with the register of dated decisions (Polish, verbatim internal document) |
| `keys/` | Scoring keys of the 10 questions: core answer, rubric, penalties, required legal bases, sources checked |
| `answers/<P>/` | 16 answers per question (8 models × W0/W1), as returned by the system, with tool traces where the tool records them |
| `cards/` | 160 reference cards: scores A/B, error classes F/T/W/S, label "hallucinated", every citation checked, version date |
| `judges/` | Outputs of five model judges (Gemini 4 Argon, GPT-6.1 Sol, Gemini 3.1 Pro, Gemini 3.8 Flash, GPT-6 Astra) and of the "judge with verification report" variants (`*meta*`) |
| `verification/` | Verification layer reports: citation check (code) and support check (model), per card and aggregate runs |
| `costs/` | Price list of 18 October 2026 and cost per answer (API-equivalent) |
| `reports/` | Benchmark 02 report (PDF, HTML, Markdown sources, `dane.py` that computes every number from the cards) and the methodology paper v1.2 |
| `probes/` | Follow-up probes referenced in the report (P07, 24 queries) |
| `tools/` | Scripts: running the systems, running the judges, comparing judges with the cards, the verification layer |
| `data/` | Machine-readable layer: `questions`, `keys`, `answers`, `cards`, `judgments`, `verification` as JSONL (English field names, Polish content), with a dataset card — see [data/README.md](data/README.md) |

Model names: the files use working names (`chatgpt_codex` = GPT-6.1 Sol, `codex_astra6` = GPT-6 Astra, `codex_terra56` = GPT-5.6 Terra, `opus_cli`/`sonnet_cli`/`haiku_cli` = Claude Opus/Sonnet/Haiku 5.5 via Claude Code, `gemini38flash_vertex` = Gemini 3.8 Flash, `argon4_high_vertex` = Gemini 4 Argon; `w0` = no tools, `w1`/`web` = web search). The full mapping is in appendix D of the report.

Every data file and every JSONL record carries the canary string from [CANARY.txt](CANARY.txt) (BIG-bench convention): **this benchmark is not training data.** The remaining 40 questions of the pool stay unpublished to limit contamination.

## How the scoring works (short)

- **Block A (objective)**: core answer, required legal bases, citations; **A6** is binary: one claim about a source of law that disagrees with the official text (classes: F — source does not exist, T — real source, content not there, W — wording from another date, S — case number with a thesis from another case) sets A6 to 0 and labels the answer "hallucinated".
- **Block B (judgement)**: calibration, completeness, usefulness.
- **Correctly grounded** = full core + A6 = 1 + at least one checked citation.
- Cards were filled in by a model (Claude) checking every citation at the source, then reviewed by one lawyer. Rules were refined during the work; every change is dated in `SPEC/`.

This is a calibration set, not a ranking: 10 questions, one run per system, one reviewing lawyer. Read the report's chapter 8 before quoting numbers.

## Re-running

- Tables of the report: `python3 -I reports/benchmark-02/src/dane.py` (reads `cards/`, `keys/`, `judges/`, `costs/`).
- JSONL layer: `python3 -I tools/export_jsonl.py` (rebuilds `data/` from the Markdown/YAML/JSON sources and checks the totals against `dane.py`).
- Judges vs cards: `python3 -I tools/porownaj_sedziow.py`.
- Running a system on the questions: `tools/eval_*.py` (need the provider's CLI or Vertex AI access; no credentials are stored here).
- Verification layer (`tools/verification/`) needs [legal-cite-pl](https://github.com/apiotrowski-afk/legal-cite-pl) for ISAP/ELI lookups.

Scripts are published as used; paths were made relative, nothing else was changed. Comments and logs are in Polish.

## Citation

Piotrowski A., Koman A. (2026). *LexAlpha Lab · Benchmark 02 · pytania prawne*. Version 1.0, 27 October 2026. — `reports/benchmark-02/`

Piotrowski A. (2026). *"Hallucination" Is Not Enough: Why Legal LLM Benchmarks Should Measure "Correctly Grounded"*. LexAlpha Lab, v1.2, 26 October 2026. doi:10.5281/zenodo.23674794 — `reports/paper-v1.2/`

## Licence

Data, keys, cards, reports and texts: [CC BY 4.0](LICENSE-CC-BY-4.0.txt). Code in `tools/` and `reports/*/src/*.py`: [MIT](LICENSE). Model answers are reproduced for evaluation purposes; statutes and court rulings quoted in them are public documents under Polish copyright law (art. 4 pr.aut.).

Contact: Adam Piotrowski, a.piotrowski@ktzr.pl · https://lawbenchmark.pl
