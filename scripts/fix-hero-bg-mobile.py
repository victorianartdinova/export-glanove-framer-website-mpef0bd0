#!/usr/bin/env python3
"""
FIX 7 — Hero фон не загружается на mobile, виден alt="Women in Orange BG" на белом.

Корень: hero <img> в Framer JS-чанке ссылается на
https://framerusercontent.com/images/PNql8FwjCxLPNXeuzrGEMxR2o4.webp
который возвращает 404 от CloudFront. Локально файл существует:
/assets/framer/images/PNql8FwjCxLPNXeuzrGEMxR2o4.webp (HTTP 200).

Что делает скрипт:
1. В JS-чанке V6MP5xCojziNbtxidWz9fUuPNsqKAdC__dr2Zg5uIS8.DeEx7wm8.mjs
   подменяет URL https://framerusercontent.com/images/PNql8... на
   локальный /assets/framer/images/PNql8FwjCxLPNXeuzrGEMxR2o4.webp.
2. На случай если другие image-url-ы тоже не подгрузятся — инжектит в
   index.html <style id="glavnoe-hero-bg-fallback"> с фоном #000 на
   родителе hero-картинки, чтобы alt-текст «Women in Orange BG» не
   читался белым по белому.

Идемпотентность:
- маркер /* fix:hero-bg-mobile applied */ в JS и в HTML
"""
from pathlib import Path

ROOT = Path('/root/framerexport/full-site-export-may21')
JS = ROOT / 'assets/framer/sites/1OcdQgezFomPwA9UGakYyz/V6MP5xCojziNbtxidWz9fUuPNsqKAdC__dr2Zg5uIS8.DeEx7wm8.mjs'
HTML = ROOT / 'index.html'

JS_MARKER = '/* fix:hero-bg-mobile applied */'
HTML_MARKER = '<!-- fix:hero-bg-mobile applied -->'

EXTERNAL_PREFIX = 'https://framerusercontent.com/images/PNql8FwjCxLPNXeuzrGEMxR2o4.webp'
LOCAL_PATH = '/assets/framer/images/PNql8FwjCxLPNXeuzrGEMxR2o4.webp'

HTML_STYLE = (
    '<style id="glavnoe-hero-bg-fallback">' + HTML_MARKER + '\n'
    # Hero <section data-framer-name="Hero"> и его BG-картинка-wrapper.
    # Если изображение не подгрузилось — фон чёрный, alt-текст невидим.
    'section[data-framer-name="Hero"]{background-color:#000 !important}\n'
    'section[data-framer-name="Hero"] [data-framer-background-image-wrapper]{background-color:#000 !important}\n'
    'section[data-framer-name="Hero"] img[alt*="Women in Orange"]{color:#000 !important;background:#000 !important}\n'
    '</style>'
)


def patch_js():
    if not JS.exists():
        print('WARN: JS chunk not found:', JS)
        return False
    src = JS.read_text(encoding='utf-8')
    if JS_MARKER in src:
        print('JS already patched.')
        return False
    # Replace all variants — main src + srcset variants
    # The URL appears as `https://framerusercontent.com/images/PNql8...` followed by params
    # e.g. ?width=2848&height=1600 or ?scale-down-to=...
    count = src.count('framerusercontent.com/images/PNql8FwjCxLPNXeuzrGEMxR2o4.webp')
    new = src.replace(
        'https://framerusercontent.com/images/PNql8FwjCxLPNXeuzrGEMxR2o4.webp',
        LOCAL_PATH
    )
    new = JS_MARKER + '\n' + new
    JS.write_text(new, encoding='utf-8')
    print(f'JS: replaced {count} URL occurrences')
    return True


def patch_html():
    src = HTML.read_text(encoding='utf-8')
    if HTML_MARKER in src:
        print('HTML already has hero-bg fallback.')
        return False
    idx = src.find('</head>')
    if idx == -1:
        print('ERROR: </head> not found in index.html')
        return False
    new = src[:idx] + HTML_STYLE + '\n' + src[idx:]
    HTML.write_text(new, encoding='utf-8')
    print('HTML: hero-bg fallback injected.')
    return True


if __name__ == '__main__':
    patch_js()
    patch_html()
