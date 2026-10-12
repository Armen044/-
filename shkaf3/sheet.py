#!/usr/bin/env python3
"""Шкаф со столом (стена 25–26), лист А2, масштаб 1:20.

Размеры – по 3D-эскизам заказчика: ширина 600 + 600 + 1200 = 2400, глубина 600,
антресоль 600 (276 + 276), слева открытые полки с подсветкой (315/300/300/300, ниже 311/311),
в середине полки ≈308, справа две штанги (958/959); три распашные двери 1965,
сверху декоративная рейчатая панель HIWOOD LV129 Long NP (660);
стол 1200 × 600, высота 765,66, тумба с 4 ящиками 167,87.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                          # noqa: E402
from generate import e, text, line, rect, dim_h, dim_v, leader  # noqa: E402

S = 1 / 20
T = 16
DT = 18
C1, C2, C3 = 600, 600, 1200          # открытые полки | полки за дверью | штанги
W = C1 + C2 + C3                     # 2400
X1, X2 = C1, C1 + C2                 # оси стоек 600 и 1200
DEPTH = 600
CD = DEPTH - DT                      # 582
PL = 50                              # цоколь
B0 = PL + T                          # верх дна = 66
ZA = None                            # низ дна антресоли – считается ниже (≈1983)
A_IN = 276                           # отделения антресоли
CEIL = 2660                          # потолок (под перекрытием 100)
PANEL = (2000, CEIL)                 # рейчатая панель 660 по всей ширине

# левая секция: снизу 311, 311, затем 300 × 3 и 315 (размеры в свету)
L_SHELVES = []
z = B0
for gap in (311, 311, 300, 300, 300):
    z += gap
    L_SHELVES.append(z)
    z += T
ZA = z + 315                         # верхнее отделение 315 → дно антресоли 1983
A_SHELF = ZA + T + A_IN              # низ полки антресоли
ZTOP = A_SHELF + T + A_IN            # низ крышки
H = ZTOP + T                         # верх корпуса = 2583
# средняя секция: 5 полок равномерно (≈306)
M_GAP = (ZA - B0 - 5 * T) / 6
M_SHELVES = [B0 + M_GAP * (i + 1) + T * i for i in range(5)]
# правая секция: нижняя зона 958, полка, верхняя зона
R_SHELF = B0 + 958
RAIL_UP = ZA - 55
RAIL_LOW = R_SHELF - 55

# двери
DOOR_Z = (20, 1985)                  # 1965
DOOR_GAP = 2
DOORS = [(X1, X2), (X2, X2 + C3 / 2), (X2 + C3 / 2, W)]

# стол и тумба
DESK_TOP = 765.66
DESK_T = 26
DESK_Y = (DEPTH, DEPTH + 1200)       # столешница выходит из шкафа на 1200
DESK_X = (0, C1)                     # ширина 600 – по левой секции
PED_Y = (DESK_Y[1] - 400, DESK_Y[1]) # тумба 400 по длине стола (ПРИНЯТО)
PED_H = DESK_TOP - DESK_T            # 739,66
DRW = 167.87
DRW_GAP = (PED_H - 4 * DRW) / 5      # зазоры между фасадами ящиков

CUT = "#7d6c5b"
FACADE = "#e3dfda"
CORPUS = "#e4dfd8"
WOOD = "#c79a64"
WALNUT = "#5a3d2b"
FLUTE = "#3b3836"
LOW_DOOR = (20, 735)                 # фасад под столом (левая секция), петли слева


class V:
    def __init__(self, ox, fy):
        self.ox, self.fy = ox, fy

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    def box(self, x0, x1, z0, z1, fill=CORPUS, sw=0.2, stroke="#111", dash=None):
        rect(self.X(x0), self.Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, stroke=stroke, sw=sw, dash=dash)


def hangers(v, x0, x1, z, length):
    n = max(2, int((x1 - x0) / 110))
    step = (x1 - x0) / (n + 1)
    for i in range(1, n + 1):
        cx = v.X(x0 + step * i)
        hw = min(150, step * 0.9) * S
        e(f'<path d="M{cx:.2f},{v.Z(z):.2f} l{-hw / 2:.2f},1.2 l{hw:.2f},0 z" fill="none" stroke="#999" stroke-width="0.15"/>')
        rect(cx - hw / 2, v.Z(z) + 1.2, hw, length * S - 1.2, fill="#ece8e3", stroke="#b5aca2", sw=0.12)


def waves(v, x0, x1, z0, z1):
    """Верхние фасады: цвет как у нижних, фрезеровка «волна» (вертикальные волнистые пазы)."""
    for k in range(4):
        a, b = x0 + k * 600 + 1, x0 + (k + 1) * 600 - 1
        v.box(a, b, z0 + 2, z1 - 2, fill=FACADE, sw=0.3)
        x = a + 30
        while x < b - 10:
            pts = []
            z = z0 + 10
            while z <= z1 - 10:
                pts.append(f"{v.X(x + 12 * math.sin((z - z0) / 110 * math.pi)):.2f},{v.Z(z):.2f}")
                z += 10
            e(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#a49c95" stroke-width="0.22"/>')
            x += 60


def led(v, x, z0, z1):
    rect(v.X(x) - 0.35, v.Z(z1), 0.7, (z1 - z0) * S, fill="#f0a800", stroke="none")


def carcass(v, inside=True):
    v.box(50, W - 50, 0, PL, fill="#b3aaa1")
    v.box(0, W, PL, H, fill="#f7f4f0", sw=0.4)
    for x in (0, X1 - T / 2, X2 - T / 2, W - T):
        v.box(x, x + T, PL, H)
    for zz in (PL, ZA, ZTOP):
        v.box(0, W, zz, zz + T)
    v.box(0, X2, A_SHELF, A_SHELF + T)
    for zz in L_SHELVES:
        v.box(T, X1 - T / 2, zz, zz + T, fill=WOOD)
    for zz in M_SHELVES:
        v.box(X1 + T / 2, X2 - T / 2, zz, zz + T)
    v.box(X2 + T / 2, W - T, R_SHELF, R_SHELF + T)
    led(v, T + 10, B0, ZA)
    led(v, W - T - 10, ZA + T, ZTOP)
    if inside:
        for zr, ln in ((RAIL_UP, 800), (RAIL_LOW, 820)):
            hangers(v, X2 + T / 2, W - T, zr, ln)
            line(v.X(X2 + T / 2) + 0.3, v.Z(zr), v.X(W - T) - 0.3, v.Z(zr), w=0.6, color="#333")
            text(v.X(X2 + T / 2) + 1.2, v.Z(zr) - 0.8, "штанга", size=1.6, anchor="start", fill="#444")
        for zz in M_SHELVES[:-1]:
            rect(v.X(X1 + 70), v.Z(zz + T + 140), 440 * S, 140 * S, fill="#e6e0d8", stroke="#bbb", sw=0.1)
        for zz in L_SHELVES[2:]:
            rect(v.X(120), v.Z(zz + T + 180), 160 * S, 180 * S, fill="#d8cfc4", stroke="#aaa", sw=0.1)


# ---------------------------------------------------------------------------
def view_facade(ox, fy):
    v = V(ox, fy)
    text(v.X(W / 2), v.Z(CEIL) - 13, "ФАСАД — СТЕНА 25–26", size=3.4, weight="bold")
    text(v.X(W / 2), v.Z(CEIL) - 9, "двери закрыты, стол в торец", size=2.1)
    rect(v.X(-100), v.Z(CEIL + 100), (W + 200) * S, 100 * S, fill="url(#hatch)", sw=0.25)
    line(v.X(-150), v.Z(0), v.X(W + 150), v.Z(0), w=0.45)
    carcass(v, inside=False)
    for x0, x1 in DOORS:
        v.box(x0 + DOOR_GAP / 2, x1 - DOOR_GAP / 2, *DOOR_Z, fill=FACADE, sw=0.3)
    for xj in (X2, X2 + C3 / 2):                      # профиль-ручка на стыках
        rect(v.X(xj) - 0.5, v.Z(1600), 1.0, 1100 * S, fill="#1d1b1a", stroke="none")
    for (x0, x1), hinge in zip(DOORS, (X1, X2, W)):
        far = x1 if hinge == x0 else x0
        line(v.X(hinge), v.Z(DOOR_Z[0]), v.X(far), v.Z(sum(DOOR_Z) / 2), w=0.12, color="#999", dash="1 0.8")
        line(v.X(hinge), v.Z(DOOR_Z[1]), v.X(far), v.Z(sum(DOOR_Z) / 2), w=0.12, color="#999", dash="1 0.8")
    waves(v, 0, W, *PANEL)
    # стол в торец: столешница и боковина тумбы; за ней – фасад под столом (пунктир)
    v.box(0, C1, 0, PED_H, fill="#e9e5e0", sw=0.3)
    v.box(2, C1 - 2, *LOW_DOOR, fill="none", sw=0.3, dash="1.2 0.8")
    v.box(0, C1, DESK_TOP - DESK_T, DESK_TOP, fill=WALNUT, sw=0.3)
    yb = v.Z(0) + 9
    for a, b in ((0, X1), (X1, X2), (X2, W)):
        dim_h(v.X(a), v.X(b), yb, str(b - a), ext_from=v.Z(0) + 1, size=2.0)
    dim_h(v.X(0), v.X(W), yb + 6, str(W))
    xl = v.X(0) - 5
    for a, b in ((0, DESK_TOP), (DESK_TOP, PANEL[0]), PANEL):
        dim_v(v.Z(b), v.Z(a), xl, str(round(b - a, 2)).replace(".", ","), ext_from=v.X(0), size=1.9)
    dim_v(v.Z(CEIL), v.Z(0), xl - 6, str(CEIL))
    xr = v.X(W) + 5
    dim_v(v.Z(DOOR_Z[1]), v.Z(DOOR_Z[0]), xr, "1965", ext_from=v.X(W), size=1.9)
    leader(v.X(W * 0.6), v.Z(2350), v.X(W + 150), v.Z(2550), "верхние фасады: цвет как у нижних,\nфрезеровка «волна»", size=1.8)
    leader(v.X(150), v.Z(300), v.X(-250), v.Z(450), "фасад под столом\n(за тумбой, пунктир)", anchor="end", size=1.8)
    leader(v.X(X2), v.Z(1300), v.X(W + 150), v.Z(1500), "профиль-ручка\nна стыке дверей", size=1.8)
    leader(v.X(300), v.Z(DESK_TOP - 10), v.X(-250), v.Z(1050), "стол 1200 × 600\n(в торец)", anchor="end", size=1.8)
    return v


def view_inside(ox, fy):
    v = V(ox, fy)
    text(v.X(W / 2), v.Z(CEIL) - 13, "НАПОЛНЕНИЕ", size=3.4, weight="bold")
    text(v.X(W / 2), v.Z(CEIL) - 9, "двери, панель и стол условно сняты", size=2.1)
    line(v.X(-150), v.Z(0), v.X(W + 150), v.Z(0), w=0.45)
    carcass(v, inside=True)
    v.box(0, C1, DESK_TOP - DESK_T, DESK_TOP, fill="none", sw=0.25, dash="1.2 0.8")
    # левые размеры
    xl = v.X(0) - 5
    chain, prev = [], B0
    for zz in L_SHELVES:
        chain.append((prev, zz))
        prev = zz + T
    chain.append((prev, ZA))
    for a, b in chain:
        dim_v(v.Z(b), v.Z(a), xl, str(round(b - a)), ext_from=v.X(0), size=1.7)
    dim_v(v.Z(A_SHELF), v.Z(ZA + T), xl, str(A_IN), ext_from=v.X(0), size=1.7)
    dim_v(v.Z(ZTOP), v.Z(A_SHELF + T), xl, str(A_IN), ext_from=v.X(0), size=1.7)
    dim_v(v.Z(H), v.Z(ZA), xl - 6, "600", size=1.8)
    dim_v(v.Z(H), v.Z(0), xl - 12, str(H), size=1.9)
    # средние
    xm = v.X(X1) + 2.5
    prev = B0
    for zz in M_SHELVES + [ZA]:
        dim_v(v.Z(zz), v.Z(prev), xm, str(round(zz - prev)), size=1.4)
        prev = zz + T
    # правые
    xr = v.X(W) + 5
    for a, b in ((B0, R_SHELF), (R_SHELF + T, ZA)):
        dim_v(v.Z(b), v.Z(a), xr, str(round(b - a)), ext_from=v.X(W), size=1.8)
    dim_v(v.Z(RAIL_UP), v.Z(0), xr + 6, f"{RAIL_UP} штанга", size=1.7)
    dim_v(v.Z(RAIL_LOW), v.Z(0), xr + 12, f"{RAIL_LOW} штанга", size=1.7)
    yb = v.Z(0) + 9
    for a, b in ((0, X1), (X1, X2), (X2, W)):
        dim_h(v.X(a), v.X(b), yb, str(b - a), ext_from=v.Z(0) + 1, size=2.0)
    dim_h(v.X(0), v.X(W), yb + 6, str(W))
    leader(v.X(T + 10), v.Z(1500), v.X(-250), v.Z(1700), "открытые полки\n(шпон/дерево),\nLED-подсветка", anchor="end", size=1.7)
    return v


def view_side(ox, fy):
    """Вид сбоку на стол (взгляд от стены 24–25): глубина шкафа + столешница 1200 + тумба."""
    v = V(ox, fy)               # x – расстояние от стены 25–26
    L = DESK_Y[1]
    text(v.X(L / 2), v.Z(CEIL) - 13, "ВИД СБОКУ — СТОЛ", size=3.4, weight="bold")
    text(v.X(L / 2), v.Z(CEIL) - 9, "столешница выходит из шкафа, тумба с ящиками", size=2.1)
    rect(v.X(-100), v.Z(CEIL + 100), 100 * S, (CEIL + 180) * S, fill="url(#hatch)", sw=0.25)
    line(v.X(-100), v.Z(0), v.X(L + 200), v.Z(0), w=0.45)
    v.box(0, CD, PL, H, fill="#ece7e1", sw=0.3)                         # боковина шкафа
    v.box(CD, DEPTH, *PANEL, fill=FACADE, sw=0.3)
    v.box(0, CD, 2000, H, fill="#ece7e1", sw=0.3)
    v.box(CD, DEPTH, *DOOR_Z, fill=FACADE, sw=0.3)
    v.box(DESK_Y[0], DESK_Y[1], DESK_TOP - DESK_T, DESK_TOP, fill=WALNUT, sw=0.3)
    v.box(PED_Y[0], PED_Y[1], 0, PED_H, fill="#e9e5e0", sw=0.3)
    for i in range(4):
        z0 = DRW_GAP + i * (DRW + DRW_GAP)
        v.box(PED_Y[0] + 10, PED_Y[1] - 10, z0, z0 + DRW, fill=FACADE, sw=0.25)
        dim_v(v.Z(z0 + DRW), v.Z(z0), v.X(PED_Y[1]) + 3, "167,87", size=1.4)
    yb = v.Z(0) + 9
    dim_h(v.X(0), v.X(DEPTH), yb, "600", ext_from=v.Z(0) + 1, size=2.0)
    dim_h(v.X(DESK_Y[0]), v.X(DESK_Y[1]), yb, "1200 столешница", ext_from=v.Z(0) + 1, size=2.0)
    dim_h(v.X(PED_Y[0]), v.X(PED_Y[1]), v.Z(PED_H) - 3, "400*", size=1.6)
    xr = v.X(L) + 10
    dim_v(v.Z(DESK_TOP), v.Z(0), xr, "765,66", ext_from=v.X(L), size=1.8)
    dim_v(v.Z(DESK_TOP), v.Z(DESK_TOP - DESK_T), xr - 4, "26", size=1.3)
    return v


def view_plan(ox, oy):
    def P(x, y):
        return ox + x * S, oy + y * S
    text(ox + W / 2 * S, oy - 8, "ПЛАН", size=3.4, weight="bold")
    rect(*P(-100, -100), (W + 200) * S, 100 * S, fill="url(#hatch)", sw=0.25)
    rect(*P(-100, 0), 100 * S, 2000 * S, fill="url(#hatch)", sw=0.25)
    a, b = P(0, 0)
    rect(a, b, W * S, CD * S, fill="#f1ece6", sw=0.3)
    for x in (X1, X2):
        line(*P(x, 0), *P(x, CD), w=0.35)
    line(*P(X2 + 20, CD / 2), *P(W - 20, CD / 2), w=0.4, color="#555", dash="2 0.8")
    for (x0, x1), hinge in zip(DOORS, (X1, X2, W)):
        a, b = P(x0 + 1, CD)
        rect(a, b, (x1 - x0 - 2) * S, DT * S, fill=FACADE, stroke="#111", sw=0.25)
        r = (x1 - x0) * S
        hx, hy = P(hinge, DEPTH)
        sgn = 1 if hinge == x0 else -1
        line(hx, hy, hx, hy + r, w=0.25, color="#555")
        e(f'<path d="M{hx:.2f},{hy + r:.2f} A{r:.2f},{r:.2f} 0 0 {0 if sgn > 0 else 1} {hx + sgn * r:.2f},{hy:.2f}" '
          f'fill="none" stroke="#777" stroke-width="0.18" stroke-dasharray="1 0.7"/>')
    a, b = P(DESK_X[0], DESK_Y[0])
    rect(a, b, C1 * S, 1200 * S, fill="#8a6a55", sw=0.3)
    hx, hy = P(0, DEPTH)
    r = C1 * S
    e(f'<path d="M{hx:.2f},{hy + r:.2f} A{r:.2f},{r:.2f} 0 0 0 {hx + r:.2f},{hy:.2f}" fill="none" stroke="#fff" '
      f'stroke-width="0.2" stroke-dasharray="1 0.7"/>')
    a, b = P(DESK_X[0], PED_Y[0])
    rect(a, b, C1 * S, 400 * S, fill="none", sw=0.25, dash="1.2 0.8")
    text(*P(300, DESK_Y[0] + 400), "стол", size=2.2, fill="#fff", weight="bold")
    text(*P(300, PED_Y[0] + 220), "тумба", size=1.8, fill="#fff")
    dim_h(P(0, 0)[0], P(X1, 0)[0], oy - 4, "600", size=1.6)
    dim_h(P(X1, 0)[0], P(X2, 0)[0], oy - 4, "600", size=1.6)
    dim_h(P(X2, 0)[0], P(W, 0)[0], oy - 4, "1200", size=1.6)
    dim_v(oy, oy + DEPTH * S, P(W, 0)[0] + 4, "600", ext_from=P(W, 0)[0], size=1.8)
    xr = P(C1, 0)[0] + 4
    dim_v(oy + DESK_Y[0] * S, oy + DESK_Y[1] * S, xr, "1200", size=1.8)


def notes(x, y):
    text(x, y, "ПРИМЕЧАНИЯ", size=3.0, weight="bold", anchor="start")
    rows = [
        f"Шкаф {W} × {DEPTH} × {H}, цоколь 50; антресоль закрыта 4 фасадами по 600,",
        "      высота 660 (до потолка 2660): цвет как у нижних, фрезеровка «волна».",
        "Секции: 600 открытые полки с LED (снизу 311 / 311, выше 300 × 3 и 315),",
        "      600 полки за дверью (≈306), 1200 две штанги (зоны 958 / ≈902).",
        "Антресоль 600: два отделения по 276, справа — с вертикальной подсветкой.",
        "Двери: 3 распашные по 600, высота 1965, профиль-ручка на стыках.",
        "Под столом — фасад на левую секцию (600 × 715), петли слева, открывание под стол.",
        "Стол: столешница 1200 × 600 × 26 (орех), высота 765,66, выходит из шкафа",
        "      в торец левой секции; тумба 4 ящика по 167,87 (ширина 400* — принято).",
        "Материалы фасадов/корпуса уточнить; фасады показаны в светлом камне.",
        "Размеры уточнить по месту.",
    ]
    for i, s in enumerate(rows):
        text(x, y + 5.5 + i * 4.3, s, size=2.3, anchor="start")


def title_block():
    bx, by, bw, bh = 455, 372, 125, 38
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 13, bx + bw, by + 13, w=0.3)
    line(bx + 80, by + 13, bx + 80, by + bh, w=0.3)
    text(bx + bw / 2, by + 6, "ШКАФ СО СТОЛОМ", size=3.8, weight="bold")
    text(bx + bw / 2, by + 10.5, "стена 25–26, по эскизам заказчика", size=2.3)
    text(bx + 3, by + 19, f"шкаф {W} × {DEPTH} × {H}, стол 1200 × 600", size=2.3, anchor="start")
    text(bx + 3, by + 25, "фасады: низ гладкие, верх «волна»", size=2.3, anchor="start")
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
    fy = 205
    view_facade(45, fy)
    view_inside(248, fy)
    view_side(420, fy)
    view_plan(45, 262)
    notes(225, 262)
    title_block()
    e('</svg>')
    with open(os.path.join(HERE, "shkaf3.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


if __name__ == "__main__":
    main()
