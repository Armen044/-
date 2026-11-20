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
def front_view(s, X, G):
    """Вид спереди: X — лево листа, G — уровень пола на листе."""
    f = lambda x, z: (X + x * K, G - z * K)
    R = lambda x0, z0, x1, z1, **kw: s.rc(*f(x0, z0), *f(x1, z1), **kw)
    for x in (60, 936, 1864, M.L - 60):
        R(x - 25, 0, x + 25, M.LEG, fill="#222", stroke="#000")
    # основание (утоплено на 100) — открытые секции с полками
    R(0, M.LEG, M.L, M.PLB, fill=LDSP_C, stroke="#111", w=0.25)
    for a, b in M.SEC:
        R(a, M.LEG + M.T, b, M.PLB, fill="#3c3f42", stroke="#111", w=0.15)
        R(a, 375, b, 391, fill=LDSP_C, stroke="#111", w=0.15)
    # короб
    R(0, M.PLB, M.L, M.ZT - M.TM, fill=LDSP_C, stroke="#111", w=0.25)
    R(M.T, M.PLB + M.T, M.L - M.T, M.ZT - M.TM, fill=MDF_C, stroke="#111", w=0.2)
    for z in M.FRONT_ROWS:
        for a, b in M.FRONT_SEG:
            R(a, z - 5, b, z + 5, fill="#3a2f22", stroke="none", rx=0.5)
    R(0, M.ZT - M.TM, M.L, M.ZT, fill=MDF_C, stroke="#111", w=0.25)
    s.ln(*f(M.L / 2, M.ZT - M.TM), *f(M.L / 2, M.ZT), 0.25)
    # задняя стенка
    for x in (0, M.L - M.T):
        R(x, M.ZT, x + M.T, M.ZW, fill=LDSP_C, stroke="#111", w=0.2)
    R(M.T, M.ZT, M.L - M.T, M.ZW - M.T, fill=MDF_C, stroke="#111", w=0.2)
    for x, z in M.WALL_SLOTS:
        R(x - 15, z - 4, x + 15, z + 4, fill="#3a2f22", stroke="none", rx=0.4)
    R(M.T, M.ZW - M.T, M.L - M.T, M.ZW, fill=LDSP_C, stroke="#111", w=0.2)
    s.ln(*f(M.T + 20, M.ZW - M.T - 4), *f(M.L - M.T - 20, M.ZW - M.T - 4), 0.6, "#f5c518")
    # размеры
    dim_h(s, *f(0, 0)[:1], f(M.L, 0)[0], G + 9, "2800", 2.6)
    for a, b in M.SEC:
        dim_h(s, f(a, 0)[0], f(b, 0)[0], G + 4.5, f"{b-a}", 2.0)
    xr = f(M.L, 0)[0]
    for z0, z1 in ((0, M.LEG), (M.LEG, M.PLB), (M.PLB, M.ZT), (M.ZT, M.ZW)):
        dim_v(s, f(0, z0)[1], f(0, z1)[1], xr + 5, f"{z1-z0}", 2.2, side=1.8)
    dim_v(s, G, f(0, M.ZT)[1], xr + 11, "900", 2.4, side=1.8)
    dim_v(s, G, f(0, M.ZW)[1], X - 6, "1450", 2.6)
    s.t(X + M.L * K / 2, G - M.ZW * K - 4, "ВИД СПЕРЕДИ", 3, weight="bold")
    # указатель разреза
    for z, tag in ((M.ZW + 60, "А"), (-60, "А")):
        x, y = f(700, z)
        s.t(x, y + (1 if z < 0 else 0) + (2.5 if z < 0 else -0.5), tag, 3, weight="bold")
    s.ln(*f(700, M.ZW + 30), *f(700, M.ZW - 60), 0.5, "#111")
    s.ln(*f(700, 30), *f(700, -40), 0.5, "#111")


