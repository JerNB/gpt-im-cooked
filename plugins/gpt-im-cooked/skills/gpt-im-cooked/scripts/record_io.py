"""Read and update one Markdown record with conflict detection and a backup.

Commands:
  read   PATH [--section NAME]          content (or one `## NAME` section) and the whole-file SHA-256
  commit PATH --candidate FILE --expected-sha256 HASH
                                        replace the whole record with FILE
  update PATH --section NAME --fragment FILE --expected-sha256 HASH --mode MODE
                                        change one `## NAME` section; every other byte is kept
      replace      FILE becomes the section body
      append       FILE is added after the section's existing body (prose or lists)
      upsert-rows  FILE holds Markdown table rows; a row whose key cells (first column, or
                   every --key-column HEADER given) match an existing row replaces it,
                   otherwise it is added after the table's last row

Every write checks the whole-file SHA-256, takes a lock, keeps `<record>.bak`, and
verifies the written bytes. No semantic grading, multi-file transaction, or
protection against writers that ignore this helper. Python 3.10+, stdlib only.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import tempfile

BOM = b'\xef\xbb\xbf'
# CommonMark: up to three spaces of indent; `##` alone is an (empty) heading; `#tag` is not.
HEADING = re.compile(r'^ {0,3}(#{1,2})(?:[ \t]+(.*?))?[ \t#]*$')
FENCE_OPEN = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
SETEXT = re.compile(r'^ {0,3}(?:=+|-+)[ \t]*$')
CELL_SPLIT = re.compile(r'(?<!\\)\|')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_record(path):
    path = Path(path)
    data = path.read_bytes() if path.exists() else b''
    return {'exists': path.exists(), 'sha256': digest(data),
            'content': data.decode('utf-8-sig')}


def atomic_write(path, data):
    fd, name = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def check_record(data):
    if not data.decode('utf-8-sig').strip().startswith('# '):
        raise ValueError('Expected a nonempty UTF-8 Markdown record with a title')


def locked_write(path, expected, build):
    """Under the lock: compare hashes, build new bytes from the current ones, back up, write, verify."""
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = Path(str(path) + '.lock')
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.close(fd)
        current = read_record(path)
        if current['sha256'] != expected:
            raise ValueError('Record changed; reread and merge before retrying')
        old = path.read_bytes() if current['exists'] else b''
        data, details = build(old, current['exists'])
        check_record(data)
        if current['sha256'] == digest(data):
            return {'changed': False, 'sha256': current['sha256'], **details}
        if current['exists']:
            atomic_write(Path(str(path) + '.bak'), old)
        atomic_write(path, data)
        if path.read_bytes() != data:
            raise OSError('Post-write verification failed; inspect the record and backup')
        return {'changed': True, 'sha256': digest(data),
                'backup': str(path) + '.bak' if current['exists'] else None, **details}
    finally:
        lock.unlink(missing_ok=True)


def separate(path, other):
    path, other = Path(path).resolve(), Path(other).resolve()
    if path == other or other in (Path(str(path) + '.bak'), Path(str(path) + '.lock')):
        raise ValueError('Candidate/fragment must be a separate file, not the record or its sidecars')
    return other


def commit_record(path, candidate, expected):
    data = separate(path, candidate).read_bytes()
    check_record(data)
    return locked_write(path, expected, lambda old, exists: (data, {}))


# ------------------------------------------------------------------ sections

def fence_step(line, fence):
    """CommonMark fences: return (fence still open after this line, whether the line is fence/code)."""
    text = line.rstrip('\r\n')
    if fence:
        char, size = fence
        closing = re.match(r'^ {0,3}' + re.escape(char) + '{' + str(size) + r',}[ \t]*$', text)
        return (None if closing else fence), True
    mark = FENCE_OPEN.match(text)
    if mark and not (mark.group(1)[0] == '`' and '`' in mark.group(2)):
        return (mark.group(1)[0], len(mark.group(1))), True
    return None, False


def split_sections(text):
    """Return (lines, sections); each section is [name, heading_line, end_line) for `## ` headings.

    Headings inside fenced code blocks are ignored; `# ` and `## ` both end a section.
    An unclosed fence would swallow every later section, so it is refused.
    """
    lines = text.splitlines(keepends=True)
    found, fence, opened = [], None, 0
    for i, line in enumerate(lines):
        was_open = fence
        fence, code = fence_step(line, fence)
        if fence and not was_open:
            opened = i + 1
        if code:
            continue
        heading = HEADING.match(line.rstrip('\r\n'))
        if heading:
            if found and found[-1][2] is None:
                found[-1][2] = i
            found.append([(heading.group(2) or '').strip() if len(heading.group(1)) == 2 else None, i, None])
    if fence:
        raise ValueError(f'Code fence opened on line {opened} is never closed; fix the record by hand before section updates')
    if found and found[-1][2] is None:
        found[-1][2] = len(lines)
    return lines, [s for s in found if s[0] is not None]


def find_section(sections, name):
    matches = [s for s in sections if s[0].casefold() == name.strip().casefold()]
    if len(matches) != 1:
        names = [s[0] for s in sections]
        problem = 'not found' if not matches else 'appears more than once'
        raise ValueError(f'Section {name!r} {problem}; sections: {names}')
    return matches[0]


def read_section(path, name):
    result = read_record(path)
    if not result['exists']:
        raise ValueError('Record does not exist')
    lines, sections = split_sections(result['content'])
    _, start, end = find_section(sections, name)
    return {'exists': True, 'sha256': result['sha256'], 'section': lines[start].strip().lstrip('#').strip(),
            'content': ''.join(lines[start + 1:end]).strip('\r\n'), 'sections': [s[0] for s in sections]}


def fragment_lines(raw):
    text = raw.decode('utf-8-sig').replace('\r\n', '\n').strip('\n')
    if not text.strip():
        raise ValueError('Fragment is empty')
    lines, fence, previous = text.split('\n'), None, ''
    for line in lines:
        fence, code = fence_step(line, fence)
        if not code:
            setext = SETEXT.match(line) and previous.strip() and not previous.lstrip().startswith('|')
            if HEADING.match(line) or setext:
                raise ValueError('Fragment must not contain # or ## headings (including underlined ones); '
                                 'it changes one section body only')
        previous = '' if code else line
    if fence:
        raise ValueError('Fragment opens a code fence it never closes; that would swallow later sections')
    return lines


def cells(row):
    row = row.strip()
    if not (row.startswith('|') and row.endswith('|')) or len(row) < 2:
        raise ValueError(f'Not a Markdown table row: {row[:60]!r}')
    return [c.strip() for c in CELL_SPLIT.split(row[1:-1])]


def upsert_rows(body, new_rows, key_columns=None):
    table = [i for i, line in enumerate(body) if line.strip().startswith('|')]
    if len(table) < 2:
        raise ValueError('Section has no Markdown table (header and separator row) for upsert-rows')
    first = table[0]
    last = first
    while last + 1 < len(body) and body[last + 1].strip().startswith('|'):
        last += 1
    separator = body[first + 1].strip() if last > first else ''
    if '-' not in separator or set(separator) - set('|:- '):
        raise ValueError('Section table needs a header row followed by a separator row')
    header = cells(body[first])
    width = len(header)
    if isinstance(key_columns, str):
        key_columns = [key_columns]
    ks = []
    for name in key_columns or [header[0]]:
        named = [i for i, h in enumerate(header) if h.casefold() == name.strip().casefold()]
        if len(named) != 1:
            raise ValueError(f'Key column {name!r} not found; columns: {header}')
        ks.append(named[0])
    key_of = lambda row_cells: tuple(row_cells[k] for k in ks)
    keys = {}
    for i in range(first + 2, last + 1):
        keys.setdefault(key_of(cells(body[i])), []).append(i)
    for row in new_rows:
        if len(cells(row)) != width:
            raise ValueError(f'Row has {len(cells(row))} cells; the table has {width}: {row[:60]!r}')
    new_keys = [key_of(cells(r)) for r in new_rows]
    if len(set(new_keys)) != len(new_keys):
        raise ValueError('The fragment repeats a row key')
    replaced, added = 0, []
    for row in new_rows:
        row_cells = cells(row)
        key = key_of(row_cells)
        if not all(key):
            raise ValueError(f'Key cells {[header[k] for k in ks]} must not be empty')
        hits = keys.get(key, [])
        if len(hits) > 1:
            raise ValueError(f'Key {key!r} matches {len(hits)} existing rows; use replace and merge by hand')
        if hits:
            body[hits[0]] = row.strip()
            replaced += 1
        else:
            added.append(row.strip())
    body[last + 1:last + 1] = added
    return {'rows_replaced': replaced, 'rows_added': len(added)}


def update_section(path, name, fragment, expected, mode, key_columns=None):
    if mode not in ('replace', 'append', 'upsert-rows'):
        raise ValueError('mode must be replace, append, or upsert-rows')
    new = fragment_lines(separate(path, fragment).read_bytes())

    def build(old, exists):
        if not exists:
            raise ValueError('Record does not exist; create it from the template with commit')
        bom = BOM if old.startswith(BOM) else b''
        text = old.decode('utf-8-sig')
        nl = '\r\n' if '\r\n' in text else '\n'
        lines, sections = split_sections(text)
        section, start, end = find_section(sections, name)
        body = [line.rstrip('\r\n') for line in lines[start + 1:end]]
        while body and not body[-1].strip():
            body.pop()
        while body and not body[0].strip():
            body.pop(0)
        details = {'section': section, 'mode': mode}
        if mode == 'replace':
            body = list(new)
        elif mode == 'append':
            body = body + new
        else:
            details.update(upsert_rows(body, new, key_columns))
        is_last = end == len(lines)
        block = nl + nl.join(body) + nl + ('' if is_last else nl)
        heading = lines[start] if lines[start].endswith(('\n', '\r')) else lines[start] + nl
        result = ''.join(lines[:start]) + heading + block + ''.join(lines[end:])
        if [s[0] for s in split_sections(result)[1]] != [s[0] for s in sections]:
            raise ValueError('The update would change the record\'s section structure; nothing was written')
        return bom + result.encode('utf-8'), details

    return locked_write(path, expected, build)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    read = sub.add_parser('read')
    read.add_argument('path', type=Path)
    read.add_argument('--section', help='return only this `## ` section (whole-file hash still returned)')
    commit = sub.add_parser('commit')
    commit.add_argument('path', type=Path)
    commit.add_argument('--candidate', type=Path, required=True)
    commit.add_argument('--expected-sha256', required=True)
    update = sub.add_parser('update')
    update.add_argument('path', type=Path)
    update.add_argument('--section', required=True)
    update.add_argument('--fragment', type=Path, required=True)
    update.add_argument('--expected-sha256', required=True)
    update.add_argument('--mode', required=True, choices=['replace', 'append', 'upsert-rows'])
    update.add_argument('--key-column', action='append', help='upsert-rows: header of a column that identifies a row; '
                        'repeat for a composite key (default: first column)')
    args = parser.parse_args()
    try:
        if args.command == 'read':
            result = read_section(args.path, args.section) if args.section else read_record(args.path)
        elif args.command == 'commit':
            result = commit_record(args.path, args.candidate, args.expected_sha256)
        else:
            result = update_section(args.path, args.section, args.fragment, args.expected_sha256, args.mode, args.key_column)
        print(json.dumps(result, ensure_ascii=True))
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
