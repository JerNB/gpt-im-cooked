# Exam-sheet comparison, v2.0.1 vs final T017 skill — 2026-11-19

**Exploratory, n = 3 sessions per arm × 4 turns, synthetic STA course, one scripted student, tutor model `gpt-6-luna` (medium), Codex CLI 0.162.1, run serially on one host with arm order alternated.**

- **Arms.** Old = v2.0.1 (`20bb271`). New = `453f74c`: `cc/T017-sheet-print-fallback`, PR #10, codex-approved, standard-library PDF writer.
- **Setup.** Fixtures, the four student messages, isolation and evidence format are those of the T016 pilot ([plan](../../FEATURE-PILOT.md)). Runner: `tests/run_sheet_compare.py`, which reuses `tests/run_feature_pilot.py` unchanged.
- **Host.** The system Python has PyMuPDF but no ReportLab. v2.0.1 therefore makes its PDFs by writing its own PyMuPDF layout program in each session. A host without PyMuPDF would not give it that path.
- **Who.** Runs and analysis by cc. No blind reviewer.

All 24 turns completed: no quota failure, no rerun, no global-skill access.

## Behaviour

| Check | Old (v2.0.1) | New (453f74c) |
|---|---|---|
| Turn 1 asks only the allowance question, then waits | 0/3: drafts a study-guide PDF immediately | 3/3 |
| Sheet PDFs made by the skill's renderer | 0/3: each session writes its own PyMuPDF program | 3/3 in every PDF turn (`engine=native`) |
| `Reference-sheet preferences` saved after the revision | 0/3: the feature does not exist in v2.0.1 | 3/3 |
| Fresh turn 4 asks the allowance question again | 0/3 | 0/3: New reads the saved allowance |
| Final sheet | 2 pages (two-sided allowance) | 1 page at 13–14 pt: spare space became larger type, no extra page |

## Time and tokens (descriptive; CLI counters, not a bill)

Mean over 3 sessions per arm. "Tokens" are processed tokens (input including cached input, plus output).

| Phase | Old | New | Change of means | Per session, Old / New |
|---|---|---|---|---|
| **Turn 4: fresh session, same request** | 106.2 s · 361,660 tok | **65.4 s · 187,671 tok** | **−38% time, −48% tokens** | 73 / 168 / 78 s vs 79 / 63 / 55 s |
| Turn 3: one revision | 127.1 s · 469,116 tok | 116.7 s · 360,027 tok | −8% time, −23% tokens | 88 / 88 / 206 s vs 46 / 71 / 233 s |
| Turns 1–2: first sheet | 353.6 s · 709,409 tok | 304.9 s · 582,631 tok | −14% time, −18% tokens | not like for like (see below) |
| Whole 4-turn session | 586.9 s · 1,540,185 tok | 487.0 s · 1,130,329 tok | −17% time, −27% tokens | 393 / 678 / 690 s vs 458 / 288 / 715 s |

How to read these numbers:

- **Turns 1–2 do different work in each arm.** Old drafts a study guide in turn 1 and makes a second, exam-sheet PDF in turn 2. New asks one question in turn 1 and makes one PDF in turn 2. The comparison holds for the work up to the first sheet that meets the stated allowance; it is not a measure of the same task done faster.
- **Turn 4 is the closest like-for-like comparison:** a new session, the same message, and each arm produces a sheet. New also benefits there from the allowance and preferences saved earlier, which is part of the feature being compared.
- **The sessions vary widely, and the ranges overlap.** For example, one New revision took 233 s, more than two of the three Old revisions. With n = 3, these are exploratory differences in means, not established effects.
- **New does not run fewer commands.** Turn-4 commands averaged Old 17.3 vs New 22; turn 3, 7.3 vs 8.7. The savings come from smaller outputs and context: content JSON plus a renderer, instead of a hand-written layout program.

All 24 turns together: 8,011,542 processed tokens.

## Not measured

Sheet content quality (no blind scoring), learning gains, other models, hosts without PyMuPDF for the Old arm, paper printing, viewers other than PDFium.

## Evidence

- `protocol.json` (revisions, fingerprints, isolation) and `results-sheet-*.json`.
- `runs/<session>/`: prompts, sanitized events, responses, per-turn file snapshots including the PDFs.
- `analysis-raw.json`: per-turn values used above.
- Frozen skills: `skill-Old/` and `skill-New/`.
- Private home-directory prefixes, host names and Windows SIDs were replaced with placeholders. Links into temporary session folders were turned into plain text.
