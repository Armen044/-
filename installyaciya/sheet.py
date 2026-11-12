#!/usr/bin/env python3
"""Обшивка инсталляции со шкафами (по эскизу заказчика). Лист А2, 1:12.
Ширина 2483: низ — короб инсталляции 2050 × 1154; над ним шкафы 860 | 330 | 860 высотой 1790;
справа на всю высоту шкаф 433. Глубина 195, ЛДСП 16."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                       # noqa: E402
from generate import e, line, rect, LED                    # noqa: E402

F = 2.0
_t = g.text


def text(x, y, s, size=2.6, **kw):
    _t(x, y, s, size=size * F, **kw)


g.text = text
dim_h, dim_v = g.dim_h, g.dim_v

S = 1 / 12
T, D = 16, 195
W, LOW_W, RIGHT = 2483, 2050, 433
LOW_H, UP_H = 1154, 1790
H = LOW_H + UP_H                       # 2944
SECS = [860, 330, 860]                 # верхние шкафы
GAP, GOLA = 2, 24                      # зазор фасадов, вертикальный профиль Gola
BODY, FACE, GLASS = "#ead8c4", "#f6f3ee", "#d4e6ec"


class V:
    def __init__(self, ox, fy):
        self.ox, self.fy = ox, fy

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    def r(self, x0, x1, z0, z1, fill=BODY, sw=0.25, **kw):
        rect(self.X(x0), self.Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, sw=sw, **kw)


def shelves(z0, z1, lo=300, hi=400):
    """Полки между z0 (верх дна) и z1 (низ крыши) с одинаковым просветом 300–400."""
    n = 1
    while (z1 - z0 - n * T) / (n + 1) > hi:
        n += 1
    c = (z1 - z0 - n * T) // (n + 1)
    first = z1 - n * (c + T)
    return [first + i * (c + T) for i in range(n)]


def columns():
    """[(x0, x1, z0, z1, вид)] – корпуса шкафов."""
    cols, x = [], 0
    for w, k in zip(SECS, ("gola", "glass", "gola")):
        cols.append((x, x + w, LOW_H, H, k))
        x += w
    cols.append((LOW_W, W, 0, H, "right"))
    return cols


def carcass_view(v):
    """Вид без фасадов: корпуса, полки, подсветка, размеры в свету."""
    v.r(0, LOW_W, 0, LOW_H, fill="url(#drw)", sw=0.35)
    text(v.X(LOW_W / 2), v.Z(LOW_H / 2), "КОРОБ ИНСТАЛЛЯЦИИ", size=2.2, weight="bold")
    text(v.X(LOW_W / 2), v.Z(LOW_H / 2) + 5.5, "обшивка, ревизионный люк — по месту", size=1.6)
    for x0, x1, z0, z1, k in columns():
        v.r(x0, x1, z0, z1, fill="#fbf8f3", sw=0.35)
        for a, b in ((x0, x0 + T), (x1 - T, x1)):
            v.r(a, b, z0, z1)
        v.r(x0 + T, x1 - T, z0, z0 + T)
        v.r(x0 + T, x1 - T, z1 - T, z1)
        zs = shelves(z0 + T, z1 - T)
        for z in zs:
            v.r(x0 + T, x1 - T, z, z + T)
            if k == "glass":
                line(v.X(x0 + T) + 0.4, v.Z(z) + 0.5, v.X(x1 - T) - 0.4, v.Z(z) + 0.5, w=0.8, color=LED, dash="1.5 0.6")
        pts = [z0 + T] + [p for z in zs for p in (z, z + T)] + [z1 - T]
        for a, b in zip(pts[0::2], pts[1::2]):
            dim_v(v.Z(b), v.Z(a), v.X(x1 - T) - 3, str(b - a), size=1.5)
        text(v.X((x0 + x1) / 2), v.Z(z1) + 6, f"{x1 - x0}", size=1.8, weight="bold", fill="#8a6a3f")


def front_view(v):
    """Вид с фасадами."""
    v.r(0, LOW_W, 0, LOW_H, fill="#efe8de", sw=0.35)
    text(v.X(LOW_W / 2), v.Z(LOW_H / 2), "ОБШИВКА ИНСТАЛЛЯЦИИ", size=2.2, weight="bold")
    for x0, x1, z0, z1, k in columns():
        if k == "gola":
            mid = (x0 + x1) / 2
            v.r(mid - GOLA / 2, mid + GOLA / 2, z0, z1, fill="#1b1b1b", sw=0.2)       # профиль Gola
            for a, b in ((x0 + GAP, mid - GOLA / 2), (mid + GOLA / 2, x1 - GAP)):
                v.r(a, b, z0 + GAP, z1 - GAP, fill=FACE, sw=0.4)
                text(v.X((a + b) / 2), v.Z((z0 + z1) / 2), f"{round(b - a)}×{z1 - z0 - 2 * GAP}", size=1.6)
        elif k == "glass":
            v.r(x0 + GAP, x1 - GAP, z0 + GAP, z1 - GAP, fill="#3b3b3b", sw=0.4)
            v.r(x0 + GAP + 20, x1 - GAP - 20, z0 + GAP + 20, z1 - GAP - 20, fill=GLASS, sw=0.2)
            for z in shelves(z0 + T, z1 - T):
                line(v.X(x0 + 25), v.Z(z), v.X(x1 - 25), v.Z(z), w=0.5, color=LED, dash="1.5 0.6")
            text(v.X((x0 + x1) / 2), v.Z((z0 + z1) / 2), "стекло в алюм. раме", size=1.5, rot=-90)
        else:
            v.r(x0 + GAP, x1 - GAP, z0 + GAP, z1 - GAP, fill=FACE, sw=0.4)
            text(v.X((x0 + x1) / 2), v.Z(H / 2), f"{x1 - x0 - 2 * GAP}×{z1 - z0 - 2 * GAP}", size=1.6)
    # размеры
    y = v.Z(0)
    line(v.X(0) - 4, y, v.X(W) + 4, y, w=0.5)
    dim_h(v.X(0), v.X(LOW_W), y + 6, str(LOW_W), ext_from=y + 0.5, size=2.0)
    dim_h(v.X(LOW_W), v.X(W), y + 6, str(RIGHT), ext_from=y + 0.5, size=2.0)
    dim_h(v.X(0), v.X(W), y + 13, str(W), size=2.4)
    x = 0
    for w in SECS:
        dim_h(v.X(x), v.X(x + w), v.Z(H) - 5, str(w), ext_from=v.Z(H), size=2.0)
        x += w
    dim_v(v.Z(LOW_H), v.Z(0), v.X(0) - 6, str(LOW_H), ext_from=v.X(0), size=2.0)
    dim_v(v.Z(H), v.Z(LOW_H), v.X(0) - 6, str(UP_H), ext_from=v.X(0), size=2.0)
    dim_v(v.Z(H), v.Z(0), v.X(0) - 13, str(H), ext_from=v.X(0), size=2.4)


def section(ox, fy):
    v = V(ox, fy)
    text(v.X(D / 2), v.Z(H) - 12, "РАЗРЕЗ", size=2.4, weight="bold")
    rect(v.X(-60), v.Z(H + 60), 60 * S, (H + 60) * S, fill="url(#wall)", sw=0.2)
    v.r(0, D, 0, LOW_H, fill="url(#drw)", sw=0.3)
    v.r(0, D, LOW_H, H, fill="#fbf8f3", sw=0.3)
    for z in [LOW_H, H - T] + shelves(LOW_H + T, H - T):
        v.r(0, D - 20, z, z + T)
    v.r(D, D + 18, LOW_H, H, fill=FACE, sw=0.3)
    dim_h(v.X(0), v.X(D), v.Z(0) + 6, str(D), ext_from=v.Z(0), size=2.0)
    dim_v(v.Z(H), v.Z(0), v.X(D + 18) + 6, str(H), ext_from=v.X(D + 18), size=2.0)


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)
    text(297, 20, "ОБШИВКА ИНСТАЛЛЯЦИИ СО ШКАФАМИ", size=4.2, weight="bold")
    fy = 300
    v1 = V(45, fy)
    front_view(v1)
    text(v1.X(W / 2), fy + 30, "ВИД С ФАСАДАМИ", size=2.6, weight="bold")
    v2 = V(285, fy)
    carcass_view(v2)
    line(v2.X(0) - 4, v2.Z(0), v2.X(W) + 4, v2.Z(0), w=0.5)
    text(v2.X(W / 2), fy + 30, "ВИД БЕЗ ФАСАДОВ (полки, размеры в свету)", size=2.6, weight="bold")
    section(525, fy)
    bx, by, bw, bh = 405, 362, 180, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    line(bx + 120, by + 14, bx + 120, by + bh, w=0.3)
    text(bx + bw / 2, by + 7, "ОБШИВКА ИНСТАЛЛЯЦИИ", size=3.2, weight="bold")
    text(bx + bw / 2, by + 12, "фасады, полки, размеры", size=1.7)
    text(bx + 3, by + 22, f"{W} × {D} × {H}, ЛДСП 16", size=1.9, anchor="start")
    text(bx + 3, by + 30, "Gola вертикальный в шкафах 860", size=1.9, anchor="start")
    text(bx + 3, by + 38, "330 — стекло в алюм. раме, LED", size=1.9, anchor="start")
    text(bx + 150, by + 24, "Масштаб 1:12", size=1.6)
    text(bx + 150, by + 34, "Лист 1", size=2.4, weight="bold")
    e('</svg>')
    open(os.path.join(HERE, "sheet1.svg"), "w", encoding="utf-8").write("\n".join(g.out))


if __name__ == "__main__":
    main()
