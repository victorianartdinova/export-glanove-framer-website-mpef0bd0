# CONTENT_GENERATION_RULES.md

> Workflow `template → products.json → generator → pages`.
> Это правила контентного цикла. Архитектура — в `FRAMER_EXPORT_ARCHITECTURE.md`, шаблон — в `PRODUCT_TEMPLATE_SPEC.md`.

---

## 1. Базовый принцип

**Содержимое продуктовых страниц генерируется. Не редактируется руками постранично.**

```
product/avito-ads/index.html  ── template ──┐
                                            ├──► node build-products.mjs ──► product/<slug>/index.html  × N
data/products.json            ── content ───┘                              ──► sitemap.xml (обновление)
                                                                           ──► search-index.json (обновление)
```

- **template** — эталон `product/avito-ads/index.html` **из ветки `main` (origin/main HEAD `ebcf0e8`)**. Один на весь сайт.
- **content** — `data/products.json`. Один файл, массив объектов по schema. **Должен быть в git** (см. `FRAMER_EXPORT_ARCHITECTURE.md` §9).
- **generator** — `scripts/build-products.mjs` (Node + Cheerio). Один скрипт. **Должен быть в git.**
- **pages** — `product/<slug>/index.html` для каждого продукта. Артефакт сборки, но коммитится в git (репозиторий — это и есть deploy-артефакт).

Никаких других путей замены контента в продуктовых страницах не существует.

---

## 2. Запрещённые подходы

| Подход | Почему запрещён |
|---|---|
| Ручное редактирование `product/<slug>/index.html` (4+ копий) | Не масштабируется, рассинхронизирует шаблон, ломается при re-export |
| Патчинг `assets/framer/sites/.../*-v2.mjs` под «перетирание контента» | Контент не должен решаться через runtime. Перетирание = разметка отошла от эталона |
| Поиск решения в `/root/glavnoe-real/` (React) | Другой проект, явно запрещён `PROJECT_RULES.md` |
| Создание JSX-шаблона `ProductPage.tsx` | Это не React-проект |
| Подмена `class="framer-..."`, `data-framer-component-type`, `data-framer-appear-*`, `data-framer-hydrate-v` | Контракт с runtime, ломает гидратацию и стили |
| Создание новой страницы копированием другой дочерней | Только эталон — source of truth (`PRODUCT_TEMPLATE_SPEC.md` §4) |
| Правка sitemap.xml / search-index.json руками | Это артефакты сборки |

---

## 3. Рекомендуемая структура `data/products.json`

JSON-массив, по одному объекту на продукт. Schema извлекается из эталона avito-ads (всё, что отличает продукты).

```jsonc
[
  {
    "slug": "avito-ads",
    "cyrillicSlug": "авито-адс",
    "seo": {
      "title": "Авито Адс | ГЛАВНОЕ",
      "description": "Стратегические партнёры по маркетингу для застройщиков...",
      "ogTitle": "Авито Адс | ГЛАВНОЕ",
      "ogDescription": "...",
      "ogImage": "/assets/framer/assets/Rf8zWc2T6zVsrABCdIoWtdai428.png",
      "ogUrl": "https://glanove.framer.website/product/avito-ads",
      "twitterTitle": "...",
      "twitterDescription": "...",
      "twitterImage": "/assets/framer/assets/Rf8zWc2T6zVsrABCdIoWtdai428.png",
      "canonical": "https://glanove.framer.website/product/avito-ads"
    },
    "content": {
      "hero": {
        "title": "...",
        "subtitle": "...",
        "image": "/assets/.../hero.png",
        "ctaText": "...",
        "ctaHref": "..."
      },
      "brandDescription": "...",
      "features": [
        { "id": "01", "title": "...", "body": "...", "icon": "/assets/.../icon-1.svg" },
        { "id": "02", "title": "...", "body": "...", "icon": "/assets/.../icon-2.svg" }
      ],
      "pricing": {
        "planName": "BASIC PLAN",
        "price": "...",
        "items": ["...", "..."],
        "ctaText": "...",
        "ctaHref": "..."
      },
      "finalCta": {
        "title": "...",
        "buttonText": "CALL US",
        "buttonHref": "..."
      }
    },
    "sitemap": {
      "include": true,
      "priority": 0.8,
      "changefreq": "monthly"
    },
    "searchIndex": {
      "include": true
    }
  }
]
```

**Правила схемы:**
- Schema **выводится из эталона avito-ads**, а не выдумывается. Любое поле имеет соответствие в DOM эталона (по `data-framer-name` или стабильному селектору).
- Все ссылки и пути — относительные либо абсолютные `https://glanove.framer.website/...`, но **согласованные между всеми продуктами**.
- Если у продукта какой-то блок отсутствует — оставлять `null`, генератор по политике решает: скрыть узел или подставить плейсхолдер из эталона.
- Никакой логики в JSON — только данные. Всё «как рендерить» — в генераторе.

---

## 4. Рекомендуемая структура `scripts/build-products.mjs`

Node + Cheerio. Без билд-фреймворков, без сборки сайта целиком.

Логические шаги:

