I’ll check the course materials, then explain loop tracing using examples that match your class.

**Loop tracing means following a loop one step at a time**, recording the index, the values it reads, and any changes it makes. Your notes emphasize using the actual operations, rather than guessing from variable names.

For Quiz 4, **count only comparisons between list elements**. Don’t count assignments, index updates, or checks that decide whether the loop continues.

Here’s a loop that compares adjacent elements:

```python
a = [6, 2, 9]
for i in range(len(a) - 1):
    print(a[i] > a[i + 1])
```

Trace each iteration:

| `i` | Elements compared | Result |
|---|---|---|
| 0 | `6 > 2` | `True` |
| 1 | `2 > 9` | `False` |

It prints `True`, then `False`. The list stays unchanged because the code only compares and prints.

The reported count is **2 element-to-element comparisons**: one for each adjacent pair. A single pass through all adjacent pairs of a list with length `n ≥ 1` makes **`n − 1` comparisons**. Think of counting the gaps between neighboring elements.

Try practice **Q1**: A pass compares each adjacent pair in `[4, 1, 7, 3]`. Which pairs are compared, and how many element-to-element comparisons are there?