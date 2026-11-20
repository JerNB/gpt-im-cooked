import json, sys, subprocess
from pathlib import Path
skill=Path(r'<HOME>\AppData\Local\Temp\sheet-rerun-a0fa29d0bc874d10b361b6469c8db2e1\home-sheet-New-rep2\skills\gpt-im-cooked\scripts')
sys.path.insert(0, str(skill))
import render_sheet as rs
sheet=rs.load_sheet(json.loads(Path('outputs/sta-final-sheet.json').read_text(encoding='utf-8')))
html=rs.to_html(sheet, 0)
html_path=Path('outputs/sta-final-sheet.html').resolve()
html_path.write_text(html, encoding='utf-8')
browser=Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
profile=Path('outputs/tmp/edge-profile').resolve(); profile.mkdir(parents=True, exist_ok=True)
pdf=Path('outputs/sta-final-sheet.pdf').resolve()
url=html_path.as_uri()
args=[str(browser),'--headless','--disable-gpu','--no-first-run','--no-default-browser-check',f'--user-data-dir={profile}',f'--print-to-pdf={pdf}','--no-pdf-header-footer',url]
r=subprocess.run(args, capture_output=True, text=True, timeout=90)
print('edge_exit',r.returncode)
print('pdf_exists',pdf.exists(), 'bytes',pdf.stat().st_size if pdf.exists() else 0)
if pdf.exists():
    data=pdf.read_bytes(); print('page_count',rs.pdf_page_count(data))
print('stderr',r.stderr[-1200:])
