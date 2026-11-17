# Review artifacts

## Choose the output

Conversation is the default for concept review. Honor requests for practice, a mock exam, a study guide, or a permitted reference sheet directly. A brief recap stays in chat; a requested study/review guide defaults to PDF, and a requested mock exam defaults to HTML. The student need not specify a file type or choose from a format menu. Use loaded learning state and pending evidence for ordinary replies. For personalized artifacts, follow the save/refresh checkpoint in [state.md](state.md); without evidence, label a course-based output honestly.

| Request | Default delivery |
|---|---|
| Explain a concept, recap, or give a few practice questions | Conversation |
| Make a mock exam / exam simulation | Self-contained HTML exam worksheet and a separate checked key |
| Make a study guide / review guide / cheat sheet | Ask the one allowance question below; default: a two-page (one two-sided sheet) exam reference sheet PDF marked exam use unconfirmed. "Just for reviewing" gives a study-guide PDF |
| Make an interactive page for selected concepts | Focused self-contained HTML concept exploration |
| Make a study plan / schedule / calendar | `.ics` file plus a printable self-contained HTML calendar, built by `scripts/plan_study.py` following [study-plan.md](study-plan.md) |

Explicit language, format, and coverage requests override these defaults. A permitted reference sheet follows confirmed instructor rules.

Interactive concept pages are an optional aid for one or a few selected concepts. Offer one briefly when exploring a relationship would be useful, and continue conversational teaching unless the student chooses it. A past use of webpages is not a standing instruction to generate them for future review. Requested pages follow [interactive-review.md](interactive-review.md).

Webpages have three experiences: concept exploration for understanding, coached practice for targeted questions, and an independent worksheet for an explicit mock-exam request. A concept-learning webpage defaults to exploration with meaningful operations and explanatory feedback, rather than a question list. Infer the experience from the student's intent; supplied papers calibrate content and formats without selecting exam mode by themselves. Follow an explicit format or preferred artifact when accessible. Keep mock-exam solutions separate and preserve course breadth.

For mock exams, read [mock-exam-layout.md](mock-exam-layout.md) and the exam path in [interactive-review.md](interactive-review.md), even if "webpage" was omitted. The STA199 reference supplies a numbered-paper layout; the student's actual course supplies topics, question formats, and rules.

For sheets and guides, write the content JSON (shape: [assets/sheet-example.json](../assets/sheet-example.json)) and render it with `scripts/render_sheet.py`; do not hand-build a layout program. The renderer needs ReportLab. If it reports that ReportLab is missing, ask the student before running `pip install reportlab`; if they decline or installation fails, deliver a clearly labeled editable source, explain the specific limitation, and identify unverified layout. Do not claim that source text, a print button, or an HTML preview is a generated PDF.

## Review packets without a named concept

A collection of notes, slides, outlines, and papers is enough to propose a starting route. Inspect the supplied outline/review structure and relevant file sections first; group related concepts into a concise topic map with supplied-source locators. Distinguish confirmed scope, excluded/unconfirmed topics, missing teaching content, and unread sections. A listed topic is not yet a verified teaching unit. Keep different courses/exams separate.

Recommend a starting concept using current reviewed difficulty evidence when available, then supported prerequisite relationships, explicit instructor emphasis, and course order. Explain the basis briefly. Without useful student evidence, label a course-based route; file volume, question frequency, and topic selection alone do not diagnose weakness or predict exam importance.

- Files with no clear goal: give a brief supported materials/scope orientation and a proposed next activity; ask only for a goal or ambiguity that changes the next action. Do not automatically generate an exam or a large website.
- General "help me review these materials": give the concise topic map and suggested route, then explain a supported concept in plain English in chat. Follow [concept-tutoring.md](concept-tutoring.md). Honor guide, practice, or exam requests directly, without making a diagnostic or artifact a prerequisite.
- "Make a concept-review webpage" with no chosen concept: recommend one or a few supported concepts, explain the selection briefly, and create the focused learning unit. Use light navigation only if the selected units need it; do not automatically create a whole-course hub. If the student actually asks for a starter navigator, label planned units and partial coverage honestly.
- Explicit "cover every confirmed topic/chapter" website: inspect enough source material and deliver the requested supported coverage, preferably as small navigable units in a self-contained page or explicitly requested linked files. Every delivered unit needs its own meaningful interaction, explanation, and understanding evidence. Report genuine source gaps precisely; do not replace the request with one starter or claim unread topics are covered.

When a navigator is requested or useful for the selected units, use honest labels such as Available, Planned, Source needed, and Excluded. Show activity completion separately from reviewed understanding, and preserve answers when switching between implemented units. Let students change the suggested route without an intake questionnaire.

When a student asks for a study guide, review guide, or cheat sheet and the course profile does not already record the allowance, ask exactly one question before drafting: "Is this a cheat sheet you'll bring into the exam? How many sheets, and one- or two-sided?" If they do not know or skip it, build one two-sided sheet (two pages) and mark it exam use unconfirmed. Only "it's just for reviewing, not for the exam" produces a study guide. Record the answer in the course profile. Do not ask for approval of a content plan before the first draft: generate it and let the student revise. Do not assume that double-sided means two sheets: sheets and printed sides are different. An exam sheet must meet confirmed restrictions. Preserve an instructed document structure during edits.

## Content rules

