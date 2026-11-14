# Runtime convention transfer check — separate key

Original synthetic practice; topic P2.

Question: A pass through [4, 1, 7, 3] compares each adjacent pair once. After the pass, it compares the first and last elements once more. The procedure also performs assignments, index updates, and loop-condition checks. Under the Quiz 4 convention, how many comparisons should be reported? Explain what is included and excluded.

Scope/style basis: materials/notes.md §2.1–§2.3; materials/outline.md, Reporting rule; materials/practice.md Q1–Q4.

Personal target: distinguish counting actual element-to-element comparisons from applying n−1 to an entire procedure automatically. Prior reviewed evidence: Q1 counted elements instead of pairs; Q3 and Q4 correct on the same adjacent-pair pattern. This task adds a comparison outside that pattern.

Answer evidence: Reasoned solution; manual derivation, no code execution needed or performed.

Solution: 4 element-to-element comparisons. The adjacent pairs are (4, 1), (1, 7), and (7, 3), giving 3. The additional first-to-last comparison (4, 3) adds 1. Exclude assignments, index updates, and loop-condition checks. The n−1 rule counts the adjacent-pair pass, not the additional comparison.

Review criteria: correct total, explicit inclusion of the extra comparison, and exclusion of the non-element operations. No hint or solution has been delivered with the question. Evaluate assistance from the student's subsequent response and any intervening help.
