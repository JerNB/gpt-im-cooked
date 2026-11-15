I’ll read the study skill and local progress notes, then resume from where you left off.

**Hi student, let's get you uncooked.**

Your saved next step was **list aliasing**. You demonstrated comparison counting last time; we’ll recheck it before the quiz. Big-O still lacks teaching notes in your materials.

A list variable refers to a list object. With `b = a`, both names refer to **the same list**, so changing an element through either name is visible through both. ([Notes §1.1–1.2](materials/notes.md))

For example:

```python
a = [3, 8]
b = a
b[0] = 5
```

Now both `a` and `b` show `[5, 8]`: there is one list with two names referring to it.

With `b = a.copy()`, the outer list is new, but nested lists inside it may still be shared. ([Notes §1.3](materials/notes.md))

Try this application:

```python
a = [[2, 4], [6]]
b = a.copy()
b[0][1] = 9
```

What do `a` and `b` contain afterward, and why?