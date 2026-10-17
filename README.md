<p align="center"><img src="docs/assets/wordmark.svg" alt="GPT, I'm Cooked. Your course. Your weak spots. A better next attempt." width="100%"></p>

<p align="center"><a href="https://jernb.github.io/gpt-im-cooked/demo.html"><strong>Try the mock exam</strong></a> · <a href="#quick-start">Get started</a> · <a href="docs/INSTALLATION.md">Install</a> · <a href="VALIDATION.md">Testing & limitations</a></p>

A reusable **English learning and exam-review skill and plugin** for college and graduate students. Understand your course concepts through clear conversation, retain meaningful learning evidence and weak spots, and use that record for personalized practice exams and study guides. Interactive pages are an optional aid for selected concepts.

Designed for English-language college and graduate study, including international students at US universities. Tutoring, page copy, feedback, and generated study outputs default to English unless the student explicitly asks for another language. Teaching uses plain language, small worked examples, and explanations of why each step follows. Optional concept pages use purposeful interactions and spacious layouts suited to the idea.

**Preview v0.5.1** · Main skill: `$gpt-im-cooked` · Codex-ready instructions · No bundled AI server

The October 17 patch preserves answer exposure across retries in a [repaired concept-page example](examples/grouped-transformations.html), adds an executable regression, and clarifies how tutors review contradictory export labels. [Evidence, repeated tutor runs, and limits](tests/reports/2026-10-17/REPORT.md) distinguish the reproduced page defect from model judgments and unmeasured learning gains.

The October 15 update makes conversation the primary review experience, with optional interactive pages for selected concepts. A simple mock-exam request produces an HTML paper with a separate key; a study-guide request produces a PDF when the host supports generation. See the [v0.5.0 changes and package checks](tests/reports/2026-10-15/RELEASE.md).

## Try an exam-style demo

