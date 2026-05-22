# RESEARCH_HANDOFF_2026-05-21.md

> Сводка исследования и фактического состояния проекта `full-site-export-may21` на 2026-05-21.
> Документ создан в ответ на серию research-задач; никаких изменений в HTML / runtime / product pages в ходе исследования не вносилось.
> Следующая сессия начинает с этого файла. Новое исследование не запускать.

---

## 1. Источник истины проекта (по git)

**Origin URL:** `git@github.com:victorianartdinova/export-glanove-framer-website-mpef0bd0.git`

**Main branch:** `main` (на origin), HEAD `ebcf0e8`.

**Текущая ветка:** `runtime-restore-may21` (локальная, на origin отсутствует).

**Список локальных веток:**

| Ветка | Состояние |
|---|---|
| `main` | Совпадает с `origin/main`, HEAD `ebcf0e8` |
| `content-filled-static-fallback` | Совпадает с `main`, HEAD `ebcf0e8` |
| `runtime-restore-may21` | `main` + 5 локальных коммитов, HEAD `89d89bb` |

**Ветки только локально (не запушены на origin):**
- `runtime-restore-may21`
- `content-filled-static-fallback`

**Ветки на origin:** только `main`.

**`full-site-export-may20-stable`** (упоминается в `PROJECT_RULES.md` как запрещённая) — **не существует** ни локально, ни на origin. Запись устарела либо относилась к другой папке.

### Source of truth

- **Source of truth проекта = `origin/main` HEAD `ebcf0e8`**. Все архитектурные решения принимаются на основе main, не текущей рабочей ветки.
- **Экспериментальная ветка = `runtime-restore-may21`**. Содержит 5 коммитов локальной работы (runtime-restore, safetyJS, заливка 4 страниц). Не запушена. Не является источником архитектурных решений.
- **Fallback ветка = `content-filled-static-fallback`**. Идентична main, существует как safe checkpoint.

---

## 2. История проекта (git log)

### Main (4 коммита, автор Victoria Nartdinova)

| SHA | Сообщение | Назначение |
|---|---|---|
| `9934c96` | Deploy from NoCodeExport | **Исходный NoCodeExport snapshot** — 225 файлов, 6374 insertions. Начальная точка проекта. |
| `6532201` | chore(overrides): footer labels match header + Sasha/channel links | Корректировка футера, ссылки на канал и Сашу. |
| `0287eb7` | chore(meta): replace Fuel template branding with ГЛАВНОЕ + avito footer fix | Снятие шаблонного брендинга NoCodeExport, замена на ГЛАВНОЕ. |
| `ebcf0e8` | fix(content): unbreak product/case pages + fill AAG/SPB bodies + ASCII avito URL | **HEAD origin/main.** Починка продуктовых/кейс-страниц, заливка AAG/SPB кейсов, ASCII-slug для avito. |

### runtime-restore-may21 (+5 коммитов поверх main)

| SHA | Сообщение | Что вносит |
|---|---|---|
| `d6f50ad` | fix(runtime): restore Framer JS bundle + minimal post-hydration patch | Возвращает Framer runtime script_main; добавляет inline `<script data-glavnoe-safety>` на 15 страниц (safetyJS), переименовывает chunks в `-v2.mjs`. |
| `94e5cc6` | feat(content): home product cards + audience sections + overlap/footer fixes | Продуктовые карточки и audience-секции на главной. |
| `ae9a86e` | docs: session handoff 2026-05-21 — product cards next task | Handoff-документ в `docs/`. |
| `11130a2` | fix(home): product cards full-width on desktop (scenario B) | Width-фикс десктопа главной (max-width:1392px → width:100%). |
| `89d89bb` | feat(products): wire 4 product pages to static routes with own content | **HEAD runtime-restore-may21.** Заливка контента 4 продуктовых страниц + новые `-v2.mjs`. |

### Ключевые наблюдения

- В main **нет** safetyJS, **нет** `-v2.mjs`, **нет** заполненного контента 4 продуктовых страниц.
- safetyJS появился именно в `d6f50ad` — как реакция на «hydration mismatch» / «React #405».
- Заливка 4 страниц (`89d89bb`) сделана **поверх** safetyJS — без него ситуация не была решена.

---

## 3. Архитектура Framer Export (сводка)

### Что это
Статический snapshot сайта `glanove.framer.website` через **NoCodeExport** в режиме **Maximum Fidelity Mode**. React-runtime Framer-а замиррорен локально (~60 mjs chunks, ~92 МБ). Это **не React-проект**, не SSG, не Next.js.

