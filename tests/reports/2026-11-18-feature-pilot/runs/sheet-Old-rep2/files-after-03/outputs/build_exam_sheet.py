from pathlib import Path
import re, html, fitz
src=Path('outputs/exam-sheet-draft.md').read_text(encoding='utf-8-sig')
parts=re.split(r'(?m)^## SIDE B.*$',src,maxsplit=1)
assert len(parts)==2
side_a=parts[0]; side_b='## SIDE B'+parts[1]
def make_html(md):
    lines=md.splitlines(); blocks=[]; i=0
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
        plain=re.sub(r'\*\*(.*?)\*\*',r'\1',s).replace('`','')
        esc=html.escape(plain)
        if s.startswith('# '): blocks.append('<h1>'+html.escape(s[2:])+'</h1>')
        elif s.startswith('## '): blocks.append('<h2>'+html.escape(s[3:])+'</h2>')
        elif s.startswith('### '): blocks.append('<h3>'+html.escape(s[4:])+'</h3>')
        elif s.startswith('- '): blocks.append('<p class="bullet">&#8226; '+html.escape(plain[2:])+'</p>')
        else: blocks.append('<p>'+esc+'</p>')
        i+=1
    return '''<html><head><style>
body { font-family:sans-serif; font-size:13.5pt; line-height:1.36; color:#182230; }
h1 { font-size:22pt; color:#123b63; margin:0 0 10pt; } h2 { font-size:18pt; color:#145a72; margin:13pt 0 7pt; }
h3 { font-size:15pt; color:#145a72; margin:11pt 0 5pt; } p { margin:0 0 9pt; }
table { border-collapse:collapse; width:100%; margin:3pt 0 6pt; font-size:12pt; }
th { background:#e7f0f5; text-align:left; } td,th { border:0.5pt solid #b8c8d3; padding:5pt; vertical-align:top; }
.bullet { margin-left:8pt; }
</style></head><body>'''+''.join(blocks)+'</body></html>'
doc=fitz.open()
for md in (side_a,side_b):
    page=doc.new_page(width=612,height=792)
    story=fitz.Story(html=make_html(md))
    more,filled=story.place(fitz.Rect(42,38,570,754))
    story.draw(page.get_drawings if False else page.new_shape().doc) if False else None
    # render Story through a temporary one-page writer
    page.delete_image if False else None
    # Easier: create via writer in the loop below
# Write each side using Story/DocumentWriter for fixed letter pages
out=fitz.DocumentWriter('outputs/exam-sheet-draft.pdf')
for md in (side_a,side_b):
    story=fitz.Story(html=make_html(md)); dev=out.begin_page(fitz.Rect(0,0,612,792))
    more,filled=story.place(fitz.Rect(42,38,570,754)); story.draw(dev); out.end_page()
    if more: raise RuntimeError('Side overflows one page')
out.close(); check=fitz.open('outputs/exam-sheet-draft.pdf')
print('pages',len(check),'chars',[len(p.get_text()) for p in check])
for i,p in enumerate(check): p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(f'outputs/exam-side-{i+1}.png')