def top_view(s, X, Yt):
    """Вид сверху: передний край стола — снизу, Yt — задний край (y = 700) на листе."""
    f = lambda x, y: (X + x * K, Yt + (M.D - y) * K)
    R = lambda x0, y0, x1, y1, **kw: s.rc(*f(x0, y0), *f(x1, y1), **kw)
    for x0 in (0, M.L / 2):
        R(x0, 0, x0 + M.L / 2, M.TOPY, fill=MDF_C, stroke="#111", w=0.25)
    for x, y in M.TOP_SLOTS:
        R(x - 20, y - 5, x + 20, y + 5, fill="#3a2f22", stroke="none", rx=0.5)
    for xc in M.RIBS:
        s.ln(*f(xc, 36), *f(xc, M.TOPY), 0.2, "#777", "1.2 0.8")
    R(M.T, M.TOPY, M.L - M.T, M.D, fill=MDF_C, stroke="#111", w=0.2)
    for x in (0, M.L - M.T):
        R(x, M.D - 166, x + M.T, M.D, fill=LDSP_C, stroke="#111", w=0.2)
    R(M.T, M.D - 166, M.L - M.T, M.D, fill="none", stroke="#111", w=0.25, dash="2 1")
    for x in M.OUTLETS:
        R(x - 80, M.D, x + 80, M.D + 80, fill="#c9cdd1", stroke="#555", w=0.2)
        x0, y0 = f(x, M.D + 80)
        s.t(x0, y0 - 1.3, "Ø160", 1.8)
    dim_h(s, f(0, 0)[0], f(M.L / 2, 0)[0], f(0, 0)[1] + 5, "1400 (стык над сдвоенным ребром)", 2.1)
    dim_h(s, f(M.L / 2, 0)[0], f(M.L, 0)[0], f(0, 0)[1] + 5, "1400", 2.1)
    dim_v(s, f(0, 0)[1], f(0, M.D)[1], X - 6, "700", 2.4)
    dim_v(s, f(0, 0)[1], f(0, M.TOPY)[1], X - 2.5, "684", 2.0)
    s.t(X + M.L * K / 2, Yt - 10.5, "ВИД СВЕРХУ  (пунктир — рёбра под столешницей и козырёк)", 3, weight="bold")


