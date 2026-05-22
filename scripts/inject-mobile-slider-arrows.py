#!/usr/bin/env python3
"""FIX 5 (A5): добавить стрелки переключения для мобильного слайдера тарифов.

На /product/product-telegram/ (и других продуктовых страницах) мобильный
scroll-snap слайдер тарифов виден только через swipe — нет визуальных
prev/next кнопок. Вика просит добавить ←/→.

Решение:
- CSS: позиционируем 2 кнопки prev/next по бокам секции тарифов на
  мобильных (<1100px). 44×44px, border-radius 100%. Фон контрастный к
  фону секции.
- JS: после загрузки находим каждый `[data-tariff-grid]` внутри
  `[data-glavnoe-tariffs="1"]`, инжектим обёртку с кнопками, обработчики
  scrollBy(±cardWidth+gap).

Применяется ко всем 4 страницам с тарифами:
content-product, product-statii, product-telegram, youtube-product.
"""
from pathlib import Path

ROOT = Path('/root/framerexport/full-site-export-may21')
PAGES = ['content-product', 'product-statii', 'product-telegram', 'youtube-product']

INJECT = (
    '<style id="glavnoe-tariff-mobile-arrows-style">'
    '@media (max-width:1100px){'
      '[data-glavnoe-tariffs="1"] [data-tariff-grid]{position:relative;}'
      '.glavnoe-arrow-row{display:flex;justify-content:center;gap:16px;padding:8px 20px 0 20px;}'
      '.glavnoe-arrow-row button{'
        'width:44px;height:44px;border-radius:50%;border:none;cursor:pointer;'
        'display:inline-flex;align-items:center;justify-content:center;'
        'background:#fff;color:#000;'
        'box-shadow:0 2px 8px rgba(0,0,0,0.18);'
        'transition:transform 0.15s ease;'
      '}'
      '.glavnoe-arrow-row button:active{transform:scale(0.92);}'
      '.glavnoe-arrow-row button[disabled]{opacity:0.35;cursor:default;}'
      '.glavnoe-arrow-row button svg{width:22px;height:22px;display:block;}'
      # Dark tier-style sections (Telegram tariff has dark bg): white bg button is fine
      # But on white-bg sections, swap to black button
      '[data-glavnoe-tariffs="1"][data-tariffs-theme="light"] .glavnoe-arrow-row button{'
        'background:#000;color:#fff;'
      '}'
    '}'
    '@media (min-width:1101px){'
      '.glavnoe-arrow-row{display:none!important;}'
    '}'
    '</style>'
    '<script id="glavnoe-tariff-mobile-arrows">'
    '(function(){'
      'var ARROW_LEFT=\'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>\';'
      'var ARROW_RIGHT=\'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>\';'
      'function step(grid){'
        'var card=grid.querySelector("article[data-tier]");'
        'if(!card)return 320;'
        'var r=card.getBoundingClientRect();'
        'return r.width+12;'
      '}'
      'function update(grid,prev,next){'
        'var max=grid.scrollWidth-grid.clientWidth-2;'
        'prev.disabled=grid.scrollLeft<=2;'
        'next.disabled=grid.scrollLeft>=max;'
      '}'
      'function init(grid){'
        'if(grid.dataset.glavnoeArrows==="1")return;'
        'grid.dataset.glavnoeArrows="1";'
        'var row=document.createElement("div");'
        'row.className="glavnoe-arrow-row";'
        'var prev=document.createElement("button");'
        'prev.setAttribute("aria-label","Предыдущий тариф");'
        'prev.innerHTML=ARROW_LEFT;'
        'var next=document.createElement("button");'
        'next.setAttribute("aria-label","Следующий тариф");'
        'next.innerHTML=ARROW_RIGHT;'
        'row.appendChild(prev);'
        'row.appendChild(next);'
        'grid.parentNode.insertBefore(row,grid.nextSibling);'
        'function move(dir){'
          'grid.scrollBy({left:dir*step(grid),behavior:"smooth"});'
        '}'
        'prev.addEventListener("click",function(){move(-1);});'
        'next.addEventListener("click",function(){move(1);});'
        'grid.addEventListener("scroll",function(){update(grid,prev,next);},{passive:true});'
        'window.addEventListener("resize",function(){update(grid,prev,next);});'
        'update(grid,prev,next);'
      '}'
      'function patch(){'
        'if(window.innerWidth>1100)return;'
        'var grids=document.querySelectorAll(\'[data-glavnoe-tariffs="1"] [data-tariff-grid]\');'
        'for(var i=0;i<grids.length;i++){init(grids[i]);}'
      '}'
      'var tries=0;'
      'var iv=setInterval(function(){tries++;patch();if(tries>=200){clearInterval(iv);}},250);'
      'window.addEventListener("resize",patch);'
    '})();'
    '</script>'
)

MARK = 'id="glavnoe-tariff-mobile-arrows"'


def main():
    for slug in PAGES:
        f = ROOT / 'product' / slug / 'index.html'
        if not f.exists():
            print(f'MISS {slug}')
            continue
        h = f.read_text(encoding='utf-8')
        if MARK in h:
            print(f'SKIP {slug}')
            continue
        new = h.replace('</head>', INJECT + '</head>', 1)
        if new == h:
            print(f'FAIL {slug}')
            continue
        f.write_text(new, encoding='utf-8')
        print(f'OK {slug}')


if __name__ == '__main__':
    main()
