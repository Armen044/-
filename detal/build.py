#!/usr/bin/env python3
"""Деталировка (ЛДСП / МДФ / задняя стенка 10 мм) и фурнитура для двух шкафов:
«Шкаф со столом» (shkaf3) и «Шкаф с ящиками и тумба» (shkaf2).

Принятые правила (указаны на листах):
- корпус ЛДСП 16 мм, фасады МДФ 18 мм, задняя стенка 10 мм накладная на тыльную сторону
  → глубина боковин и горизонтов = глубина корпуса − 10;
- крыша и дно – между боковинами; стойки – между крышей и дном;
- съёмные полки −2 мм по длине, глубина полок = глубина боковины − 20;
- ящики Blum TANDEMBOX antaro M, NL 500: дно (LW−75) × (NL−24), задняя стенка (LW−87) × 84;
- кромка ПВХ: 2 мм – видимые торцы, 0,4 мм – прочие открытые торцы.
"""
import importlib.util
import os
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    import sys
    sys.path.insert(0, os.path.join(ROOT, "garderobnaya"))
    spec.loader.exec_module(m)
    return m


s2 = load("s2", os.path.join(ROOT, "shkaf2", "sheet.py"))
s3 = load("s3", os.path.join(ROOT, "shkaf3", "sheet.py"))

T, BACK = 16, 10
L16, L26, B10, M18 = "ЛДСП 16", "ЛДСП 26 (столешница)", "Задняя стенка 10", "МДФ 18"
# кромка: строка из 4 символов – Д1 Д2 Ш1 Ш2: «2» – 2 мм, «4» – 0,4 мм, «-» – без кромки
NL, LWB = 500, 75          # TANDEMBOX: NL и вычет на дно


def r(v):
    """Размер детали: до 0,01 мм (как в проекте), целые – без дробной части."""
    v = round(v, 2)
    return int(v) if v == int(v) else v


class Item:
    def __init__(self, name, mat, L, Wd, qty, edge="----", note=""):
        self.name, self.mat, self.L, self.W, self.qty, self.edge, self.note = name, mat, r(L), r(Wd), qty, edge, note


# ---------------------------------------------------------------------------
def parts_shkaf3():
    """Шкаф со столом 2400 × 600 × 2583 (цоколь 50) + стол 1200 × 600 с тумбой."""
    W, H, PL = s3.W, s3.H, s3.PL
    CH = H - PL                           # высота корпуса 2533
    SD = s3.CD - BACK                     # глубина боковин 572
    SH = SD - 20                          # глубина полок 552
    w1 = s3.X1 - T - T / 2                # секция 1 в свету 576
    w2 = s3.X2 - s3.X1 - T                # секция 2 в свету 584
    w3 = W - s3.X2 - T / 2 - T            # секция 3 в свету 1176
    P = []
    P += [Item("Боковина", L16, CH, SD, 2, "2-4-", "кромка 2 – перед, 0,4 – верхний торец"),
          Item("Крыша", L16, W - 2 * T, SD, 1, "2---"),
          Item("Дно", L16, W - 2 * T, SD, 1, "2---"),
          Item("Стойка вертикальная", L16, CH - 2 * T, SD, 2, "2---", "оси 600 и 1200"),
          Item("Дно антресоли, секция 1", L16, w1, SD, 1, "2---"),
          Item("Дно антресоли, секция 2", L16, w2, SD, 1, "2---"),
          Item("Дно антресоли, секция 3", L16, w3, SD, 1, "2---"),
          Item("Полка антресоли, секция 1 (съёмная)", L16, w1 - 2, SH, 1, "2---"),
          Item("Полка антресоли, секция 2 (съёмная)", L16, w2 - 2, SH, 1, "2---"),
          Item("Полка открытая, секция 1 (декор дерево)", L16, w1 - 2, SH, 5, "2---", "подсветка у левой боковины"),
          Item("Полка, секция 2 (съёмная)", L16, w2 - 2, SH, 5, "2---"),
          Item("Полка, секция 3 (неподвижная)", L16, w3, SH, 1, "2---", "над нижней штангой"),
          Item("Цоколь", L16, W - 100, PL - 2, 1, "2---", "на опорах, отступ 50")]
    # тумба стола: ширина 400 (вдоль стола), глубина 580, высота 740
    PW, PD, PH = 400, 580, 740
    pSD = PD - s3.DT - BACK               # 552
    LW = PW - 2 * T                       # 368
    P += [Item("Тумба стола: боковина", L16, PH, pSD, 2, "2---"),
          Item("Тумба стола: дно", L16, LW, pSD, 1, "2---"),
          Item("Тумба стола: царга верхняя", L16, LW, 100, 2, "----", "крепление столешницы"),
          Item("Ящик тумбы: дно (TANDEMBOX)", L16, LW - LWB, NL - 24, 4, "----"),
          Item("Ящик тумбы: задняя стенка (TANDEMBOX M)", L16, LW - 87, 84, 4, "4---")]
    P += [Item("Столешница стола", L26, 1200, 600, 1, "2222", "декор орех, 3 видимых торца + торец у шкафа")]
    # задние стенки 10 мм (шкаф – из двух частей со стыком на стойке 1200)
    P += [Item("Задняя стенка шкафа (2 части, стык на стойке 1200)", B10, CH - 4, s3.X2 - 2, 2, "----"),
          Item("Задняя стенка тумбы стола", B10, PH - 4, PW - 4, 1, "----")]
    # МДФ 18
    d0, d1 = s3.DOOR_Z
    P += [Item("Дверь", M18, d1 - d0, 600 - 2, 3, "----", "профиль-ручка на кромке у стыка"),
          Item("Фасад антресоли «волна»", M18, s3.PANEL[1] - s3.PANEL[0] - 4, 600 - 2, 4, "----",
               "фрезеровка «волна», выступает до потолка"),
          Item("Фасад под столом", M18, s3.LOW_DOOR[1] - s3.LOW_DOOR[0], 600 - 2, 1, "----"),
          Item("Фасад ящика тумбы", M18, PW - 4, s3.DRW, 4, "----")]
    return P


