I’ll use a short loop with two passes to check both state tracking and comparison counting. I’ll keep the solution in a separate file.

**Hi student, let's get you uncooked.**

Trace this code by hand. The last line swaps the two indicated elements.

```python
a = [3, 1, 2]

for pass_number in range(2):
    for i in range(len(a) - 1):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
```

**What is the final list, and how many element-to-element comparisons occur in total?** Explain which operation you counted and which operations you excluded.

This question applies [Notes §2.1–2.3](materials/notes.md) and the [quiz reporting rule](materials/outline.md).