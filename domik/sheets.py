#!/usr/bin/env python3
"""Листы А3: 1 — план каркаса (вид сверху, 1:50) с привязками стоек; 2 — 3D-виды и спецификация."""
import base64
import math
import os

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "DejaVu Sans, Arial, sans-serif"
RED = "#c0392b"
KG_M = 7.07          # масса трубы 80×80×3, кг/м (ГОСТ 30245)
STOCK = 12000        # длина хлыста, мм
KERF = 3             # пропил


class S:
    def __init__(s):
        s.o = []

    def e(s, x):
        s.o.append(x)

    def t(s, x, y, txt, size=2.5, anchor="middle", weight="normal", fill="#111", rot=None):
        r = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ""
        s.e(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}"{r}>{txt}</text>')

    def ln(s, x1, y1, x2, y2, w=0.2, c="#111", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.e(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}"{d}/>')

    def save(s, name, w=420, h=297):
        frame = (f'<rect x="5" y="5" width="{w-10}" height="{h-10}" fill="none" stroke="#111" stroke-width="0.4"/>')
        with open(os.path.join(HERE, name), "w") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">'
                    f'<rect width="{w}" height="{h}" fill="#fff"/>{frame}{"".join(s.o)}</svg>')


def header(s, title, sub, n):
    s.t(12, 17, title, 6, "start", "bold")
    s.t(12, 24, sub, 3, "start")
    s.t(408, 17, f"Лист {n}/2", 3.2, "end")


# ---------------------------------------------------------------- лист 1
K = 1 / 50
X0, Y0 = 45, 222          # точка (0,0) плана на листе; Y плана — вверх


def P(x, y):
    return X0 + x * K, Y0 - y * K


def chain(s, vals, fixed, o, off, small=False):
    """Цепочка размеров. vals — координаты вдоль линии; o='x' — горизонтальная (fixed — Y листа), 'y' — вертикальная."""
    fs = 2.0 if small else 2.3
    for a, b in zip(vals, vals[1:]):
        if o == "x":
            xa, xb = X0 + a * K, X0 + b * K
            s.ln(xa, fixed, xb, fixed, 0.15, RED)
            for xx in (xa, xb):
                s.ln(xx - 0.7, fixed + 0.7, xx + 0.7, fixed - 0.7, 0.3, RED)
            s.t((xa + xb) / 2, fixed - 0.8, f"{round(b - a)}", fs, fill=RED)
        else:
            ya, yb = Y0 - a * K, Y0 - b * K
            s.ln(fixed, ya, fixed, yb, 0.15, RED)
            for yy in (ya, yb):
                s.ln(fixed - 0.7, yy + 0.7, fixed + 0.7, yy - 0.7, 0.3, RED)
            s.t(fixed - 0.8, (ya + yb) / 2, f"{round(b - a)}", fs, fill=RED, rot=-90)


def posts_on(name):
    n, o, c, a, b, p = [l for l in M.LINES if l[0] == name][0]
    return sorted((x if o == "x" else y) for (x, y) in M.posts
                  if abs((y if o == "x" else x) - c) < 1 and a - 1 <= (x if o == "x" else y) <= b + 1)


