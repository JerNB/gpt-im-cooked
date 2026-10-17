# Answer exposure, reviewed evidence, and next practice

Date: October 17, 2026 (Asia/Shanghai). Source before patch: commit `389a7a6`
(v0.5.0). Candidate: v0.5.1. All learner responses in this evaluation are synthetic.
No real-student learning outcome or external expert verdict is reported.

## Finding and repair

The original October 15 generated concept page has an executable evidence defect:
its first Check displays the answer, but its next same-item response still exports
`reveal_before_submission: false` and `stage: independent_transfer`. This loses
known answer exposure before the tutor reviews the response. A new attempt ID
does not make that response a new independent context.

This was reproduced by executing the actual archived script, not by inferring
failure from the old report. [Original page](../../fixtures/legacy-grouped-transformations.html)
SHA-256: `e864c12972c2cb1cc48f9da6b22a93743e2e272cec1f5bbf25a3887522f11495`.
[Original exported responses](inputs/legacy-attempt.json) SHA-256:
`19aa3be22e9c4b83f9424b3fd7ee4c2f9354323365207b44fba5014eeba8e548`.
These files preserve the observed defect; do not repair them in place.

The [repaired standalone example](../../../examples/grouped-transformations.html)
captures exposure before feedback, then remembers that feedback revealed the
answer. Retry clears the display while retaining that item exposure. It no
longer claims that an activity stage proves independence. Its artifact version
is 1.0.1; its package provenance is the current 0.5.1 candidate. The serialized
example expression also uses the existing `rate` column rather than the missing
`tax_rate`. No R execution is claimed.

Two small instruction changes address the same evidence boundary:
[page authoring](../../../plugins/gpt-im-cooked/skills/gpt-im-cooked/references/interactive-review.md)
includes a response-before-feedback state pattern; [import review](../../../plugins/gpt-im-cooked/skills/gpt-im-cooked/references/state.md)
explicitly reconciles exported flags with the inspected feedback path, retaining
original bytes and qualified judgments. No new grading engine, mastery metric,
mandatory diagnostic or study format was added. Existing installed/generated
pages are not automatically migrated. v0.5.0 archives remain untouched.

## Evidence audit

| Requirement | Design before patch | Mechanical evidence | Tutor behavior evidence | Real learner evidence |
|---|---|---|---|---|
| Correct answer and reasoning | Existing skill/practice guidance | Exact arithmetic in computation.json; cannot grade arbitrary reasoning | October 10 raw examples; current correct-number/wrong-reason and equivalence cases | None |
| Assistance at response time | Existing state/page guidance | Existing public-demo snapshots pass; original October 15 concept page fails the new replay | Current before/after import tests below | None |
| Import identity and selective state | Existing state guidance and helper | Existing conflict/backup tests rerun; duplicate record/backup hashes preserved in current cases | Three repeated-import sessions below | None |
| Corrected review removes stale diagnosis | Existing revision guidance | Byte integrity only; no semantic guarantee | Controlled false prior verdict corrected in one fresh context | None |
| Record informs next practice | Existing blueprint requirement | Source/record/item links can be inspected | Record replacement changes topic in one ablation comparison | None |
| Learning improves or lasts | Existing evaluation proposal | Not established by script tests | A simulated student is not a learner | Unperformed |
| Plugin discovery / new HTML/PDF defaults | Existing release requirements | Package checks only | Not tested in this scoped run | Unperformed |

The October 15 initial grading error is visible in [extracted original messages](historical-grading-excerpts.json):
the tutor first endorses OR, then accepts a correction to AND. The full original
local logs retain their original hashes; the extracted messages omit native paths
and unrelated metadata. The original review/key URLs were unavailable to the web
tool on October 17, so that instructor-key claim is historical, not a fresh
independent verification of Q21. The old misplaced import-ledger row was also
observed in the local record snapshot; no fresh recurrence is claimed here.

## Raw chain and bidirectional locators

