#!/usr/bin/env python3
"""
FIX 3 — Regardis case mid-section photo caption + mobile hide.

Photos of a woman in the mid-section had no caption (UX audit flagged
'что это? кто это? зачем?').

Fix:
- Inject a real <div class="glavnoe-photo-caption"> after the photos
  with text 'Атмосфера бренд-медиа Regardis' on desktop/tablet.
  Caption is absolutely positioned so it doesn't disrupt the parent's
  flex-row layout (Framer's Bottom row holds text col + photos col).
  MutationObserver re-injects if Framer's hydration replaces children.
- Hide the photos on mobile (<=810px) where they fill the screen
  without context; hide the caption there too.

Idempotent — replaces prior <style id> and <script id> blocks.
"""
import re
import sys
from pathlib import Path

TARGET = Path(__file__).resolve().parent.parent / "work/regardis-telegram-ads-premium/index.html"
STYLE_ID = "glavnoe-regardis-photo-fix"
SCRIPT_ID = "glavnoe-regardis-photo-fix-js"

BLOCK = """
<style id="glavnoe-regardis-photo-fix">
.glavnoe-photo-caption {
    position: absolute;
    /* photos column right-aligned within .framer-1mb2zip (which has no inner
       padding). caption mirrors that column. */
    right: 0;
    bottom: -40px;
    width: 671px;
    text-align: center;
    /* Content section in this case page has WHITE background — caption sits
       in that white area below the photos, so use dark text. */
    color: rgba(0, 0, 0, 0.6);
    font-size: 14px;
    line-height: 1.4;
    letter-spacing: 0.02em;
    pointer-events: none;
    z-index: 5;
}
/* Make sure the Bottom row has room for caption below + relative anchor */
.framer-1mb2zip[data-framer-name="Bottom"] {
    position: relative !important;
}
section.framer-zfg0k1[data-framer-name="Content"] > .framer-1mb2zip[data-framer-name="Bottom"] {
    margin-bottom: 48px;
}
@media (max-width: 810px) {
    .framer-1l5j7fw[data-framer-name="Images"] {
        display: none !important;
    }
    .glavnoe-photo-caption {
        display: none !important;
    }
    section.framer-zfg0k1[data-framer-name="Content"] > .framer-1mb2zip[data-framer-name="Bottom"] {
        margin-bottom: 0;
    }
}
@media (min-width: 811px) and (max-width: 1199.98px) {
    .glavnoe-photo-caption {
        right: 0;
        width: 50%;
    }
}
</style>
<script id="glavnoe-regardis-photo-fix-js">(function(){
  var TEXT = 'Атмосфера бренд-медиа Regardis';
  function ensureCaption(){
    var images = document.querySelector('.framer-1l5j7fw[data-framer-name="Images"]');
    if (!images) return false;
    var bottom = images.closest('.framer-1mb2zip[data-framer-name="Bottom"]');
    if (!bottom) return false;
    var existing = bottom.querySelector(':scope > .glavnoe-photo-caption');
    if (existing) return true;
    var cap = document.createElement('div');
    cap.className = 'glavnoe-photo-caption';
    cap.setAttribute('data-glavnoe-caption', 'regardis');
    cap.textContent = TEXT;
    bottom.appendChild(cap);
    return true;
  }
  function tryNow(){ ensureCaption(); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', tryNow, { once: true });
  } else {
    tryNow();
  }
  var tries = 0;
  var iv = setInterval(function(){
    tries++;
    ensureCaption();
    if (tries >= 100) clearInterval(iv);
  }, 300);
  try {
    var mo = new MutationObserver(function(){ ensureCaption(); });
    mo.observe(document.body, { childList: true, subtree: true });
    setTimeout(function(){ mo.disconnect(); }, 60000);
  } catch(e) {}
})();</script>
"""


def main():
    html = TARGET.read_text(encoding="utf-8")
    for sid in (STYLE_ID, SCRIPT_ID):
        html = re.sub(r'<style id="' + re.escape(sid) + r'">.*?</style>', '', html, flags=re.DOTALL)
        html = re.sub(r'<script id="' + re.escape(sid) + r'">.*?</script>', '', html, flags=re.DOTALL)
    if "</head>" not in html:
        print("ERROR: </head> not found", file=sys.stderr)
        sys.exit(1)
    html = html.replace("</head>", BLOCK.strip() + "</head>", 1)
    TARGET.write_text(html, encoding="utf-8")
    print(f"Injected {STYLE_ID}+{SCRIPT_ID}")


if __name__ == "__main__":
    main()
