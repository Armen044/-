// posts/*.html -> PNG 1080×1350
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const jobs = require(__dirname + '/posts/jobs.json');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const [html, png] of jobs) {
    await p.goto('file://' + html);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(150);
    await p.screenshot({ path: png });
  }
  await b.close();
})();
