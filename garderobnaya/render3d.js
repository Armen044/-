const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 2400, height: 1700 } });
  p.on('console', m => console.log('console:', m.text()));
  p.on('pageerror', e => console.log('err:', e.message));
  for (const v of ['front', 'axo']) {
    await p.goto('file://' + dir + '/view3d.html?view=' + v);
    await p.waitForFunction('window.DONE === true', null, { timeout: 120000 });
    await (await p.$('canvas')).screenshot({ path: dir + '/3d_' + v + '.png' });
  }
  await b.close();
})();
