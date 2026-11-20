#!/usr/bin/env python3
"""Листы А3 шлифовального стола: 1 — вид спереди, вид сверху, разрез А–А (1:10); 2 — 3D, детали, фурнитура."""
import base64
import math
import os

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "DejaVu Sans, Arial, sans-serif"
RED = "#c0392b"
K = 1 / 10
LDSP_C, MDF_C = "#5b5f63", "#e2cfa9"


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
        defs = ('<defs><pattern id="hatch" width="1.2" height="1.2" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                '<rect width="1.2" height="1.2" fill="#fff"/><line x1="0" y1="0" x2="0" y2="1.2" stroke="#555" stroke-width="0.25"/></pattern></defs>')
        with open(os.path.join(HERE, name), "w") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">{defs}'
                    f'<rect width="{w}" height="{h}" fill="#fff"/>'
                    f'<rect x="5" y="5" width="{w-10}" height="{h-10}" fill="none" stroke="#111" stroke-width="0.4"/>'
                    f'{"".join(s.o)}</svg>')


def dim_h(s, x1, x2, y, label, size=2.3):
    s.ln(x1, y, x2, y, 0.15, RED)
    for x in (x1, x2):
        s.ln(x - 0.7, y + 0.7, x + 0.7, y - 0.7, 0.3, RED)
    s.t((x1 + x2) / 2, y - 0.8, label, size, fill=RED)


def dim_v(s, y1, y2, x, label, size=2.3, side=-1):
    s.ln(x, y1, x, y2, 0.15, RED)
    for y in (y1, y2):
        s.ln(x - 0.7, y + 0.7, x + 0.7, y - 0.7, 0.3, RED)
    s.t(x + side * 0.8, (y1 + y2) / 2, label, size, fill=RED, rot=-90)


def header(s, title, sub, n):
    s.t(12, 15, title, 5.6, "start", "bold")
    s.t(12, 21.5, sub, 2.9, "start")
    s.t(408, 15, f"Лист {n}/2", 3.2, "end")


# ---------------------------------------------------------------- лист 1
COL = {M.LDSP: LDSP_C, M.MDF16: MDF_C, M.MDF19: MDF_C}


def profile(p):
    """Контур детали в плоскости Y–Z (для разреза)."""
    if p["kind"] == "prism":
        return p["poly"]
    return [(p["y0"], p["z0"]), (p["y1"], p["z0"]), (p["y1"], p["z1"]), (p["y0"], p["z1"])]


