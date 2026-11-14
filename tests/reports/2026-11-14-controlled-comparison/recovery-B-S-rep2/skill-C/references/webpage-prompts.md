# Webpage generation prompts

These authoring briefs apply after a student requests a webpage, accepts a concept-page offer, or requests a mock exam (HTML by default). Ordinary concept review stays in conversation under [concept-tutoring.md](concept-tutoring.md). A short student request is enough; do not require a template. Default concept pages to one or a few selected concepts and apply [interactive-review.md](interactive-review.md) for mode selection, verification, and evidence export.

## Concept-page authoring prompt

```text
Create a lightweight interactive learning webpage for the student's chosen
concept or small connected concept group.

Default student-facing copy, controls, explanations, feedback, and navigation
to English unless the student explicitly requests another language. If no
concept is named, apply the review-packet routing below before selecting a unit.

Use accessible supplied course materials, the student's stated scope, and the
current learning record. Use available past papers to calibrate applications;
they are optional. Keep rules, methods, and model assumptions traceable to
source locators. Flag missing teaching content instead of filling it from
general knowledge. Without learning evidence, label a course-based starter.

Before implementation, prepare a compact design brief:
learning objective -> cognitive task -> core operation -> observable feedback
-> understanding evidence -> transfer task.
Include topic/source locators and how model outputs or evaluation criteria
will be checked. Choose the interaction from the reasoning task and actual
difficulty, rather than applying one interface to every subject.

Build at least one core operation that helps explain a relationship, process,
distinction, or judgment. Possibilities include changing conditions, tracing
state, constructing relationships, comparing evidence, and revising arguments.
Make consequences visible and explain why they follow from the course content.
Questions, flashcards, and answer reveals can support the page; the main
interaction must do explanatory work. Keep controls few and purposeful.

Allow exploration and capture meaningful predictions, explanations,
constructions, or revisions without forcing a quiz before every operation.
Add a small transfer task with a changed situation or reasoning demand.
Keep that task's solution hidden until submission or explicit help; capture
responses before revealing it. Keep exploration, assisted responses, and
independent transfer distinguishable. Open prose receives self-review criteria
or later tutor review, not keyword-based automatic grading.

Prefer one self-contained HTML file with embedded CSS/JavaScript and no required
network, account, build process, analytics, external fonts, or embedded AI.
Provide readable, responsive, keyboard-operable controls and a clear next action.
Apply the visual direction below and the interactive-review visual baseline.
Export original responses, relevant conditions, revisions, and assistance using
the existing artifact/session/attempt identities and history rules. Explain how
to bring the export back for tutor review and learning-record updates. Clicks,
time on page, and completion do not establish understanding.

Verify source correctness and applicable interaction, transfer, retry, and
export paths. Deliver the actual file, a brief explanation of the learning
design, and precise verification limits.
```

## Compact concept design examples

Use these patterns only when the supplied materials support the concepts.

| Concept | Cognitive task and operation | Feedback | Evidence and transfer |
|---|---|---|---|
| Conditional probability | Identify the reference group by changing a condition/filter | Highlight numerator/denominator groups; link counts, fraction, and explanation | Save a predicted denominator and reason; use a fresh table for independent transfer |
| Object references versus copying | Predict state, step through code, and change an object | Synchronize code position, variables, object graph, and explanation | Save state predictions and revisions; interpret a new supported code snippet |
| Historical causal explanation | Link supplied evidence to a claim, then introduce counterevidence | Show supporting/conflicting sources and prompts about limits; allow revised claims | Save original/revised claim with reasons; evaluate a new source set through tutor review |

## Review-packet authoring prompt

```text
The student supplied an overall review packet without choosing a concept.
Inspect the outline/review structure and relevant supplied materials; give a
compact topic map with source locators, confirmed scope, and honest coverage
gaps. Separate courses/exams. Unread content is not verified teaching coverage.

Recommend a starting concept using reviewed learning evidence when available,
then supported prerequisites, explicit instructor emphasis, and course order.
Without student evidence, label a course-based route and invent no weaknesses.

If the request is general review, begin explaining a supported concept in plain
English in chat. Files alone do not request a mock exam or webpage. A previous
webpage preference does not turn every later review into a website.
If a concept-review webpage is requested without a named topic, recommend one
or a few supported concepts and create a focused unit using the concept-page
brief. Add navigation only where useful; a whole-course hub is not the default.
For an explicitly requested starter navigator, label planned/source-limited
units honestly and identify partial coverage as a starter.
If complete coverage is explicitly requested, deliver that supported coverage
with meaningful units; do not silently substitute a starter. Read further
materials as required and report genuine teaching-source gaps.

Let students change the recommended route. Preserve responses when switching
implemented units. Use English by default and the shared visual baseline.
```

