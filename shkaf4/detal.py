#!/usr/bin/env python3
"""Деталировка шкафа с антресолью и тумбой (по распилу заказчика + добавленные позиции) и фурнитура."""
import importlib.util
import os
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("db", os.path.join(HERE, "..", "detal", "build.py"))
db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db)
from geom import *          # noqa: E402,F403

L16, FC = "ЛДСП 16", "Фасад 20"


class P(db.Item):
    def __init__(self, pos, name, mat, L, Wd, qty, edge="----", note="", added=False):
        super().__init__(name, mat, L, Wd, qty, edge, note)
        self.posname, self.added = pos, added


GROOVE = "паз 16 × 8 под LED, 100 от лица (по внутр. грани)"


def parts():
    out = []
    m = "Модуль 1 — нижний правый, 2 штанги (1100 × 1930 × 560)"
    out += [P(m, "Боковина", L16, 1914, 560, 2, "2---", GROOVE),
            P(m, "Крыша", L16, 1100, 560, 1, "2---", "2 отв. под датчики открывания"),
            P(m, "Дно / полка", L16, 1068, 560, 2, "2---", "полка: 1598 от низа (300 до крыши)"),
            P(m, "Задняя стенка", L16, 1930, 1100, 1, "----", "накладная")]
    m = "Модуль 2 — нижний левый, ящики + полки (1100 × 1930 × 560)"
    out += [P(m, "Боковина", L16, 1914, 560, 1, "2---", GROOVE),
            P(m, "Боковина левая (до лица фасадов)", L16, 1914, 580, 1, "2---", GROOVE + "; видимая над тумбой"),
            P(m, "Крыша", L16, 1100, 560, 1, "2---", "2 отв. под датчики открывания"),
            P(m, "Дно / полки", L16, 1068, 560, 3, "2---", "полки: 1207 и 1598 от низа"),
            P(m, "Полка над ящиками", L16, 1068, 490, 1, "2---", "816 от низа, утоплена"),
            P(m, "Утолщение: панель", L16, 800, 480, 2, "2---", "на планках, отступ 80 от лица"),
            P(m, "Утолщение: планка", L16, 800, 80, 4, "----", "16 + 16 по бокам ящиков"),
            P(m, "Ящик: боковина", L16, 440, 130, 8, "2---"),
            P(m, "Ящик: перед / зад", L16, 994, 101, 8, "2---"),
            P(m, "Ящик: дно", L16, 994, 440, 4, "----"),
            P(m, "Ящик: фасад внутренний", L16, 998, 165, 4, "2222", "щель под пальцы 35"),
            P(m, "Задняя стенка", L16, 1930, 1084, 1, "----", "накладная")]
    m = "Антресоли — 2 модуля (1100 × 630 × 560)"
    out += [P(m, "Боковина", L16, 630, 560, 3, "2---", GROOVE),
            P(m, "Боковина левая (до лица фасадов)", L16, 630, 580, 1, "2---", GROOVE),
            P(m, "Крыша / дно", L16, 1068, 560, 4, "2---", "в днищах — по 2 отв. под датчики"),
            P(m, "Задняя стенка", L16, 1100, 630, 1, "----", "накладная"),
            P(m, "Задняя стенка", L16, 1084, 630, 1, "----", "накладная")]
    m = "Тумба (1568 × 580 × 420)"
    out += [P(m, "Перед / зад", L16, 1568, 404, 2, "2---"),
            P(m, "Бок", L16, 548, 404, 2, "----"),
            P(m, "Дно", L16, 1568, 580, 1, "2222")]
    m = "Дополнительно (добавлено)"
    out += [P(m, "Фальш-панель правая, на всю высоту", L16, H_ALL, DEPTH, 1, "2-2-", "в цвет фасадов/корпуса", True),
            P(m, "Фальш-панель левая (у тумбы)", L16, LEGS + TUMBA_H + FAC, TUMBA_D + FAC, 1, "2-2-", "", True)]
    m = "Фасады 20 (зазор 3)"
    out += [P(m, "Фасад нижний Ф1 (петли вкладные)", FC, DOOR_LOW_H, DOOR_W[0], 1, "----", "петли: " + ", ".join(map(str, HINGE_LOW)), True),
            P(m, "Фасад нижний Ф2", FC, DOOR_LOW_H, DOOR_W[1], 1, "----", "петли: " + ", ".join(map(str, HINGE_LOW)), True),
            P(m, "Фасад нижний Ф3, Ф4", FC, DOOR_LOW_H, DOOR_W[2], 2, "----", "петли: " + ", ".join(map(str, HINGE_LOW)), True),
            P(m, "Фасад антресоли А1 (петли вкладные)", FC, DOOR_ANT_H, DOOR_W[0], 1, "----", "петли: 100, 529", True),
            P(m, "Фасад антресоли А2", FC, DOOR_ANT_H, DOOR_W[1], 1, "----", "петли: 100, 529", True),
            P(m, "Фасад антресоли А3, А4", FC, DOOR_ANT_H, DOOR_W[2], 2, "----", "петли: 100, 529", True),
            P(m, "Крышка тумбы (фасад, вверх)", FC, LID[0], LID[1], 1, "----", "3 петли сзади + 2 газлифта", True),
            P(m, "Фальш-фасад тумбы", FC, FALSE_FRONT[0], FALSE_FRONT[1], 1, "----", "зазор 3 до крышки", True)]
    return out


