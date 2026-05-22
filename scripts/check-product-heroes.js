/**
 * Headless проверка: для каждой /product/<slug>/ страницы поднимаем браузер,
 * ждём отрисовку и читаем текст первого видимого <h2>/<h1> в hero-секции.
 *
 * Запуск: node scripts/check-product-heroes.js
 */
const { chromium } = require('/root/node_modules/playwright');

const BASE = 'http://localhost:3343';
const TARGETS = {
  'avito-ads':        'Авито Адс',
  'content-product':  'Коммуникационная стратегия',
  'product-statii':   'ПромоСтраницы Яндекс',
  'product-telegram': 'Лидген Телеграм',
  'youtube-product':  'Личный бренд YouTube',
};

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  let fail = 0;

  for (const [slug, expected] of Object.entries(TARGETS)) {
    const url = `${BASE}/product/${slug}/`;
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    // Чуть подождать пока REPLACEMENTS отработает (DOMContentLoaded callback)
    await page.waitForTimeout(800);
    const title = await page.title();
    // ищем самый крупный заголовок продукта — внутри hero-секции это, как правило, h2 / h1
    const heroText = await page.evaluate(() => {
      const cands = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5'));
      // эвристика: самый крупный шрифт первого экрана
      let best = null;
      let bestSize = 0;
      for (const el of cands) {
        const r = el.getBoundingClientRect();
        if (r.top < 0 || r.top > 1500) continue;
        const fs = parseFloat(getComputedStyle(el).fontSize) || 0;
        if (fs > bestSize && el.textContent.trim().length > 0) {
          bestSize = fs;
          best = el;
        }
      }
      return best ? best.textContent.trim() : null;
    });
    const okTitle = title.startsWith(expected + ' |');
    const okHero  = heroText === expected;
    console.log(
      `${(okTitle && okHero) ? 'OK  ' : 'FAIL'}  /${slug}/` +
      `   title="${title}"` +
      `   hero=${JSON.stringify(heroText)}` +
      `   expected="${expected}"`,
    );
    if (!okTitle || !okHero) fail++;
  }

  await browser.close();
  process.exit(fail ? 1 : 0);
})();
