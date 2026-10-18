// SVG -> PNG (прозрачный и на кремовом фоне) + PDF (вектор) для логотипов в export/
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, 'export');
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  for (const f of fs.readdirSync(dir).filter(n => n.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const [, , w, h] = svg.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number);
    const base = path.join(dir, f.replace('.svg', ''));
    const light = f.includes('svetlyy');
    const W = 3000, H = Math.round(W * h / w);
    const page = bg => `<html><body style="margin:0;background:${bg}">` +
      svg.replace('<svg ', `<svg style="display:block" width="${W}" height="${H}" `) + '</body></html>';
    await p.setViewportSize({ width: W, height: H });
    await p.setContent(page('transparent'));
    await p.screenshot({ path: base + '.png', omitBackground: true });
    await p.setContent(page(light ? '#2E2620' : '#F3ECE2'));
    await p.screenshot({ path: base + (light ? '-na-temnom' : '-na-kremovom') + '.png' });
    if (!light) {                                     // PDF: логотип 150 мм по ширине, поля 15 мм
      const wm = 150, hm = wm * h / w;
      await p.setContent(`<html><body style="margin:0">` +
        svg.replace('<svg ', `<svg style="display:block;margin:15mm" width="${wm}mm" height="${hm}mm" `) + '</body></html>');
      await p.pdf({ path: base + '.pdf', width: (wm + 30) + 'mm', height: (hm + 30) + 'mm', printBackground: false, pageRanges: '1' });
    }
  }
  await b.close();
})();
