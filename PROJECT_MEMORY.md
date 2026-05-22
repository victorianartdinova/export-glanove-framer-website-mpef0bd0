# PROJECT MEMORY

## PROJECT

/root/framerexport/full-site-export-may21

repo:
victorianartdinova/export-glanove-framer-website-mpef0bd0

branch:
runtime-restore-may21

preview:
http://srv1207957.hstgr.cloud:3343/

---

## SOURCE OF TRUTH

product/avito-ads/index.html

Avito Ads = MASTER TEMPLATE

---

## FORBIDDEN

/root/glavnoe-real
React ProductPage
src/products/*
src/templates/ProductPage.tsx
new components
new layouts
redesign

---

## PRODUCT PAGE RULE

All product pages must inherit Avito Ads structure.

Allowed:
- text
- prices
- images
- CTA
- FAQ

Not allowed:
- new sections
- different process block
- different result block
- different tariff structure

---

## CURRENT STATUS

### DONE

- homepage restored
- footer localized
- social links fixed
- partner block fixed
- pre-footer fixed
- 4 product pages cloned byte-for-byte from product/avito-ads/index.html (md5 4a3f7fec9d5850130ddcf89083693e9a)
- product-specific text/prices/CTA applied via post-hydration override script
- all 5 pages share identical structure: hero (inset) → audience 3 cols → 2 tariff cards → "КАК БУДЕМ РАБОТАТЬ" → about → big number → partners → pre-footer → footer

### NOT DONE

- side-by-side comparison approved by Vika
- commit of uncommitted changes
- tablet/mobile verification by Vika

---

## RESEARCH CONCLUSIONS

Framer Export:
template → products.json → generator → pages

Do not use hydration debugging before locating content source.

Do not use runtime patches as content management.

---

## IMPLEMENTATION NOTES (2026-05-21)

Approach: clone master HTML byte-for-byte into 4 sibling product directories.
Insert a single `<script data-glavnoe-product-override>` block before `</body>`
that runs once after Framer hydration completes (load + 2.8s) and substitutes
content text nodes via two-pass placeholder mapping:

1. Pass 1 — exact-match source text → unique `PH<n>` placeholder.
2. Pass 2 — placeholder → product-specific target text.

EXACT match only (no substring). Substring matching is unsafe because some
target strings contain source substrings (e.g. "280 k." contains "80 k." →
re-run would mangle into "2150 k."). Single deterministic pass at +2.8s after
window.load.

### Files

- product/{content-product, product-statii, product-telegram, youtube-product}/index.html — 4 byte-for-byte clones of avito-ads + injected override script.
- scripts/clone-and-content.py — re-cloning script (regenerates 4 child files from master).
- scripts/inject-override.py — injects post-hydration content override script into each child HTML.
- /root/snap-product-clones.mjs — playwright snapshot script (5 pages × 3 viewports).
- /tmp/product-clones-may21/ — screenshots desktop/tablet/mobile.

### Content map (per product)

| Field | content-product | product-statii | product-telegram | youtube-product |
|--|--|--|--|--|
| Hero h2 | Контент-маркетинг | Рекламная стратегия | Лидген Telegram | Личный бренд YouTube |
| Hero caption-left | (контент + СМИ) | (стратегия + прогноз) | (трафик + канал) | (продюсирование) |
| Hero caption-right | контент/стратегия | стратегия/медиа | лиды/Telegram | охваты/YouTube |
| Tier 1 name | КОНТЕНТ | МЕДИАПЛАН | ЗАПУСК РЕКЛАМЫ | ЗАПУСК КАНАЛА |
| Tier 1 price | 150 k. | 200 k. | 165 k. | 180 k. |
| Tier 2 name | КОНТЕНТ + HR-БРЕНД | СТРАТЕГИЯ + ЗАПУСК | РЕКЛАМА + КАНАЛ | КАНАЛ + ПРОДЮСИРОВАНИЕ |
| Tier 2 price | 280 k. | 400 k. | 220 k. | 300 k. |
| Big number | 500+ | 300+ | 800+ | 50+ |
| Stat label | запусков контент-систем | рекламных стратегий для застройщиков | заявок из Telegram-рекламы | личных брендов основателей |
| Page <title> | Контент-маркетинг \| ГЛАВНОЕ | Рекламная стратегия \| ГЛАВНОЕ | Лидген Telegram \| ГЛАВНОЕ | Личный бренд YouTube \| ГЛАВНОЕ |

### Verified

- 5 pages render with identical structure on desktop 1440.
- Master Avito Ads untouched (md5 4a3f7fec9d5850130ddcf89083693e9a preserved).
- Override script substitutes exactly the listed fields; all other content (3 audience columns, process steps, partner logos, footer) inherits from master.

### Known limitations

- Long multi-line about paragraph (`Запускаем рекламу на Авито…`) is rendered by Framer as 6 wrap-spans; not yet substituted per product (visible paragraph is product-specific because Framer hydrates it from CMS per URL; the hidden measure-ref still shows avito text but is `display: none`).
- 3 audience columns ("Кому подходит") are filled by Framer CMS per slug, not by override script. They already differ per product, matching Vika's intent.

---

## LAST VERIFIED STATE

date:
2026-05-21

commit:
89d89bb (HEAD of runtime-restore-may21) — uncommitted changes on top: 4 product HTML files + scripts/.

status:
4 product pages match Avito Ads structure (desktop verified via puppeteer screenshots). Awaiting Vika's approval before commit.

---

## NEXT TASK

1. Vika to approve side-by-side comparison.
2. On approve: commit changes — `feat(products): 4 product pages as byte-for-byte clones of Avito Ads master with content override`.
3. Verify tablet (810) and mobile (390) viewports — screenshots already saved in /tmp/product-clones-may21/, need visual approval.
4. Update CURRENT_TASK.md status.
