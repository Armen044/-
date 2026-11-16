#!/usr/bin/env python3
"""Шкаф в коридоре 900 + 900 + 450, глубина 520 — три варианта наполнения (вид без фасадов)."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                       # noqa: E402
from generate import e, line, rect, LED                    # noqa: E402

F = 1.8
_t = g.text


def text(x, y, s, size=2.6, **kw):
    _t(x, y, s, size=size * F, **kw)


g.text = text
dim_h, dim_v = g.dim_h, g.dim_v

S = 1 / 20
T, D, H, PL, ANT = 16, 520, 3000, 80, 570
SECS = [900, 900, 450]
W = sum(SECS)
TOP = H - ANT                     # низ антресоли (корпуса)
BODY, BACK, DRW, SHOE = "#e9e6e1", "#fbfaf8", "#efe5d6", "#cfc2b0"


class V:
    def __init__(self, ox, fy):
        self.ox, self.fy = ox, fy

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    def r(self, x0, x1, z0, z1, fill=BODY, sw=0.22, **kw):
        rect(self.X(x0), self.Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, sw=sw, **kw)

    def box(self, x0, x1, z0, z1):
        self.r(x0, x1, z0, z1, fill=BACK, sw=0.3)
        for a, b in ((x0, x0 + T), (x1 - T, x1)):
            self.r(a, b, z0, z1)
        self.r(x0 + T, x1 - T, z0, z0 + T)
        self.r(x0 + T, x1 - T, z1 - T, z1)

    def shelf(self, x0, x1, z):
        self.r(x0 + T, x1 - T, z, z + T)

    def rail(self, x0, x1, z, length):
        line(self.X(x0 + T + 5), self.Z(z), self.X(x1 - T - 5), self.Z(z), w=0.6, color="#222")
        n = max(2, int((x1 - x0) / 110))
        st = (x1 - x0 - 2 * T) / (n + 1)
        for i in range(1, n + 1):
            cx = self.X(x0 + T + st * i)
            hw = min(90, st * 0.8) * S
            rect(cx - hw / 2, self.Z(z) + 0.8, hw, length * S - 0.8, fill="#ece7e1", stroke="#b5aca2", sw=0.1)

    def drawers(self, x0, x1, z0, n, h=180):
        for i in range(n):
            a = z0 + i * h
            self.r(x0 + T + 4, x1 - T - 4, a + 4, a + h - 4, fill=DRW, sw=0.25)
            cx = (self.X(x0) + self.X(x1)) / 2
            line(cx - 3, self.Z(a + h - 40), cx + 3, self.Z(a + h - 40), w=0.4, color="#222")
        return z0 + n * h

    def shoes(self, x0, x1, z0, n, step=200, slope=True):
        """Обувные полки (наклонные 15° с бортиком) от z0 с шагом step."""
        for i in range(n):
            z = z0 + i * step
            self.r(x0 + T, x1 - T, z, z + T, fill=SHOE)
            if slope:
                line(self.X(x0 + T), self.Z(z + 120), self.X(x1 - T), self.Z(z + 120), w=0.15, color="#8c7b62", dash="1 0.6")
        return z0 + n * step

    def label(self, x0, x1, z, s, size=1.5):
        text(self.X((x0 + x1) / 2), self.Z(z), s, size=size, weight="bold", fill="#5b4636")


def frame(v):
    x = 0
    edges = [0]
    for w in SECS:
        v.box(x, x + w, PL, TOP)
        v.box(x, x + w, TOP, H)
        v.r(x + 40, x + w - 40, 0, PL, fill="url(#hatch)", sw=0.12)
        x += w
        edges.append(x)
    line(v.X(-200), v.Z(0), v.X(W + 200), v.Z(0), w=0.4)
    for a, b in zip(edges, edges[1:]):
        dim_h(v.X(a), v.X(b), v.Z(0) + 4, str(b - a), ext_from=v.Z(0) + 0.5, size=1.6)
    return edges


def var_a(v):
    e_ = frame(v)
    a0, a1, b0, b1, c0, c1 = e_[0], e_[1], e_[1], e_[2], e_[2], e_[3]
    # 900 №1 — верхняя одежда длинная + обувь внизу
    v.shelf(a0, a1, 1950)
    v.rail(a0, a1, 1880, 1150)
    top = v.shoes(a0, a1, PL + T + 10, 2, step=190)
    v.label(a0, a1, 1300, "ВЕРХНЯЯ ОДЕЖДА")
    v.label(a0, a1, PL + 210, "обувь, 2 полки")
    # 900 №2 — короткая одежда сверху, ящики, обувь
    v.shelf(b0, b1, 1950)
    v.rail(b0, b1, 1880, 850)
    z = v.shoes(b0, b1, PL + T + 10, 3, step=190)
    v.shelf(b0, b1, z)
    v.label(b0, b1, 1450, "куртки, сумки")
    v.label(b0, b1, PL + 300, "обувь, 3 полки")
    # 450 — ящики под мелочь + полки
    z = v.drawers(c0, c1, PL + T, 3)
    for zz in (z, z + 330, z + 660, z + 990, 1950):
        v.shelf(c0, c1, zz)
    v.label(c0, c1, PL + 300, "3 ящика", 1.3)
    v.label(c0, c1, 1200, "полки", 1.3)


def var_b(v):
    e_ = frame(v)
    a0, a1, b0, b1, c0, c1 = e_[0], e_[1], e_[2 - 1], e_[2], e_[2], e_[3]
    # 900 №1 — вся секция под верхнюю одежду (сезонная + гостевая), под ней низкая полка
    v.shelf(a0, a1, 1950)
    v.rail(a0, a1, 1880, 1350)
    v.shelf(a0, a1, 400)
    v.label(a0, a1, 1300, "ВЕРХНЯЯ ОДЕЖДА")
    v.label(a0, a1, 230, "сапоги, коробки")
    # 900 №2 — обувница во всю высоту + 2 ящика
    z = v.drawers(b0, b1, PL + T, 2)
    v.shelf(b0, b1, z)
    z = v.shoes(b0, b1, z + 200, 8, step=200)
    v.label(b0, b1, PL + 200, "2 ящика", 1.4)
    v.label(b0, b1, 1300, "обувные полки, 8 шт")
    # 450 — полки + штанга-ключница сверху
    for zz in (450, 800, 1150, 1500, 1950):
        v.shelf(c0, c1, zz)
    v.label(c0, c1, 1000, "полки", 1.3)
    v.label(c0, c1, 250, "пылесос", 1.3)


def var_c(v):
    e_ = frame(v)
    a0, a1, b0, b1, c0, c1 = e_[0], e_[1], e_[1], e_[2], e_[2], e_[3]
    # 900 №1 и №2 — штанга сверху, внизу выдвижные обувные полки / ящики
    for x0, x1 in ((a0, a1), (b0, b1)):
        v.shelf(x0, x1, 1950)
        v.rail(x0, x1, 1880, 1000)
    v.label(a0, a1, 1350, "ВЕРХНЯЯ ОДЕЖДА")
    v.label(b0, b1, 1350, "ВЕРХНЯЯ ОДЕЖДА")
    z = v.shoes(a0, a1, PL + T + 10, 3, step=200, slope=False)
    v.label(a0, a1, PL + 330, "обувные полки, 3", 1.2)
    z = v.drawers(b0, b1, PL + T, 2, h=200)
    v.shelf(b0, b1, z)
    v.label(b0, b1, PL + 200, "2 ящика", 1.4)
    # 450 — внизу отсек 1200 под пылесос, выше обувные полки
    zv = PL + T + 1200
    v.shelf(c0, c1, zv)
    v.label(c0, c1, PL + 600, "пылесос", 1.2)
    dim_v(v.Z(zv), v.Z(PL + T), v.X(c1 - T) - 2.5, "1200", size=1.2)
    v.shoes(c0, c1, zv + T + 210, 4, step=210)
    v.label(c0, c1, 2250, "обувные полки", 1.1)


def pullout(v, x0, x1, z, length):
    """Выдвижная штанга BELLE под полкой: вид спереди — торец, одежда висит вдоль глубины."""
    cx = (x0 + x1) / 2
    v.r(cx - 40, cx + 40, z, z + 40, fill="#6d6d6d", sw=0.2)              # направляющая
    line(v.X(cx - 30), v.Z(z), v.X(cx - 55), v.Z(z - 60), w=0.4, color="#555")
    line(v.X(cx + 30), v.Z(z), v.X(cx + 55), v.Z(z - 60), w=0.4, color="#555")
    for k in range(3):                                                     # вещи вдоль глубины, видны торцом
        dx = (k - 1) * 22
        v.r(cx + dx - 18, cx + dx + 18, z - 60 - length + k * 60, z - 60, fill="#ece7e1", sw=0.12)


def var_g(v):
    e_ = frame(v)
    a0, a1, b0, b1, c0, c1 = e_[0], e_[1], e_[1], e_[2], e_[2], e_[3]
    # 900 №1 — верхняя одежда + обувь
    v.shelf(a0, a1, 1950)
    v.rail(a0, a1, 1880, 1150)
    v.shoes(a0, a1, PL + T + 10, 2, step=190)
    v.label(a0, a1, 1300, "ВЕРХНЯЯ ОДЕЖДА")
    v.label(a0, a1, PL + 210, "обувь, 2 полки")
    # 900 №2 — куртки + обувь
    v.shelf(b0, b1, 1950)
    v.rail(b0, b1, 1880, 850)
    z = v.shoes(b0, b1, PL + T + 10, 3, step=190)
    v.shelf(b0, b1, z)
    v.label(b0, b1, 1450, "куртки, сумки")
    v.label(b0, b1, PL + 300, "обувь, 3 полки")
    # 450 — выдвижная штанга BELLE + 2 ящика
    v.shelf(c0, c1, 1950)
    pullout(v, c0, c1, 1950 - 40, 1250)
    z = v.drawers(c0, c1, PL + T, 2)
    v.shelf(c0, c1, z)
    v.label(c0, c1, 2050, "выдв. штанга", 1.1)
    v.label(c0, c1, PL + 200, "2 ящика", 1.2)


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)
    text(297, 18, "ШКАФ В КОРИДОРЕ 900 + 900 + 450, глубина 520 — ВАРИАНТЫ НАПОЛНЕНИЯ", size=3.6, weight="bold")
    notes = {
        "ВАРИАНТ А — универсальный": [
            "900: длинная верхняя одежда (штанга 1880) + 2 полки для обуви внизу",
            "900: куртки и сумки + 3 обувные полки внизу",
            "450: 3 выдвижных ящика под мелочь + полки",
        ],
        "ВАРИАНТ Б — много обуви": [
            "900: вся высота под верхнюю одежду (пальто, пуховики)",
            "900: 2 ящика под мелочь + 8 наклонных обувных полок",
            "450: открытые полки, внизу место под пылесос",
        ],
        "ВАРИАНТ В — две штанги": [
            "900 + 900: штанги на всю ширину 1800",
            "под ними: обувные полки и 2 ящика",
            "450: отсек 1200 под пылесос, выше обувные полки",
        ],
    }
    for k, (fn, (title, rows)) in enumerate(zip((var_a, var_b, var_c), notes.items())):
        ox = 30 + k * 190
        v = V(ox, 212)
        fn(v)
        text(v.X(W / 2), 34, title, size=2.2, weight="bold")
        dim_v(v.Z(H), v.Z(0), v.X(W) + 5, str(H), ext_from=v.X(W), size=1.6)
        for a, b in ((0, PL), (PL, TOP), (TOP, H)):
            dim_v(v.Z(b), v.Z(a), v.X(W) + 11, str(b - a), ext_from=v.X(W), size=1.4)
        for i, s in enumerate(rows):
            text(ox, 225 + i * 7, "• " + s, size=1.5, anchor="start")
    bx, by, bw, bh = 445, 362, 140, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    text(bx + bw / 2, by + 7, "ШКАФ В КОРИДОРЕ", size=3.0, weight="bold")
    text(bx + bw / 2, by + 12, "варианты наполнения, М 1:20", size=1.6)
    text(bx + 3, by + 22, "900 + 900 + 450, глубина 520", size=1.7, anchor="start")
    text(bx + 3, by + 30, "Вид без фасадов", size=1.7, anchor="start")
    text(bx + 3, by + 38, "Размеры в мм", size=1.7, anchor="start")
    e('</svg>')
    open(os.path.join(HERE, "sheet1.svg"), "w", encoding="utf-8").write("\n".join(g.out))


if __name__ == "__main__":
    main()