def hw_shkaf3():
    return OrderedDict([
        ("Петли и подъём", [
            ("Петля Blum CLIP top BLUMOTION 110°, накладная", 11, "двери у боковин, фасады антресоли у боковин, фасад под столом"),
            ("Петля Blum CLIP top BLUMOTION 110°, полунакладная", 14, "двери и фасады антресоли на стойках 600/1200"),
            ("Монтажная планка Blum CLIP 0 мм", 25, ""),
            ("Толкатель Blum TIP-ON для дверей", 4, "фасады антресоли «волна» (без ручек)"),
        ]),
        ("Ящики", [
            ("Blum TANDEMBOX antaro M, NL 500, BLUMOTION (комплект)", 4, "тумба стола, LW 368"),
        ]),
        ("Ручки", [
            ("Профиль-ручка вертикальный (алюм., чёрный), L 1965", 3, "на кромках дверей у стыков"),
            ("Профиль-ручка вертикальный, L 715", 1, "фасад под столом"),
        ]),
        ("Наполнение", [
            ("Штанга овальная (чёрная), L 1174", 2, "секция 3"),
            ("Штангодержатель", 4, ""),
            ("Полкодержатель с фиксацией (под ЛДСП 16)", 48, "12 съёмных полок × 4"),
        ]),
        ("Крепёж корпуса", [
            ("Конфирмат 7 × 50", 85, "шкаф 64 + тумба стола 18, с запасом"),
            ("Заглушка конфирмата (в цвет корпуса)", 30, "только на видимых местах"),
            ("Саморез 3,5 × 25 (задняя стенка 10 мм)", 170, "шаг 150 мм"),
            ("Опора регулируемая h 50", 8, "шкаф"),
            ("Клипса цоколя", 4, ""),
            ("Подпятник", 4, "тумба стола"),
            ("Уголок мебельный металлический", 6, "крепление столешницы к шкафу и тумбе"),
            ("Крепление к стене (уголок / навес)", 4, ""),
        ]),
        ("Подсветка", [
            ("Профиль алюминиевый врезной с рассеивателем, 2 м", 1, "секция 1, вертикально"),
            ("Профиль алюминиевый врезной с рассеивателем, 0,6 м", 1, "антресоль справа"),
            ("Лента LED 24 В, 4000 K, м", 3, ""),
            ("Блок питания 24 В, 30 Вт", 1, ""),
            ("Выключатель / датчик движения", 1, "открытые полки"),
            ("Датчик открывания двери", 1, "антресоль справа"),
        ]),
    ])


