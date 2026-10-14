#!/usr/bin/env python3
"""Подробная 3D-модель кухни (по деталировке): корпуса из панелей, фасады, техника, наполнение.

Оси: x – вдоль основной стены (0 – левый торец пенала), y – от стены в комнату, z – вверх.
Нижние и колонны: зазор 22 у стены, корпус 560, фасад 18 (плоскость фасадов y = 600 / x = 3400).
"""
import json
import os

from geom import *          # noqa: F403

HERE = os.path.dirname(os.path.abspath(__file__))
boxes, groups, cyls, cur = [], {}, [], [None]
T, HDF = 16, 3
Y0, Y1 = 22, 582             # корпус нижних
XF = CORNER_X[0]             # 3400 – плоскость фасадов правой стены
XC0, XC1 = XF + FT, XF + FT + 560     # корпус колонн по x: 3418…3978
UY0, UY1 = 0, 330            # верхние шкафы
COLORS = {"body": 0xf7f6f3, "back": 0xe4e1dc, "enamel": 0xffffff, "gola": 0x111111, "metal": 0x9a9da1,
          "steel": 0xc4c7ca, "alu": 0x2a2a2a, "glass": 0xcfe3ea, "plinth": 0x2b2b2b, "grill": 0x1a1a1a,
          "handle": 0xb9bcc0, "tap": 0xd0d3d6, "burner": 0x3a3a3a, "led": 0xffd36b, "duct": 0xb0b0b0,
          "fridgeIn": 0xf7f7f7, "plate": 0xfafafa, "jar": 0xe8dcc2, "book": 0x6d7f8c, "dark": 0x222222,
          "floor": 0xb9a58c, "wall_back": 0xeeece8, "wall_right": 0xeeece8, "wall_left": 0xeeece8,
          "veg": 0x5d8a3a, "fruit": 0xd9822b, "board": 0xb08a5a}
EDGES = {"body": 0x9a948c, "enamel": 0xb5b0a8, "oak": 0x7a5a3a}
WOODK = ["oak", "board"]


def box(x0, x1, y0, y1, z0, z1, kind):
    b = [round(x0), round(x1), round(y0), round(y1), round(z0), round(z1), kind]
    if cur[0]:
        b.append(cur[0])
    boxes.append(b)


def cyl(cx, cy, r, z0, z1, kind):
    cyls.append([round(cx), round(cy), round(r), round(z0), round(z1), kind, 0])


def group(gid, **meta):
    groups[gid] = meta
    cur[0] = gid


def end():
    cur[0] = None


# ---------------------------------------------------------------- нижние модули
def base_carcass(x0, x1, rails=True, back=True):
    box(x0, x0 + T, Y0, Y1 - 3, PL, CB, "body")
    box(x1 - T, x1, Y0, Y1 - 3, PL, CB, "body")
    box(x0 + T, x1 - T, Y0, Y1 - 3, PL, PL + T, "body")
    if rails:
        box(x0 + T, x1 - T, Y0, Y0 + 100, CB - T, CB, "body")
    box(x0 + T, x1 - T, Y1 - 160, Y1 - 60, CB - T - 40, CB - 40, "body")      # передняя царга за Gola
    if back:
        box(x0 + 2, x1 - 2, Y0 - HDF, Y0, PL + 2, CB - 2, "back")
    # профиль Gola (верхний) – чёрный канал
    box(x0, x1, Y1 - 40, Y1, GOLA_TOP[0], CB, "gola")


def drawer(gid, x0, x1, z0, z1, h, name, contents=0):
    """Ящик Firmax: фасад эмаль + металлические борта, дно, задняя стенка."""
    group(gid, set="drawers", name=name, dir=[0, 1], travel=430)
    box(x0 + 1, x1 - 1, Y1, Y1 + FT, z0, z1, "enamel")
    zb = z0 + 30
    box(x0 + T + 6, x0 + T + 22, Y1 - 500, Y1, zb, zb + h, "metal")
    box(x1 - T - 22, x1 - T - 6, Y1 - 500, Y1, zb, zb + h, "metal")
    box(x0 + T + 22, x1 - T - 22, Y1 - 500, Y1 - 484, zb, zb + h - 20, "body")
    box(x0 + T + 22, x1 - T - 22, Y1 - 500, Y1, zb, zb + 16, "body")
    if contents == 1:          # кастрюли
        for k, (dx, r) in enumerate(((150, 110), (390, 95))):
            cyl(x0 + dx, Y1 - 250, r, zb + 16, zb + 16 + 150 - k * 30, "steel")
        cyls[-1].append(gid); cyls[-2].append(gid)
    elif contents == 2:        # приборы – лоток
        box(x0 + 60, x1 - 60, Y1 - 470, Y1 - 40, zb + 16, zb + 60, "dark")
        for k in range(5):
            box(x0 + 90 + k * 90, x0 + 110 + k * 90, Y1 - 440, Y1 - 120, zb + 60, zb + 66, "steel")
    end()


