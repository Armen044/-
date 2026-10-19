#!/usr/bin/env python3
"""Посты 10–16 с фото последнего объекта: слайды 1080×1350 (карусели), тексты, страница-превью, архив."""
import base64
import html
import io
import json
import os
import subprocess
import zipfile

from PIL import Image

from gen import BG, FILL, BRASS, TEXT
from gen_posts import CSS, mini_arch, foot

HERE = os.path.dirname(os.path.abspath(__file__))
ED = os.path.join(HERE, "foto", "edit")
OUT = os.path.join(HERE, "posts", "obekt")
TAGS = "#мебельнаказ #мебелькраснодар #мебельподключ #неоклассика #дизайнинтерьера #rustamyan_mebel"
PHONE = "8 918 945-54-16"


def slide(photo):
    return (f'<div class="post"><div class="photo" style="background-image:url(file://{ED}/{photo}.jpg)"></div>'
            f'<div class="tag" style="left:44px;bottom:44px;padding:12px 22px;font-size:18px">{mini_arch(22)}Rustamyan</div></div>')


def tv_cover():
    return f'''<div class="post" style="background:{FILL}">
<div style="padding:84px 80px 0"><div class="cap brass">Квартира под ключ · последний объект</div>
<div class="disp" style="font-size:80px;margin-top:18px">Шкафы во всю стену<br>с ТВ-зоной</div></div>
<div style="margin-top:54px;height:810px;background:url(file://{ED}/foto-06.jpg) center/cover"></div>
<div style="padding:30px 80px 0;font-size:27px;line-height:1.4">Неоклассика · фасады с фрезеровкой · скрытая антресоль</div></div>'''


