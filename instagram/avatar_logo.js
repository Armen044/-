// Аватарка: логотип 1 (знак + RUSTAMYAN / МЕБЕЛЬ) целиком внутри круга, белый фон, 1080×1080
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const svg = fs.readFileSync(path.join(__dirname, '..', 'logo', 'export', 'rustamyan-mebel-1-arka-shkaf.svg'), 'utf8');
  const [, , w, h] = svg.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number);
  const H = Math.round(1130 / Math.hypot(w / h, 1)), W = Math.round(H * w / h);   // углы рамки логотипа на окружности r=490
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1080 } });
  const page = (circle) => `<html><body style="margin:0;background:#fff;width:1080px;height:1080px;display:grid;place-items:center;position:relative">` +
    svg.replace('<svg ', `<svg style="display:block" width="${W}" height="${H}" `) +
    (circle ? '<div style="position:absolute;inset:0;border-radius:50%;box-shadow:0 0 0 2000px rgba(0,0,0,.35)"></div>' : '') + '</body></html>';
  await p.setContent(page(false)); await p.screenshot({ path: path.join(__dirname, 'export', 'avatar-logo-belyy.png') });
  await p.setContent(page(true)); await p.screenshot({ path: '/tmp/claude-0/-home-user--/3ec63d47-11eb-57c2-b5f1-6698a94cf5fc/scratchpad/avatar-krug.png' });
  await b.close(); console.log(W, H);
})();
