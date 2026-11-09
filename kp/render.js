const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome' });
  const p = await b.newPage();
  await p.goto('file://' + dir + '/_kp.html');
  await p.pdf({ path: dir + '/Коммерческое_предложение.pdf', preferCSSPageSize: true, printBackground: true });
  await b.close();
})();
