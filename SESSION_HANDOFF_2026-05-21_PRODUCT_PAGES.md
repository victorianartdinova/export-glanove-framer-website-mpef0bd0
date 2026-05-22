# SESSION HANDOFF — 2026-05-21 — PRODUCT PAGES

## Проект

Рабочая директория: `/root/framerexport/full-site-export-may21`
Ветка: `runtime-restore-may21`
Master template: `product/avito-ads/index.html`
Preview: `http://srv1207957.hstgr.cloud:3343/`

---

## Что было целью

Использовать Avito Ads как master template для:

- `product/content-product/`
- `product/product-statii/`
- `product/product-telegram/`
- `product/youtube-product/`

Менять только контент. Структура секций, классы Framer и DOM-иерархия — байт-в-байт от эталона.

---

## Что выполнено

Зафиксировано как факт:

- 4 страницы переведены на шаблон Avito Ads (byte-for-byte клон HTML + override).
- Структура секций совпадает с Avito Ads: hero → audience 3 cols → тарифы → «КАК БУДЕМ РАБОТАТЬ» → about → big number → партнёры → pre-footer → footer.
- Flash «Авито Адс» устранён: hero подменяется до первого paint (синхронный pass + MutationObserver).
- Hero подменяется до первого отображения для всех 4 продуктов (проверено через playwright на DOMContentLoaded).
- Content Product hero исправлен на «Коммуникационная стратегия».
- Тарифный блок:
  - content-product, product-statii, product-telegram — **3 карточки** (Tier 1 + Tier 2 + добавочный Tier 3 = клон белой карточки Avito, prepend перед Tier 1).
  - youtube-product — **2 карточки** как в Avito.
  - На desktop карточки делят ширину контейнера (`flex: 1 1 0`); на tablet/mobile Framer-媒体запросы переводят контейнер в колонку.
- Блок процесса использует структуру Avito (тёмный капсульный блок «КАК БУДЕМ РАБОТАТЬ»).
- Блок результата использует структуру Avito (одна красная плитка big number).
- Длинный параграф под процессом подменён на product-specific; hidden measure-ref wrap-spans с Avito-текстом занулены.
- Кнопка CTA в процесс-блоке (Avito: «СБОРКА КАМПАНИИ») подменена на product CTA.
- Mobile/tablet Framer-fallback («PREMIUM PLAN»/«For enterprise and organizations»/«12000») подменён на product Tier 2 содержимое — на product-страницах. На самой `avito-ads` баг сохранён (эталон не трогали).

---

## Какие файлы были изменены

### Tracked, modified (`git status -M`):

- `product/content-product/index.html` — клон Avito Ads + inline override script.
- `product/product-statii/index.html` — то же.
- `product/product-telegram/index.html` — то же.
- `product/youtube-product/index.html` — то же.
- `docs/SESSION_HANDOFF_2026-05-21_PRODUCT_CARDS.md` — handoff предыдущей сессии (был модифицирован раньше, в этой сессии не трогали).

### Untracked (новые файлы):

- `scripts/clone-and-content.py` — переклонирует 4 child HTML из master Avito (использовался один раз).
- `scripts/inject-override.py` — инжектит override-script в 4 child HTML (запускался многократно).
- `SESSION_HANDOFF_2026-05-21_PRODUCT_PAGES.md` — этот файл.

Корневые архитектурные доки (`CLAUDE.md`, `PROJECT_RULES.md`, `PROJECT_MEMORY.md`, `RESEARCH_HANDOFF_2026-05-21.md`, `PRODUCT_TEMPLATE_SPEC.md`, `CURRENT_PRODUCT_STATUS.md`, `FRAMER_EXPORT_ARCHITECTURE.md`, `CONTENT_GENERATION_RULES.md`, `PRODUCT_GENERATION_PLAN.md`, `CURRENT_TASK.md`, `README_RESTORE.md`) — untracked, в этой сессии не модифицировались.

### .mjs изменения

В этой сессии `.mjs` chunks **не трогались**. Существующие `-v2.mjs` (от предыдущей сессии) — без изменений.

---

## Как реализовано

