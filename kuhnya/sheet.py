#!/usr/bin/env python3
"""Чертёж угловой кухни по заводскому чертежу (DRUID) + остров, лист А2, масштаб 1:20."""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                          # noqa: E402
from generate import e, text, line, rect, dim_h, dim_v       # noqa: E402
from geom import (H, PL, BT, TOP, UB, U_MID, BD, UD, FD, W_MAIN, W_SIDE, SIDE_X, FRIDGE, OVEN_COL,  # noqa: E402
                  FR_LOW, FR_DOOR, TOP_ROW, OC_DRAWER, MW, OVEN, OC_DOOR, BASE_800, CORNER, CORNER_FRONT,
                  CORNER_FILL, FRONT_SPLIT, SINK, DW, SIDE_END, UPPER_MAIN, UPPER_SIDE, U_SIDE_X, ISLAND)

S = 1 / 20
FACADE = "#ebe7e2"
QUARTZ = "#d6d2cc"
CORPUS = "#ece7e1"
DARK = "#2b2b2d"
LEDC = "#f0a800"


class V:
    def __init__(self, ox, fy):
        self.ox, self.fy = ox, fy

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    def box(self, x0, x1, z0, z1, fill=FACADE, sw=0.25, stroke="#111", dash=None):
        rect(self.X(x0), self.Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, stroke=stroke, sw=sw, dash=dash)


def stone(v, x0, x1, z0, z1):
    v.box(x0, x1, z0, z1, fill=QUARTZ)
    rnd = random.Random(int(x0 * 7 + z0))
    for _ in range(int((x1 - x0) * (z1 - z0) / 9000)):
        e(f'<circle cx="{v.X(rnd.uniform(x0 + 5, x1 - 5)):.2f}" cy="{v.Z(rnd.uniform(z0 + 5, z1 - 5)):.2f}" r="0.12" fill="#9b958e"/>')


def front(v, x0, x1, z0, z1, label=None, gola=False, fill=FACADE):
    v.box(x0 + 1.5, x1 - 1.5, z0, z1, fill=fill)
    if gola:                                     # интегрированная ручка
        line(v.X(x0 + 1.5), v.Z(z1 - 15), v.X(x1 - 1.5), v.Z(z1 - 15), w=0.35, color="#2a2826")
    if label:
        text(v.X((x0 + x1) / 2), v.Z((z0 + z1) / 2) + 0.8, label, size=2.0, fill="#555")


def swing(v, x0, x1, z0, z1, hinge_left):
    hx, fx = (x0, x1) if hinge_left else (x1, x0)
    for zz in (z0, z1):
        line(v.X(hx), v.Z(zz), v.X(fx), v.Z((z0 + z1) / 2), w=0.12, color="#999", dash="1 0.8")


def legs(v, x0, x1):
    v.box(x0 + 40, x1 - 40, 0, PL, fill="#b0a9a2", sw=0.2)


