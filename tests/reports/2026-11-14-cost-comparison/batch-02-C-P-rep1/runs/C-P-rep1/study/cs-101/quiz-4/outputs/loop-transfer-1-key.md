# Loop transfer 1 — separate solution

- Topic: P2; original synthetic practice.
- Sources: materials/notes.md sections 2.1-2.3; materials/outline.md Reporting rule.
- Target: Trace changes across two passes and distinguish element comparisons from loop-condition checks. Changed demand: repeated pass over updated state rather than one-pass n-1 recall.
- Task: Start a=[3,1,2]. Perform two passes; each visits i=0 then i=1, compares a[i] > a[i+1], and swaps those entries when true. Report final list, counted comparisons, and excluded operations.
- Answer evidence: Verified computation using a controlled Python snippet locally.
- Final list: [1,2,3]. Count: 4 element-to-element comparisons, including false comparisons. Exclude assignments, swaps as assignments, index/pass updates, loop-condition checks.
- Trace (pass, index, left, right, swapped, list afterward):
(1, 0, 3, 1, True, [1, 3, 2])
(1, 1, 3, 2, True, [1, 2, 3])
(2, 0, 1, 2, False, [1, 2, 3])
(2, 1, 2, 3, False, [1, 2, 3])
