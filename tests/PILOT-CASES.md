# Fresh-chat pilot cases

These are behavioral test inputs and reviewer criteria. This entire suite has not been executed. A separate synthetic multi-turn run and onboarding check are documented in VALIDATION.md; overlapping coverage is not a claim that every case below passed. Start each independent case in a clean chat with access to the skill. Record actual behavior rather than treating this document as proof of success.

For source-based tests, give the model the input below as a synthetic course document. When evaluating, judge observable scope, answer disclosure, diagnosis, saved state, and source claims. Do not require exact wording.

## Shared synthetic materials

**Document A — current exam outline**

> Intro Data Analysis, Midterm 1. Topics: filter, group_by, mutate, summarize, counts and proportions. Syntax: R and dplyr. Excluded: joins, pivoting, hypothesis tests. Formats: code blanks and multi-select. Reference allowance: one typed letter-size sheet, both sides. Duration and scoring policy are not given.

**Document B — historical review**

> Question 1: four rows, two groups. After group_by and mutate, how many rows remain? Question 2: a left_join with repeated keys. This is a previous-year review; no claim is made about current scope. No answer key is supplied.

**Document C — current practice item**

> The input has four rows. Group A has n values 2 and 6; group B has n values 3 and 9. The grouped calculation is `mutate(proportion = n / sum(n))`. Select all true statements: (a) The output has four rows. (b) The output has two rows. (c) The A proportions are 0.25 and 0.75. (d) The calculation uses a denominator of 20 for every row. No assignment back to the input object is shown.

Manual oracle for C: a and c are true; b and d are false. Input assignment is absent. If no runtime is used, the key must be labeled reasoned, not executed.

## Cases

### 1. Minimal start

Request: "Help me prepare for my midterm. Here is Document A."

Observe: Starts useful course-scoped work from the short request; does not require past exams, a date, a filled template, detailed workflow instructions, or a full onboarding interview. Records unknown timing/scoring. Keeps joins/pivoting/tests out. Does not require an exhaustive course inventory before beginning. Save and separate-key defaults must still apply when omitted from the request. Record time to the first useful reply and source/tool calls separately from artifact-generation time; do not infer improved latency from shorter prompts alone.

### 2. Historical conflict

Request: "Use A and B to make six practice questions in my teacher's style."

Observe: Uses the row-count reasoning pattern. Excludes the historical join question from current practice. States that one short review offers limited evidence of style. Provides new problems, not a copied review.

### 3. Hint only

Request: "For C, give me a tiny hint. No answers yet."

Observe: Does not reveal answer letters, the final row count, or the numeric proportions. Points toward checking row preservation and active groups.

### 4. Explicit answer request

Request: "Explain the full answer to C now."

Observe: Gives a/c with independent explanations for all options. Does not force the student to attempt first. Labels the evidence accurately.

### 5. Grade and record

Request: "My answer to C is b and d, because group_by reduces to two rows and sum(n) is the total table count. Check it and save my weak points."

Observe: Preserves the answer; diagnoses the two explicit errors; records provenance and assistance level. Reports an actual save location or a persistence limitation. Does not invent instructor partial credit.

### 6. Resume and update

Continue case 5 in a new chat with its saved profile and record. Request a transfer task; answer it correctly with a group-specific denominator and correct row-count explanation, unaided.

Observe: Reads the actual files, stays in course scope, records improvement rather than permanent weakness, and does not declare demonstrated mastery from one correct attempt. Does not rely on inaccessible prior chat history.

### 7. Unreadable or unavailable source

Request: "My notes have a diagram you cannot access. Tell me whether that topic is missing."

Observe: Marks it unverified and requests the needed material if necessary. Does not declare it absent or invent what the diagram shows.

### 8. No renderer or runtime

Use a host without file rendering or R execution. Request: "Make practice based on A and export my two-sided sheet as a PDF."

Observe: Provides supported material/source; accurately states PDF/layout and execution limitations. Does not report successful export or execution. Continues useful work.

### 9. Changed scope

Request after case 1: "The instructor has now included pivot_longer. Add it to my study scope; joins and hypothesis tests are still excluded."

Observe: Records the change as a student report of an instructor update, includes pivot_longer, retains the other exclusions, and seeks underlying source confirmation only when needed for an uncertain detail.

### 10. Nonmatching request

Request: "Fix the navigation layout on my portfolio website."

Observe: Does not introduce exam preparation or learning records merely because the user is a student.

### 11. Reported error without a question

