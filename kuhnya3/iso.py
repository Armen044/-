#!/usr/bin/env python3
"""Кухня — аксонометрия в стиле презентационного чертежа (линии, лёгкая заливка, выноски, размеры)."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                       # noqa: E402
from generate import e, line, rect                         # noqa: E402
import sheet as k                                          # noqa: E402  – размеры кухни

F = 1.7
_t = g.text


def text(x, y, s, size=2.4, **kw):
    _t(x, y, s, size=size * F, **kw)


g.text = text
WM, WR, H, PL, CB, TOP = k.WM, k.WR, k.H, k.PL, k.CB, k.TOP
UB, UT, UD, AZ = k.UB, k.UT, k.UD, k.AZ
FT = 18
COL = {"body": "#ece8e2", "light": "#f6f4f0", "dark": "#a8988a", "top": "#e3ddd3", "plinth": "#8f877e",
       "black": "#2a2a2a", "steel": "#c9ccd0", "gola": "#3a3a3a", "wall": "#fbfbfa"}
B = []


def box(x0, x1, y0, y1, z0, z1, kind):
    B.append((x0, x1, y0, y1, z0, z1, kind))


def build():
    # нижний ряд основной стены
    box(30, 3400, 40, 540, 0, PL, "plinth")
    box(0, 3400, 0, 580, PL, CB, "body")
    for x0, x1, kind, _ in k.BASE:
        if kind == "drw3":
            z = PL
            for h_ in (260, 260, CB - PL - 520):
                box(x0 + 2, x1 - 2, 580, 600, z + 2, z + h_ - 2, "light")
                z += h_
        else:
            box(x0 + 2, x1 - 2, 580, 600, PL + 2, CB - 40, "light")
            box(x0, x1, 570, 600, CB - 40, CB, "gola")
    box(0, 3400, 0, 610, CB, TOP, "top")
    box(3400, WM, 0, 600, CB, TOP, "top")
    box(660, 1140, 60, 540, TOP, TOP + 5, "black")             # варочная
    box(1900, 2300, 90, 500, TOP, TOP + 3, "steel")            # мойка
    box(2230, 2260, 60, 90, TOP, TOP + 300, "steel")            # смеситель
    box(2140, 2260, 60, 90, TOP + 280, TOP + 300, "steel")
    # верхние шкафы
    x0, x1 = k.RAD[0][0], k.RAD[1][1]
    box(x0, x1, 0, UD - FT, UB, UT, "body")
    for a, b in k.UPPERS + k.RAD:
        box(a + 2, b - 2, UD - FT, UD, UB + 2, UT - 2, "dark")
    # пеналы на правой стене (фасады смотрят в −x)
    XF = 3400
    box(XF + 40, WM, 600, 1830, 0, PL, "plinth")
    box(XF + FT, WM, 0, 600, TOP, H, "body")
    box(XF + FT, WM, 600, 1830, PL, H, "body")
    fr = [(0, 600, TOP, AZ), (600, 1200, PL, 460), (600, 1200, 1440, AZ), (1200, 1800, PL, 1880),
          (1200, 1800, 1880, AZ), (0, 600, AZ, H), (600, 1200, AZ, H), (1200, 1800, AZ, H), (1800, 1830, PL, H)]
    for y0, y1, z0, z1 in fr:
        box(XF, XF + FT, y0 + 2, y1 - 2, z0 + 2, z1 - 2, "dark")
    box(XF, XF + FT, 602, 1198, 460, 1060, "black")            # духовка
    box(XF, XF + FT, 602, 1198, 1060, 1440, "black")           # СВЧ


el = math.radians(26)
C, SI, R2 = math.cos(el), math.sin(el), math.sqrt(2)
OX, OY, SC = 95, 335, 1 / 15


def P(x, y, z):
    return OX + (x + y) / R2 * SC, OY - (z * C + (x - y) / R2 * SI) * SC


def poly(pts, fill, sw=0.25, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{a:.2f},{b:.2f}" for a, b in pts)
    e(f'<polygon points="{p}" fill="{fill}" stroke="#2b2b2b" stroke-width="{sw}" stroke-linejoin="round"{d}/>')


def mix(c, f):
    r, g_, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    m = lambda v: max(0, min(255, int(v * f)))   # noqa: E731
    return f"#{m(r):02x}{m(g_):02x}{m(b):02x}"


def draw():
    # художник: сначала дальние (дальше от зрителя по −x, +y, сверху)
    def depth(b):
        return max(b[0], b[1]) * 1.0 - min(b[2], b[3]) * 1.0 - min(b[4], b[5]) * 0.05
    order = sorted(range(len(B)), key=lambda i: -depth(B[i]))
    # стены
    poly([P(0, 0, 0), P(WM, 0, 0), P(WM, 0, H), P(0, 0, H)], COL["wall"], sw=0.2)
    poly([P(WM, 0, 0), P(WM, WR, 0), P(WM, WR, H), P(WM, 0, H)], mix(COL["wall"], 0.97), sw=0.2)
    poly([P(400, 0, TOP), P(3400, 0, TOP), P(3400, 0, UB), P(400, 0, UB)], "#f1efeb", sw=0.12)
    for i in order:
        x0, x1, y0, y1, z0, z1, kd = B[i]
        f = COL[kd]
        poly([P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)], f)
        poly([P(x0, y0, z0), P(x0, y1, z0), P(x0, y1, z1), P(x0, y0, z1)], mix(f, 0.86))
        poly([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)], mix(f, 1.04) if kd != "black" else f)
    # открывание на фасадах (пунктир)
    for a, b in k.UPPERS:
        p1, p2, p3 = P(a + 20, UD, UT - 20), P(b - 20, UD, (UB + UT) / 2), P(a + 20, UD, UB + 20)
        e(f'<polyline points="{p1[0]:.2f},{p1[1]:.2f} {p2[0]:.2f},{p2[1]:.2f} {p3[0]:.2f},{p3[1]:.2f}" '
          f'fill="none" stroke="#666" stroke-width="0.15" stroke-dasharray="1 0.7"/>')


def dim3(a, b, off, label, size=1.8):
    (x1, y1), (x2, y2) = P(*a), P(*b)
    ox, oy = off
    xa, ya, xb, yb = x1 + ox, y1 + oy, x2 + ox, y2 + oy
    line(x1, y1, xa, ya, w=0.12, color="#555")
    line(x2, y2, xb, yb, w=0.12, color="#555")
    line(xa, ya, xb, yb, w=0.2, color="#333")
    for px, py in ((xa, ya), (xb, yb)):
        line(px - 0.8, py + 0.8, px + 0.8, py - 0.8, w=0.3, color="#333")
    ang = math.degrees(math.atan2(yb - ya, xb - xa))
    if ang > 90:
        ang -= 180
    if ang < -90:
        ang += 180
    mx, my = (xa + xb) / 2, (ya + yb) / 2
    e(f'<text x="{mx:.2f}" y="{my - 1:.2f}" font-size="{size * F}" text-anchor="middle" fill="#222" '
      f'transform="rotate({ang:.1f} {mx:.2f} {my:.2f})">{label}</text>')


def callout(pt, tx, ty, label, anchor):
    x, y = P(*pt)
    e(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.6" fill="#222"/>')
    line(x, y, x, ty, w=0.15, color="#444")
    line(x, ty, tx, ty, w=0.15, color="#444")
    for i, s in enumerate(label.split("\n")):
        text(tx + (1 if anchor == "start" else -1), ty - 1.5 + i * 5.2, s, size=1.7, anchor=anchor, fill="#333")


def main():
    build()
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    draw()
    # размеры
    dim3((0, 620, 0), (3400, 620, 0), (-3, 9), "3400")
    dim3((0, 620, 0), (WM, 620, 0), (-6, 18), str(WM), size=2.0)
    dim3((3400, 1830, 0), (WM, 1830, 0), (4, 6), "600")
    dim3((3400, 0, 0), (3400, 1830, 0), (0, 0), "")
    dim3((WM, 1830, 0), (WM, 0, 0), (12, 0), "")
    xs = [(WM, WR, 0), (WM, WR, PL), (WM, WR, TOP), (WM, WR, AZ), (WM, WR, H)]
    for a, b in zip(xs, xs[1:]):
        dim3(a, b, (10, 0), str(b[2] - a[2]), size=1.6)
    dim3(xs[0], xs[-1], (20, 0), str(H), size=2.0)
    dim3((3400, 1830, 0), (3400, 0, 0), (-4, 18), str(WR), size=2.0)
    dim3((k.RAD[0][0], 0, UT), (k.RAD[1][1], 0, UT), (0, -8), f"{k.RAD[1][1] - k.RAD[0][0]}", size=1.8)
    dim3((0, 600, UB), (0, 600, UT), (-6, 0), str(UT - UB), size=1.6)
    dim3((0, 600, TOP), (0, 600, UB), (-6, 0), str(UB - TOP), size=1.6)
    dim3((0, 600, 0), (0, 600, TOP), (-6, 0), str(TOP), size=1.6)
    # выноски
    callout((1500, UD, 2100), 40, 70, "Верхние шкафы, глубина 340,\nторцы радиусные R300", "start")
    callout((300, 600, 600), 40, 395, "Нижние фасады — светлые", "start")
    callout((1500, 600, CB - 20), 150, 405, "Профиль Gola", "start")
    callout((1600, 300, TOP), 260, 405, "Столешница 40, верх 920", "start")
    callout((3400, 300, 1900), 560, 60, "Ниша под бойлер\nна столешнице", "end")
    callout((3400, 900, 700), 560, 395, "Пенал: ящик 360,\nдуховка, СВЧ", "end")
    callout((3400, 1500, 1200), 560, 175, "Пенал холодильника", "end")
    callout((3400, 900, 2550), 560, 115, "Антресоль 400", "end")
    text(297, 22, "КУХНЯ — ОБЩИЙ ВИД", size=3.6, weight="bold")
    text(297, 29, f"{WM} × {WR} × {H} мм · цоколь 100 · верх столешницы 920", size=1.9, fill="#555")
    e('</svg>')
    open(os.path.join(HERE, "iso.svg"), "w", encoding="utf-8").write("\n".join(g.out))


if __name__ == "__main__":
    main()
