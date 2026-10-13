#!/usr/bin/env python3
"""3D-модель гардеробной №2 (по видео дизайнера).

Комната 2400 × 1740 × 2640. Оси: x – вдоль задней стены (слева направо от входа),
y – от задней стены к входу, z – вверх.
  Задняя стена: по центру ниша 800 с поворотно-выдвижной обувницей ALPHALUX Aiden,
  по бокам от неё проходы 234 к угловым зонам.
  Левая сторона (глубина 550): угол со штангами в 2 яруса (550 + 538), комод 500 (4 ящика),
  ниша 120 с выдвижным поворотным зеркалом у входа.
  Правая сторона (глубина 550): угол со штангами в 2 яруса (550 + 538), стеллаж 420 с полками,
  ниша 232 для гладильной доски у входа.
"""
W, D, H = 2400, 1740, 2640
T = 16
PL = 80
SD = 550                     # глубина боковых рядов и задней ниши
ANT = 2200                   # полка антресоли по периметру
RAIL, RAIL_LOW = 2130, 1080
CORNER = SD + 538            # конец угловой зоны по y = 1088
GAP = 234
NX0, NX1 = SD + GAP, W - SD - GAP     # ниша обувницы: панели 784…800 и 1600…1616
# левая сторона
L_DR = (CORNER + T, CORNER + T + 500)          # комод
L_MIR = (L_DR[1] + T, D - T)                   # ниша зеркала ~120
DR_TOP = PL + T + 4 * 200                      # 896
# правая сторона
R_SH = (CORNER + T, CORNER + T + 420)          # стеллаж
R_BRD = (R_SH[1] + T, D - T)                   # ниша доски ~200
# обувница Aiden ALF0814.10S.43
RACK_W, RACK_D, RACK_H = 764, 400, 1900
RACK_Z = PL + T
RACK_TOP = RACK_Z + RACK_H
# зеркало Lexy 480×50×1405, доска
MIR_D, MIR_T, MIR_H, MIR_Z = 480, 50, 1405, 450
BOARD_L, BOARD_W, BOARD_T = 1300, 380, 70

boxes, groups, cur = [], {}, [None]
CLOTH = ["#e9e5df", "#cfc8bf", "#b9b2aa", "#8d8680", "#f3f1ec", "#a39383", "#6f6a66", "#d8cdbf"]
COLORS = {"carcass": 0xebe8e3, "plinth": 0xd9d5cf, "front": 0xf3f1ed, "handle": 0x3a3a3a,
          "rail": 0x2b2b2b, "floor": 0xb59b80, "dbox": 0xdcd8d2, "dbottom": 0xe8e5e0}
EDGES = {"carcass": 0x9d968d, "plinth": 0x9d968d, "front": 0x9d968d}


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


def clothes_y(y0, y1, xc, ztop, length, step=75):
    n = int((y1 - y0 - 40) / step)
    for i in range(n):
        y = y0 + 40 + i * step
        ln = length - (i * 97 % 3) * 60
        box(xc - 220, xc + 220, y, y + 28, ztop - ln, ztop - 30, "cloth%d" % (i * 3 % len(CLOTH)))


def side_run(x0, x1, xf, sign):
    """Каркас бокового ряда: x0…x1 по глубине, xf – плоскость фронта, sign – направление в проход."""
    for z in (PL, ANT, H - T):
        box(x0, x1, SD, D, z, z + T, "carcass")
    box(x0, x1, D - T, D, PL, H, "carcass")                  # торец у входа
    box(x0, x1, CORNER, CORNER + T, PL, H, "carcass")        # граница угловой зоны
    pa, pb = sorted((xf - sign * 50, xf - sign * 34))
    box(pa, pb, SD, D, 0, PL, "plinth")
    la, lb = sorted((xf - sign * 22, xf - sign * 4))
    box(la, lb, SD, D - T, ANT - 10, ANT, "led")
    # угловая зона: 2 яруса штанг вдоль y от задней стены
    xc = (x0 + x1) / 2
    for z in (RAIL, RAIL_LOW):
        box(xc - 10, xc + 10, 0, CORNER, z - 10, z + 10, "rail")
    clothes_y(SD + 10, CORNER, xc, RAIL, 900)
    clothes_y(SD + 10, CORNER, xc, RAIL_LOW, 850)


