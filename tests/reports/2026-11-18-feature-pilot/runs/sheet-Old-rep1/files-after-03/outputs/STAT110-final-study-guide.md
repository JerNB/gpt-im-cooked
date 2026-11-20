# STAT 110 Final Study Guide

**Exam listed in course profile:** December 8, 2026, 9:00 a.m.–12:00 p.m.  
**Scope caution:** The supplied outline is titled *Midterm 1 outline*, not a final review outline. It confirms T1–T4 for that midterm only. Treat these as supported review topics, not a verified complete cumulative-final list. Ask for the final review outline before concluding coverage.

## Source map

| Topic | What to retrieve | Course source |
|---|---|---|
| T1 Conditional probability | Identify the reference group; divide overlap by its size; name the group | Lecture notes §1; practice set A Q1–Q4 |
| T2 Two-way table percentages | Cell ÷ row total for row percent; cell ÷ column total for column percent | Lecture notes §2 |
| T3 Bayes’ rule | In scope on the supplied outline, but the teaching notes are not posted | Outline only; **source needed** |
| T4 Grouped summaries | One summary per non-empty group; compare like summaries | Lecture notes §3 |

**Excluded on the supplied Midterm 1 outline:** hypothesis testing (moved to Midterm 2). A 2025 paper includes it, but that historical question does not establish final scope.

## 1. Conditional probability (T1)

Read **P(A | B)** as “the probability of A among B.” B is the reference group. Count cases in both A and B, then divide by the number in B:

**P(A | B) = count(A and B) / count(B)**

The denominator is not automatically the whole sample. The order matters: P(A | B) and P(B | A) generally use different groups and can differ. The notes assume equally weighted cases and a non-empty reference group.

**Worked example (Practice A Q1):** 10 of the 25 commuters cycle. 10 ÷ 25 = 0.40, so report **40.0% of commuters**. The denominator is the 25 commuters because the question asks about commuters.

**Reporting rule:** Every proportion must be a percentage rounded to one decimal place, with the reference group named in words. Write “40.0% of commuters.” Do not leave it as 0.4, 40%, or 2/5.

**Quick check:** If asked “what percentage of remote workers are trainees?”, the denominator is remote workers, not all employees. Practice A Q2 gives 6 ÷ 24 = **25.0% of remote workers**.

## 2. Two-way tables (T2)

A two-way table counts cases across two categorical variables and includes row and column totals. For any cell:

- **Row percentage:** cell count ÷ that row’s total. Percentages across a row add to 100%.
- **Column percentage:** cell count ÷ that column’s total. Percentages down a column add to 100%.

Choosing a row or column denominator is the same reference-group decision as in conditional probability. Before calculating, say the group in words and use that group’s total.

**Fragile distinction:** A column percentage uses the column total, even if the question mentions a category shown in a row. Read what the question conditions on; do not choose the denominator from the table’s visual orientation alone.

**Personal review target:** Your learning record notes one earlier error: you selected a row total for a column percentage. Corrective cue: **name the reference group, then use its total as the denominator.** After calculating, check that row percentages add to 100% within each row, or column percentages add to 100% within each column.

The supplied notes do not include a numerical two-way table to work through; use your class table examples for additional computation practice.

## 3. Bayes’ rule (T3) — course source needed

The outline lists Bayes’ rule as in scope and says it was covered in lecture, but the posted notes do not explain it. I’m leaving the method and formulas blank rather than inventing a course rule. Add the lecture notes or an instructor example, then review the rule and work a course-style problem. Until then, this topic is **unassessed**, not evidence of a weakness.

## 4. Grouped summaries (T4)

A grouped summary splits cases by a categorical variable and computes one summary value (such as a mean or count) per group. The result has **one row per non-empty group**, not one row per original case. Compare groups using the same kind of summary; do not compare one group’s mean with another group’s total.

**Worked example (2025 past paper Q3):** Four course sections are the groups. A grouped summary of mean score has **4 rows**, regardless of the 120 students, assuming all four sections are non-empty. This is a historical example of the grouped-summary idea; it does not confirm final exam format.

## Retrieval checklist

1. For a conditional percentage, can I name the reference group before choosing the denominator?
2. Can I distinguish row percent from column percent and state which direction totals to 100%?
3. Can I state the number of output rows in a grouped summary from the number of non-empty groups?
4. Have I obtained the missing Bayes’ rule lecture notes?
5. Have I checked the instructor’s final outline for topics not covered in this Midterm 1 packet?

## Short study route

Start with T2 denominator practice because the saved record documents a row/column denominator error. Recheck T1 before the exam (it is marked Demonstrated, with a recheck due). Learn T4 from §3 of the notes, then obtain the Bayes’ rule lecture material. Finally, compare every topic against the actual final outline. No exam format or reference-sheet allowance was supplied.

## Sources used

- `materials/outline.md`, “STAT 110 (synthetic) — Midterm 1 outline,” in-scope and excluded lists, reporting rule.
- `materials/notes.md`, §§1–3.
- `materials/practice.md`, Practice set A Q1–Q4; `materials/practice-key.md`, instructor key.
- `materials/midterm-2025.md`, Q2–Q3, historical paper.
- `course-profile.md` and `learning-record.md`, exam date and prior T1/T2 learning evidence.
