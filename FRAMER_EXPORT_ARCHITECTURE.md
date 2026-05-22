# FRAMER_EXPORT_ARCHITECTURE.md

> Архитектурное описание `full-site-export-may21`. Что внутри, как устроено, где границы.
> Этот документ — справочный. Правила и запреты — в `PROJECT_RULES.md` и `CLAUDE.md`.

---

## 1. Что это

Статический снимок сайта `glanove.framer.website`, снятый через **NoCodeExport** 2026-05-20 в режиме **Maximum Fidelity Mode**: Framer React runtime (react, motion, framer) замиррорен локально вместе со всеми HTML-страницами и ассетами.

- Это **не React-проект**, не SSG, не Next.js. Нет `src/`, нет `package.json` с билдом сайта.
- HTML каждой страницы — уже отрендеренный snapshot DOM (SSR-output Framer-а), который при загрузке гидратируется локальным runtime для анимаций и интерактива.
- CMS-страницы (`blog/*`, `cases/portfolio/*`, `work/*`) превращены в отдельные статические HTML — без API, без коллекций, без фильтрации.

Полный гайд по запуску — `RUN_LOCALLY.md`.

---

## 2. Структура верхнего уровня

```
full-site-export-may21/
├── index.html                    # главная
├── 404/index.html                # 404
├── search.html                   # клиентский поиск
├── search-index.json             # индекс для поиска (Framer-format)
├── sitemap.xml                   # карта сайта
├── robots.txt
│
├── product/                      # продуктовые страницы
│   ├── avito-ads/index.html      # ⭐ ЭТАЛОН (master template)
│   ├── content-product/index.html
│   ├── product-statii/index.html
│   ├── product-telegram/index.html
│   ├── youtube-product/index.html
│   └── %D0%B0%D0%B2%D0%B8%D1%82%D0%BE-%D0%B0%D0%B4%D1%81 → avito-ads   # symlink для cyrillic URL
│
├── blog/<slug>/index.html        # экспортированные CMS-посты
├── cases/portfolio/<slug>/       # портфолио
├── work/<slug>/index.html        # кейсы
│
├── assets/
│   ├── fonts/                    # локальные woff2
│   ├── framer/
│   │   ├── sites/<siteId>/       # 🔒 Framer runtime (десятки .mjs chunks)
│   │   ├── modules/              # внешние модули (Video, fontshare, и т.д.)
│   │   ├── images/               # иконки, favicons
│   │   ├── assets/               # картинки, woff2 с framerusercontent
│   │   └── third-party-assets/   # сторонние ассеты
│
├── docs/                         # внутренние handoff-документы
├── seo-report/                   # SEO-аудит
│
├── CLAUDE.md                     # инструкции для агента (с приоритетом)
├── PROJECT_RULES.md              # правила и forbidden
├── CURRENT_TASK.md               # операционная задача
├── README_RESTORE.md             # клон-протокол
├── README.md / RUN_LOCALLY.md    # запуск
└── .git/
```

---

## 3. HTML-страница: устройство

Каждый `index.html` — самодостаточный (один HTTP-запрос отдаёт всё для рендера):

- **`<head>`**
  - `<title>`, `description`, `og:*`, `twitter:*` — SEO/social, впечатаны статически.
  - `<style data-framer-font-css>` — `@font-face` локальные шрифты (`../../assets/fonts/*.woff2`) и Suisse Intl (`/assets/framer/assets/*.woff2`).
  - `<style data-framer-css-ssr-minified>` — критический CSS, выданный SSR-ом Framer-а.
  - `<link rel="icon">`, `<link rel="manifest">` (если есть).
  - `<meta name="framer-search-index">` — путь к `search-index.json`.
- **`<body>`** — отрендеренный DOM с разметкой `data-framer-*`:
  - `data-framer-name` — имя секции/слоя из Framer Studio (на 125 уникальных имён в `avito-ads`).
  - `data-framer-component-type`, `data-framer-component-text-autosized`, `data-framer-appear-animation`, `data-framer-appear-id`, `data-framer-hydrate-v` — runtime-маркеры для гидратации и анимаций.
  - `data-framer-page-link-current` — активный пункт навигации.
  - `data-framer-name="$"` — служебный root-узел.
