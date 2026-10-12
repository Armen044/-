#!/usr/bin/env python3
"""Чертёж распашного шкафа с ящиками (по эскизу заказчика), лист А3, масштаб 1:20.

Высоты взяты с эскиза: антресоль 450, полки с шагом 300, блок ящиков 803 (4 × 170,75),
справа два яруса штанг (зоны 784 и 951, штанга на Н=1800). Цоколь 80, ЛДСП 16.
Ширина и глубина на эскизе не указаны – приняты 1600 × 600 (уточнить).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                          # noqa: E402
from generate import e, text, line, rect, dim_h, dim_v, leader  # noqa: E402

S = 1 / 20
T = 16                  # ЛДСП Egger «Кашемир»
DT = 18                 # фасад МДФ, эмаль
W = 1600                # ширина корпуса (ПРИНЯТО, уточнить)
DEPTH = 600             # глубина с фасадами (ПРИНЯТО, уточнить)
CD = DEPTH - DT         # глубина корпуса = 582
PL = 80                 # цоколь
ZB = PL                 # низ корпуса (дно)
B0 = ZB + T             # верх дна = 96
MID = W / 2

# левый отсек: ящики 803, полки с шагом 300, антресоль 450 (размеры в свету)
DRAWER_ZONE = 803
L_SHELVES = []          # низ каждой полки слева
z = B0 + DRAWER_ZONE
for gap in (300, 300, 300, 300):
    L_SHELVES.append(z)
    z += T + gap
ZA = z                  # низ полки антресоли = 2163
L_SHELVES.append(ZA)
ZTOP = ZA + T + 450     # низ крышки = 2629
H = ZTOP + T            # общая высота с цоколем = 2645

# правый отсек: нижняя зона 951, верхняя 784, полка 300, антресоль 450
R_MID = B0 + 951        # низ средней полки = 1047
R_UP = R_MID + T + 784  # низ верхней полки = 1847
R_SHELVES = [R_MID, R_UP, ZA]
RAIL_UP = 1800          # верхняя штанга (с эскиза)
RAIL_LOW = R_MID - 47   # нижняя штанга = 1000

# ящики (внутренние, за распашными дверями)
DR_H = 170.75
DR_GAP = 11.25
DR_SET = 30             # отступ фасадов ящиков от переднего края корпуса
DR_Z = [B0 + 30 + i * (DR_H + DR_GAP) for i in range(4)]

# фасады: 4 нижние двери + 4 антресольные, фрезерованная ручка на стыках
DOOR_GAP = 3
SPLIT = ZA + T / 2      # стык нижних и антресольных дверей
GROOVE = (230, 2420)    # фрезеровка-ручка на кромках: от – до (по высоте)
GROOVE_W = 30           # зазор между фасадами на стыках = место ручки
HGAP = GROOVE_W
MILL = 12               # ширина розовой фрезеровки на кромке фасада
PINK = "#eba3b3"
DOOR_W = (W - 3 * HGAP) / 4      # ширина створки = 377,5


def door_x(i):
    """Края i-й створки (зазор 30 на каждом из трёх стыков)."""
    x0 = i * (DOOR_W + HGAP)
    return x0, x0 + DOOR_W

CUT = "#7d6c5b"
FACADE = "#d9cfc9"
CORPUS = "#cdc3b8"


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


def led(v, x, z0, z1):
    rect(v.X(x) - 0.35, v.Z(z1), 0.7, (z1 - z0) * S, fill="#f0a800", stroke="none")


def handle_gap(v, xa, xb, z0, z1):
    """Стык створок: зазор 30 (виден корпус) и розовая фрезеровка на кромках со скруглённым верхом."""
    v.box(xa, xb, PL + 2, H - 2, fill="#8f857d", sw=0.15)
    ga, gb = GROOVE
    w = (xb - xa) + 2 * MILL
    r = w * S / 2
    x0 = v.X(xa - MILL)
    e(f'<path d="M{x0:.2f},{v.Z(ga):.2f} L{x0:.2f},{v.Z(gb) + r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x0 + 2 * r:.2f},{v.Z(gb) + r:.2f} '
      f'L{x0 + 2 * r:.2f},{v.Z(ga):.2f} z" fill="{PINK}" stroke="#b5737f" stroke-width="0.2"/>')
    v.box(xa, xb, ga, gb - (xb - xa) / 2, fill="#8f857d", sw=0.1)


# ---------------------------------------------------------------------------
def view_facade(ox, fy):
    v = V(ox, fy)
    text(v.X(W / 2), v.Z(H) - 13, "ФАСАД", size=3.4, weight="bold")
    text(v.X(W / 2), v.Z(H) - 9, "двери закрыты", size=2.1)
    line(v.X(-150), v.Z(0), v.X(W + 150), v.Z(0), w=0.45)
    v.box(50, W - 50, 0, PL, fill="#a99d93")                     # цоколь
    dw = W / 4
    for i in range(4):
        x0, x1 = door_x(i)
        v.box(x0, x1, PL + 2, SPLIT - DOOR_GAP / 2, fill=FACADE, sw=0.3)
        v.box(x0, x1, SPLIT + DOOR_GAP / 2, H - 2, fill=FACADE, sw=0.3)
    for k in (1, 2, 3):
        handle_gap(v, door_x(k - 1)[1], door_x(k)[0], *GROOVE)
    # раскрытие (условно): створки 1 и 3 – петли слева, 2 и 4 – справа
    for i, (hinge, far) in enumerate(((0, door_x(0)[1]), (door_x(1)[1], door_x(1)[0]),
                                      (door_x(2)[0], door_x(2)[1]), (W, door_x(3)[0]))):
        for z0, z1 in ((PL + 2, SPLIT), (SPLIT, H - 2)):
            line(v.X(hinge), v.Z(z0), v.X(far), v.Z((z0 + z1) / 2), w=0.12, color="#999", dash="1 0.8")
            line(v.X(hinge), v.Z(z1), v.X(far), v.Z((z0 + z1) / 2), w=0.12, color="#999", dash="1 0.8")
    yb = v.Z(0) + 9
    for i in range(4):
        x0, x1 = door_x(i)
        dim_h(v.X(x0), v.X(x1), yb, "377,5", ext_from=v.Z(0) + 1, size=1.7)
        if i < 3:
            dim_h(v.X(x1), v.X(door_x(i + 1)[0]), yb - 4, "30", ext_from=v.Z(0) + 1, size=1.5)
    dim_h(v.X(0), v.X(W), yb + 6, f"{W}*")
    xl = v.X(0) - 5
    for a, b in ((0, PL), (PL, SPLIT), (SPLIT, H)):
        dim_v(v.Z(b), v.Z(a), xl, str(round(b - a)), ext_from=v.X(0), size=2.0)
    dim_v(v.Z(H), v.Z(0), xl - 6, str(H))
    leader(v.X(door_x(0)[1] - MILL / 2), v.Z(1700), v.X(W + 120), v.Z(1950),
           "зазор 30 — место ручки,\nфрезеровка кромок\n(розовая эмаль)", size=1.8)
    leader(v.X(dw * 3.5), v.Z(1200), v.X(W + 120), v.Z(1350), "фасад МДФ,\nпокраска эмаль", size=1.8)
    return v


def view_inside(ox, fy):
    v = V(ox, fy)
    text(v.X(W / 2), v.Z(H) - 13, "НАПОЛНЕНИЕ", size=3.4, weight="bold")
    text(v.X(W / 2), v.Z(H) - 9, "фасады условно сняты", size=2.1)
    line(v.X(-150), v.Z(0), v.X(W + 150), v.Z(0), w=0.45)
    v.box(50, W - 50, 0, PL, fill="#a99d93")
    v.box(0, W, ZB, H, fill="#f6f3ef", sw=0.4)
    for x in (0, MID - T / 2, W - T):
        v.box(x, x + T, ZB, H)
    for zz in (ZB, ZTOP):
        v.box(0, W, zz, zz + T)
    lx0, lx1, rx0, rx1 = T, MID - T / 2, MID + T / 2, W - T
    for zz in L_SHELVES:
        v.box(lx0, lx1, zz, zz + T)
    for zz in R_SHELVES:
        v.box(rx0, rx1, zz, zz + T)
    # коробки на антресоли
    for x0, x1 in ((lx0, lx1), (rx0, rx1)):
        rect(v.X(x0 + 50), v.Z(ZA + T + 300), (x1 - x0 - 100) * S, 300 * S, fill="#e3d9cc", stroke="#aaa", sw=0.12)
    # стопки вещей на полках слева
    for zz in L_SHELVES[:-1]:
        for k in range(2):
            rect(v.X(lx0 + 60 + k * 360), v.Z(zz + T + 150), 300 * S, 150 * S, fill="#e6e0d8", stroke="#bbb", sw=0.1)
    # ящики
    for zz in DR_Z:
        v.box(lx0 + 4, lx1 - 4, zz, zz + DR_H, fill="#ddd3c9", sw=0.3)
        cx = v.X((lx0 + lx1) / 2)
        r = 60 * S
        e(f'<path d="M{cx - r:.2f},{v.Z(zz + DR_H):.2f} A{r:.2f},{r * 0.6:.2f} 0 0 0 {cx + r:.2f},{v.Z(zz + DR_H):.2f}" '
          f'fill="#f6f3ef" stroke="#555" stroke-width="0.2"/>')
    # штанги и одежда справа
    for zr, ln in ((RAIL_UP, 700), (RAIL_LOW, 820)):
        hangers(v, rx0, rx1, zr, ln)
        line(v.X(rx0) + 0.3, v.Z(zr), v.X(rx1) - 0.3, v.Z(zr), w=0.6, color="#555")
        text(v.X(rx0) + 1.2, v.Z(zr) - 0.8, "штанга", size=1.6, anchor="start", fill="#444")
    # вертикальная подсветка
    led(v, lx0 + 12, B0, ZTOP)
    led(v, rx0 + 12, B0, ZTOP)
    # размеры слева (в свету, как на эскизе)
    xl = v.X(0) - 5
    chain = [(B0, B0 + DRAWER_ZONE)]
    prev = L_SHELVES[0] + T
    for zz in L_SHELVES[1:]:
        chain.append((prev, zz))
        prev = zz + T
    chain.append((prev, ZTOP))
    for a, b in chain:
        dim_v(v.Z(b), v.Z(a), xl, str(round(b - a)), ext_from=v.X(0), size=1.8)
    dim_v(v.Z(H), v.Z(0), xl - 6, str(H), size=2.0)
    for zz in DR_Z:
        dim_v(v.Z(zz + DR_H), v.Z(zz), v.X(lx0) + 2.2, "170,75", size=1.3)
    # размеры справа
    xr = v.X(W) + 5
    chain = [(B0, R_MID), (R_MID + T, R_UP), (R_UP + T, ZA), (ZA + T, ZTOP)]
    for a, b in chain:
        dim_v(v.Z(b), v.Z(a), xr, str(round(b - a)), ext_from=v.X(W), size=1.8)
    dim_v(v.Z(RAIL_UP), v.Z(0), xr + 6, f"{RAIL_UP} штанга", size=1.8)
    dim_v(v.Z(R_MID + T), v.Z(0), xr + 12, str(round(R_MID + T)), size=1.8)
    dim_v(v.Z(PL), v.Z(0), xr, str(PL), ext_from=v.X(W), size=1.6)
    yb = v.Z(0) + 9
    dim_h(v.X(0), v.X(MID), yb, str(round(MID)), ext_from=v.Z(ZB) + 1, size=2.0)
    dim_h(v.X(MID), v.X(W), yb, str(round(MID)), ext_from=v.Z(ZB) + 1, size=2.0)
    dim_h(v.X(0), v.X(W), yb + 6, f"{W}*")
    leader(v.X(lx0 + 12), v.Z(1400), v.X(-260), v.Z(1500), "вертикальная\nподсветка\n(от открывания)", anchor="end", size=1.7)
    leader(v.X(MID / 2 + 300), v.Z(DR_Z[1] + 80), v.X(-260), v.Z(500), "ящики 4 × 170,75\nзазор 11,25;\nвырез под ручку", anchor="end", size=1.7)
    return v


def view_section(ox, fy):
    """Разрез по левому отсеку (полки и ящики)."""
    v = V(ox, fy)
    text(v.X(300), v.Z(H) - 13, "РАЗРЕЗ 1–1", size=3.4, weight="bold")
    text(v.X(300), v.Z(H) - 9, "по отсеку с ящиками", size=2.1)
    rect(v.X(-100), v.Z(H + 100), 100 * S, (H + 180) * S, fill="url(#hatch)", sw=0.25)
    line(v.X(-100), v.Z(0), v.X(DEPTH + 450), v.Z(0), w=0.45)
    v.box(0, 4, ZB, H, fill="#777")                              # задняя стенка
    v.box(0, CD - 50, 0, PL, fill="#a99d93")                     # цоколь
    for zz in [ZB, ZTOP] + L_SHELVES:
        v.box(0, CD, zz, zz + T, fill=CUT)
    v.box(CD, DEPTH, PL + 2, SPLIT - 1.5, fill=FACADE, sw=0.3)
    v.box(CD, DEPTH, SPLIT + 1.5, H - 2, fill=FACADE, sw=0.3)
    for i, zz in enumerate(DR_Z):
        off = 400 if i == 3 else 0
        dash = "1 0.7" if off else None
        fx = CD - DR_SET
        v.box(40 + off, fx - 18 + off, zz + 15, zz + DR_H - 25, fill="none" if off else "#efe9e1", sw=0.2, dash=dash)
        v.box(fx - 18 + off, fx + off, zz, zz + DR_H, fill="none" if off else "#ddd3c9", sw=0.3, dash=dash)
    led_x = CD - 10
    rect(v.X(led_x) - 0.3, v.Z(ZTOP), 0.6, (ZTOP - B0) * S, fill="#f0a800", stroke="none")
    yb = v.Z(0) + 9
    dim_h(v.X(0), v.X(CD), yb, str(CD), ext_from=v.Z(0) + 1, size=2.0)
    dim_h(v.X(CD), v.X(DEPTH), yb, str(DT), ext_from=v.Z(0) + 1, size=1.6)
    dim_h(v.X(0), v.X(DEPTH), yb + 6, f"{DEPTH}*")
    dim_h(v.X(CD - DR_SET), v.X(CD), v.Z(DR_Z[0]) + 2.5, "30", size=1.5)
    dim_h(v.X(CD - DR_SET), v.X(CD - DR_SET + 400), v.Z(DR_Z[3] + DR_H) - 2, "ход 400", size=1.6)
    leader(v.X(led_x), v.Z(1600), v.X(DEPTH + 60), v.Z(1800), "LED-профиль\nна торце стойки", size=1.7)
    return v


def view_plan(ox, oy):
    def P(x, y):
        return ox + x * S, oy + y * S
    text(ox + W / 2 * S, oy - 8, "ПЛАН", size=3.4, weight="bold")
    rect(*P(-100, -100), (W + 200) * S, 100 * S, fill="url(#hatch)", sw=0.25)
    a, b = P(0, 0)
    rect(a, b, W * S, CD * S, fill="#f1ece6", sw=0.3)
    line(*P(MID, 0), *P(MID, CD), w=0.35)
    line(*P(MID + 20, CD / 2), *P(W - 20, CD / 2), w=0.4, color="#555", dash="2 0.8")
    dw = W / 4
    for i in range(4):
        x0, x1 = door_x(i)
        a, b = P(x0, CD)
        rect(a, b, (x1 - x0) * S, DT * S, fill=FACADE, stroke="#111", sw=0.25)
    r = DOOR_W * S
    for hinge, sgn in ((0, 1), (door_x(1)[1], -1), (door_x(2)[0], 1), (W, -1)):
        hx, hy = P(hinge, DEPTH)
        line(hx, hy, hx, hy + r, w=0.25, color="#555")
        sweep = 0 if sgn > 0 else 1
        e(f'<path d="M{hx:.2f},{hy + r:.2f} A{r:.2f},{r:.2f} 0 0 {sweep} {hx + sgn * r:.2f},{hy:.2f}" '
          f'fill="none" stroke="#777" stroke-width="0.18" stroke-dasharray="1 0.7"/>')
    cx = P(MID / 2, 0)[0]
    line(cx, oy - 6, cx, oy + 950 * S, w=0.3, color="#1f4e8c", dash="5 1 1 1")
    text(cx + 2.5, oy - 5, "1", size=2.6, weight="bold", fill="#1f4e8c")
    dim_h(P(0, 0)[0], P(W, 0)[0], oy + 1050 * S, f"{W}*", size=2.0)
    dim_v(oy, oy + DEPTH * S, P(W, 0)[0] + 4, f"{DEPTH}*", ext_from=P(W, 0)[0], size=2.0)


def notes(x, y):
    text(x, y, "ПРИМЕЧАНИЯ", size=3.0, weight="bold", anchor="start")
    rows = [
        "Корпус — ЛДСП Egger 16 мм, цвет «Кашемир»; цоколь 80.",
        "Фасады — МДФ 18 мм, эмаль; 4 нижние + 4 антресольные двери по 377,5 мм.",
        "Между фасадами на стыках зазор 30 — место ручки; кромки фрезерованы, розовая эмаль.",
        "Левый отсек: антресоль 450, 4 полки с шагом 300, блок ящиков 803:",
        "      4 внутренних ящика, фасады 170,75, зазор 11,25, отступ 30 от края,",
        "      вырез под ручку, направляющие полного выдвижения 500 мм.",
        "Правый отсек: антресоль 450, полка 300, штанга Н=1800 (зона 784),",
        "      полка, нижняя штанга Н=1000 (зона 951).",
        "Вертикальная LED-подсветка в каждом отсеке, включение от открывания.",
        "* Ширина 1600 и глубина 600 на эскизе не указаны — ПРИНЯТЫ, уточнить.",
        "Размеры в свету между полками — как на эскизе заказчика.",
    ]
    for i, s in enumerate(rows):
        text(x, y + 5.5 + i * 4.1, s, size=2.15, anchor="start")


def title_block():
    bx, by, bw, bh = 290, 252, 120, 38
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 13, bx + bw, by + 13, w=0.3)
    line(bx + 80, by + 13, bx + 80, by + bh, w=0.3)
    text(bx + bw / 2, by + 6, "ШКАФ С ЯЩИКАМИ", size=3.8, weight="bold")
    text(bx + bw / 2, by + 10.5, "распашной, по эскизу заказчика", size=2.3)
    text(bx + 3, by + 19, f"{W}* × {DEPTH}* × {H} мм", size=2.4, anchor="start")
    text(bx + 3, by + 25, "ЛДСП Egger «Кашемир», МДФ эмаль", size=2.4, anchor="start")
    text(bx + 3, by + 31, "Размеры в мм", size=2.4, anchor="start")
    text(bx + 100, by + 20, "Масштаб", size=2.2)
    text(bx + 100, by + 26, "1:20", size=3.4, weight="bold")
    text(bx + 100, by + 33, "Лист 1 (А3)", size=2.2)


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 420, 297, fill="#fff", stroke="none")
    rect(8, 5, 407, 287, sw=0.5)
    fy = 183
    view_facade(32, fy)
    view_inside(200, fy)
    view_section(330, fy)
    view_plan(40, 222)
    notes(150, 214)
    title_block()
    e('</svg>')
    with open(os.path.join(HERE, "shkaf2.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


if __name__ == "__main__":
    main()