def base_drawers(x0, x1, idx, hob=False, inner=False):
    base_carcass(x0, x1)
    box(x0, x1, Y1 - 40, Y1, GOLA_MID[0], GOLA_MID[1], "gola")
    drawer(f"dl{idx}", x0, x1, DR_LOW[0] + 1, DR_LOW[1] - 1, 210, "Ящик нижний (Firmax Smartline)", 1)
    drawer(f"du{idx}", x0, x1, DR_UP[0] + 1, DR_UP[1] - 1, 110 if not hob else 90,
           "Ящик верхний" + (" + скрытый внутренний ящик" if inner else ""), 2)
    if inner:      # внутренний ящик – внутри верхнего (видна лицевая панель при открывании)
        cur[0] = f"du{idx}"
        box(x0 + T + 24, x1 - T - 24, Y1 - 60, Y1 - 44, DR_UP[0] + 40, DR_UP[0] + 130, "body")
        cur[0] = None


def dishwasher(x0, x1):
    # корпус ПММ (нерж.) – открытый спереди, внутри 2 корзины
    box(x0 + 2, x0 + 4, Y0 + 10, Y1, PL, GOLA_TOP[0], "steel")
    box(x1 - 4, x1 - 2, Y0 + 10, Y1, PL, GOLA_TOP[0], "steel")
    box(x0 + 4, x1 - 4, Y0 + 10, Y0 + 12, PL, GOLA_TOP[0], "steel")
    box(x0 + 4, x1 - 4, Y0 + 10, Y1, GOLA_TOP[0] - 4, GOLA_TOP[0], "steel")
    box(x0 + 4, x1 - 4, Y0 + 10, Y1, PL, PL + 4, "steel")
    for z in (220, 520):
        box(x0 + 30, x1 - 30, Y0 + 40, Y1 - 30, z, z + 8, "metal")
        for k in range(6):
            box(x0 + 60 + k * 85, x0 + 66 + k * 85, Y0 + 60, Y1 - 60, z + 8, z + 160, "plate")
    box(x0, x1, Y1 - 40, Y1, GOLA_TOP[0], CB, "gola")
    group("dw", set="tech", name="Посудомоечная машина 600 (откидная дверь)", type="flap", pivot=[Y1, PL + 4], angle=88)
    box(x0 + 1, x1 - 1, Y1, Y1 + FT, PL + 4, GOLA_TOP[0] - 1, "enamel")
    box(x0 + 10, x1 - 10, Y1 - 50, Y1, PL + 20, GOLA_TOP[0] - 20, "steel")
    end()


def sink(x0, x1):
    box(x0, x0 + T, Y0, Y1 - 3, PL, CB, "body")
    box(x1 - T, x1, Y0, Y1 - 3, PL, CB, "body")
    box(x0 + T, x1 - T, Y0, Y1 - 3, PL, PL + T, "body")
    box(x0 + T, x1 - T, Y1 - 160, Y1 - 60, CB - T - 40, CB - 40, "body")
    box(x0 + 2, x1 - 2, Y0 - HDF, Y0, PL + 2, PL + 300, "back")
    box(x0, x1, Y1 - 40, Y1, GOLA_TOP[0], CB, "gola")
    # чаша, сифон
    sx0, sx1, sy0, sy1 = 2950, 3250, 120, 480
    box(sx0, sx1, sy0, sy1, 690, 700, "steel")
    for a in ((sx0, sx0 + 2, sy0, sy1), (sx1 - 2, sx1, sy0, sy1), (sx0, sx1, sy0, sy0 + 2), (sx0, sx1, sy1 - 2, sy1)):
        box(*a, 700, TOP - 2, "steel")
    cyl((sx0 + sx1) / 2, 300, 25, 450, 690, "metal")
    cyl((sx0 + sx1) / 2, 300, 22, 400, 450, "dark")
    # смеситель
    cyl(3310, 540 - 400, 28, TOP, TOP + 40, "tap")
    cyl(3310, 140, 14, TOP + 40, TOP + 300, "tap")
    box(3200, 3324, 132, 148, TOP + 280, TOP + 300, "tap")
    hx = x0 + 1 if SINK_HINGE_LEFT else x1 - 1
    group("sinkdoor", set="doors", name="Дверь под мойку", type="hinge", pivot=[hx, Y1],
          angle=-100 if SINK_HINGE_LEFT else 100)
    box(x0 + 1, x1 - 1, Y1, Y1 + FT, PL + 2, GOLA_TOP[0] - 1, "enamel")
    end()


