"""Модель кухни: параллелепипеды [x0, x1, y0, y1, z0, z1, вид]."""
from geom import *

boxes = []


def box(x0, x1, y0, y1, z0, z1, kind):
    boxes.append((x0, x1, y0, y1, z0, z1, kind))


def fy(x0, x1, z0, z1, kind="front", y=BD):
    """Фасад в плоскости y (смотрит в комнату)."""
    box(x0 + GAP / 2, x1 - GAP / 2, y, y + FT, z0, z1, kind)


def fx(y0, y1, z0, z1, kind="front", x=CORNER_X[0]):
    """Фасад правой стены (смотрит в −x)."""
    box(x - FT, x, y0 + GAP / 2, y1 - GAP / 2, z0, z1, kind)


def build():
    boxes.clear()
    # ---- пенал 400: стеклянные двери в алюминиевой раме, боковина – эмаль
    x0, x1 = PENCIL
    box(x0, x0 + 18, 0, BD + FT, 0, H, "enamel")             # левая боковина (эмаль)
    box(x0 + 18, x1, 0, BD, PL, H, "carcass")
    box(x0 + 18, x1, BD - 60, BD - 40, 0, PL, "plinth")
    for z0, z1 in ((PL + GAP, 1298), (1302, H - 4)):
        fy(x0 + 18, x1, z0, z1, "alu")
        box(x0 + 18 + 22, x1 - 22, BD + FT, BD + FT + 1, z0 + 22, z1 - 22, "glass")
    # ---- нижние модули
    for xa, xb, kind in BASES:
        box(xa, xb, 0, BD, PL, CB, "carcass")
        box(xa, xb, BD - 60, BD - 40, 0, PL, "plinth")
        if kind in ("hob", "drw", "drw2"):
            fy(xa, xb, *DR_LOW)
            fy(xa, xb, *DR_UP)
            box(xa, xb, BD - 30, BD, GOLA_MID[0], GOLA_MID[1], "gola")
        elif kind == "dw":
            fy(xa, xb, PL + GAP, GOLA_TOP[0], "front")
        else:
            fy(xa, xb, PL + GAP, GOLA_TOP[0], "front")
        box(xa, xb, BD - 30, BD, GOLA_TOP[0], CB, "gola")
    # угол под столешницей (глухая зона)
    box(CORNER_X[0], WM, 0, BD, PL, CB, "carcass")
    # столешница 3600
    box(PENCIL[1], CORNER_X[0], 0, BD + 20, CB, TOP, "top")
    box(CORNER_X[0], WM, 0, BD, CB, TOP, "top")
    # варочная панель и мойка
    box(450, 950, 40, 560, TOP, TOP + 6, "hob")
    box(2900, 3300, 80, 520, TOP - 2, TOP + 2, "sink")
    box(3310, 3340, 120, 160, TOP, TOP + 260, "tap")
    # ---- верхние шкафы
    for xa, xb, kind in UPPERS:
        box(xa, xb, 0, UD - FT, UB, H, "carcass")
        fy(xa, xb, UB, H, "front", y=UD - FT)
        if kind == "hood":
            box(xa + 40, xb - 40, 60, UD + 60, UB - 40, UB, "hood")
    # ---- колонны правой стены
    xa, xb = CORNER_X
    for y0, y1 in (FRIDGE_Y, OVEN_Y):
        box(xa, xb, y0, y1, PL, H, "carcass")
        box(xa + 40, xa + 60, y0, y1, 0, PL, "grill")
    box(xa - FT, xb, OVEN_Y[1], OVEN_Y[1] + 18, 0, H, "veneer")   # торец справа – шпон
    fx(*FRIDGE_Y, *FR_LOW)
    fx(*FRIDGE_Y, *FR_UP)
    fx(*FRIDGE_Y, *TOP_DOOR)
    fx(*OVEN_Y, *OV_DRW)
    box(xa - 30, xa, OVEN_Y[0], OVEN_Y[1], *OV_GOLA, "gola")
    fx(*OVEN_Y, *OVEN, "oven")
    fx(*OVEN_Y, *MW, "mw")
    fx(*OVEN_Y, *OV_DOOR)
    fx(*OVEN_Y, *TOP_DOOR)
    # угловой верхний на правой стене: планка 50 + шкаф 550
    y0, y1 = CORNER_UP_Y
    box(xa, xb, y0, y1, UB, H, "carcass")
    box(xa - FT, xa, y0, y0 + 50, UB, H, "filler")
    fx(y0 + 50, y1, UB, H)
    # ---- планка 130 под натяжной потолок по периметру
    box(PENCIL[0], PENCIL[1], 0, BD + FT, H, HT, "strip")
    box(PENCIL[1], CORNER_X[0], UD - FT, UD, H, HT, "strip")
    box(CORNER_X[0] - FT, CORNER_X[0], 0, OVEN_Y[1] + 18, H, HT, "strip")
    return boxes
