# CLAUDE.md — папка проекта theglavnoe.com

> Эти инструкции **переопределяют** глобальный `/root/CLAUDE.md` при работе в этой директории.
> Это активная папка сайта (прод). Обновлено: 23 мая 2026.

---

## 🔴 ПЕРВЫМ ДЕЛОМ ПРОЧИТАТЬ

1. **`/root/ops/dev/state-theglavnoe-com.md`** — единый источник правды по сайту, 2 воронкам (AI-школа + ГЛАВНОЕ), геймификации кейсов, статусу контента. **Читать всегда первым.**
2. `./README.md` — навигация по документам этой папки.

После прочтения проверить:
```bash
pwd                                                  # должна быть /root/framerexport/full-site-export-may21
curl -sI https://theglavnoe.com/ | head -1           # HTTP/2 200
```

---

## ЧТО ЭТО

Активная папка сайта theglavnoe.com. Static HTML/CSS/JS из:
- **Framer-экспорта** (главная, продуктовые, /about, /contact, /cases портфолио, меню) — зона Виктории, она правит в Framer Studio и переэкспортирует
- **Моих кастомных страниц с геймификацией** (`/work/*` кейсы, `/blog/*` статьи) — зона Клода

Раздаётся через **Caddy** на VPS (блок `theglavnoe.com {...}` в `/etc/caddy/Caddyfile`). Переключено 22.05.2026 с Next.js на статику.

## ЗОНЫ ОТВЕТСТВЕННОСТИ

| Я (Клод) | Вика (Framer Studio) |
|----------|----------------------|
| `/work/*` (3 кейса) | `index.html` (главная) |
| `/blog/*` (6 статей) | `product/*` (5 продуктовых) |
| `/404/` (если меняем) | `about/`, `contact/` |
| SEO статей и кейсов | меню/бургер/футер |
| og:image, Schema.org, sitemap | hero-фоны и иллюстрации |
| Контент полностью (пишу, верстаю, публикую) | Презентационная витрина |

**Вика НЕ таскает кейсы и статьи во Framer CMS — это моя зона полностью.**

## SOURCE OF TRUTH

| Что | Где |
|-----|-----|
| Локально | `/root/framerexport/full-site-export-may21/` |
| Прод (URL) | https://theglavnoe.com |
| State-файл проекта | `/root/ops/dev/state-theglavnoe-com.md` |
| Цифры кейсов | `/root/ops/CASE_SOURCES_OF_TRUTH.md` (SPB ppc.world, Regardis elama.ru, AAG `/root/Эфир 16.04..pdf`) |
| Эталон геймификации | `./work/case-spb-15mln/index.html` (1575 строк) |
| Концепция геймификации | `./CASE_EXPERIENCE_V2.md` + `/root/ops/VIKA_PROMPT_CASE_EXPERIENCE_V2.md` |
| Шаблоны | `./CASE_TEMPLATE_V1.md`, `./GUIDE_TEMPLATE_V1.md` |
| Архитектура контента | `./CONTENT_ARCHITECTURE_V1.md` |
| Programmatic SEO план | `/root/ops/seo-machine-plan.md` (на будущее, не сейчас) |

## ВОРОНКИ — 2 ШТУКИ (дефолтный контекст, не переспрашивать)

**AI-школа (личный бренд @vnartdinova):**
рилс → «ПОЕХАЛИ» → ManyChat → TG-канал → бот @lopata_voronka (БД `/root/lopata-bot/lopata.db`) → /ai-startup/ гайд → скилл-пак

**Агентство ГЛАВНОЕ:**
Google SEO / прямой → главная → Guide `/blog/*` → Case `/work/*` → Product `/product/*` → Hard CTA → форма `/api/lead` → @glavnoe_rebot (БД `/root/glavnoe-leads-bot/data/leads_re.db`, топик 927 группы `-1003915597546`)

## ✅ ALLOWED

- Править/создавать HTML в `work/<slug>/`, `blog/<slug>/`, `404/`
- Править ассеты (картинки, аватарки, og:image) в моих папках
- Править тексты, цифры (только из CASE_SOURCES_OF_TRUTH), ссылки, SEO-метаданные на моих страницах
- Перед коммитом: `curl -sI` 200 на изменённую страницу + проверка og:image через opengraph.xyz

## ❌ FORBIDDEN

- **Не править** `index.html` (главная), `product/*`, `about/`, `contact/`, меню/футер — это зона Framer Studio Виктории
- **Не предлагать** Вике таскать кейсы и статьи во Framer CMS вручную
- **Не делать тёмные лендинги** для кейсов и обучающих статей — paper-style #FBF7F1 обязательно (см. CASE_EXPERIENCE_V2)
- **Не выдумывать цифры** в кейсах — только CASE_SOURCES_OF_TRUTH.md
- **Не упоминать имя «Денис»** нигде на сайте (URL, текст, alt) — `feedback_no_denis_in_public`
- **Не путать БД ботов**: `lopata.db` = AI-школа, `leads_re.db` = агентство. Разные воронки, разные базы.
- **Не лезть в legacy** (`/tmp/trash-2026-05-23/glavnoe-site/`, `/tmp/trash-2026-05-23/glavnoe-real/`) — удалены 23.05, восстанавливать только если что-то реально пропустили
- **Не подключать домен к Framer hosting** — блокирует геймификацию и ломает /leads, /ai-startup, /api/*

## ОБЯЗАТЕЛЬНЫЕ ЭЛЕМЕНТЫ ГЕЙМИФИЦИРОВАННОЙ СТРАНИЦЫ (кейс / гайд)

См. полный список в `state-theglavnoe-com.md §3.3`. Главное:

- Paper-style фон #FBF7F1, **НЕ тёмный**
- Sticky progress bar сверху
- Sticky TOC слева (desktop) / collapsible (mobile)
- Reveal-анимации на scroll
- Funnel-step карточки (большая цифра + value + label)
- 4-6 нумерованных этапов с try-this box после каждого
- Инсайт/wow-момент после каждого этапа
- Карточка читателя в начале (время / этапы / для кого)
- Wow-блок в конце (единственное место где допустим #1A1814 тёмный)
- Hard CTA на связанный Product + Related cards
- Author block с `vika-avatar.jpg`
- SEO: title 50-60, description 150-160, Schema.org Article + Breadcrumb, og:image 1200×630

## ФОРМАТ ОТВЕТОВ (из глобального /root/CLAUDE.md, в силе)

- Коротко 3-5 предложений в чате
- Без полотен, заголовков, буллетов, кода — это всё в файлах
- Антибред-фильтр: факт или додумка, проверено ли, есть ли результат
- «Не знаю» допустимо
- Не отчитываться о процессе — только результат
- Никаких dev-терминов в чат (nodeId, MCP-методы, путь к компонентам) — только человеческие слова

## ПОСЛЕ КАЖДОЙ СЕССИИ — ОБНОВИТЬ

- `/root/ops/dev/state-theglavnoe-com.md` — статус кейсов/статей, открытые задачи, дата вверху
- Если изменилась архитектура (новые папки, новые маршруты Caddy) — `README.md` и этот `CLAUDE.md`

---

Обновлено: 23 мая 2026
