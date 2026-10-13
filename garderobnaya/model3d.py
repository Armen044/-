#!/usr/bin/env python3
"""3D-модель гардеробной (набор параллелепипедов) -> model.js для view3d.html.

Оси: x – вдоль задней стены (0…2400, слева направо от входа),
y – от задней стены к входу (0…1740), z – вверх (0…2640).
"""
import json
import os

from generate import (T, H, W, D, DEPTH, PLINTH, ANT, RAIL, RAIL_LOW, B1, B2,
                      L1, L1E, LM, R1, SIDE, BOARD_L, BOARD_W, BOARD_T,
                      MIR_D, MIR_T, MIR_H, MIR_Z,
                      RACK_W, RACK_D, RACK_H, RACK_Z, RACK_TOP, RACK_SHELF, RACK_Y)

boxes = []
groups = {}             # подвижные части для интерактивной модели
cur = [None]            # текущая группа, к которой добавляются детали
CLOTH = ["#e9e5df", "#cfc8bf", "#b9b2aa", "#8d8680", "#f3f1ec", "#a39383", "#6f6a66", "#d8cdbf"]


def box(x0, x1, y0, y1, z0, z1, kind):
    b = [round(x0), round(x1), round(y0), round(y1), round(z0), round(z1), kind]
    if cur[0]:
        b.append(cur[0])
    boxes.append(b)


def group(gid, **meta):
    groups[gid] = meta
    cur[0] = gid


def end_group():
    cur[0] = None


def drawer_body(x0, x1, y0, y1, z0, z1, axis):
    """Корпус ящика (боковины, дно, задняя стенка); axis – ось выдвижения."""
    t = 12
    if axis == "y":
        box(x0, x0 + t, y0, y1, z0, z1, "dbox")
        box(x1 - t, x1, y0, y1, z0, z1, "dbox")
        box(x0, x1, y0, y0 + t, z0, z1, "dbox")
        box(x0, x1, y0, y1, z0, z0 + 8, "dbottom")
    else:
        box(x0, x1, y0, y0 + t, z0, z1, "dbox")
        box(x0, x1, y1 - t, y1, z0, z1, "dbox")
        box(x0, x0 + t, y0, y1, z0, z1, "dbox")
        box(x0, x1, y0, y1, z0, z0 + 8, "dbottom")


def clothes_x(x0, x1, yc, ztop, length, step=75):
    """Одежда на штанге, идущей вдоль x."""
    n = int((x1 - x0 - 40) / step)
    for i in range(n):
        x = x0 + 40 + i * step
        ln = length - (i * 97 % 3) * 60
        box(x, x + 28, yc - 220, yc + 220, ztop - ln, ztop - 30, "cloth%d" % (i * 5 % len(CLOTH)))


def clothes_y(y0, y1, xc, ztop, length, step=75):
    """Одежда на штанге, идущей вдоль y."""
    n = int((y1 - y0 - 40) / step)
    for i in range(n):
        y = y0 + 40 + i * step
        ln = length - (i * 97 % 3) * 60
        box(xc - 220, xc + 220, y, y + 28, ztop - ln, ztop - 30, "cloth%d" % (i * 3 % len(CLOTH)))


def drawers_side(y0, y1, xf, sign):
    """Ящики в боковой секции; xf – плоскость фасада, sign – направление в проход."""
    for i in range(4):
        zb = PLINTH + T + i * 200
        group("drw_s%d_%d" % (int(y0), i), type="drawer", dir=[sign, 0], travel=450)
        xa, xb = sorted((xf, xf - sign * 18))
        box(xa, xb, y0 + 2, y1 - 2, zb + 2, zb + 198, "front")
        cy = (y0 + y1) / 2
        xa, xb = sorted((xf, xf + sign * 12))
        box(xa, xb, cy - 90, cy + 90, zb + 125, zb + 137, "handle")
        xa, xb = sorted((xf - sign * 18, xf - sign * 518))
        drawer_body(xa, xb, y0 + 13, y1 - 13, zb + 25, zb + 165, "x")
        end_group()


