"""Render an exam reference sheet or study guide from a content JSON file into a PDF.

The model writes content only (sections, blocks, weights). This script lays it out
(two columns for an exam sheet, one for a study guide), picks the most spacious
layout preset that fits the allowed page count, never goes below the minimum
type size, and reports overflow per section instead of shrinking further.
It also writes checks.json and, when pypdfium2 is available, page previews.

Usage:
  python render_sheet.py SHEET.json --out DIR [--force] [--engine auto|reportlab|browser] [--browser PATH]
  python render_sheet.py SHEET.json --check

Validation needs only the Python 3.10+ standard library. Rendering uses ReportLab when it is installed;
otherwise it prints an equivalent HTML layout to PDF with an installed Microsoft Edge, Google Chrome or
Chromium (headless, temporary profile). With neither, it writes the printable HTML and exits with code 3.
The script never installs packages.
"""
from pathlib import Path
import html
import math
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


_CODE_SPAN = re.compile(r'`([^`]+)`')
_MARKUP = [
    (re.compile(r'\*\*(.+?)\*\*'), r'<b>\1</b>'),
    (re.compile(r'\^\{(.+?)\}'), r'<super>\1</super>'),
    (re.compile(r'_\{(.+?)\}'), r'<sub>\1</sub>'),
]


def inline(text):
    """Escape text and apply **bold**, ^{super} and _{sub} outside `code` spans; code is kept literally.

    Unmatched markers stay literal.
    """
    out, last = [], 0
    for match in _CODE_SPAN.finditer(text):
        out.append(_markup(text[last:match.start()]))
        out.append('<font face="{mono}">' + html.escape(match.group(1), quote=False) + '</font>')
        last = match.end()
    out.append(_markup(text[last:]))
    return ''.join(out)


def _markup(text, rules=None):
    out = html.escape(text, quote=False)
    for pattern, replacement in rules or _MARKUP:
        out = pattern.sub(replacement, out)
    return out


_HTML_MARKUP = [(pattern, replacement.replace('super>', 'sup>')) for pattern, replacement in _MARKUP]


def inline_html(text):
    """Like inline(), for the HTML engine: <code> spans are literal, markup applies outside them."""
    out, last = [], 0
    for match in _CODE_SPAN.finditer(text):
        out.append(_markup(text[last:match.start()], _HTML_MARKUP))
        out.append('<code>' + html.escape(match.group(1), quote=False) + '</code>')
        last = match.end()
    out.append(_markup(text[last:], _HTML_MARKUP))
    return ''.join(out)


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
    title._sheet = (section['id'], 'title')
    blocks = [_block_flowables(block, styles, fonts, width) for block in section['blocks']]
    for flowable in _leaves([f for group in blocks for f in group]):
        flowable._sheet = (section['id'], 'block')
    from reportlab.platypus import KeepTogether
    # A heading must never sit alone at the bottom of a column: keep it with the first block.
    return [KeepTogether([title] + blocks[0])] + [f for group in blocks[1:] for f in group]


def _leaves(flowables):
    from reportlab.platypus import KeepTogether
    for flowable in flowables:
        if isinstance(flowable, KeepTogether):
            yield from _leaves(flowable._content)
        else:
            yield flowable


PAGE_SIZES = {'letter': (612.0, 792.0), 'a4': (595.2756, 841.8898)}  # points, as in reportlab.lib.pagesizes


