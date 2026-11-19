# Sheet PDF without ReportLab, and pilot wording fixes (T017)

Status: plan, cc, 2026-11-19. Source: findings 1-5 of the T016 pilot (`tests/reports/2026-11-18-feature-pilot/REPORT.md` on `codex/T016-feature-pilot`). The human chose to add a browser fallback before the release and the post.

## Problem

`render_sheet.py` needs ReportLab. On the pilot host (no ReportLab), the new skill delivered JSON/Markdown sources in 2 of 2 sessions and never asked to install, while v2.0.1 printed a PDF through the browser in 2 of 2. Many student machines will look like the pilot host.

## Design

**Engines.** `--engine auto|reportlab|browser` (default `auto`): ReportLab when importable, otherwise the browser engine. `--browser PATH` overrides discovery.

**Browser engine.**

- `to_html(sheet, preset)` writes one self-contained HTML document from the same content JSON: the same presets (body, code, gaps), two CSS columns for an exam sheet and one for a guide, high-weight headings tinted and larger, `stages`/`example`/`mistake` as label grids, tables, cue bullets. `@page` sets paper and margins, and its margin boxes carry the title, course, the "Exam use unconfirmed" note and page numbers. Headings stay with their first block, and blocks avoid column breaks. No external assets.
- `find_browser()` looks for Microsoft Edge, Google Chrome or Chromium in the usual Windows, macOS and Linux locations and on `PATH`.
- Printing runs the browser headless with a temporary profile, so no profile ends up in the study folder (T016 smoke 2). The output PDF is kept only when it is complete, with a trailing `%%EOF` and a stable size. On Windows the Edge launcher returns before the PDF exists, so the engine waits for the file, up to a timeout.
- Fitting uses the same rules as ReportLab: the same candidate presets, minimum body size, guide start preset and page target. Each candidate is printed and its pages counted from the PDF's page tree. The most spacious preset that fits wins. A code line wider than a column is estimated from the monospace advance width (0.6 em) and reported as the same `OVERFLOW ... reason=a code line ...`. Overflow from page count reports `sections=` empty with `reason=content is taller than the allowed pages (browser engine)`.
- Outputs: the same as ReportLab (`<slug>-v<round>.pdf`, `.json` copy, `checks.json`, previews when pypdfium2 exists), plus `<slug>-v<round>.html`, the printable source. `checks.json` adds `engine` and `browser` (program name only, no path), and records `missing_glyphs: "unchecked"` (browsers substitute fonts) and `column_fill: null`.
- **Neither engine:** write the printable HTML, print `ERROR no PDF engine: ...` and exit 3. The message gives the exact install question, so a tutor can relay it.

**Skill wording.**

1. `review-artifacts.md` and `SKILL.md`: the renderer prints through ReportLab or an installed Edge/Chrome. On exit 3, deliver the printable HTML labelled "not a PDF yet" and ask exactly: "I can make the PDF if you let me install one Python package (`pip install reportlab`). Install it?" Then end the turn.
2. **Ask, then wait** (sheet allowance question and calendar availability question): ask in the reply text and end the turn. Use the default only when the student's next message skips or cannot answer. Do not use a separate question tool that may return no answer.
3. `study-plan.md` Deliver: the unrecorded-course offer becomes part of the delivery message, made once per plan. The Gather step points to it.
4. `plan_study.py`: `exam.end` may be omitted. A 3-hour duration is assumed, and the `.ics` description and HTML say so. `study-plan.md` says to state the assumption instead of asking or inventing an end time.

## Tests (red first)

- `check_sheet_render.py` (standard library, no browser): HTML structure, escaping, inline code literal, presets in CSS, unconfirmed note, columns by kind. Fit selection with a fake browser that writes a minimal PDF whose page count depends on the preset. Overflow when no preset fits. Code-width estimate overflow. Exit 3 with HTML written and the exact question when neither engine exists. An incomplete or never-written PDF fails with an `ERROR`. No profile directory is left in the output.
- Real-browser checks run when a Chromium browser is found (skipped otherwise): the example renders to 2 pages or fewer, with header, footer and text present.
- `check_study_plan.py`: missing `exam.end` is accepted, and the assumed end appears in the `.ics` and HTML. An explicit end is unchanged.

## Review round 1 (codex, REQUEST_CHANGES) and changes

1. Long tokens could overflow a column: tables now use a fixed layout, and cells, prose and inline code wrap anywhere. A real-browser check confirms that every character on page 1 stays inside a column (needs pypdfium2).
2. A code block taller than a column passed browser fitting: its height is now estimated per preset, and it is rejected with the ReportLab reason, for sheets and guides. Other blocks taller than a column continue in the next column and are never clipped.
3. A detached browser child could outlive a timeout and keep its profile: the processes whose command line names the throwaway profile are stopped, the profile is removed, and a profile that cannot be removed is reported (`leftover_profiles`). The fake launcher now detaches a delayed or hanging child that holds the profile.

## Review round 2 (codex, REQUEST_CHANGES) and changes

1. A read error while waiting for the PDF skipped cleanup: cleanup now runs in `finally`. A read error (for example a Windows sharing violation) is retried until the deadline and then reported as a `SheetError`.
2. The code-height check ignored padding and wrapping: the width check now uses the column minus the code padding, tabs are 4 spaces in both the estimate and the CSS, and the height counts wrapped lines at a 0.60 em fallback font width.
3. `review-artifacts.md` says which blocks the browser engine checks.

## Not covered

Glyph coverage in the browser engine, print layout on paper, and browsers other than Chromium (Firefox has no headless print-to-PDF). A short re-run of the New sheet sessions on `gpt-6-luna` (8 turns) follows the codex review and gives the post its sheet screenshot.
