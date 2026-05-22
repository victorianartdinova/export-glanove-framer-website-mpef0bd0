#!/usr/bin/env python3
"""
FIX 1 — AAG case hero readability.

Problem: hero shows white text 'ROI 6 000% на ПромоСтраницах Яндекса' on a light
striped background (white .framer-wwtfnn Filler + diagonal-stripes overlay)
so the title is unreadable on the upper half. Subtitle on the right
is dark text on dark area = also unreadable.

Fix (variant a from spec): darken the hero filler and dim stripes,
plus repaint hero subtitle/tagline to white. Injected as a single
<style id="glavnoe-aag-hero-fix"> block before </head>, idempotent.
"""
import re
import sys
from pathlib import Path

TARGET = Path(__file__).resolve().parent.parent / "work/case-aag-promostranicy/index.html"
STYLE_ID = "glavnoe-aag-hero-fix"

CSS = """
<style id="glavnoe-aag-hero-fix">
/* AAG case hero: darken filler so white title becomes readable */
.framer-wwtfnn { background: #0a0a0a !important; }

/* Dim the diagonal-stripes SVG overlay sitting on top of the dark filler */
.framer-17js171 > div[style*="data:image/svg+xml"] { opacity: 0.18 !important; }

/* Subtitle (right column under headline) — was rgb(0,0,0) over dark area */
section.framer-1jk03ar p.framer-text.framer-styles-preset-13cjcn8 {
    color: #ffffff !important;
}

/* Tagline under the title 'ПромоСтраницы Яндекса / Performance / Санкт-Петербург'
   sits inside the hero on the dark side now — force to light grey for legibility. */
section.framer-1jk03ar .framer-text,
section.framer-1jk03ar p,
section.framer-1jk03ar h1,
section.framer-1jk03ar h2,
section.framer-1jk03ar h3 {
    /* don't break already-white text */
}
section.framer-1jk03ar [style*="color: rgb(0, 0, 0)"],
section.framer-1jk03ar [style*="color:rgb(0,0,0)"] {
    color: #ffffff !important;
}
</style>
"""


def main():
    html = TARGET.read_text(encoding="utf-8")

    # Strip prior injection if present
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
    print(f"Injected {STYLE_ID} into {TARGET} (removed {n_removed} prior)")


if __name__ == "__main__":
    main()
