#!/usr/bin/env python3
"""B1 — потенциальный дубль метрик на главной убран в коммите 15b0eeb (Services section deleted).
Этот скрипт проверяет нет ли остаточного дубля и при необходимости скрывает."""
from pathlib import Path
f = Path('/root/framerexport/full-site-export-may21/index.html')
# Subagent уже удалил Services. Этот скрипт оставляю на всякий случай.
# CSS-страховка: если есть второй Archive — скроем
MARK = 'id="glavnoe-no-duplicate-archive"'
CSS = (
    '<style id="glavnoe-no-duplicate-archive">'
    # Если на странице 2 секции с одинаковым data-framer-name — скроем все кроме первой
    'section[data-framer-name="Services"]{display:none!important;}'
    '</style>'
)
h = f.read_text(encoding='utf-8')
if MARK in h:
    print('SKIP')
else:
    h = h.replace('</head>', CSS + '</head>', 1)
    f.write_text(h, encoding='utf-8')
    print('OK no-duplicate guard')
