#!/usr/bin/env python3
"""FIX 4 (D1): убрать ссылку «Разработали сайт мы:)».

Вика 22.05: «убрать ссылку с фразы "сайт разработали мы"». Фраза в HTML —
«Разработали сайт мы:)», ссылка ведёт на https://t.me/ksandrbloger
(SSR) и https://contra.com/future_things_... (после hydration из Framer
JS chunk).

Делаем два шага:
1. Убираем `<a href>` в SSR HTML, оставляем текст в `<span>`.
2. Добавляем JS-инжект `glavnoe-strip-dev-link`, который после
   гидратации мониторит DOM и преобразует появившуюся `<a>` обратно
   в `<span>` (Framer вставляет её из payload).

Затронуты все footer-ы: index, продукты, work-кейсы, 404.
"""
from pathlib import Path
import re

ROOT = Path('/root/framerexport/full-site-export-may21')

FILES = [
    'index.html',
    'product/avito-ads/index.html',
    'product/product-statii/index.html',
    'product/youtube-product/index.html',
    'product/content-product/index.html',
    'product/product-telegram/index.html',
    'work/case-aag-promostranicy/index.html',
    'work/regardis-telegram-ads-premium/index.html',
    'work/case-spb-15mln/index.html',
    '404/index.html',
]

LINK_RE = re.compile(
    r'<a\b([^>]*)>([^<]*[Рр]азработали сайт мы[^<]*)</a>',
    re.DOTALL,
)

POST_HYDRATE_SCRIPT = (
    '<script id="glavnoe-strip-dev-link">'
    '(function(){'
      'function strip(){'
        'var anchors=document.querySelectorAll("a");'
        'for(var i=0;i<anchors.length;i++){'
          'var a=anchors[i];'
          'if((a.textContent||"").indexOf("азработали сайт мы")>=0){'
            'var s=document.createElement("span");'
            's.className=a.className;'
            's.style.cssText=a.style.cssText;'
            's.textContent=a.textContent;'
            'a.parentNode.replaceChild(s,a);'
          '}'
        '}'
      '}'
      'var tries=0;'
      'var iv=setInterval(function(){tries++;strip();if(tries>=300){clearInterval(iv);}},200);'
    '})();'
    '</script>'
)

MARK = 'id="glavnoe-strip-dev-link"'


def replacer(m):
    attrs = m.group(1)
    text = m.group(2)
    cls_m = re.search(r'class="([^"]+)"', attrs)
    cls = cls_m.group(1) if cls_m else ''
    return f'<span class="{cls}">{text}</span>'


def main():
    total = 0
    for rel in FILES:
        f = ROOT / rel
        if not f.exists():
            print(f'MISS {rel}')
            continue
        h = f.read_text(encoding='utf-8')
        new_h, n = LINK_RE.subn(replacer, h)
        if MARK not in new_h:
            new_h = new_h.replace('</head>', POST_HYDRATE_SCRIPT + '</head>', 1)
        if new_h != h:
            f.write_text(new_h, encoding='utf-8')
            print(f'OK {rel} ({n} SSR-link(s) stripped + JS-stripper)')
            total += n
        else:
            print(f'SKIP {rel}')
    print(f'Total SSR links stripped: {total}')


if __name__ == '__main__':
    main()
