#!/usr/bin/env python3
"""
Fix 3: Пересобрать search-index.json с актуальными title / description.

Старый search-index.json содержал 19 элементов от Framer-template "Fuel".
Обходим все реальные index.html и пишем массив:
  [ { "url": "/...", "title": "...", "description": "..." }, ... ]

Idempotent: всегда перезаписывает search-index.json по факту обхода файловой системы.
"""
import os
import re
import json
import html

ROOT = '/root/framerexport/full-site-export-may21'
OUT = os.path.join(ROOT, 'search-index.json')

# Список разрешённых разделов — относительно ROOT
INCLUDE_PATHS = [
    '',                          # /
    'about',
    'contact',
    '404',
    'cases/portfolio',
    # blog index + each blog post
    'blog',
    'blog/strategiya-marketinga-dlya-developera-2026',
    'blog/kak-zastrojshchiku-vesti-telegram-kanal',
    'blog/gde-iskat-klientov-brokeru-2026',
    'blog/telegram-dlya-agentstva-nedvizhimosti-90-zayavok',
    'blog/50-kvallidov-premium-nedvizhimost-telegram-ads',
    'blog/6-sdelok-srednim-chekom-15-mln-telegram-ads',
    # cases (work/*)
    'work/case-aag-promostranicy',
    'work/case-spb-15mln',
    'work/regardis-telegram-ads-premium',
    # products
    'product/avito-ads',
    'product/content-product',
    'product/product-statii',
    'product/product-telegram',
    'product/youtube-product',
]

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(
    r'<meta\s+name="description"\s+content="([^"]*)"', re.IGNORECASE
)

def url_for(rel):
    if rel == '':
        return '/'
    return '/' + rel + '/'

def extract(content):
    title = ''
    desc = ''
    m = TITLE_RE.search(content)
    if m:
        title = html.unescape(m.group(1).strip())
    m = META_DESC_RE.search(content)
    if m:
        desc = html.unescape(m.group(1).strip())
    return title, desc

def main():
    items = []
    for rel in INCLUDE_PATHS:
        path = os.path.join(ROOT, rel, 'index.html')
        if not os.path.exists(path):
            print(f'  skip (missing): {path}')
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        title, desc = extract(content)
        url = url_for(rel)
        items.append({
            'url': url,
            'title': title,
            'description': desc,
        })
        print(f'  {url:60s}  "{title[:60]}"')

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f'\nWrote {len(items)} entries → {OUT}')

if __name__ == '__main__':
    main()
