# Exam reference sheet and study-guide PDF — design (T011)

Status: **design for human approval; nothing implemented.** Author: cc. Base: `origin/main` at `627bca5` (v2.0.1). Branch: `cc/T010-T011-design`. Decisions marked *(human)* were made by the maintainer in conversation on 2026-11-16; everything else is cc's proposal.

## 1. Why

Two problems, both observed on the maintainer's own use of the skill:

1. **Too many revision rounds.** A two-page statistics exam sheet needed two annotation rounds and 15 edits before it was usable (maintainer's local revision history, 2026-11-16; not committed because it is personal study material). Almost every edit removed or compressed content, asked for one worked example instead of abstract rules, or asked to spend freed space on readability rather than new material. The current rules push the other way: "include a few compact examples, fragile distinctions, common pitfalls…", with no notion of depth tiers, visual priority, or leaving space empty, and no place to remember what the student already asked for.
2. **Too slow.** From that Codex session's log: first draft 14.7 min (21 tool calls), first revision 7.8 min (8 calls), second revision 4.8 min (15 calls) — about 27 minutes. The model wrote a 228-line ReportLab program from scratch (about 28k output tokens in the draft turn), hand-tuned per-column font sizes, line spacing and gaps to hit exactly two pages, and applied each revision as string-replacement patches on that program. The session was already ~380k tokens deep, so every tool call re-processed that context. One session, one course; the cause analysis is from its files and log, not a controlled measurement.

The sheet is also the second feature for the public post planned for 2026-11-20.

## 2. Goals, non-goals, anti-goals

Goals:

- G1. **Default to an exam-room sheet** *(human)*. A "study guide / review guide / cheat sheet" request gets exactly one question before drafting: "Is this a cheat sheet you'll bring into the exam? How many sheets, one- or two-sided?" If the student does not know or skips, build **one two-sided sheet (two pages)** and mark it *exam use unconfirmed* *(human)*. Only "it's just for reviewing, not for the exam" produces a full study guide.
- G2. **No content-plan confirmation before the first draft** *(human)*: generate directly; the student revises the PDF.
- G3. Fewer revision rounds: the first draft should already follow the content rules in §5.2, and every lasting preference the student states during revision is saved and applied to the next sheet.
- G4. Faster drafts and revisions: the model writes content only; a script does layout, page fitting, checks and previews. A revision is a content edit plus one render.

Non-goals:

- Proving an optimal sheet design or measuring exam outcomes.
- Typesetting arbitrary LaTeX. Formulas use Unicode text, sub/superscript markup and tables; complex derivations are out of scope for v1.
- Changing the mock-exam path or the learning-record format.

Anti-goals:

- Shrinking every font to fit more material. Below the minimum size the script refuses and asks for cuts.
- Treating a student's "leave this off my sheet" as an instructor-confirmed exam exclusion, or dropping a concept because only its code syntax was removed.
- Adding new topics because space became free after a deletion.
- Claiming a sheet is permitted in the exam when the allowance is unconfirmed.

## 3. Constraints

- The package currently needs only the Python standard library. PDF layout needs a measuring layout engine; **ReportLab** is the proposed optional dependency (see §4). Installing it changes the student's environment, so the skill asks before running `pip install reportlab`. If it is missing and not installed, fall back to the existing rule: a clearly labelled editable source with the specific limitation stated.
- Glyph coverage: ReportLab's built-in Helvetica/Courier are Latin-1 only, so Greek letters, ≤, → and similar would render as boxes. The script must locate a Unicode TTF on the host (Windows: Segoe UI / Arial / Consolas; macOS: Arial / Menlo from `Supplemental`; Linux: DejaVu) and use ReportLab's built-in CID font for Chinese when the student asked for Chinese explanations. Missing glyphs are a check failure, not a silent box.
- Student data never enters the package; the sheet content file lives in the student's study directory.
- New files must be added to `scripts/build_packages.py` `SKILL_FILES`.

## 4. Approaches considered

| | How | Trade-off |
|---|---|---|
| **A (chosen)** | **Content JSON → `scripts/render_sheet.py` (ReportLab) → PDF + PNG previews + checks** | Native text measurement makes automatic page fitting and per-section overflow reports straightforward. Cost: optional third-party dependency and a font-discovery step |
| B | Content JSON → self-contained HTML with print CSS → headless Chrome/Edge `--print-to-pdf` | Best typography (system fonts, SVG, MathML) and the HTML doubles as editable source; but finding which section overflows needs a JS measurement round-trip through the browser, and browser discovery varies by host |
| C | Keep model-written layout, only tighten the rules | Fixes some revision rounds; leaves the 15-minute hand-built layout and its per-session inconsistency |

A matches what the Codex host already had installed (ReportLab, pypdf, Poppler were used in the measured session) and the mock-exam split (model writes JSON, script renders and checks). B stays the candidate if ReportLab proves unavailable on common hosts.

## 5. Design

### 5.1 Flow

1. Request arrives. Save pending evidence (existing artifact checkpoint). Read the course profile's *Reference-sheet allowance* and *Paper size / typed or handwritten / content restrictions*, and its *Reference-sheet preferences* (§5.4).
2. If the allowance is unknown, ask the one G1 question; do not ask anything else. Record the answer in the course profile.
3. Choose content by §5.2 from the course scope, the learning record and the student's preferences. Write the content JSON (§5.3).
4. Run `render_sheet.py`. On `OVERFLOW`, cut or demote the lowest-value blocks the report names and re-run — never lower the minimum font. On success, look at the full-page previews once (one image per page) for the exam-tool check in §5.5.
5. Deliver the PDF link, one line on what was personalised, the allowance status, and any coverage gaps.
6. **Revision rounds:** apply exactly the requested edits to the content JSON; keep standing constraints from earlier rounds (for example "no new information") active; re-render. Saved space is not refilled — the renderer automatically uses it for a larger type size and spacing (§5.3). Durable preferences from the round are saved (§5.4).

### 5.2 Content rules (replaces "Content hierarchy" and parts of "Corrected mistakes" in `review-artifacts.md`)

- **Start from retrieval need, not course coverage.** A topic earns space only if the student needs help finding, interpreting or applying it during a question. Confirmed in-scope topics that get no space are listed in the response, not silently dropped.
- **Tier every topic before writing:** *worked* (a short explained example), *cue* (one line: a sign rule, a definition, what a function returns), or *omit*. Choose by the learning record (errors, Needs practice, Recheck), instructor emphasis and the student's preferences. Easy facts get a cue, never a paragraph.
- **One running example per cluster.** Interpret related quantities (for example every coefficient of one model, its group equations and differences) on a single shared example with variables, units and baseline defined once, instead of several abstract templates or several unrelated contexts.
- **Stage multi-step conversions.** Show each stage on its own line and label what scale it is on (for example fitted value → log-odds → odds → probability).
- **Prominence follows importance.** High-priority or error-prone sections get more space, larger type or a table; low-priority cues stay compact.
- **No generic reminders.** Pitfalls and checklists appear only when tied to the student's recorded errors or explicit instructor emphasis.
- **Minimum sufficient explanation.** Enough to make the idea usable on the exam, no extended implications.
- **Empty space is allowed.** Never add material because there is room.
- **Scope precision.** Removing a code block does not remove the concept; a student's "leave it off" is a content preference, not an instructor exclusion; excluded-for-writing can still be needed for reading.
- Corrected-mistake units (existing rule) stay available, but on a sheet they usually compress to the corrected rule plus its condition.
- These rules apply to full study guides too; a guide simply has no page cap.

### 5.3 Content file and renderer

`render_sheet.py SHEET.json --out DIR [--force]` and `--check`. Input sketch:

```json
{
  "format": "gpt-im-cooked-sheet/1",
  "kind": "exam-sheet",
  "title": "STA 199 Exam 2", "course": "STA 199",
  "allowance": {"status": "unconfirmed", "sheets": 1, "sides": 2, "paper": "letter", "rules": null},
  "language": "en",
  "sections": [
    {"id": "logit", "title": "Logistic model: one worked profile", "weight": "high", "topics": ["T7"],
     "blocks": [
       {"type": "stages", "steps": [
         {"label": "Fitted value (log-odds)", "text": "−1.2 + 0.8(2) = 0.4"},
         {"label": "Odds", "text": "e^{0.4} = 1.49"},
         {"label": "Probability", "text": "1.49 / (1 + 1.49) = 0.60"}]},
       {"type": "cue", "text": "Slope 0.8: each +1 in x multiplies the **odds** by e^{0.8} = 2.23."}]}
  ],
  "omitted": [{"topic": "T9", "reason": "student preference, not instructor exclusion"}],
  "revision": {"round": 2, "standing": ["no new information"], "changes": ["R² reduced to one sentence"]}
}
```

- Block types: `cue`, `text`, `stages`, `example` (setup + steps + takeaway), `table`, `code`, `mistake`. Inline markup: `**bold**`, `` `code` ``, `x_{i}` / `e^{0.4}`. Images (PNG) optional; no SVG in v1.
- `weight` (`high` / `normal` / `low`) maps to type size, spacing and boxed emphasis.
- **Auto-fit:** for an exam sheet, try layout presets from most to least spacious (body 11 → 9 pt, code 9.5 → 8.5 pt, two columns, KeepTogether for stages/examples/tables) and use the **largest that fits the page count**. Content removed in a revision therefore turns into readability automatically. If the tightest preset still overflows, exit `OVERFLOW` listing each section's height and the overflow amount so the model knows what to cut. A study guide is one column, no page cap, no fitting.
- Footer on unconfirmed sheets: "Exam use unconfirmed — check your instructor's rules." No personal labels, scores or private comments in the printable output.
- Outputs: `<slug>-v<round>.pdf` (earlier rounds kept), the content JSON copy, `previews/page-N.png` when a rasteriser is available (pypdfium2 or Poppler; otherwise state that visual inspection was not possible), and `checks.json` (pages, preset, sizes, per-column fill, fonts used, missing glyphs, overflow).
- One result line: `OK pages=2 preset=3 body=10.0pt out=…`, `OVERFLOW …`, or `ERROR …`.

### 5.4 Remembering preferences

Add an optional section to the **course profile**, created on first use (existing profiles need no migration):

```markdown
## Reference-sheet preferences

Student content and style preferences for sheets and guides. These are not instructor scope decisions.

- Prefers one worked example over abstract interpretation rules (2026-11-16, sheet round 1)
- Keep freed space empty; do not add new information unless asked (2026-11-16, round 1)
- Leave off: ROC function syntax (concept stays) (2026-11-16, round 1)
```

Saved at the end of a revision round (part of the existing artifact checkpoint), read before every sheet or guide in that course. When the student starts a sheet in another course, the skill may offer once to reuse the general (non-topic) preferences.

### 5.5 Exam-tool check before delivery

Besides the script's checks: from the previews, confirm each section can be located by its heading at print size, `high` sections are visibly more prominent, staged calculations read top to bottom, and code is not wrapped mid-token. Report only what was actually inspected.

### 5.6 Skill text changes

- `review-artifacts.md`: output table row and routing for G1; §5.2 replaces "Content hierarchy"; "Layout and verification" points to the renderer and §5.5; revision-round rules (§5.1 step 6).
- `SKILL.md` §7: the one-question default and "no plan confirmation before the first draft".
- `assets/course-profile.md`: the optional preferences section; `assets/sheet-example.json`; `scripts/render_sheet.py`; allowlist.

## 6. Verification

- `tests/check_sheet_render.py` (no model calls; skipped with a clear message if ReportLab is absent): fixtures fit exactly two pages; removing a section increases the chosen body size; overflow at the tightest preset gives `OVERFLOW` with per-section heights; never below minimum sizes; Greek/≤/→ render with a discovered TTF and an unsupported glyph is reported; unconfirmed footer present; markup escaped; malformed JSON gives `ERROR`.
- Fresh-model comparison (codex, separate task, **requires human approval of model calls**): same synthetic course and the same scripted student request, v2.0.1 versus this design, fresh sessions, n ≥ 2 each. Measures: wall time and tool calls for the first draft and for one scripted revision round; whether the draft already follows §5.2 (scored from the PDF text by a reviewer who does not know the arm); preferences saved and applied to a second sheet. Descriptive counts only; the 27-minute session above is not used as the baseline because its context was unusually large.
- Screenshots from the comparison feed T013.

## 7. Done when

- [ ] Human approves this design.
- [ ] Renderer, example, rules, profile section and allowlist committed on a `cc/T011-*` branch; scratch package build and distribution check pass (release ZIPs untouched).
- [ ] `python tests/check_sheet_render.py` PASS on a host with ReportLab, and it skips cleanly without it; existing regressions pass.
- [ ] Codex review APPROVE; fresh-model comparison reported with sample size and unverified items (other hosts' fonts, print on paper, real students).

## 8. Calls cc made (please check)

1. ReportLab as an optional dependency (approach A), HTML-print as the fallback path.
2. Generalised content rules come from one student's revisions; topic-specific removals (ROC syntax, final-check box) are stored as that student's preferences, not as rules.
3. Preferences live in the course profile, with an offer to reuse general ones across courses.
4. Auto-fit picks the most spacious preset that fits, so cutting content automatically improves readability.
5. Minimum sizes 9 pt body / 8.5 pt code unless the instructor's rules say otherwise.
6. Earlier sheet versions are kept as `-v<round>` files.
