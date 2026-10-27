# Zestawienie W0/W1 — 10 pytań × 8 modeli (2026-10-19, aktualizacja 2026-10-23: Opus W1 P10 bez B9)

Źródło: `tools/zestawienie_tier.py --tylko P01,P04,P05,P06,P07,P08,P09,P10,P12,P13` (karty po decyzjach Adama do 2026-10-19) i `benchmark/koszt.py` (cennik 2026-10-18; koszt równoważny API, „≥” = dolna granica w części W1). Poprawnie ugruntowana = A6 = 1 i A-R = 2. Specyfikacja v1.0.1.

| Model | A % W0 → W1 | B % W0 → W1 | hallucinated W0 → W1 (z 10) | poprawnie ugruntowane W0 → W1 | USD / poprawnie ugruntowaną W0 → W1 |
|---|---|---|---|---|---|
| GPT-6.1 Sol | 72.8 → 84.0 | 86.7 → 96.7 | 1 → 1 | 6 → 7 | 0.042 → ≥0.221 |
| GPT-6 Astra | 75.2 → 82.5 | 83.3 → 93.3 | 1 → 0 | 6 → 7 | 0.236 → 0.545 |
| GPT-5.6 Terra | 41.7 → 72.7 | 66.7 → 86.7 | 6 → 4 | 3 → 4 | 0.069 → 0.330 |
| Claude Opus 5.5 | 55.0 → 86.0 | 73.3 → 96.7 | 9 → 5 | 0 → 4 | n/d → ≥0.489 |
| Claude Sonnet 5.5 | 43.5 → 67.8 | 60.0 → 90.0 | 9 → 9 | 0 → 0 | n/d → n/d |
| Claude Haiku 5.5 | 30.1 → 49.5 | 56.7 → 66.7 | 9 → 8 | 0 → 0 | n/d → n/d |
| Gemini 3.8 Flash | 49.6 → 78.1 | 70.0 → 86.7 | 8 → 5 | 2 → 4 | 0.058 → ≥0.128 |
| Gemini 4 Argon | 61.0 → 75.3 | 80.0 → 86.7 | 8 → 8 | 2 → 1 | 0.186 → ≥2.085 |

## Tabela generatora (pełna)

Kolumna „sprawdzone powołania” (dodana 2026-10-23): ile powołań z kart faktycznie sprawdzono w źródle urzędowym (suma po 10 kartach); statusy „nieobsługiwany / nie znaleziono / do sprawdzenia ręcznie” są w kartach osobno i nie wchodzą do błędów modelu.

