I’ll read the study skill and course materials, then explain loop tracing using your course’s examples and notation.

**Hi student, let's get you uncooked.**

I’m using your study skill for CS 101 Quiz 4. That opening line is the skill’s welcome marker.

**Loop tracing means following code step by step and writing down what actually happens.** Your notes say to record the current index, the values read, and each state change in order. ([Notes §2.1](materials/notes.md))

Here’s a new worked example applying those rules. This code moves through adjacent pairs and swaps them when the left value is larger:

```python
a = [4, 1, 3]

for i in range(len(a) - 1):
    if a[i] > a[i + 1]:
        a[i], a[i + 1] = a[i + 1], a[i]
```

The last line exchanges the two values. The list has three elements, so this loop visits indices `i = 0` and `i = 1`.

| Step | Index `i` | Values compared | Result | List afterward |
|---|---:|---|---|---|
| Start | — | — | — | `[4, 1, 3]` |
| First iteration | 0 | `4 > 1` | True → swap | `[1, 4, 3]` |
| Second iteration | 1 | `4 > 3` | True → swap | `[1, 3, 4]` |

The crucial detail is the second row of work: **the second comparison uses the updated list.** After the first swap, `a[1]` is `4`, so the next comparison is `4 > 3`.

For Quiz 4, report **2 element-to-element comparisons**: the two evaluations of `a[i] > a[i + 1]`. Your course excludes assignments, index updates, and loop-condition checks from that count. ([Notes §2.3](materials/notes.md), [Outline: Reporting rule](materials/outline.md))

For one pass comparing every adjacent pair, a list of length `n ≥ 1` has `n − 1` comparisons. That rule applies to this particular loop pattern. ([Notes §2.2](materials/notes.md))

Your tracing cue: **index → current values → comparison → state change → repeat.**

To check the key idea: in the example, why does the second comparison read `4` as its left value?

As we continue, I’ll retain meaningful learning evidence; saves normally happen after five change-bearing turns or earlier checkpoints. Recent unsaved evidence stays in this chat.