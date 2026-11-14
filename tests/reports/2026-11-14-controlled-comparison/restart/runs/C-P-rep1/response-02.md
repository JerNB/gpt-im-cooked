**Hi student, let's get you uncooked.**

I’ll check practice Q1 and the course’s counting rule against your reasoning.

Q1 has **3 comparisons**: `(4, 1)`, `(1, 7)`, and `(7, 3)`. You counted the elements; the question asks for the adjacent pairs. I’ll save that distinction as a practice target.

**Hi student, let's get you uncooked.**

Q1 has **3 comparisons**, rather than 4. You counted the elements, but the loop compares **adjacent pairs**:

```text
[4, 1, 7, 3]
 4–1
    1–7
       7–3
```

The last element has no next neighbor. For this pass, **4 elements → 4 − 1 = 3 comparisons**.

**Instructor key:** [Q1](materials/practice-key.md), consistent with Notes §2.2.

I saved this practice target in your [learning record](learning-record.md).

Try Q2: `[8, 2, 5, 6, 1, 4]`. How many adjacent pairs are compared?