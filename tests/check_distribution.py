"""Verify extracted downloads resolve their resources and match maintained source."""
from pathlib import Path
import hashlib
import json
import re
import tempfile
import zipfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_packages import collect_files, PLUGIN_FILES, SKILL_FILES

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/gpt-im-cooked'


def contained(root, value):
    assert value.startswith('./'), f'Nonrelative package path: {value}'
    target = (root / value).resolve()
    assert target.is_relative_to(root.resolve()) and target.exists(), value
    return target


def check():
    manifest = json.loads((PLUGIN / 'plugin.json').read_text(encoding='utf-8'))
    version = manifest['version']
    with tempfile.TemporaryDirectory(prefix='cooked-distribution-') as temp:
        for kind, source in [('plugin', PLUGIN), ('skill', PLUGIN / 'skills/gpt-im-cooked')]:
            path = ROOT / 'docs/downloads' / f'gpt-im-cooked-{kind}-v{version}.zip'
            expected = collect_files(source, PLUGIN_FILES if kind == 'plugin' else SKILL_FILES)
            destination = Path(temp) / kind
            with zipfile.ZipFile(path) as archive:
                assert archive.testzip() is None
                assert len(archive.namelist()) == len(set(archive.namelist()))
                assert set(archive.namelist()) == set(expected), f'Unexpected archive contents: {kind}'
                for name in archive.namelist():
                    assert (destination / name).resolve().is_relative_to(destination.resolve())
                    assert archive.read(name) == expected[name], f'Stale file: {name}'
                archive.extractall(destination)
            extracted = destination / 'gpt-im-cooked'
            if kind == 'plugin':
                portable = json.loads((extracted / 'plugin.json').read_text(encoding='utf-8'))
                compat = json.loads((extracted / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
                catalog = json.loads((extracted / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
                entry = catalog['plugins'][0]
                assert entry['name'] == portable['name'] == compat['name'] == 'gpt-im-cooked'
                assert contained(extracted, entry['source']['path']) == extracted.resolve()
                onboarding = contained(extracted, portable['extensions']['com.openai']['onboardingSkill'])
                assert onboarding.name == 'SKILL.md'
                for key in ('logo', 'composerIcon'):
                    contained(extracted, portable['extensions']['com.openai']['interface'][key])
                roots = [extracted / 'skills/gpt-im-cooked', extracted / 'skills/gpt-im-cooked-start']
            else:
                roots = [extracted]
            for skill in roots:
                assert (skill / 'SKILL.md').exists()
                for file in skill.rglob('*.md'):
                    for target in re.findall(r'\]\(([^)]+)\)', file.read_text(encoding='utf-8')):
                        if '://' in target or target.startswith('#'):
                            continue
                        ref = (file.parent / target.split('#')[0]).resolve()
                        assert ref.is_relative_to(extracted.resolve()) and ref.exists(), (file.name, target)
            print(f'PASS {kind}: {len(expected)} exact source files; extracted resources resolve; SHA256 {hashlib.sha256(path.read_bytes()).hexdigest()}')
    print('These checks verify distribution structure, not desktop installation or model behavior.')


if __name__ == '__main__':
    check()
