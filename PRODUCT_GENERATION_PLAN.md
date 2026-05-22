# PRODUCT_GENERATION_PLAN.md

> План миграции от текущей схемы «4 копии HTML руками» к схеме `template → products.json → generator → pages`.
> Это документ плана. Архитектура — `FRAMER_EXPORT_ARCHITECTURE.md`. Правила цикла — `CONTENT_GENERATION_RULES.md`. Шаблон — `PRODUCT_TEMPLATE_SPEC.md`.

---

## Этап 1. Текущее состояние проекта (baseline, по факту git на 2026-05-21)

**Канонический source of truth — `origin/main` HEAD `ebcf0e8`** (репо `victorianartdinova/export-glanove-framer-website-mpef0bd0`). Полная git-картина — `FRAMER_EXPORT_ARCHITECTURE.md` §9-10.

**Что закоммичено в `main`:**

- Исходный NoCodeExport snapshot (`9934c96`, 225 файлов).
- Чистка футера и брендинга (`6532201`, `0287eb7`).
- Починка кейсов AAG/SPB и ASCII-slug для avito (`ebcf0e8`).
- 5 продуктовых страниц (`product/avito-ads/`, `product/content-product/`, `product/product-statii/`, `product/product-telegram/`, `product/youtube-product/index.html`) с symlink-ом для cyrillic URL.
- Runtime `assets/framer/sites/1OcdQgezFomPwA9UGakYyz/*.mjs` без -v2 патчей.
- `sitemap.xml`, `search-index.json`, `robots.txt`.
- Handoff-документы в `docs/export-overrides/`.

**Что НЕ закоммичено в main, но добавлено локальной веткой `runtime-restore-may21` (5 коммитов поверх):**

- Inline `<script data-glavnoe-safety>` на 15 страницах (`d6f50ad`) — safetyJS, выходит за рамки спецификации.
- `-v2.mjs` post-hydration патчи в runtime (`d6f50ad`, `89d89bb`).
- Контент 4 продуктовых страниц (`89d89bb`).
- Продуктовые карточки и audience-секции на главной (`94e5cc6`).
- Width-фикс десктопа (`11130a2`).

**Что НЕ в git вообще, есть только на VPS (untracked):**

- `CLAUDE.md`, `PROJECT_RULES.md`, `CURRENT_TASK.md`, `README_RESTORE.md` — правила и инструкции.
- 4 архитектурных документа этого набора.

**Папок `data/`, `scripts/` нет ни в одной ветке.**

**Проблемы фактического состояния:**

1. **Правила вне git.** Любой клон с GitHub не увидит ни `CLAUDE.md`, ни `PROJECT_RULES.md`, ни этого плана — проект «без правил» с точки зрения source of truth.
2. **Ветка `runtime-restore-may21` не запушена** — все эксперименты (safetyJS, runtime-патчи, контент 4 страниц) живут локально на VPS. Потеря VPS = потеря 5 коммитов работы.
3. **safetyJS в коммите `d6f50ad`** — post-hydration `<script data-glavnoe-safety>` на 15 страницах. Это решение контентной задачи через runtime, что противоречит `PRODUCT_TEMPLATE_SPEC.md` §6 и `CONTENT_GENERATION_RULES.md` §2.
4. **4 дочерние страницы заполнены руками в `89d89bb`** — рассинхронизация с эталоном уже возможна, дальнейшая поддержка не масштабируется.
5. **При следующем re-export** Framer все ручные правки HTML, safetyJS-скрипты и `-v2.mjs` придётся переносить руками — нет генератора, который бы их воспроизвёл.
6. **`CURRENT_TASK.md` устарел** — описывает uncommitted-состояние до коммита `89d89bb`, фактически работа уже закоммичена в `runtime-restore-may21`.

**Цель миграции:**

a) Зафиксировать правила и архитектуру в git (закоммитить `CLAUDE.md`, `PROJECT_RULES.md`, новые архитектурные документы — после approve пользователя).
b) Заменить ручную поддержку 4 страниц на генератор `template + json`.
c) Снять необходимость в safetyJS — если разметка дочерних страниц приведена к эталону, runtime ничего перетирать не должен.
d) Сделать схему устойчивой к re-export.