# ---------------------------------------------------------------- верхние
def upper(x0, x1, kind, hinge_left):
    z0, z1 = UB, H
    box(x0, x0 + T, UY0, UY1, z0, z1, "body")
    box(x1 - T, x1, UY0, UY1, z0, z1, "body")
    box(x0 + T, x1 - T, UY0, UY1, z0, z0 + T, "body")
    box(x0 + T, x1 - T, UY0, UY1, z1 - T, z1, "body")
    box(x0 + 2, x1 - 2, UY0 - HDF, UY0, z0 + 2, z1 - 2, "back")
    box(x0 + T, x1 - T, UY1 - 40, UY1 - 22, z0 - 6, z0, "led")              # подсветка под шкафом
    if kind == "door":
        for z in UP_SHELVES:
            box(x0 + T + 1, x1 - T - 1, UY0 + 10, UY1 - 20, z, z + T, "body")
        for k in range(3):                                                  # тарелки, банки
            cyl(x0 + 120 + k * 170, 160, 75, UP_SHELVES[0] + T, UP_SHELVES[0] + T + 70 + k * 25, "plate" if k != 1 else "jar")
            cyl(x0 + 120 + k * 170, 160, 55, UP_SHELVES[1] + T, UP_SHELVES[1] + T + 120, "jar")
    elif kind == "hood":
        box(x0 + T + 1, x1 - T - 1, UY0 + 10, UY1 - 20, 2000, 2000 + T, "body")
        box(x0 + 30, x1 - 30, 20, UY1 - 10, z0 - 60, z0 + 120, "steel")       # блок вытяжки
        box(x0 + 40, x1 - 40, UY1 - 10, UY1 + 10, z0 - 60, z0 - 20, "steel")  # козырёк
        box(x0 + 240, x0 + 360, 60, 200, z0 + 120, z1, "duct")              # воздуховод
    elif kind == "dry":
        box(x0 + T + 1, x1 - T - 1, UY0 + 10, UY1 - 20, DRY_SHELF, DRY_SHELF + T, "body")
        box(x0 + T + 4, x1 - T - 4, 20, UY1 - 20, z0 + T, z0 + T + 10, "steel")    # поддон
        for zr, h in ((z0 + 80, 160), (z0 + 420, 120)):
            box(x0 + T + 4, x1 - T - 4, 40, UY1 - 30, zr, zr + 6, "metal")
            for k in range(9):
                box(x0 + 50 + k * 58, x0 + 54 + k * 58, 60, UY1 - 50, zr + 6, zr + 6 + 60, "metal")
                box(x0 + 52 + k * 58, x0 + 62 + k * 58, 90, UY1 - 80, zr + 6, zr + 6 + h, "plate")
    a = x0 + 1 if hinge_left else x1 - 1
    group(f"up{x0}", set="doors", name={"door": "Верхний шкаф (2 полки)", "hood": "Шкаф со встроенной вытяжкой",
                                        "dry": "Шкаф-сушка"}[kind],
          type="hinge", pivot=[a, UY1], angle=-100 if hinge_left else 100)
    box(x0 + 1, x1 - 1, UY1, UY1 + FT, z0 + 1, z1 - 1, "enamel")
    end()


