#!/usr/bin/env python3
"""3D-модель шкафа со столом (стена 25–26).

Оси: x – вдоль стены 25–26 (0 = угол у стены 24–25), y – от стены к фасаду, z – вверх от пола.
"""
from sheet import (T, DT, W, X1, X2, C1, C3, DEPTH, CD, PL, B0, ZA, A_SHELF, ZTOP, H, CEIL, PANEL,
                   L_SHELVES, M_SHELVES, R_SHELF, RAIL_UP, RAIL_LOW, DOOR_Z, DOOR_GAP, DOORS,
                   DESK_TOP, DESK_T, DESK_X, DESK_Y, PED_Y, PED_H, DRW, DRW_GAP)

boxes = []
groups = {}
cur = [None]
CLOTH = ["#e9e5df", "#cfc8bf", "#b9b2aa", "#8d8680", "#f3f1ec", "#a39383", "#6f6a66", "#d8cdbf"]


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
    # помещение: стена 25–26, стена 24–25 слева, пол
    box(-100, W + 900, -100, 0, 0, CEIL, "wall_back")
    box(-100, 0, 0, 2400, 0, CEIL, "wall_left")
    box(-100, W + 900, -100, 2600, -30, 0, "floor")

    # корпус
    box(50, W - 50, 0, CD - 50, 0, PL, "plinth")
    for x in (0, X1 - T / 2, X2 - T / 2, W - T):
        box(x, x + T, 0, CD, PL, H, "carcass")
    for z in (PL, ZA, ZTOP):
        box(0, W, 0, CD, z, z + T, "carcass")
    box(0, W, 0, 4, PL, H, "back")
    box(0, X2, 0, CD - 2, A_SHELF, A_SHELF + T, "carcass")
    for z in L_SHELVES:
        box(T, X1 - T / 2, 0, CD, z, z + T, "woodshelf")
    for z in L_SHELVES[2:]:                                     # декор на открытых полках
        box(90, 260, 150, 420, z + T, z + T + 200, "box")
        box(330, 480, 200, 400, z + T, z + T + 120, "box2")
    for z in M_SHELVES:
        box(X1 + T / 2, X2 - T / 2, 0, CD - 2, z, z + T, "shelf")
    for z in M_SHELVES[:-1]:
        box(X1 + 60, X2 - 60, 110, 470, z + T, z + T + 130, "fold%d" % (int(z) % 7))
    box(X2 + T / 2, W - T, 0, CD - 2, R_SHELF, R_SHELF + T, "shelf")
    for zr, ln in ((RAIL_UP, 800), (RAIL_LOW, 820)):
        box(X2 + T / 2, W - T, CD / 2 - 10, CD / 2 + 10, zr - 10, zr + 10, "rail")
        clothes(X2 + T / 2, W - T, zr, ln)
    for x0, x1 in ((T, X1 - T / 2), (X1 + T / 2, X2 - T / 2), (X2 + T / 2, W - T)):   # коробки на антресоли
        box(x0 + 40, x0 + 300, 80, 480, ZA + T, ZA + T + 230, "box")

    # двери: 3 распашные, профиль-ручка на стыках
    hinges = [(X1, -88), (X2, -88), (W, 88)]
    for i, ((x0, x1), (hx, ang)) in enumerate(zip(DOORS, hinges)):
        group("door%d" % i, type="hinge", pivot=[hx, DEPTH], angle=ang)
        a, b = x0 + DOOR_GAP / 2, x1 - DOOR_GAP / 2
        box(a, b, CD, DEPTH, *DOOR_Z, "facade")
        if i < 2:                                              # профиль у правой кромки
            box(b - 12, b, DEPTH - 6, DEPTH + 1, *DOOR_Z, "profile")
        if i == 2:
            box(a, a + 12, DEPTH - 6, DEPTH + 1, *DOOR_Z, "profile")
        end()

    # антресоль: рейчатые фасады HIWOOD (4 створки по 600)
    for i in range(4):
        x0, x1 = i * 600, (i + 1) * 600
        hx, ang = (x0, -85) if i % 2 == 0 else (x1, 85)
        group("top%d" % i, type="hinge", pivot=[hx, DEPTH], angle=ang)
        box(x0 + 1, x1 - 1, CD, DEPTH, PANEL[0] + 2, PANEL[1] - 2, "flutes")
        end()

    # стол: столешница из торца левой секции и тумба с 4 ящиками
    box(DESK_X[0], DESK_X[1], DESK_Y[0], DESK_Y[1], DESK_TOP - DESK_T, DESK_TOP, "walnut")
    px0, px1 = DESK_X[0] + 10, DESK_X[1] - 10
    box(px0, px1 - DT, PED_Y[0], PED_Y[1], 0, PED_H, "carcass_s")
    for i in range(4):
        z0 = DRW_GAP + i * (DRW + DRW_GAP)
        group("drw%d" % i, type="slide", dir=[1, 0], travel=330, needs=[])
        box(px1 - DT, px1, PED_Y[0] + 3, PED_Y[1] - 3, z0, z0 + DRW, "dfront")
        box(px1, px1 + 14, (PED_Y[0] + PED_Y[1]) / 2 - 80, (PED_Y[0] + PED_Y[1]) / 2 + 80,
            z0 + DRW - 45, z0 + DRW - 33, "handle")
        box(px1 - 380, px1 - DT, PED_Y[0] + 20, PED_Y[1] - 20, z0 + 15, z0 + 23, "dbox")
        for ya in (PED_Y[0] + 20, PED_Y[1] - 32):
            box(px1 - 380, px1 - DT, ya, ya + 12, z0 + 15, z0 + DRW - 30, "dbox")
        end()


def comps():
    """Подсветка: левая открытая секция – всегда, справа на антресоли – при открытых фасадах."""
    return [
        {"doors": [], "light": [X1 / 2, 1200, CD - 100], "strip": [T + 4, T + 14, CD - 30, CD - 14, B0 + 20, ZA - 10]},
        {"doors": ["door1", "door2"], "light": [X2 + C3 / 2, 1300, CD - 150], "strip": [X2 + 12, X2 + 22, CD - 30, CD - 14, B0 + 20, ZA - 20]},
        {"doors": ["top2", "top3"], "light": [W - 300, ZA + 300, CD - 100], "strip": [W - T - 14, W - T - 4, CD - 30, CD - 14, ZA + 30, ZTOP - 20]},
    ]


if __name__ == "__main__":
    build()
    print(len(boxes), "boxes", list(groups))
