#!/usr/bin/env python3
"""Первые 9 постов Instagram (1080×1350): HTML-шаблоны -> PNG через render_posts.js. Тексты постов -> posts/podpisi.md."""
import json
import os

from gen import ARCH, ICONS, BG, FILL, STROKE, BRASS, TEXT

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, "logo", "fonts")
RENDER = os.path.join(ROOT, "rabochee_mesto", "render")
PHONE = "8 918 945-54-16"
DARK = "#3E3530"

CSS = f"""
@font-face{{font-family:Corm;src:url(file://{FONTS}/corm.ttf)}}
@font-face{{font-family:Mont;font-weight:400;src:url(file://{FONTS}/mont400.ttf)}}
@font-face{{font-family:Mont;font-weight:500;src:url(file://{FONTS}/mont500.ttf)}}
@font-face{{font-family:Mont;font-weight:600;src:url(file://{FONTS}/mont.ttf)}}
*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1350px;overflow:hidden;font-family:Mont;color:{TEXT};background:{BG}}}
.post{{width:1080px;height:1350px;position:relative;display:flex;flex-direction:column}}
.disp{{font-family:Corm;font-weight:500;line-height:1.02;letter-spacing:.5px}}
.cap{{font-weight:600;letter-spacing:.32em;text-transform:uppercase;font-size:22px}}
.brass{{color:{BRASS}}}
.foot{{position:absolute;left:80px;right:80px;bottom:64px;display:flex;justify-content:space-between;align-items:center;
  font-weight:500;font-size:26px;letter-spacing:.06em}}
.foot .rule{{flex:1;height:1px;background:{BRASS};margin:0 28px;opacity:.7}}
.photo{{position:absolute;inset:0;background-size:cover;background-position:center}}
.tag{{position:absolute;left:56px;bottom:56px;background:rgba(244,240,232,.92);color:{TEXT};border-radius:40px;
  padding:16px 30px;font-weight:600;font-size:22px;letter-spacing:.18em;text-transform:uppercase;display:flex;gap:14px;align-items:center}}
.tag svg{{width:30px;height:30px}}
"""


def mini_arch(w=30):
    return f'<svg viewBox="130 105 140 200" width="{w}">{ARCH}</svg>'


def icon(key, size=150, color=None):
    body = ICONS[key][1]
    return f'<svg viewBox="0 0 100 100" width="{size}" height="{size}">{body}</svg>'


def foot(left="RUSTAMYAN · МЕБЕЛЬ", right=PHONE):
    return f'<div class="foot"><span>{left}</span><span class="rule"></span><span>{right}</span></div>'


def photo_post(img, label, pos="center"):
    return (f'<div class="post"><div class="photo" style="background-image:url(file://{img});background-position:{pos}"></div>'
            f'<div class="tag">{mini_arch(26)}{label}</div></div>')


POSTS = []

# 1. Знакомство
POSTS.append(("01-znakomstvo", f'''<div class="post" style="background:{FILL};align-items:center;justify-content:center;gap:0">
<svg viewBox="130 105 140 200" width="300">{ARCH}</svg>
<div class="disp" style="font-size:118px;letter-spacing:22px;margin:70px 0 0 22px">RUSTAMYAN</div>
<div class="cap" style="font-size:30px;letter-spacing:.6em;margin:22px 0 0 .6em">Мебель</div>
<div style="width:120px;height:2px;background:{BRASS};margin:64px 0 54px"></div>
<div class="disp" style="font-size:58px;text-align:center">Мебель на заказ под ключ<br>для квартир и домов</div>
<div style="font-size:28px;margin-top:40px;letter-spacing:.08em">Краснодар и край · Москва · Ростов</div>
</div>'''))

# 2. Рендер: общий вид
POSTS.append(("02-detskaya-obshchiy", photo_post(f"{RENDER}/vid_obshchiy.jpg", "3D-проект · детская", "center 60%")))

# 3. Что мы делаем
cells = [("pod-klyuch", "Квартира под ключ"), ("kuhni", "Кухни"), ("shkafy", "Шкафы"),
         ("garderobnye", "Гардеробные"), ("detskie", "Детские"), ("3d", "3D-проект")]
grid = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:22px;background:{FILL};border-radius:28px;padding:40px 10px 34px">'
               f'{icon(k, 150)}<div style="font-weight:500;font-size:28px;text-align:center">{t}</div></div>' for k, t in cells)
POSTS.append(("03-chto-delaem", f'''<div class="post" style="padding:96px 80px 0">
<div class="cap brass">Что мы делаем</div>
<div class="disp" style="font-size:86px;margin-top:22px">Полная меблировка<br>квартир и домов</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:64px">{grid}</div>
{foot()}</div>'''))