# ---------------------------------------------------------------- пенал-витрина
def pencil():
    x0, x1 = PENCIL[0] + 18, PENCIL[1]
    box(PENCIL[0], PENCIL[0] + 18, 0, 600, 0, H, "enamel")                 # декоративная боковина
    box(x0, x0 + T, Y0, Y1 - 3, PL, H, "body")
    box(x1 - T, x1, Y0, Y1 - 3, PL, H, "body")
    for z in (PL, 1300 - T, H - T):
        box(x0 + T, x1 - T, Y0, Y1 - 3, z, z + T, "body")
    box(x0 + 2, x1 - 2, Y0 - HDF, Y0, PL + 2, H - 2, "back")
    box(x0 + 40, x1 - 40, Y1 - 120, Y1 - 104, 0, PL - 2, "plinth")
    for z in PENCIL_SHELVES:
        box(x0 + T + 1, x1 - T - 1, Y0 + 20, Y1 - 30, z, z + 6, "glassShelf")
        for k in range(2):
            cyl(x0 + 110 + k * 160, 300, 50, z + 6, z + 6 + 110 + (z % 3) * 30, "jar" if (z + k) % 2 else "plate")
    box(x0 + T, x0 + T + 8, Y1 - 60, Y1 - 50, PL + T, H - T, "led")           # вертикальная подсветка
    for i, (z0, z1) in enumerate(((PL + 2, 1298), (1302, H - 2))):
        group(f"pen{i}", set="doors", name="Пенал-витрина: стекло в алюминиевой раме", type="hinge",
              pivot=[x0 + 1, Y1], angle=-100)
        xa, xb = x0 + 1, x1 - 1
        for a in ((xa, xa + 20, z0, z1), (xb - 20, xb, z0, z1), (xa, xb, z0, z0 + 20), (xa, xb, z1 - 20, z1)):
            box(a[0], a[1], Y1, Y1 + 20, a[2], a[3], "alu")
        box(xa + 20, xb - 20, Y1 + 8, Y1 + 12, z0 + 20, z1 - 20, "glass")
        end()


# ---------------------------------------------------------------- правая стена
def column(y0, y1):
    box(XC0, XC1, y0, y0 + T, PL, H, "body")
    box(XC0, XC1, y1 - T, y1, PL, H, "body")
    box(XC0, XC1, y0 + T, y1 - T, PL, PL + T, "body")
    box(XC0, XC1, y0 + T, y1 - T, H - T, H, "body")
    box(XC1, XC1 + HDF, y0 + 2, y1 - 2, PL + 2, H - 2, "back")
    box(XF + 40, XF + 56, y0, y1, 0, PL - 2, "plinth")
    box(XF + 38, XF + 40, y0 + 150, y1 - 150, 25, 75, "grill")


def fridge_col():
    y0, y1 = FRIDGE_Y
    column(y0, y1)
    box(XC0, XC1, y0 + T, y1 - T, FR_SHELF, FR_SHELF + T, "body")          # полка над холодильником
    # холодильник: камера (белая) с полками
    fx0, fx1 = XC0 + 50, XC1 - 20
    box(fx1 - 10, fx1, y0 + 30, y1 - 30, PL + 20, FR_SHELF - 10, "fridgeIn")
    box(fx0, fx1, y0 + 30, y0 + 40, PL + 20, FR_SHELF - 10, "fridgeIn")
    box(fx0, fx1, y1 - 40, y1 - 30, PL + 20, FR_SHELF - 10, "fridgeIn")
    box(fx0, fx1, y0 + 30, y1 - 30, PL + 20, PL + 30, "fridgeIn")
    box(fx0, fx1, y0 + 30, y1 - 30, 820, 840, "fridgeIn")                     # разделитель морозилки
    box(fx0, fx1, y0 + 30, y1 - 30, FR_SHELF - 20, FR_SHELF - 10, "fridgeIn")
    for z in (1150, 1450, 1750):
        box(fx0 + 10, fx1 - 10, y0 + 40, y1 - 40, z, z + 6, "glassShelf")
    for k, z in enumerate((1156, 1456, 1756)):
        cyl(fx0 + 200, 900 + (k - 1) * 120, 60, z, z + 140, "fruit" if k == 1 else "veg")
    box(fx0 + 30, fx1 - 60, y0 + 60, y1 - 60, 300, 420, "fridgeIn")            # ящики морозилки
    box(fx0 + 30, fx1 - 60, y0 + 60, y1 - 60, 560, 700, "fridgeIn")
    for i, (z0, z1, nm) in enumerate(((FR_LOW[0], FR_LOW[1], "Холодильник: морозильная камера (фасад шпон)"),
                                      (FR_UP[0] - 2, H - 2, "Холодильник: фасад цельный 1680 (шпон)"))):
        group(f"fr{i}", set="tech", name=nm, type="hinge", pivot=[XF, y1 - 1], angle=95)
        box(XF, XF + FT, y0 + 1, y1 - 1, z0, z1, "oak")
        dz1 = min(z1, FR_SHELF - 20) if i else z1
        box(XF + FT, XF + 60, y0 + 30, y1 - 30, z0 + 20, dz1 - 20, "fridgeIn")    # дверь холодильника
        for z in range(z0 + 150, dz1 - 100, 300):
            box(XF + 60, XF + 110, y0 + 60, y1 - 60, z, z + 60, "fridgeIn")       # полки двери
        end()


