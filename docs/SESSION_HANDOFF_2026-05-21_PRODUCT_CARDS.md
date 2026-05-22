# Session handoff — 2026-05-21 — product cards (round 2)

## 1. Current preview
http://srv1207957.hstgr.cloud:3343/

Static-server отдаёт `/root/framerexport/full-site-export-may21/` на VPS srv1207957. Сейчас checked out `runtime-restore-may21`.

## 2. Branch / commit
- **Working branch:** `runtime-restore-may21`
- **HEAD:** `ae9a86e` (`docs: session handoff 2026-05-21 — product cards next task`)
- **Last feature commit:** `94e5cc6` (`feat: home product cards + audience sections + overlap/footer fixes`)
- **Backup branch:** `content-filled-static-fallback` на `ebcf0e8` (без Framer bundle, контент из SSR-HTML)
- **Backup tag:** `content-filled-static-fallback-may21`
- **Main:** `0287eb7` — **не двигаем**, без approve не сливать

GitHub: `victorianartdinova/export-glanove-framer-website-mpef0bd0`

## 3. Что уже работает

**Контент главной:**
- Hero, dashboard pin, «работаем с визионерами в каждом сегменте», 6 injected product cards (Авито Адс, Лидген Telegram, Коммуникационная стратегия, Рекламная стратегия, ПромоСтраницы, YouTube), кейсы с метриками, showreel брендов, footer.
- 3 case-карточки кликабельны: «50 квал-лидов» → `/work/regardis-telegram-ads-premium/`, «6 сделок» → `/work/case-spb-15mln/`, «Промо для МФК» → `/work/case-aag-promostranicy/`.

**5 product pages (avito-ads, content-product, product-statii, product-telegram, youtube-product):**
- hero / описание / 3 карточки аудитории / тарифы / процесс / статистика / pinned «Написать сейчас» CTA.

**2 case pages (AAG, SPB):**
- Впрыснут article body (метрики + «Что делали» + «Почему сработало» + CTA на product page).

**Runtime:**
- Восстановлен `<script data-framer-bundle="main">` на всех 15 страницах. Анимации, scroll, video, hero, dashboard pin, hover, header-навигация — живы.
- `<script data-glavnoe-safety="1">` на каждой странице (`window.load + 1500ms`): `fixOpacity`, `fixVisibility` (deduplication), `fixFooterColor`, `ensureAbout`, `ensureAudience`, `ensureCaseBody`, `ensureProductCards`, `hideEmpty`.

**URL:**
- `/product/avito-ads/` (ASCII), кириллический slug → symlink для backward compat.

## 4. Pending

**🔴 Главная задача — product cards на home (визуальная интеграция)**

Текущая сетка сделана через `ensureProductCards` (safety JS, строки 423–449 в `index.html`). Контент корректный, hrefs на месте, на mobile/tablet выглядит чисто. **Проблема — desktop**:

- viewport 1440 → сетка зажата в 774px, по бокам ~333px чёрных полей материнской dark-секции.
- Heading «работаем с визионерами» сверху и logo-strip — full-bleed, cards-grid — нет. Визуальный разрыв.
- Tablet 810 (762px) и mobile 390 (342px) — выглядят интегрированно.

**Решение по итогам исследования (4 агента):**

Framer block с заголовком «Рекламная стратегия» в export **существует** (`data-framer-name="Archive" > List`, byte 313983 в `index.html`), но это **showreel брендов** (5× `XL Primary` + 1× `XL Secondary`, контент: Juvede / Zaine / Wall Out / Geaton / Skate, без href, без CMS-data). Переиспользование как product-list = подмена всего контента и добавление кликабельности → это уже redesign, не contentup. Решено: **сценарий B (full-width injected grid)**.

**Action plan для следующей сессии (≤30 минут):**

1. В `index.html` строка ~447 `max-width:1392px` → `max-width:none` + `width:100%`.
2. Снять чёрные пустые поля по бокам — padding контейнера выровнять с heading-секцией («работаем с визионерами»). Замерить её padding на 1440/810/390 (DevTools или puppeteer DOM rect), привести cards-секцию к тому же.
3. Опционально: подсветить активные карточки (тёмный фон + красный accent border вместо текущего серого).
4. Снять crops `/tmp/product-cards-v2/{desktop,tablet,mobile}.png`, проверить через Read.
5. Коммит на `runtime-restore-may21` (НЕ merge main).
6. Обновить этот handoff и `state-glavnoe-real.md` / `next-session-framer.md`.

