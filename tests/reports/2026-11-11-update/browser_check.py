"""Independent local Chromium checks of captured recovery-batch worksheets.

Uses the already-installed Python Playwright and Chromium, with no downloads.
Synthetic browser responses are exported here, never written into study records.
"""
from pathlib import Path
import json
import re
from importlib.metadata import version as package_version
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'browser'
OUT.mkdir(exist_ok=True)
results = []
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    version = browser.version
    for study in sorted((ROOT / 'model-recovery/runs').glob('pair-*/final-study')):
        name = study.parent.name
        pages = [p for p in study.rglob('*.html') if 'skill' not in p.relative_to(study).parts]
        papers = [p for p in pages if re.search(r'<(?:input|textarea)\b', p.read_text(encoding='utf-8'), re.I)]
        if len(papers) != 1:
            raise AssertionError(f'{name}: expected one worksheet with answer controls, found {len(papers)}')
        context = browser.new_context(viewport={'width': 1280, 'height': 900}, accept_downloads=True)
        network, errors = [], []
        context.route(re.compile(r'^https?://'), lambda route: route.abort())
        context.on('request', lambda request: network.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(papers[0].as_uri())
        checks = {}
        screenshots = []
        for width in (1280, 375):
            page.set_viewport_size({'width': width, 'height': 900})
            page.screenshot(path=str(OUT / f'{name}-{width}.png'))
            screenshots.append(f'browser/{name}-{width}.png')
            checks[f'no_document_overflow_{width}'] = page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.set_viewport_size({'width': 1280, 'height': 900})
        page.evaluate("document.documentElement.style.zoom='1.5'")
        checks['no_document_overflow_css_zoom_150_percent'] = page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.evaluate("document.documentElement.style.zoom=''")
        page.keyboard.press('Tab')
        checks['keyboard_reaches_control'] = page.evaluate("['A','BUTTON','INPUT','TEXTAREA','SUMMARY','SELECT'].includes(document.activeElement.tagName)")
        checks['starts_without_checked_answers'] = page.locator('input[type=radio]:checked').count() == 0
        radios = page.locator('input[type=radio]:visible')
        if radios.count():
            radios.first.check()
        text = page.locator('textarea:not([readonly]):visible')
        if text.count():
            text.first.fill('Independent synthetic browser check; this is not a student attempt.')
        export = page.locator('button#export')
        if not export.count():
            raise AssertionError(f'{name}: cannot identify the worksheet export action')

        def exported(label):
            with page.expect_download(timeout=10000) as download:
                export.first.click()
            path = OUT / f'{name}-{label}.json'
            download.value.save_as(path)
            return json.loads(path.read_text(encoding='utf-8'))

        first, second = exported('first'), exported('repeat')
        checks['export_schema_1_0'] = first.get('schema_version') == '1.0'
        items = first.get('items')
        if items is None:
            history = first.get('attempt_history') or first.get('history') or []
            items = (history[-1].get('items') or history[-1].get('responses') or []) if history else []
        checks['five_exported_items'] = len(items) == 5
        checks['repeat_export_stable_attempt'] = first.get('attempt_id') == second.get('attempt_id')
        checks['repeat_export_stable_session'] = first.get('session_id') == second.get('session_id')
        # The candidate has fixed template selectors; check the complete exposure/retry path independently.
        if name.endswith('-v2') and page.locator('#key-link').count() and page.locator('#retry').count():
            page.locator('#key-link').evaluate('(a) => { let d=a.closest("details"); if(d) d.open=true; }')
            with context.expect_page() as popup:
                page.locator('#key-link').click()
            popup.value.wait_for_load_state()
            popup.value.close()
            page.locator('#retry').click()
            retry = exported('retry-after-key')
            checks['retry_has_new_attempt'] = retry.get('attempt_id') != first.get('attempt_id')
            checks['retry_keeps_session'] = retry.get('session_id') == first.get('session_id')
            checks['retry_keeps_key_exposure'] = all(i['assistance']['key_opened_in_page'] for i in retry['items'])
            checks['prior_snapshot_keeps_pre_key_exposure'] = any(
                all(not item['assistance']['key_opened_in_page'] for item in snap['items'])
                for snap in retry.get('attempt_history', []))
        checks['no_page_javascript_errors'] = not errors
        checks['no_http_requests'] = not network
        results.append({'run': name, 'worksheet': papers[0].relative_to(ROOT).as_posix(), 'checks': checks,
                        'page_errors': errors, 'http_requests': network, 'screenshots': screenshots})
        context.close()
    browser.close()
config = json.loads((ROOT / 'model-recovery/protocol.json').read_text(encoding='utf-8'))
assert len(results) == 2 * config['pairs'], 'Expected both captured study workspaces in each recovery pair'
payload = {'browser': 'Chromium ' + version, 'playwright': package_version('playwright'), 'headless': True, 'viewport_heights': 900,
           'limits': 'Desktop and emulated CSS viewport, not a physical phone or accessibility certification; no print check.',
           'results': results}
(OUT / 'results.json').write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8', newline='\n')
failed = [(r['run'], name) for r in results for name, passed in r['checks'].items() if not passed]
print(json.dumps({'runs': len(results), 'checks': sum(len(r['checks']) for r in results), 'failed': failed,
                  'browser': payload['browser']}, indent=2))
if failed:
    raise SystemExit('Browser concerns recorded; inspect results and screenshots')