| Claim / event | Original evidence | Review, record and consequence |
|---|---|---|
| Mutate keeps four observations; scalar summary has two groups | Existing fixture course-packet.md L2; original concept page Transfer/comparison; exact arithmetic in computation.json | Conditional intended-task grading; literal original R expression is defective |
| First response predicts two because there are two regions | inputs/legacy-attempt.json transfer_history[0], matching original page item | runs/legacy-01/feedback.md and learning-record.md Attempt history retain the original error |
| First Check reveals four and its explanation | Original page Check handler; legacy-replay-red.json feedback_before_retry | Later exposure must be considered even without a reveal-button event |
| Retry predicts four with correct explanation, but claims no reveal | inputs/legacy-attempt.json transfer_history[1]; replay export entry 1 | All three before and three after tutors qualify it as assisted improvement |
| Original export remains unchanged | Input SHA above; per-run hashes in manifest.json | Review corrections live in feedback/record, not overwritten JSON |
| New practice is a fresh row-count application | runs/revised-01/learning-record.md Concepts/Next session | runs/revised-01/next-question.md and separate next-solution.md; not yet student evidence |
| Numeric correctness can hide wrong population reasoning | runs/baseline-01/response-04.md and clinic-attempt-01.md | record-after-04.md changes to Recheck while preserving prior successes |
| Correct same-item recall follows disclosed feedback | runs/baseline-01/clinic-attempt-02.md | record-after-05.md changes to Improving and assigns a new population task; no independent-transfer count |

Each run directory retains its original inputs, tutor-saved replies, feedback,
question/key and final record. Baseline runs also retain every turn's record.
Relative links in records point back to source/attempt/feedback and forward to
the next question. `manifest.json` fingerprints 213 archived files and both full
skill snapshots; these are saved artifacts, not complete service/tool transcripts.

## Protocol and model results

See [initial protocol](PROTOCOL.md), [legacy protocol](LEGACY-PROTOCOL.md),
[grading/correction cases](COUNTEREXAMPLES.md), and `adjudication.json`.
Twelve isolated tutor contexts completed 24 turns. Tutors received realistic
requests, their frozen skill and permitted raw inputs only, without these
protocols, expected verdicts or author conclusions. No run was interrupted or
discarded. Rubric judgments below were made by the author/root agent, not an
external assessor. File-integrity tests do not independently endorse those
semantic judgments.

All contexts inherited the same parent model configuration without overrides.
The collaboration service does not expose an exact backend model ID/build;
strict backend-version pinning is therefore **not established**. Frozen source,
inputs, requests and outcomes are reproducible; an identical model response is
not promised. The first three baseline turns use identical inputs across three
contexts. Turns 4-5 use each tutor's own generated follow-up, so their numerical
details differ and are reported as a separate extension.

| Specific criterion | Failures / applicable completed contexts | Evidence |
|---|---|---|
| Grading: correct Q4 + seven blanks | 0/3 | baseline-01..03, turn 1 |
| Diagnosis: correct number but wrong population reason is not fully correct | 0/3 | baseline-01..03, turn 4 |
| Assistance: untracked outside help is not established independence | 0/3 | baseline-01..03, turn 1 |
| Assistance: later key access does not rewrite earlier exposure | 0/3 | baseline-01..03, turn 2 |
| Duplicate evidence: reimport adds no attempt/success and no record/backup write | 0/3 | turn 3; before-duplicate.json equals after-duplicate.json |
| Propagation: same-item correct recall after feedback is not fresh transfer | 0/3 | turn 5; original errors remain, next task changes context |
| Equivalent answer accepted | 0/1 | counterexamples C1: 7/10 = 0.70 |
| Ambiguity/key conflict is not confirmed student error | 0/1 | counterexamples C2: Plus 28/40; all-short 40/60; key 28/60 is a different joint population |
| Review correction supersedes verdict without a new attempt or stale drill | 0/1 | counterexamples record-before.md versus learning-record.md |
| Legacy contradictory export: assistance error, before instruction patch | 0/3 | legacy-01..03; actual page path overrides false flags |
| Legacy contradictory export: assistance error, after instruction patch | 0/3 | revised-01..03, identical original inputs |
| Legacy export error propagates to independent success/mastery/next task | 0/3 before; 0/3 after | respective Concepts/Attempt history/Next session and separate questions |

