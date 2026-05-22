# CURRENT_TASK.md

> Что делаем прямо сейчас. Обновлять в конце каждой сессии.

---

## ЗАДАЧА

**Все 4 продуктовые страницы должны стать копиями `product/avito-ads/index.html` с подменённым контентом.**

| Страница | Файл | Статус |
|----------|------|--------|
| Avito Ads (эталон) | `product/avito-ads/index.html` | ✅ master |
| Content Product | `product/content-product/index.html` | 🟡 правится (uncommitted) |
| Статьи | `product/product-statii/index.html` | 🟡 правится (uncommitted) |
| Telegram | `product/product-telegram/index.html` | 🟡 правится (uncommitted) |
| YouTube | `product/youtube-product/index.html` | 🟡 правится (uncommitted) |

---

## ТРЕБОВАНИЯ К РЕЗУЛЬТАТУ

Каждая из 4 страниц должна:
1. Иметь **ту же структуру секций** что и `avito-ads` (hero → описание → блоки преимуществ → pricing → CTA → footer — или какой там порядок в эталоне).
2. Использовать **те же Framer-классы и data-атрибуты**, что и `avito-ads` — чтобы Framer runtime отрисовал её 1:1 по верстке.
3. Иметь **только новый контент** (тексты, заголовки, цифры, картинки, ссылки) под свой продукт.
4. Корректно рендериться без перетёртой Framer-гидратацией разметки — если runtime перетирает, патчить `.mjs` chunk через `-v2.mjs` версии.
5. Работать на 3 viewport: 390 mobile / 810 tablet / 1440 desktop.

---

## ИСТОЧНИК

- Эталон контента/структуры: `product/avito-ads/index.html`
- Эталон Framer runtime: `assets/framer/sites/1OcdQgezFomPwA9UGakYyz/script_main.B9JEDTsv.mjs`
- Post-hydration патчи: `assets/framer/sites/1OcdQgezFomPwA9UGakYyz/*-v2.mjs`

---

## ЧТО НЕЛЬЗЯ

- ❌ Искать решение в React (`/root/glavnoe-real/src/products/*`, `ProductPage.tsx`).
- ❌ Запускать агентов в `/root/glavnoe-real/`.
- ❌ Использовать React product template как референс.
- ❌ Задавать «mode questions» (какой режим? какой подход?). Режим один — править HTML export напрямую.
- ❌ Коммитить/пушить/мёрджить без approve пользователя.

---

## ТЕКУЩЕЕ СОСТОЯНИЕ (по `git status` на 2026-05-21)

Ветка: `runtime-restore-may21`

**Modified (M):**
- `assets/framer/sites/.../V6MP5xCojziNbtxidWz9fUuPNsqKAdC__dr2Zg5uIS8.DeEx7wm8.mjs`
- `assets/framer/sites/.../script_main.B9JEDTsv.mjs`
- `docs/SESSION_HANDOFF_2026-05-21_PRODUCT_CARDS.md`
- `product/content-product/index.html`
- `product/product-statii/index.html`
- `product/product-telegram/index.html`
- `product/youtube-product/index.html`

**Deleted (D):** оригинальные `.mjs` chunks (заменены `-v2.mjs` версиями ниже).

**Untracked (??):** `-v2.mjs` патч-версии chunks — post-hydration патчи.

**Последний коммит:** `11130a2 fix(home): product cards full-width on desktop (scenario B)`

---

## СЛЕДУЮЩИЙ ШАГ

1. Прочитать `docs/SESSION_HANDOFF_2026-05-21_PRODUCT_CARDS.md` — что было сделано в прошлой сессии, что осталось.
2. Сверить уже изменённые `product/*/index.html` с эталоном `product/avito-ads/index.html` по структуре.
3. Сделать снимки 4 продуктовых страниц на 3 viewport, сравнить попиксельно с эталоном.
4. Найти все расхождения структуры. Подменить контент так, чтобы структура оставалась 1:1.
5. Запустить reality-checker и code-reviewer (с явным `cwd` этой папки) до того как сказать «готово».
6. Показать пользователю результат (URL + crops). Approve → коммит. Без approve — не коммитить.

---

## PREVIEW

`http://srv1207957.hstgr.cloud:3343/`

Страницы для проверки:
- `http://srv1207957.hstgr.cloud:3343/product/avito-ads/` (эталон)
- `http://srv1207957.hstgr.cloud:3343/product/content-product/`
- `http://srv1207957.hstgr.cloud:3343/product/product-statii/`
- `http://srv1207957.hstgr.cloud:3343/product/product-telegram/`
- `http://srv1207957.hstgr.cloud:3343/product/youtube-product/`

---

Обновлено: 2026-05-21
