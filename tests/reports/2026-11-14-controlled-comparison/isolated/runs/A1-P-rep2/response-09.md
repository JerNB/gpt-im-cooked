**Recursion is when a function calls itself to solve a smaller version of the same problem.** It needs:

- A **base case** that returns an answer without another recursive call.
- A **recursive step** that moves closer to the base case.

For example:

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

For `factorial(3)`, the calls build up:

```text
factorial(3) → 3 * factorial(2)
factorial(2) → 2 * factorial(1)
factorial(1) → 1 * factorial(0)
factorial(0) → 1                 ← base case
```

Then the answers return backward: `1`, `1`, `2`, and finally **6**. Each waiting call finishes once the smaller call returns.

Without a reachable base case, the calls keep building until Python raises a recursion error.

For your study priorities, the current outline explicitly says **recursion is not on Quiz 4; it moved to Unit 5**, even though you encountered it on your last quiz.