#!/usr/bin/env python3
"""Шкаф со столом и тумбой (по видео-модели заказчика) — развёртка. Лист А2, 1:15.
Слева направо: стол 2700 (тумба 800 с ящиками, над правым краем — открытая ниша 600 с LED),
шкаф 2 × 600 (низ 2350 + антресоль 550, цоколь 70), справа низкая тумба 2150 × 350."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                       # noqa: E402
from generate import e, line, rect, LED                    # noqa: E402

F = 1.9
_t = g.text


def text(x, y, s, size=2.6, **kw):
    _t(x, y, s, size=size * F, **kw)


g.text = text
dim_h, dim_v = g.dim_h, g.dim_v

S = 1 / 12
T, PL = 16, 70
LOW, ANT = 2350, 550
H = PL + LOW + ANT                    # 2970
DESK_L, DESK_H, TOP_T = 2700, 750, 32
DESK = DESK_H + TOP_T                 # 782
PED = 800
SEC = 600
TB_W, TB_D, TB_H = 2150, 350, DESK    # низкая тумба
X_NICHE = DESK_L - SEC                # ниша над правым краем стола
X_W = DESK_L                          # шкаф
X_TB = X_W + 2 * SEC                  # тумба
W_ALL = X_TB + TB_W
BODY, BACK, FRONT, TOPC = "#e9e6e1", "#fbfaf8", "#f4f2ee", "#4a3b31"


class V:
    def __init__(self, ox, fy):
        self.ox, self.fy = ox, fy

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    def r(self, x0, x1, z0, z1, fill=BODY, sw=0.25, **kw):
        rect(self.X(x0), self.Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, sw=sw, **kw)

    def box(self, x0, x1, z0, z1, fill=BACK):
        self.r(x0, x1, z0, z1, fill=fill, sw=0.35)
        self.r(x0, x0 + T, z0, z1)
        self.r(x1 - T, x1, z0, z1)
        self.r(x0 + T, x1 - T, z0, z0 + T)
        self.r(x0 + T, x1 - T, z1 - T, z1)

    def shelf(self, x0, x1, z, led=False):
        self.r(x0, x1, z, z + T)
        if led:
            line(self.X(x0) + 0.4, self.Z(z) + 0.5, self.X(x1) - 0.4, self.Z(z) + 0.5, w=0.8, color=LED, dash="1.5 0.6")

    def gaps(self, x, pts, size=1.4):
        """pts: [низ просвета, верх, низ, верх, ...]"""
        for a, b in zip(pts[0::2], pts[1::2]):
            dim_v(self.Z(b), self.Z(a), self.X(x), str(round(b - a)), size=size)


def even(z0, z1, n):
    c = (z1 - z0 - n * T) // (n + 1)
    first = z1 - n * (c + T)
    return [first + i * (c + T) for i in range(n)]


def interior(v):
    line(v.X(0) - 4, v.Z(0), v.X(W_ALL) + 4, v.Z(0), w=0.5)
    # ---- стол: тумба 800 слева, столешница 2700
    v.box(0, PED, 0, DESK_H)
    for i in range(3):
        z0 = T + 4 + i * (DESK_H - 2 * T) / 3
        v.r(T + 6, PED - T - 6, z0, z0 + (DESK_H - 2 * T) / 3 - 8, fill="#efe9e1", sw=0.25)
    text(v.X(PED / 2), v.Z(DESK_H / 2), "тумба 800, 3 ящика", size=1.6, weight="bold")
    v.r(0, DESK_L, DESK_H, DESK, fill=TOPC, sw=0.3)
    # под нишей – открытая полка под столом
    v.box(X_NICHE, DESK_L, 0, DESK_H)
    zs = [380]
    v.shelf(X_NICHE + T, DESK_L - T, zs[0])
    v.gaps(DESK_L - T - 4, [T, zs[0], zs[0] + T, DESK_H - T])
    text(v.X((PED + X_NICHE) / 2), v.Z(DESK_H / 2), "место для ног", size=1.6, fill="#777")
    # ---- открытая ниша над столом с LED + антресоль
    z0, z1 = DESK, PL + LOW
    v.box(X_NICHE, DESK_L, z0, z1, fill="#fff6dc")
    ns = even(z0 + T, z1 - T, 4)
    for z in ns:
        v.shelf(X_NICHE + T, DESK_L - T, z, led=True)
    v.gaps(DESK_L - T - 4, [z0 + T] + [p for z in ns for p in (z, z + T)] + [z1 - T])
    text(v.X(X_NICHE + SEC / 2), v.Z((z0 + z1) / 2) + 2, "ниша, LED", size=1.6, weight="bold", fill="#8a6a3f")
    v.box(X_NICHE, DESK_L, PL + LOW, H)
    v.gaps(DESK_L - T - 4, [PL + LOW + T, H - T])
    # ---- шкаф 2 × 600
    for k in range(2):
        x0, x1 = X_W + k * SEC, X_W + (k + 1) * SEC
        v.r(x0 + 40, x1 - 40, 0, PL, fill="url(#hatch)", sw=0.15)
        v.box(x0, x1, PL, PL + LOW)
        v.box(x0, x1, PL + LOW, H)
        b = PL + T
        s0 = 500                                 # полка над нижним отсеком
        dr = [(s0 + T + 10, s0 + T + 170), (s0 + T + 180, s0 + T + 340)]
        s1 = s0 + T + 360                        # полка над ящиками
        v.shelf(x0 + T, x1 - T, s0)
        for a, c in dr:
            v.r(x0 + T + 8, x1 - T - 8, a, c, fill="#efe9e1", sw=0.3)
            cx = (v.X(x0) + v.X(x1)) / 2
            line(cx - 4, v.Z(c - 40), cx + 4, v.Z(c - 40), w=0.5, color="#222")
        v.shelf(x0 + T, x1 - T, s1)
        top = PL + LOW - T
        ss = even(s1 + T, top, 4)
        for z in ss:
            v.shelf(x0 + T, x1 - T, z)
        pts = [b, s0, s1 + T] + [p for z in ss for p in (z, z + T)] + [top]
        v.gaps(x1 - T - 4, [b, s0] + pts[2:])
        dim_v(v.Z(s0 + T + 340), v.Z(s0 + T + 10), v.X(x0 + T + 30), "2 ящика", size=1.2)
        v.gaps(x1 - T - 4, [PL + LOW + T, H - T])
        text(v.X((x0 + x1) / 2), v.Z(H) + 5, f"секция {k + 1} — 600", size=1.6, weight="bold", fill="#8a6a3f")
    # ---- низкая тумба 2150 × 350
    v.box(X_TB, W_ALL, PL, TB_H)
    v.r(X_TB + 40, W_ALL - 40, 0, PL, fill="url(#hatch)", sw=0.15)
    for k in range(1, 3):
        xx = X_TB + k * TB_W / 3
        v.r(xx - T / 2, xx + T / 2, PL + T, TB_H - T)
    v.shelf(X_TB + T, W_ALL - T, PL + T + (TB_H - PL - 2 * T) / 2 - T / 2)
    text(v.X(X_TB + TB_W / 2), v.Z(TB_H) - 4, f"тумба {TB_W} × {TB_D} × {TB_H}", size=1.7, weight="bold")


def fronts(v):
    line(v.X(0) - 4, v.Z(0), v.X(W_ALL) + 4, v.Z(0), w=0.5)
    G = 2
    # стол
    v.box(0, PED, 0, DESK_H, fill=BODY)
    for i in range(3):
        z0 = i * DESK_H / 3
        v.r(G, PED - G, z0 + G, z0 + DESK_H / 3 - G, fill=FRONT, sw=0.35)
    v.r(X_NICHE, DESK_L, 0, DESK_H, fill=BACK, sw=0.3)
    v.r(0, DESK_L, DESK_H, DESK, fill=TOPC, sw=0.3)
    v.r(X_NICHE, DESK_L, DESK, PL + LOW, fill="#fff6dc", sw=0.3)
    v.r(X_NICHE + G, DESK_L - G, PL + LOW + G, H - G, fill=FRONT, sw=0.35)
    # шкаф
    for k in range(2):
        x0, x1 = X_W + k * SEC, X_W + (k + 1) * SEC
        v.r(x0 + 40, x1 - 40, 0, PL, fill="url(#hatch)", sw=0.15)
        v.r(x0 + G, x1 - G, PL + G, PL + LOW - G, fill=FRONT, sw=0.4)
        v.r(x0 + G, x1 - G, PL + LOW + G, H - G, fill=FRONT, sw=0.4)
    # тумба
    v.r(X_TB + 40, W_ALL - 40, 0, PL, fill="url(#hatch)", sw=0.15)
    for k in range(3):
        a = X_TB + k * TB_W / 3
        v.r(a + G, a + TB_W / 3 - G, PL + G, TB_H - G, fill=FRONT, sw=0.4)


def dims(v):
    y = v.Z(0)
    xs = [0, PED, X_NICHE, DESK_L, X_W + SEC, X_TB, W_ALL]
    for a, b in zip(xs, xs[1:]):
        dim_h(v.X(a), v.X(b), y + 5, str(b - a), ext_from=y + 0.5, size=1.9)
    dim_h(v.X(0), v.X(DESK_L), y + 11, f"{DESK_L} столешница", size=1.9)
    dim_h(v.X(0), v.X(W_ALL), y + 17, str(W_ALL), size=2.2)
    xr = v.X(X_TB) - 3
    for a, b in ((0, PL), (PL, PL + LOW), (PL + LOW, H)):
        dim_v(v.Z(b), v.Z(a), v.X(X_W + 2 * SEC) + 4, str(b - a), ext_from=v.X(X_W + 2 * SEC), size=1.8)
    dim_v(v.Z(H), v.Z(0), v.X(X_W + 2 * SEC) + 10, str(H), ext_from=v.X(X_W + 2 * SEC), size=2.2)
    dim_v(v.Z(DESK_H), v.Z(0), v.X(0) - 4, str(DESK_H), ext_from=v.X(0), size=1.8)
    dim_v(v.Z(DESK), v.Z(DESK_H), v.X(0) - 4, str(TOP_T), ext_from=v.X(0), size=1.4)
    dim_v(v.Z(DESK), v.Z(0), v.X(0) - 10, str(DESK), ext_from=v.X(0), size=1.8)



def stamp(sheet):
    bx, by, bw, bh = 445, 362, 140, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    text(bx + bw / 2, by + 7, "ШКАФ СО СТОЛОМ", size=3.0, weight="bold")
    text(bx + bw / 2, by + 12, f"развёртка, М 1:12 · лист {sheet}", size=1.6)
    text(bx + 3, by + 21, f"Шкаф 2 × 600: {LOW} + антресоль {ANT} + цоколь {PL} = {H}", size=1.6, anchor="start")
    text(bx + 3, by + 28, f"Стол {DESK_L}, высота {DESK_H} + {TOP_T}, тумба {PED}", size=1.6, anchor="start")
    text(bx + 3, by + 35, f"Тумба низкая {TB_W} × {TB_D}; ЛДСП 16", size=1.6, anchor="start")
    text(bx + 3, by + 42, "Размеры в мм", size=1.6, anchor="start")


def page(name, title, fn, sheet):
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)
    text(297, 20, title, size=4.0, weight="bold")
    v = V(45, 320)
    fn(v)
    dims(v)
    stamp(sheet)
    e('</svg>')
    open(os.path.join(HERE, name), "w", encoding="utf-8").write("\n".join(g.out))


def main():
    page("sheet1.svg", "ШКАФ СО СТОЛОМ И ТУМБОЙ — ВИД С ФАСАДАМИ", fronts, 1)
    page("sheet2.svg", "ШКАФ СО СТОЛОМ И ТУМБОЙ — ВИД БЕЗ ФАСАДОВ (размеры в свету)", interior, 2)


if __name__ == "__main__":
    main()
