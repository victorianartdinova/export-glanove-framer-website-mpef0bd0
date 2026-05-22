(function(){
  if (window.__glavnoeTariffBulletsLoaded) return;
  window.__glavnoeTariffBulletsLoaded = true;

  // Avito-default bullets that hydrate into all product pages because of CMS template re-use.
  var AVITO_BULLETS = [
    'Управление кампаниями и бюджетом',
    'Разработка баннеров 3-5 шт/1 оффер',
    'Отчёты 4 раза/мес "план-факт"',
    'Cтратегия заявок до квалификации',
    'Разработка технического задания на посадочные',
    'Разработка посадочной страницы',
    'Настройка рекламы на канал, если посадочная не подошла',
    'гиперСегментация ЦА и подбор офферов'
  ];

  var BULLETS = {
    '/product/content-product/': [
      ['Аудит каналов и контента', 'Точки роста на 90 дней', 'План производства с метриками'],
      ['Полная контент-стратегия', 'Производство 12-20 единиц в месяц', 'Дистрибуция в каналах', 'Аналитика и оптимизация'],
      ['Всё из тарифа «Контент»', 'HR-бренд и корпоративный контент', 'Презентация компании', 'Лидген для найма']
    ],
    '/product/product-statii/': [
      ['Анализ каналов и креативов', 'Сегментация ЦА и аудит CPL', 'План на 90 дней с прогнозом'],
      ['Полный медиаплан с прогнозом продаж', 'Сегментация и офферы', 'KPI по неделям', 'Защита плана перед советом'],
      ['Всё из тарифа «Медиаплан»', 'Запуск всех каналов', 'Сквозная аналитика', 'Управление командой подрядчиков']
    ],
    '/product/product-telegram/': [
      ['Аудит контент-стратегии канала', 'Бенчмарки CPL и конкурентов', 'Запуск тестовой кампании'],
      ['Telegram Ads под ключ', '4 оффера, ~200 каналов для таргета', 'Управление бюджетом 80/20', 'Еженедельное обновление креативов'],
      ['Всё из тарифа «Запуск рекламы»', 'Контент-план канала', 'WhatsApp-бот + интеграция CRM', 'Полная воронка лидов']
    ],
    '/product/youtube-product/': [
      ['Упаковка канала и позиционирование', 'Сценарии первых 4 выпусков', 'Запуск производства'],
      ['Полное продюсирование канала', '8 выпусков за 3 месяца', 'SEO и аналитика', 'Монетизация и партнёрства']
    ]
  };

  function path(){ return window.location.pathname.replace(/index\.html$/, '').replace(/\/?$/, '/'); }

  function findTierCards(){
    var card1 = document.querySelector('.framer-17whp4j');
    if (!card1) return [];
    return Array.from(card1.children).filter(function(c){
      return c.offsetParent !== null || true;
    });
  }

  function replaceBulletsInCard(card, bullets){
    if (!card || !bullets || !bullets.length) return false;
    var lis = card.querySelectorAll('li');
    if (!lis.length) {
      lis = card.querySelectorAll('[data-framer-name="Feature"], [data-framer-name="Benefit"]');
    }
    if (!lis.length) {
      var hits = Array.from(card.querySelectorAll('p, span, div')).filter(function(el){
        if (el.children.length) return false;
        var t = (el.textContent || '').trim();
        return AVITO_BULLETS.indexOf(t) >= 0;
      });
      if (!hits.length) return false;
      hits.forEach(function(el, i){
        if (i < bullets.length) el.textContent = bullets[i];
        else el.textContent = '';
      });
      return true;
    }
    var idx = 0;
    lis.forEach(function(li){
      if (idx < bullets.length) {
        li.textContent = bullets[idx];
        li.style.opacity = '1';
        li.style.visibility = 'visible';
        idx++;
      }
    });
    return idx > 0;
  }

  function run(){
    var data = BULLETS[path()];
    if (!data) return;
    var cards = findTierCards();
    if (!cards.length) {
      // Fallback: scan top-level text nodes and replace any avito-default bullet
      var allFlat = Array.from(document.querySelectorAll('p, span, div, li')).filter(function(el){
        if (el.children.length) return false;
        var t = (el.textContent || '').trim();
        return AVITO_BULLETS.indexOf(t) >= 0;
      });
      // Split allFlat into 3 buckets per Tier by their order
      var allBullets = data.reduce(function(acc, arr){ return acc.concat(arr); }, []);
      var i = 0;
      allFlat.forEach(function(el){
        if (i < allBullets.length) { el.textContent = allBullets[i]; i++; }
        else el.textContent = '';
      });
      return;
    }
    var ordered = [];
    cards.forEach(function(c){ ordered.push(c); });
    ordered.forEach(function(card, idx){
      if (idx < data.length) replaceBulletsInCard(card, data[idx]);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run, { once:true });
  } else {
    run();
  }
  window.addEventListener('load', function(){ setTimeout(run, 1200); setTimeout(run, 3000); setTimeout(run, 6000); });
})();
