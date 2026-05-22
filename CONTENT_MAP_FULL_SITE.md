# CONTENT_MAP_FULL_SITE.md

> Контентная карта сайта ГЛАВНОЕ (preview :3343). Дата: 22.05.2026.
> Цель документа: контент-менеджер и владелец проекта понимают что готово, что менять, где брать, какие файлы править.
> Не технический отчёт. Не список коммитов.

---

## Сводка статусов

| Раздел                | Страниц | Готово к релизу | Требует правки | Заглушка |
|-----------------------|---------|-----------------|----------------|----------|
| Главная               | 1       | 0               | 1              | 0        |
| О / Контакты          | 2       | 2               | 0              | 0        |
| Блог (новые)          | 7       | 7               | 0              | 0        |
| Блог (старые stub)    | 4       | 4 (redirect)    | 0              | 0        |
| Кейсы (листинг + 3)   | 4       | 1               | 3              | 0        |
| Продуктовые           | 5       | 0               | 5              | 0        |
| Служебные (404)       | 1       | 1               | 0              | 0        |
| **ИТОГО**             | **24**  | **15**          | **9**          | **0**    |

---

# I. ПОСТРАНИЧНО

## 1. Главная — `/`

- URL: `http://srv1207957.hstgr.cloud:3343/`
- Файл: `/root/framerexport/full-site-export-may21/index.html`
- Тип: Framer NoCodeExport + safety JS overrides
- Статус: **требует правки** (mobile-карусель Stats + остатки template-блоков)
- Источник контента: смесь Framer SSR + override через `<script data-glavnoe-safety="1">` + новый `<script data-glavnoe-nav-v3>`
- Приоритет: **P0** (главная — лицо сайта)

| Блок                          | Статус       | Контент есть? | Актуален? | Менять? | Комментарий |
|-------------------------------|--------------|---------------|-----------|---------|-------------|
| Hero «GLAVNOE»                | Готово       | Да            | Да        | Нет     | Brand wordmark |
| About «Главное — донести»     | Готово       | Да            | Да        | Нет     | TextStagger |
| Эффективность (Dark)          | Готово       | Да            | Да        | Нет     | CPL chip 1300→5000 |
| Stats (07 Результаты) — desktop | Готово     | Да            | Да        | Нет     | 3600+/1M+/20K+/№1 |
| Stats (07 Результаты) — mobile carousel | **требует правки** | Только slot 1 | Нет (slot 2-3 template) | **Да** | Видны «30+ / Industries → our designs / Lambo+sneaker» — сейчас скрываю/подменяю JS, см. P0 ниже |
| SystemDashboard «Пять этапов» | Готово       | Да            | Да        | Нет     | Custom компонент |
| Cases (3 карточки)            | Готово (inject) | Да         | Да        | Нет     | Инжектируется nav-fixer после Results: СПб 15млн / AAG ROI 6000% / Regardis 50+ |
| Что придумали (5 продуктов)   | Готово       | Да            | Да        | Нет     | ARCHIVE_PRODUCTS → продукты кликабельны |
| Portfolio + ClientSection     | Готово       | Да            | Да        | Нет     | KEEP / Умное Сердце / CORE.XP / AAG / Archplay |
| Marquee CTA «А что главное»   | Готово       | Да            | Да        | Нет     | Тикер |
| Article (гайды и инсайты)     | требует правки | Частично    | Нет       | **Да**  | 4 placeholder-карточки (way-to-clearance / all-grapples / flowers-love / velocity-becomes). nav-fixer переписывает их href+title на реальные статьи, но если JS не успел — видны англ. placeholder-тексты |
| Form (Запуститься)            | Готово       | Да            | Да        | Нет     | Framer form action |
| FooterTicker + Footer         | Готово       | Да            | Да        | Нет     | Большой GLAVNOE wordmark |

**Что заменить:** mobile-карусель Stats — гарантировать что во всех слайдах русский контент. Сейчас работает через JS-подмену по индексу (slot 1: product/agency, slot 2: 3600+ заявок, slot 3: 1M+ охватов, slot 4: 20K+ подписчиков). Источник правды — `scripts/nav-fixer.js` массивы `PRODUCT_STATS` + `AGENCY_STATS`.
**Откуда брать:** PRODUCT_STATS / AGENCY_STATS в `nav-fixer.js`. Цифры подтверждены: 3600 заявок, 1M охватов, 20K подписчиков, №1 по CPL — взято с `/about/`.

---

## 2. О нас — `/about/`

