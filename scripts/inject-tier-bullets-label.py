#!/usr/bin/env python3
"""Inject "Что входит в тариф:" label CSS before tier bullets.
Adds <style id="glavnoe-tier-bullets-label"> right before </head>."""
from pathlib import Path

ROOT = Path('/root/framerexport/full-site-export-may21')
PAGES = ['content-product', 'product-statii', 'product-telegram', 'youtube-product']

# Label appears via CSS ::before pseudo on [data-bullets].
# Russian "Что входит в тариф:" — same for all cards.
CSS = (
  '<style id="glavnoe-tier-bullets-label">'
  '[data-glavnoe-tariffs="1"] [data-bullets]{position:relative;padding-top:8px;}'
  '[data-glavnoe-tariffs="1"] [data-bullets]::before{'
  'content:"Что входит в тариф:";'
  'display:block;'
  'font-family:"DM Sans","DM Sans Placeholder",sans-serif;'
  'font-weight:600;font-size:13px;line-height:18px;'
  'text-transform:uppercase;letter-spacing:0.4px;'
  'margin:0 0 12px 0;opacity:0.7;'
  '}'
  '[data-glavnoe-tariffs="1"] article[data-tier-style="dark"] [data-bullets]::before{opacity:0.85;}'
  '</style>'
)

MARK = 'id="glavnoe-tier-bullets-label"'

for slug in PAGES:
    f = ROOT / 'product' / slug / 'index.html'
    html = f.read_text(encoding='utf-8')
    if MARK in html:
        print(f'SKIP {slug} (already injected)')
        continue
    new = html.replace('</head>', CSS + '</head>', 1)
    if new == html:
        print(f'FAIL {slug}')
        continue
    f.write_text(new, encoding='utf-8')
    print(f'OK {slug}')
