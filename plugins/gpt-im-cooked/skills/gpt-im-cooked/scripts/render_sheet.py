"""Render an exam reference sheet or study guide from a content JSON file into a PDF.

The model writes content only (sections, blocks, weights). This script lays it out
(two columns for an exam sheet, one for a study guide), picks the most spacious
layout preset that fits the allowed page count, never goes below the minimum
type size, and reports overflow per section instead of shrinking further.
It also writes checks.json and, when pypdfium2 is available, page previews.

Usage:
  python render_sheet.py SHEET.json --out DIR [--force]
  python render_sheet.py SHEET.json --check

Validation needs only the Python 3.10+ standard library; rendering needs ReportLab.
The script never installs packages.
"""
import html
import re

FORMAT = 'gpt-im-cooked-sheet/1'
KINDS = {'exam-sheet', 'study-guide'}
BLOCKS = {'cue', 'text', 'stages', 'example', 'table', 'code', 'mistake'}
WEIGHTS = {'high', 'normal', 'low'}
PAPERS = {'letter', 'a4'}
SLUG = re.compile(r'^[a-z0-9][a-z0-9-]{0,63}$')


class SheetError(ValueError):
    """The content cannot be rendered as written."""


def _need(condition, message):
    if not condition:
        raise SheetError(message)


def _text(value, where, required=True):
    if value is None and not required:
        return ''
    _need(isinstance(value, str) and value.strip(), f'{where}: missing text')
    return value.strip()


def _steps(value, where):
    _need(isinstance(value, list) and value, f'{where}.steps: expected a list of {{label, text}}')
    return [{'label': _text(s.get('label') if isinstance(s, dict) else None, f'{where}.steps[{i}].label'),
             'text': _text(s.get('text') if isinstance(s, dict) else None, f'{where}.steps[{i}].text')}
            for i, s in enumerate(value)]


def _block(block, where):
    _need(isinstance(block, dict), f'{where}: expected an object')
    kind = block.get('type')
    _need(kind in BLOCKS, f'{where}: unknown block type {kind!r} (use {", ".join(sorted(BLOCKS))})')
    if kind in ('cue', 'text'):
        return {'type': kind, 'text': _text(block.get('text'), where)}
    if kind == 'code':
        code = block.get('text')
        _need(isinstance(code, str) and code.strip(), f'{where}: missing code')
        return {'type': kind, 'text': code.rstrip()}
    if kind == 'stages':
        return {'type': kind, 'steps': _steps(block.get('steps'), where)}
    if kind == 'example':
        return {'type': kind, 'setup': _text(block.get('setup'), f'{where}.setup', required=False),
                'steps': _steps(block.get('steps'), where),
                'takeaway': _text(block.get('takeaway'), f'{where}.takeaway', required=False)}
    if kind == 'table':
        header, rows = block.get('header'), block.get('rows')
        _need(isinstance(header, list) and header and all(isinstance(h, str) for h in header),
              f'{where}: table header must be a list of strings')
        _need(isinstance(rows, list) and rows, f'{where}: table needs rows')
        for r, row in enumerate(rows):
            _need(isinstance(row, list) and len(row) == len(header) and all(isinstance(c, str) for c in row),
                  f'{where}: table row {r} must have {len(header)} text cells')
        return {'type': kind, 'header': header, 'rows': rows}
    return {'type': kind, 'prompt': _text(block.get('prompt'), f'{where}.prompt', required=False),
            'first_error': _text(block.get('first_error'), f'{where}.first_error'),
            'fix': _text(block.get('fix'), f'{where}.fix'),
            'conditions': _text(block.get('conditions'), f'{where}.conditions', required=False)}


