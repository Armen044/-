#!/usr/bin/env python3
"""Деталировка кухни по позициям (ЛДСП корпус, ХДФ, фасады эмаль, фасады шпон, стекло)
и фурнитура отдельным файлом.

Правила (согласованы с заказчиком):
- корпус ЛДСП 16; задняя стенка ХДФ 3 мм накладная → глубина боковин = глубина корпуса − 3;
- нижние и колонны: глубина корпуса 560 (зазор 22 у стены), верхние 980 — глубина 330,
  угловой верхний — 560 (в плоскости колонн);
- дно и крыша — между боковинами; у нижних вместо крыши две царги 100;
- фасады основной стены — МДФ 18 эмаль, правой стены — шпон 18; двери пенала — стекло в алюм. раме;
- зазор фасадов 2 мм; петли с доводчиком; ящики Firmax Smartline NL 500.
"""
import importlib.util
import os
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("db", os.path.join(HERE, "..", "detal", "build.py"))
db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db)
from geom import *          # noqa: E402,F403

T, HDF = 16, 3
L16, HD3, EM, VN, GL = "ЛДСП 16 (корпус)", "ХДФ 3 (задние стенки)", "МДФ 18 эмаль", "Шпон 18", "Стекло / алюм. рама"
BASE_H, BASE_D = CB - PL, 560            # 780 × 560
UP_H, UP_D = UH, 330                     # 980 × 330
COL_H, COL_D = H - PL, 560               # 2400 × 560
NL = 500


class P(db.Item):
    def __init__(self, pos, name, mat, L, Wd, qty, edge="----", note=""):
        super().__init__(name, mat, L, Wd, qty, edge, note)
        self.posname = pos


def carcass(pos, W, Hh, D, top="крыша", shelves=0, fixed=(), note_side="", rails=False):
    """Корпус: боковины, дно, крыша (или 2 царги), полки, задняя стенка ХДФ."""
    sd = D - HDF
    lw = W - 2 * T
    out = [P(pos, "Боковина", L16, Hh, sd, 2, "2---", note_side),
           P(pos, "Дно", L16, lw, sd, 1, "2---")]
    if rails:
        out.append(P(pos, "Царга (вместо крыши)", L16, lw, 100, 2, "4---", "передняя за профилем Gola, задняя"))
    else:
        out.append(P(pos, "Крыша", L16, lw, sd, 1, "2---"))
    for name, q in fixed:
        out.append(P(pos, name, L16, lw, sd, q, "2---", "неподвижная (конфирматы)"))
    if shelves:
        out.append(P(pos, "Полка съёмная", L16, lw - 2, sd - 20, shelves, "2---"))
    out.append(P(pos, "Задняя стенка", HD3, Hh - 4, W - 4, 1, "----", "накладная, отступ 2 мм по контуру"))
    return out


def drawers(pos, lw, n_low, n_up, inner=0):
    out = [P(pos, "Ящик Firmax: дно", L16, lw - 75, NL - 24, n_low + n_up, "----", "проверить по каталогу Firmax Smartline"),
           ]
    if n_up:
        out.append(P(pos, "Ящик Firmax (средний борт): задняя стенка", L16, lw - 87, 84, n_up, "4---", "по каталогу Firmax"))
    if n_low:
        out.append(P(pos, "Ящик Firmax (высокий борт): задняя стенка", L16, lw - 87, 167, n_low, "4---", "по каталогу Firmax"))
    if inner:
        out += [P(pos, "Внутренний ящик: дно", L16, lw - 75, NL - 24, inner, "----", "скрытый, внутри верхнего ящика"),
                P(pos, "Внутренний ящик: задняя стенка", L16, lw - 87, 84, inner, "4---"),
                P(pos, "Внутренний ящик: лицевая панель", L16, lw - 6, 90, inner, "2---", "размер по каталогу Firmax")]
    return out


