#!/usr/bin/env python3
"""Inject 3rd tier into TIERS array of content/statii/youtube product pages.
Telegram is NOT touched (already has 3 tiers).
Values are taken from CURRENT_PRODUCT_STATUS.md (original Framer table)."""
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path('/root/framerexport/full-site-export-may21')

# Product → display name → 3rd tier definition
TIER3 = {
    'content-product': {
        'product': 'Коммуникационная стратегия',
        'tier': {
            'name': 'ОМНИКАНАЛ',
            'desc': 'Полная коммуникационная экосистема под ключ.',
            'price': '350 k.',
            'bullets': [
                'PR-планы и упаковка экспертизы под рынок',
                'AI-команда: сценарии, монтаж, дистрибуция',
                'Брендинг каналов и единая визуальная система',
                'Кросс-канальные посевы и ретаргетинг',
                'Сопровождение топ-менеджмента'
            ],
            'included_line': 'Всё из тарифа «Полная стратегия»'
        }
    },
    'product-statii': {
        'product': 'ПромоСтраницы Яндекса',
        'tier': {
            'name': 'ПРОМОСТРАНИЦЫ + ВЕДЕНИЕ',
            'desc': 'Полный цикл ПромоСтраниц: запуск, ведение, аналитика.',
            'price': '400 k.',
            'bullets': [
                'Стратегия + 10-15 статей в месяц',
                'A/B тесты заголовков и форматов',
                'Расширение по сегментам и аудиториям',
                'Метрика, сквозная аналитика, ROI-отчёт',
                'Ретаргетинг и масштабирование удачных связок'
            ],
            'included_line': 'Всё из тарифа «Ведение + A/B»'
        }
    },
    'youtube-product': {
        'product': 'Личный бренд YouTube',
        'tier': {
            'name': 'ПРОДЮСИРОВАНИЕ',
            'desc': 'Полный продакшн под ключ — от идеи до публикации.',
            'price': '300 k.',
            'bullets': [
                'Стратегия + сценарии + продакшн',
                'Съёмки, монтаж, обложки, описания',
                'Дистрибуция: Reels / Shorts / Threads',
                'Воронка → сайт → CRM',
                'Команда продюсеров и монтажёров'
            ],
            'included_line': 'Всё из тарифа «Стратегия + сценарии»'
        }
    }
}

MARK = 'data-glavnoe-tier3-injected'


def build_href(product, tier_name):
    text = f"Здравствуйте! Пишу с сайта ГЛАВНОЕ, хочу обсудить продукт: {product}. Интересует тариф: {tier_name}."
    return f"https://t.me/ksandrbloger?text={quote(text)}"


def patch_one(slug, cfg):
    f = ROOT / 'product' / slug / 'index.html'
    html = f.read_text(encoding='utf-8')
    if MARK in html:
        print(f'SKIP {slug} — already injected')
        return False

    # Find: var TIERS = [ ... ];
    m = re.search(r'(var\s+TIERS\s*=\s*)(\[.*?\])(\s*;)', html, re.DOTALL)
    if not m:
        print(f'FAIL {slug}: TIERS not found')
        return False

    tiers_text = m.group(2)
    tiers = json.loads(tiers_text)
    if len(tiers) >= 3:
        print(f'SKIP {slug} — already has {len(tiers)} tiers')
        return False

    new_tier = dict(cfg['tier'])
    new_tier['href'] = build_href(cfg['product'], new_tier['name'])
    tiers.append(new_tier)
    new_json = json.dumps(tiers, ensure_ascii=False)
    new_html = html[:m.start(2)] + new_json + html[m.end(2):]
    # Add marker comment near script tag for idempotency
    new_html = new_html.replace(
        'data-glavnoe-product-override',
        f'{MARK}="1" data-glavnoe-product-override',
        1
    )
    f.write_text(new_html, encoding='utf-8')
    print(f'OK {slug}: +ОМНИКАНАЛ/ПРОДЮСИРОВАНИЕ/ПРОМО+ВЕДЕНИЕ ({new_tier["name"]} {new_tier["price"]})')
    return True


for slug, cfg in TIER3.items():
    patch_one(slug, cfg)
