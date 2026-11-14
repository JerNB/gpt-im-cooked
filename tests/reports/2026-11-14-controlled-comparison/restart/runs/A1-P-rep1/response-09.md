**Recursion is when a function calls itself to solve a smaller version of a problem.**

Your current outline says recursion is **not on Quiz 4—it moved to Unit 5**. We can still review it.

A recursive function needs:

- A **base case** that returns without another recursive call.
- A **recursive step** that moves toward the base case.

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

For `factorial(3)`, the calls go down to the base case:

```text
factorial(3) → 3 * factorial(2)
factorial(2) → 2 * factorial(1)
factorial(1) → 1 * factorial(0)
factorial(0) → 1
```

Then the pending multiplications finish:

```text
factorial(1) returns 1
factorial(2) returns 2
factorial(3) returns 6
```

Each call waits for the smaller call’s result. Without a reachable base case, the calls keep piling up until Python raises an error.

Quick check: what is the base case here, and how does each recursive call move toward it?