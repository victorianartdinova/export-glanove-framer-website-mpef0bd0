#!/usr/bin/env python3
"""
FIX мелкий — Футер: «■ Политика кон-ти ■ Разработали сайт мы:)»

Что в аудите:
- «Политика кон-ти» — текст обрезан, должно быть «Политика
  конфиденциальности».
- «■» — оранжевые квадраты-плейсхолдеры (на самом деле это Divider Dot
  с brand-orange backgroundColor rgb(252,102,48)). На mobile в узкую
  колонку они выглядят как обрезанные иконки.

Что делает скрипт:
1. В script_main.B9JEDTsv.mjs (Framer Footer-компонент) меняет
   «Политика кон-ти» на «Политика конфиденциальности» в двух местах.
2. В index.html инжектит <style id="glavnoe-footer-fix"> с правилами:
   - на @media (max-width:600px) — Divider Dot 01/02 скрываются (на
     узком экране их visual смысл теряется, без них чище).
   - «Политика конфиденциальности» получает word-break: keep-all и
     min-width: 0 чтобы корректно переноситься.

Идемпотентность: маркер /* fix:footer-policy applied */
"""
from pathlib import Path

ROOT = Path('/root/framerexport/full-site-export-may21')
JS = ROOT / 'assets/framer/sites/1OcdQgezFomPwA9UGakYyz/script_main.B9JEDTsv.mjs'
HTML = ROOT / 'index.html'

JS_MARKER = '/* fix:footer-policy applied */'
HTML_MARKER = '/* fix:footer-policy applied */'

OLD_TEXT = 'Политика кон-ти'
NEW_TEXT = 'Политика конфиденциальности'

STYLE = (
    '<style id="glavnoe-footer-fix">/* fix:footer-policy applied */\n'
    '@media (max-width:600px){\n'
    # Hide orange divider squares on narrow mobile
    '  [data-framer-name="Divider Dot 01"],\n'
    '  [data-framer-name="Divider Dot 02"]{\n'
    '    display:none !important;\n'
    '  }\n'
    # Make privacy policy text not break on hyphen
    '  [data-framer-name="Privacy Policy Link"] a,\n'
    '  [data-framer-name="Credit Text – Designed by Future Things"] a,\n'
    '  [data-framer-name="Credit Text – Designed by Future Things"] span{\n'
    '    word-break:normal !important;\n'
    '    overflow-wrap:anywhere !important;\n'
    '  }\n'
    '}\n'
    '</style>'
)


def patch_js():
    if not JS.exists():
        print('WARN: JS not found')
        return False
    src = JS.read_text(encoding='utf-8')
    if JS_MARKER in src:
        print('JS already patched.')
        return False
    cnt = src.count(OLD_TEXT)
    if cnt == 0:
        print('No "Политика кон-ти" found.')
        return False
    new = src.replace(OLD_TEXT, NEW_TEXT)
    new = JS_MARKER + '\n' + new
    JS.write_text(new, encoding='utf-8')
    print(f'JS: replaced {cnt} occurrences of "{OLD_TEXT}" → "{NEW_TEXT}"')
    return True


def patch_html():
    src = HTML.read_text(encoding='utf-8')
    if HTML_MARKER in src:
        print('HTML already has footer-policy style.')
        return False
    idx = src.find('</head>')
    if idx == -1:
        raise SystemExit('</head> not found')
    src = src[:idx] + STYLE + '\n' + src[idx:]
    HTML.write_text(src, encoding='utf-8')
    print('HTML: footer-policy style injected.')
    return True


if __name__ == '__main__':
    patch_js()
    patch_html()
