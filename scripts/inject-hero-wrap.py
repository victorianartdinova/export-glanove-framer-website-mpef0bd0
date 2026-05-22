#!/usr/bin/env python3
"""Inject hero-wrap CSS into 4 product pages (not avito-ads).
Adds <style id="glavnoe-hero-wrap"> right before </head>."""
import re
from pathlib import Path

ROOT = Path('/root/framerexport/full-site-export-may21')
PAGES = ['content-product', 'product-statii', 'product-telegram', 'youtube-product']

CSS = (
  '<style id="glavnoe-hero-wrap">'
  '.framer-41obj2{width:100%!important;max-width:100%!important;}'
  '.framer-41obj2 h1,.framer-41obj2 h2,.framer-41obj2 .framer-text'
  '{white-space:normal!important;word-break:keep-all;overflow-wrap:break-word;line-height:1.1!important;}'
  '</style>'
)

MARK = 'id="glavnoe-hero-wrap"'

for slug in PAGES:
    f = ROOT / 'product' / slug / 'index.html'
    html = f.read_text(encoding='utf-8')
    if MARK in html:
        print(f'SKIP {slug} (already injected)')
        continue
    new = html.replace('</head>', CSS + '</head>', 1)
    if new == html:
        print(f'FAIL {slug}: </head> not found')
        continue
    f.write_text(new, encoding='utf-8')
    print(f'OK {slug}')
