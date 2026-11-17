# Exam Reference Sheet Renderer Implementation Plan (T011)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make exam sheets and study guides from a short content JSON with a script that fits the page count, checks the result and renders previews, and rewrite the skill's sheet rules from the maintainer's revision lessons.

**Architecture:** `render_sheet.py` validates content with the standard library only, then lazily imports ReportLab to lay out blocks in two columns (sheet) or one (guide), trying layout presets from most to least spacious and keeping the largest that fits. It writes the PDF, `checks.json` and, when pypdfium2 is available, page PNGs. The skill text gains the one-question default, tiered content rules, a revision protocol and a preferences section saved through `record_io.py`.

**Tech Stack:** Python 3.10+; ReportLab (optional runtime dependency); pypdfium2 (optional, previews and test text extraction); plain-script tests.

**Spec:** `tests/REFERENCE-SHEET-DESIGN.md` (approved by human 2026-11-16).

## Global Constraints

- Validation and markup code must import without ReportLab; only rendering imports it.
- Minimum sizes: body 9 pt, code 8.5 pt, unless the content's `allowance.rules` gives an instructor minimum, which wins.
- Exam sheet default: `sheets: 1, sides: 2` → exactly 2 pages, US Letter unless `paper: "a4"`; two columns.
- Study guide (`kind: "study-guide"`): one column, no page cap, no fitting.
- Unconfirmed allowance → footer `Exam use unconfirmed — check your instructor's rules.` on every page.
- No personal labels, scores or private comments in printable output.
- Missing ReportLab → `ERROR reportlab is not installed; ask the student before running pip install reportlab` exit 3; never install from the script.
- Result line: `OK pages=<n> preset=<i> body=<pt>pt out=<path>` (exit 0), `OVERFLOW over=<pt>pt sections=<id>:<pt>,...` (exit 2), `ERROR <reason>` (exit 1/3); no traceback for bad input.
- Package allowlist in `scripts/build_packages.py`; do not rebuild `docs/downloads/`.
- Repo content is English; claim locks in `.collab/LOCKS.md` before editing.
- Dev environment: a local virtualenv (`.venv/`, gitignored) with `reportlab` and `pypdfium2`. Installing them needs the human's OK.

## Review Focus

1. Content using Greek letters, `≤`, `→`, `²` → rendered with a Unicode TTF, not boxes; a character no discovered font covers → listed in `checks.json` `missing_glyphs` and a warning in the result (Task 3 `test_unicode_glyphs`).
2. A single block taller than a column (huge table or code) → `OVERFLOW` naming that section, not an infinite loop or a silently clipped block (Task 4 `test_block_taller_than_column`).
3. Chinese explanation text (`language: "zh"`) → CID font used, no boxes (Task 3 `test_cjk`).
4. Re-rendering round 2 into the same folder → round-1 PDF kept, new `-v2.pdf` written (Task 5 `test_versions_kept`).
5. Inline markup with unbalanced `**` or a literal `<` → escaped text, never a ReportLab parse error (Task 1 `test_inline_escaping`).

---

### Task 1: Content format, validation and inline markup

**Files:**
- Create: `plugins/gpt-im-cooked/skills/gpt-im-cooked/scripts/render_sheet.py`
- Create: `plugins/gpt-im-cooked/skills/gpt-im-cooked/assets/sheet-example.json`
- Test: `tests/check_sheet_render.py`

**Interfaces:**
- Produces: `class SheetError(ValueError)`; `FORMAT = 'gpt-im-cooked-sheet/1'`; `BLOCKS = {'cue','text','stages','example','table','code','mistake'}`; `load_sheet(data: dict) -> dict` (normalised copy with defaults: `allowance.status='unconfirmed'`, `sheets=1`, `sides=2`, `paper='letter'`, `language='en'`, section `weight='normal'`, `revision.round=1`); `inline(text: str) -> str` returning ReportLab paragraph markup.

