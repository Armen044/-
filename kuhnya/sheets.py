#!/usr/bin/env python3
"""Листы А3 кухни: 1 — развёртка, план, разрез (1:20); 2 — узлы (пенал специй, духовка, ящики Gola);
3 — модули, фасады, фурнитура Blum."""
import math
import os

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "DejaVu Sans, Arial, sans-serif"
RED = "#c0392b"
EN, WN, GL = "#ffffff", "#8a5d3b", "#e4f1f6"
FILL = {M.ENAMEL: EN, M.WALNUT: WN, M.ALU: "#b0b4b8"}


class S:
    def __init__(s):
        s.o = []

    def e(s, x):
        s.o.append(x)

    def t(s, x, y, txt, size=2.5, anchor="middle", weight="normal", fill="#111", rot=None):
        r = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ""
        s.e(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}"{r}>{txt}</text>')

    def ln(s, x1, y1, x2, y2, w=0.2, c="#111", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.e(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}"{d}/>')

    def rc(s, x0, y0, x1, y1, fill="none", stroke="#111", w=0.2, dash=None, rx=0):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.e(f'<rect x="{min(x0,x1):.2f}" y="{min(y0,y1):.2f}" width="{abs(x1-x0):.2f}" height="{abs(y1-y0):.2f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{w}"{d}/>')

    def save(s, name, w=420, h=297):
        defs = ('<defs><pattern id="hatch" width="1" height="1" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                '<rect width="1" height="1" fill="#fff"/><line x1="0" y1="0" x2="0" y2="1" stroke="#555" stroke-width="0.22"/></pattern>'
                '<pattern id="glass" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">'
                '<rect width="3" height="3" fill="#e4f1f6"/><line x1="0" y1="0" x2="0" y2="3" stroke="#9cc3d2" stroke-width="0.25"/></pattern>'
                '<linearGradient id="cyl" x1="0" x2="1"><stop offset="0" stop-color="#0d0e10"/><stop offset="0.35" stop-color="#4a4d52"/>'
                '<stop offset="0.55" stop-color="#2a2c30"/><stop offset="1" stop-color="#08090a"/></linearGradient>'
                '<radialGradient id="glow" cx="0.5" cy="0" r="1"><stop offset="0" stop-color="#ffe9b0" stop-opacity="0.9"/>'
                '<stop offset="1" stop-color="#ffe9b0" stop-opacity="0"/></radialGradient>'
                '<pattern id="veneer" width="2" height="6" patternUnits="userSpaceOnUse">'
                '<rect width="2" height="6" fill="#8a5d3b"/><line x1="0.6" y1="0" x2="0.9" y2="6" stroke="#7a5133" stroke-width="0.25"/></pattern></defs>')
        with open(os.path.join(HERE, name), "w") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">{defs}'
                    f'<rect width="{w}" height="{h}" fill="#fff"/>'
                    f'<rect x="5" y="5" width="{w-10}" height="{h-10}" fill="none" stroke="#111" stroke-width="0.4"/>'
                    f'{"".join(s.o)}</svg>')


def dim_h(s, x1, x2, y, label, size=2.0):
    s.ln(x1, y, x2, y, 0.15, RED)
    for x in (x1, x2):
        s.ln(x - 0.6, y + 0.6, x + 0.6, y - 0.6, 0.28, RED)
    s.t((x1 + x2) / 2, y - 0.7, label, size, fill=RED)


def dim_v(s, y1, y2, x, label, size=2.0, side=-1):
    s.ln(x, y1, x, y2, 0.15, RED)
    for y in (y1, y2):
        s.ln(x - 0.6, y + 0.6, x + 0.6, y - 0.6, 0.28, RED)
    s.t(x + side * 0.7, (y1 + y2) / 2, label, size, fill=RED, rot=-90)


def header(s, title, sub, n, tot=2):
    s.t(12, 15, title, 5.6, "start", "bold")
    s.t(12, 21.5, sub, 2.8, "start")
    s.t(408, 15, f"Лист {n}/{tot}", 3.2, "end")


