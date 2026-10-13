#!/usr/bin/env python3
"""Генератор чертежа гардеробной (SVG, лист А2, масштаб 1:15).

Комната: ширина 2400, глубина (стены слева/справа) 1740, высота 2640.
Глубина корпусов 600, ЛДСП 16 мм, цоколь 80.
"""

S = 1 / 15          # масштаб 1:15 (мм натуры -> мм листа)
T = 16              # толщина ЛДСП
H = 2640            # высота
W = 2400            # ширина комнаты
D = 1740            # глубина комнаты (боковые стены)
DEPTH = 600         # глубина гардероба
PLINTH = 80
ANT = 2200          # низ антресоли
RAIL = 2130         # верхняя штанга
RAIL_LOW = 1080     # нижняя штанга (2 яруса)
BOARD_L = 1300      # длина гладильной доски (хранение вертикально)
BOARD_W = 380       # ширина доски
BOARD_T = 70        # толщина сложенной доски
DRAWER_TOP = PLINTH + T + 4 * 200   # 896

out = []
FONT = "DejaVu Sans, Arial, sans-serif"
LED = "#f0a800"


def e(s):
    out.append(s)


def text(x, y, s, size=2.6, anchor="middle", weight="normal", rot=None, fill="#111"):
    tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ""
    e(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" '
      f'font-weight="{weight}" fill="{fill}"{tr}>{s}</text>')


