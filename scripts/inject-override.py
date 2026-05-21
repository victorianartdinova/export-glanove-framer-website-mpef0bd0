#!/usr/bin/env python3
"""Inject post-hydration content override <script> before </body> in each of 4
product page HTMLs.

Replacement strategy: two-pass via placeholders. First pass maps all source
text-node values to unique placeholders; second pass maps placeholders to the
product-specific target text. This prevents collisions where one replacement
output is a substring of another source (e.g. "80 k." in "280 k.").
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Order matters only for human reading; runtime applies the whole map.
# Each entry: source-text => destination-text. Source MUST appear as a complete
# text node value in avito-ads' DOM (single-line). Multi-line wrapped Framer
# paragraphs are intentionally NOT replaced here.

AVITO_ABOUT_PARAGRAPH = 'Запускаем рекламу на Авито со сквозной аналитикой — от первого показа до заявки в CRM. Аудит конкурентов, точная сегментация по 560 сегментам, квиз-лендинг, A/B тесты и контроль CPL до сделки.'

TG_HANDLE = 'ksandrbloger'

def tg_link(product_name: str, tier_name: str) -> str:
    """Build a t.me link with pre-filled message identifying source + product + tier."""
    import urllib.parse
    text = (
        f"Здравствуйте! Пишу с сайта ГЛАВНОЕ, хочу обсудить продукт: "
        f"{product_name}. Интересует тариф: {tier_name}."
    )
    return f"https://t.me/{TG_HANDLE}?text={urllib.parse.quote(text, safe='')}"

def fill(name, caption_left, caption_center, caption_right,
         tier1_name, tier1_desc, price1,
         tier2_name, tier2_desc, price2,
         tier_first_label, big_num, stat_label, hero_title_meta,
         about_paragraph, cta_button,
         tier1_bullets, tier2_bullets,
         extra_tiers=None,
         tier1_bullets_full=None, tier2_bullets_full=None):
    """Build override config. Tier 3 is intentionally not supported — the 2-tier
    layout is approved as final. `tier1_bullets` / `tier2_bullets` are 3 / 5
    product-specific replacements for the Avito-default bullets inside the tier
    cards. Each is a list of [source-string, target-string] pairs; the source
    side reflects the Avito-default bullet text present in the master HTML."""
    cfg = {
        'page_title': hero_title_meta,
        'meta_description': f"{name}. Стратегические партнёры по маркетингу недвижимости. ГЛАВНОЕ.",
        'about_paragraph': about_paragraph,
        'product_name': name,
        'tier1_name': tier1_name,
        'tier2_name': tier2_name,
        'tier1_href': tg_link(name, tier1_name),
        'tier2_href': tg_link(name, tier2_name),
        'replacements': [
            ['Авито Адс', name],
            ['(управление + Адс)', caption_left],
            ['Реклама + квиз-лендинг + сквозная аналитика. CPL в 2–5 раз дешевле Директа.', caption_center],
            ['лиды/классифайд', caption_right],
            ['ТОЛЬКО РЕКЛАМА', tier1_name],
            ['Запуск и управление кампаний.', tier1_desc],
            ['80 k.', price1],
            ['РЕКЛАМА + ПОСАДОЧНАЯ', tier2_name],
            ['Управление всей воронкой', tier2_desc],
            ['120 k.', price2],
            ['Всё из тарифа «Только реклама»', f'Всё из тарифа «{tier_first_label}»'],
            ['1000', big_num],
            ['отношение к результатам', stat_label],
            # Framer's tablet/mobile variant of Tier 2 ships with English
            # placeholder text ("PREMIUM PLAN" etc.). Map each to the matching
            # product-specific Tier 2 content so the narrow-viewport card
            # carries the same bullets as the desktop tier-2 first three.
            ['PREMIUM PLAN', tier2_name],
            ['For enterprise and organizations', tier2_desc],
            ['12000', price2],
            ['Fully mangage project', tier2_bullets[0][1]],
            ['Creative strategy', tier2_bullets[1][1]],
            ['Access to entire team', tier2_bullets[2][1]],
            # Big number carousel slides 2/3 ship an Avito-only Russian
            # subtitle that is irrelevant to other products. Clear it so
            # those slides show only the number + stat label.
            ['Cтоимость целевого обращения на недвижимость бизнес и премиум-класса', stat_label],
            ['Стоимость целевого обращения на недвижимость бизнес и премиум-класса', stat_label],
            # About paragraph under the "КАК БУДЕМ РАБОТАТЬ" block.
            [AVITO_ABOUT_PARAGRAPH, about_paragraph],
            # CTA button inside the dark process block.
            ['СБОРКА КАМПАНИИ', cta_button],
        ] + tier1_bullets + tier2_bullets,
        # Expose desktop tier-2 bullet pairs so the override script can read
        # the target strings (the desktop bullet text the user sees) and
        # carry them into the mobile Tier 2 card.
        'tier2_bullets_src': tier2_bullets,
        'tier2_included_line': f'Всё из тарифа «{tier_first_label}»',
        # Fields consumed by the custom tariff block renderer in
        # OVERRIDE_TMPL.renderCustomTariffs. These let the override draw a
        # fully controllable pair of tariff cards (white Tier 1 + red Tier 2)
        # without relying on Framer's mobile variant of Tier 2.
        'tier1_name': tier1_name,
        'tier1_desc': tier1_desc,
        'tier1_price': price1,
        'tier1_bullets_dst': [pair[1] for pair in tier1_bullets],
        'tier2_name_full': tier2_name,
        'tier2_desc_full': tier2_desc,
        'tier2_price': price2,
    }
    # Build tiers array consumed by renderCustomTariffs in OVERRIDE_TMPL.
    # Each tier dict: {name, desc, price, bullets, href, included_line}.
    # `tier1_bullets_full` / `tier2_bullets_full` override the REPLACEMENTS-pair
    # bullet lists when the page needs more than the 3/5 default count.
    t1_dst = tier1_bullets_full if tier1_bullets_full is not None else [pair[1] for pair in tier1_bullets]
    t2_dst = tier2_bullets_full if tier2_bullets_full is not None else [pair[1] for pair in tier2_bullets]
    tiers = [
        {
            'name': tier1_name,
            'desc': tier1_desc,
            'price': price1,
            'bullets': t1_dst,
            'href': tg_link(name, tier1_name),
            'included_line': None,
        },
        {
            'name': tier2_name,
            'desc': tier2_desc,
            'price': price2,
            'bullets': t2_dst,
            'href': tg_link(name, tier2_name),
            'included_line': f'Всё из тарифа «{tier_first_label}»',
        },
    ]
    if extra_tiers:
        for et in extra_tiers:
            tiers.append({
                'name': et['name'],
                'desc': et['desc'],
                'price': et['price'],
                'bullets': et['bullets'],
                'href': tg_link(name, et['name']),
                'included_line': et.get('included_line') or f"Всё из тарифа «{et.get('includes_label') or tier_first_label}»",
            })
    cfg['tiers'] = tiers
    return cfg

# Avito-default bullets present in master tier cards. These are the source
# strings for bullet substitutions; product-specific targets are defined per
# product below. Tier 1 has 3 bullets, Tier 2 has 5.
TIER1_BULLETS_SRC = [
    'Управление кампаниями и бюджетом',
    'Разработка баннеров 3–5 шт/1 оффер',
    'Отчёты 4 раза/мес "план-факт"',
]
TIER2_BULLETS_SRC = [
    'Cтратегия заявок до квалификации',
    'Разработка технического задания на посадочные',
    'Разработка посадочной страницы',
    'Настройка рекламы на канал, если посадочная не подошла',
    'гиперСегментация ЦА и подбор офферов',
]

def bullets(t1, t2):
    """Pair tier-1 / tier-2 product-specific bullets with Avito source strings."""
    assert len(t1) == 3, "tier 1 expects 3 bullets"
    assert len(t2) == 5, "tier 2 expects 5 bullets"
    return (
        [[src, dst] for src, dst in zip(TIER1_BULLETS_SRC, t1)],
        [[src, dst] for src, dst in zip(TIER2_BULLETS_SRC, t2)],
    )

PRODUCTS = {}

# П6 — Авито Адс. Источник: GLAVNOE_products_from_sheet_2026-03-19.md.
# Tier 1: Тестовый запуск 80k (1.5 мес). Tier 2: Ежемесячное ведение 100k.
_av_t1, _av_t2 = bullets(
    ['Анализ конкурентов и сегментация ЦА',
     'Запуск кампаний с тестовыми гипотезами',
     '3-5 креативов с A/B-тестами'],
    ['Управление рекламой (CPC + CPM) до результата',
     'Сегментация по 560 аудиторным параметрам',
     'Квиз-лендинг с конверсией 12-30%',
     'Сквозная аналитика (Roistat) от показа до сделки',
     'Отчёты 2 раза в месяц «план-факт»'],
)
_av_t1_full = [
    'Сегментация по 560 аудиторным параметрам',
    'Анализ конкурентов в локации и сегменте',
    '3-5 креативов с A/B-тестами',
    'Управление рекламой (CPC + CPM)',
    'Сквозная аналитика (Roistat)',
    'Отчёт по тестовому периоду 1.5 мес',
]
_av_t2_full = [
    'Управление рекламой (CPC + CPM) ежемесячно',
    'Сегментация по 560 аудиторным параметрам',
    '3-5 новых креативов в месяц с A/B-тестами',
    'Квиз-лендинг с конверсией 12-30%',
    'Сквозная аналитика (Roistat) от показа до сделки',
    'Анализ конкурентов и оптимизация связок',
    'Отчёты 2 раза в месяц «план-факт»',
]
PRODUCTS['avito-ads'] = fill(
    name='Авито Адс',
    caption_left='(управление + Адс)',
    caption_center='Реклама + квиз-лендинг + сквозная аналитика. CPL в 2–5 раз дешевле Директа.',
    caption_right='лиды/классифайд',
    tier1_name='ТЕСТОВЫЙ',
    tier1_desc='Запуск и проверка гипотез за 1.5 мес.',
    price1='80 k.',
    tier2_name='ЕЖЕМЕСЯЧНО',
    tier2_desc='Управление и оптимизация под CPL.',
    price2='120 k.',
    tier_first_label='Тестовый',
    big_num='1000',
    stat_label='отношение к результатам',
    hero_title_meta='Авито Адс | ГЛАВНОЕ',
    about_paragraph=AVITO_ABOUT_PARAGRAPH,
    cta_button='СБОРКА КАМПАНИИ',
    tier1_bullets=_av_t1, tier2_bullets=_av_t2,
    tier1_bullets_full=_av_t1_full, tier2_bullets_full=_av_t2_full,
)

# П2 — Контент-стратегия. Источник: /root/ops/marketing/GLAVNOE_products_from_sheet_2026-03-19.md
# Варианты в таблице: HR-бренд 120k / 1-2 канала 150k / Полная стратегия 200k.
# Берём 1-2 канала (150k) и Полную стратегию (200k) как 2-tier.
_cp_t1, _cp_t2 = bullets(
    ['Анализ форматов контента и позиционирования',
     'Контент-план на 3 месяца, 1-2 канала',
     'Инструменты роста аудитории'],
    ['Контент-план на 3 месяца под все каналы',
     'Разработка УТП и tone of voice',
     'Техническая интеграция для сбора лидов',
     'AI-инфраструктура для контент-команды',
     'Лидген через контент + закрепление статуса на рынке'],
)
_cp_t1_full = [
    'Анализ форматов контента и позиционирования',
    'Разработка УТП и tone of voice',
    'Контент-план на 3 месяца под 1-2 канала',
    'Инструменты роста аудитории',
    'Базовая техническая интеграция для сбора лидов',
]
_cp_t2_full = [
    'Анализ форматов контента и позиционирования',
    'Разработка УТП и tone of voice',
    'Контент-план на 3 месяца под все каналы (TG, Reels, YouTube, Threads)',
    'Инструменты роста аудитории по каждому каналу',
    'Техническая интеграция для сбора лидов: формы, боты, посадочные',
    'AI-инфраструктура для контент-команды: сценарии, монтаж, дистрибуция',
    'Закрепление статуса на рынке: PR-планы и упаковка экспертизы',
]
PRODUCTS['content-product'] = fill(
    name='Коммуникационная стратегия',
    caption_left='(контент + СМИ)',
    caption_center='Контент-система для продаж, найма и экспертности. От УТП до AI-инфраструктуры команды.',
    caption_right='контент/стратегия',
    tier1_name='1-2 КАНАЛА',
    tier1_desc='Стратегия для 1-2 каналов.',
    price1='150 k.',
    tier2_name='ПОЛНАЯ СТРАТЕГИЯ',
    tier2_desc='Все каналы + лидген + AI-команда.',
    price2='200 k.',
    tier_first_label='1-2 канала',
    big_num='500',
    stat_label='запусков контент-систем',
    hero_title_meta='Коммуникационная стратегия | ГЛАВНОЕ',
    about_paragraph='Делаем коммуникационную стратегию на 3 месяца: позиционирование, УТП, контент-план, инструменты роста аудитории и техническая интеграция для сбора лидов. Подключаем AI-инфраструктуру в работу команды.',
    cta_button='ЗАПУСК СТРАТЕГИИ',
    tier1_bullets=_cp_t1, tier2_bullets=_cp_t2,
    tier1_bullets_full=_cp_t1_full, tier2_bullets_full=_cp_t2_full,
)

# П5 — ПромоСтраницы Яндекса. Источник: GLAVNOE_products_from_sheet_2026-03-19.md.
# Tier 1: разовый запуск 80k (стратегия + 3-5 статей). Tier 2: ведение 130k/мес (4-6 статей + A/B + ретаргет).
_ps_t1, _ps_t2 = bullets(
    ['Контент-стратегия для ПромоСтраниц',
     '3-5 статей в нативном формате',
     'Настройка аналитики ассоциированных конверсий'],
    ['4-6 статей в месяц',
     'A/B тесты заголовков и форматов',
     'Связка: ПромоСтраницы → посадочная → Метрика → ретаргетинг',
     'Оптимизация по влиянию на продажи, не только просмотры',
     'Настройка ловца лидов (телемаркетинг)'],
)
_ps_t1_full = [
    'Контент-стратегия для ПромоСтраниц: темы, форматы, воронка',
    '3-5 статей в нативном формате',
    'Настройка аналитики ассоциированных конверсий',
    'A/B тесты заголовков на запуске',
    'Связка ПромоСтраниц с Метрикой и ретаргетингом',
]
_ps_t2_full = [
    '4-6 статей в месяц',
    'A/B тесты заголовков и форматов',
    'Связка: ПромоСтраницы → посадочная → Метрика → ретаргетинг → заявка',
    'Оптимизация по влиянию на продажи, не только просмотры',
    'Настройка ловца лидов (телемаркетинг)',
    'Ежемесячный отчёт: дочитывания, переходы, ассоциированные конверсии',
]
PRODUCTS['product-statii'] = fill(
    name='ПромоСтраницы Яндекса',
    caption_left='(статьи + аналитика)',
    caption_center='Нативные статьи с оплатой за дочитывание. На 32% дешевле перформанса, ROI до 6 000%.',
    caption_right='статьи/яндекс',
    tier1_name='РАЗОВЫЙ ЗАПУСК',
    tier1_desc='Стратегия и 3-5 статей.',
    price1='80 k.',
    tier2_name='ВЕДЕНИЕ + A/B',
    tier2_desc='Ежемесячное ведение с тестами.',
    price2='130 k.',
    tier_first_label='Разовый запуск',
    big_num='6000',
    stat_label='% ROI ПромоСтраниц',
    hero_title_meta='ПромоСтраницы Яндекса | ГЛАВНОЕ',
    about_paragraph='Запускаем ПромоСтраницы Яндекса: оплата только за дочитывание и переход, 3 минуты контакта с пользователем. Контент-стратегия, нативные статьи, аналитика ассоциированных конверсий, A/B тесты заголовков и связка с ретаргетингом — до заявки.',
    cta_button='ЗАПУСК ПРОМОСТРАНИЦ',
    tier1_bullets=_ps_t1, tier2_bullets=_ps_t2,
    tier1_bullets_full=_ps_t1_full, tier2_bullets_full=_ps_t2_full,
)

# Лидген в Telegram — 3 тарифа Студия / Дуплекс / Пентхаус. Источник: PDF
# "Glavnoe тарифы" от 21.05.2026, блок «Если нужен комплекс работ».
# Базовые tier1_bullets / tier2_bullets держим короткими (для REPLACEMENTS на
# скрытом master-блоке), полные списки идут в *_bullets_full и extra_tiers.
_pt_t1, _pt_t2 = bullets(
    ['15 публикаций и контент-план',
     'Адаптация фир. стиля для telegram-канала (12 постов + 2 gif)',
     '2 созвона в zoom и чат-поддержка'],
    ['30 публикаций, 10 сториз, 4 сценария для голосовых, монтаж 1 ролика',
     'pdf-каталог, 5 Gif-постов и контент-план',
     'Адаптация фир. стиля для telegram-канала (12 постов + 2 gif)',
     '2 созвона в zoom + 1 созвон с брокерами по обработке',
     'Telegram Ads: постоплата, 15 запущенных связок, итоговый отчёт'],
)
_pt_t1_full = [
    '15 публикаций и контент-план',
    'Адаптация фир. стиля для telegram-канала (12 постов + 2 gif)',
    '2 созвона в zoom и чат-поддержка',
    '1 созвон с брокерами по обработке',
    'Автоматизация приёма обращений: бот в WhatsApp/Telegram + связка с AMO CRM, WhatsApp-автоответы',
    'Telegram Ads: подключение постоплаты. 5 запущенных связок, итоговый отчёт',
]
_pt_t2_full = [
    '30 публикаций, 10 сториз, 4 сценария для голосовых, монтаж 1 ролика',
    'pdf-каталог, 5 Gif-постов, контент-план',
    'Адаптация фир. стиля для telegram-канала (12 постов + 2 gif)',
    '2 созвона в zoom и чат-поддержка',
    '1 созвон с брокерами по обработке',
    'Автоматизация приёма обращений: бот в WhatsApp/Telegram + связка с AMO CRM',
    'Telegram Ads: подключение постоплаты. 15 запущенных связок, итоговый отчёт',
]
_pt_t3_full = [
    '60 публикаций, 20 сториз, 10 сценариев для голосовых, монтаж 2 роликов',
    'pdf-каталог, 15 Gif-постов, контент-план',
    'Адаптация фир. стиля для telegram-канала (12 постов + 2 gif)',
    '4 созвона в zoom и чат-поддержка',
    '2 созвона с брокерами по обработке',
    'Автоматизация приёма обращений: бот в WhatsApp/Telegram + связка с AMO CRM',
    'Telegram Ads: подключение постоплаты. 15 запущенных связок, итоговый отчёт',
]
PRODUCTS['product-telegram'] = fill(
    name='Лидген Telegram',
    caption_left='(трафик + канал)',
    caption_center='Лидген через Telegram: контент, реклама, автоматизация обращений. CPL квалифицированного лида — 10 000 ₽.',
    caption_right='лиды/Telegram',
    tier1_name='СТУДИЯ',
    tier1_desc='Подойдёт, если хотите затестить источник.',
    price1='145 k.',
    tier2_name='ДУПЛЕКС',
    tier2_desc='Оптимальный, если не планируете много контента.',
    price2='165 k.',
    tier_first_label='Студия',
    big_num='800',
    stat_label='заявок из Telegram-рекламы',
    hero_title_meta='Лидген Telegram | ГЛАВНОЕ',
    about_paragraph='Запускаем лидогенерацию в Telegram под ключ: контент-план и публикации, адаптация фирменного стиля канала, Telegram Ads с постоплатой, созвоны с брокерами и автоматизация обращений через бота WhatsApp/Telegram + AMO CRM. Стоимость квалифицированного лида — 10 000 ₽.',
    cta_button='ЗАПУСК TELEGRAM',
    tier1_bullets=_pt_t1, tier2_bullets=_pt_t2,
    tier1_bullets_full=_pt_t1_full, tier2_bullets_full=_pt_t2_full,
    extra_tiers=[{
        'name': 'ПЕНТХАУС',
        'desc': 'Плотно интегрируемся в отдел продаж — каждый контакт работает как бетонная плита.',
        'price': '240 k.',
        'bullets': _pt_t3_full,
        'includes_label': 'Дуплекс',
    }],
)

# П4 — YouTube-стратегия. Источник: GLAVNOE_products_from_sheet_2026-03-19.md.
# Tier 1: стратегия канала 120k. Tier 2: стратегия + 5 сценариев 150k.
_yt_t1, _yt_t2 = bullets(
    ['Концепция YouTube-канала: позиционирование и ниша',
     'Упаковка канала: ТЗ на дизайн и визуал',
     'Стратегия роликов и форматы'],
    ['Несколько готовых сценариев + методология',
     'ТЗ на оптимизацию каждого ролика',
     'Юнит-экономика 1 съёмки и плана на 4 ролика/мес',
     'Воронка контента: YouTube → Reels → TG → Сайт',
     'Команда + AI-инструменты + найм монтажёра'],
)
_yt_t1_full = [
    'Концепция YouTube-канала: позиционирование, ниша, формат',
    'Упаковка канала: ТЗ на дизайн и визуал',
    'Стратегия роликов и форматы',
    'Собственные смыслы и ценности для личного бренда',
    'ТЗ на оптимизацию каждого ролика (SEO, thumbnail, hook)',
    'Юнит-экономика 1 съёмки и плана на 4 ролика/мес',
    'Команда + AI-инструменты + бюджет и прогнозы',
]
_yt_t2_full = [
    'Концепция YouTube-канала: позиционирование, ниша, формат',
    'Упаковка канала: ТЗ на дизайн и визуал',
    'Стратегия роликов и форматы + готовые сценарии',
    'ТЗ на оптимизацию каждого ролика',
    'Юнит-экономика 1 съёмки и плана на 4 ролика/мес',
    'Воронка контента: YouTube → Reels → TG → Сайт',
    'Система найма монтажёра + AI-инструменты для монтажа',
    'Команда + бюджет + прогнозы охватов и заявок',
]
PRODUCTS['youtube-product'] = fill(
    name='YouTube-стратегия',
    caption_left='(стратегия + сценарии)',
    caption_center='Запуск YouTube с готовой стратегией. Видео → заявка → сделка за 3-4 недели.',
    caption_right='youtube/бренд',
    tier1_name='СТРАТЕГИЯ КАНАЛА',
    tier1_desc='Концепция, упаковка и форматы.',
    price1='120 k.',
    tier2_name='СТРАТЕГИЯ + СЦЕНАРИИ',
    tier2_desc='Стратегия плюс готовые сценарии.',
    price2='150 k.',
    tier_first_label='Стратегия канала',
    big_num='50',
    stat_label='личных брендов основателей',
    hero_title_meta='YouTube-стратегия | ГЛАВНОЕ',
    about_paragraph='Запускаем YouTube-канал с готовой стратегией: концепция, позиционирование, упаковка, форматы роликов, юнит-экономика съёмок. Воронка контента YouTube → Reels → TG → Сайт. Команда, AI-инструменты и план найма монтажёра.',
    cta_button='ЗАПУСК YOUTUBE',
    tier1_bullets=_yt_t1, tier2_bullets=_yt_t2,
    tier1_bullets_full=_yt_t1_full, tier2_bullets_full=_yt_t2_full,
)


OVERRIDE_TMPL = """
<script data-glavnoe-product-override="{slug}">
(function(){{
  var REPLACEMENTS = {replacements_json};
  var PAGE_TITLE = {title_json};
  var META_DESC = {desc_json};
  var ABOUT_PARAGRAPH = {about_json};
  var TIER1_HREF = {tier1_href_json};
  var TIER2_HREF = {tier2_href_json};
  var TIER2_DESKTOP_BULLETS = {tier2_desktop_bullets_json};
  var TIER2_INCLUDED_LINE = {tier2_included_line_json};
  var TIERS = {tiers_json};
  var TIER_BUTTON_LABEL = 'Обсудить тариф';
  var TIER_PRICE_NOTE = 'Оплата раз в месяц + рекламный бюджет';
  var CUSTOM_TARIFF_CSS = {custom_tariff_css_json};
  var EXTRA_OFFER_TITLE = 'Нужен другой формат работы?';
  var EXTRA_OFFER_TEXT = 'Мы открыты к индивидуальным задачам и нестандартным условиям сотрудничества. Расскажите о вашем проекте — предложим оптимальное решение под ваши цели и вводные данные.';
  var AVITO_PARAGRAPH_FULL = 'Запускаем рекламу на Авито со сквозной аналитикой — от первого показа до заявки в CRM. Аудит конкурентов, точная сегментация по 560 сегментам, квиз-лендинг, A/B тесты и контроль CPL до сделки.';
  var AVITO_FRAGMENT_RE = /(Авито|сегментам|аналитикой —|конкурентов,|CPL до|A\\/B тесты|квиз-)/;

  // Build a Map for O(1) exact-match lookup: source -> target.
  // EXACT trimmed match only — safe even when target contains source as a
  // substring (e.g. "280 k." contains "80 k."), because we never match
  // substrings and never re-process an already-substituted node value.
  var SRC2DST = {{}};
  var DST_VALUES = {{}};
  for (var i = 0; i < REPLACEMENTS.length; i++) {{
    SRC2DST[REPLACEMENTS[i][0]] = REPLACEMENTS[i][1];
    DST_VALUES[REPLACEMENTS[i][1]] = true;
  }}

  function applyMetaOverrides(){{
    try {{
      if (document.title !== PAGE_TITLE) document.title = PAGE_TITLE;
      var sels = [
        ['meta[name="description"]', META_DESC],
        ['meta[property="og:title"]', PAGE_TITLE],
        ['meta[property="og:description"]', META_DESC],
        ['meta[name="twitter:title"]', PAGE_TITLE],
        ['meta[name="twitter:description"]', META_DESC]
      ];
      sels.forEach(function(p){{
        var el = document.querySelector(p[0]);
        if (el && el.getAttribute('content') !== p[1]) el.setAttribute('content', p[1]);
      }});
    }} catch(e) {{}}
  }}

  function maybeReplace(node){{
    if (!node || node.nodeType !== 3) return;
    // Never touch text inside our custom tariff block — it owns its content.
    if (node.parentElement && node.parentElement.closest && node.parentElement.closest('[data-glavnoe-tariffs="1"]')) return;
    var raw = node.nodeValue;
    if (!raw) return;
    var t = raw.replace(/\\u00A0/g, ' ').trim();
    if (!t) return;
    // Skip nodes that already hold one of our target values — they were
    // substituted on a previous pass; touching them risks reverting.
    if (DST_VALUES[t]) return;
    var dst = SRC2DST[t];
    if (dst !== undefined) {{
      node.nodeValue = dst;
    }}
  }}

  function walkAndReplace(root){{
    if (!root) return;
    try {{
      var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
      var n;
      while ((n = walker.nextNode())) maybeReplace(n);
    }} catch(e) {{}}
  }}

  // 1. Synchronous pass — runs at parse time, before first paint of <body>'s
  //    tail content. Catches everything SSR'd by Framer into the HTML.
  applyMetaOverrides();
  if (document.body) walkAndReplace(document.body);

  // 2. Persistent MutationObserver — catches anything Framer rewrites during
  //    client-side hydration (text nodes inside React-managed trees).
  var observer = new MutationObserver(function(mutations){{
    applyMetaOverrides();
    for (var m = 0; m < mutations.length; m++) {{
      var mut = mutations[m];
      if (mut.type === 'characterData') {{
        maybeReplace(mut.target);
      }} else if (mut.type === 'childList') {{
        for (var a = 0; a < mut.addedNodes.length; a++) {{
          var added = mut.addedNodes[a];
          if (added.nodeType === 3) {{
            maybeReplace(added);
          }} else if (added.nodeType === 1) {{
            walkAndReplace(added);
          }}
        }}
      }}
    }}
  }});
  function startObserver(){{
    if (document.body) {{
      observer.observe(document.body, {{
        childList: true,
        subtree: true,
        characterData: true
      }});
    }}
  }}
  startObserver();

  // 3. Safety re-sweeps + observer shutdown.
  //    Framer typically completes hydration within ~2-3s. After that we do a
  //    final full sweep and disconnect the observer to avoid runtime overhead.
  function fullSweep(){{
    applyMetaOverrides();
    walkAndReplace(document.body);
  }}

  // 3b. About-section paragraph replacement.
  //     Master Avito paragraph is rendered as one visible text node PLUS a
  //     set of measurement wrap-spans (inline-block <span>s without classes)
  //     that split the same paragraph into lines. On desktop those spans are
  //     hidden by media query; on mobile they become visible and would leak
  //     stale Avito text. We replace the visible paragraph with the product
  //     text and clear every wrap-span that carries Avito-specific tokens.
  //     A wide token regex is used so the cleanup catches any wrap segment
  //     of the master paragraph regardless of where Framer chose to break.
  var AVITO_WRAP_TOKEN_RE = /(Авито|сквозной аналитикой|первого показа|заявки в CRM|конкурентов, точная|сегментация по 560|сегментам, квиз|тесты и контроль CPL|Запускаем рекламу|до сделки|^сделки\\.$)/;
  function replaceAboutParagraph(){{
    if (!ABOUT_PARAGRAPH) return;
    var about = document.querySelector('section[data-framer-name="About"]');
    if (!about) return;
    try {{
      var walker = document.createTreeWalker(about, NodeFilter.SHOW_TEXT, null);
      var nodes = [];
      var n;
      var didReplaceMain = false;
      while ((n = walker.nextNode())) nodes.push(n);
      nodes.forEach(function(node){{
        // Skip text nodes that live inside our custom tariff block.
        if (node.parentElement && node.parentElement.closest && node.parentElement.closest('[data-glavnoe-tariffs="1"]')) return;
        var raw = node.nodeValue;
        if (!raw) return;
        var t = raw.replace(/\\u00A0/g, ' ').trim();
        if (!t) return;
        if (t === AVITO_PARAGRAPH_FULL || t === ABOUT_PARAGRAPH) {{
          if (node.nodeValue !== ABOUT_PARAGRAPH) node.nodeValue = ABOUT_PARAGRAPH;
          didReplaceMain = true;
          return;
        }}
        // Original narrow fragment match — keeps legacy hidden refs cleared.
        if (AVITO_FRAGMENT_RE.test(t)) {{
          node.nodeValue = '';
          return;
        }}
        // Mobile wrap-span cleanup: <span> with no class, inline-block, text
        // carrying any unique Avito token — these never match a product
        // paragraph, only the master Avito one.
        var p = node.parentElement;
        if (p && p.tagName === 'SPAN' && !p.className) {{
          var cs;
          try {{ cs = window.getComputedStyle(p); }} catch(e) {{}}
          if (cs && cs.display === 'inline-block' && t.length <= 80) {{
            if (AVITO_WRAP_TOKEN_RE.test(t)) {{
              node.nodeValue = '';
            }}
          }}
        }}
      }});
      if (didReplaceMain) about.setAttribute('data-glavnoe-about-applied', '1');
    }} catch(e) {{}}
  }}

  // 4. Tariff container discovery on the LIVE DOM.
  //    Tariff cards section is .framer-17whp4j in the Avito master template.
  //    We also fall back to structural discovery (children with price tokens)
  //    so the block still works if Framer renames the class.
  var PRICE_RE = /\\d{{2,4}}\\s*k\\./;
  function findTariffContainer(){{
    var direct = document.querySelector('.framer-17whp4j');
    if (direct) return direct;
    var best = null;
    var nodes = document.querySelectorAll('div, ul, section');
    for (var i = 0; i < nodes.length; i++) {{
      var el = nodes[i];
      var kids = el.children;
      if (!kids || kids.length < 2 || kids.length > 5) continue;
      var ok = true;
      for (var j = 0; j < kids.length; j++) {{
        var txt = (kids[j].textContent || '').slice(0, 800);
        if (!PRICE_RE.test(txt)) {{ ok = false; break; }}
      }}
      if (ok) {{
        if (!best || el.outerHTML.length < best.outerHTML.length) best = el;
      }}
    }}
    return best;
  }}

  // 6. Extra offer block — plain in-flow text inserted as a sibling of the
  //    tariff container, inside the pricing section. Typography is copied
  //    from a real, already-rendered paragraph on the page so the block uses
  //    the same Suisse Intl font, sizes, line-heights, and colors as site
  //    body text, not a new style.
  function findSiteBodyRef(){{
    // Walk visible leaf text nodes, return the first paragraph-shape one
    // that matches site secondary body text: 14-22px regular Suisse Intl,
    // near-black with reduced opacity (rgba(0,0,0,0.4..0.7)). This is the
    // audience-card description style.
    var nodes = document.querySelectorAll('p, div, span');
    for (var i = 0; i < nodes.length; i++) {{
      var el = nodes[i];
      if (el.children && el.children.length > 0) continue;
      var t = (el.textContent || '').trim();
      if (t.length < 30) continue;
      var cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none') continue;
      var fs = parseFloat(cs.fontSize);
      if (fs < 14 || fs > 22) continue;
      if (cs.fontWeight !== '400') continue;
      if (!/Suisse/i.test(cs.fontFamily)) continue;
      // Only accept dark-on-light secondary text (audience descriptions etc.)
      if (/^rgba\\(0, 0, 0, 0\\.[3-7]/.test(cs.color)) return el;
    }}
    return null;
  }}
  function findSiteTitleRef(){{
    var nodes = document.querySelectorAll('p, div, span');
    var fallback = null;
    for (var i = 0; i < nodes.length; i++) {{
      var el = nodes[i];
      if (el.children && el.children.length > 0) continue;
      var t = (el.textContent || '').trim();
      if (t.length < 5 || t.length > 80) continue;
      var cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none') continue;
      var fs = parseFloat(cs.fontSize);
      if (fs < 14 || fs > 22) continue;
      if (!/Suisse/i.test(cs.fontFamily)) continue;
      var fw = parseInt(cs.fontWeight, 10);
      if (fw < 500) continue;
      if (cs.color === 'rgb(0, 0, 0)' || /rgba\\(0, 0, 0, 0\\.[7-9]/.test(cs.color)) return el;
      if (!fallback) fallback = el;
    }}
    return fallback;
  }}
  function copyTypography(target, ref){{
    if (!ref) return;
    var cs = getComputedStyle(ref);
    target.style.fontFamily = cs.fontFamily;
    target.style.fontSize = cs.fontSize;
    target.style.lineHeight = cs.lineHeight;
    target.style.fontWeight = cs.fontWeight;
    target.style.color = cs.color;
    target.style.letterSpacing = cs.letterSpacing;
  }}
  function injectExtraOfferBlock(){{
    if (document.querySelector('[data-glavnoe-extra-offer="1"]')) return false;
    var cont = findTariffContainer();
    if (!cont || !cont.parentNode) return false;
    var titleRef = findSiteTitleRef();
    var bodyRef = findSiteBodyRef();
    if (!titleRef || !bodyRef) return false; // wait until refs are ready

    var wrap = document.createElement('div');
    wrap.setAttribute('data-glavnoe-extra-offer', '1');
    wrap.style.marginTop = '64px';
    wrap.style.maxWidth = '720px';
    wrap.style.textAlign = 'left';

    var h = document.createElement('p');
    h.textContent = EXTRA_OFFER_TITLE;
    h.style.margin = '0 0 12px 0';
    copyTypography(h, titleRef);

    var p = document.createElement('p');
    p.textContent = EXTRA_OFFER_TEXT;
    p.style.margin = '0';
    copyTypography(p, bodyRef);

    wrap.appendChild(h);
    wrap.appendChild(p);

    cont.parentNode.insertBefore(wrap, cont.nextSibling);
    return true;
  }}

  // 6c. Hide big-number Avito subtitle ("Cтоимость целевого обращения...").
  //     Framer splits this phrase character-by-character into spans, so
  //     text-node REPLACEMENTS can't match. Find the element whose full
  //     textContent equals the subtitle and hide it.
  var BIG_NUM_SUBTITLE = 'Cтоимость целевого обращения на недвижимость бизнес и премиум-класса';
  var BIG_NUM_SUBTITLE_ALT = 'Стоимость целевого обращения на недвижимость бизнес и премиум-класса';
  function hideBigNumberSubtitle(){{
    var tc1 = document.querySelector('[data-framer-name="Tablet Card 1"]');
    if (!tc1) return false;
    var found = false;
    tc1.querySelectorAll('*').forEach(function(el){{
      if (el.getAttribute('data-glavnoe-subtitle-hidden') === '1') return;
      var t = (el.textContent || '').replace(/\\s+/g, ' ').trim();
      if (t === BIG_NUM_SUBTITLE || t === BIG_NUM_SUBTITLE_ALT) {{
        // Hide only if no other meaningful content nested next to it.
        el.style.display = 'none';
        el.setAttribute('data-glavnoe-subtitle-hidden', '1');
        found = true;
      }}
    }});
    return found;
  }}

  // 6b. Hide audience block ("Кому подходит") — 3-column white section
  //     between hero and tariffs. Per latest spec it does not match the
  //     product page visual so we remove it from the layout.
  function hideAudienceBlock(){{
    // The block is a <section> without data-framer-name inside
    // <section data-framer-name="About">. Identify it by its child
    // labels (01.5) / (Кому подходит).
    var about = document.querySelector('section[data-framer-name="About"]');
    if (!about) return false;
    var sections = about.querySelectorAll('section');
    for (var i = 0; i < sections.length; i++) {{
      var s = sections[i];
      if (s.getAttribute('data-glavnoe-audience-hidden') === '1') continue;
      var t = (s.textContent || '');
      if (/\\(Кому подходит\\)/.test(t) && /Девелопер|Девелоп|Застройщик|Агентств|Команд/.test(t)) {{
        s.style.display = 'none';
        s.setAttribute('data-glavnoe-audience-hidden', '1');
        return true;
      }}
    }}
    return false;
  }}

  // 7. Tariff CTA links — point both tier card buttons to Telegram
  //    (@ksandrbloger) with a pre-filled message that identifies source +
  //    product + tier. Sets only the href attribute on existing anchors.
  function wireTariffButtons(){{
    var cont = findTariffContainer();
    if (!cont) return false;
    var kids = cont.children;
    if (!kids || kids.length < 2) return false;
    var pairs = [
      [kids[0], TIER1_HREF],
      [kids[1], TIER2_HREF]
    ];
    for (var i = 0; i < pairs.length; i++) {{
      var card = pairs[i][0];
      var href = pairs[i][1];
      var anchors = card.querySelectorAll('a');
      for (var j = 0; j < anchors.length; j++) {{
        if (anchors[j].getAttribute('href') !== href) {{
          anchors[j].setAttribute('href', href);
        }}
      }}
    }}
    return true;
  }}

  // Carry the full desktop Tier 2 content into the mobile Tier 2 card.
  // Mobile variant of Tier 2 ships with only 3 bullet slots; desktop has 5
  // bullets plus a "Всё из тарифа «...»" header line. We clone an existing
  // mobile bullet row, swap its text, and append it for each missing bullet.
  function enrichMobileTier2(){{
    var cont = document.querySelector('.framer-17whp4j');
    if (!cont || cont.children.length < 2) return false;
    var tier2 = cont.children[1];
    if (tier2.getAttribute('data-glavnoe-mobile-tier2-enriched') === '1') return true;
    // Discover the bullet container — the deepest element that holds a text
    // node matching the FIRST product bullet. Climb to its parent: that's the
    // grid/flex wrapper that lays out all bullets in the mobile variant.
    var firstBulletText = TIER2_DESKTOP_BULLETS[0];
    var firstNode = null;
    var walker = document.createTreeWalker(tier2, NodeFilter.SHOW_TEXT, null);
    var n;
    while ((n = walker.nextNode())) {{
      var t = (n.nodeValue || '').trim();
      if (t === firstBulletText) {{
        var p = n.parentElement;
        // Climb until we find the bullet-row element (one whose textContent
        // equals exactly one bullet phrase, not more).
        while (p && p !== tier2) {{
          var pt = (p.textContent || '').replace(/\\s+/g, ' ').trim();
          if (pt === firstBulletText) {{ firstNode = p; }}
          else break;
          p = p.parentElement;
        }}
        if (firstNode) break;
      }}
    }}
    if (!firstNode) return false;
    var bulletParent = firstNode.parentElement;
    if (!bulletParent) return false;
    // Confirm bulletParent holds multiple bullet rows by checking siblings.
    var existingBullets = Array.from(bulletParent.children).filter(function(c){{
      var ct = (c.textContent || '').replace(/\\s+/g, ' ').trim();
      return TIER2_DESKTOP_BULLETS.indexOf(ct) !== -1;
    }});
    if (existingBullets.length < 2) return false;

    // Helper: clone the template bullet and replace every non-empty text leaf
    // so the clone carries `text` only (the first text leaf), with all later
    // duplicate text leaves cleared. Bullet-marker spans/icons stay intact.
    function makeBullet(text){{
      var clone = firstNode.cloneNode(true);
      var subWalker = document.createTreeWalker(clone, NodeFilter.SHOW_TEXT, null);
      var leafs = [];
      var nn;
      while ((nn = subWalker.nextNode())) leafs.push(nn);
      var assigned = false;
      leafs.forEach(function(lf){{
        var lt = (lf.nodeValue || '').trim();
        if (!lt) return;
        if (!assigned) {{
          lf.nodeValue = text;
          assigned = true;
        }} else {{
          // Wipe any further text leaf so the clone doesn't carry a stale
          // duplicate of the template bullet text.
          lf.nodeValue = '';
        }}
      }});
      return clone;
    }}

    // Determine which desktop bullets are missing in mobile variant.
    var presentTexts = existingBullets.map(function(c){{
      return (c.textContent || '').replace(/\\s+/g, ' ').trim();
    }});
    var missing = TIER2_DESKTOP_BULLETS.filter(function(b){{ return presentTexts.indexOf(b) === -1; }});
    if (missing.length === 0) {{
      tier2.setAttribute('data-glavnoe-mobile-tier2-enriched', '1');
      return true;
    }}
    missing.forEach(function(m){{
      var b = makeBullet(m);
      bulletParent.appendChild(b);
    }});

    // De-duplicate: traverse bulletParent children, hide any whose visible
    // text matches a previously-seen bullet text. Keep the first instance.
    var seen = {{}};
    Array.from(bulletParent.children).forEach(function(c){{
      var ct = (c.textContent || '').replace(/\\s+/g, ' ').trim();
      if (!ct) return;
      if (seen[ct]) {{
        c.style.display = 'none';
      }} else {{
        seen[ct] = true;
      }}
    }});

    // Inject "Всё из тарифа «...»" header at the top of bulletParent if absent.
    var headerText = TIER2_INCLUDED_LINE;
    var hasHeader = Array.from(bulletParent.children).some(function(c){{
      return (c.textContent || '').replace(/\\s+/g, ' ').trim() === headerText;
    }});
    if (!hasHeader && headerText) {{
      var headerNode = makeBullet(headerText);
      bulletParent.insertBefore(headerNode, bulletParent.firstChild);
    }}

    tier2.setAttribute('data-glavnoe-mobile-tier2-enriched', '1');
    return true;
  }}

  // 8. Custom tariff block — fully replace Framer's `.framer-17whp4j` (which
  //    ships a broken mobile Tier 2 with 3 English placeholder bullets) with
  //    a controlled HTML pair of cards in the site's visual style. All tariff
  //    text comes from this script, not from Framer SSR, so there is no
  //    mobile/desktop content divergence by design.
  function ensureCustomTariffStyles(){{
    if (document.getElementById('glavnoe-tariffs-css')) return;
    var st = document.createElement('style');
    st.id = 'glavnoe-tariffs-css';
    st.textContent = CUSTOM_TARIFF_CSS;
    (document.head || document.documentElement).appendChild(st);
  }}

  function buildBulletList(bullets){{
    var ul = document.createElement('ul');
    ul.setAttribute('data-bullets', '');
    for (var i = 0; i < bullets.length; i++) {{
      var li = document.createElement('li');
      li.textContent = bullets[i];
      ul.appendChild(li);
    }}
    return ul;
  }}

  function buildTariffCard(opts){{
    var card = document.createElement('article');
    card.setAttribute('data-tier', String(opts.index));
    card.setAttribute('data-tier-style', opts.isAccent ? 'dark' : 'light');

    var header = document.createElement('div');
    header.setAttribute('data-tier-header', '');
    var name = document.createElement('span');
    name.setAttribute('data-tier-name', '');
    name.textContent = opts.name;
    var desc = document.createElement('p');
    desc.setAttribute('data-tier-desc', '');
    desc.textContent = opts.desc;
    header.appendChild(name);
    header.appendChild(desc);
    card.appendChild(header);

    var priceBlock = document.createElement('div');
    priceBlock.setAttribute('data-price', '');
    var amount = document.createElement('span');
    amount.setAttribute('data-price-amount', '');
    amount.textContent = opts.price;
    var note = document.createElement('p');
    note.setAttribute('data-price-note', '');
    note.textContent = TIER_PRICE_NOTE;
    priceBlock.appendChild(amount);
    priceBlock.appendChild(note);
    card.appendChild(priceBlock);

    if (opts.includedLine) {{
      var inc = document.createElement('p');
      inc.setAttribute('data-included', '');
      inc.textContent = opts.includedLine;
      card.appendChild(inc);
    }}

    card.appendChild(buildBulletList(opts.bullets || []));

    var cta = document.createElement('a');
    cta.setAttribute('data-cta', '');
    cta.setAttribute('href', opts.href);
    cta.setAttribute('target', '_blank');
    cta.setAttribute('rel', 'noopener');
    cta.textContent = TIER_BUTTON_LABEL;
    card.appendChild(cta);

    return card;
  }}

  // Some Framer ancestor wrappers ship overflow:clip / overflow-x:clip and are
  // narrower than the viewport, which would clip our full-bleed tariff block.
  // We open them up only for the chain leading to the tariff container, and
  // only when the ancestor is itself narrower than the viewport. Full-width
  // ancestors keep their original overflow.
  function unclipAncestorsTo(el){{
    var cur = el.parentElement;
    while (cur && cur !== document.body) {{
      try {{
        var cs = window.getComputedStyle(cur);
        var r = cur.getBoundingClientRect();
        var clipped = cs.overflowX === 'clip' || cs.overflowX === 'hidden' || cs.overflow === 'clip' || cs.overflow === 'hidden';
        var isNarrower = (window.innerWidth - r.width) > 2;
        if (clipped && isNarrower) {{
          cur.style.overflow = 'visible';
          cur.style.overflowX = 'visible';
          cur.setAttribute('data-glavnoe-unclipped', '1');
        }}
      }} catch(e) {{}}
      cur = cur.parentElement;
    }}
  }}

  function renderCustomTariffs(){{
    if (document.querySelector('[data-glavnoe-tariffs="1"]')) return true;
    var cont = findTariffContainer();
    if (!cont || !cont.parentNode) return false;
    if (!TIERS || TIERS.length === 0) return false;

    ensureCustomTariffStyles();
    unclipAncestorsTo(cont);

    var wrap = document.createElement('div');
    wrap.setAttribute('data-glavnoe-tariffs', '1');

    var grid = document.createElement('div');
    grid.setAttribute('data-tariff-grid', '');
    grid.setAttribute('data-tier-count', String(TIERS.length));

    for (var ti = 0; ti < TIERS.length; ti++) {{
      var t = TIERS[ti];
      grid.appendChild(buildTariffCard({{
        index: ti + 1,
        isAccent: ti === TIERS.length - 1,
        name: t.name,
        desc: t.desc,
        price: t.price,
        bullets: t.bullets,
        href: t.href,
        includedLine: t.included_line || '',
      }}));
    }}

    wrap.appendChild(grid);
    cont.parentNode.insertBefore(wrap, cont);

    // Replace, not mask: original Framer tariff container is fully superseded
    // by our controlled block — hiding it removes nothing the user can see.
    cont.style.display = 'none';
    cont.setAttribute('data-glavnoe-tariff-replaced', '1');
    return true;
  }}

  function applyAll(){{
    fullSweep();
    replaceAboutParagraph();
    renderCustomTariffs();
    injectExtraOfferBlock();
    wireTariffButtons();
    hideAudienceBlock();
    hideBigNumberSubtitle();
  }}
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', function(){{
      startObserver();
      applyAll();
    }});
  }}
  window.addEventListener('load', function(){{
    applyAll();
    // Run applyAll every 500ms for 30 seconds, then disconnect observer.
    // This catches Framer's late-added carousel slides (subtitle elements
    // appear around 12-14s).
    var ticks = 0;
    var iv = setInterval(function(){{
      applyAll();
      ticks++;
      if (ticks >= 60) {{
        clearInterval(iv);
        try {{ observer.disconnect(); }} catch(e) {{}}
      }}
    }}, 500);
  }});
}})();
</script>
"""


CUSTOM_TARIFF_CSS = """
[data-glavnoe-tariffs="1"] {
  display: block;
  background: #000;
  border-radius: 0;
  margin-left: calc(-50vw + 50%);
  margin-right: calc(-50vw + 50%);
  width: 100vw;
  padding: 80px 48px;
  box-sizing: border-box;
  font-family: "Suisse Intl","Suisse Intl Placeholder",sans-serif;
}
[data-glavnoe-tariffs="1"] [data-tariff-grid] {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  width: 100%;
}
[data-glavnoe-tariffs="1"] [data-tariff-grid][data-tier-count="3"] {
  grid-template-columns: repeat(3, 1fr);
}
[data-glavnoe-tariffs="1"] article[data-tier] {
  background: #fff;
  color: #000;
  border-radius: 24px;
  padding: 36px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-width: 0;
}
[data-glavnoe-tariffs="1"] article[data-tier-style="dark"] {
  background: linear-gradient(151deg, rgb(249, 69, 45) 26%, rgb(255, 123, 106) 100%);
  color: #fff;
}
[data-glavnoe-tariffs="1"] [data-tier-name] {
  font-family: "DM Sans","DM Sans Placeholder",sans-serif;
  font-weight: 600;
  font-size: 18px;
  letter-spacing: -0.36px;
  line-height: 24px;
  text-transform: uppercase;
  display: block;
}
[data-glavnoe-tariffs="1"] [data-tier-desc] {
  font-weight: 400;
  font-size: 16px;
  line-height: 22px;
  margin: 8px 0 0 0;
}
[data-glavnoe-tariffs="1"] article[data-tier-style="light"] [data-tier-desc] {
  color: rgba(0, 0, 0, 0.5);
}
[data-glavnoe-tariffs="1"] article[data-tier-style="dark"] [data-tier-desc] {
  color: rgba(255, 255, 255, 0.85);
}
[data-glavnoe-tariffs="1"] [data-price-amount] {
  font-family: "DM Sans","DM Sans Placeholder",sans-serif;
  font-weight: 600;
  font-size: 44px;
  line-height: 1;
  letter-spacing: -0.88px;
  display: block;
}
[data-glavnoe-tariffs="1"] [data-price-note] {
  font-weight: 400;
  font-size: 13px;
  line-height: 18px;
  margin: 10px 0 0 0;
}
[data-glavnoe-tariffs="1"] article[data-tier-style="light"] [data-price-note] {
  color: rgba(0, 0, 0, 0.5);
}
[data-glavnoe-tariffs="1"] article[data-tier-style="dark"] [data-price-note] {
  color: rgba(255, 255, 255, 0.85);
}
[data-glavnoe-tariffs="1"] [data-included] {
  font-weight: 500;
  font-size: 14px;
  line-height: 20px;
  margin: 0;
  opacity: 0.9;
}
[data-glavnoe-tariffs="1"] [data-bullets] {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
[data-glavnoe-tariffs="1"] [data-bullets] li {
  font-weight: 400;
  font-size: 15px;
  line-height: 22px;
  padding-left: 18px;
  position: relative;
}
[data-glavnoe-tariffs="1"] [data-bullets] li::before {
  content: "—";
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0.55;
}
[data-glavnoe-tariffs="1"] [data-cta] {
  align-self: flex-start;
  padding: 14px 24px;
  border-radius: 100px;
  font-family: "DM Sans","DM Sans Placeholder",sans-serif;
  font-weight: 600;
  font-size: 14px;
  line-height: 16px;
  letter-spacing: -0.28px;
  text-transform: uppercase;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  margin-top: auto;
  transition: opacity 0.2s ease;
}
[data-glavnoe-tariffs="1"] [data-cta]:hover {
  opacity: 0.85;
}
[data-glavnoe-tariffs="1"] article[data-tier-style="light"] [data-cta] {
  background: #000;
  color: #fff;
}
[data-glavnoe-tariffs="1"] article[data-tier-style="dark"] [data-cta] {
  background: #fff;
  color: rgb(249, 69, 45);
}
@media (max-width: 1100px) {
  [data-glavnoe-tariffs="1"] [data-tariff-grid][data-tier-count="3"] {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 810px) {
  [data-glavnoe-tariffs="1"] {
    padding: 48px 20px;
    border-radius: 0;
  }
  [data-glavnoe-tariffs="1"] [data-tariff-grid],
  [data-glavnoe-tariffs="1"] [data-tariff-grid][data-tier-count="3"] {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  [data-glavnoe-tariffs="1"] article[data-tier] {
    padding: 28px 24px;
    gap: 20px;
  }
  [data-glavnoe-tariffs="1"] [data-price-amount] {
    font-size: 36px;
    letter-spacing: -0.72px;
  }
}
"""


def main():
    import re
    for slug, cfg in PRODUCTS.items():
        target = ROOT / 'product' / slug / 'index.html'
        html = target.read_text(encoding='utf-8')
        # Drop any prior override scripts (wherever they sit).
        html = re.sub(
            r'<script data-glavnoe-product-override="[^"]+">[\s\S]*?</script>',
            '',
            html,
            count=0,
        )
        # Extract desktop Tier 2 bullets (the target strings) from the per-product
        # config so the override can carry them into the mobile Tier 2 card.
        tier2_desktop_targets = [pair[1] for pair in cfg.get('tier2_bullets_src', [])]
        snippet = OVERRIDE_TMPL.format(
            slug=slug,
            replacements_json=json.dumps(cfg['replacements'], ensure_ascii=False),
            title_json=json.dumps(cfg['page_title'], ensure_ascii=False),
            desc_json=json.dumps(cfg['meta_description'], ensure_ascii=False),
            about_json=json.dumps(cfg.get('about_paragraph'), ensure_ascii=False),
            tier1_href_json=json.dumps(cfg['tier1_href'], ensure_ascii=False),
            tier2_href_json=json.dumps(cfg['tier2_href'], ensure_ascii=False),
            tier2_desktop_bullets_json=json.dumps(tier2_desktop_targets, ensure_ascii=False),
            tier2_included_line_json=json.dumps(cfg.get('tier2_included_line', ''), ensure_ascii=False),
            tiers_json=json.dumps(cfg['tiers'], ensure_ascii=False),
            custom_tariff_css_json=json.dumps(CUSTOM_TARIFF_CSS, ensure_ascii=False),
        )
        # Inject right after the opening <body ...> tag so the MutationObserver
        # starts watching BEFORE Framer's SSR children are parsed in. That way
        # text-node substitutions happen as nodes enter the DOM, before the
        # first paint can show "Авито Адс".
        m = re.search(r'<body\b[^>]*>', html)
        if m:
            insertion = m.end()
            html = html[:insertion] + snippet + html[insertion:]
        else:
            # Fallback: prepend to </body> if no opening tag matched (shouldn't happen).
            html = html.replace('</body>', snippet + '</body>')
        target.write_text(html, encoding='utf-8')
        print(f'wrote {target.relative_to(ROOT)} ({len(html)} bytes)')


if __name__ == '__main__':
    main()
