#!/usr/bin/env python3
"""Mobile Tablet/Phone карточки результатов не подменяются REPLACEMENTS
(Framer перерисовывает их после disconnect MutationObserver-а).
Этот скрипт держит подмену через polling setInterval каждые 250ms в течение 60 sec.

Также заменяет 2 фото-иконки (Avito jпг с машиной/молотком) на SVG иконки
по теме каждого продукта."""
from pathlib import Path

ROOT = Path('/root/framerexport/full-site-export-may21')

# Для каждой страницы: правильные значения + 2 иконки
PAGES = {
    'product-telegram': {
        'number': '800+',
        'text': 'заявок из Telegram Ads с CPL в 2 раза ниже рынка',
        # SVG icons: trend-up + send (Telegram-like)
        'icon1': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23F9452D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
        'icon2': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23F9452D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>'
    },
    'content-product': {
        'number': '500+',
        'text': 'запусков контент-систем для застройщиков и агентств недвижимости',
        # bar-chart + sparkles
        'icon1': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23F9452D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        'icon2': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23F9452D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l1.9 5.8L20 11l-5.5 2.5L12 21l-2.5-7.5L4 11l5.8-1.9z"/></svg>'
    },
    'product-statii': {
        'number': '6000+',
        'text': 'обращений с ПромоСтраниц Яндекса по цене на 32% ниже контекста',
        # newspaper + percent
        'icon1': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23F9452D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 22h16a2 2 0 002-2V4a2 2 0 00-2-2H8a2 2 0 00-2 2v16a2 2 0 01-2 2zm0 0a2 2 0 01-2-2V6h4"/><path d="M18 14h-8M15 18h-5M10 6h8v4h-8z"/></svg>',
        'icon2': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23F9452D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>'
    },
    'youtube-product': {
        'number': '1M+',
        'text': 'совокупных охватов YouTube-каналов экспертов в недвижимости',
        # play-circle + users
        'icon1': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23F9452D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg>',
        'icon2': 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23F9452D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>'
    }
}


def script_for(slug):
    cfg = PAGES[slug]
    return (
      f'<script id="glavnoe-mobile-card-fix">'
      '(function(){'
        f'var NUMBER={cfg["number"]!r};'
        f'var TEXT={cfg["text"]!r};'
        f'var ICON1={cfg["icon1"]!r};'
        f'var ICON2={cfg["icon2"]!r};'
        'function patch(){'
          # Replace "30+" or any small N+ in Tablet/Phone variant cards
          'var variants=document.querySelectorAll(\'[data-framer-name="Tablet"], [data-framer-name="Phone"]\');'
          'for(var i=0;i<variants.length;i++){'
            'var v=variants[i];'
            # h2 with N+ → NUMBER
            'var hs=v.querySelectorAll("h2");'
            'for(var j=0;j<hs.length;j++){'
              'var t=hs[j].textContent.trim();'
              'if(/^[0-9]+\\+$/.test(t)&&t!==NUMBER){'
                'hs[j].innerHTML=NUMBER;'
              '}'
            '}'
            # Industries text → TEXT (find any element with English template)
            'var ps=v.querySelectorAll("p,span,div");'
            'for(var k=0;k<ps.length;k++){'
              'var el=ps[k];'
              'if(el.children.length>0)continue;'
              'var tt=el.textContent.trim();'
              'if(/Industries|our designs|adapting to unique/i.test(tt)){'
                'el.textContent=TEXT;'
              '}'
            '}'
            # Replace 2 images with SVG icons
            'var imgs=v.querySelectorAll("img");'
            'for(var m=0;m<imgs.length;m++){'
              'var img=imgs[m];'
              'if(img.src.indexOf("framerusercontent")>=0||img.alt==="image"){'
                'if(m===0)img.src=ICON1;'
                'else img.src=ICON2;'
                'img.srcset="";'
                'img.style.objectFit="contain";'
                'img.style.padding="20px";'
                'img.style.background="rgba(255,255,255,0.05)";'
                'img.style.borderRadius="12px";'
              '}'
            '}'
          '}'
        '}'
        'var tries=0;'
        'var iv=setInterval(function(){'
          'tries++;'
          'patch();'
          'if(tries>=300){clearInterval(iv);}'
        '},200);'
      '})();'
      '</script>'
    )

MARK = 'id="glavnoe-mobile-card-fix"'

for slug, cfg in PAGES.items():
    f = ROOT / 'product' / slug / 'index.html'
    h = f.read_text(encoding='utf-8')
    if MARK in h:
        print(f'SKIP {slug}')
        continue
    h = h.replace('</head>', script_for(slug) + '</head>', 1)
    f.write_text(h, encoding='utf-8')
    print(f'OK {slug}')
