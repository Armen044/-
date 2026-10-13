// HTML деталировки → PDF (А3, вектор) + PNG первых страниц для проверки
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = __dirname, out = process.argv[2] || dir;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1588, height: 1123 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + dir + '/detal.html');
  await p.pdf({ path: dir + '/Деталировка_и_фурнитура.pdf', preferCSSPageSize: true, printBackground: true });
  await b.close();
})();
