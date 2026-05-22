#!/usr/bin/env python3
"""Rewrite canonical & og:url to relative project paths.

Before:  https://glanove.framer.website/<path>
After:   /<path>/

Skips files in .git, node_modules, seo-report. Does not touch og:image (those are valid /assets/).
Applies to canonical, og:url, twitter:url.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ABS_HOST = 'https://glanove.framer.website'

PATTERN_HREF = re.compile(r'(href=")' + re.escape(ABS_HOST) + r'([^"]*)("[^>]*?rel="canonical")')
PATTERN_HREF2 = re.compile(r'(rel="canonical"[^>]*?href=")' + re.escape(ABS_HOST) + r'([^"]*)(")')
PATTERN_OG_URL = re.compile(r'(property="og:url"[^>]*?content=")' + re.escape(ABS_HOST) + r'([^"]*)(")')
PATTERN_TW_URL = re.compile(r'(property="twitter:url"[^>]*?content=")' + re.escape(ABS_HOST) + r'([^"]*)(")')


def canonicalize_path(p: str) -> str:
    if not p or p == '/':
        return '/'
    if not p.startswith('/'):
        p = '/' + p
    if not p.endswith('/') and '.' not in p.rsplit('/', 1)[-1]:
        p = p + '/'
    return p


def patch(html: str) -> tuple[str, int]:
    count = 0
    def repl(m):
        nonlocal count
        count += 1
        return m.group(1) + canonicalize_path(m.group(2)) + m.group(3)
    new = PATTERN_HREF.sub(repl, html)
    new = PATTERN_HREF2.sub(repl, new)
    new = PATTERN_OG_URL.sub(repl, new)
    new = PATTERN_TW_URL.sub(repl, new)
    return new, count


def main():
    files = sorted([
        p for p in ROOT.rglob('index.html')
        if '.git' not in p.parts and 'node_modules' not in p.parts and 'seo-report' not in p.parts
    ])
    total = 0
    for path in files:
        html = path.read_text(encoding='utf-8')
        new, n = patch(html)
        if n:
            path.write_text(new, encoding='utf-8')
            total += n
            print(f'OK   {path.relative_to(ROOT)} ({n} replacements)')
        else:
            print(f'==   {path.relative_to(ROOT)}')
    print(f'Total replacements: {total}')

if __name__ == '__main__':
    sys.exit(main())
