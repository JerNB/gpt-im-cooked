"""Build reproducible standalone-skill and locally installable plugin ZIPs."""
from pathlib import Path
import argparse
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/gpt-im-cooked'


def build(output):
    manifest = json.loads((PLUGIN / 'plugin.json').read_text(encoding='utf-8'))
    version = manifest['version']
    output = Path(output).resolve()
    if output.is_relative_to(PLUGIN):
        raise ValueError('Archives must be outside the installed plugin.')
    output.mkdir(parents=True, exist_ok=True)
    for kind, source in [('skill', PLUGIN / 'skills/gpt-im-cooked'), ('plugin', PLUGIN)]:
        path = output / f'gpt-im-cooked-{kind}-v{version}.zip'
        files = {}
        for file in sorted(source.rglob('*')):
            if file.is_symlink():
                raise ValueError(f'Unexpected symlink: {file}')
            if file.is_file() and '__pycache__' not in file.parts:
                files['gpt-im-cooked/' + file.relative_to(source).as_posix()] = file.read_bytes()
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name, content in sorted(files.items()):
                entry = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, content)
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise ValueError(f'Corrupt archive: {path}')
            if kind == 'plugin':
                catalog = json.loads(archive.read('gpt-im-cooked/.agents/plugins/marketplace.json'))
                if catalog['plugins'][0]['source']['path'] != './':
                    raise ValueError('Extracted plugin marketplace must resolve its own root.')
        print(f'{path.name}: {len(files)} files, {path.stat().st_size} bytes')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/downloads')
    build(parser.parse_args().output)
