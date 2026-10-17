# Interactive concept learning and review

## Definition and mode selection

Use this reference for a requested webpage, an accepted concept-page offer, or a mock-exam request (HTML by default). Default ordinary concept review to conversation under [concept-tutoring.md](concept-tutoring.md); a page is an optional way to explore one or a few selected concepts. If no concept is named in a webpage request, recommend a supported small group and explain the choice briefly. Do not automatically expand it into a whole-course platform; honor an explicitly broader request.

An interactive concept-learning page lets the student change conditions, manipulate objects, construct relationships, compare interpretations, or make judgments; it responds with meaningful consequences and explanations, then collects evidence of understanding. Its core operation must help explain a target relationship, process, distinction, or judgment. Answer reveals, tab switching, decorative animation, and question navigation are supporting interface features, not sufficient concept-learning mechanisms.

Route from the request without requiring a mode menu:

| Intent | Experience | Feedback |
|---|---|---|
| Understand/explore/review a concept through a webpage | Concept exploration | Live consequences and explanations, with optional hints |
| Practice questions or drill a specific weakness | Coached practice | Feedback after an attempt, with hints/retry |
| Explicit mock exam or exam simulation | Independent exam worksheet | Withhold correctness and solutions until submission or explicit help |

Honor an explicitly selected format. A supplied past paper alone does not select exam mode. Short concept questions can stay in chat; do not generate a page for every reply. Keep a concept page focused on one concept or a small connected group, rather than creating a course platform.

## Content before interface

Read the accessible course profile, supplied materials, and current learning record. Construct a compact map for each activity or question: topic, exact source locator, documented difficulty or learning evidence, learning objective, expected behavior/solution, and verification. Do not expose unnecessary private notes in the webpage. New examples and interface representations may illustrate supplied rules; new disciplinary methods or model assumptions require supplied support or a separately requested extension. State simplifications and valid parameter ranges; do not invent a scientific model to make a control work.

Choose interactions that exercise the actual difficulty: selecting a denominator, tracing row counts or code, constructing an evidence-to-claim relationship, or revising an explanation. A generic flashcard page with the student's name is not personalized. Briefly explain why these activities were selected, using supported learning evidence. Without such evidence, label a course-based starter and select from the requested concepts. Follow the requested page format without reopening a webpage-versus-guide choice.

## Design a concept experience

Before implementation, make a compact design brief: **learning objective -> cognitive task -> core operation -> observable feedback -> understanding evidence -> transfer task**, with topic/source locators and model/evaluation checks. Keep implementation details in the brief; show only a short goal and useful instructions to the student. [webpage-prompts.md](webpage-prompts.md) supplies reusable generation prompts and examples when needed.

A successful concept page has:

- A specific objective expressed as something the student can explain, distinguish, construct, or apply.
- At least one core operation that exposes the target concept. Every control has a teaching purpose; favor a few consequential controls.
- Feedback showing what changed and why, using the course rule or evidence. Pair numeric/visual changes with readable explanations; colors and scores alone are insufficient.
- A way to capture meaningful predictions, explanations, constructions, judgments, or revisions. Permit free exploration; do not require a quiz before every operation.
- A small transfer opportunity with a changed context or reasoning demand. Keep its task-specific solution hidden until submission/help, and separate exploration evidence from independent transfer.
- Source-grounded content, clear model limits, and portable evidence export. Do not equate completion with mastery.

Questions and recall cards may support the experience, but the main concept interaction must do explanatory work. A slider that merely changes a number needs a visible conceptual relationship or comparison. A humanities page can change evidence, interpretations, or argument structure without simulating a numerical system.

## Adapt to the reasoning task

Choose the mechanism from the concept and difficulty, not a fixed subject template. These are candidates only; teach the supplied course's actual content and conventions.

