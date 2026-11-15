Recursion is when **a function calls itself to solve a smaller version of a problem**.

Your current Quiz 4 outline says recursion has moved to Unit 5 and is **not on Quiz 4**, but here’s a quick explanation.

```python
def countdown(n):
    if n == 0:          # Base case: stop
        return
    print(n)
    countdown(n - 1)    # Recursive call: smaller problem
```

Calling `countdown(3)` prints:

```text
3
2
1
```

Each call has its own value of `n`: first 3, then 2, then 1, then 0. At 0, the function returns without making another call. The earlier calls then finish.

Recursion needs two things:

- **A base case:** a condition that stops the calls.
- **Progress toward that case:** here, subtracting 1 each time.

Without a reachable base case, the calls keep going until Python raises an error.