def tag(s, x, y, code):
    s.e(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.3" fill="#fff" stroke="#1f4e79" stroke-width="0.25"/>')
    s.t(x, y + 0.8, code, 1.8, weight="bold", fill="#1f4e79")


def ctx(name):
    return [c for c in M.CONTEXT if c["name"].startswith(name)]


def facade_draw(s, R, f, fa, k):
    fill = "url(#veneer)" if fa["mat"] == M.WALNUT else FILL[fa["mat"]]
    if fa["kind"] == "glass":
        R(fa["x0"], fa["z0"], fa["x1"], fa["z1"], fill="#b0b4b8", stroke="#111", w=0.22)
        R(fa["x0"] + 20, fa["z0"] + 20, fa["x1"] - 20, fa["z1"] - 20, fill="url(#glass)", stroke="#777", w=0.12)
        return
    R(fa["x0"], fa["z0"], fa["x1"], fa["z1"], fill=fill, stroke="#111", w=0.22)
    if fa["mat"] == M.WALNUT and fa["z1"] - fa["z0"] > 2000:      # торцевая ручка из массива (вертикально, со стороны открывания)
        R(fa["x0"], fa["z0"] + 900, fa["x0"] + 18, fa["z0"] + 1700, fill="#5a3a22", stroke="#2b1a0e", w=0.1)
    if fa["kind"] == "dw":
        x, y = f((fa["x0"] + fa["x1"]) / 2, (fa["z0"] + fa["z1"]) / 2)
        s.t(x, y, "ПММ 600", 1.8, fill="#777")


# ---------------------------------------------------------------- лист 1
K = 1 / 20


def elevation(s, X, G):
    f = lambda x, z: (X + x * K, G - z * K)
    R = lambda x0, z0, x1, z1, **kw: s.rc(*f(x0, z0), *f(x1, z1), **kw)
    R(0, 0, M.L, M.H, fill="#f7f5f1", stroke="#bbb", w=0.15)
    s.ln(*f(-150, M.H), *f(M.L + 150, M.H), 0.3, "#777", "2 1")
    s.ln(*f(-150, 0), *f(M.L + 150, 0), 0.4)
    for p in M.PARTS:
        if p["group"] == "П1" and p["name"] in ("Боковина", "Крышка"):
            R(p["x0"], p["z0"], p["x1"], p["z1"], fill="url(#veneer)" if p["name"] == "Боковина" else "#c9b8a6", stroke="#111", w=0.2)
        if p["group"] == "В8":
            R(p["x0"], p["z0"], p["x1"], p["z1"], fill="url(#veneer)", stroke="#111", w=0.2)
        if p["group"] == "Р":
            for xx in range(int(p["x0"]) + 30, int(p["x1"]), 60):
                R(xx - 20, p["z0"], xx + 20, p["z1"], fill="url(#veneer)", stroke="#5a3a22", w=0.1)
    fr = ctx("Холодильник")[0]
    R(fr["x0"], fr["z0"], fr["x1"], fr["z1"], fill="#2b2d30", stroke="#000", w=0.2)
    s.ln(*f((fr["x0"] + fr["x1"]) / 2, 0), *f((fr["x0"] + fr["x1"]) / 2, fr["z1"]), 0.2, "#666")
    x, y = f(M.X0 / 2, 1300)
    s.t(x, y, "холодильник", 2.0, fill="#ddd")
    s.t(x, y + 2.8, "отдельностоящий", 1.8, fill="#ddd")
    R(M.X0, 0, M.XT, M.PL, fill="#ececea", stroke="#888", w=0.15)
    R(M.XT, 0, M.L, M.PL, fill="url(#veneer)", stroke="#888", w=0.15)
    R(M.X0, M.ZB, M.XT, M.ZB + M.CT, fill="#e6e3dc", stroke="#111", w=0.22)
    s.ln(*f(M.X0, M.ZB - 15), *f(M.XT, M.ZB - 15), 0.9, "#444")
    for fa in M.FACADES:
        facade_draw(s, R, f, fa, K)
        if fa["kind"] == "drawer" and fa["z1"] < 700 and fa["z1"] > 300:
            s.ln(*f(fa["x0"], fa["z1"] + 16), *f(fa["x1"], fa["z1"] + 16), 0.9, "#444")
    ov = ctx("Духовой")[0]
    R(ov["x0"], ov["z0"], ov["x1"], ov["z1"], fill="#1f2022", stroke="#000", w=0.2)
    R(ov["x0"] + 50, ov["z0"] + 80, ov["x1"] - 50, ov["z1"] - 140, fill="#3a3d41", stroke="#555", w=0.1)
    s.ln(*f(ov["x0"], ov["z0"] - 16), *f(ov["x1"], ov["z0"] - 16), 0.9, "#444")
    hd = ctx("Вытяжка")[0]
    xc = (hd["x0"] + hd["x1"]) / 2
    # каминная вытяжка: цилиндр Ø300 h 650 + труба Ø160 до потолка, LED-кольцо снизу
    gx, gy = f(xc - 230, M.ZU0 + 40)
    s.e(f'<ellipse cx="{f(xc, 0)[0]:.2f}" cy="{f(0, M.ZU0 - 120)[1]:.2f}" rx="{230 * K:.2f}" ry="{170 * K:.2f}" fill="url(#glow)"/>')
    R(xc - 80, 2150, xc + 80, M.H, fill="url(#cyl)", stroke="#000", w=0.15)
    R(xc - 150, M.ZU0 + 40, xc + 150, 2160, fill="url(#cyl)", stroke="#000", w=0.2, rx=0.8)
    R(xc - 150, M.ZU0 + 40, xc + 150, M.ZU0 + 58, fill="#f5c518", stroke="none", rx=0.6)
    R(xc - 150, 2140, xc + 150, 2160, fill="#3a3d41", stroke="#000", w=0.1)
    for p in M.PARTS:
        if p["name"].startswith("Полка стеклянная"):
            s.ln(*f(p["x0"], (p["z0"] + p["z1"]) / 2), *f(p["x1"], (p["z0"] + p["z1"]) / 2), 0.3, "#5b93a8")
        if p["name"].startswith("Профиль LED"):
            R(p["x0"], p["z0"], p["x1"], p["z1"], fill="#f5c518", stroke="none")
    s.ln(*f(M.X0, M.ZU0 - 8), *f(M.X0 + 1050, M.ZU0 - 8), 0.7, "#f5c518")
    s.ln(*f(M.X0 + 1650, M.ZU0 - 8), *f(M.XT, M.ZU0 - 8), 0.7, "#f5c518")
    xs = [0, M.X0]
    for w, _ in M.BASE + M.TALL:
        xs.append(xs[-1] + w)
    for a, b in zip(xs, xs[1:]):
        dim_h(s, f(a, 0)[0], f(b, 0)[0], G + 5, str(b - a), 1.8)
    dim_h(s, f(0, 0)[0], f(M.L, 0)[0], G + 10, f"{M.L}  (на рендере подписано 5600 — сверить с замером)", 2.3)
    xu = [M.X0]
    for w, _ in M.UPPER:
        xu.append(xu[-1] + w)
    for a, b in zip(xu, xu[1:]):
        dim_h(s, f(a, 0)[0], f(b, 0)[0], f(0, M.H)[1] - 4, f"{b - a:g}".replace(".", ","), 1.8)
    xr = f(M.L, 0)[0]
    lv = [0, M.PL, M.ZB + M.CT, M.ZU0, M.ZU1, M.H]
    for z0, z1 in zip(lv, lv[1:]):
        dim_v(s, f(0, z0)[1], f(0, z1)[1], xr + 5, str(z1 - z0), 1.8, side=1.6)
    dim_v(s, f(0, 0)[1], f(0, M.H)[1], X - 5, "3000", 2.3)
    s.t(X + M.L * K / 2, f(0, M.H)[1] - 9, "РАЗВЁРТКА ПО СТЕНЕ  М 1:20", 3, weight="bold")
    for z, d in ((M.H + 80, -0.6), (-80, 3.2)):
        x, y = f(1900, z)
        s.t(x - 2.5, y + d, "А", 2.6, weight="bold")
    s.ln(*f(1900, M.H + 60), *f(1900, M.H - 50), 0.5)
    s.ln(*f(1900, 40), *f(1900, -60), 0.5)


def plan(s, X, Yw):
    f = lambda x, y: (X + x * K, Yw + y * K)
    R = lambda x0, y0, x1, y1, **kw: s.rc(*f(x0, y0), *f(x1, y1), **kw)
    s.ln(*f(-150, 0), *f(M.L + 150, 0), 0.5)
    R(0, 0, M.X0, M.DFR, fill="#e9e3dc", stroke="#111", w=0.2)
    fr = ctx("Холодильник")[0]
    R(fr["x0"], fr["y0"], fr["x1"], fr["y1"], fill="#2b2d30", stroke="#000", w=0.15)
    R(M.X0, 0, M.XT, 600, fill="#e6e3dc", stroke="#111", w=0.2)
    for c in ctx("Варочная") + ctx("Мойка"):
        R(c["x0"], c["y0"], c["x1"], c["y1"], fill="#222" if "Вароч" in c["name"] else "#b9bcbf", stroke="#111", w=0.15, rx=0.6)
    hd = ctx("Вытяжка")[0]
    xc = (hd["x0"] + hd["x1"]) / 2
    s.e(f'<circle cx="{f(xc, 0)[0]:.2f}" cy="{f(0, 250)[1]:.2f}" r="{120 * K:.2f}" fill="none" stroke="#111" stroke-width="0.25" stroke-dasharray="1.2 0.8"/>')
    R(M.XT, 0, M.L, M.DTALL + 22, fill="#e9e3dc", stroke="#111", w=0.2)
    s.ln(*f(M.XT + 600, 0), *f(M.XT + 600, M.DTALL + 22), 0.2)
    s.ln(*f(M.X0, M.DU + 22), *f(M.XT, M.DU + 22), 0.25, "#111", "2 1")
    dim_v(s, f(0, 0)[1], f(0, M.DFR)[1], X - 4, "700", 1.8)
    dim_v(s, f(0, 0)[1], f(0, 600)[1], f(M.L, 0)[0] + 4, "600", 1.8, side=1.6)
    s.t(X + M.L * K / 2, Yw - 3, "ПЛАН  М 1:20  (пунктир — верхний ряд и вытяжка)", 2.8, weight="bold")


def section(s, X, G, xc=1900):
    f = lambda y, z: (X + y * K, G - z * K)
    R = lambda y0, z0, y1, z1, **kw: s.rc(*f(y0, z0), *f(y1, z1), **kw)
    s.ln(*f(0, -50), *f(0, M.H + 50), 0.5)
    s.ln(*f(-50, 0), *f(800, 0), 0.4)
    for p in M.PARTS:
        if p["x0"] < xc < p["x1"]:
            R(p["y0"], p["z0"], p["y1"], p["z1"], fill="url(#hatch)", stroke="#111", w=0.2)
    for fa in M.FACADES:
        if fa["x0"] < xc < fa["x1"]:
            R(fa["y"], fa["z0"], fa["y"] + M.FD, fa["z1"], fill="url(#veneer)" if fa["mat"] == M.WALNUT else "#fff", stroke="#111", w=0.25)
    for z in [M.ZB - 15, M.ZC + 16]:
        R(M.DB - 40, z - 12, M.DB, z + 12, fill="#888", stroke="#333", w=0.15)
    lv = [0, M.PL, M.ZB + M.CT, M.ZU0, M.ZU1, M.H]
    for z0, z1 in zip(lv, lv[1:]):
        dim_v(s, f(0, z0)[1], f(0, z1)[1], X - 4, str(z1 - z0), 1.8)
    dim_h(s, f(0, 0)[0], f(600, 0)[0], G + 4.5, "600", 1.8)
    dim_h(s, f(0, M.H)[0], f(M.DU + 22, 0)[0], f(0, M.H)[1] - 3, "372", 1.8)
    s.t(X + 380 * K, f(0, M.H)[1] - 8, "РАЗРЕЗ А–А  М 1:20", 2.8, weight="bold")


def sheet1():
    s = S()
    header(s, "Кухня — развёртка, план, разрез",
           "Низ и верх: МДФ эмаль белая (2 стороны), Gola  |  Пеналы и антресоль: МДФ шпон американского ореха, торцевая ручка массив  |  Фурнитура Blum", 1)
    elevation(s, 20, 205)
    plan(s, 20, 236)
    section(s, 350, 205)
    X, Y = 330, 234
    s.t(X, Y, "Обозначения", 3.0, "start", "bold")
    for i, (fill, txt) in enumerate(((EN, "МДФ эмаль белая, покраска 2 стороны"), ("url(#veneer)", "МДФ шпон американского ореха"),
                                     ("url(#glass)", "алюм. рамка + стекло"), ("#444", "профиль Gola"), ("#f5c518", "LED-подсветка"))):
        y = Y + 3 + i * 4.3
        s.rc(X, y, X + 7, y + 2.8, fill=fill, stroke="#111", w=0.15)
        s.t(X + 9, y + 2.3, txt, 2.1, "start")
    s.t(X, Y + 28, "Вид сбоку с материалами и глубинами — лист 2", 2.0, "start")
    s.save("kuhnya_list1.svg")


# ---------------------------------------------------------------- лист 2: узлы
def detail_spice(s, X, G, k=1 / 15):
    f = lambda x, z: (X + (x - (M.XT + 600)) * k, G - z * k)
    R = lambda x0, z0, x1, z1, **kw: s.rc(*f(x0, z0), *f(x1, z1), **kw)
    for p in M.PARTS:
        if p["group"] in ("П3", "А6"):
            if p["name"].startswith("Внутренний"):
                R(p["x0"], p["z0"], p["x1"], p["z1"], fill="#5f6368", stroke="#222", w=0.2)
                R(p["x0"] + 10, p["z1"] - 25, p["x1"] - 10, p["z1"] - 5, fill="#7b8086", stroke="none")
            elif p["name"].startswith("Дистанц"):
                R(p["x0"], p["z0"], p["x1"], p["z1"], fill="#d9b98c", stroke="#111", w=0.15)
            else:
                R(p["x0"], p["z0"], p["x1"], p["z1"], fill="url(#veneer)" if "шпон" in p["mat"] else "#cbb9a6", stroke="#111", w=0.2)
    R(M.XT + 600, 0, M.L, M.PL, fill="url(#veneer)", stroke="#888", w=0.15)
    s.ln(*f(M.XT + 580, 0), *f(M.L + 30, 0), 0.4)
    zs = [M.PL] + [z for zz in M.INNER for z in zz] + [1760, 2150, M.ZU1]
    for a, b in zip(zs, zs[1:]):
        if b - a > 60:
            dim_v(s, f(0, a)[1], f(0, b)[1], f(M.L, 0)[0] + 3, str(round(b - a)), 1.6, side=1.5)
    dim_h(s, f(M.XT + 600, 0)[0], f(M.L, 0)[0], G + 4, "300", 1.8)
    s.t(f(M.XT + 750, 0)[0], f(0, M.H)[1] - 4, "П3 — шкаф под специи", 2.6, weight="bold")
    s.t(f(M.XT + 750, 0)[0], f(0, M.H)[1] - 0.8, "без фасада, М 1:15", 2.2)


def detail_section_tall(s, X, G, k=1 / 15):
    f = lambda y, z: (X + y * k, G - z * k)
    R = lambda y0, z0, y1, z1, **kw: s.rc(*f(y0, z0), *f(y1, z1), **kw)
    s.ln(*f(0, 0), *f(0, M.H), 0.5)
    R(0, M.PL, M.DTALL, M.PL + M.T, fill="url(#hatch)", stroke="#111", w=0.2)
    R(0, M.ZU1 - M.T, M.DTALL, M.ZU1, fill="url(#hatch)", stroke="#111", w=0.2)
    for z in (1760, 2150):
        R(20, z, M.DTALL - 20, z + M.T, fill="url(#hatch)", stroke="#111", w=0.2)
    for z0, z1 in M.INNER:
        R(40, z0, M.DTALL - 50, z1, fill="#5f6368", stroke="#222", w=0.15)
        R(M.DTALL - 70, z0, M.DTALL - 50, z1 + 10, fill="#7b8086", stroke="#222", w=0.1)
    R(M.DTALL + 3, M.PL + 3, M.DTALL + 22, M.ZU1 - 3, fill="url(#veneer)", stroke="#111", w=0.2)
    R(0, M.ZU1, M.DTALL, M.ZA1, fill="none", stroke="#111", w=0.2)
    R(M.DTALL + 3, M.ZU1 + 3, M.DTALL + 22, M.H - 3, fill="url(#veneer)", stroke="#111", w=0.2)
    dim_h(s, f(0, 0)[0], f(M.DTALL + 22, 0)[0], G + 4, "602", 1.8)
    s.t(f(300, 0)[0], f(0, M.H)[1] - 4, "разрез П3", 2.4, weight="bold")
    s.t(f(300, 0)[0], f(0, M.H)[1] - 0.8, "М 1:15", 2.2)


def detail_oven(s, X, G, k=1 / 10):
    x0, x1 = M.X0 + 1050, M.X0 + 1650
    f = lambda x, z: (X + (x - x0) * k, G - (z - M.PL) * k)
    R = lambda a, b, c, d, **kw: s.rc(*f(a, b), *f(c, d), **kw)
    for p in M.PARTS:
        if p["group"] == "Н3":
            R(p["x0"], p["z0"], p["x1"], p["z1"], fill="#e9e9e6", stroke="#111", w=0.2)
    for fa in M.FACADES:
        if fa["module"] == "Н3":
            R(fa["x0"], fa["z0"], fa["x1"], fa["z1"], fill="#fff", stroke="#111", w=0.25)
    ov = ctx("Духовой")[0]
    R(ov["x0"], ov["z0"], ov["x1"], ov["z1"], fill="#1f2022", stroke="#000", w=0.2)
    R(ov["x0"] + 50, ov["z0"] + 80, ov["x1"] - 50, ov["z1"] - 140, fill="#3a3d41", stroke="#555", w=0.1)
    R(x0, M.ZB, x1, M.ZB + M.CT, fill="#e6e3dc", stroke="#111", w=0.22)
    R(x0 + 30, M.ZB + M.CT, x1 - 30, M.ZB + M.CT + 6, fill="#222", stroke="none")
    s.ln(*f(x0, M.ZB - 15), *f(x1, M.ZB - 15), 1.0, "#444")
    s.ln(*f(x0, ov["z0"] - 16), *f(x1, ov["z0"] - 16), 1.0, "#444")
    xr = f(x1, 0)[0]
    zs = [M.PL, ov["z0"], ov["z1"], M.ZB, M.ZB + M.CT]
    for a, b in zip(zs, zs[1:]):
        dim_v(s, f(0, a)[1], f(0, b)[1], xr + 3, str(round(b - a)), 1.7, side=1.5)
    dim_h(s, f(x0, 0)[0], f(x1, 0)[0], G + 4, "600", 1.8)
    s.t(f((x0 + x1) / 2, 0)[0], f(0, M.ZB + M.CT)[1] - 6, "Н3 — духовка + варочная, М 1:10", 2.5, weight="bold")


def detail_gola(s, X, G, k=1 / 10):
    f = lambda y, z: (X + y * k, G - (z - M.PL) * k)
    R = lambda a, b, c, d, **kw: s.rc(*f(a, b), *f(c, d), **kw)
    s.ln(*f(0, M.PL), *f(0, M.ZB + 80), 0.5)
    R(0, M.PL, M.DB, M.PL + M.T, fill="url(#hatch)", stroke="#111", w=0.2)
    R(M.DB - 100, M.ZB - M.T, M.DB, M.ZB, fill="url(#hatch)", stroke="#111", w=0.2)
    R(0, M.ZB - M.T, 100, M.ZB, fill="url(#hatch)", stroke="#111", w=0.2)
    R(0, M.ZB, 600, M.ZB + M.CT, fill="#e6e3dc", stroke="#111", w=0.22)
    boxes = [(M.PL + M.T + 10, M.ZC - 40), (M.DR_MID[0] + 15, M.DR_MID[1] - 25), (M.DR_TOP[0] + 15, M.ZB - M.T - 20)]
    labels = ["MERIVOBOX E + BOXCAP — через C", "MERIVOBOX M — через C", "MERIVOBOX M — через L"]
    for (z0, z1), lab in zip(boxes, labels):
        R(30, z0, 530, z1, fill="#5f6368", stroke="#222", w=0.15)
        x, y = f(280, (z0 + z1) / 2)
        s.t(x, y + 0.8, lab, 1.9, fill="#fff")
    for z0, z1 in (M.DR_LOW, M.DR_MID, M.DR_TOP):
        R(M.DB + 3, z0, M.DB + 22, z1, fill="#fff", stroke="#111", w=0.25)
    for z in [M.ZB - 15, M.ZC + 16]:
        R(M.DB - 40, z - 13, M.DB, z + 13, fill="#888", stroke="#333", w=0.15)
    R(M.DB - 60, 0 + M.PL - 100, M.DB - 44, M.PL, fill="#ddd", stroke="#555", w=0.15)
    x, y = f(M.DB + 30, M.ZB - 15)
    s.t(x, y + 0.7, "Gola L", 1.9, "start")
    x, y = f(M.DB + 30, M.ZC + 16)
    s.t(x, y + 0.7, "Gola C", 1.9, "start")
    dim_h(s, f(0, 0)[0], f(600, 0)[0], G + 4, "600", 1.8)
    s.t(f(300, 0)[0], f(0, M.ZB + M.CT)[1] - 6, "Шкаф с ящиками Н2/Н5 — разрез, М 1:10", 2.5, weight="bold")


def sheet2():
    s = S()
    header(s, "Кухня — узлы", "Технические решения по пеналу специй, шкафу духовки и ящикам с Gola", 2)
    detail_spice(s, 22, 240)
    detail_section_tall(s, 55, 240)
    detail_oven(s, 120, 125)
    detail_gola(s, 120, 240)
    X, Y = 220, 40
    s.t(X, Y, "Технические решения", 3.2, "start", "bold")
    notes = [
        "П1 — холодильник",
        "• Боковины до пола, без дна и цоколя; видимые боковины — МДФ шпон ореха 19.",
        "• Ниша 912 под холодильник 900: зазоры по 6 мм — мало для двустворчатого (French door)",
        "  холодильника. Сверить по паспорту: нужны вентзазоры и открывание дверей > 90°.",
        "• Сверху антресоль 950 на AVENTOS HK top (2 фасада 472).",
        "",
        "Н3 — духовой шкаф + варочная",
        "• Корпус без задней стенки; полка под духовку на 219–235; ниша 595 по высоте.",
        "• Под духовкой — низкий ящик MERIVOBOX N, фасад 129; между ним и духовкой — Gola C.",
        "• Варочную и духовку проверить по совместимости (общий бренд / разнесённые провода).",
        "",
        "Н4 — посудомойка 600 (встраиваемая)",
        "• Без корпуса: фасад 597×729 крепится на дверь ПММ; под столешницей — пароизоляция.",
        "• Цоколь перед ПММ — с вырезом/сдвигом по паспорту машины.",
        "",
        "Н2/Н5 — ящики с Gola",
        "• 3 ящика, один профиль Gola C посередине. Нижний (фасад 348) — через C;",
        "  второй (173) стоит над C и открывается за нижний край через C;",
        "  верхний (173) — через Gola L под столешницей. Между верхними — зазор 3 мм.",
        "• MERIVOBOX NL 500 (корпус 560); высоты бортов — по конфигуратору Blum.",
        "",
        "Н7 — бутылочница 150 под столешницей",
        "• Карго 150 (бутылки), фасад эмаль 147×729 на карго; столешница до пеналов — 3800.",
        "• Над ней — открытая полка 150 шпон ореха (В8) и антресоль А4.",
        "",
        "П3 — шкаф под специи 300 (как на фото 3)",
        "• Система Blum SPACE TOWER: 6 внутренних ящиков MERIVOBOX + 2 полки сверху.",
        "• Дистанционные планки 16 мм по боковинам — ящики проходят мимо петель двери.",
        "• Дверь 297×2444 шпон, 5 петель CLIP top BLUMOTION, торцевая ручка массив ореха.",
        "",
        "П2 — стеклянный шкаф 600",
        "• Фасад алюм. рамка со стеклом 597×2444 (проверить макс. высоту у поставщика),",
        "  стеклянные полки 8 мм на держателях, LED-профили по бокам + датчик открывания.",
        "• Левая боковина видна над столешницей — МДФ 19 шпон ореха.",
        "",
        "Верх / антресоль / вытяжка",
        "• Верхние двери 1047: CLIP top + TIP-ON, 3 петли. Антресоль: AVENTOS HK top.",
        "• Над варочной — проём 600 до потолка под каминную вытяжку, на стене рейки шпон ореха.",
        "• Под верхними шкафами — LED-профиль, блок питания в антресоли.",
        "",
        "Фасады",
        "• Эмаль: покраска с двух сторон (по ТЗ), торцы — в цвет. Шпон: лак 2 стороны.",
        "• Видимые торцы пеналов и антресоли — МДФ 19 шпон ореха.",
    ]
    for i, txt in enumerate(notes):
        bold = txt and not txt.startswith(("•", " "))
        s.t(X, Y + 5.5 + i * 3.55, txt, 2.15, "start", "bold" if bold else "normal")
    s.save("kuhnya_list2.svg")


# ---------------------------------------------------------------- лист 3: спецификация
def sheet3():
    s = S()
    header(s, "Кухня — модули, фасады, фурнитура Blum", "Размеры фасадов: высота × ширина, зазоры 3 мм учтены", 3)
    X, Y = 12, 32
    s.t(X, Y, "Модули", 3.2, "start", "bold")
    for i, (code, name, x0, x1, z0, z1, d, mat) in enumerate(M.MODULES):
        y = Y + 4 + i * 3.6
        s.rc(X, y - 2.7, X + 150, y + 0.9, fill="#fff" if i % 2 else "#f5f5f5", stroke="none")
        s.t(X + 1, y, code, 2.0, "start", "bold")
        s.t(X + 9, y, name, 1.95, "start")
        s.t(X + 149, y, f"{round(x1-x0)}×{round(z1-z0)}" + (f"×{d}" if d else ""), 1.95, "end")
    X2, Y2 = 172, 32
    s.t(X2, Y2, "Фасады", 3.2, "start", "bold")
    kinds = {"door": "дверь", "drawer": "ящик", "cargo": "карго", "glass": "рамка+стекло", "dw": "на ПММ", "lift": "подъёмный"}
    mats = {M.ENAMEL: "эмаль белая", M.WALNUT: "шпон ореха", M.ALU: "алюминий"}
    rows = sorted(M.facade_spec().items(), key=lambda r: (r[0][0], -r[0][2], -r[0][3]))
    s.rc(X2, Y2 + 2, X2 + 108, Y2 + 7, fill="#eef1f4", stroke="#999", w=0.15)
    for c, h in zip((1, 28, 52, 82, 96), ("Материал", "Вид", "В × Ш", "Кол.", "м²")):
        s.t(X2 + c, Y2 + 5.6, h, 2.1, "start", "bold")
    area = {}
    n_tot = 0
    for i, ((mat, kind, h, w), n) in enumerate(rows):
        y = Y2 + 7 + 3.8 * (i + 1)
        a = h * w * n / 1e6
        area[mat] = area.get(mat, 0) + a
        n_tot += n
        s.rc(X2, y - 2.8, X2 + 108, y + 1, fill="#fff" if i % 2 else "#f5f5f5", stroke="none")
        for c, v in zip((1, 28, 52, 82, 96), (mats[mat], kinds[kind], f"{h} × {w}", n, f"{a:.2f}")):
            s.t(X2 + c, y, str(v), 1.95, "start")
    y = Y2 + 7 + 3.8 * (len(rows) + 1) + 4
    s.t(X2, y, f"Всего {n_tot} фасадов:", 2.2, "start", "bold")
    for j, (mat, a) in enumerate(area.items()):
        s.t(X2, y + 4 + j * 3.6, f"{mats[mat]}: {a:.2f} м²" + (" (покраска 2 стороны)" if mat == M.ENAMEL else ""), 2.1, "start")
    X3, Y3 = 290, 32
    s.t(X3, Y3, "Фурнитура Blum и комплектующие", 3.2, "start", "bold")
    n_lift = sum(1 for f in M.FACADES if f["kind"] == "lift")
    items = [
        ("MERIVOBOX E + BOXCAP, NL 500 — нижние ящики Н2, Н5", "2 шт."),
        ("MERIVOBOX M, NL 500 — верхние ящики Н2, Н5", "4 шт."),
        ("MERIVOBOX N, NL 500 — ящик под духовкой", "1 шт."),
        ("SPACE TOWER: внутр. ящики MERIVOBOX — П3", "6 шт."),
        ("CLIP top BLUMOTION 110° — нижние двери (Н1, Н6)", "6 шт."),
        ("CLIP top 110° + TIP-ON — верхние двери (6 × 3)", "18 + 6"),
        ("CLIP top BLUMOTION — дверь П3 (5) + А4 (2)", "7 шт."),
        ("AVENTOS HK top — антресоль", f"{n_lift} шт."),
        ("Петли для алюм. рамки — П2", "5 шт."),
        ("Бутылочница-карго 150 под столешницу — Н7", "1 шт."),
        ("Профиль Gola L", f"{(M.XT - M.X0) / 1000:.2f} м"),
        ("Профиль Gola C (Н2, Н5, Н3 — по 1)", "3 × 0,6 м"),
        ("Торцевая ручка массив ореха — П3", "1 шт."),
        ("Полки стекло 8 мм закал. + держатели — П2", "5 шт."),
        ("LED-профиль: П2 2 × 2,4 м; под верхом 3,1 м", "к-т"),
        ("Блоки питания 24 В, датчики двери/движения", "к-т"),
        ("Опоры цоколя + клипсы", "≈ 30 шт."),
        ("Столешница 38, иск. камень (напр. Corian)", f"{(M.XT - M.X0) / 1000:.2f} м"),
        ("Вытяжка каминная 600 + воздуховод", "1 к-т"),
        ("Рейки шпон ореха 40×20 (над вытяжкой)", "10 шт."),
        ("Шина навеса / навесы для верхних шкафов", "по длине"),
    ]
    for i, (a, b) in enumerate(items):
        y = Y3 + 6 + i * 4.2
        s.rc(X3, y - 3, X3 + 118, y + 1.1, fill="#fff" if i % 2 else "#f5f5f5", stroke="#e3e3e3", w=0.1)
        s.t(X3 + 1.5, y, a, 2.0, "start")
        s.t(X3 + 116.5, y, b, 2.0, "end", "bold")
    ar = {}
    for (nm, mt, a, b, t), n in M.spec().items():
        ar[mt] = ar.get(mt, 0) + a * b * n / 1e6
    y = Y3 + 6 + len(items) * 4.2 + 5
    s.t(X3, y, "Корпуса", 3.0, "start", "bold")
    for j, (mt, a) in enumerate(ar.items()):
        s.t(X3, y + 4.5 + j * 3.8, f"{mt}: {a:.1f} м² ≈ {math.ceil(a * 1.2 / 5.8)} лист. 2800×2070", 2.1, "start")
    s.t(X3, y + 4.5 + len(ar) * 3.8, "Задние стенки — ХДФ 3 мм (кроме Н3, Н6).", 2.1, "start")
    s.save("kuhnya_list3.svg")




# ---------------------------------------------------------------- лист 4: аксонометрия с выносками
A1, A2, B1, B2 = math.cos(math.radians(12)), math.sin(math.radians(12)), 0.6 * math.cos(math.radians(40)), 0.6 * math.sin(math.radians(40))
VIEW = (B1, A1, A2 * B1 + B2 * A1)


def axo():
    s = S()
    header(s, "Кухня — вид сбоку (аксонометрия): материалы и глубины",
           "Как на примере заказчика: видно глубины пеналов, нижнего и верхнего ряда  |  Размеры в мм, без масштаба", 2)
    raw = lambda x, y, z: (x * A1 - y * B1, x * A2 + y * B2 - z)
    pts = [raw(x, y, z) for x in (0, M.L + 500) for y in (0, M.DFR + 200) for z in (0, M.H)]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    k = min(245 / (max(xs) - min(xs)), 262 / (max(ys) - min(ys)))
    OX, OY = 78 - min(xs) * k, 38 - min(ys) * k

    def P(x, y, z):
        return OX + (x * A1 - y * B1) * k, OY + (x * A2 + y * B2 - z) * k

    def poly(pts, fill, stroke="#222", w=0.18, extra=""):
        s.e('<path d="M' + "L".join(f"{a:.2f} {b:.2f}" for a, b in pts) + f'Z" fill="{fill}" stroke="{stroke}" stroke-width="{w}" {extra}/>')

    items = []     # (глубина, функция рисования)

    def boxi(x0, x1, y0, y1, z0, z1, fill, front=None, side=None, top=None, extra=None):
        def draw():
            poly([P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)], front or fill)
            poly([P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1)], side or fill)
            poly([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)], top or fill)
            if extra:
                extra()
        c = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
        items.append((c[0] * VIEW[0] + c[1] * VIEW[1] + c[2] * VIEW[2] + (x1 - x0) * 0.0, draw))

    WN_F, WN_S, WN_T = "url(#veneer)", "#7a5133", "#9c6d48"
    EN_F, EN_S, EN_T = "#ffffff", "#e9e9e6", "#f4f4f2"

    def facades_of(codes, yf):
        def f():
            for fa in M.FACADES:
                if fa["module"] in codes:
                    pts = [P(fa["x0"], yf, fa["z0"]), P(fa["x1"], yf, fa["z0"]), P(fa["x1"], yf, fa["z1"]), P(fa["x0"], yf, fa["z1"])]
                    if fa["kind"] == "glass":
                        poly(pts, "#b0b4b8", "#222", 0.2)
                        inner = [P(fa["x0"] + 25, yf, fa["z0"] + 25), P(fa["x1"] - 25, yf, fa["z0"] + 25),
                                 P(fa["x1"] - 25, yf, fa["z1"] - 25), P(fa["x0"] + 25, yf, fa["z1"] - 25)]
                        poly(inner, "url(#glass)", "#777", 0.12)
                        for zz in range(400, 2500, 400):
                            s.ln(*P(fa["x0"] + 25, yf, zz), *P(fa["x1"] - 25, yf, zz), 0.25, "#5b93a8")
                    else:
                        poly(pts, WN_F if fa["mat"] == M.WALNUT else EN_F, "#222", 0.18)
                        if fa["mat"] == M.WALNUT and fa["z1"] - fa["z0"] > 2000:
                            poly([P(fa["x0"], yf + 2, fa["z0"] + 900), P(fa["x0"] + 20, yf + 2, fa["z0"] + 900),
                                  P(fa["x0"] + 20, yf + 2, fa["z0"] + 1700), P(fa["x0"], yf + 2, fa["z0"] + 1700)], "#4a2f1a", "#2b1a0e", 0.1)
        return f

    # стена и пол
    poly([P(0, 0, 0), P(M.L, 0, 0), P(M.L, 0, M.H), P(0, 0, M.H)], "#f6f4f0", "#ccc", 0.15)
    poly([P(0, 0, 0), P(M.L, 0, 0), P(M.L + 300, 1100, 0), P(-300, 1100, 0)], "#efebe4", "none", 0)
    # холодильник и пенал под него
    fr = ctx("Холодильник")[0]
    boxi(fr["x0"], fr["x1"], fr["y0"], fr["y1"], 0, fr["z1"], "#2b2d30", side="#1d1f21", top="#3a3c3f")
    boxi(0, M.FD, 0, M.DFR, 0, M.ZU1, WN_F, side=WN_S, top=WN_T)
    boxi(M.X0 - M.FD, M.X0, 0, M.DFR, 0, M.ZU1, WN_F, side=WN_S, top=WN_T)
    boxi(M.FD, M.X0 - M.FD, 0, M.DFR, M.ZFR, M.ZU1, WN_S, front=WN_F, top=WN_T, extra=facades_of({"П1"}, M.DFR + 22.5))
    # нижний ряд
    boxi(M.X0, M.XT, M.DB - 60, M.DB - 44, 0, M.PL, "#e6e6e3")
    for code, name, x0, x1, z0, z1, d, mat in M.MODULES:
        if code.startswith("Н"):
            boxi(x0, x1, 0, M.DB + 22, M.PL, M.ZB, EN_S, front=EN_F, extra=facades_of({code}, M.DB + 22.5))
    ov = ctx("Духовой")[0]
    items.append((1e6 - 3, lambda: poly([P(ov["x0"], M.DB + 23, ov["z0"]), P(ov["x1"], M.DB + 23, ov["z0"]),
                                          P(ov["x1"], M.DB + 23, ov["z1"]), P(ov["x0"], M.DB + 23, ov["z1"])], "#1f2022", "#000", 0.2)))
    boxi(M.X0, M.XT, 0, 600, M.ZB, M.ZB + M.CT, "#e3e0d9", top="#efede8", side="#d6d2ca")
    hb = ctx("Варочная")[0]
    sk = ctx("Мойка")[0]
    items.append((1e6 - 2, lambda: (poly([P(hb["x0"], hb["y0"], 901), P(hb["x1"], hb["y0"], 901), P(hb["x1"], hb["y1"], 901), P(hb["x0"], hb["y1"], 901)], "#111", "#000", 0.15),
                                     poly([P(sk["x0"], sk["y0"], 901), P(sk["x1"], sk["y0"], 901), P(sk["x1"], sk["y1"], 901), P(sk["x0"], sk["y1"], 901)], "#c9ccce", "#666", 0.15))))
    # верх, антресоль, пеналы
    for code, name, x0, x1, z0, z1, d, mat in M.MODULES:
        if code[0] == "В" and d:
            if "Открытая" in name:
                boxi(x0, x1, 0, d, z0, z1, WN_F, side=WN_S, top=WN_T)
            else:
                boxi(x0, x1, 0, d + 22, z0, z1, EN_S, front=EN_F, top=EN_T, extra=facades_of({code}, d + 22.5))
        if code[0] == "А" or code in ("П2", "П3"):
            boxi(x0, x1, 0, d + 22, z0 if code[0] == "А" else 0, z1 if code[0] == "А" else z1, WN_S, front=WN_F, side=WN_S, top=WN_T,
                 extra=facades_of({code}, d + 22.5))
    hd = ctx("Вытяжка")[0]
    xc = (hd["x0"] + hd["x1"]) / 2
    def cylinder(cx, cy, r, z0, z1):
        def draw():
            ring = lambda z: [P(cx + r * math.cos(t / 24 * 2 * math.pi), cy + r * math.sin(t / 24 * 2 * math.pi), z) for t in range(24)]
            pts = sorted(set(ring(z0) + ring(z1)))
            def half(seq):
                h = []
                for p in seq:
                    while len(h) >= 2 and (h[-1][0] - h[-2][0]) * (p[1] - h[-2][1]) - (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0]) <= 0:
                        h.pop()
                    h.append(p)
                return h
            hull = half(pts)[:-1] + half(pts[::-1])[:-1]
            poly(hull, "url(#cyl)", "#000", 0.15)
            poly(ring(z1), "#3a3d41", "#000", 0.12)
        c = (cx, cy, (z0 + z1) / 2)
        items.append((c[0] * VIEW[0] + c[1] * VIEW[1] + c[2] * VIEW[2], draw))
    cylinder(xc, 250, 80, 2150, M.H)
    cylinder(xc, 250, 150, M.ZU0 + 40, 2160)
    items.append((1e6, lambda: poly([P(xc + 150 * math.cos(t / 24 * 2 * math.pi), 250 + 150 * math.sin(t / 24 * 2 * math.pi), M.ZU0 + 40)
                                     for t in range(24)], "#f5c518", "#b8901a", 0.1)))
    for _, draw in sorted(items, key=lambda t: t[0]):
        draw()
    # Gola на фасадной плоскости нижнего ряда
    yG = M.DB + 23
    s.ln(*P(M.X0, yG, M.ZB - 15), *P(M.XT, yG, M.ZB - 15), 0.7, "#444")
    for code in ("Н2", "Н5", "Н3"):
        x0, x1 = [(m[2], m[3]) for m in M.MODULES if m[0] == code][0]
        z = M.ZC + 16 if code != "Н3" else ctx("Духовой")[0]["z0"] - 16
        s.ln(*P(x0, yG, z), *P(x1, yG, z), 0.7, "#444")

    # размеры (красным): высоты справа, глубины
    def dim3(p0, p1, label, off=(0, 0), size=2.1):
        a, b = P(*p0), P(*p1)
        s.ln(*a, *b, 0.18, RED)
        for q in (a, b):
            s.e(f'<circle cx="{q[0]:.2f}" cy="{q[1]:.2f}" r="0.45" fill="{RED}"/>')
        s.t((a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1], label, size, fill=RED, weight="bold")

    xr, yr = M.L + 450, M.DTALL + 22
    lv = [0, M.PL, M.ZB + M.CT, M.ZU0, M.ZU1, M.H]
    for z0, z1 in zip(lv, lv[1:]):
        dim3((xr, yr, z0), (xr, yr, z1), str(z1 - z0), (4, 1))
    dim3((xr + 450, yr, 0), (xr + 450, yr, M.H), "3000", (5, 1))
    dim3((M.L, 0, -40), (M.L, M.DTALL + 22, -40), "602", (-1, 5), 2.4)
    dim3((M.X0 + 40, 0, M.ZB + M.CT + 5), (M.X0 + 40, 600, M.ZB + M.CT + 5), "600", (-4, 2), 2.4)
    dim3((M.X0 + 1060, 0, M.ZU0 - 20), (M.X0 + 1060, M.DU + 22, M.ZU0 - 20), "372", (2.5, 3.5), 2.4)
    dim3((M.X0 + 10, 0, 1200), (M.X0 + 10, M.DFR, 1200), "700", (-4, 2.5), 2.4)
    dim3((0, M.DFR + 22 + 150, 0), (M.L, M.DFR + 22 + 150, 0), f"{M.L}", (0, 6), 2.5)
    X, Y = 330, 250
    s.t(X, Y, "Глубины (красным)", 2.8, "start", "bold")
    for i, txt in enumerate(["700 — пенал под холодильник (без фасада)", "600 — столешница (корпус 560 + фасад 22)",
                             "372 — верхние шкафы (корпус 350 + фасад)", "602 — стеклянный шкаф и шкаф под специи",
                             "Антресоль — по глубине того, что под ней"]):
        s.t(X, Y + 4.5 + i * 3.6, txt, 2.15, "start")

    # выноски
    def callout(pt, tx, ty, lines, anchor="start"):
        a = P(*pt)
        s.ln(*a, tx, ty, 0.2, "#333")
        s.e(f'<circle cx="{a[0]:.2f}" cy="{a[1]:.2f}" r="0.6" fill="#333"/>')
        for i, l in enumerate(lines):
            s.t(tx + (1 if anchor == "start" else -1), ty - 1 + i * 3.2, l, 2.3, anchor, "bold" if i == 0 else "normal")
        s.ln(tx, ty + 0.5, tx + (40 if tx > 100 else 30), ty + 0.5, 0.2, "#333")

    L_, R_ = 18, 322
    callout((2900, M.DU + 22, 2000), R_, 40, ["Фасады МДФ в эмали, белый", "покраска с двух сторон"])
    callout((xc, 260, 2400), R_, 56, ["Вытяжка-цилиндр Ø300, чёрная", "LED-кольцо, труба до потолка"])
    callout((M.XT + 300, M.DTALL + 22, 1900), R_, 72, ["Стеклянный шкаф 600:", "алюм. рамка + стекло, LED"])
    callout((M.XT + 610, M.DTALL + 22, 1300), R_, 88, ["Торцевая ручка", "массив ореха"])
    callout((M.XT + 750, M.DTALL + 22, 700), R_, 104, ["Шкаф под специи 300:", "Blum SPACE TOWER, 6 ящиков"])
    callout((M.XT - 75, M.DB + 22, 500), R_, 120, ["Бутылочница 150", "под столешницей"])
    callout((3300, 300, 900), R_, 136, ["Столешница — иск. камень", "(напр. Corian), 38 мм"])
    callout((300, M.DFR + 22, 2780), L_, 48, ["Антресоль и пеналы —", "МДФ шпон ам. ореха"])
    callout((M.X0 / 2, M.DFR, 1400), L_, 110, ["Холодильник", "отдельностоящий;", "пенал без дна"])
    callout((1700, M.DB + 23, M.ZC + 16), L_, 200, ["Gola L + C", "ящики Blum", "MERIVOBOX"])
    s.save("kuhnya_list2.svg")


if __name__ == "__main__":
    assert M.check() == 0
    sheet1()
    axo()
