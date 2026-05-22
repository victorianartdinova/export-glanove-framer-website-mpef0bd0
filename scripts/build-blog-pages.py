#!/usr/bin/env python3
"""Generate clean static blog pages from glavnoe-site MDX articles.

Source: /root/glavnoe-site/content/blog/*.mdx
Target: /root/framerexport/full-site-export-may21/blog/<slug>/index.html

- Parses YAML frontmatter and FAQ list.
- Converts a minimal Markdown subset (paragraphs, headings, lists, bold, italic, links).
- Wraps output in dark theme layout that matches /blog/index.html, /about/, /contact/.
"""
import re
import html
import sys
from pathlib import Path

SRC_DIR = Path('/root/glavnoe-site/content/blog')
DEST_ROOT = Path('/root/framerexport/full-site-export-may21/blog')

TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_html} | ГЛАВНОЕ</title>
<meta name="description" content="{desc_attr}">
<link rel="canonical" href="/blog/{slug}/">
<meta property="og:type" content="article">
<meta property="og:title" content="{title_attr}">
<meta property="og:description" content="{desc_attr}">
<meta property="og:url" content="/blog/{slug}/">
<meta property="og:image" content="/assets/framer/assets/Rf8zWc2T6zVsrABCdIoWtdai428.png">
<meta name="author" content="{author_attr}">
<meta name="keywords" content="{keywords_attr}">
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{background:#0a0a0a;color:#fff;font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}}
  a{{color:inherit;text-decoration:none}}
  .nav{{display:flex;justify-content:space-between;align-items:center;padding:24px 32px;font-size:14px;letter-spacing:0.04em;text-transform:uppercase;border-bottom:1px solid rgba(255,255,255,0.08)}}
  .nav__logo{{font-weight:700;letter-spacing:-0.02em;font-size:20px;text-transform:none}}
  .nav__items{{display:flex;gap:28px;flex-wrap:wrap}}
  .nav__items a:hover{{color:#ff3b30}}
  .hero{{padding:88px 32px 32px;max-width:880px;margin:0 auto}}
  .meta{{font-size:14px;color:rgba(255,255,255,0.5);letter-spacing:0.04em;text-transform:uppercase;margin-bottom:20px;display:flex;flex-wrap:wrap;gap:12px}}
  .hero__title{{font-size:clamp(32px,5vw,56px);line-height:1.1;letter-spacing:-0.02em;font-weight:700}}
  .hero__sub{{margin-top:24px;font-size:clamp(18px,2vw,22px);line-height:1.5;color:rgba(255,255,255,0.7);max-width:760px}}
  .article{{padding:24px 32px 96px;max-width:760px;margin:0 auto;font-size:18px;line-height:1.7;color:rgba(255,255,255,0.85)}}
  .article p{{margin:18px 0}}
  .article h2{{margin:48px 0 16px;font-size:clamp(24px,3vw,32px);letter-spacing:-0.01em;line-height:1.2;color:#fff;font-weight:700}}
  .article h3{{margin:36px 0 12px;font-size:22px;letter-spacing:-0.01em;line-height:1.25;color:#fff;font-weight:600}}
  .article ul,.article ol{{margin:18px 0 18px 24px}}
  .article li{{margin:8px 0}}
  .article a{{color:#ff7a73;text-decoration:underline;text-underline-offset:3px}}
  .article a:hover{{color:#ff3b30}}
  .article strong{{color:#fff}}
  .article blockquote{{margin:32px 0;padding:18px 24px;border-left:3px solid #ff3b30;color:rgba(255,255,255,0.75);font-style:italic}}
  .article hr{{border:none;border-top:1px solid rgba(255,255,255,0.12);margin:48px 0}}
  .faq{{padding:32px 32px 64px;max-width:760px;margin:0 auto}}
  .faq__title{{font-size:clamp(24px,3vw,32px);letter-spacing:-0.01em;line-height:1.2;color:#fff;margin-bottom:24px}}
  .faq__item{{padding:24px 0;border-top:1px solid rgba(255,255,255,0.12)}}
  .faq__q{{font-size:18px;color:#fff;font-weight:600;margin-bottom:8px}}
  .faq__a{{font-size:16px;line-height:1.6;color:rgba(255,255,255,0.75)}}
  .cta{{padding:48px 32px 96px;max-width:760px;margin:0 auto;text-align:center}}
  .cta__title{{font-size:clamp(24px,3vw,32px);letter-spacing:-0.01em;color:#fff;margin-bottom:24px}}
  .cta__btn{{display:inline-flex;align-items:center;gap:12px;padding:18px 32px;background:#ff3b30;color:#fff;border-radius:48px;font-size:16px;letter-spacing:0.02em;text-transform:uppercase;font-weight:600}}
  .footer{{padding:48px 32px;border-top:1px solid rgba(255,255,255,0.08);font-size:14px;color:rgba(255,255,255,0.5);display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}}
  .footer a:hover{{color:#fff}}
</style>
</head>
<body>
<nav class="nav">
  <a class="nav__logo" href="/">ГЛАВНОЕ</a>
  <div class="nav__items">
    <a href="/">Главная</a>
    <a href="/#products">Услуги</a>
    <a href="/cases/portfolio/">Кейсы</a>
    <a href="/#results">Результаты</a>
    <a href="/blog/">Статьи</a>
  </div>
</nav>
<section class="hero">
  <div class="meta">
    <span>(гайды и инсайты)</span>
    <span>{date_html}</span>
    <span>{author_html}</span>
  </div>
  <h1 class="hero__title">{title_html}</h1>
  <p class="hero__sub">{desc_html}</p>
</section>
<article class="article">
{body_html}
</article>
{faq_block}
<section class="cta">
  <div class="cta__title">Напишем под ваш проект — расскажите задачу</div>
  <a class="cta__btn" href="mailto:hello@glavnoe.com">Написать на hello@glavnoe.com</a>
</section>
<footer class="footer">
  <span>© 2026 ГЛАВНОЕ</span>
  <div class="nav__items">
    <a href="/blog/">Все статьи</a>
    <a href="mailto:hello@glavnoe.com">hello@glavnoe.com</a>
    <a href="https://t.me/glavnoe_channel" target="_blank" rel="noopener">Telegram</a>
    <a href="https://www.instagram.com/glavnoe_agency" target="_blank" rel="noopener">Instagram</a>
  </div>
</footer>
</body>
</html>
"""


def parse_frontmatter(text: str):
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---', 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip()
    body = text[end + 4:]
    fm = {}
    current_key = None
    current_list = None
    pending_obj = None
    pending_obj_list = None
    for raw_line in raw.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$', line)
        if m and not line.startswith(' ') and not line.startswith('\t'):
            key, val = m.group(1), m.group(2).strip()
            if val == '':
                fm[key] = []
                current_list = fm[key]
                current_key = key
                pending_obj = None
            else:
                if val.startswith('[') and val.endswith(']'):
                    inner = val[1:-1]
                    items = [x.strip().strip('"\'') for x in re.split(r',(?![^\[]*\])', inner) if x.strip()]
                    fm[key] = items
                else:
                    fm[key] = val.strip('"\'')
                current_list = None
                current_key = None
                pending_obj = None
        elif line.lstrip().startswith('-'):
            content = line.lstrip()[1:].strip()
            if current_list is None:
                continue
            if ':' in content:
                ks = content.split(':', 1)
                k = ks[0].strip()
                v = ks[1].strip().strip('"\'')
                pending_obj = { k: v }
                current_list.append(pending_obj)
            else:
                current_list.append(content.strip('"\''))
                pending_obj = None
        elif pending_obj is not None and ':' in line.lstrip():
            ks = line.lstrip().split(':', 1)
            k = ks[0].strip()
            v = ks[1].strip().strip('"\'')
            pending_obj[k] = v
    return fm, body


INLINE_LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
INLINE_BOLD = re.compile(r'\*\*([^*]+)\*\*')
INLINE_ITAL = re.compile(r'(?<!\*)\*([^*]+)\*(?!\*)')
INLINE_CODE = re.compile(r'`([^`]+)`')


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = INLINE_CODE.sub(lambda m: f'<code style="font-family:ui-monospace,Menlo,Monaco,monospace;background:rgba(255,255,255,0.08);padding:2px 6px;border-radius:6px;font-size:.92em">{m.group(1)}</code>', text)
    text = INLINE_LINK.sub(lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>', text)
    text = INLINE_BOLD.sub(lambda m: f'<strong>{m.group(1)}</strong>', text)
    text = INLINE_ITAL.sub(lambda m: f'<em>{m.group(1)}</em>', text)
    return text


def render_markdown(md: str) -> str:
    lines = md.splitlines()
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith('#'):
            m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
            if m:
                level = min(len(m.group(1)), 6)
                tag = f'h{max(2, level)}'
                out.append(f'<{tag}>{inline(m.group(2))}</{tag}>')
                i += 1
                continue
        if stripped == '---':
            out.append('<hr>')
            i += 1
            continue
        if stripped.startswith('> '):
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip().lstrip('>').lstrip())
                i += 1
            out.append('<blockquote>' + inline(' '.join(buf)) + '</blockquote>')
            continue
        if re.match(r'^[-*]\s+', stripped):
            buf = []
            while i < n and re.match(r'^[-*]\s+', lines[i].strip()):
                buf.append(re.sub(r'^[-*]\s+', '', lines[i].strip()))
                i += 1
            out.append('<ul>' + ''.join(f'<li>{inline(b)}</li>' for b in buf) + '</ul>')
            continue
        if re.match(r'^\d+\.\s+', stripped):
            buf = []
            while i < n and re.match(r'^\d+\.\s+', lines[i].strip()):
                buf.append(re.sub(r'^\d+\.\s+', '', lines[i].strip()))
                i += 1
            out.append('<ol>' + ''.join(f'<li>{inline(b)}</li>' for b in buf) + '</ol>')
            continue
        # paragraph
        buf = [stripped]
        i += 1
        while i < n and lines[i].strip() and not re.match(r'^(#{1,6} |[-*] |\d+\.\s|> |---)', lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        out.append('<p>' + inline(' '.join(buf)) + '</p>')
    return '\n'.join(out)


def strip_mdx_imports(md: str) -> str:
    """Drop <import statements, <Component .../> blocks, JSX-only lines we cannot render."""
    lines = []
    for line in md.splitlines():
        if re.match(r'^\s*import\s', line):
            continue
        if re.match(r'^\s*<[A-Z][A-Za-z0-9_]*[\s/>]', line):
            continue
        if re.match(r'^\s*</[A-Z][A-Za-z0-9_]*>', line):
            continue
        lines.append(line)
    return '\n'.join(lines)


def render_faq(faq):
    if not faq:
        return ''
    items = []
    for it in faq:
        if not isinstance(it, dict):
            continue
        q = it.get('question', '')
        a = it.get('answer', '')
        if not q or not a:
            continue
        items.append(f'<div class="faq__item"><div class="faq__q">{html.escape(q)}</div><div class="faq__a">{html.escape(a)}</div></div>')
    if not items:
        return ''
    return '<section class="faq"><h2 class="faq__title">Частые вопросы</h2>' + '\n'.join(items) + '</section>'


def build_page(mdx_path: Path, slug: str):
    raw = mdx_path.read_text(encoding='utf-8')
    fm, body = parse_frontmatter(raw)
    body = strip_mdx_imports(body)
    body_html = render_markdown(body)
    faq_block = render_faq(fm.get('faq'))
    keywords = ', '.join(fm.get('keywords', [])) if isinstance(fm.get('keywords'), list) else fm.get('keywords', '')
    ctx = {
        'slug': slug,
        'title_html': html.escape(fm.get('title', slug)),
        'title_attr': html.escape(fm.get('title', slug), quote=True),
        'desc_html': html.escape(fm.get('description', '')),
        'desc_attr': html.escape(fm.get('description', ''), quote=True),
        'date_html': html.escape(fm.get('date', '')),
        'author_html': html.escape(fm.get('author', '')),
        'author_attr': html.escape(fm.get('author', ''), quote=True),
        'keywords_attr': html.escape(keywords, quote=True),
        'body_html': body_html,
        'faq_block': faq_block,
    }
    return TEMPLATE.format(**ctx)


def main():
    items = []
    if not SRC_DIR.exists():
        print(f'SOURCE MISSING: {SRC_DIR}')
        return 1
    for mdx in sorted(SRC_DIR.glob('*.mdx')):
        slug = mdx.stem
        target_dir = DEST_ROOT / slug
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / 'index.html'
        page = build_page(mdx, slug)
        target.write_text(page, encoding='utf-8')
        items.append(slug)
        print(f'OK {slug}')
    print(f'Generated {len(items)} blog pages')

if __name__ == '__main__':
    sys.exit(main())
