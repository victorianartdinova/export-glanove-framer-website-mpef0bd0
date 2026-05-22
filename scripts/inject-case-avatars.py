#!/usr/bin/env python3
"""
Inject client + media avatars into case study hero.

Adds a 64px circular avatar pair (client + media outlet) below the existing
metric-hero card in the right column of the hero-grid.

CSS is appended into the existing <style> block, HTML is wrapped around the
existing <aside class="metric-hero"> so that avatars stack below it.

Idempotent: skips if [data-glavnoe-avatars] already present.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

CASES = {
    "case-spb-15mln": {
        "client_src": "assets/avatars/client-belyaev.jpg",
        "client_alt": "Александр Беляев, агентство недвижимости СПб",
        "media_src": "assets/avatars/media-ppc-world.png",
        "media_alt": "ppc.world — публикация кейса",
        "caption": "Клиент: агентство недвижимости, СПб · СМИ: ppc.world",
    },
    "case-aag-promostranicy": {
        "client_src": "assets/avatars/client-barakovskaya.jpg",
        "client_alt": "Евгения Бараковская, руководитель рекламы AAG Development",
        "media_src": "assets/avatars/media-efir.svg",
        "media_alt": "Эфир ГЛАВНОЕ — внутренняя публикация кейса",
        "caption": "Клиент: AAG Development · СМИ: Эфир ГЛАВНОЕ",
    },
    "regardis-telegram-ads-premium": {
        "client_src": "assets/avatars/client-regardis.svg",
        "client_alt": "Regardis — агентство премиум-недвижимости в Москве",
        "media_src": "assets/avatars/media-elama.png",
        "media_alt": "eLama — публикация кейса",
        "caption": "Клиент: Regardis · СМИ: eLama",
    },
}

CSS_BLOCK = """
/* === case avatars (client + media outlet) === */
.hero-side{display:flex;flex-direction:column;gap:18px}
.avatars{display:flex;align-items:center;gap:14px;justify-content:center;background:var(--bg-card);border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px}
.avatars .av{display:flex;flex-direction:column;align-items:center;gap:8px;min-width:0}
.avatars .av-circle{width:64px;height:64px;border-radius:50%;overflow:hidden;border:1px solid #E5E0D8;background:#0d0d0d;flex:none;display:flex;align-items:center;justify-content:center}
.avatars .av-circle img{width:100%;height:100%;object-fit:cover;display:block}
.avatars .av-circle svg{width:100%;height:100%;display:block}
.avatars .av-role{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--text-mute);text-align:center}
.avatars .av-sep{width:1px;height:48px;background:var(--line-2);flex:none}
.avatars-caption{font-size:12px;color:var(--text-mute);text-align:center;line-height:1.5;margin-top:-4px}
@media (max-width:809px){
  .avatars{padding:14px 16px;gap:10px}
  .avatars .av-circle{width:40px;height:40px}
  .avatars .av-sep{height:36px}
  .avatars .av-role{font-size:10px}
  .avatars-caption{font-size:11px}
}
"""

CSS_MARKER = "/* === case avatars (client + media outlet) === */"
ASIDE_RE = re.compile(
    r'(<aside class="metric-hero">.*?</aside>)',
    re.DOTALL,
)


def build_html(client_src: str, client_alt: str, media_src: str, media_alt: str,
               caption: str) -> str:
    def render_img(src: str, alt: str) -> str:
        # SVG inline rendering via <img> works fine; keep object-fit cover
        return f'<img src="{src}" alt="{alt}" loading="lazy">'

    return (
        '<div class="avatars" data-glavnoe-avatars role="group" '
        f'aria-label="{caption}">'
        '<div class="av">'
        f'<div class="av-circle">{render_img(client_src, client_alt)}</div>'
        '<div class="av-role">Клиент</div>'
        '</div>'
        '<div class="av-sep" aria-hidden="true"></div>'
        '<div class="av">'
        f'<div class="av-circle">{render_img(media_src, media_alt)}</div>'
        '<div class="av-role">СМИ</div>'
        '</div>'
        '</div>'
        f'<p class="avatars-caption">{caption}</p>'
    )


def inject(path: pathlib.Path, conf: dict) -> str:
    text = path.read_text(encoding="utf-8")

    if "data-glavnoe-avatars" in text:
        return "skip: avatars already present"

    # 1) inject CSS before closing </style> of the first <style> block
    if CSS_MARKER not in text:
        style_close = text.find("</style>")
        if style_close == -1:
            return "fail: no </style> found"
        text = text[:style_close] + CSS_BLOCK + text[style_close:]

    # 2) wrap <aside class="metric-hero">...</aside> with hero-side div +
    #    append avatars HTML inside it
    avatars_html = build_html(
        conf["client_src"], conf["client_alt"],
        conf["media_src"], conf["media_alt"],
        conf["caption"],
    )

    def repl(m: re.Match) -> str:
        aside = m.group(1)
        return (
            '<div class="hero-side">'
            f"{aside}"
            f"{avatars_html}"
            "</div>"
        )

    new_text, count = ASIDE_RE.subn(repl, text, count=1)
    if count == 0:
        return "fail: <aside class=\"metric-hero\"> not found"

    path.write_text(new_text, encoding="utf-8")
    return f"ok: injected (css+html)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--root",
        default="/root/framerexport/full-site-export-may21/work",
        help="work/ root path",
    )
    ap.add_argument(
        "--case",
        choices=list(CASES.keys()) + ["all"],
        default="all",
    )
    args = ap.parse_args()

    cases = list(CASES.keys()) if args.case == "all" else [args.case]
    root = pathlib.Path(args.root)
    for c in cases:
        p = root / c / "index.html"
        if not p.exists():
            print(f"{c}: missing {p}", file=sys.stderr)
            continue
        result = inject(p, CASES[c])
        print(f"{c}: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
