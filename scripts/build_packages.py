"""Build reproducible standalone-skill and locally installable plugin ZIPs."""
from pathlib import Path
import argparse
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/gpt-im-cooked'

# Explicit distribution boundary: additions require an intentional review.
SKILL_FILES = {
    'SKILL.md', 'agents/openai.yaml', 'assets/first-use.md',
    'assets/course-profile.md', 'assets/learning-record.md',
    'references/state.md', 'references/practice-and-feedback.md',
    'references/review-artifacts.md', 'references/interactive-review.md',
    'references/webpage-prompts.md',
    'references/concept-tutoring.md',
    'references/mock-exam-layout.md',
    'scripts/record_io.py',
}
PLUGIN_FILES = {
    'plugin.json', '.codex-plugin/plugin.json',
    '.agents/plugins/marketplace.json', 'INSTALLATION.md', 'assets/icon.svg',
    'skills/gpt-im-cooked-start/SKILL.md',
    'skills/gpt-im-cooked-start/agents/openai.yaml',
} | {'skills/gpt-im-cooked/' + name for name in SKILL_FILES}


def collect_files(source, allowed):
    files = {}
    for file in sorted(source.rglob('*')):
        if file.is_symlink():
            raise ValueError(f'Unexpected symlink: {file}')
        if not file.is_file() or '__pycache__' in file.parts:
            continue
        name = file.relative_to(source).as_posix()
        if name not in allowed:
            raise ValueError(f'Unapproved package file: {name}')
        files['gpt-im-cooked/' + name] = file.read_bytes()
    missing = allowed - {name.removeprefix('gpt-im-cooked/') for name in files}
    if missing:
        raise ValueError(f'Missing package files: {sorted(missing)}')
    return files


def build(output):
    manifest = json.loads((PLUGIN / 'plugin.json').read_text(encoding='utf-8'))
    version = manifest['version']
    output = Path(output).resolve()
    if output.is_relative_to(PLUGIN):
        raise ValueError('Archives must be outside the installed plugin.')
    # Validate both boundaries before writing either archive.
    packages = [('skill', collect_files(PLUGIN / 'skills/gpt-im-cooked', SKILL_FILES)),
                ('plugin', collect_files(PLUGIN, PLUGIN_FILES))]
    output.mkdir(parents=True, exist_ok=True)
    for kind, files in packages:
        path = output / f'gpt-im-cooked-{kind}-v{version}.zip'
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
