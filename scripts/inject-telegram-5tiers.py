#!/usr/bin/env python3
"""Telegram-страница: 5 тарифов в 2 группах (по презентации Glavnoe тарифы.pdf 21.05).
Группа A: "Если нужна только реклама" (Telegram ads 100k, Telegram ads + воронки 120k)
Группа B: "Если нужен комплекс работ" (Студия 145k, Дуплекс 165k, Пентхаус 240k)

Меняет:
1. var TIERS — 5 объектов, у каждого поле "group": "ads"|"complex"
2. renderCustomTariffs — рисует 2 grid-блока с подписями вместо одного
3. Inject CSS для подзаголовка-капсулы и responsive 3 viewport
"""
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path('/root/framerexport/full-site-export-may21')
PRODUCT = 'Лидген Telegram'
F = ROOT / 'product' / 'product-telegram' / 'index.html'

def href(tier_name):
    text = f"Здравствуйте! Пишу с сайта ГЛАВНОЕ, хочу обсудить продукт: {PRODUCT}. Интересует тариф: {tier_name}."
    return f"https://t.me/ksandrbloger?text={quote(text)}"

TIERS = [
    # === ГРУППА A: ЕСЛИ НУЖНА ТОЛЬКО РЕКЛАМА ===
    {
        "group": "ads",
        "name": "TELEGRAM ADS",
        "desc": "Подключаем рекламу на постоплату — без вашего юрлица и предоплат.",
        "price": "100 k.",
        "bullets": [
            "15 запущенных связок, прохождение модерации на постоплату",
            "2 созвона в zoom и чат-поддержка",
            "15 графических баннеров для запуска РК",
            "Сводная таблица: стоимость лида, подписки, потраченный РК. 2 встречи с отделом продаж «План/факт»",
            "1 созвон с брокерами по обработке",
            "Telegram Ads: подключение постоплаты. 15 запущенных связок, итоговый отчёт"
        ],
        "href": href("TELEGRAM ADS"),
        "included_line": None
    },
    {
        "group": "ads",
        "name": "TELEGRAM ADS + ВОРОНКИ",
        "desc": "Реклама + посадочные посты + подготовка канала к модерации.",
        "price": "120 k.",
        "bullets": [
            "15 запущенных связок, прохождение модерации на постоплату",
            "Техническое задание на посадочные посты для вашей команды",
            "15 графических баннеров для запуска РК",
            "Сводная таблица: стоимость лида, подписки, потраченный РК. 4 встречи с отделом продаж «План/факт»",
            "4 созвона в zoom и чат-поддержка",
            "2 созвона с брокерами по обработке",
            "Подготовка канала к модерации: проверка и список требований к контенту",
            "Автоматизация приёма обращений: бот WhatsApp/Telegram + связка с AMO CRM, WhatsApp-автоответы"
        ],
        "href": href("TELEGRAM ADS + ВОРОНКИ"),
        "included_line": None
    },
    # === ГРУППА B: ЕСЛИ НУЖЕН КОМПЛЕКС РАБОТ ===
    {
        "group": "complex",
        "name": "СТУДИЯ",
        "desc": "Подойдёт, если хотите затестить источник.",
        "price": "145 k.",
        "bullets": [
            "15 публикаций и контент-план",
            "Адаптация фир. стиля для telegram-канала (12 постов + 2 gif)",
            "2 созвона в zoom и чат-поддержка",
            "1 созвон с брокерами по обработке",
            "Автоматизация приёма обращений: бот WhatsApp/Telegram + связка с AMO CRM, WhatsApp-автоответы",
            "Telegram Ads: подключение постоплаты. 5 запущенных связок, итоговый отчёт"
        ],
        "href": href("СТУДИЯ"),
        "included_line": None
    },
    {
        "group": "complex",
        "name": "ДУПЛЕКС",
        "desc": "Оптимальный, если не планируете выпускать много контента.",
        "price": "165 k.",
        "bullets": [
            "30 публикаций, 10 сториз, 4 сценария для голосовых, монтаж 1 ролика, pdf-каталог, 5 Gif-постов, контент-план",
            "Адаптация фир. стиля для telegram-канала (12 постов + 2 gif)",
            "2 созвона в zoom и чат-поддержка",
            "1 созвон с брокерами по обработке",
            "Автоматизация приёма обращений: бот WhatsApp/Telegram + связка с AMO CRM, WhatsApp-автоответы",
            "Telegram Ads: подключение постоплаты. 15 запущенных связок, итоговый отчёт"
        ],
        "href": href("ДУПЛЕКС"),
        "included_line": "Всё из тарифа «Студия»"
    },
    {
        "group": "complex",
        "name": "ПЕНТХАУС",
        "desc": "Плотно интегрируемся в отдел продаж — каждый контакт работает как бетонная плита.",
        "price": "240 k.",
        "bullets": [
            "60 публикаций, 20 сториз, 10 сценариев для голосовых, монтаж 2 роликов, pdf-каталог, 15 Gif-постов, контент-план",
            "Адаптация фир. стиля для telegram-канала (12 постов + 2 gif)",
            "4 созвона в zoom и чат-поддержка",
            "2 созвона с брокерами по обработке",
            "Автоматизация приёма обращений: бот WhatsApp/Telegram + связка с AMO CRM, WhatsApp-автоответы",
            "Telegram Ads: подключение постоплаты. 15 запущенных связок, итоговый отчёт"
        ],
        "href": href("ПЕНТХАУС"),
        "included_line": "Всё из тарифа «Дуплекс»"
    },
]

