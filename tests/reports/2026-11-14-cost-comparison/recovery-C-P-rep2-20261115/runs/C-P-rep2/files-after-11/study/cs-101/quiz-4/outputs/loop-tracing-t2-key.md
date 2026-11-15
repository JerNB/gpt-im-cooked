# Loop tracing T2 — separate key

Original course-based question. Sources: materials/notes.md §§2.1–2.3; materials/outline.md Reporting rule.
Target: Trace mutations in order and distinguish successful conditions, assignments, and all element comparisons. Transfer changes the task from single-pass pair counting to tracing a mutating list with a counter.

Question code:
```python
a = [2, 1, 3, 0]
changes = 0
for i in range(len(a) - 1):
    if a[i] > a[i + 1]:
        a[i + 1] = a[i]
        changes = changes + 1
```
Prompt: Give final a, final changes, and runtime count under the course convention; show values compared each iteration and state counted/excluded operations.

Answer evidence: Verified computation using local Python; assertions passed. Trace below is execution output.

Trace (i, left, right, result, list afterward, changes):
(0, 2, 1, True, [2, 2, 3, 0], 1)
(1, 2, 3, False, [2, 2, 3, 0], 1)
(2, 3, 0, True, [2, 2, 3, 3], 2)

Final a=[2,2,3,3]; changes=2; runtime count=3 element-to-element comparisons. Count every evaluation of a[i] > a[i+1], including false results; exclude list/counter assignments, index updates, and loop-condition checks. Check explanation as well as totals. No student attempt yet.
