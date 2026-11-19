"""Standard-library PDF writer for render_sheet.py: no ReportLab, no browser, works inside sandboxes.

It reads system TrueType fonts (glyf outlines, embedding permitted), embeds a subset of each, lays the sheet
out in columns with the same presets as the ReportLab engine, and writes a PDF 1.4 file with extractable text
(ToUnicode maps). Every block is kept together; a block taller than one column, or a code line wider than one,
is reported instead of being split or clipped.
"""
from pathlib import Path
import os
import re
import struct
import zlib

ROLES = ('body', 'bold', 'mono')


class NoFont(Exception):
    """No usable TrueType font for a role on this host."""


class TooTall(Exception):
    def __init__(self, section, height, reason):
        super().__init__(reason)
        self.section, self.height, self.reason = section, height, reason


# ---------------------------------------------------------------- fonts

def _candidates(language):
    windir = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'
    mac = Path('/System/Library/Fonts/Supplemental')
    linux_dirs = [Path('/usr/share/fonts'), Path('/usr/local/share/fonts'), Path.home() / '.fonts']
    linux = {p.name: p for d in linux_dirs if d.is_dir() for p in d.rglob('*.ttf')}
    found = {
        'body': [windir / 'segoeui.ttf', windir / 'arial.ttf', mac / 'Arial.ttf', linux.get('DejaVuSans.ttf'),
                 linux.get('LiberationSans-Regular.ttf')],
        'bold': [windir / 'segoeuib.ttf', windir / 'arialbd.ttf', mac / 'Arial Bold.ttf',
                 linux.get('DejaVuSans-Bold.ttf'), linux.get('LiberationSans-Bold.ttf')],
        'mono': [windir / 'consola.ttf', windir / 'cour.ttf', mac / 'Courier New.ttf',
                 linux.get('DejaVuSansMono.ttf'), linux.get('LiberationMono-Regular.ttf')],
    }
    if language.split('-')[0] in ('zh', 'ja', 'ko'):
        cjk = [windir / 'simhei.ttf', windir / 'simsunb.ttf', mac / 'Arial Unicode.ttf',
               linux.get('NotoSansCJK-Regular.ttf'), linux.get('wqy-microhei.ttf')]
        found['body'] = cjk + found['body']
        found['bold'] = cjk + found['bold']
    return found


def find_font_files(language='en'):
    """{role: path} of the first usable font per role, or None if a role has none."""
    chosen = {}
    for role, paths in _candidates(language).items():
        for path in paths:
            if path is not None and path.is_file():
                try:
                    TrueType(path)
                except (ValueError, OSError, struct.error):
                    continue
                chosen[role] = path
                break
        else:
            return None
    return chosen


_CACHE = {}


def load_fonts(language='en'):
    files = find_font_files(language)
    if files is None:
        raise NoFont('no usable TrueType font (Segoe UI, Arial, DejaVu Sans or Liberation, plus a monospace font)')
    out = {}
    for role, path in files.items():
        key = str(path)
        if key not in _CACHE:
            _CACHE[key] = TrueType(path)
        out[role] = _CACHE[key]
    out['files'] = {role: str(path) for role, path in files.items()}
    return out