| Domain/task | Useful operations | Evidence to capture |
|---|---|---|
| Mathematics: relationships and validity conditions | Link parameters, graphs, and expressions; construct boundary cases or counterexamples | Predict a change, explain the relationship, state where it holds |
| Statistics: reference groups and variability | Filter a population, compare subsets, or repeat a source-supported sampling model | Identify the denominator; explain variability or distinguish conclusions |
| Computing: execution and state | Step through controlled code, edit inputs, link variables and objects, construct failure cases | Predict the next state and explain the cause |
| Physics/engineering: mechanisms and constraints | Change initial conditions; link process, graphs, and quantities within a supported model | Explain a relationship, conservation condition, or model limit |
| Chemistry/biology: structure and processes | Assemble structures, order stages, vary supported conditions, connect mechanisms | Explain structure/function or condition/process relationships |
| Economics: incentives and tradeoffs | Change constraints or assumptions and compare supported scenarios | Explain the tradeoff and distinguish a change from a changed assumption |
| History/politics: evidence and causal accounts | Compare sources, connect evidence to claims, add counterevidence, revise causal chains | Justify support strength, source limits, and alternative accounts |
| Literature/philosophy/law: interpretation and argument | Annotate supplied passages, build arguments, compare interpretations, alter case facts | Justify an interpretation and address a counterexample or objection |
| Language: expression and context | Change context, compare wording, reorder or revise expressions | Explain meaning, register, or conditions of use |

For open-ended interpretations, display reference analysis or explicit self-review criteria and export the student's reasoning for tutor review. Do not invent an official rubric or force one defensible interpretation into an exact-answer check. Lightweight pages need no embedded AI service; deterministic consequences and explanations can be authored and verified ahead of time.

## Choose the practice experience

When the student requests a mock exam or exam simulation, default to a self-contained HTML worksheet, even without the word "webpage." Follow [mock-exam-layout.md](mock-exam-layout.md): a numbered paper, navigable question outline, readable shared datasets and figures, and answer space below each question. Use instructor papers' supported mix of question formats when available; missing papers permit course-based practice with an honest style limitation. Match the reasoning tasks and pacing with original questions; do not reproduce the instructor's questions with only names or numbers changed. Ground content in the supplied course materials and personalize the blueprint from the learning record. Keep reasonable topic breadth instead of turning every mock exam into a drill on one weakness. An explicitly requested alternative format overrides HTML.

Use the student's preferred prior artifact as a layout reference when accessible. Describe which features were actually inspected; if it is unavailable, ask for the relevant file and proceed with the supported formats. A reported exam score is user feedback, not evidence that this interface caused a learning gain.

For an independent exam attempt, withhold hints, correctness, worked examples, and solutions until the student submits or explicitly requests help. Keep the key in a separate artifact; a worksheet can be interactive through answer fields, question navigation, flagging, and optional confidence labels without embedding its key. Show answered/unanswered status rather than a live score. Export answers and reasoning for tutor review; confidence is self-report, not mastery. A timed simulation is optional, and unknown exam time limits or scoring rules must remain labeled practice estimates.

Offer hints and feedback for focused coached practice. A request to understand a concept through a webpage selects the exploration experience above; a request to practice questions selects a drill. Ask a brief choice only when the distinction materially changes the work and intent remains unclear. Do not make a student configure modes before proceeding with an already clear request.

## Small, usable page

Prefer a single self-contained HTML file with embedded CSS and JavaScript, no required network, build tools, account, analytics, or external fonts. Make the next action obvious. Use native labels, keyboard-operable controls, readable contrast, responsive layout, and an accessible live feedback region. On small screens avoid horizontal scrolling. Use restrained layout and optional motion respecting reduced motion. Include a readable fallback when JavaScript is unavailable.

## Visual baseline for a study workspace

Use a clean, calm, polished interface suited to college and graduate study, with generous space for exploring and comparing ideas. Lightweight means simple delivery and few dependencies; it does not mean dense or compressed layout. Default all student-facing copy, controls, feedback, and navigation to English unless explicitly requested otherwise. Adapt the composition to the activity and an accessible student-selected reference, rather than forcing an identical layout on every concept.