### Где что лежит

| Что | Где |
|---|---|
| Страницы | `index.html`, `product/<slug>/index.html`, `blog/<slug>/index.html`, `cases/portfolio/<slug>/`, `work/<slug>/index.html`, `404/index.html`, `search.html` |
| Framer runtime | `assets/framer/sites/1OcdQgezFomPwA9UGakYyz/*.mjs` (entrypoint — `script_main.<hash>.mjs`) |
| Внешние модули | `assets/framer/modules/` (Video, fontshare, third-party) |
| Картинки/ассеты | `assets/framer/images/`, `assets/framer/assets/` |
| Шрифты | `assets/fonts/*.woff2` |
| Контент | **впечатан в HTML как DOM-узлы**, размечен `data-framer-name`, `data-framer-component-type`, и др. JSON data layer отсутствует |
| Карта сайта | `sitemap.xml`, `search-index.json`, `robots.txt` |
| Handoff/SEO | `docs/`, `seo-report/` |

### Природные ограничения экспорта

1. **Нет CMS-API.** Поиск/фильтрация/коллекции заморожены. Каждый CMS-айтем — отдельный HTML.
2. **Нет JSON data layer.** Контент впечатан в HTML.
3. **Runtime обфусцирован.** mjs не редактируется как обычный код.
4. **Hash rotation.** Каждый republish во Framer ротирует имена chunks. Старые URL живут на Framer CDN ~2 недели.
5. **Часть ассетов внешние.** Некоторые шрифты и image-resize варианты грузятся с `framerusercontent.com`.
6. **Формы внешние.** `<form action>` указывает на исходный backend (Formspree и т.п.).
7. **Гидратация может перетирать DOM.** Если разметка дочерней страницы не совпадает с тем, что ожидает runtime, — он переписывает узлы при mount-е.

### Когда нужен re-export
- Смена дизайна/брендинга/палитры во Framer.
- Новые типы секций или компонентов.
- Изменилась глобальная навигация.
- Прошло ~2 недели и оригинал во Framer активно правится.
- Старые chunk-URL начали 404.

### Когда re-export НЕ нужен
- Меняется текст/заголовок/цена/CTA/картинка секции.
- Добавляются новые страницы по существующему шаблону.
- Чинятся SEO-теги, sitemap, robots.
- Обновляется контент блог-постов / кейсов.

**Правило:** дизайн и runtime ⇒ re-export. Контент ⇒ template + json + генератор.

---

## 4. ГЛАВНЫЙ ВЫВОД ИССЛЕДОВАНИЯ

> ### AVITO ADS = MASTER TEMPLATE
>
> Все продуктовые страницы строятся на основе:
>
>     product/avito-ads/index.html  (из origin/main HEAD ebcf0e8)
>
> Продуктовые страницы **не являются самостоятельными дизайнами**.
>
> Продуктовые страницы являются **экземплярами одного шаблона**.
>
> Меняется **только контент**.
>
> **Структура страниц должна оставаться одинаковой** (DOM-иерархия, все `data-framer-*`, классы `framer-*`, CSS-блоки, runtime entrypoint).
>
> Предпочтительная архитектура:
>
>     template → products.json → generator → pages
>
> - template: `product/avito-ads/index.html` (один на весь сайт)
> - products.json: контент-схема, по объекту на продукт
> - generator: `scripts/build-products.mjs` (Node + Cheerio)
> - pages: `product/<slug>/index.html` × N (артефакт сборки, коммитится в git)

Это архитектурное правило проекта. Зафиксировано в `PRODUCT_TEMPLATE_SPEC.md`, `CONTENT_GENERATION_RULES.md`, `PRODUCT_GENERATION_PLAN.md`.

---

## 5. Что уже проверено (исследованные гипотезы)

