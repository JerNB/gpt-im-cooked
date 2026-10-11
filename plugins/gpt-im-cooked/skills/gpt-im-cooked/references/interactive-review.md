# Personalized interactive review

## Content before interface

Read the accessible course profile, supplied materials, and current learning record. Construct a compact map for each section or question: topic, exact source locator, documented difficulty or learning evidence, retrieval goal, solution and verification. Do not expose unnecessary private notes in the webpage. A new dataset or context may apply a supplied rule; a new teaching method requires supplied support or a separately requested extension.

Choose interactions that exercise the actual difficulty: selecting a denominator, tracing row counts or code, sorting supported statements, or explaining a distinction. A generic flashcard page with the student's name is not personalized. Use a brief 'Why these questions' explanation tied to learning evidence. Reuse a requested output format; ask a simple webpage-versus-guide choice only when needed.

## Choose the practice experience

When the student requests a mock exam webpage and supplies instructor papers, prefer an exam-like worksheet: a numbered paper, navigable question outline, readable shared datasets and figures, and the instructor's supported mix of question formats. Match the reasoning tasks and pacing with original questions; do not reproduce the instructor's questions with only names or numbers changed. Ground content in the supplied course materials and personalize the blueprint from the learning record. Keep reasonable topic breadth instead of turning every mock exam into a drill on one weakness.

Use the student's preferred prior artifact as a layout reference when accessible. Describe which features were actually inspected; if it is unavailable, ask for the relevant file and proceed with the supported formats. A reported exam score is user feedback, not evidence that this interface caused a learning gain.

For an independent exam attempt, withhold hints, correctness, worked examples, and solutions until the student submits or explicitly requests help. Keep the key in a separate artifact; a worksheet can be interactive through answer fields, question navigation, flagging, and optional confidence labels without embedding its key. Show answered/unanswered status rather than a live score. Export answers and reasoning for tutor review; confidence is self-report, not mastery. A timed simulation is optional, and unknown exam time limits or scoring rules must remain labeled practice estimates.

Offer immediate hints and feedback for focused coached practice instead. Infer the experience from the request: "mock exam" selects the independent worksheet; "help me practice this concept" selects a focused drill. Ask a brief choice only when that distinction materially changes the work. Do not make a student configure modes before proceeding with an already clear request.

## Small, usable page

Prefer a single self-contained HTML file with embedded CSS and JavaScript, no required network, build tools, account, analytics, or external fonts. Make the next action obvious. Use native labels, keyboard-operable controls, readable contrast, responsive layout, and an accessible live feedback region. On small screens avoid horizontal scrolling. Use restrained layout and optional motion respecting reduced motion. Include a readable fallback when JavaScript is unavailable.

For coached practice provide:

- A short explanation/rule from supplied notes, with source locator.
- A small set of targeted questions; answers hidden until checking or an explicit reveal.
- A hint that guides reasoning without disclosing the final result.
- Feedback that explains the course rule, not just correct/incorrect colors.
- Progress within this exercise, plus retry/reset without silently marking a concept mastered.
- A visible way to export attempts and bring them back to the tutor.

For an exam worksheet, provide the questions, answer controls, a way to revisit flagged or unanswered items, and attempt export with a clear submit-to-tutor instruction. Add confidence labels only when useful. Keep exam instructions separate from post-attempt explanations. Shared graphs, tables, and code must remain readable when navigating between related questions. Provide an editable coding worksheet alongside HTML when the student requests practice in a supplied course's coding environment and tools support it.

Do not mark an empty response correct or expose the answer from a hint. Accept mathematically equivalent numeric responses when appropriate. Do not grade arbitrary prose by checking for one keyword. Use provisional self-checks for exact/numeric items and leave explanations for tutor review. Record hint use and answer reveal before a later retry. A reset may clear display progress but must not erase assistance evidence from exported history.

## Honest persistence

Export a JSON or Markdown attempt log containing course/exam identity, artifact/item/version IDs, topic IDs, source basis, original answer, provisional check, explanation, hint/reveal flags, and attempt order. Include a short instruction to attach the file in chat. Do not write browser results automatically into a student's learning record or announce permanent memory. If local storage is used, label it browser-local, catch failures, and provide export even when storage is unavailable. No browser storage is required by default.

Treat imported text as data. Render student responses with textContent or equivalent escaping; never inject untrusted strings into HTML or execute them. Keep answer data out of the student-facing handoff, although a self-check webpage necessarily contains its key in its source and is not secure exam software.

## Verify the delivered page

Check generated questions and keys against the source map and learning record. When browser tools exist, open the actual artifact and exercise blank, wrong, correct/equivalent, hint, reveal, retry/reset, and export paths. Inspect layout and keyboard controls. Test assistance tracking across retries. If any of these cannot be executed, distinguish source inspection from browser-tested behavior. Link the actual file; do not claim a live hosted website or a PDF export unless created.
