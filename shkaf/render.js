// Рендер листа шкафа: PNG + PDF (А3)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1588, height: 1123 }, deviceScaleFactor: 2.5 });
  await p.goto('file://' + dir + '/shkaf.svg');
  await p.screenshot({ path: dir + '/shkaf.png' });
  await p.pdf({ path: dir + '/shkaf.pdf', width: '420mm', height: '297mm', printBackground: true, pageRanges: '1' });
  await b.close();
})();