def _geometry(sheet):
    page_w, page_h = PAGE_SIZES[sheet['allowance']['paper']]
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
    fill, placements = {}, []

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
            if getattr(flowable, '_sheet', None) and frame is not None:
                placements.append((*flowable._sheet, (self.page, frame.id)))
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
    return {'pages': doc.page, 'column_fill': [fill[k] for k in sorted(fill)], 'placements': placements}


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
        styles = _styles(fonts, preset, section['weight'])
        blocks = [f for block in section['blocks'] for f in _block_flowables(block, styles, fonts, col_w)]
        for flowable in blocks:
            w, h = _measure(flowable, col_w)
            if h > frame_h:
                raise Overflow(h - frame_h, [(section['id'], round(h, 1))], f'a block in section {section["id"]} is taller than one column')
            if isinstance(flowable, Preformatted):
                from reportlab.pdfbase.pdfmetrics import stringWidth
                style = flowable.style
                w = max(stringWidth(line, style.fontName, style.fontSize) for line in flowable.lines)
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
    guide = sheet['kind'] == 'study-guide'
    if guide:  # a guide starts one step below the most spacious preset and has no page cap
        presets = presets[1:] or presets
    target = sheet['allowance']['sheets'] * sheet['allowance']['sides']
    block_problem, any_block_fit = None, False
    for index, preset in presets:
        try:  # every candidate must hold each block and code line at its own sizes
            _check_blocks_fit(sheet, fonts, preset, col_w, frame_h)
        except Overflow as error:
            block_problem = error  # the last one is from the tightest preset tried
            continue
        any_block_fit = True
        pages, fill = layout(sheet, fonts, preset)
        if guide or pages <= target:
            return {'preset': index, 'pages': pages, 'column_fill': fill, 'body': preset['body'], 'code': preset['code']}
    if not any_block_fit:
        raise block_problem
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


def _slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:60] or 'sheet'


def _inventory(sheet):
    """(prose, code): every rendered character, split by the font that draws it.

    Backtick spans inside any paragraph field are drawn in the mono font, so they go with code blocks;
    everything else is drawn in the body or bold font. Markup characters are not drawn and are removed.
    """
    fields = [sheet['title'], sheet['course']]
    code = []
    for section in sheet['sections']:
        fields.append(section['title'])
        for block in section['blocks']:
            if block['type'] == 'code':
                code.append(block['text'])
                continue
            for key in ('text', 'setup', 'takeaway', 'prompt', 'first_error', 'fix', 'conditions'):
                if block.get(key):
                    fields.append(block[key])
            for step in block.get('steps', []):
                fields += [step['label'], step['text']]
            fields += block.get('header', []) + [cell for row in block.get('rows', []) for cell in row]
    prose = []
    for field in fields:
        code += _CODE_SPAN.findall(field)
        prose.append(_CODE_SPAN.sub(' ', field))
    return re.sub(r'\*\*|\^\{|_\{|\}', '', ' '.join(prose)), ' '.join(code)


def _previews(pdf_path, out_dir, stem):
    try:
        import pypdfium2 as pdfium
    except ImportError:
        return None
    try:
        document = pdfium.PdfDocument(str(pdf_path))
    except Exception:  # a PDF pdfium cannot open gets no previews; the caller reports previews=none
        return None
    folder = out_dir / 'previews'
    folder.mkdir(exist_ok=True)
    paths = []
    try:
        for i in range(len(document)):
            name = f'previews/{stem}-page-{i + 1}.png'
            document[i].render(scale=150 / 72).to_pil().save(out_dir / name)
            paths.append(name)
    finally:
        document.close()
    return paths


def check_glyphs(sheet, fonts):
    """Raise SheetError naming every character the chosen fonts cannot draw (text in body/bold, code in mono)."""
    text, code = _inventory(sheet)
    problems = {}
    for chars, font in ((missing_glyphs(text, fonts['body']), fonts['body']),
                        (missing_glyphs(text, fonts['bold']), fonts['bold']),
                        (missing_glyphs(code, fonts['mono']), fonts['mono'])):
        for char in chars:
            problems.setdefault(char, set()).add(font)
    if problems:
        listed = ', '.join(f"U+{ord(c):04X} {c!r} ({'/'.join(sorted(f))})" for c, f in sorted(problems.items()))
        raise SheetError(f'missing glyphs: {listed}; rewrite or spell out these characters and re-render')


# Browser engine: the same content and presets as HTML with print CSS, printed by an installed Chromium browser.

NO_ENGINE_QUESTION = 'I can make the PDF if you let me install one Python package (pip install reportlab). Install it?'
MONO_ADVANCE = 0.55  # em, Consolas; wider monospace fonts (Menlo, DejaVu Sans Mono: 0.60) wrap instead of clipping
MONO_ADVANCE_WIDE = 0.6  # em; code height assumes the widest common fallback, so wrapped lines are counted
CODE_PAD = 3.0  # pt of padding on each side of a code block
TAB_SIZE = 4
BODY_FONTS = '"Segoe UI", Arial, "Helvetica Neue", "DejaVu Sans", sans-serif'
CJK_FONTS = '"Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Hiragino Sans", "Malgun Gothic", '
MONO_FONTS = 'Consolas, Menlo, "DejaVu Sans Mono", "Courier New", monospace'


