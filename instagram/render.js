// SVG из export/ -> PNG того же размера (1080×1080 аватарки, 1080×1920 обложки)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, 'export');
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  for (const f of fs.readdirSync(dir).filter(n => n.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const [w, h] = svg.match(/viewBox="0 0 (\d+) (\d+)"/).slice(1).map(Number);
    await p.setViewportSize({ width: w, height: h });
    await p.setContent(`<html><body style="margin:0">${svg.replace('<svg ', '<svg style="display:block" ')}</body></html>`);
    await p.screenshot({ path: path.join(dir, f.replace('.svg', '.png')) });
  }
  await b.close();
})();
