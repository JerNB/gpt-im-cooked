# Independent quality review

Date: October 31, 2026. Reviewer scope: supplied packet, scripted student prompts, each arm's six final response files, and final record snapshots. No model was run for this review. Token counts, latency, and the desired efficiency result were not used to grade quality. This is an authoring-agent review, not an external educator assessment or a learner-outcome study.

## Pair 1

### Outcome

Both arms pass the narrow end-of-session evidence-preservation and feedback gates. No material arithmetic, supplied-rule, or final-record omission was found. The responses are not identical teaching treatments: baseline's first response gives a Q3-specific denominator cue, while V2's first response asks a different hypothetical. Baseline correctly records this difference later. The comparison can support task-level preservation, but not a claim of identical instructional content.

| Gate | Baseline | V2 | Evidence |
|---|---|---|---|
| Five answers correctly reviewed | Pass | Pass | Responses 01-05 match packet keys: Q1 2/8=25%, Q2 8 rows, Q3 3/12=25%, Q4 6 matching pairs, Q5 5/20=25% |
| Three errors and original reasoning retained | Pass | Pass | Final records, Attempt history, lines 20-24 retain full-sample denominator reasoning, grouping-implies-one-row-per-group, and one-match-per-right-row reasoning |
| Both correct applications retained | Pass | Pass | Both records preserve Q3 and Q5 values and explicit conditioned-population explanations, rather than only a generic progress label |
| Assistance and exposure reconciled | Pass, with self-report limit | Pass, with self-report limit | Baseline explicitly qualifies Q3 as guided; V2 records prior Q1/Q3 teaching and treats independence as reported rather than proof of no outside help |
| No exaggerated mastery | Pass | Pass | Both keep C1 Improving and C2/C3 Needs practice; neither calls all three mastered or counts unanswered follow-ups as successes |
| Closing save and usable next step | Pass at snapshot level | Pass at snapshot level | Final snapshots include all five attempts and a concrete C2/C3 review followed by a C1 recheck; responses 06 confirm a saved handoff |

### Assistance difference that must remain visible

Baseline [response-01.md](runs/pair-1-baseline/response-01.md), line 17, explicitly asks which of Q3's 20 students and 12 residents belongs in the denominator. The scripted Q3 submission later says it was completed without a question-specific hint. Baseline [response-03.md](runs/pair-1-baseline/response-03.md), line 13, catches that conflict and calls the success a guided recheck. Its [final record](runs/pair-1-baseline/learning-record-after-06.md), lines 22 and 38, preserves the student's claim together with the qualification. This is the appropriate interpretation of the actual feedback history.

V2 [response-01.md](runs/pair-1-v2/response-01.md), line 18, instead asks whether increasing the total number of students while commuter counts stay fixed changes Q1's fraction. It does not cue Q3's specific data. V2 [response-03.md](runs/pair-1-v2/response-03.md), line 14, explicitly ties the correct Q3 answer to earlier Q1 instruction. Its [final record](runs/pair-1-v2/learning-record-after-06.md), lines 22 and 24, retains exposure to prior explanations. Q3/Q5 are treated as same-structure improvement, not established distinct transfer.

Neither arm observes outside assistance, and the packet itself contains instructor keys. The supplied student self-reports are not independent proof of unaided work. Baseline's Q5 phrase "independent application" is grounded in the reported lack of a Q5-specific hint and the observed tutor history; it should not be quoted as externally verified independence. It does not lead to an inflated progress label in this run.

### Persistence and handoff

Both final records preserve all five attempts with corrective rules. Baseline [response-06.md](runs/pair-1-baseline/response-06.md), lines 7-15, and final record lines 36-43 identify where to resume, preserve Q3's earlier cue, and leave unanswered transfer checks unscored. V2 [response-06.md](runs/pair-1-v2/response-06.md), lines 5-13, and final record lines 36-43 explicitly state that all five solutions have been exposed and the follow-up prompts remain unanswered. Both provide a source locator and practical next step without requiring the full old chat.

The snapshot review establishes that closing state exists in the captured final files; the execution trace remains the source for verifying the record helper's commit success, conflict checks, and timing. This review does not establish crash safety for interim unsaved evidence.

### Minor presentation issue

Baseline responses 02-06 contain repeated opening markers and tool-progress preambles in the saved response text. Several responses in both arms place a progress sentence before the standalone marker. These are presentation differences rather than grading or evidence-loss failures, but they mean the outputs are not perfectly controlled for response form or length. Actual generated content length should accompany efficiency metrics.

## Pair 2

### Outcome

