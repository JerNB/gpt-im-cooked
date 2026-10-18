# Separate solution

Answer evidence: **Reasoned solution**; manually traced, unexecuted in R. Source: [course packet](course-packet.md) §L2, with format basis §E1 Q2 / §K1 Q2.

| Item | Topic | Task / format | Scope / style basis | Personal target | Evidence |
|---|---|---|---|---|---|
| next-01 | STA 199CCL EX1-DPLYR; packet T2 used only as supporting analogue | Short row-count comparison with explanation | Packet L2, E1 Q2; original synthetic item | Apply the operation distinction independently after same-item feedback | Reasoned solution |

Pipeline M has **7 rows**, because grouped mutate keeps all 2 + 1 + 4 original work sessions and adds information to each one. Pipeline S has **3 rows**, because scalar summarise returns one row for each of the three teams. Grouping alone does not remove rows.

The team counts 2, 1 and 4 are computed values; they are not separate reductions in Pipeline M's number of observations. Each pipeline starts from the original table, so the two outputs are compared independently.

Wording and key checked against L2: the summarise calculation is explicitly one scalar per group; no filtering, joins, or sequential dependence between pipelines is implied. This solution's existence is not a student attempt or evidence of improvement.
