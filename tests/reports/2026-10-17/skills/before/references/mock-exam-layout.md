# Default HTML mock-exam layout

Use this reference whenever a student requests a mock exam or exam simulation without specifying another format. Deliver an actual HTML worksheet, not just questions pasted in chat or a Markdown file. Read [practice-and-feedback.md](practice-and-feedback.md) for original content and a checked blueprint, and [interactive-review.md](interactive-review.md) for exam behavior, evidence export, and browser verification.

## Layout reference

The default visual reference is [STA 199 — Mock Practice B](https://jernb.github.io/gpt-im-cooked/examples/sta199/practice/STA199_Mock_Practice_B.html). Its rendered page and source were inspected: white document surface, restrained typography, comfortable central reading column, right-side table of contents, title/subtitle, usage instructions, numbered question headings with task types, nearby figures/tables/code, answer and confidence space, and separate solutions. It is a browser-readable Quarto worksheet; answers are edited in its QMD source, not automatically graded in HTML.

The specification below is self-contained: the installed skill does not need to fetch that page or require Quarto. Use its paper composition across subjects, while choosing content, question types, terminology, and rules from the student's supplied course. Never inherit its STA199 topics, 32-question count, 80-90 minute practice estimate, reference allowance, student name, datasets, or questions as defaults. Honor another explicitly selected layout when accessible.

## Paper composition

- Lead with course/exam title, a concise question-count/task subtitle, and short independent-attempt instructions. Include timing and allowed aids only with confirmed rules or an explicit practice-estimate label.
- Use a white or near-white page, dark text, a restrained accent, readable system typography, and generous margins. Aim for a main column around 760-900px on desktop; allow tables, plots, and code sufficient width. Avoid a dashboard, dense question-card grid, or enclosing the whole paper in one giant card.
- Keep a continuous numbered paper with stable anchors: `Question 1: [task] — [response type]`. Separate questions with whitespace and a subtle rule. Put complete shared data, assumptions, figures, and code near the relevant questions, with clear cross-references when reused.
- Place answer and reasoning controls below each question. Use radio buttons for single choice, checkboxes for multiple select, and sufficiently roomy text/code fields for written responses. Confidence is optional self-report. Inputs must not contain hints, correct option selections, or completed solutions.
- Provide a compact sticky question outline beside the paper on wide screens, like the reference's right-hand contents list. Show answered/unanswered status and optional revisit flags. Collapse or move navigation above the paper on phones; it must not cover content. Preserve answers while navigating.
- Keep submit/export actions distinct from answering. Submission captures the attempt for tutor review; it does not imply automatic grading. Keep all solutions, answer-bearing explanations, and key data out of the worksheet, including its scripts and hidden markup. Deliver the checked key separately, normally as a readable companion HTML file unless another key format is requested.
- Provide a clean print stylesheet: hide navigation and operational buttons, retain questions/data and readable answer space, and avoid splitting short question/figure blocks where practical. Do not claim a specific printed page count without inspecting print rendering.

Answer controls, status, flags, and JSON/Markdown attempt export are additions for the generated worksheet; they are not claims about features in the original Quarto example. Follow the existing identity, response-snapshot, and assistance-history rules. A separate key is not access control.

## Portable delivery and checks

Prefer one HTML worksheet with embedded CSS/JavaScript and essential figures, no required network or build step. Bundle necessary datasets or an editable coding worksheet only when the requested course exercise needs them, and explain what requires a separate runtime. Do not imply that browser code fields execute R or another language.

Check each question/key against course sources, all alternatives, and any controlled computations actually performed. Open the delivered HTML when browser tools exist: verify anchors, readable data/plots/code, input labels, answer preservation, blank versus answered status, flagging, submit/export, and absence of solution leakage. Inspect desktop and phone layouts. Report specific unavailable checks honestly. Link the HTML paper, separate key, and any necessary companion files.
