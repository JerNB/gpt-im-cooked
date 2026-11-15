# Conditional probability transfer check 1 - separate key

Original synthetic practice; source basis: materials/notes.md sections 1.2-1.4; materials/outline.md Reporting rule. Builds on materials/practice.md Q4, but changes the conditioning group.

## Question
A store had 45 shoppers: 20 ordered online and 25 shopped in person. Of the online shoppers, 9 returned an item. Of the in-person shoppers, 6 returned an item. What percentage of shoppers who returned an item had ordered online? Give your answer to one decimal place, name the reference group, and explain your denominator.

## Solution - keep separate from independent attempt
Answer evidence: Verified computation (Python arithmetic executed locally).
Reference group: all shoppers who returned an item, 9 + 6 = 15.
Numerator: 9 online shoppers who returned an item.
Answer: 60.0% of shoppers who returned an item had ordered online.
Reasoning: The question restricts attention to returners, across both purchasing groups. The online-shopper total of 20 answers a different conditional question.
Personal target: Reverse the conditioning group from Practice A Q4 and construct its total from two subgroups, rather than use an explicitly provided subgroup total. Transfer check, not merely new numbers. No task-specific hint or solution supplied to student before attempt.
