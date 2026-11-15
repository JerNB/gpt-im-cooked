I’ll read the study skill and local progress notes to find where you left off.

**Hi student, let's get you uncooked.**

Welcome back. Your saved next step is **list aliasing**. You previously demonstrated loop tracing; a later recheck is still due. Big-O remains in scope, but its teaching notes are missing.

A list variable refers to a list object. With `b = a`, both names refer to **the same list**, so changing it through either name is visible through the other. ([Notes §1.1–1.2](materials/notes.md))

For example:

```python
a = [2, 4]
b = a
b[0] = 9
```

Both `a` and `b` now show `[9, 4]`. The assignment `b = a` gave the existing list another name.

By comparison, `b = a.copy()` creates a **new outer list**. Its nested lists can still be shared, which is the key detail in a *shallow copy*. ([Notes §1.3](materials/notes.md))

```python
a = [[2], [4]]
b = a.copy()
b[0][0] = 9
```

Here, `a` also becomes `[[9], [4]]`: the outer lists are separate, but their first elements refer to the same inner list.

Try this short check:

```python
x = [[3], [6]]
y = x
z = x.copy()

y[1][0] = 8
```

What do `x`, `y`, and `z` contain afterward? Explain which lists are shared.