Block shapes: `cue{text}`, `text{text}`, `stages{steps:[{label,text}]}`, `example{setup, steps:[{label,text}], takeaway?}`, `table{header:[str], rows:[[str]]}` (rectangular), `code{text}`, `mistake{prompt?, first_error, fix, conditions?}`. `inline`: XML-escape first, then `**x**` → `<b>x</b>`, `` `x` `` → `<font face="{mono}">x</font>`, `_{x}` → `<sub>x</sub>`, `^{x}` → `<super>x</super>`; unmatched markers stay literal. The example is a synthetic two-page statistics sheet (no real course content) with one `high` section using `stages` and `example`, `cue`s, one `table`, one `code` block, and an `omitted` entry.

- [ ] **Step 1: Failing tests** in `tests/check_sheet_render.py` (scaffold as `tests/check_mock_render.py`; tests needing ReportLab are grouped in a function that prints `SKIP rendering checks: reportlab not installed` and returns when the import fails, so the script still prints `PASS` for the rest):
  - `test_example_valid`: `load_sheet(EXAMPLE)` ok.
  - `test_rejects_*` with substrings: bad `format` → `"format"`; unknown block type → `"block type"`; ragged table → `"table"`; empty sections → `"sections"`; `kind` not `exam-sheet`/`study-guide` → `"kind"`; duplicate section id → `"duplicate"`; `weight` `"huge"` → `"weight"`; `sides` 3 → `"sides"`.
  - `test_inline_markup`: `inline('**R²** uses `tidy()` and e^{0.4}, x_{i}')` contains `<b>R²</b>`, `<font face=`, `<super>0.4</super>`, `<sub>i</sub>`.
  - `test_inline_escaping`: `inline('a < b & **c')` == `'a &lt; b &amp; **c'`.
- [ ] **Step 2:** `python tests/check_sheet_render.py` → FAIL (module missing).
- [ ] **Step 3:** Implement `SheetError`, `load_sheet`, `inline`, the example.
- [ ] **Step 4:** Run → `PASS` (rendering group skipped if no ReportLab).
- [ ] **Step 5:** Commit `feat: reference-sheet content format and markup [T011]`.

### Task 2: Dev environment

- [ ] **Step 1:** With the human's OK: `python -m venv .venv` and `.venv/Scripts/python -m pip install reportlab pypdfium2`; confirm `.venv/` is ignored (`git check-ignore .venv`), adding it to `.gitignore` in this task's commit if not.
- [ ] **Step 2:** `.venv/Scripts/python tests/check_sheet_render.py` → `PASS` (still no rendering tests yet).

### Task 3: Fonts and glyph coverage

**Files:**
- Modify: `.../scripts/render_sheet.py`
- Test: `tests/check_sheet_render.py`

**Interfaces:**
- Produces: `find_fonts(language: str) -> dict` returning `{'body': name, 'bold': name, 'mono': name, 'files': {name: path}}` after registering with ReportLab; `missing_glyphs(text: str, font_name: str) -> set[str]`.

Candidates in order — Windows `%WINDIR%/Fonts`: `segoeui.ttf`/`segoeuib.ttf`, `arial.ttf`/`arialbd.ttf`, mono `consola.ttf`; macOS `/System/Library/Fonts/Supplemental/Arial.ttf`/`Arial Bold.ttf`, mono `/System/Library/Fonts/Menlo.ttc` (subfont 0) or `Courier New.ttf`; Linux `/usr/share/fonts/**/DejaVuSans.ttf`/`DejaVuSans-Bold.ttf`/`DejaVuSansMono.ttf`. Fallback: built-in Helvetica/Courier (and every non-Latin-1 character then counts as missing). `language: "zh"` → body/bold `UnicodeCIDFont('STSong-Light')`, mono unchanged. Coverage check via the TTF face's character map; CID font treated as covering CJK + ASCII.

- [ ] **Step 1: Failing tests** (rendering group): `test_fonts_found` (body font is not Helvetica on Windows/macOS/Linux CI hosts that have one of the candidates; otherwise assert the fallback path reports missing glyphs for `'β'`); `test_unicode_glyphs`: `missing_glyphs('β ≤ → ²', body) == set()` when a TTF was found; `test_cjk`: `find_fonts('zh')['body'] == 'STSong-Light'` and `missing_glyphs(CJK_SAMPLE, 'STSong-Light') == set()` where `CJK_SAMPLE` is a four-character Chinese phrase written with Python unicode escapes (`validate_package.py` rejects CJK characters in repo text).
- [ ] **Step 2:** Run with `.venv` → FAIL. **Step 3:** Implement. **Step 4:** Run → `PASS`.
- [ ] **Step 5:** Commit `feat: font discovery and glyph checks for sheets [T011]`.

