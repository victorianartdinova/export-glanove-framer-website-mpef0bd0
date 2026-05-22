#!/usr/bin/env python3
"""FIX 5 — Добавить CTA «Все услуги →» под списком продуктов на главной.

UX-аудит: под блоком «(Что придумали)» с 5 продуктами нет CTA на список услуг.
Добавляем тонкую ссылку в стиле «все статьи / все кейсы».

Place: сразу после закрывающего </section> у section[data-framer-name="Archive"]
(там же id="products"). Стиль — минималистичный, под Suisse Intl Regular,
по центру, white-on-black (главная — тёмная тема).

href="/#products" — по ТЗ. Идемпотент: marker data-glavnoe-injected="cta-services".
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'index.html'
MARKER = 'cta-services'

CTA_STYLE = (
    '<style id="glavnoe-cta-services-style" data-fix="cta-services">'
    '.glavnoe-cta-services-wrap{'
    'display:flex;justify-content:center;width:100%;'
    'padding:48px 24px 64px;'
    'background:rgb(0,0,0);'
    '}'
    '.glavnoe-cta-services-link{'
    'font-family:"Suisse Intl Regular",sans-serif;'
    'font-size:18px;letter-spacing:-0.3px;'
    'color:rgb(255,255,255);'
    'text-decoration:none;'
    'border-bottom:1px solid rgba(255,255,255,0.3);'
    'padding-bottom:4px;'
    'transition:border-color 0.2s ease,color 0.2s ease;'
    'display:inline-flex;align-items:center;gap:8px;'
    '}'
    '.glavnoe-cta-services-link:hover{'
    'border-bottom-color:rgb(255,255,255) !important;'
    '}'
    '@media (max-width: 810px){'
    '.glavnoe-cta-services-wrap{padding:32px 20px 48px;}'
    '.glavnoe-cta-services-link{font-size:16px;}'
    '}'
    '</style>'
)

# JS-инжектор. Framer-гидратация стирает или перемещает статические элементы
# вне своего корня. Держим CTA через polling: проверяем не только наличие, но
# и позицию — должна быть directly after section[data-framer-name="Archive"].
CTA_SCRIPT = (
    '<script id="glavnoe-cta-services-inject">'
    '(function(){'
    'function build(){'
      'var w=document.createElement("div");'
      'w.className="glavnoe-cta-services-wrap";'
      'w.setAttribute("data-glavnoe-injected","cta-services");'
      'var a=document.createElement("a");'
      'a.className="glavnoe-cta-services-link";'
      'a.setAttribute("href","/#products");'
      'a.innerHTML="Все услуги <span aria-hidden=\\"true\\">→</span>";'
      'w.appendChild(a);'
      'return w;'
    '}'
    'function ensure(){'
      'var archive=document.querySelector(\'section[data-framer-name="Archive"]\');'
      'if(!archive||!archive.parentNode)return;'
      'var existing=document.querySelector(\'[data-glavnoe-injected="cta-services"]\');'
      'if(existing){'
        # Already in DOM — move CTA to right after Archive if not there
        'if(archive.nextSibling!==existing){'
          'archive.parentNode.insertBefore(existing,archive.nextSibling);'
        '}'
        'return;'
      '}'
      'archive.parentNode.insertBefore(build(),archive.nextSibling);'
    '}'
    'ensure();'
    'var tries=0;'
    'var iv=setInterval(function(){tries++;ensure();if(tries>=300){clearInterval(iv);}},200);'
    '})();'
    '</script>'
)


def main() -> int:
    html = PAGE.read_text(encoding='utf-8')
    # Idempotent: remove any prior CTA HTML/script/style
    if 'id="glavnoe-cta-services-inject"' in html:
        print(f'[skip] already injected in {PAGE}')
        return 0
    # Insert style + script into <head>
    head_close = '</head>'
    new = html.replace(head_close, CTA_STYLE + CTA_SCRIPT + head_close, 1)
    if new == html:
        print('[err] no </head> found', file=sys.stderr)
        return 1
    # Remove any leftover static CTA injection from previous experiments
    new = re.sub(
        r'<div class="glavnoe-cta-services-wrap"[^>]*data-glavnoe-injected="cta-services"[^>]*>.*?</div>\s*(?:<style data-glavnoe-injected-style="cta-services">.*?</style>)?',
        '',
        new,
        flags=re.S,
    )
    PAGE.write_text(new, encoding='utf-8')
    print(f'[ok] injected CTA «Все услуги →» (JS keeper) into {PAGE}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
