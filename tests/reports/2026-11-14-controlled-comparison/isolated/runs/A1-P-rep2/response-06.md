Trace this code:

```python
values = [6, 2, 5, 1]
count = 0

for i in range(len(values) - 1):
    if values[i] > values[i + 1]:
        count += 1
```

**What is the final value of `count`, and how many comparisons should you report under the course’s runtime convention? State which operations you counted.**