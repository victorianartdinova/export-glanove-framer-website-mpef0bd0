#!/usr/bin/env python3
"""
Fix A4 (img-101847) — Mobile: white gaps + collision at PricingAccordion → Team.

Symptom (mobile, ≤810px): the pricing accordion section (`(03) Стоимость`)
ships with `background:#fff` (it's a Framer block named "Process Section",
class `framer-b1f3u1`). The next section "(02) Наша команда" sits on
`body { background:#000 }`. Between the two there is no padding-block, the
white section bleeds horizontal `border-radius` / `border-bottom` lines at
the viewport edges → white slivers, and the dark team section overlaps.

Fix: on viewports ≤1100px (tablet+mobile of product pages):
  • Force `main`, `<body>`, `<section>` backgrounds to #000 so the product
    page is one continuous dark surface (the pricing block is fine being
    light internally — its tariff cards are white inside the dark frame).
  • Strip any `border` / `border-radius` from <section> elements that
    would otherwise paint a white halo at section boundaries.
  • Add `padding-block: 40px` to product page sections so consecutive
    blocks don't collide visually.
  • Specifically neutralise the white SECTION `framer-b1f3u1`
    (Pricing/Process) to inherit `#000` so its body stops painting white
    slivers when the inner card stays light.

Scoped: each product/<slug>/index.html. Idempotent marker 'fix:section-bg v1'.
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
MARKER = '/* fix:section-bg v1 */'
CSS_BLOCK = f'''<style id="glavnoe-section-bg-fix" data-fix="section-bg">{MARKER}
/* Surgical fix for the PricingAccordion → TeamSection seam on mobile/tablet.
   We don't touch the rest of the page — only:
     (a) strip any borders on the WHITE process section (`framer-b1f3u1`)
         so it can't paint 1px white lines at its bottom/right edges
         when the next section starts in #000;
     (b) add padding-block to the dark sections that sit on body{{bg:#000}}
         right after / before the white pricing block so they don't kiss it;
     (c) ensure both sections span the full viewport width to avoid the
         left/right white slivers visible at the edges of the screenshot. */
@media (max-width: 1100px) {{
  section[class*="framer-b1f3u1"],
  section[data-framer-name="Process Section"] {{
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    width: 100% !important;
    max-width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
  }}
  /* The dark Team section + carousel/slideshow that sits right after the
     white pricing block on mobile. Force full-bleed width and add a
     comfortable top padding so there is no collision. */
  section[class*="framer-rTJXX"][class*="framer-2itchk"],
  section[class*="framer-rTJXX"][class*="framer-118wpoh"],
  section[data-framer-name="L"],
  section[data-framer-name="S"] {{
    width: 100% !important;
    max-width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    padding-top: 48px !important;
    padding-bottom: 48px !important;
    background: #000 !important;
    border: 0 !important;
  }}
  /* Any section immediately following the white pricing block — keep a
     clear 48px top gap so the boundary isn't a hairline. */
  section[class*="framer-b1f3u1"] + section,
  section[data-framer-name="Process Section"] + section,
  section[data-framer-name="Process Section"] + div > section {{
    margin-top: 0 !important;
    padding-top: 48px !important;
    border-top: 0 !important;
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
