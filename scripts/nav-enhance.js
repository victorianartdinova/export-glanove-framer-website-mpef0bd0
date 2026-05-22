(function(){// Burger menu drawer — Framer exported only "Moblie Closed" variant.
  // The hamburger icon exists but click does nothing. Wire a real drawer.
  // ─────────────────────────────────────────────────────────────────────
  var BURGER_NAV = [
    { label: 'Главная',     href: '/' },
    { label: 'Услуги',      href: '/#products', kids: [
        { label: 'Авито Адс',                  href: '/product/avito-ads/' },
        { label: 'Коммуникационная стратегия', href: '/product/content-product/' },
        { label: 'ПромоСтраницы Яндекс',       href: '/product/product-statii/' },
        { label: 'Лидген Телеграм',            href: '/product/product-telegram/' },
        { label: 'Личный бренд YouTube',       href: '/product/youtube-product/' }
    ]},
    { label: 'Кейсы',       href: '/cases/portfolio/' },
    { label: 'Блог',        href: '/blog/' },
    { label: 'О нас',       href: '/about/' },
    { label: 'Связаться',   href: '/contact/' }
  ];

  function ensureBurgerStyles(){
    if (document.getElementById('glavnoe-burger-style')) return;
    var s = document.createElement('style');
    s.id = 'glavnoe-burger-style';
    s.textContent = ''
      + '#glavnoe-burger-drawer{position:fixed;inset:0;z-index:99999;display:none;font-family:"Suisse Intl Regular","Inter",system-ui,sans-serif}'
      + '#glavnoe-burger-drawer.open{display:block}'
      + '#glavnoe-burger-drawer .gbd-backdrop{position:absolute;inset:0;background:rgba(0,0,0,0.6);backdrop-filter:blur(4px)}'
      + '#glavnoe-burger-drawer .gbd-panel{position:absolute;top:0;right:0;bottom:0;width:min(86vw,360px);background:#0a0a0a;color:#fff;padding:24px 22px 32px;overflow-y:auto;box-shadow:-20px 0 50px rgba(0,0,0,0.5);transform:translateX(100%);transition:transform .28s ease}'
      + '#glavnoe-burger-drawer.open .gbd-panel{transform:translateX(0)}'
      + '#glavnoe-burger-drawer .gbd-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:32px}'
      + '#glavnoe-burger-drawer .gbd-brand{font-family:"Suisse Intl SemiBold","Inter",sans-serif;font-weight:700;font-size:18px;letter-spacing:-0.01em;color:#fff;text-decoration:none}'
      + '#glavnoe-burger-drawer .gbd-close{background:none;border:0;color:#fff;font-size:30px;line-height:1;cursor:pointer;padding:4px 8px}'
      + '#glavnoe-burger-drawer ul{list-style:none;margin:0;padding:0}'
      + '#glavnoe-burger-drawer li{border-top:1px solid rgba(255,255,255,0.08)}'
      + '#glavnoe-burger-drawer li:last-child{border-bottom:1px solid rgba(255,255,255,0.08)}'
      + '#glavnoe-burger-drawer .gbd-link{display:flex;justify-content:space-between;align-items:center;padding:18px 4px;color:#fff;text-decoration:none;font-size:17px;letter-spacing:-0.01em}'
      + '#glavnoe-burger-drawer .gbd-link:hover,#glavnoe-burger-drawer .gbd-link:focus{color:#ff3b30}'
      + '#glavnoe-burger-drawer .gbd-toggle{background:none;border:0;color:rgba(255,255,255,0.6);font-size:22px;line-height:1;padding:6px 10px;cursor:pointer;transition:transform .2s}'
      + '#glavnoe-burger-drawer .gbd-sub{display:none;padding:0 0 14px 12px}'
      + '#glavnoe-burger-drawer .gbd-sub.open{display:block}'
      + '#glavnoe-burger-drawer .gbd-sub a{display:block;padding:10px 4px;font-size:14px;color:rgba(255,255,255,0.7);text-decoration:none}'
      + '#glavnoe-burger-drawer .gbd-sub a:hover{color:#ff3b30}'
      + '#glavnoe-burger-drawer .gbd-foot{margin-top:32px;font-size:13px;color:rgba(255,255,255,0.4);line-height:1.6}'
      + '#glavnoe-burger-drawer .gbd-foot a{color:rgba(255,255,255,0.7);text-decoration:none}'
      + '#glavnoe-burger-drawer .gbd-cta{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:22px;padding:14px 18px;background:#ff3b30;color:#fff;border-radius:48px;text-decoration:none;font-family:"Suisse Intl SemiBold","Inter",sans-serif;font-weight:600;font-size:14px;letter-spacing:0.02em;text-transform:uppercase}'
      + '@media (min-width:1024px){#glavnoe-burger-drawer{display:none !important}}'
      ;
    document.head.appendChild(s);
  }

  function buildBurgerDrawer(){
    if (document.getElementById('glavnoe-burger-drawer')) return;
    ensureBurgerStyles();
    var d = document.createElement('div');
    d.id = 'glavnoe-burger-drawer';
    d.setAttribute('aria-hidden', 'true');
    var lis = BURGER_NAV.map(function(item, i){
      if (item.kids) {
        var subs = item.kids.map(function(k){
          return '<a class="gbd-sublink" href="'+k.href+'">'+k.label+'</a>';
        }).join('');
        return ''
          + '<li>'
          + '  <div style="display:flex;align-items:center;justify-content:space-between">'
          + '    <a class="gbd-link" href="'+item.href+'" style="flex:1">'+item.label+'</a>'
          + '    <button class="gbd-toggle" type="button" data-gbd-toggle="'+i+'" aria-label="Открыть подменю">+</button>'
          + '  </div>'
          + '  <div class="gbd-sub" data-gbd-sub="'+i+'">'+subs+'</div>'
          + '</li>';
      }
      return '<li><a class="gbd-link" href="'+item.href+'">'+item.label+'</a></li>';
    }).join('');
    d.innerHTML = ''
      + '<div class="gbd-backdrop" data-gbd-close="1"></div>'
      + '<aside class="gbd-panel" role="dialog" aria-label="Меню">'
      + '  <div class="gbd-head">'
      + '    <a class="gbd-brand" href="/">ГЛАВНОЕ</a>'
      + '    <button class="gbd-close" type="button" data-gbd-close="1" aria-label="Закрыть">×</button>'
      + '  </div>'
      + '  <ul>'+lis+'</ul>'
      + '  <a class="gbd-cta" href="/contact/">Старт проекта →</a>'
      + '  <div class="gbd-foot">'
      + '    <div><a href="mailto:hello@glavnoe.com">hello@glavnoe.com</a></div>'
      + '    <div><a href="https://t.me/glavnoe_channel" target="_blank" rel="noopener">Telegram</a> · <a href="https://www.instagram.com/glavnoe_agency" target="_blank" rel="noopener">Instagram</a></div>'
      + '    <div style="margin-top:10px">© 2026 ГЛАВНОЕ</div>'
      + '  </div>'
      + '</aside>';
    document.body.appendChild(d);
    d.addEventListener('click', function(e){
      var t = e.target;
      if (t.getAttribute && t.getAttribute('data-gbd-close')) { closeBurger(); return; }
      var tg = t.getAttribute && t.getAttribute('data-gbd-toggle');
      if (tg !== null && tg !== undefined) {
        var sub = d.querySelector('[data-gbd-sub="'+tg+'"]');
        if (sub) {
          sub.classList.toggle('open');
          t.textContent = sub.classList.contains('open') ? '−' : '+';
        }
        e.preventDefault();
      }
    });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') closeBurger(); });
  }

  function openBurger(){
    buildBurgerDrawer();
    var d = document.getElementById('glavnoe-burger-drawer');
    if (!d) return;
    d.classList.add('open');
    d.setAttribute('aria-hidden', 'false');
    document.documentElement.style.overflow = 'hidden';
  }
  function closeBurger(){
    var d = document.getElementById('glavnoe-burger-drawer');
    if (!d) return;
    d.classList.remove('open');
    d.setAttribute('aria-hidden', 'true');
    document.documentElement.style.overflow = '';
  }

  function wireBurger(){
    if (window.__glavnoeBurgerWired) return;
    // Wire Framer's existing hamburger icon
    var icon = document.querySelector('[data-framer-name="Mobile Menu Icon"]');
    if (!icon) return;
    window.__glavnoeBurgerWired = true;
    icon.style.cursor = 'pointer';
    icon.setAttribute('role', 'button');
    icon.setAttribute('aria-label', 'Меню');
    icon.addEventListener('click', function(e){
      e.preventDefault();
      e.stopPropagation();
      openBurger();
    }, true);
    // Also wire any parent button container if Framer renders one
    var p = icon.parentElement;
    if (p && p.tagName === 'BUTTON') {
      p.addEventListener('click', function(e){ e.preventDefault(); e.stopPropagation(); openBurger(); }, true);
    }
  }

  // ─────────────────────────────────────────────────────────────────────
  // Enrich slim static footers on about/contact/portfolio/blog index.
  // Framer Footer is missing on these pages — only a <footer class="footer">
  // line exists. Add Glavnoe brand block + sitemap above the slim line.
  // ─────────────────────────────────────────────────────────────────────
  function enrichSlimFooter(){
    if (document.querySelector('[data-glavnoe-rich-footer]')) return;
    var existing = document.querySelector('footer.footer');
    if (!existing) return;
    // Don't enrich if Framer Footer is also on this page
    if (document.querySelector('[data-framer-name="Footer"]')) return;

    var rich = document.createElement('div');
    rich.setAttribute('data-glavnoe-rich-footer', '1');
    rich.style.cssText = 'background:#0a0a0a;color:#fff;padding:64px 24px 32px;border-top:1px solid rgba(255,255,255,0.08)';
    rich.innerHTML = ''
      + '<div style="max-width:1280px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:32px">'
      + '  <div>'
      + '    <div style="font-family:\'Suisse Intl SemiBold\',\'Inter\',sans-serif;font-weight:700;font-size:22px;letter-spacing:-0.02em;margin-bottom:12px">ГЛАВНОЕ</div>'
      + '    <div style="font-size:14px;line-height:1.6;color:rgba(255,255,255,0.6)">Performance-агентство в нише недвижимости. Системный маркетинг и измеримые заявки.</div>'
      + '  </div>'
      + '  <div>'
      + '    <div style="font-size:13px;letter-spacing:0.06em;text-transform:uppercase;color:rgba(255,255,255,0.4);margin-bottom:14px">Карта сайта</div>'
      + '    <div style="display:flex;flex-direction:column;gap:8px;font-size:15px">'
      + '      <a href="/" style="color:#fff;text-decoration:none">Главная</a>'
      + '      <a href="/#products" style="color:#fff;text-decoration:none">Услуги</a>'
      + '      <a href="/cases/portfolio/" style="color:#fff;text-decoration:none">Кейсы</a>'
      + '      <a href="/blog/" style="color:#fff;text-decoration:none">Блог</a>'
      + '      <a href="/about/" style="color:#fff;text-decoration:none">О нас</a>'
      + '      <a href="/contact/" style="color:#fff;text-decoration:none">Связаться</a>'
      + '    </div>'
      + '  </div>'
      + '  <div>'
      + '    <div style="font-size:13px;letter-spacing:0.06em;text-transform:uppercase;color:rgba(255,255,255,0.4);margin-bottom:14px">На связи</div>'
      + '    <div style="display:flex;flex-direction:column;gap:8px;font-size:15px">'
      + '      <a href="mailto:hello@glavnoe.com" style="color:#fff;text-decoration:none">hello@glavnoe.com</a>'
      + '      <a href="https://t.me/glavnoe_channel" target="_blank" rel="noopener" style="color:#fff;text-decoration:none">Telegram</a>'
      + '      <a href="https://www.instagram.com/glavnoe_agency" target="_blank" rel="noopener" style="color:#fff;text-decoration:none">Instagram</a>'
      + '    </div>'
      + '  </div>'
      + '</div>';
    existing.parentNode.insertBefore(rich, existing);
    // Hide redundant duplicate links in the slim footer below — keep just copyright
    var slimLinks = existing.querySelector('.nav__items');
    if (slimLinks) slimLinks.style.display = 'none';
    existing.style.background = '#0a0a0a';
    existing.style.borderTop = 'none';
  }

  // ─────────────────────────────────────────────────────────────────────
  // Services section max-width on home — at viewports ≥1440 the inner
  // "Top" container fills width-24px-padding and feels edge-bound.
  // Constrain it to 1280px with auto margins.
  // ─────────────────────────────────────────────────────────────────────
  function ensureServicesMaxWidth(){
    if (document.getElementById('glavnoe-services-maxw')) return;
    var s = document.createElement('style');
    s.id = 'glavnoe-services-maxw';
    s.textContent = ''
      + '@media (min-width:1440px){'
      + '  section[data-framer-name="Services"] > [data-framer-name="Top"]{'
      + '    max-width:1280px !important;margin-left:auto !important;margin-right:auto !important;'
      + '  }'
      + '  section[data-framer-name="Archive"] > .framer-rmlqiv-container,'
      + '  section[data-framer-name="Archive"] > div:not([data-framer-name]):first-child{'
      + '    max-width:1280px !important;margin-left:auto !important;margin-right:auto !important;'
      + '  }'
      + '}'
      ;
    document.head.appendChild(s);
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
    try { ensureServicesMaxWidth(); } catch(e){}
    try { wireBurger(); } catch(e){}
    try { enrichSlimFooter(); } catch(e){}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run, { once:true });
  } else {
    run();
  }
  window.addEventListener('load', function(){ setTimeout(run, 500); setTimeout(run, 1800); setTimeout(run, 4000); });
})();
})();