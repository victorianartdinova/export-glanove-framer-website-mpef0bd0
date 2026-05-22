#!/usr/bin/env python3
"""
Fix 4: AAG-кейс — добавить галерею из 3 слайдов Эфира 16.04.

Источник: /root/Эфир 16.04..pdf, слайды 8, 9, 10
  - aag-format.jpg   — слайд 8 (Этап 02 «Придумали формат»)
  - aag-articles.jpg — слайд 9 (Этап 03 «Запустили перформанс» с обложками статей)
  - aag-results.jpg  — слайд 10 (Этап 10 «Результаты», таблица метрик)

Картинки лежат в /assets/cases/aag/.

Изменения:
1. В work/case-aag-promostranicy/index.html, в CASES-объекте функции ensureCaseBody,
   у ключа '/work/case-aag-promostranicy/' добавить поле `gallery: [...]`.
2. Расширить рендер ensureCaseBody так, чтобы после блока «Что делали / Почему сработало»
   рисовать `<div class="glavnoe-case-gallery">` с тремя <img>.
3. CSS-стили галереи: на desktop/tablet — 3 колонки, на mobile (<810px) — 1 колонка,
   border-radius 24px, gap 16px.

Idempotent: маркер 'fix:aag-gallery applied'.
"""
import sys

HTML = '/root/framerexport/full-site-export-may21/work/case-aag-promostranicy/index.html'
MARKER = '/* fix:aag-gallery applied */'

# Локализованный фрагмент для замены — найдём оригинал и заменим расширенной версией.
# Будем менять строку для '/work/case-aag-promostranicy/' блока: подставим gallery после
# why: [...] и закроем объект. Минимально инвазивный подход — заменим конкретную подстроку.

OLD_AAG_BLOCK_TAIL = (
    "'Эмоциональный слой через ностальгию — то, что отличает премиум-продукт от рационального предложения']\n"
    "      },\n"
    "      '/work/case-spb-15mln/':"
)

NEW_AAG_BLOCK_TAIL = (
    "'Эмоциональный слой через ностальгию — то, что отличает премиум-продукт от рационального предложения'],\n"
    "        gallery: ['/assets/cases/aag/aag-format.jpg','/assets/cases/aag/aag-articles.jpg','/assets/cases/aag/aag-results.jpg']\n"
    "      },\n"
    "      '/work/case-spb-15mln/':"
)

# Расширение sec.innerHTML: после блока со ссылкой на продукт, добавим галерею если есть.
# Найдём место сразу после "more.parentNode.insertBefore(sec, more);" и вставим рендер галереи
# в виде второго блока перед перемещением.

OLD_RENDER = (
    "    more.parentNode.insertBefore(sec, more);\n"
    "  }\n"
    "\n"
    "  function isEmpty(li){"
)

NEW_RENDER = (
    "    more.parentNode.insertBefore(sec, more);\n"
    "    if (data.gallery && data.gallery.length){\n"
    "      var gsec = document.createElement('section');\n"
    "      gsec.setAttribute('data-glavnoe-injected', 'case-gallery');\n"
    "      gsec.style.cssText = 'background:rgb(0,0,0);padding:0 24px 96px 24px;color:#fff';\n"
    "      var imgs = data.gallery.map(function(src){\n"
    "        return '<img src=\"'+src+'\" alt=\"\" loading=\"lazy\" style=\"width:100%;height:auto;display:block;border-radius:24px;background:#111\">';\n"
    "      }).join('');\n"
    "      gsec.innerHTML = '<div class=\"glavnoe-case-gallery\" style=\"max-width:1392px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:16px\">'+imgs+'</div>';\n"
    "      more.parentNode.insertBefore(gsec, more);\n"
    "    }\n"
    "  }\n"
    "\n"
    "  function isEmpty(li){"
)

CSS_MOBILE = (
    "<style data-fix=\"aag-gallery\">" + MARKER + "\n"
    "@media (max-width: 810px) {\n"
    "  .glavnoe-case-gallery { grid-template-columns: 1fr !important; }\n"
    "}\n"
    "</style>"
)

def main():
    with open(HTML, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        print('Already applied, skip.')
        return

    if OLD_AAG_BLOCK_TAIL not in content:
        print('ERROR: OLD_AAG_BLOCK_TAIL not found, please inspect manually.', file=sys.stderr)
        sys.exit(2)
    if OLD_RENDER not in content:
        print('ERROR: OLD_RENDER not found, please inspect manually.', file=sys.stderr)
        sys.exit(3)

    content = content.replace(OLD_AAG_BLOCK_TAIL, NEW_AAG_BLOCK_TAIL, 1)
    content = content.replace(OLD_RENDER, NEW_RENDER, 1)

    # Инжект CSS перед </head>
    idx = content.find('</head>')
    if idx == -1:
        print('ERROR: </head> not found', file=sys.stderr)
        sys.exit(4)
    content = content[:idx] + CSS_MOBILE + '\n' + content[idx:]

    with open(HTML, 'w', encoding='utf-8') as f:
        f.write(content)
    print('AAG gallery injected: 3 images (format/articles/results)')

if __name__ == '__main__':
    main()
