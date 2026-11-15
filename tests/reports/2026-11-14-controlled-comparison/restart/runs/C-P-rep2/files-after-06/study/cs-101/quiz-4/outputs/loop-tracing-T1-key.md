# Loop tracing transfer check T1 - separate solution

## Question identity

T1: values=[3,1,2], hits=0; two full passes; each pass compares every adjacent pair using > and increments hits only when true. Student must report the course runtime comparison count and identify what is counted/excluded.

## Blueprint

- Topic: P2 loop tracing and runtime convention.
- Sources: materials/notes.md sections 2.1-2.3; materials/outline.md Reporting rule.
- Authorship: Original synthetic practice; not an instructor question.
- Personal target: Separate total comparisons from successful tests and from list length; apply the convention across two passes after Q3/Q4 same-structure success.
- Changed demand: Two passes and a conditional counter; n-1 describes each pass, not the total.

## Checked solution

4 element-to-element comparisons: each pass compares (3,1) and (1,2), so 2 passes times 2 comparisons = 4. Both true and false comparisons count. hits ends at 2 because only 3>1 succeeds in each pass; hits is not the runtime count. Assignments, index updates, loop-condition checks and printing are excluded under the course convention. The list does not change.

## Evidence

Verified computation: controlled Python instrumentation executed locally; comparisons=4, hits=2. Instrumentation is not part of the displayed question. Trace (pass_number, i, result, hits):
[(0, 0, True, 1), (0, 1, False, 1), (1, 0, True, 2), (1, 1, False, 2)]
