# Independent synthetic-study quality review

A read-only Codex reviewer inspected supplied materials, prompts, responses, record snapshots, resource-free command evidence, and captured recovery artifacts **without consulting token/time summaries or usage/accounting JSONL**. This is agent adjudication, not an external educator assessment, blinded human trial, or learner-outcome measurement.

## Original batch

The complete first pair's six Q1/Q3/Q5 feedback events were correct. Both arms retain all 100 historical attempt rows and the three new attempts with original reasoning, keep C1 Improving, and leave C2/C3 Unassessed. The original candidate explicitly records its earlier Q3 denominator-identification prompt rather than treating the later answer as independent transfer. Final handoffs contain sources, exposed-answer context and next actions.

The reviewer checked the first pair's authored questions/keys in successful command evidence and corroborated recorded standard-library calculations and Playwright runs. Their five-item papers cover S1-S3 and use mixed formats. However, exact original generated files were lost by end-only capture when the later batch failed. The six **Artifact NOT RETAINED** HTML notices are not tested papers; original artifact conclusions are source/execution-evidence review, not an independent rerun of retained original bytes. See [failure and recovery](FAILURE-AND-RECOVERY.md).

The remaining original pair's six feedback events were also reviewed and correct, bringing total reviewed feedback coverage to **18 events**: 12 original and six recovery. Original pair-2 candidate authoring commands support five correct keys as well, but that is source/execution evidence only. Final-file academic review covers the **two actual recovery papers and their ten keys**, not capture-loss notices. An independent integrity check confirms all **23 captured record snapshots** retain their 100 original historical rows in order, and all six study contexts keep one continued-session identity; see [integrity-checks.json](integrity-checks.json).

## Recovery pair: actual retained files

| Gate | Baseline | Candidate |
|---|---|---|
| Q1/Q3/Q5 mathematical feedback and original reasoning | Pass | Pass |
| All 100 original historical rows retained | Pass | Pass |
| Actual final record equals fourth-turn snapshot | Pass | Pass |
| Conservative progress: C1 Improving; C2/C3 Unassessed | Pass | Pass |
| Five original, source-grounded questions across S1-S3 | Pass within this packet | Pass within this packet |
| Mixed formats and separate checked key | Pass | Pass |
| No embedded worked solutions/live scoring in worksheet | Pass in source inspection | Pass in source inspection |
| Independent parent browser/viewport checks | Pass in executed scope | Pass in executed scope |
| Fully matched teaching/assistance treatment | Not established | Minor retrieval-cue qualification |

Record evidence: baseline `model-recovery/runs/pair-1-baseline/learning-record-after-04.md`, lines 122-126 and 138-145; candidate equivalent, lines 121-123 and 135-142. All historical row contents match the initial fixture. Saved mock questions are not counted as student attempts or demonstrated transfer.

The baseline [actual key](model-recovery/runs/pair-1-baseline/final-study/mock-exam-key.html) was independently checked: Q1 B gives 6/16=37.5%; Q2 keeps 4/10=40% fixed while 4/30 changes to 4/40=10%; Q3 mutate returns nine rows; Q4 pipelines return six and two; Q5 joins contribute 6+2=8, with unmatched keys contributing zero.

The candidate [actual JSON](model-recovery/runs/pair-1-v2/final-study/outputs/course-mock-a-v1.0.json), lines 28-255, and [separate key](model-recovery/runs/pair-1-v2/final-study/outputs/course-mock-a-v1.0-key.html) were independently checked: Q1 B gives 10/16=62.5% rather than 10/40=25%; Q2 reverse conditions give 6/10=60% versus 6/15=40%; Q3 A,B,D are true; Q4 mutate returns 11 rows versus four for scalar summary; Q5 contributes K:4 plus M:3, seven pairs, with unmatched rows excluded. All choice alternatives and explanations were reviewed.

Both papers include a changed-condition task and multi-key/unmatched-row joins, beyond changing names/numbers alone. Routine recognition items still provide ordinary rule practice, not strong transfer evidence by themselves. Generating these tasks does not establish student performance.

## Assistance qualification

Candidate recovery `response-01.md:19` asks the student to look at Q3 and identify its denominator. The final Q3 row retains prior teaching but does not explicitly name that general retrieval cue. It supplies no numeric answer, and the record correctly avoids a transfer/Demonstrated claim. Nevertheless, the arms are not identical teaching treatments; later success should retain the self-report/exposure limitation. Do not advertise the comparison as fully equivalent-quality unaided performance.

## Recovered execution failures

Baseline recovery `command-evidence.json` records three nonzero batches:

1. A post-write content-equality assertion failed because of newline handling after the helper had successfully committed.
2. A next-action replacement missed its target and was caught by assertion; the following command corrected the pointer and verified it.
3. A key-page horizontal-overflow assertion failed; the tutor added fixed-layout/wrapping CSS and reran both pages at 1280px and 375px successfully.

These retries remain in resource measurements. Final evidence shows no resulting record loss or mathematical error. The candidate recovery has zero nonzero command batches. This small observation is not a general failure-rate estimate or proof that one mechanism caused the difference.

## Browser evidence and limits

The parent independently executed 26 checks on the two actual retained worksheets and four key-page viewport checks, with Chromium 148.0.7778.96. Results and screenshots are recorded in [VERIFICATION.md](VERIFICATION.md). Candidate key/retry exposure is exercised; baseline uses explicit self-reported assistance. Candidate's initial final reply honestly said its browser had not been tested; the later independent checks do not retroactively turn that earlier statement into a claim of author execution.

No real learners, knowledge retention, cross-chat recovery, physical phones, full accessibility, plugin discovery, or print rendering were evaluated. Passing this narrow review does not establish quality-neutral savings across other workloads.