def parts():
    out = []
    lw6 = 600 - 2 * T                                   # 568
    # 1. Пенал-витрина 400: корпус 382 + боковина-эмаль 18
    pw = PENCIL[1] - PENCIL[0] - 18                     # 382
    out += carcass("1. Пенал-витрина 400", pw, COL_H, COL_D, fixed=[("Полка на стыке дверей (Н=1300)", 1)],
                   note_side="левая закрывается панелью эмаль")
    out += [P("1. Пенал-витрина 400", "Боковина декоративная (до пола)", EM, H, 600, 1, "----", "ЭМАЛЬ, видимая сторона"),
            P("1. Пенал-витрина 400", "Дверь — стекло в алюминиевой раме", GL, 1196, pw - 2, 2, "----",
              "рамка чёрная/алюм., стекло 4 мм; петли под рамку"),
            P("1. Пенал-витрина 400", "Полка стеклянная, закалённое 6 мм", GL, pw - 2 * T - 2, COL_D - HDF - 30,
              len(PENCIL_SHELVES), "----", "шлифованная кромка; держатели для стекла")]
    # 2–4. Модули 600 с ящиками
    for pos, inner in (("2. Модуль 600 — 2 ящика", 0), ("3. Модуль 600 под варочную — 2 ящика", 0),
                       ("4. Модуль 600 — 2 ящика + скрытый", 1)):
        out += carcass(pos, 600, BASE_H, BASE_D, rails=True, note_side="вырезы под профиль Gola верх и средний")
        out += drawers(pos, lw6, 1, 1, inner)
        out += [P(pos, "Фасад ящика нижний", EM, 598, DR_LOW[1] - DR_LOW[0], 1, "----"),
                P(pos, "Фасад ящика верхний", EM, 598, DR_UP[1] - DR_UP[0], 1, "----",
                  "под варочной — проверить отступ под панель" if "варочн" in pos else "")]
    # 5. ПММ – без корпуса
    out.append(P("5. ПММ 600 встраиваемая", "Фасад ПММ", EM, 598, GOLA_TOP[0] - PL - GAP, 1, "----",
                 "крепится к двери ПММ, корпуса нет"))
    # 6. Мойка
    pos = "6. Модуль 600 под мойку"
    sd = BASE_D - HDF
    out += [P(pos, "Боковина", L16, BASE_H, sd, 2, "2---", "вырез под профиль Gola верх"),
            P(pos, "Дно", L16, lw6, sd, 1, "2---", "влагостойкий коврик/поддон"),
            P(pos, "Царга передняя", L16, lw6, 100, 1, "4---", "задней царги нет — коммуникации"),
            P(pos, "Задняя стенка (нижняя часть)", HD3, 300, 596, 1, "----", "сверху открыто под сифон и трубы"),
            P(pos, "Дверь", EM, 598, GOLA_TOP[0] - PL - GAP, 1, "----")]
    # 7. Глухой угол
    out.append(P("7. Глухой угол 600 (под столешницей)", "Стойка-опора столешницы", L16, BASE_H, sd, 1, "2---",
                 "у стены справа; корпуса нет"))
    # 8–11. Верхние
    for pos, extra in (("8. Верхний 600 — 2 полки", "sh"), ("9. Верхний 600 под вытяжку", "hood"),
                       ("10. Верхний 600 — 2 полки", "sh"), ("11. Верхний 600 — сушка + полка", "dry")):
        if extra == "sh":
            out += carcass(pos, 600, UP_H, UP_D, shelves=2)
        elif extra == "dry":
            out += carcass(pos, 600, UP_H, UP_D, shelves=1)
        else:
            out += carcass(pos, 600, UP_H, UP_D, fixed=[("Полка над вытяжкой (вырез под воздуховод)", 1)])
            out[-4].note = "вырез под встраиваемую вытяжку — по паспорту"   # дно
        out.append(P(pos, "Дверь", EM, 598, UP_H - 2, 1, "----"))
    # 12. Угловой верхний на правой стене
    pos = "12. Угловой верхний 580 + планка 20"
    out += carcass(pos, 580, UP_H, COL_D, shelves=2)
    out += [P(pos, "Дверь", VN, 578, UP_H - 2, 1, "----"),
            P(pos, "Планка (фальш) 20", VN, UP_H, 20, 1, "----", "на брусок ЛДСП"),
            P(pos, "Брусок под планку", L16, UP_H, 50, 1, "----")]
    # 13. Колонна холодильника
    pos = "13. Колонна холодильника 600"
    out += carcass(pos, 600, COL_H, COL_D, fixed=[("Полка над холодильником (отсек 450)", 1)])
    out += [P(pos, "Фасад нижний", VN, 598, FR_LOW[1] - FR_LOW[0], 1, "----", "на дверь холодильника (полозья в комплекте)"),
            P(pos, "Фасад верхний (цельный)", VN, 598, 1680, 1, "----", "на дверь холодильника; закрывает и отсек 450")]
    # 14. Колонна духовки + СВЧ
    pos = "14. Колонна духовки + СВЧ 600"
    out += carcass(pos, 600, COL_H, COL_D, shelves=2,
                   fixed=[("Полка под духовку", 1), ("Полка под СВЧ", 1), ("Полка над СВЧ", 1)])
    out += drawers(pos, lw6, 1, 0)
    out += [P(pos, "Фасад ящика под духовкой", VN, 598, OV_DRW[1] - OV_DRW[0], 1, "----", "профиль Gola над ним"),
            P(pos, "Дверь верхняя (цельная 920)", VN, 598, 916, 1, "----", "над СВЧ, внутри 2 полки")]
    # 15. Общие: цоколь, планки, торцы
    pos = "15. Цоколь, планки 130, торцы"
    out += [P(pos, "Цоколь основной стены", L16, 3382, PL - 2, 1, "2---", "можно из 2 частей; за профилем фасадов"),
            P(pos, "Цоколь колонн с вырезами под решётки", L16, 1200, PL - 2, 1, "2---", "2 вент. решётки"),
            P(pos, "Торцевая панель правая (до пола)", VN, H, 600, 1, "----", "ШПОН"),
            P(pos, "Планка 130 над пеналом", EM, 400, STRIP, 1, "----"),
            P(pos, "Планка 130 возврат пенал → верхние", EM, 250, STRIP, 1, "----"),
            P(pos, "Планка 130 над верхними", EM, STRIP_END - PENCIL[1], STRIP, 1, "----", "до сушки"),
            P(pos, "Планка 130 загиб к стене", EM, UD, STRIP, 1, "----", "после сушки"),
            P(pos, "Планка 130 правая стена", VN, WR, STRIP, 1, "----", "над угловым и колоннами"),
            P(pos, "Планка 130 возврат на торце", VN, 600, STRIP, 1, "----"),
            P(pos, "Столешница", "Столешница 40", WM - PENCIL[1], 600, 1, "----",
              "3600 × 600 × 40, материал по выбору; вырезы под мойку и варочную")]
    return out


