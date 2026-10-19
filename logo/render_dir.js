// node render_dir.js <папка> <цвет фона>: каждый SVG -> PNG прозрачный, PNG на фоне, PDF (вектор)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.resolve(process.argv[2]), bg = process.argv[3] || '#FFFFFF';
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  for (const f of fs.readdirSync(dir).filter(n => n.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const [, , w, h] = svg.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number);
    const base = path.join(dir, f.replace('.svg', ''));
    const W = 3000, H = Math.round(W * h / w);
    const page = c => `<html><body style="margin:0;background:${c}">` +
      svg.replace('<svg ', `<svg style="display:block" width="${W}" height="${H}" `) + '</body></html>';
    await p.setViewportSize({ width: W, height: H });
    await p.setContent(page('transparent'));
    await p.screenshot({ path: base + '.png', omitBackground: true });
    await p.setContent(page(bg));
    await p.screenshot({ path: base + '-na-fone.png' });
    const wm = 150, hm = wm * h / w;
    await p.setContent(`<html><body style="margin:0">` +
      svg.replace('<svg ', `<svg style="display:block;margin:15mm" width="${wm}mm" height="${hm}mm" `) + '</body></html>');
    await p.pdf({ path: base + '.pdf', width: (wm + 30) + 'mm', height: (hm + 30) + 'mm', pageRanges: '1' });
  }
  await b.close();
})();
