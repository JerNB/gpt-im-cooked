# Loop transfer 1 - attempt 1

Date: 2026-11-14

## Original student response

The final list is [1, 2, 3], with 4 element-to-element comparisons. First pass: compare 3 > 1 (true), swap to [1, 3, 2]; then compare 3 > 2 (true), swap to [1, 2, 3]. Second pass starts with that list: compare 1 > 2 (false), then 2 > 3 (false), so no further swaps. Each of the two passes makes two adjacent-element comparisons. I exclude assignments, the assignments involved in swaps, index updates, and loop-condition checks from the reported comparison count.

## Tutor feedback

Correct final state, all four traced comparisons and truth values, and counting exclusions. False element-to-element comparisons still count. Checked against loop-transfer-1-key.md (Verified computation) and materials/notes.md sections 2.1-2.3.

Assistance: No task-specific hint or solution shown in conversation before submission; prior general worked example and Q1-Q4 teaching/feedback available. No claim about outside help. This is an unaided-in-chat changed-demand transfer: two passes over updated state, rather than one-pass adjacent-pair counting.

P2 Demonstrated based on Q3/Q4 plus this transfer; all evidence is same-session. Recheck before exam using a later unaided trace after another topic or in a later session. This does not establish skill with arbitrary loops or Big-O.
