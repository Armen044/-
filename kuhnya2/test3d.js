const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = __dirname, out = process.argv[2] || dir;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + dir + '/kuhnya2_3d.html');
  await p.waitForTimeout(3000);
  await p.screenshot({ path: out + '/g1.png' });
  await p.click('#b_doors'); await p.click('#b_drawers'); await p.click('#b_tech');
  await p.waitForTimeout(2500);
  await p.screenshot({ path: out + '/g2.png' });
  await p.click('text=Вид с угла');
  await p.waitForTimeout(2500);
  await p.screenshot({ path: out + '/g3.png' });
  await p.click('text=Вид сверху');
  await p.waitForTimeout(2500);
  await p.screenshot({ path: out + '/g4.png' });
  console.log('errors:', JSON.stringify(errs));
  await b.close();
})();
