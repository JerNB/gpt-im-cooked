"""Render a mock-exam JSON file into an HTML worksheet and a separate answer key.

The worksheet uses assets/mock-exam-template.html, whose tested script handles
answer status, revisit flags, attempt snapshots, key-exposure tracking, retry,
and schema 1.0 export. Key data is never written to the worksheet. The script
checks structure (IDs, options, answers, evidence labels, sources, unsafe SVG);
it cannot check whether a question or answer is academically correct.

Usage:
  python render_mock_exam.py EXAM.json --out DIR [--force]
  python render_mock_exam.py EXAM.json --check

Requires Python 3.10+ and only its standard library.
"""
from pathlib import Path
import argparse
import html
import json
import re

PACKAGE_VERSION = '2.0.0'
FORMAT = 'gpt-im-cooked-mock-exam/1'
TEMPLATE = Path(__file__).resolve().parents[1] / 'assets' / 'mock-exam-template.html'
KINDS = {
    'single': 'Choose one',
    'multi': 'Choose all that apply',
    'short': 'Short answer',
    'numeric': 'Numeric answer',
    'code': 'Code',
    'long': 'Written response',
}
CHOICE = {'single', 'multi'}
EVIDENCE = {'Instructor key', 'Verified computation', 'Reasoned solution'}
SLUG = re.compile(r'^[a-z0-9][a-z0-9-]{0,63}$')
OPTION_ID = re.compile(r'^[A-Z0-9]{1,3}$')
UNSAFE_SVG = re.compile(r'<\s*script|<\s*foreignObject|\son[a-z]+\s*=|javascript:|(?:href|src)\s*=\s*["\']?\s*https?:', re.I)


class ExamError(ValueError):
    pass


def esc(text):
    return html.escape(str(text), quote=True)


def inline(text):
    """Escape text, then allow `code` and **bold** only."""
    out = esc(text)
    out = re.sub(r'`([^`]+)`', r'<code>\1</code>', out)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', out)


# ---------------------------------------------------------------- validation

def check_blocks(blocks, where, errors, warnings):
    if not isinstance(blocks, list) or not blocks:
        errors.append(f'{where}: needs a nonempty list of blocks')
        return
    for i, block in enumerate(blocks):
        at = f'{where}[{i}]'
        if isinstance(block, str):
            if not block.strip():
                errors.append(f'{at}: empty paragraph')
            continue
        if not isinstance(block, dict):
            errors.append(f'{at}: a block is a string or an object')
            continue
        kinds = set(block) & {'p', 'code', 'table', 'svg', 'image', 'list'}
        if len(kinds) != 1:
            errors.append(f'{at}: use exactly one of p, code, table, svg, image, list')
            continue
        kind = kinds.pop()
        extra = set(block) - {kind, 'lang', 'alt', 'caption'}
        if extra:
            errors.append(f'{at}: unknown fields {sorted(extra)}')
        if kind == 'table':
            table = block['table']
            columns = table.get('columns') if isinstance(table, dict) else None
            rows = table.get('rows') if isinstance(table, dict) else None
            if not columns or not isinstance(rows, list) or any(len(r) != len(columns) for r in rows):
                errors.append(f'{at}: table needs columns and rows of the same width')
        elif kind == 'svg':
            svg = str(block['svg'])
            if not svg.lstrip().startswith('<svg'):
                errors.append(f'{at}: svg must start with <svg')
            if UNSAFE_SVG.search(svg):
                errors.append(f'{at}: svg contains script, event handlers, foreignObject, or external links')
            if not block.get('alt'):
                errors.append(f'{at}: svg needs alt text describing what it shows')
        elif kind == 'image':
            src = str(block['image'])
            if not block.get('alt'):
                errors.append(f'{at}: image needs alt text')
            if src.startswith(('http:', 'https:', '//', 'javascript:')):
                errors.append(f'{at}: image must be a data: URI or a relative file, not a network URL')
            elif not src.startswith('data:image/'):
                warnings.append(f'{at}: relative image {src!r} must be delivered beside the worksheet; it is not self-contained')
        elif kind == 'list':
            if not isinstance(block['list'], list) or not block['list']:
                errors.append(f'{at}: list needs items')
        elif not str(block[kind]).strip():
            errors.append(f'{at}: empty {kind}')