- **`<script type="module" data-framer-bundle="main" src="/assets/framer/sites/<siteId>/script_main.<hash>.mjs">`** — точка входа в runtime.

Контент впечатан в DOM как обычные текстовые узлы (innerText заголовков, абзацев, кнопок). **JSON-источника данных нет.**

---

## 4. Runtime assets — содержимое `assets/framer/sites/<siteId>/`

- `siteId` для этого экспорта: `1OcdQgezFomPwA9UGakYyz`.
- **~60 файлов `.mjs`** в корне `sites/<siteId>/` — chunks React + Framer Motion + components.
- **Подпапки `sites/<siteId>/<chunkGroup>/`** — субчанки (на момент аудита: `fia4wPSLQ2rXovUai4Zb`, `ts8giR4tgNFwbnq1ajjk`, `uDy2kUsr1pTsm4RNguGn`).
- **`script_main.<hash>.mjs`** — entrypoint, на него ссылаются все HTML.
- **`*-v2.mjs`** — **post-hydration patches**, добавленные вручную в текущей ветке поверх оригинального экспорта.
- **Хеши имён файлов содержат content hash** и ротируются Framer-ом на каждом republish. Поэтому экспорт «протухает» — старые URL-ы chunks Framer держит на CDN ~2 недели, потом 404.

Это **обфусцированный код**, не источник контента. Правка `.mjs` руками — антипаттерн (см. §6 и `CONTENT_GENERATION_RULES.md`).

`assets/framer/modules/` — отдельные модули (например, `Video.eys1QPK8.mjs`, fontshare chunks), которые HTML загружает по необходимости.

---

## 5. Маршруты

- `/` → `index.html`
- `/search` → `search.html` (клиентский поиск по `search-index.json`)
- `/404` → `404/index.html`
- `/product/<slug>/` → `product/<slug>/index.html` (5 продуктов: avito-ads, content-product, product-statii, product-telegram, youtube-product)
- `/blog/<slug>/` → `blog/<slug>/index.html` (4 поста на момент аудита)
- `/cases/portfolio/<slug>/` → `cases/portfolio/<slug>/index.html`
- `/work/<slug>/` → `work/<slug>/index.html` (3 кейса)
- Cyrillic URL мапятся через symlink в файловой системе (например, `/product/%D0%B0%D0%B2%D0%B8%D1%82%D0%BE-%D0%B0%D0%B4%D1%81/`).

Источник правды по маршрутам: `sitemap.xml` + физическая структура папок. Никаких роутеров.

---

## 6. Ограничения экспорта

Эти ограничения — **природа NoCodeExport**, а не дефект текущей сборки:

1. **Нет CMS-API.** Поиск/фильтрация/коллекции — заморожены. Каждый CMS-айтем = отдельный HTML.
2. **Нет JSON data layer.** Контент впечатан в HTML. Чтобы менять масштабно — нужен внешний JSON и генератор (см. `CONTENT_GENERATION_RULES.md`).
3. **Runtime chunks обфусцированы.** Ручные правки нечитаемы, ломаются при re-export.
4. **Hash rotation.** Любой republish во Framer-е инвалидирует имена `.mjs`. Старые URL живут ~2 недели на Framer CDN, потом 404.
5. **Часть ассетов остаётся внешними.** Некоторые шрифты и image-resize варианты грузятся с `framerusercontent.com` — без интернета частично «лысеют».
6. **Формы — внешние.** `<form action="">` указывает на тот endpoint, что был во Framer-е (Formspree / собственный backend).
7. **Гидратация может перетирать DOM.** Если runtime ожидает другой контент, чем впечатан в HTML — он переписывает узел при mount-е. **Решение НЕ в правке runtime**, а в том, чтобы оставлять разметку, которую runtime ожидает (структура эталона + только подмена текста, см. `PRODUCT_TEMPLATE_SPEC.md`).

---

## 7. Когда нужен re-export Framer

