// Листы каркаса: PNG + общий PDF (А3)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { execFileSync } = require('child_process');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1588, height: 1123 }, deviceScaleFactor: 2 });
  const pdfs = [];
  for (const n of ['stol_list1', 'stol_list2']) {
    await p.goto('file://' + dir + '/' + n + '.svg');
    await p.screenshot({ path: dir + '/' + n + '.png' });
    await p.pdf({ path: dir + '/' + n + '.pdf', width: '420mm', height: '297mm', printBackground: true, pageRanges: '1' });
    pdfs.push(dir + '/' + n + '.pdf');
  }
  await b.close();
  execFileSync('pdfunite', [...pdfs, dir + '/stol_shlif.pdf']);
  for (const f of pdfs) require('fs').unlinkSync(f);
})();
