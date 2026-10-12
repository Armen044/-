#!/usr/bin/env python3
"""3D-модель кухни с островом: открываются двери, ящики и вся техника."""
from geom import (CEIL, PL, BT, TOP, BD, FD, BC, UD, CTD, UB, UT, MAIN, FILLER_MAIN, LEFT, FILLER_LEFT,
                  UPPER_MAIN, UPPER_LEFT, ISLAND, TALL_DRAWER, OVEN, MW, TALL_TOP, FRIDGE_DOOR, FRIDGE_TOP)

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


def drawers_y(x0, x1, splits, name="Ящик", y_front=BD, sign=1, depth=480):
    """Ящики на фасаде, смотрящем в +y (sign=1) или −y (sign=−1)."""
    for i, (z0, z1) in enumerate(splits):
        gid = "dr_%d_%d_%d" % (x0, round(y_front), i)
        group(gid, type="slide", dir=[0, sign], travel=depth * 0.8, needs=[], name=name)
        fa, fb = sorted((y_front, y_front - sign * FD))
        box(x0 + 1.5, x1 - 1.5, fa, fb, z0, z1, "front")
        ba, bb = sorted((y_front - sign * FD, y_front - sign * (FD + depth)))
        box(x0 + 30, x1 - 30, ba, bb, z0 + 20, z0 + 28, "dbox")
        for xa in (x0 + 30, x1 - 42):
            box(xa, xa + 12, ba, bb, z0 + 20, min(z1 - 20, z0 + 160), "dbox")
        box(x0 + 30, x1 - 30, *(sorted((y_front - sign * (FD + depth), y_front - sign * (FD + depth - 12)))),
            z0 + 20, min(z1 - 20, z0 + 160), "dbox")
        gy = y_front + sign * 0.6                        # профиль-подрезка (gola) сверху фасада
        box(x0 + 1.5, x1 - 1.5, *sorted((gy, gy - sign * 6)), z1 - 22, z1 - 2, "gola")
        end()


def drawers_x(y0, y1, splits, x_front=BD, depth=480):
    for i, (z0, z1) in enumerate(splits):
        group("drl_%d_%d" % (y0, i), type="slide", dir=[1, 0], travel=depth * 0.8, needs=[], name="Ящик")
        box(x_front - FD, x_front, y0 + 1.5, y1 - 1.5, z0, z1, "front")
        box(x_front - FD - depth, x_front - FD, y0 + 30, y1 - 30, z0 + 20, z0 + 28, "dbox")
        for ya in (y0 + 30, y1 - 42):
            box(x_front - FD - depth, x_front - FD, ya, ya + 12, z0 + 20, min(z1 - 20, z0 + 160), "dbox")
        box(x_front + 0.6 - 6, x_front + 0.6, y0 + 1.5, y1 - 1.5, z1 - 22, z1 - 2, "gola")
        end()


def door_y(gid, x0, x1, z0, z1, hinge_left, name="Дверца", y_front=BD, kind="front", tech=False):
    """Распашная дверца на фасаде +y (петли слева или справа)."""
    hx = x0 if hinge_left else x1
    group(gid, type="hinge", pivot=[hx, y_front], angle=-92 if hinge_left else 92, name=name, tech=tech)
    box(x0 + 1.5, x1 - 1.5, y_front - FD, y_front, z0, z1, kind)
    end()


def three_drawers(z_lo=PL + 2, z_hi=BT - 2):
    h = (z_hi - z_lo - 6) / 3
    return [(z_lo + i * (h + 3), z_lo + i * (h + 3) + h) for i in range(3)]


