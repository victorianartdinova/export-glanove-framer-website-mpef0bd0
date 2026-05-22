#!/usr/bin/env python3
"""
fix-mobile-header-internal.py
─────────────────────────────
На статических HTML-страницах (about, contact, blog, blog/<slug>, cases/portfolio)
ШАПКА — <nav class="nav"> со ссылками Главная/Услуги/Кейсы/Результаты/Статьи внутри
.nav__items. На mobile (≤1024px) этот горизонтальный nav переносится и наезжает на
логотип «ГЛАВНОЕ», текст сливается («ГЛАВНОЕКЕЙСЫ»), ломая первый экран на 10+
внутренних страницах.

Что делает скрипт:
1. Находит все index.html со статической <nav class="nav"> (т.е. без Framer-runtime).
2. Идемпотентно инжектит <style id="glavnoe-mobile-header-fix"> + <script id="...-js">
   перед </head>. Если блок уже есть — стирается и записывается заново.

Что инжектится:
- CSS @media (max-width:1024px): скрываем .nav__items, показываем бургер-кнопку.
- JS: ищет nav.nav, добавляет туда <button class="glavnoe-static-burger"
  data-framer-name="Mobile Menu Icon"> с SVG-иконкой бургера. Атрибут
  data-framer-name="Mobile Menu Icon" нужен, чтобы wireBurger() из nav-enhance.js
  автоматически подхватил кнопку и открыл общий drawer (как на главной).

Главная (index.html в корне) НЕ трогается — у неё уже Framer-header со своим бургером.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STYLE_ID = 'glavnoe-mobile-header-fix'
SCRIPT_ID = 'glavnoe-mobile-header-fix-js'

STYLE_BLOCK = (
    '<style id="' + STYLE_ID + '">'
    'nav.nav{position:relative;}'
    'nav.nav .glavnoe-static-burger{'
    'display:none;align-items:center;justify-content:center;'
    'width:40px;height:40px;background:transparent;border:0;'
    'color:#fff;cursor:pointer;padding:0;margin-left:auto;'
    '}'
    'nav.nav .glavnoe-static-burger:hover{color:#ff3b30;}'
    'nav.nav .glavnoe-static-burger svg{width:24px;height:24px;display:block;}'
    '@media (max-width:1024px){'
    'nav.nav .nav__items{display:none !important;}'
    'nav.nav{padding:18px 20px !important;align-items:center !important;}'
    'nav.nav .glavnoe-static-burger{display:flex !important;}'
    '}'
    '</style>'
)

SCRIPT_BLOCK = (
    '<script id="' + SCRIPT_ID + '">'
    '(function(){'
    'function inject(){'
    'var nav=document.querySelector("nav.nav");'
    'if(!nav)return;'
    'if(nav.querySelector(".glavnoe-static-burger"))return;'
    'var btn=document.createElement("button");'
    'btn.type="button";'
    'btn.className="glavnoe-static-burger";'
    'btn.setAttribute("aria-label","Меню");'
    'btn.setAttribute("data-framer-name","Mobile Menu Icon");'
    'btn.innerHTML=\'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>\';'
    'nav.appendChild(btn);'
    '}'
    'if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",inject,{once:true});}else{inject();}'
    '})();'
    '</script>'
)

BLOCK = STYLE_BLOCK + SCRIPT_BLOCK

STRIP_PATTERNS = [
    re.compile(r'<style id="' + re.escape(STYLE_ID) + r'">.*?</style>', re.DOTALL),
    re.compile(r'<script id="' + re.escape(SCRIPT_ID) + r'">.*?</script>', re.DOTALL),
]


def has_static_nav(html: str) -> bool:
    return '<nav class="nav">' in html


def inject(html: str) -> str:
    for pat in STRIP_PATTERNS:
        html = pat.sub('', html)
    if '</head>' not in html:
        return html
    return html.replace('</head>', BLOCK + '</head>', 1)


def main() -> int:
    files = []
    for p in ROOT.rglob('index.html'):
        if '.git' in p.parts or 'node_modules' in p.parts or 'seo-report' in p.parts:
            continue
        rel = p.relative_to(ROOT)
        if str(rel) == 'index.html':
            continue
        files.append(p)

    changed = 0
    skipped = 0
    for path in sorted(files):
        text = path.read_text(encoding='utf-8')
        if not has_static_nav(text):
            skipped += 1
            continue
        new = inject(text)
        if new != text:
            path.write_text(new, encoding='utf-8')
            changed += 1
            print(f'OK   {path.relative_to(ROOT)}')
        else:
            print(f'==   {path.relative_to(ROOT)}')

    print(f'\nChanged: {changed}')
    print(f'Skipped (no <nav class="nav">): {skipped}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
