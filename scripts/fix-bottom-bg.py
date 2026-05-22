#!/usr/bin/env python3
"""
Fix A2 (img-101646) — Desktop: bottom of product page goes white.

Symptom (desktop ≥1200px): at the bottom of every product page, just above
the footer, there is a full-bleed white section (1440 × 330px) painting
`background: rgb(255, 255, 255)` over the page's dark body. Two case-thumb
cards barely visible at the very bottom on dark — the white block above is
the CTA / footer-pre section.

Probed: `section[class*="framer-zpXos"][class*="framer-18ghmdc"]`
(data-framer-name="Desktop") at top ≈5607, h=330, w=1440 — bg white.

Fix: override that section's background to #000 and flip text color to #fff
so any dark copy inside stays readable. Scoped to desktop / tablet on the 5
product pages.

Idempotent marker 'fix:bottom-bg v1'.
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
MARKER = '/* fix:bottom-bg v1 */'
CSS_BLOCK = f'''<style id="glavnoe-bottom-bg-fix" data-fix="bottom-bg">{MARKER}
/* The Desktop CTA / footer-pre section ships `background:#fff` from Framer.
   Override to #000 so the bottom of the page stays on the dark site palette
   (body bg is #000). Apply on desktop AND tablet — the section variants
   share the `framer-zpXos` family class on both breakpoints. */
section[class*="framer-zpXos"],
section[class*="framer-18ghmdc"],
section[data-framer-name="Desktop"][class*="framer-zpXos"] {{
  background: #000 !important;
  color: #fff !important;
}}

/* Children that hard-code `color:#000` against the (formerly) white bg
   need to be flipped so they stay legible on the dark surface. */
section[class*="framer-zpXos"] p,
section[class*="framer-zpXos"] h1,
section[class*="framer-zpXos"] h2,
section[class*="framer-zpXos"] h3,
section[class*="framer-zpXos"] span:not([style*="background"]),
section[class*="framer-zpXos"] a:not([style*="background"]) {{
  color: #fff !important;
}}

/* The earlier white SECTION "Desktop Card 1" (big-number block) also paints
   the page white between About and Team. Keep dark unless it's the inner
   white card itself (which retains its own internal background style). */
section[data-framer-name="Desktop Card 1"][class*="framer-1b12ems"] {{
  background: transparent !important;
}}

/* Belt-and-braces: any descendant <div> directly applying the same white
   that bleeds full-width inherits #000 unless it's the inner card chrome. */
section[class*="framer-zpXos"] > div:first-child {{
  background: transparent !important;
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