def sheet1():
    s = S()
    header(s, "Металлический каркас домика — план (вид сверху)",
           "Труба профильная 80×80  |  Домик на сваях  |  Высота 3000  |  Шаг стоек ≤ 2000  |  Под перегородками — только нижняя обвязка  |  Размеры в мм, 1:50", 1)
    # контур дома (наружные грани) — тонко
    out = [(0, 0), (5400, 0), (5400, -1400), (9400, -1400), (9400, 6300), (0, 6300)]
    s.e('<path d="M' + "L".join(f"{P(*q)[0]:.2f} {P(*q)[1]:.2f}" for q in out) + 'Z" fill="#f6f4ef" stroke="#999" stroke-width="0.2"/>')
    # верхняя обвязка (видимая сверху) — серым, стойки — тёмным
    for m in M.members:
        if m["kind"] in ("верхняя обвязка", "обвязка под перегородку"):
            x0, y1 = P(m["x0"], m["y0"])
            x1, y0 = P(m["x1"], m["y1"])
            fill = "#aab1b9" if m["kind"] == "верхняя обвязка" else "#d9b98c"
            s.e(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1-x0:.2f}" height="{y1-y0:.2f}" fill="{fill}" stroke="#555" stroke-width="0.12"/>')
    # проёмы: разрыв нижней обвязки у дверей — штрих, окна — голубая линия снаружи
    for name, oa, ob, z0, z1, kind in M.OPENINGS:
        n, o, c, a, b, p = [l for l in M.LINES if l[0] == name][0]
        col = "#8a5a2b" if kind == "дверь" else "#2e86de"
        if o == "x":
            (xa, ya), (xb, _) = P(oa, c), P(ob, c)
            s.ln(xa, ya, xb, ya, 0.9, col)
            s.t((xa + xb) / 2, ya + (4.2 if c < 1000 else -2.2) * (1 if name != "В3" else -1), f"{kind} {ob-oa}", 1.9, fill=col)
        else:
            (xa, ya), (_, yb) = P(c, oa), P(c, ob)
            s.ln(xa, ya, xa, yb, 0.9, col)
            dx = -2.2 if c < 100 else (3.6 if c > 9000 else 2.6)
            s.t(xa + dx, (ya + yb) / 2, f"{kind} {ob-oa}", 1.9, fill=col, rot=-90)
    for (x, y) in M.posts:
        px, py = P(x, y)
        h = M.T * K
        s.e(f'<rect x="{px-h/2:.2f}" y="{py-h/2:.2f}" width="{h:.2f}" height="{h:.2f}" fill="#1f4e79" stroke="#000" stroke-width="0.1"/>')
    # цепочки по осям стоек снаружи
    top = P(0, 6300)[1]
    chain(s, posts_on("4"), top - 8, "x", 0)
    s.ln(X0, top - 15, X0 + 9400 * K, top - 15, 0.15, RED)
    s.t(X0 + 4700 * K, top - 15.8, "9400", 2.5, fill=RED, weight="bold")
    chain(s, posts_on("6"), X0 - 8, "y", 0)
    s.ln(X0 - 15, Y0, X0 - 15, Y0 - 6300 * K, 0.15, RED)
    s.t(X0 - 15.8, Y0 - 3150 * K, "6300", 2.5, fill=RED, weight="bold", rot=-90)
    r = X0 + 9400 * K
    chain(s, posts_on("5"), r + 8, "y", 0)
    s.ln(r + 15, Y0 + 1400 * K, r + 15, Y0 - 6300 * K, 0.15, RED)
    s.t(r + 14.2, Y0 - 2450 * K, "7700", 2.5, fill=RED, weight="bold", rot=-90)
    chain(s, posts_on("1"), Y0 + 8, "x", 0)
    chain(s, posts_on("3"), Y0 + 1400 * K + 8, "x", 0)
    s.ln(X0, Y0 + 1400 * K + 15, X0 + 9400 * K, Y0 + 1400 * K + 15, 0.15, RED)
    for a, b in ((0, 5400), (5400, 9400)):
        s.t(X0 + (a + b) / 2 * K, Y0 + 1400 * K + 14.2, str(b - a), 2.5, fill=RED, weight="bold")
    chain(s, [v for v in posts_on("2") if v <= 40], X0 + 5400 * K - 8, "y", 0)
    # привязка осей перегородок
    chain(s, [40, 3150, 4300, 6260], X0 + 3500 * K - 4, "y", 0, small=True)
    # номера стен
    for n, (x, y) in {"1": (2700, -900), "2": (4700, -900), "3": (7400, -2300), "4": (4700, 7500),
                      "5": (10600, 1000), "6": (-1050, 1300)}.items():
        px, py = P(x, y)
        s.e(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="2.6" fill="#fff" stroke="#111" stroke-width="0.3"/>')
        s.t(px, py + 1, n, 2.8, weight="bold")
    # помещения
    for name, (x, y) in {"П1а": (1750, 4700), "П1б": (1750, 1500), "П4": (4450, 5300),
                         "П2/3": (4450, 1300), "П5": (7400, 2400)}.items():
        px, py = P(x, y)
        s.t(px, py, name, 3, fill="#9a9a9a", weight="bold")
    # легенда и примечания
    X, Y = 268, 40
    s.t(X, Y, "Условные обозначения", 3.4, "start", "bold")
    items = [("#1f4e79", "Стойка 80×80, h = 2840 (между обвязками)"),
             ("#aab1b9", "Обвязка наружных стен (верхняя; нижняя — под ней)"),
             ("#d9b98c", "Обвязка под перегородку (только низ, без стоек)"),
             ("#2e86de", "Окно / витраж: перемычка сверху, ригель снизу"),
             ("#8a5a2b", "Дверь: в наружной стене — перемычка; во внутренней — без каркаса")]
    for i, (c, txt) in enumerate(items):
        yy = Y + 6 + i * 6
        if c in ("#2e86de", "#8a5a2b"):
            s.ln(X, yy - 1, X + 6, yy - 1, 0.9, c)
        else:
            s.e(f'<rect x="{X + (2 if c == "#1f4e79" else 0)}" y="{yy-2.5}" width="{2 if c == "#1f4e79" else 6}" height="2" fill="{c}" stroke="#000" stroke-width="0.1"/>')
        s.t(X + 9, yy, txt, 2.5, "start")
    Y += 42
    s.t(X, Y, "Решения по каркасу", 3.4, "start", "bold")
    notes = [
        "1. Всё из трубы 80×80 (стенка 3 мм), сварка.",
        "2. Домик на сваях: нижняя обвязка — несущая",
        "   рама пола, сплошная по всему контуру и под",
        "   перегородками, в дверях не разрезается.",
        "3. Наружные стены — труба внутрь от наружной",
        "   грани; оси перегородок — по исходному плану.",
        "4. Стойки — только в наружных стенах: в углах,",
        "   по обе стороны проёмов и промежуточные",
        "   с шагом не более 2000 мм (размеры — по осям).",
        "5. Над проёмами наружных стен — перемычка,",
        "   под окнами (низ 900) — подоконный ригель.",
        "6. Перегородки — без металлических стоек и",
        "   верхней обвязки: ставятся лёгкими (дерево /",
        "   ГКЛ) на обвязку под перегородку.",
        "7. Пролёты обвязок 9400 и 7540 — из хлыста 12 м;",
        "   сваи — под углами, примыканиями перегородок",
        "   и по нижней обвязке с шагом по расчёту.",
        "8. Крыша, раскосы, балки пола и оголовки свай —",
        "   по отдельному расчёту.",
    ]
    for i, txt in enumerate(notes):
        s.t(X, Y + 5.5 + i * 4.1, txt, 2.45, "start")
    Y += 5.5 + len(notes) * 4.1 + 6
    s.t(X, Y, f"Стоек: {len(M.posts)} шт.  ·  Трубы всего: {sum(L*n for (k, L), n in M.spec().items())/1000:.1f} м", 2.8, "start", "bold")
    s.t(X, Y + 5, "Спецификация и раскрой — лист 2", 2.6, "start")
    s.save("karkas_list1.svg")


# ---------------------------------------------------------------- лист 2
def pack(pieces):
    """Раскрой на хлысты STOCK (первый подходящий, по убыванию)."""
    bars = []
    for L in sorted(pieces, reverse=True):
        for b in bars:
            if sum(b) + len(b) * KERF + L <= STOCK:
                b.append(L)
                break
        else:
            bars.append([L])
    return bars


def sheet2():
    s = S()
    header(s, "Металлический каркас домика — 3D и спецификация",
           "Труба профильная 80×80×3  |  Обвязки — серые, под перегородками — коричневые, стойки — синие, перемычки — оранжевые, ригели — зелёные", 2)
    for i, (v, cap) in enumerate((("sw", "Вид с юго-запада (стены 1, 2, 3, 6)"), ("ne", "Вид с северо-востока (стены 4, 5); пол показан прозрачным"))):
        b64 = base64.b64encode(open(os.path.join(HERE, f"3d_{v}.png"), "rb").read()).decode()
        x = 12 + i * 133
        s.e(f'<image x="{x}" y="32" width="128" height="89.6" href="data:image/png;base64,{b64}"/>')
        s.e(f'<rect x="{x}" y="32" width="128" height="89.6" fill="none" stroke="#ccc" stroke-width="0.2"/>')
        s.t(x + 64, 126, cap, 2.6)
    # спецификация
    X, Y = 12, 140
    s.t(X, Y, "Спецификация (длины по факту реза)", 3.4, "start", "bold")
    cols = [X, X + 10, X + 70, X + 92, X + 108, X + 128]
    Y += 4
    s.e(f'<rect x="{X}" y="{Y}" width="152" height="6" fill="#eef1f4" stroke="#999" stroke-width="0.15"/>')
    for c, h in zip(cols, ["№", "Элемент", "Длина, мм", "Кол-во", "Всего, м", "Масса, кг"]):
        s.t(c + 1.5, Y + 4.2, h, 2.4, "start", "bold")
    Y += 6
    tot_m = tot_kg = 0
    rows = sorted(M.spec().items(), key=lambda r: (["нижняя обвязка", "обвязка под перегородку", "верхняя обвязка", "стойка", "перемычка", "подоконный ригель"].index(r[0][0]), -r[0][1]))
    for i, ((k, L), n) in enumerate(rows):
        m = L * n / 1000
        kg = m * KG_M
        tot_m += m
        tot_kg += kg
        s.e(f'<rect x="{X}" y="{Y}" width="152" height="4.6" fill="{"#fff" if i % 2 else "#fafafa"}" stroke="#ddd" stroke-width="0.1"/>')
        for c, v in zip(cols, [i + 1, k, L, n, f"{m:.2f}", f"{kg:.1f}"]):
            s.t(c + 1.5, Y + 3.3, str(v), 2.3, "start")
        Y += 4.6
    s.e(f'<rect x="{X}" y="{Y}" width="152" height="6" fill="#eef1f4" stroke="#999" stroke-width="0.15"/>')
    s.t(cols[1] + 1.5, Y + 4.2, "ИТОГО", 2.6, "start", "bold")
    s.t(cols[3] + 1.5, Y + 4.2, str(sum(M.spec().values())), 2.6, "start", "bold")
    s.t(cols[4] + 1.5, Y + 4.2, f"{tot_m:.1f}", 2.6, "start", "bold")
    s.t(cols[5] + 1.5, Y + 4.2, f"≈ {tot_kg:.0f}", 2.6, "start", "bold")
    # раскрой
    pieces = [L for (k, L), n in M.spec().items() for _ in range(n)]
    bars = pack(pieces)
    X2, Y2 = 280, 32
    s.t(X2, Y2, f"Раскрой на хлысты {STOCK // 1000} м (пропил {KERF} мм)", 3.4, "start", "bold")
    s.t(X2, Y2 + 5, f"Хлыстов: {len(bars)} шт. = {len(bars) * STOCK / 1000:.0f} м, отход "
        f"{(len(bars) * STOCK - sum(pieces)) / 1000:.1f} м ({(1 - sum(pieces) / (len(bars) * STOCK)) * 100:.0f}%)", 2.5, "start")
    sc = 120 / STOCK
    yy = Y2 + 10
    for j, b in enumerate(bars):
        s.t(X2, yy + 2.6, f"{j+1}", 2.2, "start")
        x = X2 + 5
        s.e(f'<rect x="{x}" y="{yy}" width="{STOCK*sc:.2f}" height="3.6" fill="#f2f2f2" stroke="#999" stroke-width="0.12"/>')
        for L in b:
            w = L * sc
            s.e(f'<rect x="{x:.2f}" y="{yy}" width="{w:.2f}" height="3.6" fill="#cfd8e3" stroke="#1f4e79" stroke-width="0.15"/>')
            if w > 7:
                s.t(x + w / 2, yy + 2.65, str(L), 1.9)
            x += w + KERF * sc
        yy += 4.6
    yy += 5
    s.t(X2, yy, "Примечания", 3.2, "start", "bold")
    for i, txt in enumerate([
        f"• Масса: {KG_M} кг/м для 80×80×3 (ГОСТ 30245); при стенке 4 мм —",
        "  ≈ 9,2 кг/м, масса вырастет примерно на 30%.",
        "• Длинные обвязки 9400 и 7540 — цельными из хлыста 12 м;",
        "  если хлысты 6 м — стык со вставкой-накладкой над стойкой.",
        "• Запас на брак и подгонку — +5% к закупке.",
        "• Раскосы жёсткости в углах и кровля в расчёт не входят.",
    ]):
        s.t(X2, yy + 5 + i * 4, txt, 2.35, "start")
    s.save("karkas_list2.svg")


if __name__ == "__main__":
    assert M.check() == 0
    sheet1()
    sheet2()