def build():
    box(-100, W + 100, -100, 0, 0, H, "wall_back")
    box(-100, 0, -100, D, 0, H, "wall_left")
    box(W, W + 100, -100, D, 0, H, "wall_right")
    box(-100, W + 100, -100, D + 400, -30, 0, "floor")

    # ---- задний ряд: антресоль по всей ширине, ниша обувницы
    for z in (ANT, H - T):
        box(0, W, 0, SD, z, z + T, "carcass")
    box(T, W - T, SD - 22, SD - 4, ANT - 10, ANT, "led")
    box(0, T, 0, D, PL, H, "carcass")                         # боковины у стен
    box(W - T, W, 0, D, PL, H, "carcass")
    for x in (NX0, NX1 - T):
        box(x, x + T, 0, SD, PL, ANT, "carcass")
    box(NX0, NX1, 0, SD, PL, PL + T, "carcass")
    box(NX0, NX1, SD - 50, SD - 34, 0, PL, "plinth")
    box(0, NX0, 0, SD, PL, PL + T, "carcass")                 # дно угловых зон
    box(NX1, W, 0, SD, PL, PL + T, "carcass")
    for xa, xb in ((SD, NX0), (NX1, W - SD)):
        box(xa, xb, SD - 50, SD - 34, 0, PL, "plinth")
    for xa in (120, 1000, 1950):                             # коробки на антресоли
        box(xa, xa + 330, 100, 460, ANT + T, ANT + T + 240, "box")
    shoe_rack((NX0 + NX1) / 2)

    # ---- левая сторона
    side_run(0, SD, SD, +1)
    y0, y1 = L_DR
    for i in range(4):                                       # комод: 4 ящика
        zb = PL + T + i * 200
        group("drw_l%d" % i, type="drawer", dir=[1, 0], travel=420)
        box(SD - 18, SD, y0 + 2, y1 - 2, zb + 2, zb + 198, "front")
        cy = (y0 + y1) / 2
        box(SD, SD + 10, cy - 80, cy + 80, zb + 170, zb + 180, "handle")
        box(T + 20, SD - 18, y0 + 13, y0 + 25, zb + 25, zb + 165, "dbox")
        box(T + 20, SD - 18, y1 - 25, y1 - 13, zb + 25, zb + 165, "dbox")
        box(T + 20, T + 32, y0 + 13, y1 - 13, zb + 25, zb + 165, "dbox")
        box(T + 20, SD - 18, y0 + 13, y1 - 13, zb + 25, zb + 33, "dbottom")
        end_group()
    box(T, SD, y0, y1, DR_TOP, DR_TOP + T, "carcass")          # столешница комода
    box(T, SD, y1, y1 + T, PL, H, "carcass")                  # перегородка к нише зеркала
    for k in range(3):                                         # стопки на комоде
        box(150, 420, y0 + 40 + k * 150, y0 + 170 + k * 150, DR_TOP + T, DR_TOP + T + 90 + k * 20,
            "cloth%d" % (k + 2))
    # ниша зеркала Lexy
    yc = (L_MIR[0] + L_MIR[1]) / 2
    group("mirror", type="mirror", dir=[1, 0], travel=SD, pivot=[40, yc])
    box(40, 40 + MIR_D, yc - MIR_T / 2, yc + MIR_T / 2, MIR_Z, MIR_Z + MIR_H, "mirror_frame")
    box(60, 20 + MIR_D, yc + MIR_T / 2, yc + MIR_T / 2 + 3, MIR_Z + 20, MIR_Z + MIR_H - 20, "mirror")
    end_group()
    box(20, SD, yc - 10, yc + 10, MIR_Z + MIR_H + 5, MIR_Z + MIR_H + 25, "mirror_frame")

    # ---- правая сторона
    xf = W - SD
    side_run(xf, W, xf, -1)
    y0, y1 = R_SH
    box(xf, W, y1, y1 + T, PL, H, "carcass")
    for i in range(1, 7):                                      # стеллаж: 6 полок
        z = PL + i * (ANT - PL) / 7
        box(xf, W - T, y0, y1, z, z + T, "carcass")
        if i % 2:
            box(xf + 120, W - 120, y0 + 50, y1 - 50, z + T, z + T + 120 + i * 8, "cloth%d" % (i % 8))
    # ниша гладильной доски
    y0, y1 = R_BRD
    yc = (y0 + y1) / 2
    box(xf, W - T, y0, y1, 1560, 1560 + T, "carcass")
    group("board", type="board", dir=[-1, 0], travel=520)
    box(xf + 110, xf + 110 + BOARD_W, yc - BOARD_T / 2, yc + BOARD_T / 2,
        PL + T + 10, PL + T + 10 + BOARD_L, "board")
    end_group()
    box(xf + 180, xf + 400, yc - 55, yc + 55, 1576, 1700, "iron")
    box(W - 20 - T, W - T, yc - 40, yc + 40, 1680, 1760, "socket")


def shoe_rack(cx):
    """Обувница ALPHALUX Aiden ALF0814.10S.43: по 5 полок с двух сторон, выдвигается и поворачивается."""
    a, b = cx - RACK_W / 2, cx + RACK_W / 2
    y0 = (SD - RACK_D) / 2
    y1 = y0 + RACK_D
    yc = (y0 + y1) / 2
    for x in (cx - 200, cx + 200):
        box(x - 15, x + 15, 20, SD - 30, RACK_Z, RACK_Z + 12, "rack")
        box(x - 15, x + 15, 20, SD - 30, RACK_TOP + 2, RACK_TOP + 14, "rack")
    box(NX0 + T, NX1 - T, 0, SD - 20, RACK_TOP + 14, RACK_TOP + 14 + T, "carcass")   # полка над обувницей
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
            box(a + 20, b - 20, ya, yb, zs - 6, zs, "rack")
            yl = yb - 14 if side == 0 else ya
            box(a + 20, b - 20, yl, yl + 14, zs, zs + 30, "rack")
            for k in range(6):
                sx = a + 40 + k * 115
                ys0, ys1 = (yc + 20, yb - 16) if side == 0 else (ya + 16, yc - 20)
                box(sx, sx + 95, ys0, ys1, zs, zs + 120 - (k % 2) * 25, "shoe" if (i + k + side) % 3 else "shoe2")
    end_group()
