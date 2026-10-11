#!/usr/bin/env python3
"""Листы: 1 — схема зонирования (А3, 1:100), 2 — план рассадки декоративной зоны (А3, 1:50).
Вариант: костровая зона справа, дорожка к огороду проходит мимо неё."""
import math
import os
import random

from shapely.geometry import Point
import geom as G
import plants as PL

HERE = os.path.dirname(os.path.abspath(__file__))
SERIF = "Liberation Serif, DejaVu Serif, serif"
SANS = "DejaVu Sans, Liberation Sans, sans-serif"
INK = "#2b3326"
ZC = {"A": "#5f8f3e", "B": "#c49a6c", "C": "#4f8a5b", "D": "#3f7a4e", "E": "#b9a98f",
      "K": "#9a9389", "F": "#b8873f", "G": "#b8a07a", "H": "#8e2f45", "I": "#6a8f4a"}


class Sheet:
    def __init__(self, w, h):
        self.w, self.h, self.o, self.defs = w, h, [], []

    def e(self, s):
        self.o.append(s)

    def text(self, x, y, s, size=3, anchor="start", weight="normal", fill=INK, font=SANS, extra=""):
        self.e(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{font}" font-size="{size}" '
               f'text-anchor="{anchor}" font-weight="{weight}" fill="{fill}" {extra}>{s}</text>')

    def save(self, name):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" '
               f'viewBox="0 0 {self.w} {self.h}"><defs>{"".join(self.defs)}</defs>'
               f'<rect width="{self.w}" height="{self.h}" fill="#fbfaf6"/>{"".join(self.o)}</svg>')
        with open(os.path.join(HERE, name), "w") as f:
            f.write(svg)


def defs(sh):
    sh.defs.append("""
<pattern id="lawn" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="3" fill="#7fae4f"/>
 <rect width="1.5" height="3" fill="#86b556"/><circle cx="0.7" cy="0.8" r="0.18" fill="#6f9e44"/><circle cx="2.2" cy="2.1" r="0.15" fill="#93c063"/></pattern>
<pattern id="gravel" width="2" height="2" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#e3d6bf"/>
 <circle cx="0.4" cy="0.5" r="0.22" fill="#cdbd9f"/><circle cx="1.4" cy="1.3" r="0.2" fill="#d4c6ab"/><circle cx="1.5" cy="0.3" r="0.12" fill="#bfae90"/><circle cx="0.6" cy="1.6" r="0.13" fill="#f0e6d4"/></pattern>
<pattern id="mulch" width="2.4" height="2.4" patternUnits="userSpaceOnUse"><rect width="2.4" height="2.4" fill="#6b5a45"/>
 <circle cx="0.6" cy="0.6" r="0.35" fill="#5c4c3a"/><circle cx="1.8" cy="1.7" r="0.3" fill="#7a6750"/></pattern>
<pattern id="tiles" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#e6ddcf" stroke="#cfc3b0" stroke-width="0.2"/></pattern>
<pattern id="roof" width="2" height="2" patternUnits="userSpaceOnUse" patternTransform="rotate(90)"><rect width="2" height="2" fill="#b9b7b2"/><rect width="1" height="2" fill="#a9a7a2"/></pattern>
<pattern id="brick" width="4" height="2.4" patternUnits="userSpaceOnUse"><rect width="4" height="2.4" fill="#c27a5c"/>
 <path d="M0 1.2H4M0 0V1.2M2 1.2V2.4" stroke="#d9a58c" stroke-width="0.2"/></pattern>
<pattern id="wood" width="3" height="1" patternUnits="userSpaceOnUse"><rect width="3" height="1" fill="#a8743f"/><rect y="0.5" width="3" height="0.15" fill="#8d5f31"/></pattern>
<pattern id="soil" width="1.6" height="1.6" patternUnits="userSpaceOnUse"><rect width="1.6" height="1.6" fill="#5a4636"/><circle cx="0.5" cy="0.5" r="0.2" fill="#4a3829"/></pattern>
<radialGradient id="fireglow"><stop offset="0" stop-color="#ffd166"/><stop offset="0.45" stop-color="#f08a24"/><stop offset="1" stop-color="#7a2e0e"/></radialGradient>
<radialGradient id="leaf" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#ffffff" stop-opacity="0.35"/><stop offset="1" stop-color="#000000" stop-opacity="0.25"/></radialGradient>
""")


