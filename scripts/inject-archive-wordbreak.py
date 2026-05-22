#!/usr/bin/env python3
"""FIX 1 — word-break на карточках главной mobile

На главной в mobile (<=1024px) названия карточек продуктов внутри секции
"Archive" переносятся по слогам ("Коммуникаци / онная / стратегия", "Личный /
бренд / YouTube"). Это hyphens=auto + word-break=break-word из Framer-стилей.

Этот скрипт инжектит scoped CSS в <head> /index.html: ломку по слогам и
форс-перенос отключаем для h5 и framer-text внутри section[data-framer-name="Archive"].

Идемпотент: marker id="glavnoe-archive-wordbreak".
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'index.html'

MARKER = 'glavnoe-archive-wordbreak'

STYLE = (
    f'<style id="{MARKER}" data-fix="archive-wordbreak">'
    '/* FIX 1 — отключаем перенос по слогам в карточках products на главной mobile.'
    '   Дополнительно: уменьшаем fz/letter-spacing, чтобы длинные слова'
    '   ("Коммуникационная") помещались по слову, а не резались. */'
    '@media (max-width: 1024px) {'
    '  section[data-framer-name="Archive"] h5,'
    '  section[data-framer-name="Archive"] h5 *,'
    '  section[data-framer-name="Archive"] .framer-text {'
    '    word-break: keep-all !important;'
    '    overflow-wrap: normal !important;'
    '    word-wrap: normal !important;'
    '    -webkit-hyphens: none !important;'
    '    hyphens: none !important;'
    '  }'
    '  /* fz fit для длинных слов в правой колонке Archive (171px на 390px) */'
    '  section[data-framer-name="Archive"] h5 {'
    '    --framer-font-size: 18px !important;'
    '    font-size: 18px !important;'
    '    line-height: 22px !important;'
    '    letter-spacing: -0.6px !important;'
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
        print(f'[err] no </head> found in {PAGE}', file=sys.stderr)
        return 1
    PAGE.write_text(new, encoding='utf-8')
    print(f'[ok] injected archive-wordbreak fix into {PAGE}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
