from pathlib import Path
p=Path('outputs/sta-final-sheet.json')
lines=p.read_text(encoding='utf-8').splitlines()
lines[12]='      {"type":"text","text":"Example counts: among 25 commuters, 10 cycle and 15 do not; among 15 noncommuters, 5 cycle and 10 do not. Total = 40. (Notes sections 1-2; practice Q1)"},'
lines[13]='      {"type":"example","setup":"Ask first: Among which group? That group is the denominator.","steps":['
lines[14]='        {"label":"Among commuters, what share cycle?","text":"10 / 25 = **40.0% of commuters**. P(cycle | commuter): overlap divided by commuter total."},'
lines[16]='        {"label":"Row percentage","text":"Cell divided by its row total. Each row sums to 100%. Example: commuter/cycle = 10/25 = 40.0%."},'
lines[17]='        {"label":"Column percentage","text":"Cell divided by its column total. Each column sums to 100%. Example: commuter/cycle = 10/15 = 66.7%."}],"takeaway":"P(A | B) means A among B: B supplies the denominator. P(A | B) usually differs from P(B | A). (Notes sections 1.1-1.4, 2.2-2.3)"},'
lines[23]='        {"label":"Rows returned","text":"One row per nonempty group. Four nonempty sections = **4 rows**, even if the original data had 120 students. (Notes section 3.2; 2025 past paper Q3)"},'
lines[25]='    ]}'
p.write_text('\n'.join(lines)+'\n', encoding='utf-8')
