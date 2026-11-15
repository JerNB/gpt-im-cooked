I’ll read the study skill and local course records to find where you left off.

**Hi student, let's get you uncooked.**

We left off in **CS 101 Quiz 4** after your correct two-pass loop trace. Your record has loop tracing marked Demonstrated, with a later recheck due. Next was **list aliasing**, followed by nested data summaries.

Aliasing means **two variable names refer to the same list**. Your [notes §1.1–1.2](materials/notes.md) explain that assigning a list to another variable does not make a copy:

```python
a = [4, 1, 7]
b = a
b[0] = 9
```

Both `a` and `b` now show `[9, 1, 7]`. There is one list: `b[0] = 9` changes that shared object, so the change is visible through either name.

A shallow copy creates a separate **outer** list:

```python
a = [4, 1, 7]
b = a.copy()
b[0] = 9
```

Here, `a` remains `[4, 1, 7]`, while `b` becomes `[9, 1, 7]`. But nested mutable lists can still be shared between a list and its shallow copy. ([Notes §1.3](materials/notes.md))

The useful question is: **Which list object does each name refer to?**

In your own words, why did changing `b[0]` also change what `a` showed in the first example?