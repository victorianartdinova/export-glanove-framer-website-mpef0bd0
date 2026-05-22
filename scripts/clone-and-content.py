#!/usr/bin/env python3
"""Clone product/avito-ads/index.html byte-for-byte into 4 sibling product directories,
then substitute only content text nodes per product.

Master = product/avito-ads/index.html.
Children = content-product, product-statii, product-telegram, youtube-product.
"""
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / 'product' / 'avito-ads' / 'index.html'

# Content per child page. Keys are exact strings as they appear in master.
PRODUCTS = {
    'content-product': {
        'title': 'Контент-маркетинг | ГЛАВНОЕ',
        'description': 'Кросс-платформенная коммуникационная стратегия для застройщиков: продажи, найм, экспертность. Стратегические партнёры по маркетингу недвижимости.',
        'h2_hero': 'Контент-маркетинг',
        'hero_caption': '(контент + СМИ)',
        'price1': '150 k.',
        'price2': '280 k.',
        'tier_first_name': 'Контент',
    },
    'product-statii': {
        'title': 'Рекламная стратегия | ГЛАВНОЕ',
        'description': 'Рекламная стратегия с медиапланом и прогнозом продаж. Стратегические партнёры по маркетингу недвижимости.',
        'h2_hero': 'Рекламная стратегия',
        'hero_caption': '(стратегия + прогноз)',
        'price1': '200 k.',
        'price2': '400 k.',
        'tier_first_name': 'Медиаплан',
    },
    'product-telegram': {
        'title': 'Лидген Telegram | ГЛАВНОЕ',
        'description': 'Лидген в Telegram: аналитика, контент, креатив. CPL в 2 раза ниже рынка. Стратегические партнёры по маркетингу недвижимости.',
        'h2_hero': 'Лидген Telegram',
        'hero_caption': '(трафик + канал)',
        'price1': '165 k.',
        'price2': '220 k.',
        'tier_first_name': 'Запуск рекламы',
    },
    'youtube-product': {
        'title': 'Личный бренд YouTube | ГЛАВНОЕ',
        'description': 'Личный бренд на YouTube: сценарии, продюсирование, запуск канала. Стратегические партнёры по маркетингу недвижимости.',
        'h2_hero': 'Личный бренд YouTube',
        'hero_caption': '(продюсирование)',
        'price1': '180 k.',
        'price2': '300 k.',
        'tier_first_name': 'Запуск канала',
    },
}

# Master values that we will replace inside each child copy.
MASTER_TITLE = 'Авито Адс | ГЛАВНОЕ'
MASTER_DESC = 'Стратегические партнёры по маркетингу для застройщиков. Performance-маркетинг, Telegram, Авито, стратегия продвижения недвижимости.'
MASTER_H2 = 'Авито Адс'
MASTER_HERO_CAP = '(управление + Адс)'
MASTER_PRICE1 = '80 k.'
MASTER_PRICE2 = '120 k.'
MASTER_TIER_FIRST = 'Только реклама'

def substitute(html: str, p: dict) -> str:
    # Page <title>
    html = html.replace(f'<title>{MASTER_TITLE}</title>', f"<title>{p['title']}</title>")

    # All meta tags that carry the title — og:title, twitter:title, og:site_name uses different value, leave it.
    html = re.sub(
        r'(<meta[^>]+(?:property="og:title"|name="twitter:title")[^>]+content=")[^"]*("[^>]*>)',
        lambda m: m.group(1) + p['title'] + m.group(2),
        html,
    )

    # description / og:description / twitter:description — overwrite even if master has shared text
    html = re.sub(
        r'(<meta[^>]+(?:name="description"|property="og:description"|name="twitter:description")[^>]+content=")[^"]*("[^>]*>)',
        lambda m: m.group(1) + p['description'] + m.group(2),
        html,
    )

    # Hero H2 (product name) — replace ALL occurrences of "Авито Адс" inside visible content,
    # but NOT inside SEO/<title> (already overwritten above). Use word-boundary-ish match —
    # Russian text, so just textual replace is enough; remaining "Авито Адс" mentions in deep
    # SEO meta block have been replaced via regex above.
    html = html.replace('>Авито Адс<', f">{p['h2_hero']}<")
    # The hero h2 may appear wrapped with spaces or split — handle plain ">Авито Адс<".

    # Hero caption (управление + Адс) → product caption
    html = html.replace(f'>{MASTER_HERO_CAP}<', f">{p['hero_caption']}<")

    # Prices in pricing cards
    html = html.replace(f'>{MASTER_PRICE1}<', f">{p['price1']}<")
    html = html.replace(f'>{MASTER_PRICE2}<', f">{p['price2']}<")

    # Tier name reference: «Только реклама» → product first tier name
    html = html.replace(f'«{MASTER_TIER_FIRST}»', f"«{p['tier_first_name']}»")

    # Canonical / og:url — point to product slug
    slug = p.get('slug')  # injected by caller
    if slug:
        html = re.sub(
            r'(<meta[^>]+property="og:url"[^>]+content=")[^"]*("[^>]*>)',
            lambda m: m.group(1) + f'/product/{slug}/' + m.group(2),
            html,
        )
        html = re.sub(
            r'(<link[^>]+rel="canonical"[^>]+href=")[^"]*("[^>]*>)',
            lambda m: m.group(1) + f'/product/{slug}/' + m.group(2),
            html,
        )

    return html

def main():
    master_html = MASTER.read_text(encoding='utf-8')
    for slug, content in PRODUCTS.items():
        target = ROOT / 'product' / slug / 'index.html'
        # byte-for-byte clone first
        shutil.copyfile(MASTER, target)
        content_with_slug = dict(content, slug=slug)
        out = substitute(master_html, content_with_slug)
        target.write_text(out, encoding='utf-8')
        print(f'wrote {target.relative_to(ROOT)} ({len(out)} bytes)')

if __name__ == '__main__':
    main()
