// Рендер листов: PNG каждого листа + общий PDF (2 листа А2)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const dir = __dirname;
  const sheets = ['garderobnaya3'];
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 2245, height: 1588 }, deviceScaleFactor: 2 });
  for (const s of sheets) {
    await p.goto('file://' + dir + '/' + s + '.svg');
    await p.screenshot({ path: dir + '/' + s + '.png' });
  }
  const html = '<html><head><style>@page{size:594mm 420mm;margin:0}body{margin:0}' +
    'img{display:block;width:594mm;height:420mm;page-break-after:always}</style></head><body>' +
    sheets.map(s => `<img src="${s}.svg">`).join('') + '</body></html>';
  fs.writeFileSync(dir + '/_print.html', html);
  await p.goto('file://' + dir + '/_print.html');
  await p.pdf({ path: dir + '/garderobnaya3.pdf', width: '594mm', height: '420mm', printBackground: true });
  fs.unlinkSync(dir + '/_print.html');
  await b.close();
})();
