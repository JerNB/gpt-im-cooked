# New-arm exam-sheet rerun on the native PDF engine — 2026-11-19

**Exploratory, n = 2 sessions × 4 turns, synthetic STA course, one scripted student, tutor model `gpt-6-luna` (medium), Codex CLI 0.162.1.** Same fixtures, prompts, isolation and scoring as the T016 pilot ([report](../2026-11-18-feature-pilot/REPORT.md)) and the first rerun ([report](../2026-11-19-sheet-rerun/REPORT.md)).

- Skill under test: `337022d` on `cc/T017-sheet-print-fallback` (PR #10). It adds the standard-library PDF writer `scripts/sheet_pdf.py`; codex approved it in review round 5.
- Runner: `tests/run_sheet_rerun.py --rev 337022d`.
- The host's system Python still has no ReportLab.
- No separate smoke turn: the same harness passed a smoke turn earlier the same day.
- Runs and scoring: cc. No blind second reviewer.

All 8 turns completed: no quota failure, no rerun, no global-skill access, and no package installation.

## Headline

- **PDFs are now produced inside the Codex sandbox: 2 of 2 first drafts.**
  - Both first drafts were rendered by `render_sheet.py` with `engine=native`, the first draft in turn 2 after the allowance answer.
  - Rep 1: 1 page, 11 pt. Rep 2: 2 pages, 11 pt.
  - The T016 pilot and the first rerun produced 0 of 2.
- **Ask, then wait: 2 of 2.** Turn 1 asked only the allowance question and ended the turn.
- **Preferences saved: 2 of 2** (`Reference-sheet preferences` after the revision). **Reused in a fresh session: 2 of 2**: both turn-4 replies cite or follow the saved preference.
- **New issue: no room to grow.** Both revisions freed space, but the largest preset is 11 pt. Both revised sheets fill about one column of one page and leave the rest empty.
  - Rep 1 reported that 11 pt is the maximum.
  - Rep 2 copied `render_sheet.py`, edited its presets to 15 pt and delivered that PDF (turn 3). That breaks the rule against hand-building a layout program, and its turn-4 reply linked this hand-patched v2 instead of the renderer's own v3.

## Checks

| Check | rep 1 | rep 2 |
|---|---|---|
| S1a one allowance question, then end the turn | pass | pass |
| S1b no content-plan approval request | pass | pass |
| S2 first draft is a PDF of 2 pages or fewer via `render_sheet.py` | pass (turn 2, 1 page, `engine=native`) | pass (turn 2, 2 pages, `engine=native`) |
| S2b no install without asking | pass | pass |
| S4 revision applied, no new topics (tutor-reported; sources checked by cc, not blind) | pass | pass in content, but the PDF came from a **hand-patched renderer** (15 pt presets) |
| S5 preference saved / reused in turn 4 | pass / pass | pass / pass (but linked the turn-3 v2 PDF, not its new v3) |

S3 (blind content quality) is not scored. cc looked at the renderer-made PDFs (rep 1 v1 and v3, rep 2 v1 and v3), rendered with pypdfium2 outside the run:

- The layout matches the design: two columns, tinted high-priority headings, staged grids, extractable text.
- **Equal-width table columns split words** ("Commuter / s", "Noncomm / uters").
- Tall worked examples kept together leave large gaps at the bottom of a column.

## Resources (descriptive; CLI counters, not a bill)

| Session | Turn 1 | Turn 2 | Turn 3 | Turn 4 | Tokens (all turns) |
|---|---|---|---|---|---|
| rep 1 | 85 s | 93 s | 74 s | 78 s | 960,961 |
| rep 2 | 109 s | 178 s | 344 s | 124 s | 2,235,622 |

8 turns: 3,196,583 processed tokens. Rep 2's turn 3 is the largest at about 1.1M tokens: it read and patched the renderer.

## Findings

1. **Larger presets for sparse sheets.** Add presets above 11 pt (for example 12-14 pt), so that freed space becomes larger type, as `review-artifacts.md` promises. Also state the cap in the reference, so tutors do not patch the renderer.
2. **Table column widths.** Size table columns by content (at least the longest word in each column, where the total width allows it) instead of equal shares.
3. **Never modify the renderer.** Add an explicit rule to `review-artifacts.md`: do not copy or edit `render_sheet.py`; if the layout cannot meet a request, say so.
4. **Link the newest round.** Deliver the PDF the renderer just wrote (the highest `revision.round`).

## Not measured

Learning gains, real students, other models, macOS/Linux sandboxes, viewers other than PDFium, paper printing, blind content quality.

## Evidence

`protocol.json`, `results-*.json`, `runs/<session>/` (prompts, sanitized JSONL events, responses, per-turn snapshots including the PDFs), and the frozen `skill-New/` (337022d). `skill-Old/` is unused; the shared runner prepares both. Private home-directory prefixes, host names and Windows SIDs in evidence files were replaced with placeholders. Links into temporary session folders were turned into plain text.
