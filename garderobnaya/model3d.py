#!/usr/bin/env python3
"""3D-модель гардеробной (набор параллелепипедов) -> model.js для view3d.html.

Оси: x – вдоль задней стены (0…2400, слева направо от входа),
y – от задней стены к входу (0…1740), z – вверх (0…2640).
"""
import json
import os

from generate import (T, H, W, D, DEPTH, PLINTH, ANT, RAIL, RAIL_LOW, B1, B2,
                      L1, R1, SIDE, BOARD_L, BOARD_W, BOARD_T)

boxes = []
CLOTH = ["#e9e5df", "#cfc8bf", "#b9b2aa", "#8d8680", "#f3f1ec", "#a39383", "#6f6a66", "#d8cdbf"]


def box(x0, x1, y0, y1, z0, z1, kind):
    boxes.append([round(x0), round(x1), round(y0), round(y1), round(z0), round(z1), kind])


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


def drawers_back(x0, x1):
    for i in range(4):
        zb = PLINTH + T + i * 200
        box(x0 + 2, x1 - 2, DEPTH - 18, DEPTH, zb + 2, zb + 198, "front")
        cx = (x0 + x1) / 2
        box(cx - 90, cx + 90, DEPTH, DEPTH + 12, zb + 125, zb + 137, "handle")
    box(x0, x1, 0, DEPTH, PLINTH + T + 800, PLINTH + 2 * T + 800, "carcass")


def drawers_side(y0, y1, xf, sign):
    """Ящики в боковой секции; xf – плоскость фасада, sign – направление в проход."""
    for i in range(4):
        zb = PLINTH + T + i * 200
        xa, xb = sorted((xf, xf - sign * 18))
        box(xa, xb, y0 + 2, y1 - 2, zb + 2, zb + 198, "front")
        cy = (y0 + y1) / 2
        xa, xb = sorted((xf, xf + sign * 12))
        box(xa, xb, cy - 90, cy + 90, zb + 125, zb + 137, "handle")


def shelf_back(x0, x1, z):
    box(x0, x1, 0, DEPTH - 20, z, z + T, "carcass")
    box(x0, x1, DEPTH - 40, DEPTH - 22, z - 10, z, "led")


def shelf_side(y0, y1, xs, xf, z, led=True):
    box(min(xs, xf), max(xs, xf), y0, y1, z, z + T, "carcass")
    if led:
        xa = xf - 20 if xf > xs else xf + 2
        box(xa, xa + 18, y0, y1, z - 10, z, "led")


def build():
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
    # З2 – ящики и полки
    x0, x1 = px[1] + T, px[2]
    drawers_back(x0, x1)
    for z in (1230, 1550, 1870):
        shelf_back(x0, x1, z)
    for i, z in enumerate((1230 + T, 1550 + T, 1870 + T)):   # сумки / коробки
        box(x0 + 60, x0 + 260, 200, 450, z, z + 200 - i * 20, "bag%d" % i)
        box(x0 + 320, x0 + 520, 220, 450, z, z + 170, "bag%d" % ((i + 1) % 3))
    # З3 – длинная одежда
    x0, x1 = px[2] + T, W - T
    box(x0, x1, 290, 310, RAIL - 10, RAIL + 10, "rail")
    clothes_x(x0, x1, 300, RAIL, 1450)
    # коробки на антресоли
    for xa in (120, 520, 1000, 1600, 2000):
        box(xa, xa + 330, 120, 520, ANT + T, ANT + T + 260, "box")

    # ---------------- левый ряд (x 0…600) ------------------------------
    ye = D                                  # торец у входа
    yp = D - L1                             # перегородка Л1/Л2
    box(0, DEPTH, ye - T, ye, PLINTH, H, "carcass")
    box(0, DEPTH, yp - T / 2, yp + T / 2, PLINTH, H, "carcass")
    for z in (PLINTH, ANT, H - T):
        box(0, DEPTH, DEPTH, D, z, z + T, "carcass")
    box(DEPTH - 50, DEPTH - 34, DEPTH, D, 0, PLINTH, "plinth")
    box(DEPTH - 22, DEPTH - 4, DEPTH, D - T, ANT - 10, ANT, "led")
    # Л1 – ящики + полки
    y0, y1 = yp + T / 2, ye - T
    drawers_side(y0, y1, DEPTH, +1)
    box(0, DEPTH, y0, y1, PLINTH + T + 800, PLINTH + 2 * T + 800, "carcass")
    for z in (1230, 1550, 1870):
        shelf_side(y0, y1, 0, DEPTH - 20, z)
        for k in range(3):                  # стопки вещей
            box(150, 480, y0 + 30 + k * 170, y0 + 180 + k * 170, z + T, z + T + 140 + k * 15, "cloth%d" % (k + 2))
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
    box(xf + 110, xf + 110 + BOARD_W, yc - BOARD_T / 2, yc + BOARD_T / 2,
        PLINTH + T + 10, PLINTH + T + 10 + BOARD_L, "board")
    box(xf + 200, xf + 420, yc - 55, yc + 55, 1576, 1700, "iron")
    box(W - 20, W, yc - 40, yc + 40, 1680, 1760, "socket")


if __name__ == "__main__":
    build()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "model.js"), "w") as f:
        f.write("window.MODEL = " + json.dumps(boxes) + ";\n")
        f.write("window.CLOTH = " + json.dumps(CLOTH) + ";\n")
    print(len(boxes), "boxes")