# ---------------------------------------------------------------------------
def parts_shkaf2():
    """Шкаф с ящиками 1600 × 600 × 2645 (цоколь 80) + тумба 1565 × 500 + фальш-планки 20."""
    W, H, PL = s2.W, s2.H, s2.PL
    CH = H - PL                           # 2565
    SD = s2.CD - BACK                     # 572
    SH = SD - 20                          # 552
    w = s2.MID - T / 2 - T                # 776
    LW = w - 2 * T                        # ящики между проставками: 744
    P = [Item("Боковина", L16, CH, SD, 2, "2-4-", "кромка 2 – перед, 0,4 – верхний торец"),
         Item("Крыша", L16, W - 2 * T, SD, 1, "2---"),
         Item("Дно", L16, W - 2 * T, SD, 1, "2---"),
         Item("Стойка средняя", L16, CH - 2 * T, SD, 1, "2---"),
         Item("Полка антресоли (неподвижная)", L16, w, SH, 2, "2---"),
         Item("Полка над ящиками (неподвижная)", L16, w, SH, 1, "2---"),
         Item("Полка левая (съёмная)", L16, w - 2, SH, 3, "2---"),
         Item("Полка правая под штангами (неподвижная)", L16, w, SH, 2, "2---"),
         Item("Проставка под ящики", L16, s2.DRAWER_ZONE, SD - 30, 2, "2---", "по бокам блока ящиков"),
         Item("Фасад ящика внутренний", L16, LW - 4, s2.DR_H, 4, "2222", "зазор между фасадами 30 – место ручки"),
         Item("Ящик: дно (TANDEMBOX)", L16, LW - LWB, NL - 24, 4, "----"),
         Item("Ящик: задняя стенка (TANDEMBOX M)", L16, LW - 87, 84, 4, "4---"),
         Item("Цоколь", L16, W - 100, PL - 2, 1, "2---", "на опорах, отступ 50"),
         Item("Планка крепления фальш-панели", L16, CH - 2, 80, 1, "----", "справа"),
         ]
    # тумба
    TW, THt, TD = s2.TB_W, s2.TB_H, s2.TB_D
    BH = THt - s2.TB_LID - PL             # высота корпуса тумбы 402
    tSD = TD - s2.DT - BACK               # 572
    P += [Item("Тумба: боковина", L16, BH, tSD, 2, "2-4-", "0,4 – верхний торец под крышкой"),
          Item("Тумба: перегородка", L16, BH - T, tSD, 1, "2---"),
          Item("Тумба: дно", L16, TW - 2 * T, tSD, 1, "----"),
          Item("Тумба: царга задняя (под петли крышки)", L16, (TW - 3 * T) / 2, 100, 2, "----"),
          Item("Тумба: цоколь", L16, TW - 100, PL - 2, 1, "2---"),
          Item("Планка крепления фальш-панели тумбы", L16, THt - 2, 80, 1, "----", "слева")]
    P += [Item("Задняя стенка шкафа", B10, CH - 4, W - 4, 1, "----"),
          Item("Задняя стенка тумбы", B10, BH - 4, TW - 4, 1, "----")]
    dw = W / 4 - s2.DOOR_GAP
    low = s2.SPLIT - s2.DOOR_GAP / 2 - (PL + 2)
    up = (H - 2) - (s2.SPLIT + s2.DOOR_GAP / 2)
    half = TW / 2 - 3
    P += [Item("Дверь нижняя", M18, low, dw, 4, "----", "фрезеровка-ручка 15 мм по кромке у стыка, розовая эмаль"),
          Item("Дверь антресоли", M18, up, dw, 4, "----", "фрезеровка-ручка (продолжение паза)"),
          Item("Тумба: передняя панель", M18, BH - 4, half, 2, "----", "неподвижная"),
          Item("Тумба: крышка", M18, TD, half, 2, "----", "открывание вверх"),
          Item("Фальш-планка 20 (шкаф, справа)", M18, CH - 2, 20, 1, "----"),
          Item("Фальш-планка 20 (тумба, слева)", M18, THt - 2, 20, 1, "----")]
    return P


