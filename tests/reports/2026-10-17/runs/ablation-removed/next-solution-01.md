# Next question — solution

Open after attempting [the question](next-question-01.md).

| Item | Topic ID | Task/format | Scope/style basis | Personal target | Answer evidence |
|---|---|---|---|---|---|
| transfer-01 | within-group-denominator | Interpret a table; name a reference population | [Course packet S3](course-packet.md#s3-denominators); [worksheet Q4](worksheet.html#q4) | Extend the correct Q4 reasoning to a group defined by wait category | Reasoned solution; arithmetic verified with Python 3.13.12 |

This is original synthetic practice, not an instructor question.

The reference population is all short-wait tickets: 10 + 6 = 16. Six of those are Plus-plan tickets, so the fraction is 6/16 = 3/8 = 0.375 (37.5%). The denominator is 16 because the question begins with short-wait tickets. Using 15 would answer a different question: the fraction of Plus-plan tickets with a short wait.

Verification: both plan totals equal 15; the short-wait total is 16, the long-wait total is 14, and the overall total is 30. Python verified 6/(10+6) = 0.375. The denominator choice follows the supplied S3 rule; execution verifies the arithmetic only.
