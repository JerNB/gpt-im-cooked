# Separate solution: next question 02

| Item | Topic ID | Task/format | Scope/style basis | Personal target | Answer evidence |
|---|---|---|---|---|---|
| transfer-02 | within-group-denominator | Critique a report; correct a fraction; interpret the competing denominator | course-packet.md S3 supplies within-group proportions; worksheet.html Q4 provides population-selection format. This original synthetic item adds critique and reverse population interpretation beyond the clinic redo. | Test fresh population selection after a correct same-item redo, without the clinic numbers or solution | Reasoned solution; exact arithmetic verified in Python 3.13.12 |

The report's claim is incorrect. Its stated population is **all audio-tour users**, totaling `20 + 18 = 38`. Of these, 18 are children, so the correct fraction is **18/38 = 9/19**.

The fraction `18/30 = 3/5` instead describes the fraction **of child visitors who took the audio tour**. Here the reference population is all 30 child visitors, rather than all audio-tour users.

The numerator happens to be 18 in both questions, but the named group determines the denominator. This follows directly from [course-packet.md S3](course-packet.md#s3-denominators).

Wording/data check: there are 50 adults and 30 children; 20 and 18 audio-tour users respectively, leaving nonnegative non-user counts 30 and 12. No missing-value issue or additional statistical rule is required. Python 3.13.12 verified `20 + 18 = 38`, `Fraction(18, 38) = 9/19`, and `Fraction(18, 30) = 3/5`. Not an instructor key. No student answer to this question has been supplied.
