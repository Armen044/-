#!/usr/bin/env python3
"""Шлифовальный стол с нижней вытяжкой (по фото цеха). Размеры в мм.

Оси: X — вдоль стола (0…2800, слева направо при взгляде спереди), Y — вглубь (0 — передний край),
Z — вверх от пола. Длина 2800, глубина 700, рабочая поверхность на 900, задняя стенка 550 над столом.

Состав:
  • основание из ЛДСП 16 на регулируемых опорах, 3 открытые секции с полками, отступ от фасада 100;
  • вытяжной короб (высота 250): перфорированная столешница МДФ 19, лицевая панель МДФ 16
    с продольными прорезями, рёбра жёсткости с проходами для воздуха, 2 патрубка Ø160 сзади;
  • задняя перфорированная стенка МДФ 16 (под крючки), боковые стойки и козырёк со светодиодной лентой.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
L, D = 2800, 700          # длина, глубина
ZT = 900                  # верх столешницы
WALL_H = 550              # задняя стенка над столешницей
ZW = ZT + WALL_H          # 1450 — верх стенки
LEG = 100                 # регулируемые опоры
T, TM = 16, 19            # ЛДСП / МДФ столешницы
SET = 100                 # отступ основания от переднего края
PLB = 634                 # низ плиты-перекрытия (дно короба)
TOPY = D - T              # столешница до задней стенки: 684
LDSP, MDF16, MDF19 = "ЛДСП 16 антрацит", "МДФ 16", "МДФ 19"

PARTS = []   # (название, материал, x0, x1, y0, y1, z0, z1)


def part(name, mat, x0, x1, y0, y1, z0, z1):
    PARTS.append((name, mat, x0, x1, y0, y1, z0, z1))


# ---- основание
for x in (0, L - T):
    part("Бок основания", LDSP, x, x + T, SET, D, LEG, PLB)
part("Дно основания", LDSP, T, L - T, SET, D, LEG, LEG + T)
SEC = [(T, 928), (944, 1856), (1872, L - T)]          # 3 секции в свету
for a, b in zip(SEC, SEC[1:]):
    part("Перегородка основания", LDSP, a[1], b[0], SET, D - T, LEG + T, PLB)
part("Задняя стенка основания", LDSP, T, L - T, D - T, D, LEG + T, PLB)
for a, b in SEC:
    part("Полка основания", LDSP, a, b, SET + 10, D - T, 375, 375 + T)
# ---- вытяжной короб
for x in (0, L - T):
    part("Бок короба", LDSP, x, x + T, 20, D, PLB, ZT - TM)
part("Плита-перекрытие (дно короба)", LDSP, T, L - T, 20, TOPY, PLB, PLB + T)
part("Задняя стенка короба", LDSP, T, L - T, D - T, D, PLB + T, ZT)
part("Лицевая панель с прорезями", MDF16, T, L - T, 20, 20 + T, PLB + T, ZT - TM)
RIBS = [467, 933, 1392, 1408, 1867, 2333]              # оси рёбер (пролёт ≈ 450); в центре — сдвоенное под стык
for xc in RIBS:
    part("Ребро короба", LDSP, xc - 8, xc + 8, 36, TOPY, PLB + T, ZT - TM)
for x0 in (0, L / 2):
    part("Столешница перфорированная (половина)", MDF19, x0, x0 + L / 2, 0, TOPY, ZT - TM, ZT)
# ---- задняя стенка
part("Стенка перфорированная", MDF16, T, L - T, D - T, D, ZT, ZW - T)
for x in (0, L - T):
    part("Стойка задней стенки", LDSP, x, x + T, D - 166, D, ZT, ZW)
part("Козырёк со светом", LDSP, T, L - T, D - 166, D, ZW - T, ZW)

# ---- перфорация (координаты центров, размеры прорезей)
TOP_SLOT = (40, 10)          # вдоль X × вдоль Y
TOP_SLOTS = []
for r, y in enumerate(range(60, 641, 50)):
    off = 0 if r % 2 == 0 else 40
    for x in range(80 + off, L - 79, 80):
        if all(abs(x - xc) > 30 for xc in RIBS):     # над рёбрами — без прорезей
            TOP_SLOTS.append((x, y))
WALL_SLOT = (30, 8)          # вдоль X × по высоте
WALL_SLOTS = []
for r, z in enumerate(range(ZT + 40, ZW - T - 29, 38)):
    off = 0 if r % 2 == 0 else 30
    for x in range(60 + off, L - 59, 60):
        WALL_SLOTS.append((x, z))
FRONT_ROWS = [700, 745, 790, 835]       # продольные прорези лицевой панели, высота 10
FRONT_SEG = []
_n, _m, _br = 4, 60, 60
_len = (L - 2 * T - 2 * _m - (_n - 1) * _br) / _n
for i in range(_n):
    a = T + _m + i * (_len + _br)
    FRONT_SEG.append((a, a + _len))
OUTLETS = [700, 2100]        # патрубки Ø160 в задней стенке короба, ось Z = 767
OUT_Z, OUT_D = 767, 160


def size(p):
    """Размеры детали: длина × ширина × толщина (две большие стороны и толщина)."""
    d = sorted([p[3] - p[2], p[5] - p[4], p[7] - p[6]], reverse=True)
    return round(d[0]), round(d[1]), round(d[2])


def check():
    bad = 0
    for i, a in enumerate(PARTS):
        for b in PARTS[i + 1:]:
            if all(min(a[k + 1], b[k + 1]) - max(a[k], b[k]) > 0.5 for k in (2, 4, 6)):
                print("пересечение:", a[0], "/", b[0])
                bad += 1
    return bad


def spec():
    rows = {}
    for p in PARTS:
        key = (p[0], p[1]) + size(p)
        rows[key] = rows.get(key, 0) + 1
    return rows


def open_area():
    a = TOP_SLOT[0] * TOP_SLOT[1] - (TOP_SLOT[1] ** 2 - math.pi * (TOP_SLOT[1] / 2) ** 2)
    return len(TOP_SLOTS) * a / 1e6


if __name__ == "__main__":
    print("пересечений:", check())
    for k, n in spec().items():
        print(n, k)
    print("прорезей в столешнице:", len(TOP_SLOTS), "живое сечение, м²:", round(open_area(), 3))
    print("прорезей в стенке:", len(WALL_SLOTS))
    with open(os.path.join(HERE, "model.js"), "w") as f:
        f.write("window.PARTS = " + json.dumps([[p[2], p[3], p[4], p[5], p[6], p[7], p[1], p[0]] for p in PARTS]) + ";\n")
        f.write("window.TOP_SLOTS = " + json.dumps(TOP_SLOTS) + ";\n")
        f.write("window.WALL_SLOTS = " + json.dumps(WALL_SLOTS) + ";\n")
        f.write("window.FRONT = " + json.dumps({"rows": FRONT_ROWS, "seg": FRONT_SEG}) + ";\n")
        f.write("window.OUTLETS = " + json.dumps({"x": OUTLETS, "z": OUT_Z, "d": OUT_D}) + ";\n")
        f.write(f"window.DIM = {json.dumps(dict(L=L, D=D, ZT=ZT, ZW=ZW, TM=TM, T=T, TOPY=TOPY, LEG=LEG, SET=SET, RIBS=RIBS, PLB=PLB))};\n")
