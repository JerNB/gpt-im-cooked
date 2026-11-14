# Loop-tracing transfer check: separate solution

- Item ID: P2-transfer-early-stop-1
- Authorship: Original synthetic question.
- Scope basis: materials/notes.md sections 2.1-2.3; materials/outline.md Reporting rule.
- Target: Decide whether n-1 applies when an adjacent-pair pass stops early; exclude assignments, index updates, and loop-condition checks.
- Question: A loop scans [1, 4, 2, 7, 9] from left to right, comparing adjacent elements. It stops immediately when the left element is greater than the right element. Otherwise it moves to the next adjacent pair. During execution it also performs assignments, index updates, and loop-condition checks. What comparison count should be reported under the course convention? Identify the pairs compared and explain whether n-1 applies.
- Answer evidence: Reasoned solution; manual trace, not executed. No instructor key for this original item.
- Checked trace: 1 > 4 is false; move to next adjacent pair. 4 > 2 is true; stop immediately. No later adjacent pairs are compared.
- Answer: 2 element-to-element comparisons. Exclude assignments, index updates, and loop-condition checks. The n-1 rule would give 4 for a complete adjacent-pair pass over five elements, but this pass stops early.
- Evaluation: Require the count 2, the pairs (1,4) and (4,2), and a distinction between actual early stopping and a complete pass. Do not infer broad mastery from this item alone; combine with reviewed prior evidence and plan a later unaided recheck.