## Visual direction prompt

```text
Design a calm, polished study workspace for college and graduate students.
Use a simple header and learning goal; give the interaction, explanation,
comparison, and transfer task distinct regions or staged views. Allow roomy
diagrams and generous whitespace rather than packing the whole lesson into one
card or one screen. Start with light neutral surfaces, readable
dark text, one interface accent, system sans-serif type, and a consistent
spacing scale. Keep body text around 16-18px with comfortable line spacing.
Define shared CSS tokens and a clear heading/body/label hierarchy.

Choose a layout that fits the concept: an experiment stage, a side-by-side
comparison, a step trace, or a narrative with embedded interactions. Use larger
spacing between major regions than within controls. Keep the next learning
action primary, with hints/reset/export secondary. Use sparse navigation when
needed; adapt it on small screens. Put feedback near the action it explains.
Keep needed assumptions visible and lengthy source notes expandable.

Avoid oversized marketing headings, dense card grids, decorative backgrounds,
and unnecessary dashboards. Keep typography and visual conventions consistent
across subjects while allowing different spatial compositions. Verify
readability, states, keyboard operation, and responsive layout when possible.
```

## Student prompts

Concept study:

```text
Use $gpt-im-cooked. Based on my supplied course materials, make an interactive
webpage to help me understand [concept]. Choose a useful way for me to explore
or construct the idea, explain the feedback, and include a small transfer task.
Use my learning record if available and let me export my reasoning for review.
```

Webpage requested from a packet, no chosen concept:

```text
Use $gpt-im-cooked. Here are my review materials. Pick a couple of concepts that
would benefit from exploration and make an interactive learning page for them.
```

Complete coverage, when that is the student's actual goal:

```text
Use $gpt-im-cooked. Build an English interactive concept-review website covering
every confirmed topic in these materials. Give each supported concept group a
working learning unit and a clear navigation route. Report source gaps and
excluded topics explicitly; keep my responses when switching between units.
```

Targeted question practice:

```text
Use $gpt-im-cooked. Give me a short coached-practice webpage on [concept/weakness]
within my supplied course scope. Let me attempt each question before feedback,
offer small hints, and preserve my answers and assistance history for export.
```

Mock exam:

```text
Use $gpt-im-cooked. Make an original mock exam for [course/exam] using
my confirmed scope and the available past papers' supported formats. Use my
learning record to select priorities while retaining course breadth. Keep
solutions in a separate file and hide correctness/hints during my independent
attempt. Let me flag questions and export answers and reasoning for review.
```

## Mock-exam authoring prompt

```text
Create an independent mock-exam worksheet only for an explicit exam-simulation
request. Default to a self-contained HTML file even if the student does not
say "webpage"; honor an explicit alternative format. Follow mock-exam-layout.md:
white exam-paper surface, comfortable reading column, concise instructions,
numbered question headings with task types, related data/figures/code beside
the relevant question, answer space below it, and a compact side outline on
desktop that becomes collapsible or inline on phones. Adapt question formats
to this course; the STA199 reference is a layout model, not a content source
for other courses. Keep generous spacing between questions and a print layout.
Read the confirmed course scope, relevant past papers if available,
and current learning record. Build an original blueprint with course breadth
and supported formats, weighted toward documented difficulties without turning
the paper into a single-concept drill. Label missing style/timing evidence.

Generate and check the separate key before delivering the worksheet. Provide
readable questions and shared figures/data, independent answer and reasoning
fields, question navigation, answered/unanswered status, and revisit flags.
Withhold hints, correctness, worked examples, and solutions until submission
or explicit help. Keep solutions outside the worksheet; do not embed a live
score or exam key. Timing is optional and must use confirmed rules or a labeled
practice estimate. Export responses and help exposure using the existing
identity/history rules. Verify the artifact and report actual verification.
Default student-facing content to English and use the shared visual baseline,
while retaining a readable exam-paper layout appropriate to the request.
```
