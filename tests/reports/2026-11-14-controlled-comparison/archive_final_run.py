"""Archive only the new recovery; prior raw attempts and judgments remain in place."""
from pathlib import Path
import json,re,shutil,hashlib
base=Path(__file__).parent
report=base/'recovery-final-A1-S-rep2'
work=Path.home()/'.codex/runs/t004/recovery-final-A1-S-rep2/run-A1-S-rep2'
out=report/'runs/A1-S-rep2'
for p in work.rglob('*'):
 rel=p.relative_to(work)
 if not p.is_file() or any(x in ('skill','__pycache__') for x in rel.parts) or rel.name=='AGENTS.md':continue
 dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():shutil.copy2(p,dest)
for snap in out.glob('files-after-*'):
 if not (snap/'materials').exists():shutil.copytree(work/'materials',snap/'materials')
probe=report/'environment-preflight/runs/A1-S-rep2'
if (probe/'files-after-00/environment-probe.txt').exists():shutil.copy2(probe/'files-after-00/environment-probe.txt',probe/'environment-probe.txt')
variants=set()
for path in (Path.home(),work.parent):
 variants.add(path.as_posix())
 for n in (1,2,4,8):variants.add(str(path).replace('\\','\\'*n))
changes=[]
targets=list(report.rglob('*'))+[base/'final/blind/CASE-03.json',base/'final/auto-blind/CASE-03.json',base/'final/CASE-03-primary.json',base/'final/CASE-03-second.json',base/'final/CASE-03-adjudication.json']
for p in targets:
 if not p.is_file() or p.suffix not in ('.md','.json','.jsonl','.txt','.bak'):continue
 if any(x in ('fixtures','skill-B','skill-C') for x in p.relative_to(base).parts):continue
 old=p.read_bytes();text=old.decode('utf-8-sig')
 for s in sorted(variants,key=len,reverse=True):text=text.replace(s,'<ROOT>')
 for n in (1,2,4,8):text=text.replace('C:'+('\\'*n)+'Program Files','<ROOT>')
 text=text.replace('C:/Program Files','<ROOT>');text=re.sub('[\u3400-\u9fff]','\ufffd',text)
 new=text.replace('\r\n','\n').encode('utf-8')
 if new!=old:p.write_bytes(new);changes.append({'path':p.relative_to(base).as_posix(),'original_sha256':hashlib.sha256(old).hexdigest(),'archived_sha256':hashlib.sha256(new).hexdigest()})
(report/'archive-transformations.json').write_text(json.dumps(changes,indent=2)+'\n',encoding='utf-8',newline='')
p=base/'DIAGNOSTICS.md';s=p.read_text(encoding='utf-8')
s=s.replace('Select all eight byte-exact S sessions from `exact-S/runs/`.', 'Select seven byte-exact S sessions from `exact-S/runs/`, excluding the failed A1-S-rep2, and the complete fresh A1-S-rep2 from `recovery-final-A1-S-rep2/runs/`.')
if '## Final authorized recovery' not in s:s+='''\n## Final authorized recovery\n\nHuman confirmed a reset and authorized one fresh final A1-S-rep2. Before launch, temporary auth copies were zero; B97be172/C4d102f6 and all16 C/all7 S original fingerprints matched. A completely new report/work path used the existing runner with non-login shell and separate preflight. Preflight and tutoring thread IDs differ; the preflight marker is absent from initial tutor context, and workspace inventory stayed unchanged. Phase1 read materials successfully, with no global skill access. The turn7 answer was written from that session's own question before phase2. All11 student calls completed. This supplemental session crosses quota windows; its time is not a skill-effect estimate. Prior fifteen judgments and adjudications remain unchanged. Later cc commits were excluded from the dataset.\n'''
p.write_text(s,encoding='utf-8',newline='')
print('New final run mirrored and sanitized; diagnostic history updated.')