class NoEngine(SheetError):
    """Neither ReportLab nor a Chromium browser is available; a printable HTML file was written instead."""

    def __init__(self, html_path):
        super().__init__(
            f'no PDF engine: ReportLab is not installed and no Edge, Chrome or Chromium was found. '
            f'Printable HTML written (not a PDF; page count unchecked): {html_path}. '
            f'Ask the student exactly: "{NO_ENGINE_QUESTION}" '
            f'If they decline, they can open the HTML and use Print > Save as PDF.')
        self.html_path = html_path


def _css_string(text):
    """A double-quoted CSS string that cannot end the string or the <style> element."""
    return '"' + ''.join(c if c.isalnum() or c in ' .,:;!?()[]-_\'/&+=#%@*' else f'\\{ord(c):x} ' for c in text) + '"'


def _html_block(block):
    kind = block['type']
    if kind == 'text':
        return f'<p class="block">{inline_html(block["text"])}</p>'
    if kind == 'cue':
        return f'<p class="block cue">{inline_html(block["text"])}</p>'
    if kind == 'code':
        return f'<pre class="block code">{html.escape(block["text"], quote=False)}</pre>'
    if kind in ('stages', 'example'):
        parts = [f'<p class="muted">{inline_html(block["setup"])}</p>'] if kind == 'example' and block['setup'] else []
        rows = ''.join(f'<tr><th>{inline_html(s["label"])}</th><td>{inline_html(s["text"])}</td></tr>'
                       for s in block['steps'])
        parts.append(f'<table class="grid steps"><colgroup><col style="width:32%"><col></colgroup>{rows}</table>')
        if kind == 'example' and block['takeaway']:
            parts.append(f'<p class="takeaway">{inline_html("**Takeaway:** " + block["takeaway"])}</p>')
        return f'<div class="block {kind}">' + ''.join(parts) + '</div>'
    if kind == 'table':
        head = ''.join(f'<th>{inline_html(h)}</th>' for h in block['header'])
        body = ''.join('<tr>' + ''.join(f'<td>{inline_html(c)}</td>' for c in row) + '</tr>' for row in block['rows'])
        return f'<table class="block data"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'
    rows = [('Question', block['prompt'])] if block['prompt'] else []
    rows += [('First error', block['first_error']), ('Fix', block['fix'])]
    if block['conditions']:
        rows.append(('Holds when', block['conditions']))
    cells = ''.join(f'<tr><th>{label}</th><td>{inline_html(text)}</td></tr>' for label, text in rows)
    return f'<table class="block grid mistake"><colgroup><col style="width:28%"><col></colgroup>{cells}</table>'


