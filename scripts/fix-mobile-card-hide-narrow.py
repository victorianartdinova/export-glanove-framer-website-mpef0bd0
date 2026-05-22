#!/usr/bin/env python3
"""FIX 1 (A6): заменить слишком широкое скрытие variants на узкое.

Прошлый коммит 3d0391c скрывал [data-framer-name="Tablet"|"Phone"|"Desktop"]
полностью на mobile/tablet (<1100px), чтобы убрать английский Industries-
эталон. Это перебор: теперь на mobile нет ВООБЩЕ блока с цифрами.

Новый подход:
1. Удаляем CSS-инжект `glavnoe-mobile-card-hide`.
2. Добавляем JS-инжект `glavnoe-mobile-card-hide-narrow`, который проходит
   по [data-framer-name="Tablet"], [data-framer-name="Phone"],
   [data-framer-name="Desktop"] и скрывает ТОЛЬКО те, в которых
   ещё остался английский шаблон ("Industries" / "our designs" /
   "adapting to unique") после работы patcher-а.
3. Стрелки (Arrow Red/White/Image) тоже скрываем, но только если ВСЕ
   variants скрыты — иначе оставляем.
"""
from pathlib import Path
import re

ROOT = Path('/root/framerexport/full-site-export-may21')
SLUGS = ['product-telegram', 'content-product', 'product-statii', 'youtube-product']

OLD_STYLE_RE = re.compile(
    r'<style id="glavnoe-mobile-card-hide">.*?</style>',
    re.DOTALL,
)

NEW_INJECT = (
    '<script id="glavnoe-mobile-card-hide-narrow">'
    '(function(){'
      'function isEnglishTemplate(el){'
        'var t=(el.textContent||"").toLowerCase();'
        'return t.indexOf("industries")>=0||t.indexOf("our designs")>=0||t.indexOf("adapting to unique")>=0;'
      '}'
      'function isEmpty(el){'
        'return (el.textContent||"").trim().length<3;'
      '}'
      'function patch(){'
        'var vs=document.querySelectorAll(\'[data-framer-name="Tablet"], [data-framer-name="Phone"], [data-framer-name="Desktop"]\');'
        'for(var i=0;i<vs.length;i++){'
          'var v=vs[i];'
          'if(window.innerWidth>1100){v.style.display="";continue;}'
          'if(isEnglishTemplate(v)||isEmpty(v)){'
            'v.style.display="none";'
          '}else{'
            'v.style.display="";'
          '}'
        '}'
      '}'
      'var tries=0;'
      'var iv=setInterval(function(){tries++;patch();if(tries>=300){clearInterval(iv);}},200);'
      'window.addEventListener("resize",patch);'
    '})();'
    '</script>'
)

MARK = 'id="glavnoe-mobile-card-hide-narrow"'

for slug in SLUGS:
    f = ROOT / 'product' / slug / 'index.html'
    h = f.read_text(encoding='utf-8')
    # Remove old broad-hide style
    new_h, n = OLD_STYLE_RE.subn('', h)
    # Add new narrow JS if not present
    if MARK not in new_h:
        new_h = new_h.replace('</head>', NEW_INJECT + '</head>', 1)
    if new_h != h:
        f.write_text(new_h, encoding='utf-8')
        print(f'OK {slug} (removed {n} old style block(s))')
    else:
        print(f'SKIP {slug}')