| # | Гипотеза | Что проверялось | Подтвердилось? |
|---|---|---|---|
| 1 | **HTML-замена** — менять контент прямо в `product/<slug>/index.html` руками | Сделано в коммите `89d89bb` для 4 страниц | Частично работает, но **не масштабируется** на 20-50 страниц и рассинхронизирует шаблон |
| 2 | **Hydration mismatch как причина** того, что Framer runtime перетирает DOM | Описано в `d6f50ad`: React #405, ситуации с visibility:hidden, opacity:0/translateY(40px) | Подтверждено как симптом; **первопричина** — разметка дочерних страниц отошла от того, что ожидает runtime |
| 3 | **Runtime-патчи через `-v2.mjs`** — править chunks, чтобы они не перетирали контент | Сделано в `d6f50ad`, `89d89bb` (replace `<hash>.mjs` на `<hash>-v2.mjs`) | Антипаттерн: лечит симптом, не причину; ломается при re-export Framer |
| 4 | **safetyJS** — inline `<script data-glavnoe-safety>` на каждой странице, чинит DOM post-hydration (`fixOpacity`, `fixVisibility`, `ensureAbout`, `ensureCaseBody`, `hideEmpty`) | Сделано в `d6f50ad` на 15 страниц | Работает как костыль; **противоречит** архитектурному правилу «контент не решается через runtime»; усложняет re-export |
| 5 | **`-v2.mjs` chunks** как способ распространить runtime-патчи | Сделано в `d6f50ad`, `89d89bb` | См. п.3 — антипаттерн |
| 6 | **Route experiments** — `wire 4 product pages to static routes with own content` | Сделано в `89d89bb` (faktic-маршруты + контент) | Маршрутизация рабочая (5 product/<slug>/ + symlink для cyrillic); проблема не в маршрутах, а в контенте |
| 7 | **Ручное заполнение страниц** | Сделано в `89d89bb` | Работает на 4 страницах; не масштабируется; нет единого источника контента |
| 8 | **template + json + generator** (Node + Cheerio) | Только теоретическое исследование (web-research + аудит структуры эталона: 125 уникальных `data-framer-name`) | **Не реализовано в коде.** Архитектурно зафиксировано в `CONTENT_GENERATION_RULES.md` и `PRODUCT_GENERATION_PLAN.md` как целевая схема |
| 9 | **React-rebuild / переход на Next.js / покупка CMS** | Отвергнуто пользователем явно и `PROJECT_RULES.md` | Не применяется |

---

## 6. Что НЕ повторять

Без новых фактов **не запускать** следующие линии исследования:

- ❌ Очередной поиск причин hydration mismatch / React #405. Корень — разметка дочерних страниц расходится с эталоном. Решение — генератор, не runtime-патчи.
- ❌ Обсуждение переэкспорта Framer как способа починить контент. Re-export нужен только для дизайна/runtime, не для контента (см. §3).
- ❌ Создание новых дизайнов отдельных product pages. Продуктовая страница = экземпляр шаблона.
- ❌ Ручную поддержку множества копий страниц. Не масштабируется. Не делать.
- ❌ Архитектурные обсуждения без `git status` / `git log` / `git diff --stat`. Опираться на CURRENT_TASK.md / PROJECT_RULES.md без сверки с git — даёт устаревшую картину (см. §7, §9).
- ❌ Эксперименты с React rebuild, Next.js, покупкой CMS, ProductPage.tsx, `/root/glavnoe-real/` — все запрещены `PROJECT_RULES.md`.
- ❌ Новые safetyJS-скрипты или `-v2.mjs` патчи. Если runtime перетирает контент — править разметку, не runtime.

---

## 7. Текущее состояние продуктовых страниц

### Факты от структурного анализа (grep + diff на 2026-05-21)

Все 5 продуктовых страниц на ветке `runtime-restore-may21` имеют **идентичную метрическую структуру**:

| Страница | Размер (bytes) | Уникальных `data-framer-name` | Всего `data-framer-name` |
|---|---|---|---|
| `product/avito-ads/index.html` (эталон) | 461 668 | 125 | 548 |
| `product/content-product/index.html` | 461 558 | 125 | 548 |
| `product/product-statii/index.html` | 461 775 | 125 | 548 |
| `product/product-telegram/index.html` | 461 635 | 125 | 548 |
| `product/youtube-product/index.html` | 461 726 | 125 | 548 |

`diff <sorted unique data-framer-name avito> <sorted unique data-framer-name <each child>>` для всех 4 дочерних — **пустой**. Набор `data-framer-name` совпадает 1:1.

Разница в размере (±200 байт) объясняется длиной текстового контента, а не структурой.

### Утверждение пользователя (на верификацию)

Заявлено как причина «ЗАДАЧА НЕ ВЫПОЛНЕНА»:

- Тарифный блок отличается.
- Блок процесса отличается.
- Блок результатов отличается.
- Текущие страницы — собственные вариации, а не клоны Avito Ads.

