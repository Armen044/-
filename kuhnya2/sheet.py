#!/usr/bin/env python3
"""Чертёж кухни: фасад основной стены, развёртка правой стены, план, вид с угла. Лист А2, 1:20."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                   # noqa: E402
from generate import e, text, line, rect, dim_h, dim_v, leader   # noqa: E402
from geom import *                                     # noqa: E402,F403
import model                                           # noqa: E402

S = 1 / 20
FILL = {"carcass": "#ebe8e3", "front": "#f4f2ee", "gola": "#111111", "top": "#d3cbbf", "alu": "#9aa1a8",
        "glass": "#d4e6ec", "enamel": "#fbf8f2", "veneer": "#c99d6f", "plinth": "#5b5b5b", "grill": "#2d2d2d",
        "hob": "#222222", "sink": "#b9bec2", "tap": "#8a8a8a", "hood": "#a3a3a3", "oven": "#2f2f2f",
        "mw": "#3c3c3c", "filler": "#e2dfda", "strip": "#ffffff"}
B = model.build()


def poly(pts, fill, sw=0.18, dash=None, stroke="#222"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    e(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{d}/>')


def ortho(boxes, face, key, ox, oy):
    """Ортогональная проекция: face(b) -> (u0, u1, v0, v1) в мм, key – порядок (сначала дальние)."""
    for b in sorted(boxes, key=key):
        u0, u1, v0, v1 = face(b)
        sw = 0.12 if b[6] in ("glass", "tap") else 0.2
        rect(ox + u0 * S, oy - v1 * S, (u1 - u0) * S, (v1 - v0) * S, fill=FILL[b[6]], sw=sw)


def glass_marks(x0, x1, z0, z1, X, Z):
    for k in (0.3, 0.55):
        cx, cy = X(x0 + (x1 - x0) * k), Z(z0 + (z1 - z0) * (1 - k))
        line(cx - 2, cy + 2, cx + 2, cy - 2, w=0.15, color="#6c8a94")
        line(cx - 1, cy + 3, cx + 3, cy - 1, w=0.15, color="#6c8a94")


# ===========================================================================
def front_view(ox, fy):
    X = lambda x: ox + x * S                 # noqa: E731
    Z = lambda z: fy - z * S                 # noqa: E731
    text(X(WM / 2), Z(HT) - 15, "ВИД А — ОСНОВНАЯ СТЕНА (фасад)", size=3.6, weight="bold")
    # стена и плитка
    rect(X(0), Z(HT), WM * S, HT * S, fill="#fafafa", stroke="#999", sw=0.15)
    rect(X(PENCIL[1]), Z(UB), (CORNER_X[0] - PENCIL[1]) * S, (UB - TOP) * S, fill="url(#tile)", stroke="none")
    rect(X(GAP_UP[0]), Z(H), (GAP_UP[1] - GAP_UP[0]) * S, (H - UB) * S, fill="url(#tile)", stroke="none")
    ortho(B, lambda b: (b[0], b[1], b[4], b[5]), lambda b: (b[3], -(b[1] - b[0]) * (b[5] - b[4])), ox, fy)
    line(X(0) - 5, Z(0), X(WM) + 5, Z(0), w=0.5)
    # стекло пенала
    for z0, z1 in ((PL + GAP, 1298), (1302, H - 4)):
        glass_marks(40, 360, z0 + 40, z1 - 40, X, Z)
        for zz in range(z0 + 300, z1 - 100, 380):           # полки за стеклом
            line(X(40), Z(zz), X(360), Z(zz), w=0.15, color="#7f9aa3", dash="1 0.6")
    # скрытый внутренний ящик в верхнем ящике 3-го модуля
    rect(X(1640), Z(DR_UP[1] - 40), 520 * S, 150 * S, fill="none", stroke="#c0392b", sw=0.25, dash="1.2 0.7")
    # вытяжка, сушка
    hx0, hx1 = UPPERS[0][0], UPPERS[0][1]
    rect(X(hx0 + 40), Z(UB), (hx1 - hx0 - 80) * S, 40 * S, fill="#a3a3a3", sw=0.2)
    rect(X(hx0 + 200), Z(H), 200 * S, (H - UB) * S, fill="none", stroke="#666", sw=0.2, dash="1.2 0.7")
    text(X((hx0 + hx1) / 2), Z(2000), "ВЫТЯЖКА", size=2.0, weight="bold", fill="#444")
    text(X((hx0 + hx1) / 2), Z(2000) + 3, "встроенная", size=1.7, fill="#444")
    dx0, dx1 = UPPERS[3][0], UPPERS[3][1]
    for zz in (UB + 250, UB + 600):
        line(X(dx0 + 40), Z(zz), X(dx1 - 40), Z(zz), w=0.25, color="#666", dash="0.6 0.5")
        for k in range(9):
            xx = dx0 + 60 + k * 55
            line(X(xx), Z(zz), X(xx), Z(zz + 110), w=0.12, color="#888")
    text(X((dx0 + dx1) / 2), Z(2300), "СУШКА", size=2.0, weight="bold", fill="#444")
    text(X(2500), Z(UB + 10) - 2.5, "", size=1.5)
    # подписи на фасадах
    text(X(2500), Z(470), "ПММ 600", size=2.0, weight="bold", fill="#555")
    text(X(2500), Z(470) + 3, "встраиваемая", size=1.7, fill="#555")
    text(X(3100), Z(470), "мойка", size=2.0, fill="#555")
    text(X(3700), Z(1300), "торец — ШПОН", size=2.0, rot=-90, weight="bold", fill="#7a5530")
    text(X(3100), Z(1200), "плитка", size=1.8, fill="#888")
    # размеры
    y1 = fy + 5
    xs = [0, 400, 1000, 1600, 2200, 2800, 3400, WM]
    for a, b in zip(xs, xs[1:]):
        dim_h(X(a), X(b), y1, str(b - a), ext_from=fy + 0.5, size=2.0)
    dim_h(X(PENCIL[1]), X(WM), y1 + 6, f"{WM - PENCIL[1]} столешница", size=2.0)
    dim_h(X(0), X(WM), y1 + 12, str(WM), size=2.4)
    yt = Z(HT) - 4
    for a, b in ((0, 400), (400, 1000), (1000, 1600), (1600, 2200), (2200, 2800), (2800, 3400), (3400, WM)):
        dim_h(X(a), X(b), yt, str(b - a), ext_from=Z(HT), size=1.8)
    zs = [0, PL, CB, TOP, UB, H, HT]
    xl = X(0) - 5
    for a, b in zip(zs, zs[1:]):
        dim_v(Z(b), Z(a), xl, str(b - a), ext_from=X(0), size=1.8)
    dim_v(Z(HT), Z(0), xl - 6, str(HT), ext_from=X(0), size=2.3)
    dim_v(Z(TOP), Z(0), X(PENCIL[1]) + 3, str(TOP), size=1.8)
    # выноски
    leader(X(10), Z(1700), X(0) - 18, Z(2700) + 1, "Боковина пенала —\nЭМАЛЬ", anchor="end", size=1.8)
    leader(X(200), Z(1900), X(0) - 18, Z(2300), "Пенал 400: двери —\nстекло в алюм. раме", anchor="end", size=1.8)
    leader(X(1300), Z(GOLA_MID[0] + 20), X(1150), Z(260), "Профиль Gola (чёрный)", size=1.7)
    leader(X(1900), Z(DR_UP[1] - 100), X(1950), Z(1120), "Верхний ящик + скрытый\nвнутренний ящик", size=1.7)
    leader(X(3000), Z(H + 60), X(3150), Z(H - 120), "Планка 130 под натяжной\nпотолок (по периметру)", size=1.7)
    leader(X(1300), Z(TOP - 20), X(1350), Z(1250), "Столешница 40", size=1.7)
    return X, Z


# ===========================================================================
def right_view(ox, fy):
    U = lambda y: ox + y * S                 # noqa: E731
    Z = lambda z: fy - z * S                 # noqa: E731
    text(U(WR / 2), Z(HT) - 15, "ВИД Б — ПРАВАЯ СТЕНА", size=3.6, weight="bold")
    rect(U(0), Z(HT), WR * S, HT * S, fill="#fafafa", stroke="#999", sw=0.15)
    rect(U(0), Z(UB), BD * S, (UB - TOP) * S, fill="url(#tile)", stroke="none")
    sel = [b for b in B if b[1] > CORNER_X[0] - 100 or b[6] in ("top",)]
    ortho(sel, lambda b: (b[2], b[3], b[4], b[5]), lambda b: (-b[0], -(b[3] - b[2]) * (b[5] - b[4])), ox, fy)
    line(U(0) - 4, Z(0), U(WR) + 4, Z(0), w=0.5)
    # подписи
    y0, y1 = FRIDGE_Y
    text(U((y0 + y1) / 2), Z(1450), "ХОЛОДИЛЬНИК", size=1.9, weight="bold", fill="#555")
    text(U((y0 + y1) / 2), Z(1450) + 3, "встраиваемый", size=1.7, fill="#555")
    y0, y1 = OVEN_Y
    text(U((y0 + y1) / 2), Z(900), "ДУХОВКА 600", size=1.8, weight="bold", fill="#fff")
    text(U((y0 + y1) / 2), Z(1390), "СВЧ", size=1.8, weight="bold", fill="#fff")
    text(U((y0 + y1) / 2), Z(330), "ящик выкатной", size=1.6, fill="#555")
    text(U(300), Z(2000), "угловой", size=1.7, fill="#555")
    text(U(300), Z(2000) + 2.8, "верхний 550", size=1.7, fill="#555")
    text(U(25), Z(2000), "50", size=1.4, rot=-90, fill="#555")
    for yy in (FRIDGE_Y, OVEN_Y):
        text(U(sum(yy) / 2), Z(50) + 0.6, "вент. решётка", size=1.3, fill="#fff")
    # размеры
    y1 = fy + 5
    for a, b in ((0, 600), (600, 1200), (1200, WR)):
        dim_h(U(a), U(b), y1, str(b - a), ext_from=fy + 0.5, size=2.0)
    dim_h(U(0), U(WR), y1 + 6, str(WR), size=2.4)
    zs = [0, PL, OV_GOLA[0], OVEN[0], MW[0], MW[1], TOP_DOOR[0], H, HT]
    xr = U(WR) + 5
    for a, b in zip(zs, zs[1:]):
        dim_v(Z(b), Z(a), xr, str(b - a), ext_from=U(WR), size=1.6)
    dim_v(Z(HT), Z(0), xr + 6, str(HT), ext_from=U(WR), size=2.2)
    zs = [PL, FR_LOW[1], TOP_DOOR[0], H]
    xm = U(FRIDGE_Y[0]) + 3
    for a, b in zip(zs, zs[1:]):
        dim_v(Z(b), Z(a), xm, str(b - a), size=1.6)
    leader(U(1500), Z(OV_GOLA[0] + 20), U(1300), Z(-180), "Gola под духовкой", size=1.6)
    return U, Z


# ===========================================================================
def plan_view(ox, oy):
    X = lambda x: ox + x * S                 # noqa: E731
    Y = lambda y: oy + y * S                 # noqa: E731
    text(X(WM / 2), Y(0) - 22, "ПЛАН", size=3.6, weight="bold")
    WT = 100
    rect(X(-WT), Y(-WT), (WM + 2 * WT) * S, WT * S, fill="url(#wall)", sw=0.3)
    rect(X(WM), Y(0), WT * S, (WR + 300) * S, fill="url(#wall)", sw=0.3)
    sel = [b for b in B if b[5] <= TOP + 300 or b[1] > CORNER_X[0] - 100 or b[1] <= PENCIL[1]]
    sel = [b for b in sel if not (b[4] >= UB and b[1] > CORNER_X[0] - 100 and b[2] < BD)]
    for b in sorted(sel, key=lambda b: b[5]):
        rect(X(b[0]), Y(b[2]), (b[1] - b[0]) * S, (b[3] - b[2]) * S, fill=FILL[b[6]], sw=0.2)
    # верхние шкафы – пунктир
    rect(X(UPPERS[0][0]), Y(0), (UPPERS[-1][1] - UPPERS[0][0]) * S, UD * S, fill="none", sw=0.25, dash="1.5 0.8")
    rect(X(CORNER_X[0]), Y(0), (WM - CORNER_X[0]) * S, BD * S, fill="none", sw=0.25, dash="1.5 0.8")
    for xa, xb, k in UPPERS[1:]:
        line(X(xa), Y(0), X(xa), Y(UD), w=0.2, dash="1.5 0.8")
    # конфорки и мойка
    for cx, cy in ((570, 180), (830, 180), (570, 420), (830, 420)):
        e(f'<circle cx="{X(cx):.2f}" cy="{Y(cy):.2f}" r="{80 * S:.2f}" fill="none" stroke="#bbb" stroke-width="0.2"/>')
    rect(X(2940), Y(120), 320 * S, 360 * S, fill="#a7adb2", sw=0.2)
    text(X(700), Y(BD) + 4.5, "варочная", size=1.7)
    text(X(3100), Y(BD) + 4.5, "мойка", size=1.7)
    text(X(2500), Y(300), "ПММ", size=1.8)
    text(X(3700), Y(300), "угол (глухой)", size=1.6, fill="#555")
    text(X(3700), Y(900), "холодильник", size=1.7, rot=-90)
    text(X(3700), Y(1500), "духовка + СВЧ", size=1.7, rot=-90)
    text(X(200), Y(300), "пенал", size=1.7, rot=-90)
    # размеры
    top = Y(-WT)
    xs = [0, 400, 1000, 1600, 2200, 2800, 3400, WM]
    for a, b in zip(xs, xs[1:]):
        dim_h(X(a), X(b), top - 3.5, str(b - a), ext_from=top, size=1.8)
    dim_h(X(0), X(WM), top - 9, str(WM), ext_from=top, size=2.2)
    xr = X(WM + WT)
    for a, b in ((0, 600), (600, 1200), (1200, WR)):
        dim_v(Y(a), Y(b), xr + 4, str(b - a), ext_from=xr, size=1.8)
    dim_v(Y(0), Y(WR), xr + 10, str(WR), ext_from=xr, size=2.2)
    dim_v(Y(0), Y(BD), X(0) - 4, "600", ext_from=X(0), size=1.8)
    dim_v(Y(0), Y(UD), X(1000) + 2.5, "350", size=1.5)
    # стрелки видов
    for (x, y, s, ang) in ((2000, 2100, "А", 0), (2300, 1200, "Б", 90)):
        cx, cy = X(x), Y(y)
        if ang == 0:
            line(cx, cy, cx, cy - 7, w=0.35)
            e(f'<path d="M{cx:.2f},{cy - 8:.2f} l-1,2 l2,0 z" fill="#111"/>')
        else:
            line(cx, cy, cx + 7, cy, w=0.35)
            e(f'<path d="M{cx + 8:.2f},{cy:.2f} l-2,-1 l0,2 z" fill="#111"/>')
        text(cx - (2.5 if ang else 0), cy + (3.5 if not ang else -1.5), s, size=2.6, weight="bold")
    return X, Y


# ===========================================================================
def iso_view(ox, oy, s=1 / 26):
    """Вид с угла (аксонометрия): смотрим из комнаты на угол между стенами."""
    el = math.radians(28)
    c, si = math.cos(el), math.sin(el)
    r2 = math.sqrt(2)

    def P(x, y, z):
        u = (x + y) / r2
        v = z * c + (x - y) / r2 * si
        return ox + u * s, oy - v * s

    # пол и стены (контур)
    poly([P(0, 0, 0), P(WM, 0, 0), P(WM, WR + 200, 0), P(0, WR + 200, 0)], "#f3f1ee", sw=0.15)
    poly([P(0, 0, 0), P(WM, 0, 0), P(WM, 0, HT + 80), P(0, 0, HT + 80)], "#fafafa", sw=0.15)
    poly([P(WM, 0, 0), P(WM, WR + 200, 0), P(WM, WR + 200, HT + 80), P(WM, 0, HT + 80)], "#f6f6f6", sw=0.15)
    poly([P(400, 0, TOP), P(WM, 0, TOP), P(WM, 0, UB), P(400, 0, UB)], "url(#tile)", sw=0.1)
    # порядок отрисовки: A раньше B, если A дальше (больше x, меньше y, ниже)
    bs = list(B)
    n = len(bs)

    def bbox(b):
        pts = [P(x, y, z) for x in b[:2] for y in b[2:4] for z in b[4:6]]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return min(xs), max(xs), min(ys), max(ys)

    bb = [bbox(b) for b in bs]

    def overlap(i, j):
        a, b = bb[i], bb[j]
        return a[0] < b[1] - 0.05 and b[0] < a[1] - 0.05 and a[2] < b[3] - 0.05 and b[2] < a[3] - 0.05

    def behind(a, b):
        """a дальше b по одной из осей разделения (сначала x/y, затем z)."""
        if a[0] >= b[1] or a[3] <= b[2]:
            return True
        if b[0] >= a[1] or b[3] <= a[2]:
            return False
        return a[5] <= b[4]

    order, done = [], [False] * n
    deps = [[j for j in range(n) if j != i and overlap(i, j) and behind(bs[j], bs[i])] for i in range(n)]
    depth = lambda b: -(b[0] + b[1]) / 2 + (b[2] + b[3]) / 2 + (b[4] + b[5]) / 4   # noqa: E731
    while len(order) < n:
        progressed = False
        for i in range(n):
            if not done[i] and all(done[j] for j in deps[i]):
                done[i] = True
                order.append(i)
                progressed = True
        if not progressed:
            rest = [i for i in range(n) if not done[i]]
            i = min(rest, key=lambda i: depth(bs[i]))
            done[i] = True
            order.append(i)
    for i in order:
        x0, x1, y0, y1, z0, z1, k = bs[i]
        f = FILL[k]
        sw = 0.15
        poly([P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)], f, sw)      # фронт (+y)
        poly([P(x0, y0, z0), P(x0, y1, z0), P(x0, y1, z1), P(x0, y0, z1)], shade(f), sw)  # левый торец (−x)
        poly([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)], light(f), sw)  # верх
    # подписи
    leader(*P(0, 300, 1100), 404, 150, "эмаль", anchor="end", size=1.9)
    leader(*P(200, BD + FT, 1900), 404, 128, "стекло в\nалюм. раме", anchor="end", size=1.9)
    leader(*P(3700, WR + 18, 900), 566, 196, "шпон", size=1.9)
    leader(*P(1300, BD + FT, 500), 455, 200, "профиль Gola", anchor="end", size=1.9)
    leader(*P(700, UD, 1530), 404, 104, "вытяжка", anchor="end", size=1.9)
    text(*P(WM / 2, -200, HT + 650), "ВИД С УГЛА", size=3.6, weight="bold")


def hexmix(col, k):
    if not col.startswith("#"):
        return col
    r, g_, b = (int(col[i:i + 2], 16) for i in (1, 3, 5))
    m = lambda v: max(0, min(255, int(v * k)))   # noqa: E731
    return f"#{m(r):02x}{m(g_):02x}{m(b):02x}"


def shade(col):
    return hexmix(col, 0.82)


def light(col):
    return hexmix(col, 1.06) if col != "#ffffff" else "#ffffff"


# ===========================================================================
def notes():
    x, y = 285, 222
    text(x, y, "СОСТАВ И МАТЕРИАЛЫ", size=3.0, weight="bold", anchor="start")
    rows = [
        "Пенал 400 (слева): 2 двери — стекло в алюминиевой раме, полки внутри; левая боковина — ЭМАЛЬ",
        "Нижний ряд без ручек: профиль Gola чёрный (верхний под столешницей и средний между ящиками)",
        "Модули 600: под варочной — 2 ящика; 2-й — 2 ящика; 3-й — 2 ящика, в верхнем скрытый внутренний ящик",
        "4-й — ПММ 600 встраиваемая (один фасад); 5-й — под мойку (один фасад); угол 600 — глухой",
        "Высота низа 920 = цоколь 100 + корпус 780 + столешница 40; столешница 3600 до правой стены",
        "Фартук 600 — плитка (после кухни); над мойкой верхнего шкафа нет",
        "Верхний ряд 980 (низ 1520, верх 2500): шкаф со встроенной вытяжкой над варкой, сушка у мойки",
        "Правая стена: угловой верхний 550 + планка 50; колонна холодильника (фасады 716 / 1234 / 450)",
        "Колонна духовки: ящик выкатной под духовкой + Gola, духовка 600, СВЧ 380, фасады 466 и 450",
        "Правый торец колонн — ШПОН; вентиляционные решётки в цоколе колонн",
        "Планка 130 под натяжной потолок по всему периметру; общая высота кухни 2630",
    ]
    for i, s in enumerate(rows):
        text(x, y + 6 + i * 4.4, s, size=2.0, anchor="start")
    # условные обозначения материалов
    y = 280
    text(x, y, "МАТЕРИАЛЫ ФАСАДОВ", size=3.0, weight="bold", anchor="start")
    for i, (k, s) in enumerate((("front", "Фасады — по выбору заказчика (на чертеже светлые)"),
                               ("enamel", "Эмаль — левая боковина пенала"),
                               ("veneer", "Шпон — правый торец колонн"),
                               ("glass", "Стекло в алюминиевой раме — двери пенала"),
                               ("gola", "Профиль Gola — чёрный"))):
        yy = y + 5 + i * 4.6
        rect(x, yy - 2.6, 9, 3.6, fill=FILL[k], sw=0.25)
        text(x + 12, yy, s, size=2.0, anchor="start")
    # штамп
    bx, by, bw, bh = 405, 362, 180, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    line(bx, by + 30, bx + bw, by + 30, w=0.3)
    line(bx + 120, by + 14, bx + 120, by + bh, w=0.3)
    text(bx + bw / 2, by + 6.5, "КУХНЯ УГЛОВАЯ", size=4.2, weight="bold")
    text(bx + bw / 2, by + 11.5, "Общий вид: фасады, план, вид с угла (по эскизу от 06.10.26)", size=2.3)
    text(bx + 3, by + 20, f"Основная стена {WM} (столешница 3600), правая {WR}", size=2.4, anchor="start")
    text(bx + 3, by + 26, f"Высота {H} + планка {STRIP} = {HT} мм", size=2.4, anchor="start")
    text(bx + 3, by + 36, "Все размеры в миллиметрах", size=2.4, anchor="start")
    text(bx + 3, by + 42, "Цоколь 100, столешница 40, низ 920", size=2.4, anchor="start")
    text(bx + 150, by + 20.5, "Масштаб", size=2.3)
    text(bx + 150, by + 26.5, "1:20", size=3.6, weight="bold")
    text(bx + 150, by + 36.5, "Лист", size=2.3)
    text(bx + 150, by + 42.5, "1 (А2)", size=3.2, weight="bold")


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    e('<defs><pattern id="tile" width="5" height="5" patternUnits="userSpaceOnUse">'
      '<rect width="5" height="5" fill="#f1f3f4"/><path d="M0,0 H5 M0,0 V5" stroke="#d3d8db" stroke-width="0.2"/>'
      '</pattern></defs>')
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)
    front_view(48, 182)
    right_view(282, 182)
    iso_view(420, 175)
    plan_view(48, 250)
    notes()
    e('</svg>')
    with open(os.path.join(HERE, "kuhnya2.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


if __name__ == "__main__":
    main()