Каждый из 4 child HTML — byte-for-byte клон `product/avito-ads/index.html` со вставленным inline `<script data-glavnoe-product-override="<slug>">` сразу после открывающего `<body>` тега.

Содержимое override-скрипта (логика):

1. **Синхронный pass на парсинге HTML.** При выполнении `<script>` сразу же пробегается по `document.body` и подменяет все exact-match text nodes по таблице REPLACEMENTS (source → target). Это гарантирует подмену hero / тарифов / параграфов до первого paint.
2. **applyMetaOverrides** — синхронно: `document.title`, `meta[name=description]`, `og:title`, `og:description`, `twitter:title`, `twitter:description`.
3. **MutationObserver на `document.body`** (`childList`, `subtree`, `characterData`) — ловит любые узлы, которые Framer добавляет/перерисовывает во время гидрации, и тут же подменяет их. Наблюдатель отключается через 6 секунд после `window.load`.
4. **Tier-3 инжекция (`injectThirdTier`)** — после `window.load + 800ms`:
   - Находит контейнер `.framer-17whp4j` (родитель двух карточек).
   - Клонирует первую карточку (Tier 1, Desktop Primary, белая).
   - Внутри клона подменяет name/desc/price (`SRC2DST` = `[tier1_name → tier3_name, tier1_desc → tier3_desc, price1 → tier3_price]`).
   - Помечает клон атрибутом `data-glavnoe-tier-clone="1"`.
   - Меняет ширину контейнера на `100%`, у каждой из 3 карточек — `flex: 1 1 0; min-width: 0; width: auto`.
   - Prepend клона перед Tier 1 (порядок: Tier3 audit | Tier1 base | Tier2 premium).
   - Guard `data-glavnoe-tier-third="1"` исключает повторную инжекцию.
   - `maybeReplace` пропускает узлы внутри клона (`closest('[data-glavnoe-tier-clone="1"]')`), чтобы основной REPLACEMENTS map не возвращал tier3 цифры обратно к tier1.
5. **About-paragraph handler (`replaceAboutParagraph`)** — на `section[data-framer-name="About"]`:
   - Один text node, равный полному Avito-параграфу, → product-specific paragraph.
   - Все остальные text nodes внутри `About`, содержащие фрагменты Avito-текста (`/Авито|сегментам|аналитикой —|конкурентов,|CPL до|A\/B тесты|квиз-/`), → пустая строка (это hidden measure-ref wrap-spans).

### Селекторы

- `.framer-17whp4j` — контейнер тарифных карточек.
- `section[data-framer-name="About"]` — секция с длинным параграфом.
- `meta[name="description"]`, `meta[property="og:title"]`, и т.д. — meta-теги.
- Все остальные подмены — exact text node match по таблице REPLACEMENTS.

### Данные REPLACEMENTS (на каждый продукт)

- `Авито Адс` → hero title
- 3 строки caption под hero
- Tier 1 name / desc / price
- Tier 2 name / desc / price + mobile fallback (PREMIUM PLAN / For enterprise and organizations / 12000)
- `Всё из тарифа «Только реклама»` → `Всё из тарифа «{tier1_label}»`
- `1000` → big number
- `отношение к результатам` → stat label
- Полный About-параграф → product paragraph
- `СБОРКА КАМПАНИИ` → product CTA
- Tier 2 mobile-variant bullets (3 фразы на английском) → нейтральные ru-замены

---

## Текущее состояние страниц

### content-product

URL: `http://srv1207957.hstgr.cloud:3343/product/content-product/`

- hero: **Коммуникационная стратегия**
- captions: `(контент + СМИ)` / Кросс-платформенная контент-система: продажи, найм, экспертность. Для команд с минимумом ресурсов. / `контент/стратегия`
- тарифы: **3** карточки — КОНТЕНТ-АУДИТ 80 k. | КОНТЕНТ 150 k. | КОНТЕНТ + HR-БРЕНД 280 k.
- big number: **500+** запусков контент-систем
- about: «Запускаем кросс-платформенную контент-систему: продажи, найм, экспертность. Стратегия, продакшен и дистрибуция в каналах. Аудит площадок, контент-план, A/B тесты заголовков и контроль CTR от просмотра до заявки.»
- CTA процесса: **ЗАПУСК СИСТЕМЫ**
- статус: hero/title/тарифы/параграф/CTA/big number — подменены на desktop/tablet/mobile. Stale Avito-строк не обнаружено.

