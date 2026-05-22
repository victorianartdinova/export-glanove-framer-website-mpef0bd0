# README_RESTORE.md — восстановление проекта

> Что делать если папка `/root/framerexport/full-site-export-may21/` пропала, повреждена, или Claude/агент потерял контекст и работает не там.

---

## ШАГ 1. Проверить наличие папки

```bash
ls -la /root/framerexport/full-site-export-may21/
```

Если папка есть — перейти в неё и **STOP**. Восстанавливать не нужно.

```bash
cd /root/framerexport/full-site-export-may21/
pwd
git remote -v
git branch --show-current
git status --short
```

---

## ШАГ 2. Если папки НЕТ — клонировать с GitHub

```bash
mkdir -p /root/framerexport
cd /root/framerexport
git clone git@github.com:victorianartdinova/export-glanove-framer-website-mpef0bd0.git full-site-export-may21
cd full-site-export-may21
git checkout runtime-restore-may21
```

После клонирования проверить:

```bash
pwd          # → /root/framerexport/full-site-export-may21
git remote -v
# должно показать:
# origin  git@github.com:victorianartdinova/export-glanove-framer-website-mpef0bd0.git (fetch)
# origin  git@github.com:victorianartdinova/export-glanove-framer-website-mpef0bd0.git (push)
git branch --show-current
# должно показать: runtime-restore-may21
```

---

## ШАГ 3. Если SSH-ключ не работает — HTTPS fallback

```bash
git clone https://github.com/victorianartdinova/export-glanove-framer-website-mpef0bd0.git full-site-export-may21
```

(потребуется GitHub token в `~/.git-credentials` или запрос пароля)

---

## ШАГ 4. Поднять preview

Preview уже работает на VPS на порту **3343** через node-сервер (`pid 629881` на момент 2026-05-21).
URL: `http://srv1207957.hstgr.cloud:3343/`

Если preview упал — поднять статический сервер из папки экспорта:

```bash
cd /root/framerexport/full-site-export-may21
python3 -m http.server 3343
# или
npx serve -p 3343 .
```

---

## ШАГ 5. Восстановить контекст задачи

1. Прочитать `PROJECT_RULES.md` — правила и forbidden paths.
2. Прочитать `CURRENT_TASK.md` — что сейчас делается.
3. Прочитать `CLAUDE.md` — инструкции для агента.
4. Прочитать `docs/SESSION_HANDOFF_2026-05-21_PRODUCT_CARDS.md` — handoff от предыдущей сессии.

---

## ЧЕГО НЕ ДЕЛАТЬ ПРИ ВОССТАНОВЛЕНИИ

- ❌ Не клонировать в `/root/glavnoe-real/` — это другой устаревший React-проект.
- ❌ Не использовать `/root/framerexport/full-site-export-may20/` — это предыдущий снепшот, не текущий.
- ❌ Не работать в ветке `main` без approve. Текущая рабочая ветка — `runtime-restore-may21`.
- ❌ Не пытаться «починить» React-проект `/root/glavnoe-real/` — он не имеет отношения к задаче.

---

## КОНТРОЛЬНАЯ ПРОВЕРКА (выполнить ОБЯЗАТЕЛЬНО перед началом работы)

```bash
[ "$(pwd)" = "/root/framerexport/full-site-export-may21" ] && \
git remote get-url origin | grep -q "victorianartdinova/export-glanove-framer-website-mpef0bd0" && \
echo "OK — можно работать" || \
echo "STOP — неверная папка или repo"
```

Если вывод не `OK — можно работать` — **STOP. Не делать ничего. Сообщить пользователю.**

---

Обновлено: 2026-05-21
