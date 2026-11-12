"""Exercise record conflicts, locks, backups and package boundary failures."""
from pathlib import Path
import importlib.util
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def fails(call):
    try:
        call()
    except (ValueError, FileExistsError, OSError):
        return
    raise AssertionError('Expected rejection')


def outside(text, name):
    """Everything except the named section, to prove other sections are byte-identical."""
    start = text.index(f'## {name}')
    nxt = text.find('\n## ', start + 1)
    return text[:start] + (text[nxt:] if nxt != -1 else '')


def check_sections(io, root):
    template = (ROOT / 'plugins/gpt-im-cooked/skills/gpt-im-cooked/assets/learning-record.md').read_text(encoding='utf-8')
    record, frag = root/'learning-record.md', root/'fragment.md'
    record.write_bytes(template.encode('utf-8'))  # write_text would add CRLF on Windows
    sha = lambda: io.read_record(record)['sha256']

    def update(name, mode, body, expected=None):
        frag.write_text(body, encoding='utf-8')
        return io.update_section(record, name, frag, expected or sha(), mode)

    concepts = io.read_section(record, 'concepts')
    assert concepts['sha256'] == sha() and concepts['content'].startswith('| Concept ID')
    assert 'Import ledger' in concepts['sections'] and 'Learning record' not in concepts['sections']

    before = record.read_text(encoding='utf-8')
    row = '| stats-cond | Conditional probability | Improving | P2: two same-structure successes | Condition on the given event | Transfer task |'
    result = update('Concepts', 'upsert-rows', row)
    assert result['changed'] and result['rows_added'] == 1 and result['rows_replaced'] == 0
    after = record.read_text(encoding='utf-8')
    assert outside(after, 'Concepts') == outside(before, 'Concepts'), 'other sections must not change'
    assert Path(result['backup']).read_text(encoding='utf-8') == before
    newer = row.replace('Improving', 'Demonstrated').replace('Transfer task', 'Recheck in a week')
    result = update('Concepts', 'upsert-rows', newer + '\n| stats-bayes | Bayes rule | Needs practice | P3 | Invert carefully | Retry |')
    assert (result['rows_replaced'], result['rows_added']) == (1, 1)
    text = record.read_text(encoding='utf-8')
    assert 'Demonstrated' in text and '| Improving |' not in text and text.index('stats-cond') < text.index('stats-bayes')

    # Rows go after the table, before the section's trailing note; keyed by the attempt column, not the first one.
    ledger_key = ['Course/artifact/version', 'Session / attempt ID']
    frag.write_text('| STA/mock-a/1.0 | s1 / s1:1 | exports/a.json / abc | export | 2026-11-11 / review.md | — |', encoding='utf-8')
    io.update_section(record, 'Import ledger', frag, sha(), 'upsert-rows', ledger_key)
    frag.write_text('| STA/mock-a/1.0 | s1 / s1:2 | exports/b.json / def | retry | 2026-11-11 / review.md | — |', encoding='utf-8')
    assert io.update_section(record, 'Import ledger', frag, sha(), 'upsert-rows', ledger_key)['rows_added'] == 1
    ledger = io.read_section(record, 'Import ledger')['content']
    assert 's1 / s1:1' in ledger and ledger.index('s1 / s1:2') < ledger.index('Use existing entries'), ledger
    fails(lambda: io.update_section(record, 'Import ledger', frag, sha(), 'upsert-rows', ['No such column']))
    # Same session/attempt ID on another paper is a different row; on the same paper it is a revision.
    frag.write_text('| STA/mock-b/1.0 | s1 / s1:1 | exports/c.json / 123 | export | 2026-11-12 / r.md | — |', encoding='utf-8')
    assert io.update_section(record, 'Import ledger', frag, sha(), 'upsert-rows', ledger_key)['rows_added'] == 1
    frag.write_text('| STA/mock-a/1.0 | s1 / s1:1 | exports/a2.json / 456 | re-export | 2026-11-12 / r.md | revision |', encoding='utf-8')
    assert io.update_section(record, 'Import ledger', frag, sha(), 'upsert-rows', ledger_key)['rows_replaced'] == 1
    ledger = io.read_section(record, 'Import ledger')['content']
    assert 'mock-b/1.0 | s1 / s1:1' in ledger and 'a2.json' in ledger and 'exports/a.json' not in ledger, ledger
    day = '| 2026-11-11 | s1:{n} / q3 | stats-cond | answers/{n}.md | Correct | None | Reasoned solution | ok |'
    for n in (1, 2):
        frag.write_text(day.format(n=n), encoding='utf-8')
        io.update_section(record, 'Attempt history', frag, sha(), 'upsert-rows', 'Attempt ID / item locator')
    history = io.read_section(record, 'Attempt history')['content']
    assert 's1:1 / q3' in history and 's1:2 / q3' in history, 'same-date attempts must not overwrite each other'

    update('Open questions', 'append', '- Is the final cumulative? Asked 2026-11-11.\n\n```python\n## not a heading\n```')
    assert io.read_section(record, 'Open questions')['content'].startswith('None recorded.\n- Is the final')
    update('Next session', 'replace', '- Current activity: Bayes retry\n- Next action: Transfer task on stats-cond')
    text = record.read_text(encoding='utf-8')
    assert text.endswith('- Next action: Transfer task on stats-cond\n') and 'Establish from request' not in text
    assert io.read_section(record, 'Open questions')['sections'][-1] == 'Next session', 'code fence ## is not a section'

    # Unchanged content is a no-op; every rejection leaves the bytes alone.
    assert not update('Next session', 'replace', '- Current activity: Bayes retry\n- Next action: Transfer task on stats-cond')['changed']
    stable = record.read_bytes()
    fails(lambda: update('Concepts', 'upsert-rows', row, expected=io.digest(b'stale')))
    fails(lambda: update('Concepts', 'replace', '## Sneaky new section\nx'))
    fails(lambda: update('Concepts', 'upsert-rows', '| too | few |'))
    fails(lambda: update('Concepts', 'upsert-rows', row + '\n' + row))
    fails(lambda: update('Concepts', 'upsert-rows', 'not a row'))
    fails(lambda: update('Open questions', 'upsert-rows', '| a | b |'))
    fails(lambda: update('Missing section', 'append', 'x'))
    fails(lambda: update('Concepts', 'append', '   \n'))
    fails(lambda: io.update_section(record, 'Concepts', record, sha(), 'replace'))
    assert record.read_bytes() == stable and not Path(str(record) + '.lock').exists()
    record.write_text('# R\n\n## A\n\nx\n\n## A\n\ny\n', encoding='utf-8')
    fails(lambda: update('A', 'append', 'z'))
    fails(lambda: io.update_section(root/'absent.md', 'A', frag, io.digest(b''), 'append'))

    # Code fences follow CommonMark; an unclosed one would swallow later sections (second review repro).
    record.write_bytes(b'# R\n\n## A\n\nx\n\n## B\n\nkeep me\n')
    for bad in ('```\nunclosed', '````\ncode\n```', '~~~\n## x\n```', '   ## indented heading', 'Title\n---', '##'):
        fails(lambda b=bad: update('A', 'append', b))
    assert record.read_bytes() == b'# R\n\n## A\n\nx\n\n## B\n\nkeep me\n'
    update('A', 'append', '````md\n```\n## inside\n```\n````\n\n| a |\n|---|')  # nested fence; table separator is not setext
    update('A', 'replace', 'new')
    assert record.read_bytes() == b'# R\n\n## A\n\nnew\n\n## B\n\nkeep me\n'
    record.write_bytes(b'# R\n\n## A\n\n```\nnever closed\n\n## B\n\nkeep me\n')
    fails(lambda: update('A', 'replace', 'x'))
    fails(lambda: io.read_section(record, 'B'))
    assert b'keep me' in record.read_bytes()

    # CRLF and a BOM survive a section update.
    record.write_bytes(io.BOM + b'# R\r\n\r\n## A\r\n\r\nold\r\n\r\n## B\r\n\r\nkeep\r\n')
    update('A', 'replace', 'new')
    assert record.read_bytes() == io.BOM + b'# R\r\n\r\n## A\r\n\r\nnew\r\n\r\n## B\r\n\r\nkeep\r\n'

    # CLI round trip.
    import json, subprocess, sys
    helper = ROOT / 'plugins/gpt-im-cooked/skills/gpt-im-cooked/scripts/record_io.py'
    frag.write_text('more', encoding='utf-8')
    run = subprocess.run([sys.executable, '-B', str(helper), 'update', str(record), '--section', 'B', '--fragment', str(frag),
                          '--expected-sha256', sha(), '--mode', 'append'], capture_output=True, text=True)
    assert run.returncode == 0 and json.loads(run.stdout)['changed'], run.stderr
    run = subprocess.run([sys.executable, '-B', str(helper), 'read', str(record), '--section', 'B'], capture_output=True, text=True)
    assert json.loads(run.stdout)['content'] == 'keep\r\nmore', run.stdout