def hardware():
    return OrderedDict([
        ("Петли (все с доводчиком)", [
            ("Петля накладная 110° с доводчиком (Blum CLIP top BLUMOTION / аналог)", 14,
             "верхние 4 × 2, угловой 2, мойка 2, дверь колонны над СВЧ 2"),
            ("Монтажная планка к петле", 14, ""),
            ("Петля для алюминиевой рамки с доводчиком", 6, "двери пенала: 2 × 3"),
            ("Монтажная планка к петле алюм. рамки", 6, ""),
        ]),
        ("Ящики Firmax Smartline (NL 500, полное выдвижение, доводчик)", [
            ("Комплект ящика, высокий борт", 4, "нижние ящики поз. 2–4 + ящик под духовкой"),
            ("Комплект ящика, средний борт", 3, "верхние ящики поз. 2–4"),
            ("Комплект внутреннего (скрытого) ящика", 1, "поз. 4, внутри верхнего"),
            ("Крепление фасада / стяжки фасада Firmax", 8, "по одному на ящик"),
        ]),
        ("Профиль Gola (чёрный)", [
            ("Профиль Gola L (верхний, под столешницу), 3000 мм", 1, "поз. 2–6"),
            ("Профиль Gola C (средний), 1800 мм", 1, "поз. 2–4"),
            ("Профиль Gola C / L, 600 мм", 1, "над ящиком под духовкой"),
            ("Заглушки торцевые и соединители Gola", 6, ""),
        ]),
        ("Наполнение", [
            ("Сушка для посуды в шкаф 600, 2 уровня, с поддоном", 1, "поз. 11"),
            ("Полкодержатель под ЛДСП 16 (с фиксацией)", 36, "9 съёмных полок × 4"),
            ("Полкодержатель для стеклянной полки", 24, "6 стеклянных полок × 4"),
            ("Направляющие / крепление фасадов встраиваемого холодильника", 1, "в комплекте с холодильником"),
            ("Комплект крепления фасада ПММ", 1, "в комплекте с ПММ"),
        ]),
        ("Крепёж и монтаж", [
            ("Конфирмат 7 × 50", 220, "с запасом"),
            ("Заглушка конфирмата (в цвет корпуса)", 40, "видимые места"),
            ("Гвоздь / саморез для ХДФ 3 × 16", 450, "шаг 120 мм"),
            ("Опора регулируемая h 100", 28, "нижние 4 × 4, пенал 4, колонны 2 × 4"),
            ("Клипса цоколя", 14, ""),
            ("Решётка вентиляционная в цоколь", 2, "под колоннами"),
            ("Решётка вентиляционная верхняя (холодильник)", 1, "в крыше/планке колонны"),
            ("Навес для верхних шкафов регулируемый (пара)", 6, "поз. 8–12 + запас"),
            ("Монтажная шина для навесов, 2 м", 2, ""),
            ("Стяжка межсекционная", 16, ""),
            ("Уголок крепления столешницы", 12, ""),
            ("Крепление колонн и пенала к стене (уголок)", 6, ""),
            ("Герметик для вырезов столешницы", 1, ""),
        ]),
        ("Техника (не в составе мебели — для справки)", [
            ("Вытяжка встраиваемая 600", 1, "поз. 9, воздуховод к вент. выходу"),
            ("Варочная панель 600", 1, "поз. 3"),
            ("Мойка + смеситель", 1, "поз. 6"),
            ("ПММ 600 полновстраиваемая", 1, "поз. 5"),
            ("Холодильник встраиваемый (2 двери)", 1, "поз. 13; ниша по паспорту"),
            ("Духовой шкаф 600, СВЧ встраиваемая 38 см", 2, "поз. 14; высоту ниш сверить по паспорту"),
        ]),
    ])


