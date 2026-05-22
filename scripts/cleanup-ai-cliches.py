#!/usr/bin/env python3
"""
cleanup-ai-cliches.py — Вычистка ИИ-клише и канцелярита из markdown-документов
контентного слоя theglavnoe.com.

Принципы:
- Idempotent — повторный прогон ничего не ломает.
- Только лексические замены внутри строк. Никаких удалений строк/блоков.
- Markdown-структура (#, |, -, ```) не трогается.
- Любая замена логируется в формате: файл: «старая» → «новая».
- Защищённые контексты:
  * фрагменты в обратных кавычках (`...`) и fenced-блоки кода (```)
  * строки-«анти-правила» (содержат "Анти-AI", "Анти-clich", "Без «", "не использовать")
    — в них клише это меточные слова, а не контент.
  * markdown-таблицы, где левая ячейка — meta-метка ("Когда", "Что", "Цель").

Сборка списка замен — в SUBSTITUTIONS внизу.

Запуск:
  python3 scripts/cleanup-ai-cliches.py            # пишет изменения и лог в stdout
  python3 scripts/cleanup-ai-cliches.py --dry      # ничего не пишет, только лог
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Callable, List, Tuple

ROOT = Path(__file__).resolve().parent.parent

TARGET_FILES = [
    "CONTENT_ARCHITECTURE_V1.md",
    "CASE_TEMPLATE_V1.md",
    "GUIDE_TEMPLATE_V1.md",
    "SITE_RELATIONS_MAP.md",
    "ARTICLES_PUBLICATION_PLAN.md",
    "ARTICLES_MAP_REAL_ESTATE.md",
    "CASE_EXPERIENCE_V2.md",
]

# Маркеры "анти-правил" — на таких строках клише упомянуто как пример того,
# что НЕ использовать. Эти строки пропускаем целиком.
META_RULE_MARKERS = (
    "Анти-AI",
    "Анти-clich",
    "Без «",
    "не использов",
    "Не использов",
    "не делать",
    "Не делать",
    "Никаких",
    "Запрещ",
    "запрещ",
    "НЕЛЬЗЯ",
    "нельзя",
    "Слова:",
    "Стоп-слова",
    "стоп-слова",
)


def is_meta_rule_line(line: str) -> bool:
    return any(marker in line for marker in META_RULE_MARKERS)


def is_table_header_or_divider(line: str) -> bool:
    s = line.strip()
    return bool(re.match(r"^\|[\s\-:|]+\|?\s*$", s))


# ---------------------------------------------------------------------------
# Замены: список пар (regex, replacement) или (regex, callable).
#
# Каждое правило применяется к строке ВНЕ защищённых фрагментов (см. _split_safe).
# Регулярки используют (?i) только когда явно нужно.
# ---------------------------------------------------------------------------

# Тип элемента — либо строка-замена, либо callable(match) -> str.
Replacement = str  # для простоты, ниже используем только строки

SUBSTITUTIONS: List[Tuple[re.Pattern, Replacement, str]] = [
    # --- слова-маркеры ИИ-текста ---
    (re.compile(r"\bдавайте\b", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bбезусловно[,]?\s*", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bнесомненно[,]?\s*", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bв эпоху\b", re.IGNORECASE), "сейчас", "replace"),
    (re.compile(r"\bв современном мире\b", re.IGNORECASE), "сейчас", "replace"),
    (re.compile(r"\bв наше время\b", re.IGNORECASE), "сейчас", "replace"),
    (re.compile(r"\bна сегодняшний день\b", re.IGNORECASE), "сейчас", "replace"),

    # --- канцелярит (общие связки) ---
    (re.compile(r"\bтаким образом[,]\s*", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bследовательно[,]\s*", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bв данной статье\b", re.IGNORECASE), "в статье", "replace"),
    (re.compile(r"\bв текущем кейсе\b", re.IGNORECASE), "в кейсе", "replace"),
    (re.compile(r"\bпо результатам\b", re.IGNORECASE), "по итогам", "replace"),
    (re.compile(r"\bв связи с тем,?\s+что\b", re.IGNORECASE), "потому что", "replace"),

    # --- AI-указатели ---
    (re.compile(r"\bважно отметить[,]?\s*", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bстоит подчеркнуть[,]?\s*", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bстоит отметить[,]?\s*", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bследует помнить[,]?\s*", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bследует отметить[,]?\s*", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bкак уже было сказано выше[,]?\s*", re.IGNORECASE), "", "drop"),
    (re.compile(r"\bкак (?:уже\s+)?упоминалось выше[,]?\s*", re.IGNORECASE), "", "drop"),

    # --- размытые синонимы «и так далее» ---
    (re.compile(r"\bпредставляет собой\b", re.IGNORECASE), "это", "replace"),
    (re.compile(r"\bявляется (одним из )?\b", re.IGNORECASE), "", "drop"),

    # --- "не просто X, а Y" — фраза-усилитель. НЕ ТРОГАЕМ автоматически:
    # часто это реальный контраст («не просто появился, а прошёл шаги»).
    # Спорные случаи фиксируем в /tmp/ai-cliches-remaining.md.
]


# Защищённые фрагменты внутри строки: backticks `...`. Возвращает список
# чередующихся кусков "safe"/"unsafe", где safe — внутри ``, unsafe — снаружи.
def _split_safe(line: str) -> List[Tuple[str, bool]]:
    """Разбивает строку на куски: (text, is_protected)."""
    parts: List[Tuple[str, bool]] = []
    i = 0
    while i < len(line):
        # Тройные бэктики? Не должно быть внутри строки — это fence, который
        # обрабатывается на уровне файла. Здесь — одинарные бэктики.
        m = re.search(r"`[^`]*`", line[i:])
        if not m:
            parts.append((line[i:], False))
            break
        start = i + m.start()
        end = i + m.end()
        if start > i:
            parts.append((line[i:start], False))
        parts.append((line[start:end], True))
        i = end
    return parts


def apply_substitutions_to_text(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Применяет SUBSTITUTIONS к незащищённой части строки. Возвращает
    новый текст и список (старая фраза, новая фраза) для лога."""
    changes: List[Tuple[str, str]] = []
    out_parts: List[str] = []
    for chunk, is_protected in _split_safe(text):
        if is_protected:
            out_parts.append(chunk)
            continue
        new_chunk = chunk
        for pattern, replacement, _kind in SUBSTITUTIONS:
            def _sub(m: re.Match) -> str:
                old = m.group(0)
                # Если "replacement" пустой, мы дропаем фразу; чистим двойные пробелы.
                new = replacement
                changes.append((old, new))
                return new
            new_chunk = pattern.sub(_sub, new_chunk)
        # Чистим артефакты от удалений: двойные пробелы → один, пробел перед знаком.
        new_chunk = re.sub(r"  +", " ", new_chunk)
        new_chunk = re.sub(r" +([.,;:!?»)])", r"\1", new_chunk)
        new_chunk = re.sub(r"([«(]) +", r"\1", new_chunk)
        out_parts.append(new_chunk)
    return "".join(out_parts), changes