def to_html(sheet, preset_index):
    """A self-contained printable page for one layout preset (no scripts, no external assets)."""
    preset = PRESETS[preset_index]
    columns = 2 if sheet['kind'] == 'exam-sheet' else 1
    paper = 'letter' if sheet['allowance']['paper'] == 'letter' else 'A4'
    fonts = (CJK_FONTS if sheet['language'].split('-')[0] in ('zh', 'ja', 'ko') else '') + BODY_FONTS
    body, gap = preset['body'], preset['gap']
    note = '' if sheet['allowance']['status'] == 'confirmed' else (
        f'@bottom-left {{ content: {_css_string(UNCONFIRMED_NOTE)}; font: 7.5pt {fonts}; color: {MUTED}; }}')
    course = f'@top-right {{ content: {_css_string(sheet["course"])}; font: 8.5pt {fonts}; color: {MUTED}; }}' \
        if sheet['course'] else ''
    css = f'''
@page {{ size: {paper}; margin: {MARGIN + HEADER}pt {MARGIN}pt {MARGIN + FOOTER}pt;
  @top-left {{ content: {_css_string(sheet["title"])}; font: 600 8.5pt {fonts}; color: {MUTED}; }}
  {course}
  {note}
  @bottom-right {{ content: counter(page); font: 7.5pt {fonts}; color: {MUTED}; }} }}
html {{ background: #fff; }}
body {{ margin: 0; color: {INK}; font-family: {fonts}; font-size: {body}pt; line-height: {LEADING};
  columns: {columns}; column-gap: {COLUMN_GAP}pt; column-fill: auto; overflow-wrap: anywhere; }}
.section.high {{ font-size: {round(body * HIGH_SCALE, 2)}pt; }}
h2 {{ font-size: 1.16em; line-height: 1.2; color: {BRAND}; margin: {preset['section_gap']}pt 0 {gap}pt;
  break-after: avoid; }}
.section.high h2 {{ background: {TINT}; padding: 2pt 3pt; }}
body > .section:first-child h2 {{ margin-top: 0; }}
.keep {{ break-inside: avoid; }}
.block {{ margin: 0 0 {gap}pt; break-inside: avoid; }}
p {{ margin: 0 0 {gap}pt; }}
.cue {{ padding-left: 0.9em; text-indent: -0.9em; }}
.cue::before {{ content: "\\2022"; display: inline-block; width: 0.9em; text-indent: 0; }}
.muted {{ color: {MUTED}; }}
table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
th, td {{ text-align: left; vertical-align: top; padding: 1.5pt 3pt; border-bottom: 0.4pt solid {RULE}; font-weight: normal; overflow-wrap: anywhere; }}
.grid th {{ color: {BRAND}; font-weight: 600; }}
.data thead th {{ background: {TINT}; font-weight: 600; }}
.takeaway {{ margin: {round(gap * 0.6, 2)}pt 0 0; }}
code, pre {{ font-family: {MONO_FONTS}; }}
pre.code {{ font-size: {preset['code']}pt; line-height: 1.2; background: #f1f0ea; padding: {CODE_PAD}pt; tab-size: {TAB_SIZE};
  white-space: pre-wrap; overflow-wrap: anywhere; }}
'''
    sections = []
    for section in sheet['sections']:
        blocks = [_html_block(b) for b in section['blocks']]
        title = f'<h2>{inline_html(section["title"])}</h2>'
        weight = ' high' if section['weight'] == 'high' else ''
        sections.append(f'<section class="section{weight}" id="{section["id"]}"><div class="keep">{title}{blocks[0]}</div>'
                        + ''.join(blocks[1:]) + '</section>')
    lang = html.escape(sheet['language'])
    return (f'<!doctype html>\n<html lang="{lang}" data-preset="{preset_index}"><head><meta charset="utf-8">'
            f'<title>{html.escape(sheet["title"])}</title><style>{css}</style></head>\n<body>\n'
            + '\n'.join(sections) + '\n</body></html>\n')


def _browser_candidates():
    import shutil
    paths = []
    if os.name == 'nt':
        for base in (os.environ.get('PROGRAMFILES(X86)'), os.environ.get('PROGRAMFILES'), os.environ.get('LOCALAPPDATA')):
            if base:
                paths += [Path(base) / 'Microsoft/Edge/Application/msedge.exe',
                          Path(base) / 'Google/Chrome/Application/chrome.exe',
                          Path(base) / 'Chromium/Application/chrome.exe']
    paths += [Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
              Path('/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'),
              Path('/Applications/Chromium.app/Contents/MacOS/Chromium')]
    for name in ('msedge', 'microsoft-edge', 'microsoft-edge-stable', 'google-chrome', 'google-chrome-stable',
                 'chromium', 'chromium-browser', 'chrome'):
        found = shutil.which(name)
        if found:
            paths.append(Path(found))
    return paths


def find_browser():
    """Command prefix for the first installed Chromium browser, or None."""
    for path in _browser_candidates():
        if path.is_file():
            return [str(path)]
    return None


def pdf_page_count(data):
    """Page count from the PDF page tree (the root /Pages node has the largest /Count), or None."""
    counts = [int(n) for n in re.findall(rb'/Type\s*/Pages\b[^>]*?/Count\s+(\d+)', data)]
    counts += [int(n) for n in re.findall(rb'/Count\s+(\d+)[^>]*?/Type\s*/Pages\b', data)]
    return max(counts) if counts else None


def _browser_name(browser):
    return Path(browser[-1]).name


