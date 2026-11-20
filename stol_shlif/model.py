#!/usr/bin/env python3
"""Шлифовальный стол с вытяжной камерой, выкатными ящиками и стеллажом (по эскизу заказчика). Размеры в мм.

Оси: X — вдоль стола (0…2800), Y — вглубь (0 — передний край), Z — вверх от пола.
Габарит 2800 × 700, столешница на 900, задняя стенка 550 над столом (до 1450), стеллаж 500 (до 1950).

Состав (по эскизу):
  • камера для пылесоса/аспирации — пустота под столешницей (от перекрытия на 391 до 900) с наклонным
    перфорированным фасадом и вертикальный канал за перфостенкой до 1450; патрубки Ø160 сзади на высоте 520;
  • ниже камеры — 3 выкатных ящика на направляющих полного выдвижения (по одному в секции 912);
  • сверху — открытый стеллаж высотой 500, глубиной 450, под ним светодиодная лента.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
L, D = 2800, 700
LEG = 100                 # регулируемые опоры
T, TM = 16, 19
ZD = 375                  # низ перекрытия над ящиками (дно камеры — 391)
ZT = 900                  # верх столешницы
YT = 450                  # глубина рабочей столешницы (дальше — перфостенка и канал)
ZW = 1450                 # верх задней стенки (550 над столом)
SH_H, SH_Y = 500, 250     # стеллаж: высота, передний край
ZS = ZW + SH_H            # 1950
SLANT = 84                # наклон фасада камеры: внизу отступ 84 от края
LDSP, MDF16, MDF19 = "ЛДСП 16 антрацит", "МДФ 16", "МДФ 19"

PARTS = []    # dict(name, mat, kind='box'|'prism', x0,x1, y0,y1,z0,z1 | poly=[(y,z)...], tag)


def box(name, mat, x0, x1, y0, y1, z0, z1, tag=""):
    PARTS.append(dict(name=name, mat=mat, kind="box", x0=x0, x1=x1, y0=y0, y1=y1, z0=z0, z1=z1, tag=tag))


def prism(name, mat, x0, x1, poly, tag=""):
    ys, zs = [p[0] for p in poly], [p[1] for p in poly]
    PARTS.append(dict(name=name, mat=mat, kind="prism", x0=x0, x1=x1, poly=poly,
                      y0=min(ys), y1=max(ys), z0=min(zs), z1=max(zs), tag=tag))


SIDE = [(0, LEG), (D, LEG), (D, ZW), (YT, ZW), (YT, ZT), (0, ZT), (0, ZT - TM), (SLANT, ZD + T), (0, ZD + T)]
FASCIA = [(0, ZT - TM), (T, ZT - TM), (SLANT + T, ZD + T), (SLANT, ZD + T)]
SEC = [(T, 928), (944, 1856), (1872, L - T)]

# ---- корпус
for x in (0, L - T):
    prism("Боковина (фигурная)", LDSP, x, x + T, SIDE)
box("Дно", LDSP, T, L - T, 0, D - T, LEG, LEG + T)
box("Задняя стенка нижняя", LDSP, T, L - T, D - T, D, LEG, ZD)
for a, b in zip(SEC, SEC[1:]):
    box("Перегородка ящиков", LDSP, a[1], b[0], 0, D - T, LEG + T, ZD)
box("Перекрытие (дно камеры)", LDSP, T, L - T, 0, D - T, ZD, ZD + T)
# ---- камера
box("Задняя стенка камеры", LDSP, T, L - T, D - T, D, ZD, ZW)
prism("Фасад камеры наклонный, с прорезями", MDF16, T, L - T, FASCIA)
RIBS = [467, 933, 1392, 1408, 1867, 2333]
for xc in RIBS:
    box("Ребро камеры (с вырезами)", LDSP, xc - 8, xc + 8, 100, D - T, ZD + T, ZT - TM)
for x0, x1 in ((T, L / 2), (L / 2, L - T)):
    box("Столешница перфорированная (половина)", MDF19, x0, x1, 0, YT, ZT - TM, ZT)
box("Перфостенка (передняя стенка канала)", MDF16, T, L - T, YT, YT + T, ZT - TM, ZW - T)
for xc in (936, 1864):
    box("Ребро канала (с вырезом)", LDSP, xc - 8, xc + 8, YT + T, D - T, ZT, ZW - T)
box("Крышка канала", LDSP, T, L - T, YT + T, D - T, ZW - T, ZW)
# ---- стеллаж
for x in (0, L - T):
    box("Бок стеллажа", LDSP, x, x + T, SH_Y, D, ZW, ZS)
box("Дно стеллажа", LDSP, T, L - T, SH_Y, D, ZW, ZW + T)
box("Крышка стеллажа", LDSP, T, L - T, SH_Y, D, ZS - T, ZS)
box("Задняя стенка стеллажа", LDSP, T, L - T, D - T, D, ZW + T, ZS - T)
for a, b in zip(SEC, SEC[1:]):
    box("Перегородка стеллажа", LDSP, a[1], b[0], SH_Y, D - T, ZW + T, ZS - T)
# ---- выкатные ящики (направляющие 600, зазор 13 на сторону)
DR_Z0, DR_Z1 = 140, 340
for i, (a, b) in enumerate(SEC):
    tag = f"drawer{i}"
    box("Фасад ящика", LDSP, a + 2, b - 2, 0, T, LEG + T + 2, ZD - 2, tag)
    for x in (a + 13, b - 29):
        box("Бок ящика", LDSP, x, x + T, T, T + 600, DR_Z0, DR_Z1, tag)
    for y in (T, T + 600 - T):
        box("Перед/зад ящика", LDSP, a + 29, b - 29, y, y + T, DR_Z0, DR_Z1, tag)
    box("Дно ящика", LDSP, a + 29, b - 29, 2 * T, T + 600 - T, DR_Z0, DR_Z0 + T, tag)
# первая «перед/зад» у ящика совпадает с фасадом по Y — сдвигаем внутренний перед за фасад
for p in PARTS:
    if p["name"] == "Перед/зад ящика" and p["y0"] == T:
        p["y0"], p["y1"] = T + 2, 2 * T + 2
for p in PARTS:
    if p["name"] == "Дно ящика":
        p["y0"] = 2 * T + 2
        p["z0"], p["z1"] = DR_Z0, DR_Z0 + T
        p["x0"], p["x1"] = p["x0"], p["x1"]

# ---- перфорация
TOP_SLOT = (40, 10)
TOP_SLOTS = []
for r, y in enumerate(range(50, YT - 39, 50)):
    off = 0 if r % 2 == 0 else 40
    for x in range(80 + off, L - 79, 80):
        if all(abs(x - xc) > 30 for xc in RIBS):
            TOP_SLOTS.append((x, y))
WALL_SLOTS = []
for r, z in enumerate(range(ZT + 40, ZW - T - 29, 38)):
    off = 0 if r % 2 == 0 else 30
    for x in range(60 + off, L - 59, 60):
        if all(abs(x - xc) > 25 for xc in (936, 1864)):
            WALL_SLOTS.append((x, z))
FASCIA_ROWS = [0.2, 0.35, 0.5, 0.65, 0.8]      # доли длины наклонного фасада (снизу вверх)
FRONT_SEG = []
_n, _m, _br = 4, 60, 60
_len = (L - 2 * T - 2 * _m - (_n - 1) * _br) / _n
for i in range(_n):
    a = T + _m + i * (_len + _br)
    FRONT_SEG.append((a, a + _len))
OUTLETS, OUT_Z, OUT_D = [700, 2100], 520, 160
FASCIA_LEN = round(math.hypot(SLANT, ZT - TM - ZD - T))


def fascia_point(t):
    """Точка на наружной грани наклонного фасада: t = 0 — низ, 1 — верх."""
    return SLANT * (1 - t), ZD + T + (ZT - TM - ZD - T) * t


def size(p):
    if p["kind"] == "prism" and p["name"].startswith("Фасад"):
        return round(p["x1"] - p["x0"]), FASCIA_LEN, T
    d = sorted([p["x1"] - p["x0"], p["y1"] - p["y0"], p["z1"] - p["z0"]], reverse=True)
    return round(d[0]), round(d[1]), round(d[2])


def check():
    """Пересечения коробок между собой (фигурные детали проверяются по контуру отдельно)."""
    bad = 0
    bx = [p for p in PARTS if p["kind"] == "box"]
    for i, a in enumerate(bx):
        for b in bx[i + 1:]:
            if all(min(a[k + "1"], b[k + "1"]) - max(a[k + "0"], b[k + "0"]) > 0.5 for k in "xyz"):
                print("пересечение:", a["name"], a["tag"], "/", b["name"], b["tag"])
                bad += 1
    return bad


def spec():
    rows = {}
    for p in PARTS:
        key = (p["name"], p["mat"]) + size(p)
        rows[key] = rows.get(key, 0) + 1
    return rows


def open_area():
    a = TOP_SLOT[0] * TOP_SLOT[1] - (TOP_SLOT[1] ** 2 - math.pi * (TOP_SLOT[1] / 2) ** 2)
    return len(TOP_SLOTS) * a / 1e6


if __name__ == "__main__":
    print("пересечений:", check())
    for k, n in spec().items():
        print(n, k)
    print("прорезей в столешнице:", len(TOP_SLOTS), "живое сечение, м²:", round(open_area(), 3), "фасад:", FASCIA_LEN)
    with open(os.path.join(HERE, "model.js"), "w") as f:
        f.write("window.PARTS = " + json.dumps(PARTS, ensure_ascii=False) + ";\n")
        f.write("window.TOP_SLOTS = " + json.dumps(TOP_SLOTS) + ";\n")
        f.write("window.WALL_SLOTS = " + json.dumps(WALL_SLOTS) + ";\n")
        f.write("window.FASCIA = " + json.dumps({"rows": [fascia_point(t) for t in FASCIA_ROWS], "seg": FRONT_SEG}) + ";\n")
        f.write("window.OUTLETS = " + json.dumps({"x": OUTLETS, "z": OUT_Z, "d": OUT_D}) + ";\n")
        f.write("window.DIM = " + json.dumps(dict(L=L, D=D, ZT=ZT, ZW=ZW, ZS=ZS, YT=YT, SH_Y=SH_Y, T=T, LEG=LEG, ZD=ZD)) + ";\n")