### product-statii

URL: `http://srv1207957.hstgr.cloud:3343/product/product-statii/`

- hero: **Рекламная стратегия**
- captions: `(стратегия + прогноз)` / Медиаплан с прогнозом продаж. Экономия 30% бюджета. Аналитика и контроль CPL по каналам. / `стратегия/медиа`
- тарифы: **3** карточки — АУДИТ РЕКЛАМЫ 80 k. | МЕДИАПЛАН 200 k. | СТРАТЕГИЯ + ЗАПУСК 400 k.
- big number: **300+** рекламных стратегий для застройщиков
- about: «Разрабатываем рекламную стратегию с прогнозом продаж: медиаплан по каналам, бюджеты и KPI. Аудит конкурентов, сегментация аудитории, A/B тесты гипотез и контроль CPL по каналам — от первого показа до сделки.»
- CTA процесса: **СБОРКА СТРАТЕГИИ**
- статус: ok на desktop/tablet/mobile. Stale Avito-строк не обнаружено.

### product-telegram

URL: `http://srv1207957.hstgr.cloud:3343/product/product-telegram/`

- hero: **Лидген Telegram**
- captions: `(трафик + канал)` / Реклама в Telegram + квиз-лендинг + сквозная аналитика. CPL в 2 раза ниже рынка. / `лиды/Telegram`
- тарифы: **3** карточки — АУДИТ КАНАЛА 120 k. | ЗАПУСК РЕКЛАМЫ 165 k. | РЕКЛАМА + КАНАЛ 220 k.
- big number: **800+** заявок из Telegram-рекламы
- about: «Запускаем лидогенерацию в Telegram со сквозной аналитикой — от первого показа до заявки в CRM. Аудит конкурентов, сегментация аудитории, квиз-лендинг, A/B тесты и контроль CPL до сделки.»
- CTA процесса: **ЗАПУСК TELEGRAM**
- статус: ok на desktop/tablet/mobile. Stale Avito-строк не обнаружено.

### youtube-product

URL: `http://srv1207957.hstgr.cloud:3343/product/youtube-product/`

- hero: **Личный бренд YouTube**
- captions: `(продюсирование)` / Сценарии + продюсирование + запуск канала. Высокие охваты в узкой нише за 1.5 недели. / `охваты/YouTube`
- тарифы: **2** карточки — ЗАПУСК КАНАЛА 180 k. | КАНАЛ + ПРОДЮСИРОВАНИЕ 300 k.
- big number: **50+** личных брендов основателей
- about: «Запускаем YouTube-канал с продюсерским контролем: сценарии, продакшен, дистрибуция и монетизация. Аудит конкурентов, упаковка эксперта, A/B заголовков и обложек, рост охватов в нише.»
- CTA процесса: **ЗАПУСК КАНАЛА**
- статус: ok на desktop/tablet/mobile. Stale Avito-строк не обнаружено.

---

## Оставшиеся задачи

1. **Добавить подпись под тарифным блоком** на все 4 product-страницы:

   > Нужен другой формат работы?
   >
   > Мы открыты к индивидуальным задачам и нестандартным условиям сотрудничества. Расскажите о вашем проекте — предложим оптимальное решение под ваши цели и вводные данные.

2. **Bullets внутри тарифных карточек** на всех 4 продуктах — содержат Avito-default, не подменяются автоматически:
   - Tier 1 (белая): «Управление кампаниями и бюджетом», «Разработка баннеров 3–5 шт/1 оффер», «Отчёты 4 раза/мес "план-факт"».
   - Tier 2 (красная): «Cтратегия заявок до квалификации», «Разработка технического задания на посадочные», «Разработка посадочной страницы», «Настройка рекламы на канал, если посадочная не подошла», «гиперСегментация ЦА и подбор офферов».
   - Tier 3 (клон Tier 1): унаследовал bullets Tier 1.
   - Telegram частично подходит; для остальных требуются product-specific формулировки.

