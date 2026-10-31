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

S = 1 / 10
FY = 318
OX = 40
F = 1.7                     # увеличение шрифта

_text = g.text


def text(x, y, s, size=2.6, **kw):
    _text(x, y, s, size=size * F, **kw)


def leader(x1, y1, x2, y2, label, anchor="start", size=2.3):
    line(x1, y1, x2, y2, w=0.18)
    e(f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="#111"/>')
    dx = 0.8 if anchor == "start" else -0.8
    for i, t in enumerate(label.split("\n")):
        text(x2 + dx, y2 + 1.2 + i * (size * F + 0.8), t, size=size, anchor=anchor)


g.text = text
_dh, _dv = dim_h, dim_v


def dim_h(*a, size=2.4, **kw):
    _dh(*a, size=max(size, 1.6), **kw)


def dim_v(*a, size=2.4, **kw):
    _dv(*a, size=max(size, 1.6), **kw)
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
    text(bx + 150, by + 26.5, "1:10", size=3.6, weight="bold")
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
    section(452, FY)
    groove_detail(55, 60)
    notes1(40, 350)
    stamp("ШКАФ С АНТРЕСОЛЬЮ И ТУМБОЙ", "Общий вид, разрез, паз подсветки", "1 (А2)",
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
        text(x, y + 7 + k * 5.1, s, size=2.0, anchor="start")


# ===========================================================================
# Лист 2: модули как в эскизе заказчика – рисунок модуля, рядом список деталей.
# Подчёркивание размера = кромка: одна черта – по одной стороне этого размера, две – по двум.
MODULES = [
    ("МОДУЛЬ 1 — нижний правый, 2 штанги", (1100, 1930, 560), "rails", [
        ((1914, 1), (560, 0), 2, "паз"), ((1100, 1), (560, 2), 1, ""), ((1068, 1), (560, 0), 2, ""),
        ((1930, 0), (1100, 0), 1, "задняя стенка")]),
    ("МОДУЛЬ 2 — нижний левый, ящики + полки", (1100, 1930, 560), "drawers", [
        ((1914, 1), (560, 0), 1, "паз"), ((1914, 1), (580, 2), 1, "паз"), ((1100, 1), (560, 2), 1, ""),
        ((1068, 1), (560, 0), 3, ""), ((1068, 1), (490, 0), 1, ""),
        ((800, 1), (480, 0), 2, "утолщение под ящики"), ((800, 1), (80, 0), 4, "утолщение под ящики"),
        ((440, 1), (130, 2), 8, ""), ((994, 2), (101, 0), 8, ""), ((994, 2), (440, 0), 4, ""),
        ((998, 2), (165, 2), 4, ""), ((1930, 0), (1084, 0), 1, "задняя стенка")]),
    ("АНТРЕСОЛИ — 2 модуля", (1100, 630, 560), "ant", [
        ((630, 1), (560, 2), 3, "паз"), ((1068, 1), (560, 0), 4, ""), ((630, 2), (580, 2), 1, "паз"),
        ((1100, 0), (630, 0), 1, "задняя стенка"), ((1084, 0), (630, 0), 1, "задняя стенка")]),
    ("ТУМБА — крышка открывается вверх", (1568, 420, 580), "tumba", [
        ((1568, 1), (404, 2), 2, ""), ((548, 1), (404, 0), 2, ""), ((1568, 2), (580, 2), 1, "дно")]),
]


def module_sketch(x, y, W, H, D, kind, sc):
    """Косоугольная проекция: фронт W × H, глубина под 45° с коэфф. 0,5. (x, y) – левый нижний угол фронта."""
    dx, dy = D * sc * 0.5 * 0.7, -D * sc * 0.5 * 0.7
    w, h = W * sc, H * sc
    st = 'fill="none" stroke="#1d2a6b" stroke-width="0.45" stroke-linejoin="round"'
    e(f'<path d="M{x},{y} h{w} v{-h} h{-w} z M{x},{y - h} l{dx},{dy} h{w} l{-dx},{-dy} '
      f'M{x + w},{y} l{dx},{dy} v{-h}" {st}/>')
    if kind == "rails":
        for zz in (H - 330,):
            line(x, y - zz * sc, x + w, y - zz * sc, w=0.4, color="#1d2a6b")
        for zz in (1538, 800):
            yy = y - zz * sc
            line(x + 3, yy, x + w - 3, yy, w=0.4, color="#1d2a6b")
            for xx in (x + 3, x + w - 3):
                e(f'<circle cx="{xx:.2f}" cy="{yy:.2f}" r="1.0" fill="#fff" stroke="#1d2a6b" stroke-width="0.4"/>')
    elif kind == "drawers":
        for zz in (816, 1207, 1598):
            line(x, y - zz * sc, x + w, y - zz * sc, w=0.4, color="#1d2a6b")
        for a, b in DR_FRONTS:
            rect(x + 3.5, y - b * sc, w - 7, (b - a) * sc, stroke="#1d2a6b", sw=0.35)
        rect(x + 1.2, y - 816 * sc, 2.3, 800 * sc, stroke="#1d2a6b", sw=0.3)
        rect(x + w - 3.5, y - 816 * sc, 2.3, 800 * sc, stroke="#1d2a6b", sw=0.3)
    elif kind == "tumba":
        for k in range(3):
            xx = x + 10 + k * (w - 20) / 2
            line(xx, y, xx, y + 4, w=0.5, color="#1d2a6b")
    # размеры
    dim_h(x, x + w, y + 6, str(W), ext_from=y + 0.5, size=2.4)
    dim_v(y - h + dy, y + dy, x + w + dx + 6, str(H), ext_from=x + w + dx, size=2.4)
    text(x + w + dx * 0.5 + 2.5, y + dy * 0.5 + 2, str(D), size=2.4, anchor="start", rot=-45)


def part_line(x, y, a, b, qty, note, fs=3.6):
    """Строка «1914 × 560 — 2 шт — паз» с подчёркиванием (кромка)."""
    cw = 0.62 * fs * F                     # ширина цифры (DejaVu Sans)
    def num(xx, v, n):
        sv = str(v)
        text(xx, y, sv, size=fs, anchor="start", fill="#1d2a6b")
        wv = len(sv) * cw
        for k in range(n):
            line(xx, y + 1.3 + k * 1.1, xx + wv, y + 1.3 + k * 1.1, w=0.35, color="#1d2a6b")
        return xx + wv
    xx = num(x, *a)
    text(xx + 1.8, y, "×", size=fs, anchor="start", fill="#1d2a6b")
    xx = num(xx + 2.4 + cw * 1.2, *b)
    tail = f" — {qty} шт" + (f" — {note}" if note else "")
    text(xx + 1, y, tail, size=fs, anchor="start", fill="#1d2a6b")


def sheet2():
    frame()
    text(297, 20, "МОДУЛИ ШКАФА — ДЕТАЛИ (ЛДСП 16)", size=4.6, weight="bold")
    text(297, 27, "подчёркнутый размер — кромка по этой стороне: одна черта — 1 сторона, две — 2 стороны; "
         "«паз» — паз 16 под подсветку, 100 от лица", size=2.1, fill="#444")
    cells = [(22, 36), (306, 36), (22, 262), (306, 262)]
    for (title, (W, H, D), kind, parts), (cx, cy) in zip(MODULES, cells):
        text(cx, cy + 4, title, size=3.0, weight="bold", anchor="start")
        sc = {"rails": 0.086, "drawers": 0.086, "ant": 0.085, "tumba": 0.072}[kind]
        hy = cy + 22 + H * sc + D * sc * 0.35
        module_sketch(cx + 6, hy, W, H, D, kind, sc)
        px = cx + (132 if kind != "tumba" else 160)
        n = len(parts)
        fs, step = (3.6, 15) if n < 9 else (3.0, 13.2)
        y0 = cy + 22 if kind != "tumba" else cy + 30
        for k, (a, b, q, nt) in enumerate(parts):
            part_line(px, y0 + k * step, a, b, q, nt, fs=fs)
    line(297, 40, 297, 410, w=0.25, color="#999")
    line(15, 256, 579, 256, w=0.25, color="#999")
    save("sheet2.svg")


if __name__ == "__main__":
    sheet1()
    sheet2()
