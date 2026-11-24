#!/usr/bin/env python3
"""Листы А3 кухни: 1 — развёртка по стене, план, разрез (1:20); 2 — 3D, модули, фасады, фурнитура."""
import base64
import math
import os

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "DejaVu Sans, Arial, sans-serif"
RED = "#c0392b"
K = 1 / 20


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
                '<rect width="3" height="3" fill="#e4f1f6"/><line x1="0" y1="0" x2="0" y2="3" stroke="#9cc3d2" stroke-width="0.25"/></pattern></defs>')
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


def header(s, title, sub, n):
    s.t(12, 15, title, 5.6, "start", "bold")
    s.t(12, 21.5, sub, 2.9, "start")
    s.t(408, 15, f"Лист {n}/2", 3.2, "end")


def tag(s, x, y, code):
    s.e(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.4" fill="#fff" stroke="#1f4e79" stroke-width="0.25"/>')
    s.t(x, y + 0.85, code, 1.9, weight="bold", fill="#1f4e79")


# ---------------------------------------------------------------- развёртка
def elevation(s, X, G):
    f = lambda x, z: (X + x * K, G - z * K)
    R = lambda x0, z0, x1, z1, **kw: s.rc(*f(x0, z0), *f(x1, z1), **kw)
    R(0, 0, M.L, M.H, fill="#f7f5f1", stroke="#bbb", w=0.15)                 # стена
    s.ln(*f(-150, M.H), *f(M.L + 150, M.H), 0.3, "#777", "2 1")                # потолок
    s.ln(*f(-150, 0), *f(M.L + 150, 0), 0.4)                                    # пол
    # корпуса без фасадов: пенал под холодильник
    for p in M.PARTS:
        if p["group"] == "П1" and p["name"] == "Боковина":
            R(p["x0"], p["z0"], p["x1"], p["z1"], fill="#e9e9e6", stroke="#111", w=0.2)
        if p["group"] == "П1" and p["name"] == "Крышка":
            R(p["x0"], p["z0"], p["x1"], p["z1"], fill="#e9e9e6", stroke="#111", w=0.2)
    fr = M.CONTEXT[0]
    R(fr["x0"], fr["z0"], fr["x1"], fr["z1"], fill="none", stroke="#777", w=0.2, dash="1.5 1")
    x, y = f(475, 1000)
    s.t(x, y, "холодильник 900", 2.2, fill="#666")
    s.t(x, y + 3, "(отдельностоящий)", 1.9, fill="#666")
    # цоколь, столешница
    R(M.X0, 0, M.XT, M.PL, fill="#dedcd8", stroke="#888", w=0.15)
    R(M.XT, 0, M.L, M.PL, fill="#dedcd8", stroke="#888", w=0.15)
    R(M.X0, M.ZB, M.XT, M.ZB + M.CT, fill="#8c8378", stroke="#111", w=0.2)
    s.ln(*f(M.X0, M.ZB - 15), *f(M.XT, M.ZB - 15), 0.9, "#555")              # профиль Gola L
    # фасады
    for fa in M.FACADES:
        if fa["kind"] == "glass":
            R(fa["x0"], fa["z0"], fa["x1"], fa["z1"], fill="#b0b4b8", stroke="#111", w=0.25)
            R(fa["x0"] + 20, fa["z0"] + 20, fa["x1"] - 20, fa["z1"] - 20, fill="url(#glass)", stroke="#777", w=0.15)
            continue
        R(fa["x0"], fa["z0"], fa["x1"], fa["z1"], fill="#fff", stroke="#111", w=0.22)
        if fa["kind"] == "drawer" and fa["z1"] < 700:
            s.ln(*f(fa["x0"], fa["z1"] + 16), *f(fa["x1"], fa["z1"] + 16), 0.9, "#555")   # профиль Gola C
        if fa["kind"] == "door" and fa["module"].startswith(("Н", "В", "А")):
            # направление открывания — тонкие линии к петлям (левые петли у чётных)
            pass
    # стеклянные полки и подсветка в пенале-витрине
    for p in M.PARTS:
        if p["name"].startswith("Полка стеклянная"):
            s.ln(*f(p["x0"], (p["z0"] + p["z1"]) / 2), *f(p["x1"], (p["z0"] + p["z1"]) / 2), 0.3, "#5b93a8")
        if p["name"].startswith("Профиль LED"):
            R(p["x0"], p["z0"], p["x1"], p["z1"], fill="#f5c518", stroke="none")
    # карго — пунктир корзин
    for fa in M.FACADES:
        if fa["kind"] == "cargo":
            n = 6 if fa["z1"] > 1500 else 2
            for i in range(1, n + 1):
                z = fa["z0"] + (fa["z1"] - fa["z0"]) * i / (n + 1)
                s.ln(*f(fa["x0"] + 15, z), *f(fa["x1"] - 15, z), 0.2, "#777", "1 0.8")
    # вытяжка (за фасадом)
    hood = M.CONTEXT[3]
    R(hood["x0"], hood["z0"] + 1, hood["x1"], hood["z0"] + 60, fill="none", stroke="#777", w=0.2, dash="1.5 1")
    x, y = f((hood["x0"] + hood["x1"]) / 2, hood["z0"] + 200)
    s.t(x, y, "встраиваемая", 1.8, fill="#666")
    s.t(x, y + 2.4, "вытяжка 600", 1.8, fill="#666")
    # коды модулей
    for code, name, x0, x1, z0, z1, d in M.MODULES:
        zc = {"П": 2250, "Н": 520, "В": 2050, "А": 2780}[code[0]]
        if code == "П1":
            zc = 2200
        tag(s, *f((x0 + x1) / 2, zc), code)
    # размеры: низ по модулям, верх по модулям, общий
    xs = [0, M.X0]
    x = M.X0
    for w, _ in M.BASE:
        x += w
        xs.append(x)
    xs += [M.XT + 600, M.L]
    for a, b in zip(xs, xs[1:]):
        dim_h(s, f(a, 0)[0], f(b, 0)[0], G + 5, str(b - a), 1.9)
    dim_h(s, f(0, 0)[0], f(M.L, 0)[0], G + 10, "5500", 2.5)
    xu = [M.X0]
    x = M.X0
    for w, _ in M.UPPER:
        x += w
        xu.append(x)
    for a, b in zip(xu, xu[1:]):
        dim_h(s, f(a, 0)[0], f(b, 0)[0], f(0, M.H)[1] - 4, str(b - a), 1.9)
    xr = f(M.L, 0)[0]
    lv = [0, M.PL, M.ZB + M.CT, M.ZU0, M.ZU1, M.H]
    for z0, z1 in zip(lv, lv[1:]):
        dim_v(s, f(0, z0)[1], f(0, z1)[1], xr + 5, str(z1 - z0), 1.9, side=1.6)
    dim_v(s, f(0, 0)[1], f(0, M.H)[1], X - 5, "3000", 2.4)
    s.t(X + M.L * K / 2, f(0, M.H)[1] - 9, "РАЗВЁРТКА ПО СТЕНЕ  М 1:20", 3, weight="bold")
    # разрез
    for z, d in ((M.H + 80, -0.6), (-80, 3.2)):
        x, y = f(1600, z)
        s.t(x - 2.5, y + d, "А", 2.8, weight="bold")
    s.ln(*f(1600, M.H + 60), *f(1600, M.H - 50), 0.5)
    s.ln(*f(1600, 40), *f(1600, -60), 0.5)


def plan(s, X, Yw):
    """Вид сверху: стена — сверху (Yw), фасады — вниз."""
    f = lambda x, y: (X + x * K, Yw + y * K)
    R = lambda x0, y0, x1, y1, **kw: s.rc(*f(x0, y0), *f(x1, y1), **kw)
    s.ln(*f(-150, 0), *f(M.L + 150, 0), 0.5)
    R(0, 0, M.X0, M.DFR, fill="#e9e9e6", stroke="#111", w=0.2)
    fr = M.CONTEXT[0]
    R(fr["x0"], fr["y0"], fr["x1"], fr["y1"], fill="none", stroke="#777", w=0.2, dash="1.5 1")
    R(M.X0, 0, M.XT, 600, fill="#cfc8bd", stroke="#111", w=0.2)
    for c in M.CONTEXT[1:3]:
        R(c["x0"], c["y0"], c["x1"], c["y1"], fill="#333" if "Вароч" in c["name"] else "#b9bcbf", stroke="#111", w=0.15, rx=0.6)
    R(M.XT, 0, M.L, M.DTALL + 22, fill="#e9e9e6", stroke="#111", w=0.2)
    s.ln(*f(M.XT + 600, 0), *f(M.XT + 600, M.DTALL + 22), 0.2)
    s.ln(*f(M.X0, M.DU + 22), *f(M.XT, M.DU + 22), 0.25, "#111", "2 1")
    x, y = f(3300, M.DU + 22)
    s.t(x, y - 1, "верхний ряд (пунктир)", 1.8, fill="#555")
    for xx, txt in ((475, "П1"), (2300, "варочная"), (4200, "мойка"), (5050, "П2"), (5425, "П3")):
        x, y = f(xx, 380 if txt.startswith("П") else 640)
        s.t(x, y + (4 if not txt.startswith("П") else 0), txt, 1.9, fill="#333")
    dim_v(s, f(0, 0)[1], f(0, M.DFR)[1], X - 4, "700", 1.9)
    dim_v(s, f(0, 0)[1], f(0, 600)[1], f(M.L, 0)[0] + 4, "600", 1.9, side=1.6)
    s.t(X + M.L * K / 2, Yw - 3, "ПЛАН  М 1:20", 3, weight="bold")


def section(s, X, G, xc=1600):
    f = lambda y, z: (X + y * K, G - z * K)
    R = lambda y0, z0, y1, z1, **kw: s.rc(*f(y0, z0), *f(y1, z1), **kw)
    s.ln(*f(0, -50), *f(0, M.H + 50), 0.5)
    s.ln(*f(-50, 0), *f(800, 0), 0.4)
    for p in M.PARTS:
        if p["x0"] < xc < p["x1"]:
            R(p["y0"], p["z0"], p["y1"], p["z1"], fill="url(#hatch)", stroke="#111", w=0.2)
        elif p["group"] in ("Н2", "В2", "А3") and p["name"] == "Боковина" and p["x0"] > xc:
            R(p["y0"], p["z0"], p["y1"], p["z1"], fill="#f1f1ef", stroke="#999", w=0.12)
    for p in M.PARTS:
        if p["x0"] < xc < p["x1"]:
            R(p["y0"], p["z0"], p["y1"], p["z1"], fill="url(#hatch)", stroke="#111", w=0.2)
    for fa in M.FACADES:
        if fa["x0"] < xc < fa["x1"]:
            R(fa["y"], fa["z0"], fa["y"] + M.FD, fa["z1"], fill="#fff", stroke="#111", w=0.25)
    # Gola: L под столешницей, C между ящиками
    for z in [M.ZB - 15] + [fa["z1"] + 16 for fa in M.FACADES if fa["module"] == "Н2" and fa["z1"] < 700]:
        R(M.DB - 40, z - 12, M.DB, z + 12, fill="#888", stroke="#333", w=0.15)
    lv = [0, M.PL, M.ZB + M.CT, M.ZU0, M.ZU1, M.H]
    for z0, z1 in zip(lv, lv[1:]):
        dim_v(s, f(0, z0)[1], f(0, z1)[1], X - 4, str(z1 - z0), 1.8)
    dim_h(s, f(0, 0)[0], f(600, 0)[0], G + 4.5, "600", 1.8)
    dim_h(s, f(0, M.H)[0], f(M.DU + 22, 0)[0], f(0, M.H)[1] - 3, "372", 1.8)
    s.t(X + 380 * K, f(0, M.H)[1] - 8, "РАЗРЕЗ А–А  М 1:20", 2.8, weight="bold")


def sheet1():
    s = S()
    header(s, "Кухня 5500 × 3000 — развёртка, план, разрез",
           "Фасады МДФ 19 эмаль белая, ручка Gola  |  Корпуса ЛДСП 16 белый  |  Столешница 38 на высоте 900  |  Размеры в мм", 1)
    elevation(s, 22, 205)
    plan(s, 22, 235)
    section(s, 345, 205)
    X, Y = 328, 232
    s.t(X, Y, "Примечания", 3.0, "start", "bold")
    for i, txt in enumerate([
        "• Н-нижние, В-верхние, А-антресоли, П-пеналы.",
        "• П1: без дна, боковины до пола; ширина ниши",
        "  918 под холодильник 900 — сверить по модели.",
        "• П2: стеклянные полки 8 мм, LED по бокам,",
        "  фасад — алюм. рамка со стеклом на 5 петлях.",
        "• П3: высокое карго 150 за фасадом (крупы).",
        "• В3: шкаф под встраиваемую вытяжку 600,",
        "  без дна; воздуховод через А4 в вентканал.",
        "• Верх и пеналы — открывание push (TIP-ON).",
    ]):
        s.t(X, Y + 4.8 + i * 3.4, txt, 2.1, "start")
    s.save("kuhnya_list1.svg")


# ---------------------------------------------------------------- лист 2
def sheet2():
    s = S()
    header(s, "Кухня — 3D, модули, фасады, фурнитура", "Размеры фасадов: высота × ширина, зазоры 3 мм учтены", 2)
    for i, (v, cap) in enumerate((("persp", "Общий вид"), ("open", "Без фасадов: корпуса и наполнение"))):
        b64 = base64.b64encode(open(os.path.join(HERE, f"3d_{v}.png"), "rb").read()).decode()
        x = 12 + i * 133
        s.e(f'<image x="{x}" y="27" width="128" height="83.2" href="data:image/png;base64,{b64}"/>')
        s.rc(x, 27, x + 128, 110.2, stroke="#ccc")
        s.t(x + 64, 114, cap, 2.5)
    # модули
    X, Y = 12, 123
    s.t(X, Y, "Модули (корпуса ЛДСП 16 белый)", 3.2, "start", "bold")
    Y += 2.5
    for i, (code, name, x0, x1, z0, z1, d) in enumerate(M.MODULES):
        y = Y + 3.6 + i * 3.6
        s.rc(X, y - 2.7, X + 128, y + 0.9, fill="#fff" if i % 2 else "#f7f7f7", stroke="none")
        s.t(X + 1, y, code, 2.0, "start", "bold")
        s.t(X + 10, y, name, 2.0, "start")
        s.t(X + 127, y, f"{round(x1-x0)}×{round(z1-z0)}×{d}", 2.0, "end")
    # фасады
    X2, Y2 = 145, 123
    s.t(X2, Y2, "Фасады (заказ в покраску)", 3.2, "start", "bold")
    kinds = {"door": "дверь", "drawer": "ящик", "cargo": "карго", "glass": "алюм. рамка + стекло"}
    rows = sorted(M.facade_spec().items(), key=lambda r: (r[0][0], -r[0][2], -r[0][3]))
    s.rc(X2, Y2 + 2, X2 + 128, Y2 + 7, fill="#eef1f4", stroke="#999", w=0.15)
    for c, h in zip((1, 40, 70, 100, 118), ("Материал", "Вид", "В × Ш, мм", "Кол.", "м²")):
        s.t(X2 + c, Y2 + 5.6, h, 2.1, "start", "bold")
    tot, n_tot = 0, 0
    for i, ((mat, kind, h, w), n) in enumerate(rows):
        y = Y2 + 7 + 3.9 * (i + 1)
        a = h * w * n / 1e6
        tot += a if mat == M.MDF else 0
        n_tot += n
        s.rc(X2, y - 2.9, X2 + 128, y + 1, fill="#fff" if i % 2 else "#f7f7f7", stroke="none")
        for c, v in zip((1, 40, 70, 100, 118), ("МДФ 19 эмаль" if mat == M.MDF else "алюминий", kinds[kind], f"{h} × {w}", n, f"{a:.2f}")):
            s.t(X2 + c, y, str(v), 2.0, "start")
    y = Y2 + 7 + 3.9 * (len(rows) + 1) + 4
    s.t(X2, y, f"Итого: {n_tot} фасадов, МДФ эмаль {tot:.1f} м² (белый, матовый/глянец — уточнить)", 2.2, "start", "bold")
    # фурнитура
    X3, Y3 = 280, 27
    s.t(X3, Y3, "Фурнитура и комплектующие", 3.2, "start", "bold")
    n_doors = sum(1 for f in M.FACADES if f["kind"] in ("door",))
    items = [
        ("Профиль Gola L (под столешницей)", "3,8 м"),
        ("Профиль Gola C (между ящиками)", "4 × 0,6 м"),
        ("Ящики полного выдвижения, 500 мм (Blum/Hettich)", "6 шт."),
        ("Карго нижнее 150, 2 корзины", "1 шт."),
        ("Карго высокое 150, 5–6 корзин, h ≈ 2000", "1 шт."),
        ("Петли с доводчиком / под push (по 2–3 на дверь)", f"≈ {n_doors * 2 + 8} шт."),
        ("Толкатели push-to-open (верх, антресоль, пеналы)", "≈ 22 шт."),
        ("Фасад алюм. рамка 20 мм + стекло, 597 × 2444", "1 шт."),
        ("Петли для алюм. рамки", "5 шт."),
        ("Полки стекло 8 мм закалённое, с полировкой", "5 шт."),
        ("Профиль LED вертикальный + лента 24 В", "2 × 2,4 м"),
        ("Блок питания 24 В + датчик открывания двери", "1 к-т"),
        ("Опоры цоколя регулируемые 100 + клипсы", "≈ 30 шт."),
        ("Цоколь белый 100", "4,6 м"),
        ("Столешница 38 × 600 (материал по выбору)", "3,8 м"),
        ("Встраиваемая вытяжка 600 + воздуховод", "1 к-т"),
        ("Кронштейны/шина навеса верхних шкафов", "по длине"),
    ]
    for i, (a, b) in enumerate(items):
        y = Y3 + 6 + i * 4.3
        s.rc(X3, y - 3.1, X3 + 128, y + 1.1, fill="#fff" if i % 2 else "#f7f7f7", stroke="#e3e3e3", w=0.1)
        s.t(X3 + 1.5, y, a, 2.1, "start")
        s.t(X3 + 126.5, y, b, 2.1, "end", "bold")
    ar = sum(size[0] * size[1] * n for (nm, mt, *size), n in [((k[0], k[1], k[2], k[3], k[4]), v) for k, v in M.spec().items()]) / 1e6
    y = Y3 + 6 + len(items) * 4.3 + 4
    s.t(X3, y, f"Корпуса ЛДСП 16 белый: {ar:.1f} м² ≈ {math.ceil(ar * 1.2 / 5.8)} листов 2800×2070", 2.3, "start", "bold")
    s.t(X3, y + 4, "Задние стенки — ХДФ 3 мм белый (≈ 13 м²).", 2.2, "start")
    s.save("kuhnya_list2.svg")


if __name__ == "__main__":
    assert M.check() == 0
    sheet1()
    sheet2()