### Совмещение фактов

`data-framer-name`-метрика структуры **совпадает у всех 5 страниц** — это говорит, что Framer-классы и иерархия секций сохранены. Утверждение пользователя про различия в тарифном/процесс/результаты-блоках может относиться к:
- Текстовому **содержанию** этих блоков (это контент, не структура).
- Тонким различиям в **порядке** узлов (set-diff не ловит порядок).
- Различиям в `class="framer-..."` или нумерации (`Desktop Card 1` vs `Desktop Card 4`).
- Визуальному рендеру (включая поведение safetyJS / `-v2.mjs`).

**Это исследование не проведено** структурно (полный diff DOM-дерева, не set-diff). В следующей сессии — **не запускать новое исследование**, а делать продуктовую задачу (см. §8); structural diff делается в рамках самой задачи как первый шаг.

### Статус задачи

**ЗАДАЧА НЕ ВЫПОЛНЕНА** — формальная фиксация пользователя.

**Причина (по заявлению пользователя):** Структура страниц отличается от Avito Ads. Отличаются: тарифный блок, блок процесса, блок результатов. Текущие страницы являются собственными вариациями, а не клонами Avito Ads.

**Причина (на основании git):** Заливка 4 страниц в `89d89bb` опиралась на runtime safetyJS из `d6f50ad`, а не на дисциплину «копия эталона». Поэтому контентные блоки могли расходиться с эталоном на уровне текстовой/визуальной структуры, даже если `data-framer-name`-сет совпал.

---

## 8. Следующий шаг для новой сессии

> Следующая сессия **НЕ запускает новое исследование**.
> Следующая сессия выполняет продуктовую задачу.

### Цель

Привести 4 страницы к структуре Avito Ads:

- `product/content-product/index.html`
- `product/product-statii/index.html`
- `product/product-telegram/index.html`
- `product/youtube-product/index.html`

### Что сохранить

- Порядок секций.
- Структуру секций.
- Карточки тарифов.
- Блок процесса.
- Блок результатов.

### Правило изменений

- Менять **только контент** внутри шаблона (тексты, цифры, картинки, ссылки).
- **Не менять** структуру секций.
- **Не менять** Framer-классы и `data-framer-*` атрибуты.
- Эталон берётся **из `product/avito-ads/index.html` на ветке `main`** (без safetyJS и `-v2.mjs`). Если нужно — `git show main:product/avito-ads/index.html`.

### Рекомендуемый порядок шагов (для следующей сессии)

1. Перечитать этот файл (`RESEARCH_HANDOFF_2026-05-21.md`).
2. Перечитать `PRODUCT_TEMPLATE_SPEC.md`, `CONTENT_GENERATION_RULES.md`.
3. Извлечь эталон из main: `git show main:product/avito-ads/index.html` → во временный файл для diff.
4. Для каждой из 4 страниц: structural diff с эталоном → список блоков, где **структура** отличается.
5. Привести структуру дочерних страниц к эталону (без правки runtime и без safetyJS).
6. Контент подменить руками или, если объём оправдан, реализовать минимальный `scripts/build-products.mjs` по `CONTENT_GENERATION_RULES.md`.
7. Снять снимки 3 viewport (390/810/1440), сверить с эталоном.
8. Approve пользователя → коммит → push.

---

## 9. Документация проекта (на 2026-05-21)

| Файл | Существует | В git | Tracked | Актуален |
|---|---|---|---|---|
| `CLAUDE.md` | ✅ | ❌ | untracked | требует обновления (см. §10 + ранее предложенная секция PRODUCT PAGE RULES) |
| `PROJECT_RULES.md` | ✅ | ❌ | untracked | требует обновления (запись про ветку `full-site-export-may20-stable` — устарела; пункт ALLOWED про `.mjs` правки противоречит §6 этого документа) |
| `CURRENT_TASK.md` | ✅ | ❌ | untracked | **устарел** — описывает состояние до коммита `89d89bb`, фактически работа закоммичена |
| `README_RESTORE.md` | ✅ | ❌ | untracked | актуален |
| `FRAMER_EXPORT_ARCHITECTURE.md` | ✅ | ❌ | untracked | актуален (создан + обновлён 2026-05-21) |
| `PRODUCT_TEMPLATE_SPEC.md` | ✅ | ❌ | untracked | актуален (создан + обновлён 2026-05-21) |
| `CONTENT_GENERATION_RULES.md` | ✅ | ❌ | untracked | актуален (создан + обновлён 2026-05-21) |
| `PRODUCT_GENERATION_PLAN.md` | ✅ | ❌ | untracked | актуален (создан + обновлён 2026-05-21) |
| `RESEARCH_HANDOFF_2026-05-21.md` | ✅ | ❌ | untracked | этот файл, актуален |