def hardware():
    led_m1, led_m2, led_a = 1914 - T, 1914 - SH_DRW - T, H_ANT - 2 * T
    total = 2 * led_m1 + 2 * led_m2 + 4 * led_a
    return OrderedDict([
        ("Петли (с доводчиком)", [
            ("Петля накладная 110° с доводчиком", 21, "Ф2–Ф4 по 5, А2–А4 по 2"),
            ("Петля вкладная 110° с доводчиком", 7, "Ф1 — 5, А1 — 2 (левая боковина выступает)"),
            ("Монтажная планка", 28, ""),
            ("Петля для крышки тумбы (мебельная, откидная)", 3, "крышка 1562 × 600"),
            ("Газлифт / подъёмник крышки", 2, "подобрать по весу крышки"),
        ]),
        ("Ящики и наполнение", [
            ("Направляющие шариковые полного выдвижения, пара", 4, "под коробку 440 (L 400–450 по каталогу)"),
            ("Штанга овальная, L 1066", 2, "модуль 1, оси 1538 и 800 от низа"),
            ("Штангодержатель", 4, ""),
        ]),
        ("Подсветка", [
            (f"Профиль алюм. врезной 16 + рассеиватель, всего {total / 1000:.1f} м", 1,
             f"модуль 1: 2 × {led_m1}; модуль 2: 2 × {led_m2}; антресоли: 4 × {led_a}"),
            ("Лента LED 24 В, м", round(total / 1000 * 1.1 + 0.5), "с запасом 10 %"),
            ("Датчик открывания двери (на подсветку)", 8, "на каждый фасад: крыша нижних модулей, дно антресолей"),
            ("Блок питания 24 В, 100 Вт", 1, ""),
            ("Провод, коннекторы, распределитель", 1, "комплект"),
        ]),
        ("Крепёж и монтаж", [
            ("Ножка регулируемая 80 мм", 14, "нижние модули 2 × 4, тумба 6; отступ 50 от лица"),
            ("Конфирмат 7 × 50", 160, "с запасом"),
            ("Заглушка конфирмата", 40, "видимые места"),
            ("Саморез 4 × 30 (задние стенки ЛДСП 16)", 120, ""),
            ("Стяжка межсекционная", 12, "модули между собой и антресоли к нижним"),
            ("Крепление к стене (уголок/навес)", 6, ""),
        ]),
    ])


RULES = ("Корпус ЛДСП 16; задние стенки ЛДСП 16 накладные; фасады 20, зазор 3. Размеры — по распилу "
         "заказчика; строки с пометкой «+» добавлены. Кромка ПВХ: Д — длина, Ш — ширина; 2 — 2 мм. "
         "Паз под LED: 16 × 8 по всей длине боковин, 100 от лица, на внутренней грани.")
