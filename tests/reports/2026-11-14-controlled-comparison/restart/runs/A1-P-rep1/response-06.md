Trace this code:

```python
values = [4, 1, 3, 2]
swaps = 0

for i in range(len(values) - 1):
    if values[i] > values[i + 1]:
        values[i], values[i + 1] = values[i + 1], values[i]
        swaps += 1
```

What are the final values of `values` and `swaps`, and what runtime count should you report under the course convention? Show the list after each iteration and state which operations you counted.