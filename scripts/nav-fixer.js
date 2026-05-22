(function(){
  if (window.__glavnoeNavFixerLoaded) return;
  window.__glavnoeNavFixerLoaded = true;

  var NAV_MAP = {
    'Услуги':       '/#products',
    'Результаты':   '/#results',
    'Статьи':       '/blog/',
    'Кейсы':        '/cases/portfolio/',
    'Главная':      '/',
    'Написать CEO': 'mailto:hello@glavnoe.com',
    'СТАРТ ПРОЕКТА': '/contact/',
    'START PROJECT': '/contact/',
    'Забронировать звонок': '/contact/',
    'забронировать': '/contact/',
    'Написать сейчас': '/contact/'
  };

  var SECTION_MARKERS = {
    '(Немного о нас)':    'about',
    '(Что придумали)':    'products',
    '(Результаты)':       'results',
    '(гайды и инсайты)':  'articles',
    '(Ваша обратная свзяь)': 'contact'
  };

  var BLOG_CARDS = {
    '/blog/way-to-clearance/':  { slug: 'strategiya-marketinga-dlya-developera-2026', title: 'Стратегия маркетинга для девелопера в 2026', tag: 'Стратегия' },
    '/blog/all-grapples/':      { slug: 'kak-zastrojshchiku-vesti-telegram-kanal',     title: 'Как застройщику вести Telegram-канал',           tag: 'Telegram' },
    '/blog/flowers-love/':      { slug: '6-sdelok-srednim-chekom-15-mln-telegram-ads', title: '6 сделок × 15 млн ₽ через Telegram Ads — кейс',  tag: 'Кейс' },
    '/blog/velocity-becomes/':  { slug: 'gde-iskat-klientov-brokeru-2026',             title: 'Где брокеру искать клиентов в 2026',             tag: 'Брокеры' }
  };

  // Post-hydration text replacements — Framer SSR can re-render and overwrite static HTML edits.
  // These mirror the static replacements in product/*/index.html, work/*/index.html, 404/index.html.
  var TEXT_REPLACEMENTS = {
    'Glavnoe@2026':       'ГЛАВНОЕ © 2026',
    'START PROJECT':      'Запустить проект',
    '(Meet Our Team)':    '(Наша команда)',
    'Live Preview':       'Смотреть кейс',
    '404 Error':          '404 — Страница не найдена',
    'A curated selection of refined digital work shaped through structure.':
      'Похоже, страница потерялась. Вернитесь на главную или посмотрите наши работы.'
  };

  function fixVisibleText(){
    document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, a, div').forEach(function(el){
      if (el.children.length) return;
      var t = (el.textContent || '').trim();
      if (!t) return;
      var rep = TEXT_REPLACEMENTS[t];
      if (rep && el.textContent !== rep) el.textContent = rep;
    });
  }

  // Hide 5th "Skate" card on homepage Article section — no Russian content mapped for it.
  function hideExtraBlogCards(){
    if (!isHomepage()) return;
    document.querySelectorAll('h5.framer-text').forEach(function(el){
      if ((el.textContent || '').trim() === 'Skate') {
        var card = el.closest('a, [data-framer-name="Card"], .framer-h52ftj') || el.parentElement;
        if (card) card.style.setProperty('display', 'none', 'important');
      }
    });
  }

  function fixBlogCards(){
    document.querySelectorAll('a[href]').forEach(function(a){
      var raw = a.getAttribute('href');
      if (!raw) return;
      var normalized = raw.replace(/^https?:\/\/[^/]+/, '').replace(/index\.html$/, '');
      if (!normalized.endsWith('/')) normalized += '/';
      var map = BLOG_CARDS[normalized];
      if (!map) return;
      var newHref = '/blog/' + map.slug + '/';
      if (a.getAttribute('href') !== newHref) a.setAttribute('href', newHref);
      a.querySelectorAll('h2, h3, h4, [data-framer-name="Title"]').forEach(function(t){
        if (t.children.length === 0 && t.textContent && t.textContent.trim() !== map.title) {
          t.textContent = map.title;
        }
      });
      a.querySelectorAll('[data-framer-name="Tag"], [data-framer-name="Category"]').forEach(function(t){
        if (t.children.length === 0 && t.textContent && t.textContent.trim().length && t.textContent.trim() !== map.tag) {
          t.textContent = map.tag;
        }
      });
    });
  }

  function fixLinks(root){
    (root || document).querySelectorAll('a').forEach(function(a){
      var t = (a.textContent || '').trim();
      if (!t) return;
      var dest = NAV_MAP[t];
      if (!dest) return;
      if (a.getAttribute('href') === dest) return;
      a.setAttribute('href', dest);
      if (dest.indexOf('mailto:') !== 0 && a.getAttribute('target') === '_blank') {
        a.removeAttribute('target');
      }
    });
  }

  function addAnchorIds(){
    if (!isHomepage()) return;
    Object.keys(SECTION_MARKERS).forEach(function(marker){
      var id = SECTION_MARKERS[marker];
      if (document.getElementById(id)) return;
      var hit = Array.from(document.querySelectorAll('p, h2, h3, h4, span')).find(function(el){
        return el.textContent && el.textContent.trim() === marker && el.children.length === 0;
      });
      if (!hit) return;
      var sec = hit.closest('section') || hit.closest('div[data-framer-name]') || hit.parentElement;
      if (sec && !sec.id) sec.id = id;
    });
  }

  function isHomepage(){
    var p = window.location.pathname.replace(/index\.html$/, '');
    return p === '/' || p === '';
  }

  function isProductPage(){
    return /^\/product\/[a-z0-9-]+\//.test(window.location.pathname.replace(/index\.html$/, ''));
  }

  function injectPricingNote(){
    if (!isProductPage()) return;
    if (document.querySelector('[data-glavnoe-injected="pricing-note"]')) return;
    var pricingHead = Array.from(document.querySelectorAll('p, h2, h3')).find(function(el){
      return el.textContent && el.textContent.trim() === '(Стоимость)';
    });
    if (!pricingHead) return;
    var sec = pricingHead.closest('section');
    if (!sec || !sec.parentNode) return;
    var note = document.createElement('section');
    note.setAttribute('data-glavnoe-injected', 'pricing-note');
    note.style.cssText = 'background:#0a0a0a;color:#fff;padding:72px 24px 88px;text-align:center';
    note.innerHTML = ''
      + '<div style="max-width:760px;margin:0 auto">'
      + '  <div style="font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:32px;line-height:1.15;letter-spacing:-1px;margin-bottom:20px">Нужен другой формат работы?</div>'
      + '  <div style="font-family:\'Suisse Intl Regular\',sans-serif;font-size:18px;line-height:1.5;color:rgba(255,255,255,0.75);margin-bottom:36px">Мы открыты к индивидуальным задачам и нестандартным условиям сотрудничества. Расскажите о вашем проекте — предложим оптимальное решение под ваши цели и вводные данные.</div>'
      + '  <a href="mailto:hello@glavnoe.com" style="display:inline-flex;align-items:center;gap:12px;padding:18px 32px;background:#ff3b30;color:#fff;text-decoration:none;border-radius:48px;font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:16px;letter-spacing:0.02em;text-transform:uppercase">Написать на hello@glavnoe.com</a>'
      + '</div>';
    sec.parentNode.insertBefore(note, sec.nextSibling);
  }

  var HOMEPAGE_CASES = [
    {
      href: '/work/case-spb-15mln/',
      tag: 'Telegram Ads · СПб',
      title: '6 сделок × 15 млн ₽ через Telegram Ads',
      metrics: [['6','Сделок'],['15 млн ₽','Средний чек'],['19 973 ₽','CPL']],
      desc: 'Премиум-агентство недвижимости, 4 месяца, бюджет 1 053 352 ₽. Опубликовано на PPC World.'
    },
    {
      href: '/work/case-aag-promostranicy/',
      tag: 'ПромоСтраницы · AAG',
      title: 'ROI 6000% на ПромоСтраницах Яндекса',
      metrics: [['6 000%','ROI'],['−32%','CPL vs контекст'],['62%','Дочитываемость']],
      desc: 'AAG Development, премиум-девелопер СПб. 3 формата статей, гео СПб+ЛО.'
    },
    {
      href: '/work/regardis-telegram-ads-premium/',
      tag: 'Telegram Ads · Москва',
      title: '50+ квал-лидов в месяц на премиум',
      metrics: [['50+','Лидов/мес'],['9 684 ₽','CPL'],['20 млн ₽','Средний чек']],
      desc: 'Regardis. Бренд-медиа в Telegram + баннеры Telegram Ads, бюджет 1 млн ₽/мес.'
    }
  ];

  function injectHomepageCases(){
    if (!isHomepage()) return;
    if (document.querySelector('[data-glavnoe-injected="homepage-cases"]')) return;
    var anchor = document.getElementById('results')
              || Array.from(document.querySelectorAll('p, h2, h3')).find(function(el){
                   return el.textContent && el.textContent.trim() === '(Результаты)';
                 });
    if (!anchor) return;
    var hostSection = anchor.closest('section') || anchor;
    if (!hostSection || !hostSection.parentNode) return;
    var sec = document.createElement('section');
    sec.id = 'cases';
    sec.setAttribute('data-glavnoe-injected', 'homepage-cases');
    sec.style.cssText = 'background:#0a0a0a;color:#fff;padding:96px 24px 96px';
    var cards = HOMEPAGE_CASES.map(function(c){
      var metrics = c.metrics.map(function(m){
        return '<div style="flex:1 1 0;min-width:96px"><div style="font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:24px;line-height:1;letter-spacing:-0.02em;color:#fff">'+m[0]+'</div><div style="font-family:\'Suisse Intl Regular\',sans-serif;font-size:12px;line-height:1.3;color:rgba(255,255,255,0.5);margin-top:6px">'+m[1]+'</div></div>';
      }).join('');
      return '<a href="'+c.href+'" style="background:#141414;border:1px solid rgba(255,255,255,0.08);border-radius:24px;padding:32px;display:flex;flex-direction:column;gap:18px;text-decoration:none;color:inherit;transition:border-color .2s">'
        + '<div style="display:flex;justify-content:space-between;font-family:\'Suisse Intl Regular\',sans-serif;font-size:12px;letter-spacing:0.08em;text-transform:uppercase;color:#ff3b30"><span>'+c.tag+'</span><span style="color:rgba(255,255,255,0.4)">2026</span></div>'
        + '<div style="font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:22px;line-height:1.2;letter-spacing:-0.01em;color:#fff">'+c.title+'</div>'
        + '<div style="display:flex;gap:16px;flex-wrap:wrap">'+metrics+'</div>'
        + '<div style="font-family:\'Suisse Intl Regular\',sans-serif;font-size:14px;line-height:1.5;color:rgba(255,255,255,0.6);flex:1">'+c.desc+'</div>'
        + '<div style="margin-top:4px;font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:13px;letter-spacing:0.05em;text-transform:uppercase;color:#ff3b30">Открыть кейс →</div>'
        + '</a>';
    }).join('');
    sec.innerHTML = '<div style="max-width:1392px;margin:0 auto">'
      + '<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:32px;font-family:\'Suisse Intl Regular\',sans-serif;font-size:14px;color:rgba(255,255,255,0.4)"><span>(03)</span><span>(Кейсы)</span><span>© 2026</span></div>'
      + '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px">'+cards+'</div>'
      + '<div style="margin-top:48px;text-align:center"><a href="/cases/portfolio/" style="display:inline-flex;align-items:center;gap:12px;padding:18px 32px;background:transparent;color:#fff;border:1px solid rgba(255,255,255,0.3);border-radius:48px;text-decoration:none;font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:14px;letter-spacing:0.04em;text-transform:uppercase">Все кейсы →</a></div>'
      + '</div>';
    hostSection.parentNode.insertBefore(sec, hostSection.nextSibling);
  }

  var TEMPLATE_TEXTS = [
    'Industries → our designs have supported businesses, adapting to unique needs and challenges',
    'our designs have supported businesses, adapting to unique needs and challenges',
    'Industries → our designs',
    'adapting to unique needs and challenges'
  ];

  // 4 slots of Framer Stats carousel — slot 1 is product-specific, slots 2-4 are agency-wide
  var PRODUCT_STATS = {
    '/product/avito-ads/':       [['1000+','Стоимость целевого обращения на недвижимость бизнес и премиум-класса']],
    '/product/content-product/': [['500+', 'Запусков контент-систем для застройщиков и агентств недвижимости']],
    '/product/product-statii/':  [['6000+','Обращений с ПромоСтраниц Яндекса по цене на 32% ниже контекста']],
    '/product/product-telegram/':[['800+', 'Заявок из Telegram Ads с CPL в 2 раза ниже рынка']],
    '/product/youtube-product/': [['50+',  'Личных брендов основателей запущенных за 1.5 недели']]
  };
  var CASE_STATS = {
    '/work/case-spb-15mln/':                [['6',    'Сделок премиум-недвижимости закрыто через Telegram Ads']],
    '/work/case-aag-promostranicy/':        [['6000%','ROI на ПромоСтраницах Яндекса для AAG Development']],
    '/work/regardis-telegram-ads-premium/': [['50+',  'Квалифицированных лидов в месяц на премиум-недвижимость']]
  };
  // Agency-wide stats — used for slots 2..N on every product/case page
  var AGENCY_STATS = [
    ['3600+', 'Квалифицированных заявок собрано для клиентов в недвижимости'],
    ['1M+',   'Охватов в Telegram и Яндекс ПромоСтраницах ежемесячно'],
    ['20K+',  'Подписчиков на каналах клиентов'],
    ['№1',    'Performance-агентство в нише недвижимости по CPL']
  ];

  function pageStats(){
    var head = PRODUCT_STATS[path()] || CASE_STATS[path()];
    if (!head) return null;
    return head.concat(AGENCY_STATS);
  }

  function patchTemplateBlocks(){
    var stats = pageStats();
    // 1. Replace each "30+" by index from stats list
    if (stats) {
      var bigNodes = [];
      document.querySelectorAll('h1, h2, h3, p, span, div').forEach(function(el){
        if (el.children.length) return;
        if ((el.textContent || '').trim() === '30+') bigNodes.push(el);
      });
      bigNodes.forEach(function(el, i){
        var s = stats[Math.min(i, stats.length - 1)];
        if (s && s[0]) el.textContent = s[0];
      });
      // 2. Replace each template phrase by index from stats list
      var phraseNodes = [];
      document.querySelectorAll('h1, h2, h3, h4, p, span, div').forEach(function(el){
        if (el.children.length) return;
        var t = (el.textContent || '').trim();
        if (!t) return;
        if (TEMPLATE_TEXTS.some(function(p){ return t.indexOf(p) >= 0; })) phraseNodes.push(el);
      });
      phraseNodes.forEach(function(el, i){
        var s = stats[Math.min(i, stats.length - 1)];
        if (s && s[1]) el.textContent = s[1];
      });
    } else {
      // No mapping for this path — at least hide template sections
      document.querySelectorAll('h1, h2, h3, p, span, div').forEach(function(el){
        if (el.children.length) return;
        var t = (el.textContent || '').trim();
        if (TEMPLATE_TEXTS.some(function(p){ return t.indexOf(p) >= 0; })) {
          var sec = el.closest('section, [data-framer-name]');
          if (sec) sec.style.setProperty('display', 'none', 'important');
        }
      });
    }
    // 3. Hide template placeholder images (lambo + sneaker)
    document.querySelectorAll('img, [data-framer-background-image-wrapper] img, picture img').forEach(function(img){
      var s = (img.getAttribute('src')||'') + ' ' + (img.getAttribute('srcset')||'') + ' ' + (img.getAttribute('alt')||'');
      if (/lambo|sneaker|shoe|automobile|yellow-car|nike|adidas/i.test(s)) {
        var hidden = img.closest('figure, picture, [data-framer-name="Image"]') || img;
        hidden.style.setProperty('display', 'none', 'important');
        hidden.setAttribute('data-glavnoe-hidden', 'template-image');
      }
    });
  }

  function run(){
    try { fixLinks(); } catch(e){}
    try { addAnchorIds(); } catch(e){}
    try { injectPricingNote(); } catch(e){}
    try { fixBlogCards(); } catch(e){}
    try { injectHomepageCases(); } catch(e){}
    try { patchTemplateBlocks(); } catch(e){}
    try { fixVisibleText(); } catch(e){}
    try { hideExtraBlogCards(); } catch(e){}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run, { once:true });
  } else {
    run();
  }
  window.addEventListener('load', function(){ setTimeout(run, 500); setTimeout(run, 1800); setTimeout(run, 4000); });
})();