def _stop_profile_processes(profile):
    """Stop browser processes started for this print: they are the only ones whose command line names `profile`."""
    import subprocess
    marker = str(profile)
    try:
        if os.name == 'nt':
            quoted = marker.replace("'", "''")
            script = ("Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -ne $PID -and $_.CommandLine "
                      f"-and $_.CommandLine.Contains('{quoted}') }} | ForEach-Object {{ "
                      "Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }")
            subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command', script],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        else:
            subprocess.run(['pkill', '-KILL', '-f', re.escape(marker)], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=30)
    except (OSError, subprocess.SubprocessError):
        pass  # the caller reports the profile if it cannot be removed


def _remove_profile(profile):
    """Remove the throwaway profile, stopping its browser processes if they still hold it. True when removed."""
    import shutil
    import time
    for attempt in range(24):
        shutil.rmtree(profile, ignore_errors=True)
        if not profile.exists():
            return True
        if attempt in (3, 12):  # still in use after about 1 s / 4 s: stop what this print started
            _stop_profile_processes(profile)
        time.sleep(0.25)
    return False


def print_pdf(browser, html_path, pdf_path, timeout=60, leftovers=None):
    """Print `html_path` with a headless browser and a throwaway profile; return the finished PDF bytes.

    A profile that cannot be removed is appended to `leftovers` (and named in the error on failure).
    """
    import subprocess
    import tempfile
    import time
    profile = Path(tempfile.mkdtemp(prefix='gim-sheet-browser-'))
    command = list(browser) + ['--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
                               '--disable-extensions', f'--user-data-dir={profile}', '--no-pdf-header-footer',
                               '--print-to-pdf-no-header', f'--print-to-pdf={pdf_path}', html_path.resolve().as_uri()]
    name = _browser_name(browser)
    deadline = time.monotonic() + timeout
    data, failure, removed = None, None, True
    try:
        try:
            # Output goes to DEVNULL: a detached browser child must not keep our pipes (and this call) open.
            subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=timeout)
        except (OSError, subprocess.SubprocessError) as error:
            failure = f'the browser ({name}) could not print the sheet: {error}'
        if failure is None:
            # Some launchers (Edge on Windows) return before the PDF exists: wait for a complete, stable file.
            last = -1
            while time.monotonic() < deadline:
                try:
                    current = pdf_path.read_bytes() if pdf_path.is_file() else None
                except OSError:  # still being written (sharing violation): try again until the deadline
                    current = None
                if current is not None:
                    if current.startswith(b'%PDF') and current.rstrip().endswith(b'%%EOF') and len(current) == last:
                        data = current
                        break
                    last = len(current)
                time.sleep(0.25)
            else:
                failure = f'the browser ({name}) did not write a complete PDF within {timeout}s'
    finally:  # runs on every exit, including unexpected errors and interrupts
        if data is None:
            _stop_profile_processes(profile)
        removed = _remove_profile(profile)
        if not removed and leftovers is not None:
            leftovers.append(str(profile))
    if failure is not None:
        raise SheetError(failure + ('' if removed else f'; temporary browser profile left at {profile}'))
    return data


def _candidate_presets(sheet):
    min_body = max(9.0, float(sheet['allowance']['min_body'] or 0))
    presets = [(i, p) for i, p in enumerate(PRESETS) if p['body'] >= min_body]
    if not presets:
        raise Overflow(0, [], f'no layout preset meets the minimum body size {min_body}pt')
    if sheet['kind'] == 'study-guide':
        presets = presets[1:] or presets
    return presets


def _code_fits(sheet, preset, col_w, frame_h):
    """Estimated code width and height against one column, or an Overflow describing the first problem.

    Code is the one block the browser cannot break sensibly; other blocks taller than a column are
    continued in the next column (never clipped), as `break-inside: avoid` allows.
    """
    for section in sheet['sections']:
        for block in section['blocks']:
            if block['type'] != 'code':
                continue
            lines = [line.expandtabs(TAB_SIZE) for line in block['text'].splitlines()]
            text_w = col_w - 2 * CODE_PAD
            widest = max(len(line) for line in lines) * MONO_ADVANCE * preset['code']
            if widest > text_w + 0.5:
                return Overflow(widest - text_w, [], f'a code line in section {section["id"]} is wider than one column')
            visual = sum(max(1, math.ceil(len(line) * MONO_ADVANCE_WIDE * preset['code'] / text_w)) for line in lines)
            height = visual * preset['code'] * 1.2 + 2 * CODE_PAD + preset['gap']
            if height > frame_h:
                return Overflow(height - frame_h, [(section['id'], round(height, 1))],
                                f'a block in section {section["id"]} is taller than one column')
    return None


