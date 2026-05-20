# Ночная сессия 2026-05-20 → 2026-05-21 — статус и PENDING

> Вика выдала разрешение на ночную автономную работу по списку задач без доп. approve.
> Сделано в эту сессию + что нужно от Вики дальше.

---

## ✅ Сделано в эту ночь (после approve checkpoint)

### 1. Footer labels = header (3 ручные правки Вики)
- Footer «Карта сайта» полностью синхронизирован с header menu: **Главная / Услуги / Кейсы / Результаты / Статьи / Написать CEO**.
- «Отдел заботы 💙» теперь ведёт на `https://t.me/ksandrbloger` (контакт Саши).
- «тг с пользой» теперь ведёт на `https://t.me/glavnoe_channel` (канал ГЛАВНОЕ).
- Mail link href: `mailto:dummy@mail.com` → `mailto:hello@glavnoe.com`.
- Instagram link href в JS chunk приведён к agency-аккаунту.
- Применено к 16 HTML + JS chunk `script_main.B9JEDTsv.mjs`.
- Verify: `grep -roE '>(О компании|Цены|Связаться)<'` → 0 совпадений.

### 2. Бренд-метаданные «Fuel - Premium Agency & Portfolio» → «ГЛАВНОЕ» (15 HTML)
Заменены title, og:title, twitter:title, meta description, og:description, twitter:description.

Использован каноничный текст из `/root/glavnoe-site/data/siteConfig.ts`:
- **Title default**: «ГЛАВНОЕ — стратегический маркетинг для застройщиков»
- **Description**: «Стратегические партнёры по маркетингу для застройщиков. Performance-маркетинг, Telegram, Авито, стратегия продвижения недвижимости.»

Конкретные titles по страницам:
- `/` → «ГЛАВНОЕ — стратегический маркетинг для застройщиков»
- `/cases/portfolio/` → «Кейсы | ГЛАВНОЕ»
- `/product/авито-адс/` → «Авито Адс | ГЛАВНОЕ»
- `/product/content-product/` → «Контент-продукт | ГЛАВНОЕ»
- `/product/product-statii/` → «Статьи как продукт | ГЛАВНОЕ»
- `/product/product-telegram/` → «Лидген Telegram | ГЛАВНОЕ»
- `/product/youtube-product/` → «Личный бренд YouTube | ГЛАВНОЕ»
- `/404/` → «Страница не найдена | ГЛАВНОЕ»
- Case-страницы (`work/case-*`) — суффикс ` - Fuel - Premium Agency & Portfolio` срезан до ` | ГЛАВНОЕ`, сами тайтлы кейсов уже осмысленные.

### 3. Avito footer baseline fix
В файле `product/%D0%B0%D0%B2%D0%B8%D1%82%D0%BE-%D0%B0%D0%B4%D1%81/index.html` 4-й слот футера показывал «Кейсы» дважды из-за двойного применения скрипта через симлинк `product/avito-ads`. Исправлено: 4-й слот теперь «Результаты», все 6 footer labels совпадают с header.

---

## ⏸ PENDING (требует решений Вики или контента)

### A. Avito Ads — Cyrillic URL 404 на static server
**Проблема**: URL `/product/%D0%B0%D0%B2%D0%B8%D1%82%D0%BE-%D0%B0%D0%B4%D1%81/` отдаёт 404 на `serve`-static-server (наш preview). Симлинк `product/avito-ads` уже создан и работает (`/product/avito-ads/` → 200).

**Что нужно от Вики**:
- (a) ОК ли перейти на ASCII-slug `avito-ads` как каноничный URL? Потребуется в Framer Studio сменить slug страницы на `avito-ads`.
- ИЛИ (b) Хостинг (Vercel/Netlify) сам декодирует UTF-8 paths — тогда оставить кириллицу, симлинк только для локального preview.

Если (a) — нужно поправить canonical OG URLs и Open Graph metadata по всем 15 файлам.

### B. Avito Ads — пустые секции в hero/middle (visual bug на desktop)
Скрин: `/tmp/may21-night/avito-via-symlink-desktop.png`. После hero «Авито Адс» 3-4 пустые белые секции до блока «1000+».

