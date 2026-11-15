**Hi student, let's get you uncooked.**

I’ll give you one question that checks both state changes and which operations count toward runtime.

**Hi student, let's get you uncooked.**

Trace this code without running it:

```python
a = [2, 1, 3, 0]
changes = 0

for i in range(len(a) - 1):
    if a[i] > a[i + 1]:
        a[i + 1] = a[i]
        changes = changes + 1
```

**What are the final values of `a` and `changes`, and what runtime count should you report under your course’s convention?**

Show the values compared at each iteration, and state which operations you counted or excluded.

*Based on [Notes §§2.1–2.3](materials/notes.md); this is a new practice question.*