#!/usr/bin/env python3
"""FIX 3 — гигантский футер «Glavnoe» уменьшить вдвое.

Декоративная надпись "Glavnoe" в футере main page имеет font-size:224px
(rendered ~1.7em высоты футера). Уменьшаем в 2 раза до 112px на desktop,
пропорционально на mobile (-10.7px letter-spacing тоже шкалится).

Footer Heading контейнер: <div class="framer-cknar8" data-framer-name="Heading">
с h1.framer-text.

Идемпотент: marker id="glavnoe-footer-half".
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'index.html'
MARKER = 'glavnoe-footer-half'

STYLE = (
    f'<style id="{MARKER}" data-fix="footer-glavnoe-half">'
    '/* FIX 3 — уменьшаем гигантский декоративный Glavnoe в футере в 2 раза */'
    '[data-framer-name="Heading"] h1.framer-text {'
    '  --framer-font-size: 112px !important;'
    '  font-size: 112px !important;'
    '  --framer-letter-spacing: -5.35px !important;'
    '  letter-spacing: -5.35px !important;'
    '}'
    '@media (max-width: 810px) {'
    '  [data-framer-name="Heading"] h1.framer-text {'
    '    --framer-font-size: 56px !important;'
    '    font-size: 56px !important;'
    '    --framer-letter-spacing: -2.5px !important;'
    '    letter-spacing: -2.5px !important;'
    '  }'
    '}'
    '</style>'
)


def main() -> int:
    html = PAGE.read_text(encoding='utf-8')
    if f'id="{MARKER}"' in html:
        print(f'[skip] already injected in {PAGE}')
        return 0
    new = html.replace('</head>', STYLE + '</head>', 1)
    if new == html:
        print(f'[err] no </head> in {PAGE}', file=sys.stderr)
        return 1
    PAGE.write_text(new, encoding='utf-8')
    print(f'[ok] injected footer-glavnoe-half into {PAGE}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