# ---------------------------------------------------------------------------
def view_main(ox, fy):
    v = V(ox, fy)
    text(v.X(W_MAIN / 2), v.Z(H) - 20, "ФАСАД — ОСНОВНАЯ СТЕНА", size=3.4, weight="bold")
    text(v.X(W_MAIN / 2), v.Z(H) - 15.5, "по заводскому чертежу «Габариты изделия»", size=2.1)
    line(v.X(-150), v.Z(0), v.X(W_MAIN + 150), v.Z(0), w=0.45)
    # пенал холодильника
    x0, x1 = FRIDGE
    legs(v, x0, x1)
    front(v, x0, x1, *FR_LOW, gola=True)
    front(v, x0, x1, *FR_DOOR, "встр. холодильник")
    front(v, x0, x1, *TOP_ROW)
    for z in (FR_LOW, FR_DOOR, TOP_ROW):
        swing(v, x0, x1, *z, True)
    # пенал ДШ + СВЧ
    x0, x1 = OVEN_COL
    legs(v, x0, x1)
    front(v, x0, x1, *OC_DRAWER, gola=True)
    v.box(x0 + 2, x1 - 2, *MW, fill=DARK)
    text(v.X((x0 + x1) / 2), v.Z(sum(MW) / 2) + 0.8, "СВЧ", size=2.4, fill="#ddd", weight="bold")
    v.box(x0 + 2, x1 - 2, *OVEN, fill=DARK)
    text(v.X((x0 + x1) / 2), v.Z(sum(OVEN) / 2) + 0.8, "ДШ", size=2.4, fill="#ddd", weight="bold")
    front(v, x0, x1, *OC_DOOR)
    front(v, x0, x1, *TOP_ROW)
    swing(v, x0, x1, *OC_DOOR, False)
    swing(v, x0, x1, *TOP_ROW, False)
    # нижний ряд
    x0, x1 = BASE_800
    legs(v, x0, x1)
    m = (x0 + x1) / 2
    front(v, x0, m, PL + 2, BT - 2, gola=True)
    front(v, m, x1, PL + 2, BT - 2, gola=True)
    swing(v, x0, m, PL + 2, BT - 2, True)
    swing(v, m, x1, PL + 2, BT - 2, False)
    v.box(x0 + 100, x1 - 100, TOP, TOP + 8, fill=DARK, sw=0.2)
    text(v.X(m), v.Z(TOP + 60), "варочная*", size=1.6, fill="#555")
    legs(v, CORNER[0], SIDE_X)
    fa, fb = CORNER_FRONT
    front(v, fa, fb, PL + 2, FRONT_SPLIT - 3, gola=True)
    front(v, fa, fb, FRONT_SPLIT + 3, BT - 2, gola=True)
    swing(v, fa, fb, PL + 2, FRONT_SPLIT - 3, False)
    swing(v, fa, fb, FRONT_SPLIT + 3, BT - 2, False)
    v.box(*CORNER_FILL, PL + 2, BT - 2)
    # торец бокового ряда
    v.box(SIDE_X, W_MAIN, 0, BT, fill="#e3ded8")
    text(v.X((SIDE_X + W_MAIN) / 2), v.Z(450), "торец бок. ряда", size=1.6, fill="#555")
    stone(v, 1200, W_MAIN, BT, TOP)
    stone(v, 1200, U_SIDE_X, TOP, UB)
    # верхние шкафы
    for x0, x1, n in UPPER_MAIN:
        w = (x1 - x0) / n
        for k in range(n):
            a, b = x0 + k * w, x0 + (k + 1) * w
            hl = k == 0 and n > 1
            front(v, a, b, UB + 2, U_MID - 2)
            front(v, a, b, *TOP_ROW)
            swing(v, a, b, UB + 2, U_MID - 2, hl)
    v.box(U_SIDE_X, W_MAIN, UB, H, fill="#e3ded8")                    # торец боковых верхних
    rect(v.X(1200), v.Z(UB) - 0.1, (W_MAIN - 1200) * S, 0.7, fill=LEDC, stroke="none")
    # размеры
    yt = v.Z(H) - 4
    pts = [0, 600, 1200, 1995, 2790, W_MAIN]
    for a, b in zip(pts, pts[1:]):
        dim_h(v.X(a), v.X(b), yt, str(b - a), ext_from=v.Z(H), size=1.8)
    dim_h(v.X(0), v.X(W_MAIN), yt - 6, str(W_MAIN))
    yb = v.Z(0) + 9
    pts = [0, 600, 1200, 2000, 3100, W_MAIN]
    for a, b in zip(pts, pts[1:]):
        dim_h(v.X(a), v.X(b), yb, str(b - a), ext_from=v.Z(0) + 1, size=1.8)
    xr = v.X(W_MAIN) + 5
    for a, b in ((0, PL), (PL, BT), (BT, TOP), (TOP, UB), (UB, H)):
        dim_v(v.Z(b), v.Z(a), xr, str(b - a), ext_from=v.X(W_MAIN), size=1.7)
    dim_v(v.Z(H), v.Z(0), xr + 6, str(H))
    xl = v.X(0) - 5
    for a, b in ((0, PL), (PL, FR_LOW[1]), (FR_LOW[1], FR_DOOR[1]), (FR_DOOR[1], H)):
        dim_v(v.Z(b), v.Z(a), xl, str(round(b - a)), ext_from=v.X(0), size=1.6)
    dim_v(v.Z(H), v.Z(PL), xl - 6, "2700 пенал", size=1.7)
    text(v.X(1300), v.Z(UB) + 3, "LED врезная под верхними шкафами", size=1.6, anchor="start", fill="#8a6100")
    return v


