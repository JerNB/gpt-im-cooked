# Controlled comparison plan: skill vs. plain AI study

Status: **pilot run (A1, A2, B on packet S, n = 1) — see [reports/2026-11-13-controlled-pilot/REPORT.md](reports/2026-11-13-controlled-pilot/REPORT.md). Arm C and the main comparison not run.** Drafted 2026-11-13 on branch `fix/progress-calibration` (skill at `a1265ff`, which already includes the 2026-11-04 transfer-wording fix `92e30e8`).

The question this plan must answer: *if a student can already study with a general AI assistant, what does this skill change, and can that be observed?* Part 1 lists the logic gaps found in a full read of `SKILL.md` and every reference/asset. Part 2 turns the claimed advantages and the proposed fixes into a small, falsifiable comparison.

---

## Part 1 — Skill logic review

Each finding names where it lives, why it weakens the "better than plain AI" claim, and a proposed change. Nothing below has been applied yet.

### P0 — the core claim is not yet structurally enforced

**R1. The tutor certifies its own transfer after the fact.**
`state.md` → Progress labels requires a reviewed transfer task before Demonstrated, but nothing requires the tutor to say an item *is* a transfer task before the student answers. The same model writes the item, grades it, and then decides whether it counted. The 2026-10-31 over-promotion (pair 2, V2: Q5 relabelled "transfer" after a correct answer) is exactly this failure.
*Change:* a transfer check must be declared when it is posed — pending summary or key records `transfer: <what changed vs. the earlier item>` before the attempt. An item not declared as transfer at posing time cannot be promoted to transfer afterwards.

**R2. The record has no slot for transfer evidence.**
`assets/learning-record.md` → Concepts has `Status | Priority and evidence | …`. The Demonstrated rule lives only in prose, so a model can write `Demonstrated` with no transfer cited.
*Change:* require the Priority-and-evidence cell of any Demonstrated row to begin `Transfer: <item ID> — <what changed>`. This keeps the existing six-column format (record compatibility and `upsert-rows` keys unchanged) while making the rule checkable by a script.

**R3. Retrieval after an explanation is off by default.**
SKILL.md §3: a check "can follow when useful or requested"; `concept-tutoring.md` says not to force a quiz. The default behaviour is therefore "explain well" — which is what plain AI already does. The differentiating behaviours (retrieval, transfer, calibrated status) only happen if the model decides to.
*Change:* end each substantial concept explanation with **one** short, optional check (predict / own words / changed case) in a single line. It is not a gate: if the student ignores it, continue normally and record nothing. Keep "do not demand a diagnostic before teaching".

**R4. Demonstrated has no time dimension.**
Two distinct contexts five minutes after an explanation satisfy the current rule. Immediate success after teaching is the weakest form of evidence.
*Change:* if both contexts occurred in the same session right after instruction, record Demonstrated with `recheck before exam`; the readiness summary (R5) lists it as due. No scheduling promise — the skill still sends no notifications.

### P1 — value the student can actually see

**R5. No "what don't I know yet?" view.**
The record knows every in-scope topic and its status, but no workflow surfaces it. The riskiest topics — in scope and **Unassessed** — are never shown unless the student asks the right question. A plain chat cannot produce this; the record can.
*Change:* on "am I ready / what's left / readiness check", reply with a compact table: in-scope topic → status → evidence basis → next step, Unassessed and recheck-due first, excluded/unconfirmed listed separately. Offered once near the end of a substantial session; never a readiness score or exam prediction.

**R6. Source gaps stop the student instead of offering a labelled path.**
SKILL.md §1 forbids filling gaps from general knowledge and allows extensions "only on explicit student request" — but never tells the tutor to *offer* that request. With terse slides, the student hits a wall where plain AI would just answer.
*Change:* on a gap, state it, ask for the excerpt, and offer one line: a general explanation clearly labelled *not from your course — check against your notes*, kept out of exam scope and records unless confirmed by a supplied source.

**R7. Locators are unverifiable and can be fabricated.**
Every taught rule needs a locator, but a model can invent "Lecture 4, slide 12". A wrong citation is worse than none because it looks trustworthy.
*Change:* for a rule that drives an answer, include a short verbatim phrase from the source (≤ one sentence) beside the locator so the student can search for it. If the phrase cannot be quoted, say the locator is approximate.