**Гипотеза**: Framer CMS-collection для подразделов Avito пустая, либо контент-блоки не созданы в Framer Studio. Это не правится в export-side — нужно либо наполнить в Framer и re-export, либо ручная вставка HTML по образцу другого продукта.

**Что нужно от Вики**: контент для middle-секций Avito Ads (заголовок секции, описание, картинка, метрики) — либо разрешение скопировать структуру с product-telegram и заменить тексты.

### C. cases/portfolio — пустая сетка кейсов
Hero страницы рендерится, но grid кейсов пустой. CMS-коллекция кейсов не подключена или без записей.

**Что нужно от Вики**: 
- Список case-карточек: 4 уже есть как отдельные страницы (case-aag-promostranicy, case-spb-15mln, regardis-telegram-ads-premium). Это всё или добавить ещё?
- Решение: подгружать через CMS-коллекцию (Framer Studio) или вставить статические карточки в `cases/portfolio/index.html` по образцу.

### D. Product card links на главной
**Проблема**: на homepage НЕТ внутренних ссылок на продуктовые страницы. `grep 'href="(\./|\.\./|/)product/' index.html` → 0 совпадений. Пользователь не может перейти из главной на /product/avito-ads/, /product/product-telegram/ и т.д.

**Что нужно от Вики**: вероятно карточки продуктов на главной существуют визуально, но без href. Нужно решить:
- Список продуктовых ссылок (slug → URL): avito-adс, content-product, product-statii, product-telegram, youtube-product.
- Из текущего export текст продуктовых карточек на главной непонятен — «Лидген в телеграм / Москва», «Лидген в телеграм / СПб», «Девелопмент / СПб» — это product cards или другая секция?

### E. Reviews / mobile checks (390/810/1440)
Скриншоты сняты в `/tmp/may21-night/`:
- home/cases/p-content/p-statii/p-telegram/p-youtube × desktop+tablet+mobile.
- p-avito-* — 6-9KB (404, см. A).

Visual review не проводила полностью — это требует side-by-side с эталонным дизайном Framer-сайта, который у меня нет под рукой как референс. Из быстрого взгляда: home-desktop имеет несколько пустых чёрных/белых полос между секциями (как у Avito) — может быть design intent или CMS-пустоты.

**Что нужно от Вики**: эталонный URL `https://glanove.framer.website/` (или dev-preview из Framer Studio) — сделаю side-by-side по всем секциям × 3 viewports и батч-фикс.

### F. Дублирование tariff components
**Проблема**: непонятно куда именно. На `product/product-telegram/` есть tariff cards (3 шт.: 120 000 / 165 000 / 200 000). На других product-страницах надо ли такие же?

**Что нужно от Вики**: список «где нужны tariff cards» + цены + что включает каждый тариф.

### G. Blog page titles — placeholder texts
Все 4 блога имеют английские placeholder-названия из Framer template:
- `blog/all-grapples/` → «All Grapples»
- `blog/flowers-love/` → «Flowers Love»
- `blog/velocity-becomes/` → «Velocity Becomes»
- `blog/way-to-clearance/` → «Way To Clearance»

**Что нужно от Вики**: реальные тайтлы и содержание блогов, либо удалить блоги из export (если они не нужны).

---

## 📋 Файлы override-документации (этот репо)

- `docs/export-overrides/footer-and-links-2026-05-20.md` — approve checkpoint + 3 ручные правки
- `docs/export-overrides/PENDING-cases-portfolio-2026-05-20.md` — отдельно по cases/portfolio
- `docs/export-overrides/NIGHT-PENDING-2026-05-20.md` ← этот файл

---

## 🔗 Где что лежит

- **Preview**: `http://srv1207957.hstgr.cloud:3343/`
- **GitHub**: `https://github.com/victorianartdinova/export-glanove-framer-website-mpef0bd0`
- **Last commit**: `6532201` (approve + 3 ручные правки)
- **Next commit** (этой ночи): добавит ГЛАВНОЕ-бренд в метаданных + avito footer baseline + этот PENDING-doc
- **Скрины**: `/tmp/may21-night/` (home/cases/products × 3 viewport)