def oven_col():
    y0, y1 = OVEN_Y
    column(y0, y1)
    for z in (OV_GOLA[1] - T, 1200 - T, MW[1] - T + 16):
        box(XC0, XC1, y0 + T, y1 - T, z, z + T, "body")
    for z in OV_SHELVES:
        box(XC0 + 20, XC1, y0 + T + 1, y1 - T - 1, z, z + T, "body")
        cyl(XC0 + 250, (y0 + y1) / 2, 90, z + T, z + T + 160, "jar")
    box(XF, XF + 30, y0, y1, OV_GOLA[0], OV_GOLA[1], "gola")
    # духовка
    box(XF - 2, XF + 20, y0 + 3, y1 - 3, OVEN[0] + 2, OVEN[1], "ovenglass")
    box(XF + 20, XC1 - 20, y0 + 20, y1 - 20, OVEN[0] + 2, OVEN[1] - 2, "dark")
    box(XF - 30, XF - 2, y0 + 80, y1 - 80, OVEN[1] - 70, OVEN[1] - 56, "handle")
    box(XF - 3, XF - 2, y0 + 80, y1 - 80, OVEN[1] - 40, OVEN[1] - 10, "steel")
    # СВЧ
    box(XF - 2, XF + 20, y0 + 3, y1 - 3, MW[0] + 2, MW[1] - 2, "ovenglass")
    box(XF + 20, XC1 - 150, y0 + 20, y1 - 20, MW[0] + 2, MW[1] - 2, "dark")
    box(XF - 4, XF - 2, y1 - 150, y1 - 30, MW[0] + 60, MW[1] - 60, "steel")
    # ящик под духовкой
    group("ovdrw", set="drawers", name="Ящик под духовкой (Firmax, фасад шпон)", dir=[-1, 0], travel=430)
    box(XF, XF + FT, y0 + 1, y1 - 1, OV_DRW[0] + 1, OV_DRW[1] - 1, "oak")
    zb = OV_DRW[0] + 30
    box(XF + FT, XF + FT + 500, y0 + T + 6, y0 + T + 22, zb, zb + 220, "metal")
    box(XF + FT, XF + FT + 500, y1 - T - 22, y1 - T - 6, zb, zb + 220, "metal")
    box(XF + FT, XF + FT + 500, y0 + T + 22, y1 - T - 22, zb, zb + 16, "body")
    box(XF + FT + 484, XF + FT + 500, y0 + T + 22, y1 - T - 22, zb, zb + 200, "body")
    for k in range(3):
        box(XF + 80 + k * 140, XF + 200 + k * 140, y0 + 100, y1 - 100, zb + 16, zb + 40 + k * 10, "dark")
    end()
    group("ovdoor", set="doors", name="Шкаф над СВЧ (цельный фасад 920, шпон)", type="hinge", pivot=[XF, y1 - 1], angle=100)
    box(XF, XF + FT, y0 + 1, y1 - 1, OV_DOOR[0] - 2, H - 2, "oak")
    end()


def corner_upper():
    y0, y1 = CORNER_FILL, 600
    box(XC0, XC1, y0, y0 + T, UB, H, "body")
    box(XC0, XC1, y1 - T, y1, UB, H, "body")
    box(XC0, XC1, y0 + T, y1 - T, UB, UB + T, "body")
    box(XC0, XC1, y0 + T, y1 - T, H - T, H, "body")
    box(XC1, XC1 + HDF, y0 + 2, y1 - 2, UB + 2, H - 2, "back")
    for z in UP_SHELVES:
        box(XC0 + 20, XC1, y0 + T + 1, y1 - T - 1, z, z + T, "body")
        for k in range(2):
            cyl(XC0 + 250, y0 + 150 + k * 250, 70, z + T, z + T + 100, "plate")
    box(XF, XF + FT, 0, y0, UB, H, "oak")                                     # планка 20
    box(XF + FT, XC0 + 30, 0, 50, UB, H, "body")
    box(XC0, XC0 + 18, y0 + T, y1 - T, UB - 6, UB, "led")
    group("cup", set="doors", name="Угловой верхний шкаф 580 (шпон)", type="hinge", pivot=[XF, y0 + 1], angle=-100)
    box(XF, XF + FT, y0 + 1, y1 - 1, UB + 1, H - 1, "oak")
    end()


