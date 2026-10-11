"""Check the GPT, I'm Cooked package structure; does not evaluate model behavior."""

from fractions import Fraction
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'gpt-im-cooked'


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def packaged_files():
    roots = (ROOT / 'plugins', ROOT / '.agents', ROOT / 'examples', ROOT / 'tests', ROOT / 'docs', ROOT / 'scripts')
    files = [ROOT / name for name in ('README.md', 'VALIDATION.md', '.gitignore')]
    for directory in roots:
        files.extend(p for p in directory.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    return sorted(files)


def main():
    portable = read_json(PLUGIN / 'plugin.json')
    compat = read_json(PLUGIN / '.codex-plugin/plugin.json')
    for key in ('name', 'version', 'description', 'repository', 'author'):
        require(portable[key] == compat[key], f'Manifest mismatch: {key}')
    require(portable['name'] == 'gpt-im-cooked', 'Incorrect plugin identity')
    require(portable['version'] == '0.4.0', 'Incorrect release version')
    require(compat['skills'] == './skills/', 'Incorrect compatibility skill path')

    extensions = portable['extensions']['com.openai']
    onboarding = extensions['onboardingSkill']
    require(onboarding == compat['extensions']['com.openai']['onboardingSkill'], 'Onboarding mismatch')
    onboarding_path = (PLUGIN / onboarding).resolve()
    require(onboarding_path.is_relative_to(PLUGIN) and onboarding_path.is_file(), 'Missing onboarding skill')
    interface = extensions['interface']
    require(interface == compat['interface'], 'Listing metadata mismatch')
    require(len(interface['shortDescription']) <= 30, 'Listing subtitle exceeds 30 characters')
    prompts = interface['defaultPrompt']
    require(1 <= len(prompts) <= 3 and len(set(prompts)) == len(prompts), 'Invalid starter prompt list')
    require(all(isinstance(p, str) and 0 < len(p) <= 128 and '\n' not in p and '@' not in p for p in prompts), 'Invalid starter prompt')
    for key in ('logo', 'composerIcon'):
        icon_path = (PLUGIN / interface[key]).resolve()
        require(icon_path.is_relative_to(PLUGIN) and icon_path.is_file(), f'Missing {key}')
        ET.parse(icon_path)

    catalog = read_json(ROOT / '.agents/plugins/marketplace.json')
    entry = catalog['plugins'][0]
    require(entry['name'] == portable['name'], 'Marketplace plugin mismatch')
    require((ROOT / entry['source']['path']).resolve() == PLUGIN, 'Marketplace source path mismatch')
    require(entry['policy']['installation'] == 'AVAILABLE' and bool(entry['category']), 'Invalid marketplace metadata')

    extracted_catalog = read_json(PLUGIN / '.agents/plugins/marketplace.json')
    extracted_entry = extracted_catalog['plugins'][0]
    require(extracted_entry['name'] == portable['name'], 'Download marketplace identity mismatch')
    require((PLUGIN / extracted_entry['source']['path']).resolve() == PLUGIN, 'Download marketplace must resolve plugin root')

    skills = sorted((PLUGIN / 'skills').iterdir())
    require({p.name for p in skills if p.is_dir()} == {'gpt-im-cooked', 'gpt-im-cooked-start'}, 'Missing bundled skill')
    for skill in skills:
        content = (skill / 'SKILL.md').read_text(encoding='utf-8')
        match = re.match(r'^---\n(.*?)\n---', content, re.S)
        require(match is not None, f'Invalid frontmatter: {skill.name}')
        meta = yaml.safe_load(match.group(1))
        require(meta['name'] == skill.name and bool(meta['description']), f'Invalid skill metadata: {skill.name}')
        require('[TODO:' not in content, f'Unfinished scaffold: {skill.name}')
        ui = yaml.safe_load((skill / 'agents/openai.yaml').read_text(encoding='utf-8'))
        require(f'${skill.name}' in ui['interface']['default_prompt'], f'Invalid invocation prompt: {skill.name}')
        require(25 <= len(ui['interface']['short_description']) <= 64, f'Invalid description length: {skill.name}')
        require(ui['policy']['allow_implicit_invocation'] is True, f'Unexpected discovery setting: {skill.name}')

    files = packaged_files()
    for path in files:
        if path.suffix in ('.jpg', '.png', '.zip', '.pdf', '.xlsx'):
            continue
        content = path.read_text(encoding='utf-8')
        if path != ROOT / 'docs/examples/sta199/learning-record-original.md':
            require(not re.search(r'[\u3400-\u9fff]', content), f'Non-English package content: {path.name}')
        require(not re.search(r'C:[/\\]Users[/\\]|OneDrive[/\\]|DukeCS[/\\]', content), f'Personal absolute path: {path.name}')
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', content):
                if '://' in target or target.startswith('#'):
                    continue
                resolved = (path.parent / target.split('#')[0]).resolve()
                require(resolved.is_relative_to(ROOT) and resolved.exists(), f'Broken relative link: {path.name} -> {target}')

    require(Fraction(2, 8) == Fraction(3, 12) == Fraction(1, 4), 'Diagnostic arithmetic mismatch')
    require(Fraction(4, 10) == Fraction(2, 5) and Fraction(9, 12) == Fraction(3, 4), 'Transfer arithmetic mismatch')
    require(Fraction(2, 20) == Fraction(1, 10), 'Ambiguity fixture mismatch')
    pilot = (ROOT / 'tests/PILOT-CASES.md').read_text(encoding='utf-8')
    require(len(re.findall(r'^### \d+\.', pilot, re.M)) == 22, 'Expected 22 behavioral pilot cases')
    print(f'PASS: {len(files)} package files, 2 skills, onboarding paths, starter prompts, links, and synthetic arithmetic.')
    print('This command checks package structure only; see VALIDATION.md for behavioral evidence and host limits.')


if __name__ == '__main__':
    main()
