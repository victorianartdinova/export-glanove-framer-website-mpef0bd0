# PROJECT RULES — full-site-export-may21

> Читать ПЕРВЫМ. Эти правила имеют приоритет над любыми другими CLAUDE.md, MEMORY.md, привычками агентов и прошлыми сессиями.

---

## ЧТО ЭТО ЗА ПРОЕКТ

**FRAMER / NOCODEEXPORT STATIC EXPORT.**

Это статический HTML/CSS/JS export сайта из Framer (через NoCodeExport).
**Это НЕ React-проект.** Здесь нет `src/`, нет компонентов, нет шаблонов, нет JSX, нет Vite, нет Next.js.

---

## SOURCE OF TRUTH (источник правды)

- **Локально:** `/root/framerexport/full-site-export-may21/`
- **GitHub:** `victorianartdinova/export-glanove-framer-website-mpef0bd0`

Любая правка должна делаться ТОЛЬКО внутри этой папки.
Любой `git remote -v` должен показывать именно этот repo.

---

## FORBIDDEN (запрещено абсолютно)

- ❌ `/root/glavnoe-real/` — это устаревший React-проект. Не открывать, не читать, не запускать в нём агентов, не использовать как «справочник».
- ❌ `src/products/*` — нет здесь таких файлов и не должно быть.
- ❌ `src/templates/ProductPage.tsx` — никогда не использовать как шаблон. Удалена сама идея React-шаблона.
- ❌ **React rebuild** — не переписывать сайт на React.
- ❌ **React product template** — не делать единый шаблон через JSX.
- ❌ Ветка `full-site-export-may20-stable` — не работать в ней, не мёрджить в неё.
- ❌ Менять `main` без явного approve пользователя.
- ❌ Запускать агентов или открывать файлы из других проектов «по аналогии».

---

## ALLOWED (разрешено)

- ✅ Править HTML export — файлы `product/*/index.html`, `index.html`, `blog/`, `cases/`, etc.
- ✅ Править JS chunks в `assets/framer/sites/.../*.mjs` — если Framer runtime перетирает текст/контент после гидратации.
- ✅ Править ссылки, текст, контент.
- ✅ Править assets (изображения, шрифты, иконки) в `assets/`.
- ✅ Работать только внутри `/root/framerexport/full-site-export-may21/`.

---

## CURRENT TASK

Product pages должны использовать **Avito Ads** как master content/template reference.

- `product/avito-ads/index.html` — ЭТАЛОН (структура, секции, верстка).
- `product/content-product/index.html` — должна быть копия Avito Ads с другим контентом.
- `product/product-statii/index.html` — то же.
- `product/product-telegram/index.html` — то же.
- `product/youtube-product/index.html` — то же.

**Что значит «копия»:** одинаковая структура секций, одинаковая разметка/классы Framer, одинаковый порядок блоков. Меняется только **контент** (тексты, цифры, картинки, ссылки) под каждый продукт.

**Чего делать НЕЛЬЗЯ:**
- ❌ Искать решение в React.
- ❌ Запускать агентов в `/root/glavnoe-real/`.
- ❌ Использовать `ProductPage.tsx` как референс.
- ❌ Задавать «mode questions» («какой режим выбрать?»). Режим один — править HTML export.

---

## ПРОТОКОЛ ПЕРЕД ЛЮБОЙ ЗАДАЧЕЙ

Обязательная проверка в самом начале сессии:

```bash
pwd                # → /root/framerexport/full-site-export-may21
git remote -v      # → victorianartdinova/export-glanove-framer-website-mpef0bd0
git branch --show-current
```

Если `pwd` НЕ `/root/framerexport/full-site-export-may21/` — **STOP. Перейти в правильную папку.**
Если `git remote` НЕ `victorianartdinova/export-glanove-framer-website-mpef0bd0` — **STOP. Не работать.**

---

## ПРОТОКОЛ ПОСЛЕ ЛЮБОЙ ЗАДАЧИ

1. Показать `git status --short` (только релевантные файлы, не cache).
2. Показать `git diff --stat` по делу.
3. Никогда не коммитить без явного approve пользователя.
4. Никогда не пушить без явного approve.
5. Никогда не мёрджить в `main` без явного approve.

---

## АГЕНТЫ

- Agents (Explore, code-reviewer, reality-checker, и т.д.) запускать ТОЛЬКО с явным указанием `cwd: /root/framerexport/full-site-export-may21/`.
- В промпте агенту первой строкой: **«Работать только в /root/framerexport/full-site-export-may21/. Папка glavnoe-real запрещена.»**

---

Обновлено: 2026-05-21