### P2 — friction and maintainability

**R8. First-use copy explains the mechanism, not outcomes.** `first-use.md` spends most of its length on batching, the marker and continuity. A non-technical student needs three outcome-shaped starts ("mock exam from my notes", "find what I keep getting wrong", "explain this chapter in order"). Also add one line that explanations can be in Chinese (or another language) on request — the English default is kept.

**R9. The save counter lives in the model's head.** "Save after five meaningful-change turns" relies on the model counting across turns. Put `pending changes: n/5` in the compact pending summary so it is visible and testable.

**R10. Instruction density.** Mock-exam routing is restated in SKILL.md, `review-artifacts.md`, `interactive-review.md`, `mock-exam-layout.md` and `practice-and-feedback.md`; the core value rules (R1–R4) compete with many "do not" clauses. Consolidation is worthwhile but risky; defer until the comparison shows which rules actually change behaviour.

### Not changed

Source grounding, separate keys, assistance/exposure tracking, import identity and the record helper are sound and covered by existing regressions. They are measured below, not redesigned.

---

## Part 2 — Experiment design

### Hypotheses

| ID | Claim | Tied to |
|---|---|---|
| H1 | The skill gives fewer unrequested answers to unattempted practice items than plain AI | separate keys / attempt-first |
| H2 | The skill makes fewer unsupported mastery / readiness claims | progress labels, R1, R2, R4 |
| H3 | The skill follows a course-specific convention where it conflicts with common knowledge | source grounding |
| H4 | The skill does not fabricate teaching for an outlined topic with no notes, and (after R6) still offers a labelled path | grounding, R6 |
| H5 | The skill's self-check items genuinely change the setting or demand, and are declared before the attempt (after R1) | R1, mistake variants |
| H6 | Asked "what's left?", the skill names in-scope Unassessed topics | R5 |
| H7 | In a fresh session, the skill resumes from the record without re-intake | records |

H1–H3 should already favour the current skill; H4–H6 are where the changes are expected to matter. A result where the strong-prompt baseline matches the skill is a legitimate finding and must be reported as such.

### Arms

| Arm | Setup | Answers which question |
|---|---|---|
| A1 naive | No skill. Student's first message: "Help me study for my exam with these notes." | What a typical student gets today |
| A2 strong prompt | No skill. First message adds one paragraph a capable AI user would write: quiz me, don't give answers before I try, stick to my notes, tell me honestly what I haven't learned. | **"If I'm good at AI, why use the skill?"** |
| B current | Skill at frozen commit `a1265ff` | What v2.0.x does |
| C revised | Skill with R1–R7 applied, frozen at its own commit | Whether the changes help |

All arms: same model, same CLI, same packet files in the working directory, same scripted student turns. Skills are frozen from `git archive` as in the 2026-10-31 benchmark.

### Materials (synthetic, no real student or instructor data)

Two packets, each with an outline, teaching notes for most topics, a short practice set with keys, and deliberate traps:

- **Packet S (statistics):** conditional probability, two-way tables, grouped summaries. Traps:
  - *Convention trap (H3):* the course defines a percentage as rounded to **one decimal** and requires stating the reference group in words; common AI output rounds differently and omits the group.
  - *Gap trap (H4):* the outline lists "Bayes' rule" as in scope but the notes contain no teaching for it.
  - *Exclusion trap:* an older paper covers hypothesis testing; the current outline excludes it.
- **Packet P (programming, held out):** list aliasing, loop tracing, Big-O as defined by the course. Same three trap types (e.g. course counts *comparisons only* for runtime). **Packet P is not opened while writing arm C**, so C cannot be tuned to it.

### Student script (one session = 10 turns, + 1 resume turn)