def hw_shkaf2():
    return OrderedDict([
        ("Петли", [
            ("Петля Blum CLIP top BLUMOTION 110°, накладная", 14, "двери у боковин: 5 + 5 нижние, 2 + 2 антресоль"),
            ("Петля Blum CLIP top BLUMOTION 110°, полунакладная", 14, "двери на средней стойке: 5 + 5, 2 + 2"),
            ("Монтажная планка Blum CLIP 0 мм", 28, ""),
        ]),
        ("Ящики", [
            ("Blum TANDEMBOX antaro M, NL 500, BLUMOTION (комплект)", 4, "внутренние, LW 744 (между проставками)"),
            ("Крепление внутреннего фасада TANDEMBOX", 4, ""),
        ]),
        ("Наполнение", [
            ("Штанга овальная, L 774", 2, "правый отсек"),
            ("Штангодержатель", 4, ""),
            ("Полкодержатель с фиксацией", 12, "3 съёмные полки × 4"),
        ]),
        ("Тумба", [
            ("Петля для откидной крышки (рояльная), L 750", 2, "по одной на крышку"),
            ("Подъёмник крышки с плавным опусканием (lid stay)", 4, "по 2 на крышку, крышка ≈ 6,5 кг"),
            ("Опора регулируемая h 80", 6, ""),
            ("Клипса цоколя", 3, ""),
        ]),
        ("Крепёж корпуса", [
            ("Конфирмат 7 × 50", 90, "шкаф 64 + тумба 21, с запасом"),
            ("Заглушка конфирмата", 20, "на видимых местах"),
            ("Саморез 3,5 × 25 (задняя стенка 10 мм)", 130, "шаг 150 мм"),
            ("Саморез 4 × 30 (передние панели тумбы, фальш-планки)", 24, ""),
            ("Опора регулируемая h 80", 6, "шкаф"),
            ("Клипса цоколя", 4, "шкаф"),
            ("Крепление к стене (уголок / навес)", 4, ""),
        ]),
        ("Подсветка", [
            ("Профиль алюминиевый врезной с рассеивателем, 2,5 м", 2, "вертикально в каждом отсеке"),
            ("Лента LED 24 В, 4000 K, м", 5, ""),
            ("Блок питания 24 В, 30 Вт", 1, ""),
            ("Датчик открывания двери", 2, "по одному на отсек"),
        ]),
    ])


# ---------------------------------------------------------------------------
def edge_len(p):
    """Метры кромки (2 мм, 0,4 мм) для позиции с учётом количества."""
    e2 = e04 = 0
    for k, ch in enumerate(p.edge):
        ln = p.L if k < 2 else p.W
        if ch == "2":
            e2 += ln
        elif ch == "4":
            e04 += ln
    return e2 * p.qty / 1000, e04 * p.qty / 1000


def edge_text(edge):
    names = ["Д1", "Д2", "Ш1", "Ш2"]
    out = []
    for k, ch in enumerate(edge):
        if ch == "2":
            out.append(f"{names[k]} 2")
        elif ch == "4":
            out.append(f"{names[k]} 0,4")
    return ", ".join(out) if out else "—"


def fmt(v):
    return str(v).replace(".", ",")


