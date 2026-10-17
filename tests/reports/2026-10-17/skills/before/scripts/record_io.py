"""Read and replace one Markdown record with conflict detection and a backup.

No semantic grading, multi-file transaction, or protection against writers that
ignore this helper. Requires Python 3.10+ and only its standard library.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import tempfile


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


def commit_record(path, candidate, expected):
    path, candidate = Path(path).resolve(), Path(candidate).resolve()
    if path == candidate or candidate in (Path(str(path) + '.bak'), Path(str(path) + '.lock')):
        raise ValueError('Candidate must be a separate file, not the record or its sidecars')
    data = candidate.read_bytes()
    if not data.decode('utf-8-sig').strip().startswith('# '):
        raise ValueError('Expected a nonempty UTF-8 Markdown record with a title')
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = Path(str(path) + '.lock')
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.close(fd)
        current = read_record(path)
        if current['sha256'] != expected:
            raise ValueError('Record changed; reread and merge before retrying')
        if current['sha256'] == digest(data):
            return {'changed': False, 'sha256': current['sha256']}
        if current['exists']:
            atomic_write(Path(str(path) + '.bak'), path.read_bytes())
        atomic_write(path, data)
        if path.read_bytes() != data:
            raise OSError('Post-write verification failed; inspect the record and backup')
        return {'changed': True, 'sha256': digest(data),
                'backup': str(path) + '.bak' if current['exists'] else None}
    finally:
        lock.unlink(missing_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    read = sub.add_parser('read')
    read.add_argument('path', type=Path)
    commit = sub.add_parser('commit')
    commit.add_argument('path', type=Path)
    commit.add_argument('--candidate', type=Path, required=True)
    commit.add_argument('--expected-sha256', required=True)
    args = parser.parse_args()
    try:
        result = (read_record(args.path) if args.command == 'read' else
                  commit_record(args.path, args.candidate, args.expected_sha256))
        print(json.dumps(result, ensure_ascii=True))
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
