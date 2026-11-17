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
from pathlib import Path
import html
import os
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


def _font_candidates():
    windir = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'
    mac = Path('/System/Library/Fonts/Supplemental')
    linux = sorted(Path('/usr/share/fonts').rglob('DejaVuSans*.ttf')) if Path('/usr/share/fonts').is_dir() else []
    by_name = {p.name: p for p in linux}
    return {
        'body': [windir / 'segoeui.ttf', windir / 'arial.ttf', mac / 'Arial.ttf', by_name.get('DejaVuSans.ttf')],
        'bold': [windir / 'segoeuib.ttf', windir / 'arialbd.ttf', mac / 'Arial Bold.ttf', by_name.get('DejaVuSans-Bold.ttf')],
        'mono': [windir / 'consola.ttf', windir / 'cour.ttf', mac / 'Courier New.ttf', by_name.get('DejaVuSansMono.ttf')],
    }


def find_fonts(language='en'):
    """Register Unicode fonts found on this host; fall back to built-in Latin-1 fonts (then reported as missing glyphs)."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping

    fallback = {'body': 'Helvetica', 'bold': 'Helvetica-Bold', 'mono': 'Courier'}
    chosen, files = {}, {}
    for role, paths in _font_candidates().items():
        for path in paths:
            if path is not None and path.is_file():
                name = f'Sheet-{role}-{path.stem}'
                if name not in pdfmetrics.getRegisteredFontNames():
                    try:
                        pdfmetrics.registerFont(TTFont(name, str(path)))
                    except Exception:  # unreadable or unsupported font file: try the next candidate
                        continue
                chosen[role], files[name] = name, str(path)
                break
        else:
            chosen[role] = fallback[role]
    if chosen['body'] == 'Helvetica' or chosen['bold'] == 'Helvetica-Bold':
        chosen['body'], chosen['bold'] = 'Helvetica', 'Helvetica-Bold'
    if language.split('-')[0] in ('zh', 'ja', 'ko'):
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        cid = {'zh': 'STSong-Light', 'ja': 'HeiseiMin-W3', 'ko': 'HYSMyeongJo-Medium'}[language.split('-')[0]]
        if cid not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(UnicodeCIDFont(cid))
        chosen['body'] = chosen['bold'] = cid
    for bold, italic in ((0, 0), (1, 0), (0, 1), (1, 1)):  # lets <b> inside paragraphs use the bold file
        addMapping(chosen['body'], bold, italic, chosen['bold'] if bold else chosen['body'])
    return {**chosen, 'files': files}


PRESETS = [  # most spacious first; fit() keeps the first one that fits
    {'body': 11.0, 'code': 9.5, 'gap': 6.0, 'section_gap': 11.0},
    {'body': 10.5, 'code': 9.25, 'gap': 5.0, 'section_gap': 9.5},
    {'body': 10.0, 'code': 9.0, 'gap': 4.5, 'section_gap': 8.0},
    {'body': 9.5, 'code': 8.75, 'gap': 3.5, 'section_gap': 6.5},
    {'body': 9.0, 'code': 8.5, 'gap': 3.0, 'section_gap': 5.0},
]
LEADING = 1.24
HIGH_SCALE = 1.08
MARGIN = 36.0
COLUMN_GAP = 16.0
HEADER = 18.0
FOOTER = 16.0
UNCONFIRMED_NOTE = "Exam use unconfirmed — check your instructor's rules."
INK, MUTED, BRAND, TINT, RULE = '#1f2a24', '#5f6b63', '#2f5d50', '#e7efe9', '#c9d3cc'


class Overflow(Exception):
    """Content does not fit the allowed pages even at the tightest permitted preset."""

    def __init__(self, over_pt, sections, reason='content is taller than the allowed pages'):
        super().__init__(f'{reason}: over by about {over_pt:.0f}pt')
        self.over_pt, self.sections, self.reason = over_pt, sections, reason


def _styles(fonts, preset, weight):
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    scale = HIGH_SCALE if weight == 'high' else 1.0
    size = preset['body'] * scale
    base = ParagraphStyle('body', fontName=fonts['body'], fontSize=size, leading=size * LEADING,
                          textColor=colors.HexColor(INK), spaceAfter=preset['gap'])
    return {
        'body': base,
        'cue': ParagraphStyle('cue', parent=base, leftIndent=size * 0.9, bulletIndent=0),
        'cell': ParagraphStyle('cell', parent=base, spaceAfter=0),
        'label': ParagraphStyle('label', parent=base, fontName=fonts['bold'], spaceAfter=0,
                                textColor=colors.HexColor(BRAND)),
        'muted': ParagraphStyle('muted', parent=base, textColor=colors.HexColor(MUTED)),
        'title': ParagraphStyle('title', parent=base, fontName=fonts['bold'], fontSize=size * 1.16,
                                leading=size * 1.16 * 1.2, textColor=colors.HexColor(BRAND),
                                spaceBefore=preset['section_gap'], spaceAfter=preset['gap'],
                                backColor=colors.HexColor(TINT) if weight == 'high' else None,
                                borderPadding=(2, 3, 2, 3) if weight == 'high' else 0),
        'code': ParagraphStyle('code', fontName=fonts['mono'], fontSize=preset['code'],
                               leading=preset['code'] * 1.2, textColor=colors.HexColor(INK),
                               backColor=colors.HexColor('#f1f0ea'), borderPadding=3, spaceAfter=preset['gap'] + 2),
    }


def _para(text, style, fonts):
    from reportlab.platypus import Paragraph
    return Paragraph(inline(text).replace('{mono}', fonts['mono']), style)


def _grid(rows, widths, styles, header=False):
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors
    table = Table(rows, colWidths=widths, hAlign='LEFT')
    commands = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 1.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
                ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor(RULE))]
    if header:
        commands.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(TINT)))
    table.setStyle(TableStyle(commands))
    return table


def _block_flowables(block, styles, fonts, width):
    from reportlab.platypus import Preformatted, Spacer, KeepTogether
    P = lambda text, key='body': _para(text, styles[key], fonts)  # noqa: E731
    gap = styles['body'].spaceAfter
    kind = block['type']
    if kind == 'text':
        return [P(block['text'])]
    if kind == 'cue':
        from reportlab.platypus import Paragraph
        return [Paragraph(inline(block['text']).replace('{mono}', fonts['mono']), styles['cue'], bulletText='•')]
    if kind == 'code':
        return [Preformatted(block['text'], styles['code'])]
    if kind in ('stages', 'example'):
        parts = [P(block['setup'], 'muted')] if kind == 'example' and block['setup'] else []
        label_w = width * 0.32
        rows = [[P(s['label'], 'label'), P(s['text'], 'cell')] for s in block['steps']]
        parts.append(_grid(rows, [label_w, width - label_w], styles))
        if kind == 'example' and block['takeaway']:
            parts += [Spacer(1, gap * 0.6), P('**Takeaway:** ' + block['takeaway'])]
        parts.append(Spacer(1, gap))
        return [KeepTogether(parts)]
    if kind == 'table':
        n = len(block['header'])
        rows = [[P(f'**{h}**' if h else '', 'cell') for h in block['header']]]
        rows += [[P(c, 'cell') for c in row] for row in block['rows']]
        return [KeepTogether([_grid(rows, [width / n] * n, styles, header=True), Spacer(1, gap)])]
    rows = [[P('Question', 'label'), P(block['prompt'], 'cell')]] if block['prompt'] else []
    rows += [[P('First error', 'label'), P(block['first_error'], 'cell')], [P('Fix', 'label'), P(block['fix'], 'cell')]]
    if block['conditions']:
        rows.append([P('Holds when', 'label'), P(block['conditions'], 'cell')])
    label_w = width * 0.28
    return [KeepTogether([_grid(rows, [label_w, width - label_w], styles), Spacer(1, gap)])]


def _section_flowables(section, fonts, preset, width):
    styles = _styles(fonts, preset, section['weight'])
    title = _para(section['title'], styles['title'], fonts)
    title.keepWithNext = True
    body = []
    for block in section['blocks']:
        body += _block_flowables(block, styles, fonts, width)
    return [title] + body


def _geometry(sheet):
    from reportlab.lib.pagesizes import letter, A4
    page_w, page_h = letter if sheet['allowance']['paper'] == 'letter' else A4
    columns = 2 if sheet['kind'] == 'exam-sheet' else 1
    frame_h = page_h - 2 * MARGIN - HEADER - FOOTER
    col_w = (page_w - 2 * MARGIN - COLUMN_GAP * (columns - 1)) / columns
    return page_w, page_h, columns, col_w, frame_h


def _build(sheet, fonts, preset, target=None):
    """Lay out with one preset into `target` (a path or file object; in-memory when None). Returns pages and fill."""
    import io
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
    from reportlab.lib import colors

    page_w, page_h, columns, col_w, frame_h = _geometry(sheet)
    frames = [Frame(MARGIN + i * (col_w + COLUMN_GAP), MARGIN + FOOTER, col_w, frame_h, id=f'col{i}',
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0) for i in range(columns)]
    fill = {}

    def decorate(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor(MUTED))
        canvas.setFont(fonts['bold'], 8.5)
        top = page_h - MARGIN - 10
        canvas.drawString(MARGIN, top, sheet['title'])
        if sheet['course']:
            canvas.setFont(fonts['body'], 8.5)
            canvas.drawRightString(page_w - MARGIN, top, sheet['course'])
        canvas.setStrokeColor(colors.HexColor(RULE))
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, top - 4, page_w - MARGIN, top - 4)
        canvas.setFont(fonts['body'], 7.5)
        if sheet['allowance']['status'] != 'confirmed':
            canvas.drawString(MARGIN, MARGIN, UNCONFIRMED_NOTE)
        canvas.drawRightString(page_w - MARGIN, MARGIN, f'{doc.page}')
        canvas.restoreState()

    class Doc(BaseDocTemplate):
        def afterFlowable(self, flowable):
            frame = getattr(self, 'frame', None)
            if frame is None or not getattr(frame, '_height', 0):
                return
            used = (frame._y1 + frame._height - frame._y) / frame._height
            fill[(self.page, frame.id)] = round(max(fill.get((self.page, frame.id), 0), used), 3)

    out = target if target is not None else io.BytesIO()
    doc = Doc(out, pagesize=(page_w, page_h), leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN,
              bottomMargin=MARGIN, title=sheet['title'], author='', subject=sheet['course'],
              creator="GPT, I'm Cooked render_sheet.py")
    doc.addPageTemplates([PageTemplate(id='sheet', frames=frames, onPage=decorate)])
    story = []
    for section in sheet['sections']:
        story += _section_flowables(section, fonts, preset, col_w)
    doc.build(story)
    return {'pages': doc.page, 'column_fill': [fill[k] for k in sorted(fill)]}


def _measure(flowable, width):
    """(width, height incl. spacing) without a canvas; KeepTogether groups are measured by their parts."""
    from reportlab.platypus import KeepTogether
    if isinstance(flowable, KeepTogether):
        sizes = [_measure(f, width) for f in flowable._content]
        return max((w for w, _ in sizes), default=0), sum(h for _, h in sizes)
    w, h = flowable.wrap(width, 10 ** 6)
    return w, h + flowable.getSpaceBefore() + flowable.getSpaceAfter()


def _section_heights(sheet, fonts, preset, col_w):
    heights = []
    for section in sheet['sections']:
        total = 0.0
        for flowable in _section_flowables(section, fonts, preset, col_w):
            total += _measure(flowable, col_w)[1]
        heights.append((section['id'], round(total, 1)))
    return heights


def _check_blocks_fit(sheet, fonts, preset, col_w, frame_h):
    """A single block taller than a column, or code wider than it, cannot be fixed by fitting."""
    from reportlab.platypus import Preformatted
    for section in sheet['sections']:
        for flowable in _section_flowables(section, fonts, preset, col_w)[1:]:
            w, h = _measure(flowable, col_w)
            if h > frame_h:
                raise Overflow(h - frame_h, [(section['id'], round(h, 1))], f'a block in section {section["id"]} is taller than one column')
            if isinstance(flowable, Preformatted) and w > col_w + 0.5:
                raise Overflow(w - col_w, [(section['id'], round(h, 1))], f'a code line in section {section["id"]} is wider than one column')


def layout(sheet, fonts, preset):
    """Build once with `preset` in memory; returns (pages, column_fill)."""
    result = _build(sheet, fonts, preset)
    return result['pages'], result['column_fill']


def fit(sheet, fonts):
    """Most spacious permitted preset that fits the allowed pages; raises Overflow with per-section heights."""
    min_body = max(9.0, float(sheet['allowance']['min_body'] or 0))
    presets = [(i, p) for i, p in enumerate(PRESETS) if p['body'] >= min_body]
    if not presets:
        raise Overflow(0, [], f'no layout preset meets the minimum body size {min_body}pt')
    _, _, columns, col_w, frame_h = _geometry(sheet)
    if sheet['kind'] == 'study-guide':
        index, preset = presets[min(1, len(presets) - 1)]
        pages, fill = layout(sheet, fonts, preset)
        return {'preset': index, 'pages': pages, 'column_fill': fill, 'body': preset['body'], 'code': preset['code']}
    target = sheet['allowance']['sheets'] * sheet['allowance']['sides']
    _check_blocks_fit(sheet, fonts, presets[-1][1], col_w, frame_h)
    for index, preset in presets:
        pages, fill = layout(sheet, fonts, preset)
        if pages <= target:
            return {'preset': index, 'pages': pages, 'column_fill': fill, 'body': preset['body'], 'code': preset['code']}
    heights = _section_heights(sheet, fonts, presets[-1][1], col_w)
    capacity = target * columns * frame_h
    over = max(sum(h for _, h in heights) - capacity, 1.0)
    raise Overflow(over, heights)


def _covered_by_cid(char):
    code = ord(char)
    return code < 0x80 or 0x3000 <= code <= 0x9FFF or 0xFF00 <= code <= 0xFFEF


def missing_glyphs(text, font_name):
    """Characters in `text` that the named font cannot draw (whitespace ignored)."""
    from reportlab.pdfbase import pdfmetrics
    font = pdfmetrics.getFont(font_name)
    face = getattr(font, 'face', None)
    cmap = getattr(face, 'charToGlyph', None)
    missing = set()
    for char in set(text):
        if char.isspace():
            continue
        if cmap is not None:
            ok = ord(char) in cmap
        elif font_name in ('STSong-Light', 'HeiseiMin-W3', 'HYSMyeongJo-Medium'):
            ok = _covered_by_cid(char)
        else:
            try:
                char.encode('cp1252')
                ok = True
            except UnicodeEncodeError:
                ok = False
        if not ok:
            missing.add(char)
    return missing