def view_side(ox, fy):
    """Фасад боковой стены: горизонталь – y (0 = основная стена, слева)."""
    v = V(ox, fy)
    text(v.X(W_SIDE / 2), v.Z(H) - 20, "ФАСАД — БОКОВАЯ СТЕНА", size=3.4, weight="bold")
    text(v.X(W_SIDE / 2), v.Z(H) - 15.5, "мойка, ПММ 450, сушилка", size=2.1)
    line(v.X(-150), v.Z(0), v.X(W_SIDE + 150), v.Z(0), w=0.45)
    v.box(0, BD, 0, BT, fill="url(#hatch)")                         # угол – основной ряд в разрезе
    v.box(0, UD, UB, H, fill="url(#hatch)")
    v.box(UD, UPPER_SIDE[0][0], UB, H, fill="#e3ded8")
    for y0, y1 in (SINK, DW):
        legs(v, y0, y1)
    front(v, *SINK, PL + 2, FRONT_SPLIT - 3, gola=True)
    front(v, *SINK, FRONT_SPLIT + 3, BT - 2, gola=True)
    swing(v, *SINK, PL + 2, FRONT_SPLIT - 3, True)
    swing(v, *SINK, FRONT_SPLIT + 3, BT - 2, True)
    text(v.X(sum(SINK) / 2), v.Z(BT - 120), "мойка", size=1.8, fill="#555")
    front(v, *DW, PL + 2, BT - 2, "ПММ 450", gola=True)
    v.box(*SIDE_END, PL, BT)
    stone(v, 0, W_SIDE, BT, TOP)
    stone(v, UD, W_SIDE, TOP, UB)
    line(v.X(sum(SINK) / 2), v.Z(TOP), v.X(sum(SINK) / 2), v.Z(TOP + 300), w=0.5)
    for i, (y0, y1, n) in enumerate(UPPER_SIDE):
        w = (y1 - y0) / n
        for k in range(n):
            a, b = y0 + k * w, y0 + (k + 1) * w
            front(v, a, b, UB + 2, U_MID - 2, "сушилка" if i == 0 else None)
            front(v, a, b, *TOP_ROW)
            swing(v, a, b, UB + 2, U_MID - 2, k == 0)
    rect(v.X(UD), v.Z(UB) - 0.1, (W_SIDE - UD) * S, 0.7, fill=LEDC, stroke="none")
    yt = v.Z(H) - 4
    pts = [0, 600, 1070, W_SIDE]
    for a, b in zip(pts, pts[1:]):
        dim_h(v.X(a), v.X(b), yt, str(b - a), ext_from=v.Z(H), size=1.8)
    dim_h(v.X(0), v.X(W_SIDE), yt - 6, str(W_SIDE))
    yb = v.Z(0) + 9
    pts = [0, 600, 1300, 1750, W_SIDE]
    for a, b in zip(pts, pts[1:]):
        dim_h(v.X(a), v.X(b), yb, str(b - a), ext_from=v.Z(0) + 1, size=1.8)
    xr = v.X(W_SIDE) + 5
    for a, b in ((0, TOP), (TOP, UB), (UB, H)):
        dim_v(v.Z(b), v.Z(a), xr, str(b - a), ext_from=v.X(W_SIDE), size=1.8)
    dim_v(v.Z(H), v.Z(0), xr + 6, str(H))
    for a, b in ((PL, FRONT_SPLIT), (FRONT_SPLIT, BT)):
        dim_v(v.Z(b), v.Z(a), v.X(SINK[0]) + 2.2, str(b - a - 3), size=1.3)
    return v