def build():
    # комната
    box(-900, WM + 100, -100, 0, 0, HT, "wall_back")
    box(WM, WM + 100, -100, 3200, 0, HT, "wall_right")
    box(-900, WM + 100, -100, 3200, -30, 0, "floor")
    # фартук – плитка
    box(PENCIL[1], XF, -2, 0, TOP, UB, "tile")
    box(GAP_UP[0], XF, -2, 0, UB, H, "tile")
    box(WM - 2, WM, 0, 600, TOP, UB, "tile")
    pencil()
    for i, (x0, x1, kind) in enumerate(BASES):
        if kind == "dw":
            dishwasher(x0, x1)
        elif kind == "sink":
            sink(x0, x1)
        else:
            base_drawers(x0, x1, i, hob=(kind == "hob"), inner=(kind == "drw2"))
    box(PENCIL[1], XF, Y1 - 120, Y1 - 104, 0, PL - 2, "plinth")
    # глухой угол: стойка-опора
    box(XF + 200, XF + 216, Y0, Y1, PL, CB, "body")
    # столешница с вырезом под мойку
    sx0, sx1, sy0, sy1 = 2950, 3250, 120, 480
    for a in ((PENCIL[1], sx0, 0, 600), (sx1, WM, 0, 600), (sx0, sx1, 0, sy0), (sx0, sx1, sy1, 600)):
        box(a[0], a[1], a[2], a[3], CB, TOP, "stone")
    # варочная панель
    hx0, hx1 = HOB_X
    box(hx0 + 30, hx1 - 30, 50, 560, TOP, TOP + 6, "hobglass")
    for cx, cy, r in ((hx0 + 160, 180, 95), (hx0 + 440, 180, 75), (hx0 + 160, 430, 75), (hx0 + 440, 430, 95)):
        cyl(cx, cy, r, TOP + 6, TOP + 7, "burner")
    box(hx0 + 220, hx1 - 220, 520, 545, TOP + 6, TOP + 7, "steel")
    # декор на столешнице
    box(1750, 2150, 80, 330, TOP, TOP + 25, "board")
    cyl(2350, 200, 80, TOP, TOP + 210, "steel")
    cyl(650, 250, 140, TOP, TOP + 90, "plate")
    for k in range(3):
        cyl(600 + k * 60, 240, 35, TOP + 90, TOP + 150, "fruit")
    # верхние
    for i, (x0, x1, kind) in enumerate(UPPERS):
        upper(x0, x1, kind, hinge_left=UP_HINGE_LEFT[i])
    # правая стена
    fridge_col()
    oven_col()
    corner_upper()
    box(XF, WM, OVEN_Y[1], OVEN_Y[1] + 18, 0, H, "oak")                      # торец – шпон
    box(XF + 40, XF + 56, 600, 1800, 0, PL - 2, "plinth")
    # планки 130
    box(PENCIL[0], PENCIL[1], 582, 600, H, HT, "enamel")
    box(PENCIL[1], PENCIL[1] + 16, UY1 + FT, 600, H, HT, "enamel")
    box(PENCIL[1], STRIP_END, UY1, UY1 + FT, H, HT, "enamel")
    box(STRIP_END - 16, STRIP_END, 0, UY1, H, HT, "enamel")
    box(XF, XF + FT, 0, OVEN_Y[1] + 18, H, HT, "oak")
    box(XF + FT, WM, OVEN_Y[1], OVEN_Y[1] + 18, H, HT, "oak")


def data():
    build()
    return {"room": [WM, 2400, HT], "boxes": boxes, "groups": groups, "cyls": cyls, "cloth": [],
            "colors": COLORS, "edges": EDGES, "wood": WOODK, "woodTex": ["#c9a376", "120,84,48"],
            "sets": [["doors", "Двери"], ["drawers", "Ящики"], ["tech", "Техника"]],
            "lights": [[700, 250, 1450], [1600, 250, 1450], [2500, 250, 1450], [3100, 300, 2200]]}


if __name__ == "__main__":
    d = data()
    print(len(d["boxes"]), "boxes,", len(d["cyls"]), "cyls,", len(d["groups"]), "groups")