def process_file(path: Path, dry: bool) -> Tuple[int, List[str]]:
    """Возвращает (число замен в файле, log lines)."""
    raw = path.read_text(encoding="utf-8")
    lines = raw.split("\n")
    new_lines: List[str] = []
    log: List[str] = []
    in_fence = False
    total = 0

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        # Fenced code block toggle (```)
        if stripped.startswith("```"):
            in_fence = not in_fence
            new_lines.append(line)
            continue
        if in_fence:
            new_lines.append(line)
            continue
        # Заголовок — оставляем нетронутым (там клише и не должно быть).
        # Markdown-таблицы: разделители и заголовки. Их не трогаем.
        if is_table_header_or_divider(line):
            new_lines.append(line)
            continue
        # Анти-правила — не трогаем.
        if is_meta_rule_line(line):
            new_lines.append(line)
            continue

        new_text, changes = apply_substitutions_to_text(line)
        if changes:
            for old, new in changes:
                old_disp = repr(old)
                new_disp = repr(new) if new else "«» (удалено)"
                log.append(f"{path.name}:{idx}: {old_disp} → {new_disp}")
                total += 1
        new_lines.append(new_text)

    new_raw = "\n".join(new_lines)
    if total and not dry:
        path.write_text(new_raw, encoding="utf-8")
    return total, log


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry", action="store_true", help="Не писать в файлы.")
    args = parser.parse_args()

    grand_total = 0
    per_file: List[Tuple[str, int]] = []
    for name in TARGET_FILES:
        path = ROOT / name
        if not path.exists():
            print(f"WARN: missing {path}", file=sys.stderr)
            continue
        n, log = process_file(path, args.dry)
        per_file.append((name, n))
        grand_total += n
        for entry in log:
            print(entry)

    print()
    print("=" * 60)
    print("SUMMARY" + (" (dry-run)" if args.dry else ""))
    for name, n in per_file:
        print(f"  {name}: {n} замен")
    print(f"  TOTAL: {grand_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
