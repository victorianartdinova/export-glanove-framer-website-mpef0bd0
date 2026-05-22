#!/usr/bin/env python3
"""Inject scripts/nav-fixer.js into every page as <script data-glavnoe-nav-v3>.

Idempotent: re-runs replace previous v3 block in place.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS_PATH = ROOT / 'scripts' / 'nav-fixer.js'

HTML_FILES = sorted([
    p for p in ROOT.rglob('index.html')
    if '.git' not in p.parts and 'node_modules' not in p.parts and 'seo-report' not in p.parts
])

MARKER_OPEN = '<script data-glavnoe-nav-v3="1">'
MARKER_CLOSE = '</script>'

PATTERN = re.compile(
    r'<script data-glavnoe-nav-v3="1">.*?</script>\s*',
    re.DOTALL,
)

def inject(html: str, payload: str) -> str:
    block = f'{MARKER_OPEN}{payload}{MARKER_CLOSE}\n'
    html = PATTERN.sub('', html)
    if '</body>' not in html:
        return html + block
    return html.replace('</body>', block + '</body>', 1)

def main():
    payload = JS_PATH.read_text(encoding='utf-8')
    changed = 0
    for path in HTML_FILES:
        original = path.read_text(encoding='utf-8')
        updated = inject(original, payload)
        if updated != original:
            path.write_text(updated, encoding='utf-8')
            changed += 1
        print(f'{"OK " if updated != original else "== "} {path.relative_to(ROOT)}')
    print(f'Updated: {changed}/{len(HTML_FILES)}')

if __name__ == '__main__':
    sys.exit(main())