def load_sheet(data):
    """Validate content and return a normalised copy with defaults filled."""
    _need(isinstance(data, dict), 'content: expected a JSON object')
    _need(data.get('format') == FORMAT, f'format: expected {FORMAT!r}')
    kind = data.get('kind', 'exam-sheet')
    _need(kind in KINDS, f'kind: use {" or ".join(sorted(KINDS))}')
    raw = data.get('allowance') or {}
    _need(isinstance(raw, dict), 'allowance: expected an object')
    allowance = {'status': raw.get('status', 'unconfirmed'), 'sheets': raw.get('sheets', 1),
                 'sides': raw.get('sides', 2), 'paper': raw.get('paper', 'letter'),
                 'rules': raw.get('rules'), 'min_body': raw.get('min_body')}
    _need(allowance['status'] in ('confirmed', 'unconfirmed'), 'allowance.status: confirmed or unconfirmed')
    _need(isinstance(allowance['sheets'], int) and 1 <= allowance['sheets'] <= 10, 'allowance.sheets: 1-10')
    _need(allowance['sides'] in (1, 2), 'allowance.sides: 1 or 2')
    _need(allowance['paper'] in PAPERS, f'allowance.paper: use {" or ".join(sorted(PAPERS))}')
    _need(allowance['rules'] is None or isinstance(allowance['rules'], str), 'allowance.rules: text or null')
    _need(allowance['min_body'] is None or (isinstance(allowance['min_body'], (int, float)) and 6 <= allowance['min_body'] <= 14),
          'allowance.min_body: instructor minimum body size in points (6-14) or null')

    sections, seen = [], set()
    raw_sections = data.get('sections')
    _need(isinstance(raw_sections, list) and raw_sections, 'sections: expected at least one section')
    for i, section in enumerate(raw_sections):
        _need(isinstance(section, dict), f'sections[{i}]: expected an object')
        sid = section.get('id')
        _need(isinstance(sid, str) and SLUG.match(sid), f'sections[{i}].id: use lowercase letters, digits and hyphens')
        _need(sid not in seen, f'sections[{i}].id: duplicate section {sid!r}')
        seen.add(sid)
        weight = section.get('weight', 'normal')
        _need(weight in WEIGHTS, f'section {sid}: weight must be high, normal or low')
        blocks = section.get('blocks')
        _need(isinstance(blocks, list) and blocks, f'section {sid}: needs at least one block')
        sections.append({'id': sid, 'title': _text(section.get('title'), f'section {sid}.title'), 'weight': weight,
                         'topics': [t for t in section.get('topics', []) if isinstance(t, str)],
                         'blocks': [_block(b, f'section {sid} block {j}') for j, b in enumerate(blocks)]})

    revision = data.get('revision') or {}
    _need(isinstance(revision, dict), 'revision: expected an object')
    round_ = revision.get('round', 1)
    _need(isinstance(round_, int) and round_ >= 1, 'revision.round: whole number from 1')
    language = data.get('language', 'en')
    _need(isinstance(language, str) and re.match(r'^[a-z]{2}(-[A-Za-z]{2,4})?$', language), 'language: code like en or zh')
    return {'format': FORMAT, 'kind': kind, 'title': _text(data.get('title'), 'title'),
            'course': _text(data.get('course'), 'course', required=False), 'allowance': allowance,
            'language': language, 'sections': sections,
            'omitted': [o for o in data.get('omitted', []) if isinstance(o, dict)],
            'revision': {'round': round_, 'standing': list(revision.get('standing', [])),
                         'changes': list(revision.get('changes', []))}}


_MARKUP = [
    (re.compile(r'\*\*(.+?)\*\*'), r'<b>\1</b>'),
    (re.compile(r'`(.+?)`'), r'<font face="{mono}">\1</font>'),
    (re.compile(r'\^\{(.+?)\}'), r'<super>\1</super>'),
    (re.compile(r'_\{(.+?)\}'), r'<sub>\1</sub>'),
]


def inline(text):
    """Escape text, then apply **bold**, `code`, ^{super} and _{sub}; unmatched markers stay literal."""
    out = html.escape(text, quote=False)
    for pattern, replacement in _MARKUP:
        out = pattern.sub(replacement, out)
    return out
