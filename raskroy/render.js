const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome' });
  const p = await b.newPage({ viewport: { width: 1588, height: 1123 }, deviceScaleFactor: 2 });
  for (const s of ['sheet1']) {
    await p.goto('file://' + dir + '/' + s + '.svg');
    await p.screenshot({ path: dir + '/' + s + '.png' });
  }
  fs.writeFileSync(dir + '/_p.html', '<html><head><style>@page{size:420mm 297mm;margin:0}body{margin:0}' +
    'img{display:block;width:420mm;height:297mm;page-break-after:always}</style></head><body>' +
    '<img src="sheet1.svg"></body></html>');
  await p.goto('file://' + dir + '/_p.html');
  await p.pdf({ path: dir + '/Раскрой_ЛДСП.pdf', width: '420mm', height: '297mm', printBackground: true });
  fs.unlinkSync(dir + '/_p.html');
  await b.close();
})();
