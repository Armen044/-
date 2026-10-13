#!/usr/bin/env python3
"""3D-модель гардеробной с островом – набор параллелепипедов."""
import math

from geom import *

boxes, groups, cur = [], {}, [None]
cyls = []                # полуцилиндры: [cx, cy, r, z0, z1, kind, toward]
CLOTH = ["#e9e5df", "#cfc8bf", "#b9b2aa", "#8d8680", "#f3f1ec", "#a39383", "#6f6a66", "#d8cdbf",
         "#2f2d2c", "#7a8a9a"]
COLORS = {"carcass": 0x6a4c38, "front": 0x7a5a44, "plinth": 0x3e2c20, "handle": 0x1d1d1d, "rail": 0x1d1d1d,
          "frame": 0x1b1b1b, "tray": 0x5a3e2c, "isl": 0x6a4c38, "pouf": 0x7a5a44, "velvet": 0xe8e0d0, "dbox": 0x8c6c55, "dbottom": 0x9c7c64,
          "floor": 0x8f8a84, "rug": 0xe6e1d8, "cushion": 0xe2d6c0, "box": 0x1f1f1f, "shoe": 0x2c2622,
          "shoe2": 0x8a6a52, "socket": 0x2a2a2a, "item0": 0x8a2b2b, "item1": 0x2b4a7a, "item2": 0xc9a227,
          "wall_back": 0xe8e4df, "wall_left": 0xe8e4df, "wall_right": 0xe8e4df}
EDGES = {"carcass": 0x2a1d14, "front": 0x2a1d14, "tray": 0x2a1d14, "frame": 0x000000}
WOOD = ["carcass", "front", "tray", "isl", "pouf"]


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


def clothes_x(x0, x1, yc, ztop, length, step=80, k0=0):
    n = int((x1 - x0 - 40) / step)
    for i in range(n):
        x = x0 + 40 + i * step
        ln = length - (i * 97 % 3) * 70
        box(x, x + 30, yc - 220, yc + 220, ztop - ln, ztop - 30, "cloth%d" % ((i * 3 + k0) % len(CLOTH)))


def clothes_y(y0, y1, xc, ztop, length, step=80, k0=0):
    n = int((y1 - y0 - 40) / step)
    for i in range(n):
        y = y0 + 40 + i * step
        ln = length - (i * 97 % 3) * 70
        box(xc - 220, xc + 220, y, y + 30, ztop - ln, ztop - 30, "cloth%d" % ((i * 7 + k0) % len(CLOTH)))