def section(s, X, G):
    """Разрез А–А: передний край стола — слева."""
    f = lambda y, z: (X + y * K, G - z * K)
    R = lambda y0, z0, y1, z1, **kw: s.rc(*f(y0, z0), *f(y1, z1), **kw)
    cut = dict(fill="url(#hatch)", stroke="#111", w=0.25)
    # ребро за плоскостью разреза (вид)
    zt = M.ZT - M.TM - 60
    R(36, zt, M.TOPY, M.ZT - M.TM, fill="#d5d7d9", stroke="#777", w=0.15)
    for a, b in ((36, 136), ((36 + M.TOPY) / 2 - 50, (36 + M.TOPY) / 2 + 50), (M.TOPY - 100, M.TOPY)):
        R(a, M.PLB + M.T, b, zt, fill="#d5d7d9", stroke="#777", w=0.15)
    # бок основания за разрезом (контур)
    R(M.SET, M.LEG, M.D, M.PLB, fill="none", stroke="#999", w=0.15, dash="1.5 1")
    for y in (M.SET + 60, M.D - 60):
        R(y - 25, 0, y + 25, M.LEG, fill="#222", stroke="#000")
    R(M.SET, M.LEG, M.D, M.LEG + M.T, **cut)                    # дно основания
    R(M.SET + 10, 375, M.D - M.T, 391, **cut)                   # полка
    R(M.D - M.T, M.LEG + M.T, M.D, M.PLB, **cut)                # задняя стенка основания
    R(20, M.PLB, M.TOPY, M.PLB + M.T, **cut)                    # дно короба
    R(M.D - M.T, M.PLB + M.T, M.D, M.ZT, **cut)                 # задняя стенка короба
    R(20, M.PLB + M.T, 36, M.ZT - M.TM, **cut)                  # лицевая панель
    R(0, M.ZT - M.TM, M.TOPY, M.ZT, **cut)                      # столешница
    R(M.TOPY, M.ZT, M.D, M.ZW - M.T, **cut)                     # перфостенка
    R(M.D - 166, M.ZW - M.T, M.D, M.ZW, **cut)                  # козырёк
    R(M.D - 166, M.ZT, M.D, M.ZW, fill="none", stroke="#999", w=0.15, dash="1.5 1")   # стойка за разрезом
    # патрубок
    R(M.D, M.OUT_Z - 80, M.D + 90, M.OUT_Z + 80, fill="#c9cdd1", stroke="#555", w=0.2)
    s.ln(*f(M.D - 166 + 20, M.ZW - M.T - 4), *f(M.D - 20, M.ZW - M.T - 4), 0.7, "#f5c518")
    # поток воздуха
    for y in (150, 330, 510):
        x0, y0 = f(y, M.ZT + 90)
        x1, y1 = f(y, M.ZT - 120)
        s.e(f'<path d="M{x0:.2f} {y0:.2f} L{x1:.2f} {y1:.2f}" stroke="#2e86de" stroke-width="0.4" fill="none" marker-end="url(#arr)"/>')
    x0, y0 = f(400, M.OUT_Z)
    x1, y1 = f(M.D + 120, M.OUT_Z)
    s.e(f'<path d="M{x0:.2f} {y0:.2f} L{x1:.2f} {y1:.2f}" stroke="#2e86de" stroke-width="0.4" fill="none" marker-end="url(#arr)"/>')
    s.e('<defs><marker id="arr" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto"><path d="M0 0 L4 2 L0 4Z" fill="#2e86de"/></marker></defs>')
    x, y = f(M.D + 90, M.OUT_Z - 140)
    s.t(x, y, "Ø160 → к", 1.9, "end", fill="#2e86de")
    s.t(x, y + 2.4, "аспирации", 1.9, "end", fill="#2e86de")
    # размеры
    dim_h(s, f(0, 0)[0], f(M.D, 0)[0], G + 9, "700", 2.4)
    dim_h(s, f(0, 0)[0], f(M.SET, 0)[0], G + 4.5, "100", 2.0)
    dim_h(s, f(M.SET, 0)[0], f(M.D, 0)[0], G + 4.5, "600", 2.0)
    dim_h(s, f(M.D - 166, 0)[0], f(M.D, 0)[0], f(0, M.ZW)[1] - 3, "166", 2.0)
    xr = f(M.D, 0)[0]
    for z0, z1 in ((0, M.LEG), (M.LEG, 375), (375, M.PLB), (M.PLB, M.ZT), (M.ZT, M.ZW)):
        dim_v(s, f(0, z0)[1], f(0, z1)[1], X - 4, f"{z1-z0}", 2.0)
    dim_v(s, f(0, M.PLB + M.T)[1], f(0, M.ZT - M.TM)[1], xr + 12, "231 короб", 1.9, side=1.8)
    s.t(X + M.D * K / 2, f(0, M.ZW)[1] - 9, "РАЗРЕЗ А–А", 3, weight="bold")


def sheet1():
    s = S()
    header(s, "Стол шлифовальный с нижней вытяжкой 2800 × 700",
           "Высота столешницы 900, задняя стенка 550  |  ЛДСП 16 антрацит, МДФ 19 (столешница), МДФ 16 (лицевая панель, перфостенка)  |  М 1:10, размеры в мм", 1)
    front_view(s, 22, 180)
    top_view(s, 22, 210)
    section(s, 322, 180)
    X, Y = 330, 210
    s.t(X, Y, "Как работает", 3.2, "start", "bold")
    for i, txt in enumerate([
        "Воздух с пылью уходит вниз через прорези",
        "столешницы в короб высотой 250 мм и",
        "отводится через 2 патрубка Ø160 сзади",
        "в общую аспирацию (тройник → Ø200).",
        f"Прорези 40×10: {len(M.TOP_SLOTS)} шт., живое сечение",
        f"{M.open_area():.2f} м². Рекомендуемая производитель-",
        "ность вытяжки — от 2000 м³/ч.",
        "Шлифмашинки дополнительно — к пылесосам,",
        "как сейчас в цеху.",
        "Столешница из двух половин по 1400 —",
        "изношенную меняют по частям.",
    ]):
        s.t(X, Y + 5 + i * 3.6, txt, 2.3, "start")
    s.save("stol_list1.svg")