class TrueType:
    """The parts of a TrueType (glyf) font needed to measure, subset and embed it."""

    def __init__(self, path):
        self.path = Path(path)
        data = self.path.read_bytes()
        self.data = data
        if data[:4] not in (b'\x00\x01\x00\x00', b'true'):
            raise ValueError('not a single TrueType font')
        count = struct.unpack('>H', data[4:6])[0]
        self.tables = {}
        for i in range(count):
            tag, _, offset, length = struct.unpack('>4sIII', data[12 + 16 * i: 28 + 16 * i])
            self.tables[tag.decode('latin-1')] = data[offset:offset + length]
        for need in ('head', 'hhea', 'hmtx', 'maxp', 'cmap', 'loca', 'glyf'):
            if need not in self.tables:
                raise ValueError(f'font lacks {need}')
        os2 = self.tables.get('OS/2', b'')
        fs_type = struct.unpack('>H', os2[8:10])[0] if len(os2) >= 10 else 0
        if fs_type & 0x000F == 0x0002 or fs_type & 0x0200:  # restricted licence or bitmap-only embedding
            raise ValueError('font licence does not permit embedding')
        self.no_subset = bool(fs_type & 0x0100)  # licence allows embedding only the whole font
        head = self.tables['head']
        self.units = struct.unpack('>H', head[18:20])[0]
        self.bbox = struct.unpack('>hhhh', head[36:44])
        self.loca_long = struct.unpack('>h', head[50:52])[0] == 1
        hhea = self.tables['hhea']
        self.ascent, self.descent = struct.unpack('>hh', hhea[4:8])
        n_metrics = struct.unpack('>H', hhea[34:36])[0]
        self.glyphs = struct.unpack('>H', self.tables['maxp'][4:6])[0]
        hmtx = self.tables['hmtx']
        advances = [struct.unpack('>H', hmtx[4 * i:4 * i + 2])[0] for i in range(n_metrics)]
        self.advances = advances + [advances[-1]] * (self.glyphs - n_metrics)
        self.cap = struct.unpack('>h', os2[88:90])[0] if len(os2) >= 90 else int(self.ascent * 0.7)
        self.cmap = self._cmap(self.tables['cmap'])
        name = re.sub(r'[^A-Za-z0-9-]', '', self.path.stem) or 'Font'
        self.name = name[:40]

    @staticmethod
    def _cmap(table):
        count = struct.unpack('>H', table[2:4])[0]
        subtables = {}
        for i in range(count):
            platform, encoding, offset = struct.unpack('>HHI', table[4 + 8 * i: 12 + 8 * i])
            subtables[(platform, encoding)] = offset
        mapping = {}
        offset = subtables.get((3, 10)) or subtables.get((0, 4))
        if offset is not None and struct.unpack('>H', table[offset:offset + 2])[0] == 12:
            groups = struct.unpack('>I', table[offset + 12:offset + 16])[0]
            for g in range(groups):
                start, end, gid = struct.unpack('>III', table[offset + 16 + 12 * g: offset + 28 + 12 * g])
                for code in range(start, min(end, 0x10FFFF) + 1):
                    mapping[code] = gid + code - start
            return mapping
        offset = subtables.get((3, 1)) or subtables.get((0, 3))
        if offset is None or struct.unpack('>H', table[offset:offset + 2])[0] != 4:
            raise ValueError('no Unicode cmap')
        seg2 = struct.unpack('>H', table[offset + 6:offset + 8])[0]
        ends = offset + 14
        starts = ends + seg2 + 2
        deltas = starts + seg2
        ranges = deltas + seg2
        for s in range(seg2 // 2):
            end = struct.unpack('>H', table[ends + 2 * s: ends + 2 * s + 2])[0]
            start = struct.unpack('>H', table[starts + 2 * s: starts + 2 * s + 2])[0]
            delta = struct.unpack('>h', table[deltas + 2 * s: deltas + 2 * s + 2])[0]
            range_offset = struct.unpack('>H', table[ranges + 2 * s: ranges + 2 * s + 2])[0]
            for code in range(start, end + 1):
                if code == 0xFFFF:
                    continue
                if range_offset == 0:
                    gid = (code + delta) & 0xFFFF
                else:
                    at = ranges + 2 * s + range_offset + 2 * (code - start)
                    gid = struct.unpack('>H', table[at:at + 2])[0]
                    gid = (gid + delta) & 0xFFFF if gid else 0
                if gid:
                    mapping[code] = gid
        return mapping

    def gid(self, char):
        return self.cmap.get(ord(char), 0)

    def width(self, text, size):
        return sum(self.advances[self.gid(c)] for c in text) * size / self.units

    def missing(self, text):
        return {c for c in text if not c.isspace() and ord(c) not in self.cmap}

    def _glyph_range(self, gid):
        loca = self.tables['loca']
        if self.loca_long:
            a, b = struct.unpack('>II', loca[4 * gid:4 * gid + 8])
        else:
            a, b = (2 * x for x in struct.unpack('>HH', loca[2 * gid:2 * gid + 4]))
        return a, b

    def subset(self, gids):
        """A valid font file keeping glyph IDs, with outlines only for `gids` (plus composite parts).

        Fonts whose licence forbids subsetting (OS/2 fsType bit 8) are returned whole.
        """
        if self.no_subset:
            return self.data
        glyf = self.tables['glyf']
        keep, todo = set(), set(gids) | {0}
        while todo:
            gid = todo.pop()
            if gid in keep or gid >= self.glyphs:
                continue
            keep.add(gid)
            a, b = self._glyph_range(gid)
            if b - a >= 10 and struct.unpack('>h', glyf[a:a + 2])[0] < 0:  # composite: collect its components
                at = a + 10
                while True:
                    flags, part = struct.unpack('>HH', glyf[at:at + 4])
                    todo.add(part)
                    at += 4 + (4 if flags & 0x0001 else 2)
                    at += 8 if flags & 0x0080 else 4 if flags & 0x0040 else 2 if flags & 0x0008 else 0
                    if not flags & 0x0020:
                        break
        new_glyf, offsets = bytearray(), []
        for gid in range(self.glyphs):
            offsets.append(len(new_glyf))
            if gid in keep:
                a, b = self._glyph_range(gid)
                new_glyf += glyf[a:b]
                new_glyf += b'\0' * (-len(new_glyf) % 4)
        offsets.append(len(new_glyf))
        head = bytearray(self.tables['head'])
        head[8:12] = b'\0\0\0\0'  # checkSumAdjustment: not used by PDF readers
        head[50:52] = struct.pack('>h', 1)
        tables = {'head': bytes(head), 'hhea': self.tables['hhea'], 'hmtx': self.tables['hmtx'],
                  'maxp': self.tables['maxp'], 'loca': struct.pack(f'>{len(offsets)}I', *offsets), 'glyf': bytes(new_glyf)}
        for optional in ('cvt ', 'fpgm', 'prep', 'OS/2'):
            if optional in self.tables:
                tables[optional] = self.tables[optional]
        return _font_file(tables)


def _checksum(data):
    data += b'\0' * (-len(data) % 4)
    return sum(struct.unpack(f'>{len(data) // 4}I', data)) & 0xFFFFFFFF


def _font_file(tables):
    tags = sorted(tables)
    n = len(tags)
    power = 1 << (n.bit_length() - 1)
    header = struct.pack('>IHHHH', 0x00010000, n, power * 16, power.bit_length() - 1, n * 16 - power * 16)
    offset = 12 + 16 * n
    directory, body = b'', b''
    for tag in tags:
        data = tables[tag]
        directory += struct.pack('>4sIII', tag.encode('latin-1'), _checksum(data), offset + len(body), len(data))
        body += data + b'\0' * (-len(data) % 4)
    return header + directory + body


# ---------------------------------------------------------------- inline text

_CODE = re.compile(r'`([^`]+)`')
_MARK = re.compile(r'\*\*(.+?)\*\*|\^\{(.+?)\}|_\{(.+?)\}')


def runs(text, bold=False):
    """[(text, role, kind)] with kind '', 'sup' or 'sub'.

    As in the ReportLab engine, `code` spans are split out first and kept literal; **bold**, ^{sup} and _{sub}
    apply outside them, and markup nests inside bold. Unmatched markers stay literal.
    """
    out, last = [], 0
    for match in _CODE.finditer(text):
        out += _marked(text[last:match.start()], bold)
        out.append((match.group(1), 'mono', ''))
        last = match.end()
    return out + _marked(text[last:], bold)


def _marked(text, bold):
    out, last = [], 0
    base = 'bold' if bold else 'body'
    for match in _MARK.finditer(text):
        if match.start() > last:
            out.append((text[last:match.start()], base, ''))
        strong, sup, sub = match.groups()
        if strong is not None:
            out += _marked(strong, True)
        elif sup is not None:
            out.append((sup, base, 'sup'))
        else:
            out.append((sub, base, 'sub'))
        last = match.end()
    if last < len(text):
        out.append((text[last:], base, ''))
    return out


def plain(text):
    """The characters a cell prints, without markup."""
    return ''.join(part for part, _, _ in runs(text))


def table_widths(columns, width, measure, pad=6.0):
    """Column widths for a table: every column at least as wide as its longest word when the total allows,
    remaining space shared by how much each column's longest cell still needs; equal shares otherwise.

    `columns` lists each column's cells (header first); `measure(text, bold=False)` gives a width in points.
    """
    count = len(columns)
    equal = [width / count] * count
    mins = [max((measure(word, bold=row == 0) for row, cell in enumerate(col) for word in plain(cell).split()),
                default=0.0) + pad for col in columns]
    if sum(mins) > width + 0.01:
        return equal
    natural = [max(m, max((measure(plain(cell), bold=row == 0) for row, cell in enumerate(col)), default=0.0) + pad)
               for m, col in zip(mins, columns)]
    if sum(natural) <= width:
        extra = (width - sum(natural)) / count
        return [n + extra for n in natural]
    room = width - sum(mins)
    wants = [n - m for m, n in zip(mins, natural)]
    return [m + room * w / sum(wants) for m, w in zip(mins, wants)]


def label_width(labels, width, share, measure, pad=6.0, cap=0.45):
    """Label column of a two-column grid: `share` of the width, widened (up to `cap`) so the longest
    label word is not split."""
    longest = max((measure(word, bold=True) for label in labels for word in plain(label).split()), default=0.0)
    return min(max(width * share, longest + pad), width * cap)


class Layout:
    """Measures and wraps text for one preset; collects drawing operations."""

    def __init__(self, fonts, size, color):
        self.fonts, self.size, self.color = fonts, size, color

    def measure(self, text, bold=False):
        """Printed width of `text` (markup applied, whitespace collapsed) at this layout's size."""
        text = re.sub(r'\s+', ' ', text).strip()
        return sum(self.fonts[role].width(part, self.seg_size(kind, self.size)) for part, role, kind in runs(text, bold))

    def seg_size(self, kind, size):
        return size * 0.7 if kind in ('sup', 'sub') else size

    def wrap(self, text, width, size=None, bold=False, color=None):
        """Lines of [(text, role, kind, size, color)] fitting `width`; long words are broken by character."""
        size = size or self.size
        color = color or self.color
        text = re.sub(r'\s+', ' ', text).strip()
        pieces = []  # (word or ' ', role, kind)
        for chunk, role, kind in runs(text, bold):
            for part in re.split(r'( )', chunk):
                if part:
                    pieces.append((part, role, kind))
        lines, line, used = [], [], 0.0

        def w(piece):
            part, role, kind = piece
            return self.fonts[role].width(part, self.seg_size(kind, size))

        def flush():
            nonlocal line, used
            while line and line[-1][0] == ' ':
                used -= w(line.pop())
            lines.append(line)
            line, used = [], 0.0
        for piece in pieces:
            if piece[0] == ' ' and not line:
                continue
            width_p = w(piece)
            if used + width_p <= width + 0.01:
                line.append(piece)
                used += width_p
                continue
            if line and piece[0] != ' ':
                flush()
            if piece[0] == ' ':
                continue
            if width_p <= width + 0.01:
                line.append(piece)
                used += width_p
                continue
            part, role, kind = piece  # a token wider than the line: break it by character
            chunk = ''
            for char in part:
                if self.fonts[role].width(chunk + char, self.seg_size(kind, size)) + used > width + 0.01 and (chunk or line):
                    if chunk:
                        line.append((chunk, role, kind))
                    flush()
                    chunk = char
                else:
                    chunk += char
            if chunk:
                line.append((chunk, role, kind))
                used += self.fonts[role].width(chunk, self.seg_size(kind, size))
        if line or not lines:
            flush()
        return [[(p, r, k, size, color) for p, r, k in ln] for ln in lines]


# ---------------------------------------------------------------- page model

class Canvas:
    def __init__(self):
        self.ops = []
        self.used = {role: {} for role in ROLES}  # role -> {gid: char}

    def rect(self, x, y, w, h, color):
        self.ops.append(f'{_rgb(color)} rg {x:.2f} {y:.2f} {w:.2f} {h:.2f} re f')

    def line(self, x1, y1, x2, y2, color, width):
        self.ops.append(f'{_rgb(color)} RG {width:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S')

    def text(self, fonts, x, y, segments):
        """Draw one line of segments starting at baseline (x, y)."""
        for part, role, kind, size, color in segments:
            font = fonts[role]
            draw = size * 0.7 if kind in ('sup', 'sub') else size
            rise = size * 0.33 if kind == 'sup' else -size * 0.12 if kind == 'sub' else 0
            gids = []
            for char in part:
                gid = font.gid(char)
                self.used[role].setdefault(gid, char)
                gids.append(gid)
            hexed = ''.join(f'{g:04X}' for g in gids)
            self.ops.append(f'BT /F{ROLES.index(role) + 1} {draw:.2f} Tf {_rgb(color)} rg {rise:.2f} Ts '
                            f'{x:.2f} {y:.2f} Td <{hexed}> Tj ET')
            x += font.width(part, draw)

    def text_right(self, fonts, x_right, y, segments):
        width = sum(fonts[r].width(p, s * 0.7 if k in ('sup', 'sub') else s) for p, r, k, s, _ in segments)
        self.text(fonts, x_right - width, y, segments)


def _rgb(color):
    color = color.lstrip('#')
    return ' '.join(f'{int(color[i:i + 2], 16) / 255:.3f}' for i in (0, 2, 4))


class Box:
    """A block measured at a width: height plus a draw(canvas, x, top) callback."""

    def __init__(self, height, draw, space_after=0.0, space_before=0.0):
        self.height, self.draw, self.space_after, self.space_before = height, draw, space_after, space_before


def _paragraph(lay, fonts, lines, leading, left=0.0, bullet=None):
    height = leading * len(lines)

    def draw(canvas, x, top):
        baseline = top - leading * 0.8
        if bullet:
            canvas.text(fonts, x, baseline, bullet)
        for line in lines:
            canvas.text(fonts, x + left, baseline, line)
            baseline -= leading
    return height, draw


def build_blocks(section, fonts, preset, width, theme):
    """Boxes for a section: the title box first, then one box per block."""
    scale = theme['HIGH_SCALE'] if section['weight'] == 'high' else 1.0
    size = preset['body'] * scale
    leading = size * theme['LEADING']
    gap = preset['gap']
    lay = Layout(fonts, size, theme['INK'])

    def para(text, color=None, bold=False, left=0.0, bullet=None, w=None):
        lines = lay.wrap(text, (w or width) - left, size, bold, color)
        return _paragraph(lay, fonts, lines, leading, left, bullet)

    boxes = []
    t_size = size * 1.16
    t_lead = t_size * 1.2
    t_lines = lay.wrap(section['title'], width - (6 if section['weight'] == 'high' else 0), t_size, True, theme['BRAND'])
    t_height = t_lead * len(t_lines) + (4 if section['weight'] == 'high' else 0)

    def draw_title(canvas, x, top):
        if section['weight'] == 'high':
            canvas.rect(x, top - t_height, width, t_height, theme['TINT'])
            x, top = x + 3, top - 2
        baseline = top - t_lead * 0.8
        for line in t_lines:
            canvas.text(fonts, x, baseline, line)
            baseline -= t_lead
    boxes.append(Box(t_height, draw_title, gap, preset['section_gap']))

    for block in section['blocks']:
        kind = block['type']
        if kind == 'text':
            h, d = para(block['text'])
            boxes.append(Box(h, d, gap))
        elif kind == 'cue':
            indent = size * 0.9
            bullet = [('\u2022', 'body', '', size, theme['INK'])] if fonts['body'].gid('\u2022') else \
                [('-', 'body', '', size, theme['INK'])]
            h, d = para(block['text'], left=indent, bullet=bullet)
            boxes.append(Box(h, d, gap))
        elif kind == 'code':
            code_size = preset['code']
            c_lead = code_size * 1.2
            lines = block['text'].expandtabs(4).splitlines() or ['']
            widest = max(fonts['mono'].width(line, code_size) for line in lines)
            if widest > width - 6 + 0.5:
                raise TooTall(section['id'], widest, f'a code line in section {section["id"]} is wider than one column')
            h = c_lead * len(lines) + 6

            def draw_code(canvas, x, top, lines=lines, h=h, code_size=code_size, c_lead=c_lead):
                canvas.rect(x, top - h, width, h, theme['CODE_BG'])
                baseline = top - 3 - c_lead * 0.8
                for line in lines:
                    if line:
                        canvas.text(fonts, x + 3, baseline, [(line, 'mono', '', code_size, theme['INK'])])
                    baseline -= c_lead
            boxes.append(Box(h, draw_code, gap + 2))
        elif kind in ('stages', 'example', 'mistake'):
            parts = []
            if kind == 'example' and block['setup']:
                parts.append(('para', para(block['setup'], color=theme['MUTED'])))
            if kind == 'mistake':
                rows = ([('Question', block['prompt'])] if block['prompt'] else []) + \
                    [('First error', block['first_error']), ('Fix', block['fix'])] + \
                    ([('Holds when', block['conditions'])] if block['conditions'] else [])
                label_w = label_width([r[0] for r in rows], width, 0.28, lay.measure)
            else:
                rows = [(s['label'], s['text']) for s in block['steps']]
                label_w = label_width([r[0] for r in rows], width, 0.32, lay.measure)
            parts.append(('grid', _grid(lay, fonts, rows, [label_w, width - label_w], size, leading, theme,
                                        label_role=True)))
            if kind == 'example' and block['takeaway']:
                parts.append(('gap', gap * 0.6))
                parts.append(('para', para('**Takeaway:** ' + block['takeaway'])))
            boxes.append(_stack(parts, gap))
        elif kind == 'table':
            columns = [[h] + [r[i] for r in block['rows']] for i, h in enumerate(block['header'])]
            widths = table_widths(columns, width, lay.measure)
            rows = [[f'**{h}**' if h else '' for h in block['header']]] + block['rows']
            boxes.append(_stack([('grid', _grid(lay, fonts, rows, widths, size, leading, theme, header=True))], gap))
    return boxes


def _stack(parts, gap):
    height = sum(p[1] if p[0] == 'gap' else p[1][0] for p in parts)

    def draw(canvas, x, top):
        for kind, item in parts:
            if kind == 'gap':
                top -= item
                continue
            item[1](canvas, x, top)
            top -= item[0]
    return Box(height, draw, gap)


def _grid(lay, fonts, rows, widths, size, leading, theme, header=False, label_role=False):
    pad_x, pad_y = 3.0, 1.5
    laid = []
    for r, row in enumerate(rows):
        cells = []
        for c, text in enumerate(row):
            if label_role and c == 0:
                lines = lay.wrap(text, widths[c] - 2 * pad_x, size, True, theme['BRAND'])
            else:
                lines = lay.wrap(text, widths[c] - 2 * pad_x, size)
            cells.append(lines)
        laid.append((cells, max(len(c) for c in cells) * leading + 2 * pad_y))
    height = sum(h for _, h in laid)

    def draw(canvas, x, top):
        y = top
        for r, (cells, h) in enumerate(laid):
            if header and r == 0:
                canvas.rect(x, y - h, sum(widths), h, theme['TINT'])
            cx = x
            for c, lines in enumerate(cells):
                baseline = y - pad_y - leading * 0.8
                for line in lines:
                    canvas.text(fonts, cx + pad_x, baseline, line)
                    baseline -= leading
                cx += widths[c]
            y -= h
            canvas.line(x, y, x + sum(widths), y, theme['RULE'], 0.4)
    return height, draw


def layout(sheet, fonts, preset, geometry, theme):
    """Flow sections into columns. Returns pages [[(column, top_used, [(box, y_top)])...]], heights, fill."""
    _, _, columns, col_w, frame_h = geometry
    units, heights = [], []
    for section in sheet['sections']:
        boxes = build_blocks(section, fonts, preset, col_w, theme)
        total = sum(b.space_before + b.height + b.space_after for b in boxes)
        heights.append((section['id'], round(total, 1)))
        for box in boxes:
            if box.height > frame_h:
                raise TooTall(section['id'], box.height, f'a block in section {section["id"]} is taller than one column')
        units.append((section['id'], [boxes[0], boxes[1]] if len(boxes) > 1 else [boxes[0]]))
        units += [(section['id'], [b]) for b in boxes[2:]]
    placed = [[]]  # list of columns; each column a list of (box, offset_from_top)
    used = 0.0
    for _, group in units:
        lead = group[0].space_before if placed[-1] else 0.0
        need = lead + sum(b.height for b in group) + sum(b.space_after for b in group[:-1])
        if placed[-1] and used + need > frame_h + 0.01:
            placed.append([])
            used, lead = 0.0, 0.0
            need = sum(b.height for b in group) + sum(b.space_after for b in group[:-1])
        if need > frame_h + 0.01:  # a title + first block that cannot share a column: let them part
            for box in group:
                if placed[-1] and used + box.height > frame_h + 0.01:
                    placed.append([])
                    used = 0.0
                placed[-1].append((box, used))
                used += box.height + box.space_after
            continue
        used += lead
        for box in group:
            placed[-1].append((box, used))
            used += box.height + box.space_after
    fill = []
    for column in placed:
        bottom = max((off + box.height for box, off in column), default=0.0)
        fill.append(round(min(bottom / frame_h, 1.0), 3))
    pages = (len(placed) + columns - 1) // columns
    return {'columns': placed, 'pages': pages, 'heights': heights, 'fill': fill}


# ---------------------------------------------------------------- PDF output

def write_pdf(sheet, fonts, result, geometry, theme, path):
    page_w, page_h, columns, col_w, frame_h = geometry
    margin, footer = theme['MARGIN'], theme['FOOTER']
    canvases = []
    for p in range(result['pages']):
        canvas = Canvas()
        for c in range(columns):
            index = p * columns + c
            if index >= len(result['columns']):
                break
            x = margin + c * (col_w + theme['COLUMN_GAP'])
            top = margin + footer + frame_h
            for box, offset in result['columns'][index]:
                box.draw(canvas, x, top - offset)
        _decorate(canvas, sheet, fonts, theme, page_w, page_h, p + 1)
        canvases.append(canvas)

    objects = []

    def add(body):
        objects.append(body)
        return len(objects)
    font_ids = {}
    for role in ROLES:
        used = {}
        for canvas in canvases:
            used.update(canvas.used[role])
        font_ids[role] = _embed_font(add, fonts[role], used, role)
    resources = '<< /Font << ' + ' '.join(f'/F{i + 1} {font_ids[r]} 0 R' for i, r in enumerate(ROLES)) + ' >> >>'
    pages_id = len(objects) + 1 + 2 * len(canvases)  # contents + page objects come first, then the tree
    kids = []
    for canvas in canvases:
        stream = zlib.compress('\n'.join(canvas.ops).encode('latin-1'))
        content = add(_stream(stream, '/Filter /FlateDecode'))
        kids.append(add(f'<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {page_w:.2f} {page_h:.2f}] '
                        f'/Resources {resources} /Contents {content} 0 R >>'.encode('latin-1')))
    assert add(f'<< /Type /Pages /Count {len(kids)} /Kids [{" ".join(f"{k} 0 R" for k in kids)}] >>'
               .encode('latin-1')) == pages_id
    info = add(f'<< /Title {_pdf_text(sheet["title"])} /Subject {_pdf_text(sheet["course"])} '
               f'/Creator {_pdf_text("GPT, I am Cooked render_sheet.py (native)")} >>'.encode('latin-1'))
    catalog = add(f'<< /Type /Catalog /Pages {pages_id} 0 R >>'.encode('latin-1'))
    out = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f'{number} 0 obj\n'.encode('latin-1') + body + b'\nendobj\n'
    xref = len(out)
    out += f'xref\n0 {len(objects) + 1}\n0000000000 65535 f \n'.encode('latin-1')
    out += b''.join(f'{o:010d} 00000 n \n'.encode('latin-1') for o in offsets)
    out += (f'trailer\n<< /Size {len(objects) + 1} /Root {catalog} 0 R /Info {info} 0 R >>\n'
            f'startxref\n{xref}\n%%EOF\n').encode('latin-1')
    Path(path).write_bytes(bytes(out))
    return len(canvases)


def _decorate(canvas, sheet, fonts, theme, page_w, page_h, number):
    margin = theme['MARGIN']
    top = page_h - margin - 10
    muted = theme['MUTED']
    canvas.text(fonts, margin, top, [(sheet['title'], 'bold', '', 8.5, muted)])
    if sheet['course']:
        canvas.text_right(fonts, page_w - margin, top, [(sheet['course'], 'body', '', 8.5, muted)])
    canvas.line(margin, top - 4, page_w - margin, top - 4, theme['RULE'], 0.5)
    if sheet['allowance']['status'] != 'confirmed':
        canvas.text(fonts, margin, margin, [(theme['UNCONFIRMED_NOTE'], 'body', '', 7.5, muted)])
    canvas.text_right(fonts, page_w - margin, margin, [(str(number), 'body', '', 7.5, muted)])


def _stream(data, extra=''):
    return f'<< /Length {len(data)} {extra} >>\nstream\n'.encode('latin-1') + data + b'\nendstream'


def _pdf_text(text):
    return '<FEFF' + (text or '').encode('utf-16-be').hex().upper() + '>'


def _tag(role):
    return {'body': 'GIMAAA', 'bold': 'GIMAAB', 'mono': 'GIMAAC'}[role]


def _embed_font(add, font, used, role):
    used = dict(used)
    used.setdefault(0, '')
    program = font.subset(set(used))
    file_id = add(_stream(zlib.compress(program), f'/Filter /FlateDecode /Length1 {len(program)}'))
    scale = 1000 / font.units
    bbox = ' '.join(str(round(v * scale)) for v in font.bbox)
    name = f'{_tag(role)}+{font.name}'
    descriptor = add((f'<< /Type /FontDescriptor /FontName /{name} /Flags 32 /FontBBox [{bbox}] /ItalicAngle 0 '
                      f'/Ascent {round(font.ascent * scale)} /Descent {round(font.descent * scale)} '
                      f'/CapHeight {round(font.cap * scale)} /StemV 80 /FontFile2 {file_id} 0 R >>').encode('latin-1'))
    widths = ' '.join(f'{gid} [{round(font.advances[gid] * scale)}]' for gid in sorted(used))
    cid = add((f'<< /Type /Font /Subtype /CIDFontType2 /BaseFont /{name} '
               f'/CIDSystemInfo << /Registry (Adobe) /Ordering (Identity) /Supplement 0 >> '
               f'/FontDescriptor {descriptor} 0 R /W [{widths}] /CIDToGIDMap /Identity >>').encode('latin-1'))
    pairs = [(gid, ch) for gid, ch in sorted(used.items()) if ch]
    chunks = [pairs[i:i + 100] for i in range(0, len(pairs), 100)]
    cmap = ('/CIDInit /ProcSet findresource begin 12 dict begin begincmap /CIDSystemInfo << /Registry (Adobe) '
            '/Ordering (UCS) /Supplement 0 >> def /CMapName /Adobe-Identity-UCS def /CMapType 2 def '
            '1 begincodespacerange <0000> <FFFF> endcodespacerange\n')
    for chunk in chunks:
        cmap += f'{len(chunk)} beginbfchar\n' + ''.join(
            f'<{gid:04X}> <{ch.encode("utf-16-be").hex().upper()}>\n' for gid, ch in chunk) + 'endbfchar\n'
    cmap += 'endcmap CMapName currentdict /CMap defineresource pop end end'
    to_unicode = add(_stream(zlib.compress(cmap.encode('latin-1')), '/Filter /FlateDecode'))
    return add((f'<< /Type /Font /Subtype /Type0 /BaseFont /{name} /Encoding /Identity-H '
                f'/DescendantFonts [{cid} 0 R] /ToUnicode {to_unicode} 0 R >>').encode('latin-1'))
