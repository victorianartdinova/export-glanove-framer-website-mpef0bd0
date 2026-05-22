#!/usr/bin/env python3
"""
Fix Home Article Cards — 4 placeholder cards (Velocity Becomes / Way To
Clearance / All Grapples / Flowers Love) перед футером главной заменить
на 4 реальных блог-поста.

Проблема: nav-fixer.js имел fixBlogCards(), но:
1. Селектор не матчил href вида "./blog/velocity-becomes/index.html"
   (BLOG_CARDS ключи начинаются с "/", а Framer-export пишет "./").
2. Селектор `t.children.length === 0` отсекал [data-framer-name="Title"]
   потому что внутри есть <p class="framer-text">. Текст лежал глубже.
3. Framer-хидратация переопределяет SSR-HTML позже, чем срабатывает
   run() из nav-fixer (DOMContentLoaded + 500/1800/4000ms).

Что делает скрипт:
1. Идемпотентно патчит scripts/nav-fixer.js:
   - BLOG_CARDS дополнен полем year (=© 2026) и matchTitles[] для
     резервного фолбэка по тексту английского плейсхолдера
   - _normalizeBlogHref() обрабатывает "./blog/...", "blog/...", "/blog/..."
   - fixBlogCards() рекурсивно ищет leaf-текстовый элемент внутри
     Title/Category/Year (включая вложенный <p class="framer-text">)
   - Селектор [data-framer-name="Year"] подменяет копирайт на "© 2026"
   - Добавлен MutationObserver для ловли пост-хидратационных ре-рендеров
2. Перезапускает inject-nav-fixer.py — обновлённый код инлайнится в
   HTML-страницы (там фактически загружается).

Идемпотентность: маркер MARKER в файле, повторный запуск skip.
"""
import subprocess
from pathlib import Path

ROOT = Path('/root/framerexport/full-site-export-may21')
NAV_FIXER = ROOT / 'scripts' / 'nav-fixer.js'
MARKER = '/* fix:home-article-cards-v2 applied */'

NEW_BLOG_CARDS = """  var BLOG_CARDS = {
    '/blog/way-to-clearance/':  { slug: 'strategiya-marketinga-dlya-developera-2026', title: 'Стратегия маркетинга для девелопера в 2026', tag: 'Стратегия', year: '© 2026', match: ['Way To Clearance'] },
    '/blog/all-grapples/':      { slug: 'kak-zastrojshchiku-vesti-telegram-kanal',     title: 'Как застройщику вести Telegram-канал',           tag: 'Telegram', year: '© 2026', match: ['All Grapples'] },
    '/blog/flowers-love/':      { slug: '6-sdelok-srednim-chekom-15-mln-telegram-ads', title: '6 сделок × 15 млн ₽ через Telegram Ads',          tag: 'Кейс',     year: '© 2026', match: ['Flowers Love'] },
    '/blog/velocity-becomes/':  { slug: 'gde-iskat-klientov-brokeru-2026',             title: 'Где брокеру искать клиентов в 2026',             tag: 'Брокеры',  year: '© 2026', match: ['Velocity Becomes'] }
  };
"""

