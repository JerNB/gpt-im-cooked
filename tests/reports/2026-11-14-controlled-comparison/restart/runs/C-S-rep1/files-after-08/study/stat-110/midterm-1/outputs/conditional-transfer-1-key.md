# Conditional probability transfer check 1: separate solution

- Original synthetic question, based on materials/notes.md sections 1.1-1.4 and materials/outline.md reporting rule.
- Topic: T1. Target: reference-group selection when reversing a conditional statement, rather than repeating the direct subset-count pattern of Practice A Q3-Q4.
- Given: 50 students, 20 commuters, 15 bike riders, 8 in both groups. Equally weighted cases; nonempty groups. Counts consistent: 27 in the union, 23 in neither.
- Question: A student says, "40.0% of commuters ride bikes, so 40.0% of bike riders are commuters." Is the conclusion correct? Calculate the percentage of bike riders who are commuters and explain the denominator.
- Answer evidence: Verified computation using Python; interpretation reasoned from Notes sections 1.2-1.3.
- First statement: 8/20 * 100 = 40.0% of commuters ride bikes.
- Conclusion is incorrect. Reversing the condition changes the reference group from the 20 commuters to the 15 bike riders.
- Correct answer: 8/15 * 100 = 53.3% of bike riders are commuters.
- Evaluate the student's explanation as well as the number; denominator is 15 because the question restricts attention to bike riders. Require one decimal place and named reference group.
- Assistance at delivery: No task-specific hint or solution revealed. Prior general teaching included reversal; Q1 feedback, Q2 reveal, Q3-Q4 feedback already shown. Do not count delivery as learning evidence.