| Сценарий | Re-export нужен? |
|---|---|
| Смена дизайна/брендинга/палитры во Framer | ✅ Да |
| Новые типы секций или компонентов, которых нет в текущем HTML | ✅ Да |
| Изменилась глобальная навигация / структура страниц | ✅ Да |
| Поменялся набор шрифтов | ✅ Да |
| Original Framer-проект republished, старые runtime chunks начали 404 | ✅ Да |
| Прошло ~2 недели с предыдущего экспорта, и проект во Framer активно правится | ✅ Да (профилактика) |

## 8. Когда re-export НЕ нужен

| Сценарий | Re-export нужен? |
|---|---|
| Меняется текст, заголовок, цена, CTA-ссылка | ❌ Нет — это контент |
| Добавляются новые продуктовые страницы по шаблону существующей | ❌ Нет — это template + json |
| Меняются картинки секций (на ассеты той же формы) | ❌ Нет |
| Чинятся `<title>`, `description`, OG-теги | ❌ Нет |
| Обновляется `sitemap.xml`, `robots.txt`, `search-index.json` | ❌ Нет |
| Обновляется контент блог-постов / кейсов | ❌ Нет |

**Правило:** дизайн и runtime ⇒ re-export. Контент ⇒ template + json + генератор.

---

## 9. Git source of truth (фактическое состояние на 2026-05-21)

**Канонический источник проекта — `origin/main` репо `victorianartdinova/export-glanove-framer-website-mpef0bd0`.**

История main (4 коммита, автор Victoria Nartdinova):

| SHA | Сообщение | Смысл |
|---|---|---|
| `9934c96` | Deploy from NoCodeExport | Исходный snapshot экспорта, 225 файлов |
| `6532201` | chore(overrides): footer labels match header + Sasha/channel links | Корректировка футера |
| `0287eb7` | chore(meta): replace Fuel template branding with ГЛАВНОЕ + avito footer fix | Снятие шаблонного брендинга NoCodeExport |
| `ebcf0e8` | fix(content): unbreak product/case pages + fill AAG/SPB bodies + ASCII avito URL | **HEAD origin/main** — заполнение AAG/SPB кейсов, ASCII slug для avito |

**Локальные ветки:**

| Ветка | Состояние | Назначение |
|---|---|---|
| `main` | Совпадает с `origin/main` (HEAD `ebcf0e8`) | Канонический source of truth |
| `content-filled-static-fallback` | Совпадает с `main` (HEAD `ebcf0e8`) | Safe fallback: статический контент без runtime-патчей |
| `runtime-restore-may21` | `main` + 5 коммитов, **только локально, на origin отсутствует** | Рабочая ветка с runtime-патчами и заполнением 4 страниц |

5 коммитов `runtime-restore-may21` поверх `main`:

| SHA | Сообщение | Что вносит |
|---|---|---|
| `d6f50ad` | fix(runtime): restore Framer JS bundle + minimal post-hydration patch | Возвращает Framer runtime + добавляет inline `<script data-glavnoe-safety>` на все 15 страниц (safetyJS) |
| `94e5cc6` | feat(content): home product cards + audience sections + overlap/footer fixes | Продуктовые карточки и audience-секции на главной |
| `ae9a86e` | docs: session handoff 2026-05-21 — product cards next task | Handoff-документ |
| `11130a2` | fix(home): product cards full-width on desktop (scenario B) | Width-фикс десктопа |
| `89d89bb` | feat(products): wire 4 product pages to static routes with own content | **HEAD runtime-restore-may21** — контент 4 продуктовых страниц + `-v2.mjs` post-hydration патчи |

Что НЕ существует в git, но фигурирует в правилах VPS:
- Ветка `full-site-export-may20-stable` — упоминается в `PROJECT_RULES.md` как запрещённая, фактически отсутствует и локально, и на origin. Запись устарела либо относилась к другой папке.

**Untracked файлы на 2026-05-21 (есть на VPS, нет в git):**

- `CLAUDE.md` — инструкции агенту
- `PROJECT_RULES.md` — правила, forbidden, allowed
- `CURRENT_TASK.md` — операционная задача (описывает состояние ДО коммита `89d89bb`, устарело)
- `README_RESTORE.md` — клон-протокол
- `FRAMER_EXPORT_ARCHITECTURE.md` — этот документ
- `PRODUCT_TEMPLATE_SPEC.md`
- `CONTENT_GENERATION_RULES.md`
- `PRODUCT_GENERATION_PLAN.md`

