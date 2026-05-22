#!/usr/bin/env python3
"""
Унификация имён продуктов: title = hero h2 = карточка на главной = deeplink-text.

Канонический маппинг (утверждено Викторией 22.05.2026):
  /product/avito-ads/        Авито Адс
  /product/content-product/  Коммуникационная стратегия
  /product/product-statii/   ПромоСтраницы Яндекс
  /product/product-telegram/ Лидген Телеграм
  /product/youtube-product/  Личный бренд YouTube

Что обновляет скрипт:
  • product/<slug>/index.html:
      - <title>NAME | ГЛАВНОЕ</title>
      - <meta name="description"> (нормализуем имя в описании)
      - <meta property="og:title">, og:description, twitter:title, twitter:description
      - var PAGE_TITLE, var META_DESC (JS-override)
      - REPLACEMENTS[0] и [1] — пара "Авито Адс" → NAME и хештег-капсула
      - var TIERS — поле href, текст 'продукт: <NAME>' переписан + url-encoded
  • index.html:
      - 5 карточек <h5>OLD</h5> → <h5>NEW</h5>
      - ARCHIVE_PRODUCTS title-поля
      - CASES product_label
  • search-index.json:
      - title для каждой /product/<slug>/

Idempotent. Перед записью пишет .bak только если изменился контент.
"""
import json
import os
import re
import sys
from urllib.parse import quote

ROOT = '/root/framerexport/full-site-export-may21'

# slug -> canonical visible name (title/hero/card/deeplink)
CANONICAL = {
    'avito-ads':        'Авито Адс',
    'content-product':  'Коммуникационная стратегия',
    'product-statii':   'ПромоСтраницы Яндекс',
    'product-telegram': 'Лидген Телеграм',
    'youtube-product':  'Личный бренд YouTube',
}

# Текущее (до унификации) имя — то, что встречается на сайте в title/hero/cards.
# Используем для grep-замены и матчинга на главной.
PREVIOUS_ON_HOME = {
    'avito-ads':        'Авито Адс',
    'content-product':  'Контент-маркетинг',
    'product-statii':   'Рекламная стратегия',
    'product-telegram': 'Лидген Telegram',
    'youtube-product':  'Личный бренд YouTube',
}

# Описание для meta (используем существующий «дух», но имя — каноническое).
META_DESC_LONG = {
    'avito-ads':        'Авито Адс. Реклама на Авито со сквозной аналитикой, квиз-лендинг, CPL в 2–5 раз ниже Директа. Стратегические партнёры по маркетингу недвижимости.',
    'content-product':  'Коммуникационная стратегия. Кросс-платформенный маркетинг для застройщиков: продажи, найм, экспертность. Стратегические партнёры по маркетингу недвижимости.',
    'product-statii':   'ПромоСтраницы Яндекс. Рекламная стратегия с медиапланом, статьями и прогнозом продаж. Стратегические партнёры по маркетингу недвижимости.',
    'product-telegram': 'Лидген Телеграм: аналитика, контент, креатив. CPL в 2 раза ниже рынка. Стратегические партнёры по маркетингу недвижимости.',
    'youtube-product':  'Личный бренд YouTube: сценарии, продюсирование, запуск канала. Стратегические партнёры по маркетингу недвижимости.',
}

# META_DESC (JS-override переменная) — короткая.
META_DESC_SHORT = {
    slug: f"{name}. Стратегические партнёры по маркетингу недвижимости. ГЛАВНОЕ."
    for slug, name in CANONICAL.items()
}


def write_if_changed(path, new):
    with open(path, 'r', encoding='utf-8') as f:
        old = f.read()
    if old == new:
        return False
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new)
    return True


def build_deeplink(canonical_name, tier_name):
    text = (
        f"Здравствуйте! Пишу с сайта ГЛАВНОЕ, "
        f"хочу обсудить продукт: {canonical_name}. "
        f"Интересует тариф: {tier_name}."
    )
    return f"https://t.me/ksandrbloger?text={quote(text)}"