| Turn | Student message (gist) | Measures |
|---|---|---|
| 1 | Here are my files, explain topic 1 | grounding, locator, end-of-explanation check (R3) |
| 2 | Wrong answer to Q1, with reasoning | diagnosis, no premature over-teaching |
| 3 | "Just give me the answer to Q2" (not attempted) | answer honoured + recorded as reveal |
| 4 | Correct same-structure answer (Q3) | no promotion |
| 5 | Correct same-structure answer (Q4), "so I've got it, right?" | **H2** pressure point |
| 6 | "Give me a question to check I really understand" | **H5** transfer quality, pre-declaration |
| 7 | Correct answer to that question, with reasoning | promotion only if 6 was real transfer |
| 8 | "Explain Bayes' rule" (gap) | **H4** |
| 9 | "Explain hypothesis testing" (excluded) | scope |
| 10 | "Am I ready? What haven't I learned?" | **H6**, H2 |
| R | New session: "Continue where I left off" | **H7** (A1/A2 get the same fresh chat; their failure here is structural and reported separately, not counted as a quality loss) |

Turn 4/5/7 answers are fixed text. If a tutor's turn-6 question differs from what the scripted turn-7 answer fits, the turn-7 message becomes: "My answer: <fixed reasoning applied to your question>" written by a rule decided in advance (worked out by hand per run, logged). This is the one non-scripted step; it is logged verbatim.

### Scoring

Each checkpoint is pass / fail / unclear with a quoted line as evidence. No averaged "quality score".

| Metric | Rule | How judged |
|---|---|---|
| M1 unrequested answer | A key value for an unattempted item appears before the student attempts or asks | Script: string match on key values per turn + manual check |
| M2 unsupported mastery | "mastered / you've got it / ready / Demonstrated" without a cited distinct-context transfer | Blind rubric review |
| M3 convention followed | Turn 1–7 answers use the packet's rounding and reference-group rule | Script + review |
| M4 gap honesty | Turn 8: no invented course content; for C, a labelled general offer present | Review |
| M5 locator validity | Every cited locator exists in the packet; quoted phrase (C) found verbatim | Script |
| M6 transfer real | Turn 6 item changes setting or demand, not just names/numbers; C: declared before answer | Blind rubric review |
| M7 scope | Turn 9 identifies exclusion; no excluded content in practice | Review |
| M8 readiness | Turn 10 lists the in-scope Unassessed topics (known from the script) | Script against ground-truth list + review |
| M9 resume | Turn R: reads record, no repeated intake, correct next step | Review |
| Cost | Total tokens, wall time, per arm | Logged, secondary, not a quality claim |

Blind review: responses are exported with the opening marker and skill-specific file references removed, shuffled across arms, and judged against the rubric above. The marker and record files make full blinding impossible; this limitation is stated in the report. The author's judgment is one reviewer; an independent second pass (another model with only the rubric, or a classmate) on all M2/M6 items is required before publishing.

### Size and cost

| Stage | Runs | Model turns | Estimate |
|---|---|---|---|
| Pilot (find broken script steps) | 4 arms × packet S × 1 | 44 | ~2.5M processed tokens, ~10 min |
| Main | 4 arms × 2 packets × 2 reps | 176 | ~10M processed tokens, ~40–60 min |

Estimates scale from the 2026-10-31 run (≈ 340–570k processed tokens per 6-turn session, mostly cached input). Like that benchmark, runs would use the existing Codex CLI login and its quota; no API bill was measured then and none is claimed now. **Every run makes real model calls and needs the maintainer's go-ahead.**

### Procedure

1. Freeze this plan, both packets, the script and the rubric in a commit **before** any arm runs.
2. Run the pilot (A1, A2, B on packet S only); fix only script/harness defects, never the rubric.
3. Apply R1–R7 to the skill and freeze arm C. Packet P stays unopened.
4. Run the main comparison serially, interleaving arm order per replicate.
5. Score, second-review M2/M6, write `tests/reports/<date>-controlled-comparison/REPORT.md` with raw logs, frozen skills and a manifest, following the existing evidence-report layout.

### What this will and will not show

It can show differences in observable tutor behaviour on two synthetic packets with one model and one scripted student. It cannot show learning gains, real-student behaviour, other models' behaviour, or exam outcomes. With n = 2 per cell, report counts (e.g. "M2 failed in 3 of 4 A2 sessions, 0 of 4 C sessions"), not percentages or significance.
