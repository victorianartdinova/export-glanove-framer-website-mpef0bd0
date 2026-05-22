const puppeteer = require('/root/archplay-report/node_modules/puppeteer');
const fs = require('fs');
const path = require('path');

const BASE = 'http://localhost:3343';
const PAGES = ['content-product', 'product-statii', 'product-telegram', 'youtube-product'];
const OUT = '/root/framerexport/full-site-export-may21/docs/shots-2026-05-22/recheck';

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await puppeteer.launch({
    executablePath: '/root/.cache/puppeteer/chrome/linux-146.0.7680.153/chrome-linux64/chrome',
    args: ['--no-sandbox']
  });
  for (const slug of PAGES) {
    const p = await b.newPage();
    await p.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
    const url = `${BASE}/product/${slug}/`;
    await p.goto(url, { waitUntil: 'load', timeout: 30000 });
    await new Promise(r => setTimeout(r, 5000));
    // Count tier cards
    const tierCount = await p.evaluate(() => {
      const c = document.querySelectorAll('.framer-17whp4j > *');
      return c.length;
    });
    const clones = await p.evaluate(() => document.querySelectorAll('[data-glavnoe-tier-clone="1"]').length);
    console.log(`${slug}: tiers=${tierCount} clones=${clones}`);
    await p.screenshot({ path: path.join(OUT, `${slug}-desktop.png`), fullPage: true });
    await p.close();
  }
  await b.close();
  console.log('DONE');
})().catch(e => { console.error(e); process.exit(1); });
