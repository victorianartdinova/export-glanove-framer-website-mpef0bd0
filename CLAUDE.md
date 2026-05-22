# CLAUDE.md — full-site-export-may21

> Эти инструкции **переопределяют** глобальный `/root/CLAUDE.md` и любые CLAUDE.md из родительских папок при работе в этой директории.

---

## 🔴 ПЕРВЫМ ДЕЛОМ ПРОЧИТАТЬ

1. `PROJECT_RULES.md` — что можно/нельзя, source of truth, forbidden paths.
2. `CURRENT_TASK.md` — текущая задача, текущее состояние.
3. `README_RESTORE.md` — как восстановить проект если папка пропала.

После прочтения **обязательно** запустить:

```bash
pwd
git remote -v
git branch --show-current
git status --short
```

Если что-то из этого не совпадает с ожидаемым (см. `PROJECT_RULES.md`) — **STOP. Сообщить пользователю.**

---

## ЧТО ЭТО

Static HTML/CSS/JS export Framer-сайта `glanove.framer.website` через NoCodeExport.
**НЕ React. НЕ Next.js. НЕ Vite.** Никаких `src/`, `components/`, `templates/`.

Структура:
- `index.html` — главная.
- `product/<slug>/index.html` — продуктовые страницы (avito-ads, content-product, product-statii, product-telegram, youtube-product).
- `blog/`, `cases/` — контент-разделы.
- `assets/framer/sites/1OcdQgezFomPwA9UGakYyz/` — JS chunks Framer runtime + style chunks.
- `assets/images/` — графика.
- `docs/` — внутренние handoff-документы по сессиям.

---

## SOURCE OF TRUTH

| Что | Где |
|-----|-----|
| Локально | `/root/framerexport/full-site-export-may21/` |
| GitHub | `git@github.com:victorianartdinova/export-glanove-framer-website-mpef0bd0.git` |
| Ветка для текущей работы | `runtime-restore-may21` |
| Preview | `http://srv1207957.hstgr.cloud:3343/` |

---

## ❌ FORBIDDEN

Никогда:
- Не открывать, не читать, не править `/root/glavnoe-real/`.
- Не запускать агентов в `/root/glavnoe-real/`.
- Не ссылаться на `src/products/*`, `src/templates/ProductPage.tsx` — это другой устаревший проект.
- Не делать React rebuild сайта.
- Не работать в ветке `full-site-export-may20-stable`.
- Не мёрджить в `main` без approve.
- Не коммитить/пушить без approve.

## ✅ ALLOWED

- Править HTML в `product/`, `index.html`, `blog/`, `cases/`.
- Править Framer JS chunks в `assets/framer/sites/.../*.mjs` (есть `-v2.mjs` варианты — это post-hydration patches).
- Править assets (картинки, иконки).
- Править тексты, ссылки, контент.

---

## ТЕКУЩАЯ ЗАДАЧА (см. CURRENT_TASK.md для деталей)

Все 4 продуктовые страницы должны быть копиями `product/avito-ads/index.html` с подменённым контентом:
- `product/content-product/index.html`
- `product/product-statii/index.html`
- `product/product-telegram/index.html`
- `product/youtube-product/index.html`

Структура секций, классы Framer, порядок блоков — **идентичны Avito Ads**. Меняется только контент.

---

## ФОРМАТ ОТВЕТОВ (наследую из /root/CLAUDE.md, оставляю в силе)

- Коротко, 3-5 предложений в чате.
- Без заголовков/буллетов/кода в чате (исключение — структурированные статусы по запросу).
- Антибред-фильтр перед каждым ответом: факт или додумка, есть ли результат, проверено ли.
- «Не знаю» — допустимо.
- Не отчитываться о процессе — только результат.

---

Обновлено: 2026-05-21