---

## Этап 2. Создание `data/products.json`

**Действия:**

1. Создать каталог `data/` в корне репозитория.
2. Извлечь schema из эталона `product/avito-ads/index.html`:
   - Пройти по всем уникальным `data-framer-name` (125 на эталоне — `grep -oE 'data-framer-name="[^"]+"' | sort -u`).
   - Отметить, какие из них являются контентом (см. `PRODUCT_TEMPLATE_SPEC.md` §3), какие — шаблоном.
   - Зафиксировать **content schema** — список полей, которые отличают продукты.
3. Создать `data/products.json` с 5 объектами:
   - 1-й — `avito-ads`, заполненный из эталона (текущие тексты, картинки, ссылки).
   - 4 остальных — заполнить контентом, который сейчас уже впечатан в их uncommitted HTML (вытаскивается тем же скриптом-экстрактором из текущих файлов).
4. Завалидировать JSON, согласовать schema с пользователем.

**Критерии приёмки этапа 2:**
- `data/products.json` парсится.
- Все 5 продуктов представлены.
- Каждое поле schema соответствует существующему узлу в эталоне.
- Пользователь подтвердил список полей.

**Что НЕ делается на этапе 2:**
- Не редактируются HTML продуктов.
- Не пишется генератор.
- Не трогается runtime.

---

## Этап 3. Создание `scripts/build-products.mjs`

**Действия:**

1. Создать каталог `scripts/`.
2. Создать `scripts/build-products.mjs` по спецификации из `CONTENT_GENERATION_RULES.md` §4:
   - Зависимость: `cheerio` (через локальный `package.json` либо `npx --yes cheerio` — финальный выбор обсуждается).
   - Чтение эталона, чтение `products.json`, цикл по продуктам, запись HTML.
   - Логирование: какие узлы подменены, какие — не найдены (warning).
   - Идемпотентность.
3. Прогон на **dry-run режиме**: писать в `tmp/build-out/<slug>/index.html`, не трогать `product/`.
4. Сравнить dry-run результат с текущими uncommitted `product/<slug>/index.html` — диф должен показать только подмену контента, без расхождений шаблона.
5. Если дифы расходятся за пределы контента — править ЛИБО `data/products.json` (если ошибка в данных), ЛИБО `scripts/build-products.mjs` (если ошибка в селекторах). HTML руками не трогать.

**Критерии приёмки этапа 3:**
- `node scripts/build-products.mjs --dry-run` отрабатывает без ошибок.
- Dry-run выход для `avito-ads` побайтово идентичен эталону (sanity check).
- Dry-run выход для остальных 4 страниц отличается от эталона только в контентных узлах.

**Что НЕ делается на этапе 3:**
- Не перезаписываются реальные `product/<slug>/index.html`.
- Не трогается sitemap / search-index.

---

## Этап 4. Генерация страниц

**Действия:**

1. **Резервный коммит** или ветка-снапшот текущего состояния (`runtime-restore-may21-pre-generator`) — для отката.
2. Запустить генератор без `--dry-run`: `node scripts/build-products.mjs`.
3. Скрипт перезапишет 4 дочерние страницы (`content-product`, `product-statii`, `product-telegram`, `youtube-product`).
4. **`avito-ads/index.html` остаётся эталоном** — генератор его не трогает (либо перезаписывает идентично, см. этап 3).
5. Открыть preview (`http://srv1207957.hstgr.cloud:3343/`).
6. Сделать снимки 5 страниц на 3 viewport (390 / 810 / 1440).
7. Визуальный диф с эталоном — структура совпадает, контент отличается.
8. Запустить ревью-агентов (`reality-checker`, `code-reviewer`) с явным `cwd` экспорта.
9. **Если генератор работает корректно — откатить `-v2.mjs` патчи в runtime** (они становятся не нужны, потому что теперь разметка дочерних страниц совпадает с эталоном, и runtime не перетирает узлы).
10. Approve пользователя → коммит → push.

**Критерии приёмки этапа 4:**
- 4 дочерние страницы пересобраны генератором.
- Визуальный диф 3 viewport: только контент отличается, структура идентична эталону.
- Гидратация не перетирает контент → `-v2.mjs` патчи runtime можно убрать.
- Ревью-агенты не нашли регрессий.