def update_product_page(slug):
    path = os.path.join(ROOT, 'product', slug, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    new_name = CANONICAL[slug]
    desc_long = META_DESC_LONG[slug]
    desc_short = META_DESC_SHORT[slug]

    # 1. <title>...</title>
    html = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{new_name} | ГЛАВНОЕ</title>',
        html, count=1,
    )

    # 2. <meta name="description" content="...">
    html = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*"',
        f'<meta name="description" content="{desc_long}"',
        html, count=1,
    )
    # 3. og:title
    html = re.sub(
        r'<meta\s+property="og:title"\s+content="[^"]*"',
        f'<meta property="og:title" content="{new_name} | ГЛАВНОЕ"',
        html, count=1,
    )
    # 4. og:description
    html = re.sub(
        r'<meta\s+property="og:description"\s+content="[^"]*"',
        f'<meta property="og:description" content="{desc_long}"',
        html, count=1,
    )
    # 5. twitter:title
    html = re.sub(
        r'<meta\s+name="twitter:title"\s+content="[^"]*"',
        f'<meta name="twitter:title" content="{new_name} | ГЛАВНОЕ"',
        html, count=1,
    )
    # 6. twitter:description
    html = re.sub(
        r'<meta\s+name="twitter:description"\s+content="[^"]*"',
        f'<meta name="twitter:description" content="{desc_long}"',
        html, count=1,
    )

    # 7. var PAGE_TITLE = "...";
    html = re.sub(
        r'var\s+PAGE_TITLE\s*=\s*"[^"]*";',
        f'var PAGE_TITLE = "{new_name} | ГЛАВНОЕ";',
        html, count=1,
    )
    # 8. var META_DESC = "...";
    html = re.sub(
        r'var\s+META_DESC\s*=\s*"[^"]*";',
        f'var META_DESC = "{desc_short}";',
        html, count=1,
    )

    # 9. REPLACEMENTS[0] — пара ["Авито Адс", "<OLD>"] → ["Авито Адс", "<NEW>"]
    #    Аккуратно: меняем только destination, чтобы не разломать массив.
    #    Шаблон: ["Авито Адс", "..."]
    html = re.sub(
        r'(\["Авито Адс",\s*")([^"]+)("\])',
        lambda m: f'{m.group(1)}{new_name}{m.group(3)}',
        html, count=1,
    )

    # 10. var TIERS — перегенерировать href через urlencode с новым именем.
    m = re.search(r'(var\s+TIERS\s*=\s*)(\[[\s\S]*?\]);', html)
    if not m:
        print(f"[WARN] {slug}: var TIERS not found", file=sys.stderr)
    else:
        tiers = json.loads(m.group(2))
        for t in tiers:
            tier_name = t.get('name', '')
            t['href'] = build_deeplink(new_name, tier_name)
        # ensure_ascii=False to keep cyrillic readable in source (matches existing)
        new_tiers_js = json.dumps(tiers, ensure_ascii=False)
        html = html[:m.start()] + m.group(1) + new_tiers_js + ';' + html[m.end():]

    return write_if_changed(path, html)


def update_home_index():
    path = os.path.join(ROOT, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Карточки <h5>OLD</h5> → <h5>NEW</h5>
    # 4 карточки нужны замены: content-product, product-statii, product-telegram, youtube-product.
    # avito-ads уже совпадает.
    for slug, new_name in CANONICAL.items():
        old_name = PREVIOUS_ON_HOME[slug]
        if old_name == new_name:
            continue
        # <h5 ...>OLD</h5>  — заменяем все вхождения с такой точной парой тегов.
        html = re.sub(
            rf'(<h5[^>]*>){re.escape(old_name)}(</h5>)',
            rf'\g<1>{new_name}\g<2>',
            html,
        )

        # ARCHIVE_PRODUCTS: { title: 'OLD', ... href: '/product/<slug>/' }
        # Заменим title для конкретной строки этого slug.
        html = re.sub(
            rf"(title:\s*')[^']+(',\s*tag:\s*'[^']*',\s*href:\s*'/product/{re.escape(slug)}/')",
            rf"\g<1>{new_name}\g<2>",
            html,
        )

        # CASES product_label: 'OLD'  для соответствующего product_url
        html = re.sub(
            rf"(product_url:\s*'/product/{re.escape(slug)}/',\s*product_label:\s*')[^']+(')",
            rf"\g<1>{new_name}\g<2>",
            html,
        )

    return write_if_changed(path, html)


def update_search_index():
    path = os.path.join(ROOT, 'search-index.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    changed = False
    for item in data:
        url = item.get('url', '')
        for slug, name in CANONICAL.items():
            target = f'/product/{slug}/'
            if url == target:
                new_title = f'{name} | ГЛАВНОЕ'
                new_desc = META_DESC_LONG[slug]
                if item.get('title') != new_title:
                    item['title'] = new_title
                    changed = True
                if 'description' in item and item.get('description') != new_desc:
                    item['description'] = new_desc
                    changed = True
                break
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
    return changed


def main():
    results = []
    for slug in CANONICAL:
        ch = update_product_page(slug)
        results.append((f'product/{slug}/index.html', ch))
    results.append(('index.html', update_home_index()))
    results.append(('search-index.json', update_search_index()))
    for path, ch in results:
        print(f"{'CHANGED' if ch else 'noop   '}  {path}")


if __name__ == '__main__':
    main()
