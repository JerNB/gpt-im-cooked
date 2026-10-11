# Practice design and feedback

## Extract instructor patterns

For each accessible paper/review, record its identity and whether it is an exam, review, or answer key. Describe formats and reasoning operations: tracing, constructing code, selecting a graph, interpreting data, explaining a mechanism, comparing models, or doing calculations. Use question locators to support claims.

Identify distractor mechanisms, such as confusing an output with its input object, reversing a logical implication, omitting a boundary condition, or mixing related quantities. Also record assumptions used by the course. Two near-identical review sheets are not two independent samples of exam tendencies; make this limitation explicit. Missing pages and unreadable diagrams limit frequency counts.

## Blueprint and item metadata

For a mock exam, match known formats, approximate reasoning depth, and confirmed topic breadth. If timing is unknown, give an estimated practice time and label it as an estimate. Targeted drills may deliberately emphasize one weakness. Do not claim a generated paper predicts the exam.

Keep a small blueprint in the solution file:

| Item | Topic ID | Task/format | Scope/style basis | Personal target | Answer evidence |
|---|---|---|---|---|---|

Separate scope/style provenance from authorship: newly generated items are original synthetic practice, not instructor questions. Missing historical papers permit course-scoped practice but not claims of instructor-style matching.

## Design and check questions

- Make each item answerable from the provided information and approved concepts. State necessary assumptions, variable meanings, units, and data.
- Prefer distractors that reflect an identifiable reasoning error. For multi-select, ensure each option has an independent, unambiguous truth value; explain each in the key.
- Use fresh situations and altered reasoning demands. New names alone do not create a transfer task. Keep prerequisite methods inside scope.
- Check the expected answer first. Compare every option to it. For code, distinguish compilation errors, runtime errors, printed output, returned values, and changes to objects.
- When a runnable environment exists, use controlled synthetic snippets/data to check outputs. Note runtime/version where relevant. Execution verifies that snippet under those conditions, not every claim of asymptotic complexity.
- When execution is unavailable, retain a manual trace/derivation and label it unexecuted. Fix or omit items whose correctness remains materially unresolved.
- If an item depends on a graph, supply a legible graph or a self-contained table plus a suitable rewritten question. Do not refer to a graph the student cannot see.

## Domain adaptations

### Programming

Track initial state -> reference/object relationships -> loop/branch changes -> final printed/returned expression. Use small traces and counterexamples. For runtime, define input sizes, distinguish one operation from amortized/total work, and state course simplifications separately from literal language/library costs. Do not assume that a compiler run establishes Big O.

### Statistics and data analysis

Track unit of observation, variable types, grouping state, row/column counts, denominator, missing-value policy, and whether a result was assigned back to the original object. Check graph choice against variables and analytic purpose. Interpret distributions using appropriate features; distinguish association from causal claims. Match the allowed course packages and syntax.

### Astronomy and other conceptual sciences

Distinguish related concepts and the physical mechanism connecting them. Use comparison questions, diagrams when available, limiting cases, and qualitative predictions. Keep mathematical computation out of a concepts-only request. If formulas are included, use the instructor's conventions and explain units and assumptions.

## Feedback and scoring

Compare the student's answer to the exact prompt before diagnosing. Show the first error, its consequence, and the corrective rule. A self-report of missed question numbers without the paper or answer key is a reported difficulty, not a verified diagnosis. Ask for the relevant item or explain a general concept with that limitation.

Without a supplied rubric, use correct / partially complete / incorrect / unresolved / unattempted. If the student requests numerical grading, explicitly state provisional scoring rules first and distinguish them from instructor rules. Handle equivalent code, alternative derivations, and justified interpretations fairly.

Offer a short follow-up that changes the situation or asks for reasoning, rather than requesting recall of the just-displayed answer. Update the record using the assistance level and result. Keep explanations proportionate: one straightforward error may need only a short paragraph, while a multi-step trace can warrant a table.
