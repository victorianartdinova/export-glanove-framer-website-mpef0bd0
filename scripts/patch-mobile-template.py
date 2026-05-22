#!/usr/bin/env python3
"""Patch the REPLACEMENTS array inside each product HTML to also catch the
Framer 'Industries' template default + '30+' big number that appear on mobile
variants. Extends the lifetime of the per-page MutationObserver too.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# slug → (big_number, big_label)
PRODUCTS = {
    'avito-ads':        ('1000+', 'Стоимость целевого обращения на недвижимость бизнес и премиум-класса'),
    'content-product':  ('500+',  'запусков контент-систем для застройщиков и агентств недвижимости'),
    'product-statii':   ('6000+', 'обращений с ПромоСтраниц Яндекса по цене на 32% ниже контекста'),
    'product-telegram': ('800+',  'заявок из Telegram Ads с CPL в 2 раза ниже рынка'),
    'youtube-product':  ('50+',   'личных брендов основателей запущенных за 1.5 недели'),
}

TEMPLATE_PHRASES_FULL = [
    'Industries → our designs have supported businesses, adapting to unique needs and challenges',
    'our designs have supported businesses, adapting to unique needs and challenges',
    'Industries → our designs',
    'adapting to unique needs and challenges',
]

def patch(slug: str, html: str, num: str, label: str) -> str:
    # 1. Append entries to REPLACEMENTS = [...] array
    new_entries = []
    new_entries.append(f'["30+", "{num}"]')
    for phrase in TEMPLATE_PHRASES_FULL:
        safe = phrase.replace('\\', '\\\\').replace('"', '\\"')
        safe_label = label.replace('\\', '\\\\').replace('"', '\\"')
        new_entries.append(f'["{safe}", "{safe_label}"]')

    extra_block = ', ' + ', '.join(new_entries)

    # Insert before ']];' at end of REPLACEMENTS = [...]
    # The REPLACEMENTS line ends with ]];  — we add before the final ]];
    sentinel = 'data-glavnoe-mobile-template-patch'
    if sentinel in html:
        # Already patched once — remove old patch by stripping marker line and re-apply
        html = re.sub(r'/\* ' + sentinel + r' \*/.*?/\* end-' + sentinel + r' \*/', '', html, flags=re.DOTALL)

    pattern = re.compile(r'(var REPLACEMENTS\s*=\s*\[\[)(.*?)(\]\];)', re.DOTALL)
    m = pattern.search(html)
    if not m:
        return html
    prefix = m.group(1)
    body = m.group(2)
    suffix = m.group(3)
    annotated = f'/* {sentinel} */ {extra_block.lstrip(",").strip()} /* end-{sentinel} */'
    new_body = body + ', ' + annotated.lstrip(', ')
    new_html = html[:m.start()] + prefix + new_body + suffix + html[m.end():]

    # 2. Extend MO lifetime to 30s
    new_html = new_html.replace(
        'observer.disconnect();}, 6000);',
        'observer.disconnect();}, 30000);'
    )
    new_html = new_html.replace(
        'observer.disconnect();}, 6e3);',
        'observer.disconnect();}, 30000);'
    )
    return new_html


def main():
    n = 0
    for slug, (num, label) in PRODUCTS.items():
        path = ROOT / 'product' / slug / 'index.html'
        if not path.exists():
            print(f'MISS {path}')
            continue
        html = path.read_text(encoding='utf-8')
        new = patch(slug, html, num, label)
        if new != html:
            path.write_text(new, encoding='utf-8')
            n += 1
            print(f'OK   {slug}')
        else:
            print(f'==   {slug}')
    print(f'Patched: {n}/{len(PRODUCTS)}')

if __name__ == '__main__':
    sys.exit(main())
