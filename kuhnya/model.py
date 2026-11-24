#!/usr/bin/env python3
"""Кухня по эскизу заказчика. Размеры в мм.

Оси: X — вдоль стены слева направо, Y — от стены (0) к фасадам, Z — вверх от пола. Потолок 3000.
Слева направо (общая длина 5500):
  • пенал 950 под отдельностоящий холодильник 900 — без дна, боковины до пола, сверху антресоль;
  • нижний ряд 3800: 450 | 600 ящики | 600 варочная | 600 | 600 ящики | 800 мойка | 150 карго;
    МДФ эмаль белая, ручка Gola; столешница на 900;
  • верхний ряд 1500 = шкафы 1050 (от 1500) + антресоль 450: 520 | 520 | 640 под вытяжку | 4 × 530;
  • пенал 600: стеклянные полки, подсветка по бокам, фасад — алюминиевая рамка со стеклом;
  • пенал 150 справа: высокое выдвижное карго за фасадом (крупы, специи).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
H = 3000
T, FD, GAP = 16, 19, 3        # ЛДСП корпуса, МДФ фасада, зазор между фасадами
PL = 100                      # цоколь
ZB = 862                      # верх корпусов нижнего ряда
CT = 38                       # столешница → верх 900
ZU0, ZU1 = 1500, 2550         # верхние шкафы
ZA1 = 2990                    # верх корпуса антресоли (10 мм до потолка)
DB, DU, DTALL, DFR = 560, 350, 580, 700   # глубины корпусов: низ, верх, пенал, пенал под холодильник
GOLA = 30                     # проём под профиль Gola над фасадом
X0 = 950                      # начало нижнего/верхнего ряда
BASE = [(450, "door"), (600, "drawers"), (600, "hob"), (600, "door"), (600, "drawers"), (800, "sink"), (150, "cargo")]
UPPER = [(520, "door"), (520, "door"), (640, "hood"), (530, "door"), (530, "door"), (530, "door"), (530, "door")]
XT = X0 + sum(w for w, _ in BASE)        # 4750 — начало пеналов справа
TALL = [(600, "glass"), (150, "cargo_tall")]
L = XT + sum(w for w, _ in TALL)         # 5500
assert sum(w for w, _ in UPPER) == sum(w for w, _ in BASE)

LDSP, MDF, HDF, ALU = "ЛДСП 16 белый", "МДФ 19 эмаль белая", "ХДФ 3 белый", "Алюм. рамка + стекло"
PARTS = []      # dict: name, mat, group, x0..z1
FACADES = []    # dict: module, x0, x1, z0, z1, mat, kind, y
MODULES = []    # (код, название, x0, x1, z0, z1, глубина)


def box(name, mat, group, x0, x1, y0, y1, z0, z1):
    PARTS.append(dict(name=name, mat=mat, group=group, x0=x0, x1=x1, y0=y0, y1=y1, z0=z0, z1=z1))


def carcass(code, x0, x1, z0, z1, d, bottom=True, top=True, shelves=0, rails=False):
    """Корпус: боковины, дно, крышка (или царги), полки."""
    box("Боковина", LDSP, code, x0, x0 + T, 0, d, z0, z1)
    box("Боковина", LDSP, code, x1 - T, x1, 0, d, z0, z1)
    if bottom:
        box("Дно", LDSP, code, x0 + T, x1 - T, 0, d, z0, z0 + T)
    if rails:
        box("Царга", LDSP, code, x0 + T, x1 - T, d - 100, d, z1 - T, z1)
        box("Царга", LDSP, code, x0 + T, x1 - T, 0, 100, z1 - T, z1)
    elif top:
        box("Крышка", LDSP, code, x0 + T, x1 - T, 0, d, z1 - T, z1)
    zb, zt = z0 + (T if bottom else 0), z1 - T
    for i in range(1, shelves + 1):
        z = zb + (zt - zb) * i / (shelves + 1)
        box("Полка", LDSP, code, x0 + T, x1 - T, 20, d - 20, z - T / 2, z + T / 2)


def facade(code, x0, x1, z0, z1, y, kind="door", mat=MDF):
    FACADES.append(dict(module=code, x0=x0 + GAP / 2, x1=x1 - GAP / 2, z0=z0, z1=z1, y=y, kind=kind, mat=mat))


# ---- пенал под холодильник (без дна, боковины до пола)
MODULES.append(("П1", "Пенал под холодильник 900 (без дна)", 0, X0, 0, ZU1, DFR))
carcass("П1", 0, X0, 0, ZU1, DFR, bottom=False)
# ---- нижний ряд
DRAWERS = [(PL + 3, PL + 224), (PL + 256, PL + 478), (PL + 510, ZB - GOLA)]   # фасады ящиков между профилями Gola
x = X0
for i, (w, kind) in enumerate(BASE):
    code = f"Н{i+1}"
    names = {"door": "Шкаф нижний с дверью", "drawers": "Шкаф нижний, 3 ящика", "hob": "Шкаф под варочную панель",
             "sink": "Шкаф под мойку", "cargo": "Карго нижнее 150"}
    MODULES.append((code, f"{names[kind]} {w}", x, x + w, PL, ZB, DB))
    carcass(code, x, x + w, PL, ZB, DB, rails=True, shelves=1 if kind in ("door", "hob") else 0)
    yF = DB + GAP
    if kind == "drawers":
        for z0, z1 in DRAWERS:
            facade(code, x, x + w, z0, z1, yF, "drawer")
    elif kind == "sink":
        facade(code, x, x + w / 2, PL + 3, ZB - GOLA, yF)
        facade(code, x + w / 2, x + w, PL + 3, ZB - GOLA, yF)
    else:
        facade(code, x, x + w, PL + 3, ZB - GOLA, yF, "cargo" if kind == "cargo" else "door")
    x += w
box("Столешница (материал по выбору)", "Столешница 38", "top", X0, XT, 0, 600, ZB, ZB + CT)
box("Цоколь", "Цоколь ПВХ/МДФ белый", "plinth", X0, XT, DB - 60, DB - 44, 0, PL)
# ---- верхний ряд и антресоль над ним
x = X0
for i, (w, kind) in enumerate(UPPER):
    code = f"В{i+1}"
    MODULES.append((code, ("Шкаф под встраиваемую вытяжку " if kind == "hood" else "Шкаф верхний ") + str(w), x, x + w, ZU0, ZU1, DU))
    carcass(code, x, x + w, ZU0, ZU1, DU, bottom=kind != "hood", shelves=0 if kind == "hood" else 2)
    facade(code, x, x + w, ZU0, ZU1 - GAP, DU + GAP)
    x += w
# ---- пеналы справа
x = XT
for i, (w, kind) in enumerate(TALL):
    code = f"П{i+2}"
    MODULES.append((code, ("Пенал-витрина, стеклянные полки, подсветка " if kind == "glass" else "Пенал с высоким карго ") + str(w),
                    x, x + w, PL, ZU1, DTALL))
    carcass(code, x, x + w, PL, ZU1, DTALL)
    if kind == "glass":
        for k in range(1, 6):
            z = PL + T + (ZU1 - PL - 2 * T) * k / 6
            box("Полка стеклянная 8 мм", "Стекло 8 закалённое", code, x + T + 14, x + w - T - 14, 30, DTALL - 30, z - 4, z + 4)
        for xl in (x + T, x + w - T - 12):
            box("Профиль LED вертикальный", "LED", code, xl, xl + 12, DTALL - 60, DTALL - 48, PL + T + 20, ZU1 - T - 20)
        facade(code, x, x + w, PL + 3, ZU1 - GAP, DTALL + GAP, "glass", ALU)
    else:
        facade(code, x, x + w, PL + 3, ZU1 - GAP, DTALL + GAP, "cargo")
    x += w
box("Цоколь", "Цоколь ПВХ/МДФ белый", "plinth", XT, L, DTALL - 60, DTALL - 44, 0, PL)
# ---- антресоль по всей длине (отдельные корпуса 440 + фасады 444)
ANTR = [("А1", 0, X0, DFR, 2)] + \
       [(f"А{i+2}", X0 + sum(u[0] for u in UPPER[:i]), X0 + sum(u[0] for u in UPPER[:i + 1]), DU, 1) for i in range(len(UPPER))] + \
       [("А9", XT, XT + 600, DTALL, 1), ("А10", XT + 600, L, DTALL, 1)]
for code, a, b, d, n in ANTR:
    MODULES.append((code, f"Антресоль {b-a}", a, b, ZU1, ZA1, d))
    carcass(code, a, b, ZU1, ZA1, d)
    for k in range(n):
        facade(code, a + (b - a) * k / n, a + (b - a) * (k + 1) / n, ZU1 + GAP, H - 3, d + GAP)
# ---- для наглядности (в спецификацию не входят)
CONTEXT = [
    dict(name="Холодильник 900 (отдельностоящий)", x0=25, x1=925, y0=20, y1=720, z0=0, z1=1800),
    dict(name="Варочная панель", x0=2030, x1=2570, y0=60, y1=580, z0=900, z1=906),
    dict(name="Мойка", x0=3900, x1=4500, y0=80, y1=540, z0=880, z1=901),
    dict(name="Вытяжка встраиваемая", x0=2010, x1=2610, y0=20, y1=330, z0=ZU0, z1=ZU0 + 40),
]


def size(p):
    d = sorted([p["x1"] - p["x0"], p["y1"] - p["y0"], p["z1"] - p["z0"]], reverse=True)
    return round(d[0]), round(d[1]), round(d[2])


def check():
    bad = 0
    for i, a in enumerate(PARTS):
        for b in PARTS[i + 1:]:
            if all(min(a[k + "1"], b[k + "1"]) - max(a[k + "0"], b[k + "0"]) > 0.5 for k in "xyz"):
                print("пересечение:", a["group"], a["name"], "/", b["group"], b["name"])
                bad += 1
    return bad


def spec():
    rows = {}
    for p in PARTS:
        if p["mat"] in (LDSP,):
            k = (p["name"], p["mat"]) + size(p)
            rows[k] = rows.get(k, 0) + 1
    return rows


def facade_spec():
    rows = {}
    for f in FACADES:
        k = (f["mat"], f["kind"], round(f["z1"] - f["z0"]), round(f["x1"] - f["x0"]))
        rows[k] = rows.get(k, 0) + 1
    return rows


if __name__ == "__main__":
    print("пересечений:", check(), " длина:", L)
    for m in MODULES:
        print(m)
    for k, n in sorted(facade_spec().items()):
        print(n, k)
    with open(os.path.join(HERE, "model.js"), "w") as f:
        f.write("window.PARTS = " + json.dumps(PARTS, ensure_ascii=False) + ";\n")
        f.write("window.FACADES = " + json.dumps(FACADES, ensure_ascii=False) + ";\n")
        f.write("window.CONTEXT = " + json.dumps(CONTEXT, ensure_ascii=False) + ";\n")
        f.write("window.DIM = " + json.dumps(dict(L=L, H=H, PL=PL, ZB=ZB, CT=CT, ZU0=ZU0, ZU1=ZU1, X0=X0, XT=XT, GOLA=GOLA)) + ";\n")
