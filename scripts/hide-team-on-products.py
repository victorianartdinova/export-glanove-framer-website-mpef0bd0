#!/usr/bin/env python3
"""FIX 2 — скрыть блок «Команда» (5 портретов) на 5 продуктовых страницах.

UX-аудит: блок «Команда» (Виктория / Александр / Мурат / Мариам / Ирина)
не нужен на продуктовых страницах. Должен быть только на /about/.

В framer-export секция команды — это <section data-framer-name="L"> (внутри
slideshow framer-rTJXX framer-2itchk). Tablet variant — "S". На /about/
команды нет (своя кастомная разметка), на главной — тоже нет.

Скрипт инжектит scoped CSS в <head> каждой продуктовой страницы, скрывающий
section[data-framer-name="L"] и section[data-framer-name="S"] и контейнер
.framer-13yoypl-container (внешний враппер, который иначе оставляет паддинг).

Также скрывает заголовок секции "(02) Наша команда" — Overlap Detailing
прямо перед слайдером, если такой блок есть.

Идемпотент: marker id="glavnoe-hide-team".
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    'product/avito-ads/index.html',
    'product/content-product/index.html',
    'product/product-statii/index.html',
    'product/product-telegram/index.html',
    'product/youtube-product/index.html',
]

MARKER = 'glavnoe-hide-team'

STYLE = (
    f'<style id="{MARKER}" data-fix="hide-team-on-products">'
    '/* FIX 2 — скрыть блок команды на продуктовых страницах */'
    'section[data-framer-name="L"][class*="framer-rTJXX"],'
    'section[data-framer-name="S"][class*="framer-rTJXX"],'
    '[class*="framer-13yoypl-container"],'
    '[class*="framer-1wnktnx-container"]'
    '{ display: none !important; }'
    '</style>'
)


def inject(path: Path) -> bool:
    html = path.read_text(encoding='utf-8')
    if f'id="{MARKER}"' in html:
        print(f'[skip] {path}')
        return False
    new = html.replace('</head>', STYLE + '</head>', 1)
    if new == html:
        print(f'[err] no </head> in {path}', file=sys.stderr)
        return False
    path.write_text(new, encoding='utf-8')
    print(f'[ok] {path}')
    return True


def main() -> int:
    ok = 0
    for rel in PAGES:
        p = ROOT / rel
        if not p.exists():
            print(f'[miss] {p}', file=sys.stderr)
            continue
        if inject(p):
            ok += 1
    print(f'\ninjected into {ok}/{len(PAGES)} pages')
    return 0


if __name__ == '__main__':
    sys.exit(main())
