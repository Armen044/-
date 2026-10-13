const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/rustamyan_logo1_mebel.svg');
  await p.pdf({ path: __dirname + '/rustamyan_logo1_mebel.pdf', width: '297mm', height: '210mm', printBackground: true, pageRanges: '1' });
  await p.screenshot({ path: __dirname + '/rustamyan_logo1_mebel.png' });
  await b.close();
})();