3. **«Кому подходит» (audience cards)** — Framer заполняет своим механизмом из CMS. На content-product визуально видно `Когда соцсети дают до 50% лидов и нужна стратегия, а не разовые посты` (product-specific). На statii/telegram/youtube детально не верифицированы — нужна визуальная проверка.

4. **avito-ads (эталон) на tablet/mobile** показывает шаблонный «PREMIUM PLAN / For enterprise and organizations / 12000» вместо «РЕКЛАМА + ПОСАДОЧНАЯ». Это исходный баг Framer-экспорта tablet/mobile варианта тарифной карточки. На product-страницах исправлено через REPLACEMENTS; на самой Avito — оставлено как есть (эталон не трогали).

5. **Проверить весь контент страниц на соответствие ТЗ** по каждой секции.

6. **Проверить desktop / tablet / mobile** визуально (скриншоты или live) — на текущий момент проверены только тарифные карточки и hero/title/CTA/big number; полноэкранная визуальная сверка с эталоном не делалась.

7. **Коммит изменений** — текущая сессия завершена без коммита. Изменены 4 product HTML + 1 modified doc + новый script-каталог + новый handoff. Ждёт approve.

---

## Проверено и работает

### Страницы, прошедшие автоматическую проверку:

- `product/content-product/` — desktop / tablet / mobile.
- `product/product-statii/` — desktop / tablet / mobile.
- `product/product-telegram/` — desktop / tablet / mobile.
- `product/youtube-product/` — desktop / tablet / mobile.
- `product/avito-ads/` — desktop (как эталон).

### Виды проверок:

- **No-flash hero/title** — playwright snapshot на `DOMContentLoaded`: для всех 4 продуктов `document.title` и первый `<h2>` уже содержат product content без «Авито Адс».
- **Количество тарифных карточек** — content/statii/telegram = 3 на всех viewport; youtube = 2 на всех viewport; avito = 2 на всех viewport.
- **Содержимое тарифных карточек** — title/price подменены корректно (АУДИТ * / Tier 1 / Tier 2).
- **No-overflow** — `document.documentElement.scrollWidth <= window.innerWidth` на всех 3 viewport для всех 4 продуктов.
- **Hidden-Avito-text** — `walk-by-visible-text` не находит на product-страницах ни одной из:
  `'Авито Адс'`, `'Авито со сквозной'`, `'СБОРКА КАМПАНИИ'`, `'PREMIUM PLAN'`, `'For enterprise'`, `'12000'`.

### Баги исправлены в этой сессии:

- Flash «Авито Адс» при первом paint.
- Content Product hero вместо «Контент-маркетинг» → «Коммуникационная стратегия».
- Tier-3 цена клонировалась с Tier 1 → добавлен guard `data-glavnoe-tier-clone` + skip в `maybeReplace`.
- Mobile/tablet Framer-fallback «PREMIUM PLAN/12000» → подмена на product Tier 2.
- Длинный About-параграф «Запускаем рекламу на Авито со сквозной аналитикой…» → подмена через DOM-handler по `section[data-framer-name="About"]`; hidden wrap-spans с Avito-фрагментами занулены.
- Кнопка процесса «СБОРКА КАМПАНИИ» → product CTA.
- Циклический баг `Fully mangage project → Управление всей воронкой → tier2_desc` (DST_VALUES guard блокировал вторую подмену) → промежуточная подстановка убрана, теперь mobile-bullet подменяется на нейтральный текст в один шаг.

---

## Следующая сессия

Следующая сессия должна сначала прочитать:

1. `PROJECT_MEMORY.md`
2. `RESEARCH_HANDOFF_2026-05-21.md`
3. `SESSION_HANDOFF_2026-05-21_PRODUCT_PAGES.md` (этот файл)
4. `CURRENT_PRODUCT_STATUS.md`
5. `PRODUCT_TEMPLATE_SPEC.md`

Только после этого продолжать работу.

Первая задача следующей сессии — пункт 1 из «Оставшихся задач»: добавить подпись «Нужен другой формат работы?» под тарифным блоком на все 4 product-страницы.