def view_island(ox, fy):
    v = V(ox, fy)
    ix0, ix1, iy0, iy1 = ISLAND
    W = ix1 - ix0
    text(v.X(W / 2 + 300), v.Z(H) - 20, "ОСТРОВ", size=3.4, weight="bold")
    text(v.X(W / 2 + 300), v.Z(H) - 15.5, "из дизайн-проекта, ящики к кухне", size=2.1)
    line(v.X(-150), v.Z(0), v.X(W + 1100), v.Z(0), w=0.45)
    legs(v, 0, W)
    h = (BT - 2 - PL - 2 - 6) / 3
    for x0, x1 in ((0, W / 2), (W / 2, W)):
        for i in range(3):
            z0 = PL + 2 + i * (h + 3)
            front(v, x0, x1, z0, z0 + h, gola=True)
    stone(v, -20, W + 20, BT, TOP)
    yb = v.Z(0) + 9
    dim_h(v.X(0), v.X(W / 2), yb, "600", ext_from=v.Z(0) + 1, size=1.9)
    dim_h(v.X(W / 2), v.X(W), yb, "600", ext_from=v.Z(0) + 1, size=1.9)
    xl = v.X(-20) - 5
    for a, b in ((0, PL), (PL, BT), (BT, TOP)):
        dim_v(v.Z(b), v.Z(a), xl, str(b - a), ext_from=v.X(-20), size=1.7)
    s0 = W + 450
    legs(v, s0, s0 + 600)
    v.box(s0, s0 + FD, PL + 2, BT - 2)
    v.box(s0 + 600 - FD, s0 + 600, PL, BT)
    for i in range(3):
        z0 = PL + 2 + i * (h + 3)
        v.box(s0 + FD, s0 + FD + 480, z0 + 20, z0 + 160, fill="#f1ede7", sw=0.15)
    stone(v, s0 - 20, s0 + 620, BT, TOP)
    dim_h(v.X(s0 - 20), v.X(s0 + 620), yb, "640", ext_from=v.Z(0) + 1, size=1.7)
    text(v.X(s0 + 300), v.Z(TOP) - 3, "разрез", size=1.8, fill="#555")


def view_plan(ox, oy):
    def P(x, y):
        return ox + x * S, oy + y * S
    text(ox + W_MAIN / 2 * S, oy - 12, "ПЛАН", size=3.4, weight="bold")
    rect(*P(-200, -100), (W_MAIN + 300) * S, 100 * S, fill="url(#hatch)", sw=0.25)
    rect(*P(W_MAIN, 0), 100 * S, 2300 * S, fill="url(#hatch)", sw=0.25)

    def prect(x0, x1, y0, y1, **kw):
        a, b = P(x0, y0)
        rect(a, b, (x1 - x0) * S, (y1 - y0) * S, **kw)
    prect(*FRIDGE, 0, BD, fill=CORPUS, sw=0.3)
    prect(*OVEN_COL, 0, BD, fill=CORPUS, sw=0.3)
    prect(1200, W_MAIN, 0, BD, fill=QUARTZ, sw=0.3)
    prect(SIDE_X, W_MAIN, BD, W_SIDE, fill=QUARTZ, sw=0.3)
    for x in (2000,):
        line(*P(x, 0), *P(x, BD), w=0.2)
    line(*P(SIDE_X, BD), *P(W_MAIN, BD), w=0.2, dash="1 0.7")
    line(*P(SIDE_X, DW[0]), *P(W_MAIN, DW[0]), w=0.2)
    for x, y, s in ((300, 300, "холод."), (900, 300, "ДШ+СВЧ"), (1600, 470, "2 двери"), (2250, 470, "угол 1100"),
                    (2850, 950, "мойка"), (2850, 1520, "ПММ")):
        text(*P(x, y), s, size=1.8, fill="#444")
    prect(SIDE_X + 80, W_MAIN - 60, SINK[0] + 100, SINK[1] - 100, fill="#b9bcbf", sw=0.2)
    for cx, cy, r in ((1460, 160, 95), (1740, 160, 75), (1460, 430, 75), (1740, 430, 95)):
        e(f'<circle cx="{P(cx, cy)[0]:.2f}" cy="{P(cx, cy)[1]:.2f}" r="{r * S:.2f}" fill="none" stroke="#333" stroke-width="0.2"/>')
    prect(1200, W_MAIN, 0, UD, fill="none", stroke="#666", sw=0.2, dash="1.5 1")
    prect(U_SIDE_X, W_MAIN, UD, W_SIDE, fill="none", stroke="#666", sw=0.2, dash="1.5 1")
    ix0, ix1, iy0, iy1 = ISLAND
    prect(ix0 - 20, ix1 + 20, iy0 - 20, iy1 + 20, fill=QUARTZ, sw=0.3)
    line(*P((ix0 + ix1) / 2, iy0), *P((ix0 + ix1) / 2, iy1), w=0.2)
    text(*P((ix0 + ix1) / 2, (iy0 + iy1) / 2), "остров", size=1.8, fill="#444")
    dim_h(P(0, 0)[0], P(W_MAIN, 0)[0], oy - 6, str(W_MAIN), size=1.8)
    dim_h(P(0, 0)[0], P(SIDE_X, 0)[0], P(0, BD)[1] + 5, str(SIDE_X) + " (≈2543 по столешнице)", size=1.6)
    xr = P(W_MAIN + 100, 0)[0] + 5
    dim_v(oy, P(0, W_SIDE)[1], xr, str(W_SIDE), size=1.8)
    dim_v(P(0, BD)[1], P(0, W_SIDE)[1], P(SIDE_X, 0)[0] - 4, "1200", size=1.6)
    dim_h(P(U_SIDE_X, 0)[0], P(W_MAIN, 0)[0], P(0, W_SIDE)[1] + 4, "340", size=1.5)
    dim_h(P(SIDE_X, 0)[0], P(W_MAIN, 0)[0], P(0, W_SIDE)[1] + 9, "600", size=1.6)
    xi = P(ix0 - 20, 0)[0] - 4
    dim_v(P(0, BD)[1], P(0, iy0)[1], xi, str(iy0 - BD), size=1.6)
    dim_v(P(0, iy0)[1], P(0, iy1)[1], xi, str(iy1 - iy0), size=1.6)
    dim_h(P(ix0, 0)[0], P(ix1, 0)[0], P(0, iy1)[1] + 5, "600 + 600", size=1.6)