def shoe_rack(cx, interactive):
    """Обувница ALPHALUX Aiden: каркас на механизме, по 5 полок с двух сторон центральной стенки."""
    a, b = cx - RACK_W / 2, cx + RACK_W / 2
    y0, y1 = RACK_Y, RACK_Y + RACK_D
    yc = (y0 + y1) / 2
    for x in (cx - 200, cx + 200):          # направляющие механизма (низ/верх)
        box(x - 15, x + 15, 20, DEPTH - 30, RACK_Z, RACK_Z + 12, "rack")
        box(x - 15, x + 15, 20, DEPTH - 30, RACK_TOP + 2, RACK_SHELF, "rack")
    group("rack", type="rack", dir=[0, 1], travel=470, pivot=[cx, yc], angle=3.14159)
    z0, z1 = RACK_Z + 14, RACK_TOP
    for z in (z0, z1 - 20):
        box(a, b, y0, y1, z, z + 20, "rack")
    for x in (a, b - 20):
        for y in (y0, y1 - 20):
            box(x, x + 20, y, y + 20, z0, z1, "rack")
    box(a + 20, b - 20, yc - 4, yc + 4, z0 + 20, z1 - 20, "rackmesh")
    step = (z1 - z0 - 40) / 5
    for i in range(5):
        zs = z0 + 20 + i * step + 30
        for side, (ya, yb) in ((0, (yc + 4, y1)), (1, (y0, yc - 4))):
            box(a + 20, b - 20, ya, yb, zs - 6, zs, "rack")                     # полка
            yl = yb - 14 if side == 0 else ya
            box(a + 20, b - 20, yl, yl + 14, zs, zs + 30, "rack")               # бортик
            for k in range(6):                                                  # 3 пары
                sx = a + 40 + k * 115
                ys0, ys1 = (yc + 20, yb - 16) if side == 0 else (ya + 16, yc - 20)
                box(sx, sx + 95, ys0, ys1, zs, zs + 120 - (k % 2) * 25, "shoe" if (i + k + side) % 3 else "shoe2")
    end_group()


def shelf_back(x0, x1, z):
    box(x0, x1, 0, DEPTH - 20, z, z + T, "carcass")
    box(x0, x1, DEPTH - 40, DEPTH - 22, z - 10, z, "led")


def shelf_side(y0, y1, xs, xf, z, led=True):
    box(min(xs, xf), max(xs, xf), y0, y1, z, z + T, "carcass")
    if led:
        xa = xf - 20 if xf > xs else xf + 2
        box(xa, xa + 18, y0, y1, z - 10, z, "led")


