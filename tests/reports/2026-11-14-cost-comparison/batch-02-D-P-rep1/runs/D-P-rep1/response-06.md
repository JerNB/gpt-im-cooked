I’ll use a question with two passes and changing values to check how you apply the counting convention.

**Hi student, let's get you uncooked.**

This code makes two complete passes, swapping neighboring values when the left one is larger:

```python
values = [3, 1, 4, 2]

for pass_number in range(2):
    for i in range(len(values) - 1):
        if values[i] > values[i + 1]:
            values[i], values[i + 1] = values[i + 1], values[i]
```

**Under your course’s runtime convention, how many comparisons should you report for the entire code? Explain which operations you counted and excluded.**

Use the convention in [Notes §2.3](materials/notes.md).