I’ll read the study skill and the local course progress, then continue from where you left off.

**Hi student, let's get you uncooked.**

I’m using the study skill. Your saved record puts **list aliasing** next. You demonstrated loop tracing; an unaided recheck is still due before the quiz.

A list variable refers to a list object. With `b = a`, both names refer to **the same list**, so changing an element through either name is visible through both. With `b = a.copy()`, you get a new outer list, though nested lists may still be shared. ([Notes §§1.1–1.3](materials/notes.md))

For example:

```python
a = [2, 5]
b = a
a[1] = 8
```

Both `a` and `b` now show `[2, 8]`: the assignment gave one list two names.

Try this short application:

```python
a = [4, 7]
b = a
b[0] = 9
```

**What are `a` and `b` afterward, and why?**