def build():
    # помещение
    box(-100, 7570, -100, 0, 0, CEIL, "wall_back")
    box(-100, 0, 0, 2950, 0, CEIL, "wall_left")
    box(-100, 7570, -100, 3100, -30, 0, "floor")

    # ---- нижний ряд вдоль стены 10–9 ----
    for x0, x1, kind in MAIN:
        top = UT if kind == "tall" else BT
        box(x0, x1, 0, BC - 60 if kind != "tall" else BC, 0, PL, "plinth")
        for x in (x0, x1 - T):
            box(x, x + T, 0, BC, PL, top, "carcass")
        box(x0, x1, 0, BC, PL, PL + T, "carcass")
        box(x0, x1, 0, 4, PL, top, "back")
        if kind == "tall":
            box(x0, x1, 0, BC, top - T, top, "carcass")
    box(*FILLER_MAIN, 0, BD, PL, UT, "front")
    # столешница и фартук – искусственный камень
    box(0, 3000, 0, CTD, BT, TOP, "quartz")
    box(0, CTD, CTD, LEFT[0][1], BT, TOP, "quartz")
    box(0, 3000, 0, 12, TOP, UB, "quartz")
    box(0, 12, 12, LEFT[0][1], TOP, UB, "quartz")

    for x0, x1, kind in MAIN:
        if kind == "sink":
            door_y("sink_l", x0, (x0 + x1) / 2, PL + 2, BT - 2, True)
            door_y("sink_r", (x0 + x1) / 2, x1, PL + 2, BT - 2, False)
            box(x0 + 80, x1 - 80, 80, 520, TOP - 180, TOP - 2, "sinkbowl")         # мойка
            box(x0 + 60, x1 - 60, 60, 540, TOP - 1, TOP + 1, "steel")
            box((x0 + x1) / 2 - 15, (x0 + x1) / 2 + 15, 40, 70, TOP, TOP + 300, "chrome")   # смеситель
            box((x0 + x1) / 2 - 12, (x0 + x1) / 2 + 12, 40, 230, TOP + 280, TOP + 300, "chrome")
        elif kind == "dw":
            box(x0 + 20, x1 - 20, 20, BC - 10, PL + 20, BT - 20, "appliance")       # корпус ПММ
            group("dw", type="lid", pivot=[BD, PL + 2], angle=88, name="Посудомоечная машина", tech=True)
            box(x0 + 1.5, x1 - 1.5, BD - FD, BD, PL + 2, BT - 2, "front")
            box(x0 + 30, x1 - 30, BD - FD - 40, BD - FD, PL + 40, BT - 40, "steel")
            box(x0 + 1.5, x1 - 1.5, BD + 0.6 - 6, BD + 0.6, BT - 24, BT - 4, "gola")
            end()
            for zz in (PL + 120, PL + 420):                                         # корзины
                box(x0 + 40, x1 - 40, 40, BC - 60, zz, zz + 8, "chrome")
        elif kind == "hob":
            drawers_y(x0, x1, [(PL + 2, 470), (476, BT - 2)])
            box(x0 + 5, x1 - 5, 40, 560, TOP, TOP + 6, "glass")                     # варочная панель
            for cx, cy, r in ((x0 + 160, 160, 95), (x0 + 440, 160, 75), (x0 + 160, 420, 75), (x0 + 440, 420, 95)):
                box(cx - r, cx + r, cy - r, cy + r, TOP + 6, TOP + 7, "burner")
        elif kind == "drawers":
            drawers_y(x0, x1, three_drawers())
        elif kind == "tall":
            drawers_y(x0, x1, [TALL_DRAWER])
            box(x0 + 20, x1 - 20, 20, BC - 5, OVEN[0], OVEN[1], "appliance")      # духовой шкаф
            box(x0 + 60, x1 - 60, 60, BC - 30, OVEN[0] + 60, OVEN[0] + 64, "chrome")
            group("oven", type="lid", pivot=[BD, OVEN[0]], angle=85, name="Духовой шкаф", tech=True)
            box(x0 + 2, x1 - 2, BD - 22, BD, OVEN[0], OVEN[1], "ovenglass")
            box(x0 + 60, x1 - 60, BD, BD + 25, OVEN[1] - 50, OVEN[1] - 38, "chrome")
            end()
            box(x0 + 20, x1 - 20, 220, BC - 5, MW[0], MW[1], "appliance")         # СВЧ
            group("mw", type="hinge", pivot=[x0 + 2, BD], angle=-95, name="СВЧ", tech=True)
            box(x0 + 2, x1 - 2, BD - 22, BD, MW[0] + 3, MW[1] - 3, "ovenglass")
            end()
            door_y("tall_top", x0, x1, *TALL_TOP, False)

    # ---- ряд вдоль стены 10–11/12 (фасады в +x) ----
    for y0, y1, kind in LEFT:
        top = UT if kind == "fridge" else BT
        box(0, BC - 60, y0, y1, 0, PL, "plinth")
        for y in (y0, y1 - T):
            box(0, BC, y, y + T, PL, top, "carcass")
        box(0, BC, y0, y1, PL, PL + T, "carcass")
        box(0, 4, y0, y1, PL, top, "back")
        if kind == "drawers480":
            drawers_x(y0, y1, three_drawers())
        else:
            box(0, BC, y0, y1, top - T, top, "carcass")
            box(30, BC - 5, y0 + 25, y1 - 25, PL + 20, FRIDGE_DOOR[1] - 10, "fridge")   # холодильник
            for zz in (500, 850, 1200, 1500):
                box(40, BC - 40, y0 + 35, y1 - 35, zz, zz + 6, "glassshelf")
            group("fridge", type="hinge", pivot=[BD, y1], angle=-92, name="Холодильник", tech=True)
            box(BD - FD, BD, y0 + 1.5, y1 - 1.5, *FRIDGE_DOOR, "front")
            box(BD - FD - 60, BD - FD, y0 + 40, y1 - 40, FRIDGE_DOOR[0] + 80, FRIDGE_DOOR[1] - 80, "fridge")
            end()
            group("fridge_top", type="hinge", pivot=[BD, y1], angle=-92, name="Дверца")
            box(BD - FD, BD, y0 + 1.5, y1 - 1.5, *FRIDGE_TOP, "front")
            end()
    box(0, BD, *FILLER_LEFT, PL, UT, "front")

    # ---- верхние шкафы ----
    xs = UPPER_MAIN
    box(0, xs[-1], 0, UD - FD, UB, UB + T, "carcass")
    box(0, xs[-1], 0, UD - FD, UT - T, UT, "carcass")
    for x in xs[1:]:
        box(x - T, x, 0, UD - FD, UB, UT, "carcass")
    for i in range(len(xs) - 1):
        x0, x1 = xs[i], xs[i + 1]
        box(x0, x1, 0, UD - FD, (UB + UT) / 2, (UB + UT) / 2 + T, "shelf")
        door_y("up%d" % i, x0, x1, UB + 2, UT - 4, i % 2 == 0, y_front=UD)
    ys = UPPER_LEFT
    box(0, UD - FD, ys[0], ys[-1], UB, UB + T, "carcass")
    box(0, UD - FD, ys[0], ys[-1], UT - T, UT, "carcass")
    for i in range(len(ys) - 1):
        y0, y1 = ys[i], ys[i + 1]
        hinge_near = i == 0
        hy = y0 if hinge_near else y1
        group("upl%d" % i, type="hinge", pivot=[UD, hy], angle=92 if hinge_near else -92, name="Дверца")
        box(UD - FD, UD, y0 + 1.5, y1 - 1.5, UB + 2, UT - 4, "front")
        end()
    # подсветка под верхними шкафами
    box(0, xs[-1], UD - 40, UD - 25, UB - 6, UB, "led")
    box(UD - 40, UD - 25, ys[0], ys[-1], UB - 6, UB, "led")
    # вытяжка, встроенная под шкаф над варочной панелью: выдвижной козырёк
    hx0, hx1 = 1800, 2400
    box(hx0 + 10, hx1 - 10, 0, 280, UB - 60, UB, "steel")
    group("hood", type="slide", dir=[0, 1], travel=180, needs=[], name="Вытяжка", tech=True)
    box(hx0 + 10, hx1 - 10, 260, 300, UB - 60, UB - 10, "front")
    end()

    # ---- остров 2 × 600, ящики со стороны кухни ----
    ix0, ix1, iy0, iy1 = ISLAND
    box(ix0 + 50, ix1 - 50, iy0 + 60, iy1 - 50, 0, PL, "plinth")
    for x in (ix0, (ix0 + ix1) / 2 - T / 2, ix1 - T):
        box(x, x + T, iy0 + FD, iy1, PL, BT, "carcass")
    box(ix0, ix1, iy0 + FD, iy1, PL, PL + T, "carcass")
    box(ix0, ix1, iy1 - FD, iy1, PL, BT, "front")                                   # фасад-панель с тыла
    box(ix0 - 20, ix1 + 20, iy0 - 20, iy1 + 20, BT, TOP, "quartz")
    for x0, x1 in ((ix0, (ix0 + ix1) / 2), ((ix0 + ix1) / 2, ix1)):
        drawers_y(x0, x1, three_drawers(), y_front=iy0, sign=-1, depth=480)


def comps():
    return [
        {"doors": [], "light": [1500, UB - 150, 450], "strip": [0, 0, 0, 0, 0, 0]},
        {"doors": ["fridge"], "light": [300, 1000, 1380], "strip": [0, 0, 0, 0, 0, 0]},
    ]


if __name__ == "__main__":
    build()
    print(len(boxes), "boxes", len(groups), "groups")
