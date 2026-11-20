# Fresh-model feature pilot — 2026-11-18 (T016)

**Exploratory pilot, n = 2 sessions per cell, synthetic courses, one scripted student, tutor model `gpt-6-luna` (medium), Codex CLI 0.162.1.** Plan: [tests/FEATURE-PILOT.md](../../FEATURE-PILOT.md). Skill under test: `main` at `74dceec` (arm New); sheet comparison arm v2.0.1 `20bb271` (arm Old). Harness: `tests/run_feature_pilot.py` at `dc19cf3`. Runs and scoring: cc (the maintainer asked cc to command execution); fixtures and harness first written by codex. No blind second reviewer yet.

All 22 planned turns completed: no quota failure, no rerun, no global-skill access. Three earlier smoke attempts are kept separately (two harness defects, one pass); none enters these results.

## Headline

- **Calendar works end to end on a smaller model.** In 2 of 2 sessions the tutor derived every task from the records exactly as `references/study-plan.md` prescribes, cited a real record row for each, ran `plan_study.py`, and delivered `plan.ics` + `calendar.html` with nothing unplaced.
- **Three behaviour gaps in the calendar flow:** it did not wait for the availability answer in 1 of 2 sessions, never offered to add courses without records (0 of 2), and in 1 of 2 sessions did not add HIST 101 when asked.
- **The new sheet path produced no PDF (0 of 4 sheet sessions × turns)** because the test host's Python has no ReportLab. The tutor correctly did not install it unasked and delivered an editable source, but it also **did not ask the student** whether to install it (0 of 2), which the skill requires. v2.0.1 produced a two-page PDF in 2 of 2 sessions (with PyMuPDF, installed on this host; see the correction below). On a host like this, the new sheet path is a regression in output format.
- **Preference memory works:** after the revision, New saved a `Reference-sheet preferences` section in 2 of 2 sessions and both fresh turn-4 sessions read it.

## Calendar (arm New)

| Check | rep 1 | rep 2 |
|---|---|---|
| C1 one availability question, waits for it | **fail** — asked via the CLI question tool, received no answer in non-interactive exec, then built an all-day fallback in the same turn (turn 2 then rebuilt it with windows) | pass — asked once in the reply and stopped |
| C2 `plan_study.py` ran; `.ics` + HTML delivered | pass | pass |
| C3 every basis cites a record row | pass (12/12 tasks; mocks cite the per-course rule) | pass (12/12) |
| C4 task kinds match the table | pass — T1 recheck not before 11-20, T2/P2 variant, P1 transfer practice, T3/P3 source-gap, T4/P4 learn then practice, X1/P5 nothing | pass (same) |
| C5a unrecorded-course offer made once | **fail** (no offer) | **fail** (no offer) |
| C5b HIST 101 added as review blocks only | **fail** — asked for the exam end time instead; final plan has no HIST | pass — 8 × 60-min review blocks, basis "No learning record"; exam end invented as 09:01 |
| C6 no calendar write, no reminders, unplaced reported | pass | pass |

Both sessions ran `plan_study.py` several times (rep 1: 8 runs in turn 1; rep 2: 10 in turn 2), i.e. iterated on plan JSON errors before success; the error texts are in the turn logs.

## Exam sheet (arms Old and New)

| Check | Old rep 1 | Old rep 2 | New rep 1 | New rep 2 |
|---|---|---|---|---|
| S1a asked the allowance question before drafting | no | no | no — used the unconfirmed one-sheet default | **yes** — the exact one question |
| S1b no content-plan approval request | pass | pass | pass | pass |
| S2 first draft is a ≤2-page PDF | pass (2 pages, turn 1) | pass (2 pages, turn 1) | **fail** — ReportLab missing; JSON source delivered | **fail** — ReportLab missing; Markdown source delivered |
| S2b asked before installing ReportLab | n/a | n/a | **fail** — did not ask | **fail** — did not ask |
| S5 preference saved after revision | no section (not in v2.0.1) | no section | pass | pass |
| S5 turn-4 draft follows the saved preference | not scored | not scored | reply consistent (worked distinction kept) — not scored blind | pass — reply cites the saved preference |