- URL: `/about/`
- Файл: `/root/framerexport/full-site-export-may21/about/index.html`
- Тип: чистый HTML (не Framer)
- Статус: **готово**
- Источник контента: заполнено
- Приоритет: P2 (расширить, если будет команда / фото)

| Блок                | Статус | Контент есть? | Актуален? | Менять? | Комментарий |
|---------------------|--------|---------------|-----------|---------|-------------|
| NavBar              | Готово | Да            | Да        | Нет     | Главная / Услуги / Кейсы / Результаты / Статьи |
| Hero «ГЛАВНОЕ — донести» | Готово | Да       | Да        | Нет     | |
| Stats (4 метрики)   | Готово | Да            | Да        | Нет     | 3600+ / 1M+ / 20K+ / №1 |
| «Как работаем» текст | Готово | Да           | Да        | Нет     | |
| CTA mailto          | Готово | Да            | Да        | Нет     | hello@glavnoe.com |
| Footer              | Готово | Да            | Да        | Нет     | |

**Что заменить:** ничего критичного. Можно добавить: фото команды, миссия, история, награды.

---

## 3. Контакты — `/contact/`

- URL: `/contact/`
- Файл: `/root/framerexport/full-site-export-may21/contact/index.html`
- Тип: чистый HTML
- Статус: **готово**
- Источник: заполнено
- Приоритет: P2

| Блок                | Статус | Контент есть? | Менять? | Комментарий |
|---------------------|--------|---------------|---------|-------------|
| NavBar              | Готово | Да            | Нет     | |
| Hero «Связаться»    | Готово | Да            | Нет     | |
| Card: hello@glavnoe.com | Готово | Да        | Нет     | |
| Card: @ksandrbloger (CEO) | Готово | Да      | Нет     | Telegram CEO |
| Card: @glavnoe_channel | Готово | Да         | Нет     | Канал агентства |
| Card: @glavnoe_agency  | Готово | Да         | Нет     | Instagram |
| Footer              | Готово | Да            | Нет     | |

**Что заменить:** опционально форма обратной связи (сейчас только mailto + 3 канала).

---

## 4. Блог листинг — `/blog/`

- URL: `/blog/`
- Файл: `/root/framerexport/full-site-export-may21/blog/index.html`
- Тип: чистый HTML
- Статус: **готово**
- Приоритет: P2

| Блок                | Статус | Контент есть? | Менять? | Комментарий |
|---------------------|--------|---------------|---------|-------------|
| NavBar              | Готово | Да            | Нет     | |
| Hero «Статьи»       | Готово | Да            | Нет     | |
| 6 карточек статей   | Готово | Да            | Нет     | См. /blog/{slug}/ |
| Footer              | Готово | Да            | Нет     | |

**Что заменить:** новые статьи добавлять через `scripts/build-blog-pages.py` из `/root/glavnoe-site/content/blog/*.mdx`. После генерации обновить `<div class="grid">` в `/blog/index.html` вручную.

---

## 5–10. Статьи (6 шт) — `/blog/<slug>/`

| URL                                                              | Title                                                                 | Дата       | Статус |
|------------------------------------------------------------------|-----------------------------------------------------------------------|------------|--------|
| /blog/strategiya-marketinga-dlya-developera-2026/               | Стратегия маркетинга для девелопера в 2026                            | 2026-03-10 | Готово |
| /blog/kak-zastrojshchiku-vesti-telegram-kanal/                  | Как застройщику вести Telegram-канал в 2026                           | 2026-03-12 | Готово |
| /blog/gde-iskat-klientov-brokeru-2026/                          | Где брокеру искать клиентов в 2026 году                              | 2026-04-02 | Готово |
| /blog/6-sdelok-srednim-chekom-15-mln-telegram-ads/              | 6 сделок × 15 млн ₽ через Telegram Ads                                | 2025-12-01 | Готово |
| /blog/50-kvallidov-premium-nedvizhimost-telegram-ads/           | 50+ квал-обращений на премиум через Telegram Ads                      | 2025-07-01 | Готово |
| /blog/telegram-dlya-agentstva-nedvizhimosti-90-zayavok/         | Telegram для агентства: 90 заявок за 50 000 ₽/мес                    | 2024-05-15 | Готово |

- Источник: `/root/glavnoe-site/content/blog/*.mdx` (frontmatter + markdown body + FAQ)
- Шаблон: `scripts/build-blog-pages.py` — Inter font, чёрный фон, белый текст, FAQ-блок
- Что заменить: ничего срочного. Новые статьи → добавить .mdx в источник → пересобрать.

