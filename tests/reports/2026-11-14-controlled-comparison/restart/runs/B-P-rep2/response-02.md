**Hi student, let's get you uncooked.**

I’ll check Q1 and the practice guidance against your answer.

**Hi student, let's get you uncooked.**

Q1’s answer is **3 element-to-element comparisons**. You counted the elements, but the question asks how many **adjacent pairs** are compared:

```text
[4, 1, 7, 3]
 4──1           comparison 1
    1──7        comparison 2
       7──3     comparison 3
```

The last element has no neighbor to its right, so it doesn’t start another comparison. For this pass, **4 elements → 4 − 1 = 3 comparisons**. ([Notes §2.2](materials/notes.md))

A complete quiz answer would be: “**3 comparisons, counting only comparisons between adjacent list elements.**”

**Instructor key:** confirms 3 for [practice Q1](materials/practice-key.md).

To check the reasoning: if the list contained just **one element**, how many adjacent-pair comparisons would there be, and why?