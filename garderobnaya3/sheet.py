#!/usr/bin/env python3
"""Чертёж гардеробной с островом: лист А2, масштаб 1:30 (узел острова 1:20)."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                       # noqa: E402  – общие функции рисования
from generate import e, text, line, rect, dim_h, dim_v, leader, LED   # noqa: E402
from geom import *                          # noqa: E402,F403

S = 1 / 30
WOOD = "#d9c3ae"       # кромка ЛДСП «орех» на чертеже
FRONT = "#b48f73"
FY = 152               # линия пола развёрток


class V:
    """Развёртка: u – по горизонтали (мм), z – высота."""

    def __init__(self, ox, length):
        self.ox, self.w = ox, length

    def X(self, u):
        return self.ox + u * S

    def Z(self, z):
        return FY - z * S

    def pv(self, u, z0=PL, z1=H):
        rect(self.X(u), self.Z(z1), T * S, (z1 - z0) * S, fill=WOOD, sw=0.15)

    def ph(self, u0, u1, z):
        rect(self.X(u0), self.Z(z + T), (u1 - u0) * S, T * S, fill=WOOD, sw=0.15)

    def rail(self, u0, u1, z, label=True):
        y = self.Z(z)
        line(self.X(u0) + 0.3, y, self.X(u1) - 0.3, y, w=0.55, color="#222")
        if label:
            text(self.X(u0) + 1.2, y - 0.8, f"штанга Н={z}", size=1.5, anchor="start", fill="#444")

    def hangers(self, u0, u1, z, length):
        n = max(2, int((u1 - u0) / 140))
        step = (u1 - u0) / (n + 1)
        for i in range(1, n + 1):
            cx = self.X(u0 + step * i)
            hw = min(150, step * 0.85) * S
            y = self.Z(z)
            e(f'<path d="M{cx:.2f},{y:.2f} l{-hw / 2:.2f},1.3 l{hw:.2f},0 z" fill="none" stroke="#999" stroke-width="0.12"/>')
            rect(cx - hw / 2, y + 1.3, hw, length * S - 1.3, fill="#efebe6", stroke="#bdb4aa", sw=0.1)

    def drawers(self, u0, u1):
        for i in range(DR_N):
            zb = PL + T + i * DR_H
            rect(self.X(u0) + 0.12, self.Z(zb + DR_H) + 0.12, (u1 - u0) * S - 0.24, DR_H * S - 0.24,
                 fill=FRONT, stroke="#3a2a20", sw=0.18)
            cx = (self.X(u0) + self.X(u1)) / 2
            line(cx - 7, self.Z(zb + DR_H - 35), cx + 7, self.Z(zb + DR_H - 35), w=0.45, color="#111")
        self.ph(u0, u1, DR_TOP)

    def tray(self, u0, u1, z=TRAY_Z, label="лоток"):
        rect(self.X(u0) + 0.2, self.Z(z + 55), (u1 - u0) * S - 0.4, 55 * S, fill="#8a6650", stroke="#3a2a20", sw=0.18)
        text((self.X(u0) + self.X(u1)) / 2, self.Z(z + 55) - 0.7, label, size=1.4, fill="#5a3e2c")

    def shoes(self, u0, u1, z):
        n = max(1, int((u1 - u0) / 220))
        sw = (u1 - u0 - 60) / n
        for k in range(n):
            sx = u0 + 30 + k * sw
            e(f'<path d="M{self.X(sx + 15):.2f},{self.Z(z):.2f} L{self.X(sx + 15):.2f},{self.Z(z + 100):.2f} '
              f'L{self.X(sx + sw * 0.45):.2f},{self.Z(z + 65):.2f} L{self.X(sx + sw - 15):.2f},{self.Z(z + 30):.2f} '
              f'L{self.X(sx + sw - 15):.2f},{self.Z(z):.2f} z" fill="#e6ddd3" stroke="#8b7f73" stroke-width="0.12"/>')

    def stack(self, u0, u1, z):
        a, b = u0 + (u1 - u0) * 0.25, u1 - (u1 - u0) * 0.25
        rect(self.X(a), self.Z(z + T + 140), (b - a) * S, 140 * S, fill="#efe9e1", stroke="#bbb", sw=0.1)

    def boxes(self, u0, u1, z):
        a = (u0 + u1) / 2 - 170
        rect(self.X(a), self.Z(z + T + 220), 340 * S, 220 * S, fill="#2a2a2a", stroke="none")

    def base(self):
        rect(self.X(0), self.Z(PL), self.w * S, PL * S, fill="url(#hatch)", sw=0.15)
        rect(self.X(0), self.Z(H), self.w * S, H * S, sw=0.45)
        line(self.X(0) - 4, self.Z(0), self.X(self.w) + 4, self.Z(0), w=0.5)

    def led(self, u0, u1, z=A1 - 9):
        line(self.X(u0) + 0.3, self.Z(z), self.X(u1) - 0.3, self.Z(z), w=0.6, color=LED, dash="1.4 0.7")

    def mark(self, u, s):
        cx, cy = self.X(u), self.Z(H - 150)
        e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.2" fill="#fff" stroke="#111" stroke-width="0.25"/>')
        text(cx, cy + 0.8, s, size=2.0, weight="bold")


def side_elevation(ox, left):
    """Боковая стена из прохода. Левая: слева вход, справа угол; правая – наоборот."""
    v = V(ox, D)
    U = (lambda y: D - y) if left else (lambda y: y)
    span = lambda ya, yb: tuple(sorted((U(ya), U(yb))))     # noqa: E731
    v.base()
    for z in (PL, A1, A2, H - T):
        v.ph(0, D, z)
    for y in PANELS_Y:
        a, b = span(y, y + T)
        v.pv(a)
    v.led(*span(BD, D - T))
    # колонны S, A, C, B
    a, b = span(*COL_S)
    for z in S_SHELVES:
        v.ph(a, b, z)
        v.shoes(a, b, z + T)
    v.shoes(a, b, PL + T)
    v.mark((a + b) / 2, ("Л" if left else "П") + "4")
    a, b = span(*COL_A)
    v.drawers(a, b)
    v.tray(a, b, label="лоток для украшений")
    for z in A_SHELVES:
        v.ph(a, b, z)
        v.stack(a, b, z)
    v.mark((a + b) / 2, ("Л" if left else "П") + "3")
    for k, col in enumerate((COL_C, COL_B)):
        a, b = span(*col)
        v.rail(a, b, RAIL)
        v.hangers(a, b, RAIL, 1000)
        v.tray(a, b, label="лоток ремни/галстуки")
        v.ph(a, b, SHOE)
        v.shoes(a, b, SHOE + T)
        v.mark((a + b) / 2, ("Л" if left else "П") + "2")
    # угол: продолжение задней секции (за плоскостью – угловая зона 600)
    a, b = span(300, CORNER[1])
    cz = span(0, BD)
    line(v.X(cz[0] if left else cz[1]), v.Z(H - T), v.X(cz[0] if left else cz[1]), v.Z(PL), w=0.3,
         color="#c0392b", dash="2 1")
    v.rail(a, b, RAIL)
    ca, cb = span(BD, CORNER[1])
    if left:
        v.hangers(ca, cb, RAIL, 1550)
        v.ph(*span(0, CORNER[1]), SHOE)
    else:
        v.hangers(ca, cb, RAIL, 950)
        v.ph(*span(0, CORNER[1]), MID)
        v.rail(a, b, RAIL_LOW)
        v.hangers(ca, cb, RAIL_LOW, 900)
    v.mark((ca + cb) / 2, "Л1" if left else "П1")
    for u0 in (0,):
        pass
    for z in (A1,):
        for col in (COL_S, COL_A, COL_C, COL_B):
            if (col[0] // 300) % 2 == 0:
                v.boxes(*span(*col), z)
    # размеры по длине
    segs = [0, BD, CORNER[1], COL_B[1], COL_C[1], COL_A[1], D]
    us = sorted(U(y) for y in segs)
    y1 = FY + 5
    for p, q in zip(us, us[1:]):
        dim_h(v.X(p), v.X(q), y1, str(round(q - p)), ext_from=FY + 0.6, size=2.0)
    dim_h(v.X(0), v.X(D), y1 + 6, str(D), size=2.2)
    text(v.X(0 if left else D) + (2 if left else -2), FY + 15.5, "← вход" if left else "вход →",
         size=1.7, anchor="start" if left else "end", fill="#666")
    text(v.X(D if left else 0) + (-2 if left else 2), FY + 15.5, "задняя стена →" if left else "← задняя стена",
         size=1.7, anchor="end" if left else "start", fill="#666")
    return v


def back_elevation(ox):
    v = V(ox, W)
    v.base()
    for z in (PL, A1, A2, H - T):
        v.ph(0, W, z)
    for x in (0, XL - T / 2, XR - T / 2, W - T):
        v.pv(x)
    v.led(T, W - T)
    for z in COL_SHELVES:
        v.ph(XL + T / 2, XR - T / 2, z)
        v.stack(XL + T / 2, XR - T / 2, z)
    v.rail(T, XL - T / 2, RAIL)
    v.hangers(SD, XL - T / 2, RAIL, 1550)
    v.ph(T, XL - T / 2, SHOE)
    v.shoes(SD, XL - T / 2, SHOE + T)
    v.rail(XR + T / 2, W - T, RAIL)
    v.hangers(XR + T / 2, W - SD, RAIL, 950)
    v.ph(XR + T / 2, W - T, MID)
    v.rail(XR + T / 2, W - T, RAIL_LOW, label=False)
    text(v.X(XR + T / 2) + 1.2, v.Z(RAIL_LOW) - 0.8, f"штанга Н={RAIL_LOW}", size=1.5, anchor="start", fill="#444")
    v.hangers(XR + T / 2, W - SD, RAIL_LOW, 900)
    for x in (XL + 150, XR + 300):
        v.boxes(x, x + 340, A1)
    for x in (SD, W - SD):
        line(v.X(x), v.Z(H - T), v.X(x), v.Z(PL), w=0.3, color="#c0392b", dash="2 1")
    for u, s in ((XL / 2 + 250, "З1"), ((XL + XR) / 2, "З2"), ((XR + W) / 2 - 250, "З3")):
        v.mark(u, s)
    y1 = FY + 5
    for p, q in ((0, SD), (SD, XL), (XL, XR), (XR, W - SD), (W - SD, W)):
        dim_h(v.X(p), v.X(q), y1, str(q - p), ext_from=FY + 0.6, size=2.0)
    dim_h(v.X(0), v.X(W), y1 + 6, str(W), size=2.2)
    text(v.X(SD / 2), v.Z(H) + 4, "угол", size=1.6, fill="#c0392b")
    text(v.X(W - SD / 2), v.Z(H) + 4, "угол", size=1.6, fill="#c0392b")
    return v


def heights(v, x, right=False):
    zs = [0, PL, DR_TOP, RAIL_LOW, MID, RAIL, A1, A2, H]
    k = 1 if right else -1
    edge = v.X(v.w) if right else v.X(0)
    for a, b in zip(zs, zs[1:]):
        dim_v(v.Z(b), v.Z(a), x, str(b - a), ext_from=edge, size=1.7)
    dim_v(v.Z(H), v.Z(0), x + k * 6, str(H), ext_from=edge, size=2.2)


def elevations():
    vl = side_elevation(42, True)
    vb = back_elevation(230)
    vr = side_elevation(378, False)
    for v, t, s in ((vl, "ЛЕВАЯ СТЕНА", "развёртка, вид из прохода"), (vb, "ЗАДНЯЯ СТЕНА", "вид от входа"),
                    (vr, "ПРАВАЯ СТЕНА", "развёртка, вид из прохода")):
        cx = v.X(v.w / 2)
        text(cx, 30, t, size=3.6, weight="bold")
        text(cx, 34.5, s, size=2.0)
    heights(vl, vl.X(0) - 5)
    heights(vr, vr.X(D) + 5, right=True)
    # высоты на задней стене (полки центральной колонны)
    zs = [PL + T] + [z for z in COL_SHELVES] + [A1]
    xm = vb.X(XR) + 2.2
    for a, b in zip(zs, zs[1:]):
        dim_v(vb.Z(b), vb.Z(a), xm, str(b - a), size=1.4)
    # отметки
    for v in (vl,):
        for z, s in ((TRAY_Z, f"лотки Н={TRAY_Z}"),):
            pass
    leader(vb.X(XR + 750), vb.Z(A1 - 9), vb.X(XR + 600), vb.Z(2850),
           "LED под антресолью", size=1.6)


def plan():
    ox, oy = 48, 205
    WT = 100

    def P(x, y):
        return ox + x * S, oy + y * S

    text(ox + W * S / 2, oy - WT * S - 17, "ПЛАН (вид сверху)", size=3.6, weight="bold")
    # стены
    rect(ox - WT * S, oy - WT * S, (W + 2 * WT) * S, WT * S, fill="url(#wall)", sw=0.3)
    rect(ox - WT * S, oy, WT * S, D * S, fill="url(#wall)", sw=0.3)
    rect(ox + W * S, oy, WT * S, D * S, fill="url(#wall)", sw=0.3)

    def bx(x0, y0, x1, y1, fill="#f1e8de", sw=0.3, dash=None):
        a, b = P(x0, y0)
        rect(a, b, (x1 - x0) * S, (y1 - y0) * S, fill=fill, sw=sw, dash=dash)

    bx(0, 0, W, BD)
    bx(0, BD, SD, D)
    bx(W - SD, BD, W, D)
    for x in (XL, XR):
        line(*P(x, 0), *P(x, BD), w=0.35)
    for xa, xb in ((0, SD), (W - SD, W)):
        for y in PANELS_Y[:-1]:
            line(*P(xa, y + T / 2), *P(xb, y + T / 2), w=0.35)
        bx(xa, COL_A[0], xb, COL_A[1], fill="url(#drw)", sw=0.25)
    for x in (SD, W - SD):
        line(*P(x, 0), *P(x, BD), w=0.2, color="#c0392b", dash="1.5 1")
    # штанги
    for a, b in ((P(300, 300), P(XL, 300)), (P(XR, 300), P(W - 300, 300)),
                 (P(SD / 2, 300), P(SD / 2, CORNER[1])), (P(W - SD / 2, 300), P(W - SD / 2, CORNER[1])),
                 (P(SD / 2, COL_B[0]), P(SD / 2, COL_C[1])), (P(W - SD / 2, COL_B[0]), P(W - SD / 2, COL_C[1]))):
        line(*a, *b, w=0.45, color="#444", dash="2 0.8")
    # остров (скруглён к задней стене) и пуф
    x0, x1 = ISL_X
    y0, y1 = ISL_Y
    r = ISL_W / 2
    a0, b0 = P(x0, y0 + r)
    a1, b1 = P(x1, y1)
    rr = r * S
    e(f'<path d="M{a0:.2f},{b1:.2f} L{a0:.2f},{b0:.2f} A{rr:.2f},{rr:.2f} 0 0 1 {a1:.2f},{b0:.2f} '
      f'L{a1:.2f},{b1:.2f} z" fill="#e8dccf" stroke="#111" stroke-width="0.35"/>')
    e(f'<path d="M{a0 + 1:.2f},{b1 - 1:.2f} L{a0 + 1:.2f},{b0:.2f} A{rr - 1:.2f},{rr - 1:.2f} 0 0 1 {a1 - 1:.2f},{b0:.2f} '
      f'L{a1 - 1:.2f},{b1 - 1:.2f} z" fill="#dfeaec" stroke="#5b7a80" stroke-width="0.2" stroke-dasharray="0.8 0.5"/>')
    cx, cy = P((x0 + x1) / 2, y1 + 10)
    pr = POUF_R * S
    e(f'<path d="M{cx - pr:.2f},{cy:.2f} A{pr:.2f},{pr:.2f} 0 0 0 {cx + pr:.2f},{cy:.2f} z" '
      f'fill="#efe4d0" stroke="#111" stroke-width="0.35"/>')
    text(cx, b0 + 6, "ОСТРОВ", size=2.0, weight="bold")
    text(cx, b0 + 9, "витрина (стекло)", size=1.6, fill="#5b7a80")
    text(cx, cy + 4.5, "пуф", size=1.8)
    # ковёр
    bx(SD + 150, BD + 200, W - SD - 150, D - 300, fill="none", sw=0.15, dash="1 1")
    # стеклянная перегородка
    a, b = P(0, D)
    rect(a, b, W * S, 20 * S, fill="#cfe0e6", stroke="#111", sw=0.3)
    for xa, xb in ((800, 1600), (1600, 2400)):
        a, b = P(xa, D + 24)
        rect(a, b, (xb - xa) * S, 20 * S, fill="#e6f0f3", stroke="#111", sw=0.25)
    for xs, dx in ((1200, -1), (2000, 1)):
        a, b = P(xs, D + 120)
        line(a, b, a + dx * 10, b, w=0.3, color="#33373b")
        e(f'<path d="M{a + dx * 10:.2f},{b:.2f} l{-dx * 1.6:.2f},-0.7 l0,1.4 z" fill="#33373b"/>')
    text(*P(W / 2, D + 330), "ВХОД — стеклянная перегородка, 2 раздвижные двери", size=1.9, weight="bold")
    # подписи секций
    for x, y, s in ((XL / 2 + 250, 300, "З1"), ((XL + XR) / 2, 300, "З2"), ((XR + W) / 2 - 250, 300, "З3"),
                    (SD / 2 + 120, (BD + CORNER[1]) / 2, "Л1"), (SD / 2, sum(COL_B) / 2, "Л2"),
                    (SD / 2, sum(COL_C) / 2, "Л2"), (SD / 2, sum(COL_A) / 2, "Л3"), (SD / 2, sum(COL_S) / 2, "Л4"),
                    (W - SD / 2 - 120, (BD + CORNER[1]) / 2, "П1"), (W - SD / 2, sum(COL_B) / 2, "П2"),
                    (W - SD / 2, sum(COL_C) / 2, "П2"), (W - SD / 2, sum(COL_A) / 2, "П3"),
                    (W - SD / 2, sum(COL_S) / 2, "П4")):
        c1, c2 = P(x, y)
        e(f'<circle cx="{c1:.2f}" cy="{c2:.2f}" r="2.0" fill="#fff" stroke="#111" stroke-width="0.25"/>')
        text(c1, c2 + 0.7, s, size=1.8, weight="bold")
    # размеры
    top = oy - WT * S
    for p, q in ((0, SD), (SD, XL), (XL, XR), (XR, W - SD), (W - SD, W)):
        dim_h(P(p, 0)[0], P(q, 0)[0], top - 3.5, str(q - p), ext_from=top, size=1.8)
    dim_h(P(0, 0)[0], P(W, 0)[0], top - 9, str(W), ext_from=top)
    xl = ox - WT * S
    ys = [0, BD, CORNER[1], COL_B[1], COL_C[1], COL_A[1], D]
    for p, q in zip(ys, ys[1:]):
        dim_v(oy + p * S, oy + q * S, xl - 4, str(q - p), ext_from=xl, size=1.8)
    dim_v(oy, oy + D * S, xl - 10, str(D), ext_from=xl)
    xr = ox + (W + WT) * S
    for p, q in ((BD, y0), (y0, y1), (y1, y1 + 10 + POUF_R), (y1 + 10 + POUF_R, D)):
        dim_v(oy + p * S, oy + q * S, xr + 4, str(round(q - p)), ext_from=xr, size=1.8)
    ym = oy + (y1 - 150) * S
    dim_h(P(SD, 0)[0], P(x0, 0)[0], ym, str(round(x0 - SD)), size=1.7)
    dim_h(P(x0, 0)[0], P(x1, 0)[0], ym, str(ISL_W), size=1.7)
    dim_h(P(x1, 0)[0], P(W - SD, 0)[0], ym, str(round(W - SD - x1)), size=1.7)
    dim_h(P(0, 0)[0], P(SD, 0)[0], oy + (D - 200) * S, str(SD), size=1.7)
    dim_h(P(W - SD, 0)[0], P(W, 0)[0], oy + (D - 200) * S, str(SD), size=1.7)


def island_detail():
    s = 1 / 20
    ox, fy = 185, 262
    text(ox + 52, 197, "ОСТРОВ С ВИТРИНОЙ И ПУФ", size=3.2, weight="bold")
    text(ox + 52, 201.5, "вид сбоку и с торца, М 1:20", size=2.0)
    x0, x1 = ISL_X
    y0, y1 = ISL_Y
    # вид сбоку: u = y – y0
    U = lambda y: ox + (y - y0) * s         # noqa: E731
    Z = lambda z: fy - z * s                # noqa: E731
    line(ox - 3, fy, U(y1 + 400) + 3, fy, w=0.45)
    rect(U(y0), Z(ISL_H), (y1 - y0) * s, (ISL_H - PL) * s, fill="#e8dccf", sw=0.35)
    rect(U(y0 + 40), Z(PL), (y1 - y0 - 80) * s, PL * s, fill="url(#hatch)", sw=0.2)
    rect(U(y0), Z(ISL_H), (y1 - y0) * s, 40 * s, fill=WOOD, sw=0.25)
    rect(U(y0 + 30), Z(ISL_H) + 0.1, (y1 - y0 - 60) * s, 40 * s - 0.2, fill="#dfeaec", stroke="#5b7a80", sw=0.15)
    for i in range(2):
        zb = PL + 20 + i * 370
        rect(U(y0 + ISL_W / 2 + 20), Z(zb + 350), (y1 - y0 - ISL_W / 2 - 40) * s, 350 * s, fill=FRONT, sw=0.25)
        c = (U(y0 + ISL_W / 2 + 20) + U(y1 - 20)) / 2
        line(c - 9, Z(zb + 305), c + 9, Z(zb + 305), w=0.45)
    rect(U(y1 + 10), Z(POUF_H), POUF_R * s, (POUF_H - 70) * s + 70 * s, fill="#efe4d0", sw=0.35)
    rect(U(y1 + 10), Z(POUF_H - 70), POUF_R * s, (POUF_H - 70) * s, fill=FRONT, sw=0.25)
    rect(U(y1 - 20), Z(720), 6 * s, 80 * s, fill="#333", stroke="none")
    dim_h(U(y0), U(y1), fy + 5, str(y1 - y0), ext_from=fy + 0.5, size=1.8)
    dim_h(U(y1), U(y1 + 10 + POUF_R), fy + 5, str(10 + POUF_R), ext_from=fy + 0.5, size=1.8)
    dim_v(Z(ISL_H), Z(0), U(y0) - 4, str(ISL_H), ext_from=U(y0), size=1.8)
    dim_v(Z(POUF_H), Z(0), U(y1 + 10 + POUF_R) + 4, str(POUF_H), ext_from=U(y1 + 10 + POUF_R), size=1.8)
    dim_v(Z(ISL_H), Z(ISL_H - 40), U(y0) - 9, "40", size=1.5)
    leader(U(y0 + 500), Z(ISL_H - 10), U(y0 + 300), Z(ISL_H) - 6, "стекло 6 мм, внутри ложементы", size=1.6)
    leader(U(y1 - 17), Z(680), U(y1 + 120), Z(1100), "розетки", size=1.6)
    text(U(y0 + ISL_W / 4), Z(500), "R350", size=1.6, rot=-90, fill="#666")
    # вид с торца (со стороны пуфа)
    ex = U(y1 + 400) + 22
    X = lambda x: ex + (x - x0) * s         # noqa: E731
    line(X(x0) - 3, fy, X(x1) + 3, fy, w=0.45)
    rect(X(x0), Z(ISL_H), ISL_W * s, (ISL_H - PL) * s, fill="#e8dccf", sw=0.35)
    rect(X(x0 + 40), Z(PL), (ISL_W - 80) * s, PL * s, fill="url(#hatch)", sw=0.2)
    rect(X(x0), Z(ISL_H), ISL_W * s, 40 * s, fill=WOOD, sw=0.25)
    rect(X(x0), Z(POUF_H), ISL_W * s, 70 * s, fill="#efe4d0", sw=0.3)
    rect(X(x0), Z(POUF_H - 70), ISL_W * s, (POUF_H - 70) * s, fill=FRONT, sw=0.3)
    dim_h(X(x0), X(x1), fy + 5, str(ISL_W), ext_from=fy + 0.5, size=1.8)
    text((X(x0) + X(x1)) / 2, Z(ISL_H) - 3, "торец с пуфом", size=1.7, fill="#555")


def notes():
    x, y = 395, 182
    text(x, y, "СЕКЦИИ", size=3.0, weight="bold", anchor="start")
    rows = [
        ("З1", f"{XL} (угол)", "Длинная одежда, штанга Н=2230, полка для обуви Н=380 (Г-обр. с Л1)"),
        ("З2", str(XR - XL), "Колонна открытых полок (7 полок + антресоль)"),
        ("З3", f"{W - XR} (угол)", "2 яруса штанг Н=2230 / 1080, полка Н=1150 (Г-обр. с П1)"),
        ("Л1/П1", "700", "Продолжение угловой зоны: штанги Г-образно"),
        ("Л2/П2", "2 × 900", "Штанга Н=2230 + выдвижной лоток для ремней/галстуков Н=950 + полка обуви"),
        ("Л3/П3", "800", "4 выкатных ящика по 200 + лоток для украшений + 3 полки"),
        ("Л4/П4", "700", "Полки для обуви (8 ярусов) у входа"),
        ("Остров", "700×1100", "Витрина под стеклом, 4 ящика по бокам, розетки, полукруглый пуф R350"),
        ("—", str(W), "Антресоль: 2 полки Н=2300 / 2680 по всему периметру, LED под нижней"),
    ]
    for i, (a, w, s) in enumerate(rows):
        yy = y + 5.5 + i * 4.3
        text(x, yy, a, size=2.0, anchor="start", weight="bold")
        text(x + 15, yy, w, size=2.0, anchor="start")
        text(x + 33, yy, s, size=2.0, anchor="start")
    y = 228
    text(x, y, "ФУРНИТУРА", size=3.0, weight="bold", anchor="start")
    items = [
        "Направляющие полного выдвижения с доводчиком 500 мм — 12 комплектов (8 ящиков + 4 в острове)",
        "Выдвижные лотки (ремни/галстуки) — 4 шт., лоток для украшений с ложементами — 2 шт.",
        "Штанги овальные чёрные: 2230 — 6 линий (в т.ч. Г-образные углы), 1080 — 2 линии; держатели",
        "Ручки-скобы чёрные 450 мм — 8 шт. (ящики), 360 мм — 4 шт. (остров)",
        "Стеклянная перегородка: профиль чёрный, 2 глухих полотна + 2 раздвижные двери",
        "Стекло витрины острова 6 мм, LED-лента 24 В в профиле под антресолью",
    ]
    for i, s in enumerate(items):
        text(x, y + 5.5 + i * 4.3, s, size=1.95, anchor="start")
    y = 262
    text(x, y, "ИСХОДНЫЕ ДАННЫЕ", size=3.0, weight="bold", anchor="start")
    info = [
        f"Комната: ширина {W} × глубина {D} × высота {H} мм, цоколь {PL} мм",
        f"Глубина: задний ряд {BD} мм, боковые ряды {SD} мм; проход 2100 мм",
        "Материал: ЛДСП 16 мм «орех», кромка ПВХ; фасады ящиков — в цвет корпуса",
        "Компоновка — по видео дизайн-проекта; размеры уточнить после замера",
    ]
    for i, s in enumerate(info):
        text(x, y + 5.5 + i * 4.3, s, size=1.95, anchor="start")
    # штамп
    bx, by, bw, bh = 405, 362, 180, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    line(bx, by + 30, bx + bw, by + 30, w=0.3)
    line(bx + 120, by + 14, bx + 120, by + bh, w=0.3)
    text(bx + bw / 2, by + 6.5, "ГАРДЕРОБНАЯ С ОСТРОВОМ", size=4.0, weight="bold")
    text(bx + bw / 2, by + 11.5, "Общий вид: план, развёртки стен, остров", size=2.4)
    text(bx + 3, by + 20, f"Габариты: {W} × {D} × {H} мм", size=2.5, anchor="start")
    text(bx + 3, by + 26, f"Цоколь {PL} мм, ЛДСП 16 мм «орех»", size=2.5, anchor="start")
    text(bx + 3, by + 36, "Все размеры в миллиметрах", size=2.5, anchor="start")
    text(bx + 3, by + 42, "Стеклянная перегородка на входе", size=2.5, anchor="start")
    text(bx + 150, by + 20.5, "Масштаб", size=2.3)
    text(bx + 150, by + 26.5, "1:30", size=3.6, weight="bold")
    text(bx + 150, by + 36.5, "Лист", size=2.3)
    text(bx + 150, by + 42.5, "1 (А2)", size=3.2, weight="bold")


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)
    elevations()
    plan()
    island_detail()
    notes()
    e('</svg>')
    with open(os.path.join(HERE, "garderobnaya3.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


if __name__ == "__main__":
    main()