| System | kart | śr. A % | śr. B % | hallucinated | sprawdzone powołania | z pamięci | odczyt źródła | źródło wtórne | nieustalone | bez weryfikacji źródła |
|---|---|---|---|---|---|---|---|---|---|---|
| chatgpt_codex_web_r2 | 8 | **93.2** | 100.0 | 0 z 8 | 32 z 34 | 0 | 0 | 0 | 0 | 0 z 8 |
| chatgpt_codex_web | 8 | **92.6** | 100.0 | 0 z 8 | 34 z 35 | 0 | 0 | 0 | 0 | 0 z 8 |
| chatgpt_codex_high_web | 8 | **92.0** | 100.0 | 0 z 8 | 37 z 37 | 0 | 0 | 0 | 0 | 0 z 8 |
| chatgpt_app_tmp_r3 | 5 | **88.8** | 93.3 | 0 z 5 | 22 z 22 | 0 | 0 | 0 | 0 | 2 z 5 |
| chatgpt_app_r3 | 5 | **86.1** | 93.3 | 1 z 5 | 26 z 26 | 0 | 1 | 0 | 0 | 1 z 5 |
| opus_cli_w1_r3 | 10 | **86.0** | 96.7 | 5 z 10 | 147 z 147 | 4 | 0 | 0 | 1 | 6 z 10 |
| chatgpt_codex_web_r3 | 10 | **84.0** | 96.7 | 1 z 10 | 72 z 73 | 0 | 1 | 0 | 0 | 0 z 10 |
| codex_astra6_web_r3 | 10 | **82.5** | 93.3 | 0 z 10 | 63 z 63 | 0 | 0 | 0 | 0 | 0 z 10 |
| gemini38flash_vertex_w1_r3 | 10 | **78.1** | 86.7 | 5 z 10 | 97 z 97 | 1 | 1 | 1 | 2 | 7 z 10 |
| argon4_high_vertex_w1_r3 | 10 | **75.3** | 86.7 | 8 z 10 | 189 z 189 | 4 | 3 | 0 | 1 | 3 z 10 |
| codex_astra6_w0_r3 | 10 | **75.2** | 83.3 | 1 z 10 | 59 z 59 | 1 | 0 | 0 | 0 | 10 z 10 |
| chatgpt_codex_w0 | 8 | **73.0** | 75.0 | 1 z 8 | 23 z 23 | 1 | 0 | 0 | 0 | 8 z 8 |
| chatgpt_codex_w0_r3 | 10 | **72.8** | 86.7 | 1 z 10 | 51 z 51 | 1 | 0 | 0 | 0 | 10 z 10 |
| codex_terra56_web_r3 | 10 | **72.7** | 86.7 | 4 z 10 | 70 z 70 | 3 | 1 | 0 | 0 | 1 z 10 |
| chatgpt_codex_w0_r2 | 8 | **71.1** | 79.2 | 2 z 8 | 24 z 24 | 2 | 0 | 0 | 0 | 8 z 8 |
| sonnet_cli_w1_r3 | 10 | **67.8** | 90.0 | 9 z 10 | 104 z 111 | 6 | 0 | 0 | 3 | 6 z 10 |
| argon4_high_vertex_w0_r3 | 10 | **61.0** | 80.0 | 8 z 10 | 115 z 121 | 8 | 0 | 0 | 0 | 10 z 10 |
| fable_cli_w0_r3 | 5 | **58.5** | 66.7 | 5 z 5 | 64 z 64 | 5 | 0 | 0 | 0 | 5 z 5 |
| opus_cli_w0_r3 | 10 | **55.0** | 73.3 | 9 z 10 | 123 z 123 | 9 | 0 | 0 | 0 | 10 z 10 |
| gemini31_vertex_w0_r3 | 5 | **52.5** | 73.3 | 5 z 5 | 32 z 32 | 5 | 0 | 0 | 0 | 5 z 5 |
| gemini38flash_vertex_w0_r3 | 10 | **49.6** | 70.0 | 8 z 10 | 75 z 77 | 8 | 0 | 0 | 0 | 10 z 10 |
| haiku_cli_w1_r3 | 10 | **49.5** | 66.7 | 8 z 10 | 75 z 77 | 3 | 1 | 3 | 1 | 7 z 10 |
| bielik_11b_v3_q8_chmura | 8 | **44.0** | 50.0 | 5 z 8 | 9 z 9 | 5 | 0 | 0 | 0 | 8 z 8 |
| sonnet_cli_w0_r3 | 10 | **43.5** | 60.0 | 9 z 10 | 93 z 93 | 9 | 0 | 0 | 0 | 10 z 10 |
| codex_terra56_w0_r3 | 10 | **41.7** | 66.7 | 6 z 10 | 41 z 41 | 6 | 0 | 0 | 0 | 10 z 10 |
| gemini_vertex_w0_r3 | 5 | **41.4** | 73.3 | 5 z 5 | 27 z 27 | 5 | 0 | 0 | 0 | 5 z 5 |
| gemini3flash_vertex_w0_r3 | 5 | **41.2** | 60.0 | 5 z 5 | 20 z 20 | 5 | 0 | 0 | 0 | 5 z 5 |
| argon4_vertex_w0_r3 | 5 | **38.9** | 46.7 | 5 z 5 | 50 z 51 | 5 | 0 | 0 | 0 | 5 z 5 |
| haiku_cli_w0_r3 | 10 | **30.1** | 56.7 | 9 z 10 | 62 z 62 | 9 | 0 | 0 | 0 | 10 z 10 |
| bielik_11b_v3_web | 8 | **28.0** | 41.7 | 6 z 8 | 8 z 8 | 6 | 0 | 0 | 0 | 8 z 8 |
| qwen38_27b_chmura | 8 | **24.6** | 50.0 | 8 z 8 | 20 z 20 | 8 | 0 | 0 | 0 | 8 z 8 |
| bielik_11b_v3_lokalnie | 8 | **22.6** | 37.5 | 7 z 8 | 6 z 6 | 7 | 0 | 0 | 0 | 8 z 8 |
| qwen35_9b_lokalnie | 8 | **14.2** | 25.0 | 8 z 8 | 15 z 15 | 8 | 0 | 0 | 0 | 8 z 8 |
| qwen35_9b_web | 8 | **14.2** | 29.1 | 8 z 8 | 15 z 15 | 5 | 0 | 3 | 0 | 8 z 8 |
| bielik_11b_v3_web_wymus | 8 | **10.6** | 20.8 | 6 z 8 | 12 z 13 | 6 | 0 | 0 | 0 | 7 z 8 |