Both arms correctly review all five submitted answers and preserve all three mistakes, both later correct applications, their reasoning, and the prior teaching context. Both closing records contain usable continuation steps and note that displayed solutions are not new student attempts. V2 has one material progress-calibration concern: it promotes C1 to Demonstrated based on two same-structure denominator calculations with changed labels and numbers. Baseline keeps C1 Improving and requests a changed-demand check.

| Gate | Baseline | V2 | Evidence |
|---|---|---|---|
| Five answers correctly reviewed | Pass | Pass | Responses 01-05 match S1-S3 and keys Q1=25%, Q2=8 rows, Q3=25%, Q4=6 rows, Q5=25% |
| Three errors and original reasoning retained | Pass | Pass | Both final records, Attempt history, lines 20-24 |
| Both correct applications retained | Pass | Pass | Both records preserve the actual Q3/Q5 values, reference populations, and explanations |
| Assistance and exposure preserved | Pass, self-report limited | Pass, self-report limited | Q3/Q5 say no question-specific hint was reported and retain earlier teaching; neither Q1 response exposes Q3-specific data |
| Conservative progress calibration | Pass | Concern / reviewer-assessed overpromotion | Baseline C1 stays Improving; V2 response 05 and final record promote C1 to Demonstrated without a stronger transfer task |
| Closing save and usable next step | Pass at snapshot level | Pass at snapshot level | Final snapshots retain all five reviews and practical C2/C3 next tasks; closing responses identify a saved handoff |

### Progress-calibration concern

V2 [response-05.md](runs/pair-2-v2/response-05.md), line 16, treats the resident and workplace settings as sufficient to mark C1 Demonstrated. The [final record](runs/pair-2-v2/learning-record-after-06.md), line 13, repeats that label, and line 24 calls Q5 a transfer. Yet line 22 explicitly describes Q3 as a same-structure application. Q3 and Q5 both ask the student to take the stated subgroup numerator over the explicitly named reference-group denominator; both answers are 25%. Only the population labels and counts change.

The frozen [state rules](skills/v2/references/state.md), line 84, require two distinct contexts including a transfer task for Demonstrated. Frozen [practice guidance](skills/v2/references/practice-and-feedback.md), line 28, says that new names alone do not create transfer, while line 38 distinguishes execution practice from changed-context or changed-demand transfer. Under a conservative reading of those rules, this test supplies repeated same-structure success but not a sufficiently discriminating transfer check. The reviewer therefore flags V2's promotion as too strong for the evidence. This is a qualitative adjudication, not a mathematical grading failure or proof that the learner lacks understanding.

V2 does explicitly limit the Demonstrated label as "not mastery" and recommends a later recheck. That qualification narrows the concern but does not remove the gap between the evidence and the operational status. Baseline [response-05.md](runs/pair-2-baseline/response-05.md), line 15, and [final record](runs/pair-2-baseline/learning-record-after-06.md), lines 13 and 40, retain Improving and state that changed-demand transfer remains unchecked.

### Assistance and handoff

Neither arm's first response explicitly prompts Q3's residents/12-versus-20 denominator choice, unlike pair-1 baseline. Both Q3 records preserve earlier Q1 teaching, and both Q5 records preserve the student's reported lack of question-specific hints and earlier feedback. Independence remains self-reported; unseen help and access to the packet keys were not independently established.

Baseline's final record lines 36-41 retain original reasoning, pending checks, source scope, and a C2/C3-first continuation plan. V2's final record lines 36-41 explicitly state that all five instructor answers were exposed, no new attempts occurred at close, and optional follow-ups remain unanswered. Both preserve a workable next session. This review uses `learning-record-after-06.md` as the final-state source, not the `final-study` collection mirror.

## Overall narrow quality result

Across four completed six-turn arm sessions, all 20 submitted question reviews were mathematically and conceptually correct under the synthetic packet. All four final records retained the three original error mechanisms and both correct applications with useful reasoning, assistance context, and next steps. No recorded evidence was found missing solely because V2 deferred saving. This supports narrow evidence preservation in these captured completed sessions, not crash safety or equal teaching quality in general.

For progress calibration, both baseline sessions and the first V2 session remained conservative. The second V2 session received one reviewer-assessed overpromotion concern. Thus the complete quality-gate set is not an unqualified pass for V2: lower resource usage, if observed, must be reported together with this calibration limitation rather than described as an entirely quality-neutral improvement.

Responses differ in follow-up choice, wording, formatting, and potentially length. Pair-1 baseline supplied a question-specific Q3 cue and then honestly recorded that cue; no matching cue appears in the other sessions. Two paired synthetic sessions from one packet, one model/configuration, and one reviewer cannot establish general tutoring reliability, humanities performance, retention, or real learner gains. No token or timing summaries were consulted for this quality adjudication.