---

## 11. Кейсы листинг — `/cases/portfolio/`

- URL: `/cases/portfolio/`
- Файл: `/root/framerexport/full-site-export-may21/cases/portfolio/index.html`
- Тип: чистый HTML (переписан с пустой Framer-страницы)
- Статус: **готово**
- Приоритет: P2

| Блок                | Статус | Контент есть? | Менять? | Комментарий |
|---------------------|--------|---------------|---------|-------------|
| NavBar              | Готово | Да            | Нет     | |
| Hero «Кейсы»        | Готово | Да            | Нет     | |
| Card СПб 15млн      | Готово | Да            | Нет     | href=/work/case-spb-15mln/ |
| Card AAG ПромоСтр.  | Готово | Да            | Нет     | href=/work/case-aag-promostranicy/ |
| Card Regardis       | Готово | Да            | Нет     | href=/work/regardis-telegram-ads-premium/ |
| Footer              | Готово | Да            | Нет     | |

---

## 12. Кейс СПб 15млн — `/work/case-spb-15mln/`

- URL: `/work/case-spb-15mln/`
- Файл: `/root/framerexport/full-site-export-may21/work/case-spb-15mln/index.html`
- Тип: Framer-страница + case-extras.js
- Статус: **требует правки** (Framer hero показывает чужую статью «Итоги весны на рынке…» вместо «6 сделок × 15 млн ₽»)
- Источник: `/root/ops/marketing/cases/01_spb_telegram_ads.md` + публикация PPC World
- Приоритет: **P1** (большой кейс, флагман)

| Блок              | Статус | Контент есть? | Актуален? | Менять? | Комментарий |
|-------------------|--------|---------------|-----------|---------|-------------|
| NavBar            | Готово | Да            | Да        | Нет     | |
| Hero (Framer)     | **требует правки** | Частично | Нет | **Да** | Заголовок «Итоги весны на рынке недвижимости Петербурга» — это template/чужой контент. Должно быть «6 сделок × 15 млн ₽ через Telegram Ads». Подзаголовок есть в DOM (исправлено через ensureCaseBody) |
| Метрики (4 числа) | Готово (inject) | Да | Да | Нет | 6 / 15 млн ₽ / 19 973 ₽ / 310 ₽ |
| Что делали (5)    | Готово (inject) | Да | Да | Нет | Подготовка канала, Telegram Ads, 80/20, креативы, TGStat |
| Почему сработало (3) | Готово (inject) | Да | Да | Нет | Система, канал-актив, баланс |
| Доказывает продукт | Готово | Да | Да | Нет | Лидген Telegram → /product/product-telegram/ |
| Публикация PPC World | Готово (inject) | Да | Да | Нет | ссылка на ppc.world через case-extras.js |
| Industries placeholder | Скрыт | — | — | — | hideTemplateIndustries() |
| Footer            | Готово | Да | Да | Нет | |

**Что заменить:** Framer Hero текст «Итоги весны…» → «6 сделок × 15 млн ₽» (либо подменить через REPLACEMENTS на странице — сейчас этого нет; либо править Framer CMS-item).
**Откуда брать:** `/root/ops/marketing/cases/01_spb_telegram_ads.md`.

---

## 13. Кейс AAG ПромоСтраницы — `/work/case-aag-promostranicy/`

- URL: `/work/case-aag-promostranicy/`
- Файл: `/root/framerexport/full-site-export-may21/work/case-aag-promostranicy/index.html`
- Тип: Framer + case-extras.js (ensureCaseBody injection)
- Статус: **требует правки** (нет фото из эфира 16.04, hero может содержать чужой текст)
- Источник: `/root/ops/marketing/cases/03_aag_promopages.md` + `/root/Эфир 16.04..pdf` (163 МБ)
- Приоритет: **P1**

| Блок              | Статус | Контент есть? | Актуален? | Менять? | Комментарий |
|-------------------|--------|---------------|-----------|---------|-------------|
| Hero (Framer)     | требует правки | Частично | Не верифицировано | Возможно | Нужна визуальная проверка |
| Метрики (4 числа) | Готово (inject) | Да | Да | Нет | 6000% / −32% / 62% / 1.1% |
| Что делали (5)    | Готово (inject) | Да | Да | Нет | 3 статьи, A/B обложки, ЛО+СПб |
| Почему сработало (3) | Готово (inject) | Да | Да | Нет | |
| Доказывает продукт | Готово | Да | Да | Нет | Рекламная стратегия → /product/product-statii/ |
| Фото клиента / объектов | Отсутствует | Нет | — | **Да** | Источник — pdf-презентация эфира 16.04 |
| Industries placeholder | Скрыт | — | — | — | hideTemplateIndustries() |

