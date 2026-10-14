# v0.5.0 preview release

Date: October 15, 2026. This update preserves plugin/skill identities and existing study files. Both current downloads include the maintained instructions and their supporting resources; previous versioned archives remain available.

## Final workflow and defaults

- Review starts in plain-English conversation: explain meaning, use a small source-grounded example, clarify the reasoning, and give an accurate retrieval cue. Short natural requests suffice; no mandatory diagnostic or webpage gate.
- A full packet without a named concept gets a concise supported topic map, coverage gaps, a proposed starting route, and conversational teaching. Course materials define the boundary; past papers are optional format/application evidence.
- Save selected difficulties, original reasoning, corrections, and improvements. Keep self-report, assistance, and independent transfer distinct. Browser exports still require tutor review before record updates.
- Mock exams default to HTML numbered-paper worksheets with separate checked keys, following the inspected STA199 paper composition. That reference does not impose statistics content, a fixed question count, or its time/aid rules on other courses.
- Study/review guides default to actual PDF files, with rendered-page inspection when tools support it. Explicit format requests override defaults; genuine generation limits receive a labeled editable fallback.
- Interactive concept pages are optional for one or a few selected concepts. Choose operations from the reasoning task and discipline; use meaningful consequences, explanation, understanding evidence, transfer, and spacious activity regions.
- Default student-facing tutoring, commentary, artifacts, and new record summaries to English, with explicit language overrides. Retain original responses and course terminology faithfully.

## Release verification

The release checks compare both ZIPs byte-for-byte to the explicit source allowlists, extract them into temporary directories, and verify contained resource links, manifests, icon/setup paths, and the local marketplace root. Main and onboarding skills receive frontmatter validation. Record-helper/package-boundary regressions and the demo-script checks cover their existing implementations; they are not model tests.

Passed locally:

| Check | Result |
|---|---|
| `python tests/validate_package.py` | Package metadata, English content, resource links, and synthetic arithmetic |
| `python tests/check_distribution.py` | Skill: 13 exact source files; plugin: 20; extracted references resolve |
| Skill-creator `quick_validate.py` | Main and onboarding skills valid |
| `python tests/check_state_io.py` | Record-write conflict/lock/backup behavior and package-boundary rejection |
| `node tests/check_demo_state.cjs` | Existing demo snapshots, retry identities, and assistance exposure |
| `git diff --check` | No whitespace errors |

Current archive SHA-256 values:

- Skill: `2e7fbc7e867d36142be9ca97f04696b630500e6925dcd8bade2ac451a15199c3`
- Plugin: `2f98ce3e8e74491956b5baaa3fc710a98add9fa8dba63f7c744fcc970d884332`

No private course packet, local test workspace, transcript, or new student learning record is included in the downloads. The already-public examples remain separate from the skill/plugin archives.

## Behavioral limits

The local GPT-6 Luna statistics run occurred before the HTML-mock/PDF-guide defaults. It exercised question feedback, a weak concept, a requested concept page in Chrome, reviewed attempt import, a six-question Markdown mock, and a Markdown guide. It cannot establish adherence to the new formats.

The run exposed initial incorrect grading corrected after a student challenge, inaccurate assistance/version labels in exports, an import entry placed in Concepts instead of Import ledger, and an initially incomplete guide. Instructions now clarify these checks, but no fresh model run proves those reliability issues resolved. Actual desktop plugin discovery, physical mobile/accessibility coverage, new-format generation, and student learning gains remain unverified. See [VALIDATION.md](../../../VALIDATION.md) for the older evidence and its limits.
