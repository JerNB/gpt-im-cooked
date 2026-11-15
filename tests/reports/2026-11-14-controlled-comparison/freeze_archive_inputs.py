from pathlib import Path
import zipfile,hashlib,json
base=Path(__file__).parent
archive=base/'executed-inputs.zip'
index={}
with zipfile.ZipFile(archive,'a',compression=zipfile.ZIP_DEFLATED) as z:
 existing=set(z.namelist())
 for p in sorted(base.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(base)
  if not any(x in ('fixtures','skill-B','skill-C','frozen-packet-s-git') for x in rel.parts):continue
  key=rel.as_posix()
  if key not in existing:z.writestr(key,p.read_bytes())
  raw=z.read(key)
  index[key]={'executed_sha256':hashlib.sha256(raw).hexdigest()}
# Store portable LF text previews; exact executed input bytes remain in the ZIP.
for p in base.rglob('*'):
 if p.is_file() and p.suffix in ('.md','.json','.jsonl','.py','.txt','.csv','.bak'):
  data=p.read_bytes();new=data.replace(b'\r\n',b'\n')
  if data!=new:p.write_bytes(new)
for key,row in index.items():row['preview_sha256']=hashlib.sha256((base/key).read_bytes()).hexdigest()
(base/'executed-input-index.json').write_text(json.dumps({'note':'ZIP entries preserve executed bytes; plaintext previews use LF for Git portability. Compare protocol fixture hashes to ZIP entries. S original files and C skill files are already LF and match previews too.','files':index},indent=2)+'\n',encoding='utf-8',newline='')
p=base/'REPORT.md';s=p.read_text(encoding='utf-8').replace('Known fixed source/skill copies retain their original bytes.', 'Executed frozen input/skill bytes are retained in [executed-inputs.zip](executed-inputs.zip); [the input index](executed-input-index.json) records executed and LF-preview hashes. Plaintext previews use LF for portable Git storage. Corrected S originals and C skill files already use LF and still match their supplied fingerprints.')
p.write_text(s,encoding='utf-8',newline='')
manifest={p.relative_to(base).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(base.rglob('*')) if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(base/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='')
print('Exact inputs:',len(index),'entries; WIP manifest:',len(manifest),'files.')
