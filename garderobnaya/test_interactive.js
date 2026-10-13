// Проверка интерактивной модели: скриншоты в разных состояниях
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = __dirname, out = process.argv[2] || dir;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + dir + '/garderobnaya_3d.html');
  await p.waitForTimeout(2500);
  await p.screenshot({ path: out + '/i1.png' });
  await p.click('#bDrawers'); await p.click('#bRack'); await p.click('#bRack'); await p.click('#bMirror'); await p.click('#bBoard');
  await p.waitForTimeout(2500);
  await p.screenshot({ path: out + '/i2.png' });
  await p.click('#bMirror'); await p.click('#bTop');
  await p.waitForTimeout(2500);
  await p.screenshot({ path: out + '/i3.png' });
  // поворот мышью
  await p.mouse.move(700, 450); await p.mouse.down(); await p.mouse.move(500, 420, { steps: 10 }); await p.mouse.up();
  await p.waitForTimeout(800);
  await p.screenshot({ path: out + '/i4.png' });
  console.log('errors:', JSON.stringify(errs));
  await b.close();
})();
