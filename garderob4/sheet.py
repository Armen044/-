#!/usr/bin/env python3
"""Гардеробная П-образная — развёртки стен (по 3D-модели заказчика). Лист А2, 1:15.
Внутренние размеры по полу: задняя 334 | 600 | 334; левая 558 | 500; правая 258 | 700 | 200.
Глубина 550, высота 2530, цоколь 70, ЛДСП 16."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                       # noqa: E402
from generate import e, line, rect, LED                    # noqa: E402

F = 1.6
_t = g.text


def text(x, y, s, size=2.6, **kw):
    _t(x, y, s, size=size * F, **kw)


g.text = text
dim_h, dim_v = g.dim_h, g.dim_v

S = 1 / 15
T, D, H, PL = 16, 550, 2530, 70
TOP = H - T                    # низ крыши 2514
ANT = 2100                     # полка антресоли (низ)
RAIL_UP, RAIL_LOW = 2030, 1050 # штанги, 2 яруса
DR_TOP = 800                   # комод в правом ряду
SHOE_N = 11
WOOD, BODY, DARK = "#c9a27c", "#ead8c4", "#5b4636"

# задняя стена: [секция слева 550 под левым рядом] 334 | 16 | 600 | 16 | 334 [550 под правым рядом]
BW = D + 334 + T + 600 + T + 334 + D           # 2400
BX1 = D + 334                                   # перегородка 1
BX2 = BX1 + T + 600                             # перегородка 2
LW = D + 558 + T + 500 + T                      # левая стена 1640
RW = D + 258 + T + 700 + T + 200 + T            # правая стена 1756


class V:
    def __init__(self, ox, fy, w):
        self.ox, self.fy, self.w = ox, fy, w

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    def r(self, x0, x1, z0, z1, fill=BODY, sw=0.2, **kw):
        rect(self.X(x0), self.Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, sw=sw, **kw)

    def base(self):
        rect(self.X(0), self.Z(H + 100), self.w * S, 100 * S, fill="url(#wall)", sw=0.25)   # потолок
        self.r(0, self.w, 0, H, fill="#f7f1ea", sw=0.35)
        self.r(0, self.w, 0, PL, fill="url(#hatch)")
        self.r(0, self.w, PL, PL + T)
        self.r(0, self.w, TOP, H)
        line(self.X(0) - 4, self.Z(0), self.X(self.w) + 4, self.Z(0), w=0.5)

    def panel(self, x):
        self.r(x, x + T, PL + T, TOP)

    def shelf(self, x0, x1, z, led=True):
        self.r(x0, x1, z, z + T)
        if led:
            line(self.X(x0) + 0.4, self.Z(z) + 0.5, self.X(x1) - 0.4, self.Z(z) + 0.5, w=0.7, color=LED, dash="1.5 0.6")

    def rail(self, x0, x1, z):
        line(self.X(x0) + 0.5, self.Z(z), self.X(x1) - 0.5, self.Z(z), w=0.7, color="#222")
        for xx in (x0, x1):
            e(f'<circle cx="{self.X(xx):.2f}" cy="{self.Z(z):.2f}" r="0.6" fill="#222"/>')

    def clothes(self, x0, x1, z, length):
        n = max(1, int((x1 - x0) / 120))
        st = (x1 - x0) / (n + 1)
        for i in range(1, n + 1):
            cx = self.X(x0 + st * i)
            hw = min(110, st * 0.8) * S
            y = self.Z(z)
            e(f'<path d="M{cx:.2f},{y:.2f} l{-hw / 2:.2f},1.2 l{hw:.2f},0 z" fill="none" stroke="#888" stroke-width="0.15"/>')
            rect(cx - hw / 2, y + 1.2, hw, length * S - 1.2, fill="#efeae4", stroke="#b5aca2", sw=0.12)

    def section(self, x0, x1):
        """Боковой ряд в разрезе (виден торцом)."""
        self.r(x0, x1, PL, H, fill="url(#drw)", sw=0.3)
        text((self.X(x0) + self.X(x1)) / 2, self.Z(H / 2), "боковой ряд 550 (разрез)", size=1.6, rot=-90, fill="#555")

    def vdims(self, zs, x, ext, size=1.8):
        for a, b in zip(zs, zs[1:]):
            dim_v(self.Z(b), self.Z(a), x, str(b - a), ext_from=ext, size=size)

    def hdims(self, xs, y, ext, size=1.9):
        for a, b in zip(xs, xs[1:]):
            dim_h(self.X(a), self.X(b), y, str(round(b - a)), ext_from=ext, size=size if b - a > 40 else 1.4)

    def mark(self, x, s):
        cx, cy = self.X(x), self.Z(H) - 12
        e(f'<line x1="{cx:.2f}" y1="{cy - 4:.2f}" x2="{cx:.2f}" y2="{self.Z(H) - 1:.2f}" stroke="#c0392b" stroke-width="0.3"/>')
        e(f'<path d="M{cx - 1:.2f},{self.Z(H) - 2.5:.2f} l1,1.6 l1,-1.6 z" fill="#c0392b"/>')
        text(cx, cy - 5, s, size=2.6, fill="#c0392b", weight="bold")


def hanging(v, x0, x1, double=True, length=1500):
    v.shelf(x0, x1, ANT)
    if double:
        v.rail(x0, x1, RAIL_UP)
        v.rail(x0, x1, RAIL_LOW)
        v.clothes(x0, x1, RAIL_UP, 900)
        v.clothes(x0, x1, RAIL_LOW, 850)
    else:
        v.rail(x0, x1, RAIL_UP)
        v.clothes(x0, x1, RAIL_UP, length)


def back_wall(ox, fy):
    v = V(ox, fy, BW)
    v.base()
    v.section(0, D)
    v.section(BW - D, BW)
    v.panel(BX1)
    v.panel(BX2)
    hanging(v, D, BX1)
    hanging(v, BX2 + T, BW - D)
    # обувные полки в центре
    step = (ANT - PL - T) / (SHOE_N + 1)
    zs = [round(PL + T + step * (i + 1)) for i in range(SHOE_N)]
    for z in zs:
        v.shelf(BX1 + T, BX2, z)
    v.shelf(BX1 + T, BX2, ANT)
    v.hdims([0, D, BX1, BX1 + T, BX2, BX2 + T, BW - D, BW], v.Z(0) + 5, v.Z(0) + 0.5)
    dim_h(v.X(0), v.X(BW), v.Z(0) + 12, str(BW), size=2.4)
    v.vdims([0, PL, RAIL_LOW, RAIL_UP, ANT, TOP, H], v.X(0) - 5, v.X(0))
    dim_v(v.Z(H), v.Z(0), v.X(0) - 12, str(H), ext_from=v.X(0), size=2.4)
    v.vdims([PL + T, zs[0]] + [zs[1]], v.X(BX2) - 3, None, size=1.5)
    text(v.X((BX1 + BX2) / 2), v.Z(ANT) - 13, f"{SHOE_N} полок для обуви, шаг {round(step)}", size=1.6, weight="bold")
    v.mark(0, "1")
    v.mark(BW, "2")
    return v


def left_wall(ox, fy):
    """Левая стена: смотрим из гардеробной; слева – вход, справа – угол с задней стеной."""
    v = V(ox, fy, LW)
    v.base()
    x_sh0, x_sh1 = T, T + 500                 # открытые полки у входа
    x_c0 = x_sh1 + T                           # угловая зона 558
    v.panel(0)
    v.panel(x_sh1)
    v.section(LW - D, LW)
    step = (ANT - PL - T) / 8
    for i in range(1, 8):
        v.shelf(x_sh0, x_sh1, round(PL + T + step * i))
    v.shelf(x_sh0, x_sh1, ANT)
    hanging(v, x_c0, LW - D, double=False)
    text(v.X((x_sh0 + x_sh1) / 2), v.Z(1300), "открытые полки", size=1.8, weight="bold")
    text(v.X((x_sh0 + x_sh1) / 2), v.Z(1300) + 3.5, f"7 полок, шаг {round(step)}, LED", size=1.5)
    v.hdims([0, T, x_sh1, x_c0, LW - D, LW], v.Z(0) + 5, v.Z(0) + 0.5)
    dim_h(v.X(0), v.X(LW), v.Z(0) + 12, str(LW), size=2.4)
    v.vdims([0, PL, RAIL_UP, ANT, TOP, H], v.X(LW) + 5, v.X(LW))
    v.vdims([PL + T, round(PL + T + step)], v.X(x_sh1) - 3, None, size=1.5)
    v.mark(0, "3")
    v.mark(LW, "1")
    return v


def right_wall(ox, fy):
    """Правая стена: слева – угол с задней стеной, справа – вход."""
    v = V(ox, fy, RW)
    v.base()
    v.section(0, D)
    x_h0 = D + 258 + T                         # ниша 700
    x_h1 = x_h0 + 700
    x_n0 = x_h1 + T                            # ниша 200 (гладильная доска)
    v.panel(D + 258)
    v.panel(x_h1)
    v.panel(RW - T)
    # угол 258 – продолжение штанг задней стены
    v.shelf(D, D + 258, ANT)
    # 700: комод + штанга
    v.r(x_h0, x_h1, PL + T, DR_TOP)
    for i in range(4):
        z0 = PL + T + i * (DR_TOP - PL - T) / 4
        v.r(x_h0 + 3, x_h1 - 3, z0 + 2, z0 + (DR_TOP - PL - T) / 4 - 2, fill="#d9bea2", sw=0.25)
        cx = v.X((x_h0 + x_h1) / 2)
        line(cx - 5, v.Z(z0 + 140), cx + 5, v.Z(z0 + 140), w=0.5, color="#222")
    v.shelf(x_h0, x_h1, DR_TOP, led=False)
    hanging(v, x_h0, x_h1, double=False, length=1100)
    text(v.X((x_h0 + x_h1) / 2), v.Z(DR_TOP / 2 + 40), "КОМОД — 4 ящика", size=1.8, weight="bold")
    # 200: гладильная доска + 2 полки сверху
    for z in (1750, 1950):
        v.shelf(x_n0, RW - T, z, led=False)
    v.shelf(x_n0, RW - T, ANT)
    v.r(x_n0 + 40, x_n0 + 110, PL + T + 20, PL + T + 1400, fill="#cfe0ef", sw=0.25)
    text(v.X(x_n0 + 100), v.Z(800), "гладильная доска", size=1.5, rot=-90, fill="#2f5d8a")
    v.hdims([0, D, D + 258, x_h0, x_h1, x_n0, RW - T, RW], v.Z(0) + 5, v.Z(0) + 0.5)
    dim_h(v.X(0), v.X(RW), v.Z(0) + 12, str(RW), size=2.4)
    v.vdims([0, PL, DR_TOP + T, RAIL_UP, ANT, TOP, H], v.X(RW) + 5, v.X(RW))
    v.vdims([PL + T, 1750, 1950, ANT], v.X(x_n0) - 3, None, size=1.5)
    v.mark(0, "2")
    v.mark(RW, "4")
    return v


def plan(ox, oy):
    s = 1 / 30
    P = lambda x, y: (ox + x * s, oy + y * s)       # noqa: E731
    text(ox + BW * s / 2, oy - 12, "ПЛАН", size=2.8, weight="bold")
    rect(ox, oy, BW * s, D * s, fill=BODY, sw=0.3)
    rect(ox, oy + D * s, D * s, (LW - D) * s, fill=BODY, sw=0.3)
    rect(ox + (BW - D) * s, oy + D * s, D * s, (RW - D) * s, fill=BODY, sw=0.3)
    rect(*P(D, D), (BW - 2 * D) * s, (max(LW, RW) - D) * s, fill="#fff", sw=0.2, dash="1 0.8")
    for (x, y, t_) in ((BW / 2, 250, "1"), (BW + 150, D / 2, "2"), (-150, (LW + D) / 2, "3"), (BW + 150, (RW + D) / 2, "4")):
        cx, cy = P(x, y)
        text(cx, cy + 1, t_, size=2.2, fill="#c0392b", weight="bold")
    text(*P(BW / 2, D + 350), "проход 1268", size=1.7, fill="#555")
    for k, (a, b) in enumerate(((D, BX1), (BX1 + T, BX2), (BX2 + T, BW - D))):
        pass
    dim_h(ox, ox + BW * s, oy - 3, str(BW), size=1.7)


def notes(x, y):
    text(x, y, "УСЛОВНЫЕ ОБОЗНАЧЕНИЯ", size=2.6, weight="bold", anchor="start")
    items = [(LED, "LED-лента в профиле по переднему краю полок"), ("#222", "штанга"),
             ("url(#drw)", "боковой ряд в разрезе"), ("url(#hatch)", "цоколь 70")]
    for k, (c, s) in enumerate(items):
        yy = y + 8 + k * 6
        if c.startswith("url"):
            rect(x, yy - 2.2, 10, 4, fill=c, sw=0.2)
        else:
            line(x, yy, x + 10, yy, w=0.8, color=c, dash="1.5 0.6" if c == LED else None)
        text(x + 13, yy + 1, s, size=1.9, anchor="start")
    y2 = y + 38
    text(x, y2, "ПРИМЕЧАНИЕ", size=2.6, weight="bold", anchor="start")
    rows = ["1. Корпус ЛДСП 16, глубина 550, высота 2530, цоколь 70.",
            "2. Размеры ниш по полу — в свету (по 3D-модели): 334 / 600 / 334; 558 / 500; 258 / 700 / 200.",
            "3. Высоты полок и штанг — уточнить по месту; штанги 2 яруса: 2030 и 1050.",
            "4. Подсветка — в каждой открытой полке и под полкой антресоли."]
    for k, s in enumerate(rows):
        text(x, y2 + 7 + k * 5.5, s, size=1.9, anchor="start")


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)
    text(297, 20, "РАЗВЁРТКИ СТЕН. ГАРДЕРОБНАЯ", size=4.4, weight="bold")
    fy = 210
    for v, t_ in ((back_wall(40, fy), "РАЗВЁРТКА 1–2 (задняя стена)"), (left_wall(255, fy), "РАЗВЁРТКА 3–1 (левая стена)"),
                  (right_wall(400, fy), "РАЗВЁРТКА 2–4 (правая стена)")):
        text(v.X(v.w / 2), v.Z(0) + 24, t_, size=2.4, weight="bold")
    plan(60, 285)
    notes(190, 270)
    bx, by, bw, bh = 405, 362, 180, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    line(bx + 120, by + 14, bx + 120, by + bh, w=0.3)
    text(bx + bw / 2, by + 7, "ГАРДЕРОБНАЯ П-ОБРАЗНАЯ", size=3.4, weight="bold")
    text(bx + bw / 2, by + 12, "развёртки стен", size=1.9)
    text(bx + 3, by + 22, "Высота 2530, глубина 550, цоколь 70", size=2.0, anchor="start")
    text(bx + 3, by + 30, "Корпус ЛДСП 16", size=2.0, anchor="start")
    text(bx + 3, by + 38, "Размеры в мм", size=2.0, anchor="start")
    text(bx + 150, by + 24, "Масштаб 1:15", size=2.0)
    text(bx + 150, by + 34, "Лист 1", size=2.6, weight="bold")
    e('</svg>')
    open(os.path.join(HERE, "sheet1.svg"), "w", encoding="utf-8").write("\n".join(g.out))


if __name__ == "__main__":
    main()