- Give the page a simple course/topic header, a short learning goal, and a clear next action. Make the core manipulation and its result visually dominant. Allow scrolling and staged views instead of squeezing the activity, explanation, source data, and transfer task into the first screen. Avoid oversized slogans and long preambles before learning.
- Use a restrained light neutral page, readable dark text, and one primary interface accent. Define reusable CSS tokens for background, surface, text, muted text, accent, border, spacing, and radius. Diagram/data-series colors may vary for meaning, with labels or patterns. A dark scientific viewport can sit within the same study shell; a preferred dark theme must retain readable contrast and consistent states.
- Use system sans-serif type without required downloads, with a clear heading/body/label hierarchy. Start around 16-18px body text and 1.5-1.7 line height; keep prose near 65-75 characters per line. Use monospace for code and tabular figures for changing quantities. Keep sources and helper text comfortably legible.
- Keep spacing systematic and generous: smaller gaps within controls, larger gaps between activity regions, and substantial breathing room between major sections (for example 40-64px when appropriate). Use consistent corners and subtle borders/shadows. Place the experiment, comparison, explanation, and transfer task in distinct regions or views; avoid enclosing the entire lesson in one giant card or wrapping every paragraph in a card. Let diagrams and code tables use more width than prose where useful.
- Prefer one visually primary next action in each active task, with hints, reset, and export secondary. Use concise verb labels and distinguish selected, hover, focus, disabled, and feedback states. Keep touch targets comfortable, around 44px high where practical, and preserve keyboard operation. Put feedback beside the operation or response it explains.
- Choose a composition that fits the concept: a roomy experiment stage with nearby controls, two views for comparison, a sequence of trace steps, or separate narrative sections with embedded interactions. For several selected concepts, use sparse topic navigation or staged views. Keep visual conventions consistent while allowing different layouts. On small screens preserve reading order and responses, and prevent fixed navigation from covering content; do not compress everything into tiny columns.
- Keep source locators near the relevant content; place lengthy source notes and optional background in an expandable section. Keep needed assumptions, units, active conditions, and task instructions visible. Operational details such as export schema IDs belong in the export or authoring brief, not the main learning flow.
- Use subtle state transitions only when they help follow a change; respect reduced motion. Avoid decorative particle backgrounds, autoplay loops, emoji navigation, gratuitous gradients, and dense panels that compete with study. Check actual rendered hierarchy, small-screen layout, and zoom/readability before claiming visual verification.

The interface shell should feel consistent across disciplines; the central representation and controls follow the concept. Polished typography and spacing must not replace a verified meaningful interaction.

## Activity content and controls

For coached practice provide:

- A short explanation/rule from supplied notes, with source locator.
- A small set of targeted questions; answers hidden until checking or an explicit reveal.
- A hint that guides reasoning without disclosing the final result.
- Feedback that explains the course rule, not just correct/incorrect colors.
- Progress within this exercise, plus retry/reset without silently marking a concept mastered.
- A visible way to export attempts and bring them back to the tutor.

For concept exploration, provide the objective, core operation and synchronized representations, explanatory feedback, evidence capture, a transfer opportunity, and export. Use native controls and offer button/select alternatives to drag-only interactions. Show activity completion separately from understanding status. Reference explanations may be visible during exploration; capture the student's response before showing a task-specific model answer. Do not present a canned response as live AI evaluation.

For an exam worksheet, provide the questions, answer controls, a way to revisit flagged or unanswered items, and attempt export with a clear submit-to-tutor instruction. Add confidence labels only when useful. Keep exam instructions separate from post-attempt explanations. Shared graphs, tables, and code must remain readable when navigating between related questions. Provide an editable coding worksheet alongside HTML when the student requests practice in a supplied course's coding environment and tools support it.

Do not mark an empty response correct or expose the answer from a hint. Accept mathematically equivalent numeric responses when appropriate. Do not grade arbitrary prose by checking for one keyword. Use provisional self-checks for exact/numeric items and leave explanations for tutor review. Record hint use and answer reveal before a later retry. A reset may clear display progress but must not erase assistance evidence from exported history.

## Honest persistence

