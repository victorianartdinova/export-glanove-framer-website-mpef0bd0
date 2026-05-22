#!/usr/bin/env python3
"""Rename tier CTA button: «Обсудить тариф» → «Стартовать» on 4 product pages."""
import re
from pathlib import Path

ROOT = Path('/root/framerexport/full-site-export-may21')
PAGES = ['content-product', 'product-statii', 'product-telegram', 'youtube-product']

OLD = "var TIER_BUTTON_LABEL = 'Обсудить тариф';"
NEW = "var TIER_BUTTON_LABEL = 'Стартовать';"

for slug in PAGES:
    f = ROOT / 'product' / slug / 'index.html'
    h = f.read_text(encoding='utf-8')
    if OLD not in h:
        # Try double-quoted variant
        oldq = 'var TIER_BUTTON_LABEL = "Обсудить тариф";'
        newq = 'var TIER_BUTTON_LABEL = "Стартовать";'
        if oldq in h:
            h = h.replace(oldq, newq, 1)
        else:
            print(f'SKIP {slug}: pattern not found')
            continue
    else:
        h = h.replace(OLD, NEW, 1)
    f.write_text(h, encoding='utf-8')
    print(f'OK {slug}: button → Стартовать')
