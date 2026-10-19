#!/usr/bin/env python3
"""Страница-макет профиля Instagram: аватарка, шапка, кружки «Актуального»."""
import base64
import os

from gen import ICONS, BG, BRASS, TEXT

HERE = os.path.dirname(os.path.abspath(__file__))
EX = os.path.join(HERE, "export")


def uri(name):
    with open(os.path.join(EX, name), "rb") as fh:
        return "data:image/svg+xml;base64," + base64.b64encode(fh.read()).decode()


BIO = ["Мебель под ключ", "Полная меблировка квартир и домов",
       "Краснодар и край · Москва · Ростов", "Бесплатный замер · 3D-проект · гарантия",
       "📞 8 918 945-54-16"]
hl = "".join(f'<div class="hl"><img src="{uri(f"aktualnoe-{i:02d}-{k}.svg")}" alt=""><span>{t}</span></div>'
             for i, (k, (t, _)) in enumerate(ICONS.items(), 1))
av = "".join(f'<figure><img class="av" src="{uri(n)}" alt=""><figcaption>{c}</figcaption></figure>'
             for n, c in (("avatar-svetlaya.svg", "1. Светлая (основная)"), ("avatar-s-latunnym-kolcom.svg", "2. С латунным кольцом"),
                          ("avatar-temnaya.svg", "3. Тёмная")))
