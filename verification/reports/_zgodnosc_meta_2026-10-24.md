# Zgodność z kartami Adama: sędzia bez raportu faktów vs sędzia z raportem (karta meta)

## argon4v101 (bez raportu) vs argon4meta (z raportem) — wspólnych kart: 54 (bez raportu ogółem 76, z raportem ogółem 64)

| argon4v101 — bez raportu | zgodność | κ | n |
|---|---|---|---|
| hallucinated | 98 % | 0.96 | 54 |
| A6 | 96 % | 0.92 | 54 |
| A-R | 98 % | 0.97 | 54 |
| A2 | 94 % | 0.89 | 54 |
| A3 | 96 % | 0.78 | 54 |
| A8 | 78 % | 0.50 | 54 |
| B1 | 85 % | 0.78 | 54 |
| B2 | 94 % | 0.84 | 54 |

hallucinated: obaj tak 34 · obaj nie 19 · tylko karta 1 (brak u sędziego) · tylko sędzia 0 (nadmiar)

| argon4meta — z raportem | zgodność | κ | n |
|---|---|---|---|
| hallucinated | 93 % | 0.85 | 54 |
| A6 | 91 % | 0.81 | 54 |
| A-R | 98 % | 0.97 | 54 |
| A2 | 94 % | 0.89 | 54 |
| A3 | 96 % | 0.78 | 54 |
| A8 | 87 % | 0.70 | 54 |
| B1 | 81 % | 0.71 | 54 |
| B2 | 98 % | 0.94 | 54 |

hallucinated: obaj tak 31 · obaj nie 19 · tylko karta 4 (brak u sędziego) · tylko sędzia 0 (nadmiar)

Karty, na których raport zmienił etykietę hallucinated: 3 z 54

| P | system | karta Adama | bez raportu | z raportem | A6_typ z raportem |
|---|---|---|---|---|---|
| P05 | codex_terra56_w0_r3 | tak | tak | nie | [] |
| P05 | sonnet_cli_w1_r3 | tak | tak | nie | [] |
| P07 | gemini38flash_vertex_w1_r3 | tak | tak | nie | [] |

| P | n | bez raportu: zgodne hallucinated | z raportem: zgodne hallucinated | bez: zgodne A6 | z: zgodne A6 |
|---|---|---|---|---|---|
| P05 | 15 | 15 | 13 | 15 | 13 |
| P06 | 12 | 12 | 12 | 12 | 12 |
| P07 | 13 | 13 | 12 | 12 | 11 |
| P13 | 14 | 13 | 13 | 13 | 13 |

Karty meta (argon4meta) z etykietą hallucinated inną niż karta Adama (do decyzji człowieka): 4 — P05/codex_terra56_w0_r3, P05/sonnet_cli_w1_r3, P07/gemini38flash_vertex_w1_r3, P13/codex_terra56_w0_r3

## sol61v101 (bez raportu) vs sol61meta (z raportem) — wspólnych kart: 61 (bez raportu ogółem 92, z raportem ogółem 61)

| sol61v101 — bez raportu | zgodność | κ | n |
|---|---|---|---|
| hallucinated | 95 % | 0.88 | 61 |
| A6 | 93 % | 0.84 | 61 |
| A-R | 97 % | 0.95 | 61 |
| A2 | 98 % | 0.97 | 61 |
| A3 | 93 % | 0.70 | 61 |
| A8 | 66 % | 0.42 | 61 |
| B1 | 82 % | 0.72 | 61 |
| B2 | 95 % | 0.86 | 61 |

hallucinated: obaj tak 41 · obaj nie 17 · tylko karta 0 (brak u sędziego) · tylko sędzia 3 (nadmiar)

| sol61meta — z raportem | zgodność | κ | n |
|---|---|---|---|
| hallucinated | 92 % | 0.83 | 61 |
| A6 | 90 % | 0.79 | 61 |
| A-R | 95 % | 0.92 | 61 |
| A2 | 97 % | 0.93 | 61 |
| A3 | 95 % | 0.76 | 61 |
| A8 | 67 % | 0.42 | 61 |
| B1 | 80 % | 0.70 | 61 |
| B2 | 98 % | 0.95 | 61 |

hallucinated: obaj tak 36 · obaj nie 20 · tylko karta 5 (brak u sędziego) · tylko sędzia 0 (nadmiar)

Karty, na których raport zmienił etykietę hallucinated: 8 z 61

| P | system | karta Adama | bez raportu | z raportem | A6_typ z raportem |
|---|---|---|---|---|---|
| P05 | codex_terra56_w0_r3 | tak | tak | nie | [] |
| P05 | sonnet_cli_w1_r3 | tak | tak | nie | [] |
| P06 | gemini38flash_vertex_w1_r3 | nie | tak | nie | [] |
| P07 | gemini38flash_vertex_w1_r3 | tak | tak | nie | [] |
| P07 | opus_cli_w1_r3 | nie | tak | nie | [] |
| P07 | sonnet_cli_w1_r3 | tak | tak | nie | [] |
| P13 | codex_terra56_w0_r3 | tak | tak | nie | [] |
| P13 | gemini38flash_vertex_w0_r3 | nie | tak | nie | [] |

| P | n | bez raportu: zgodne hallucinated | z raportem: zgodne hallucinated | bez: zgodne A6 | z: zgodne A6 |
|---|---|---|---|---|---|
| P05 | 16 | 16 | 14 | 16 | 14 |
| P06 | 16 | 15 | 16 | 15 | 16 |
| P07 | 16 | 15 | 14 | 14 | 13 |
| P13 | 13 | 12 | 12 | 12 | 12 |

Karty meta (sol61meta) z etykietą hallucinated inną niż karta Adama (do decyzji człowieka): 5 — P05/codex_terra56_w0_r3, P05/sonnet_cli_w1_r3, P07/gemini38flash_vertex_w1_r3, P07/sonnet_cli_w1_r3, P13/codex_terra56_w0_r3

