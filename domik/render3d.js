// Статичные 3D-кадры каркаса для листа 2
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 2000, height: 1400 } });
  p.on('pageerror', e => console.log('err:', e.message));
  for (const v of ['sw', 'ne']) {
    await p.goto('file://' + __dirname + '/view3d.html?view=' + v);
    await p.waitForFunction('window.DONE === true', null, { timeout: 120000 });
    await (await p.$('canvas')).screenshot({ path: __dirname + '/3d_' + v + '.png' });
  }
  await b.close();
})();
