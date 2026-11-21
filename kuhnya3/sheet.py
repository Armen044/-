#!/usr/bin/env python3
"""Кухня Г-образная: основная стена 4000, правая стена 1830 с пеналами. Лист А2, 1:15.
Высота 2750, цоколь 100, корпус 820, столешница 40 (верх 920)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                       # noqa: E402
from generate import e, line, rect                         # noqa: E402

F = 1.8
_t = g.text


def text(x, y, s, size=2.6, **kw):
    _t(x, y, s, size=size * F, **kw)


g.text = text
dim_h, dim_v = g.dim_h, g.dim_v

S = 1 / 15
WM, WR, H = 4000, 1830, 2750
PL, CB, TOP = 100, 920 - 40, 920
D = 600
UB, UT = 1520, 2350                          # верхние шкафы: фартук 600, верх на уровне антресоли пеналов
UD, R = 340, 300                             # глубина верхних, радиус торцевых
G = 2
FRONT, WHITE, DARK, TOPC, TILE = "#e8e4dd", "#fbfaf8", "#5a4636", "#e9e3da", "#f1efec"

# основная стена, слева направо: (x0, x1, вид, подпись)
BASE = [(0, 600, "door1", "распашной"), (600, 1200, "drw3", "3 ящика · варка"),
        (1200, 1800, "dw", "ПММ 600"), (1800, 2400, "sink", "мойка · ведро"),
        (2400, 2900, "door", "распашной"), (2900, 3400, "corner", "ящик (уходит в угол)")]
UPPERS = [(600, 1050), (1050, 1500), (1500, 1950), (1950, 2400)]
RAD = [(UPPERS[0][0] - R, UPPERS[0][0]), (UPPERS[-1][1], UPPERS[-1][1] + R)]   # радиусные торцы
ANT = 400
AZ = H - ANT                                 # низ антресоли пеналов 2350
# правая стена (от угла): угол 600 (столешница + ниша бойлера над ней), холодильник 600, духовка 600, планка 30
R_CORNER, R_OV, R_FR = (0, 600), (600, 1200), (1200, 1800)


class V:
    def __init__(self, ox, fy):
        self.ox, self.fy = ox, fy

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    def r(self, x0, x1, z0, z1, fill=FRONT, sw=0.3, **kw):
        rect(self.X(x0), self.Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, sw=sw, **kw)

    def handle_v(self, x, z0, z1):
        line(self.X(x), self.Z(z0), self.X(x), self.Z(z1), w=0.6, color="#222")

    def handle_h(self, x0, x1, z):
        line(self.X(x0), self.Z(z), self.X(x1), self.Z(z), w=0.6, color="#222")

    def swing(self, x0, x1, z0, z1, left):
        st = dict(w=0.18, color="#9a9a9a", dash="1.4 0.9")
        xa, xb = (x0, x1) if left else (x1, x0)
        line(self.X(xa), self.Z(z1), self.X(xb), self.Z((z0 + z1) / 2), **st)
        line(self.X(xa), self.Z(z0), self.X(xb), self.Z((z0 + z1) / 2), **st)


def main_wall(v):
    v.r(0, WM, 0, H, fill="#fafafa", sw=0.25, stroke="#999")
    v.r(0, 3400, TOP, UB, fill=TILE, sw=0.15, stroke="#ccc")
    line(v.X(-200), v.Z(0), v.X(WM + 200), v.Z(0), w=0.5)
    # цоколь и столешница
    v.r(0, 3400, 0, PL, fill="#cfcac2", sw=0.2)
    v.r(0, WM, CB, TOP, fill=TOPC, sw=0.35)
    for x0, x1, k, lab in BASE:
        if k == "door1":
            v.r(x0 + G, x1 - G, PL + G, CB - G)
            v.swing(x0 + G, x1 - G, PL + G, CB - G, True)
            v.handle_v(x1 - 60, CB - 300, CB - 60)
        elif k == "doors2":
            m = (x0 + x1) / 2
            for a, b, left in ((x0, m, True), (m, x1, False)):
                v.r(a + G, b - G, PL + G, CB - G)
                v.swing(a + G, b - G, PL + G, CB - G, left)
                v.handle_h(a + 80, b - 80, CB - 60)
        elif k == "drw3":
            hs = [260, 260, CB - PL - 520]
            z = PL
            for h_ in hs:
                v.r(x0 + G, x1 - G, z + G, z + h_ - G)
                v.handle_h(x0 + 150, x1 - 150, z + h_ - 50)
                z += h_
        elif k in ("dw", "sink", "door", "corner"):
            v.r(x0 + G, x1 - G, PL + G, CB - G)
            if k == "dw":
                v.handle_h(x0 + 150, x1 - 150, CB - 60)
            elif k == "corner":
                v.handle_h(x0 + 100, x1 - 100, CB - 60)
            else:
                left = k == "sink"
                v.swing(x0 + G, x1 - G, PL + G, CB - G, left)
                v.handle_v(x1 - 60 if left else x0 + 60, CB - 300, CB - 60)
        text(v.X((x0 + x1) / 2), v.Z(PL + 300), lab, size=1.4, fill="#555")
    # техника на столешнице
    v.r(660, 1140, TOP, TOP + 6, fill="#1d1d1d", sw=0.2)
    v.r(1900, 2300, TOP - 4, TOP + 2, fill="#2b2b2b", sw=0.2)
    line(v.X(2250), v.Z(TOP), v.X(2250), v.Z(TOP + 280), w=0.8, color="#222")
    line(v.X(2250), v.Z(TOP + 280), v.X(2150), v.Z(TOP + 280), w=0.8, color="#222")
    # верхние шкафы
    for i, (x0, x1) in enumerate(UPPERS):
        v.r(x0 + G, x1 - G, UB + G, UT - G, fill="#6d6259")
        v.swing(x0 + G, x1 - G, UB + G, UT - G, i % 2 == 0)
    for k, (x0, x1) in enumerate(RAD):                    # радиусные двери R300
        v.r(x0 + G, x1 - G, UB + G, UT - G, fill="#7d7168")
        for f in (0.33, 0.66):                            # штриховка изгиба
            xx = x0 + (x1 - x0) * (f if k else 1 - f)
            line(v.X(xx), v.Z(UT - G), v.X(xx), v.Z(UB + G), w=0.15, color="#bbb")
        v.swing(x0 + G, x1 - G, UB + G, UT - G, k == 1)
        text(v.X((x0 + x1) / 2), v.Z((UB + UT) / 2), "R300", size=1.4, fill="#fff", rot=-90)
    line(v.X(RAD[0][0]), v.Z(AZ), v.X(3400), v.Z(AZ), w=0.25, color="#c0392b", dash="2 1")
    text(v.X(2900), v.Z(AZ) - 1.5, "верх на уровне антресоли 2350", size=1.3, fill="#c0392b")
    # правая стена в разрезе: пеналы / ниша бойлера
    v.r(3400, WM, PL, H, fill="url(#drw)", sw=0.3)
    text(v.X(3700), v.Z(1500), "пеналы — см. вид Б", size=1.5, rot=-90, fill="#555")
    # размеры
    y = v.Z(0)
    xs = [0] + [b[1] for b in BASE] + [WM]
    for a, b in zip(xs, xs[1:]):
        dim_h(v.X(a), v.X(b), y + 5, str(b - a), ext_from=y + 0.5, size=1.8)
    dim_h(v.X(0), v.X(WM), y + 12, f"{WM}", size=2.3)
    for a, b in zip([UPPERS[0][0]] + [u[1] for u in UPPERS], [u[1] for u in UPPERS]):
        pass
    for a, b in ((RAD[0][0], RAD[0][1]), (UPPERS[0][0], UPPERS[-1][1]), (RAD[1][0], RAD[1][1])):
        lab = f"4 × 450 = {b - a}" if b - a > 400 else "R300"
        dim_h(v.X(a), v.X(b), v.Z(UT) - 4, lab, ext_from=v.Z(UT), size=1.6)
    dim_h(v.X(RAD[0][0]), v.X(RAD[1][1]), v.Z(UT) - 10, str(RAD[1][1] - RAD[0][0]), size=1.8)
    zs = [0, PL, CB, TOP, UB, UT, H]
    for a, b in zip(zs, zs[1:]):
        dim_v(v.Z(b), v.Z(a), v.X(0) - 5, str(b - a), ext_from=v.X(0), size=1.6)
    dim_v(v.Z(H), v.Z(0), v.X(0) - 11, str(H), ext_from=v.X(0), size=2.2)
    dim_v(v.Z(TOP), v.Z(0), v.X(0) - 17, str(TOP), ext_from=v.X(0), size=1.8)
    z = PL
    xd = v.X(1200) + 2.5
    for h_ in (260, 260, CB - PL - 520):
        dim_v(v.Z(z + h_), v.Z(z), xd, str(h_), size=1.3)
        z += h_


def right_wall(v):
    """Правая стена (смотрим из кухни, слева – угол)."""
    v.r(0, WR, 0, H, fill="#fafafa", sw=0.25, stroke="#999")
    line(v.X(-100), v.Z(0), v.X(WR + 150), v.Z(0), w=0.5)
    # угол: нижняя часть (ящик уходит сюда) в разрезе + столешница + ниша бойлера
    v.r(0, 600, 0, CB, fill="url(#drw)", sw=0.3)
    v.r(0, 600, CB, TOP, fill=TOPC, sw=0.35)
    v.r(0 + G, 600 - G, TOP + G, AZ - G, fill="#6d6259")
    v.swing(G, 600 - G, TOP + G, AZ - G, True)
    for a, b in (R_CORNER, R_OV, R_FR):
        v.r(a + G, b - G, AZ + G, H - G, fill="#6d6259")
        v.swing(a + G, b - G, AZ + G, H - G, a == 0)
    text(v.X(900), v.Z(AZ + 200) + 1, "антресоль 400", size=1.3, fill="#fff")
    text(v.X(280), v.Z(1850), "НИША БОЙЛЕРА", size=1.4, weight="bold", fill="#fff")
    text(v.X(280), v.Z(1850) + 4, "на столешнице", size=1.3, fill="#fff")
    text(v.X(300), v.Z(450), "угловой ящик", size=1.3, fill="#555")
    # холодильник
    x0, x1 = R_FR
    v.r(x0 + 40, x1 - 40, 0, PL, fill="#cfcac2", sw=0.2)
    v.r(x0 + G, x1 - G, PL + G, 1880 - G, fill="#6d6259")
    v.r(x0 + G, x1 - G, 1880 + G, AZ - G, fill="#6d6259")
    v.swing(x0 + G, x1 - G, PL + G, 1880 - G, False)
    v.swing(x0 + G, x1 - G, 1880 + G, AZ - G, False)
    text(v.X((x0 + x1) / 2), v.Z(1100), "ХОЛОДИЛЬНИК", size=1.6, weight="bold", fill="#fff")
    text(v.X((x0 + x1) / 2), v.Z(1100) + 4, "встраиваемый", size=1.3, fill="#fff")
    # духовка + СВЧ
    x0, x1 = R_OV
    v.r(x0 + 40, x1 - 40, 0, PL, fill="#cfcac2", sw=0.2)
    v.r(x0 + G, x1 - G, PL + G, 460 - G, fill="#6d6259")
    v.handle_h(x0 + 150, x1 - 150, 400)
    v.r(x0 + G, x1 - G, 460 + G, 1060 - G, fill="#1f1f1f")
    v.r(x0 + G, x1 - G, 1060 + G, 1440 - G, fill="#2c2c2c")
    v.r(x0 + G, x1 - G, 1440 + G, AZ - G, fill="#6d6259")
    v.swing(x0 + G, x1 - G, 1440 + G, AZ - G, False)
    text(v.X((x0 + x1) / 2), v.Z(280), "ящик", size=1.4, fill="#fff")
    text(v.X((x0 + x1) / 2), v.Z(760), "ДУХОВКА", size=1.5, weight="bold", fill="#fff")
    text(v.X((x0 + x1) / 2), v.Z(1250), "СВЧ", size=1.5, weight="bold", fill="#fff")
    v.r(1800, WR, PL, H, fill="#6d6259", sw=0.25)
    # размеры
    y = v.Z(0)
    xs = [0, 600, 1200, 1800, WR]
    for a, b in zip(xs, xs[1:]):
        dim_h(v.X(a), v.X(b), y + 5, str(b - a), ext_from=y + 0.5, size=1.8 if b - a > 50 else 1.3)
    dim_h(v.X(0), v.X(WR), y + 12, str(WR), size=2.3)
    for zs, x in (([0, PL, 460, 1060, 1440, AZ], v.X(1200) - 3), ([0, PL, 1880, AZ, H], v.X(WR) + 5)):
        for a, b in zip(zs, zs[1:]):
            dim_v(v.Z(b), v.Z(a), x, str(b - a), ext_from=v.X(WR) if x > v.X(WR) else None, size=1.5)
    dim_v(v.Z(AZ), v.Z(TOP), v.X(600) - 3, str(AZ - TOP), size=1.5)
    dim_v(v.Z(H), v.Z(0), v.X(WR) + 11, str(H), ext_from=v.X(WR), size=2.2)


def plan(ox, oy):
    s = 1 / 40
    X = lambda x: ox + x * s        # noqa: E731
    Y = lambda y: oy + y * s        # noqa: E731
    text(X(WM / 2), oy - 8, "ПЛАН", size=2.4, weight="bold")
    rect(X(-100), Y(-100), (WM + 200) * s, 100 * s, fill="url(#wall)", sw=0.2)
    rect(X(WM), Y(0), 100 * s, WR * s, fill="url(#wall)", sw=0.2)
    rect(X(0), Y(0), 3400 * s, D * s, fill="#f3eee7", sw=0.3)
    rect(X(3400), Y(0), 600 * s, D * s, fill="#e4dacb", sw=0.3)
    rect(X(3400), Y(600), 600 * s, 1200 * s, fill="#bfb3a5", sw=0.3)
    line(X(3400), Y(1200), X(WM), Y(1200), w=0.3)
    for x0, x1, k, lab in BASE:
        line(X(x1), Y(0), X(x1), Y(D), w=0.2)
    x0, x1 = RAD[0][0], RAD[1][1]
    r = R * s
    e(f'<path d="M{X(x0):.2f},{Y(0):.2f} L{X(x1):.2f},{Y(0):.2f} L{X(x1):.2f},{Y(UD - R):.2f} '
      f'A{r:.2f},{r:.2f} 0 0 1 {X(x1 - R):.2f},{Y(UD):.2f} L{X(x0 + R):.2f},{Y(UD):.2f} '
      f'A{r:.2f},{r:.2f} 0 0 1 {X(x0):.2f},{Y(UD - R):.2f} Z" fill="none" stroke="#6d6259" stroke-width="0.4" stroke-dasharray="1.5 0.8"/>')
    text(X(1500), Y(D) + 5, "пунктир — верхние шкафы, глубина 340, торцы R300", size=1.2, fill="#6d6259")
    text(X(1700), Y(D / 2) + 3, "столешница 40, верх 920", size=1.3, fill="#555")
    text(X(3700), Y(300) + 1, "бойлер", size=1.2, fill="#555")
    text(X(3700), Y(900) + 1, "духовка", size=1.2, fill="#fff")
    text(X(3700), Y(1500) + 1, "холод.", size=1.2, fill="#fff")
    dim_h(X(0), X(WM), Y(-100) - 3, str(WM), size=1.5)
    dim_v(Y(0), Y(WR), X(WM + 100) + 3, str(WR), size=1.5)


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)
    text(297, 18, "КУХНЯ Г-ОБРАЗНАЯ 4000 × 1830, высота 2750", size=4.0, weight="bold")
    va = V(60, 225)
    main_wall(va)
    text(va.X(WM / 2), va.Z(0) + 22, "ВИД А — основная стена 4000", size=2.4, weight="bold")
    vb = V(385, 225)
    right_wall(vb)
    text(vb.X(WR / 2), vb.Z(0) + 22, "ВИД Б — правая стена 1830 (пеналы)", size=2.4, weight="bold")
    plan(60, 290)
    rows = ["Цоколь 100 + корпус 780 + столешница 40 = 920; фартук 600; общая высота 2750.",
            "Низ слева направо: распашной 600 · 3 ящика под варкой · ПММ 600 · мойка (ведро) · распашной 500 ·",
            "угловой ящик: фасад 500, короб уходит вправо под нишу бойлера.",
            "Правая стена: ниша бойлера · пенал: ящик, духовка, СВЧ · пенал холодильника; сверху антресоль 400.",
            "Верх: 4 × 450 + радиусные торцы R300, глубина 340, высота 830, верх на уровне антресоли 2350."]
    for i, s in enumerate(rows):
        text(200, 300 + i * 6.5, s, size=1.8, anchor="start")
    import math
    import rashod as rs
    y0 = 338
    text(200, y0, "РАСХОД ЛДСП 16 (корпус + фасады, +15 % на раскрой; лист 2800 × 2070)", size=2.1,
         weight="bold", anchor="start")
    rows = [("Тёмный — древесный", "пеналы, ниша бойлера, верхние шкафы (корпус = фасад)", rs.area(rs.dark)),
            ("Светлый — однотонный", "нижние шкафы, фасады низа, цоколь", rs.area(rs.light))]
    for i, (nm, where, ar) in enumerate(rows):
        yy = y0 + 8 + i * 7
        sheets = math.ceil(ar * rs.WASTE / rs.SHEET)
        rect(200, yy - 4, 7, 5, fill="#6d6259" if i == 0 else "#e8e4dd", sw=0.25)
        text(210, yy, nm, size=1.9, weight="bold", anchor="start")
        text(258, yy, where, size=1.6, anchor="start", fill="#444")
        text(365, yy, f"{ar:.1f} м² → {sheets} " + ("лист" if sheets == 1 else "листа" if sheets < 5 else "листов"), size=1.9, weight="bold", anchor="start")
    text(200, y0 + 24, f"Радиусные фасады R300 — 2 шт (~{rs.radius_area:.1f} м²): гнутый МДФ, заказ отдельно.",
         size=1.5, anchor="start", fill="#555")
    text(200, y0 + 30, "Столешница и задние стенки ХДФ в расход ЛДСП не входят.", size=1.5, anchor="start", fill="#555")
    bx, by, bw, bh = 445, 362, 140, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    text(bx + bw / 2, by + 7, "КУХНЯ", size=3.2, weight="bold")
    text(bx + bw / 2, by + 12, "фасады, план, М 1:15", size=1.6)
    text(bx + 3, by + 22, "Основная стена 4000, правая 1830", size=1.7, anchor="start")
    text(bx + 3, by + 30, "Высота 2750, низ 920", size=1.7, anchor="start")
    text(bx + 3, by + 38, "Размеры в мм", size=1.7, anchor="start")
    e('</svg>')
    open(os.path.join(HERE, "sheet1.svg"), "w", encoding="utf-8").write("\n".join(g.out))


if __name__ == "__main__":
    main()