def line(x1, y1, x2, y2, w=0.25, color="#111", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    e(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
      f'stroke="{color}" stroke-width="{w}"{d}/>')


def rect(x, y, w, h, fill="none", stroke="#111", sw=0.25, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    e(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" '
      f'stroke="{stroke}" stroke-width="{sw}"{d} {extra}/>')


def tick(x, y):
    line(x - 0.9, y + 0.9, x + 0.9, y - 0.9, w=0.35)


def dim_h(x1, x2, y, label, ext_from=None, size=2.4):
    """Горизонтальный размер (координаты листа)."""
    if ext_from is not None:
        for x in (x1, x2):
            line(x, ext_from, x, y + (1.5 if y > ext_from else -1.5), w=0.15)
    line(x1 - 1.5, y, x2 + 1.5, y, w=0.18)
    tick(x1, y)
    tick(x2, y)
    text((x1 + x2) / 2, y - 0.8, label, size=size)


def dim_v(y1, y2, x, label, ext_from=None, size=2.4):
    """Вертикальный размер (координаты листа)."""
    if ext_from is not None:
        for y in (y1, y2):
            line(ext_from, y, x + (1.5 if x > ext_from else -1.5), y, w=0.15)
    line(x, y1 - 1.5, x, y2 + 1.5, w=0.18)
    tick(x, y1)
    tick(x, y2)
    cy = (y1 + y2) / 2
    text(x - 0.8, cy, label, size=size, rot=-90)


def leader(x1, y1, x2, y2, label, anchor="start", size=2.3):
    line(x1, y1, x2, y2, w=0.18)
    e(f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.45" fill="#111"/>')
    dx = 0.8 if anchor == "start" else -0.8
    lines = label.split("\n")
    for i, s in enumerate(lines):
        text(x2 + dx, y2 + 0.9 + i * (size + 0.6), s, size=size, anchor=anchor)


class View:
    """Фасад/развёртка: x – по горизонтали (мм натуры), z – высота от пола."""

    def __init__(self, ox, floor_y, width):
        self.ox, self.fy, self.w = ox, floor_y, width

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    # --- элементы ---------------------------------------------------------
    def panel_v(self, x0, z0=PLINTH, z1=H):
        rect(self.X(x0), self.Z(z1), T * S, (z1 - z0) * S, fill="#cdbba6", sw=0.2)

    def panel_h(self, x0, x1, z0):
        rect(self.X(x0), self.Z(z0 + T), (x1 - x0) * S, T * S, fill="#cdbba6", sw=0.2)

    def led(self, x0, x1, z):
        y = self.Z(z)
        line(self.X(x0) + 0.3, y, self.X(x1) - 0.3, y, w=0.7, color=LED, dash="1.6 0.8")

    def shelf(self, x0, x1, z, led=True):
        self.panel_h(x0, x1, z)
        if led:
            self.led(x0, x1, z - 9)

    def rail(self, x0, x1, z):
        y = self.Z(z)
        text(self.X(x0) + 1.5, y - 0.9, f"штанга Н={z}", size=1.7, anchor="start", fill="#444")
        line(self.X(x0) + 0.4, y, self.X(x1) - 0.4, y, w=0.6, color="#555")
        for x in (x0, x1):
            e(f'<circle cx="{self.X(x):.2f}" cy="{y:.2f}" r="0.55" fill="#555"/>')

    def hangers(self, x0, x1, z, length, n=None):
        """Схематичная одежда на плечиках."""
        width = x1 - x0
        n = n or max(2, int(width / 130))
        step = width / (n + 1)
        for i in range(1, n + 1):
            cx = self.X(x0 + step * i)
            y = self.Z(z)
            hw = min(170, step * 0.9) * S
            e(f'<path d="M{cx:.2f},{y:.2f} l{-hw / 2:.2f},{1.6:.2f} l{hw:.2f},0 z" '
              f'fill="none" stroke="#999" stroke-width="0.15"/>')
            rect(cx - hw / 2, y + 1.6, hw, length * S - 1.6, fill="#ece8e3", stroke="#b5aca2", sw=0.12)

    def drawers(self, x0, x1, n=4, z0=PLINTH + T, h=200):
        for i in range(n):
            zb = z0 + i * h
            rect(self.X(x0) + 0.15, self.Z(zb + h) + 0.15, (x1 - x0) * S - 0.3, h * S - 0.3,
                 fill="#a89580", stroke="#333", sw=0.2)
            hy = self.Z(zb + h / 2 + 30)
            hl = (x1 - x0) * 0.45 * S
            cx = (self.X(x0) + self.X(x1)) / 2
            line(cx - hl / 2, hy, cx + hl / 2, hy, w=0.5, color="#c9a227")
            text(cx, self.Z(zb + 45), "выкатной ящик", size=1.7, fill="#fff")
        self.panel_h(x0, x1, z0 + n * h)

    def shoe_shelves(self, x0, x1, zs=(290, 490, 690), z0=PLINTH + T, top=896):
        """Полки для обуви: обувь на дне и на каждой полке, бортик 30 мм."""
        for zb in (z0,) + tuple(z + T for z in zs):
            n = 2
            sw = (x1 - x0 - 40) / n
            for i in range(n):
                sx = x0 + 20 + i * sw
                e(f'<path d="M{self.X(sx + 10):.2f},{self.Z(zb):.2f} '
                  f'L{self.X(sx + 10):.2f},{self.Z(zb + 110):.2f} '
                  f'L{self.X(sx + sw * 0.45):.2f},{self.Z(zb + 70):.2f} '
                  f'L{self.X(sx + sw - 10):.2f},{self.Z(zb + 35):.2f} '
                  f'L{self.X(sx + sw - 10):.2f},{self.Z(zb):.2f} z" '
                  f'fill="#e3dad0" stroke="#8b7f73" stroke-width="0.15"/>')
        for z in zs:
            self.panel_h(x0, x1, z)
            rect(self.X(x0), self.Z(z + T + 30), (x1 - x0) * S, 30 * S, fill="#b9a690", sw=0.15)
            text((self.X(x0) + self.X(x1)) / 2, self.Z(z) + 2.2, f"полка для обуви Н={z}", size=1.5, fill="#444")
        self.panel_h(x0, x1, top)

    def shoe_rack(self, x0, x1):
        """Обувница Aiden – вид спереди: рама, 5 ярусов на стороне к проходу (ещё 5 – с обратной)."""
        cx = (x0 + x1) / 2
        a, b = cx - RACK_W / 2, cx + RACK_W / 2
        rect(self.X(a), self.Z(RACK_TOP), RACK_W * S, RACK_H * S, fill="#e9e7e5", stroke="#3f4245", sw=0.4)
        for z in (RACK_Z, RACK_TOP - 20):
            rect(self.X(a), self.Z(z + 20), RACK_W * S, 20 * S, fill="#3f4245", stroke="none")
        for x in (a, b - 20):
            rect(self.X(x), self.Z(RACK_TOP), 20 * S, RACK_H * S, fill="#3f4245", stroke="none")
        step = (RACK_H - 40) / 5
        for i in range(5):
            zb = RACK_Z + 20 + i * step + 30
            for k in range(6):
                sx = a + 40 + k * (RACK_W - 80) / 6
                sw = (RACK_W - 80) / 6 - 14
                hh = 120 - (k % 2) * 25
                e(f'<path d="M{self.X(sx):.2f},{self.Z(zb):.2f} L{self.X(sx):.2f},{self.Z(zb + hh):.2f} '
                  f'Q{self.X(sx + sw / 2):.2f},{self.Z(zb + hh + 25):.2f} {self.X(sx + sw):.2f},{self.Z(zb + hh):.2f} '
                  f'L{self.X(sx + sw):.2f},{self.Z(zb):.2f} z" fill="#d9cfc4" stroke="#8b7f73" stroke-width="0.15"/>')
            rect(self.X(a + 20), self.Z(zb), (RACK_W - 40) * S, 1.0, fill="#3f4245", stroke="none")
        text(cx, self.Z(RACK_TOP) + 4, "ОБУВНИЦА", size=2.0, weight="bold", fill="#3f4245")
        text(cx, self.Z(RACK_TOP) + 6.6, "поворотно-выдвижная", size=1.6, fill="#3f4245")

    def carcass(self, panels_x):
        # цоколь
        rect(self.X(0), self.Z(PLINTH), self.w * S, PLINTH * S, fill="url(#hatch)", sw=0.2)
        self.panel_h(0, self.w, PLINTH)          # дно
        self.panel_h(0, self.w, H - T)           # верх
        for x in panels_x:
            self.panel_v(x)

    def frame(self):
        rect(self.X(0), self.Z(H), self.w * S, H * S, sw=0.45)
        # пол
        line(self.X(0) - 4, self.Z(0), self.X(self.w) + 4, self.Z(0), w=0.5)


def defs():
    e('<defs>'
      '<marker id="arr" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L4,2 L0,4 z" fill="#33373b"/></marker>'
      '<pattern id="hatch" width="1.2" height="1.2" patternUnits="userSpaceOnUse" '
      'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.2" stroke="#777" stroke-width="0.25"/></pattern>'
      '<pattern id="wall" width="1.6" height="1.6" patternUnits="userSpaceOnUse" '
      'patternTransform="rotate(45)"><rect width="1.6" height="1.6" fill="#e3e3e3"/>'
      '<line x1="0" y1="0" x2="0" y2="1.6" stroke="#666" stroke-width="0.3"/></pattern>'
      '<pattern id="drw" width="2" height="2" patternUnits="userSpaceOnUse" '
      'patternTransform="rotate(-45)"><rect width="2" height="2" fill="#efe6da"/>'
      '<line x1="0" y1="0" x2="0" y2="2" stroke="#b39b7f" stroke-width="0.25"/></pattern>'
      '</defs>')


# ===========================================================================
# Развёртка: левая стена | задняя стена | правая стена
# ===========================================================================
FLOOR_Y = 212
SIDE = D - DEPTH        # 1140 – длина боковых секций

LM = 120                # левая: ниша выдвижного зеркала (у входа, напротив доски)
L1 = 450                # левая: полки для обуви + полки
L1E = LM + L1           # граница Л1/Л2 от входа = 570
L2 = SIDE - L1E         # левая: 2 яруса штанг (к углу)
SHOE_Z = (290, 490, 690)  # Л1: полки для обуви (низ полки от пола), над ними полка 896
MIR_D, MIR_T, MIR_H = 480, 50, 1405   # зеркало Lexy 480×50×1405 (глубина × толщина × высота)
MIR_Z = 450             # низ зеркала от пола
R1 = 940                # правая: длинная одежда (от угла)
R2 = SIDE - R1          # правая: узкая ниша гладильной доски (у входа) = 200
B1, B2, B3 = 800, 800, 800
# З2 – поворотно-выдвижная обувница ALPHALUX Aiden ALF0814.10S.43 (база 800, 10 полок, тёмно-серый)
RACK = "ALPHALUX Aiden ALF0814.10S.43"
RACK_W, RACK_D, RACK_H = 764, 400, 1850
RACK_Z = PLINTH + T                  # низ механизма – на дне корпуса
RACK_TOP = RACK_Z + RACK_H           # 1946
RACK_SHELF = 1960                    # полка над обувницей
RACK_Y = (DEPTH - RACK_D) / 2 + 10   # от задней стены: 110…510


def elevation_left(ox):
    v = View(ox, FLOOR_Y, SIDE)
    # x=0 – вход, x=SIDE – угол (стык с задней секцией)
    v.carcass([0, L1E - T / 2])
    v.panel_v(LM - T / 2, PLINTH + T, ANT)
    # антресоль
    v.panel_h(0, SIDE, ANT)
    v.led(0, SIDE, ANT - 9)
    v.panel_v(L1E - T / 2, ANT, H)
    # ЗР – ниша выдвижного поворотного зеркала (видно торцом)
    cx = (v.X(T) + v.X(LM - T / 2)) / 2
    mw = MIR_T * S
    rect(cx - mw / 2, v.Z(MIR_Z + MIR_H), mw, MIR_H * S, fill="#cfdde6", stroke="#33373b", sw=0.35)
    for z in (MIR_Z + MIR_H + 25, MIR_Z - 25):       # механизм (верх/низ)
        rect(cx - mw / 2 - 0.3, v.Z(z) - 0.8, mw + 0.6, 1.6, fill="#33373b", stroke="none")
    text(cx + 0.7, v.Z(MIR_Z + MIR_H / 2), "ЗЕРКАЛО (торец)", size=1.7, rot=-90, fill="#33373b", weight="bold")
    # Л1 – полки для обуви + полки
    v.shoe_shelves(LM + T / 2, L1E - T / 2, SHOE_Z)
    for z in (1230, 1550, 1870):
        v.shelf(LM + T / 2, L1E - T / 2, z)
    # Л2 – две штанги, открыто в угол
    v.hangers(L1E + T / 2, SIDE, RAIL, 900)
    v.hangers(L1E + T / 2, SIDE, RAIL_LOW, 850)
    v.rail(L1E + T / 2, SIDE, RAIL)
    v.rail(L1E + T / 2, SIDE, RAIL_LOW)
    line(v.X(SIDE), v.Z(H - T), v.X(SIDE), v.Z(PLINTH + T), w=0.3, dash="1.5 1")
    v.frame()
    return v


def elevation_back(ox):
    v = View(ox, FLOOR_Y, W)
    p1, p2 = B1 - T / 2, B1 + B2 - T / 2
    v.carcass([0, p1, p2, W - T])
    v.panel_h(0, W, ANT)
    v.led(0, W, ANT - 9)
    # B1 – короткая одежда, 2 яруса (угловая зона слева)
    v.hangers(T, p1, RAIL, 900)
    v.hangers(T, p1, RAIL_LOW, 850)
    v.rail(T, p1, RAIL)
    v.rail(T, p1, RAIL_LOW)
    # B2 – поворотно-выдвижная обувница + полка
    v.shoe_rack(p1 + T, p2)
    v.shelf(p1 + T, p2, RACK_SHELF)
    # B3 – длинная одежда
    v.hangers(p2 + T, W - T, RAIL, 1450)
    v.rail(p2 + T, W - T, RAIL)
    # угловые зоны (перекрыты боковыми секциями)
    for x in (DEPTH, W - DEPTH):
        line(v.X(x), v.Z(H - T), v.X(x), v.Z(PLINTH), w=0.3, color="#c0392b", dash="2 1")
    v.frame()
    return v


def elevation_right(ox):
    v = View(ox, FLOOR_Y, SIDE)
    # x=0 – угол, x=SIDE – вход
    p = R1 - T / 2
    v.carcass([p, SIDE - T])
    v.panel_h(0, SIDE, ANT)
    v.led(0, SIDE, ANT - 9)
    # R1 – длинная одежда + 2 полки для обуви внизу, открыто в угол
    v.hangers(0, p, RAIL, 1450)
    v.rail(0, p, RAIL)
    v.shelf(0, p, 350, led=False)
    line(v.X(0), v.Z(H - T), v.X(0), v.Z(PLINTH + T), w=0.3, dash="1.5 1")
    # R2 – ниша гладильной доски
    x0, x1 = p + T, SIDE - T
    v.shelf(x0, x1, 1560, led=False)
    v.shelf(x0, x1, 1880)
    # доска хранится боком (ребром к проходу) – на фасаде видна торцом ~70 мм
    cx = (v.X(x0) + v.X(x1)) / 2
    bt = 70 * S
    yb, yt = v.Z(PLINTH + T + 10), v.Z(PLINTH + T + 10 + BOARD_L)
    rect(cx - bt / 2, yt, bt, yb - yt, fill="#dfe9f3", stroke="#2f5d8a", sw=0.3)
    text(cx + 0.7, (yb + yt) / 2, "ДОСКА (ребром)", size=1.7, rot=-90, fill="#2f5d8a", weight="bold")
    # утюг на полке (стоит на пятке)
    iy = v.Z(1560 + T)
    e(f'<path d="M{cx - 1.6:.2f},{iy:.2f} l3.2,0 l-0.4,-4 l-2.4,0 z" fill="#2f5d8a"/>')
    # держатель доски
    for z in (1250, 500):
        line(v.X(x0), v.Z(z), cx - bt / 2, v.Z(z), w=0.5, color="#2f5d8a")
    # розетка
    sx, sy = cx, v.Z(1720)
    rect(sx - 1.4, sy - 1.4, 2.8, 2.8, fill="#fff", stroke="#c0392b", sw=0.3)
    e(f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="0.7" fill="none" stroke="#c0392b" stroke-width="0.25"/>')
    v.panel_v(p, ANT, H)
    v.frame()
    return v


def dims_vertical_common(v, x, side="left"):
    """Цепочка высот у фасада."""
    k = -1 if side == "left" else 1
    edge = v.X(0) if side == "left" else v.X(v.w)
    chain = [(0, PLINTH), (PLINTH, DRAWER_TOP), (DRAWER_TOP, ANT), (ANT, H)]
    for a, b in chain:
        dim_v(v.Z(b), v.Z(a), x, str(b - a), ext_from=edge)
    dim_v(v.Z(H), v.Z(0), x + k * 6, str(H), ext_from=edge)


def build_elevations():
    xl, xb, xr = 40, 142, 322
    vl = elevation_left(xl)
    vb = elevation_back(xb)
    vr = elevation_right(xr)

    top = FLOOR_Y - H * S
    # заголовки
    text(vl.X(SIDE / 2), top - 14, "ЛЕВАЯ СТЕНА", size=3.6, weight="bold")
    text(vl.X(SIDE / 2), top - 9.5, "развёртка, вид изнутри", size=2.2)
    text(vb.X(W / 2), top - 14, "ЗАДНЯЯ СТЕНА (напротив входа)", size=3.6, weight="bold")
    text(vb.X(W / 2), top - 9.5, "фасад, вид от входа", size=2.2)
    text(vr.X(SIDE / 2), top - 14, "ПРАВАЯ СТЕНА", size=3.6, weight="bold")
    text(vr.X(SIDE / 2), top - 9.5, "развёртка, вид изнутри", size=2.2)

    # подписи "вход/угол"
    for v, a, b in ((vl, "← вход", "угол →"), (vr, "← угол", "вход →")):
        text(v.X(0), FLOOR_Y + 4, a, size=2.0, anchor="start", fill="#555")
        text(v.X(SIDE), FLOOR_Y + 4, b, size=2.0, anchor="end", fill="#555")

    # --- горизонтальные размеры -----------------------------------------
    y1, y2 = FLOOR_Y + 10, FLOOR_Y + 17
    # левая
    dim_h(vl.X(0), vl.X(LM), y1, str(LM), ext_from=FLOOR_Y + 1, size=2.0)
    dim_h(vl.X(LM), vl.X(L1E), y1, str(L1), ext_from=FLOOR_Y + 1)
    dim_h(vl.X(L1E), vl.X(SIDE), y1, str(L2), ext_from=FLOOR_Y + 1)
    dim_h(vl.X(0), vl.X(SIDE), y2, f"{SIDE} (+600 угол = {D})")
    # задняя
    dim_h(vb.X(0), vb.X(B1), y1, str(B1), ext_from=FLOOR_Y + 1)
    dim_h(vb.X(B1), vb.X(B1 + B2), y1, str(B2), ext_from=FLOOR_Y + 1)
    dim_h(vb.X(B1 + B2), vb.X(W), y1, str(B3), ext_from=FLOOR_Y + 1)
    dim_h(vb.X(0), vb.X(W), y2, str(W))
    # угловые зоны
    dim_h(vb.X(0), vb.X(DEPTH), top - 3, "600 угол", ext_from=top, size=2.0)
    dim_h(vb.X(W - DEPTH), vb.X(W), top - 3, "600 угол", ext_from=top, size=2.0)
    # правая
    dim_h(vr.X(0), vr.X(R1), y1, str(R1), ext_from=FLOOR_Y + 1)
    dim_h(vr.X(R1), vr.X(SIDE), y1, str(R2), ext_from=FLOOR_Y + 1)
    dim_h(vr.X(0), vr.X(SIDE), y2, f"{SIDE} (+600 угол = {D})")

    # --- вертикальные размеры ------------------------------------------
    dims_vertical_common(vl, vl.X(0) - 6, "left")
    mx = vl.X(T) + 1.6
    dim_v(vl.Z(MIR_Z + MIR_H), vl.Z(MIR_Z), mx, str(MIR_H), size=1.6)
    dim_v(vl.Z(MIR_Z), vl.Z(0), mx, str(MIR_Z), size=1.6)
    # задняя: штанги + полки
    ex = vb.X(0) - 6
    dim_v(vb.Z(RAIL_LOW), vb.Z(0), ex, str(RAIL_LOW), ext_from=vb.X(0))
    dim_v(vb.Z(RAIL), vb.Z(RAIL_LOW), ex, str(RAIL - RAIL_LOW), ext_from=vb.X(0))
    dim_v(vb.Z(H), vb.Z(RAIL), ex, str(H - RAIL), ext_from=vb.X(0))
    dim_v(vb.Z(H), vb.Z(0), ex - 6, str(H), ext_from=vb.X(0))
    # шаг полок в средней секции
    xm = vb.X(B1 + B2) + 4
    zs = [RACK_Z, RACK_TOP, RACK_SHELF + T, ANT]
    for a, b in zip(zs, zs[1:]):
        dim_v(vb.Z(b), vb.Z(a), xm, str(b - a), size=2.0)
    xr0 = vb.X(B1 + B2 / 2 - RACK_W / 2)
    dim_h(xr0, xr0 + RACK_W * S, vb.Z(RACK_Z) - 3, str(RACK_W), size=1.8)
    dims_vertical_common(vr, vr.X(SIDE) + 6, "right")
    # ниша доски
    ix = vr.X(R1) + 2.6
    dim_v(vr.Z(1560), vr.Z(PLINTH + T), ix, "1464", size=1.6)

    # --- выноски -------------------------------------------------------
    leader(vb.X(B1 + B2 + 450), vb.Z(ANT - 9), vb.X(B1 + B2 + 60), vb.Z(2420),
           "LED-лента в алюм. профиле\nс рассеивателем (под антресолью)", size=2.0)
    leader(vl.X(LM + L1 / 2), vl.Z(1230 - 9), vl.X(LM + 30), vl.Z(1450),
           "LED-лента по\nпереднему краю полок", size=1.9)
    # обозначения секций
    for v, x, s in ((vl, LM / 2, "Зр"), (vl, LM + L1 / 2, "Л1"), (vl, L1E + L2 / 2, "Л2"),
                    (vb, B1 / 2, "З1"), (vb, B1 + B2 / 2, "З2"), (vb, B1 + B2 + B3 / 2, "З3"),
                    (vr, R1 / 2, "П1"), (vr, R1 + R2 / 2, "П2")):
        cx, cy = v.X(x), v.Z(H - 150)
        e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.4" fill="#fff" stroke="#111" stroke-width="0.25"/>')
        text(cx, cy + 0.9, s, size=2.3, weight="bold")

    # граница развёртки
    text(vb.X(0) + 1, vb.Z(H) + 4, "угол", size=1.8, anchor="start", fill="#c0392b")
    text(vb.X(W) - 1, vb.Z(H) + 4, "угол", size=1.8, anchor="end", fill="#c0392b")


# ===========================================================================
# План
# ===========================================================================
def build_plan():
    ox, oy = 95, 272          # левый-верхний угол комнаты (задняя стена сверху)
    WT = 100                  # толщина стен на плане

    def P(x, y):
        return ox + x * S, oy + y * S

    text(ox + W * S / 2, oy - 25, "ПЛАН (вид сверху)", size=3.6, weight="bold")

    # стены
    x0, y0 = P(-WT, -WT)
    rect(x0, y0, (W + 2 * WT) * S, WT * S, fill="url(#wall)", sw=0.3)           # задняя
    rect(x0, y0, WT * S, (D + 2 * WT) * S, fill="url(#wall)", sw=0.3)           # левая
    xr, _ = P(W, -WT)
    rect(xr, y0, WT * S, (D + 2 * WT) * S, fill="url(#wall)", sw=0.3)           # правая
    door0, door1 = 800, 1600
    yf = oy + D * S
    rect(x0, yf, (door0 + WT) * S, WT * S, fill="url(#wall)", sw=0.3)
    rect(ox + door1 * S, yf, (W - door1 + WT) * S, WT * S, fill="url(#wall)", sw=0.3)
    # дверь
    # раздвижная дверь по наружной стороне стены (не мешает зеркалу и доске)
    dyo = yf + WT * S
    rect(ox + (door0 - 40) * S, dyo + 0.3, (door1 - door0 + 80) * S, 40 * S, fill="#fff", stroke="#555", sw=0.3)
    line(ox + 1100 * S, dyo + 4.2, ox + 700 * S, dyo + 4.2, w=0.25, color="#555")
    e(f'<path d="M{ox + 700 * S:.2f},{dyo + 4.2:.2f} l1.6,-0.7 l0,1.4 z" fill="#555"/>')
    text(ox + 1350 * S, yf + WT * S + 5, "ВХОД", size=2.6, weight="bold")

    # корпуса
    def box(x, y, w, h, fill="#f4efe8"):
        a, b = P(x, y)
        rect(a, b, w * S, h * S, fill=fill, sw=0.3)

    box(0, 0, W, DEPTH)
    box(0, DEPTH, DEPTH, SIDE)
    box(W - DEPTH, DEPTH, DEPTH, SIDE)
    # обувница З2 (в шкафу – сплошная, выдвинутая/поворот – пунктир)
    rx = B1 + B2 / 2 - RACK_W / 2
    a, b = P(rx, RACK_Y)
    rect(a, b, RACK_W * S, RACK_D * S, fill="#e9e7e5", stroke="#3f4245", sw=0.35)
    line(*P(rx, RACK_Y + RACK_D / 2), *P(rx + RACK_W, RACK_Y + RACK_D / 2), w=0.3, color="#3f4245")
    a, b = P(rx, DEPTH + 20)
    rect(a, b, RACK_W * S, RACK_D * S, fill="none", stroke="#3f4245", sw=0.25, dash="1.2 0.8")
    cxr, cyr = P(B1 + B2 / 2, DEPTH + 20 + RACK_D / 2)
    e(f'<path d="M{cxr - 5:.2f},{cyr + 1.5:.2f} A5.5,3 0 1 0 {cxr + 5:.2f},{cyr + 1.5:.2f}" fill="none" '
      f'stroke="#3f4245" stroke-width="0.25" marker-end="url(#arr)"/>')
    text(cxr, cyr - 3.6, "обувница: выдвинуть и повернуть 180°", size=1.6, fill="#3f4245")
    # перегородки
    for xx in (B1, B1 + B2):
        line(*P(xx, 0), *P(xx, DEPTH), w=0.4)
    line(*P(0, D - L1E), *P(DEPTH, D - L1E), w=0.4)
    line(*P(0, D - LM), *P(DEPTH, D - LM), w=0.4)
    # зеркало: в нише (сплошное) и выдвинутое/повёрнутое (пунктир)
    ym = D - LM / 2 - T / 4
    a, b = P(40, ym - MIR_T / 2)
    rect(a, b, MIR_D * S, MIR_T * S, fill="#cfdde6", stroke="#33373b", sw=0.3)
    a, b = P(DEPTH + 20, ym - MIR_T / 2)
    rect(a, b, MIR_D * S, MIR_T * S, fill="none", stroke="#33373b", sw=0.25, dash="1.2 0.8")
    cxm, cym = P(DEPTH + 20 + MIR_D / 2, ym)
    rect(cxm - MIR_T * S / 2, cym - MIR_D * S / 2, MIR_T * S, MIR_D * S, fill="none",
         stroke="#33373b", sw=0.25, dash="0.6 0.6")
    e(f'<path d="M{cxm + 6:.2f},{cym:.2f} A6,6 0 0 0 {cxm:.2f},{cym - 6:.2f}" fill="none" '
      f'stroke="#33373b" stroke-width="0.25" marker-end="url(#arr)"/>')
    a1, _ = P(40 + MIR_D, ym)
    a2, _ = P(DEPTH + 20 + MIR_D, ym)
    line(a1 + 1, cym + 2.4, a2 - 1, cym + 2.4, w=0.25, color="#33373b")
    e(f'<path d="M{a2 - 1:.2f},{cym + 2.4:.2f} l-1.6,-0.7 l0,1.4 z" fill="#33373b"/>')
    line(*P(W - DEPTH, DEPTH + R1), *P(W, DEPTH + R1), w=0.4)
    # угловые зоны / открыто
    line(*P(0, DEPTH), *P(DEPTH, DEPTH), w=0.3, color="#c0392b", dash="1.5 1")
    line(*P(W - DEPTH, DEPTH), *P(W, DEPTH), w=0.3, color="#c0392b", dash="1.5 1")
    line(*P(DEPTH, 0), *P(DEPTH, DEPTH), w=0.15, color="#c0392b", dash="1.5 1")
    line(*P(W - DEPTH, 0), *P(W - DEPTH, DEPTH), w=0.15, color="#c0392b", dash="1.5 1")
    # штанги
    for a, b in ((P(T, 300), P(B1, 300)), (P(B1 + B2, 300), P(W - T, 300)),
                 (P(300, DEPTH + 20), P(300, D - L1E)), (P(W - 300, DEPTH + 20), P(W - 300, DEPTH + R1))):
        line(*a, *b, w=0.5, color="#555", dash="2 0.8")
    # гладильная доска в нише (вид сверху – узкий прямоугольник)
    a, b = P(W - DEPTH + 110, DEPTH + R1 + 65)
    rect(a, b, 380 * S, 70 * S, fill="#dfe9f3", stroke="#2f5d8a", sw=0.25)
    # LED по фронту антресоли (на плане – пунктир по переднему краю)
    for a, b in ((P(DEPTH, DEPTH - 25), P(W - DEPTH, DEPTH - 25)),
                 (P(DEPTH - 25, DEPTH), P(DEPTH - 25, D)),
                 (P(W - DEPTH + 25, DEPTH), P(W - DEPTH + 25, D))):
        line(*a, *b, w=0.6, color=LED, dash="1.6 0.8")

    # подписи секций
    for x, y, s in ((B1 / 2 + 150, 420, "З1"), (B1 + B2 / 2, 300, "З2"), (B1 + B2 + B3 / 2 - 150, 420, "З3"),
                    (300, D - LM - L1 / 2, "Л1"), (300, DEPTH + L2 / 2 + 120, "Л2"),
                    (W - 300, DEPTH + R1 / 2 + 120, "П1"), (W - DEPTH + 45, DEPTH + R1 + 45, "П2")):
        cx, cy = P(x, y)
        e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.2" fill="#fff" stroke="#111" stroke-width="0.25"/>')
        text(cx, cy + 0.8, s, size=2.1, weight="bold")
    cx, cy = P(W / 2, DEPTH + 720)
    text(cx, cy - 2, "ПРОХОД", size=2.6, weight="bold", fill="#555")
    text(cx, cy + 2, "1200 × 1140", size=2.2, fill="#555")

    # размеры
    top = oy - WT * S
    dim_h(*[P(0, 0)[0], P(W, 0)[0]], top - 9, f"{W}", ext_from=top)
    dim_h(P(0, 0)[0], P(B1, 0)[0], top - 3.5, str(B1), ext_from=top)
    dim_h(P(B1, 0)[0], P(B1 + B2, 0)[0], top - 3.5, str(B2), ext_from=top)
    dim_h(P(B1 + B2, 0)[0], P(W, 0)[0], top - 3.5, str(B3), ext_from=top)
    yb = yf + WT * S + 10
    dim_h(P(0, 0)[0], P(DEPTH, 0)[0], yb, "600")
    dim_h(P(DEPTH, 0)[0], P(W - DEPTH, 0)[0], yb, "1200 проход")
    dim_h(P(W - DEPTH, 0)[0], P(W, 0)[0], yb, "600")
    xl = ox - WT * S
    dim_v(oy, oy + D * S, xl - 10, str(D), ext_from=xl)
    dim_v(oy, oy + DEPTH * S, xl - 4.5, "600", ext_from=xl)
    dim_v(oy + DEPTH * S, oy + (D - L1E) * S, xl - 4.5, str(L2), ext_from=xl)
    dim_v(oy + (D - L1E) * S, oy + (D - LM) * S, xl - 4.5, str(L1), ext_from=xl)
    dim_v(oy + (D - LM) * S, oy + D * S, xl - 4.5, str(LM), ext_from=xl, size=1.8)
    xr2 = ox + (W + WT) * S
    dim_v(oy, oy + D * S, xr2 + 10, str(D), ext_from=xr2)
    dim_v(oy, oy + DEPTH * S, xr2 + 4.5, "600", ext_from=xr2)
    dim_v(oy + DEPTH * S, oy + (DEPTH + R1) * S, xr2 + 4.5, str(R1), ext_from=xr2)
    dim_v(oy + (DEPTH + R1) * S, oy + D * S, xr2 + 4.5, str(R2), ext_from=xr2)
    # глубина
    a, b = P(B1 + B2 + 150, 0)
    leader(*P(W - DEPTH - 20, D - 100), xr2 + 18, oy + D * S + 6,
           "Узкая ниша гладильной доски\n200 × 600 (П2), доска стоит боком")
    leader(*P(300, D - LM / 2), ox - WT * S - 20, oy + D * S - 8,
           "Ниша зеркала 120 × 600 (Зр):\nвыдвижное поворотное зеркало\nLexy 480×50×1405, антрацит.\nВыдвинуть на 480 и повернуть", anchor="end", size=2.0)


    # линии разрезов (см. лист 2)
    def cut(xa, ya, xb, yb, dx, dy, name):
        line(xa, ya, xb, yb, w=0.35, color="#1f4e8c", dash="6 1.2 1 1.2")
        for (x, y) in ((xa, ya), (xb, yb)):
            line(x, y, x + dx * 5, y + dy * 5, w=0.5, color="#1f4e8c")
            e(f'<path d="M{x + dx * 5:.2f},{y + dy * 5:.2f} l{-dy * 1.2 - dx * 2.2:.2f},{dx * 1.2 - dy * 2.2:.2f} '
              f'l{dy * 2.4:.2f},{-dx * 2.4:.2f} z" fill="#1f4e8c"/>')
            text(x + dx * 7.5, y + dy * 7.5 + 1.2, name, size=3.2, weight="bold", fill="#1f4e8c")

    xa, _ = P(1200, 0)
    cut(xa, oy - WT * S - 1, xa, oy + (D + WT) * S + 1, 1, 0, "А")
    _, yb = P(0, DEPTH + R1 + R2 / 2)
    cut(ox + (W - DEPTH - 60) * S, yb, ox + (W + WT) * S + 1, yb, 0, 1, "Б")

# ===========================================================================
# Легенда, спецификация, штамп
# ===========================================================================
def build_notes():
    x, y = 425, 112
    text(x, y, "УСЛОВНЫЕ ОБОЗНАЧЕНИЯ", size=3.2, weight="bold", anchor="start")
    rows = [
        ("led", "LED-лента 24 В в алюм. профиле с рассеивателем"),
        ("rack", "Обувница поворотно-выдвижная " + RACK + ", 10 полок"),
        ("rail", "Штанга для плечиков (овальная, хром/золото)"),
        ("board", "Гладильная доска (хранение боком, ребром к проходу)"),
        ("corner", "Граница угловой зоны / открыто в угол"),
        ("sock", "Розетка 220 В (для утюга/отпаривателя)"),
        ("mirror", "Зеркало выдвижное поворотное Lexy 480×50×1405, антрацит"),
    ]
    for i, (k, s) in enumerate(rows):
        yy = y + 7 + i * 6
        if k == "led":
            line(x, yy, x + 10, yy, w=0.7, color=LED, dash="1.6 0.8")
        elif k == "rack":
            rect(x, yy - 2, 10, 4, fill="#e9e7e5", stroke="#3f4245", sw=0.4)
            line(x, yy, x + 10, yy, w=0.5, color="#3f4245")
        elif k == "rail":
            line(x, yy, x + 10, yy, w=0.6, color="#555")
            for xx in (x, x + 10):
                e(f'<circle cx="{xx}" cy="{yy}" r="0.55" fill="#555"/>')
        elif k == "board":
            rect(x + 2, yy - 2, 6, 4, fill="#dfe9f3", stroke="#2f5d8a", sw=0.3)
        elif k == "corner":
            line(x, yy, x + 10, yy, w=0.3, color="#c0392b", dash="2 1")
        elif k == "sock":
            rect(x + 3.6, yy - 1.4, 2.8, 2.8, fill="#fff", stroke="#c0392b", sw=0.3)
            e(f'<circle cx="{x + 5}" cy="{yy}" r="0.7" fill="none" stroke="#c0392b" stroke-width="0.25"/>')
        elif k == "mirror":
            rect(x, yy - 1.2, 10, 2.4, fill="#cfdde6", stroke="#33373b", sw=0.3)
        text(x + 13, yy + 0.9, s, size=2.4, anchor="start")

    y = 170
    text(x, y, "СЕКЦИИ", size=3.2, weight="bold", anchor="start")
    secs = [
        ("Зр", "120", "Ниша зеркала Lexy (выдвижное поворотное), напротив доски П2"),
        ("Л1", "450", "Полки для обуви: дно + 3 полки (Н=290/490/690) с бортиком 30 мм, полка 896 + 3 полки с LED"),
        ("Л2", "570", "2 яруса штанг (короткая одежда), открыта в угол"),
        ("З1", "800", "2 яруса штанг (рубашки, юбки, брюки), угловая зона"),
        ("З2", "800", "Обувница Aiden ALF0814.10S.43 764×400×1850 (10 полок) + полка Н=1960 с LED"),
        ("З3", "800", "Длинная одежда (пальто, платья), угловая зона"),
        ("П1", "940", "Длинная одежда + полка для обуви Н=350, открыта в угол"),
        ("П2", "200", "Узкая ниша доски (внутри 176): доска боком, полка утюга Н=1560"),
        ("—", "2400", "Антресоль Н=424 по всему периметру, LED снизу"),
    ]
    for i, (a, w, s) in enumerate(secs):
        yy = y + 6 + i * 4.6
        text(x, yy, a, size=2.4, anchor="start", weight="bold")
        text(x + 8, yy, w, size=2.4, anchor="start")
        text(x + 18, yy, s, size=2.4, anchor="start")

    # общие данные
    y = 40
    text(x, y, "ИСХОДНЫЕ ДАННЫЕ", size=3.2, weight="bold", anchor="start")
    info = [
        "Комната: ширина 2400 × глубина 1740 (стены слева/справа) × высота 2640",
        "Планировка П-образная, глубина гардеробной (корпусов) — 600 мм",
        "Проход между боковыми секциями — 1200 мм",
        "Материал: ЛДСП 16 мм (цвет «серо-коричневый»), кромка ПВХ 2 мм",
        "Цоколь 80 мм; З2 — обувница ALPHALUX Aiden, база 800 (внутри 784)",
        "Антресоль с низа 2200 до потолка 2640, верхняя штанга Н=2130",
        "LED: лента 24 В, 4000 K, блок питания в антресоли, датчик открытия двери",
        "Гладильная доска справа у входа (П2), напротив — выдвижное зеркало (Зр)",
        "Дверь — раздвижная (или распашная наружу), чтобы не мешать зеркалу",
        "Размеры уточнить по месту после замера и чистовой отделки стен",
    ]
    for i, s in enumerate(info):
        text(x, y + 6 + i * 4.6, s, size=2.4, anchor="start")

    # штамп
    bx, by, bw, bh = 405, 362, 180, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    line(bx, by + 30, bx + bw, by + 30, w=0.3)
    line(bx + 120, by + 14, bx + 120, by + bh, w=0.3)
    text(bx + bw / 2, by + 6.5, "ГАРДЕРОБНАЯ КОМНАТА", size=4.2, weight="bold")
    text(bx + bw / 2, by + 11.5, "Чертёж общего вида: план, развёртка стен", size=2.6)
    text(bx + 3, by + 20, "Габариты: 2400 × 1740 × 2640 мм", size=2.6, anchor="start")
    text(bx + 3, by + 26, "Глубина корпусов: 600 мм", size=2.6, anchor="start")
    text(bx + 3, by + 36, "Все размеры в миллиметрах", size=2.6, anchor="start")
    text(bx + 3, by + 42, "ЛДСП 16 мм", size=2.6, anchor="start")
    text(bx + 150, by + 20.5, "Масштаб", size=2.4)
    text(bx + 150, by + 26.5, "1:15", size=3.6, weight="bold")
    text(bx + 150, by + 36.5, "Лист", size=2.4)
    text(bx + 150, by + 42.5, "1 (А2)", size=3.2, weight="bold")


def main():
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{FONT}">')
    defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)       # рамка листа
    build_elevations()
    build_plan()
    build_notes()
    e('</svg>')
    with open(__file__.rsplit("/", 1)[0] + "/garderobnaya.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(out))


if __name__ == "__main__":
    main()
