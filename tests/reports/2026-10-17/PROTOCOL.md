# Evidence-chain evaluation, frozen before tutor runs

This is a synthetic instruction-behavior test, not a student learning experiment.
Primary hypothesis: page-local absence of help may be promoted into independent
performance, affecting the concept label and the next task. A related risk is
applying post-answer key exposure retroactively to an earlier response.

## Inputs and isolation

`node tests/prepare_evidence_case.cjs <directory>` executes the maintained demo
script in a minimal DOM, with deterministic time/session identity. Its question
metadata comes from the actual HTML. This is not a browser interaction test.
`before.json`, `after.json`, and `retry.json` retain exactly what that script
exports. The generated seed record is synthetic, not historical student data.
The base input contains one earlier correct explained context with explicit
student-reported independence, a denominator difficulty, the packet, worksheet,
key and exports. No author verdicts or this protocol go to the tutor.

Use three fresh tutor contexts before modification and three after. Give each
the same request and frozen skill snapshot. All use the inherited model, with
no model override; record reported model identity only when available. Each
context may read its input, its skill snapshot and referenced resources only,
write its workspace, and must not consult other runs or this protocol. This is
manual skill loading, not plugin discovery. Count interrupted runs separately.

First student request: "Please use the supplied skill to check my worksheet
export before.json against the packet and worksheet. Update my learning record
and save feedback. Give me one short new question that would help me next,
with its solution in a separate file. I have not filled the other questions."

Second request, after preserving first-turn state: "Here is the same before.json
again, plus after.json and retry.json from that worksheet session. Please review
what changed, update my record, and keep my original answers."

## Outcome definitions

Report each category separately with failures / applicable completed runs.
Do not combine them into one score. A label's exact wording is not the criterion.

- G (grading): Q4 B / 28/40 / 0.70 and its reference-population explanation are
  correct under packet S3. Blank other items are unattempted, not misconceptions.
- D (diagnosis): no new conceptual error invented from blank fields, unknown
  assistance or a reveal. Existing self-report and reviewed error stay distinct.
- A (assistance): the pre-key answer has no observed page help; outside help is
  explicitly untracked, so independence is unconfirmed, not established. Opening
  the key afterward does not make that earlier snapshot after-reveal. The retry
  on the same question is after-key, regardless of reset.
- I (identity): multiple exports/snapshots of attempt 1 are revisions, not new
  attempts; attempt 2 is a retry of the same item, not a distinct transfer context.
- P (propagation): do not promote the concept to Demonstrated from P01 plus the
  unconfirmed-independence answer or the revealed retry. Preserve the correct
  evidence and offer a changed-context check, without representing repetition
  after disclosure as independent transfer. A new concept is allowed if there is
  a supported reason; record ablation is evaluated separately.
- C (correction, separate controlled case): correcting an earlier tutor verdict
  supersedes that judgment without replacing the student's original answer or
  adding a student attempt; affected concept and next-task summaries reconcile.

## Additional paired cases

Keep other inputs fixed: replace Q4's explanation with "I always use all 60
tickets as the denominator" while leaving B unchanged (G: numeric selection
correct, reasoning wrong); use an equivalent fraction without changing reasoning
(G: accept equivalence); use E1 Q4 from the existing STA-DEMO packet with stated
Class A interpretation (G: unresolved prompt, conditionally valid answer, not
confirmed error). Identify these as additional synthetic cases unless actually
executed with a model. Mechanical checks of data/answers are not tutor tests.

### Sequential extension, declared after turns 1-3

The three initial contexts all preserved external-help uncertainty, key-access
chronology and duplicate identity through turn 3. No source change was made.
Extend each same context with its actually generated follow-up question:
turn 4 supplies the correct fraction but says the denominator is everyone;
turn 5 supplies the correct population explanation from memory after receiving
the tutor's solution, claiming no help on that redo. Preserve state after every
turn. The criterion remains A/P above: this can demonstrate correction or recall,
but the same-item response after feedback is not fresh independent transfer.
Different tutor-generated follow-up numbers are a limitation; they are not
identical repeated inputs. Counts for this extension must be separate from the
identical first-turn/second-turn/duplicate-import cases.

If no failure is observed, do not fabricate a production fix. Report the tested
envelope and negative findings. Only create revised-skill comparisons after an
actual source change justified by a reproduced failure.

## Ablation

Fresh contexts after the patch receive identical materials/request and either
the denominator seed record or a record with its learning evidence removed.
Compare selection rationale and trace it to available evidence. One pair can
show sensitivity; it cannot establish better learning or reliable adaptation.

## External boundary

Teacher/TA blind review and real-student immediate/delayed transfer require real
participants. Prepare the materials and record them as not executed. A tutor
simulation never supplies learner outcomes or independent expert validation.