**Safety JS — что НЕ трогать:** `fixOpacity`, `fixVisibility`, `fixFooterColor`, `ensureAbout`, `ensureAudience`, `ensureCaseBody`, `hideEmpty`. Менять только inline CSS внутри `ensureProductCards`.

## 5. Известные мелкие баги (низкий приоритет)

- React #405 console warning — upstream Framer hydration mismatch. Safety JS лечит визуально.
- Mobile-вариант 2-го тарифа Avito показывает английский Framer-default («PREMIUM PLAN / Full manage project…») — контентный баг исходника, не runtime.
- CTA «забронировать» / «START PROJECT» / «Написать CEO» в шапке → `./index.html`. **Не трогать сейчас** (Вика так сказала).
- 4 blog-placeholder карточки внизу home (Way To Clearance / All Grapples / Flowers Love / Velocity Becomes) — есть title, `hideEmpty` не считает их пустыми.
- Header nav «Услуги / Результаты / Статьи» ведут на `./index.html` (раньше были scroll-anchors; «Кейсы» работает корректно).

## 6. Почему не merge в main

`runtime-restore-may21` — рабочая ветка, не утверждённая Викой к продакшну. Никаких `git merge runtime-restore-may21 → main` и `git push origin main` без явного «merge» от Вики. Main стоит на `0287eb7`.

## 7. Маппинг 6 cards (источник правды)

Все 6 описаний берутся из исходных Framer-данных в `index.html` (объект `{title, desc, href}`, строки 315–322 safety JS):

| Карточка | href | Файл (200 OK) | desc (≤80 симв) |
|----------|------|---------------|------------------|
| Авито Адс | `/product/avito-ads/` | ✅ | CPL в 2-5 раз дешевле Директа. Реклама + квиз + сквозная аналитика. |
| Лидген Telegram | `/product/product-telegram/` | ✅ | Аналитика, контент и креатив. CPL ниже рынка в 2 раза. |
| Коммуникационная стратегия | `/product/content-product/` | ✅ | Кросс-платформенная система: продажи, найм, экспертность. |
| Рекламная стратегия | `/product/product-statii/` | ✅ | Медиаплан с прогнозом продаж. Экономия 30% бюджета. |
| ПромоСтраницы и статьи | `/product/product-statii/` | ✅ | ROI 6000%, CPL на 32% дешевле контекста. ПромоСтраницы Яндекса. |
| Личный бренд YouTube | `/product/youtube-product/` | ✅ | Высокие охваты в узкой нише. Сценарии + AI, запуск за 1.5 нед. |

Дубль href на `product-statii` для двух карточек — намеренно. Эта страница покрывает обе темы: hero «Рекламная стратегия» + отдельный блок «ПромоСтраницы и статьи».

## 8. Quick-start для новой сессии

```bash
cd /root/framerexport/full-site-export-may21
git checkout runtime-restore-may21
git log --oneline -3   # ae9a86e → 94e5cc6 → d6f50ad

# Static-сервер уже работает на :3343, рестарт не нужен.
# Preview: http://srv1207957.hstgr.cloud:3343/

# Скриншоты:
node /root/snap-all.mjs                       # 7 страниц × desktop+mobile
node /root/snap-product-cards-final.mjs       # crop product-cards секции 1440/810/390
```

Safety JS живёт в каждом из 15 HTML перед `</body>` в `<script data-glavnoe-safety="1">`. Патч одинаков на всех страницах — есть готовые Python-шаблоны в предыдущих коммитах для bulk-update.

## 9. Артефакты исследования (5/21)

- `/tmp/product-cards-current/desktop.png` — current state desktop crop (1440×1874, виден 774px-зазор)
- `/tmp/product-cards-current/tablet.png` — current state tablet crop (810×1584, выглядит ок)
- `/tmp/product-cards-current/mobile.png` — current state mobile crop (390×2844, выглядит ок)
- `/root/snap-product-cards-final.mjs` — скрипт для повторного снятия crops
