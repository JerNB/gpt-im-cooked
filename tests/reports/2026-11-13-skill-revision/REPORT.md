# Skill revision report — 2026-11-13

**Status:** three behaviour changes applied to the working tree on `fix/progress-calibration` (base `a1265ff`, merged to main as `97be172`). **Uncommitted, unreleased, no version bump.** Checked by one exploratory real-model session (arm C, n = 1); the replicated comparison is specified for Codex in `.collab/handoff/T004.md`.

## Why these changes

A controlled pilot ([../2026-11-13-controlled-pilot/REPORT.md](../2026-11-13-controlled-pilot/REPORT.md)) ran the same 11-turn scripted student through a plain model (A1), a plain model with a strong one-paragraph prompt (A2), and the skill (B). Three problems in B motivated this revision:

| Pilot observation (B, n = 1) | Revision |
|---|---|
| Saved at turn 6, held turns 7-10 as pending; the session ended without an explicit close, so the new session lost the transfer success, the Bayes source gap and the readiness review, and re-asked an already-answered question (M9 fail). A2, which rewrote a progress file every turn, resumed correctly. | **S1** save immediately on any status change and after a readiness review |
| Promoted to Demonstrated minutes after instruction, all evidence from one session. | **R4** same-session Demonstrated carries `Recheck before exam` |
| At a topic with no course notes, B (and A2) only stopped and asked for notes; A1 taught it from general knowledge without saying so. Neither gave the student a usable, honest path. | **R6** offer once a general explanation labelled as not from the course |

Review items that the pilot showed were already met by the current wording (pre-declaring transfer, ending explanations with a check) were **not** changed.

## Exact changes

Four files, eight sentence-level edits; no new files, no record-format change (the six-column Concepts table and `record_io.py` keys are untouched).

### S1 — save on status change and readiness review

`references/state.md` → Read and save checkpoints, early-save list:

> Save earlier when the student asks to save, delete, or correct a record; **when a concept's status changes (promotion, demotion, or Recheck); after answering a readiness or "what's left" question;** when course/exam scope changes …

Same section, setup explanation, appended:

> Sessions often end without an explicit close, so status changes and readiness reviews are saved when they happen rather than left for the next batch.

`SKILL.md` §5: "early-save triggers **(including any status change and a readiness review)**". `assets/first-use.md`: "or earlier at checkpoints **such as a progress-label change**". The five-meaningful-turn default is unchanged.

### R4 — same-session Demonstrated needs a later recheck

`references/state.md` → Progress labels, after the transfer rule:

> When all supporting contexts come from the same session shortly after instruction, Demonstrated is still allowed, but write `Recheck before exam` in its evidence and make a later unaided application (a later session, or after other topics intervene) the next task; a readiness review lists it as due. Immediate success after teaching is weaker evidence of retention.

`SKILL.md` §5: "…changes the setting or reasoning demand, **and same-session evidence carries a recheck before the exam**".

### R6 — labelled general explanation on a source gap

`SKILL.md` §1, after the existing "only an explicit student request permits an optional extension":

> When a gap blocks what the student asked for, offer that choice once in one line: a general explanation labelled **not from your course materials — check it against your notes**. Give it only if accepted; keep it out of exam scope, practice keys, and progress evidence until a supplied source confirms it.

`references/concept-tutoring.md` gets the matching sentence, plus: flag where course notation or conventions may differ.

Source grounding is not relaxed: nothing is taught from general knowledge unless the student accepts, and accepted content never becomes course evidence.

## Arm C check (revised skill, same packet and script)

One session, run after the pilot with the same model, CLI, packet and student turns; skill copied from the working tree and fingerprinted in [../2026-11-13-controlled-pilot-armC/protocol.json](../2026-11-13-controlled-pilot-armC/protocol.json). Turn 7 answered C's own turn-6 question ([turn7-answers.json](../2026-11-13-controlled-pilot-armC/turn7-answers.json)). Raw evidence: [../2026-11-13-controlled-pilot-armC/runs/C/](../2026-11-13-controlled-pilot-armC/runs/C/).