There is **no measured tutor-behavior improvement** from 0/3 to 0/3. The observed
repair is in the runnable concept artifact; the instruction patch documents the
required cross-check and had no observed regression in this small sample. The
current tutors already caught the original export defect without the student's
explicit disclosure. This does not prove other models or newly generated pages
will do so. We did not regenerate a sample of new pages after this patch.

## Record ablation

The packet, worksheet, export and first-turn request were held fixed. Only the
initial learning record changed. The original three baseline contexts received
the denominator history. Additional fresh contexts received no prior performance
evidence or a reviewed missing-values error, respectively.

| Initial record | Actual next question |
|---|---|
| Denominator error plus one correct prior context | All three baseline contexts use an outcome-defined population spanning table rows |
| Prior learning evidence removed | ablation-removed uses a course-grounded reference-population follow-up; no invented prior weakness |
| Replaced by reviewed na.rm/original-data error | ablation-replaced selects a mean with NA and asks what happens to original rows |

Replacement shows sensitivity to this recorded difficulty in one comparison.
Removing evidence did not change the topic relative to the recent Q4; this does
not isolate a benefit from saved memory. Neither comparison measures learning or
establishes a causal improvement in practice quality.

## Runtime RED/GREEN and repeat commands

```text
node tests/check_concept_retry.cjs tests/fixtures/legacy-grouped-transformations.html
```

Expected RED on the preserved original: `Retry after disclosed solution must
retain exposure`, actual false / expected true. The command really executed and
failed; see [red output](red.txt) and [captured feedback/export](legacy-replay-red.json).
The RED checkpoint is commit `5d4b078`, reachable from the task branch.

```text
node tests/check_concept_retry.cjs examples/grouped-transformations.html
node --test --experimental-test-coverage tests/check_demo_state.cjs tests/check_evidence_chain.cjs tests/check_concept_retry.cjs
python tests/check_evidence_archive.py
python tests/check_state_io.py
python tests/check_run_evidence.py
python tests/validate_package.py
python scripts/build_packages.py
python tests/check_distribution.py
```

The repaired page passes wrong-first and correct-first answer paths, blank and
double-click handling, stable re-export IDs, original-response preservation and
non-retroactive exposure. [Green replay](legacy-replay-green.json) preserves the
actual generated data. These tests execute real page JavaScript with a minimal
DOM; they do not establish browser rendering or native download behavior. A
direct local-file Chrome check was rejected by the browser URL security policy;
no alternate transport or browser workaround was used, and no new browser-test
claim is made. The archived October 15 screenshots are historical only.

Coverage for the three JS test adapters plus fixture preparer is 100% lines /
94.85% branches / 95.95% functions. The Node report does not instrument the HTML
script executed through `vm`; it must not be presented as product-wide or
instruction-adherence coverage. Full verification output is in VERIFICATION.md.

## External acceptance and remaining uncertainty

[External review and real-student protocol](EXTERNAL-REVIEW.md) supplies blind
adjudication cases, a rating form, comparison condition, equal study time, unseen
parallel forms and a seven-day delayed test. Teacher adjudication, recruitment,
validated test forms, learning outcomes and statistical power are unperformed.
No participant, rating or gain has been simulated as evidence.

The next most informative technical test is a frozen-source generation sample:
ask independent tutors to create concept pages, execute each actual delivered
feedback/retry/export path, and report failures for every page. The repaired
example and import checks do not prove generation compliance. To assess learning,
execute the independent teacher-validated delayed-transfer pilot separately.
