#!/usr/bin/env python3
"""Inject scripts/case-extras.js as <script data-glavnoe-case-extras-v4>.

Adds publication link (SPB → PPC World) and a missing case body (Regardis).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS = (ROOT / 'scripts' / 'case-extras.js').read_text(encoding='utf-8')

TARGETS = [
    ROOT / 'work' / 'case-spb-15mln' / 'index.html',
    ROOT / 'work' / 'case-aag-promostranicy' / 'index.html',
    ROOT / 'work' / 'regardis-telegram-ads-premium' / 'index.html',
]

PATTERN = re.compile(
    r'<script data-glavnoe-case-extras-v4="1">.*?</script>\s*',
    re.DOTALL,
)
BLOCK = f'<script data-glavnoe-case-extras-v4="1">{JS}</script>\n'


def main():
    for path in TARGETS:
        if not path.exists():
            print(f'MISS {path}')
            continue
        html = path.read_text(encoding='utf-8')
        html2 = PATTERN.sub('', html)
        if '</body>' in html2:
            html2 = html2.replace('</body>', BLOCK + '</body>', 1)
        else:
            html2 = html2 + BLOCK
        if html2 != html:
            path.write_text(html2, encoding='utf-8')
            print(f'OK   {path.relative_to(ROOT)}')
        else:
            print(f'==   {path.relative_to(ROOT)}')

if __name__ == '__main__':
    sys.exit(main())