class Map:
    """Перевод координат участка (м) в координаты листа (мм)."""

    def __init__(self, x0, y0, k, rot=False):
        self.x0, self.y0, self.k, self.rot = x0, y0, k, rot

    def __call__(self, x, y):
        if self.rot:   # дом слева, огород справа, левый забор сверху
            return self.x0 + y * self.k, self.y0 + x * self.k
        return self.x0 + x * self.k, self.y0 + (G.L - y) * self.k

    def poly(self, g):
        parts = []
        geoms = getattr(g, "geoms", [g])
        for p in geoms:
            if p.is_empty or p.geom_type != "Polygon":
                continue
            for ring in [p.exterior] + list(p.interiors):
                pts = [self(x, y) for x, y in ring.coords]
                parts.append("M" + "L".join(f"{a:.2f} {b:.2f}" for a, b in pts) + "Z")
        return "".join(parts)


def path_el(sh, m, g, fill, stroke="none", sw=0.2, extra=""):
    sh.e(f'<path d="{m.poly(g)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" fill-rule="evenodd" {extra}/>')


def blob(sh, cx, cy, r, color, seed, lobes=7, op=1.0, stroke=None):
    rnd = random.Random(seed)
    pts = []
    n = lobes * 4
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (0.86 + 0.14 * math.cos(lobes * a + rnd.random()) + 0.05 * rnd.random())
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"
    st = f'stroke="{stroke}" stroke-width="0.15"' if stroke else ""
    sh.e(f'<path d="{d}" fill="{color}" opacity="{op}" {st}/>')
    sh.e(f'<path d="{d}" fill="url(#leaf)" opacity="{op}"/>')


def stones(sh, m, size_k=1.0):
    ln = G.PATH_LINE
    s = 0.45
    while s < ln.length - 0.2:
        p, q = ln.interpolate(s - 0.05), ln.interpolate(s + 0.05)
        if G.PATIO + 0.1 < p.y < G.PIPE - 0.1:
            ax, ay = m(p.x, p.y)
            bx, by = m(q.x, q.y)
            ang = math.degrees(math.atan2(by - ay, bx - ax))
            w, h = 0.42 * m.k, 0.7 * m.k
            sh.e(f'<rect x="{-w/2:.2f}" y="{-h/2:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{0.06*m.k:.2f}" '
                 f'fill="#ece7dd" stroke="#b8ad9b" stroke-width="0.2" transform="translate({ax:.2f} {ay:.2f}) rotate({ang:.1f})"/>')
        s += 0.62


