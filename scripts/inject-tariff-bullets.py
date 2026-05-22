#!/usr/bin/env python3
"""Inject scripts/tariff-bullets.js into 4 product pages.

Targets: content-product, product-statii, product-telegram, youtube-product.
Skips avito-ads (master template, untouched).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS = (ROOT / 'scripts' / 'tariff-bullets.js').read_text(encoding='utf-8')

TARGETS = [
    ROOT / 'product' / 'content-product' / 'index.html',
    ROOT / 'product' / 'product-statii' / 'index.html',
    ROOT / 'product' / 'product-telegram' / 'index.html',
    ROOT / 'product' / 'youtube-product' / 'index.html',
]

PATTERN = re.compile(r'<script data-glavnoe-tariff-bullets="1">.*?</script>\s*', re.DOTALL)
BLOCK = f'<script data-glavnoe-tariff-bullets="1">{JS}</script>\n'


def main():
    for path in TARGETS:
        html = path.read_text(encoding='utf-8')
        html2 = PATTERN.sub('', html)
        if '</body>' in html2:
            html2 = html2.replace('</body>', BLOCK + '</body>', 1)
        else:
            html2 += BLOCK
        if html2 != html:
            path.write_text(html2, encoding='utf-8')
            print(f'OK   {path.relative_to(ROOT)}')
        else:
            print(f'==   {path.relative_to(ROOT)}')

if __name__ == '__main__':
    sys.exit(main())
