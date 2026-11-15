# Conditional probability transfer 1 - separate key

Original synthetic practice, not an instructor question.

Question: A class has 60 students. 24 attended tutoring; 18 of those passed. In total, 30 students passed. A student claims that because 75.0% of tutoring attendees passed, 75.0% of students who passed attended tutoring. Is that claim correct? Give the correct percentage of students who passed who attended tutoring, and explain the denominator.

Topic: T1. Source: materials/notes.md sections 1.1-1.4; materials/outline.md reporting rule. Personal target: distinguish reversed conditional groups after Q1 whole-sample error and correct same-structure Q3/Q4 answers. Transfer changes the reasoning demand by requiring evaluation of a reversed-conditional claim.

Answer: Claim incorrect. 60.0% of students who passed attended tutoring. Numerator: 18 students both attended and passed. Denominator: all 30 students who passed. The 24 tutoring attendees are the reference group for the other direction, which gives 75.0% of tutoring attendees passing. The total of 60 is not the requested reference group. Cases assumed equally weighted; reference groups nonempty. Counts are feasible: 18 attended and passed, 6 attended and failed, 12 did not attend and passed, 24 did not attend and failed.

Evidence: Verified computation using Python: 100*18/30 == 60.0; 100*18/24 == 75.0. Reference-group interpretation is a reasoned solution applying Notes 1.1-1.3. Key not exposed before student attempt.
