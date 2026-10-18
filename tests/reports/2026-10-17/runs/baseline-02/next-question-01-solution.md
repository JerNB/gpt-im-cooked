# Separate solution: transfer question 01

| Item | Topic ID | Task/format | Scope/style basis | Personal target | Answer evidence |
|---|---|---|---|---|---|
| transfer-01 | within-group-denominator | Interpret a proportion; explain population | course-packet.md S3; worksheet.html Q4 supports population selection, while this original synthetic item requires combining late arrivals across sessions | Extend correct Q4 reasoning to a group defined by arrival status instead of session; independence remains to be established | Reasoned solution; arithmetic verified in Python 3.13.12 |

The reference population is **all late arrivals**, morning and afternoon combined: `6 + 9 = 15`. Of those, 9 are afternoon arrivals, so the fraction is **9/15 = 0.60 (60%)**.

The 12 on-time afternoon arrivals are outside the requested population. Using `9 / (12 + 9)` would answer a different question: the fraction of afternoon arrivals that were late.

Basis: [course-packet.md S3](course-packet.md#s3-denominators): a within-group proportion divides the matching count by the total in that group. Manual derivation checked each count and wording; Python 3.13.12 evaluated `9 / (6 + 9)` as `0.6`. This is not an instructor key or evidence that the student has answered the question.
