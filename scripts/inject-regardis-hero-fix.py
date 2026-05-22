#!/usr/bin/env python3
"""
FIX 2 — Regardis hero readability.

Problem: hero shows the H2 title 'Как мы получили 50 квал. лидов в месяц
на премиум-недвижимость.' overlapping a background JPEG that has its OWN
baked-in copy ('55 квал лидов в месяц на премиум-недвижимость в москве').
Result — duplicate text bleeding through, looks like a render bug.

Fix: dim the BG Image container so its baked-in headline fades into a
moody silhouette while the framer H2 stays clean on top.

Injected as <style id="glavnoe-regardis-hero-fix"> before </head>,
idempotent.
"""
import re
import sys
from pathlib import Path

TARGET = Path(__file__).resolve().parent.parent / "work/regardis-telegram-ads-premium/index.html"
STYLE_ID = "glavnoe-regardis-hero-fix"

CSS = """
<style id="glavnoe-regardis-hero-fix">
/* Regardis hero: kill duplicate baked-in text on BG image */
section.framer-1jk03ar .framer-698lh > div > img,
section.framer-1jk03ar .framer-698lh img {
    opacity: 0.18 !important;
    filter: blur(3px) saturate(0.8) !important;
}
section.framer-1jk03ar .framer-698lh {
    background: #0a0a0a !important;
}
@media (max-width: 810px) {
    section.framer-1jk03ar .framer-698lh > div > img,
    section.framer-1jk03ar .framer-698lh img {
        opacity: 0.14 !important;
        filter: blur(5px) saturate(0.7) !important;
    }
}
section.framer-1jk03ar p.framer-text.framer-styles-preset-13cjcn8 {
    color: #ffffff !important;
}
</style>
"""


def main():
    html = TARGET.read_text(encoding="utf-8")
    pattern = re.compile(
        r'<style id="' + re.escape(STYLE_ID) + r'">.*?</style>',
        re.DOTALL,
    )
    html, n_removed = pattern.subn("", html)
    if "</head>" not in html:
        print("ERROR: </head> not found", file=sys.stderr)
        sys.exit(1)
    html = html.replace("</head>", CSS.strip() + "</head>", 1)
    TARGET.write_text(html, encoding="utf-8")
    print(f"Injected {STYLE_ID} (removed {n_removed} prior)")


if __name__ == "__main__":
    main()
