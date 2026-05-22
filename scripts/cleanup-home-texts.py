#!/usr/bin/env python3
"""FIX 4 — текстовые правки на главной (HIGH).

1. В блоке «Кейсы в СМИ» подзаголовок: убрать «:)» в конце.
   Источник: <h5>Кейсы <br>в СМИ:)</h5> → "Кейсы <br>в СМИ"
2. Слоган: «Главное — их донести®.» → убрать ® → «Главное — их донести.»
3. УМНОССЕРДЦЕ → УМНОЕ СЕРДЦЕ (defensive — в текущем index.html не найден,
   но добавлено на случай runtime/CMS подстановки).

Exact-match replacements, idempotent (повторный запуск ничего не меняет).
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'index.html'

REPLACEMENTS_HTML = [
    # 1. "Кейсы <br>в СМИ:)" -> убираем смайлик
    ('в СМИ:)</h5>', 'в СМИ</h5>'),
    # 2. "их донести®." -> убираем ®
    ('их донести®.', 'их донести.'),
    # 3. УМНОССЕРДЦЕ / УМНОЕСЕРДЦЕ → УМНОЕ СЕРДЦЕ (defensive)
    ('УМНОССЕРДЦЕ', 'УМНОЕ СЕРДЦЕ'),
    ('УМНОЕСЕРДЦЕ', 'УМНОЕ СЕРДЦЕ'),
    ('УмноССердце', 'Умное Сердце'),
]

# Framer mjs runtime содержит те же тексты — без правки runtime перезаписывает
# SSR HTML при гидрации.
REPLACEMENTS_MJS = [
    ('в СМИ:)', 'в СМИ'),
    ('их донести®', 'их донести'),
    ('УМНОССЕРДЦЕ', 'УМНОЕ СЕРДЦЕ'),
    ('УМНОЕСЕРДЦЕ', 'УМНОЕ СЕРДЦЕ'),
    ('УмноССердце', 'Умное Сердце'),
]

MJS_GLOB = 'assets/framer/sites/1OcdQgezFomPwA9UGakYyz/V6MP5xCojziNbtxidWz9fUuPNsqKAdC__dr2Zg5uIS8.DeEx7wm8.mjs'

SEARCH_INDEX_GLOBS = [
    'assets/framer/sites/1OcdQgezFomPwA9UGakYyz/searchIndex-MdzT6vHTlEuw.json',
    'assets/framer/sites/1OcdQgezFomPwA9UGakYyz/searchIndex-yuMvQ3nDRYls.json',
]


def replace_in_file(path: Path, pairs) -> bool:
    if not path.exists():
        print(f'[miss] {path}')
        return False
    txt = path.read_text(encoding='utf-8')
    orig = txt
    for old, new in pairs:
        if old in txt:
            cnt = txt.count(old)
            txt = txt.replace(old, new)
            print(f'[ok] {path.name}: {cnt}× {old!r} → {new!r}')
    if txt == orig:
        return False
    path.write_text(txt, encoding='utf-8')
    return True


def main() -> int:
    changed = False
    if replace_in_file(PAGE, REPLACEMENTS_HTML):
        changed = True
    if replace_in_file(ROOT / MJS_GLOB, REPLACEMENTS_MJS):
        changed = True
    for rel in SEARCH_INDEX_GLOBS:
        if replace_in_file(ROOT / rel, REPLACEMENTS_MJS):
            changed = True
    if not changed:
        print('[skip] no replacements applied (already clean)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
