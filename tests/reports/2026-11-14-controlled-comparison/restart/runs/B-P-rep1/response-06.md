**Hi student, let's get you uncooked.**

I’ll give you one trace where values change during the pass, so you’ll need to track both the changes and the comparisons. I’ll keep the solution separate.

**Hi student, let's get you uncooked.**

Trace this pass. Indices start at **0**, and a swap immediately changes the list.

```text
values = [4, 1, 3]
changes = 0

For i = 0, then i = 1:
    If values[i] > values[i + 1]:
        Swap those two elements
        Increase changes by 1
```

**What are the final list, the final value of `changes`, and the runtime count under your course’s convention?** Show the two values compared at each step, and state which operations you counted and excluded.

This applies your course’s rules for tracking state changes and counting only element-to-element comparisons. ([Notes §§2.1–2.3](materials/notes.md))