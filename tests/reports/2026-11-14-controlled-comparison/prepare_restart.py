from pathlib import Path
import json
root = Path(__file__).resolve().parents[3]
runner = root / 'tests/run_controlled_comparison.py'
s = runner.read_text(encoding='utf-8')
s = s.replace("REPORT = ROOT / 'tests/reports/2026-11-14-controlled-comparison'", "REPORT = ROOT / 'tests/reports/2026-11-14-controlled-comparison/restart'")
s = s.replace("env = dict(os.environ, CODEX_HOME=str(home), PYTHONUTF8='1')", "env = dict(os.environ, CODEX_HOME=str(home), PYTHONUTF8='1')\n    for key in ('CODEX_WINDOWS_REGISTERED_CORE', 'CODEX_APP_TOOLS_PIPE_PATH', 'CODEX_APP_RUNTIME_CLI_PATH'):\n        env.pop(key, None)")
s = s.replace("shutil.copytree(source, REPORT / 'fixtures' / f'packet-{packet.lower()}')", "shutil.copytree(source, REPORT / 'fixtures' / f'packet-{packet.lower()}', dirs_exist_ok=True)")
start=s.index('    texts = []',s.index('def turn1_gate'))
end=s.index('\n\n\ndef run_session',start)
s=s[:start]+'''    successful = [e['item'] for e in events if e.get('type') == 'item.completed'
                  and e.get('item', {}).get('type') == 'command_execution'
                  and e['item'].get('exit_code') == 0 and e['item'].get('status') == 'completed']
    reads = [x for x in successful if any(k in x.get('command', '').lower()
             for k in ('get-content', 'type ', 'cat ', 'read_text', 'read_bytes', 'open('))]
    material_read = any('materials' in x.get('command', '').lower() and x.get('aggregated_output', '').strip() for x in reads)
    skill_read = any('skill' in x.get('command', '').lower() and 'skill.md' in x.get('command', '').lower()
                     and x.get('aggregated_output', '').strip() for x in reads)
    return {'materials_content_read': material_read, 'skill_content_read': skill_read if arm in ('B', 'C') else True}
'''+s[end:]
s=s.replace("dump(REPORT / 'gate-results.json',", "dump(REPORT / f'gate-{arm}-{packet}-rep{rep}.json',")
s=s.replace("rows.append(row)\n            dump", "rows.append(row)\n            dump(REPORT / f'partial-{packet}-rep{rep}-{phase}.json', rows)\n            dump")
s=s.replace("rows = run_session(args.packet, args.replicate, arm_order, work, script, state, cli, range(1, 7))", "try:\n            rows = run_session(args.packet, args.replicate, arm_order, work, script, state, cli, range(1, 7))\n        finally:\n            for a in state['arms'].values():\n                (Path(a['home']) / 'auth.json').unlink(missing_ok=True)")
s=s.replace("rows = []\n        try:\n            rows = run_session", "rows = []\n        for a in state['arms'].values():\n            shutil.copy2(Path.home() / '.codex/auth.json', Path(a['home']) / 'auth.json')\n        try:\n            rows = run_session")
runner.write_text(s,encoding='utf-8')
p=root/'tests/fixtures/controlled-comparison/packet-p'
script=json.loads((p/'script.json').read_text(encoding='utf-8'))
script['turns'][1]['text']='For practice Q1, my answer is 4 comparisons because the list contains 4 elements. Is that right?'
script['turns'][3]['text']='Q3: 7 element-to-element comparisons, since 8 elements have 7 adjacent pairs. I excluded assignments, index updates, and loop-condition checks. I did not use a hint.'
source=json.loads((p/'script-source-s.json').read_text(encoding='utf-8-sig'))
script['openers']=source['openers'];script['resume_openers']=source['resume_openers']
(p/'script.json').write_text(json.dumps(script,indent=2)+'\n',encoding='utf-8')
f=p/'materials/practice.md';t=f.read_text(encoding='utf-8').replace('[5, 9, 2, 8]','[5, 9, 2, 8, 0, 6, 1, 3]');f.write_text(t,encoding='utf-8')
f=p/'materials/practice-key.md';f.write_text(f.read_text(encoding='utf-8').replace('Q3: 3 element-to-element comparisons (length 4','Q3: 7 element-to-element comparisons (length 8'),encoding='utf-8')
rub=json.loads((p/'rubric-v2.json').read_text(encoding='utf-8'));rub['ground_truth']['keys']['Q3']='7 comparisons';rub['ground_truth']['unattempted_key_values']['Q3']=['7 comparisons']
for check in rub['checks']:
    check['rule']=check['rule'].replace('shallow aliasing examples','single complete adjacent-pair passes').replace('aliasing practiced','loop tracing practiced').replace('P2/P4 next','P1/P4 next')
for name in ('rubric.json','rubric-v2.json'):(p/name).write_text(json.dumps(rub,indent=2)+'\n',encoding='utf-8')
for name in ('script-source-s.json','materials/old-quiz-3.md'):(p/name).unlink(missing_ok=True)
for arm in ('A1','A2','B','C'):
    (Path('<ROOT>')/f'home-{arm}-S-rep1/auth.json').unlink(missing_ok=True)
print('Restart prepared; old auth copies removed; original invalid evidence retained.')
