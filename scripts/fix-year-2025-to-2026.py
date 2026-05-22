#!/usr/bin/env python3
"""
FIX 10 (часть) — Унификация года © 2025 → © 2026.

Аудит: «© 2025» в нижнем cases-блоке при «© 2026» сверху и снизу —
разный год в разных блоках сайта.

Проверка: все вхождения «© 2025» в JS-чанках Framer лежат строго в
copyright/year-стампах (defaultValue/children/data-framer-name=Year),
никаких ссылок на 2025-кейсы.

Что делает скрипт:
1. По всем JS-чанкам в assets/framer/sites/.../*.mjs делает замену
   '© 2025' → '© 2026'.
2. Пропускает уже обработанные файлы (проверка: если '© 2025' нет —
   ничего не пишет).

Маркер: в начале файла добавляется /* fix:year-2026 applied */ ровно
один раз.
"""
from pathlib import Path

ROOT = Path('/root/framerexport/full-site-export-may21')
JS_DIR = ROOT / 'assets/framer/sites/1OcdQgezFomPwA9UGakYyz'
MARKER = '/* fix:year-2026 applied */'


def main():
    if not JS_DIR.exists():
        raise SystemExit('JS dir not found: ' + str(JS_DIR))

    total_replacements = 0
    files_changed = 0
    for f in JS_DIR.iterdir():
        if not f.name.endswith('.mjs'):
            continue
        try:
            text = f.read_text(encoding='utf-8')
        except Exception as e:
            print(f'skip {f.name}: {e}')
            continue
        if '© 2025' not in text:
            continue
        if MARKER in text:
            continue
        cnt = text.count('© 2025')
        new = text.replace('© 2025', '© 2026')
        new = MARKER + '\n' + new
        f.write_text(new, encoding='utf-8')
        total_replacements += cnt
        files_changed += 1
        print(f'{f.name}: replaced {cnt}')

    print(f'\nFiles changed: {files_changed}, total replacements: {total_replacements}')


if __name__ == '__main__':
    main()
