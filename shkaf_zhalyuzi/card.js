// Финальная заставка ролика 1080×1920: логотип, подпись, телефон
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const F = path.join(__dirname, '..', 'logo', 'fonts');
  const svg = fs.readFileSync(path.join(__dirname, '..', 'logo', 'export', 'rustamyan-mebel-1-arka-shkaf.svg'), 'utf8')
    .replace('<svg ', '<svg style="display:block" width="680" ');
  const html = `<html><head><style>
@font-face{font-family:Mont;font-weight:500;src:url(file://${F}/mont500.ttf)}
@font-face{font-family:Mont;font-weight:600;src:url(file://${F}/mont.ttf)}
body{margin:0;width:1080px;height:1920px;background:#fff;color:#3A2F27;font-family:Mont;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0}
.t{font-weight:500;font-size:44px;margin-top:90px;letter-spacing:.02em}
.p{font-weight:600;font-size:62px;margin-top:46px;letter-spacing:.04em;border:3px solid #3A2F27;border-radius:80px;padding:22px 60px}
.s{font-weight:500;font-size:34px;margin-top:26px;opacity:.7}
</style></head><body>${svg}
<div class="t">Мебель на заказ под ключ</div><div class="p">8 918 945-54-16</div><div class="s">замер бесплатно · звонок или WhatsApp</div></body></html>`;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const f = path.join(__dirname, 'card.html'); fs.writeFileSync(f, html); await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(__dirname, 'card.png') });
  await b.close(); fs.unlinkSync(f);
})();