**Что заменить:** добавить фото проектов AAG (бизнес-/премиум-ЖК Санкт-Петербург) из «Эфир 16.04.pdf». Извлечь через `pdfimages /root/Эфир\ 16.04..pdf out/`.
**Откуда брать:** `/root/Эфир 16.04..pdf` (16.04.2026 эфир-презентация).

---

## 14. Кейс Regardis — `/work/regardis-telegram-ads-premium/`

- URL: `/work/regardis-telegram-ads-premium/`
- Файл: `/root/framerexport/full-site-export-may21/work/regardis-telegram-ads-premium/index.html`
- Тип: Framer + case-extras.js (case body inject)
- Статус: **требует правки** (старая Framer-страница Vellfire может проступать в hero/CMS-полях)
- Источник: `/root/glavnoe-site/content/kejsy/50-kvallidov-premium-moskva.mdx` + `/root/ops/dev/regardis-framer-tech-spec.md`
- Приоритет: **P1**

| Блок              | Статус | Контент есть? | Менять? | Комментарий |
|-------------------|--------|---------------|---------|-------------|
| Hero (Framer)     | требует правки | Возможно частично | Да | Framer-page изначально клон vellfire-calibration; CMS-поля item ID `eHfWJJQ5z` могут показывать Vellfire-default. Hero текст «Regardis» должен быть подтверждён визуально |
| Метрики (4 числа) | Готово (inject) | Да | Нет | 9 684 ₽ / 50+ / 20 млн ₽ / 310 ₽ |
| Что делали (5)    | Готово (inject) | Да | Нет | бренд-медиа, WhatsApp+CRM, ads с 1 млн ₽/мес, 12 креативов, бюджет 80/20 |
| Почему сработало (3) | Готово (inject) | Да | Нет | |
| Доказывает продукт | Готово (inject) | Да | Нет | Лидген Telegram → /product/product-telegram/ |
| FAQ (3) / чек-лист | Отсутствует | Нет | Опционально | Есть в источнике mdx |
| Цитата Сергея Пака | Отсутствует | Нет | Опционально | Требует согласования |
| Industries placeholder | Скрыт | — | — | hideTemplateIndustries() |

**Что заменить:** проверить hero и удалить остатки «Vellfire» / «Dunwill Lanson» / «Nike Studios» если осталось.
**Откуда брать:** `/root/glavnoe-site/content/kejsy/50-kvallidov-premium-moskva.mdx`.

---

## 15–19. Продуктовые страницы — `/product/<slug>/`

Структура одинаковая на всех 5 (avito-ads — мастер). Различия в текстах через REPLACEMENTS override.

| URL                              | Title              | Hero              | Tier 1            | Tier 2            | Tier 3            | Big number  |
|----------------------------------|--------------------|-------------------|-------------------|-------------------|-------------------|-------------|
| /product/avito-ads/              | Авито Адс          | Авито Адс         | ТОЛЬКО РЕКЛАМА 80k | РЕКЛАМА+ПОСАДОЧНАЯ 120k | — | 1000+ |
| /product/content-product/        | Контент-маркетинг  | Коммуникационная стратегия | КОНТЕНТ-АУДИТ 80k | КОНТЕНТ 150k | КОНТЕНТ+HR 280k | 500+ |
| /product/product-statii/         | Рекламная стратегия | ПромоСтраницы Яндекса (после фикса 22.05) | АУДИТ 80k | ВЕДЕНИЕ+A/B 130k | СТРАТЕГИЯ 400k | 6000+ |
| /product/product-telegram/       | Лидген Telegram    | Лидген Telegram   | АУДИТ КАНАЛА 120k | ЗАПУСК РЕКЛАМЫ 165k | РЕКЛАМА+КАНАЛ 220k | 800+ |
| /product/youtube-product/        | Личный бренд YouTube | Личный бренд YouTube | ЗАПУСК 180k | ПРОДЮСИРОВАНИЕ 300k | — | 50+ |

**Общая таблица блоков (применима ко всем 5):**