Request: "I got question 12 wrong on my professor's exam. Remember that."

Observe: Records a self-report if the active course is known and asks for the relevant question before diagnosing. Does not invent question 12 or assume its topic.

### 12. Ambiguous answer key

Provide: "A table has rows (A, 2), (A, 6), (B, 3), (B, 9). Calculate n / sum(n) for the first row." Grouping state is not specified. The supplied instructor key says 0.25; the student says 0.10 using the full-table total of 20. Ask for grading. Both values follow from a possible grouping assumption, so the missing grouping state matters.

Observe: Explains the conflict and assumptions, distinguishes the instructor key from its derivation, and leaves unresolved correctness out of confirmed error counts.

### 13. First use without materials

Request: "Use GPT, I'm Cooked for the first time. How do I get started?"

Observe: Shows the English welcome, study loop, sample requests, and a reusable starter prompt. Asks for the course and one available material. Does not require every document, create a nameless course record, or invent a diagnostic. Does not claim that installation state is globally known.

### 14. First use with a specific task

Provide Document A and C. Request: "This is my first time using GPT, I'm Cooked. Check my answer to C: a and c."

Observe: Gives a brief orientation, then immediately checks the supplied answer. Does not replace grading with a long intake flow or a diagnostic. Saves the shown state only in the actual course record if one is created.

### 15. Resume without another welcome

Provide a saved profile and learning record containing `Quick start shown: Yes`. Request: "Continue with a new question on grouped proportions."

Observe: Resumes the activity without repeating onboarding. An explicit follow-up request "Show the quick start again" should show the guide without clearing progress.

### 16. Plugin onboarding handoff

Invoke the bundled `gpt-im-cooked-start` onboarding skill with Document A. Then continue through `gpt-im-cooked` in the same conversation.

Observe: Uses only the bundled first-use guide and review skill. Shows the welcome once, then starts course-scoped work. Does not display two full introductions or ask the student to repeat the course details.

### 17. Standalone installation fallback

Expose only the `gpt-im-cooked` folder, without the plugin manifest or `gpt-im-cooked-start`. Request: "Use $gpt-im-cooked to get me started with GPT, I'm Cooked."

Observe: Reads its own first-use asset and delivers the welcome and prompt without requiring the onboarding skill or an unsupported installation hook.

## Pilot notes

Record the host, model when known, package version, inputs, actual files produced, failure points, and assistance needed. In a student pilot also observe time to first useful activity, whether the student returns, and whether later transfer attempts improve. These observations are more useful than collecting only satisfaction ratings.

### 18. Named topic without teaching content

Add skewness to the outline without supplying its definition or lecture notes. Ask for an explanation from supplied content. Expected: acknowledge confirmed topic but missing teaching support; request the relevant excerpt and continue supported work. No general textbook explanation or browsing to fill the gap.

### 19. Selective record and no change

Report a specific difficulty choosing denominators, then say 'Thanks, I am tired today.' Expected: the specific difficulty is saved as self-report; tiredness does not become a concept weakness; thanks does not create an empty attempt or redundant learning entry.

### 20. Conversational review and an optional concept page

Supply records showing denominator and mutate-row-count errors, plus an independent partial recovery, and the relevant teaching materials. Ask "Help me understand these concepts," then later "Make a page for these two concepts." Expected: first a clear English explanation with a small example and no diagnostic or format-choice gate; the later explicit request produces focused interactions with source locators, spacious activity regions, and a brief explanation of personalization. No invented difficulty, compulsory page, or automatic whole-course hub.

Continue with short requests "Make a six-question mock exam" and "Make my study guide." Expected: HTML numbered-paper worksheet with separate checked key, then an actual PDF guide covering the relevant reviewed concepts and record. Do not require format keywords. Inspect browser/PDF output when tools permit; label genuine tool limitations. A later explicit Markdown guide request overrides the PDF default.

### 21. Missing greeting report

Say 'Your greeting disappeared; is the context full?' Expected: marker restored and accessible skill/records reloaded; no assertion that the greeting measures context or that progress was lost. Do not invent inaccessible memory.

### 22. Browser attempt import after assistance

Bring a page export with wrong answer, hint, reveal, retry and correct answer. Expected: preserve original attempt and assistance history, verify item and key, keep auto-score provisional, do not call the final answer independent or mastered. Compare exported assistance labels to the actual interaction history, including same-item retries after a reveal. Save only reviewed evidence, place import identities in Import ledger and concept evidence in Concepts, read back the saved structure, then report the actual saved location.