NEW_FIX_BLOG_CARDS = r"""  function _normalizeBlogHref(raw){
    if (!raw) return '';
    var n = raw.replace(/^https?:\/\/[^/]+/, '');
    n = n.replace(/^\.\//, '/');
    if (n.charAt(0) !== '/') n = '/' + n;
    n = n.replace(/index\.html$/, '');
    if (!n.endsWith('/')) n += '/';
    return n;
  }

  // Recursively find the deepest descendant text-bearing element.
  // Returns either a text-only <p>/<span> or the original element.
  function _leafTextEl(el){
    if (!el) return el;
    var cur = el;
    var guard = 0;
    while (cur && cur.children && cur.children.length === 1 && guard < 6) {
      cur = cur.children[0];
      guard++;
    }
    return cur;
  }

  function _setLeafText(el, newText){
    var leaf = _leafTextEl(el);
    if (!leaf) return;
    if (leaf.children.length === 0 && (leaf.textContent || '').trim() !== newText) {
      leaf.textContent = newText;
    }
  }

  function _findBlogMapByPlaceholderTitle(anchor){
    var titleEl = anchor.querySelector('[data-framer-name="Title"], h2, h3, h4');
    if (!titleEl) return null;
    var t = (titleEl.textContent || '').trim();
    for (var k in BLOG_CARDS){
      if (!Object.prototype.hasOwnProperty.call(BLOG_CARDS, k)) continue;
      var m = BLOG_CARDS[k];
      if (!m.match) continue;
      for (var i=0;i<m.match.length;i++){ if (m.match[i] === t) return m; }
    }
    return null;
  }

  function fixBlogCards(){
    document.querySelectorAll('a[href]').forEach(function(a){
      var raw = a.getAttribute('href');
      var normalized = _normalizeBlogHref(raw);
      var map = BLOG_CARDS[normalized] || _findBlogMapByPlaceholderTitle(a);
      if (!map) return;
      var newHref = '/blog/' + map.slug + '/';
      if (a.getAttribute('href') !== newHref) a.setAttribute('href', newHref);
      a.querySelectorAll('h2, h3, h4, [data-framer-name="Title"]').forEach(function(t){
        _setLeafText(t, map.title);
      });
      a.querySelectorAll('[data-framer-name="Tag"], [data-framer-name="Category"]').forEach(function(t){
        _setLeafText(t, map.tag);
      });
      if (map.year) {
        a.querySelectorAll('[data-framer-name="Year"]').forEach(function(t){
          _setLeafText(t, map.year);
        });
      }
    });
  }

  // MutationObserver — ловит пост-хидратационные ре-рендеры Framer,
  // которые откатывают наши правки.
  function _watchBlogCards(){
    if (!isHomepage()) return;
    if (window.__glavnoeBlogCardObserver) return;
    var pending = false;
    var obs = new MutationObserver(function(){
      if (pending) return;
      pending = true;
      requestAnimationFrame(function(){
        pending = false;
        try { fixBlogCards(); } catch(e){}
      });
    });
    obs.observe(document.body, { childList: true, subtree: true, characterData: true });
    window.__glavnoeBlogCardObserver = obs;
    setTimeout(function(){ try { obs.disconnect(); } catch(e){} }, 30000);
  }
"""


def patch_nav_fixer():
    src = NAV_FIXER.read_text(encoding='utf-8')
    if MARKER in src:
        print('nav-fixer.js: already patched, skip.')
        return False

    # 1. Replace BLOG_CARDS block
    s = src.find('  var BLOG_CARDS = {')
    if s == -1:
        raise SystemExit('BLOG_CARDS block not found')
    e = src.find('  };', s)
    if e == -1:
        raise SystemExit('BLOG_CARDS closing not found')
    e_eol = src.find('\n', e) + 1
    src = src[:s] + NEW_BLOG_CARDS + src[e_eol:]

    # 2. Replace fixBlogCards function (scan brace balance)
    fbc_start = src.find('  function fixBlogCards(){')
    if fbc_start == -1:
        raise SystemExit('fixBlogCards function not found')
    idx = fbc_start
    depth = 0
    started = False
    end_fbc = -1
    while idx < len(src):
        ch = src[idx]
        if ch == '{':
            depth += 1
            started = True
        elif ch == '}':
            depth -= 1
            if started and depth == 0:
                end_fbc = idx + 1
                if idx + 1 < len(src) and src[idx+1] == '\n':
                    end_fbc = idx + 2
                break
        idx += 1
    if end_fbc == -1:
        raise SystemExit('fixBlogCards function end not found')
    src = src[:fbc_start] + NEW_FIX_BLOG_CARDS + src[end_fbc:]

    # 3. Hook _watchBlogCards into run()
    src = src.replace(
        '    try { fixBlogCards(); } catch(e){}\n',
        '    try { fixBlogCards(); } catch(e){}\n'
        '    try { _watchBlogCards(); } catch(e){}\n',
        1
    )

    # 4. Marker
    src = MARKER + '\n' + src
    NAV_FIXER.write_text(src, encoding='utf-8')
    print('Patched nav-fixer.js with marker', MARKER)
    return True


def main():
    changed = patch_nav_fixer()
    # Re-run inject-nav-fixer.py so updated code is inlined in HTML pages.
    if changed:
        print('Re-injecting nav-fixer into HTML...')
        subprocess.run(['python3', str(ROOT / 'scripts' / 'inject-nav-fixer.py')], check=True, cwd=str(ROOT))


if __name__ == '__main__':
    main()
