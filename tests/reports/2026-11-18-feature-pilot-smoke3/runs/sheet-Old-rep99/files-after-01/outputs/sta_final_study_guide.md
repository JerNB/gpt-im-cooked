# STAT 110 Final Study Guide — supported starter

**Scope note:** The profile lists a cumulative final on December 8, 2026, but the only supplied outline is labeled “Midterm 1.” This guide covers topics confirmed in that outline; it does not establish the final’s full scope. Ask for the final review sheet or remaining lecture notes to complete it. Bayes’ rule is listed in scope in the outline, but its teaching notes were not supplied, so it is marked as a source gap here. Hypothesis testing is explicitly excluded from the supplied Midterm 1 outline; its status on the final is unconfirmed.

## 1. Conditional probability (T1)

**Meaning:** `P(A | B)` means “the probability of A among cases in B.” The group after the vertical bar is the reference group and supplies the denominator.

**Method:** Identify the restricted group B, count cases that are in both A and B, and divide the overlap by the total number in B. State the answer as a percentage rounded to one decimal place and name B in words. The course notes assume equally weighted cases and a nonempty reference group.

**Example:** 10 of 25 commuters cycle: `10 / 25 = 40.0% of commuters`.

**Fragile distinction:** `P(cycles | commuter)` uses commuters as the denominator. `P(commuter | cycles)` uses cyclists. These are generally different questions.

**Common check:** Before dividing, say aloud “out of which group?” That group must be the denominator. In the saved practice attempt, the chosen denominator was the row total when the question asked for a column percentage; use the requested reference group, not the other table margin.

Source: Lecture notes §1.1–1.4; practice set A Q1–Q4 and instructor key; saved attempt STA-attempt-01 (2026-11-17).

## 2. Two-way tables: row and column percentages (T2)

A two-way table counts cases across two categorical variables. Each cell is the count for one combination; row and column totals summarize their respective groups.

| Asked for | Divide cell by | Interpretation |
|---|---|---|
| Row percentage | Total of that row | Share of that row group in the cell category |
| Column percentage | Total of that column | Share of that column group in the cell category |

Row percentages add to 100% across each row. Column percentages add to 100% down each column. Percentages across a row of column percentages need not add to 100%.

**How to choose:** Treat the wording as a conditional probability. The population named after “of,” “among,” or “within” is the reference group and therefore the margin total used in the denominator.

**Example structure:** For a cell “remote workers who are trainees,” “what percentage of remote workers are trainees?” divides that cell by the remote-worker total. The answer names the reference group and follows the reporting rule, e.g. `x.x% of remote workers`.

Source: Lecture notes §2.1–2.3; reporting rule in supplied outline. Personal target from the saved record: distinguish the column total from the row total by naming the reference group before calculating.

## 3. Grouped summaries (T4)

A grouped summary splits cases by a categorical variable and calculates one summary (such as a mean or count) for each group. The output has one row per **nonempty group**, not one row per original case.

**Example:** A mean score for each of four course sections produces four rows, even if there are 120 students. Each row represents a section’s summary, not an individual student.

**Comparison rule:** Compare like with like: mean to mean, count to count. Do not compare a group mean with a group total.

Source: Lecture notes §3.1–3.3; historical Midterm 1 2025 Q3 illustrates the row-count application (historical example only).

## 4. Named but unsupported topic: Bayes’ rule (T3)

The supplied outline says Bayes’ rule was covered in lecture, but the teaching notes were not posted in the supplied files. This guide does not invent a rule or formula. Add the lecture notes or a course example before relying on a Bayes’ rule explanation for the final.

Source: Supplied outline, T3.

## 5. Exam reporting and quick checklist

The supplied outline requires every proportion to be reported as a percentage rounded to one decimal place, with its reference group named. Example form: `40.0% of commuters`.

1. What group does the question restrict me to?
2. Is the denominator that group’s total?
3. Is this a row or column percentage, if using a table?
4. Have I reported a percentage to one decimal place and named the reference group?
5. For grouped summaries, am I counting nonempty groups and comparing the same type of summary?

**Course-based review route:** Recheck T1 independently; spend extra retrieval practice on T2’s denominator choice (the saved record flags this as needing practice); learn T4 from the supplied notes; obtain course notes for T3. The final’s full scope and format remain unconfirmed from the available materials.

## Sources used

- `materials/outline.md` — current as supplied, but labeled Midterm 1.
- `materials/notes.md` — §§1–3.
- `materials/practice.md` and `materials/practice-key.md` — T1 examples and checked instructor answers.
- `materials/midterm-2025.md` — historical examples only; not used to claim current final coverage.
- `course-profile.md` and `learning-record.md` — exam date and reviewed learning evidence.