Export a JSON or Markdown attempt log containing course/exam identity, artifact/item/version IDs, topic IDs, source basis, original answer, provisional check, explanation, hint/reveal flags, and attempt order. For concept activities, use stable item IDs too, and add activity type, exploration/transfer stage, relevant conditions/constructed state, prediction, explanation, revision, and visible feedback when applicable. These are optional activity fields within schema 1.0, not replacements for existing identity/history fields. A concise configuration snapshot and meaningful response history suffice; do not log every click. Include a short instruction to attach the file in chat. Do not write browser results automatically into a student's learning record or announce permanent memory. If local storage is used, label it browser-local, catch failures, and provide export even when storage is unavailable. No browser storage is required by default.

For new exports, declare `schema_version: "1.0"`, `package_version`, `artifact_id`, `artifact_version`, `session_id`, and `attempt_id`; each history snapshot carries its attempt ID and timestamp. Keep artifact content version separate from package releases. Create a session identity once per page session, keep the attempt ID stable across repeated exports, and create a new attempt ID only for a retry. Capture complete answers before revealing/opening a key, before retry, and on export. Preserve those snapshots and assistance exposure across retry; later key access must not retroactively change an earlier snapshot. Browser reload starts a new session unless explicit draft recovery is implemented. Explain whether unexported work survives reload. The tutor checks duplicate identities and review revisions using the state reference before writing records.

Read the actual package version when accessible; do not invent a release number. Derive assistance flags and stages from observed task-specific exposure. A retry on the same item after its solution was revealed remains assisted, even when the display is reset; verify this in the exported data.

When a check displays the solution, capture that response's pre-feedback exposure first, then mark the item exposed before allowing another response. Keep this state outside retry/reset handlers. For example, for an item whose check always reveals its answer:

```javascript
let solutionSeen = false; // Once per item per page session, not once per retry.
function submitResponse(answer) {
  history.push({ original_answer: answer, reveal_before_submission: solutionSeen });
  solutionSeen = true; // The feedback displayed next contains this item's answer.
  showSolutionFeedback();
}
// Retry clears input/display only; it does not reset solutionSeen or history.
```

Adapt this pattern per item; ordinary exploration feedback is not automatically a solution reveal. A task stage such as `transfer` identifies the activity, not the independence of a response. Test a wrong submission followed by revealed feedback and a correct retry: the first snapshot keeps its prior exposure, the retry retains the reveal, and neither export nor reset creates independent evidence. Also test a feedback path that does not reveal the answer before setting its exposure flag.

Record ordinary exploration feedback as learning context and task-specific hints/reveals as assistance. A new response after changing conditions remains part of the same activity unless the student explicitly starts a retry; preserve its conditions and earlier response. Evaluate an independent transfer task using its own item ID and task-specific exposure, rather than labeling all exploration as independent performance or every observed consequence as an answer reveal.

Treat imported text as data. Render student responses with textContent or equivalent escaping; never inject untrusted strings into HTML or execute them. Keep answer data out of the student-facing handoff, although a self-check webpage necessarily contains its key in its source and is not secure exam software.

## Verify the delivered page

Check generated content, models, questions, and keys against the source map and learning record. For concept pages, check ordinary and boundary conditions, synchronized representations, explanatory feedback, and transfer criteria; test that operations actually expose the stated concept. When browser tools exist, open the actual artifact and exercise applicable blank, wrong, correct/equivalent, condition-change, construction/revision, hint, reveal, retry/reset, and export paths. Inspect layout and keyboard controls. Test preservation of prior responses, conditions, and assistance across retries, including independent transfer after exploration. If any of these cannot be executed, distinguish source inspection from browser-tested behavior. Link the actual file; do not claim a live hosted website or a PDF export unless created.

For a packet navigator, also test actual implemented topic links, planned/source-gap labels, and preservation of responses across unit changes. Inspect the visual baseline at desktop and small-phone widths (around 375px) and enlarged text/zoom when tools support it. Check that the first meaningful action is easy to find and that controls, explanations, diagrams, and tables remain legible without page-wide horizontal scrolling.