def main():
    io = module('record_io', ROOT / 'plugins/gpt-im-cooked/skills/gpt-im-cooked/scripts/record_io.py')
    builder = module('builder', ROOT / 'scripts/build_packages.py')
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        record, candidate = root/'record.md', root/'candidate.md'
        candidate.write_text('# Record\nFirst attempt\n', encoding='utf-8')
        empty = io.read_record(record)['sha256']
        first = io.commit_record(record, candidate, empty)
        assert first['changed'] and first['backup'] is None
        assert not io.commit_record(record, candidate, first['sha256'])['changed']
        candidate.write_text('# Record\nSecond attempt\n', encoding='utf-8')
        second = io.commit_record(record, candidate, first['sha256'])
        assert Path(second['backup']).read_text() == '# Record\nFirst attempt\n'
        fails(lambda: io.commit_record(record, candidate, first['sha256']))
        assert record.read_text() == '# Record\nSecond attempt\n'
        lock = Path(str(record)+'.lock')
        lock.touch()
        fails(lambda: io.commit_record(record, candidate, second['sha256']))
        assert lock.exists()
        lock.unlink()
        candidate.write_text('', encoding='utf-8')
        fails(lambda: io.commit_record(record, candidate, second['sha256']))
        assert record.read_text() == '# Record\nSecond attempt\n'
        # Simulate replacement failure: original and its recoverable backup survive.
        candidate.write_text('# Record\nThird attempt\n', encoding='utf-8')
        replace = io.os.replace
        def broken_replace(source, target):
            if target == record:
                raise OSError('Simulated failed replacement')
            replace(source, target)
        io.os.replace = broken_replace
        try:
            fails(lambda: io.commit_record(record, candidate, second['sha256']))
        finally:
            io.os.replace = replace
        assert record.read_text() == Path(str(record)+'.bak').read_text()
        assert not lock.exists() and not list(root.glob('*.tmp'))
        check_sections(io, root)
        package = root/'package'
        package.mkdir()
        (package/'SKILL.md').write_text('# Skill')
        assert len(builder.collect_files(package, {'SKILL.md'})) == 1
        (package/'private-attempt.json').write_text('{}')
        fails(lambda: builder.collect_files(package, {'SKILL.md'}))
        (package/'private-attempt.json').unlink()
        fails(lambda: builder.collect_files(package, {'SKILL.md', 'missing.md'}))
    print('PASS: create/no-change/backup/conflict/lock/invalid/write failure, section read/replace/append/upsert-rows '
          '(other sections unchanged, rejections leave bytes alone, CRLF/BOM kept) and package rejection')


if __name__ == '__main__':
    main()
