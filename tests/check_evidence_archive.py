"""Check archived bytes/identities; semantic tutor verdicts remain manual reviews."""
from pathlib import Path
import hashlib
import json

RUN = Path(__file__).resolve().parent / 'reports/2026-10-17'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((RUN / 'manifest.json').read_text(encoding='utf-8'))
    for name, expected in manifest['files'].items():
        file = (RUN / name).resolve()
        assert file.is_relative_to(RUN.resolve()) and not file.is_symlink(), name
        assert digest(file) == expected, name
    assert len(manifest['runs']) == 12
    assert sum(run['turns'] for run in manifest['runs']) == 24
    before = json.loads((RUN / 'before-duplicate.json').read_text(encoding='utf-8-sig'))
    after = json.loads((RUN / 'after-duplicate.json').read_text(encoding='utf-8-sig'))
    assert before == after, 'Duplicate import changed a record or backup'
    for row in before:
        run = RUN / 'runs' / row['run']
        assert digest(run / 'record-after-02.md') == row['record'].lower()
        assert digest(run / 'record-after-03.md') == row['record'].lower()
    source = RUN / 'runs/legacy-01'
    for condition in ('legacy', 'revised'):
        for index in range(1, 4):
            run = RUN / 'runs' / f'{condition}-{index:02}'
            for name in ('attempt.json', 'concept.html', 'course-packet.md'):
                assert (run / name).read_bytes() == (source / name).read_bytes()
            assert (run / 'response-01.md').is_file()
    original = RUN.parents[1] / 'fixtures/legacy-grouped-transformations.html'
    assert digest(original) == 'e864c12972c2cb1cc48f9da6b22a93743e2e272cec1f5bbf25a3887522f11495'
    assert (source / 'concept.html').read_bytes() == original.read_bytes()
    assert digest(RUN / 'inputs/legacy-attempt.json') == '19aa3be22e9c4b83f9424b3fd7ee4c2f9354323365207b44fba5014eeba8e548'
    old = {p.relative_to(RUN / 'skills/before').as_posix(): p.read_bytes()
           for p in (RUN / 'skills/before').rglob('*') if p.is_file()}
    new = {p.relative_to(RUN / 'skills/after').as_posix(): p.read_bytes()
           for p in (RUN / 'skills/after').rglob('*') if p.is_file()}
    assert old.keys() == new.keys()
    assert {name for name in old if old[name] != new[name]} == {
        'references/state.md', 'references/interactive-review.md'}
    adjudication = json.loads((RUN / 'adjudication.json').read_text(encoding='utf-8'))
    for case in adjudication['cases']:
        for judgment in case['judgments']:
            assert judgment['result'] in ('pass', 'fail', 'unresolved')
            for name in judgment['evidence']:
                assert (RUN / name).is_file(), name
    print(f"PASS: {len(manifest['files'])} archived fingerprints, 12 contexts/24 turns, unchanged duplicate hashes, identical comparison inputs, two changed instruction references, and manual-verdict evidence paths.")
    print('This validates evidence integrity, not the correctness of author semantic judgments.')


if __name__ == '__main__':
    main()
