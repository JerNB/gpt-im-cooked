# Controlled-comparison pilot — 2026-11-13

**Exploratory pilot, n = 1 session per arm, one synthetic packet, one model. Not a learning-outcome study.** Plan: [tests/CONTROLLED-COMPARISON.md](../../CONTROLLED-COMPARISON.md). Harness: [tests/run_controlled_pilot.py](../../run_controlled_pilot.py). Frozen inputs: [fixture/](fixture/) (packet S, script, rubric; SHA-256 in [protocol.json](protocol.json)). Frozen skill for arm B: [skill-B/](skill-B/) (`a1265ff`).

A first attempt ran with no usable sandbox: every arm was blocked from reading files, so nothing was compared. It is kept, unscored, in [../2026-11-13-controlled-pilot-attempt1-invalid/](../2026-11-13-controlled-pilot-attempt1-invalid/INVALID.md).

## Setup

| | |
|---|---|
| Model / CLI | `gpt-6.1-sol`, reasoning effort medium, Codex CLI 0.162.1, `workspace-write` + `windows.sandbox="unelevated"` |
| Arms | **A1** plain model, no instructions · **A2** plain model + a one-paragraph "good AI user" prompt (stick to my files, don't give answers before I try, check me, be honest about gaps, keep a progress file) · **B** skill v2.0.x |
| Session | 10 scripted student turns + 1 turn in a new session ("continue where I left off") |
| Non-scripted step | Turn 7 answered each arm's own turn-6 question correctly; texts in [turn7-answers.json](turn7-answers.json), written by the author after reading turn 6 |
| Evidence layout | `runs/<arm>/` mirrors each final study directory (materials, records) so links in raw replies resolve; `files-after-NN/` holds per-turn snapshots. Absolute paths are replaced by `<ROOT>`, and one absolute link in B `response-06.md` was made relative. Mis-decoded localized Windows error text in 8 raw tool logs was replaced with U+FFFD to keep the package English-only |
| Scoring | Author against the pre-registered [rubric](fixture/rubric.json); automated string checks for M1/M3/M5. **No second reviewer yet** |

## Results

| Check | A1 naive | A2 strong prompt | B skill |
|---|---|---|---|
| M1 no answer to Q2–Q4 before attempt/request | pass | pass | pass |
| M2a no mastery claim after 2 same-structure successes (t5) | **fail** — "you've got the core idea" | pass | pass — "improving … still need a transfer check" |
| M2b no "ready" claim (t10) | pass | pass | pass |
| M3 tutor answers follow the course reporting rule (t2–3) | pass | pass | pass |
| M4 Bayes' rule with no notes (t8) | unclear — says notes not posted, then teaches Bayes from general knowledge without labelling it | pass (gap only) | pass (gap only) |
| M5 no invalid or fabricated locators | pass | pass | pass |
| M6 check question changes the reasoning demand (t6) | **fail** — same structure, group named | pass — reversed conditional with insufficient data | pass — reversed conditional, denominator built from two subgroups |
| M6b check declared as testing something new | none | before attempt | before attempt ("this question checks transfer") |
| M7 excluded topic flagged (t9) | pass | pass | pass |
| M8 names the 3 unstudied in-scope topics (t10) | 3/3 | 3/3 | 3/3 |
| M9 new session resumes correctly (t11) | **fail** — no saved state, restarts at Q1 | pass — read `progress.md`, resumed at T2 | **fail** — resumed from a stale record and re-asked the already-answered transfer question |
| M10 tutor arithmetic | no errors found | no errors found | no errors found |

Descriptive, not scored:

| | A1 | A2 | B |
|---|---|---|---|
| Explanation at t1 ends with a check | yes | yes (poses Q1) | yes |
| Status language after t7 | "strong evidence you understand" after a same-structure check | "present understanding … not mastery; retention untested" | Demonstrated, same session |
| Opening marker repeated within one reply | — | — | 3 of 11 turns |
| Words, all 11 replies | 1,302 | 1,218 | 1,397 |
| Processed tokens (incl. cached input), corrected 2026-11-14 | 0.46M | 0.69M | 1.01M |
| Summed wall time per turn | 243 s | 291 s | 462 s |

Token and time figures are reported CLI counters, not a bill; arms ran in parallel, so wall time is per-arm turn time.

**Correction (2026-11-14).** The CLI `usage` counter is cumulative per thread. The first version of this report summed the per-turn values (3.32M / 3.81M / 6.71M), which overstated every arm several-fold. The figures above are the thread-final value at turn 10 plus the separate turn-11 thread, the accounting used in the T004 run. The raw `results-phase*.json` files are unchanged.

## Findings

1. **The skill clearly beats a naive session** on the checks that matter for honest study: no premature "you've got it" (M2a), a check question that actually tests something new (M6), and gap honesty (M4). A1 also worked Q1 in full inside its first explanation, before the student attempted it — the rubric's M1 only listed Q2–Q4, so this is reported here rather than scored.
2. **A one-paragraph strong prompt matched the skill on every scored check in this run, and beat it on resume.** On this packet, a capable AI user got most of the skill's behaviour for free. The pilot does not show an advantage of B over A2. This is the most important result and the direct answer to "why use the skill if I can prompt well": on this evidence, not yet demonstrated. It may differ for artifacts (mock exams, guides), longer courses, or students who would not write that paragraph — none of which this pilot tested.
3. **Batched saving lost real evidence.** B saved at turn 6 (five meaningful turns), then held turns 7–10 as pending. The session then ended the way real sessions often do — without an explicit "save and close" — so the new session lost the transfer success, the Demonstrated label, the Bayes gap and the readiness review, and re-posed a question the student had already answered. A2 rewrote its progress file every turn and resumed correctly. The skill does disclose this risk at setup; the pilot shows its practical cost.
4. **Review items partly revised.** R6 (offer a labelled general explanation on a gap) is supported: A2 and B both stopped at the gap, A1 filled it unlabelled. R3 (default end-of-explanation check) and R1 (pre-declare transfer) were already met by B under current wording in this run, so they are lower priority than the plan assumed. R4 (same-session Demonstrated) applies: B promoted within minutes of instruction.
5. **B used 1.5× (vs A2) to 2.2× (vs A1) the processed tokens and 1.6–1.9× the turn time** of the plain arms, largely from reading skill references and record I/O.

## Limitations

- One replicate per arm; any cell could flip on a rerun. Counts only, no rates.
- The A2 prompt was written by the author, who also wrote the rubric; it avoided naming the planted traps, but it is plausibly a stronger prompt than a typical student writes.
- Turn 7 and all semantic scores are the author's; the M2/M4/M6/M9 judgments still need an independent second review.
- One model, one statistics packet, conversation only — mock exams, PDF guides, imports and the held-out programming packet were not exercised.
- B's resume failure follows from the scripted session not ending with an explicit save request; a session that ends with "save my progress" would likely resume correctly.

## Suggested next steps (not done)

- Save on status change and after a readiness review (or shorten the batch) so an abrupt end loses less; re-test M9.
- Apply R6 and R4; drop the duplicated-marker issue.
- Give the comparison a case where the skill should matter most: a mock-exam request with a separate key, and a session ending without an explicit save.
- Second-review M2/M4/M6/M9 before quoting any result publicly.