1. **Загрузить эталон.** `fs.readFileSync('product/avito-ads/index.html')` → `cheerio.load(...)`.
2. **Загрузить данные.** `data/products.json`.
3. **Для каждого продукта:**
   - Сделать копию `$` (cheerio root) — не мутировать общий.
   - Подменить `<title>`, все `meta[name="description"]`, `meta[property^="og:"]`, `meta[name^="twitter:"]`, `<link rel="canonical">`.
   - Пройтись по контентным узлам через стабильные селекторы (preferably `[data-framer-name="<name>"]`).
   - Подменить `text()` / `attr('src')` / `attr('href')` согласно `product.content`.
   - Не трогать `class`, `data-framer-component-type`, `data-framer-appear-*`, `data-framer-hydrate-v`.
4. **Записать** в `product/<slug>/index.html`. Создать каталог, если его нет.
5. **Обновить symlink-ы** (если требуется кириллический URL).
6. **Перегенерировать** `sitemap.xml` из `products.json` + статических разделов.
7. **Перегенерировать** `search-index.json` из контента всех продуктов.
8. **Идемпотентность.** Повторный запуск с теми же данными даёт побайтово тот же результат.

Никаких build-watch, никаких HMR. Это batch-скрипт, запускается явно (`node scripts/build-products.mjs`).

---

## 5. Правила генерации новых продуктов

1. Добавить объект в `data/products.json`. Slug — уникальный, ASCII.
2. Если slug нужен с кириллицей в URL — добавить `cyrillicSlug`; генератор создаст symlink (по аналогии с `авито-адс`).
3. Изображения положить в `assets/framer/assets/` или `assets/framer/images/` руками **до** запуска генератора, прописать пути в JSON.
4. Запустить генератор. Проверить:
   - Файл `product/<slug>/index.html` создан.
   - Запись в `sitemap.xml` добавилась.
   - Запись в `search-index.json` добавилась.
   - Страница рендерится локально на 3 viewport.
5. Запустить визуальный диф со эталоном — структура должна совпадать (только контент отличается).
6. Только после этого — коммит (с явным approve пользователя, см. `PROJECT_RULES.md`).

---

## 6. Правила обновления контента существующего продукта

1. Найти объект в `data/products.json` по `slug`.
2. Поменять нужное поле.
3. Запустить генератор. Произойдёт перезапись `product/<slug>/index.html`.
4. **Не трогать руками** сгенерированный HTML — следующий запуск генератора всё равно перезапишет.
5. Визуальный диф → approve → коммит.

---

## 7. Правила обновления SEO

SEO любого продукта правится **только** через секцию `seo` в `products.json`. Запрещено:
- Менять `<title>` руками в `product/<slug>/index.html`.
- Менять OG/Twitter руками.
- Поддерживать «локальные» SEO-патчи поверх генерации.

Если в эталоне появилась новая SEO-тег (например, `<link rel="alternate" hreflang>`) — добавляется в логику генератора, в schema продукта, и применяется ко всем сразу.

---

## 8. Правила обновления sitemap

`sitemap.xml` — **артефакт**, регенерируется на каждый запуск `build-products.mjs`:

- Для каждого продукта с `sitemap.include: true` — добавляется `<url>` с `loc`, `lastmod`, `changefreq`, `priority`.
- Для статических разделов (главная, search, blog list, cases list) — фиксированный список в генераторе.
- Для блог-постов и кейсов — отдельный модуль генератора (если будет требоваться). На текущем этапе они в экспорте уже есть статически.

Запрещено редактировать `sitemap.xml` вручную.

---

## 9. Правила обновления `search-index.json`

Аналогично sitemap — артефакт. Поля индекса (title, description, content excerpt, url) заполняются из `products.json` и из статических разделов. Формат — тот, что ожидает Framer search runtime (см. `<meta name="framer-search-index">` в HTML).

---

## 10. Поведение при re-export

После re-export Framer (новый ZIP от NoCodeExport):

1. **Не сливать** старый и новый экспорт автоматически.
2. Перезаписать `assets/framer/`, эталон `product/avito-ads/index.html`, общие разделы.
3. **Не трогать** `data/products.json` и `scripts/build-products.mjs` — они переживают re-export.
4. Адаптировать `scripts/build-products.mjs` под изменения структуры эталона (если они есть): новые `data-framer-name`, новые секции, изменения SEO.
5. Перезапустить генератор → все продуктовые страницы пересоберутся под новый runtime.
6. Визуальный диф 5 страниц на 3 viewport → approve → коммит.

---

## 11. Чек-лист перед каждым запуском генератора

- [ ] Эталон `product/avito-ads/index.html` валиден и открывается локально.
- [ ] `data/products.json` валиден (JSON parse OK).
- [ ] Все `slug` уникальны.
- [ ] Все ссылки на изображения существуют в `assets/`.
- [ ] Никаких ручных правок в `product/<slug>/index.html` с момента прошлого билда (`git status` чистый по этим файлам).
- [ ] Текущая ветка соответствует `PROJECT_RULES.md` (`runtime-restore-may21` или производная feature-ветка).

---

Создан: 2026-05-21
