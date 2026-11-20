import json, sys
from pathlib import Path
skill=Path(r'<HOME>\AppData\Local\Temp\sheet-rerun-a0fa29d0bc874d10b361b6469c8db2e1\home-sheet-New-rep2\skills\gpt-im-cooked\scripts')
sys.path.insert(0, str(skill))
import render_sheet as rs
p=Path('outputs/sta-final-sheet.json')
data=json.loads(p.read_text(encoding='utf-8'))
table=next(s for s in data['sections'] if s['id']=='table')
table['title']='Worked table example: let the reference group set the denominator'
table['blocks']=[
    table['blocks'][0],
    {
      'type':'example',
      'setup':'One table: commuters: 10 cycle, 15 do not (25 total); noncommuters: 5 cycle, 10 do not (15 total). Choose the reference group named in the question.',
      'steps':[
        {'label':'Row: cycle among commuters','text':'10 / 25 = **40.0% of commuters**.'},
        {'label':'Column: commuters among cyclists','text':'10 / 15 = **66.7% of cyclists**. For the earlier column-denominator error, use the cycle-column total 15, not the commuter-row total 25.'}
      ],
      'takeaway':'The shared count is 10; the percentage changes because the reference group changes.'
    },
    {'type':'cue','text':'Conditional probability assumes equally weighted cases and a nonempty reference group. (Notes section 1.4)'}
]
data['sections'][2]['blocks'][0]['steps'][1]['text']='Compare the same summary across groups (mean with mean, count with count); do not compare a group mean with a group total. (Notes section 3.3)'
data['sections'][2]['blocks'][0]['takeaway']='One summary value per nonempty group. (Notes sections 3.1-3.2)'
data['revision']={'round':2,'standing':['No new information; use one worked table example in place of abstract interpretation rules.'],'changes':['Replaced abstract row/column and conditional-probability interpretation rules with one worked example; increased readability by using the most spacious layout.']}
sheet=rs.load_sheet(data)
p.write_text(json.dumps(data,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
html=rs.to_html(sheet,0)
out=Path('outputs/sta-final-sheet.html')
out.write_text(html,encoding='utf-8')
print('revision',data['revision']['round'],'sections',len(sheet['sections']),'html_bytes',out.stat().st_size,'body_font_pt',rs.PRESETS[0]['body'],'print_columns',2)
print('external_assets', 'https://' in html or 'http://' in html)