def validate(exam):
    errors, warnings = [], []
    if exam.get('format') != FORMAT:
        errors.append(f'format must be {FORMAT!r}')
    if not SLUG.match(str(exam.get('artifact_id', ''))):
        errors.append('artifact_id must be a lowercase slug (letters, digits, hyphens)')
    for field in ('artifact_version', 'course', 'exam'):
        if not str(exam.get(field, '')).strip():
            errors.append(f'{field} is required')
    estimate = exam.get('time_estimate')
    if estimate is not None and (not isinstance(estimate, dict) or estimate.get('basis') not in ('practice estimate', 'confirmed')
                                 or not isinstance(estimate.get('minutes'), (int, float))):
        errors.append("time_estimate needs minutes and basis 'practice estimate' or 'confirmed'")
    sources = exam.get('sources')
    if not isinstance(sources, dict) or not sources:
        errors.append('sources must map source IDs to {title, locator}')
        sources = {}
    for sid, source in sources.items():
        if not isinstance(source, dict) or not str(source.get('title', '')).strip():
            errors.append(f'sources.{sid}: needs a title')
    shared = {}
    for i, item in enumerate(exam.get('shared', [])):
        sid = item.get('id', '')
        if not SLUG.match(sid) or sid in shared:
            errors.append(f'shared[{i}]: needs a unique slug id')
        if not str(item.get('title', '')).strip():
            errors.append(f'shared[{i}]: needs a title')
        check_blocks(item.get('blocks'), f'shared[{i}].blocks', errors, warnings)
        shared[sid] = item
    questions = exam.get('questions')
    if not isinstance(questions, list) or not questions:
        errors.append('questions must be a nonempty list')
        questions = []
    seen = set()
    for i, q in enumerate(questions):
        at = f"questions[{i}] ({q.get('id', '?')})"
        qid, kind = q.get('id', ''), q.get('type')
        if not SLUG.match(qid) or qid in seen:
            errors.append(f'{at}: needs a unique slug id')
        seen.add(qid)
        if kind not in KINDS:
            errors.append(f'{at}: type must be one of {sorted(KINDS)}')
        for field in ('title', 'topic_id'):
            if not str(q.get(field, '')).strip():
                errors.append(f'{at}: {field} is required')
        if q.get('source') not in sources:
            errors.append(f'{at}: source must be one of the declared source IDs')
        if q.get('shared_ref') is not None and q['shared_ref'] not in shared:
            errors.append(f'{at}: shared_ref {q["shared_ref"]!r} is not declared in shared')
        check_blocks(q.get('prompt'), f'{at}.prompt', errors, warnings)
        options = q.get('options')
        key = q.get('key')
        if not isinstance(key, dict):
            errors.append(f'{at}: key is required')
            continue
        evidence = key.get('evidence')
        if evidence == 'Unresolved':
            errors.append(f'{at}: answer is Unresolved; fix or omit this item before delivery')
        elif evidence not in EVIDENCE:
            errors.append(f'{at}: key.evidence must be one of {sorted(EVIDENCE)}')
        for field in ('explanation', 'verification'):
            if not str(key.get(field, '')).strip():
                errors.append(f'{at}: key.{field} is required')
        if kind in CHOICE:
            if not isinstance(options, list) or len(options) < 2:
                errors.append(f'{at}: needs at least two options')
                continue
            ids = [o.get('id') for o in options]
            if len(set(ids)) != len(ids) or not all(OPTION_ID.match(str(x)) for x in ids):
                errors.append(f'{at}: option ids must be unique short labels like A, B, C')
            if any(not str(o.get('text', '')).strip() for o in options):
                errors.append(f'{at}: every option needs text')
            answer = key.get('answer')
            if not isinstance(answer, list) or not set(answer) <= set(ids) or len(set(answer)) != len(answer):
                errors.append(f'{at}: key.answer must list option ids from this question')
            elif kind == 'single' and len(answer) != 1:
                errors.append(f'{at}: a single-choice item needs exactly one correct option')
            elif kind == 'multi' and not answer:
                warnings.append(f'{at}: no option is correct; make sure the instructions allow that')
            notes = key.get('option_notes', {})
            missing = [x for x in ids if not str(notes.get(x, '')).strip()]
            if kind == 'multi' and missing:
                errors.append(f'{at}: multi-select keys must explain every option; missing {missing}')
            elif missing:
                warnings.append(f'{at}: option_notes missing for {missing}')
        else:
            if options:
                errors.append(f'{at}: only single/multi items take options')
            if not str(key.get('answer', '')).strip():
                errors.append(f'{at}: key.answer is required')
    if errors:
        raise ExamError('\n'.join(errors))
    return warnings


# ------------------------------------------------------------------ rendering