These apply to exam sheets and study guides; a guide simply has no page cap.

- **Start from retrieval need, not course coverage.** A topic earns space only if the student needs help finding, interpreting, or applying it during a question. Name confirmed in-scope topics that got no space in your reply; do not drop them silently.
- **Tier every topic before writing:** *worked* (a short explained example), *cue* (one line: a sign rule, a definition, what a function returns), or *omit*. Choose from the learning record (errors, Needs practice, Recheck), instructor emphasis, and the student's saved preferences. Easy facts get a cue, never a paragraph.
- **One running example per cluster.** Interpret related quantities (for example every coefficient of one model, its group equations and differences) on one shared example with variables, units, and baseline defined once, rather than several abstract templates or several unrelated contexts.
- **Stage multi-step conversions.** Put each stage on its own line and label what scale it is on (for example fitted value, log-odds, odds, probability); use a `stages` block.
- **Prominence follows importance.** Mark high-priority or error-prone sections `"weight": "high"` (larger type, tinted heading); keep low-priority cues compact.
- **No generic reminders.** Pitfalls and checklists appear only when tied to the student's recorded errors or explicit instructor emphasis.
- **Minimum sufficient explanation.** Enough to make the idea usable on the exam; no extended implications.
- **Empty space is allowed.** Never add material because there is room.
- **Scope precision.** Removing a code block does not remove its concept. A student's "leave it off my sheet" is a content preference, not an instructor exclusion; record it in `omitted` with that reason. Material excluded for writing may still be needed for reading.

Connect each section to confirmed topic IDs (`topics`); the printed sheet does not show them. Keep optional background out of an exam sheet unless requested. Do not fill space with long lists of every function or copied answer paragraphs. Avoid personal labels, unnecessary scores, private comments, or unrelated information in printable artifacts.

For a personalized sheet or guide, check all relevant concepts reviewed in the active session and saved record against the requested scope. Include both weaknesses and useful corrected distinctions; do not silently cover only the most recent concept. State genuine coverage gaps.

## Corrected mistakes and content balance

Include selected reviewed mistakes when they explain a fragile distinction or recurring failure better than a generic example. A compact unit contains the necessary prompt, a short original reasoning excerpt or faithful summary, the first error, the corrected method and its conditions, and an optional unanswered variant. Mark missing original reasoning and tentative diagnoses; use only verified errors as confirmed mistakes. Keep independent practice and its key separate from guide explanations.

Choose the share of page space from course demands, exam format, learning stage, and available evidence, rather than a fixed percentage. Early review usually needs more conceptual structure; repeated application errors may justify more corrected examples; exam review still needs confirmed topic coverage, including unassessed topics. For humanities, a short response excerpt with explained revision can serve the role of a worked mistake. Briefly state the selection rationale without claiming a proven optimal ratio.

For exam-room sheets, apply confirmed content and layout restrictions first. Include worked questions or answers only when permitted; otherwise condense their lessons into allowed distinctions, conditions, or cues. On a sheet a corrected mistake usually compresses to the corrected rule and its condition (a `mistake` block or a cue). A full study guide can include explanations without inheriting the sheet's space limit.

## Rendering and verification

Check formulas, examples, terminology, and scope against the source materials and learning record before rendering. Then run:

```text
python <skill>/scripts/render_sheet.py SHEET.json --out <study dir>/sheets [--force]
```

- `OK pages=… preset=… body=…pt out=…`: the renderer chose the most spacious layout that fits the allowed pages. `missing_glyphs=n` means some characters have no font on this host: rewrite them (for example spell out a symbol) and re-render. `previews=none` means no page images could be made: deliver with that inspection limit stated.
- `OVERFLOW over=…pt sections=…`: cut or demote content from the lowest-value sections it lists (turn worked examples into cues, remove *omit*-tier material) and re-render. Never request smaller type; the renderer will not go below 9 pt body / 8.5 pt code, or below an instructor minimum given as `allowance.min_body`. A `reason` naming one block or code line means that block must be shortened or split.
- `ERROR …`: fix the content file and re-run.

Look at each page preview once as an exam tool: each section can be found by its heading at print size, high-weight sections are visibly more prominent, staged calculations read top to bottom, and code is not cut mid-token. Report only what was actually inspected; never describe an uninspected layout as print-verified. For HTML handouts, check that they work without external assets and verify print preview separately before making page-count claims. Link final deliverables and mention only meaningful validation.

## Revision rounds and preferences

When the student asks for changes, apply exactly those edits to the content JSON, increase `revision.round`, and re-render; earlier rounds' PDFs are kept. Standing constraints from earlier rounds (for example "no new information") stay active in later rounds; list them in `revision.standing`. Space freed by deletions is not refilled: the renderer turns it into larger type and spacing.

Save durable preferences from a round in the course profile section `Reference-sheet preferences` (created by the one-command save on first use). Write each as a dated bullet, and keep them separate from scope decisions, for example `- Prefers one worked example over abstract rules (2026-11-16, round 1)` or `- Leave off: ROC function syntax; concept stays (2026-11-16, round 1)`. Read this section before every sheet or guide in that course. When starting a sheet in another course, offer once to reuse the general, non-topic preferences.

Keep the student attempt, solution key, and reference sheet in distinct artifacts. A file separation supports independent study but is not access control: the student can still open a key.
