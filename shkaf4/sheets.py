#!/usr/bin/env python3
"""Чертежи шкафа с антресолью и тумбой: лист 1 – общий вид без фасадов, разрез, узел паза LED;
лист 2 – фасады, зазоры, петли (расстояния от низа фасада). А2, масштаб 1:12."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                       # noqa: E402
from generate import e, text, line, rect, dim_h, dim_v, leader, LED   # noqa: E402
from geom import *                                          # noqa: E402,F403

S = 1 / 12
FY = 262
OX = 30
BODY, BODY_D, FACE, THK = "#efe7dc", "#e2d6c6", "#f3f1ee", "#ddd3c4"


def X(x):
    return OX + x * S


def Z(z):
    return FY - z * S


def r(x0, x1, z0, z1, fill=BODY, sw=0.18, dash=None, stroke="#222"):
    rect(X(x0), Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, sw=sw, dash=dash, stroke=stroke)


def legs(x0, x1, n=2):
    for k in range(n):
        xx = x0 + 60 + k * (x1 - x0 - 120 - 40) / max(1, n - 1)
        r(xx, xx + 40, 0, LEGS, fill="#555", sw=0.1)


def sensor(x, z):
    rect(X(x) - 1.1, Z(z) - 0.7, 2.2, 1.4, fill="#c0392b", stroke="none")


def frame():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)


def stamp(title, sub, sheet, extra):
    bx, by, bw, bh = 405, 362, 180, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    line(bx, by + 30, bx + bw, by + 30, w=0.3)
    line(bx + 120, by + 14, bx + 120, by + bh, w=0.3)
    text(bx + bw / 2, by + 6.5, title, size=4.0, weight="bold")
    text(bx + bw / 2, by + 11.5, sub, size=2.3)
    for k, s in enumerate(extra):
        text(bx + 3, by + 20 + k * 6 + (4 if k > 1 else 0), s, size=2.4, anchor="start")
    text(bx + 150, by + 20.5, "Масштаб", size=2.3)
    text(bx + 150, by + 26.5, "1:12", size=3.6, weight="bold")
    text(bx + 150, by + 36.5, "Лист", size=2.3)
    text(bx + 150, by + 42.5, sheet, size=3.2, weight="bold")


def save(name):
    e('</svg>')
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


# ===========================================================================
def carcass_front():
    """Общий вид без фасадов (внутреннее наполнение)."""
    line(X(0) - 4, Z(0), X(W_ALL) + 4, Z(0), w=0.5)
    # фальш-панели
    r(0, FILL, 0, LEGS + TUMBA_H + FAC, fill=THK)
    r(W_ALL - FILL, W_ALL, 0, H_ALL, fill=THK)
    # тумба
    t0, t1 = X_TUMBA, X_TUMBA + TUMBA_W
    legs(t0, t1, 3)
    r(t0, t1, LEGS, LEGS + TUMBA_H, fill="#faf7f2")
    r(t0, t1, LEGS, LEGS + T)
    r(t0 + GAP, t1 - GAP, LEGS + TUMBA_H, LEGS + TUMBA_H + FAC, fill=FACE)
    text(X((t0 + t1) / 2), Z(LEGS + 230), "ТУМБА 1568 × 580 × 420", size=2.4, weight="bold")
    text(X((t0 + t1) / 2), Z(LEGS + 230) + 3.5, "крышка-фасад открывается вверх", size=1.9, fill="#555")
    text(X((t0 + t1) / 2), Z(LEGS + 230) + 6.5, "спереди фальш-фасад (зазор 3)", size=1.9, fill="#555")
    # шкаф
    for m, xm in ((2, X_M2), (1, X_M1)):
        z0 = LEGS
        legs(xm, xm + MOD, 2)
        r(xm, xm + MOD, z0, z0 + H_LOW, fill="#faf7f2")
        r(xm, xm + T, z0, z0 + H_LOW)
        r(xm + MOD - T, xm + MOD, z0, z0 + H_LOW)
        r(xm + T, xm + MOD - T, z0, z0 + T)
        r(xm + T, xm + MOD - T, z0 + H_LOW - T, z0 + H_LOW)
        # антресоль
        za = z0 + H_LOW
        r(xm, xm + MOD, za, za + H_ANT, fill="#faf7f2")
        r(xm, xm + T, za, za + H_ANT)
        r(xm + MOD - T, xm + MOD, za, za + H_ANT)
        r(xm + T, xm + MOD - T, za, za + T)
        r(xm + T, xm + MOD - T, za + H_ANT - T, za + H_ANT)
        # подсветка в пазах боковин (условно – по внутренним граням)
        for xx in (xm + T + 1.5, xm + MOD - T - 1.5):
            zl0 = z0 + (SH_DRW + T if m == 2 else T)
            line(X(xx), Z(zl0), X(xx), Z(z0 + H_LOW - T), w=0.6, color=LED, dash="1.4 0.7")
            line(X(xx), Z(za + T), X(xx), Z(za + H_ANT - T), w=0.6, color=LED, dash="1.4 0.7")
        # датчики открывания: на крыше нижнего модуля и на дне антресоли – по одному на фасад
        for dx in (MOD * 0.25, MOD * 0.75):
            sensor(xm + dx, z0 + H_LOW - T - 12)
            sensor(xm + dx, za + T + 12)
    # модуль 2: утолщение, ящики, полки
    xm, z0 = X_M2, LEGS
    for xa in (xm + T, xm + MOD - T - THICK):
        r(xa, xa + THICK, z0 + T, z0 + T + DR_SEC, fill=THK, sw=0.15)
    for a, b in DR_FRONTS:
        r(xm + T + THICK + 3, xm + MOD - T - THICK - 3, z0 + a, z0 + b, fill="#e9dfd2")
    r(xm + T, xm + MOD - T, z0 + SH_DRW, z0 + SH_DRW + T)
    for zz in SH_M2:
        r(xm + T, xm + MOD - T, z0 + zz, z0 + zz + T)
    # модуль 1: полка, штанги
    xm = X_M1
    for zz in SH_M1:
        r(xm + T, xm + MOD - T, z0 + zz, z0 + zz + T)
    for zz in RAILS_M1:
        line(X(xm + T + 10), Z(z0 + zz), X(xm + MOD - T - 10), Z(z0 + zz), w=0.6, color="#444")
        for xx in (xm + T + 10, xm + MOD - T - 10):
            e(f'<circle cx="{X(xx):.2f}" cy="{Z(z0 + zz):.2f}" r="0.6" fill="#444"/>')
        text(X(xm + 300), Z(z0 + zz) - 1, f"штанга, ось {zz} от дна модуля", size=1.7, anchor="start", fill="#444")


def sheet1():
    frame()
    text(OX + W_ALL * S / 2, 22, "ОБЩИЙ ВИД БЕЗ ФАСАДОВ — НАПОЛНЕНИЕ И РАЗМЕРЫ", size=3.8, weight="bold")
    carcass_front()
    z0 = LEGS
    # --- горизонтальные размеры
    y1 = FY + 5
    xs = [0, FILL, X_WARD, X_M1, X_M1 + MOD, W_ALL]
    for a, b in zip(xs, xs[1:]):
        dim_h(X(a), X(b), y1, str(b - a), ext_from=FY + 0.5, size=2.0)
    dim_h(X(0), X(W_ALL), y1 + 12, str(W_ALL), size=2.4)
    for xm in (X_M2, X_M1):
        dim_h(X(xm + T), X(xm + MOD - T), y1 + 6, str(MOD - 2 * T), size=1.8)
    # --- вертикальные: общая цепочка справа
    xr = X(W_ALL) + 5
    for a, b in ((0, LEGS), (LEGS, LEGS + H_LOW), (LEGS + H_LOW, H_ALL)):
        dim_v(Z(b), Z(a), xr, str(b - a), ext_from=X(W_ALL), size=2.0)
    dim_v(Z(H_ALL), Z(0), xr + 6, str(H_ALL), ext_from=X(W_ALL), size=2.4)
    # тумба слева
    xl = X(0) - 5
    for a, b in ((0, LEGS), (LEGS, LEGS + TUMBA_H), (LEGS + TUMBA_H, LEGS + TUMBA_H + FAC)):
        dim_v(Z(b), Z(a), xl, str(b - a), ext_from=X(0), size=1.8)
    # модуль 2: ящики (фасады 165, щель 35)
    xm = X_M2
    xd = X(xm + MOD - T - THICK - 3) - 2.5
    zs = [T] + [v for ab in DR_FRONTS for v in ab] + [SH_DRW]
    for a, b in zip(zs, zs[1:]):
        dim_v(Z(z0 + b), Z(z0 + a), xd, str(b - a), size=1.3)
    text(X(xm + MOD / 2), Z(z0 + 100), "внутренние ящики, фасады 998 × 165", size=1.6, fill="#555")
    text(X(xm + MOD / 2), Z(z0 + 300), "щель под пальцы 35", size=1.6, fill="#555")
    # полки модуля 2 (в свету)
    xs2 = X(xm + 250)
    for a, b in ((SH_DRW + T, SH_M2[0]), (SH_M2[0] + T, SH_M2[1]), (SH_M2[1] + T, H_LOW - T)):
        dim_v(Z(z0 + b), Z(z0 + a), xs2, str(b - a), size=1.7)
    dim_v(Z(z0 + SH_DRW), Z(z0 + T), X(xm + 120), str(SH_DRW - T), size=1.6)
    text(X(xm + 120) + 1, Z(z0 + SH_DRW) - 1.5, "полка 490 (утоплена)", size=1.4, anchor="start", fill="#555")
    # модуль 1
    xm = X_M1
    dim_v(Z(z0 + H_LOW - T), Z(z0 + SH_M1[0] + T), X(xm + 850), str(H_LOW - T - SH_M1[0] - T), size=1.7)
    dim_v(Z(z0 + RAILS_M1[0]), Z(z0 + T), X(xm + 950), str(RAILS_M1[0] - T), size=1.6)
    dim_v(Z(z0 + RAILS_M1[1]), Z(z0 + T), X(xm + 200), str(RAILS_M1[1] - T), size=1.6)
    # антресоль
    for xm in (X_M2, X_M1):
        dim_v(Z(z0 + H_TOT - T), Z(z0 + H_LOW + T), X(xm + MOD / 2), str(H_ANT - 2 * T), size=1.7)
    # выноски
    leader(X(X_M2 + T + THICK / 2), Z(z0 + 600), X(X_M2 - 380), Z(z0 + 1300),
           "Утолщение 16 + 16 по бокам ящиков\n(панель 800×480 на планках 800×80),\nотступ 80 от лица — место под петли",
           anchor="end", size=1.8)
    leader(X(X_M1 + T + 2), Z(z0 + 1300), X(X_M1 + 300), Z(z0 + 1250), "LED-профиль в пазу боковины", size=1.7)
    leader(X(X_M1 + MOD * 0.75), Z(z0 + H_LOW - T - 12), X(X_M1 + 520), Z(z0 + 1700),
           "датчик открывания на крыше\nнижнего модуля (на каждый фасад)", size=1.6)
    leader(X(X_M1 + MOD * 0.75), Z(z0 + H_LOW + T + 12), X(X_M1 + 520), Z(z0 + 2120),
           "датчик на дне антресоли", size=1.6)
    text(X(W_ALL - FILL / 2) - 0.8, Z(1300), "фальш-панель 16", size=1.6, rot=-90, fill="#555")
    text(X(FILL / 2) - 0.8, Z(260), "фальш 16", size=1.5, rot=-90, fill="#555")
    for xm, s in ((X_M2, "МОДУЛЬ 2 — ящики + полки"), (X_M1, "МОДУЛЬ 1 — 2 штанги")):
        text(X(xm + MOD / 2), Z(LEGS + H_LOW + H_ANT - 120), "АНТРЕСОЛЬ 1100 × 630", size=2.0, weight="bold", fill="#555")
        text(X(xm + MOD / 2), Z(LEGS + H_LOW - 150), s, size=2.2, weight="bold")
    section(372, FY)
    groove_detail(460, 70)
    notes1(445, 190)
    stamp("ШКАФ С АНТРЕСОЛЬЮ И ТУМБОЙ", "Общий вид без фасадов, разрез, паз подсветки", "1 (А2)",
          [f"Габариты {W_ALL} × {DEPTH} × {H_ALL}", "Корпус ЛДСП 16, задняя ЛДСП 16", "Размеры в мм",
           "Ножки 80, отступ 50 от лица"])
    save("sheet1.svg")


def section(ox, fy):
    """Разрез А–А по модулю 2 (вид слева): y – глубина от стены, z – высота."""
    Y = lambda y: ox + y * S          # noqa: E731
    Zs = lambda z: fy - z * S         # noqa: E731
    text(Y(DEPTH / 2), 22, "РАЗРЕЗ А–А", size=3.4, weight="bold")
    text(Y(DEPTH / 2), 26.5, "по модулю 2, вид слева", size=1.9)
    line(Y(0) - 3, Zs(0), Y(DEPTH) + 3, Zs(0), w=0.5)
    rect(Y(0) - 2, Zs(H_ALL), 2, H_ALL * S, fill="url(#wall)", sw=0.2)
    z0 = LEGS
    rect(Y(0), Zs(z0 + H_TOT), BACK * S, H_TOT * S, fill=BODY, sw=0.2)           # задняя стенка
    rect(Y(BACK), Zs(z0 + H_TOT), D * S, H_TOT * S, fill="#faf7f2", sw=0.2)      # боковина (фон)
    for zz in (0, H_LOW - T, H_LOW, H_TOT - T):
        rect(Y(BACK), Zs(z0 + zz + T), D * S, T * S, fill=BODY_D, sw=0.2)
    for zz in SH_M2:
        rect(Y(BACK), Zs(z0 + zz + T), D * S, T * S, fill=BODY_D, sw=0.2)
    rect(Y(BACK + D - 490), Zs(z0 + SH_DRW + T), 490 * S, T * S, fill=BODY_D, sw=0.2)
    # утолщение (за разрезом – пунктир) и ящики
    rect(Y(BACK), Zs(z0 + T + DR_SEC), (D - 80) * S, DR_SEC * S, fill="none", sw=0.2, dash="1 0.6")
    for a, b in DR_FRONTS:
        rect(Y(BACK + D - T - 440), Zs(z0 + a + 130), 440 * S, 130 * S, fill="#f3ece2", sw=0.15)
        rect(Y(BACK + D - T), Zs(z0 + b), T * S, (b - a) * S, fill="#e9dfd2", sw=0.2)
    # фасады
    rect(Y(BACK + D), Zs(z0 + DOOR_LOW_H), FAC * S, DOOR_LOW_H * S, fill=FACE, sw=0.25)
    rect(Y(BACK + D), Zs(z0 + H_TOT), FAC * S, DOOR_ANT_H * S, fill=FACE, sw=0.25)
    # ножки: 50 от лица корпуса и у задней стенки
    face = BACK + D
    for yy in (face - LEG_OFF - 40, BACK + 30):
        rect(Y(yy), Zs(LEGS), 40 * S, LEGS * S, fill="#555", sw=0.1)
    dim_h(Y(face - LEG_OFF), Y(face), Zs(0) + 4, str(LEG_OFF), ext_from=Zs(0), size=1.6)
    # паз LED: 100 от лица
    yl = face - LED_FROM_FACE
    line(Y(yl), Zs(z0 + T), Y(yl), Zs(z0 + H_TOT - T), w=0.5, color=LED, dash="1.4 0.7")
    dim_h(Y(yl), Y(face), Zs(z0 + H_TOT) - 4, str(LED_FROM_FACE), ext_from=Zs(z0 + H_TOT), size=1.6)
    # датчики
    for zz in (H_LOW - T - 12, H_LOW + T + 12):
        rect(Y(face - 60) - 1, Zs(z0 + zz) - 0.7, 2.2, 1.4, fill="#c0392b", stroke="none")
    # размеры глубины
    yb = Zs(0) + 11
    for a, b in ((0, BACK), (BACK, face), (face, DEPTH)):
        dim_h(Y(a), Y(b), yb, str(b - a), ext_from=Zs(0) + 0.5, size=1.6)
    dim_h(Y(0), Y(DEPTH), yb + 6, str(DEPTH), size=1.9)
    dim_v(Zs(z0 + H_TOT), Zs(z0 + H_LOW), Y(DEPTH) + 4, str(H_ANT), ext_from=Y(DEPTH), size=1.6)
    dim_v(Zs(z0 + H_LOW), Zs(z0), Y(DEPTH) + 4, str(H_LOW), ext_from=Y(DEPTH), size=1.6)
    dim_v(Zs(z0), Zs(0), Y(DEPTH) + 4, str(LEGS), ext_from=Y(DEPTH), size=1.6)


def groove_detail(ox, oy):
    """Узел Б: паз под врезной профиль LED в боковине, вид сверху, М 1:2."""
    s = 0.5
    text(ox + 50, oy - 22, "УЗЕЛ Б — ПАЗ ПОД ПОДСВЕТКУ", size=3.0, weight="bold")
    text(ox + 50, oy - 17.5, "сечение боковины, вид сверху, М 1:2", size=1.9)
    L = 180
    # боковина 16 (горизонтально – глубина вдоль x), лицо справа
    x0 = ox
    rect(x0, oy, L * s, T * s, fill=BODY, sw=0.3)
    gx = x0 + (L - LED_FROM_FACE - LED_PROFILE) * s
    rect(gx, oy + (T - 8) * s, LED_PROFILE * s, 8 * s, fill="#fff", sw=0.25)
    rect(gx + 1 * s, oy + (T - 8) * s, (LED_PROFILE - 2) * s, 2 * s, fill="#d9d9d9", sw=0.15)
    rect(gx + 2 * s, oy + (T - 6) * s, (LED_PROFILE - 4) * s, 2 * s, fill=LED, stroke="none")
    # фасад
    rect(x0 + L * s, oy - 30 * s, FAC * s, 70 * s, fill=FACE, sw=0.3)
    text(x0 + L * s + FAC * s / 2, oy + 30, "фасад 20", size=1.7, rot=-90)
    dim_h(gx + LED_PROFILE * s, x0 + L * s, oy + T * s + 6, str(LED_FROM_FACE), ext_from=oy + T * s, size=1.8)
    dim_h(gx, gx + LED_PROFILE * s, oy + T * s + 11, str(LED_PROFILE), ext_from=oy + T * s, size=1.8)
    dim_v(oy, oy + T * s, x0 - 3, "16", size=1.6)
    text(x0 + 10, oy - 3, "боковина ЛДСП 16 (внутренняя грань снизу)", size=1.7, anchor="start")
    leader(gx + LED_PROFILE * s / 2, oy + (T - 4) * s, gx - 20, oy + 28,
           "паз 16 × 8 по всей длине боковины,\nпрофиль врезной 16 + LED-лента", anchor="end", size=1.7)


def notes1(x, y):
    text(x, y, "ПРИМЕЧАНИЯ", size=3.0, weight="bold", anchor="start")
    rows = [
        "1. Все размеры полок и ящиков — в свету (между ЛДСП). Отсчёт высот — от низа модуля.",
        "2. Ящики внутренние: 4 шт, фасады 998 × 165, щель под пальцы 35 между фасадами.",
        "3. В модуле с ящиками утолщение по бокам 16 + 16: панель 800×480 на планках 800×80,",
        "    отступ 80 от лица — ящики не задевают петли фасадов.",
        "4. Подсветка: паз 16 в боковинах по всей длине, 100 от лица; профиль врезной 16 + лента.",
        "    В модуле 2 лента — выше полки над ящиками.",
        "5. Датчики открывания фасадов: на крыше нижних модулей и на дне антресолей — по 1 на фасад.",
        "6. Ножки 80, отступ 50 от лица корпуса. Фальш-панели 16 по бокам (справа — на всю высоту).",
        "7. Глубина: корпус 560 + задняя ЛДСП 16 + фасад 20 = 596. Левая боковина 580 — до лица фасадов.",
    ]
    for k, s in enumerate(rows):
        text(x, y + 6 + k * 4.4, s, size=2.0, anchor="start")


# ===========================================================================
def swing(xa, xb, ya, yb, side):
    st = dict(w=0.18, color="#9a9a9a", dash="1.4 0.9")
    if side == "L":
        line(xa, ya, xb, (ya + yb) / 2, **st)
        line(xa, yb, xb, (ya + yb) / 2, **st)
    elif side == "R":
        line(xb, ya, xa, (ya + yb) / 2, **st)
        line(xb, yb, xa, (ya + yb) / 2, **st)
    else:                                   # крышка вверх: петли сзади (сверху на виде)
        line(xa, yb, (xa + xb) / 2, ya, **st)
        line(xb, yb, (xa + xb) / 2, ya, **st)


def sheet2():
    frame()
    text(OX + W_ALL * S / 2, 22, "ФАСАДЫ — РАЗМЕРЫ, ЗАЗОРЫ 3 мм, ПЕТЛИ", size=3.8, weight="bold")
    text(OX + W_ALL * S / 2, 27, "пунктиром за фасадами — полки и ящики (петли не попадают на полки)", size=2.0, fill="#555")
    line(X(0) - 4, Z(0), X(W_ALL) + 4, Z(0), w=0.5)
    r(0, FILL, 0, LEGS + TUMBA_H + FAC, fill=THK)
    r(W_ALL - FILL, W_ALL, 0, H_ALL, fill=THK)
    # тумба: фальш-фасад и крышка
    t0 = X_TUMBA
    legs(t0, t0 + TUMBA_W, 3)
    r(t0 + GAP, t0 + TUMBA_W - GAP, LEGS, LEGS + FALSE_FRONT[1], fill=FACE, sw=0.3)
    r(t0 + GAP, t0 + TUMBA_W - GAP, LEGS + TUMBA_H, LEGS + TUMBA_H + FAC, fill="#e9e4dc", sw=0.3)
    text(X(t0 + TUMBA_W / 2), Z(LEGS + 230), f"ФАЛЬШ-ФАСАД {FALSE_FRONT[0]} × {FALSE_FRONT[1]}", size=2.2, weight="bold")
    text(X(t0 + TUMBA_W / 2), Z(LEGS + 230) + 3.5, f"над ним зазор 3, крышка-фасад {LID[0]} × {LID[1]}", size=1.9)
    text(X(t0 + TUMBA_W / 2), Z(LEGS + 230) + 6.5, "открывание вверх: 3 петли сзади + 2 газлифта", size=1.9)
    # фасады шкафа
    for i, (dx, w) in enumerate(zip(DOOR_X, DOOR_W)):
        x0 = X_WARD + dx
        side = "L" if i % 2 == 0 else "R"
        for zb, h, hinges in ((LEGS, DOOR_LOW_H, HINGE_LOW), (LEGS + H_LOW + 1, DOOR_ANT_H, HINGE_ANT)):
            r(x0, x0 + w, zb, zb + h, fill=FACE, sw=0.3)
            swing(X(x0), X(x0 + w), Z(zb + h), Z(zb), side)
            hx = x0 + 22 if side == "L" else x0 + w - 22
            for hz in hinges:
                e(f'<circle cx="{X(hx):.2f}" cy="{Z(zb + hz):.2f}" r="{17.5 * S:.2f}" fill="#fff" stroke="#c0392b" stroke-width="0.25"/>')
            # размеры петель от низа фасада – на 1-м фасаде каждого ряда и на 3-м
            if i in (0, 3):
                xd = X(x0 + (w + 40 if side == "R" else -40)) + (2 if side == "R" else -2)
                pts = [0] + hinges + [h]
                for a, b in zip(pts, pts[1:]):
                    dim_v(Z(zb + b), Z(zb + a), xd, str(b - a), size=1.4)
        text(X(x0 + w / 2), Z(LEGS + 1000), f"{w} × {DOOR_LOW_H}", size=2.0, weight="bold")
        text(X(x0 + w / 2), Z(LEGS + H_LOW + 330), f"{w} × {DOOR_ANT_H}", size=1.9, weight="bold")
        text(X(x0 + w / 2), Z(LEGS + 900), "петли вкладные" if i == 0 else "петли накладные", size=1.5, fill="#c0392b")
    # полки и ящики за фасадами (поверх – пунктир)
    st = dict(w=0.3, color="#8c7b62", dash="1.6 0.9")
    for xm, shelves in ((X_M2, [SH_DRW] + SH_M2), (X_M1, SH_M1)):
        for zz in [0, H_LOW - T] + shelves:
            line(X(xm + T), Z(LEGS + zz + T / 2), X(xm + MOD - T), Z(LEGS + zz + T / 2), **st)
        for zz in (H_LOW + T / 2, H_TOT - T / 2):
            line(X(xm + T), Z(LEGS + zz), X(xm + MOD - T), Z(LEGS + zz), **st)
    for a, b in DR_FRONTS:
        rect(X(X_M2 + T + THICK + 3), Z(LEGS + b), (MOD - 2 * T - 2 * THICK - 6) * S, (b - a) * S,
             fill="none", stroke="#8c7b62", sw=0.2, dash="1 0.6")
    # размеры по ширине
    y1 = FY + 5
    pts = [0, FILL, X_TUMBA + GAP, X_TUMBA + TUMBA_W - GAP]
    for dx, w in zip(DOOR_X, DOOR_W):
        pts += [X_WARD + dx, X_WARD + dx + w]
    pts += [W_ALL - FILL, W_ALL]
    labs = []
    for a, b in zip(pts, pts[1:]):
        if b - a > 0:
            dim_h(X(a), X(b), y1 + (0 if b - a > 50 else 0), str(b - a), ext_from=FY + 0.5, size=1.6 if b - a < 50 else 2.0)
    dim_h(X(0), X(W_ALL), y1 + 7, str(W_ALL), size=2.4)
    # высоты справа
    xr = X(W_ALL) + 14
    zs = [0, LEGS, LEGS + DOOR_LOW_H, LEGS + H_LOW + 1, H_ALL]
    for a, b in zip(zs, zs[1:]):
        dim_v(Z(b), Z(a), xr, str(b - a), ext_from=X(W_ALL), size=1.8)
    dim_v(Z(H_ALL), Z(0), xr + 6, str(H_ALL), ext_from=X(W_ALL), size=2.3)
    xl = X(0) - 5
    for a, b in ((0, LEGS), (LEGS, LEGS + FALSE_FRONT[1]), (LEGS + FALSE_FRONT[1], LEGS + TUMBA_H),
                 (LEGS + TUMBA_H, LEGS + TUMBA_H + FAC)):
        dim_v(Z(b), Z(a), xl, str(b - a), ext_from=X(0), size=1.6)
    table2(380, 40)
    stamp("ШКАФ С АНТРЕСОЛЬЮ И ТУМБОЙ", "Фасады: размеры, зазоры, петли", "2 (А2)",
          ["Фасады толщиной 20, зазор 3", "Петли — от низа фасада до оси чашки", "Размеры в мм",
           "Полки за фасадами — пунктир"])
    save("sheet2.svg")


def table2(x, y):
    text(x, y, "СПЕЦИФИКАЦИЯ ФАСАДОВ", size=3.0, weight="bold", anchor="start")
    rows = [("Ф1", "нижний, левый", f"{DOOR_W[0]} × {DOOR_LOW_H}", 1, "вкладные 5"),
            ("Ф2", "нижний", f"{DOOR_W[1]} × {DOOR_LOW_H}", 1, "накладные 5"),
            ("Ф3–Ф4", "нижние", f"{DOOR_W[2]} × {DOOR_LOW_H}", 2, "накладные 5 + 5"),
            ("А1", "антресоль, левый", f"{DOOR_W[0]} × {DOOR_ANT_H}", 1, "вкладные 2"),
            ("А2", "антресоль", f"{DOOR_W[1]} × {DOOR_ANT_H}", 1, "накладные 2"),
            ("А3–А4", "антресоль", f"{DOOR_W[2]} × {DOOR_ANT_H}", 2, "накладные 2 + 2"),
            ("Т1", "крышка тумбы", f"{LID[0]} × {LID[1]}", 1, "3 петли + 2 газлифта"),
            ("Т2", "фальш-фасад тумбы", f"{FALSE_FRONT[0]} × {FALSE_FRONT[1]}", 1, "глухой, на конфирматы/стяжки")]
    cols = [0, 18, 52, 86, 98]
    hdr = ["Поз.", "Фасад", "Размер", "Кол.", "Петли"]
    rect(x, y + 3, 150, 6, fill="#eee", sw=0.25)
    for c, h in zip(cols, hdr):
        text(x + c + 1.5, y + 7.2, h, size=2.1, anchor="start", weight="bold")
    for k, row in enumerate(rows):
        yy = y + 9 + k * 6
        rect(x, yy, 150, 6, fill="none", sw=0.2)
        for c, v in zip(cols, row):
            text(x + c + 1.5, yy + 4.2, str(v), size=2.1, anchor="start")
    y2 = y + 9 + len(rows) * 6 + 10
    text(x, y2, "ПЕТЛИ — РАССТОЯНИЕ ОТ НИЗА ФАСАДА ДО ОСИ ЧАШКИ", size=2.8, weight="bold", anchor="start")
    text(x, y2 + 6, "Нижние фасады 1928: " + " · ".join(str(v) for v in HINGE_LOW), size=2.2, anchor="start")
    text(x, y2 + 11, "Антресоль 629: " + " · ".join(str(v) for v in HINGE_ANT), size=2.2, anchor="start")
    text(x, y2 + 16, "Чашка Ø35, отступ 22 от края фасада (по оси).", size=2.0, anchor="start", fill="#444")
    text(x, y2 + 21, "Полки (от низа модуля): ящики до 816, полка 816–832; 1207–1223; 1598–1614; крыша 1914.",
         size=2.0, anchor="start", fill="#444")
    text(x, y2 + 26, "Ближайшая петля к полке — не ближе 150 мм по оси: 1020 / 1207, 1410 / 1598, 1810 / 1914.",
         size=2.0, anchor="start", fill="#444")
    text(x, y2 + 31, "Ф1 и А1 — вкладные петли: левая боковина 580 выступает до лица фасадов.",
         size=2.0, anchor="start", fill="#444")
    text(x, y2 + 36, "Открывание: вершина треугольника — сторона открывания, основание — петли.",
         size=2.0, anchor="start", fill="#444")


if __name__ == "__main__":
    sheet1()
    sheet2()
