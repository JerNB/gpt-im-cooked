I’ll compare your recorded work with the current Quiz 4 outline, distinguishing what you’ve demonstrated from what we haven’t assessed.

**I don’t have enough evidence to say you’re ready for all of Quiz 4.** You’ve made progress on one part; three other topics remain unassessed.

| Quiz topic | What you’ve demonstrated | What remains |
|---|---|---|
| **List aliasing** | No attempts yet | List references, shared mutations, and shallow copies |
| **Loop tracing** | Correct Q3 and Q4 counts; correct comparison convention and pair order | Tracing indices and state changes; more independent practice before claiming mastery |
| **Big-O** | Not assessed | In scope, but your files lack the lecture notes, so we haven’t covered it |
| **Nested data summaries** | No attempts yet | Computing separate group statistics, means, and labeling results |

“Unassessed” doesn’t mean you don’t know it—it means you haven’t shown it here. Recursion is **not on Quiz 4**, according to the current outline.

I’ve saved this assessment in [progress.md](progress.md). Let’s check aliasing next:

```python
a = [1, 2]
b = a
b[0] = 9
```

What does `a` contain afterward, and why?