# 1) Replace TIERS array
html = F.read_text(encoding='utf-8')
m = re.search(r'(var\s+TIERS\s*=\s*)(\[.*?\])(\s*;)', html, re.DOTALL)
assert m, "TIERS not found"
new_tiers_json = json.dumps(TIERS, ensure_ascii=False)
html = html[:m.start(2)] + new_tiers_json + html[m.end(2):]

# 2) Replace renderCustomTariffs with grouping version
NEW_RENDER = r'''function renderCustomTariffs(){
    if (document.querySelector('[data-glavnoe-tariffs="1"]')) return true;
    var cont = findTariffContainer();
    if (!cont || !cont.parentNode) return false;
    if (!TIERS || TIERS.length === 0) return false;

    ensureCustomTariffStyles();
    unclipAncestorsTo(cont);

    var wrap = document.createElement('div');
    wrap.setAttribute('data-glavnoe-tariffs', '1');

    // Group tiers by .group; if no group field — single group "default"
    var groups = {};
    var order = [];
    for (var i = 0; i < TIERS.length; i++) {
      var g = TIERS[i].group || 'default';
      if (!groups[g]) { groups[g] = []; order.push(g); }
      groups[g].push(TIERS[i]);
    }

    var GROUP_LABELS = {
      ads: 'Если нужна только реклама',
      complex: 'Если нужен комплекс работ'
    };

    for (var gi = 0; gi < order.length; gi++) {
      var gKey = order[gi];
      var gTiers = groups[gKey];

      if (GROUP_LABELS[gKey]) {
        var label = document.createElement('div');
        label.setAttribute('data-tariff-group-label', '');
        label.textContent = GROUP_LABELS[gKey];
        wrap.appendChild(label);
      }

      var grid = document.createElement('div');
      grid.setAttribute('data-tariff-grid', '');
      grid.setAttribute('data-tier-count', String(gTiers.length));
      grid.setAttribute('data-group', gKey);

      for (var ti = 0; ti < gTiers.length; ti++) {
        var t = gTiers[ti];
        grid.appendChild(buildTariffCard({
          index: ti + 1,
          isAccent: ti === gTiers.length - 1,
          name: t.name,
          desc: t.desc,
          price: t.price,
          bullets: t.bullets,
          href: t.href,
          includedLine: t.included_line || '',
        }));
      }
      wrap.appendChild(grid);
    }

    cont.parentNode.insertBefore(wrap, cont);
    cont.style.display = 'none';
    cont.setAttribute('data-glavnoe-tariff-replaced', '1');
    return true;
  }'''

m2 = re.search(r'function\s+renderCustomTariffs\s*\([^)]*\)\s*\{', html)
assert m2, "renderCustomTariffs not found"
# Brace match to find function end
depth = 0
i = m2.end() - 1
while i < len(html):
    c = html[i]
    if c == '{':
        depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            break
    i += 1
old_func_end = i + 1
html = html[:m2.start()] + NEW_RENDER + html[old_func_end:]

# 3) Inject extra CSS for group labels + responsive
EXTRA_CSS = (
    '<style id="glavnoe-telegram-groups">'
    '[data-glavnoe-tariffs="1"] [data-tariff-group-label]{'
    'display:inline-block;'
    'background:rgba(255,255,255,0.08);'
    'color:#fff;'
    'border:1px solid rgba(255,255,255,0.2);'
    'border-radius:100px;'
    'padding:10px 22px;'
    'font-family:"DM Sans","DM Sans Placeholder",sans-serif;'
    'font-weight:600;font-size:14px;line-height:18px;'
    'text-transform:uppercase;letter-spacing:0.4px;'
    'margin:0 0 24px 0;'
    '}'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid]:not(:last-child){margin-bottom:48px;}'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid][data-group="ads"]{'
    'grid-template-columns:1fr 1fr;'
    '}'
    '@media (max-width:1100px){'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid][data-group="ads"],'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid][data-group="complex"]'
    '{grid-template-columns:1fr;}'
    '}'
    '@media (max-width:810px){'
    '[data-glavnoe-tariffs="1"] [data-tariff-group-label]{'
    'font-size:12px;padding:8px 16px;margin-bottom:16px;'
    '}'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid]:not(:last-child){margin-bottom:32px;}'
    '}'
    '</style>'
)
MARK = 'id="glavnoe-telegram-groups"'
if MARK not in html:
    html = html.replace('</head>', EXTRA_CSS + '</head>', 1)

F.write_text(html, encoding='utf-8')
print('OK product-telegram: 5 tiers in 2 groups, render + CSS injected')
