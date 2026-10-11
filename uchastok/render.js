// Рендер листов участка: PNG + общий PDF (А3)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const sheets = [['uchastok_list1', 1123, 1588, '297mm', '420mm'], ['uchastok_list2', 1588, 1123, '420mm', '297mm']];
  const pdfs = [];
  for (const [n, w, h, pw, ph] of sheets) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    await p.goto('file://' + dir + '/' + n + '.svg');
    await p.screenshot({ path: dir + '/' + n + '.png' });
    await p.pdf({ path: dir + '/' + n + '.pdf', width: pw, height: ph, printBackground: true, pageRanges: '1' });
    await p.close();
  }
  await b.close();
})();
