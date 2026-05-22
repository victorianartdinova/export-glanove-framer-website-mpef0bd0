#!/usr/bin/env python3
"""FIX 3 (B4): добавить Беляева в отзывы на главной.

Контекст:
- В index.html уже лежит SSR-блок `<div class="glavnoe-mobile-testimonial"
  data-glavnoe-mt="belyaev">` с цитатой Беляева. CSS делает его видимым
  только на mobile (<809.98px).
- Но Framer React-гидратация стирает этот блок (он не в payload). Поэтому
  на mobile он не появляется.

Решение: JS-инжект `glavnoe-belyaev-keeper`, который после гидратации
проверяет наличие блока в DOM и если его нет — вставляет копию в конец
секции `<section data-framer-name="Testimonial">`. Polling в течение 60s.

Iдempotent: marker `id="glavnoe-belyaev-keeper"`.
"""
from pathlib import Path
import re

HTML = Path('/root/framerexport/full-site-export-may21/index.html')

# Extract the existing belyaev block from SSR — это будет template
SCRIPT = (
    '<script id="glavnoe-belyaev-keeper">'
    '(function(){'
      'var TEMPLATE=null;'
      'function snapshot(){'
        'if(TEMPLATE)return;'
        'var el=document.querySelector(\'.glavnoe-mobile-testimonial[data-glavnoe-mt="belyaev"]\');'
        'if(el){TEMPLATE=el.cloneNode(true);}'
      '}'
      'function ensure(){'
        'if(!TEMPLATE)return;'
        'if(document.querySelector(\'.glavnoe-mobile-testimonial[data-glavnoe-mt="belyaev"]\'))return;'
        'var host=document.querySelector(\'section[data-framer-name="Testimonial"]\');'
        'if(!host){host=document.querySelector(\'[data-framer-name="Testimonial"]\');}'
        'if(!host)return;'
        'host.appendChild(TEMPLATE.cloneNode(true));'
      '}'
      'snapshot();'
      'var tries=0;'
      'var iv=setInterval(function(){'
        'tries++;'
        'snapshot();'
        'ensure();'
        'if(tries>=300){clearInterval(iv);}'
      '},200);'
    '})();'
    '</script>'
)

MARK = 'id="glavnoe-belyaev-keeper"'


def main():
    h = HTML.read_text(encoding='utf-8')
    if MARK in h:
        print('Already applied.')
        return
    if 'data-glavnoe-mt="belyaev"' not in h:
        print('ERROR: belyaev SSR block not found, abort')
        return
    h = h.replace('</head>', SCRIPT + '</head>', 1)
    HTML.write_text(h, encoding='utf-8')
    print('Belyaev keeper script injected.')


if __name__ == '__main__':
    main()
