#!/usr/bin/env python3
"""3D-модель рабочего места в детской (для интерактивной страницы).

Оси: x – вдоль стены (0 = левый край мебели), y – от стены в комнату, z – вверх от пола.
"""
import random

from sheet import (T, DT, NT, W, DW, CEIL, ZT, ZN0, ZN1, ZSH, UD, UCD, ZD, TT, DD,  # noqa: F401
                   PW, PD, PCD, PLINTH, DRAW, GAP, SOCK_A, SOCK_B, HR)

boxes = []
groups = {}
handles = []
cur = [None]
BOOKS = ["#e9e6e1", "#8c8580", "#5e5a56", "#d8d2cb", "#a8a29c", "#f0ede8", "#6f6964"]


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


def books():
    rnd = random.Random(3)
    x = NT + 40
    while x < W - NT - 60:
        if rnd.random() < 0.18:
            for k in range(3):
                box(x, x + 220 - k * 10, 60 + k * 6, 270 - k * 6, ZN0 + NT + k * 38, ZN0 + NT + (k + 1) * 38,
                    "book%d" % rnd.randrange(len(BOOKS)))
            x += 250
        else:
            w = rnd.randint(18, 36)
            box(x, x + w, 70, 270, ZN0 + NT, ZN0 + NT + rnd.randint(170, 225), "book%d" % rnd.randrange(len(BOOKS)))
            x += w + 1
        if rnd.random() < 0.06:
            x += 80


def build():
    # помещение
    box(-1500, W + 2600, -100, 0, 0, CEIL, "wall_back")
    box(-1500, W + 2600, -100, 2600, -30, 0, "floor")

    # антресоль: корпус, перегородки, полки, коробки
    for x in (0, DW - T / 2, 2 * DW - T / 2, W - T):
        box(x, x + T, 0, UCD, ZN1, ZT, "carcass")
    for z in (ZN1, ZT - T, ZSH - T):
        box(0, W, 0, UCD, z, z + T, "carcass")
    box(0, W, 0, 4, ZN1, ZT, "back")
    for i in range(3):
        x0 = i * DW + T
        box(x0 + 40, x0 + 340, 60, 300, ZSH, ZSH + 260, "box")
        box(x0 + 50, x0 + 310, 60, 300, ZN1 + T, ZN1 + T + 200, "box2")

    # ниша «пыльная роза»
    box(0, W, 0, UD, ZN1 - NT, ZN1, "rose")
    box(0, W, 0, UD, ZN0, ZN0 + NT, "rose")
    box(0, NT, 0, UD, ZN0 + NT, ZN1 - NT, "rose")
    box(W - NT, W, 0, UD, ZN0 + NT, ZN1 - NT, "rose")
    box(NT, W - NT, 0, 6, ZN0 + NT, ZN1 - NT, "rose_back")
    books()

    # стол
    box(0, W, 0, DD, ZD - TT, ZD, "top")
    box(W - TT, W, 0, DD, 0, ZD - TT, "top")

    # тумба: корпус, цоколь 80, ящики
    for x in (0, PW - T):
        box(x, x + T, 0, PCD, PLINTH, ZD - TT, "carcass")
    box(T, PW - T, 0, PCD, PLINTH, PLINTH + T, "carcass")
    box(T, PW - T, 0, 4, PLINTH, ZD - TT, "back")
    box(T + 10, PW - T - 10, PCD - 60 - T, PCD - 60, 0, PLINTH, "plinth")
    for i, (a, b) in enumerate(zip(DRAW, DRAW[1:])):
        gid = "drawer%d" % i
        group(gid, type="slide", dir=[0, 1], travel=400, needs=[])
        box(1, PW - 1, PCD, PD, a + 1, b - 1, "facade")
        x0, x1 = T + 13, PW - T - 13
        box(x0, x1, 40, PCD - 2, a + 20, a + 20 + T, "drawer_box")
        box(x0, x0 + 12, 40, PCD - 2, a + 20, a + 170, "drawer_box")
        box(x1 - 12, x1, 40, PCD - 2, a + 20, a + 170, "drawer_box")
        box(x0, x1, 40, 52, a + 20, a + 170, "drawer_box")
        box(x0 + 30, x0 + 160, 120, 380, a + 36, a + 90, "book%d" % (i * 2 + 1))
        end()
        handles.append([gid, PW / 2, PD, b - 1])

    # антресоль: 3 фасада, открывание нажатием
    hinges = [(0, -100), (DW, -100), (W, 100)]
    for i, (hx, ang) in enumerate(hinges):
        group("door%d" % i, type="hinge", pivot=[hx, UD], angle=ang)
        box(i * DW + 1, (i + 1) * DW - 1, UCD, UD, ZN1 + 2, ZT - 2, "facade")
        end()

    # розетки
    for (x0, x1, z0, z1) in (SOCK_A, SOCK_B):
        box(x0, x1, 0, 10, z0, z1, "socket")

    # кровать (обстановка)
    bx = W + GAP
    box(bx, bx + 90, 0, 900, 0, 900, "bed")
    box(bx + 90, bx + 2000, 0, 900, 60, 360, "bed")
    box(bx + 90, bx + 2000, 0, 90, 360, 900, "bed")
    box(bx + 110, bx + 1980, 100, 880, 360, 560, "linen")
    box(bx + 140, bx + 640, 110, 260, 560, 900, "pillow")
    box(bx + 140, bx + 600, 280, 420, 560, 860, "pillow2")


if __name__ == "__main__":
    build()
    print(len(boxes), "boxes", list(groups))
