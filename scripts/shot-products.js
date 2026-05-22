const puppeteer = require('/root/archplay-report/node_modules/puppeteer');
const fs = require('fs');
const path = require('path');

const BASE = 'http://localhost:3343';
const PAGES = ['avito-ads', 'content-product', 'product-statii', 'product-telegram', 'youtube-product'];
const VPS = [
  { name: 'mobile', w: 390, h: 844, dpr: 2, isMobile: true },
  { name: 'tablet', w: 810, h: 1080, dpr: 2, isMobile: false },
  { name: 'desktop', w: 1440, h: 900, dpr: 1, isMobile: false }
];
const OUT = '/root/framerexport/full-site-export-may21/docs/shots-2026-05-22';

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await puppeteer.launch({
    executablePath: '/root/.cache/puppeteer/chrome/linux-146.0.7680.153/chrome-linux64/chrome',
    args: ['--no-sandbox']
  });
  for (const slug of PAGES) {
    for (const v of VPS) {
      const p = await b.newPage();
      await p.setViewport({ width: v.w, height: v.h, deviceScaleFactor: v.dpr, isMobile: v.isMobile });
      const url = `${BASE}/product/${slug}/`;
      try {
        await p.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
      } catch (e) {
        console.log(`TIMEOUT ${slug} ${v.name}: ${e.message}`);
      }
      await new Promise(r => setTimeout(r, 1200));
      const out = path.join(OUT, `${slug}-${v.name}.png`);
      await p.screenshot({ path: out, fullPage: true });
      console.log(`OK ${slug}-${v.name}`);
      await p.close();
    }
  }
  await b.close();
  console.log('DONE');
})().catch(e => { console.error(e); process.exit(1); });
