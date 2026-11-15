I’ll read the study skill and local progress notes, then continue from where you left off.

**Hi student, let's get you uncooked.**

We left off preparing for **CS 101 Quiz 4**. You demonstrated loop tracing, with a later unaided recheck still due. Next was **list aliasing**.

A list variable refers to a list object. With `b = a`, both names refer to the **same list**, so changing an element through either name affects what both names see. ([Notes §1.1–1.2](materials/notes.md))

```python
a = [4, 7]
b = a
b[0] = 9
```

Here, both `a` and `b` show `[9, 7]`: the assignment gave the existing list another name.

With `b = a.copy()`, Python creates a new **outer list**. Nested lists inside it can still be shared. That distinction is what “shallow copy” means in your notes. ([Notes §1.3](materials/notes.md))

Try this fresh check:

```python
a = [[4], [7]]
b = a.copy()
b[0][0] = 9
```

**What do `a` and `b` contain afterward, and why?** Explain which list was copied and which list was changed.