def poly(s, pts, fill, stroke="#111", w=0.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    s.e('<path d="M' + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + f'Z" fill="{fill}" stroke="{stroke}" stroke-width="{w}"{d}/>')


def front_view(s, X, G, k):
    f = lambda x, z: (X + x * k, G - z * k)
    for x in (60, 936, 1864, M.L - 60):
        s.rc(*f(x - 25, 0), *f(x + 25, M.LEG), fill="#222", stroke="#000")
    for p in sorted(M.PARTS, key=lambda p: -p["y0"]):
        fill = COL[p["mat"]]
        if p["y0"] >= M.D - M.T - 1:
            fill = "#3c3f42" if p["mat"] == M.LDSP else fill
        s.rc(*f(p["x0"], p["z0"]), *f(p["x1"], p["z1"]), fill=fill, stroke="#111", w=0.15)
        if p["name"].startswith("Перфостенка"):
            for x, z in M.WALL_SLOTS:
                s.rc(*f(x - 15, z - 4), *f(x + 15, z + 4), fill="#3a2f22", stroke="none")
        if p["name"].startswith("Фасад камеры"):
            for t in M.FASCIA_ROWS:
                z = M.fascia_point(t)[1]
                for a, b in M.FRONT_SEG:
                    s.rc(*f(a, z - 5), *f(b, z + 5), fill="#3a2f22", stroke="none")
        if p["name"] == "Фасад ящика":
            xc = (p["x0"] + p["x1"]) / 2
            s.rc(*f(xc - 128, p["z1"] - 40), *f(xc + 128, p["z1"] - 26), fill="#9aa0a6", stroke="#555", w=0.1)
    s.ln(*f(M.T + 20, M.ZW - 4), *f(M.L - M.T - 20, M.ZW - 4), 0.6, "#f5c518")
    dim_h(s, f(0, 0)[0], f(M.L, 0)[0], G + 9, "2800", 2.6)
    for a, b in M.SEC:
        dim_h(s, f(a, 0)[0], f(b, 0)[0], G + 4.5, f"{b-a}", 2.0)
    xr = f(M.L, 0)[0]
    lv = [0, M.LEG, M.ZD + M.T, M.ZT, M.ZW, M.ZS]
    for z0, z1 in zip(lv, lv[1:]):
        dim_v(s, f(0, z0)[1], f(0, z1)[1], xr + 5, f"{z1-z0}", 2.1, side=1.8)
    dim_v(s, G, f(0, M.ZT)[1], xr + 11, "900", 2.3, side=1.8)
    dim_v(s, G, f(0, M.ZS)[1], X - 5, "1950", 2.5)
    s.t(X + M.L * k / 2, G - M.ZS * k - 4, "ВИД СПЕРЕДИ  М 1:15", 3, weight="bold")
    for z, tag, dy in ((M.ZS + 40, "А", -1), (-40, "А", 3.5)):
        x, y = f(700, z)
        s.t(x, y + dy, tag, 3, weight="bold")
    s.ln(*f(700, M.ZS + 20), *f(700, M.ZS - 80), 0.5)
    s.ln(*f(700, 20), *f(700, -30), 0.5)


def top_view(s, X, Yt, k):
    f = lambda x, y: (X + x * k, Yt + (M.D - y) * k)
    shelf = [p for p in M.PARTS if "стеллаж" in p["name"]]
    for p in sorted([p for p in M.PARTS if p not in shelf], key=lambda p: p["z1"]):
        s.rc(*f(p["x0"], p["y0"]), *f(p["x1"], p["y1"]), fill=COL[p["mat"]], stroke="#111", w=0.15)
    for x, y in M.TOP_SLOTS:
        s.rc(*f(x - 20, y - 5), *f(x + 20, y + 5), fill="#3a2f22", stroke="none")
    s.rc(*f(0, M.SH_Y), *f(M.L, M.D), stroke="#111", w=0.3, dash="2 1")
    x, y = f(M.L / 2, 600)
    s.t(x, y + 1, "стеллаж над (пунктир)", 2.2, fill="#fff", weight="bold")
    for xo in M.OUTLETS:
        s.rc(*f(xo - 80, M.D), *f(xo + 80, M.D + 80), fill="#c9cdd1", stroke="#555")
    dim_h(s, f(0, 0)[0], f(M.L, 0)[0], f(0, 0)[1] + 5, "2800", 2.3)
    dim_v(s, f(0, 0)[1], f(0, M.D)[1], X - 9, "700", 2.3)
    dim_v(s, f(0, 0)[1], f(0, M.YT)[1], X - 4.5, "450", 2.0)
    s.t(X + M.L * k / 2, Yt - 7, "ВИД СВЕРХУ  М 1:15", 3, weight="bold")


def section(s, X, G, k, xc=700):
    f = lambda y, z: (X + y * k, G - z * k)
    behind = sorted([p for p in M.PARTS if p["x0"] >= xc], key=lambda p: -p["x0"])
    for p in behind:
        if p["name"].startswith("Ребро"):
            zt = p["z1"] - 60
            for y0, y1, z0, z1 in ((p["y0"], p["y1"], zt, p["z1"]), (p["y0"], p["y0"] + 80, p["z0"], zt), (p["y1"] - 80, p["y1"], p["z0"], zt)):
                s.rc(*f(y0, z0), *f(y1, z1), fill="#d5d7d9", stroke="#888", w=0.12)
            continue
        if p["tag"] and p["tag"] != "drawer0":
            continue
        poly(s, [f(*q) for q in profile(p)], "#eceeef" if p["kind"] == "box" else "#f6f6f6", "#999", 0.12)
    for y in (60, M.D - 60):
        s.rc(*f(y - 25, 0), *f(y + 25, M.LEG), fill="#222", stroke="#000")
    for p in M.PARTS:
        if p["x0"] < xc < p["x1"]:
            poly(s, [f(*q) for q in profile(p)], "url(#hatch)", "#111", 0.25)
    s.rc(*f(M.D, M.OUT_Z - 80), *f(M.D + 90, M.OUT_Z + 80), fill="#c9cdd1", stroke="#555")
    s.ln(*f(M.SH_Y + 12, M.ZW - 4), *f(M.SH_Y + 32, M.ZW - 4), 0.9, "#f5c518")
    # поток воздуха
    def arrow(pts):
        s.e('<path d="M' + "L".join(f"{f(*q)[0]:.2f} {f(*q)[1]:.2f}" for q in pts) +
            '" stroke="#2e86de" stroke-width="0.45" fill="none" marker-end="url(#arr)"/>')
    s.e('<defs><marker id="arr" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto"><path d="M0 0 L4 2 L0 4Z" fill="#2e86de"/></marker></defs>')
    for y in (120, 260, 380):
        arrow([(y, M.ZT + 110), (y, M.ZT - 160)])
    arrow([(M.YT - 120, 1200), (M.YT + 90, 1200), (M.YT + 120, 1120)])
    arrow([(M.YT + 130, 1050), (M.YT + 130, 620), (M.D + 140, M.OUT_Z)])
    x, y = f(M.D + 100, M.OUT_Z - 60)
    s.t(x, y, "Ø160 → к", 1.9, "start", fill="#2e86de")
    s.t(x, y + 2.4, "пылесосу /", 1.9, "start", fill="#2e86de")
    s.t(x, y + 4.8, "аспирации", 1.9, "start", fill="#2e86de")
    dim_h(s, f(0, 0)[0], f(M.D, 0)[0], G + 9, "700", 2.3)
    dim_h(s, f(0, 0)[0], f(M.YT, 0)[0], G + 4.5, "450", 2.0)
    dim_h(s, f(M.YT, 0)[0], f(M.D, 0)[0], G + 4.5, "250", 2.0)
    dim_h(s, f(0, 0)[0], f(M.SH_Y, 0)[0], f(0, M.ZS)[1] - 3, "250", 2.0)
    dim_h(s, f(M.SH_Y, 0)[0], f(M.D, 0)[0], f(0, M.ZS)[1] - 3, "450", 2.0)
    dim_h(s, f(0, 0)[0], f(M.SLANT, 0)[0], f(0, M.ZD)[1] + 4, "84", 1.8)
    lv = [0, M.LEG, M.ZD + M.T, M.ZT, M.ZW, M.ZS]
    for z0, z1 in zip(lv, lv[1:]):
        dim_v(s, f(0, z0)[1], f(0, z1)[1], X - 4, f"{z1-z0}", 2.0)
    s.t(X + M.D * k / 2, f(0, M.ZS)[1] - 9, "РАЗРЕЗ А–А  М 1:10", 3, weight="bold")


def sheet1():
    s = S()
    header(s, "Стол шлифовальный 2800 × 700: камера вытяжки, выкатные ящики, стеллаж",
           "Столешница на 900, перфостенка 550, открытый стеллаж 500 со светом  |  ЛДСП 16 антрацит, МДФ 19 / МДФ 16  |  Размеры в мм", 1)
    front_view(s, 28, 172, 1 / 15)
    top_view(s, 28, 200, 1 / 15)
    section(s, 268, 262, 1 / 10)
    X, Y = 355, 40
    s.t(X, Y, "Как устроено", 3.2, "start", "bold")
    lines = [
        "Камера (пустота) под",
        "столешницей и за перфо-",
        "стенкой — единый объём.",
        "Пылесос / аспирация тянет",
        "воздух через 2 патрубка",
        "Ø160 сзади (высота 520).",
        "",
        "Воздух входит через:",
        f"• столешницу — {len(M.TOP_SLOTS)} прорезей",
        "  40×10;",
        f"• перфостенку — {len(M.WALL_SLOTS)} прорезей",
        "  30×8 (и под крючки);",
        "• наклонный фасад —",
        "  5 рядов прорезей.",
        "",
        "Внизу — 3 выкатных",
        "ящика 908×255 на",
        "направляющих 600 мм",
        "полного выдвижения.",
        "",
        "Сверху — открытый",
        "стеллаж 500, глубина",
        "450, 3 секции; под ним",
        "LED-лента над столом.",
        "",
        "Рабочая глубина",
        "столешницы — 450.",
        "Стол можно сделать",
        "глубже — скажите.",
    ]
    for i, txt in enumerate(lines):
        s.t(X, Y + 5 + i * 3.5, txt, 2.25, "start")
    s.save("stol_list1.svg")


# ---------------------------------------------------------------- лист 2
def sheet2():
    s = S()
    header(s, "Стол шлифовальный — 3D, детали, фурнитура",
           "Детали для раскроя: L × W × толщина (для фигурных — габарит), кромка ПВХ 2 мм — по лицевым торцам ЛДСП", 2)
    for i, (v, cap) in enumerate((("front", "Общий вид"), ("back", "Сзади: патрубки Ø160 к пылесосу"),
                                  ("open", "Без столешницы и перфостенки, ящик выдвинут"))):
        b64 = base64.b64encode(open(os.path.join(HERE, f"3d_{v}.png"), "rb").read()).decode()
        x = 12 + i * 133
        s.e(f'<image x="{x}" y="28" width="128" height="89.6" href="data:image/png;base64,{b64}"/>')
        s.rc(x, 28, x + 128, 117.6, stroke="#ccc")
        s.t(x + 64, 122, cap, 2.6)
    X, Y = 12, 132
    s.t(X, Y, "Детали", 3.4, "start", "bold")
    cols = [X, X + 8, X + 86, X + 124, X + 168, X + 182]
    Y += 3
    s.rc(X, Y, X + 205, Y + 6, fill="#eef1f4", stroke="#999", w=0.15)
    for c, h in zip(cols, ["№", "Деталь", "Материал", "L × W × t, мм", "Кол.", "Площадь, м²"]):
        s.t(c + 1.5, Y + 4.2, h, 2.3, "start", "bold")
    Y += 6
    area = {}
    for i, ((name, mat, a, b, t), n) in enumerate(M.spec().items()):
        ar = a * b * n / 1e6
        area[mat] = area.get(mat, 0) + ar
        s.rc(X, Y, X + 205, Y + 4.2, fill="#fff" if i % 2 else "#fafafa", stroke="#ddd", w=0.1)
        for c, v in zip(cols, [i + 1, name, mat, f"{a} × {b} × {t}", n, f"{ar:.2f}"]):
            s.t(c + 1.5, Y + 3.1, str(v), 2.1, "start")
        Y += 4.2
    Y += 3
    for mat, ar in area.items():
        sheets = math.ceil(ar * 1.2 / (2.8 * 2.07) * 2) / 2
        s.t(X, Y + 3.5, f"{mat}: {ar:.2f} м² → с запасом на раскрой ≈ {sheets:g} листа 2800×2070", 2.4, "start", "bold")
        Y += 4.5
    # фурнитура
    X2, Y2 = 232, 132
    s.t(X2, Y2, "Фурнитура и комплектующие", 3.4, "start", "bold")
    items = [
        ("Опора регулируемая h 100 (±15), под 100 кг", "8 шт."),
        ("Направляющие шариковые 600, полного выдвижения, 45 кг", "3 пары"),
        ("Ручка-скоба 256 мм (или профиль Gola)", "3 шт."),
        ("Патрубок Ø160 с фланцем (в задней стенке камеры)", "2 шт."),
        ("Тройник 2×Ø160 → Ø200 + хомуты, гофра Ø160", "1 к-т"),
        ("Лента LED 24 В, 4000 К, с профилем (под стеллажом)", "2,7 м"),
        ("Блок питания 24 В 60 Вт + выключатель", "1 к-т"),
        ("Блок розеток 3 × 220 В (на боковину)", "1–2 шт."),
        ("Конфирмат 7×50", "≈ 200 шт."),
        ("Саморез 4×30 (столешница к рёбрам, без клея)", "≈ 40 шт."),
        ("Герметик / уплотнитель швов камеры", "1 туба"),
        ("Крючки для перфостенки (по месту)", "—"),
    ]
    for i, (a, b) in enumerate(items):
        y = Y2 + 6 + i * 5
        s.rc(X2, y - 3.6, X2 + 176, y + 1.2, fill="#fff" if i % 2 else "#fafafa", stroke="#ddd", w=0.1)
        s.t(X2 + 1.5, y, a, 2.3, "start")
        s.t(X2 + 174, y, b, 2.3, "end", "bold")
    y = Y2 + 6 + len(items) * 5 + 6
    s.t(X2, y, "Примечания", 3.2, "start", "bold")
    for i, txt in enumerate([
        "• Все детали ≤ 2768 мм — режутся из листа 2800×2070 с обрезкой кромок.",
        "• Швы камеры (перекрытие, боковины, задняя стенка, фасад, крышка канала)",
        "  — на герметик, иначе пылесос тянет воздух через щели.",
        "• Столешницу крепить саморезами в рёбра без клея — сменная.",
        "• Рёбра камеры и канала — с вырезами (пояс 60 + ножки 80),",
        "  чтобы воздух свободно шёл к патрубкам.",
        "• Боковины фигурные (скос под наклонный фасад) — по шаблону, ЧПУ.",
        "• Прорези столешницы и перфостенки — на ЧПУ, фреза Ø8–10.",
        "• Цвета на 3D условные; ЛДСП — антрацит, как на фото.",
    ]):
        s.t(X2, y + 5 + i * 3.8, txt, 2.3, "start")
    s.save("stol_list2.svg")


if __name__ == "__main__":
    assert M.check() == 0
    sheet1()
    sheet2()
