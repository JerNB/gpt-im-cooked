# STAT 110 Final Study Guide

**Course-based starter | Prepared for the December 8, 2026 final**

## Scope note

The course profile calls the final cumulative, but the only supplied scope outline is for **Midterm 1**. This guide therefore covers only the topics confirmed in that outline: conditional probability, two-way-table percentages, Bayes’ rule, and grouped summaries. It does not claim complete final coverage. Ask your instructor or check the final review outline for later topics. Hypothesis testing is excluded from the supplied Midterm 1 outline; its status for the final is unconfirmed.

**Bayes’ rule source gap:** The outline says Bayes’ rule was covered in lecture, but the notes are not posted. This guide marks it for follow-up and does not invent a formula or method.

## 1. Conditional probability: choose the reference group first

“The probability of A among B” means: restrict attention to group B, then find what share of B is also in A.

\[
P(A\mid B)=\frac{\text{number in both A and B}}{\text{number in B}}
\]

The denominator is the size of the named reference group B, not the whole sample. The order matters: (P(A\mid B)) and (P(B\mid A)) generally use different denominators. The notes assume equally weighted cases and a non-empty reference group.

**Worked example.** Of 25 commuters, 10 cycle. The question asks what percentage **of commuters** cycle, so commuters are the reference group: (10/25=0.40=40.0\%\). Report: **40.0% of commuters**.

**Before calculating:** underline “among,” “of,” or “given”; say the reference group in words; use its count as denominator; then round the proportion to one decimal place.

## 2. Two-way tables: row or column percentages

A two-way table organizes counts for two categorical variables. For a cell count:

- **Row percentage** = cell ÷ that row’s total. It answers “what share of this row group…?”
- **Column percentage** = cell ÷ that column’s total. It answers “what share of this column group…?”

This is the same reference-group choice as conditional probability. Row percentages add to 100% across a row; column percentages add to 100% down a column. Percentages across a row of column percentages need not add to 100%.

**Personal correction cue.** A reviewed attempt selected the row total for a column percentage. To avoid repeating that error, identify the requested reference group before looking at totals: for a **column** percentage, divide by the total at the bottom of that column. Write “of [column group]” beside the result. For a row percentage, use that row’s total instead.

**Quick check:** If the question asks “among people in column C, what share are in row R?”, use the count in cell (R,C) divided by the total for column C. The reference group is column C.

## 3. Grouped summaries

A grouped summary splits cases by a categorical variable and computes one summary value (for example, a mean or count) per group. It has **one row per non-empty group**, rather than one row per original case.

**Worked example.** A mean score is reported for each of four course sections: the result has **4 rows**, one per section. When comparing groups, compare the same kind of summary (mean with mean, count with count); do not compare a group mean with a group total.

## 4. Bayes’ rule: confirm the course method

Bayes’ rule is listed as in scope in the Midterm 1 outline, but the supplied notes do not explain it. Get the instructor’s lecture notes or an assigned example before memorizing a rule or practicing a method. Its presence on this outline does not establish whether it is included on the cumulative final.

## Reporting rule and final self-check

The supplied outline requires every proportion to be reported as a **percentage rounded to one decimal place**, with the reference group named in words. For example, write “40.0% of commuters,” not just “0.4,” “40%,” or “2/5.”

1. What group is the question asking about?
2. Does my denominator count exactly that group?
3. Did I label the answer “of [group]”?
4. Did I convert to a percentage and round to one decimal place?
5. For grouped summaries, did I count non-empty groups and compare like summaries?
6. Have I confirmed the cumulative final’s full topic list and Bayes’ rule materials?

## Suggested review route

First practice row versus column denominators, since the learning record flags that distinction for more practice. Then recheck conditional probability before the exam (the saved record marks it Demonstrated with a recheck due). Review grouped-summary interpretation, obtain the missing Bayes’ rule materials, and verify the final’s complete scope.

## Source map

- Course profile, “Course scope”: final date and cumulative designation; available source inventory and scope caveat.
- `materials/outline.md`, Midterm 1 outline: T1–T4 inclusion, Bayes’ rule note gap, hypothesis testing exclusion for that midterm, reporting rule.
- `materials/notes.md`, §§1–3: conditional probability definition, denominator, order and assumptions; table percentage denominators and sums; grouped summaries and comparisons.
- `materials/practice-key.md`, Q1–Q4: worked conditional-probability calculations and reporting style.
- `materials/midterm-2025.md`, Q3: historical grouped-summary row-count example (historical paper; not evidence of final format).
- `learning-record.md`, Concepts and Attempt history: T1 recheck due; T2 denominator confusion and targeted correction. This guide is a course-based starter because the record contains only limited reviewed evidence.
