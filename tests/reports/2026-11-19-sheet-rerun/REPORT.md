# New-arm exam-sheet rerun on the T017 skill — 2026-11-19

**Exploratory, n = 2 sessions × 4 turns, synthetic STA course, one scripted student, tutor model `gpt-6-luna` (medium), Codex CLI 0.162.1.** Same fixtures, prompts, isolation and scoring as the T016 pilot ([report](../2026-11-18-feature-pilot/REPORT.md)). The only change is the skill revision: `c72a32a`, branch `cc/T017-sheet-print-fallback` (PR #10, codex-approved), which adds a browser print engine to `render_sheet.py`. Runner: `tests/run_sheet_rerun.py`, a wrapper that reuses `tests/run_feature_pilot.py` unchanged. One smoke turn is kept separately in `../2026-11-19-sheet-rerun-smoke/` and is excluded from these results. The host's system Python has no ReportLab, as in T016. Runs and scoring: cc. No blind second reviewer.

All 8 turns completed: no quota failure, no rerun, no global-skill access.

## Headline

- **Still no PDF (0 of 2 sessions).** Inside the Codex Windows sandbox (`windows.sandbox="unelevated"`), headless Edge does not start. It produces no PDF, and a tutor-run probe logged `FATAL ... platform_channel ... (0x5)` (access denied).
  - cc reproduced this without the model: the same Edge print succeeds outside the sandbox and fails inside `codex sandbox`, with or without `--no-sandbox`.
  - On top of that, `render_sheet.py` crashed with a Python traceback (`PermissionError` while removing its temporary work folder) instead of a clean `ERROR` line.
  - So the T017 browser engine works on the host but not in the sandbox where the tutor runs.
- **The tutors handled the failure honestly (2 of 2).** Both delivered the printable HTML. Both said that no PDF was made and that the page count was unverified, and pointed the student to Print > Save as PDF. Neither installed anything.
- **Ask, then wait: 2 of 2** (T016: 1 of 2 asked, and neither stopped). Turn 1 asked only the exact allowance question and ended the turn.
- **Revision and preferences.**
  - Both turn-3 revisions applied the request without new topics, by the tutors' own account and the turn-3 sources. This was not diffed blind.
  - Rep 1 saved a `Reference-sheet preferences` section. Rep 2 said it saved the preference, but no such section exists in its profile. Both turn-4 sessions drafted again from the saved profile.

## Checks

| Check | rep 1 | rep 2 |
|---|---|---|
| S1a one allowance question, then end the turn | pass | pass |
| S1b no content-plan approval request | pass | pass |
| S2 first draft is a PDF of 2 pages or fewer via `render_sheet.py` | **fail**: traceback (temp-folder `PermissionError`); browser print blocked by the sandbox; printable HTML delivered and labelled unverified | **fail**: same; the tutor's own Edge probe hit `FATAL` access denied |
| S2b no install without asking | pass (nothing installed) | pass |
| S4 revision applied, no new topics (tutor-reported) | pass | pass |
| S5 `Reference-sheet preferences` saved | pass | **fail** (claimed, but not in the file) |

S3 (blind content quality) is not scored: no PDF exists.

## Resources (descriptive; CLI counters, not a bill)

| Session | Turn 1 | Turn 2 | Turn 3 | Turn 4 | Tokens (all turns) |
|---|---|---|---|---|---|
| rep 1 | 93 s | 195 s | 64 s | 54 s | 1,344,989 |
| rep 2 | 166 s | 238 s | 114 s | 62 s | 1,900,700 |

8 turns: 3,245,689 processed tokens. Turn 2 is heavy (0.7-1.0M) because the tutors read `render_sheet.py` and retried the renderer several times after the crash.

## Correction to the T016 report

The T016 report said v2.0.1 "printed a PDF through the browser". This is wrong. In both Old-arm sessions the tutor made the PDF with **PyMuPDF** (`import fitz`), which happens to be installed in this host's system Python, and no browser print command appears in those logs. The comparison in T016 was therefore "new renderer without ReportLab" versus "old free-form rendering with a library this host happens to have". It was not evidence that browser printing works in the sandbox.

## Findings

1. **A PDF path that works inside the sandbox is still missing.** Browser printing cannot run under the Codex Windows sandbox. The options are a dependency-free PDF writer in pure Python, or running the print with the host's escalation or approval, or both. Release blocker for advertising the sheet.
2. **`render_sheet.py` must not crash on temp-folder cleanup.** It should use `ignore_cleanup_errors=True` and convert a browser start failure into a clean `ERROR` that names the sandbox, so the skill's no-engine flow applies.
3. **Preference save claimed but not written** (rep 2): a record write needs read-back, as `state.md` already asks.

## Not measured

Learning gains, real students, other models, macOS/Linux sandboxes, sheet layout quality (no PDF), paper printing.

## Evidence

`protocol.json`, `results-*.json`, `runs/<session>/` (prompts, sanitized JSONL events, responses, per-turn snapshots, usage), frozen `skill-New/` (c72a32a) and `skill-Old/` (unused). The run did not need the `skill-Old` arm. It is archived because the shared runner prepares both. Private home-directory prefixes in evidence files were replaced with `<HOME>`. Links into temporary session folders were turned into plain text.