# 4. Как мы работаем
steps = [("Замер", "Бесплатно приезжаем, обмеряем помещение, обсуждаем задачу"),
         ("3D-проект", "Показываем мебель в вашем интерьере до изготовления"),
         ("Договор", "Фиксируем материалы, цену и срок"),
         ("Производство", "Изготавливаем на своём производстве в Краснодаре"),
         ("Доставка и монтаж", "Привозим, собираем, даём гарантию")]
rows = "".join(f'<div style="display:flex;gap:34px;align-items:flex-start">'
               f'<div style="flex:none;width:74px;height:74px;border-radius:50%;border:2px solid {BRASS};display:grid;place-items:center;'
               f'font-family:Corm;font-size:42px;color:{BRASS}">{i}</div>'
               f'<div><div style="font-weight:600;font-size:36px">{t}</div><div style="font-size:27px;line-height:1.35;margin-top:6px;opacity:.85">{d}</div></div></div>'
               for i, (t, d) in enumerate(steps, 1))
POSTS.append(("04-kak-rabotaem", f'''<div class="post" style="padding:96px 80px 0;background:{FILL}">
<div class="cap brass">Как мы работаем</div>
<div class="disp" style="font-size:86px;margin-top:22px">От замера<br>до монтажа</div>
<div style="display:flex;flex-direction:column;gap:38px;margin-top:62px">{rows}</div>
{foot()}</div>'''))

# 5. Рендер: ниша
POSTS.append(("05-nisha-podsvetka", photo_post(f"{RENDER}/vid_nisha.jpg", "3D-проект · ниша с подсветкой", "35% center")))

# 6. Бесплатный замер
POSTS.append(("06-besplatnyy-zamer", f'''<div class="post" style="background:{DARK};color:{FILL};align-items:center;justify-content:center;text-align:center">
<svg viewBox="0 0 100 100" width="210" height="210">{ICONS["zamer"][1].replace(TEXT, FILL)}</svg>
<div class="cap" style="color:{BRASS};margin-top:56px">Краснодар и край · Москва · Ростов</div>
<div class="disp" style="font-size:130px;margin-top:30px">Бесплатный<br>замер</div>
<div style="font-size:32px;line-height:1.45;margin-top:40px;opacity:.9">Приедем, обмерим помещение<br>и обсудим будущую мебель</div>
<div style="margin-top:70px;border:2px solid {BRASS};border-radius:60px;padding:24px 56px;font-weight:600;font-size:44px;letter-spacing:.06em">{PHONE}</div>
<div style="font-size:26px;margin-top:22px;opacity:.75">звонок или WhatsApp</div>
</div>'''))

# 7. Рендер: открытые шкафы
POSTS.append(("07-detskaya-napolnenie", photo_post(f"{RENDER}/vid_otkryto.jpg", "3D-проект · наполнение", "center 45%")))

# 8. География
cities = [("Краснодар и край", "производство, замер, монтаж"), ("Ростов-на-Дону", "замер, доставка и монтаж"),
          ("Москва", "доставка и монтаж")]
pins = "".join(f'<div style="display:flex;gap:32px;align-items:center;padding:56px 0;border-top:1px solid rgba(94,82,68,.25)">'
               f'<svg viewBox="0 0 40 52" width="58"><path fill="{BRASS}" d="M20,0 C9,0 0,9 0,20 C0,35 20,52 20,52 C20,52 40,35 40,20 C40,9 31,0 20,0 Z"/>'
               f'<circle cx="20" cy="20" r="7" fill="{FILL}"/></svg>'
               f'<div><div class="disp" style="font-size:78px">{c}</div><div style="font-size:30px;margin-top:8px;opacity:.85">{d}</div></div></div>'
               for c, d in cities)
POSTS.append(("08-geografiya", f'''<div class="post" style="padding:96px 80px 0">
<div class="cap brass">Где мы работаем</div>
<div class="disp" style="font-size:86px;margin:22px 0 56px">Производство<br>в Краснодаре</div>
{pins}
{foot()}</div>'''))

# 9. Рендер: вид спереди (горизонтальный кадр -> по центру, сверху и снизу поля)
POSTS.append(("09-detskaya-speredi", f'''<div class="post" style="background:{FILL}">
<div style="padding:84px 80px 0"><div class="cap brass">3D-проект</div>
<div class="disp" style="font-size:78px;margin-top:18px">Рабочее место<br>в детской</div></div>
<div style="margin:54px 0 0;height:810px;background:url(file://{RENDER}/vid_speredi.jpg) center/cover"></div>
<div style="padding:34px 80px 0;font-size:27px;line-height:1.4">Антресоль до потолка · ниша с подсветкой · стол с тумбой</div>
</div>'''))

if __name__ == "__main__":
    out = os.path.join(HERE, "posts")
    os.makedirs(out, exist_ok=True)
    jobs = []
    for name, body in POSTS:
        p = os.path.join(out, name + ".html")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
        jobs.append([p, os.path.join(out, name + ".png")])
    with open(os.path.join(out, "jobs.json"), "w") as fh:
        json.dump(jobs, fh)
    print("ok", len(jobs))
