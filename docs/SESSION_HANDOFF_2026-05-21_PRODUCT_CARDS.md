# Session handoff — 2026-05-21 — product cards

## 1. Что сделано в этой сессии

**Контент:**
- Главная — впрыснута custom-сетка из 6 product cards (Авито Адс, Лидген Telegram, Коммуникационная стратегия, Рекламная стратегия, ПромоСтраницы и статьи, Личный бренд YouTube) после блока «работаем с визионерами рынка в каждом сегменте». Сетка живёт в `data-glavnoe-safety` JS и собирается post-hydration.
- 5 product pages (avito-ads, content-product, product-statii, product-telegram, youtube-product) — у каждой теперь видны hero / (Как работаем) описание / (01.5) Кому подходит (3 карточки аудитории) / тарифы / процесс / статистика / pinned «Написать сейчас» CTA.
- AAG + SPB case pages — впрыснут article body (метрики + Что делали + Почему сработало + CTA на product page).

**Runtime / технический фикс:**
- Восстановлен `<script data-framer-bundle="main">` на всех 15 страницах (раньше был снесён в ebcf0e8 — там pages были пустые-но-видимые из SSR). Анимации, scroll, video, hero, dashboard pin, hover, header-навигация — живы.
- Откачены ad-hoc мутации `opacity:0 → opacity:1` и `translateY(40px) → translateY(0)` до NoCodeExport baseline (1100 правок).
- Единый inline `<script data-glavnoe-safety>` на каждой странице, выполняется на `window.load + 1500ms`. Делает: `fixOpacity`, `fixVisibility` (с дедупликацией по fingerprint текста, чтобы не подсвечивать SSR-fallback поверх анимированной версии), `fixFooterColor` (a.color: inherit), `ensureAbout`, `ensureAudience`, `ensureCaseBody`, `ensureProductCards`, `hideEmpty`.

**URL / навигация:**
- `/product/%D0%B0%D0%B2%D0%B8%D1%82%D0%BE-%D0%B0%D0%B4%D1%81/` → `/product/avito-ads/` (28 ссылок переписаны в HTML/JSON, реальная папка ASCII, Cyrillic → symlink на ASCII для backward compat).
- 3 case-карточки на главной: «50 квал-лидов в месяц» → `/work/regardis-telegram-ads-premium/`, «6 сделок за 3 месяца» → `/work/case-spb-15mln/`, «Промостраницы для МФК» → `/work/case-aag-promostranicy/`.

## 2. Preview link

http://srv1207957.hstgr.cloud:3343/

Static-server отдаёт текущее состояние папки `/root/framerexport/full-site-export-may21/` на VPS srv1207957. Сейчас там checked out runtime-restore-may21.

## 3. Branch / commit

- **Working branch:** `runtime-restore-may21`
- **HEAD:** `94e5cc6` (feat: home product cards + audience sections + overlap/footer fixes)
- **Backup branch:** `content-filled-static-fallback` на коммите `ebcf0e8` (без Framer bundle, контент из SSR-HTML; страховка)
- **Backup tag:** `content-filled-static-fallback-may21` (тот же commit)
- **Main:** `0287eb7` — не двигаем, без approve не сливать

GitHub: `victorianartdinova/export-glanove-framer-website-mpef0bd0`

## 4. Главная проблема: product cards сделаны custom JS-инъекцией

Сейчас 6 product cards на главной — это **самодельная HTML-сетка из safety JS** (`ensureProductCards` в `<script data-glavnoe-safety>`), стилизованная inline-CSS с Framer fontstack. Визуально работает, но это **не Framer-блок** и не наследует фирменный дизайн grid / hover / spacing.

**Однако:** в исходном NoCodeExport уже есть готовый Framer-блок с заголовком «Рекламная стратегия» (виден в текущей странице в районе showreel-таблицы Juvede / Zaine / Wall Out / Geaton / Skate — y≈6342 на desktop). Это явно шаблонный «product/showreel block» с CMS-данными, и его правильно было бы переиспользовать вместо самодельной сетки.

## 5. Next task

**Найти исходный Framer product-card/list block в текущем export** и заменить в нём только контент:

1. Поиск:
   - Стартовая точка — `index.html`, секция `<section ... data-framer-name="...">` рядом с y≈6300 (заголовок «Рекламная стратегия» в showreel).
   - Также проверить блоки с `data-framer-name` содержащим `Service`, `Product`, `Showcase`, `Showreel`, `Archive`, `Works`, `Offerings`, `Cards`, `Plan`.
   - Проверить CMS-структуру в `assets/framer/sites/1OcdQgezFomPwA9UGakYyz/searchIndex-*.json` — там может быть data-source для cards.
2. Если найден:
   - Удалить custom `ensureProductCards` из safety JS.
   - Подменить только text-content и href-ы внутри готового Framer-блока на 6 продуктов с правильными ссылками (см. список ниже).
   - Сохранить layout / hover / responsive / анимации Framer'а.
3. Если НЕ найден (после серьёзного поиска):
   - Сделать текущую custom-сетку full-width (max-width 1392 → 100vw), подровнять spacing под остальные секции, убрать min-height 280, тематизировать под фирстиль (тёмная карточка, акцент на красный).
   - Зафиксировать причину «Framer-блок не найден» в коммит-сообщении.

**Маппинг карточек:**
| Карточка | href |
|----------|------|
| Авито Адс | `/product/avito-ads/` |
| Лидген Telegram | `/product/product-telegram/` |
| Коммуникационная стратегия | `/product/content-product/` |
| Рекламная стратегия | `/product/product-statii/` |
| ПромоСтраницы и статьи | `/product/product-statii/` |
| Личный бренд YouTube | `/product/youtube-product/` |

## 6. Не делать merge в main без approve

`runtime-restore-may21` остаётся working branch. Никаких `git merge runtime-restore-may21` → main и никаких `git push origin main` без явного «merge» от Вики.

## Pending / known issues (низкий приоритет, не трогать сейчас)

- React #405 warning в console — upstream Framer NoCodeExport hydration mismatch. Safety JS лечит визуально.
- Mobile-вариант 2-го тарифа Avito показывает английский Framer-template default «PREMIUM PLAN / Full manage project / Creative strategy / Access to entire team» — контентный баг исходника, не runtime.
- CTA «забронировать» / «START PROJECT» / «Написать CEO» в шапке → `./index.html` — Вика явно сказала CTA не трогать сейчас.
- 4 blog-placeholder карточки внизу home (Way To Clearance / All Grapples / Flowers Love / Velocity Becomes) — у них есть title, hideEmpty не считает их пустыми.
- Header nav «Услуги / Результаты / Статьи» ведут на `./index.html` (раньше были scroll-anchors на in-page секции; «Кейсы» работает корректно).
- Hero overlap на case pages — исправлен возвратом Framer runtime.

## Quick-start для новой сессии

```bash
cd /root/framerexport/full-site-export-may21
git checkout runtime-restore-may21
git log --oneline -5  # должно начинаться с 94e5cc6

# Static-сервер уже работает на :3343, перезапуск не нужен.
# Preview: http://srv1207957.hstgr.cloud:3343/

# Для скриншот-проверок:
node /root/snap-all.mjs  # 7 страниц × desktop+mobile в /tmp/runtime-test/
```

Safety JS живёт в каждом HTML файле перед `</body>` в `<script data-glavnoe-safety="1">`. Чтобы изменить — патч в `<script>` блок одинаково на всех 15 страницах (есть готовый Python-паттерн в моих предыдущих коммитах).