RULES = ("Корпус — ЛДСП 16; задняя стенка ХДФ 3 мм накладная (боковины и горизонты = глубина корпуса − 3, "
         "ХДФ = габарит корпуса − 4). Нижние и колонны — глубина 560 (зазор 22 у стены), верхние — 330, "
         "угловой верхний — 560. Дно и крыша — между боковинами, у нижних вместо крыши 2 царги 100. "
         "Съёмные полки −2 по длине, глубина −20. Фасады: основная стена — МДФ 18 эмаль, правая — шпон 18, "
         "зазор 2. Ящики Firmax Smartline NL 500 — дно и задние стенки посчитаны по формулам "
         "(LW − 75) × (NL − 24), (LW − 87) × h: сверить с каталогом Firmax до раскроя. "
         "Кромка ПВХ: Д — длина, Ш — ширина; 2 — 2 мм, 0,4 — 0,4 мм.")
FILL = {L16: "#efe7dc", HD3: "#e6e6e6", EM: "#f6f3ee", VN: "#d8b48b", GL: "#d4e6ec", "Столешница 40": "#d3cbbf"}


def part_svg(p, box=(150, 74)):
    db_fill = {**FILL}
    bw, bh = box
    k = min((bw - 30) / p.L, (bh - 26) / p.W)
    w, h = p.L * k, p.W * k
    x0, y0 = (bw - w) / 2 + 6, (bh - h) / 2 - 2
    s = [f'<svg viewBox="0 0 {bw} {bh}" width="{bw}" height="{bh}">',
         f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{db_fill.get(p.mat, "#eee")}" stroke="#333" stroke-width="0.8"/>']
    sides = [((x0, y0 + h), (x0 + w, y0 + h)), ((x0, y0), (x0 + w, y0)), ((x0, y0), (x0, y0 + h)), ((x0 + w, y0), (x0 + w, y0 + h))]
    for ch, (a, b) in zip(p.edge, sides):
        if ch in "24":
            c, sw = ("#c0392b", 3) if ch == "2" else ("#2f6fb0", 1.6)
            s.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{c}" stroke-width="{sw}"/>')
    s.append(f'<text x="{x0 + w / 2:.1f}" y="{y0 + h + 11:.1f}" font-size="9" text-anchor="middle">{db.fmt(p.L)}</text>')
    s.append(f'<text x="{x0 - 4:.1f}" y="{y0 + h / 2:.1f}" font-size="9" text-anchor="middle" '
             f'transform="rotate(-90 {x0 - 4:.1f} {y0 + h / 2:.1f})">{db.fmt(p.W)}</text></svg>')
    return "".join(s)


def table_page(title, sub, sheet, ps, show_edge=True, total=None):
    rows, pos, area, e2, e04 = [], None, 0, 0, 0
    for p in ps:
        if p.posname != pos:
            pos = p.posname
            rows.append(f'<tr class="grp"><td colspan="8">{pos}</td></tr>')
        a = p.L * p.W * p.qty / 1e6
        x2, x4 = db.edge_len(p)
        area += a
        e2 += x2
        e04 += x4
        rows.append(f"<tr><td class='n'>{p.num}</td><td>{p.name}</td><td class='n'>{db.fmt(p.L)}</td>"
                    f"<td class='n'>{db.fmt(p.W)}</td><td class='n'>{p.qty}</td>"
                    f"<td>{db.edge_text(p.edge) if show_edge else '—'}</td><td class='n'>{a:.2f}</td><td>{p.note}</td></tr>")
    if total is None:
        tot = ""
    else:
        area = sum(p.L * p.W * p.qty for p in total) / 1e6
        e2 = sum(db.edge_len(p)[0] for p in total)
        e04 = sum(db.edge_len(p)[1] for p in total)
        ps = total
    tot = "" if total is None else (f"<tr class='sum'><td></td><td>ИТОГО</td><td></td><td></td><td class='n'>{sum(p.qty for p in ps)}</td>"
           f"<td>{'кромка 2 мм: %.1f м; 0,4 мм: %.1f м' % (e2, e04) if show_edge else ''}</td>"
           f"<td class='n'>{area:.2f}</td><td>+10–15 % на раскрой</td></tr>")
    table = ("<table><tr><th>№</th><th>Деталь</th><th>Длина</th><th>Ширина</th><th>Кол.</th><th>Кромка</th>"
             "<th>м²</th><th>Примечание</th></tr>" + "".join(rows) + tot + "</table>")
    return (f'<div class="page"><div class="frame"></div>{db.head(title, sub, sheet)}'
            f'<div class="note">{RULES}</div>{table}</div>')


def split(ps, n):
    """Делит список деталей на страницы, не разрывая позиции."""
    pages, cur, count = [], [], 0
    for pos in OrderedDict((p.posname, 0) for p in ps):
        grp = [p for p in ps if p.posname == pos]
        if cur and count + len(grp) + 1 > n:
            pages.append(cur)
            cur, count = [], 0
        cur += grp
        count += len(grp) + 1
    if cur:
        pages.append(cur)
    return pages


def sketch_page(title, sheet, ps):
    cards = "".join(f'<div class="card"><b>{p.num}. {p.name}</b><br>{p.posname.split(".")[0]} поз. · {p.qty} шт'
                    f'{part_svg(p)}<br>кромка: {db.edge_text(p.edge)}</div>' for p in ps)
    legend = ('<div class="legend"><span><span class="sw" style="border-top:3px solid #c0392b"></span>кромка 2 мм</span>'
              '<span><span class="sw" style="border-top:1.6px solid #2f6fb0"></span>кромка 0,4 мм</span>'
              '<span>Д1 — нижняя длинная сторона эскиза, Д2 — верхняя, Ш1 — левая, Ш2 — правая</span></div>')
    return (f'<div class="page"><div class="frame"></div>{db.head(title, "номера — как в таблице ЛДСП", sheet)}'
            f'{legend}<div class="cards">{cards}</div></div>')


def hw_page():
    def block(groups):
        rows = []
        for grp, items in groups:
            rows.append(f'<tr class="grp"><td colspan="3">{grp}</td></tr>')
            rows += [f"<tr><td>{n}</td><td class='n'>{q}</td><td>{c}</td></tr>" for n, q, c in items]
        return ("<table><tr><th>Наименование</th><th>Кол.</th><th>Где / примечание</th></tr>" + "".join(rows) + "</table>")
    hw = list(hardware().items())
    note = ("<div class='note'><br><b>Примечания.</b> Все распашные фасады — на петлях с доводчиком (ручек нет: "
            "нижний ряд — профиль Gola, верхние и колонны — открывание за край фасада). Ящики — Firmax Smartline "
            "NL 500 с доводчиком; дно и задние стенки ящиков — в деталировке ЛДСП (сверить с каталогом). Фасады "
            "холодильника и ПММ крепятся комплектами техники. Количество крепежа — с запасом.</div>")
    return (f'<div class="page"><div class="frame"></div>'
            f'{db.head("КУХНЯ УГЛОВАЯ — ФУРНИТУРА", "по позициям чертежа кухни (лист А2)", "Лист 1")}'
            f'<div class="cols"><div>{block(hw[:4])}</div><div>{block(hw[4:])}{note}</div></div></div>')


def write(html_pages, name):
    html = (f"<!doctype html><html lang='ru'><head><meta charset='utf-8'><style>{db.CSS}</style></head>"
            f"<body>{''.join(html_pages)}</body></html>")
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(html)


def main():
    ps = parts()
    for i, p in enumerate(ps, 1):
        p.num = i
    mats = OrderedDict([(L16, "ЛДСП 16 — КОРПУС"), (HD3, "ХДФ 3 — ЗАДНИЕ СТЕНКИ"), (EM, "ФАСАДЫ МДФ 18 ЭМАЛЬ (основная стена)"),
                        (VN, "ФАСАДЫ ШПОН 18 (правая стена)"), (GL, "СТЕКЛО И АЛЮМИНИЕВЫЕ РАМКИ (заказ отдельно)"),
                        ("Столешница 40", "СТОЛЕШНИЦА")])
    pages, sheet = [], 0
    for mat, title in mats.items():
        sel = [p for p in ps if p.mat == mat]
        # перенумерация внутри материала
        for k, p in enumerate(sel, 1):
            p.num = k
        chunks = split(sel, 36)
        for ci, chunk in enumerate(chunks):
            sheet += 1
            pages.append(table_page(title, "Кухня угловая 4000 × 1800 × 2630 — по позициям", f"Лист {sheet}",
                                    chunk, show_edge=(mat == L16),
                                    total=sel if ci == len(chunks) - 1 else None))
        if mat == L16:
            for i in range(0, len(sel), 36):
                sheet += 1
                pages.append(sketch_page("ЭСКИЗЫ ДЕТАЛЕЙ ЛДСП", f"Лист {sheet}", sel[i:i + 36]))
    write(pages, "_detal.html")
    write([hw_page()], "_hw.html")
    print(len(ps), "деталей,", sheet, "листов")


if __name__ == "__main__":
    main()