S3 (content rules, blind) and S4 (revision diff) are **not scored** in this pass: New's outputs are JSON/Markdown and Old's are PDFs, so the format reveals the arm, and no PDF exists for New. All four arms flagged the Midterm-1 outline versus Final mismatch and the missing Bayes notes (recorded as scope checks under the plan's scoring note).

## Resources (descriptive; CLI counters, not a bill)

Completed tool commands and processed tokens (input incl. cached + output), per session:

| Session | Draft (turns 1-2): s / commands / tokens | Revision (turn 3) | Fresh turn 4 | Session total tokens |
|---|---|---|---|---|
| calendar New rep 1 | 209 / 9 / 412,144 | 107 / 0 / 181,244 | — | 593,388 |
| calendar New rep 2 | 306 / 12 / 576,664 | 42 / 3 / 162,432 | — | 739,096 |
| sheet Old rep 1 | 316 / 18 / 861,741 | 71 / 2 / 202,927 | 58 / 9 / 305,413 | 1,370,081 |
| sheet Old rep 2 | 355 / 18 / 1,119,568 | 76 / 4 / 400,058 | 147 / 14 / 664,764 | 2,184,390 |
| sheet New rep 1 | 356 / 18 / 801,327 | 87 / 3 / 221,928 | 61 / 4 / 171,481 | 1,194,736 |
| sheet New rep 2 | 278 / 11 / 615,907 | 144 / 3 / 391,226 | 67 / 7 / 200,370 | 1,207,503 |

All 22 turns: 7,289,194 processed tokens, above the plan's 3-6M estimate. New's sheet sessions used fewer tokens than Old's, but New never rendered a PDF, so the comparison is not like for like and is not evidence of a speed or cost gain.

## Findings for the skill (not changed during the pilot)

1. **No-dependency PDF path needed.** `render_sheet.py` requires ReportLab; without it the new default output is a source file, where v2.0.1 made a PDF with PyMuPDF, which this host happens to have (correction below). Either add a fallback (HTML with print CSS, printed by an installed Chromium browser) or make the install question unmissable. Release blocker for advertising the sheet feature.
2. **Ask, then wait.** `study-plan.md` (and the sheet allowance question) should say: ask in the reply and end the turn; do not continue with a default unless the student asks for it. In exec mode the CLI question tool returned nothing and the tutor proceeded.
3. **Unrecorded-course offer was never made (0/2).** The instruction is in step 4 of Gather but is easy to skip; make it part of the delivery summary.
4. **Missing exam end time:** allow `exam.end` to be omitted (default duration) or tell the tutor to assume a duration and say so, instead of asking (rep 1) or inventing 09:01 (rep 2).
5. **Ask before installing ReportLab** was not followed (0/2); wording should give the exact question.

## Not measured

Learning gains, real students, other models (results on `gpt-6-luna` are not comparable with the earlier `gpt-6.1-sol` benchmarks), New-arm PDF layout and sheet content quality (no PDF), blind scoring, calendar-app import, connector writes, paper printing, other operating systems.

## Evidence

`protocol.json` (model, revisions, fingerprints, isolation), `results-*.json`, `runs/<session>/` (prompts, sanitized JSONL events, responses, per-turn file snapshots, usage metadata), frozen skills `skill-New/`, `skill-Old/`. Demo candidate for T013: `runs/calendar-New-rep2/files-after-03/plans/sta-cs-finals-2026/calendar.html` (synthetic courses). No New-arm sheet PDF exists for a screenshot.

Sanitizing (2026-11-18, cc): the runner scrubbed temporary work paths only; private home-directory prefixes in 56 evidence files across this report and the three smoke folders were replaced with `<HOME>` before commit. Numbers and event structure are unchanged.
Links in tutor replies that pointed into the temporary session folders (absolute or relative) were turned into plain `path` text so the archive has no broken links; the files themselves are in each turn's `files-after-NN/` snapshot.

## Correction (2026-11-19, cc)

An earlier version of this report said v2.0.1 printed its PDFs "through the browser". The Old-arm logs show `import fitz` (PyMuPDF) in both sessions and no browser print command. The follow-up rerun ([2026-11-19-sheet-rerun](../2026-11-19-sheet-rerun/REPORT.md)) also found that headless Edge cannot print inside the Codex Windows sandbox used here.