def fit_browser(sheet, browser, work, timeout=60, leftovers=None):
    """Print each permitted preset (most spacious first) until one fits; returns (index, pages, pdf, html)."""
    presets = _candidate_presets(sheet)
    _, _, columns, col_w, frame_h = _geometry(sheet)
    guide = sheet['kind'] == 'study-guide'
    target = sheet['allowance']['sheets'] * sheet['allowance']['sides']
    problem, pages = None, None
    for index, preset in presets:
        problem = _code_fits(sheet, preset, col_w, frame_h)
        if problem:
            continue
        html_path, pdf_path = work / f'preset-{index}.html', work / f'preset-{index}.pdf'
        html_path.write_text(to_html(sheet, index), encoding='utf-8')
        pages = pdf_page_count(print_pdf(browser, html_path, pdf_path, timeout, leftovers))
        if pages is None:
            raise SheetError(f'the browser ({_browser_name(browser)}) wrote a PDF without a readable page count')
        if guide or pages <= target:
            return index, pages, pdf_path, html_path
    if pages is None:
        raise problem
    raise Overflow((pages - target) * columns * frame_h, [],
                   f'content needs {pages} pages at the tightest permitted size, {target} allowed (browser engine)')


def _engine(requested):
    if requested != 'auto':
        return requested
    try:
        import reportlab  # noqa: F401
    except ImportError:
        return 'browser'
    return 'reportlab'