def build(interactive=False):
    # стены и пол
    box(-100, W + 100, -100, 0, 0, H, "wall_back")
    box(-100, 0, -100, D, 0, H, "wall_left")
    box(W, W + 100, -100, D, 0, H, "wall_right")
    box(-100, W + 100, -100, D + 400, -30, 0, "floor")

    # ---------------- задний ряд --------------------------------------
    px = [0, B1 - T / 2, B1 + B2 - T / 2, W - T]
    for x in px:
        box(x, x + T, 0, DEPTH, PLINTH, H, "carcass")
    for z in (PLINTH, ANT, H - T):
        box(0, W, 0, DEPTH, z, z + T, "carcass")
    box(DEPTH, W - DEPTH, DEPTH - 50, DEPTH - 34, 0, PLINTH, "plinth")
    box(T, W - T, DEPTH - 22, DEPTH - 4, ANT - 10, ANT, "led")
    # З1 – два яруса
    x0, x1 = T, px[1]
    for z in (RAIL, RAIL_LOW):
        box(x0, x1, 290, 310, z - 10, z + 10, "rail")
    clothes_x(x0, x1, 300, RAIL, 900)
    clothes_x(x0, x1, 300, RAIL_LOW, 850)
    # З2 – поворотно-выдвижная обувница Aiden + полка
    x0, x1 = px[1] + T, px[2]
    shoe_rack((x0 + x1) / 2, interactive)
    shelf_back(x0, x1, RACK_SHELF)
    for i in range(3):                      # сумки на полке
        box(x0 + 40 + i * 250, x0 + 240 + i * 250, 200, 450, RACK_SHELF + T, RACK_SHELF + T + 180 - i * 20, "bag%d" % i)
    # З3 – длинная одежда
    x0, x1 = px[2] + T, W - T
    box(x0, x1, 290, 310, RAIL - 10, RAIL + 10, "rail")
    clothes_x(x0, x1, 300, RAIL, 1450)
    # коробки на антресоли
    for xa in (120, 520, 1000, 1600, 2000):
        box(xa, xa + 330, 120, 520, ANT + T, ANT + T + 260, "box")

    # ---------------- левый ряд (x 0…600) ------------------------------
    ye = D                                  # торец у входа
    yp = D - L1E                            # перегородка Л1/Л2
    ym = D - LM                             # перегородка ниши зеркала / Л1
    box(0, DEPTH, ye - T, ye, PLINTH, H, "carcass")
    box(0, DEPTH, yp - T / 2, yp + T / 2, PLINTH, H, "carcass")
    for z in (PLINTH, ANT, H - T):
        box(0, DEPTH, DEPTH, D, z, z + T, "carcass")
    box(DEPTH - 50, DEPTH - 34, DEPTH, D, 0, PLINTH, "plinth")
    box(DEPTH - 22, DEPTH - 4, DEPTH, D - T, ANT - 10, ANT, "led")
    box(0, DEPTH, ym - T / 2, ym + T / 2, PLINTH, ANT, "carcass")
    # Зр – выдвижное поворотное зеркало (в нише, видно торцом)
    yc = (ym + T / 2 + ye - T) / 2
    # на статичном 3D зеркало выдвинуто в проход; в интерактивной модели – в нише
    mx = 40 if interactive else DEPTH + 20
    if interactive:
        # выдвигается на 600 по x, затем поворачивается вокруг внутреннего края
        group("mirror", type="mirror", dir=[1, 0], travel=DEPTH, pivot=[mx, yc])
    box(mx, mx + MIR_D, yc - MIR_T / 2, yc + MIR_T / 2, MIR_Z, MIR_Z + MIR_H, "mirror_frame")
    box(mx + 20, mx + MIR_D - 20, yc + MIR_T / 2, yc + MIR_T / 2 + 3, MIR_Z + 20, MIR_Z + MIR_H - 20, "mirror")
    if interactive:
        end_group()
        box(20, DEPTH, yc - 10, yc + 10, MIR_Z + MIR_H + 5, MIR_Z + MIR_H + 25, "mirror_frame")   # направляющая
    else:
        box(DEPTH - 40, mx + 20, yc - 10, yc + 10, MIR_Z + MIR_H + 5, MIR_Z + MIR_H + 25, "mirror_frame")
    # Л1 – ящики для белья + полки
    y0, y1 = yp + T / 2, ym - T / 2
    drawers_side(y0, y1, DEPTH, +1)
    box(0, DEPTH, y0, y1, PLINTH + T + 800, PLINTH + 2 * T + 800, "carcass")
    for z in (1230, 1550, 1870):
        shelf_side(y0, y1, 0, DEPTH - 20, z)
        for k in range(2):                  # стопки вещей
            box(150, 480, y0 + 40 + k * 200, y0 + 200 + k * 200, z + T, z + T + 140 + k * 15, "cloth%d" % (k + 2))
    # Л2 – два яруса (открыто в угол)
    y0, y1 = DEPTH, yp - T / 2
    for z in (RAIL, RAIL_LOW):
        box(290, 310, y0, y1, z - 10, z + 10, "rail")
    clothes_y(y0, y1, 300, RAIL, 900)
    clothes_y(y0, y1, 300, RAIL_LOW, 850)

    # ---------------- правый ряд (x 1800…2400) -------------------------
    xf = W - DEPTH
    yr = DEPTH + R1                         # перегородка П1/П2
    box(xf, W, ye - T, ye, PLINTH, H, "carcass")
    box(xf, W, yr - T / 2, yr + T / 2, PLINTH, H, "carcass")
    for z in (PLINTH, ANT, H - T):
        box(xf, W, DEPTH, D, z, z + T, "carcass")
    box(xf + 34, xf + 50, DEPTH, D, 0, PLINTH, "plinth")
    box(xf + 4, xf + 22, DEPTH, D - T, ANT - 10, ANT, "led")
    # П1 – длинная одежда + полка для обуви
    y0, y1 = DEPTH, yr - T / 2
    box(W - 310, W - 290, y0, y1, RAIL - 10, RAIL + 10, "rail")
    clothes_y(y0, y1, W - 300, RAIL, 1450)
    box(xf, W, y0, y1, 350, 350 + T, "carcass")
    # угловая часть полки (Г-образная, заходит в угловую зону З3)
    box(xf, W - T, 0, y0, 350, 350 + T, "carcass")
    for k in range(3):
        x = xf + 90 + k * 150
        box(x, x + 90, 120, 400, PLINTH + T, PLINTH + T + 110, "shoe")
        box(x, x + 90, 120, 400, 366, 476, "shoe")
    for k in range(5):
        y = y0 + 40 + k * 180
        box(xf + 120, xf + 400, y, y + 90, PLINTH + T, PLINTH + T + 110, "shoe")
        box(xf + 120, xf + 400, y, y + 90, 366, 476, "shoe")
    # П2 – узкая ниша гладильной доски
    y0, y1 = yr + T / 2, ye - T
    for z in (1560, 1880):
        box(xf, W, y0, y1, z, z + T, "carcass")
    box(xf + 4, xf + 22, y0, y1, 1870, 1880, "led")
    yc = (y0 + y1) / 2
    if interactive:
        group("board", type="board", dir=[-1, 0], travel=520)
    box(xf + 110, xf + 110 + BOARD_W, yc - BOARD_T / 2, yc + BOARD_T / 2,
        PLINTH + T + 10, PLINTH + T + 10 + BOARD_L, "board")
    end_group()
    box(xf + 200, xf + 420, yc - 55, yc + 55, 1576, 1700, "iron")
    box(W - 20, W, yc - 40, yc + 40, 1680, 1760, "socket")


if __name__ == "__main__":
    build()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "model.js"), "w") as f:
        f.write("window.MODEL = " + json.dumps(boxes) + ";\n")
        f.write("window.CLOTH = " + json.dumps(CLOTH) + ";\n")
    print(len(boxes), "boxes")
