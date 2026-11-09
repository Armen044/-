#!/usr/bin/env python3
"""Коммерческое предложение: позиции с двумя вариантами, итог по вариантам."""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = [  # (название, описание, фото, [(вариант 1, цена)], [(вариант 2, цена)])
    ("Шкаф в прихожую", "", None,
     [("Фасады ЛДСП", 340000)], [("Фасады шпон", 556000)]),
    ("Кухня с островом", "без столешницы", "kuhnya_c.jpg",
     [("ЛДСП и фрезерованная эмаль", 715000)], [("Шпон и фрезерованная эмаль", 985000)]),
    ("ТВ-тумба", "", None,
     [("ЛДСП, максимальная длина 2750 мм", 85000)], [("Эмаль, длина 3 м (как на чертеже)", 148000)]),
    ("Спальня гостевая: стеновые панели и шкаф", "", "spalnya_c.jpg",
     [("Шкаф ЛДСП", 155000), ("Стеновые панели ЛДСП", 54000)],
     [("Шкаф эмаль", 235000), ("Стеновые панели шпон", 125000)]),
    ("Гардеробная", "как на визуализации, с подсветкой, без остекления", "garderob_c.jpg",
     [("Гардеробная", 380000)], [("Гардеробная", 380000)]),
    ("Санузел", "тумба под раковину (без столешницы), шкаф под стиральную и сушильную машину, инсоляция",
     "sanuzel_c.jpg", [("ЛДСП и эмаль", 255000)], [("Шпон и эмаль", 320000)]),
]


def rub(v):
    return f"{v:,}".replace(",", " ") + " ₽"


def img(name):
    data = base64.b64encode(open(os.path.join(HERE, name), "rb").read()).decode()
    return f'<img src="data:image/jpeg;base64,{data}">'


def variant(title, rows):
    lines = "".join(f'<div class="row"><span>{n}</span><b>{rub(p)}</b></div>' for n, p in rows)
    total = sum(p for _, p in rows)
    tot = f'<div class="row sum"><span>Итого</span><b>{rub(total)}</b></div>' if len(rows) > 1 else ""
    return f'<div class="var"><div class="vt">{title}</div>{lines}{tot}</div>'


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'DejaVu Sans', Arial, sans-serif; color: #2b2622; }
.page { width: 210mm; height: 297mm; padding: 14mm 14mm 12mm; page-break-after: always; position: relative; }
.page:last-child { page-break-after: auto; }
.head { border-bottom: 0.5mm solid #2b2622; padding-bottom: 4mm; margin-bottom: 6mm; display: flex;
        justify-content: space-between; align-items: flex-end; }
