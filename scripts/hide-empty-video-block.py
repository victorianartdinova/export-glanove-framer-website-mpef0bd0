#!/usr/bin/env python3
"""
Fix 2: Скрыть «пустой» Video-блок ТОЛЬКО на главной (index.html).

Контекст:
- Раньше широкий CSS `[data-framer-name="Video"]{display:none}` сидел в
  index.html — селектор был «глобальный», но т.к. файл один — реально
  затрагивал только главную. Кейс-страницы не имеют этого селектора
  в HTML, проверено grep-ом.
- На главной этот блок визуально сломан: маленькая картинка слева +
  огромная тёмная пустая область — Вика просила убрать.

Новая версия:
- JS-инжект внутри `index.html`, который скрывает блок ТОЛЬКО если
  его видимое содержимое реально мизерное (картинка слишком маленькая
  относительно высоты блока — height / image-height > 2). Так на других
  страницах (если бы они шарили этот index.html — что не наш случай)
  Video с реальным видео не пострадал бы.
- Дополнительно: маркер `data-fix-page="home-only"` на script-теге,
  чтобы было видно, что фикс scoped к главной.

Idempotent: marker fix:hide-empty-video-v2.
"""
import sys

HTML = '/root/framerexport/full-site-export-may21/index.html'
OLD_STYLE_TAG_START = '<style data-fix="hide-empty-video">'
OLD_STYLE_TAG_END = '</style>'
OLD_SCRIPT_TAG_START = '<script data-fix="hide-empty-video-v2">'
OLD_SCRIPT_TAG_END = '</script>'
MARKER_NEW = '/* fix:hide-empty-video-v3 applied */'

SCRIPT_BLOCK = (
    '<script data-fix="hide-empty-video-v3" data-fix-page="home-only">'
    '/* fix:hide-empty-video-v3 applied */'
    '(function(){'
      'function isBroken(el){'
        'var r=el.getBoundingClientRect();'
        'if(r.height<50)return false;'
        'var media=el.querySelector("video,iframe,img");'
        'if(!media){return (el.textContent||"").trim().length<10;}'
        'var mr=media.getBoundingClientRect();'
        'if(mr.width<10||mr.height<10)return true;'
        'var areaRatio=(mr.width*mr.height)/(r.width*r.height);'
        'return areaRatio<0.15;'
      '}'
      'function check(){'
        'var els=document.querySelectorAll(\'[data-framer-name="Video"]\');'
        'for(var i=0;i<els.length;i++){'
          'var el=els[i];'
          'if(isBroken(el)){el.style.display="none";}'
        '}'
      '}'
      'var tries=0;'
      'var iv=setInterval(function(){tries++;check();if(tries>=200){clearInterval(iv);}},250);'
    '})();'
    '</script>'
)

def remove_block(content, start_tag, end_tag):
    start = content.find(start_tag)
    if start == -1:
        return content, False
    end = content.find(end_tag, start)
    if end == -1:
        return content, False
    return content[:start] + content[end + len(end_tag):], True


def main():
    with open(HTML, 'r', encoding='utf-8') as f:
        content = f.read()

    content, removed_css = remove_block(content, OLD_STYLE_TAG_START, OLD_STYLE_TAG_END)
    content, removed_v2 = remove_block(content, OLD_SCRIPT_TAG_START, OLD_SCRIPT_TAG_END)
    if removed_css:
        print('Removed old broad CSS hide.')
    if removed_v2:
        print('Removed previous v2 script.')

    if MARKER_NEW in content:
        with open(HTML, 'w', encoding='utf-8') as f:
            f.write(content)
        print('v3 already applied.')
        return

    idx = content.find('</head>')
    if idx == -1:
        print('ERROR: </head> not found', file=sys.stderr)
        sys.exit(1)

    new_content = content[:idx] + SCRIPT_BLOCK + '\n' + content[idx:]
    with open(HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('JS injected: area-ratio Video emptiness check (home-only scope).')

if __name__ == '__main__':
    main()