### Task 4: Layout and auto-fit

**Files:**
- Modify: `.../scripts/render_sheet.py`
- Test: `tests/check_sheet_render.py`

**Interfaces:**
- Consumes: `load_sheet`, `inline`, `find_fonts`.
- Produces: `PRESETS: list[dict]` (keys `body`, `leading`, `code`, `code_leading`, `gap`, `section_gap`, `high_scale`); `class Overflow(Exception)` with `.over_pt: float` and `.sections: list[tuple[str, float]]`; `layout(sheet: dict, fonts: dict, preset: dict) -> tuple[list, int]` (flowables, page count); `fit(sheet: dict, fonts: dict) -> dict` returning `{'preset': index, 'pages': n, 'column_fill': [float], 'body': pt, 'code': pt}` or raising `Overflow`.

Presets (index 0 most spacious): body 11.0, 10.5, 10.0, 9.5, 9.0 pt with leading 1.22× body; code 9.5, 9.25, 9.0, 8.75, 8.5 pt; gaps scale from 6 down to 3 pt. `high` sections: title 1.15× and body 1.08× of the preset (never below minimums), light tinted box; `low`: preset body. Exam sheet: two equal columns, 0.5 in margins, header line with title/course, footer as in Global Constraints; `stages`, `example`, `table`, `mistake` blocks wrapped in `KeepTogether`; code is `Preformatted` without wrapping. `fit` builds into an in-memory buffer for each preset in order and returns the first whose page count `<=` target; if even the last overflows, measure per-section heights at the last preset and raise `Overflow` with the excess. A block taller than one column raises `Overflow` naming its section immediately. Study guide: one column, preset 1, no fitting.

- [ ] **Step 1: Failing tests** (rendering group):
  - `test_example_fits_two_pages`: `fit(EXAMPLE)['pages'] == 2`.
  - `test_cut_content_grows_type`: delete the two longest sections → returned `body` `>` original `body`.
  - `test_overflow_reports_sections`: duplicate every section 4× → `Overflow`; `.sections` lists section ids with positive heights; `.over_pt > 0`.
  - `test_minimum_sizes`: for every preset `body >= 9` and `code >= 8.5`; an `allowance.rules` minimum of `10` removes smaller presets.
  - `test_block_taller_than_column`: a 200-row table → `Overflow` naming its section.
  - `test_study_guide_unbounded`: `kind: "study-guide"` with the 4× content → no exception, pages `> 2`.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implement. **Step 4:** Run → `PASS`.
- [ ] **Step 5:** Commit `feat: two-column layout with automatic page fitting [T011]`.

### Task 5: Output files and command line

**Files:**
- Modify: `.../scripts/render_sheet.py`
- Test: `tests/check_sheet_render.py`

**Interfaces:**
- Produces: `render(sheet: dict, out_dir: Path, force: bool = False) -> dict` (the `checks.json` content: `pages`, `preset`, `body`, `code`, `column_fill`, `fonts`, `missing_glyphs`, `allowance`, `previews: [paths] | null`, `pdf`); `main(argv: list[str] | None = None) -> int` with `render_sheet.py SHEET.json --out DIR [--force]` and `--check` (validation + fit, no files).

Files: `<slug(title)>-v<round>.pdf`; `<slug>-v<round>.json` (content copy); `previews/<slug>-v<round>-page-<n>.png` at 150 dpi when pypdfium2 imports, otherwise `previews: null` and the result line appends ` previews=none`; `checks.json` (overwritten each round). An existing PDF for the same round → `ERROR` unless `--force`; other rounds are never touched. Missing glyphs → still `OK`, result line appends ` missing_glyphs=<n>`.

