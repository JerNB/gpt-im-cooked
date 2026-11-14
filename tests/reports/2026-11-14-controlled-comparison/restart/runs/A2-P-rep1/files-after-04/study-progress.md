# CS 101 Quiz 4 study progress

- Course source: materials/outline.md (current), materials/notes.md, materials/practice.md.
- Preferences: use course files only; let student attempt practice before giving answers; check understanding after explanations; assess learning cautiously.
- Current topic: P2 loop tracing and element-to-element comparison counts (Notes §2).
- Introduced: record index, values read, and state changes in order; one full adjacent-pair pass on n >= 1 elements makes n-1 comparisons; count only element-to-element comparisons.
- Understanding evidence: Q1 attempt was 4 comparisons because there are 4 elements. This counts elements instead of adjacent pairs; adjacent-pair counting is not yet demonstrated. Feedback: 3 comparisons, pairing (4,1), (1,7), (7,3).
- Next check: ask why the last element does not start another adjacent-pair comparison. Q1 answer explained after attempt; Q2-Q4 answers not revealed.
- Remaining scope: P1 list aliasing, P3 Big-O, P4 nested data summaries. Big-O is in scope but lecture notes are not posted; do not fill gaps with outside content. Recursion is excluded.

- Q2: student explicitly requested the answer without attempting. Answer provided: 5 element-to-element comparisons for 6 elements. This is not evidence of independent understanding. The Q1 follow-up remains unanswered.
- Q3: correct independent attempt (student reports no hint): 7 element-to-element comparisons because 8 elements have 7 adjacent pairs; correctly excluded assignments, index updates, and loop-condition checks. Evidence supports adjacent-pair counting on this example, not mastery of general loop tracing. Next check: Q4 independently; broader tracing of index/values/state changes remains unassessed.
