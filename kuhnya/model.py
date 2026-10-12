#!/usr/bin/env python3
"""3D-модель угловой кухни (по заводскому чертежу) с островом: открываются дверцы, ящики и техника."""
from geom import (H, PL, BT, TOP, UB, U_MID, BD, UD, FD, BC, W_MAIN, W_SIDE, SIDE_X, FRIDGE, OVEN_COL,
                  FR_LOW, FR_DOOR, TOP_ROW, OC_DRAWER, MW, OVEN, OC_DOOR, BASE_800, CORNER, CORNER_FRONT,
                  CORNER_FILL, FRONT_SPLIT, SINK, DW, SIDE_END, UPPER_MAIN, UPPER_SIDE, U_SIDE_X, ISLAND)

boxes = []
groups = {}
cur = [None]
CLOTH = ["#e9e5df"]
T = 16


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


def gola_y(x0, x1, y_front, z1, sign=1):
    gy = y_front + sign * 0.6
    box(x0 + 1.5, x1 - 1.5, *sorted((gy, gy - sign * 6)), z1 - 22, z1 - 2, "gola")


def door_y(gid, x0, x1, z0, z1, hinge_left, y_front=BD, name="Дверца", tech=False, gola=False):
    """Дверца на фасаде, смотрящем в +y."""
    group(gid, type="hinge", pivot=[x0 if hinge_left else x1, y_front], angle=-92 if hinge_left else 92,
          name=name, tech=tech)
    box(x0 + 1.5, x1 - 1.5, y_front - FD, y_front, z0, z1, "front")
    if gola:
        gola_y(x0, x1, y_front, z1)
    end()


def door_mx(gid, y0, y1, z0, z1, hinge_near, x_front=SIDE_X, name="Дверца", gola=False):
    """Дверца на фасаде, смотрящем в −x (боковой ряд); hinge_near – петли со стороны угла (y0)."""
    group(gid, type="hinge", pivot=[x_front, y0 if hinge_near else y1], angle=-92 if hinge_near else 92, name=name)
    box(x_front, x_front + FD, y0 + 1.5, y1 - 1.5, z0, z1, "front")
    if gola:
        box(x_front - 0.6, x_front + 5, y0 + 1.5, y1 - 1.5, z1 - 22, z1 - 2, "gola")
    end()


def drawer_y(gid, x0, x1, z0, z1, y_front=BD, sign=1, depth=480, name="Ящик"):
    group(gid, type="slide", dir=[0, sign], travel=depth * 0.8, needs=[], name=name)
    box(x0 + 1.5, x1 - 1.5, *sorted((y_front, y_front - sign * FD)), z0, z1, "front")
    ba, bb = sorted((y_front - sign * FD, y_front - sign * (FD + depth)))
    box(x0 + 30, x1 - 30, ba, bb, z0 + 20, z0 + 28, "dbox")
    hz = min(z1 - 20, z0 + 160)
    for xa in (x0 + 30, x1 - 42):
        box(xa, xa + 12, ba, bb, z0 + 20, hz, "dbox")
    e0 = y_front - sign * (FD + depth)
    box(x0 + 30, x1 - 30, *sorted((e0, e0 + sign * 12)), z0 + 20, hz, "dbox")
    gola_y(x0, x1, y_front, z1, sign)
    end()


def carcass_y(x0, x1, top, depth=BC):
    """Корпус модуля основного ряда (фасад в +y)."""
    for x in (x0, x1 - T):
        box(x, x + T, 0, depth, PL, top, "carcass")
    box(x0, x1, 0, depth, PL, PL + T, "carcass")
    box(x0, x1, 0, depth, top - T, top, "carcass")
    box(x0, x1, 0, 4, PL, top, "back")


