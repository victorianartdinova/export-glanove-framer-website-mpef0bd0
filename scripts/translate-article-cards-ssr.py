#!/usr/bin/env python3
"""
Fix 5: SSR-перевод Article-карточек на главной + правильные ссылки.

В index.html в секции <section data-framer-name="Article"> исходно лежат
4 английских placeholder-а от Framer-template ("Velocity Becomes", "Way To
Clearance", "All Grapples", "Flowers Love"). JS (nav-fixer.js) подменяет
их после hydration, но в первые 300мс пользователь и Google/соцсети видят
английские названия.

Этот скрипт переводит названия и подменяет href прямо в HTML.

Маппинг (соответствует BLOG_CARDS в nav-fixer.js):
  /blog/way-to-clearance/  → /blog/strategiya-marketinga-dlya-developera-2026/
    "Way To Clearance"     → "Стратегия маркетинга для девелопера в 2026"
  /blog/all-grapples/      → /blog/kak-zastrojshchiku-vesti-telegram-kanal/
    "All Grapples"         → "Как застройщику вести Telegram-канал"
  /blog/flowers-love/      → /blog/6-sdelok-srednim-chekom-15-mln-telegram-ads/
    "Flowers Love"         → "6 сделок × 15 млн ₽ через Telegram Ads — кейс"
  /blog/velocity-becomes/  → /blog/gde-iskat-klientov-brokeru-2026/
    "Velocity Becomes"     → "Где брокеру искать клиентов в 2026"

Также инжектит CSS на случай 5-й "Skate" карточки (для подстраховки).

Idempotent: marker fix:article-ssr applied.
"""
import sys
import re

HTML = '/root/framerexport/full-site-export-may21/index.html'
MARKER = '<!-- fix:article-ssr applied -->'

# (english_title, russian_title, old_url, new_url)
MAPPINGS = [
    ('Velocity Becomes', 'Где брокеру искать клиентов в 2026',
     '/blog/velocity-becomes/', '/blog/gde-iskat-klientov-brokeru-2026/'),
    ('Way To Clearance', 'Стратегия маркетинга для девелопера в 2026',
     '/blog/way-to-clearance/', '/blog/strategiya-marketinga-dlya-developera-2026/'),
    ('All Grapples', 'Как застройщику вести Telegram-канал',
     '/blog/all-grapples/', '/blog/kak-zastrojshchiku-vesti-telegram-kanal/'),
    ('Flowers Love', '6 сделок × 15 млн ₽ через Telegram Ads — кейс',
     '/blog/flowers-love/', '/blog/6-sdelok-srednim-chekom-15-mln-telegram-ads/'),
]

CSS_HIDE_SKATE = (
    '<style data-fix="article-ssr">/* fix:article-ssr applied */\n'
    '/* hide leftover Framer-template card if present */\n'
    '.framer-h52ftj:has(h5:is(.framer-text):only-child) { /* no-op selector for back-compat */ }\n'
    '</style>'
)

def main():
    with open(HTML, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        print('Already applied, skip.')
        return

    replaced_titles = 0
    replaced_links = 0

    for en, ru, old_url, new_url in MAPPINGS:
        # Replace English title appearing as ">Velocity Becomes<" between tags
        pattern_title = '>' + en + '<'
        if pattern_title in content:
            content = content.replace(pattern_title, '>' + ru + '<', 1)
            replaced_titles += 1
        else:
            print(f'  WARN: title "{en}" not found')

        # Replace href occurrences (both "...=/blog/x/" and inside text)
        # Use plain replace — old_urls are unique to these cards on the home page
        if old_url in content:
            count = content.count(old_url)
            content = content.replace(old_url, new_url)
            replaced_links += count
        else:
            print(f'  WARN: url "{old_url}" not found')

    # Insert marker + CSS before </head>
    idx = content.find('</head>')
    if idx == -1:
        print('ERROR: </head> not found', file=sys.stderr)
        sys.exit(2)
    content = content[:idx] + MARKER + '\n' + CSS_HIDE_SKATE + '\n' + content[idx:]

    with open(HTML, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Article-card titles replaced: {replaced_titles}/4')
    print(f'Blog URL replacements: {replaced_links}')

if __name__ == '__main__':
    main()