Это значит: **все правила и архитектурные документы существуют только в рабочей копии**. Любой, кто склонирует репо с GitHub, их не увидит. Для того чтобы они стали частью проекта — их нужно закоммитить (требуется явный approve пользователя, см. `PROJECT_RULES.md` §«Протокол после задачи»).

**Modified uncommitted:**
- `docs/SESSION_HANDOFF_2026-05-21_PRODUCT_CARDS.md` — закоммичен в `ae9a86e`, но имеет локальные правки поверх.

**Tracked `.md` в корне репозитория (что официально является документацией проекта в git):**

- `README.md` — сгенерирован NoCodeExport
- `RUN_LOCALLY.md` — сгенерирован NoCodeExport
- `seo-report/README.md`
- `docs/SESSION_HANDOFF_2026-05-21_PRODUCT_CARDS.md`
- `docs/export-overrides/NIGHT-PENDING-2026-05-20.md`
- `docs/export-overrides/PENDING-cases-portfolio-2026-05-20.md`
- `docs/export-overrides/footer-and-links-2026-05-20.md`

Никаких «правил», «архитектурных принципов», «спецификаций шаблона» в git **нет**. Все они — на VPS.

**`.gitignore` отсутствует.** Untracked файлы не игнорируются — они просто непрокоммичены.

---

## 10. Каноничность артефактов: что считать источником

| Артефакт | Источник правды | Статус в git |
|---|---|---|
| HTML страниц | `origin/main` HEAD `ebcf0e8` | Tracked |
| Framer runtime (`assets/framer/sites/<siteId>/*.mjs`, оригинальные имена) | `origin/main` | Tracked |
| Эталон продуктовой страницы (`product/avito-ads/index.html`) | `origin/main` | Tracked |
| Шрифты, картинки (`assets/fonts/`, `assets/framer/assets/`, `assets/framer/images/`) | `origin/main` | Tracked |
| `sitemap.xml`, `search-index.json`, `robots.txt` | `origin/main` | Tracked |
| Структура папок (`product/`, `blog/`, `cases/`, `work/`) | `origin/main` | Tracked |
| Handoff-документы (`docs/`) | `origin/main` (committed) | Tracked |
| `-v2.mjs` post-hydration patches | Только `runtime-restore-may21` | Эксперимент |
| Inline `<script data-glavnoe-safety>` в HTML | Только `runtime-restore-may21` (от `d6f50ad`) | Эксперимент |
| Заполненный контент в `product/content-product/`, `product/product-statii/`, `product/product-telegram/`, `product/youtube-product/` | Только `runtime-restore-may21` (от `89d89bb`) | Эксперимент |
| `CLAUDE.md`, `PROJECT_RULES.md`, `CURRENT_TASK.md`, `README_RESTORE.md` | Только рабочая копия VPS | **НЕ в git** |
| `FRAMER_EXPORT_ARCHITECTURE.md`, `PRODUCT_TEMPLATE_SPEC.md`, `CONTENT_GENERATION_RULES.md`, `PRODUCT_GENERATION_PLAN.md` | Только рабочая копия VPS | **НЕ в git** |

**Принцип:** архитектурные решения принимаются на основе `origin/main` + закоммиченных файлов. Локальные эксперименты (включая ветку `runtime-restore-may21` целиком) не являются источником архитектурной правды — они являются «работой в процессе», которая может быть либо принята, либо откатана.

---

## 11. Источники и связки

- Полный гайд по запуску и поведению runtime: `RUN_LOCALLY.md`.
- Шаблон продуктовой страницы: `PRODUCT_TEMPLATE_SPEC.md`.
- Workflow генерации страниц: `CONTENT_GENERATION_RULES.md`.
- План миграции от текущего «4 копии» к генератору: `PRODUCT_GENERATION_PLAN.md`.
- Правила и forbidden: `PROJECT_RULES.md`, `CLAUDE.md`.

---

Создан: 2026-05-21
Обновлён: 2026-05-21 (добавлены §9-10 после факт-чека git)
