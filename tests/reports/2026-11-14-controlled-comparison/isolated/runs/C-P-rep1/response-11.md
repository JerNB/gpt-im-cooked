I’ll read the study skill and local progress records to find where you left off.

**Hi student, let's get you uncooked.**

You left off after correctly handling full-pass and early-stop comparison counts. Your saved next step was **list aliasing**, so let’s continue there.

A list variable refers to a list object. With `b = a`, both names refer to **the same list**, so changing an element through either name is visible through both. ([Notes §1.1–1.2](materials/notes.md))

```python
a = [2, 5]
b = a
b[0] = 9
```

Both `a` and `b` now show `[9, 5]`: there is one list with two names.

By comparison, `b = a.copy()` creates a separate outer list. Replacing an element in that copy leaves the original outer list unchanged. It’s a **shallow** copy: nested mutable lists can still be shared. ([Notes §1.3](materials/notes.md))

Try this short application:

```python
x = [3, 8]
y = x
z = x.copy()
y[0] = 6
```

What are the final values of `x`, `y`, and `z`? Explain which names share a list.