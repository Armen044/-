// Рендер листа рабочего места: PNG + PDF (А3)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1588, height: 1123 }, deviceScaleFactor: 2.5 });
  await p.goto('file://' + dir + '/rabochee_mesto.svg');
  await p.screenshot({ path: dir + '/rabochee_mesto.png' });
  await p.pdf({ path: dir + '/rabochee_mesto.pdf', width: '420mm', height: '297mm', printBackground: true, pageRanges: '1' });
  await b.close();
})();