| Check | B (pilot) | C (revised) | Evidence for C |
|---|---|---|---|
| M1 no answer before attempt (Q2-Q4) | pass | pass | automated, no hits |
| M2a no mastery claim at t5 | pass | pass | "Before calling the concept secure, let's check … then revisit it later before the exam" |
| M2b no "ready" claim at t10 | pass | pass | "I can't honestly call you ready for the whole midterm yet" |
| M3 course reporting rule | pass | pass | "40.0% of commuters", "25.0% of remote workers" |
| M4 gap honesty (Bayes) | pass, gap only | **pass, labelled offer** | t8: offers a general explanation labelled "not from your course materials—check it against your notes" |
| M5 locators valid | pass | pass | automated, no invalid or fabricated locators |
| M6 check changes reasoning demand | pass | pass | t6: evaluate a reversed-conditional claim (40.0% of commuters vs ?% of cyclists) |
| M7 excluded topic | pass | pass | t9 flags the exclusion; offers optional labelled explanation |
| M8 names 3 unstudied topics | 3/3 | 3/3 | t10 table |
| M9 resume in new session | **fail** | **pass** | t11 resumes at two-way tables and notes the pending retention check; record contains the Bayes gap and readiness review |
| M10 tutor arithmetic | no errors | no errors | review |
| Saved on each status change | no (t7 Demonstrated unsaved) | yes | record bytes changed at t1, t2, t4, t5, t7, t10 |
| Same-session Demonstrated marked for recheck | no | yes | record: "Recheck before exam"; t10 lists it |
| Marker repeated within a reply | 3 of 11 | **6 of 11** | t2, t4, t5, t6, t7, t10 |
| Processed tokens / summed turn time | 1.01M / 462 s | 1.14M / 435 s | CLI counters, not a bill. Corrected 2026-11-14: the first version summed cumulative per-turn counters (6.71M / 6.38M) and wrongly showed C below B; C used about 13% more |
| Words, 11 replies | 1,397 | 1,611 | |

Scoring is the author's, against the frozen pilot rubric; no blind or second review yet.

## What this does and does not show

- The three targeted behaviours appeared in C where they were absent in B: evidence was saved at the status change and the readiness review, the new session resumed correctly, the same-session promotion carried a recheck, and the gap got a labelled offer.
- n = 1 per arm, one statistics packet, one model, scripted student, author scoring. B and C ran at different times; run-to-run variation alone could explain any single cell. This is a smoke check, not a comparison result.
- It does **not** show that the skill beats A2 (the strong-prompt plain model). In the pilot A2 tied B on every scored check except resume, where it won; C now ties A2 on resume too. Whether any check separates the skill from a well-prompted plain model is the open question for T004.
- More saves cost something: the 2026-10-31 benchmark measured checkpoint turns ~82% slower. In this run C's summed turn time was not higher than B's, but its processed tokens were about 13% higher, and one session cannot settle either.

## Known issues not addressed

- **Repeated opening marker.** The marker appears twice in one reply when a tool-progress preamble is followed by the answer; 6/11 replies in C, 3/11 in B. Presentation only, but visible to students. Candidate fix: state that the marker appears once, at the start of the final answer, never in progress notes.
- **Answer leakage in examples (A1 only).** The plain model solved practice Q1 inside its first explanation; the skill arms used their own examples. The pilot rubric omitted Q1; T004 adds it.
- **Distribution check fails on HEAD** (pre-existing): v2.0.0 ZIPs predate the mock-exam renderer files in the allowlist. A release of this revision needs a 2.0.1 bump and new ZIPs; v2.0.0 archives stay untouched.
- **`docs/interactive-learning-reference.md`** (untracked, Chinese) fails `validate_package.py` in the main checkout.

## Next

1. Human: approve committing this revision to a `cc/T003-*` branch so Codex can test it from its own worktree (T004 prerequisite).
2. Codex: T004 replicated comparison (4 arms x 2 packets x 2 reps, held-out programming packet, blind scoring) per `.collab/handoff/T004.md`.
3. cc: cross-review T004 results; decide on 2.0.1 only after them.
