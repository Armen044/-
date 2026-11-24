#!/usr/bin/env python3
"""Кухня по рендеру и эскизу заказчика (вариант 2). Размеры в мм.

Оси: X — вдоль стены слева направо, Y — от стены (0) к фасадам, Z — вверх. Потолок 3000.
Слева направо (сумма ширин 5650; на рендере подписано 5,60 м — сверить с замером):
  0,95 холодильник (пенал без дна, боковины до пола) | 0,45 шкаф | 0,60 ящики | 0,60 духовка + варочная |
  0,60 посудомойка | 0,60 ящики | 0,80 мойка | 0,15 бутылочница (под столешницей) |
  0,60 стеклянный шкаф с подсветкой | 0,30 шкаф под специи (внутренние ящики Blum MERIVOBOX).
Шкафы с ящиками: один профиль Gola C посередине; внизу большой ящик (открывается через C), вверху 2 ящика
друг над другом без профиля между ними: верхний — через Gola L, второй — через C (за нижний край).
Верхний ряд: шкафы 1050 + антресоль 450 (525 · 525 · проём 600 под вытяжку · 4 × 537,5).
Фасады: нижний и верхний ряд — МДФ эмаль белая (покраска с двух сторон), ручка Gola;
пеналы и антресоль — МДФ шпон американского ореха, торцевая ручка из массива ореха.
Фурнитура Blum: ящики MERIVOBOX, петли CLIP top BLUMOTION, подъёмники AVENTOS HK top, TIP-ON.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
H = 3000
T, FD, GAP = 16, 19, 3
PL = 100
ZB = 862                      # верх нижних корпусов (+ столешница 38 = 900)
CT = 38
ZU0, ZU1 = 1500, 2550
ZA1 = 2990
DB, DU, DTALL, DFR = 560, 350, 580, 700
GOLA = 30
ENAMEL, WALNUT, ALU = "МДФ 19 эмаль белая (2 стороны)", "МДФ 19 шпон ам. ореха", "Алюм. рамка + стекло"
LDSP_W, LDSP_N, SIDE_W = "ЛДСП 16 белый", "ЛДСП 16 орех (в тон)", "МДФ 19 шпон ам. ореха (видимая боковина)"

X0 = 950
BASE = [(450, "door"), (600, "drawers"), (600, "oven"), (600, "dw"), (600, "drawers"), (800, "sink"), (150, "bottle")]
XT = X0 + sum(w for w, _ in BASE)                 # 4750
UPPER = [(525, "door"), (525, "door"), (600, "hood"), (537.5, "door"), (537.5, "door"), (537.5, "door"), (537.5, "door")]
TALL = [(600, "glass"), (300, "spice")]
L = XT + sum(w for w, _ in TALL)                  # 5650
assert sum(w for w, _ in UPPER) == XT - X0

PARTS, FACADES, MODULES, CONTEXT = [], [], [], []


def box(name, mat, group, x0, x1, y0, y1, z0, z1):
    PARTS.append(dict(name=name, mat=mat, group=group, x0=x0, x1=x1, y0=y0, y1=y1, z0=z0, z1=z1))


def carcass(code, x0, x1, z0, z1, d, mat=LDSP_W, bottom=True, top=True, rails=False, shelves=(), back=True,
            lside=None, rside=None):
    tl = FD if lside else T
    tr = FD if rside else T
    box("Боковина", lside or mat, code, x0, x0 + tl, 0, d, z0, z1)
    box("Боковина", rside or mat, code, x1 - tr, x1, 0, d, z0, z1)
    a, b = x0 + tl, x1 - tr
    if bottom:
        box("Дно", mat, code, a, b, 0, d, z0, z0 + T)
    if rails:
        box("Царга", mat, code, a, b, d - 100, d, z1 - T, z1)
        box("Царга", mat, code, a, b, 0, 100, z1 - T, z1)
    elif top:
        box("Крышка", mat, code, a, b, 0, d, z1 - T, z1)
    for z in shelves:
        box("Полка", mat, code, a, b, 20, d - 20, z, z + T)
    if back:
        PARTS.append(dict(name="Задняя стенка ХДФ 3", mat="ХДФ 3", group=code, x0=a, x1=b, y0=-3, y1=0, z0=z0, z1=z1, thin=True))


def facade(code, x0, x1, z0, z1, y, kind, mat):
    FACADES.append(dict(module=code, x0=x0 + GAP / 2, x1=x1 - GAP / 2, z0=z0, z1=z1, y=y, kind=kind, mat=mat))


# ---- холодильник: боковины до пола (шпон), без дна, крышка
MODULES.append(("П1", "Пенал под холодильник (без дна, боковины до пола)", 0, X0, 0, ZU1, DFR, "шпон"))
carcass("П1", 0, X0, 0, ZU1, DFR, mat=LDSP_N, bottom=False, back=False, lside=SIDE_W, rside=SIDE_W)
CONTEXT.append(dict(name="Холодильник 900 (отдельностоящий)", x0=X0 / 2 - 450, x1=X0 / 2 + 450, y0=20, y1=730, z0=0, z1=1800, c="black"))
# ---- нижний ряд
ZC = 451                                # верх нижнего ящика; над ним профиль Gola C (32)
DR_LOW = (PL + 3, ZC)
DR_MID = (ZC + 32, ZC + 32 + 173)
DR_TOP = (ZC + 32 + 176, ZB - GOLA)
OVEN_Z0 = 235                          # низ ниши духовки (духовка 595 → верх 830)
x = X0
for i, (w, kind) in enumerate(BASE):
    code = f"Н{i+1}"
    yF = DB + GAP
    if kind == "dw":
        MODULES.append((code, "Посудомойка встраиваемая 600 (без корпуса, фасад на дверь ПММ)", x, x + w, PL, ZB, DB, "эмаль"))
        facade(code, x, x + w, PL + 3, ZB - GOLA, yF, "dw", ENAMEL)
        CONTEXT.append(dict(name="Посудомоечная машина 600", x0=x + 2, x1=x + w - 2, y0=10, y1=DB, z0=PL - 20, z1=ZB - 40, c="steel"))
        box("Планка пароизоляции под столешницей", "Алюм. фольга / планка", code, x + 2, x + w - 2, 0, DB, ZB - 2, ZB)
        x += w
        continue
    names = {"door": "Шкаф нижний, дверь", "drawers": "Шкаф нижний, 3 ящика MERIVOBOX",
             "oven": "Шкаф под духовку + варочную, нижний ящик", "sink": "Шкаф под мойку, 2 двери",
             "bottle": "Бутылочница (карго) под столешницей"}
    MODULES.append((code, f"{names[kind]} {w}", x, x + w, PL, ZB, DB, "эмаль"))
    if kind == "oven":
        carcass(code, x, x + w, PL, ZB, DB, rails=True, back=False, shelves=(OVEN_Z0 - T,))
        facade(code, x, x + w, PL + 3, OVEN_Z0 - 3, yF, "drawer", ENAMEL)
        CONTEXT.append(dict(name="Духовой шкаф 600", x0=x + 2, x1=x + w - 2, y0=20, y1=DB + 22, z0=OVEN_Z0, z1=OVEN_Z0 + 595, c="black"))
        CONTEXT.append(dict(name="Варочная панель", x0=x + 30, x1=x + w - 30, y0=60, y1=580, z0=900, z1=906, c="black"))
    elif kind == "drawers":
        carcass(code, x, x + w, PL, ZB, DB, rails=True)
        for zz in (DR_LOW, DR_MID, DR_TOP):
            facade(code, x, x + w, *zz, yF, "drawer", ENAMEL)
    elif kind == "sink":
        carcass(code, x, x + w, PL, ZB, DB, rails=True, back=False)
        facade(code, x, x + w / 2, PL + 3, ZB - GOLA, yF, "door", ENAMEL)
        facade(code, x + w / 2, x + w, PL + 3, ZB - GOLA, yF, "door", ENAMEL)
        CONTEXT.append(dict(name="Мойка", x0=x + 120, x1=x + w - 120, y0=80, y1=540, z0=880, z1=901, c="steel"))
    elif kind == "bottle":
        carcass(code, x, x + w, PL, ZB, DB, rails=True)
        facade(code, x, x + w, PL + 3, ZB - GOLA, yF, "cargo", ENAMEL)
    else:
        carcass(code, x, x + w, PL, ZB, DB, rails=True, shelves=((PL + ZB) / 2,))
        facade(code, x, x + w, PL + 3, ZB - GOLA, yF, "door", ENAMEL)
    x += w
box("Столешница (искусств. камень, напр. Corian)", "Столешница 38", "top", X0, XT, 0, 600, ZB, ZB + CT)
box("Цоколь", "Цоколь МДФ эмаль", "plinth", X0, XT, DB - 60, DB - 44, 0, PL)
# ---- верхний ряд
x = X0
for i, (w, kind) in enumerate(UPPER):
    code = f"В{i+1}"
    if kind == "hood":
        MODULES.append((code, "Проём под каминную вытяжку 600 (до потолка)", x, x + w, ZU0, H, 0, "—"))
        CONTEXT.append(dict(name="Вытяжка каминная (цилиндр)", x0=x + 150, x1=x + w - 150, y0=100, y1=400, z0=ZU0 + 50, z1=H, c="black", round=True))
        x += w
        continue
    if kind == "open":
        MODULES.append((code, f"Открытая полка {w}, шпон ореха", x, x + w, ZU0, ZU1, DU, "шпон"))
        carcass(code, x, x + w, ZU0, ZU1, DU, mat=SIDE_W, shelves=(1850, 2200), back=False, lside=SIDE_W, rside=SIDE_W)
        x += w
        continue
    MODULES.append((code, f"Шкаф верхний {w}, дверь на CLIP top + TIP-ON", x, x + w, ZU0, ZU1, DU, "эмаль"))
    carcass(code, x, x + w, ZU0, ZU1, DU, shelves=(1850, 2200))
    facade(code, x, x + w, ZU0, ZU1 - GAP, DU + GAP, "door", ENAMEL)
    x += w
# ---- пеналы справа (шпон, торцевая ручка из массива)
x = XT
for i, (w, kind) in enumerate(TALL):
    code = f"П{i+2}"
    rs = SIDE_W if i == len(TALL) - 1 else None
    if kind == "glass":
        MODULES.append((code, "Стеклянный шкаф 600: полки стекло 8 мм, LED по бокам", x, x + w, PL, ZU1, DTALL, "алюм."))
        carcass(code, x, x + w, PL, ZU1, DTALL, mat=LDSP_N, lside=SIDE_W)
        for k in range(1, 6):
            z = PL + T + (ZU1 - PL - 2 * T) * k / 6
            box("Полка стеклянная 8 мм", "Стекло 8 закалённое", code, x + FD + 14, x + w - T - 14, 30, DTALL - 30, z - 4, z + 4)
        for xl in (x + FD, x + w - T - 12):
            box("Профиль LED вертикальный", "LED", code, xl, xl + 12, DTALL - 60, DTALL - 48, PL + T + 20, ZU1 - T - 20)
        facade(code, x, x + w, PL + 3, ZU1 - GAP, DTALL + GAP, "glass", ALU)
    else:
        MODULES.append((code, "Шкаф под специи 300: 6 внутренних ящиков MERIVOBOX + полки", x, x + w, PL, ZU1, DTALL, "шпон"))
        carcass(code, x, x + w, PL, ZU1, DTALL, mat=LDSP_N, shelves=(1760, 2150), rside=rs)
        facade(code, x, x + w, PL + 3, ZU1 - GAP, DTALL + GAP, "door", WALNUT)
    x += w
box("Цоколь", "Цоколь шпон ореха", "plinth", XT, L, DTALL - 60, DTALL - 44, 0, PL)
# внутренние ящики пенала специй: дистанционные планки 16 мм по боковинам, чтобы ящики проходили мимо петель
xs0, xs1 = XT + 600, L
INNER = []
for k in range(6):
    z0 = PL + T + 40 + k * 260
    INNER.append((z0, z0 + 160))
for xsp in (xs0 + T, xs1 - FD - 16):
    box("Дистанционная планка 16", LDSP_N, "П3", xsp, xsp + 16, 0, DTALL - 40, PL + T, 1700)
for z0, z1 in INNER:
    box("Внутренний ящик MERIVOBOX (условно)", "Ящик", "П3", xs0 + T + 16 + 13, xs1 - FD - 16 - 13, 40, DTALL - 50, z0, z1)
# ---- антресоль: шпон ореха; над вытяжкой — реечная панель на стене
ANTR = [("А1", 0, X0, DFR, 2), ("А2", X0, X0 + 1050, DU, 2), ("А3", X0 + 1650, XT, DU, 4),
        ("А4", XT, XT + 600, DTALL, 1), ("А5", XT + 600, L, DTALL, 1)]
for code, a, b, d, n in ANTR:
    MODULES.append((code, f"Антресоль {b-a}, AVENTOS HK top" if (b - a) / n >= 300 else f"Антресоль {b-a}, дверь", a, b, ZU1, ZA1, d, "шпон"))
    carcass(code, a, b, ZU1, ZA1, d, mat=LDSP_N, rside=SIDE_W if code == "А5" else None,
            lside=SIDE_W if code == "А1" else None)
    for k in range(n):
        facade(code, a + (b - a) * k / n, a + (b - a) * (k + 1) / n, ZU1 + GAP, H - 3, d + GAP, "lift" if (b - a) / n >= 300 else "door", WALNUT)


def size(p):
    d = sorted([p["x1"] - p["x0"], p["y1"] - p["y0"], p["z1"] - p["z0"]], reverse=True)
    return round(d[0]), round(d[1]), round(d[2])


def check():
    bad = 0
    pp = [p for p in PARTS if not p.get("thin")]
    for i, a in enumerate(pp):
        for b in pp[i + 1:]:
            if all(min(a[k + "1"], b[k + "1"]) - max(a[k + "0"], b[k + "0"]) > 0.5 for k in "xyz"):
                print("пересечение:", a["group"], a["name"], "/", b["group"], b["name"])
                bad += 1
    return bad


def spec():
    rows = {}
    for p in PARTS:
        if p["mat"] in (LDSP_W, LDSP_N, SIDE_W):
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
    for k, n in sorted(facade_spec().items()):
        print(n, k)
