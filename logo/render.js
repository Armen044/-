const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1700, height: 1310 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + __dirname + '/rustamyan_logos.svg');
  await p.screenshot({ path: __dirname + '/rustamyan_logos.png' });
  await b.close();
})();