**Tracked `.md` в git (то, что реально является документацией проекта на текущий момент):**

- `README.md`, `RUN_LOCALLY.md` — сгенерированы NoCodeExport, не редактируемы вручную.
- `seo-report/README.md`.
- `docs/SESSION_HANDOFF_2026-05-21_PRODUCT_CARDS.md` (закоммичен в `ae9a86e`, есть локальные правки).
- `docs/export-overrides/NIGHT-PENDING-2026-05-20.md`.
- `docs/export-overrides/PENDING-cases-portfolio-2026-05-20.md`.
- `docs/export-overrides/footer-and-links-2026-05-20.md`.

То есть **ни одна архитектурная инструкция / правило не находится в git**. Это критическое расхождение, требующее коммита.

---

## 10. Git рекомендации

### Файлы, которые НЕОБХОДИМО добавить в git (после approve пользователя)

Корневые архитектурные документы:

- `CLAUDE.md`
- `PROJECT_RULES.md` (с уточнением: ветка `full-site-export-may20-stable` — убрать или подтвердить; пункт ALLOWED про правку `.mjs` — переформулировать)
- `CURRENT_TASK.md` (обновить под фактическое git-состояние; либо удалить как устаревший и заменить ссылкой на этот handoff)
- `README_RESTORE.md`
- `FRAMER_EXPORT_ARCHITECTURE.md`
- `PRODUCT_TEMPLATE_SPEC.md`
- `CONTENT_GENERATION_RULES.md`
- `PRODUCT_GENERATION_PLAN.md`
- `RESEARCH_HANDOFF_2026-05-21.md` (этот файл)

После реализации генератора (этапы 2-5 плана):

- `data/products.json`
- `scripts/build-products.mjs`
- `package.json` + `package-lock.json` (зависимость `cheerio`)
- `.gitignore` (которого сейчас нет)

### Файлы, которые НЕ должны храниться в git

- `node_modules/`
- Временные snapshot-папки puppeteer/playwright (`/tmp/...`, `tmp/`)
- Локальные `.env`, секреты, токены
- PID-файлы dev-сервера
- Локальные кеши, build-output вне репозитория (`.cache/`, `dist-local/`)

Их нужно явно прописать в `.gitignore` при его создании.

### Предлагаемая структура документации проекта

```
full-site-export-may21/
├── CLAUDE.md                         # инструкции агенту (override глобальный)
├── PROJECT_RULES.md                  # правила, forbidden, allowed, протоколы
├── CURRENT_TASK.md                   # операционная задача текущей сессии
├── README.md                         # NoCodeExport-generated, не править
├── README_RESTORE.md                 # клон-протокол
├── RUN_LOCALLY.md                    # NoCodeExport-generated, как запускать
│
├── FRAMER_EXPORT_ARCHITECTURE.md     # архитектура экспорта (что внутри, границы)
├── PRODUCT_TEMPLATE_SPEC.md          # шаблон продуктовой страницы
├── CONTENT_GENERATION_RULES.md       # workflow template + json + generator
├── PRODUCT_GENERATION_PLAN.md        # план миграции к генератору
├── RESEARCH_HANDOFF_2026-05-21.md    # сводный handoff (этот файл)
│
├── docs/
│   ├── SESSION_HANDOFF_<date>_<topic>.md   # handoff между сессиями
│   └── export-overrides/                    # override-доки от NoCodeExport
│
├── data/                             # (после этапа 2 плана)
│   └── products.json
├── scripts/                          # (после этапа 3 плана)
│   └── build-products.mjs
│
├── product/, blog/, cases/, work/    # генерируемый/правленый HTML
└── assets/                           # runtime + статика
```

---

## Контрольный снапшот команд (для воспроизведения этого handoff)

```bash
git remote -v
git branch -a
git log --oneline -30
git status --short
git diff --stat main..HEAD
git show --stat 9934c96 ebcf0e8 d6f50ad 89d89bb
git ls-files | wc -l
git ls-files '*.md' | grep -v docs/
```

---

Создан: 2026-05-21
Автор: research session (Claude, по запросу пользователя)
