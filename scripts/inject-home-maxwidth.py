#!/usr/bin/env python3
"""A1 (img-100946) — добавить max-width 1440 на широкие секции главной
которые на >=1440 viewport растягиваются за разумные пределы."""
from pathlib import Path
f = Path('/root/framerexport/full-site-export-may21/index.html')
MARK = 'id="glavnoe-home-maxwidth"'
CSS = (
    '<style id="glavnoe-home-maxwidth">'
    '@media (min-width:1440px){'
    # Все основные wide-секции получают max-width
    'section[data-framer-name="Archive"] > .framer-yUKpH,'
    'section[data-framer-name="Archive"] > div,'
    'section[data-framer-name="Article"] > div,'
    'section[data-framer-name="Form"] > div'
    '{max-width:1440px!important;margin-left:auto!important;margin-right:auto!important;}'
    '}'
    '</style>'
)
h = f.read_text(encoding='utf-8')
if MARK in h:
    print('SKIP')
else:
    h = h.replace('</head>', CSS + '</head>', 1)
    f.write_text(h, encoding='utf-8')
    print('OK home max-width')
