# CS 101 Quiz 4 progress

- Source: materials/outline.md (current), materials/notes.md, materials/practice.md.
- Preferences: course files only; learner attempts practice before answers; check understanding after explanations; assess learning cautiously.
- Current focus: P2 loop tracing and element-to-element comparison counts (Notes §2).
- Introduced: record index, values read, and state changes in order; adjacent-pair pass has n−1 comparisons for n >= 1; exclude assignments, index updates, and loop-condition checks.
- Next: learner attempts Practice B Q1, naming the compared pairs and comparison count. No practice answers supplied.
- Evidence: no learner attempts yet; understanding and independent tracing remain unassessed.
- Remaining quiz topics: P1 aliasing, P3 Big-O, P4 nested data summaries. Big-O is in scope but lecture notes are not posted. Recursion is excluded.

## Practice Q1 attempt
- Learner answered 4 comparisons because there are 4 elements.
- Correction: adjacent pairs are (4, 1), (1, 7), (7, 3), giving 3 element-to-element comparisons. Count gaps between neighbors, not elements.
- Understanding: initial confusion between element count and comparison count; correction needs a follow-up attempt. No mastery established.
- Next: ask learner to attempt Practice Q2 and state which operations were counted; answer not supplied.

## Practice Q2 answer requested
- Learner explicitly requested the answer without attempting Q2.
- Supplied: 5 element-to-element comparisons for 6 elements (n−1); exclude assignments, index updates, and loop-condition checks.
- Evidence: Q2 was not independently solved; understanding remains unassessed after the Q1 correction.
- Next check: ask why the last element does not create a sixth adjacent-pair comparison.

## Practice Q3 independent attempt
- Learner answered 7 element-to-element comparisons: 8 elements have 7 adjacent pairs.
- Explicitly excluded assignments, index updates, and loop-condition checks; reported using no hint.
- Assessment: correct independent application of the adjacent-pair rule and reporting convention. One independent correct attempt supports progress, not mastery; tracing indices, values, and state changes is not yet demonstrated.
- Next check: Practice Q4, with adjacent pairs listed and comparison count stated; answer not supplied.