**Что НЕ делается на этапе 4:**
- Не трогать runtime, кроме отката `-v2.mjs` (если ревью подтверждает, что они больше не нужны).
- Не менять структуру эталона.

---

## Этап 5. Автоматизация sitemap и search-index

**Действия:**

1. Расширить `scripts/build-products.mjs` модулем регенерации:
   - `sitemap.xml` — на основе `data/products.json` + фиксированный список статических разделов (`/`, `/search`, `/blog`, `/cases`, `/work`, и т.д.).
   - `search-index.json` — на основе title/description/excerpt контента продуктов + статических разделов.
   - Сравнить с текущими файлами, чтобы убедиться, что формат совпадает с тем, что ожидает Framer-search.
2. Прогон → визуальная проверка sitemap и `/search` работает.
3. Зафиксировать договорённость: `sitemap.xml` и `search-index.json` **больше не редактируются вручную никогда**.
4. Approve пользователя → коммит.

**Критерии приёмки этапа 5:**
- `sitemap.xml` собирается генератором, побайтовая разница с исходным минимальна (только реальные изменения, не «переформатирование»).
- `search-index.json` собирается, `/search` работает, ищет по продуктам.
- Документация (`CONTENT_GENERATION_RULES.md` §8-9) обновлена под фактическое поведение генератора.

---

## Этап 6. Поддержка будущих re-export

**Цель:** при каждом следующем re-export из Framer (через NoCodeExport) повторное обновление сайта занимает минуты, а не часы.

**Постоянный playbook:**

1. Получить новый export ZIP от NoCodeExport.
2. Распаковать во временную папку. **Не сливать поверх рабочей** автоматически.
3. Сделать новую ветку `runtime-restore-<date>`.
4. Перенести в репозиторий:
   - Всё `assets/framer/` (runtime chunks, modules).
   - Эталон `product/avito-ads/index.html`.
   - Общие разделы (`index.html`, `blog/`, `cases/`, `work/`, `404/`, `search.html`).
   - Шрифты `assets/fonts/`.
5. **Не переносить** из ZIP дочерние `product/<slug>/index.html` — они будут регенерированы.
6. **Не трогать** `data/products.json`, `scripts/build-products.mjs`, документацию (`*.md`).
7. Адаптировать `scripts/build-products.mjs` под изменения в эталоне (если есть): новые `data-framer-name`, новые секции, новый формат SEO. Изменения в schema `data/products.json` — точечно.
8. Прогнать генератор → 4 дочерние страницы пересобираются.
9. Прогон визуального дифа 5 страниц на 3 viewport.
10. Approve → коммит → push.

**Долгосрочные сигналы**, при которых план пересматривается:
- Количество продуктов перевалило за ~30 → обсудить переезд генератора на Eleventy с `pagination size: 1`. Без изменения принципа (template + json).
- Появился второй тип шаблона (например, отдельный layout для landing-страниц) → завести в `data/` второй файл и второй генератор (`scripts/build-landings.mjs`). Принцип «один шаблон — один файл данных — один генератор» сохраняется.
- Framer перестал быть source of truth дизайна → отдельный pivot, выходит за рамки этого плана.

---

## Соответствие этапов и документов

| Этап | Основные документы |
|---|---|
| 1. Baseline | `CURRENT_TASK.md`, `PROJECT_RULES.md`, `FRAMER_EXPORT_ARCHITECTURE.md` |
| 2. `data/products.json` | `PRODUCT_TEMPLATE_SPEC.md` §3, `CONTENT_GENERATION_RULES.md` §3 |
| 3. `build-products.mjs` | `CONTENT_GENERATION_RULES.md` §4 |
| 4. Генерация страниц | `PRODUCT_TEMPLATE_SPEC.md` §4-7, `CONTENT_GENERATION_RULES.md` §5-6 |
| 5. Sitemap / search-index | `CONTENT_GENERATION_RULES.md` §8-9 |
| 6. Re-export playbook | `FRAMER_EXPORT_ARCHITECTURE.md` §7-8, `CONTENT_GENERATION_RULES.md` §10 |

---

Создан: 2026-05-21
