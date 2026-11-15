**Hi student, let's get you uncooked.**

I’ll use a new example with repeated passes to check whether you can distinguish the program’s counter from the course’s comparison count.

**Hi student, let's get you uncooked.**

Consider this code:

```python
values = [3, 1, 2]
hits = 0

for pass_number in range(2):
    for i in range(len(values) - 1):
        if values[i] > values[i + 1]:
            hits += 1

print(hits)
```

**What runtime comparison count should you report under your course’s convention?** Explain what you counted and excluded, and whether the printed value necessarily equals that count.

Use [Notes §2.1–§2.3](materials/notes.md).