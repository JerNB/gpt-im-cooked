I’ll check practice Q1 and its answer key against the course’s counting rule.

**Hi student, let's get you uncooked.**

Q1 has **3 comparisons**. You counted the elements; the question asks how many **adjacent pairs** are compared:

```text
[4, 1, 7, 3]
 4—1
    1—7
       7—3
```

Four elements make three neighboring pairs. For one full adjacent-pair pass, use **`n − 1`** comparisons when `n ≥ 1`. ([Notes §2.2](materials/notes.md))

Your answer should say: **“3 element-to-element comparisons, counting each adjacent pair once.”** This matches the [instructor key, Q1](materials/practice-key.md).

I saved this as a point to practice in your [learning record](study/cs-101/quiz-4/learning-record.md).

Try Q2 next: `[8, 2, 5, 6, 1, 4]`. How many adjacent-pair comparisons, and why?