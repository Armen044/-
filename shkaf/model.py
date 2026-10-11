#!/usr/bin/env python3
"""3D-модель подвесного шкафа в нише (для интерактивной страницы).

Оси: x – вдоль стены 2–7 (0 = угол «2»), y – от стены в комнату, z – вверх от пола.
"""
from sheet import (T, DT, W, FILL, CD, DEPTH, CEIL, ZB, ZT, ZA, RAIL, MID, SHOE, SPACER, DOOR_GAP)

boxes = []
groups = {}
cur = [None]
CLOTH = ["#e9e5df", "#cfc8bf", "#b9b2aa", "#8d8680", "#f3f1ec", "#a39383", "#6f6a66", "#d8cdbf"]


def box(x0, x1, y0, y1, z0, z1, kind):
    b = [round(x0), round(x1), round(y0), round(y1), round(z0), round(z1), kind]
    if cur[0]:
        b.append(cur[0])
    boxes.append(b)


def group(gid, **meta):
    groups[gid] = meta
    cur[0] = gid


def end():
    cur[0] = None


def clothes(x0, x1, length):
    n = int((x1 - x0 - 40) / 70)
    for i in range(n):
        x = x0 + 30 + i * 70
        ln = length - (i * 97 % 3) * 70
        box(x, x + 28, CD / 2 - 220, CD / 2 + 220, RAIL - ln, RAIL - 30, "cloth%d" % (i * 5 % len(CLOTH)))


def build():
    # помещение: стена 2–7, стена 1–2 с входной дверью, простенок 3–4, пол
    L = -FILL                                                  # стена 1–2 (x шкафа отсчитывается от его левого края)
    box(L - 100, L + 2935, -100, 0, 0, CEIL, "wall_back")
    box(L - 100, L, 0, 815, 0, CEIL, "wall_left")
    box(L - 100, L, 815, 1790, 2060, CEIL, "wall_left")       # над входной дверью
    box(L - 100, L, 1790, 1975, 0, CEIL, "wall_left")
    box(L - 100, L - 40, 815, 1790, 0, 2060, "door_entry")
    box(W + FILL, W + FILL + 100, 0, 600, 0, CEIL, "wall_right")
    box(L - 100, L + 2935, -100, 2100, -30, 0, "floor")
    for x in (-FILL, W):                                       # фальш-планки 20 мм
        box(x, x + FILL, CD - 100, DEPTH, ZB, ZT, "facade")

    # корпус
    for x in (0, MID - T / 2, W - T):
        box(x, x + T, 0, CD, ZB, ZT, "carcass")
    for z in (ZB, ZT - T):
        box(0, W, 0, CD, z, z + T, "carcass")
    box(0, W, 0, 4, ZB, ZT, "back")
    for x0, x1 in ((T, MID - T / 2), (MID + T / 2, W - T)):
        box(x0, x1, 0, CD - 2, ZA - T, ZA, "carcass")            # полка антресоли
        box(x0 + 40, x0 + 360, 80, 480, ZA, ZA + 260, "box")
        box(x0 + 400, x1 - 40, 100, 480, ZA, ZA + 220, "box2")
        box(x0, x1, CD / 2 - 10, CD / 2 + 10, RAIL - 10, RAIL + 10, "rail")
    clothes(T, MID - T / 2, 1400)
    clothes(MID + T / 2, W - T, 950)

    # выдвижные полки для обуви (отсек 2) + проставки под петли
    x0, x1 = MID + T / 2, W - T
    for xs in (x0, x1 - SPACER):
        box(xs, xs + SPACER, 0, CD, ZB + T, SHOE[-1] + 120, "spacer")
    sx0, sx1 = x0 + SPACER + 13, x1 - SPACER - 13
    for i, z in enumerate(SHOE):
        group("shoe%d" % i, type="slide", dir=[0, 1], travel=400, needs=["door2", "door3"])
        box(sx0, sx1, 40, 540, z, z + T, "shelf")
        box(sx0, sx1, 520, 540, z + T, z + 60, "shelf")           # бортик
        for k in range(3):
            bx = sx0 + 25 + k * 230
            box(bx, bx + 85, 120, 420, z + T, z + T + 100, "shoe")
            box(bx + 95, bx + 180, 120, 420, z + T, z + T + 100, "shoe")
        end()

    # фасады: 4 распашные двери, ручки у стыка створок
    dw = W / 4
    hinges = [(0, -88), (MID, 85), (MID, -85), (W, 88)]
    for i in range(4):
        hx, ang = hinges[i]
        group("door%d" % i, type="hinge", pivot=[hx, DEPTH], angle=ang)
        x0, x1 = i * dw + DOOR_GAP / 2, (i + 1) * dw - DOOR_GAP / 2
        box(x0, x1, CD, DEPTH, ZB + 2, ZT - 4, "facade")
        hxp = x1 - 45 if i in (0, 2) else x0 + 25
        box(hxp, hxp + 20, DEPTH, DEPTH + 30, 500, 1400, "handle")
        end()


if __name__ == "__main__":
    build()
    print(len(boxes), "boxes", list(groups))
