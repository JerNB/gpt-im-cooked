"""Create shuffled content-only review packets after all eight selected sessions finish."""
from pathlib import Path
import json
import random
import re

BASE=Path(__file__).resolve().parent


def mask(text):
    text=re.sub(r'\*{0,2}Hi student, let.s get you uncooked\.\*{0,2}','',text,flags=re.I)
    text=re.sub(r'(?:C|D)-(?:S|P)-rep[12]','[session]',text)
    text=re.sub(r'(?:\.\./)*skill-[CD]/[^\s)\"\x27]+','[workflow reference]',text)
    text=re.sub(r'(?:skill/)?(?:SKILL\.md|references/(?:state(?:-imports|-reference)?|concept-tutoring|practice-and-feedback)\.md)','[workflow reference]',text)
    return text.replace("GPT, I'm Cooked",'[workflow]').replace('GPT, I’m Cooked','[workflow]')


def main():
    selected=json.loads((BASE/'selected-completion.json').read_text(encoding='utf-8'))
    assert selected['completed_sessions']==8 and not selected['partial_mode'],'Run complete resource analysis first, without --allow-partial'
    sessions=sorted(selected['selected'].items());random.Random(7014).shuffle(sessions)
    dest=BASE/'blind'
    assert not dest.exists(),'Refusing to overwrite blinded review packets'
    dest.mkdir();mapping={}
    for i,(label,relative) in enumerate(sessions,1):
        case=f'CASE-{i:02}';mapping[case]=label;path=BASE/relative;packet=label.split('-')[1].lower()
        rubric=json.loads((BASE/'fixtures'/('packet-'+packet)/'rubric-v2.json').read_text(encoding='utf-8'))
        turns=[]
        for n in range(1,12):
            snap=path/f'files-after-{n:02}'
            records={p.relative_to(snap).as_posix():mask(p.read_text(encoding='utf-8')) for p in snap.rglob('*.md') if p.name in ('learning-record.md','course-profile.md')}
            turns.append({'turn':n,'student':mask((path/f'prompt-{n:02}.md').read_text(encoding='utf-8')),
                          'reply':mask((path/f'response-{n:02}.md').read_text(encoding='utf-8')),'saved_records':records})
        materials={p.relative_to(BASE/'fixtures'/('packet-'+packet)).as_posix():p.read_text(encoding='utf-8') for p in (BASE/'fixtures'/('packet-'+packet)/'materials').glob('*.md')}
        payload={'case':case,'rubric':rubric,'materials':materials,'turns':turns,'limits':'Arm mapping, cost counters and skill source excluded. Record format can permit inference; parent wrote adaptive answers and is not blind.'}
        (dest/(case+'.json')).write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='')
    (BASE/'blind-map.json').write_text(json.dumps(mapping,indent=2)+'\n',encoding='utf-8',newline='')
    print('Eight shuffled review packets prepared; mapping kept outside review folder.')


if __name__=='__main__':
    main()