def render_blocks(blocks):
    out = []
    for block in blocks:
        if isinstance(block, str):
            out.append(f'<p>{inline(block)}</p>')
            continue
        caption = f'<figcaption>{inline(block["caption"])}</figcaption>' if block.get('caption') else ''
        if 'p' in block:
            out.append(f'<p>{inline(block["p"])}</p>')
        elif 'code' in block:
            lang = f' class="language-{esc(block["lang"])}"' if block.get('lang') else ''
            out.append(f'<pre><code{lang}>{esc(block["code"])}</code></pre>')
        elif 'list' in block:
            out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in block['list']) + '</ul>')
        elif 'table' in block:
            t = block['table']
            cap = f'<caption>{inline(t["caption"])}</caption>' if t.get('caption') else ''
            head = ''.join(f'<th scope="col">{inline(c)}</th>' for c in t['columns'])
            rows = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in t['rows'])
            out.append(f'<div class="table-wrap"><table>{cap}<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
        elif 'svg' in block:
            svg = re.sub(r'^<svg', f'<svg role="img" aria-label="{esc(block["alt"])}"', block['svg'].strip(), count=1)
            out.append(f'<figure>{svg}{caption}</figure>')
        elif 'image' in block:
            out.append(f'<figure><img src="{esc(block["image"])}" alt="{esc(block["alt"])}">{caption}</figure>')
    return '\n'.join(out)


def source_text(exam, q):
    source = exam['sources'][q['source']]
    locator = q.get('source_locator') or source.get('locator')
    return f"{q['source']}: {source['title']}" + (f', {locator}' if locator else '')


def heading(number, q):
    return f'Question {number}: {inline(q["title"])} <span class="q-kind">— {KINDS[q["type"]]}</span>'


def shared_section(item):
    return (f'<section class="shared" id="shared-{esc(item["id"])}" aria-labelledby="shared-{esc(item["id"])}-title">'
            f'<h2 id="shared-{esc(item["id"])}-title">{inline(item["title"])}</h2>{render_blocks(item["blocks"])}</section>')


def answer_field(q):
    qid, kind = esc(q['id']), q['type']
    if kind in CHOICE:
        control = 'radio' if kind == 'single' else 'checkbox'
        options = ''.join(
            f'<label class="option"><input type="{control}" name="{qid}" value="{esc(o["id"])}">'
            f'<span><b>{esc(o["id"])}.</b> {inline(o["text"])}</span></label>' for o in q['options'])
        return f'<fieldset><legend class="sr-only">Your answer for {inline(q["title"])}</legend>{options}</fieldset>'
    label = {'short': 'Your answer', 'numeric': 'Your answer', 'code': 'Your code', 'long': 'Your response'}[kind]
    if kind == 'numeric':
        field = f'<input class="short" type="text" inputmode="decimal" id="{qid}-answer" name="answer">'
    else:
        rows = {'short': 2, 'code': 5, 'long': 8}[kind]
        extra = ' class="code" spellcheck="false"' if kind == 'code' else ''
        field = f'<textarea id="{qid}-answer" name="answer" rows="{rows}"{extra}></textarea>'
    return f'<label class="field-label" for="{qid}-answer">{label}</label>{field}'


def question_section(exam, number, q, shared_note):
    qid = esc(q['id'])
    return (
        f'<section class="question" id="{qid}" data-kind="{q["type"]}" data-topic="{esc(q["topic_id"])}" '
        f'data-source="{esc(source_text(exam, q))}" aria-labelledby="{qid}-title">'
        f'<div class="q-head"><h2 id="{qid}-title">{heading(number, q)}</h2>'
        f'<label class="flag"><input type="checkbox" data-flag> Revisit</label></div>'
        f'{shared_note}{render_blocks(q["prompt"])}{answer_field(q)}'
        f'<details class="reasoning"><summary>Add reasoning or confidence (optional)</summary>'
        f'<label class="field-label" for="{qid}-reason">Your reasoning</label>'
        f'<textarea id="{qid}-reason" name="reasoning" rows="3"></textarea>'
        f'<label class="field-label" for="{qid}-confidence">Confidence</label>'
        f'<select id="{qid}-confidence" name="confidence"><option value="">Not recorded</option>'
        f'<option>Low</option><option>Medium</option><option>High</option></select></details>'
        f'<p class="source">Source: {inline(source_text(exam, q))}</p></section>')


def header_html(exam):
    questions = exam['questions']
    kinds = []
    for q in questions:
        label = KINDS[q['type']].lower()
        if label not in kinds:
            kinds.append(label)
    parts = [f'{len(questions)} questions', ', '.join(kinds)]
    estimate = exam.get('time_estimate')
    if estimate:
        label = 'Time limit (confirmed)' if estimate['basis'] == 'confirmed' else 'Suggested practice time (estimate)'
        parts.append(f'{label}: {estimate["minutes"]:g} minutes')
    title = exam.get('title') or f'{exam["course"]}: {exam["exam"]} mock exam'
    out = [f'<p class="muted">{inline(exam["course"])} · {inline(exam["exam"])} · Original practice</p>',
           f'<h1>{inline(title)}</h1>', f'<p class="subtitle">{" · ".join(esc(p) for p in parts)}</p>',
           f'<p>{inline(exam.get("instructions") or "Work independently. You can leave questions unanswered. No score, hints, or solutions appear during this attempt.")}</p>']
    if exam.get('allowed_aids'):
        out.append(f'<p><strong>Allowed aids (confirmed):</strong> {inline(exam["allowed_aids"])}</p>')
    if any(q['type'] == 'multi' for q in questions):
        out.append('<p class="muted">On “choose all that apply” items, select every supported option. Code and written answers are reviewed by your tutor.</p>')
    if exam.get('personalization'):
        out.append(f'<details><summary>Why these questions?</summary><p>{inline(exam["personalization"])}</p></details>')
    return '\n'.join(out)


def body_sections(exam, renderer):
    shared = {s['id']: s for s in exam.get('shared', [])}
    placed, out = set(), []
    for number, q in enumerate(exam['questions'], 1):
        note = ''
        ref = q.get('shared_ref')
        if ref:
            if ref not in placed:
                out.append(shared_section(shared[ref]))
                placed.add(ref)
            note = f'<p class="shared-ref">Uses <a href="#shared-{esc(ref)}">{inline(shared[ref]["title"])}</a>.</p>'
        out.append(renderer(exam, number, q, note))
    return '\n'.join(out)


def artifact_meta(exam):
    meta = {'schema_version': '1.0', 'package_version': PACKAGE_VERSION, 'artifact_id': exam['artifact_id'],
            'artifact_version': str(exam['artifact_version']), 'artifact_type': 'mock-exam-worksheet',
            'course': exam['course'], 'exam': exam['exam'], 'key_file': key_name(exam)}
    raw = json.dumps(meta, ensure_ascii=False)
    return raw.replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')


def key_name(exam):
    return f'{exam["artifact_id"]}-key.html'


def fill(template, values):
    for name, value in values.items():
        template = template.replace('{{' + name + '}}', value)
    leftover = re.findall(r'\{\{[A-Z_]+\}\}', template)
    if leftover:
        raise ExamError(f'Template placeholders left unfilled: {leftover}')
    return template


def render_worksheet(exam, template):
    title = exam.get('title') or f'{exam["course"]}: {exam["exam"]} mock exam'
    nav = '\n'.join(
        f'<li><a href="#{esc(q["id"])}" data-nav="{esc(q["id"])}"><span>{n} <span class="nav-title">{inline(q["title"])}</span></span>'
        f'<span class="status" aria-label="Unanswered">○</span></a></li>' for n, q in enumerate(exam['questions'], 1))
    return fill(template, {
        'TITLE': esc(title), 'HEADER': header_html(exam), 'QUESTIONS': body_sections(exam, question_section),
        'NAV': nav, 'COUNT': str(len(exam['questions'])), 'KEY_HREF': esc(key_name(exam)),
        'ARTIFACT_JSON': artifact_meta(exam)})


def key_question(exam, number, q, shared_note):
    key = q['key']
    if q['type'] in CHOICE:
        notes = key.get('option_notes', {})
        rows = ''.join(
            f'<tr><td>{"✓ Correct" if o["id"] in key["answer"] else "Incorrect"}</td><td><b>{esc(o["id"])}.</b> {inline(o["text"])}</td>'
            f'<td>{inline(notes.get(o["id"], ""))}</td></tr>' for o in q['options'])
        answer = (f'<p><strong>Answer:</strong> {esc(", ".join(key["answer"]) or "none of the options")}</p>'
                  f'<div class="table-wrap"><table><thead><tr><th>Verdict</th><th>Option</th><th>Why</th></tr></thead><tbody>{rows}</tbody></table></div>')
    else:
        answer = f'<p><strong>Answer:</strong></p><pre><code>{esc(key["answer"])}</code></pre>'
    return (f'<section class="question" id="{esc(q["id"])}"><div class="q-head"><h2>{heading(number, q)}</h2></div>'
            f'{shared_note}{render_blocks(q["prompt"])}{answer}'
            f'<p><strong>Why:</strong> {inline(key["explanation"])}</p>'
            f'<p><strong>Answer evidence:</strong> {esc(key["evidence"])}. {inline(key["verification"])}</p>'
            f'<p class="source">Source: {inline(source_text(exam, q))} · Topic {esc(q["topic_id"])}</p></section>')


def render_key(exam, template):
    style = re.search(r'<style>.*?</style>', template, re.S).group(0)
    title = exam.get('title') or f'{exam["course"]}: {exam["exam"]} mock exam'
    blueprint = ''.join(
        f'<tr><td><a href="#{esc(q["id"])}">{n}</a></td><td>{esc(q["topic_id"])}</td><td>{KINDS[q["type"]]}</td>'
        f'<td>{inline(source_text(exam, q))}</td><td>{inline(q.get("personal_target") or "Course coverage")}</td>'
        f'<td>{esc(q["key"]["evidence"])}</td></tr>' for n, q in enumerate(exam['questions'], 1))
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Answer key · {esc(title)}</title>{style}</head><body><div class="layout" style="grid-template-columns:minmax(0,900px)"><main>'
            f'<header class="paper-head"><p class="muted">{inline(exam["course"])} · {inline(exam["exam"])} · Answer key</p>'
            f'<h1>Answer key: {inline(title)}</h1>'
            f'<p class="note">Open this only after you finish and export your attempt. If you open it earlier, tell your tutor: later answers count as assisted.</p>'
            f'<p class="muted">Questions are original practice built from your course materials, not instructor questions. '
            f'Artifact {esc(exam["artifact_id"])} version {esc(exam["artifact_version"])}.</p></header>'
            f'<section class="question"><h2>Blueprint</h2><div class="table-wrap"><table><thead><tr><th>Item</th><th>Topic ID</th>'
            f'<th>Format</th><th>Scope/style basis</th><th>Personal target</th><th>Answer evidence</th></tr></thead>'
            f'<tbody>{blueprint}</tbody></table></div></section>'
            f'{body_sections(exam, key_question)}</main></div></body></html>\n')