def part_svg(p, box=(150, 74)):
    """Эскиз детали: прямоугольник в масштабе, кромка 2 мм – толстая линия, 0,4 – тонкая цветная."""
    bw, bh = box
    k = min((bw - 30) / p.L, (bh - 26) / p.W)
    w, h = p.L * k, p.W * k
    x0, y0 = (bw - w) / 2 + 6, (bh - h) / 2 - 2
    fill = {"ЛДСП 16": "#efe7dc", "ЛДСП 26 (столешница)": "#c9a27c", "Задняя стенка 10": "#e6e6e6", "МДФ 18": "#e9e2ef"}[p.mat]
    s = [f'<svg viewBox="0 0 {bw} {bh}" width="{bw}" height="{bh}">',
         f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="#333" stroke-width="0.8"/>']
    sides = [((x0, y0 + h), (x0 + w, y0 + h)), ((x0, y0), (x0 + w, y0)), ((x0, y0), (x0, y0 + h)), ((x0 + w, y0), (x0 + w, y0 + h))]
    for ch, (a, b) in zip(p.edge, sides):
        if ch == "2":
            s.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#c0392b" stroke-width="3"/>')
        elif ch == "4":
            s.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#2f6fb0" stroke-width="1.6"/>')
    s.append(f'<text x="{x0 + w / 2:.1f}" y="{y0 + h + 11:.1f}" font-size="9" text-anchor="middle">{fmt(p.L)}</text>')
    s.append(f'<text x="{x0 - 4:.1f}" y="{y0 + h / 2:.1f}" font-size="9" text-anchor="middle" '
             f'transform="rotate(-90 {x0 - 4:.1f} {y0 + h / 2:.1f})">{fmt(p.W)}</text>')
    s.append("</svg>")
    return "".join(s)


CSS = """
@page { size: 420mm 297mm; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'DejaVu Sans', Arial, sans-serif; color: #111; }
.page { width: 420mm; height: 297mm; padding: 9mm 11mm 8mm; page-break-after: always; position: relative;
        display: flex; flex-direction: column; gap: 4mm; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.frame { position: absolute; inset: 5mm; border: 0.6mm solid #111; pointer-events: none; }
h1 { font-size: 15pt; margin: 0; }
.sub { font-size: 9pt; color: #444; margin-top: 1mm; }
.head { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 0.4mm solid #111; padding-bottom: 2mm; }
.stamp { font-size: 8.5pt; text-align: right; color: #333; }
table { border-collapse: collapse; width: 100%; font-size: 8.6pt; }
th, td { border: 0.25mm solid #777; padding: 1.1mm 1.6mm; text-align: left; vertical-align: top; }
th { background: #eee; font-weight: 700; }
td.n { text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }
tr.grp td { background: #f6f1ea; font-weight: 700; }
.cols { display: flex; gap: 6mm; flex: 1; min-height: 0; }
.cols > div { flex: 1; min-width: 0; }
.cards { display: grid; grid-template-columns: repeat(6, 1fr); gap: 2.5mm; align-content: start; }
.card { border: 0.3mm solid #999; padding: 1.5mm; font-size: 7.6pt; break-inside: avoid; }
.card b { font-size: 8pt; }
.legend { font-size: 8pt; display: flex; gap: 6mm; align-items: center; }
.sw { display: inline-block; width: 9mm; height: 0; vertical-align: middle; margin-right: 1.5mm; }
.note { font-size: 8.3pt; line-height: 1.45; }
.sum td { font-weight: 700; }
"""


def head(title, sub, sheet):
    return (f'<div class="head"><div><h1>{title}</h1><div class="sub">{sub}</div></div>'
            f'<div class="stamp">{sheet}<br>Размеры в мм · лист А3</div></div>')


RULES = ("Корпус — ЛДСП 16 мм; фасады — МДФ 18 мм; задняя стенка 10 мм накладная на тыльную сторону "
         "(глубина боковин и горизонтов = глубина корпуса − 10). Крыша и дно — между боковинами, стойки — "
         "между крышей и дном. Съёмные полки −2 мм по длине; глубина полок = глубина боковины − 20. "
         "Ящики Blum TANDEMBOX antaro M, NL 500: дно (LW − 75) × (NL − 24), задняя стенка (LW − 87) × 84 — "
         "проверить по каталогу Blum. Кромка ПВХ: Д — длина, Ш — ширина; 2 — 2 мм, 0,4 — 0,4 мм.")


def cut_page(title, sub, sheet, parts):
    rows = []
    by_mat = OrderedDict()
    for p in parts:
        by_mat.setdefault(p.mat, []).append(p)
    pos = 0
    totals = []
    for mat, ps in by_mat.items():
        rows.append(f'<tr class="grp"><td colspan="8">{mat}</td></tr>')
        area = e2 = e04 = 0
        for p in ps:
            pos += 1
            p.pos = pos
            a = p.L * p.W * p.qty / 1e6
            x2, x4 = edge_len(p)
            area += a
            e2 += x2
            e04 += x4
            rows.append(f"<tr><td class='n'>{pos}</td><td>{p.name}</td><td class='n'>{fmt(p.L)}</td>"
                        f"<td class='n'>{fmt(p.W)}</td><td class='n'>{p.qty}</td><td>{edge_text(p.edge)}</td>"
                        f"<td class='n'>{a:.2f}</td><td>{p.note}</td></tr>")
        totals.append((mat, area, e2, e04))
    tot_rows = "".join(f"<tr><td>{m}</td><td class='n'>{a:.2f} м²</td><td class='n'>{e2:.1f} м</td>"
                       f"<td class='n'>{e4:.1f} м</td></tr>" for m, a, e2, e4 in totals)
    table = ("<table><tr><th>№</th><th>Деталь</th><th>Длина</th><th>Ширина</th><th>Кол.</th><th>Кромка</th>"
             "<th>м²</th><th>Примечание</th></tr>" + "".join(rows) + "</table>")
    summary = ("<table class='sum'><tr><th>Материал</th><th>Площадь (без запаса)</th><th>Кромка 2 мм</th>"
               "<th>Кромка 0,4 мм</th></tr>" + tot_rows + "</table>")
    return (f'<div class="page"><div class="frame"></div>{head(title, sub, sheet)}'
            f'<div class="cols"><div style="flex:2.2">{table}</div>'
            f'<div><div class="note"><b>Правила раскроя</b><br>{RULES}</div><br>{summary}'
            f'<div class="note"><br>К площади добавить 10–15 % на раскрой; к кромке — 10 % и по 50 мм на торец.</div>'
            f'</div></div></div>')


def sketch_page(title, sub, sheet, parts):
    cards = "".join(f'<div class="card"><b>{p.pos}. {p.name}</b><br>{p.mat} · {p.qty} шт'
                    f'{part_svg(p)}<br>кромка: {edge_text(p.edge)}</div>' for p in parts)
    legend = ('<div class="legend"><span><span class="sw" style="border-top:3px solid #c0392b"></span>кромка 2 мм</span>'
              '<span><span class="sw" style="border-top:1.6px solid #2f6fb0"></span>кромка 0,4 мм</span>'
              '<span>Д1 — нижняя длинная сторона эскиза, Д2 — верхняя, Ш1 — левая, Ш2 — правая</span></div>')
    return (f'<div class="page"><div class="frame"></div>{head(title, sub, sheet)}{legend}'
            f'<div class="cards">{cards}</div></div>')


def hw_page(sheet):
    def block(title, hw):
        rows = []
        for grp, items in hw.items():
            rows.append(f'<tr class="grp"><td colspan="3">{grp}</td></tr>')
            rows += [f"<tr><td>{n}</td><td class='n'>{q}</td><td>{c}</td></tr>" for n, q, c in items]
        return (f"<h1 style='font-size:12pt;margin:0 0 2mm'>{title}</h1><table><tr><th>Наименование</th>"
                f"<th>Кол.</th><th>Где / примечание</th></tr>" + "".join(rows) + "</table>")
    return (f'<div class="page"><div class="frame"></div>'
            f'{head("ФУРНИТУРА", "шкаф со столом и шкаф с ящиками и тумба — отдельный лист", sheet)}'
            f'<div class="cols"><div>{block("Шкаф со столом", hw_shkaf3())}</div>'
            f'<div>{block("Шкаф с ящиками и тумба", hw_shkaf2())}'
            f'<div class="note"><br><b>Примечания.</b> Фурнитура — Blum (петли CLIP top BLUMOTION 110°, '
            f'ящики TANDEMBOX antaro). Количество крепежа дано с небольшим запасом. Петли: на дверях высотой '
            f'≈2000 — по 5 шт, на фасадах до 750 — по 2 шт. Полунакладные петли — где две двери крепятся '
            f'к одной стойке. Модели подсветки и подъёмников крышки подобрать у поставщика под вес фасадов.</div>'
            f'</div></div></div>')


def main():
    p3, p2 = parts_shkaf3(), parts_shkaf2()
    pages = [
        cut_page("ДЕТАЛИРОВКА — ШКАФ СО СТОЛОМ", "2400 × 600 × 2583, цоколь 50; стол 1200 × 600, тумба 400 с 4 ящиками",
                 "Лист 1", p3),
        sketch_page("ЭСКИЗЫ ДЕТАЛЕЙ — ШКАФ СО СТОЛОМ", "номера позиций — как в таблице деталировки", "Лист 2", p3),
        cut_page("ДЕТАЛИРОВКА — ШКАФ С ЯЩИКАМИ И ТУМБА",
                 "шкаф 1600 × 600 × 2645, цоколь 80; тумба 1565 × 500; фальш-планки 20", "Лист 3", p2),
        sketch_page("ЭСКИЗЫ ДЕТАЛЕЙ — ШКАФ С ЯЩИКАМИ И ТУМБА", "номера позиций — как в таблице деталировки",
                    "Лист 4", p2),
        hw_page("Лист 5"),
    ]
    html = f"<!doctype html><html lang='ru'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
    with open(os.path.join(HERE, "detal.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("parts:", len(p3), len(p2))


if __name__ == "__main__":
    main()
