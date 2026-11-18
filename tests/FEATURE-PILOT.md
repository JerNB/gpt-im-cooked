# Fresh-model feature pilot: study calendar and exam sheet (T016)

Status: **plan, frozen before any run; needs the human's approval of model calls.** Author: cc, 2026-11-18. Runner and reporter: codex. Skill under test: `main` at `74dceec` (PR #9: T010 calendar, T011 sheet). Comparison arm for the sheet only: v2.0.1 (`20bb271`, tag `v2.0.1`).

## Why

T010/T011 were checked by script tests and two code reviews, never by a real model following the skill text. Before v2.0.2 and the public post on 2026-11-20 we need to know, on a small synthetic workload, whether a fresh model actually uses the new workflow, and we need real outputs for the post's screenshots. This is an exploratory pilot (n = 2 per cell), not a learning-outcome study.

## What is measured

1. **Calendar (new skill only).** Does the tutor ask one combined availability question, derive tasks from the records by the `references/study-plan.md` table with a valid basis, offer unrecorded courses once, use `plan_study.py`, and deliver `plan.ics` + `calendar.html` without touching any calendar?
2. **Exam sheet (v2.0.1 versus new).** Does the new skill ask exactly one allowance question, draft without a content-plan approval request, render through `render_sheet.py` within the page allowance, follow the content rules, apply a revision exactly, and reuse the saved preference in a fresh session? How long do the first draft and one revision take compared with v2.0.1?

## Fixtures (synthetic; codex builds them under `tests/fixtures/feature-pilot/`, committed before any run)

- **STA course** (folder `STA/`): packet S materials (`tests/fixtures/controlled-comparison/packet-s/materials/`), plus a course profile (exam 2026-12-08 09:00-12:00; reference-sheet allowance `Unknown`) and a learning record whose Concepts rows cover exactly:
  - T1 Demonstrated with `Recheck before exam`, promoted in a session dated 2026-11-17;
  - T2 Needs practice, with a corrective rule and one attempt row;
  - T3 Improving (same-structure successes, no transfer yet);
  - T4 in scope and Unassessed, notes available;
  - T5 in scope, teaching notes missing;
  - T6 excluded.
- **CS course** (folder `CS/`): packet P materials with an analogous record (at least one Needs practice, one Improving, one Unassessed), exam 2026-12-10 14:00-17:00.
- **HIST 101**: no folder and no record; it exists only in the scripted student message.
- Ground truth for the checks: a `expected.json` listing each concept's status and the task kind §5.2 of the design implies.

## Sessions and script

Same model and settings as T007 (`gpt-6.1-sol`, medium, Codex CLI as installed; record the version), same isolation (isolated `CODEX_HOME`, user config ignored, global and bundled skills disabled and verified, inherited CODEX variables stripped), serial execution, fresh session per row, no splicing of failed sessions. Every student message starts with the date sentence so dates are deterministic.

**Calendar, arm New, 2 sessions** (working directory = study root containing `STA/` and `CS/`):

| Turn | Student message (fixed text) |
|---|---|
| 1 | "Today is Wednesday 2026-11-18. My STA and CS finals are coming up (folders are here). Can you make me a study calendar?" |
| 2 | "Exams: STA Dec 8, 9am-12pm; CS Dec 10, 2-5pm. I can study weekdays 7-10pm and weekends 2-6pm, not Nov 25-27 (Thanksgiving). At most 3 hours a day." |
| 3 | "Yes, please also add HIST 101: exam Dec 11 at 9am, about 2 hours a week." (sent whether or not the offer was made; the check records whether it was) |

**Exam sheet, arms Old (v2.0.1) and New, 2 sessions each, alternating which arm runs first** (working directory = `STA/` only):

| Turn | Student message (fixed text) |
|---|---|
| 1 | "Today is Wednesday 2026-11-18. Can you make me a study guide for my STA final?" |
| 2 | "It's a cheat sheet I can bring into the exam: one sheet, both sides." |
| 3 | "Please replace the abstract interpretation rules with one worked example, and use the space you save to make it easier to read. Don't add new information." |
| 4 (new session, same folder after turn 3) | "Today is Thursday 2026-11-19. Make me a cheat sheet for my STA final." |

Turn 4 tests whether the preference saved after turn 3 is reused. A PDF may legitimately appear at turn 1 (no question asked) or turn 2; record which.

## Checks (pass / fail / unclear, each with a quoted line or file evidence)

Calendar:

- **C1** The first reply asks for availability in one message (exam times, weekly windows, days off, daily cap) or offers the all-day fallback; no second clarification round before planning.
- **C2** `plan_study.py` ran and `plan.ics` and `calendar.html` were delivered (command log plus files).
- **C3** Every task's `basis` cites a concept or topic that exists in the record (script check against `expected.json`).
- **C4** Task kinds follow the table: T1 `recheck` with `not_before` ≥ 2026-11-18; T2 `variant`; T3 transfer `practice`; T4 `learn` and later `practice`; T5 `source-gap`; T6 nothing (script check).
- **C5** The unrecorded-course offer is made once; HIST 101 gets only `review` blocks with basis "No learning record".
- **C6** No attempt to write to a calendar, no reminders promised; any unplaced task is reported to the student.

Sheet:

- **S1** Before the first draft, the tutor asks at most one question and it is about the allowance; no request to approve a content plan.
- **S2** The first draft is an actual PDF; with the turn-2 answer it is at most 2 pages. New arm: produced by `render_sheet.py` (command log).
- **S3** Content rules, scored blind from the PDF text and previews by a reviewer who does not see the arm: easy facts as one-line cues; one running example per related cluster; multi-step conversions staged and labelled; no generic checklist; no clipped or unreadable text.
- **S4** The turn-3 revision applies the request and adds no new topic (diff of section and topic lists between the drafts).
- **S5** New arm: a `Reference-sheet preferences` section is saved in the course profile after turn 3; in turn 4 the draft follows it without being told again. Old arm: record whether anything comparable happened.

Resources (descriptive only): wall time, completed tool commands and processed tokens for the first draft (turns 1-2), the revision (turn 3) and turn 4, per session. CLI usage is cumulative per thread: report differences, as in T007.

## Outputs

`tests/reports/2026-11-18-feature-pilot/`: protocol with fingerprints, sanitized logs, per-turn snapshots, the final study folders (including `plan.ics`, `calendar.html`, sheet PDFs, previews and `checks.json`), scores with quotes, blind-review material, and `REPORT.md` following the house style: counts not rates, what was and was not measured, failures and reruns kept.

The best-looking calendar page and sheet preview from the **New** arm are the source for the T013 post images. They must be labelled as outputs on a synthetic course; no hand-edited or mocked screenshots.

## Budget and schedule

Main runs: 2 calendar sessions × 3 turns + 4 sheet sessions × 3 turns + 4 fresh turn-4 sessions = **22 model turns**, plus at most one smoke turn per arm (excluded from statistics). Based on T004/T007 (about 0.1-0.3M processed tokens per turn, mostly cached input), expect roughly **3-6M processed tokens** and 1-1.5 hours of CLI time. These are CLI counters, not a bill. Stop on a quota failure; no automatic retries; a rerun is a fresh whole session.

Results are needed by **Thursday 2026-11-19 noon** so the post images can be made from them.

## What this cannot show

Two sessions per cell, one model, one scripted student, synthetic courses. It cannot show learning gains, behaviour on other models or real students, calendar-app import, connector writes, paper printing, or fonts on other operating systems. Speed numbers are descriptive and may differ by run.
