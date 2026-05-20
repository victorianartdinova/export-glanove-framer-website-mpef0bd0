# Footer + links overrides — applied to full-site-export-may21 (2026-05-20)

> Approve checkpoint Вики: 2026-05-20 (вечер).
> Применено к чистому re-export `full-site-export-may21`. Доп. ручные правки 2026-05-20 описаны ниже.

---

## 1. Trash links cleanup — все 15 HTML

`find . -name '*.html' -print0 | xargs -0 sed -i`:

| Было | Стало |
|---|---|
| `https://contra.com/future_things_3ldqylhu/work?r=future_things_3ldqylhu` | `https://t.me/ksandrbloger` |
| `https://www.instagram.com/framer/` | `https://www.instagram.com/glavnoe_agency?igsh=MWNqOHVzMTIwaWlxZA%3D%3D&utm_source=qr` |
| `https://x.com/framer` | `https://t.me/ksandrbloger` (доп. правка 2026-05-20: X(Twitter) link отдан Саше, не агентству) |

Trash-паттерны: 0 совпадений по `grep -rE 'contra\.com|x\.com/framer|instagram\.com/framer' --include='*.html'`.

---

## 2. Footer labels = header labels (2026-05-20 update)

Vika approve: footer menu должен называться так же, как header menu. Применено к 15 HTML + JS chunk `script_main.B9JEDTsv.mjs`.

| Footer (было may20) | Footer (стало may21 + 2026-05-20 ручная) | Источник = Header |
|---|---|---|
| About → О компании | Главная | ✓ Главная |
| Features → Услуги | Услуги | ✓ Услуги |
| Benefits → Результаты | **Кейсы** | ✓ Кейсы |
| Pricing → Цены | **Результаты** | ✓ Результаты |
| Blogs → Статьи | Статьи | ✓ Статьи |
| Contact → Связаться | **Написать CEO** | ✓ Написать CEO |

**Surgical pattern (HTML)**: `>EN</h2>` → `>RU</h2>` (h2 = footer Link_01 component, в отличие от header p-тегов — не пересекается).

**JS chunk**: `iH0txF8LF:\`X\``.

---

## 3. «Отдел заботы 💙» → контакт Саши (2026-05-20 manual)

X(Twitter) link (внутренний Framer name) — кнопка с лейблом «Отдел заботы 💙».

- HTML: `<a name="X(Twitter) link" ... href="…">` → `href="https://t.me/ksandrbloger"`
- JS chunk: `name:\`X(Twitter) link\`` block → `JVbqtXsXU:\`https://t.me/ksandrbloger\``

---

## 4. «тг с пользой» → канал ГЛАВНОЕ (2026-05-20 manual)

Phone link (внутренний Framer name) — кнопка с лейблом «тг с пользой».

- HTML: `href="tel:12345678910"` → `href="https://t.me/glavnoe_channel"`, `target="_top"` → `target="_blank"`
- JS chunk: `name:\`Phone link\`` block → `JVbqtXsXU:\`https://t.me/glavnoe_channel\``

Канал ГЛАВНОЕ = `t.me/glavnoe_channel` (источник: `/root/glavnoe-site/`, 3020 вхождений — каноничный URL).

---

## 5. Mail link href cleanup (2026-05-20)

Label был корректный (`hello@glavnoe.com`), но href вёл на `mailto:dummy@mail.com`. Приведено в соответствие:

- HTML + JS chunk: `mailto:dummy@mail.com` → `mailto:hello@glavnoe.com`

---

## 6. Pinned CEO Card в Hero

Привязана к `https://t.me/ksandrbloger` (часть trash cleanup п.1). Pinned animation сохранена структурно — sed не трогал верстку, только URL.

---

## Verify (preview localhost:3343)

```
header labels: 2× каждое (header + footer = одинаковые)
footer hrefs:
  Phone link        → https://t.me/glavnoe_channel
  X(Twitter) link   → https://t.me/ksandrbloger
  Mail link         → mailto:hello@glavnoe.com
  Instagram link    → https://www.instagram.com/glavnoe_agency?…
EN labels:          0 совпадений (About/Features/Benefits/Pricing/Blogs/Contact)
trash URLs:         0 совпадений (contra.com / x.com/framer / instagram.com/framer / dummy@mail / tel:1234)
```

---

## Replay (для следующего re-export)

```bash
# Run from full-site-export-{date}/
python3 - << 'PYEOF'
import re, glob, os
htmls = ['index.html', '404/index.html'] + glob.glob('blog/*/index.html') + \
        glob.glob('product/*/index.html') + glob.glob('cases/*/index.html') + \
        glob.glob('work/*/index.html')
LABELS = [
    ('>О компании</h2>', '>Главная</h2>'),
    ('>Результаты</h2>', '>Кейсы</h2>'),
    ('>Цены</h2>',       '>Результаты</h2>'),
    ('>Связаться</h2>',  '>Написать CEO</h2>'),
    # If starting from clean EN export, prepend the may20 EN→RU step.
]
for p in htmls:
    s = open(p).read(); orig = s
    for o, n in LABELS: s = s.replace(o, n)
    s = re.sub(r'(<a name="Phone link"[^>]*?href=")tel:12345678910(")',
               r'\1https://t.me/glavnoe_channel\2', s, flags=re.DOTALL)
    s = re.sub(r'(<a name="Phone link"[^>]*?)target="_top"',
               r'\1target="_blank"', s, flags=re.DOTALL)
    s = re.sub(r'(<a name="X\(Twitter\) link"[^>]*?href=")[^"]+(")',
               r'\1https://t.me/ksandrbloger\2', s, flags=re.DOTALL)
    s = re.sub(r'(<a name="Mail link"[^>]*?href=")mailto:dummy@mail\.com(")',
               r'\1mailto:hello@glavnoe.com\2', s, flags=re.DOTALL)
    if s != orig: open(p, 'w').write(s)

js = 'assets/framer/sites/1OcdQgezFomPwA9UGakYyz/script_main.B9JEDTsv.mjs'
s = open(js).read()
for o, n in [
    ('iH0txF8LF:`О компании`',   'iH0txF8LF:`Главная`'),
    ('iH0txF8LF:`Результаты`',   'iH0txF8LF:`Кейсы`'),
    ('iH0txF8LF:`Цены`',         'iH0txF8LF:`Результаты`'),
    ('iH0txF8LF:`Связаться`',    'iH0txF8LF:`Написать CEO`'),
]: s = s.replace(o, n)
s = re.sub(r'(name:`Phone link`[^}]{0,500}?JVbqtXsXU:`)tel:12345678910(`)',
           r'\1https://t.me/glavnoe_channel\2', s, flags=re.DOTALL)
s = re.sub(r'(name:`X\(Twitter\) link`[^}]{0,500}?JVbqtXsXU:`)[^`]+(`)',
           r'\1https://t.me/ksandrbloger\2', s, flags=re.DOTALL)
s = re.sub(r'(name:`Mail link`[^}]{0,500}?JVbqtXsXU:`)mailto:dummy@mail\.com(`)',
           r'\1mailto:hello@glavnoe.com\2', s, flags=re.DOTALL)
s = re.sub(r'(name:`Instagram link`[^}]{0,500}?JVbqtXsXU:`)https://www\.instagram\.com/framer/(`)',
           r'\1https://www.instagram.com/glavnoe_agency?igsh=MWNqOHVzMTIwaWlxZA%3D%3D&utm_source=qr\2',
           s, flags=re.DOTALL)
open(js, 'w').write(s)
PYEOF
```
