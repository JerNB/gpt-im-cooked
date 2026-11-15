"""Mirror completed runs, preserve pre-normalization bytes, then write manifest LAST."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import zipfile

BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parents[1]))
import run_cost_comparison as runner


def main():
    scratch=Path.home()/'codex-runs/T007-review'
    # Later batches consume these executed bytes even after Git-portable previews use LF.
    for source in (BASE/'fixtures').iterdir():
        target=scratch/'frozen-packets'/source.name
        if not target.exists():
            shutil.copytree(source,target)
    for report in BASE.iterdir():
        if not report.is_dir() or not (report/'protocol.json').is_file():
            continue
        statefiles=list(scratch.glob(report.name+'/state.json'))
        if not statefiles:
            continue
        state=json.loads(statefiles[0].read_text(encoding='utf-8'))
        if state['failed'] or state['last_turn'] not in (2,11):
            continue
        work=Path(state['cwd']);out=report/'runs'/state['label']
        for p in work.rglob('*'):
            rel=p.relative_to(work)
            if not p.is_file() or 'skill' in rel.parts or '__pycache__' in rel.parts or rel.name=='AGENTS.md':
                continue
            dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():
                shutil.copy2(p,dest)
        for snap in out.glob('files-after-*'):
            if not (snap/'materials').exists():
                shutil.copytree(work/'materials',snap/'materials')
    archive=BASE/'executed-evidence.zip';index={}
    with zipfile.ZipFile(archive,'a',compression=zipfile.ZIP_DEFLATED) as z:
        existing=set(z.namelist())
        for p in sorted(BASE.rglob('*')):
            if not p.is_file():
                continue
            rel=p.relative_to(BASE)
            is_input=any(x in ('fixtures','skill-C','skill-D') for x in rel.parts)
            is_record=p.name in ('learning-record.md','course-profile.md')
            if not (is_input or is_record):
                continue
            name=rel.as_posix()
            if name not in existing:
                z.writestr(name,p.read_bytes())
            index[name]={'executed_sha256':hashlib.sha256(z.read(name)).hexdigest()}
    transformations=[]
    for p in sorted(BASE.rglob('*')):
        if not p.is_file() or p.suffix not in (runner.TEXT|{'.py','.csv'}):
            continue
        old=p.read_bytes();new=old.replace(b'\r\n',b'\n')
        if old!=new:
            p.write_bytes(new)
            transformations.append({'path':p.relative_to(BASE).as_posix(),'before_sha256':hashlib.sha256(old).hexdigest(),'after_sha256':hashlib.sha256(new).hexdigest(),'kind':'LF-preview'})
    for name,row in index.items():
        row['preview_sha256']=hashlib.sha256((BASE/name).read_bytes()).hexdigest()
    runner.frozen.dump(BASE/'executed-evidence-index.json',{'note':'ZIP entries preserve executed input and pre-normalization record snapshot bytes. Plaintext previews use LF; future calls use external frozen-packets, never converted previews. Existing ZIP entries never overwritten.','files':index})
    ledger=BASE/'archive-transformations.json'
    prior=json.loads(ledger.read_text(encoding='utf-8')) if ledger.exists() else []
    runner.frozen.dump(ledger,prior+transformations)
    manifest={p.relative_to(BASE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(BASE.rglob('*')) if p.is_file() and p!=BASE/'manifest.json' and '__pycache__' not in p.parts}
    runner.frozen.dump(BASE/'manifest.json',manifest)
    print(f'Archive preserved {len(index)} byte-exact entries; manifest {len(manifest)} files written last.')


if __name__=='__main__':
    main()
