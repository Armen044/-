#!/usr/bin/env python3
"""Чертёж рабочего места в детской, лист А3, масштаб 1:20.

Ширина 1370: антресоль на 3 распашных шкафа до потолка, под ней открытая ниша
«пыльная роза» с LED-подсветкой, стол 750 со столешницей 38 и боковой опорой справа,
тумба 400 на 3 ящика, цоколь 80.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                          # noqa: E402
from generate import e, text, line, rect, dim_h, dim_v, leader  # noqa: E402

S = 1 / 20
T = 16                  # ЛДСП корпуса
DT = 18                 # фасады МДФ
NT = 22                 # ЛДСП ниши
W = 1370                # общая ширина
DW = W / 3              # ширина фасада ≈457
CEIL = 2660             # высота помещения (750 + 600 + 1310)
ZT = 2630               # верх антресоли, зазор 30 до потолка
ZN0, ZN1 = 1350, 1640   # ниша: низ / верх
ZSH = 2135              # полка в шкафах (верх)
UD = 355                # глубина антресоли и ниши с фасадами
UCD = UD - DT           # глубина корпуса антресоли = 337
ZD = 750                # высота стола
TT = 38                 # толщина столешницы и опоры
DD = 600                # глубина стола
PW = 400                # ширина тумбы
PD = 560                # глубина тумбы с фасадами
PCD = PD - DT           # корпус тумбы = 542
PLINTH = 80             # цоколь тумбы
DRAW = [PLINTH, 290, 501, ZD - TT]   # границы ящиков: 210 / 211 / 211
HR = 70                 # радиус ручки-полукруга
GAP = 40                # зазор до кровати
SOCK_A = (930, 1170, 810, 890)       # 2 розетки + выключатель над столом (центр Н=850)
SOCK_B = (1160, 1240, 330, 570)      # интернет + 2 розетки под столом (центр Н=450)
GREIGE = "#a39d97"
GREIGE_D = "#8e8882"
ROSE = "#d0a19d"
ROSE_D = "#b98682"
HANDLE = "#e2afa6"
WALLC = "#efedeb"
CUT = "#7d6c5b"


class V:
    def __init__(self, ox, fy):
        self.ox, self.fy = ox, fy

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    def box(self, x0, x1, z0, z1, fill=GREIGE, sw=0.2, stroke="#111", dash=None):
        rect(self.X(x0), self.Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, stroke=stroke, sw=sw, dash=dash)


def half_disc(v, cx, ztop):
    r = HR * S
    x, y = v.X(cx), v.Z(ztop)
    e(f'<path d="M{x - r:.2f},{y:.2f} A{r:.2f},{r:.2f} 0 0 0 {x + r:.2f},{y:.2f} Z" fill="{HANDLE}" stroke="#111" stroke-width="0.18"/>')


def books(v, seed=3):
    rnd = random.Random(seed)
    x = NT + 40
    cols = ["#e9e6e1", "#8c8580", "#5e5a56", "#d8d2cb", "#a8a29c", "#f0ede8", "#6f6964"]
    while x < W - NT - 60:
        if rnd.random() < 0.18:                     # стопка лёжа
            w = 220
            for k in range(3):
                v.box(x, x + w - k * 10, ZN0 + NT + k * 38, ZN0 + NT + (k + 1) * 38, fill=rnd.choice(cols), sw=0.1)
            x += w + 30
        else:
            w = rnd.randint(18, 36)
            v.box(x, x + w, ZN0 + NT, ZN0 + NT + rnd.randint(170, 225), fill=rnd.choice(cols), sw=0.1)
            x += w + 1
        if rnd.random() < 0.06:
            x += 80


def sockets(v):
    x0, x1, z0, z1 = SOCK_A
    v.box(x0, x1, z0, z1, fill="#fff", sw=0.15)
    for k in range(3):
        v.box(x0 + 10 + k * 80, x0 + 70 + k * 80, z0 + 10, z1 - 10, fill="none", sw=0.1)
    x0, x1, z0, z1 = SOCK_B
    v.box(x0, x1, z0, z1, fill="#fff", sw=0.15)
    for k in range(3):
        v.box(x0 + 10, x1 - 10, z0 + 10 + k * 80, z0 + 70 + k * 80, fill="none", sw=0.1)


def room(v, x0, x1):
    rect(v.X(x0), v.Z(CEIL + 100), (x1 - x0) * S, 100 * S, fill="url(#hatch)", sw=0.25)
    rect(v.X(x0), v.Z(0), (x1 - x0) * S, 80 * S, fill="url(#hatch)", sw=0.25)


# ---------------------------------------------------------------------------
def view_front(ox, fy):
    """Фасад: фасады закрыты, с розетками и подсветкой."""
    v = V(ox, fy)
    text(v.X(W / 2), v.Z(CEIL) - 22, "ФАСАД", size=3.4, weight="bold")
    text(v.X(W / 2), v.Z(CEIL) - 18, "фасады закрыты", size=2.1)
    room(v, -200, W + 420)
    rect(v.X(-200), v.Z(CEIL), (W + 620) * S, CEIL * S, fill=WALLC, sw=0.3)
    # антресоль: 3 фасада, открывание нажатием
    for i in range(3):
        x0, x1 = i * DW + 1, (i + 1) * DW - 1
        v.box(x0, x1, ZN1 + 2, ZT - 2, fill=GREIGE, sw=0.3)
        hinge, far = (x0, x1) if i < 2 else (x1, x0)
        line(v.X(far), v.Z(ZN1 + 2), v.X(hinge), v.Z((ZN1 + ZT) / 2), w=0.12, color="#555", dash="1 0.8")
        line(v.X(far), v.Z(ZT - 2), v.X(hinge), v.Z((ZN1 + ZT) / 2), w=0.12, color="#555", dash="1 0.8")
    # ниша
    v.box(0, W, ZN0, ZN1, fill=ROSE, sw=0.3)
    v.box(NT, W - NT, ZN0 + NT, ZN1 - NT, fill=ROSE_D, sw=0.2)
    books(v)
    rect(v.X(0), v.Z(ZN0), W * S, 300 * S, fill="url(#led)", stroke="none")
    rect(v.X(20), v.Z(ZN0) - 0.1, (W - 40) * S, 0.5, fill="#f2c46d", stroke="none")
    # стол
    v.box(0, W, ZD - TT, ZD, fill=GREIGE, sw=0.3)
    v.box(W - TT, W, 0, ZD - TT, fill=GREIGE, sw=0.3)
    # тумба
    v.box(10, PW - 10, 0, PLINTH, fill=GREIGE_D, sw=0.2)
    for a, b in zip(DRAW, DRAW[1:]):
        v.box(1, PW - 1, a + 1, b - 1, fill=GREIGE, sw=0.3)
        half_disc(v, PW / 2, b - 1)
    sockets(v)
    # кровать (условно)
    v.box(W + GAP, W + GAP + 90, 0, 900, fill="none", sw=0.2, dash="1.2 0.8", stroke="#777")
    v.box(W + GAP + 90, W + 420, 60, 520, fill="none", sw=0.2, dash="1.2 0.8", stroke="#777")
    text(v.X(W + 260), v.Z(300), "кровать", size=1.9, fill="#666")
    # размеры
    yt = v.Z(CEIL + 100) - 3
    for i in range(3):
        dim_h(v.X(i * DW), v.X((i + 1) * DW), yt, "457", size=2.0)
    yb = v.Z(0) + 10
    dim_h(v.X(0), v.X(PW), yb, str(PW), ext_from=v.Z(0) + 4.5, size=2.0)
    dim_h(v.X(PW), v.X(W - TT), yb, str(W - TT - PW), ext_from=v.Z(0) + 4.5, size=2.0)
    dim_h(v.X(W - TT), v.X(W), yb, str(TT), ext_from=v.Z(0) + 4.5, size=1.5)
    dim_h(v.X(0), v.X(W), yb + 6, str(W))
    dim_h(v.X(W), v.X(W + GAP), yb + 6, str(GAP), size=1.5)
    xl = v.X(-200) - 4
    zs = [0, ZD, ZN0, ZN1, ZT, CEIL]
    for a, b in zip(zs, zs[1:]):
        dim_v(v.Z(b), v.Z(a), xl, str(b - a), ext_from=v.X(0), size=2.0)
    dim_v(v.Z(CEIL), v.Z(0), xl - 6, str(CEIL), size=2.2)
    # розетки
    xs = v.X(860)
    dim_v(v.Z(450), v.Z(0), xs, "450", size=1.6)
    dim_v(v.Z(850), v.Z(450), xs, "400", size=1.6)
    line(xs + 1.5, v.Z(450), v.X(SOCK_B[0]), v.Z(450), w=0.12, color="#777")
    line(xs + 1.5, v.Z(850), v.X(SOCK_A[0]), v.Z(850), w=0.12, color="#777")
    dim_h(v.X(SOCK_A[1]), v.X(W), v.Z(SOCK_A[3]) - 3, "200", size=1.6)
    dim_h(v.X(SOCK_B[1]), v.X(W), v.Z(SOCK_B[2]) + 3, "130", size=1.6)
    leader(v.X(W / 2), v.Z(ZN0) + 1.5, v.X(W + 90), v.Z(1180), "LED-лента 3000 K\nв профиле", size=1.8)
    leader(v.X(DW * 2.5), v.Z(2300), v.X(W + 90), v.Z(2300), "открывание нажатием\n(push-to-open)", size=1.8)
    return v


def view_inside(ox, fy):
    """Наполнение: фасады условно сняты."""
    v = V(ox, fy)
    text(v.X(W / 2), v.Z(CEIL) - 22, "НАПОЛНЕНИЕ", size=3.4, weight="bold")
    text(v.X(W / 2), v.Z(CEIL) - 18, "фасады условно сняты", size=2.1)
    line(v.X(-150), v.Z(0), v.X(W + 150), v.Z(0), w=0.45)
    line(v.X(-150), v.Z(CEIL), v.X(W + 150), v.Z(CEIL), w=0.3, dash="2 1")
    # антресоль
    v.box(0, W, ZN1, ZT, fill="#fbfaf8", sw=0.4)
    for x in (0, DW - T / 2, 2 * DW - T / 2, W - T):
        v.box(x, x + T, ZN1, ZT)
    for z in (ZN1, ZT - T, ZSH - T):
        v.box(0, W, z, z + T)
    for i in range(3):
        x0 = i * DW + T
        rect(v.X(x0 + 40), v.Z(ZSH + 260), 300 * S, 260 * S, fill="#e7ddd0", stroke="#aaa", sw=0.12)
        rect(v.X(x0 + 50), v.Z(ZN1 + T + 200), 260 * S, 200 * S, fill="#d8ccbc", stroke="#aaa", sw=0.12)
        cx, cy = v.X(i * DW + DW / 2), v.Z(ZT - 150)
        e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.2" fill="#fff" stroke="#111" stroke-width="0.25"/>')
        text(cx, cy + 0.8, str(i + 1), size=2.2, weight="bold")
    # ниша
    v.box(0, W, ZN0, ZN1, fill=ROSE, sw=0.3)
    v.box(NT, W - NT, ZN0 + NT, ZN1 - NT, fill=ROSE_D, sw=0.2)
    books(v)
    # стол и тумба
    v.box(0, W, ZD - TT, ZD)
    v.box(W - TT, W, 0, ZD - TT)
    v.box(0, PW, 0, ZD - TT, fill="#fbfaf8", sw=0.3)
    for x in (0, PW - T):
        v.box(x, x + T, 0, ZD - TT)
    v.box(T, PW - T, PLINTH, PLINTH + T)
    v.box(T + 10, PW - T - 10, 0, PLINTH, fill=GREIGE_D, sw=0.15)
    for a, b in zip(DRAW, DRAW[1:]):
        rect(v.X(T + 13), v.Z(a + 20 + 150), (PW - 2 * T - 26) * S, 150 * S, fill="url(#drw)", stroke="#8a7560", sw=0.15)
        line(v.X(T), v.Z(a + 30), v.X(PW - T), v.Z(a + 30), w=0.25, color="#c9a227")
    sockets(v)
    # размеры
    xr = v.X(W) + 5
    zs = [0, ZD, ZN0, ZN1, ZSH, ZT]
    for a, b in zip(zs, zs[1:]):
        dim_v(v.Z(b), v.Z(a), xr, str(b - a), ext_from=v.X(W), size=1.9)
    xl = v.X(0) - 5
    for a, b in zip([0] + DRAW, DRAW):
        if b > a:
            dim_v(v.Z(b), v.Z(a), xl, str(b - a), ext_from=v.X(0), size=1.6)
    dim_v(v.Z(ZD), v.Z(DRAW[-1]), xl, str(TT), ext_from=v.X(0), size=1.3)
    yb = v.Z(0) + 10
    dim_h(v.X(0), v.X(DW), yb, "457", ext_from=v.Z(0) + 1, size=1.8)
    dim_h(v.X(DW), v.X(2 * DW), yb, "457", ext_from=v.Z(0) + 1, size=1.8)
    dim_h(v.X(2 * DW), v.X(W), yb, "456", ext_from=v.Z(0) + 1, size=1.8)
    dim_h(v.X(0), v.X(W), yb + 6, str(W))
    leader(v.X(PW / 2), v.Z(DRAW[2] + 30), v.X(PW + 120), v.Z(560), "направляющие\nполного выдвижения 500", size=1.7)
    leader(v.X(W / 2), v.Z(ZSH - 8), v.X(W / 2 + 80), v.Z(ZSH - 230), "полка", size=1.7)
    return v


def view_section(ox, fy):
    """Разрез 1–1 через тумбу (x = 200), вид справа; горизонталь – глубина от стены."""
    v = V(ox, fy)
    text(v.X(300), v.Z(CEIL) - 22, "РАЗРЕЗ 1–1", size=3.4, weight="bold")
    text(v.X(300), v.Z(CEIL) - 18, "через тумбу", size=2.1)
    rect(v.X(-100), v.Z(CEIL + 100), 100 * S, (CEIL + 180) * S, fill="url(#hatch)", sw=0.25)
    rect(v.X(-100), v.Z(CEIL + 100), (DD + 560) * S, 100 * S, fill="url(#hatch)", sw=0.25)
    rect(v.X(-100), v.Z(0), (DD + 560) * S, 80 * S, fill="url(#hatch)", sw=0.25)
    # антресоль
    for z in (ZN1, ZSH - T, ZT - T):
        v.box(0, UCD, z, z + T, fill=CUT)
    v.box(0, 4, ZN1, ZT, fill="#777")
    v.box(UCD, UD, ZN1 + 2, ZT - 2, fill=GREIGE, sw=0.3)
    # ниша
    for z in (ZN0, ZN1 - NT):
        v.box(0, UD, z, z + NT, fill=ROSE_D)
    v.box(0, 6, ZN0 + NT, ZN1 - NT, fill=ROSE_D)
    v.box(30, 230, ZN0 + NT, ZN0 + NT + 210, fill="#d8d2cb", sw=0.12)
    v.box(UD - 40, UD - 15, ZN0 - 12, ZN0, fill="#f2c46d", sw=0.15)
    rect(v.X(0), v.Z(ZN0) + 0.6, UD * S, 280 * S, fill="url(#led)", stroke="none")
    # стол
    v.box(0, DD, ZD - TT, ZD, fill=CUT)
    v.box(0, DD, 0, ZD - TT, fill="none", sw=0.15, stroke="#999")        # боковая опора за разрезом
    # тумба
    v.box(0, PCD, PLINTH, PLINTH + T, fill=CUT)
    v.box(PCD - 60, PCD - 44, 0, PLINTH, fill=CUT)                         # цоколь, утоплен на 60
    v.box(0, 4, PLINTH, ZD - TT, fill="#777")
    for i, (a, b) in enumerate(zip(DRAW, DRAW[1:])):
        v.box(PCD, PD, a + 1, b - 1, fill=GREIGE, sw=0.3)
        half_disc_side = v.X(PD)
        rect(half_disc_side, v.Z(b - 1), 8 * S, HR * S, fill=HANDLE, stroke="#111", sw=0.15)
        v.box(40, PCD - 2, a + 20, a + 20 + T, fill=CUT, sw=0.15)            # дно ящика
        v.box(40, 40 + T, a + 20, a + 170, fill=CUT, sw=0.15)                # задняя стенка ящика
        line(v.X(20), v.Z(a + 30), v.X(PCD - 5), v.Z(a + 30), w=0.25, color="#c9a227")
    # верхний ящик выдвинут (пунктир)
    a = DRAW[2]
    v.box(440, PD + 400, a + 1, DRAW[3] - 1, fill="none", sw=0.2, dash="1 0.7")
    # размеры
    yt = v.Z(CEIL + 100) - 3
    dim_h(v.X(0), v.X(UCD), yt, str(UCD), size=1.8)
    dim_h(v.X(UCD), v.X(UD), yt, str(DT), size=1.4)
    dim_h(v.X(0), v.X(UD), yt - 5, str(UD), size=2.0)
    yb = v.Z(0) + 10
    dim_h(v.X(0), v.X(PCD), yb, str(PCD), ext_from=v.Z(0) + 4.5, size=1.8)
    dim_h(v.X(PCD), v.X(PD), yb, str(DT), ext_from=v.Z(0) + 4.5, size=1.4)
    dim_h(v.X(0), v.X(DD), yb + 6, f"{DD} стол", ext_from=v.Z(0) + 4.5, size=2.0)
    dim_h(v.X(PD), v.X(PD + 400), v.Z(DRAW[3]) - 2, "ход 400", size=1.6)
    dim_v(v.Z(PLINTH), v.Z(0), v.X(PD) + 4, str(PLINTH), ext_from=v.X(PD), size=1.6)
    leader(v.X(UD - 28), v.Z(ZN0 - 6), v.X(UD + 120), v.Z(ZN0 - 240), "LED-профиль", size=1.8)
    leader(v.X(UD), v.Z(2300), v.X(UD + 120), v.Z(2450), "push-to-open", size=1.8)
    return v


def view_plan(ox, oy):
    """План: столешница, тумба и антресоль (пунктир), кресло, кровать."""
    def P(x, y):
        return ox + x * S, oy + y * S
    text(ox + W / 2 * S, oy - 9, "ПЛАН", size=3.4, weight="bold")
    rect(*P(-200, -100), (W + 620) * S, 100 * S, fill="url(#hatch)", sw=0.25)
    a, b = P(0, 0)
    rect(a, b, W * S, DD * S, fill=GREIGE, sw=0.3)
    a, b = P(0, 0)
    rect(a, b, PW * S, PD * S, fill="none", stroke="#333", sw=0.2, dash="1.2 0.8")
    a, b = P(W - TT, 0)
    rect(a, b, TT * S, DD * S, fill="none", stroke="#333", sw=0.2, dash="1.2 0.8")
    line(*P(0, UD), *P(W, UD), w=0.25, color="#555", dash="3 1")
    text(P(W / 2, 0)[0], P(0, UD - 70)[1], "антресоль и ниша над столом (глубина 355)", size=1.7, fill="#333")
    for i in range(3):                                             # раскрытие фасадов антресоли
        hinge, sgn = (i * DW, 1) if i < 2 else (W, -1)
        hx, hy = P(hinge, UD)
        r = DW * S
        sweep = 0 if sgn > 0 else 1
        e(f'<path d="M{hx:.2f},{hy + r:.2f} A{r:.2f},{r:.2f} 0 0 {sweep} {hx + sgn * r:.2f},{hy:.2f}" '
          f'fill="none" stroke="#999" stroke-width="0.15" stroke-dasharray="1 0.7"/>')
    a, b = P(0, PD)
    rect(a, b, PW * S, 400 * S, fill="none", stroke="#c9a227", sw=0.2, dash="1 0.7")
    text(P(PW / 2, 0)[0], P(0, PD + 220)[1], "ход ящиков 400", size=1.6, fill="#8a6d10")
    cx, cy = P(860, 640)
    e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{260 * S:.2f}" fill="none" stroke="#777" stroke-width="0.2" stroke-dasharray="1 0.7"/>')
    text(cx, cy + 0.7, "кресло", size=1.6, fill="#666")
    a, b = P(W + GAP, 0)
    rect(a, b, 380 * S, 950 * S, fill="none", stroke="#777", sw=0.2, dash="1.2 0.8")
    text(P(W + GAP + 190, 0)[0], P(0, 500)[1], "кровать", size=1.7, fill="#666")
    # линия разреза 1–1
    cx = P(200, 0)[0]
    line(cx, oy - 6, cx, oy + 1050 * S, w=0.3, color="#1f4e8c", dash="5 1 1 1")
    text(cx + 2.5, oy - 5, "1", size=2.6, weight="bold", fill="#1f4e8c")
    text(cx + 2.5, oy + 1050 * S + 1.5, "1", size=2.6, weight="bold", fill="#1f4e8c")
    y1 = oy + 1100 * S
    dim_h(P(0, 0)[0], P(PW, 0)[0], y1, str(PW), size=1.8)
    dim_h(P(PW, 0)[0], P(W - TT, 0)[0], y1, str(W - TT - PW), size=1.8)
    dim_h(P(W - TT, 0)[0], P(W, 0)[0], y1, str(TT), size=1.3)
    dim_h(P(0, 0)[0], P(W, 0)[0], y1 + 5, str(W), size=2.0)
    xl = P(-200, 0)[0] - 3
    dim_v(oy, oy + UD * S, xl, str(UD), size=1.7)
    dim_v(oy, oy + DD * S, xl - 5, str(DD), size=1.8)


def notes(x, y):
    text(x, y, "ПРИМЕЧАНИЯ", size=3.0, weight="bold", anchor="start")
    rows = [
        "Общая ширина 1370; высота помещения принята 2660 (750 + 600 + 1310), уточнить по месту.",
        "Антресоль 1370 × 990 × 355: корпус ЛДСП 16, 3 фасада МДФ 18 ≈455 × 986,",
        "      открывание нажатием (push-to-open), в каждом отсеке полка на Н=2135. Зазор 30 до потолка.",
        "Открытая ниша 1370 × 290 × 355, ЛДСП 22 «пыльная роза», задняя стенка в цвет;",
        "      снизу LED-лента 3000 K в профиле, длина ≈1330.",
        "Стол: столешница 1370 × 600 × 38, справа опора 38 × 712 × 600 (соединение на 45° или стяжки).",
        "Тумба 400 × 712 × 560: цоколь 80 (утоплен на 60), 3 ящика 210 / 211 / 211,",
        "      направляющие полного выдвижения 500; ручки — полукруг Ø140, розовые.",
        "Розетки: над столом 2 шт. + выключатель (центр Н=850, 200 от правого края),",
        "      под столом интернет + 2 шт. (центр Н=450, 130 от правого края).",
        "Цвета: серо-бежевый #8E8882 (фасады, стол), ниша #C4908C, ручки #E2AFA6.",
        "Глубины на исходном эскизе не указаны — приняты 355 / 600 / 560.",
    ]
    for i, s in enumerate(rows):
        text(x, y + 5.5 + i * 4.1, s, size=2.1, anchor="start")


def title_block():
    bx, by, bw, bh = 290, 252, 120, 38
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 13, bx + bw, by + 13, w=0.3)
    line(bx + 80, by + 13, bx + 80, by + bh, w=0.3)
    text(bx + bw / 2, by + 6, "РАБОЧЕЕ МЕСТО В ДЕТСКОЙ", size=3.8, weight="bold")
    text(bx + bw / 2, by + 10.5, "антресоль, ниша с подсветкой, стол с тумбой", size=2.3)
    text(bx + 3, by + 19, "1370 × 600 × 2630", size=2.4, anchor="start")
    text(bx + 3, by + 25, "стол Н=750, цоколь тумбы 80", size=2.4, anchor="start")
    text(bx + 3, by + 31, "Размеры в мм", size=2.4, anchor="start")
    text(bx + 100, by + 20, "Масштаб", size=2.2)
    text(bx + 100, by + 26, "1:20", size=3.4, weight="bold")
    text(bx + 100, by + 33, "Лист 1 (А3)", size=2.2)


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297" '
      f'font-family="{g.FONT}">')
    g.defs()
    e('<defs><linearGradient id="led" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#f6d9a8" stop-opacity="0.95"/><stop offset="1" stop-color="#f6d9a8" stop-opacity="0"/>'
      '</linearGradient></defs>')
    rect(0, 0, 420, 297, fill="#fff", stroke="none")
    rect(8, 5, 407, 287, sw=0.5)
    fy = 182
    view_front(40, fy)
    view_inside(188, fy)
    view_section(318, fy)
    view_plan(44, 220)
    notes(150, 214)
    title_block()
    e('</svg>')
    with open(os.path.join(HERE, "rabochee_mesto.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


if __name__ == "__main__":
    main()
