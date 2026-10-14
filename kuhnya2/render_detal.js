// HTML деталировки и фурнитуры → два PDF (А3, вектор) + PNG страниц для проверки
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = __dirname, out = process.argv[2] || dir;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1588, height: 1123 } });
  for (const [src, pdf] of [['_detal.html', 'Кухня_деталировка.pdf'], ['_hw.html', 'Кухня_фурнитура.pdf']]) {
    await p.goto('file://' + dir + '/' + src);
    await p.pdf({ path: dir + '/' + pdf, preferCSSPageSize: true, printBackground: true });
  }
  await b.close();
})();
