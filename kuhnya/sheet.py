#!/usr/bin/env python3
"""Чертёж кухни с островом (кухня-гостиная), лист А2, масштаб 1:20."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                          # noqa: E402
from generate import e, text, line, rect, dim_h, dim_v, leader  # noqa: E402
from geom import (CEIL, PL, BT, TOP, BD, FD, UD, CTD, UB, UT, MAIN, FILLER_MAIN, LEFT, FILLER_LEFT,  # noqa: E402
                  UPPER_MAIN, UPPER_LEFT, ISLAND, TALL_DRAWER, OVEN, MW, TALL_TOP, FRIDGE_DOOR, FRIDGE_TOP)

S = 1 / 20
FACADE = "#e7e3de"
QUARTZ = "#d6d2cc"
CORPUS = "#ece7e1"
DARK = "#2b2b2d"
LEDC = "#f0a800"


class V:
    def __init__(self, ox, fy, flip=False):
        self.ox, self.fy, self.flip = ox, fy, flip

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    def box(self, x0, x1, z0, z1, fill=FACADE, sw=0.25, stroke="#111", dash=None):
        rect(self.X(x0), self.Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, stroke=stroke, sw=sw, dash=dash)


def stone(v, x0, x1, z0, z1, n=None):
    v.box(x0, x1, z0, z1, fill=QUARTZ, sw=0.25)
    import random
    rnd = random.Random(int(x0 * 7 + z0))
    for _ in range(n or int((x1 - x0) * (z1 - z0) / 9000)):
        px, pz = rnd.uniform(x0 + 5, x1 - 5), rnd.uniform(z0 + 5, z1 - 5)
        e(f'<circle cx="{v.X(px):.2f}" cy="{v.Z(pz):.2f}" r="0.12" fill="#9b958e"/>')


def three(z_lo=PL + 2, z_hi=BT - 2):
    h = (z_hi - z_lo - 6) / 3
    return [(z_lo + i * (h + 3), z_lo + i * (h + 3) + h) for i in range(3)]


def front(v, x0, x1, z0, z1, label=None, fill=FACADE, gola=True):
    v.box(x0 + 1.5, x1 - 1.5, z0, z1, fill=fill)
    if gola:
        line(v.X(x0 + 1.5), v.Z(z1 - 12), v.X(x1 - 1.5), v.Z(z1 - 12), w=0.35, color="#2a2826")
    if label:
        text(v.X((x0 + x1) / 2), v.Z((z0 + z1) / 2) + 0.8, label, size=2.0, fill="#555")


def swing(v, x0, x1, z0, z1, hinge_left):
    hx, fx = (x0, x1) if hinge_left else (x1, x0)
    for zz in (z0, z1):
        line(v.X(hx), v.Z(zz), v.X(fx), v.Z((z0 + z1) / 2), w=0.12, color="#999", dash="1 0.8")


# ---------------------------------------------------------------------------
def view_main(ox, fy):
    """Развёртка стены 10–9: нижний ряд, пенал ДШ+СВЧ, верхние шкафы."""
    v = V(ox, fy)
    W = FILLER_MAIN[1]
    text(v.X(W / 2), v.Z(CEIL) - 20, "РАЗВЁРТКА СТЕНЫ 10–9", size=3.4, weight="bold")
    text(v.X(W / 2), v.Z(CEIL) - 15.5, "кухня, вид из комнаты", size=2.1)
    rect(v.X(-100), v.Z(CEIL + 100), (W + 300) * S, 100 * S, fill="url(#hatch)", sw=0.25)
    line(v.X(-150), v.Z(0), v.X(W + 250), v.Z(0), w=0.45)
    for x0, x1, kind in MAIN:
        v.box(x0 + 40, x1 - 40, 0, PL, fill="#a9a29b", sw=0.2)
    # угол (глухой) – в разрезе левый ряд
    v.box(0, 600, PL, BT, fill="url(#hatch)", sw=0.25)
    text(v.X(300), v.Z(500), "угол", size=2.0, fill="#555")
    for x0, x1, kind in MAIN:
        if kind == "sink":
            m = (x0 + x1) / 2
            front(v, x0, m, PL + 2, BT - 2)
            front(v, m, x1, PL + 2, BT - 2)
            swing(v, x0, m, PL + 2, BT - 2, True)
            swing(v, m, x1, PL + 2, BT - 2, False)
            text(v.X(m), v.Z(BT - 120), "мойка", size=1.8, fill="#555")
            line(v.X(m), v.Z(TOP), v.X(m), v.Z(TOP + 300), w=0.5)
            line(v.X(m), v.Z(TOP + 300), v.X(m + 160), v.Z(TOP + 300), w=0.5)
        elif kind == "dw":
            front(v, x0, x1, PL + 2, BT - 2, "ПММ")
        elif kind == "hob":
            front(v, x0, x1, PL + 2, 470)
            front(v, x0, x1, 476, BT - 2)
            v.box(x0 + 5, x1 - 5, TOP, TOP + 8, fill=DARK, sw=0.2)
            text(v.X((x0 + x1) / 2), v.Z(600), "варочная", size=1.7, fill="#555")
        elif kind == "drawers":
            for z0, z1 in three():
                front(v, x0, x1, z0, z1)
        elif kind == "tall":
            front(v, x0, x1, *TALL_DRAWER)
            v.box(x0 + 2, x1 - 2, *OVEN, fill=DARK, sw=0.3)
            text(v.X((x0 + x1) / 2), v.Z((OVEN[0] + OVEN[1]) / 2) + 0.8, "ДШ", size=2.4, fill="#ddd", weight="bold")
            v.box(x0 + 2, x1 - 2, MW[0] + 3, MW[1] - 3, fill=DARK, sw=0.3)
            text(v.X((x0 + x1) / 2), v.Z((MW[0] + MW[1]) / 2) + 0.8, "СВЧ", size=2.4, fill="#ddd", weight="bold")
            front(v, x0, x1, *TALL_TOP, gola=False)
            swing(v, x0, x1, *TALL_TOP, False)
    v.box(*FILLER_MAIN, PL, UT, fill=FACADE)
    # столешница и фартук – искусственный камень
    stone(v, 0, 3000, BT, TOP)
    stone(v, 0, 3000, TOP, UB)
    # верхние шкафы
    xs = UPPER_MAIN
    for i in range(len(xs) - 1):
        front(v, xs[i], xs[i + 1], UB + 2, UT - 4, gola=False)
        swing(v, xs[i], xs[i + 1], UB + 2, UT - 4, i % 2 == 0)
    rect(v.X(0), v.Z(UB) - 0.1, 3000 * S, 0.7, fill=LEDC, stroke="none")
    v.box(1810, 2390, UB - 60, UB, fill="#c9c9c9", sw=0.2)          # вытяжка
    text(v.X(2100), v.Z(UB - 30) + 0.7, "вытяжка", size=1.6, fill="#333")
    # размеры
    yb = v.Z(0) + 9
    for x0, x1, kind in MAIN:
        dim_h(v.X(x0), v.X(x1), yb, str(x1 - x0), ext_from=v.Z(0) + 1, size=1.9)
    dim_h(v.X(FILLER_MAIN[0]), v.X(FILLER_MAIN[1]), yb - 4, "20", ext_from=v.Z(0) + 1, size=1.4)
    dim_h(v.X(0), v.X(W), yb + 6, str(W))
    yt = v.Z(CEIL + 100) - 4
    for i in range(len(xs) - 1):
        dim_h(v.X(xs[i]), v.X(xs[i + 1]), yt, str(xs[i + 1] - xs[i]), ext_from=v.Z(UT), size=1.6)
    xl = v.X(0) - 5
    for a, b in ((0, PL), (PL, BT), (BT, TOP), (TOP, UB), (UB, UT)):
        dim_v(v.Z(b), v.Z(a), xl, str(b - a), ext_from=v.X(0), size=1.7)
    dim_v(v.Z(CEIL), v.Z(0), xl - 6, str(CEIL))
    xr = v.X(W) + 5
    for a, b in ((0, TALL_DRAWER[1]), (OVEN[0], OVEN[1]), (MW[0], MW[1]), (TALL_TOP[0], UT)):
        dim_v(v.Z(b), v.Z(a), xr, str(round(b - a)), ext_from=v.X(W), size=1.5)
    text(v.X(1500), v.Z(1180), "фартук и столешница — искусственный камень", size=2.0, fill="#444")
    text(v.X(20), v.Z(UB) + 3, "LED-лента под верхними шкафами", size=1.7, anchor="start", fill="#8a6100")
    return v


def view_left(ox, fy):
    """Развёртка стены 10–11/12 (вид из комнаты): угол, ящики 480, пенал холодильника."""
    v = V(ox, fy)           # горизонталь – y (от стены 10–9)
    W = FILLER_LEFT[1]
    text(v.X(W / 2), v.Z(CEIL) - 20, "РАЗВЁРТКА СТЕНЫ 10–11/12", size=3.4, weight="bold")
    text(v.X(W / 2), v.Z(CEIL) - 15.5, "угловой ряд и холодильник", size=2.1)
    rect(v.X(-100), v.Z(CEIL + 100), (W + 200) * S, 100 * S, fill="url(#hatch)", sw=0.25)
    line(v.X(-150), v.Z(0), v.X(W + 150), v.Z(0), w=0.45)
    v.box(0, BD, 0, BT, fill="url(#hatch)", sw=0.25)                 # нижний ряд стены 10–9 в разрезе
    text(v.X(300), v.Z(450), "ряд 10–9", size=1.8, fill="#555")
    for y0, y1, kind in LEFT:
        v.box(y0 + 40, y1 - 40, 0, PL, fill="#a9a29b", sw=0.2)
        if kind == "drawers480":
            for z0, z1 in three():
                front(v, y0, y1, z0, z1)
        else:
            front(v, y0, y1, *FRIDGE_DOOR, "встр. холодильник", gola=False)
            swing(v, y0, y1, *FRIDGE_DOOR, False)
            front(v, y0, y1, *FRIDGE_TOP, gola=False)
            swing(v, y0, y1, *FRIDGE_TOP, False)
    v.box(*FILLER_LEFT, PL, UT, fill=FACADE)
    stone(v, 0, LEFT[0][1], BT, TOP)
    stone(v, 0, LEFT[0][1], TOP, UB)
    v.box(0, UD, UB, UT, fill="url(#hatch)", sw=0.25)                 # угловой верхний шкаф (боковина)
    ys = UPPER_LEFT
    for i in range(len(ys) - 1):
        front(v, ys[i], ys[i + 1], UB + 2, UT - 4, gola=False)
        swing(v, ys[i], ys[i + 1], UB + 2, UT - 4, i == 0)
    rect(v.X(UD), v.Z(UB) - 0.1, (ys[-1] - UD) * S, 0.7, fill=LEDC, stroke="none")
    yb = v.Z(0) + 9
    dim_h(v.X(0), v.X(BD), yb, "600", ext_from=v.Z(0) + 1, size=1.9)
    for y0, y1, kind in LEFT:
        dim_h(v.X(y0), v.X(y1), yb, str(y1 - y0), ext_from=v.Z(0) + 1, size=1.9)
    dim_h(v.X(FILLER_LEFT[0]), v.X(FILLER_LEFT[1]), yb - 4, "20", ext_from=v.Z(0) + 1, size=1.4)
    dim_h(v.X(0), v.X(W), yb + 6, str(W))
    yt = v.Z(CEIL + 100) - 4
    for a, b in ((0, UD), (UD, ys[1]), (ys[1], ys[2])):
        dim_h(v.X(a), v.X(b), yt, str(b - a), ext_from=v.Z(UT), size=1.6)
    xr = v.X(W) + 5
    for a, b in ((0, FRIDGE_DOOR[1]), (FRIDGE_TOP[0], UT)):
        dim_v(v.Z(b), v.Z(a), xr, str(round(b - a)), ext_from=v.X(W), size=1.6)
    return v


def view_island(ox, fy):
    v = V(ox, fy)
    ix0, ix1, iy0, iy1 = ISLAND
    W = ix1 - ix0
    text(v.X(W / 2 + 300), v.Z(CEIL) - 20, "ОСТРОВ", size=3.4, weight="bold")
    text(v.X(W / 2 + 300), v.Z(CEIL) - 15.5, "вид со стороны кухни и разрез", size=2.1)
    line(v.X(-150), v.Z(0), v.X(W + 1100), v.Z(0), w=0.45)
    v.box(40, W - 40, 0, PL, fill="#a9a29b", sw=0.2)
    for x0, x1 in ((0, W / 2), (W / 2, W)):
        for z0, z1 in three():
            front(v, x0, x1, z0, z1)
    stone(v, -20, W + 20, BT, TOP)
    yb = v.Z(0) + 9
    dim_h(v.X(0), v.X(W / 2), yb, "600", ext_from=v.Z(0) + 1, size=1.9)
    dim_h(v.X(W / 2), v.X(W), yb, "600", ext_from=v.Z(0) + 1, size=1.9)
    dim_h(v.X(-20), v.X(W + 20), yb + 6, str(W + 40) + " столешница", size=1.8)
    xl = v.X(-20) - 5
    for a, b in ((0, PL), (PL, BT), (BT, TOP)):
        dim_v(v.Z(b), v.Z(a), xl, str(b - a), ext_from=v.X(-20), size=1.7)
    # разрез острова
    s0 = W + 450
    v.box(s0 + 40, s0 + 560, 0, PL, fill="#a9a29b", sw=0.2)
    v.box(s0, s0 + FD, PL + 2, BT - 2, fill=FACADE)
    v.box(s0 + 600 - FD, s0 + 600, PL, BT, fill=FACADE)
    for z0, z1 in three():
        v.box(s0 + FD, s0 + FD + 480, z0 + 20, z0 + 160, fill="#f1ede7", sw=0.15)
    stone(v, s0 - 20, s0 + 620, BT, TOP, n=10)
    dim_h(v.X(s0 - 20), v.X(s0 + 620), yb, "640", ext_from=v.Z(0) + 1, size=1.7)
    text(v.X(s0 + 300), v.Z(TOP) - 3, "разрез", size=1.8, fill="#555")
    return v


def view_plan(ox, oy):
    def P(x, y):
        return ox + x * S, oy - y * S          # стена 10–9 внизу, комната вверх
    text(ox + 1800 * S, oy - 3200 * S - 6, "ПЛАН КУХНИ", size=3.4, weight="bold")
    rect(ox - 100 * S, oy, 3800 * S, 100 * S, fill="url(#hatch)", sw=0.25)                 # стена 10–9
    rect(ox - 100 * S, oy - 3000 * S, 100 * S, 3100 * S, fill="url(#hatch)", sw=0.25)       # стена 10–11
    def prect(x0, x1, y0, y1, **kw):
        a, b = P(x0, y1)
        rect(a, b, (x1 - x0) * S, (y1 - y0) * S, **kw)
    prect(0, 3000, 0, CTD, fill=QUARTZ, sw=0.3)
    prect(0, CTD, CTD, LEFT[0][1], fill=QUARTZ, sw=0.3)
    prect(3000, 3600, 0, BD, fill=CORPUS, sw=0.3)
    prect(*FILLER_MAIN, 0, BD, fill=FACADE, sw=0.2)
    prect(0, BD, LEFT[1][0], LEFT[1][1], fill=CORPUS, sw=0.3)
    prect(0, BD, *FILLER_LEFT, fill=FACADE, sw=0.2)
    for x0, x1, kind in MAIN:
        line(*P(x0, 0), *P(x0, BD), w=0.2)
        label = {"corner": "угол", "sink": "мойка", "dw": "ПММ", "hob": "варка", "drawers": "ящики",
                 "tall": "ДШ+СВЧ"}[kind]
        text(*P((x0 + x1) / 2, 300), label, size=1.8, fill="#444")
        if kind == "sink":
            prect(x0 + 80, x1 - 80, 80, 520, fill="#b9bcbf", sw=0.2)
        if kind == "hob":
            for cx, cy, r in ((x0 + 160, 160, 95), (x0 + 440, 160, 75), (x0 + 160, 420, 75), (x0 + 440, 420, 95)):
                e(f'<circle cx="{P(cx, cy)[0]:.2f}" cy="{P(cx, cy)[1]:.2f}" r="{r * S:.2f}" fill="none" stroke="#333" stroke-width="0.2"/>')
    text(*P(300, 840), "ящики", size=1.8, fill="#444")
    text(*P(300, 1380), "холод.", size=1.8, fill="#444")
    line(*P(0, LEFT[0][1]), *P(BD, LEFT[0][1]), w=0.2)
    # верхние шкафы – пунктир
    prect(0, 3000, 0, UD, fill="none", stroke="#666", sw=0.2, dash="1.5 1")
    prect(0, UD, UD, UPPER_LEFT[-1], fill="none", stroke="#666", sw=0.2, dash="1.5 1")
    # остров
    ix0, ix1, iy0, iy1 = ISLAND
    prect(ix0 - 20, ix1 + 20, iy0 - 20, iy1 + 20, fill=QUARTZ, sw=0.3)
    line(*P((ix0 + ix1) / 2, iy0), *P((ix0 + ix1) / 2, iy1), w=0.2)
    text(*P((ix0 + ix1) / 2, (iy0 + iy1) / 2), "остров (ящики к кухне)", size=1.8, fill="#444")
    # размеры
    yb = P(0, 0)[1] + 9
    for x0, x1, kind in MAIN:
        dim_h(P(x0, 0)[0], P(x1, 0)[0], yb, str(x1 - x0), size=1.7)
    xl = P(0, 0)[0] - 9
    for a, b in ((0, BD), (BD, LEFT[0][1]), (LEFT[1][0], LEFT[1][1]), FILLER_LEFT):
        dim_v(P(0, b)[1], P(0, a)[1], xl, str(b - a), size=1.6)
    xi = P(ix1 + 20, 0)[0] + 6
    for a, b in ((0, BD), (BD, iy0), (iy0, iy1), (iy1, 2950)):
        dim_v(P(0, b)[1], P(0, a)[1], xi, str(b - a), size=1.7)
    dim_h(P(ix0, 0)[0], P(ix1, 0)[0], P(0, iy1)[1] - 4, "600 + 600", size=1.7)


def notes(x, y):
    text(x, y, "ПРИМЕЧАНИЯ", size=3.0, weight="bold", anchor="start")
    rows = [
        "Нижние модули: цоколь 100, корпус до 860, столешница искусственный камень 40 (верх 900).",
        "Фартук — искусственный камень, высота 600; верхние шкафы 1160 — до потолка (2660), глубина 350.",
        "Ряд стены 10–9 (слева направо от угла): глухой угол (проточный водонагреватель), мойка,",
        "      ПММ 60, варочная панель (2 ящика), 3 ящика, пенал 600: ящик, духовой шкаф, СВЧ, дверца.",
        "Ряд стены 10–11/12: ящики 480, пенал встроенного холодильника 600 + фальш-панель 20.",
        "Верхние шкафы: 350 / 443 / 442 / 442 / 442 / 442 / 439 и 365 / 365; LED-лента под шкафами.",
        "Вытяжка встроенная под шкаф над варочной панелью, выдвижной козырёк.",
        "Остров 2 × 600 × 600, ящики со стороны кухни; 800 от кухни, 950 до стены 13–14.",
        "Фасады — под камень (как в проекте), открывание через профиль (gola) / push-to-open.",
        "Размеры мебели условные по дизайн-проекту — уточнить по замеру и технике.",
    ]
    for i, s in enumerate(rows):
        text(x, y + 5.5 + i * 4.3, s, size=2.25, anchor="start")


def title_block():
    bx, by, bw, bh = 455, 372, 125, 38
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 13, bx + bw, by + 13, w=0.3)
    line(bx + 80, by + 13, bx + 80, by + bh, w=0.3)
    text(bx + bw / 2, by + 6, "КУХНЯ С ОСТРОВОМ", size=3.8, weight="bold")
    text(bx + bw / 2, by + 10.5, "кухня-гостиная, стены 10–9 и 10–11/12", size=2.3)
    text(bx + 3, by + 19, "3600 + 1700, остров 1200 × 600", size=2.3, anchor="start")
    text(bx + 3, by + 25, "ДШ, СВЧ, ПММ, холодильник, варка", size=2.3, anchor="start")
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
    fy = 175
    view_main(40, fy)
    view_left(300, fy)
    view_island(440, fy)
    view_plan(40, 395)
    notes(255, 245)
    title_block()
    e('</svg>')
    with open(os.path.join(HERE, "kuhnya.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


if __name__ == "__main__":
    main()