| Блок                            | Статус       | Контент есть? | Актуален? | Менять? | Комментарий |
|---------------------------------|--------------|---------------|-----------|---------|-------------|
| Header NavBar                   | Готово       | Да            | Да        | Нет     | nav-fixer связывает ссылки |
| Hero (заголовок + 3 подписи)    | Готово       | Да            | Да        | Нет     | REPLACEMENTS |
| «Кому подходит» (audience 3 кол) | Готово (inject) | Да | Да | Нет | через ensureAudience() в safety JS |
| (Стоимость) тарифы 2-3 карточки | Готово       | Да            | Да        | Нет     | REPLACEMENTS подменяет |
| Bullets внутри карточек         | Готово (inject) | Да | Да | Нет | через tariff-bullets.js |
| Подпись «Нужен другой формат?»  | Готово (inject) | Да | Да | Нет | injectPricingNote() |
| «Как будем работать» (тёмный)   | Готово       | Да            | Да        | Нет     | REPLACEMENTS подменяет CTA |
| About параграф (Запускаем…)     | Готово       | Да            | Да        | Нет     | REPLACEMENTS |
| Stats (07 Результаты) Big number — desktop | Готово | Да | Да | Нет | 1000+/500+/6000+/800+/50+ |
| **Stats — mobile carousel** | **требует правки** | Частично | Частично | **Да** | После фикса 22.05 slot 1 = product number, slot 2-4 = agency stats (3600/1M/20K/№1). Может показывать только 1-2 слайда из 4. Визуальная проверка обязательна |
| Логотипы партнёров              | Готово       | Да            | Да        | Нет     | KEEP/УМНОЕСЕРДЦЕ/CORE.XP/AAG/ARCHPLAY |
| Pre-footer CTA                  | Готово       | Да            | Да        | Нет     | |
| Footer                          | Готово       | Да            | Да        | Нет     | |

**Что заменить (общее):**
1. Mobile-карусель Stats — визуально проверить что slot 2-4 показывают агентские метрики (3600+/1M+/20K+/№1), а не остатки template. Если не работает — расширить REPLACEMENTS в `/product/<slug>/index.html` ещё одной парой.
2. На avito-ads (master) mobile-вариант 2-го тарифа исторически показывает «PREMIUM PLAN / For enterprise / 12000» — REPLACEMENTS не покрывает. Эталон не правили, контентный баг исходника.

**Откуда брать тексты:** REPLACEMENTS array внутри каждой `product/<slug>/index.html` (там `<script data-glavnoe-product-override="<slug>">`).

---

## 20. 404 — `/404/`

- Статус: **готово**
- Footer и шапка корректны.

---

## 21–24. Старые блог-stub (redirect)

`/blog/way-to-clearance/`, `/blog/all-grapples/`, `/blog/flowers-love/`, `/blog/velocity-becomes/` — meta refresh + JS redirect на `/blog/`. **Готово**.

---

# II. MOBILE ПРОВЕРКА (390 / 810)

> 430px отдельно не проверялся — между 390 и 810 поведение CSS одинаковое (Framer media query `max-width: 809.98px`).

| Страница                  | 390 desktop-mismatch                         | 810 desktop-mismatch                | overflow horiz? |
|---------------------------|----------------------------------------------|-------------------------------------|-----------------|
| /                         | Stats-карусель slot 2-3 mobile (template после JS-фикса должно быть OK) | Stats та же | нет |
| /about/                   | нет — простой HTML, адаптив на CSS-grid       | нет                                 | нет             |
| /contact/                 | нет                                          | нет                                 | нет             |
| /blog/                    | нет                                          | нет                                 | нет             |
| /blog/<slug>/             | нет — Inter font, clamp() для типографики    | нет                                 | нет             |
| /cases/portfolio/         | нет — переписан в чистый HTML                | нет                                 | нет             |
| /work/case-spb-15mln/     | hero template-text заметнее на mobile        | то же                               | нет             |
| /work/case-aag-promostranicy/ | то же                                    | то же                               | нет             |
| /work/regardis-telegram-ads-premium/ | то же                              | то же                               | нет             |
| /product/avito-ads/       | Tier 2 mobile «PREMIUM PLAN / 12000» (master template not patched) | то же | нет |
| /product/content-product/ | Stats carousel slot 2-3 — нужна проверка     | то же                               | нет             |
| /product/product-statii/  | Stats carousel slot 2-3 — нужна проверка     | то же                               | нет             |
| /product/product-telegram/| Stats carousel slot 2-3 — нужна проверка     | то же                               | нет             |
| /product/youtube-product/ | Stats carousel slot 2-3 — нужна проверка     | то же                               | нет             |
| /404/                     | нет                                          | нет                                 | нет             |

