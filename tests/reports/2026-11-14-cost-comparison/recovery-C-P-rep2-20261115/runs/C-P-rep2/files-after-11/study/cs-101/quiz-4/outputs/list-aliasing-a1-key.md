# List aliasing A1 — tutor key

Source: materials/notes.md §§1.1–1.2. New application of supplied reference and shared-mutation rules.

Question:
```python
a = [4, 7]
b = a
b[0] = 9
```
What are a and b afterward, and why?

Reasoned solution: a and b both refer to the same list, whose contents are now [9, 7]. Assignment b = a shares the list object; changing its first element through b is visible through a. This solution has not been executed. No task-specific hint or solution should be shown before the student's response unless requested.
