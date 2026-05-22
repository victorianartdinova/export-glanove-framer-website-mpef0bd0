#!/usr/bin/env python3
"""
FIX 8 — На mobile H1 «В каждом хорошем проекте заложены смыслы»
рендерится двумя слоями с потенциальным сдвигом (наслоение).

Причина: Framer animated text компонент создаёт 2 копии текста:
- aria-hidden="true" с position:absolute (placeholder для анимации)
- основная видимая копия

В норме aria-hidden копия скрыта через `pointer-events:none + opacity 0`,
но иногда (особенно на mobile при медленной hydration) первая копия
становится видимой на короткое время — пользователь видит наложение.

Что делает скрипт:
Инжектит в index.html <style id="glavnoe-h1-double-fix">. CSS на @media
(max-width:1024px) ставит aria-hidden="true" текстовым копиям
opacity:0 !important, чтобы исключить любое визуальное наложение.

Идемпотентность: HTML_MARKER в файле.
"""
from pathlib import Path

HTML = Path('/root/framerexport/full-site-export-may21/index.html')
HTML_MARKER = '<!-- fix:h1-double-mobile applied -->'

STYLE = (
    '<style id="glavnoe-h1-double-fix">' + HTML_MARKER + '\n'
    '@media (max-width:1024px){\n'
    # aria-hidden text placeholders внутри Framer animated text:
    # они с position:absolute и visibility:visible !important — но
    # должны быть невидимы для глаза.
    '  div[aria-hidden="true"][style*="position: absolute"][style*="visibility: visible"]{\n'
    '    opacity:0 !important;\n'
    '  }\n'
    '}\n'
    '</style>'
)


def main():
    src = HTML.read_text(encoding='utf-8')
    if HTML_MARKER in src:
        print('Already applied.')
        return
    idx = src.find('</head>')
    if idx == -1:
        raise SystemExit('</head> not found')
    src = src[:idx] + STYLE + '\n' + src[idx:]
    HTML.write_text(src, encoding='utf-8')
    print('Patched index.html with marker', HTML_MARKER)


if __name__ == '__main__':
    main()
