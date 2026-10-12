#!/usr/bin/env python3
"""3D-модель распашного шкафа с ящиками (по эскизу заказчика).

Оси: x – по ширине шкафа (0 = левый край), y – от стены (0) к фасаду, z – вверх от пола.
"""
from sheet import (T, DT, W, CD, DEPTH, PL, ZB, B0, MID, H, ZTOP, ZA, L_SHELVES, R_SHELVES,  # noqa: F401
                   R_MID, RAIL_UP, RAIL_LOW, DR_Z, DR_H, DR_SET, DOOR_GAP, SPLIT, GROOVE, MILL, door_x)

boxes = []
groups = {}
cur = [None]
CLOTH = ["#e9e5df", "#cfc8bf", "#b9b2aa", "#8d8680", "#f3f1ec", "#a39383", "#6f6a66", "#d8cdbf"]
SHELF = ZA          # для совместимости с шаблоном


def box(x0, x1, y0, y1, z0, z1, kind):
    b = [round(x0, 1), round(x1, 1), round(y0, 1), round(y1, 1), round(z0, 1), round(z1, 1), kind]
    if cur[0]:
        b.append(cur[0])
    boxes.append(b)


def group(gid, **meta):
    groups[gid] = meta
    cur[0] = gid


def end():
    cur[0] = None


def clothes(x0, x1, rail, length):
    n = int((x1 - x0 - 40) / 70)
    for i in range(n):
        x = x0 + 30 + i * 70
        ln = length - (i * 97 % 3) * 70
        box(x, x + 28, CD / 2 - 220, CD / 2 + 220, rail - ln, rail - 30, "cloth%d" % (i * 5 % len(CLOTH)))


def build():
    # помещение: стена и пол
    box(-700, W + 700, -100, 0, 0, 2900, "wall_back")
    box(-700, W + 700, -100, 2200, -30, 0, "floor")

    # корпус
    box(50, W - 50, 0, CD - 50, 0, PL, "plinth")
    for x in (0, MID - T / 2, W - T):
        box(x, x + T, 0, CD, ZB, H, "carcass")
    for z in (ZB, ZTOP):
        box(0, W, 0, CD, z, z + T, "carcass")
    box(0, W, 0, 4, ZB, H, "back")
    lx0, lx1, rx0, rx1 = T, MID - T / 2, MID + T / 2, W - T
    for z in L_SHELVES:
        box(lx0, lx1, 0, CD - 2, z, z + T, "shelf")
    for z in R_SHELVES:
        box(rx0, rx1, 0, CD - 2, z, z + T, "shelf")
    # антресоль: коробки
    for x0, x1 in ((lx0, lx1), (rx0, rx1)):
        box(x0 + 40, x0 + 360, 80, 480, ZA + T, ZA + T + 280, "box")
        box(x0 + 400, x1 - 40, 100, 480, ZA + T, ZA + T + 230, "box2")
    # полки слева: стопки вещей
    for z in L_SHELVES[:-1]:
        for k in range(2):
            bx = lx0 + 50 + k * 360
            box(bx, bx + 300, 120, 450, z + T, z + T + 140 - k * 30, "fold%d" % (k * 3 + 1))
    # правый отсек: две штанги
    for zr, ln in ((RAIL_UP, 700), (RAIL_LOW, 820)):
        box(rx0, rx1, CD / 2 - 10, CD / 2 + 10, zr - 10, zr + 10, "rail")
        clothes(rx0, rx1, zr, ln)

    # 4 внутренних ящика слева
    fy1 = CD - DR_SET
    for i, z in enumerate(DR_Z):
        group("drawer%d" % i, type="slide", dir=[0, 1], travel=400, needs=["door0", "door1"])
        fx0, fx1 = lx0 + 4, lx1 - 4
        box(fx0, fx1, fy1 - 18, fy1, z, z + DR_H, "dfront")
        bx0, bx1 = fx0 + 13, fx1 - 13
        for xa in (bx0, bx1 - 12):
            box(xa, xa + 12, 40, fy1 - 18, z + 15, z + DR_H - 25, "dbox")
        box(bx0, bx1, 40, 52, z + 15, z + DR_H - 25, "dbox")
        box(bx0, bx1, 40, fy1 - 18, z + 15, z + 23, "dbox")
        end()

    # фасады: 4 нижние + 4 антресольные двери, зазор 30 на стыках, розовая фрезеровка кромок
    hinges = [(0, -88), (door_x(1)[1], 85), (door_x(2)[0], -85), (W, 88)]
    for row, (z0, z1) in enumerate(((PL + 2, SPLIT - DOOR_GAP / 2), (SPLIT + DOOR_GAP / 2, H - 2))):
        for i in range(4):
            hx, ang = hinges[i]
            gid = ("door%d" if row == 0 else "top%d") % i
            group(gid, type="hinge", pivot=[hx, DEPTH], angle=ang)
            x0, x1 = door_x(i)
            box(x0, x1, CD, DEPTH, z0, z1, "facade")
            gz0, gz1 = max(z0, GROOVE[0]), min(z1, GROOVE[1])
            if gz1 > gz0:
                if i > 0:                                  # фрезеровка на левой кромке
                    box(x0 - 0.5, x0 + MILL, DEPTH - 8, DEPTH + 0.6, gz0, gz1, "groove")
                if i < 3:                                  # и на правой
                    box(x1 - MILL, x1 + 0.5, DEPTH - 8, DEPTH + 0.6, gz0, gz1, "groove")
            end()


def comps():
    """Отсеки: двери, вертикальная LED-лента у левой стенки, точка света."""
    out = []
    for x0, x1, doors in ((T, MID - T / 2, ["door0", "door1"]), (MID + T / 2, W - T, ["door2", "door3"])):
        out.append({"doors": doors, "light": [(x0 + x1) / 2, (B0 + ZTOP) / 2, CD - 120],
                    "strip": [x0 + 4, x0 + 14, CD - 30, CD - 14, B0 + 20, ZTOP - 20]})
    return out


if __name__ == "__main__":
    build()
    print(len(boxes), "boxes", list(groups))
