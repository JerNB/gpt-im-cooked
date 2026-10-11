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
        package = root/'package'
        package.mkdir()
        (package/'SKILL.md').write_text('# Skill')
        assert len(builder.collect_files(package, {'SKILL.md'})) == 1
        (package/'private-attempt.json').write_text('{}')
        fails(lambda: builder.collect_files(package, {'SKILL.md'}))
        (package/'private-attempt.json').unlink()
        fails(lambda: builder.collect_files(package, {'SKILL.md', 'missing.md'}))
    print('PASS: create/no-change/backup/conflict/lock/invalid/write failure and package rejection')


if __name__ == '__main__':
    main()
