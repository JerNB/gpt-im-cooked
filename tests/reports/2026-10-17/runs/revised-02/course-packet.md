# STA-DEMO Midterm: supplied course packet

## O1: current exam outline
This is a synthetic college statistics course. Covered topics only: T1 grouped proportions, T2 row counts after grouped mutate and summarise, T3 translating a conditional-proportion question. Excluded: joins, hypothesis tests, normal approximations. T4 skewness is named in the outline, but its teaching notes have not been supplied. Exam format: short answers explaining a denominator or row count. No scoring rubric or exam-room sheet allowance supplied.

## L1: instructor notes, grouped proportions
A group's proportion is its count divided by that group's total. A whole-table proportion uses the entire table total. Always name the population forming the denominator.

## L2: instructor notes, row counts
In this course, grouped mutate adds a computed column while keeping all original rows. Grouped summarise with one scalar summary per group returns one row for each group. Grouping alone does not remove rows.

## L3: instructor notes, conditional language
For 'among A, what fraction are B?', the denominator counts A and the numerator counts rows satisfying both A and B.

## E1: current instructor practice
Q1: Class A has 8 students and 2 commuters. Class B has 12 students and 3 commuters. What proportion of Class A are commuters? Explain the denominator.
Q2: A 20-row table has two groups. How many rows result from grouped mutate? How many from grouped summarise with one scalar per group?
Q3: Among 12 students who cycle, 9 wear helmets. What fraction of the cyclists wear helmets? Explain the denominator.
Q4: A 20-row table has 2 commuters in Class A, whose total is 8. 'Find the commuter proportion.' The grouping population is unspecified.

## K1: current instructor key
Q1: 2/8 = 1/4, denominator Class A.
Q2: mutate 20 rows; summarise 2 rows.
Q3: 9/12 = 3/4, denominator cyclists.
Q4: key says 2/20, but does not specify whether the question is about Class A or the entire table.

## P0: older exam excerpt
An older paper asks students to combine two tables with left_join. This older topic is excluded by O1.