def base_plan(sh, m, garden=True, illustrate=True):
    k = m.k
    # соседние дома
    for x0, x1 in (((-1.9, -0.45), (G.W + 0.45, G.W + 1.9)) if garden else ()):
        ya, yb = (-1.5, G.L) if garden else (-1.5, G.PIPE + 0.6)
        a, b = m(x0, ya), m(x1, yb)
        sh.e(f'<rect x="{min(a[0],b[0]):.2f}" y="{min(a[1],b[1]):.2f}" width="{abs(b[0]-a[0]):.2f}" '
             f'height="{abs(b[1]-a[1]):.2f}" fill="url(#brick)" stroke="#9b5a40" stroke-width="0.3"/>')
    # огород
    if garden:
        path_el(sh, m, G.GRAVEL_G, "url(#gravel)")
        path_el(sh, m, G.RASP, "url(#mulch)")
        path_el(sh, m, G.PLUMZ, "url(#mulch)")
        for b in G.BEDS:
            path_el(sh, m, b, "url(#wood)", "#6d4826", 0.3)
            path_el(sh, m, b.buffer(-0.1), "url(#soil)")
            if illustrate:
                cx, cy = b.centroid.x, b.centroid.y
                rnd = random.Random(int(cx * 10 + cy * 100))
                for i in range(6):
                    px, py = m(cx - 0.65 + i * 0.26, cy + rnd.uniform(-0.3, 0.3))
                    blob(sh, px, py, 0.17 * k + rnd.random() * 0.06 * k, rnd.choice(["#4f8a3a", "#6aa34a", "#3f7a33", "#7cb35a"]), i + int(cx * 7))
        if illustrate:
            rnd = random.Random(5)
            y = G.PIPE + 0.3
            while y < G.L - 0.2:
                px, py = m(0.55 + rnd.uniform(-0.15, 0.15), y)
                blob(sh, px, py, 0.42 * k, rnd.choice(["#5d7f3c", "#4f7034"]), int(y * 10))
                for j in range(3):
                    sh.e(f'<circle cx="{px + rnd.uniform(-0.3,0.3)*k:.2f}" cy="{py + rnd.uniform(-0.3,0.3)*k:.2f}" r="{0.06*k:.2f}" fill="#b8263f"/>')
                y += 0.55
            for x, y, r in ((8.7, 17.6, 0.55), (8.6, 19.3, 0.6), (8.8, 25.3, 0.5), (8.3, 20.8, 0.45)):
                px, py = m(x, y)
                blob(sh, px, py, r * k, "#5f8746", int(x * y))
            px, py = m(*G.PLUM_C)
            blob(sh, px, py, G.PLUM_R * k, "#557a3f", 77, lobes=9, op=0.95, stroke="#3d5a2c")
            blob(sh, px + 0.3 * k, py - 0.3 * k, G.PLUM_R * 0.55 * k, "#6b9150", 78, op=0.7)
    # терраса
    path_el(sh, m, G.TERRACE, "url(#tiles)", "#b5ab9c", 0.2)
    import shapely.geometry as sg
    path_el(sh, m, sg.box(0, 0, G.W, G.TERR_ROOF), "url(#roof)", "#8a8780", 0.3)
    # посадки
    path_el(sh, m, G.LEFT_BED, "url(#mulch)")
    path_el(sh, m, G.RIGHT_BED, "url(#mulch)")
    path_el(sh, m, G.LAWN, "url(#lawn)", "#5d8a3a", 0.25)
    path_el(sh, m, G.PATH, "url(#gravel)", "#b8ad9b", 0.2)
    path_el(sh, m, G.FIRE, "url(#gravel)", "#a89a82", 0.3)
    stones(sh, m)
    # костровая зона: скамья, кресла, чаша
    fx, fy = G.FIRE_C
    a0, a1, rb = -65, 75, 1.45
    pts = [m(fx + rb * math.cos(math.radians(a)), fy + rb * math.sin(math.radians(a))) for a in range(a0, a1 + 1, 5)]
    d = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    sh.e(f'<path d="{d}" fill="none" stroke="#8a6440" stroke-width="{0.45*k:.2f}" stroke-linecap="round"/>')
    sh.e(f'<path d="{d}" fill="none" stroke="#d8c3a2" stroke-width="{0.32*k:.2f}" stroke-linecap="round"/>')
    for a in (135, 228):
        cx, cy = m(fx + 1.25 * math.cos(math.radians(a)), fy + 1.25 * math.sin(math.radians(a)))
        s = 0.6 * k
        sh.e(f'<rect x="{cx-s/2:.2f}" y="{cy-s/2:.2f}" width="{s:.2f}" height="{s:.2f}" rx="{0.1*k:.2f}" fill="#d9d2c4" stroke="#7a6f60" stroke-width="0.25"/>')
        sh.e(f'<rect x="{cx-s/2+0.08*k:.2f}" y="{cy-s/2+0.08*k:.2f}" width="{s-0.16*k:.2f}" height="{s-0.16*k:.2f}" rx="{0.08*k:.2f}" fill="#efe9de"/>')
    cx, cy = m(fx, fy)
    sh.e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{0.48*k:.2f}" fill="#3a3a38" stroke="#222" stroke-width="0.3"/>')
    sh.e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{0.36*k:.2f}" fill="url(#fireglow)"/>')
    # стол на площадке у дома
    tx, ty = m(2.8, 3.25)
    sh.e(f'<rect x="{tx-0.8*k:.2f}" y="{ty-0.45*k:.2f}" width="{1.6*k:.2f}" height="{0.9*k:.2f}" fill="#a67a4c" stroke="#6d4f30" stroke-width="0.25"/>') if not m.rot else \
        sh.e(f'<rect x="{tx-0.45*k:.2f}" y="{ty-0.8*k:.2f}" width="{0.9*k:.2f}" height="{1.6*k:.2f}" fill="#a67a4c" stroke="#6d4f30" stroke-width="0.25"/>')
    # инжир — крона поверх (полупрозрачно)
    return


def trees(sh, m, op=0.88):
    k = m.k
    px, py = m(*G.FIG_C)
    blob(sh, px, py, G.FIG_R * k, "#4f7f3a", 11, lobes=9, op=op, stroke="#35592a")
    blob(sh, px - 0.4 * k, py + 0.2 * k, G.FIG_R * 0.6 * k, "#6b9a4c", 12, lobes=6, op=0.6 * op)


def fence(sh, m, full=True):
    yb = G.L if full else G.PIPE + 0.6
    pts = [m(0, G.TERR_ROOF), m(0, yb), m(G.W, yb), m(G.W, G.TERR_ROOF)] if full else None
    for x in (0, G.W):
        a, b = m(x, 0), m(x, yb)
        sh.e(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="#3d3d3a" stroke-width="0.7"/>')
    if full:
        a, b = m(0, G.L), m(G.W, G.L)
        sh.e(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="#3d3d3a" stroke-width="0.7"/>')


def pipe(sh, m, label=True):
    a, b = m(-0.35, G.PIPE), m(G.W + 0.35, G.PIPE)
    sh.e(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="#2b2b2b" stroke-width="2.2"/>')
    sh.e(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="#f2c230" stroke-width="1.6" stroke-dasharray="3 2"/>')


def zone_tag(sh, x, y, code, r=3.2):
    sh.e(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{ZC[code]}" stroke="#fff" stroke-width="0.6"/>')
    sh.text(x, y + r * 0.36, code, size=r * 1.05, anchor="middle", weight="bold", fill="#fff", font=SERIF)


def callout(sh, x, y, tx, ty, lines, anchor="start"):
    sh.e(f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{tx:.2f}" y2="{ty:.2f}" stroke="{INK}" stroke-width="0.25"/>')
    sh.e(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.6" fill="{INK}"/>')
    w = max(len(s) for s in lines) * 1.45 + 3
    h = len(lines) * 3.4 + 1.6
    bx = tx if anchor == "start" else tx - w
    sh.e(f'<rect x="{bx:.2f}" y="{ty-h/2:.2f}" width="{w:.2f}" height="{h:.2f}" rx="1" fill="#fff" stroke="{INK}" stroke-width="0.25"/>')
    for i, s in enumerate(lines):
        sh.text(bx + w / 2, ty - h / 2 + 3.3 + i * 3.4, s, size=2.6, anchor="middle", weight="bold")


def dim_v(sh, x, y1, y2, label):
    sh.e(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{INK}" stroke-width="0.25"/>')
    for y in (y1, y2):
        sh.e(f'<line x1="{x-1.5}" y1="{y}" x2="{x+1.5}" y2="{y}" stroke="{INK}" stroke-width="0.35"/>')
    sh.text(x - 1.2, (y1 + y2) / 2, label, size=3, anchor="middle", weight="bold",
            extra=f'transform="rotate(-90 {x-1.2} {(y1+y2)/2})"')


def dim_h(sh, x1, x2, y, label):
    sh.e(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{INK}" stroke-width="0.25"/>')
    for x in (x1, x2):
        sh.e(f'<line x1="{x}" y1="{y-1.5}" x2="{x}" y2="{y+1.5}" stroke="{INK}" stroke-width="0.35"/>')
    sh.text((x1 + x2) / 2, y + 4.2, label, size=3, anchor="middle", weight="bold")


def plant_illustr(sh, m):
    k = m.k
    order = sorted(PL.P, key=lambda p: -PL.CAT[p[0]][2])
    greens = {1: "#3f6a33", 14: "#4f7f86", 15: "#2c5531", 9: "#3c6b35"}
    for i, (c, x, y) in enumerate(order):
        name, sort, d, col, _ = PL.CAT[c]
        px, py = m(x, y)
        r = d / 2 * k
        base = greens.get(c, "#4d7d3e" if c not in (7, 17) else "#b9ae7c")
        blob(sh, px, py, r, base, i * 13 + c, lobes=6 if c != 14 else 5)
        if c not in (1, 14, 15, 9, 12, 10):
            rnd = random.Random(i)
            for j in range(4 if d > 0.7 else 2):
                sh.e(f'<circle cx="{px + rnd.uniform(-0.5,0.5)*r:.2f}" cy="{py + rnd.uniform(-0.5,0.5)*r:.2f}" '
                     f'r="{max(0.35, r*0.28):.2f}" fill="{col}" opacity="0.95"/>')
        elif c in (12, 10):
            sh.e(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r*0.6:.2f}" fill="{col}" opacity="0.8"/>')


# ---------------------------------------------------------------- ЛИСТ 1
def sheet1():
    sh = Sheet(297, 420)
    defs(sh)
    sh.text(12, 20, "СХЕМА ЗОНИРОВАНИЯ УЧАСТКА · ВИД СВЕРХУ", size=7, font=SERIF)
    sh.e(f'<line x1="12" y1="24" x2="196" y2="24" stroke="{INK}" stroke-width="0.25"/>')
    sh.text(104, 30.5, "ЧАСТНЫЙ ДОМ · ВАРИАНТ 2: КОСТРОВАЯ ЗОНА СПРАВА", size=3.6, anchor="middle",
            font=SERIF, extra='letter-spacing="1"')
    sh.e('<rect x="205" y="9" width="80" height="24" fill="#e3eadb"/>')
    sh.text(245, 19.5, "26.0 × 9.5 м", size=7, anchor="middle", weight="bold", font=SERIF)
    sh.text(245, 28.5, "247 м²", size=7, anchor="middle", weight="bold", font=SERIF)

    m = Map(38, 50, 12.5)  # 1:80
    base_plan(sh, m)
    plant_illustr(sh, m)
    trees(sh, m)
    fence(sh, m)
    pipe(sh, m)
    a = m(0, G.L)
    sh.text((m(0, 0)[0] + m(G.W, 0)[0]) / 2, a[1] - 2, "Задний забор участка", size=3, anchor="middle")
    # подписи
    tx, ty = m(G.W / 2, G.TERR_ROOF / 2)
    sh.text(tx, ty - 0.5, "Крытая терраса", size=3.4, anchor="middle", weight="bold")
    sh.text(tx, ty + 3.5, "(выход из дома)", size=3, anchor="middle")
    for code, (x, y) in {"A": (3.6, 7.8), "B": (4.95, 12.6), "C": (1.0, 9.0), "D": (8.5, 10.9),
                         "E": (6.6, 6.5), "K": (1.4, 3.25), "F": (4.65, 21.4), "G": (4.65, 18.2),
                         "H": (0.65, 21.4), "I": (8.65, 18.3)}.items():
        zone_tag(sh, *m(x, y), code)
    x, y = m(*G.FIG_C)
    sh.text(x, y + 9, "инжир (сущ.)", size=2.8, anchor="middle", fill="#fff", weight="bold")
    x, y = m(G.W / 2, G.PIPE)
    sh.text(x, y - 2.6, "газовая труба (сохраняется) · калитка", size=2.6, anchor="middle", weight="bold")
    # подписи соседей
    for xx, lbl in ((-1.15, "Соседний жилой дом (левое здание)"), (G.W + 1.15, "Соседний жилой дом (правое здание)")):
        px, py = m(xx, 9.0)
        sh.text(px, py, lbl, size=2.6, anchor="middle", fill="#fff", weight="bold",
                extra=f'transform="rotate(-90 {px:.2f} {py:.2f})"')
    # размеры
    top, bot = m(0, G.L)[1], m(0, 0)[1]
    dim_v(sh, 26, top, bot, "26.0 м")
    l, r = m(0, 0)[0], m(G.W, 0)[0]
    dim_h(sh, l, r, bot + 5, "9.5 м")
    # север (по исходной схеме)
    sh.e(f'<g transform="translate(272 46) rotate(-45)"><path d="M0 -7 L4 5 L0 2.5 L-4 5Z" fill="{INK}"/></g>')
    sh.text(280, 50, "N", size=4, weight="bold", font=SERIF)

    # экспликация
    X, Y = 181, 60
    sh.e(f'<rect x="{X}" y="{Y}" width="104" height="8" fill="#e3eadb"/>')
    sh.text(X + 3, Y + 5.6, "ЭКСПЛИКАЦИЯ ЗОН И ПЛОЩАДЕЙ", size=3.6, weight="bold", font=SERIF)
    Y += 10
    cols = [X, X + 10, X + 66, X + 84, X + 104]
    sh.text(cols[0] + 5, Y + 4.5, "№", size=2.7, anchor="middle")
    sh.text(cols[1] + 2, Y + 4.5, "Наименование зоны", size=2.7)
    sh.text(cols[2] + 10, Y + 4.5, "м²", size=2.7, anchor="middle")
    sh.text(cols[3] + 10, Y + 4.5, "%", size=2.7, anchor="middle")
    Y += 7
    tot = 0
    rows = G.ZONES
    for code, name, g in rows:
        a = g.area
        tot += a
        h = 9.2
        sh.e(f'<rect x="{X}" y="{Y}" width="104" height="{h}" fill="#fff" stroke="#c9cfc2" stroke-width="0.2"/>')
        zone_tag(sh, X + 5, Y + h / 2, code, r=3)
        words = name.split(" ")
        lines, cur = [], ""
        for w in words:
            if len(cur) + len(w) > 31:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for i, s in enumerate(lines):
            sh.text(cols[1] + 2, Y + h / 2 + 1 - (len(lines) - 1) * 1.6 + i * 3.2, s, size=2.6)
        sh.text(cols[2] + 10, Y + h / 2 + 1, f"{a:.0f}", size=3, anchor="middle")
        sh.text(cols[3] + 10, Y + h / 2 + 1, f"{a / 2.47:.1f}%", size=2.8, anchor="middle")
        Y += h
    sh.e(f'<rect x="{X}" y="{Y}" width="104" height="8" fill="#e3eadb"/>')
    sh.text(cols[2] - 3, Y + 5.6, "ИТОГО:", size=3.2, anchor="end", weight="bold")
    sh.text(cols[2] + 10, Y + 5.6, f"{tot:.0f}", size=3.2, anchor="middle", weight="bold")
    sh.text(cols[3] + 10, Y + 5.6, "100%", size=3.2, anchor="middle", weight="bold")
    Y += 11
    deco = G.DECO.area + G.TERRACE.area
    for s1, s2 in ((f"Декоративная зона до трубы —", f"{deco:.0f} м² (≈{deco/2.47:.0f}%)"),
                   (f"Огород после газовой трубы —", f"{G.GARDEN.area:.0f} м² (≈{G.GARDEN.area/2.47:.0f}%)")):
        sh.e(f'<rect x="{X}" y="{Y}" width="104" height="12" fill="#e3eadb"/>')
        sh.text(X + 3, Y + 5, s1, size=3, font=SERIF)
        sh.text(X + 3, Y + 9.6, s2, size=3.3, weight="bold", font=SERIF)
        Y += 14
    # что изменилось
    Y += 2
    sh.text(X, Y, "ЧТО ИЗМЕНЕНО", size=3.6, weight="bold", font=SERIF)
    sh.e(f'<line x1="{X}" y1="{Y+1.5}" x2="{X+104}" y2="{Y+1.5}" stroke="{INK}" stroke-width="0.25"/>')
    notes = [
        "• Костровая зона — справа: гравийный круг",
        "  Ø 3.8 м, чаша в центре, скамья по дуге со",
        "  стороны забора, 2 кресла, вход с дорожки.",
        "  От чаши до правого забора 3.3 м.",
        "• Дорожка из плит: от террасы вдоль правой",
        "  посадки, огибает костровую площадку и",
        "  между костром и инжиром выходит к калитке",
        "  огорода по центру газовой трубы.",
        "• Газон — единым полотном по центру; левая",
        "  посадка — цельный миксбордер до инжира.",
        "• Под инжиром — тенистый уголок.",
        "• У костра вместо хвойных — лавровишня;",
        "  злаки и можжевельники — не ближе 3 м.",
        "• Огород — без изменений по концепции.",
    ]
    for i, s in enumerate(notes):
        sh.text(X, Y + 6.5 + i * 3.9, s, size=2.75)
    Y += 6.5 + len(notes) * 3.9 + 4
    # условные обозначения
    sh.text(X, Y, "УСЛОВНЫЕ ОБОЗНАЧЕНИЯ", size=3.6, weight="bold", font=SERIF)
    sh.e(f'<line x1="{X}" y1="{Y+1.5}" x2="{X+104}" y2="{Y+1.5}" stroke="{INK}" stroke-width="0.25"/>')
    Y += 5
    leg = [("lawn", "Газон"), ("gravel", "Гравийное покрытие"), ("mulch", "Посадки (мульча)"),
           ("wood", "Высокие грядки"), ("tiles", "Плитка террасы"), ("roof", "Кровля крытой террасы"),
           ("brick", "Существующие здания (соседи)"), (None, "Существующая газовая труба"),
           ("stone", "Пошаговые плиты (дорожка)"), ("fire", "Костровая чаша")]
    for i, (pat, lbl) in enumerate(leg):
        cx = X
        cy = Y + i * 6.6
        if pat == "stone":
            sh.e(f'<rect x="{cx}" y="{cy}" width="12" height="5" fill="url(#gravel)"/>')
            for j in range(3):
                sh.e(f'<rect x="{cx+1+j*3.8:.1f}" y="{cy+0.7}" width="2.6" height="3.6" rx="0.4" fill="#ece7dd" stroke="#b8ad9b" stroke-width="0.2"/>')
        elif pat == "fire":
            sh.e(f'<circle cx="{cx+6}" cy="{cy+2.5}" r="2.5" fill="#3a3a38"/><circle cx="{cx+6}" cy="{cy+2.5}" r="1.8" fill="url(#fireglow)"/>')
        elif pat is None:
            sh.e(f'<line x1="{cx}" y1="{cy+2.5}" x2="{cx+12}" y2="{cy+2.5}" stroke="#2b2b2b" stroke-width="2.2"/>'
                 f'<line x1="{cx}" y1="{cy+2.5}" x2="{cx+12}" y2="{cy+2.5}" stroke="#f2c230" stroke-width="1.6" stroke-dasharray="3 2"/>')
        else:
            sh.e(f'<rect x="{cx}" y="{cy}" width="12" height="5" fill="url(#{pat})" stroke="#999" stroke-width="0.15"/>')
        sh.text(cx + 15, cy + 3.8, lbl, size=2.7)
    # подвал
    sh.e(f'<line x1="12" y1="398" x2="285" y2="398" stroke="{INK}" stroke-width="0.2"/>')
    sh.text(12, 405, "Площади рассчитаны по геометрии схемы (генератор draw.py), точность ±0.5 м².", size=2.6)
    sh.text(12, 410, "Растения в декоративной зоне — по плану рассадки (лист 2).", size=2.6)
    sh.text(285, 405, "Масштаб 1:80", size=2.8, anchor="end")
    sh.text(285, 410, "Формат А3 · лист 1", size=2.8, anchor="end")
    sh.save("uchastok_list1.svg")


# ---------------------------------------------------------------- ЛИСТ 2
def sheet2():
    sh = Sheet(420, 297)
    defs(sh)
    sh.text(14, 17, "ПЛАН РАССАДКИ ДЕКОРАТИВНОЙ ЗОНЫ", size=7.5, font=SERIF, extra='letter-spacing="0.3"')
    sh.text(14, 24, "от террасы до газовой трубы · костровая зона справа · вид сверху, дом слева",
            size=3.4, font=SERIF, fill="#5b6455")
    k = 20  # 1:50
    m = Map(16, 36, k, rot=True)
    # фон без иллюстрации растений, приглушённый
    sh.e('<g opacity="0.55">')
    base_plan(sh, m, garden=False, illustrate=False)
    sh.e('</g>')
    fence(sh, m, full=False)
    pipe(sh, m)
    # зона 3 м от чаши
    cx, cy = m(*G.FIRE_C)
    sh.e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{3*k}" fill="none" stroke="#d2552a" stroke-width="0.45" stroke-dasharray="2.5 1.5"/>')
    # инжир — контур
    fx, fy = m(*G.FIG_C)
    sh.e(f'<circle cx="{fx:.2f}" cy="{fy:.2f}" r="{G.FIG_R*k}" fill="#6b9a4c" fill-opacity="0.12" stroke="#35592a" stroke-width="0.4" stroke-dasharray="3 1.2"/>')
    sh.e(f'<circle cx="{fx:.2f}" cy="{fy:.2f}" r="2" fill="#6b4a2b"/>')
    sh.text(fx, fy + 6, "инжир (сущ.)", size=2.8, anchor="middle", weight="bold", fill="#35592a")
    # растения
    for c, x, y in sorted(PL.P, key=lambda p: -PL.CAT[p[0]][2]):
        name, sort, d, col, _ = PL.CAT[c]
        px, py = m(x, y)
        r = d / 2 * k
        sh.e(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r:.2f}" fill="{col}" fill-opacity="0.85" stroke="#3a4a33" stroke-width="0.3"/>')
        dark = col in ("#4f6b3a", "#2f5a34", "#3f6a3a", "#4a2a3a", "#6b55a8", "#5f8a9a", "#5b6fc8")
        fs = 2.4 if r < 4.5 else 3.0
        sh.text(px, py + fs * 0.36, str(c), size=fs, anchor="middle", weight="bold", fill="#fff" if dark else INK)
    # подписи зон
    for code, (x, y) in {"A": (3.6, 7.8), "B": (4.95, 12.6), "E": (6.7, 6.2), "K": (4.7, 1.3)}.items():
        zone_tag(sh, *m(x, y), code, r=3.4)
    tx, ty = m(G.W / 2, G.TERR_ROOF / 2)
    sh.text(tx, ty + 30, "крытая терраса", size=3, anchor="middle", weight="bold",
            extra=f'transform="rotate(-90 {tx:.2f} {ty+30:.2f})"')
    px, py = m(-0.2, 4.2)
    sh.text(px, py - 1, "левый забор (соседний дом)", size=2.8)
    px, py = m(G.W + 0.2, 4.2)
    sh.text(px, py + 3.2, "правый забор (соседний дом)", size=2.4)
    px, py = m(G.W / 2, G.PIPE)
    sh.text(px + 4.5, py, "газовая труба · калитка → огород", size=2.8, anchor="middle", weight="bold",
            extra=f'transform="rotate(90 {px+4.5:.2f} {py:.2f})"')
    # размерные привязки
    a, b = m(G.W, G.FIRE_C[1]), m(*G.FIRE_C)
    sh.e(f'<line x1="{b[0]:.2f}" y1="{b[1]:.2f}" x2="{a[0]:.2f}" y2="{a[1]:.2f}" stroke="#c0461d" stroke-width="0.3"/>')
    sh.text(b[0] + 1.2, (a[1] + b[1]) / 2 - 6, "3.3 м", size=2.6, fill="#c0461d", weight="bold")
    # масштабная линейка
    X0, Y0 = 364, 200
    for i in range(5):
        sh.e(f'<rect x="{X0+i*k/2}" y="{Y0}" width="{k/2}" height="1.6" fill="{INK if i%2==0 else "#fff"}" stroke="{INK}" stroke-width="0.2"/>')
        sh.text(X0 + i * k / 2, Y0 + 5, f"{i}", size=2.4, anchor="middle")
    sh.text(X0 + 5 * k / 2, Y0 + 5, "5 м", size=2.4, anchor="middle")
    sh.text(X0, Y0 - 3, "Масштаб 1:50 (А3)", size=2.8, weight="bold")
    # примечания справа
    X, Y = 364, 40
    sh.text(X, Y, "ПРИНЦИПЫ", size=3.6, weight="bold", font=SERIF)
    sh.e(f'<line x1="{X}" y1="{Y+122}" x2="{X+10}" y2="{Y+122}" stroke="#d2552a" stroke-width="0.45" stroke-dasharray="2.5 1.5"/>')
    sh.text(X + 12, Y + 123, "R 3 м от чаши:", size=2.6, fill="#c0461d", weight="bold")
    sh.text(X, Y + 127, "без хвойных, злаков", size=2.6, fill="#c0461d", weight="bold")
    sh.text(X, Y + 130.5, "и сухостоя", size=2.6, fill="#c0461d", weight="bold")
    notes = ["Слева — многоярусный", "миксбордер: изгородь,", "кустарники, многолетники;",
             "в конце — тенистый", "уголок под инжиром.", "",
             "Справа у террасы —", "колоновидные можжевельники,", "дальше вдоль костра —",
             "лавровишня (широколист-", "ная, сочная, слабо горит).", "",
             "Костёр обрамлён кольцом", "очитка (суккулент) —", "живая противопожарная", "кайма.", "",
             "Злаки, хвойные, лаванда", "и розы — не ближе 3 м", "от чаши.", "",
             "Между плит у террасы —", "тимьян ползучий, ~1 м²", "(8–10 шт.).", "",
             "Тюльпаны 40–60 шт.", "группами между", "многолетниками слева.", "",
             "Мульча — кора сосны;", "у костра — гравий."]
    for i, s in enumerate(notes):
        sh.text(X, Y + 5.5 + i * 3.55, s, size=2.6)
    # таблица ассортимента
    Y = 238
    sh.e(f'<rect x="14" y="{Y-6}" width="392" height="7.5" fill="#e3eadb"/>')
    sh.text(17, Y - 0.8, "АССОРТИМЕНТ И КОЛИЧЕСТВО", size=3.6, weight="bold", font=SERIF)
    sh.text(403, Y - 0.8, "Климат Краснодарского края · размеры — диаметр куста во взрослом виде",
            size=2.5, anchor="end", fill="#5b6455")
    cnt = PL.counts()
    items = sorted(PL.CAT)
    per = math.ceil(len(items) / 3)
    for i, c in enumerate(items):
        col, rowi = divmod(i, per)
        x = 14 + col * 131
        y = Y + 4.5 + rowi * 7.0
        name, sort, d, color, note = PL.CAT[c]
        sh.e(f'<circle cx="{x+3.5}" cy="{y}" r="3" fill="{color}" stroke="#3a4a33" stroke-width="0.3"/>')
        dark = color in ("#4f6b3a", "#2f5a34", "#3f6a3a", "#4a2a3a", "#6b55a8", "#5f8a9a", "#5b6fc8")
        sh.text(x + 3.5, y + 1, str(c), size=2.6, anchor="middle", weight="bold", fill="#fff" if dark else INK)
        sh.text(x + 8.5, y - 0.4, f"{name} <tspan font-style=\"italic\">{sort}</tspan>", size=2.6, weight="bold")
        sh.text(x + 8.5, y + 2.8, f"{note} · Ø {d:.1f} м".replace(".", ","), size=2.2, fill="#5b6455")
        sh.text(x + 128, y + 0.6, f"{cnt.get(c, 0)} шт.", size=2.9, anchor="end", weight="bold")
    sh.text(406, 292, f"Всего растений: {sum(cnt.values())} шт. (без луковичных и тимьяна) · лист 2",
            size=2.6, anchor="end")
    sh.save("uchastok_list2.svg")


if __name__ == "__main__":
    assert PL.check() == 0
    sheet1()
    sheet2()