# ---------------------------------------------------------------- leak guard

def visible_text(markup):
    markup = re.sub(r'<script type="application/json".*?</script>', ' ', markup, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', markup)))


def leak_check(worksheet, exam):
    """Fail if key-only text appears in the worksheet; warn on free-text answers."""
    text, errors, warnings = visible_text(worksheet), [], []
    norm = lambda s: re.sub(r'\s+', ' ', re.sub(r'[`*]', '', str(s))).strip()
    for q in exam['questions']:
        key = q['key']
        private = [key['explanation'], key['verification'], q.get('personal_target', ''), *key.get('option_notes', {}).values()]
        for value in private:
            if len(norm(value)) >= 12 and norm(value) in text:
                errors.append(f'{q["id"]}: key-only text appears in the worksheet: {norm(value)[:60]!r}')
        if q['type'] not in CHOICE and len(norm(key['answer'])) >= 6 and norm(key['answer']) in text:
            warnings.append(f'{q["id"]}: the expected answer text also appears in the worksheet; check that the prompt does not give it away')
    if errors:
        raise ExamError('\n'.join(errors))
    return warnings


def render(exam):
    warnings = validate(exam)
    template = TEMPLATE.read_text(encoding='utf-8')
    worksheet = render_worksheet(exam, template)
    warnings += leak_check(worksheet, exam)
    return worksheet, render_key(exam, template), warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('exam', type=Path)
    parser.add_argument('--out', type=Path, help='directory for the worksheet and key')
    parser.add_argument('--check', action='store_true', help='validate and render in memory without writing files')
    parser.add_argument('--force', action='store_true', help='replace existing output files')
    args = parser.parse_args()
    if not args.check and args.out is None:
        parser.error('give --out DIR, or --check to validate only')
    try:
        exam = json.loads(args.exam.read_text(encoding='utf-8-sig'))
        worksheet, key, warnings = render(exam)
        result = {'valid': True, 'questions': len(exam['questions']), 'warnings': warnings}
        if not args.check:
            args.out.mkdir(parents=True, exist_ok=True)
            paths = {'worksheet': args.out / f'{exam["artifact_id"]}.html', 'key': args.out / key_name(exam)}
            existing = [str(p) for p in paths.values() if p.exists()]
            if existing and not args.force:
                raise ExamError(f'Refusing to replace {existing}; bump artifact_version and use --force, or choose another --out')
            paths['worksheet'].write_text(worksheet, encoding='utf-8')
            paths['key'].write_text(key, encoding='utf-8')
            result.update({k: str(v) for k, v in paths.items()})
        print(json.dumps(result, ensure_ascii=True, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'Mock exam not rendered:\n{error}\n')


if __name__ == '__main__':
    main()
