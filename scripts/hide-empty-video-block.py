#!/usr/bin/env python3
"""
Fix 2: Скрыть пустой Video-блок на главной (между Hero и Archive).

После применения Fix 1 (remove-duplicate-services.py) сама секция Video уже
не присутствует на странице — она была внутри удалённого Services-блока.
Тем не менее, для подстраховки на случай повторного экспорта из Framer,
этот скрипт инжектит CSS-правило, которое скроет пустую Video-секцию,
если она появится.

CSS прячет:
  - <section data-framer-name="Video">
  - элемент, в котором осталась пустая ссылка на video файл без visual окружения

Idempotent: marker fix:hide-empty-video.
"""
import sys

HTML = '/root/framerexport/full-site-export-may21/index.html'
MARKER = '/* fix:hide-empty-video applied */'
CSS_BLOCK = f'''<style data-fix="hide-empty-video">{MARKER}
[data-framer-name="Video"] {{ display: none !important; }}
</style>'''

def main():
    with open(HTML, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        print('Already applied, skip.')
        return

    # Вставляем в <head> перед </head>
    idx = content.find('</head>')
    if idx == -1:
        print('ERROR: </head> not found', file=sys.stderr)
        sys.exit(1)

    new_content = content[:idx] + CSS_BLOCK + '\n' + content[idx:]

    with open(HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print('CSS injected: [data-framer-name="Video"] { display: none !important; }')

if __name__ == '__main__':
    main()
