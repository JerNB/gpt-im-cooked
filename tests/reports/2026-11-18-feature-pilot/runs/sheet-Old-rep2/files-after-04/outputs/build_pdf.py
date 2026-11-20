from pathlib import Path
import re, html, fitz
src=Path('outputs/study-guide.md').read_text(encoding='utf-8')
lines=src.splitlines(); blocks=[]; i=0
while i<len(lines):
    s=lines[i].strip()
    if not s: i+=1; continue
    if s.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-{2,}:?',c.replace(' ','')) for c in cells): rows.append(cells)
            i+=1
        if rows:
            t='<table><tr>'+''.join('<th>'+html.escape(c)+'</th>' for c in rows[0])+'</tr>'
            for row in rows[1:]: t+='<tr>'+''.join('<td>'+html.escape(c)+'</td>' for c in row)+'</tr>'
            blocks.append(t+'</table>')
        continue
    plain=re.sub(r'\*\*(.*?)\*\*',r'\1',s); plain=plain.replace('`','')
    esc=html.escape(plain)
    if s.startswith('# '): blocks.append('<h1>'+html.escape(s[2:])+'</h1>')
    elif s.startswith('## '): blocks.append('<h2>'+html.escape(s[3:])+'</h2>')
    elif s.startswith('- '): blocks.append('<p class="bullet">&#8226; '+html.escape(plain[2:])+'</p>')
    elif re.match(r'^\d+\. ',s): blocks.append('<p class="bullet">'+esc+'</p>')
    else: blocks.append('<p>'+esc+'</p>')
    i+=1
html_doc='''<html><head><style>
body { font-family: sans-serif; font-size: 10.5pt; line-height: 1.3; color: #182230; }
h1 { color:#123b63; font-size:20pt; margin-bottom:8pt; } h2 { color:#145a72; font-size:14pt; margin-top:13pt; margin-bottom:5pt; }
p { margin:0 0 6pt 0; } table { border-collapse:collapse; width:100%; margin:3pt 0 8pt; font-size:8.5pt; }
th { background:#e7f0f5; color:#123b63; text-align:left; } td,th { border:0.5pt solid #b8c8d3; padding:4pt; vertical-align:top; }
.bullet { margin-left:10pt; }
</style></head><body>'''+''.join(blocks)+'</body></html>'
rect=fitz.Rect(54,54,558,738); story=fitz.Story(html=html_doc); writer=fitz.DocumentWriter('outputs/study-guide.pdf')
while True:
    dev=writer.begin_page(fitz.Rect(0,0,612,792)); more,_=story.place(rect); story.draw(dev); writer.end_page()
    if not more: break
writer.close(); doc=fitz.open('outputs/study-guide.pdf')
print('pages',len(doc),'chars',[len(p.get_text()) for p in doc])
for i,p in enumerate(doc): p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(f'outputs/page-{i+1}.png')
