# Practice 01: Separate solution

| Item | Topic ID | Task/format | Scope/style basis | Personal target | Answer evidence |
|---|---|---|---|---|---|
| P01 | missing-values | Predict a numerical result and original row count; explain | course-packet.md S4; original synthetic practice, not an instructor item | Recheck reviewed M01 confusion using concrete values | Reasoned solution; arithmetic checked in Python; R not executed |

The mean returned is **6**: (4 + 8)/2 = 6. The original `tickets` still has **3 rows**.

In [course-packet.md](course-packet.md), S4, `na.rm = TRUE` excludes missing values from this calculation and does not automatically edit the original dataset. There is no assignment back to `tickets`. This distinguishes the values used in a calculation from rows stored in the data.

Verification: the arithmetic was checked with Python; the R behavior was reasoned from supplied packet S4, not tested in R. No student answer has yet been reviewed for this question.
