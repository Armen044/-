// Рендер листа шкафа: PNG + PDF (А3)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 2245, height: 1588 }, deviceScaleFactor: 2 });
  await p.goto('file://' + dir + '/kuhnya.svg');
  await p.screenshot({ path: dir + '/kuhnya.png' });
  await p.pdf({ path: dir + '/kuhnya.pdf', width: '594mm', height: '420mm', printBackground: true, pageRanges: '1' });
  await b.close();
})();
