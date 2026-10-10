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

L1 = 570                # левая: ящики + полки (у входа)
L2 = SIDE - L1          # левая: 2 яруса штанг (к углу)
R1 = 690                # правая: длинная одежда (от угла)
R2 = SIDE - R1          # правая: ниша гладильной доски (у входа) = 450
B1, B2, B3 = 900, 600, 900


def elevation_left(ox):
    v = View(ox, FLOOR_Y, SIDE)
    # x=0 – вход, x=SIDE – угол (стык с задней секцией)
    v.carcass([0, L1 - T / 2])
    # антресоль
    v.panel_h(0, SIDE, ANT)
    v.led(0, SIDE, ANT - 9)
    v.panel_v(L1 - T / 2, ANT, H)
    # L1 – ящики + полки
    v.drawers(T, L1 - T / 2)
    for z in (1230, 1550, 1870):
        v.shelf(T, L1 - T / 2, z)
    # L2 – две штанги, открыто в угол
    v.hangers(L1 + T / 2, SIDE, RAIL, 900)
    v.hangers(L1 + T / 2, SIDE, RAIL_LOW, 850)
    v.rail(L1 + T / 2, SIDE, RAIL)
    v.rail(L1 + T / 2, SIDE, RAIL_LOW)
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
    # B2 – ящики + полки для сумок
    v.drawers(p1 + T, p2)
    for z in (1230, 1550, 1870):
        v.shelf(p1 + T, p2, z)
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
    # доска (вертикальное хранение)
    bw = 380 * S
    cx = (v.X(x0) + v.X(x1)) / 2
    yb, yt = v.Z(PLINTH + T + 20), v.Z(1500)
    e(f'<path d="M{cx - bw / 2:.2f},{yb:.2f} L{cx - bw / 2:.2f},{yt + 12:.2f} '
      f'Q{cx:.2f},{yt - 2:.2f} {cx + bw / 2:.2f},{yt + 12:.2f} L{cx + bw / 2:.2f},{yb:.2f} z" '
      f'fill="#dfe9f3" stroke="#2f5d8a" stroke-width="0.3"/>')
    text(cx, (yb + yt) / 2, "ГЛАДИЛЬНАЯ ДОСКА", size=2.0, rot=-90, fill="#2f5d8a", weight="bold")
    # утюг на полке
    iy = v.Z(1560 + T)
    e(f'<path d="M{cx - 3:.2f},{iy:.2f} l6,0 l-1.2,-2.4 l-3.2,0 z" fill="#2f5d8a"/>')
    # крючки для доски
    for z in (1300, 900):
        e(f'<circle cx="{cx + bw / 2 + 0.8:.2f}" cy="{v.Z(z):.2f}" r="0.5" fill="#2f5d8a"/>')
    # розетка
    sx, sy = v.X(x1) - 3, v.Z(1700)
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
    dim_h(vl.X(0), vl.X(L1), y1, str(L1), ext_from=FLOOR_Y + 1)
    dim_h(vl.X(L1), vl.X(SIDE), y1, str(L2), ext_from=FLOOR_Y + 1)
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
    # задняя: штанги + полки
    ex = vb.X(0) - 6
    dim_v(vb.Z(RAIL_LOW), vb.Z(0), ex, str(RAIL_LOW), ext_from=vb.X(0))
    dim_v(vb.Z(RAIL), vb.Z(RAIL_LOW), ex, str(RAIL - RAIL_LOW), ext_from=vb.X(0))
    dim_v(vb.Z(H), vb.Z(RAIL), ex, str(H - RAIL), ext_from=vb.X(0))
    dim_v(vb.Z(H), vb.Z(0), ex - 6, str(H), ext_from=vb.X(0))
    # шаг полок в средней секции
    xm = vb.X(B1 + B2 / 2) + 9
    zs = [DRAWER_TOP, 1230, 1550, 1870, ANT]
    for a, b in zip(zs, zs[1:]):
        dim_v(vb.Z(b), vb.Z(a), xm, str(b - a), size=2.0)
    dims_vertical_common(vr, vr.X(SIDE) + 6, "right")
    # ниша доски
    ix = vr.X(R1) + 2.2
    dim_v(vr.Z(1560), vr.Z(PLINTH + T), ix, "1464 доска", size=1.8)

    # --- выноски -------------------------------------------------------
    leader(vb.X(B1 + B2 + 450), vb.Z(ANT - 9), vb.X(B1 + B2 + 60), vb.Z(2420),
           "LED-лента в алюм. профиле\nс рассеивателем (под антресолью)", size=2.0)
    leader(vl.X(L1 / 2), vl.Z(1230 - 9), vl.X(40), vl.Z(1450),
           "LED-лента по\nпереднему краю полок", size=1.9)
    # обозначения секций
    for v, x, s in ((vl, L1 / 2, "Л1"), (vl, L1 + L2 / 2, "Л2"),
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
    dx, dy = ox + door0 * S, yf + WT * S
    r = 800 * S
    dy = yf
    line(dx, dy, dx, dy - r, w=0.3, color="#555")
    e(f'<path d="M{dx:.2f},{dy - r:.2f} A{r:.2f},{r:.2f} 0 0 1 {dx + r:.2f},{dy:.2f}" '
      f'fill="none" stroke="#555" stroke-width="0.2" stroke-dasharray="1 0.8"/>')
    text(ox + 1200 * S, yf + WT * S + 4, "ВХОД", size=2.6, weight="bold")

    # корпуса
    def box(x, y, w, h, fill="#f4efe8"):
        a, b = P(x, y)
        rect(a, b, w * S, h * S, fill=fill, sw=0.3)

    box(0, 0, W, DEPTH)
    box(0, DEPTH, DEPTH, SIDE)
    box(W - DEPTH, DEPTH, DEPTH, SIDE)
    # ящики
    box(B1, 0, B2, DEPTH, fill="url(#drw)")
    box(0, D - L1, DEPTH, L1, fill="url(#drw)")
    # перегородки
    for xx in (B1, B1 + B2):
        line(*P(xx, 0), *P(xx, DEPTH), w=0.4)
    line(*P(0, D - L1), *P(DEPTH, D - L1), w=0.4)
    line(*P(W - DEPTH, DEPTH + R1), *P(W, DEPTH + R1), w=0.4)
    # угловые зоны / открыто
    line(*P(0, DEPTH), *P(DEPTH, DEPTH), w=0.3, color="#c0392b", dash="1.5 1")
    line(*P(W - DEPTH, DEPTH), *P(W, DEPTH), w=0.3, color="#c0392b", dash="1.5 1")
    line(*P(DEPTH, 0), *P(DEPTH, DEPTH), w=0.15, color="#c0392b", dash="1.5 1")
    line(*P(W - DEPTH, 0), *P(W - DEPTH, DEPTH), w=0.15, color="#c0392b", dash="1.5 1")
    # штанги
    for a, b in ((P(T, 300), P(B1, 300)), (P(B1 + B2, 300), P(W - T, 300)),
                 (P(300, DEPTH + 20), P(300, D - L1)), (P(W - 300, DEPTH + 20), P(W - 300, DEPTH + R1))):
        line(*a, *b, w=0.5, color="#555", dash="2 0.8")
    # гладильная доска в нише (вид сверху – узкий прямоугольник)
    a, b = P(W - DEPTH + 80, DEPTH + R1 + 150)
    rect(a, b, 440 * S, 50 * S, fill="#dfe9f3", stroke="#2f5d8a", sw=0.25)
    # LED по фронту антресоли (на плане – пунктир по переднему краю)
    for a, b in ((P(DEPTH, DEPTH - 25), P(W - DEPTH, DEPTH - 25)),
                 (P(DEPTH - 25, DEPTH), P(DEPTH - 25, D)),
                 (P(W - DEPTH + 25, DEPTH), P(W - DEPTH + 25, D))):
        line(*a, *b, w=0.6, color=LED, dash="1.6 0.8")

    # подписи секций
    for x, y, s in ((B1 / 2 + 150, 420, "З1"), (B1 + B2 / 2, 300, "З2"), (B1 + B2 + B3 / 2 - 150, 420, "З3"),
                    (300, D - L1 / 2, "Л1"), (300, DEPTH + L2 / 2 + 120, "Л2"),
                    (W - 300, DEPTH + R1 / 2 + 120, "П1"), (W - 300, DEPTH + R1 + R2 / 2 + 140, "П2")):
        cx, cy = P(x, y)
        e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.2" fill="#fff" stroke="#111" stroke-width="0.25"/>')
        text(cx, cy + 0.8, s, size=2.1, weight="bold")
    cx, cy = P(W / 2, DEPTH + 260)
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
    dim_v(oy + DEPTH * S, oy + (D - L1) * S, xl - 4.5, str(L2), ext_from=xl)
    dim_v(oy + (D - L1) * S, oy + D * S, xl - 4.5, str(L1), ext_from=xl)
    xr2 = ox + (W + WT) * S
    dim_v(oy, oy + D * S, xr2 + 10, str(D), ext_from=xr2)
    dim_v(oy, oy + DEPTH * S, xr2 + 4.5, "600", ext_from=xr2)
    dim_v(oy + DEPTH * S, oy + (DEPTH + R1) * S, xr2 + 4.5, str(R1), ext_from=xr2)
    dim_v(oy + (DEPTH + R1) * S, oy + D * S, xr2 + 4.5, str(R2), ext_from=xr2)
    # глубина
    a, b = P(B1 + B2 + 150, 0)
    leader(*P(W - DEPTH - 20, D - 100), xr2 + 18, oy + D * S + 6,
           "Ниша гладильной доски\n450 × 600 (П2)")


# ===========================================================================
# Легенда, спецификация, штамп
# ===========================================================================
def build_notes():
    x, y = 425, 112
    text(x, y, "УСЛОВНЫЕ ОБОЗНАЧЕНИЯ", size=3.2, weight="bold", anchor="start")
    rows = [
        ("led", "LED-лента 24 В в алюм. профиле с рассеивателем"),
        ("drw", "Выкатной ящик (направляющие полного выдвижения, доводчик)"),
        ("rail", "Штанга для плечиков (овальная, хром/золото)"),
        ("board", "Гладильная доска (вертикальное хранение)"),
        ("corner", "Граница угловой зоны / открыто в угол"),
        ("sock", "Розетка 220 В (для утюга/отпаривателя)"),
    ]
    for i, (k, s) in enumerate(rows):
        yy = y + 7 + i * 6
        if k == "led":
            line(x, yy, x + 10, yy, w=0.7, color=LED, dash="1.6 0.8")
        elif k == "drw":
            rect(x, yy - 2, 10, 4, fill="url(#drw)", sw=0.2)
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
        text(x + 13, yy + 0.9, s, size=2.4, anchor="start")

    y = 165
    text(x, y, "СЕКЦИИ", size=3.2, weight="bold", anchor="start")
    secs = [
        ("Л1", "570", "4 выкатных ящика + 3 полки с LED (сложенные вещи)"),
        ("Л2", "570", "2 яруса штанг (короткая одежда), открыта в угол"),
        ("З1", "900", "2 яруса штанг (рубашки, юбки, брюки), угловая зона"),
        ("З2", "600", "4 выкатных ящика + 3 полки с LED (сумки)"),
        ("З3", "900", "Длинная одежда (пальто, платья), угловая зона"),
        ("П1", "690", "Длинная одежда + полка для обуви Н=350, открыта в угол"),
        ("П2", "450", "Ниша гладильной доски: доска, полка утюга (Н=1560), розетка"),
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
        "Цоколь 80 мм, ящики — фасады 200 мм, ручки-скобы латунь",
        "Антресоль с низа 2200 до потолка 2640, верхняя штанга Н=2130",
        "LED: лента 24 В, 4000 K, блок питания в антресоли, датчик открытия двери",
        "Гладильная доска справа у входа (П2); при необходимости",
        "      ниша П2 переносится зеркально на левую сторону",
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
