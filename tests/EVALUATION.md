# Evaluate usefulness, not just valid Markdown

The [October 17 evidence-chain run](reports/2026-10-17/REPORT.md) preserves an
actual faulty concept export, a repaired example, frozen tutor inputs/outputs,
record ablations and separate external-review materials. Run
`node tests/check_concept_retry.cjs` for the repaired-page regression and
`python tests/check_evidence_archive.py` for archive integrity. The preserved
legacy page intentionally fails that page regression; it is the RED fixture,
not a current implementation. Archived semantic judgments remain author reviews,
not automated grading or real-student learning results.

## Repeatable behavioral checks

Use synthetic fixtures so no student's grades or instructor papers are shared. Open a fresh model conversation with the packaged SKILL.md and its supporting files. Send one student turn at a time; save the actual reply and changed state after each turn. Do not tell the tutoring model the desired answers, failure hypotheses, or scoring checklist. A manual skill load tests instruction behavior; it does not test automatic discovery or plugin installation.

Judge critical requirements as pass/fail with evidence, rather than hiding failures in a high average score:

| Requirement | Observable evidence | Failure |
|---|---|---|
| Supplied-content grounding | Rules and questions have supplied source locators | New rule taught from general knowledge, missing notes silently filled |
| Current scope wins | Older excluded topic omitted from practice | Historical paper overrides current exclusion |
| Selective record | Reviewed errors and specific self-reports saved with provenance | Uncertainty recorded as error; irrelevant personal remark saved as weakness |
| Improvement | Correct independent explanation updates status conservatively | One success called mastered; previous evidence erased |
| Cross-chat continuity | Fresh model uses accessible record without old conversation | Claims memory without reading record; repeats intake unnecessarily |
| Personalized output | Section/item selection tied to saved learning evidence | Generic guide or page merely renamed for the student |
| Student choice | Webpage/guide choice respected | Unrequested webpage or repeated format intake |
| Hint separation | Guidance does not reveal the result | Hint gives answer; key appears before requested |
| Honest marker | Exact greeting appears; no context-meter claim | Missing marker or claim that it detects full context |
| Page behavior | Blank/wrong/equivalent/hint/retry/export paths work | Empty input passes; assistance erased; broken export |

Keep ambiguous grading in open questions. A source-bounded answer is more useful than an invented explanation. Count source review, executable assertions, browser checks, and human judgments separately.

## Test the complete loop

1. Supply a narrow course packet with current exclusions and an older conflicting exam.
2. Ask for a short practice set with a separate key.
3. Submit a mixture of an explained mistake, a correct answer, a specific difficulty, an unrelated remark, and an ambiguous question.
4. Ask about an outline topic whose teaching notes are absent.
5. Submit one unaided transfer success; check that progress improves without claiming mastery.
6. Select interactive HTML, then exercise controls and export assistance-aware attempts.
7. Start a fresh conversation with only the skill, packet, and saved learning record. Ask for a review guide, then bring back the page export for reviewed record updates.

Repeat important cases in multiple fresh runs and on actual student subjects. One successful run is evidence, not a reliability percentage. Re-run after a model or skill version change. Keep holdout questions unfamiliar to the tutor when measuring student learning.

## Human pilot

Recruit a few classmates who did not design the workflow. Give them the normal README and ask them to start, submit an attempt, request review materials, and resume a new chat. Observe where they need help, how long setup takes, whether they understand why an answer is wrong, and whether they can use the saved record. Measure learning with independent before/after transfer questions rather than asking only whether the output looks good. Keep this study separate from automated tutoring tests.

## Plugin checks

Install the package in the target client and verify discovery, onboarding, the main invocation, resource access, and persistence location in a fresh chat. Validate both standalone and plugin routes separately, without installing duplicate copies. Manifest validation cannot certify client behavior. See [validation status](../VALIDATION.md) and the [pilot cases](PILOT-CASES.md) for completed and outstanding checks.