POSTS = [
    ("10-tv-stena", [tv_cover()], f"""Наш последний объект — квартира под ключ 🤍

Начнём со спальни: шкафы во всю стену с нишей под телевизор. Фасады в стиле неоклассики с фрезеровкой, антресоль до потолка, длинные чёрные ручки.

Всё хранение спрятано за фасадами — в комнате остаётся только спокойная ровная стена.

В следующих постах покажем остальные помещения этой квартиры 👉

Хотите так же? Бесплатный замер: 📞 {PHONE}

{TAGS} #шкафнаказ #шкафвспальню #твзона"""),
    ("11-sanuzel-zelenyy", [slide("foto-04"), slide("foto-09")], f"""Санузел в глубоком зелёном 💚

Шкафы-пеналы и панели до потолка, за фасадами спрятаны инсталляция и коммуникации. Зелёный в паре с латунной фурнитурой и чёрными карнизами — выглядит дорого и очень уютно.

Листайте карусель 👉

Мебель для санузла под ваши размеры: 📞 {PHONE}

{TAGS} #мебельдляванной #санузел #зелёныйинтерьер"""),
    ("12-detskaya", [slide("foto-01"), slide("foto-03")], f"""Детская: шкаф-пенал до потолка и встроенная ниша 🌿

Высокий шкаф с антресолью и полками-нишей в стене — вместительно и не перегружает комнату. Фасады в тон стен, молдинги продолжают отделку комнаты.

Листайте 👉 на втором фото — ниша крупно.

Проект для детской: 📞 {PHONE}

{TAGS} #детскаямебель #шкафвдетскую #ниша"""),
    ("13-shkaf-raspashnoy", [slide("foto-02")], f"""Распашной шкаф на три двери 🤍

Фасады с фрезеровкой, золотистые ручки, шкаф встроен в нишу от пола до потолка — без щелей и пыльных верхов.

Внутри наполнение под задачи владельцев: штанги, полки, ящики.

Рассчитать ваш шкаф: 📞 {PHONE}

{TAGS} #шкафнаказ #распашнойшкаф #встроенныйшкаф"""),
    ("14-prihozhaya-zhalyuzi", [slide("foto-10"), slide("foto-05")], f"""Прихожая с жалюзийными фасадами 🚪

Решётчатые фасады красиво смотрятся и пропускают воздух — одежда и обувь внутри проветриваются. Рядом открытая зона с крючками для того, что носите каждый день.

Листайте 👉

Мебель для прихожей: 📞 {PHONE}

{TAGS} #прихожая #шкафвприхожую #жалюзийныефасады"""),
    ("15-sanuzel-svetlyy", [slide("foto-08")], f"""Светлый санузел: панели и шкафы над инсталляцией 🤍

Коммуникации спрятаны за фасадами, сверху — шкафы для хранения. Фасады с фрезеровкой в стиле остальной квартиры.

Сохраняйте идею, пригодится при ремонте 📌

📞 {PHONE}

{TAGS} #мебельдляванной #санузел #инсталляция"""),
    ("16-zerkalo", [slide("foto-07")], f"""Зеркало в прихожей 🪞

Большое зеркало в чёрной раме на стене с молдингами и бра по бокам. Визуально расширяет прихожую и замыкает образ квартиры.

Делаем не только шкафы — продумываем все детали интерьера.

📞 {PHONE}

{TAGS} #зеркало #прихожая #интерьерквартиры"""),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = []
    for name, slides, _ in POSTS:
        for i, body in enumerate(slides, 1):
            p = os.path.join(OUT, f"{name}-{i}.html")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
            jobs.append([p, p.replace(".html", ".png")])
    with open(os.path.join(HERE, "posts", "jobs.json"), "w") as fh:
        json.dump(jobs, fh)
    subprocess.run(["node", os.path.join(HERE, "render_posts.js")], check=True)
    for j in jobs:
        os.remove(j[0])

    def thumb(path):
        im = Image.open(path).convert("RGB").resize((540, 675))
        b = io.BytesIO()
        im.save(b, "JPEG", quality=80)
        return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

    cards = ""
    for n, (name, slides, cap) in enumerate(POSTS, 10):
        imgs = "".join(f'<img src="{thumb(os.path.join(OUT, f"{name}-{i}.png"))}" alt="">' for i in range(1, len(slides) + 1))
        kind = f"карусель, {len(slides)} фото" if len(slides) > 1 else "1 фото"
        cards += (f'<article><div class="shots">{imgs}</div><div class="txt"><div class="n">Пост {n} · {kind}</div>'
                  f'<pre id="c{n}">{html.escape(cap)}</pre><button type="button" data-t="c{n}">Скопировать текст</button></div></article>')
    page = open(os.path.join(HERE, "instagram-posty.html"), encoding="utf-8").read()
    head = page.split("<div class=\"wrap\">")[0].replace("<title>Instagram: первые 9 постов</title>", "<title>Instagram: посты с объекта</title>")
    head = head.replace("</style>", ".shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:6px}.shots img{width:100%;border-radius:6px}</style>")
    body = (f'<div class="wrap"><header><h1>Instagram: посты 10–16 с объекта</h1>'
            '<p>Фото последнего объекта обработаны (свет, контраст, резкость) и обрезаны под 4:5. Посты с несколькими фото публикуйте каруселью: при создании поста нажмите «Выбрать несколько» и отметьте фото по порядку номеров.</p></header>'
            f'<section class="list"><h2>Посты по порядку публикации</h2>{cards}</section></div>')
    script = "<script>" + page.split("<script>")[1]
    with open(os.path.join(HERE, "instagram-posty-obekt.html"), "w", encoding="utf-8") as fh:
        fh.write(head + body + script)
    with open(os.path.join(OUT, "podpisi.md"), "w", encoding="utf-8") as fh:
        fh.write("# Посты 10–16 с объекта\n\n")
        for n, (name, slides, cap) in enumerate(POSTS, 10):
            fh.write(f"## {n}. {', '.join(f'{name}-{i}.png' for i in range(1, len(slides) + 1))}\n\n```\n{cap}\n```\n\n")
    with zipfile.ZipFile(os.path.join(HERE, "instagram-posty-10-16-obekt.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(OUT)):
            z.write(os.path.join(OUT, f), f)
    print("ok", len(jobs))