def build():
    # помещение: основная стена, боковая стена справа, пол
    box(-600, W_MAIN + 100, -100, 0, 0, H + 100, "wall_back")
    box(W_MAIN, W_MAIN + 100, 0, 3000, 0, H + 100, "wall_right")
    box(-600, W_MAIN + 100, -100, 3100, -30, 0, "floor")

    # ---- пенал холодильника ----
    x0, x1 = FRIDGE
    carcass_y(x0, x1, H)
    box(x0 + 30, x1 - 30, 30, BC - 5, FR_DOOR[0] + 15, FR_DOOR[1] - 15, "fridge")
    for zz in (1150, 1500, 1850, 2200):
        box(x0 + 40, x1 - 40, 40, BC - 40, zz, zz + 6, "glassshelf")
    group("fridge", type="hinge", pivot=[x0, BD], angle=-95, name="Холодильник", tech=True)
    box(x0 + 1.5, x1 - 1.5, BD - FD, BD, *FR_DOOR, "front")
    box(x0 + 40, x1 - 40, BD - FD - 60, BD - FD, FR_DOOR[0] + 80, FR_DOOR[1] - 80, "fridge")
    end()
    door_y("fr_low", x0, x1, *FR_LOW, True, gola=True)
    door_y("fr_top", x0, x1, *TOP_ROW, True)

    # ---- пенал ДШ + СВЧ ----
    x0, x1 = OVEN_COL
    carcass_y(x0, x1, H)
    drawer_y("oc_drawer", x0, x1, *OC_DRAWER)
    box(x0 + 20, x1 - 20, 220, BC - 5, MW[0] + 10, MW[1] - 10, "appliance")         # СВЧ
    group("mw", type="hinge", pivot=[x0 + 2, BD], angle=-95, name="СВЧ", tech=True)
    box(x0 + 2, x1 - 2, BD - 22, BD, MW[0] + 3, MW[1] - 3, "ovenglass")
    end()
    box(x0 + 20, x1 - 20, 20, BC - 5, OVEN[0], OVEN[1], "appliance")                 # духовой шкаф
    box(x0 + 60, x1 - 60, 60, BC - 30, OVEN[0] + 60, OVEN[0] + 64, "chrome")
    group("oven", type="lid", pivot=[BD, OVEN[0]], angle=85, name="Духовой шкаф", tech=True)
    box(x0 + 2, x1 - 2, BD - 22, BD, OVEN[0], OVEN[1] - 90, "ovenglass")
    box(x0 + 60, x1 - 60, BD, BD + 25, OVEN[1] - 140, OVEN[1] - 128, "chrome")
    end()
    box(x0 + 2, x1 - 2, BD - 22, BD, OVEN[1] - 88, OVEN[1], "appliance")             # панель управления
    for zz in (1800, 2120):
        box(x0 + T, x1 - T, 0, BC - 2, zz, zz + T, "shelf")
    door_y("oc_door", x0, x1, *OC_DOOR, False)
    door_y("oc_top", x0, x1, *TOP_ROW, False)

    # ---- нижний ряд основной стены ----
    x0, x1 = BASE_800
    carcass_y(x0, x1, BT)
    box(x0, x1, 0, BC - 60, 0, PL, "plinth")
    m = (x0 + x1) / 2
    door_y("b800_l", x0, m, PL + 2, BT - 2, True, gola=True)
    door_y("b800_r", m, x1, PL + 2, BT - 2, False, gola=True)
    box(x0 + 100, x1 - 100, 40, 560, TOP, TOP + 6, "glass")                        # варочная панель
    for cx, cy, r in ((x0 + 260, 160, 95), (x1 - 260, 160, 75), (x0 + 260, 430, 75), (x1 - 260, 430, 95)):
        box(cx - r, cx + r, cy - r, cy + r, TOP + 6, TOP + 7, "burner")
    x0, x1 = CORNER
    carcass_y(x0, x1, BT)
    box(x0, CORNER_FILL[1], 0, BC - 60, 0, PL, "plinth")
    fa, fb = CORNER_FRONT
    door_y("cor_lo", fa, fb, PL + 2, FRONT_SPLIT - 3, False, gola=True)
    door_y("cor_hi", fa, fb, FRONT_SPLIT + 3, BT - 2, False, gola=True)
    box(*CORNER_FILL, BD - FD, BD, PL + 2, BT - 2, "front")
    box(0 + 1200, W_MAIN, 0, BD, BT, TOP, "quartz")                                 # столешница
    box(1200, W_MAIN, 0, 10, TOP, UB, "quartz")                                     # фартук

    # ---- нижний ряд боковой стены (фасады в −x) ----
    def carcass_x(y0, y1, top=BT):
        for y in (y0, y1 - T):
            box(SIDE_X + FD, W_MAIN, y, y + T, PL, top, "carcass")
        box(SIDE_X + FD, W_MAIN, y0, y1, PL, PL + T, "carcass")
        box(W_MAIN - 4, W_MAIN, y0, y1, PL, top, "back")
        box(SIDE_X + 60, W_MAIN, y0, y1, 0, PL, "plinth")
    carcass_x(*SINK)
    door_mx("sink_lo", *SINK, PL + 2, FRONT_SPLIT - 3, True, gola=True)
    door_mx("sink_hi", *SINK, FRONT_SPLIT + 3, BT - 2, True, gola=True)
    sy0, sy1 = SINK
    box(SIDE_X + 80, W_MAIN - 60, sy0 + 100, sy1 - 100, TOP - 180, TOP - 2, "sinkbowl")
    box(SIDE_X + 60, W_MAIN - 40, sy0 + 80, sy1 - 80, TOP - 1, TOP + 1, "steel")
    cyy = (sy0 + sy1) / 2
    box(W_MAIN - 70, W_MAIN - 40, cyy - 15, cyy + 15, TOP, TOP + 300, "chrome")
    box(W_MAIN - 260, W_MAIN - 40, cyy - 12, cyy + 12, TOP + 280, TOP + 300, "chrome")
    carcass_x(*DW)
    box(SIDE_X + 30, W_MAIN - 20, DW[0] + 20, DW[1] - 20, PL + 20, BT - 20, "appliance")
    for zz in (PL + 120, PL + 420):
        box(SIDE_X + 60, W_MAIN - 40, DW[0] + 40, DW[1] - 40, zz, zz + 8, "chrome")
    group("dw", type="lidz", pivot=[SIDE_X, PL + 2], angle=88, name="Посудомоечная машина", tech=True)
    box(SIDE_X, SIDE_X + FD, DW[0] + 1.5, DW[1] - 1.5, PL + 2, BT - 2, "front")
    box(SIDE_X + FD, SIDE_X + FD + 40, DW[0] + 30, DW[1] - 30, PL + 40, BT - 40, "steel")
    box(SIDE_X - 0.6, SIDE_X + 5, DW[0] + 1.5, DW[1] - 1.5, BT - 24, BT - 4, "gola")
    end()
    box(SIDE_X, W_MAIN, *SIDE_END, PL, BT, "front")
    box(SIDE_X, W_MAIN, BD, W_SIDE, BT, TOP, "quartz")
    box(W_MAIN - 10, W_MAIN, BD, W_SIDE, TOP, UB, "quartz")

    # ---- верхние шкафы основной стены: два ряда фасадов ----
    for i, (x0, x1, n) in enumerate(UPPER_MAIN):
        for x in (x0, x1 - T):
            box(x, x + T, 0, UD - FD, UB, H, "carcass")
        for zz in (UB, U_MID, H - T):
            box(x0, x1, 0, UD - FD, zz, zz + T, "carcass")
        for zz in (UB + 300 + T, UB + 2 * (300 + T)):
            box(x0 + T, x1 - T, 0, UD - FD - 2, zz, zz + T, "shelf")
        w = (x1 - x0) / n
        for k in range(n):
            a, b = x0 + k * w, x0 + (k + 1) * w
            door_y("um%d_%d" % (i, k), a, b, UB + 2, U_MID - 2, k == 0 and n > 1, y_front=UD)
            door_y("umt%d_%d" % (i, k), a, b, *TOP_ROW, k == 0 and n > 1, y_front=UD)
    # ---- верхние шкафы боковой стены ----
    box(U_SIDE_X + FD, W_MAIN, UD, UPPER_SIDE[0][0], UB, H, "carcass")             # угловая вставка
    for i, (y0, y1, n) in enumerate(UPPER_SIDE):
        for y in (y0, y1 - T):
            box(U_SIDE_X + FD, W_MAIN, y, y + T, UB, H, "carcass")
        for zz in (UB, U_MID, H - T):
            box(U_SIDE_X + FD, W_MAIN, y0, y1, zz, zz + T, "carcass")
        if i == 0:                                                                 # сушилка над мойкой
            for zz in (UB + 250, UB + 600):
                box(U_SIDE_X + 40, W_MAIN - 20, y0 + 30, y1 - 30, zz, zz + 8, "chrome")
        w = (y1 - y0) / n
        for k in range(n):
            a, b = y0 + k * w, y0 + (k + 1) * w
            near = (k == 0) if n > 1 else True
            door_mx("us%d_%d" % (i, k), a, b, UB + 2, U_MID - 2, near, x_front=U_SIDE_X)
            door_mx("ust%d_%d" % (i, k), a, b, *TOP_ROW, near, x_front=U_SIDE_X)
    # LED врезная под верхними шкафами
    box(1200, W_MAIN, UD - 40, UD - 25, UB - 6, UB, "led")
    box(U_SIDE_X - 40 + FD, U_SIDE_X - 25 + FD, UD, W_SIDE, UB - 6, UB, "led")

    # ---- остров (дизайн-проект): ящики со стороны кухни ----
    ix0, ix1, iy0, iy1 = ISLAND
    box(ix0 + 50, ix1 - 50, iy0 + 60, iy1 - 50, 0, PL, "plinth")
    for x in (ix0, (ix0 + ix1) / 2 - T / 2, ix1 - T):
        box(x, x + T, iy0 + FD, iy1, PL, BT, "carcass")
    box(ix0, ix1, iy0 + FD, iy1, PL, PL + T, "carcass")
    box(ix0, ix1, iy1 - FD, iy1, PL, BT, "front")
    box(ix0 - 20, ix1 + 20, iy0 - 20, iy1 + 20, BT, TOP, "quartz")
    for c, (x0, x1) in enumerate(((ix0, (ix0 + ix1) / 2), ((ix0 + ix1) / 2, ix1))):
        h = (BT - 2 - PL - 2 - 6) / 3
        for i in range(3):
            z0 = PL + 2 + i * (h + 3)
            drawer_y("isl%d_%d" % (c, i), x0, x1, z0, z0 + h, y_front=iy0, sign=-1)


def comps():
    return [
        {"doors": [], "light": [2000, UB - 150, 500], "strip": None},
        {"doors": ["fridge"], "light": [300, 1600, 700], "strip": None},
    ]


if __name__ == "__main__":
    build()
    print(len(boxes), "boxes", len(groups), "groups")