FILL = {L16: "#efe7dc", FC: "#e9e2ef"}


def table_page(title, sheet, ps):
    rows, pos = [], None
    for p in ps:
        if p.posname != pos:
            pos = p.posname
            rows.append(f'<tr class="grp"><td colspan="8">{pos}</td></tr>')
        a = p.L * p.W * p.qty / 1e6
        mark = " <b>+</b>" if p.added else ""
        rows.append(f"<tr><td class='n'>{p.num}</td><td>{p.name}{mark}</td><td class='n'>{db.fmt(p.L)}</td>"
                    f"<td class='n'>{db.fmt(p.W)}</td><td class='n'>{p.qty}</td><td>{db.edge_text(p.edge)}</td>"
                    f"<td class='n'>{a:.2f}</td><td>{p.note}</td></tr>")
    return rows


def main():
    ps = parts()
    for i, p in enumerate(ps, 1):
        p.num = i
    pages = []
    groups = list(OrderedDict((p.posname, 0) for p in ps))
    split = [groups[:3], groups[3:]]
    for k, gs in enumerate(split):
        sel = [p for p in ps if p.posname in gs]
        rows = table_page("", "", sel)
        tot = ""
        if k == len(split) - 1:
            sums = []
            for mat in (L16, FC):
                pm = [p for p in ps if p.mat == mat]
                a = sum(p.L * p.W * p.qty for p in pm) / 1e6
                e2 = sum(db.edge_len(p)[0] for p in pm)
                sums.append(f"<tr><td>{mat}</td><td class='n'>{a:.2f} м²</td><td class='n'>{e2:.1f} м</td></tr>")
            tot = ("<br><table class='sum' style='width:60%'><tr><th>Материал</th><th>Площадь (без запаса)</th>"
                   "<th>Кромка 2 мм</th></tr>" + "".join(sums) + "</table>")
        table = ("<table><tr><th>№</th><th>Деталь</th><th>Длина</th><th>Ширина</th><th>Кол.</th><th>Кромка</th>"
                 "<th>м²</th><th>Примечание</th></tr>" + "".join(rows) + "</table>")
        pages.append(f'<div class="page"><div class="frame"></div>'
                     f'{db.head("ДЕТАЛИРОВКА — ШКАФ С АНТРЕСОЛЬЮ И ТУМБОЙ", "по модулям, в электронном виде", f"Лист {3 + k}")}'
                     f'<div class="note">{RULES}</div>{table}{tot}</div>')
    with open(os.path.join(HERE, "_detal.html"), "w", encoding="utf-8") as f:
        f.write(f"<!doctype html><html lang='ru'><head><meta charset='utf-8'><style>{db.CSS}</style></head>"
                f"<body>{''.join(pages)}</body></html>")
    rows = []
    for grp, items in hardware().items():
        rows.append(f'<tr class="grp"><td colspan="3">{grp}</td></tr>')
        rows += [f"<tr><td>{n}</td><td class='n'>{q}</td><td>{c}</td></tr>" for n, q, c in items]
    table = ("<table><tr><th>Наименование</th><th>Кол.</th><th>Где / примечание</th></tr>" + "".join(rows) + "</table>")
    hw = (f'<div class="page"><div class="frame"></div>'
          f'{db.head("ФУРНИТУРА — ШКАФ С АНТРЕСОЛЬЮ И ТУМБОЙ", "петли, ящики, подсветка, крепёж", "Лист 5")}'
          f'{table}</div>')
    with open(os.path.join(HERE, "_hw.html"), "w", encoding="utf-8") as f:
        f.write(f"<!doctype html><html lang='ru'><head><meta charset='utf-8'><style>{db.CSS}</style></head>"
                f"<body>{hw}</body></html>")
    print(len(ps), "позиций")


if __name__ == "__main__":
    main()
