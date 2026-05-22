#!/usr/bin/env python3
"""
Fix 1: Удалить дубль секции «Что придумали» (Services) на главной.
На index.html две секции с заголовком «Что придумали» подряд:
  1. <section data-framer-name="Services"> — старый Framer-template ("© 2026 / Стратегия, performance...")
  2. <section data-framer-name="Archive"> — актуальная с продуктовыми карточками
Оставляем Archive, удаляем Services.

Idempotent: проверяет marker "remove-duplicate-services applied".
"""
import re
import sys

HTML = '/root/framerexport/full-site-export-may21/index.html'
MARKER = '<!-- fix:remove-duplicate-services applied -->'

def main():
    with open(HTML, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        print('Already applied, skip.')
        return

    # Найти Services <section ... data-framer-name="Services" ...>
    # и удалить вместе с его </section>
    m = re.search(r'<section class="framer-mdkm87"\s+data-framer-name="Services"[^>]*>', content)
    if not m:
        print('ERROR: Services section opener not found', file=sys.stderr)
        sys.exit(1)

    start = m.start()
    # Найти соответствующий </section> с учётом вложенности
    i = start
    depth = 0
    end = None
    while i < len(content):
        if content[i] == '<':
            # Проверим <section
            if content[i:i+8] == '<section' and (content[i+8] == ' ' or content[i+8] == '>'):
                depth += 1
                # пропустим до >
                j = content.find('>', i)
                if j == -1: break
                i = j + 1
                continue
            if content[i:i+10] == '</section>':
                depth -= 1
                i += 10
                if depth == 0:
                    end = i
                    break
                continue
        i += 1

    if end is None:
        print('ERROR: matching </section> not found', file=sys.stderr)
        sys.exit(1)

    print(f'Removing Services section: bytes {start}-{end} (length {end-start})')

    # Удаляем + добавляем маркер
    new_content = content[:start] + MARKER + content[end:]

    with open(HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # Verify only one "Что придумали" remains
    remaining = new_content.count('Что придумали')
    print(f'"Что придумали" occurrences after fix: {remaining}')
    print('Done.')

if __name__ == '__main__':
    main()
