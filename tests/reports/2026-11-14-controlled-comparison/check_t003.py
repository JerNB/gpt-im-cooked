from pathlib import Path
import subprocess, io, zipfile, json
root=Path(__file__).resolve().parents[3]
out=Path(__file__).parent/'verification'
out.mkdir(exist_ok=True)
work=Path.home()/'.codex/runs/t004/t003-regression'
work.mkdir(exist_ok=False)
data=subprocess.check_output(['git','archive','--format=zip','origin/cc/T003-skill-revision'],cwd=root)
with zipfile.ZipFile(io.BytesIO(data)) as z:z.extractall(work)
commands=[['python','tests/'+x+'.py'] for x in ['validate_package','check_state_io','check_mock_render','check_run_evidence','check_evidence_archive','check_distribution']]
commands += [['node','tests/'+x+'.cjs'] for x in ['check_mock_template','check_demo_state','check_concept_retry','check_evidence_chain']]
rows=[]
for cmd in commands:
 p=subprocess.run(cmd,cwd=work,capture_output=True,text=True,encoding='utf-8',errors='replace')
 text=(p.stdout+'\n'+p.stderr).replace(str(work),'<SOURCE>').replace(str(Path.home()),'<HOME>')
 name=Path(cmd[1]).stem
 (out/(name+'.txt')).write_text(text,encoding='utf-8')
 rows.append({'command':cmd,'returncode':p.returncode})
(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows))
