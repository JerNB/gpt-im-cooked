**Hi student, let's get you uncooked.**

I’ll give you one question that combines tracing a variable’s changes with deciding which operations count toward runtime.


**Hi student, let's get you uncooked.**

Trace this pseudocode. It visits `i = 0`, then `i = 1`.

```text
values = [3, 1, 2]
score = 0

for each i from 0 through 1:
    if values[i] > values[i + 1]:
        score = score + 2
    else:
        score = score + 1
```

**What is the final value of `score`, and what runtime count should you report under your course’s convention?** Show the two iterations and explain which operations you counted or excluded.

*Original practice based on Notes §2.1–2.3 and the outline’s Reporting rule.*