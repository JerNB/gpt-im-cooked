# STAT 110 Final - Cheat Sheet (Study Draft)

**Two pages for review; exam-room allowance, content rules, and cumulative final scope are unconfirmed.** The only supplied outline is for Midterm 1. Use this as an exam-room sheet only after checking the final review outline and instructor rules.

## Page 1 - Conditional probability and two-way tables

### Conditional probability: choose the reference group first

`P(A | B)` means **the share of group B that is also in A**.

`P(A | B) = count(A and B) / count(B)`

- The condition after the bar (`B`) names the reference group and denominator.
- Order matters: `P(A | B)` and `P(B | A)` generally use different denominators and can differ.
- Course condition: cases are equally weighted and the reference group is nonempty.

**Quick example.** Of 25 commuters, 10 cycle. `10 / 25 = 0.40`, so report **40.0% of commuters**. Do not divide by all 40 students: the question restricts attention to commuters.

### Two-way table percentages

| Asked for | Divide each cell by | Percentages sum to 100% |
|---|---|---|
| Row percentage | Its row total | Across each row |
| Column percentage | Its column total | Down each column |

Before dividing, name the group being considered. That group's total is the denominator. A row of column percentages need not add to 100%.

**Personal cue:** In a reviewed table attempt, the column percentage used a row total. For a column percentage, divide by the column total.

### Report every proportion this way

Convert to a percentage, round to **one decimal place**, and name the reference group in words: **"40.0% of commuters."** The supplied outline says answers without the reference group lose one point. Avoid reporting only `0.4`, `40%`, or `2/5`.

## Page 2 - Grouped summaries and scope

### Grouped summaries

A grouped summary splits cases by a categorical variable and calculates one summary (such as a mean or count) for each group.

- Output: **one row per non-empty group**, not one row per original case.
- Compare like with like: mean with mean, count with count. Do not compare a group mean with a group total.

**Quick example.** Four non-empty course sections produce four result rows, even if the sections contain 120 students altogether.

### Bayes' rule - source gap

The supplied Midterm 1 outline lists Bayes' rule and says it was covered in lecture, but the lecture method is not in the supplied notes. This sheet does not invent a formula or steps. Add the course's method from lecture notes before relying on this topic.

### Scope check before the final

**Verified from supplied materials:** conditional probability, two-way table row/column percentages, Bayes' rule (listed, method unavailable), and grouped summaries appear on the **Midterm 1 outline**.

**Unconfirmed:** whether these topics are on the cumulative final, what other topics the final includes, and whether any reference sheet is allowed or what its size/content rules are. Hypothesis testing is excluded from the supplied Midterm 1 outline only; its final status is unconfirmed.

### Source basis

`materials/outline.md` (scope and reporting rule); `materials/notes.md` --1-3 (methods and conditions); `materials/practice.md` Q1 and `materials/practice-key.md` Q1 (commuter example); `learning-record.md` (reviewed denominator error). No Bayes method or current final outline was supplied.
