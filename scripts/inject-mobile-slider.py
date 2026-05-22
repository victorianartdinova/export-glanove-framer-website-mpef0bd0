#!/usr/bin/env python3
"""Mobile horizontal scroll-snap slider for tariff cards on 4 product pages.
On desktop (≥1100px) — grid as before. On mobile/tablet (<1100px) — карточки
выстраиваются горизонтально, swipe пальцем, scroll-snap к каждой карточке.
Точные индикаторы через тонкий scrollbar."""
from pathlib import Path

ROOT = Path('/root/framerexport/full-site-export-may21')
PAGES = ['content-product', 'product-statii', 'product-telegram', 'youtube-product']

CSS = (
  '<style id="glavnoe-tariff-mobile-slider">'
  '@media (max-width:1100px){'
    # Container: prevent body overflow, allow internal scroll
    '[data-glavnoe-tariffs="1"]{padding-left:0!important;padding-right:0!important;}'
    '[data-glavnoe-tariffs="1"] [data-tariff-group-label]{margin-left:20px;}'
    # Grid → horizontal slider
    '[data-glavnoe-tariffs="1"] [data-tariff-grid],'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid][data-tier-count="2"],'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid][data-tier-count="3"],'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid][data-group="ads"],'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid][data-group="complex"]{'
      'display:flex!important;flex-direction:row!important;'
      'grid-template-columns:none!important;'
      'overflow-x:auto;'
      'scroll-snap-type:x mandatory;'
      'gap:12px;'
      'padding:0 20px 16px 20px;'
      '-webkit-overflow-scrolling:touch;'
      'scrollbar-width:thin;'
      'scrollbar-color:rgba(255,255,255,0.3) transparent;'
    '}'
    # Each card — fixed width, snap to start
    '[data-glavnoe-tariffs="1"] [data-tariff-grid] article[data-tier]{'
      'flex:0 0 88vw;'
      'max-width:380px;'
      'scroll-snap-align:start;'
      'scroll-snap-stop:always;'
    '}'
    # Webkit scrollbar styling
    '[data-glavnoe-tariffs="1"] [data-tariff-grid]::-webkit-scrollbar{height:6px;}'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid]::-webkit-scrollbar-track{background:rgba(255,255,255,0.05);border-radius:3px;}'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid]::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.35);border-radius:3px;}'
  '}'
  # Tablet ≥640 — карточки чуть шире чтобы 1.5 видно было (намёк на слайдер)
  '@media (min-width:640px) and (max-width:1100px){'
    '[data-glavnoe-tariffs="1"] [data-tariff-grid] article[data-tier]{'
      'flex:0 0 60vw;max-width:480px;'
    '}'
  '}'
  '</style>'
)

MARK = 'id="glavnoe-tariff-mobile-slider"'

for slug in PAGES:
    f = ROOT / 'product' / slug / 'index.html'
    h = f.read_text(encoding='utf-8')
    if MARK in h:
        print(f'SKIP {slug}')
        continue
    new = h.replace('</head>', CSS + '</head>', 1)
    if new == h:
        print(f'FAIL {slug}')
        continue
    f.write_text(new, encoding='utf-8')
    print(f'OK {slug}')
