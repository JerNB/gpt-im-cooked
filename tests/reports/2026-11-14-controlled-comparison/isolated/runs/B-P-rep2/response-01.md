I’ll read the study skill and course materials, then start with loop tracing using your course’s examples.

**Hi student, let's get you uncooked.**

I’m using your study skill; that greeting is its session marker. I’ll track useful learning evidence and normally save after five turns with meaningful changes; until then, recent progress stays in this chat.

**Loop tracing means following a loop one step at a time**, recording the current index, values read, and state changes in order. Your notes emphasize following the actual operations rather than guessing from variable names. ([Notes §2.1](materials/notes.md))

Consider this example applying your notes: move left to right through `[4, 1, 3, 2]`, comparing each neighboring pair. Each time, ask whether the left value is greater than the right value.

| Step | Positions compared | Values read | Result | Comparisons so far |
|---|---|---|---|---|
| 1 | First and second | 4 and 1 | True | 1 |
| 2 | Second and third | 1 and 3 | False | 2 |
| 3 | Third and fourth | 3 and 2 | True | 3 |

The false result still counts as a comparison: you performed the check either way. This example only compares values, so the list stays unchanged.

There are **three comparisons** because four elements have three neighboring pairs. In general, one pass comparing every adjacent pair makes **`n − 1` comparisons for `n ≥ 1`**. That rule applies to this particular loop pattern. ([Notes §2.2](materials/notes.md))

For Quiz 4, report **element-to-element comparisons only**. Exclude assignments, index updates, and loop-condition checks. A complete answer here would be: “3 element-to-element comparisons, counting the three adjacent-pair checks.” ([Outline, Reporting rule](materials/outline.md))

The tracing habit to remember is: **read the current values → perform the operation → record any change → advance.**

Quick check: if the list had **five elements**, how many adjacent-pair comparisons would this same pass make, and why?