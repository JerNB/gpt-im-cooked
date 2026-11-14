Trace this loop:

```python
values = [3, 1, 2]
count = 0

for i in range(len(values) - 1):
    if values[i] > values[i + 1]:
        count = count + 1
```

What is the final value of `count`, and what runtime count should you report under your course’s convention? State which operations you counted and excluded.