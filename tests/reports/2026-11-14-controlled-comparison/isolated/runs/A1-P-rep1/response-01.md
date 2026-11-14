I’ll look through the course materials, then explain loop tracing using the examples and conventions from your class.

Loop tracing means **following a loop one step at a time**, recording what it reads and what changes.

Your [course notes](materials/notes.md) recommend tracking:

1. The current index.
2. The values read or compared.
3. Each state change, in order.

For example, suppose this loop makes one pass through a list:

```python
values = [4, 1, 7, 3]

for i in range(len(values) - 1):
    if values[i] > values[i + 1]:
        print("out of order")
```

Trace each iteration:

| Index `i` | Values compared | Is left > right? | Output |
|---|---|---|---|
| 0 | 4 and 1 | Yes | `out of order` |
| 1 | 1 and 7 | No | — |
| 2 | 7 and 3 | Yes | `out of order` |

The loop prints twice, but makes **3 element-to-element comparisons**. A comparison counts whether its result is true or false. This code never changes the list.

For Quiz 4, **count only element-to-element comparisons**. Exclude assignments, index updates, and loop-condition checks.

A complete left-to-right pass comparing every adjacent pair in a nonempty list of length \(n\) makes \(n-1\) comparisons. The last element has no next neighbor.

Try practice Q2: a pass compares every adjacent pair in `[8, 2, 5, 6, 1, 4]`. How many comparisons occur? State what you counted.