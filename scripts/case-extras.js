(function(){
  if (window.__glavnoeCaseExtrasLoaded) return;
  window.__glavnoeCaseExtrasLoaded = true;

  function path(){
    return window.location.pathname.replace(/index\.html$/, '').replace(/\/?$/, '/');
  }

  var EXTRA_CASES = {
    '/work/regardis-telegram-ads-premium/': {
      product_url: '/product/product-telegram/',
      product_label: 'Лидген Telegram',
      metrics: [
        ['9 684 ₽', 'CPL квал. лида (KPI — 10 000 ₽)'],
        ['50+', 'Квалифицированных лидов в месяц'],
        ['20 млн ₽', 'Средний чек обращения'],
        ['310 ₽', 'CPM кампании (рынок ~855 ₽)']
      ],
      did: [
        'Концепция бренд-медиа в Telegram: ежедневные инвестиционные кейсы и аналитика рынка',
        'Подготовка канала: УТП, WhatsApp-бот + AmoCRM, контент-стратегия, фирменный стиль',
        'Запуск баннеров Telegram Ads с минимальным бюджетом 1 млн ₽/мес и таргетингом на финансовые/инвестиционные каналы',
        '12 креативов на старте, обновление еженедельно — выгорают за 7 дней',
        'Дневной лимит 25 000 ₽, недельный 700 000 ₽, ограничения в выходные'
      ],
      why: [
        'Бренд-медиа собрало аудиторию с реальным интересом к премиум-недвижимости — не риелторов, а покупателей',
        'Канал работает как актив: обращения приходят даже при остановленной рекламе',
        'Накопленная лояльность снизила CPL ещё на 30% в следующем месяце'
      ]
    }
  };

  var PUBLICATIONS = {
    '/work/case-spb-15mln/': {
      label: 'Опубликовано на PPC World',
      href: 'https://ppc.world/articles/kak-s-reklamoy-v-telegram-zakryt-6-sdelok-so-srednim-chekom-v-15-mln-rubley-keys-agentstva-nedvizhimosti/'
    }
  };

  function injectCaseBody(p){
    var data = EXTRA_CASES[p];
    if (!data) return;
    if (document.querySelector('[data-glavnoe-injected="case-body"]')) return;
    var more = document.querySelector('[data-framer-name="More Works"]')
            || document.querySelector('[data-framer-name="Footer"]')
            || document.querySelector('footer');
    if (!more || !more.parentNode) return;
    var sec = document.createElement('section');
    sec.setAttribute('data-glavnoe-injected', 'case-body');
    sec.style.cssText = 'background:rgb(0,0,0);padding:96px 24px 120px 24px;color:#fff';
    var M = data.metrics.map(function(m){
      return '<div style="flex:1 1 0;min-width:160px;padding:24px 0;border-top:1px solid rgba(255,255,255,0.15)"><div style="font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:48px;line-height:1;letter-spacing:-1.5px;color:#fff;margin-bottom:8px">'+m[0]+'</div><div style="font-family:\'Suisse Intl Regular\',sans-serif;font-size:14px;line-height:1.4;color:rgba(255,255,255,0.55)">'+m[1]+'</div></div>';
    }).join('');
    var D = data.did.map(function(x){ return '<li style="margin:0 0 12px 0;font-family:\'Suisse Intl Regular\',sans-serif;font-size:18px;line-height:1.5;color:rgba(255,255,255,0.85)">'+x+'</li>'; }).join('');
    var W = data.why.map(function(x){ return '<li style="margin:0 0 12px 0;font-family:\'Suisse Intl Regular\',sans-serif;font-size:18px;line-height:1.5;color:rgba(255,255,255,0.85)">'+x+'</li>'; }).join('');
    sec.innerHTML = '<div style="max-width:1392px;margin:0 auto">'
      + '<div style="display:flex;flex-wrap:wrap;gap:32px;margin-bottom:80px">'+M+'</div>'
      + '<div style="display:flex;flex-wrap:wrap;gap:64px;margin-bottom:64px">'
      +   '<div style="flex:1 1 380px"><div style="font-family:\'Suisse Intl Regular\',sans-serif;font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:24px">(Что делали)</div><ul style="list-style:disc;padding-left:24px;margin:0">'+D+'</ul></div>'
      +   '<div style="flex:1 1 380px"><div style="font-family:\'Suisse Intl Regular\',sans-serif;font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:24px">(Почему сработало)</div><ul style="list-style:disc;padding-left:24px;margin:0">'+W+'</ul></div>'
      + '</div>'
      + '<div style="padding-top:32px;border-top:1px solid rgba(255,255,255,0.15);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px">'
      +   '<div><div style="font-family:\'Suisse Intl Regular\',sans-serif;font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:8px">Доказывает продукт</div><div style="font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:28px;color:#fff">'+data.product_label+'</div></div>'
      +   '<a href="'+data.product_url+'" style="display:inline-flex;align-items:center;gap:12px;padding:18px 32px;background:#ff3b30;color:#fff;text-decoration:none;border-radius:48px;font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:16px;letter-spacing:0.02em;text-transform:uppercase">Узнать о продукте →</a>'
      + '</div></div>';
    more.parentNode.insertBefore(sec, more);
  }

  function injectPublicationLink(p){
    var pub = PUBLICATIONS[p];
    if (!pub) return;
    if (document.querySelector('[data-glavnoe-injected="publication"]')) return;
    var anchor = document.querySelector('[data-glavnoe-injected="case-body"]')
              || document.querySelector('[data-framer-name="More Works"]')
              || document.querySelector('footer');
    if (!anchor || !anchor.parentNode) return;
    var bar = document.createElement('section');
    bar.setAttribute('data-glavnoe-injected', 'publication');
    bar.style.cssText = 'background:#0a0a0a;padding:48px 24px;color:#fff;border-top:1px solid rgba(255,255,255,0.12);text-align:center';
    bar.innerHTML = '<div style="max-width:760px;margin:0 auto"><div style="font-family:\'Suisse Intl Regular\',sans-serif;font-size:14px;color:rgba(255,255,255,0.4);letter-spacing:0.06em;text-transform:uppercase;margin-bottom:12px">Публикация</div><div style="font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:28px;line-height:1.2;letter-spacing:-0.02em;margin-bottom:24px">'+pub.label+'</div><a href="'+pub.href+'" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:12px;padding:16px 28px;background:transparent;color:#fff;border:1px solid rgba(255,255,255,0.3);border-radius:48px;text-decoration:none;font-family:\'Suisse Intl SemiBold\',sans-serif;font-size:14px;letter-spacing:0.04em;text-transform:uppercase">Открыть статью →</a></div>';
    anchor.parentNode.insertBefore(bar, anchor.nextSibling);
  }

  var TEMPLATE_PHRASES = [
    'Industries → our designs have supported businesses, adapting to unique needs and challenges',
    'our designs have supported businesses, adapting to unique needs and challenges',
    'Industries → our designs',
    'adapting to unique needs and challenges',
    'отношение к результатам'
  ];

  function hideTemplateIndustries(){
    var marker = null;
    var walker = document.querySelectorAll('p, h2, h3, h4, span, div');
    for (var i = 0; i < walker.length; i++) {
      var el = walker[i];
      if (el.children.length) continue;
      var t = (el.textContent || '').trim();
      if (!t) continue;
      var match = TEMPLATE_PHRASES.some(function(phrase){
        return t === phrase || t.indexOf(phrase) >= 0;
      });
      if (match) {
        var sec = el.closest('section, [data-framer-name]');
        if (sec) {
          sec.style.setProperty('display', 'none', 'important');
          sec.setAttribute('data-glavnoe-hidden', 'industries-template');
        } else {
          el.style.setProperty('display', 'none', 'important');
        }
      }
    }
  }

  function run(){
    var p = path();
    try { injectCaseBody(p); } catch(e){}
    try { injectPublicationLink(p); } catch(e){}
    try { hideTemplateIndustries(); } catch(e){}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run, { once:true });
  } else {
    run();
  }
  window.addEventListener('load', function(){ setTimeout(run, 800); setTimeout(run, 2200); });
})();