def notes(x, y):
    text(x, y, "ПРИМЕЧАНИЯ", size=3.0, weight="bold", anchor="start")
    rows = [
        "Габариты — по заводскому чертежу: основная стена 3150, боковая 1800, высота 2800.",
        "Опоры 100, нижние корпуса до 860, столешница 40, фартук 600, верхние шкафы 1300 (два ряда фасадов, верх 318).",
        "Пенал холодильника 600: нижняя дверца, встроенный холодильник, верхняя дверца.",
        "Пенал 600: ящик, СВЧ, духовой шкаф, дверца (полки 300), верхняя дверца.",
        "Основной ряд: модуль 800 (2 двери), угловой 1100 (фасад 500 в два яруса 365 / 363 + планка 50).",
        "Боковой ряд: мойка 700 (две дверцы ярусами), ПММ 450, планка 50; над мойкой — сушилка (470).",
        "Верхние шкафы: 795 / 795 / 360 и 470 / 730, глубина 340.",
        "Материалы корпуса и фасадов — ЛДСП Egger; фурнитура Blum; подсветка врезная.",
        "Открывание: низ — интегрированная ручка, верх — Push.",
        "Остров 1200 × 600 — из дизайн-проекта (в заводском чертеже нет). * Варочная — уточнить место.",
    ]
    for i, s in enumerate(rows):
        text(x, y + 5.5 + i * 4.3, s, size=2.25, anchor="start")


def title_block():
    bx, by, bw, bh = 455, 372, 125, 38
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 13, bx + bw, by + 13, w=0.3)
    line(bx + 80, by + 13, bx + 80, by + bh, w=0.3)
    text(bx + bw / 2, by + 6, "КУХОННЫЙ ГАРНИТУР", size=3.8, weight="bold")
    text(bx + bw / 2, by + 10.5, "угловой + остров", size=2.3)
    text(bx + 3, by + 19, f"{W_MAIN} × {W_SIDE} × {H} мм", size=2.3, anchor="start")
    text(bx + 3, by + 25, "ЛДСП Egger, Blum", size=2.3, anchor="start")
    text(bx + 3, by + 31, "Размеры в мм", size=2.3, anchor="start")
    text(bx + 100, by + 20, "Масштаб", size=2.2)
    text(bx + 100, by + 26, "1:20", size=3.4, weight="bold")
    text(bx + 100, by + 33, "Лист 1 (А2)", size=2.2)


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)
    fy = 190
    view_main(45, fy)
    view_side(270, fy)
    view_island(410, fy)
    view_plan(45, 255)
    notes(250, 262)
    title_block()
    e('</svg>')
    with open(os.path.join(HERE, "kuhnya.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


if __name__ == "__main__":
    main()