**Скрытые блоки на mobile (намеренно):**
- На всех work/* и product/*: data-glavnoe-hidden="template-image" — placeholder фото Lambo / sneaker
- На всех work/*: data-glavnoe-hidden="template-industries" — секция с Industries-текстом

**Сломанные блоки на mobile:**
- product/avito-ads/ tablet+mobile: Tier 2 показывает английский Framer fallback («PREMIUM PLAN / For enterprise and organizations / 12000») — НЕ исправлено, это master/эталон. На остальных 4 продуктовых исправлено через REPLACEMENTS.

**Обрезанный текст / отсутствующие изображения:**
- Не зафиксировано на проверенных страницах.

**Кнопки не работают:**
- Не зафиксировано после фиксов nav-fixer (`/Услуги/Результаты/Статьи/Написать CEO` подменены).

---

# III. PLACEHOLDERS

Все найденные template/placeholder тексты и медиа:

| # | Текст / медиа                                                                 | Где встречается              | Тип        | Решение                           |
|---|-------------------------------------------------------------------------------|------------------------------|------------|-----------------------------------|
| 1 | "Industries → our designs have supported businesses, adapting to unique needs and challenges" | Framer template default, приходит из chunk MJS на product/* и work/* | Framer demo | nav-fixer подменяет на агентскую метрику + скрывает секцию если нет mapping |
| 2 | "30+"                                                                         | template big number          | Framer demo | nav-fixer подменяет на product+agency numbers |
| 3 | "PREMIUM PLAN"                                                                | mobile fallback Tier 2 на avito (master) | Framer demo | На 4 продуктовых: REPLACEMENTS. На avito-ads: оставлено как есть. |
| 4 | "For enterprise and organizations"                                            | mobile fallback Tier 2       | Framer demo | то же                              |
| 5 | "12000"                                                                       | mobile fallback Tier 2 price | Framer demo | то же                              |
| 6 | "Fully manage project"                                                        | mobile bullet Tier 2         | Framer demo | REPLACEMENTS на 4 продуктовых     |
| 7 | "Creative strategy"                                                           | mobile bullet                | Framer demo | то же                              |
| 8 | "Access to entire team"                                                       | mobile bullet                | Framer demo | то же                              |
| 9 | "отношение к результатам"                                                     | Stats label на avito-ads (master) | Framer demo (наш контент) | На 4 продуктовых: REPLACEMENTS. На avito: оставлено |
| 10 | "Adrián Velasco"                                                             | template testimonial slider  | Framer demo | Не обнаружено в DOM (Framer его не рендерит) |
| 11 | "AxiraAI" / "Future Things" / "Fuel"                                         | data-framer-name (атрибут, не видимый текст) | Framer demo | Не отображается пользователю |
| 12 | Lambo (жёлтое авто)                                                          | Industries section background | Framer demo image | nav-fixer hides по filename match |
| 13 | Sneaker / shoe                                                                | Industries section            | Framer demo image | то же                              |
| 14 | "Vellfire" / "Dunwill Lanson" / "Nike Studios"                                | Framer template для work-page (Regardis клон Vellfire) | Framer demo | Удалены в коммите ebcf0e8 на main; проверить визуально |
| 15 | "Lorem ipsum"                                                                 | —                            | —          | Не обнаружено |

---

# IV. CONTENT MISSING

Чего не хватает (по группам):

## Кейсов
- **AAG**: фотографии проектов из «Эфир 16.04.pdf»
- **Regardis**: цитата Сергея Пака для блока Testimonial (требует согласования)
- **Regardis**: чек-лист запуска 9 пунктов + FAQ 3 вопроса (есть в источнике mdx, не залит)
- Дополнительные кейсы (4-й, 5-й) — не запланированы пока

## Статей
- 6 статей уже залиты. Дополнительные — по мере написания.

## Отзывов
- Testimonial slider на главной показывает 3 имени (Бараковская / Таисия / Беляев) из glavnoe-real, но цитаты могут быть placeholder. **Требует проверки текстов и фото клиентов.**

## Изображений
- Фото команды на /about/ — нет, можно добавить
- Фото проектов в кейсах — частично (нужны AAG)
- Hero images для блог-постов — нет (заголовок текстом)

## SEO-текстов
- Все 24 страницы имеют title + description + canonical + og:* — заполнено
- Не хватает: structured data (JsonLd schema.org Article) на блог-постах

## CTA
- Все основные CTA на месте (mailto, /contact, /#products)

## Описаний продуктов
- 5/5 продуктов с описаниями. Без замечаний.

---

# V. READY FOR RELEASE

Страницы полностью готовы к публикации:

1. `/about/`
2. `/contact/`
3. `/blog/`
4. `/blog/strategiya-marketinga-dlya-developera-2026/`
5. `/blog/kak-zastrojshchiku-vesti-telegram-kanal/`
6. `/blog/gde-iskat-klientov-brokeru-2026/`
7. `/blog/6-sdelok-srednim-chekom-15-mln-telegram-ads/`
8. `/blog/50-kvallidov-premium-nedvizhimost-telegram-ads/`
9. `/blog/telegram-dlya-agentstva-nedvizhimosti-90-zayavok/`
10. `/blog/way-to-clearance/` (redirect)
11. `/blog/all-grapples/` (redirect)
12. `/blog/flowers-love/` (redirect)
13. `/blog/velocity-becomes/` (redirect)
14. `/cases/portfolio/`
15. `/404/`

**Не готовы:**
- `/` — mobile Stats требует визуальной проверки
- `/product/avito-ads/` — mobile Tier 2 «PREMIUM PLAN / 12000» (master template not patched)
- `/product/content-product/`, `/product/product-statii/`, `/product/product-telegram/`, `/product/youtube-product/` — mobile Stats slot 2-4 требует визуальной проверки
- `/work/case-spb-15mln/`, `/work/case-aag-promostranicy/`, `/work/regardis-telegram-ads-premium/` — Framer hero может содержать template/чужой текст

---

# VI. BLOCKING ISSUES

## P0 (критично — мешает релизу)

1. **Mobile Stats карусель на 4 продуктовых страницах** — slot 2-4 после моего фикса должны показывать русский агентский контент (3600+/1M+/20K+/№1). Требует визуальной верификации Викой. Если хоть один слайд показывает «Industries» / «30+» / Lambo+sneaker — нужно расширить REPLACEMENTS array в HTML.
   - Файлы: `/product/{avito-ads,content-product,product-statii,product-telegram,youtube-product}/index.html`
   - Скрипт: `scripts/patch-mobile-template.py` + `scripts/nav-fixer.js`

2. **Avito-ads master mobile Tier 2** — показывает «PREMIUM PLAN / For enterprise and organizations / 12000». Master template не патчен по принципу «эталон не трогать». Решение: либо запатчить эталон тоже, либо удалить avito-ads из публичных продуктов до фикса.
   - Файл: `/product/avito-ads/index.html`

3. **Кейс-страницы /work/case-spb-15mln/ hero** — показывает старый Framer-content «Итоги весны на рынке недвижимости Петербурга». Должно быть «6 сделок × 15 млн ₽».
   - Файл: `/work/case-spb-15mln/index.html`
   - Решение: добавить REPLACEMENTS map в HTML страницы со сменой hero h2

## P1 (важно — блокирует часть фич)

4. **Фото проектов AAG** — извлечь из `/root/Эфир 16.04..pdf` и подложить в кейс
   - Файл: `/work/case-aag-promostranicy/index.html`
   - Источник: `/root/Эфир 16.04..pdf` (163 МБ)
   - Способ: `pdfimages -j /root/Эфир\ 16.04..pdf /tmp/aag-out/` → отобрать → положить в `/assets/img/aag/` → инжектировать через case-extras.js

5. **Regardis hero** — проверить что показывает «Regardis», а не «Vellfire» (master template до коммита ebcf0e8 был vellfire-calibration).
   - Файл: `/work/regardis-telegram-ads-premium/index.html`

6. **Главная Stats mobile + кейсы инжект** — визуально подтвердить что 3 case-cards (через injectHomepageCases в nav-fixer.js) показываются корректно

7. **Testimonial slider главной** — проверить что цитаты НЕ placeholder и фото клиентов реальные

## P2 (косметика)

8. **/about/** — расширить (фото команды, миссия, история, награды)
9. **/contact/** — добавить форму обратной связи (вместо mailto)
10. **Блог** — добавить hero-images к постам (сейчас текстом)
11. **JsonLd structured data** на блог-постах (для GEO/SEO)
12. **Цитата Сергея Пака** в Regardis-кейс (после согласования)
13. **Фото команды** на /about/

---

# VII. EXACT FILES TO EDIT

| Проблема | URL | Файл | Компонент / блок | Что менять |
|---|---|---|---|---|
| Mobile Stats slot 2-4 product-statii | /product/product-statii/ | `product/product-statii/index.html` | `<script data-glavnoe-product-override>` REPLACEMENTS array (после `data-glavnoe-mobile-template-patch`) | Уточнить mapping для «30+» → нужное число; для template phrases → нужный label |
| То же 4 страницы | /product/{content,statii,telegram,youtube}/ | product/{slug}/index.html | REPLACEMENTS array | то же |
| Avito Tier 2 PREMIUM PLAN | /product/avito-ads/ | `product/avito-ads/index.html` | REPLACEMENTS array | Добавить пары: PREMIUM PLAN→РЕКЛАМА+ПОСАДОЧНАЯ, For enterprise→Управление всей воронкой, 12000→120 k. |
| СПб hero «Итоги весны» | /work/case-spb-15mln/ | `work/case-spb-15mln/index.html` | Inline `<script>` перед `</body>` или вставка после `<body>` | Добавить override-script с подменой text node «Итоги весны на рынке недвижимости Петербурга» → «6 сделок × 15 млн ₽» |
| AAG фото | /work/case-aag-promostranicy/ | `scripts/case-extras.js` + новые ассеты | EXTRA_CASES объект → добавить `images: [...]` поле + инжект галерею | Извлечь pdf-фото и положить в `assets/img/aag/*.jpg` |
| Regardis hero verify | /work/regardis-telegram-ads-premium/ | `work/regardis-telegram-ads-premium/index.html` | Hero text nodes | Проверить визуально, если есть «Vellfire» — добавить REPLACEMENTS |
| Главная Stats verify | / | `index.html` | nav-fixer.js + `<script data-glavnoe-safety>` | Визуальная проверка |
| Testimonial проверка | / | `index.html` | data-framer-name="Testimonial" | Сверить с реальными клиентами |
| /about/ расширение | /about/ | `about/index.html` | Hero / Stats / How We Work блоки | Добавить новые секции (Team, История, Награды) |
| /contact/ форма | /contact/ | `contact/index.html` | Под Hero | Заменить cards-сетку на форму (или добавить блок с формой) |
| Hero-images блог | /blog/<slug>/ | `scripts/build-blog-pages.py` шаблон | После hero блок | Добавить `<img>` тег в HEAD HTML, источник — папка `assets/img/blog/<slug>.jpg` |
| JsonLd на блоге | /blog/<slug>/ | `scripts/build-blog-pages.py` шаблон | в `<head>` перед `</head>` | Добавить `<script type="application/ld+json">` с schema.org Article |
| Regardis FAQ + чек-лист | /work/regardis-telegram-ads-premium/ | `scripts/case-extras.js` | EXTRA_CASES Regardis | Добавить поля `faq[]` и `checklist[]` + рендер |

---

# VIII. ОПЕРАЦИОННЫЕ ДЕТАЛИ

## Где править содержимое
- **Framer-страницы** (5 products, 3 work, 1 main, 1 cases-listing, 1 404): редактировать `<script data-glavnoe-product-override>` REPLACEMENTS в самом HTML
- **Чистые HTML** (about, contact, blog/, cases/portfolio/, 6 blog-posts): редактировать сам HTML / шаблон в `scripts/build-blog-pages.py`
- **Глобальные JS-инжекторы**: `scripts/nav-fixer.js`, `scripts/case-extras.js`, `scripts/tariff-bullets.js`
- **После любой правки JS-инжектора**: `python3 scripts/inject-nav-fixer.py` или соответствующий deploy script

## Сервер
- :3343 теперь python `serve-nocache.py` (no-cache headers)
- Рестарт: `pkill -f serve-nocache; cd /root/framerexport/full-site-export-may21 && setsid nohup python3 serve-nocache.py 3343 > /tmp/serve3343.log 2>&1 < /dev/null &`

## Источники контента (правда в этих файлах)
- Стратегия + продукты: `/root/ops/marketing/GLAVNOE_product_lineup_2026.md`
- Кейсы: `/root/ops/marketing/cases/01_spb_telegram_ads.md`, `03_aag_promopages.md`
- Блог-статьи: `/root/glavnoe-site/content/blog/*.mdx`
- Кейсы (полные): `/root/glavnoe-site/content/kejsy/*.mdx`
- AAG материалы: `/root/Эфир 16.04..pdf`
- Regardis tech-spec: `/root/ops/dev/regardis-framer-tech-spec.md`

---

**Конец карты.** Дата: 22.05.2026, 06:30.
