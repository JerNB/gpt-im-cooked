Trace this code:

```python
a = [4, 1, 3]
for i in range(len(a) - 1):
    if a[i] > a[i + 1]:
        a[i], a[i + 1] = a[i + 1], a[i]
```

What is the list after each iteration, and how many comparisons should you report under your course’s runtime convention? State which operations you counted and excluded.