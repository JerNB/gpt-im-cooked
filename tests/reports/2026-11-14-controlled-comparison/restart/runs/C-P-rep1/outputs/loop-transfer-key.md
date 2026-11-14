# Loop tracing transfer check T1 — separate solution

- Course: CS 101 Quiz 4; topic P2.
- Authorship: Original synthetic practice, not an instructor question.
- Scope basis: materials/notes.md sections 2.1–2.3; materials/outline.md reporting rule.
- Personal target: Q1 counted elements; Q3 and Q4 correctly used n−1 for full adjacent-pair passes. Change the stopping condition to test whether the student checks the actual comparisons performed.
- Format: Trace and explain the reported runtime count.

## Question

A loop processes `[1, 4, 3, 2]` from left to right. At each step it compares the current element with its next neighbor, asking whether the left element is greater than the right. It stops immediately when that comparison is true; otherwise it moves to the next adjacent pair. It never changes the list.

Using the course runtime convention, how many comparisons should you report? Show the comparisons performed and explain whether 4−1 applies here.

## Checked solution

Answer evidence: Reasoned solution, manually traced; unexecuted. No instructor key for this original item.

1. Compare 1 > 4: false. Count 1; move to next pair.
2. Compare 4 > 3: true. Count 2; stop immediately.
3. The pair (3,2) is never compared.

Report 2 element-to-element comparisons. Both true and false element comparisons count. Exclude assignments, index updates, and loop-condition checks. The full-pass n−1 rule does not give this run's count because this run stops before comparing every adjacent pair.

Review count, actual pair trace, and counting convention separately. A correct independent explanation would provide changed-condition transfer evidence together with Q3. If this supports Demonstrated in the same session, record Recheck before exam and require a later unaided application.