# ---------------------------------------------------------------- лист 2
def sheet2():
    s = S()
    header(s, "Стол шлифовальный — 3D, детали, фурнитура",
           "Детали для раскроя: размер L × W × толщина, кромка ПВХ 2 мм — по лицевым торцам ЛДСП", 2)
    for i, (v, cap) in enumerate((("front", "Общий вид"), ("back", "Сзади: патрубки Ø160"),
                                  ("open", "Без столешницы и лицевой панели: рёбра короба"))):
        b64 = base64.b64encode(open(os.path.join(HERE, f"3d_{v}.png"), "rb").read()).decode()
        x = 12 + i * 133
        s.e(f'<image x="{x}" y="28" width="128" height="89.6" href="data:image/png;base64,{b64}"/>')
        s.rc(x, 28, x + 128, 117.6, stroke="#ccc")
        s.t(x + 64, 122, cap, 2.6)
    X, Y = 12, 132
    s.t(X, Y, "Детали", 3.4, "start", "bold")
    cols = [X, X + 8, X + 82, X + 122, X + 172, X + 188]
    Y += 3
    s.rc(X, Y, X + 205, Y + 6, fill="#eef1f4", stroke="#999", w=0.15)
    for c, h in zip(cols, ["№", "Деталь", "Материал", "L × W × t, мм", "Кол.", "Площадь, м²"]):
        s.t(c + 1.5, Y + 4.2, h, 2.3, "start", "bold")
    Y += 6
    area = {}
    for i, ((name, mat, a, b, t), n) in enumerate(M.spec().items()):
        ar = a * b * n / 1e6
        area[mat] = area.get(mat, 0) + ar
        s.rc(X, Y, X + 205, Y + 4.6, fill="#fff" if i % 2 else "#fafafa", stroke="#ddd", w=0.1)
        for c, v in zip(cols, [i + 1, name, mat, f"{a} × {b} × {t}", n, f"{ar:.2f}"]):
            s.t(c + 1.5, Y + 3.3, str(v), 2.2, "start")
        Y += 4.6
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
        ("Патрубок Ø160 с фланцем (в задней стенке короба)", "2 шт."),
        ("Тройник 2×Ø160 → Ø200 + хомуты, гофра Ø160", "1 к-т"),
        ("Лента LED 24 В, 4000 К, с алюминиевым профилем", "2,7 м"),
        ("Блок питания 24 В 60 Вт + выключатель", "1 к-т"),
        ("Блок розеток 3 × 220 В (на стойку задней стенки)", "1–2 шт."),
        ("Конфирмат 7×50", "≈ 120 шт."),
        ("Саморез 4×30 (столешница к рёбрам, без клея)", "≈ 60 шт."),
        ("Герметик / уплотнитель швов короба", "1 туба"),
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
        "• Швы короба (дно, бока, задняя стенка, лицевая панель) — на герметик,",
        "  иначе вытяжка тянет воздух через щели, а не через столешницу.",
        "• Столешницу крепить саморезами в рёбра без клея — сменная.",
        "• Рёбра короба — с вырезами (верхний пояс 60 мм + 3 ножки 100 мм),",
        "  чтобы воздух свободно шёл к патрубкам.",
        "• Прорези столешницы и перфостенки — на ЧПУ, фреза Ø8–10.",
        "• Цвета на 3D условные; ЛДСП — антрацит, как на фото.",
    ]):
        s.t(X2, y + 5 + i * 3.8, txt, 2.3, "start")
    s.save("stol_list2.svg")


if __name__ == "__main__":
    assert M.check() == 0
    sheet1()
    sheet2()
