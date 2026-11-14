I’ll read the progress file and course materials to find where you left off and continue from there.

Welcome back. Your progress file says you demonstrated adjacent-pair comparison counting, but tracing actual state changes remains untested. Next is **P1: list aliasing**, followed by group summaries. Big-O is in scope, but the supplied files still lack its lecture notes.

From Notes §1: a list variable refers to a list object. With `b = a`, both names refer to the same list, so a mutation through either name is visible through the other. Using `a.copy()` creates a new outer list, though nested lists may still be shared.

Before we move on, try this check based on those rules:

```python
a = [4, 1, 7]
b = a
b[0] = 9
```

What are `a` and `b` afterward, and why?