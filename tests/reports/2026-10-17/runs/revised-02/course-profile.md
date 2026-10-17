# Course profile

## Exam and preferences

- Packet identity: STA-DEMO Midterm (synthetic statistics course).
- Artifact identity: STA 199CCL / Exam 1 (export); page header STA 199 / Exam 1. Relationship to packet unresolved; preserve separate provenance.
- Exam date, duration, scoring rubric and reference-sheet rules: Unknown.
- Language: English default; no explicit student preference supplied.
- Requested activity: Review attempt against page and packet; save feedback and record; one short question with separate solution.
- Packet format: Short answers explaining a denominator or row count (O1).

## Sources

| Source ID | Title | Path | Read status | Locator/version | Role |
|---|---|---|---|---|---|
| CP | STA-DEMO Midterm supplied course packet | [course-packet.md](course-packet.md) | Read in full | O1, L1-L3, E1, K1, P0 | Current packet scope, teaching rules, practice/key, older excerpt |
| PAGE | Grouped mutate vs summarize | [concept.html](concept.html) | Read text and JavaScript; not browser-executed | Transfer, line 9; check/retry/export, line 13; artifact version 1.0.0 | Exact task and feedback/exposure path |
| EXPORT | Student response export | [attempt.json](attempt.json) | Read in full; unchanged | schema 1.0; package 1.0.0; artifact version 1.0.0 | Original responses and claimed assistance flags |
| EXT | STA 199 slides and Lab 2 links embedded in page/export | See original files | Unread, not verified | Claimed mutate/summarize source sections | Historical artifact provenance only; not used as teaching authority |

## Course scope

| Topic ID | Topic | Status | Source locator | Assumptions |
|---|---|---|---|---|
| T1 | Grouped proportions | In scope | CP O1/L1 | Denominator names the population |
| T2 | Grouped mutate/summarise row counts | In scope | CP O1/L2; E1/K1 Q2 | Summarise has one scalar per group; content matches PAGE/EXPORT EX1-DPLYR, without resolving course identity |
| T3 | Conditional-proportion language | In scope | CP O1/L3 | Among A: denominator A, numerator both A and B |
| T4 | Skewness | Unconfirmed for supported teaching | CP O1 | Named in outline, teaching notes missing; do not teach/test here |
| EXCLUDED | Joins, hypothesis tests, normal approximations | Excluded | CP O1; older P0 | P0 left_join does not override current exclusions |

## Historical question patterns

CP E1 Q1-Q3 support short calculations with denominator/row-count explanations. Only one current practice set is supplied. P0 is an older join question, excluded currently; it does not establish current exam frequency or style for this drill.

## Conflicts and changes

- Course labels differ between CP and PAGE/EXPORT. Need identity clarification before cross-course performance merging; current review is restricted to the exact matching artifact item and supplied L2 content.
- PAGE/EXPORT operation names tax_rate; its data names rate. Intended conceptual task is clear; literal R execution is not verified. No student coding error inferred.
- PAGE always exports false help/reveal flags and independent_transfer, despite check revealing the answer before a possible retry. Corrected interpretation is in feedback/record.
- CP E1/K1 Q4 has unspecified population; key 2/20 is not a definitive rejection of a justified Class A 2/8 answer. No student attempt on it supplied.
- Embedded external sources remain unread.

## Learning files

- [Learning record](learning-record.md)
- [Review feedback](feedback.md)
- [Next question](next-question.md) and [separate solution](next-solution.md)
- Original materials: [attempt.json](attempt.json), [concept.html](concept.html), [course-packet.md](course-packet.md)