page = f'''<title>Instagram Rustamyan Мебель</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Montserrat:wght@400;500;600&display=swap">
<style>
/* макет профиля в рамке телефона + варианты аватарки + текст шапки для копирования */
:root{{--page:#F8F6F2;--ink:#2A2420;--muted:#6F6862;--line:#E2DAD0;--card:#FFFFFF;--accent:{BRASS};
  --f-disp:"Cormorant Garamond","Times New Roman",serif;--f-sans:"Montserrat","Segoe UI",Arial,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--page:#1A1715;--ink:#EDE6DE;--muted:#A79E95;--line:#3A332E;--card:#24201D;color-scheme:dark}}}}
:root[data-theme="dark"]{{--page:#1A1715;--ink:#EDE6DE;--muted:#A79E95;--line:#3A332E;--card:#24201D;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--page);color:var(--ink);font:15px/1.5 var(--f-sans);padding-inline:16px;padding-block:28px 48px}}
.wrap{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:minmax(0,400px) minmax(0,1fr);gap:40px;align-items:start}}
@media (max-width:820px){{.wrap{{grid-template-columns:1fr}}}}
h1{{font:600 clamp(28px,4vw,42px)/1.1 var(--f-disp);margin:0 0 6px}}
h2{{font:600 15px var(--f-sans);margin:0;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
p{{margin:0;max-width:62ch}}
.phone{{background:#fff;color:#111;border-radius:28px;border:1px solid var(--line);padding:20px 16px 24px;box-shadow:0 10px 40px rgba(60,40,20,.12);font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif}}
.top{{display:flex;align-items:center;gap:18px}}
.top img{{width:86px;height:86px;border-radius:50%;flex:none;border:1px solid #e6e6e6}}
.stats{{display:flex;gap:16px;text-align:center;font-size:13px;flex:1;justify-content:space-around}}
.stats b{{display:block;font-size:16px}}
.nick{{font-weight:700;font-size:14px;margin-top:12px}}
.name{{font-weight:600;font-size:14px}}
.cat{{color:#737373;font-size:13px}}
.bio{{font-size:14px;line-height:1.4;white-space:pre-line}}
.btns{{display:flex;gap:6px;margin-top:12px}}
.btns span{{flex:1;background:#efefef;border-radius:8px;text-align:center;font-weight:600;font-size:13px;padding:7px 0}}
.hls{{display:flex;gap:14px;overflow-x:auto;margin-top:16px;padding-bottom:4px}}
.hl{{display:flex;flex-direction:column;align-items:center;gap:5px;flex:none;width:64px}}
.hl img{{width:64px;height:64px;border-radius:50%;object-fit:cover;border:1px solid #dbdbdb;padding:2px;background:#fff}}
.hl span{{font-size:11.5px;color:#111;text-align:center;line-height:1.2}}
.side{{display:flex;flex-direction:column;gap:28px;min-width:0}}
.avs{{display:flex;flex-wrap:wrap;gap:20px}}
.avs figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:8px}}
.av{{width:120px;height:120px;border-radius:50%;border:1px solid var(--line)}}
.avs figcaption{{font-size:13px;color:var(--muted)}}
.copy{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:flex;flex-direction:column;gap:10px}}
.copy pre{{margin:0;font:14px/1.5 var(--f-sans);white-space:pre-wrap}}
.copy button{{align-self:flex-start;font:600 13px var(--f-sans);background:var(--accent);color:#fff;border:0;border-radius:6px;padding:7px 12px;cursor:pointer}}
.copy button:focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}
.note{{font-size:13.5px;color:var(--muted)}}
ul{{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px}}
</style>
<div class="wrap">
<div class="phone" aria-label="Макет профиля Instagram">
  <div class="top"><img src="{uri("avatar-svetlaya.svg")}" alt="Аватарка">
    <div class="stats"><div><b>9</b>публикаций</div><div><b>0</b>подписчиков</div><div><b>0</b>подписок</div></div></div>
  <div class="nick">rustamyan.mebel</div>
  <div class="name">Мебель на заказ Краснодар · RUSTAMYAN</div>
  <div class="cat">Мебель</div>
  <div class="bio">{chr(10).join(BIO)}</div>
  <div class="btns"><span>Позвонить</span><span>WhatsApp</span><span>Сообщение</span></div>
  <div class="hls">{hl}</div>
</div>
<div class="side">
  <div><h1>Instagram: аватарка и «Актуальное»</h1>
  <p>Слева показано, как будет выглядеть профиль. Аватарка и 9 обложек выполнены в цветах логотипа «Молочный и латунь». Обложки сделаны в размере сторис 1080 × 1920, значок стоит по центру и целиком попадает в кружок.</p></div>
  <div><h2>Аватарка: 3 варианта</h2><div class="avs" style="margin-top:12px">{av}</div>
  <p class="note" style="margin-top:8px">Советую первую: она светлая, как и логотип. Текста на аватарке нет, в маленьком кружке он всё равно не читается.</p></div>
  <div><h2>Поле «Имя» (по нему ищут)</h2><div class="copy" style="margin-top:10px"><pre id="nm">Мебель на заказ Краснодар · RUSTAMYAN</pre><button type="button" data-t="nm">Скопировать</button></div></div>
  <div><h2>Описание профиля</h2><div class="copy" style="margin-top:10px"><pre id="bio">{chr(10).join(BIO)}</pre><button type="button" data-t="bio">Скопировать</button></div>
  <p class="note" style="margin-top:8px">Длина {len(chr(10).join(BIO))} символов из 150 допустимых. Номер также укажите в кнопках «Позвонить» и «WhatsApp»: Редактировать профиль → Способы связи.</p></div>
  <div><h2>Как поставить обложки</h2><ul class="note" style="margin-top:10px">
    <li>Сначала выложите в сторис хотя бы одно фото по теме, например фото кухни. Сторис можно сразу удалить, потом оно останется в архиве.</li>
    <li>Откройте профиль, нажмите «+ Новое» под описанием, выберите сторис и введите название, например «Кухни».</li>
    <li>Нажмите «Редактировать обложку», выберите картинку из галереи и поставьте её по центру.</li></ul></div>
</div>
</div>
<script>
document.querySelectorAll('.copy button').forEach(b=>b.addEventListener('click',()=>{{
  const el=document.getElementById(b.dataset.t), t=el.textContent;
  navigator.clipboard.writeText(t).then(()=>{{b.textContent='Скопировано'}}).catch(()=>{{
    const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Выделено, нажмите «Копировать»'}});
}}));
</script>
'''
with open(os.path.join(HERE, "instagram-profil.html"), "w", encoding="utf-8") as fh:
    fh.write(page)
print("ok", len(chr(10).join(BIO)))
