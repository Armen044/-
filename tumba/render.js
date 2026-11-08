// Листы SVG (А2) → PDF + PNG; HTML деталировки и фурнитуры (А3) → PDF; затем склейка
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 2245, height: 1588 }, deviceScaleFactor: 2 });
  for (const s of ['sheet1', 'sheet2']) {
    await p.goto('file://' + dir + '/' + s + '.svg');
    await p.screenshot({ path: dir + '/' + s + '.png' });
    fs.writeFileSync(dir + '/_p.html', '<html><head><style>@page{size:594mm 420mm;margin:0}body{margin:0}' +
      `img{display:block;width:594mm;height:420mm}</style></head><body><img src="${s}.svg"></body></html>`);
    await p.goto('file://' + dir + '/_p.html');
    await p.pdf({ path: dir + '/_' + s + '.pdf', width: '594mm', height: '420mm', printBackground: true });
  }
  fs.unlinkSync(dir + '/_p.html');
  for (const s of ['_detal', '_hw']) {
    if (!fs.existsSync(dir + '/' + s + '.html')) continue;
    await p.goto('file://' + dir + '/' + s + '.html');
    await p.pdf({ path: dir + '/' + s + '.pdf', preferCSSPageSize: true, printBackground: true });
  }
  await b.close();
})();