- [ ] **Step 1: Failing tests:**
  - `test_cli_ok` (rendering group, subprocess): exit 0, `^OK pages=2 preset=\d body=`, PDF + checks + previews exist.
  - `test_footer_unconfirmed`: text extracted with pypdfium2 from each page contains `Exam use unconfirmed`; with `allowance.status: "confirmed"` it does not.
  - `test_versions_kept`: render round 1, then round 2 into the same dir → both PDFs exist; re-render round 2 without `--force` → exit 1.
  - `test_cli_overflow`: 4× content → exit 2, stdout starts `OVERFLOW over=`.
  - `test_cli_errors` (no ReportLab needed): malformed JSON and invalid content → exit 1, `ERROR`, no `Traceback` on stderr.
  - `test_cli_no_reportlab` (no ReportLab needed): run with `-c` wrapper that blocks the `reportlab` import (`sys.modules['reportlab'] = None`) → exit 3, message contains `ask the student before running pip install reportlab`.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implement. **Step 4:** Run with `.venv` and with system Python (no ReportLab) → both `PASS` (system run prints the SKIP line).
- [ ] **Step 5:** Open the example PDF and previews; note what was inspected in the commit body.
- [ ] **Step 6:** Commit `feat: render_sheet outputs, previews and CLI [T011]`.

### Task 6: Optional profile section in `record_io.py save`

**Files:**
- Modify: `.../scripts/record_io.py`
- Modify: `.../references/state-reference.md` (one line documenting it)
- Test: `tests/check_state_io.py`

**Interfaces:**
- Produces: in `save`, a `profile` (or `record`) section named in `OPTIONAL_SECTIONS = {'Reference-sheet preferences'}` that does not exist is appended at the end of the file as `## <name>\n\n<text>` for modes `replace` and `append`; any other missing section still fails with the existing "not found" error.

- [ ] **Step 1: Failing tests** in `tests/check_state_io.py`: `test_save_creates_optional_section` (profile from the shipped template without the section; save `{"profile": {"Reference-sheet preferences": {"mode": "append", "text": "- Prefers one worked example"}}}` → section exists once at the end, other sections byte-identical, hash/backup behaviour as for other saves); `test_save_missing_other_section_still_fails`.
- [ ] **Step 2:** Run `python tests/check_state_io.py` → FAIL. **Step 3:** Implement. **Step 4:** Run → `PASS`.
- [ ] **Step 5:** Commit `feat: create the optional sheet-preferences section on save [T011]`.

### Task 7: Skill instructions and packaging

**Files:**
- Modify: `.../references/review-artifacts.md`: output table row "Make a study guide / cheat sheet → ask the one allowance question; default one two-sided exam sheet PDF marked unconfirmed; 'just for review' → study guide PDF"; replace "Content hierarchy" with spec §5.2 rules; replace the "Layout and verification" checklist with: run `render_sheet.py`, react to `OVERFLOW` by cutting/demoting the named sections (never below minimum size), view each page preview once for the spec §5.5 exam-tool check, report only what was inspected, fallback rules when ReportLab is absent (ask before installing; otherwise labelled editable source); add "Revision rounds" (spec §5.1 step 6) and "Preferences" (spec §5.4 format, saved at the round's checkpoint, read before every sheet/guide, offer to reuse general ones across courses).
- Modify: `.../SKILL.md` §7 and the exam-room paragraph: the one question, no content-plan confirmation before the first draft, pointer to the renderer.
- Modify: `scripts/build_packages.py` `SKILL_FILES` += `scripts/render_sheet.py`, `assets/sheet-example.json`.

- [ ] **Step 1:** Write the changes.
- [ ] **Step 2:** Isolated-copy `python tests/validate_package.py` → `PASS`.
- [ ] **Step 3:** `python scripts/build_packages.py --output <scratch>`; confirm both new files are in the skill ZIP. Do not touch `docs/downloads/`; skip `check_distribution.py`.
- [ ] **Step 4:** All existing regressions from `CLAUDE.md` (except `check_distribution.py` and the benchmark) → `PASS`.
- [ ] **Step 5:** Commit `feat: exam-sheet rules, revision rounds and preferences [T011]`.

### Task 8: Handoff

- [ ] **Step 1:** `.collab/handoff/T011.md` (changes, commands and results, not verified: fonts on macOS/Linux hosts, paper printing, fresh-model behaviour and speed). TASKS.md T011 → REVIEW, release locks, LOG entry.
- [ ] **Step 2:** Push only when the human asks.