def render(sheet, out_dir, force=False, engine='auto', browser=None, timeout=60):
    """Check, fit, then write the PDF, a content copy, previews (when possible) and checks.json.

    Nothing is written when a check fails, so an existing round is never replaced by a failed render.
    The browser engine also keeps the printable HTML; with no browser it writes only that HTML and raises NoEngine.
    """
    import json
    stem = f"{_slug(sheet['title'])}-v{sheet['revision']['round']}"
    pdf_path = out_dir / f'{stem}.pdf'
    if pdf_path.exists() and not force:
        raise SheetError(f'{pdf_path.name} already exists; pass --force to replace this round')
    if _engine(engine) == 'browser':
        return _render_browser(sheet, out_dir, stem, browser or find_browser(), timeout)
    fonts = find_fonts(sheet['language'])
    check_glyphs(sheet, fonts)
    result = fit(sheet, fonts)
    out_dir.mkdir(parents=True, exist_ok=True)
    preset = PRESETS[result['preset']]
    built = _build(sheet, fonts, preset, str(pdf_path))
    (out_dir / f'{stem}.json').write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    checks = {'engine': 'reportlab', 'pdf': pdf_path.name, 'pages': built['pages'], 'preset': result['preset'],
              'body': preset['body'], 'code': preset['code'], 'column_fill': built['column_fill'],
              'fonts': {k: fonts[k] for k in ('body', 'bold', 'mono')} | {'files': fonts['files']},
              'missing_glyphs': [], 'allowance': sheet['allowance'], 'kind': sheet['kind'],
              'previews': _previews(pdf_path, out_dir, stem)}
    (out_dir / 'checks.json').write_text(json.dumps(checks, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return checks


def _render_browser(sheet, out_dir, stem, browser, timeout):
    import json
    import shutil
    import tempfile
    if browser is None:
        presets = _candidate_presets(sheet)
        index = presets[0][0] if sheet['kind'] == 'study-guide' else presets[-1][0]  # tightest: likeliest to fit
        out_dir.mkdir(parents=True, exist_ok=True)
        html_path = out_dir / f'{stem}.html'
        html_path.write_text(to_html(sheet, index), encoding='utf-8')
        raise NoEngine(html_path)
    with tempfile.TemporaryDirectory(prefix='gim-sheet-') as work:
        leftovers = []
        index, pages, tmp_pdf, tmp_html = fit_browser(sheet, browser, Path(work), timeout, leftovers)
        out_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = out_dir / f'{stem}.pdf'
        shutil.copyfile(tmp_pdf, pdf_path)
        shutil.copyfile(tmp_html, out_dir / f'{stem}.html')
    preset = PRESETS[index]
    (out_dir / f'{stem}.json').write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    checks = {'engine': 'browser', 'browser': _browser_name(browser), 'pdf': pdf_path.name, 'html': f'{stem}.html',
              'pages': pages, 'preset': index, 'body': preset['body'], 'code': preset['code'], 'column_fill': None,
              'missing_glyphs': 'unchecked', 'leftover_profiles': leftovers, 'allowance': sheet['allowance'],
              'kind': sheet['kind'],
              'previews': _previews(pdf_path, out_dir, stem)}
    (out_dir / 'checks.json').write_text(json.dumps(checks, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return checks


def main(argv=None):
    import argparse
    import json
    parser = argparse.ArgumentParser(description='Render an exam reference sheet or study guide to PDF.')
    parser.add_argument('content', type=Path)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument('--out', type=Path, help='folder for the PDF, previews and checks.json')
    target.add_argument('--check', action='store_true', help='validate and fit without writing files')
    parser.add_argument('--force', action='store_true', help='replace this revision round if it exists')
    parser.add_argument('--engine', choices=('auto', 'reportlab', 'browser'), default='auto',
                        help='auto: ReportLab when installed, otherwise an installed Edge/Chrome/Chromium')
    parser.add_argument('--browser', type=Path, help='path to a Chromium-based browser for the browser engine')
    args = parser.parse_args(argv)
    try:
        try:
            data = json.loads(args.content.read_text(encoding='utf-8'))
        except OSError as error:
            raise SheetError(f'cannot read {args.content}: {error.strerror or error}') from None
        except json.JSONDecodeError as error:
            raise SheetError(f'{args.content} is not valid JSON (line {error.lineno}: {error.msg})') from None
        sheet = load_sheet(data)
        engine = _engine(args.engine)
        if engine == 'reportlab':
            try:
                import reportlab  # noqa: F401
            except ImportError:
                print(f'ERROR reportlab is not installed; ask the student exactly: "{NO_ENGINE_QUESTION}" '
                      'or use --engine auto to print through an installed browser')
                return 3
        browser = [str(args.browser)] if args.browser else None
        if browser and not args.browser.is_file():
            raise SheetError(f'browser not found: {args.browser}')
        if args.check:
            if engine == 'browser':
                import tempfile
                browser = browser or find_browser()
                if browser is None:
                    raise SheetError('no PDF engine to check the fit: ReportLab is not installed and no browser was found')
                with tempfile.TemporaryDirectory(prefix='gim-sheet-') as work:
                    index, pages, _, _ = fit_browser(sheet, browser, Path(work))
                print(f"OK pages={pages} preset={index} body={PRESETS[index]['body']}pt out=none engine=browser")
                return 0
            fonts = find_fonts(sheet['language'])
            check_glyphs(sheet, fonts)
            result = fit(sheet, fonts)
            print(f"OK pages={result['pages']} preset={result['preset']} body={result['body']}pt out=none engine=reportlab")
            return 0
        checks = render(sheet, args.out, args.force, engine=engine, browser=browser)
        line = f"OK pages={checks['pages']} preset={checks['preset']} body={checks['body']}pt out={args.out / checks['pdf']}"
        if checks['previews'] is None:
            line += ' previews=none'
        line += f" engine={checks['engine']}"
        if checks['engine'] == 'browser':
            line += ' glyphs=unchecked'
            if checks['leftover_profiles']:
                line += f" leftover_profiles={len(checks['leftover_profiles'])}"
        print(line)
        return 0
    except NoEngine as error:
        print(f'ERROR {error}')
        return 3
    except Overflow as error:
        sections = ','.join(f'{sid}:{h:.0f}' for sid, h in error.sections)
        print(f'OVERFLOW over={error.over_pt:.0f}pt sections={sections} reason={error.reason}')
        return 2
    except SheetError as error:
        print(f'ERROR {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
