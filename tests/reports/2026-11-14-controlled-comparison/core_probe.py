from pathlib import Path
import os
import shutil
import subprocess

work = Path('<ROOT>')
work.mkdir(parents=True, exist_ok=False)
home = work / 'home'
home.mkdir()
shutil.copy2(Path.home() / '.codex/auth.json', home / 'auth.json')
(work / 'probe.txt').write_text('T004_LOCAL_READ_7319')
env = dict(os.environ, CODEX_HOME=str(home))
for key in ('CODEX_WINDOWS_REGISTERED_CORE', 'CODEX_APP_TOOLS_PIPE_PATH', 'CODEX_APP_RUNTIME_CLI_PATH'):
    env.pop(key, None)
try:
    result = subprocess.run([shutil.which('codex'), 'exec', '--json', '--skip-git-repo-check',
        '--ignore-user-config', '-m', 'gpt-6.1-sol', '-c', 'model_reasoning_effort="medium"',
        '-c', 'approval_policy="never"', '-c', 'sandbox_mode="workspace-write"',
        '-c', 'windows.sandbox="unelevated"', '-C', str(work),
        'Read probe.txt with a shell command and report its exact content.'],
        env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180)
    (work / 'events.jsonl').write_text(result.stdout, encoding='utf-8')
    print(result.stdout[-8000:])
finally:
    (home / 'auth.json').unlink(missing_ok=True)