.head h1 { margin: 0; font-size: 20pt; letter-spacing: 0.5pt; }
.head .sub { font-size: 10pt; color: #6f655c; margin-top: 1.5mm; }
.badge { background: #2b2622; color: #fff; padding: 2.5mm 4mm; font-size: 10pt; font-weight: 700; text-align: right;
         line-height: 1.5; }
.item { margin-bottom: 7mm; break-inside: avoid; }
.item h2 { font-size: 13pt; margin: 0 0 1mm; }
.item .desc { font-size: 9pt; color: #6f655c; margin-bottom: 2.5mm; }
.body { display: flex; gap: 5mm; align-items: stretch; }
.photo { width: 72mm; flex: none; }
.photo img { width: 100%; height: 52mm; object-fit: cover; display: block; border-radius: 1.5mm; }
.vars { flex: 1; min-width: 0; display: flex; gap: 3mm; }
.var { flex: 1; min-width: 0; border: 0.3mm solid #cfc6bb; border-radius: 1.5mm; padding: 3mm 3.5mm; background: #faf8f5; }
.vt { font-size: 9pt; font-weight: 700; color: #8a6a3f; text-transform: uppercase; margin-bottom: 2mm; }
.row { display: flex; justify-content: space-between; gap: 2mm; font-size: 9pt; padding: 1.2mm 0;
       border-bottom: 0.2mm solid #e6dfd6; }
.row b { white-space: nowrap; }
.row.sum { border-bottom: none; font-weight: 700; }
.totals { margin-top: 8mm; border-top: 0.5mm solid #2b2622; padding-top: 5mm; }
.totals h2 { font-size: 14pt; margin: 0 0 4mm; }
.tt { display: flex; gap: 6mm; }
.tc { flex: 1; background: #2b2622; color: #fff; border-radius: 1.5mm; padding: 5mm; }
.tc .l { font-size: 10pt; opacity: 0.8; }
.tc .v { font-size: 22pt; font-weight: 700; margin-top: 2mm; }
.tc .m { font-size: 8.5pt; opacity: 0.75; margin-top: 2mm; line-height: 1.4; }
table { width: 100%; border-collapse: collapse; font-size: 9.5pt; margin-bottom: 5mm; }
th, td { border-bottom: 0.2mm solid #d9d1c7; padding: 1.8mm 2mm; text-align: left; }
td.n, th.n { text-align: right; white-space: nowrap; }
th { font-size: 8.5pt; color: #6f655c; text-transform: uppercase; }
.note { font-size: 8.5pt; color: #6f655c; margin-top: 4mm; line-height: 1.5; }
"""


def head(n, total):
    return (f'<div class="head"><div><h1>КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ</h1>'
            f'<div class="sub">Мебель по индивидуальному проекту · лист {n} из {total}</div></div>'
            f'<div class="badge">ЛДСП Egger<br>Фурнитура Blum<br><span style="font-weight:400;font-size:8.5pt">во всех вариантах</span></div></div>')


def item_html(name, desc, photo, v1, v2):
    ph = f'<div class="photo">{img(photo)}</div>' if photo else ""
    d = f'<div class="desc">{desc}</div>' if desc else '<div class="desc">&nbsp;</div>'
    return (f'<div class="item"><h2>{name}</h2>{d}<div class="body">{ph}'
            f'<div class="vars">{variant("Вариант 1", v1)}{variant("Вариант 2", v2)}</div></div></div>')


def main():
    t1 = sum(p for it in ITEMS for _, p in it[3])
    t2 = sum(p for it in ITEMS for _, p in it[4])
    rows = "".join(f'<tr><td>{n}</td><td class="n">{rub(sum(p for _, p in a))}</td>'
                   f'<td class="n">{rub(sum(p for _, p in b))}</td></tr>' for n, _, _, a, b in ITEMS)
    pages_items = [ITEMS[:3], ITEMS[3:]]
    total_pages = 3
    pages = []
    for k, chunk in enumerate(pages_items):
        pages.append(f'<div class="page">{head(k + 1, total_pages)}'
                     + "".join(item_html(*it) for it in chunk) + '</div>')
    summary = (f'<div class="page">{head(3, total_pages)}<div class="totals" style="border:none;margin:0;padding:0">'
               f'<h2>Сводная стоимость</h2>'
               f'<table><tr><th>Позиция</th><th class="n">Вариант 1</th><th class="n">Вариант 2</th></tr>{rows}'
               f'<tr><td><b>ИТОГО</b></td><td class="n"><b>{rub(t1)}</b></td><td class="n"><b>{rub(t2)}</b></td></tr></table>'
               f'<div class="tt"><div class="tc"><div class="l">Общая стоимость — вариант 1</div><div class="v">{rub(t1)}</div>'
               f'<div class="m">ЛДСП Egger, фурнитура Blum; фасады ЛДСП / ЛДСП и эмаль</div></div>'
               f'<div class="tc"><div class="l">Общая стоимость — вариант 2</div><div class="v">{rub(t2)}</div>'
               f'<div class="m">ЛДСП Egger, фурнитура Blum; фасады шпон / эмаль / шпон и эмаль</div></div></div>'
               f'<div class="note">Столешницы, бытовая техника, сантехника и остекление в стоимость не входят. '
               f'Гардеробная в обоих вариантах — по визуализации, с подсветкой, без остекления. '
               f'Окончательная стоимость — после замера и согласования проекта.</div></div></div>')
    pages.append(summary)
    html = (f"<!doctype html><html lang='ru'><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body>{''.join(pages)}</body></html>")
    open(os.path.join(HERE, "_kp.html"), "w", encoding="utf-8").write(html)
    print(t1, t2)


if __name__ == "__main__":
    main()
