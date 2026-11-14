from pathlib import Path
import re, os, json
base=Path(__file__).parent
changes=json.loads((base/'archive-link-transformations.json').read_text(encoding='utf-8')) if (base/'archive-link-transformations.json').exists() else []
for reportroot in [base]+[p for p in base.iterdir() if p.is_dir() and (p/'runs').is_dir()]:
 runs=reportroot/'runs'
 if not runs.is_dir():continue
 for out in runs.iterdir():
  if not out.is_dir() or not re.fullmatch(r'(A1|A2|B|C)-(S|P)-rep[12]',out.name):continue
  arm=out.name.split('-')[0]
  for p in out.rglob('*.md'):
   rel=p.relative_to(out);logical=out/rel.parts[0] if rel.parts[0].startswith('files-after-') or rel.parts[0]=='final-files' else out
   text=p.read_text(encoding='utf-8')
   def rewrite(match):
    label,target=match.groups();clean=target.removeprefix('file://').lstrip('/')
    if target.startswith('skill/') and arm in ('B','C') and (reportroot/f'skill-{arm}'/target[6:]).exists():
     new=os.path.relpath(reportroot/f'skill-{arm}'/target[6:],p.parent).replace('\\','/')
     changes.append({'file':p.relative_to(base).as_posix(),'old_target':target,'new_target':new,'kind':'shared-frozen-skill-reference'})
     return '['+label+']('+new+')'
    line=re.fullmatch(r'(.+):(\d+)',target)
    if line and (p.parent/line[1]).exists():
     changes.append({'file':p.relative_to(base).as_posix(),'old_target':target,'new_target':line[1],'kind':'source-line-locator'})
     return '['+label+']('+line[1]+') (line '+line[2]+')'
    prefix='<ROOT>/run-'+out.name+'/'
    if clean.startswith(prefix):
     tail=clean[len(prefix):];dest=logical/tail
     if tail.startswith('skill/') and arm in ('B','C'):dest=reportroot/f'skill-{arm}'/tail[len('skill/'):]
     if dest.exists():
      new=os.path.relpath(dest,p.parent).replace('\\','/')
      changes.append({'file':p.relative_to(base).as_posix(),'old_target':target,'new_target':new,'kind':'internal-workspace-link'})
      return '['+label+']('+new+')'
    if '<ROOT>' in target:
     changes.append({'file':p.relative_to(base).as_posix(),'old_target':target,'kind':'nonportable-path-rendered-as-text'})
     return label+' (archived path: `'+target+'`)'
    return match.group(0)
   result=re.sub(r'\[([^\]]*)\]\(([^)\n]*)\)',rewrite,text)
   if result!=text:p.write_text(result,encoding='utf-8',newline='')
(base/'archive-link-transformations.json').write_text(json.dumps(changes,indent=2)+'\n',encoding='utf-8',newline='')
print('Recorded archive display-link transformations:',len(changes))