def side(x0, x1, sign, tag):
    """Боковой ряд. x0…x1 – по глубине (от стены к проходу), sign = +1 слева, −1 справа."""
    xf = x1 if sign > 0 else x0                  # плоскость фронта
    xw = x0 if sign > 0 else x1                  # стена
    inn = (x0, x1)
    # каркас: дно, полки антресоли, верх, перегородки
    for z in (PL, A1, A2, H - T):
        box(*inn, BD, D, z, z + T, "carcass")
    for y in PANELS_Y:
        box(*inn, y, y + T, PL, H, "carcass")
    pa, pb = sorted((xf - sign * 50, xf - sign * 34))
    box(pa, pb, BD, D, 0, PL, "plinth")
    la, lb = sorted((xf - sign * 22, xf - sign * 4))
    box(la, lb, BD, D - T, A1 - 10, A1, "led")
    xc = (x0 + x1) / 2

    # B, C – штанга + выдвижной лоток для ремней/галстуков + полка для обуви
    for k, (y0, y1) in enumerate((COL_B, COL_C)):
        box(xc - 10, xc + 10, y0, y1, RAIL - 10, RAIL + 10, "rail")
        clothes_y(y0, y1, xc, RAIL, 1000, k0=k * 3 + (sign > 0))
        box(*inn, y0, y1, SHOE, SHOE + T, "carcass")
        for j in range(3):
            yy = y0 + 80 + j * 260
            box(xw + sign * 140 if sign > 0 else xw - 420, xw + sign * 420 if sign > 0 else xw - 140,
                yy, yy + 95, SHOE + T, SHOE + T + 110, "shoe")
        gid = "tray_%s_%d" % (tag, k)
        group(gid, set="trays", name="Выдвижной лоток для ремней и галстуков", dir=[sign, 0], travel=420)
        ta, tb = sorted((xf - sign * 520, xf))
        box(ta, tb, y0 + 10, y1 - 10, TRAY_Z, TRAY_Z + 18, "tray")
        box(ta, tb, y0 + 10, y0 + 28, TRAY_Z + 18, TRAY_Z + 60, "tray")
        box(ta, tb, y1 - 28, y1 - 10, TRAY_Z + 18, TRAY_Z + 60, "tray")
        fa, fb = sorted((xf, xf - sign * 18))
        box(fa, fb, y0 + 10, y1 - 10, TRAY_Z + 18, TRAY_Z + 60, "tray")
        for r in range(9):                               # ремни/галстуки рулонами
            yy = y0 + 60 + r * 85
            box(ta + 60, tb - 60, yy, yy + 50, TRAY_Z + 18, TRAY_Z + 50, "velvet" if r % 2 else "cloth%d" % (r % 10))
        end_group()

    # A – ящики + лоток для украшений + полки
    y0, y1 = COL_A
    cy = (y0 + y1) / 2
    for i in range(DR_N):
        zb = PL + T + i * DR_H
        group("drw_%s_%d" % (tag, i), set="drawers", name="Выкатной ящик", dir=[sign, 0], travel=450)
        fa, fb = sorted((xf, xf - sign * 18))
        box(fa, fb, y0 + 2, y1 - 2, zb + 2, zb + DR_H - 2, "front")
        ha, hb = sorted((xf, xf + sign * 12))
        box(ha, hb, cy - 220, cy + 220, zb + DR_H - 40, zb + DR_H - 30, "handle")
        ba, bb = sorted((xf - sign * 18, xf - sign * 500))
        box(ba, bb, y0 + 13, y0 + 25, zb + 25, zb + DR_H - 35, "dbox")
        box(ba, bb, y1 - 25, y1 - 13, zb + 25, zb + DR_H - 35, "dbox")
        wa, wb = sorted((xf - sign * 488, xf - sign * 500))
        box(wa, wb, y0 + 13, y1 - 13, zb + 25, zb + DR_H - 35, "dbox")
        box(ba, bb, y0 + 13, y1 - 13, zb + 25, zb + 33, "dbottom")
        end_group()
    box(*inn, y0, y1, DR_TOP, DR_TOP + T, "carcass")
    group("jew_%s" % tag, set="trays", name="Выдвижной лоток для украшений", dir=[sign, 0], travel=420)
    ta, tb = sorted((xf - sign * 520, xf))
    box(ta, tb, y0 + 10, y1 - 10, TRAY_Z, TRAY_Z + 14, "tray")
    for j in range(4):                                   # ячейки с бархатом
        for r in range(3):
            ya = y0 + 30 + j * 185
            xa = ta + 20 + r * 165
            box(xa, xa + 150, ya, ya + 170, TRAY_Z + 14, TRAY_Z + 30, "velvet")
            if (j + r) % 2 == 0:
                box(xa + 50, xa + 100, ya + 60, ya + 110, TRAY_Z + 30, TRAY_Z + 45, "item%d" % ((j + r) % 3))
    fa, fb = sorted((xf, xf - sign * 18))
    box(fa, fb, y0 + 10, y1 - 10, TRAY_Z, TRAY_Z + 55, "tray")
    end_group()
    for z in A_SHELVES:
        box(*inn, y0, y1, z, z + T, "carcass")
        box(xc - 150, xc + 150, y0 + 60, y1 - 60, z + T, z + T + 130 + (z % 3) * 15, "cloth%d" % (z % 10))

    # S – полки для обуви у входа
    y0, y1 = COL_S
    for z in S_SHELVES:
        box(*inn, y0, y1, z, z + T, "carcass")
        for j in range(3):
            yy = y0 + 50 + j * 200
            sa, sb = sorted((xf - sign * 60, xf - sign * 330))
            box(sa, sb, yy, yy + 90, z + T, z + T + 105 - (j % 2) * 25, "shoe" if (j + z // 100) % 3 else "shoe2")

    # угловая зона бокового ряда – штанги продолжают задние (Г-образно)
    y0, y1 = CORNER
    box(xc - 10, xc + 10, 300, y1, RAIL - 10, RAIL + 10, "rail")


def build():
    box(-100, W + 100, -100, 0, 0, H, "wall_back")
    box(-100, 0, -100, D + 40, 0, H, "wall_left")
    box(W, W + 100, -100, D + 40, 0, H, "wall_right")
    box(-100, W + 100, -100, D + 900, -30, 0, "floor")
    box(SD + 150, W - SD - 150, BD + 200, D - 300, 0, 8, "rug")

    # ---- задний ряд
    for z in (PL, A1, A2, H - T):
        box(0, W, 0, BD, z, z + T, "carcass")
    for x in (XL - T / 2, XR - T / 2):
        box(x, x + T, 0, BD, PL, H, "carcass")
    box(SD, W - SD, BD - 50, BD - 34, 0, PL, "plinth")
    box(T, W - T, BD - 22, BD - 4, A1 - 10, A1, "led")
    for x in (XL + 150, XR + 300):                       # коробки на антресоли
        box(x, x + 340, 120, 480, A1 + T, A1 + T + 220, "box")
    for x in (220, W - 560):
        box(x, x + 340, 120, 480, A2 + T, A2 + T + 220, "box")
    # центральная колонна полок
    for z in COL_SHELVES:
        box(XL + T / 2, XR - T / 2, 0, BD, z, z + T, "carcass")
        box(XL + 120, XR - 120, 80, BD - 80, z + T, z + T + 140 + (z % 7) * 10, "cloth%d" % (z % 10))
    # левая секция – длинная одежда + полка для обуви (Г-образно с левым рядом)
    box(300, XL - T / 2, 290, 310, RAIL - 10, RAIL + 10, "rail")
    clothes_x(SD + 20, XL - T / 2, 300, RAIL, 1550)
    box(0, XL - T / 2, 0, BD, SHOE, SHOE + T, "carcass")
    box(0, SD, BD, CORNER[1], SHOE, SHOE + T, "carcass")
    clothes_y(BD + 20, CORNER[1], SD / 2, RAIL, 1550, k0=2)
    # правая секция – 2 яруса (Г-образно с правым рядом)
    box(XR + T / 2, W - 300, 290, 310, RAIL - 10, RAIL + 10, "rail")
    box(XR + T / 2, W - 300, 290, 310, RAIL_LOW - 10, RAIL_LOW + 10, "rail")
    box(XR + T / 2, W, 0, BD, MID, MID + T, "carcass")
    box(W - SD, W, BD, CORNER[1], MID, MID + T, "carcass")
    box(W - SD / 2 - 10, W - SD / 2 + 10, 300, CORNER[1], RAIL_LOW - 10, RAIL_LOW + 10, "rail")
    clothes_x(XR + T / 2, W - SD - 20, 300, RAIL, 950, k0=4)
    clothes_x(XR + T / 2, W - SD - 20, 300, RAIL_LOW, 900, k0=1)
    clothes_y(BD + 20, CORNER[1], W - SD / 2, RAIL, 950, k0=5)
    clothes_y(BD + 20, CORNER[1], W - SD / 2, RAIL_LOW, 900, k0=6)

    side(0, SD, +1, "l")
    side(W - SD, W, -1, "r")
    island()
    glass()


def round_slices(cx, cy, r, z0, z1, kind, toward, **_):
    """Полуцилиндр радиуса r; toward = −1 – выпуклость к задней стене, +1 – к входу."""
    cyls.append([round(cx), round(cy), round(r), round(z0), round(z1), kind, toward])


def island():
    x0, x1 = ISL_X
    y0, y1 = ISL_Y
    cx = (x0 + x1) / 2
    r = ISL_W / 2
    yb = y0 + r                                          # начало прямой части
    box(x0, x1, yb, y1, PL, ISL_H - 40, "carcass")
    round_slices(cx, yb, r, PL, ISL_H - 40, "isl", -1)
    box(x0 + 40, x1 - 40, yb - 300, y1 - 40, 0, PL, "plinth")
    # витрина: стеклянная крышка, внутри ячейки с бархатом
    for xa, xb in ((x0, x0 + 30), (x1 - 30, x1)):
        box(xa, xb, yb, y1, ISL_H - 40, ISL_H, "carcass")
    box(x0, x1, y1 - 30, y1, ISL_H - 40, ISL_H, "carcass")
    round_slices(cx, yb, r, ISL_H - 40, ISL_H, "isl", -1)
    box(x0 + 30, x1 - 30, y0 + 60, y1 - 30, ISL_H - 46, ISL_H - 40, "velvet")
    for j in range(4):
        for i in range(2):
            ya = y0 + 140 + j * 220
            xa = x0 + 50 + i * 310
            box(xa, xa + 290, ya, ya + 200, ISL_H - 46, ISL_H - 36, "tray")
            box(xa + 60, xa + 230, ya + 50, ya + 150, ISL_H - 36, ISL_H - 20, "item%d" % ((i + j) % 3))
    box(x0 + 30, x1 - 30, yb, y1 - 30, ISL_H - 4, ISL_H, "vitrine")
    round_slices(cx, yb, r - 30, ISL_H - 4, ISL_H, "vitrine", -1)
    box(cx - 60, cx + 60, y0 + 70, y0 + 150, ISL_H, ISL_H + 30, "item2")   # поднос
    # ящики острова по длинным сторонам (по 2)
    for side_, sx in (("l", -1), ("r", 1)):
        xf = x1 if sx > 0 else x0
        for i in range(2):
            zb = PL + 20 + i * 370
            group("isl_%s%d" % (side_, i), set="drawers", name="Ящик острова", dir=[sx, 0], travel=380)
            fa, fb = sorted((xf, xf + sx * 18))
            box(fa, fb, yb + 20, y1 - 20, zb, zb + 350, "front")
            ha, hb = sorted((xf + sx * 18, xf + sx * 28))
            box(ha, hb, (yb + y1) / 2 - 180, (yb + y1) / 2 + 180, zb + 300, zb + 310, "handle")
            ba, bb = sorted((xf, xf - sx * 330))
            box(ba, bb, yb + 40, y1 - 40, zb + 30, zb + 300, "dbox")
            end_group()
    box(cx - 60, cx + 60, y1, y1 + 6, 640, 720, "socket")            # розетки на торце
    # пуф
    round_slices(cx, y1 + 10, POUF_R, 0, POUF_H - 70, "pouf", +1, n=24)
    round_slices(cx, y1 + 10, POUF_R - 10, POUF_H - 70, POUF_H, "cushion", +1, n=24)
    box(x0 + 10, x1 - 10, y1 + 10, y1 + 30, POUF_H - 70, POUF_H, "cushion")


def glass():
    """Стеклянная перегородка у входа: чёрный профиль, 2 раздвижные двери."""
    for x0, x1, kind in GLASS:
        if kind == "fix":
            ya, yb = D, D + 20
            parts = None
        else:
            ya, yb = D + 24, D + 44
            sgn = -1 if kind == "L" else 1
            group("door_" + kind, set="doors", name="Стеклянная раздвижная дверь", dir=[sgn, 0], travel=760)
        box(x0 + 20, x1 - 20, ya + 7, yb - 7, 20, H - 20, "glass")
        for xa, xb in ((x0, x0 + 20), (x1 - 20, x1)):
            box(xa, xb, ya, yb, 0, H, "frame")
        for za, zb in ((0, 20), (H - 20, H)):
            box(x0, x1, ya, yb, za, zb, "frame")
        if kind != "fix":
            hx = x1 - 80 if kind == "L" else x0 + 60
            box(hx, hx + 20, yb, yb + 30, 900, 1500, "frame")
            end_group()
    box(0, W, D, D + 44, H - 40, H, "frame")             # верхний направляющий профиль


if __name__ == "__main__":
    build()
    print(len(boxes), "boxes")
