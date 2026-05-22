#!/usr/bin/env python3
"""
Fix A3 (img-101713) — Team grid collapsed into vertical strips on product pages.

Symptom: section "(02) Наша команда" renders 20 team cards as a single non-
wrapping flex row → each card ~61px wide × 521px tall (vertical strips).

Root cause: The team carousel is a Framer `slideshow` whose inner <ul> is
`display:flex; flex-direction:row; flex-wrap:nowrap; gap:10px` inside a
section `framer-rTJXX framer-2itchk` (data-framer-name="L" on desktop).
The carousel JS that paginates the strip never runs / never engages on these
product pages, so all 20 list items try to fit into the section width at once.

Fix: scope-inject CSS that turns that UL into a wrappable CSS grid with
`auto-fit, minmax(180px, 1fr)` and forces the LI cards to a sane min-width.
We also clamp the wrapping section to its natural width so cards can wrap
onto multiple rows. CSS is scoped to product pages via a wrapper selector
applied on each product/<slug>/index.html.

Idempotent: marker `fix:team-grid v1` inside the injected <style>.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    'product/avito-ads/index.html',
    'product/content-product/index.html',
    'product/product-statii/index.html',
    'product/product-telegram/index.html',
    'product/youtube-product/index.html',
]
MARKER = '/* fix:team-grid v1 */'
CSS_BLOCK = f'''<style id="glavnoe-team-fix" data-fix="team-grid">{MARKER}
/* Team grid (section "L" with data-framer-name) on product pages.
   Targets the slideshow inner UL that ships with 20 LI children and a
   non-wrapping flex row → strips. We override that UL to grid with
   auto-fit so cards keep a sane minimum width and wrap to new rows. */

/* Desktop / Tablet — turn the inner UL into a wrapping grid. */
section[class*="framer-rTJXX"] ul,
section[class*="framer-2itchk"] ul,
section[class*="framer-slideshow"] ul {{
  display: grid !important;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)) !important;
  gap: 16px !important;
  flex-wrap: wrap !important;
  width: 100% !important;
  max-width: 100% !important;
  overflow: visible !important;
}}

/* Each team card (LI > container > Primary) — force a sane width
   range so the card never collapses into a vertical strip. */
section[class*="framer-rTJXX"] ul > li,
section[class*="framer-2itchk"] ul > li,
section[class*="framer-slideshow"] ul > li {{
  flex: 0 1 auto !important;
  min-width: 180px !important;
  max-width: 360px !important;
  width: 100% !important;
  height: auto !important;
  list-style: none !important;
  display: block !important;
}}

/* The Primary card wrapper (framer-wjj4gq) and its inner containers. */
section[class*="framer-rTJXX"] [class*="framer-wjj4gq"],
section[class*="framer-2itchk"] [class*="framer-wjj4gq"] {{
  min-width: 180px !important;
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
}}

/* The card-content row (`framer-1i21605` = Bottom) must not be wider than
   parent — we saw it expanding to 350px while parent is 61px. */
section[class*="framer-rTJXX"] [class*="framer-1i21605"],
section[class*="framer-2itchk"] [class*="framer-1i21605"] {{
  width: 100% !important;
  max-width: 100% !important;
}}

/* Section overflow: open it so wrapped rows are visible (was hidden). */
section[class*="framer-rTJXX"][class*="framer-2itchk"] {{
  height: auto !important;
  min-height: 0 !important;
  overflow: visible !important;
}}

/* Outer wrapper (`framer-13yoypl-container`) sometimes ships fixed height. */
[class*="framer-13yoypl-container"] {{
  height: auto !important;
}}

/* Mobile — single column, full width. */
@media (max-width: 810px) {{
  section[class*="framer-rTJXX"] ul,
  section[class*="framer-2itchk"] ul,
  section[class*="framer-slideshow"] ul {{
    grid-template-columns: 1fr 1fr !important;
    gap: 12px !important;
  }}
  section[class*="framer-rTJXX"] ul > li,
  section[class*="framer-2itchk"] ul > li,
  section[class*="framer-slideshow"] ul > li {{
    min-width: 0 !important;
    max-width: none !important;
  }}
}}
</style>'''


def main():
    applied = 0
    for rel in PAGES:
        target = ROOT / rel
        if not target.exists():
            print(f'SKIP missing: {rel}', file=sys.stderr)
            continue
        html = target.read_text(encoding='utf-8')
        if MARKER in html:
            print(f'OK already-applied: {rel}')
            continue
        idx = html.find('</head>')
        if idx == -1:
            print(f'ERR no </head>: {rel}', file=sys.stderr)
            continue
        new_html = html[:idx] + CSS_BLOCK + '\n' + html[idx:]
        target.write_text(new_html, encoding='utf-8')
        applied += 1
        print(f'WROTE {rel} (+{len(CSS_BLOCK)} bytes)')
    print(f'\nDone. {applied}/{len(PAGES)} pages patched.')


if __name__ == '__main__':
    main()