[![Preview of the live mock exam worksheet](docs/assets/demo-preview.jpg)](https://jernb.github.io/gpt-im-cooked/demo.html)

**[Open the interactive mock exam →](https://jernb.github.io/gpt-im-cooked/demo.html)** · **[Visit the project page →](https://jernb.github.io/gpt-im-cooked/)**

An original, eight-question statistics paper with multiple-select questions, graph interpretation, and R code completion. Navigate the paper, mark items to revisit, record reasoning and confidence, then export your attempt. The answer key stays in a separate page.

The layout is inspired by a college mock-exam study workflow. The public demo uses a **fictional course packet and student record**; it does not reproduce an instructor's paper or use private study notes. It has no AI connection or automatic grading. Attach its exported JSON to your tutor for feedback and reviewed record updates.

[Course packet](docs/course-packet.md) · [Synthetic learning record](docs/learning-record.md) · [Question blueprint](docs/content-map.md) · [Separate solutions](docs/answer-key.html)

## Real study examples

**[Explore the real STA199 and CS201 cases →](https://jernb.github.io/gpt-im-cooked/examples/)**

These are the creator's actual study artifacts from the workflow that inspired the skill, shared for others to explore. The sessions predate the packaged release; they demonstrate the workflow, not measured learning gains from installing the plugin.

### STA199: a mock midterm shaped by saved learning evidence

[![The original STA199 mock paper: a graph interpretation question and question navigation](docs/examples/sta199/mock-preview.png)](https://jernb.github.io/gpt-im-cooked/examples/sta199/)

**[Open the original 32-question Mock Practice B](https://jernb.github.io/gpt-im-cooked/examples/sta199/practice/STA199_Mock_Practice_B.html)** · **[Download the editable QMD + datasets + six graphs](docs/examples/sta199/practice-pack.zip)**

The real record remembers a grouped-`mutate` row-count error, a duplicate-key join error, and multiple-select difficulties. It also removes stale weakness labels after correct execution, and distinguishes self-reported difficulty from assisted-session improvement. Those priorities inform new practice while retaining broad course coverage.

[Case walkthrough & reusable English prompts](https://jernb.github.io/gpt-im-cooked/examples/sta199/) · [English selection of the learning evidence](docs/examples/sta199/learning-record-english.md) · [Original Chinese study record](docs/examples/sta199/learning-record-original.md) · [Separate answer key (spoilers)](docs/examples/sta199/answer-key.md)

The original Quarto HTML is a browser-readable worksheet. Edit the QMD to answer and run R code; it has no automatic grading. The public record removes only computer-local absolute paths and adds a publication note. Private student attempts referenced in that record are not bundled.

### CS201: the actual six-page personalized review guide

[![Original CS201 guide page 4: object references, pair loops, and course-specific code](docs/examples/cs201/page-4.png)](https://jernb.github.io/gpt-im-cooked/examples/cs201/)

**[Read or download the original PDF](docs/examples/cs201/guide.pdf)** · **[Browse all six pages and the case walkthrough](https://jernb.github.io/gpt-im-cooked/examples/cs201/)** · [English source draft](docs/examples/cs201/guide-source.md)

The student's missed questions and follow-up requests became exact constructor traces, identity/equality tables, P0 reference diagrams, P1 token-window visuals, runtime reminders, and relevant APT patterns. This shows a personalized guide built from supplied course code and specific difficulties. The PDF is unchanged; reference-sheet permission depends on your own course.

## What makes it useful

| Principle | What happens in your review |
|---|---|
| **Your supplied course is the boundary** | Teaching rules need a source in your accessible notes. Missing content is flagged; excluded topics stay out. |
| **Remember useful learning evidence** | Save meaningful mistakes, specific difficulties, assisted attempts, and improvements. Read that record when resuming. |
| **Understand through clear conversation** | Explain the main idea in plain English, work through a small example, clarify the confusing step, and build an accurate takeaway. |
| **Personalize the next output** | Emphasize your documented weak spots in focused practice, an instructor-style mock exam, a study guide, or a permitted reference sheet. Optional interactive pages explore selected concepts when requested. |

Past papers provide evidence of question formats and reasoning patterns. New questions use original situations. A mock exam keeps breadth; a focused drill can concentrate on one weakness. The skill does not predict the next exam or promise a grade.

## Quick start

1. **[Download the standalone skill](docs/downloads/gpt-im-cooked-skill-v0.5.1.zip)** and extract the `gpt-im-cooked` folder.
2. Copy that entire folder into `~/.codex/skills/` (or your configured `$CODEX_HOME/skills/`). Preserve an existing copy unless you intend to replace it. Refresh the skill list or restart the client if needed, then open a new chat.
3. Add one useful course file and send:

```text
Use $gpt-im-cooked to help me prepare for my midterm.
Here are my course notes and practice paper.
```

You can start with a single course link, outline, or set of notes. A short request is enough: the skill handles scope checks, separate practice answers, and selective learning records. Past exams, dates, and official keys help, but are optional. Mention known exclusions; uncertain scope is flagged. Materials are read as needed for the current activity rather than requiring a complete course inventory before tutoring.

**Prefer the plugin?** [Download the plugin package](docs/downloads/gpt-im-cooked-plugin-v0.5.1.zip) and follow the [plugin installation guide](docs/INSTALLATION.md). It bundles the same review skill plus onboarding. Local marketplace support varies by client; install one route for normal use to avoid duplicate entries.

**Try without installing:** clone or download the repository, keep the whole skill folder accessible, and ask Codex to read [SKILL.md](plugins/gpt-im-cooked/skills/gpt-im-cooked/SKILL.md) and its relevant supporting files. This manual preview does not test automatic plugin discovery.

## The study loop

**Course scope → conversational concept review → learning evidence and record → personalized practice/mock exam → study guide**

Join at the requested step. Concept review starts in conversation, with clear explanations and source-grounded examples. Requests for targeted questions select coached practice; explicit mock-exam requests select independent exam practice with separate solutions. Past papers calibrate applications and formats when available; they are optional for concept learning. An interactive page can be offered briefly when manipulating a relationship would help, and is generated when the student chooses it. Browser exports need tutor review before they update the saved record.

No chosen concept is required. A full review packet starts with a concise topic map, a supported study route, and a first explanation in chat. Requested concept pages focus on one or a few supported concepts, with spatial layouts chosen for the activity. Explicit broader artifact requests retain their requested coverage; unread or unsupported topics remain identified honestly.

**Default formats:** mock exams are HTML exam worksheets with separate checked keys, following the [STA199 paper layout](plugins/gpt-im-cooked/skills/gpt-im-cooked/references/mock-exam-layout.md); study/review guides are PDF files with rendered-page checks when supported. Explicit format requests override these defaults. If PDF generation is unavailable, the tutor labels the editable fallback and its limits. Small recaps and ordinary concept questions stay in chat.

| You want to… | Say… |
|---|---|
| Check the boundary | “Compare my notes with the exam outline. Flag missing content.” |
| Start from a review packet | “Here are my review files. Map the topics and suggest where to start.” |
| Understand a concept | “I don't get this concept. Explain it in plain English.” |
| Get a nudge | “Give me a small hint for question 4, without the answer.” |
| Review an attempt | “Check my answers and reasoning. Keep my original attempt.” |
| Practice like the exam | “Make a short mock exam from these materials.” |
| Target a difficulty | “Give me new questions on my recent denominator mistakes.” |
| Make a guide | “Make an English review guide from my weak concepts.” |
| Explore a few concepts visually | “Make an interactive page for these two concepts.” |
| Resume | “Continue from my course profile and saved learning record.” |

See [conversational concept review](plugins/gpt-im-cooked/skills/gpt-im-cooked/references/concept-tutoring.md) for the teaching approach and [optional webpage prompts](plugins/gpt-im-cooked/skills/gpt-im-cooked/references/webpage-prompts.md) for concept-page and mock-exam briefs. A one-sentence request is enough to start.

In a writable workspace, the tutor saves a course profile and selective learning record, usually under `study/<course>/<exam>/`. Student data stays outside the installed package. A new chat must have access to that record; bring it when switching computers. Browser exports require tutor review before the record changes.

Every tutoring reply starts with **“Hi student, let's get you uncooked.”** It is a visible workflow marker. It cannot measure remaining context. If it disappears, ask the tutor to reread the skill and accessible saved records.

## What has been tested

The v0.5.1 downloads contain the maintained source. The [October 17 evidence report](tests/reports/2026-10-17/REPORT.md) includes original/repaired page-script replay, isolated tutor runs, and record ablations. These do not establish learning gains or automatic plugin discovery. The HTML-mock/PDF-guide defaults still lack a dedicated fresh model run. See the [current validation status](VALIDATION.md) and [earlier release checks](tests/reports/2026-10-15/RELEASE.md).

Version 0.4.1 adds duplicate-import/review rules, a Python standard-library helper for conflict-checked single-record writes and backups, explicit export identities, pre-key snapshots, and an allowlisted package builder. Python 3.10+ is optional; hosts without it use the documented manual fallback. Student records remain Markdown in their workspace. The helper is invoked by the tutor, not a background service. Export review and import-ledger updates remain tutor responsibilities.

Run `python tests/check_state_io.py` and `node tests/check_demo_state.cjs` for state/helper and demo-script regressions. See [state checks and limits](tests/reports/2026-10-11/STATE.md) and the [fresh-model pilot](tests/STATE-PILOT.md). Script checks do not establish new model behavior.

The previous v0.3.0 run used five isolated tutoring contexts and 14 total turns, including fresh-chat resume, selective record updates, scope boundaries, and browser export import. The earlier coached page was tested in Chrome. Those archived results describe the tested snapshots, not every later revision.

The v0.4.1 update organizes the main skill around the study loop, unifies naming, and makes the plugin download include a usable local marketplace. See the [v0.4.1 cleanup and distribution checks](tests/reports/2026-10-11/CLEANUP.md), [validation status](VALIDATION.md), the [earlier demo check](tests/reports/2026-10-10/SHOWCASE.md), and the [earlier model run](tests/reports/2026-10-10/REPORT.md). Actual plugin installation/discovery and real-student learning gains remain unverified.

## Explore the package

- [Review skill](plugins/gpt-im-cooked/skills/gpt-im-cooked/SKILL.md) and [onboarding skill](plugins/gpt-im-cooked/skills/gpt-im-cooked-start/SKILL.md)
- [Installation and updates](docs/INSTALLATION.md)
- [Evaluation method](tests/EVALUATION.md) and [22 behavioral pilot cases](tests/PILOT-CASES.md)
- [Earlier worked demonstration](examples/DEMO.md) and [fresh-chat review guide](tests/reports/2026-10-10/resume/outputs/review-guide-01.md)

For development checks, install PyYAML and run `python tests/validate_package.py`. Build both downloads from the same source with `python scripts/build_packages.py`; then run `python tests/check_distribution.py` to check their extracted contents and paths. This checks package structure; it does not install the plugin or evaluate learning gains.

The project was previously named **ExamLoop**. Version 0.4.1 unifies the plugin ID, directory, and main skill as `gpt-im-cooked`; onboarding is `gpt-im-cooked-start`. Existing `exam-loop` plugin installations need an intentional replacement; study records stay in their original workspace. This is a skills-only preview, not a public plugin-directory listing. Code execution, browsing, and PDF generation depend on the host's available tools.
