#!/usr/bin/env python3
"""Лист 2: вид сбоку (разрез А–А), разрез Б–Б по нише гладильной доски,
объёмные виды (3D). Использует общие функции и размеры из generate.py.
Перед запуском нужно отрендерить 3d_front.png и 3d_axo.png (render3d.js).
"""
import base64
import os

import generate as g
from generate import (S, T, H, D, DEPTH, PLINTH, ANT, RAIL, R1, R2, SIDE,
                      RACK_Y, RACK_D, RACK_Z, RACK_TOP, RACK_SHELF, BOARD_L, BOARD_W, LED, e, text, line, rect,
                      MIR_D, MIR_T, MIR_H, MIR_Z, LM,
                      dim_h, dim_v, leader)

HERE = os.path.dirname(os.path.abspath(__file__))
FY = 222                 # пол на разрезах (координата листа)
CUT = "#7d6c5b"          # заливка ЛДСП в разрезе


def Zf(z):
    return FY - z * S


def wall_cut(x, y, w, h):
    rect(x, y, w, h, fill="url(#wall)", sw=0.3)


# ===========================================================================
# Разрез А–А: секущая плоскость x=1200 (через середину прохода), взгляд вправо
# ===========================================================================
def section_a(ox):
    def U(u):
        return ox + u * S

    WT = 100
    text(U(D / 2), Zf(H) - 17, "ВИД СБОКУ — РАЗРЕЗ А–А", size=3.6, weight="bold")
    text(U(D / 2), Zf(H) - 12.5, "плоскость через середину прохода, взгляд на правую стену", size=2.2)

    # перекрытия и стены в разрезе
    wall_cut(U(-WT), Zf(0), (D + 2 * WT) * S, 60 * S)                 # пол
    wall_cut(U(-WT), Zf(H + 60), (D + 2 * WT) * S, 60 * S)            # потолок
    wall_cut(U(-WT), Zf(H), WT * S, H * S)                            # задняя стена
    wall_cut(U(D), Zf(H), WT * S, (H - 2100) * S)                     # перемычка над дверью
    line(U(D), Zf(2100), U(D), Zf(0), w=0.2, color="#888", dash="1.5 1")
    line(U(D + WT), Zf(2100), U(D + WT), Zf(0), w=0.2, color="#888", dash="1.5 1")
    text(U(D + WT / 2), Zf(1050), "дверной проём", size=1.8, rot=-90, fill="#666")

    # --- фон: правая стена (П1, П2) – бледно
    e('<g opacity="0.38">')
    old = g.FLOOR_Y
    g.FLOOR_Y = FY
    g.elevation_right(U(DEPTH))
    g.FLOOR_Y = old
    e('</g>')
    # фон: перегородка З2/З3 за плоскостью разреза
    rect(U(0), Zf(H), DEPTH * S, (H - PLINTH) * S, fill="#efe9e2", stroke="#bbb", sw=0.15)

    # --- задний ряд в разрезе (секция З2)
    def cutp(u0, u1, z0, z1, fill=CUT):
        rect(U(u0), Zf(z1), (u1 - u0) * S, (z1 - z0) * S, fill=fill, stroke="#111", sw=0.2)

    cutp(0, DEPTH, PLINTH, PLINTH + T)                           # дно
    cutp(DEPTH - 50, DEPTH - 34, 0, PLINTH)                       # цоколь
    # обувница Aiden (вид сбоку): каркас, центральная стенка, по 5 полок с двух сторон
    ra, rb = RACK_Y, RACK_Y + RACK_D
    rc = (ra + rb) / 2
    DK = "#3f4245"
    cutp(20, DEPTH - 30, RACK_Z, RACK_Z + 12, fill=DK)                    # направляющая низ
    cutp(20, DEPTH - 30, RACK_TOP + 2, RACK_SHELF, fill=DK)               # направляющая верх
    rect(U(ra), Zf(RACK_TOP), RACK_D * S, (RACK_TOP - RACK_Z - 14) * S, fill="#f1efed", stroke=DK, sw=0.3)
    for z in (RACK_Z + 14, RACK_TOP - 20):
        cutp(ra, rb, z, z + 20, fill=DK)
    cutp(rc - 4, rc + 4, RACK_Z + 34, RACK_TOP - 20, fill="#5a5d60")
    step = (RACK_TOP - RACK_Z - 14 - 40) / 5
    for i in range(5):
        zs = RACK_Z + 34 + i * step + 30
        for ya, yb, lip in ((rc + 4, rb, rb - 14), (ra, rc - 4, ra)):
            cutp(ya, yb, zs - 6, zs, fill=DK)
            cutp(lip, lip + 14, zs, zs + 30, fill=DK)
            sa, sb = (rc + 20, rb - 16) if ya > rc else (ra + 16, rc - 20)
            rect(U(sa), Zf(zs + 110), (sb - sa) * S, 110 * S, fill="#d9cfc4", stroke="#8b7f73", sw=0.15)
    cutp(0, DEPTH - 20, RACK_SHELF, RACK_SHELF + T)
    rect(U(DEPTH - 40), Zf(RACK_SHELF), 18 * S, 10 * S, fill=LED, stroke="#7a5a00", sw=0.15)
    rect(U(120), Zf(RACK_SHELF + T + 180), 250 * S, 180 * S, fill="#e3d6c6", stroke="#aaa", sw=0.15)
    cutp(0, DEPTH, ANT, ANT + T)
    rect(U(DEPTH - 22), Zf(ANT), 18 * S, 10 * S, fill=LED, stroke="#7a5a00", sw=0.15)
    rect(U(120), Zf(ANT + T + 260), 400 * S, 260 * S, fill="#e3d6c6", stroke="#aaa", sw=0.15)
    cutp(0, DEPTH, H - T, H)

    # --- размеры
    yb = FY + 9
    dim_h(U(0), U(DEPTH), yb, "600", ext_from=FY + 1)
    dim_h(U(DEPTH), U(D), yb, f"{SIDE} проход вдоль боковых шкафов", ext_from=FY + 1)
    dim_h(U(0), U(D), yb + 7, str(D))
    dim_h(U(RACK_Y), U(RACK_Y + RACK_D), Zf(RACK_Z) + 3.2, str(RACK_D), size=1.8)
    zs = [0, PLINTH, RACK_Z, RACK_TOP, RACK_SHELF + T, ANT, H]
    xl = U(-100) - 5
    for a, b in zip(zs, zs[1:]):
        dim_v(Zf(b), Zf(a), xl, str(b - a), ext_from=U(-100), size=2.0)
    dim_v(Zf(H), Zf(0), xl - 6, str(H), ext_from=U(-100))

    # --- выноски
    leader(U(DEPTH - 12), Zf(ANT - 5), U(DEPTH + 120), Zf(ANT) + 7,
           "LED-профиль под антресолью", size=2.0)
    leader(U(DEPTH - 30), Zf(RACK_SHELF - 5), U(DEPTH + 120), Zf(RACK_SHELF) + 5,
           "LED по краю полки", size=2.0)
    leader(U(RACK_Y + RACK_D - 40), Zf(1100), U(DEPTH + 120), Zf(1100),
           "Обувница ALPHALUX Aiden\nALF0814.10S.43, 764×400×1850,\n10 полок (5 + 5), тёмно-серый:\nвыдвинуть и повернуть 180°", size=2.0)
    text(U(300), Zf(H - 220), "З2", size=2.4, weight="bold")
    text(U(300), Zf(H - 300), "в разрезе", size=1.8, fill="#555")
    text(U(DEPTH + SIDE / 2), Zf(H) - 6.5, "правая стена (П1, П2) — за плоскостью разреза", size=1.9, fill="#666")


# ===========================================================================
# Разрез Б–Б: через узкую нишу гладильной доски, вид сбоку
# ===========================================================================
def section_b(ox):
    # h – расстояние от правой стены (0) к проходу (600)
    def U(h):
        return ox + h * S

    WT = 100
    text(U(DEPTH / 2), Zf(H) - 17, "РАЗРЕЗ Б–Б", size=3.6, weight="bold")
    text(U(DEPTH / 2), Zf(H) - 12.5, "ниша гладильной доски, вид сбоку", size=2.2)

    wall_cut(U(-WT), Zf(H + 60), (DEPTH + WT) * S, 60 * S)
    wall_cut(U(-WT), Zf(0), (DEPTH + WT + 60) * S, 60 * S)
    wall_cut(U(-WT), Zf(H), WT * S, H * S)
    # фон – торцевая стенка у входа
    rect(U(0), Zf(H), DEPTH * S, (H - PLINTH) * S, fill="#efe9e2", stroke="#bbb", sw=0.15)

    def cutp(h0, h1, z0, z1, fill=CUT):
        rect(U(h0), Zf(z1), (h1 - h0) * S, (z1 - z0) * S, fill=fill, stroke="#111", sw=0.2)

    cutp(0, DEPTH, PLINTH, PLINTH + T)
    cutp(DEPTH - 50, DEPTH - 34, 0, PLINTH)
    for z in (1560, 1880):
        cutp(0, DEPTH, z, z + T)
    rect(U(DEPTH - 22), Zf(1880), 18 * S, 10 * S, fill=LED, stroke="#7a5a00", sw=0.15)
    cutp(0, DEPTH, ANT, ANT + T)
    rect(U(DEPTH - 22), Zf(ANT), 18 * S, 10 * S, fill=LED, stroke="#7a5a00", sw=0.15)
    cutp(0, DEPTH, H - T, H)

    # гладильная доска (лицевая плоскость видна целиком)
    h0, h1 = 110, 110 + BOARD_W
    z0, z1 = PLINTH + T + 10, PLINTH + T + 10 + BOARD_L
    x0, x1, y0, y1 = U(h0), U(h1), Zf(z0), Zf(z1)
    cx = (x0 + x1) / 2
    e(f'<path d="M{x0:.2f},{y0:.2f} L{x0:.2f},{y1 + 22:.2f} Q{x0:.2f},{y1 + 6:.2f} {cx:.2f},{y1:.2f} '
      f'Q{x1:.2f},{y1 + 6:.2f} {x1:.2f},{y1 + 22:.2f} L{x1:.2f},{y0:.2f} z" '
      f'fill="#dfe9f3" stroke="#2f5d8a" stroke-width="0.35"/>')
    for a, b in ((0.15, 0.85), (0.85, 0.15)):                 # сложенные ножки
        line(x0 + (x1 - x0) * a, y0 - 3, x0 + (x1 - x0) * b, y0 - (y0 - y1) * 0.55,
             w=0.3, color="#2f5d8a", dash="1.2 0.8")
    text(cx, (y0 + y1) / 2 + 6, "ГЛАДИЛЬНАЯ", size=2.0, weight="bold", fill="#2f5d8a")
    text(cx, (y0 + y1) / 2 + 9, "ДОСКА", size=2.0, weight="bold", fill="#2f5d8a")
    text(cx, (y0 + y1) / 2 + 12.5, "≈1300×380", size=1.8, fill="#2f5d8a")
    # держатель доски
    for z in (1250, 500):
        rect(U(0), Zf(z + 10), (h0 + 15) * S, 20 * S, fill="#2f5d8a", stroke="none")
    # утюг на полке
    iz = 1560 + T
    e(f'<path d="M{U(200):.2f},{Zf(iz):.2f} L{U(430):.2f},{Zf(iz):.2f} L{U(400):.2f},{Zf(iz + 70):.2f} '
      f'Q{U(300):.2f},{Zf(iz + 140):.2f} {U(220):.2f},{Zf(iz + 90):.2f} z" fill="#2f5d8a"/>')
    # розетка
    rect(U(0), Zf(1760), 14 * S, 80 * S, fill="#fff", stroke="#c0392b", sw=0.35)

    # размеры
    yb = FY + 9
    dim_h(U(0), U(h0), yb, "110", ext_from=FY + 1, size=1.8)
    dim_h(U(h0), U(h1), yb, "380", ext_from=FY + 1, size=1.8)
    dim_h(U(h1), U(DEPTH), yb, "110", ext_from=FY + 1, size=1.8)
    dim_h(U(0), U(DEPTH), yb + 7, "600")
    xr = U(DEPTH) + 5
    zs = [0, PLINTH + T, z1, 1560, 1880, ANT, H]
    for a, b in zip(zs, zs[1:]):
        dim_v(Zf(b), Zf(a), xr, str(round(b - a)), ext_from=U(DEPTH), size=1.8)
    dim_v(Zf(1560), Zf(0), xr + 6, "1560", ext_from=U(DEPTH), size=1.8)
    dim_v(Zf(H), Zf(0), xr + 12, str(H), ext_from=U(DEPTH), size=2.0)
    text(U(-WT) - 1, Zf(1720) + 0.8, "розетка", size=1.7, anchor="end", fill="#c0392b")
    text(U(-WT) - 1, Zf(1250) + 0.8, "держатель", size=1.7, anchor="end", fill="#2f5d8a")
    text(U(-WT) - 1, Zf(1640) + 0.8, "утюг", size=1.7, anchor="end", fill="#2f5d8a")
    text(U(DEPTH / 2), Zf(2420), "антресоль", size=1.8, fill="#555")
    text(U(DEPTH / 2), Zf(2040), "полка", size=1.8, fill="#555")


# ===========================================================================
def image(x, y, w, h, path, caption):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    rect(x, y, w, h, fill="#fff", stroke="#999", sw=0.25)
    e(f'<image x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
      f'preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}"/>')
    rect(x, y, w, 9, fill="#fff", stroke="#999", sw=0.25, extra='fill-opacity="0.92"')
    text(x + 3, y + 6, caption, size=3.2, anchor="start", weight="bold")


def notes():
    x, y = 312, 262
    text(x, y, "ПРИМЕЧАНИЯ К ЛИСТУ 2", size=3.2, weight="bold", anchor="start")
    rows = [
        "Ниша доски П2 — узкая: модуль 200, внутри 176 мм (ЛДСП 16).",
        "Доска стоит вертикально БОКОМ (ребром к проходу);",
        "      сложенная ≤ 70–80 мм, длина ≤ 1350, ширина ≤ 400 мм.",
        "Держатели доски Н≈500 и 1250, утюг на полке Н=1560.",
        "Розетка 220 В в нише на Н≈1720. П1 расширена до 940 мм.",
        "Зеркало Lexy 480×50×1405 (антрацит) — в нише Зр 120 мм",
        "      слева у входа, напротив доски. Низ зеркала Н=450.",
        "      Крепление и мин. размеры ниши — по паспорту изделия.",
        "Дверь — раздвижная или наружу: не мешает зеркалу.",
        "LED 24 В в профиле: под антресолью и по краю полок.",
        "Ящики: направляющие 500 мм, доводчик, фасады 200 мм.",
        "3D-виды — иллюстрация; вещи показаны условно.",
    ]
    for i, s in enumerate(rows):
        text(x, y + 6 + i * 4.6, s, size=2.35, anchor="start")


def mirror_detail(ox, fy):
    """Узел В: выдвижное поворотное зеркало (вид сбоку и схема в плане), 1:30."""
    k = 1 / 30

    def X(h):
        return ox + h * k

    def Z(z):
        return fy - z * k

    text(X(300) + 22, Z(H) - 7, "УЗЕЛ В — ЗЕРКАЛО Lexy", size=3.0, weight="bold")
    text(X(300) + 22, Z(H) - 3, "выдвижное поворотное, 480×50×1405, 1:30", size=2.0)
    # вид сбоку
    rect(X(-100), Z(H), 100 * k, H * k, fill="url(#wall)", sw=0.25)
    line(X(-100), Z(0), X(DEPTH + 520), Z(0), w=0.4)
    for z in (PLINTH, ANT, H - T):
        rect(X(0), Z(z + T), DEPTH * k, T * k, fill=CUT, stroke="#111", sw=0.15)
    rect(X(40), Z(MIR_Z + MIR_H), MIR_D * k, MIR_H * k, fill="#cfdde6", stroke="#33373b", sw=0.4)
    for i in range(3):
        zz = MIR_Z + 300 + i * 350
        line(X(110), Z(zz), X(260), Z(zz + 250), w=0.2, color="#fff")
    for z in (MIR_Z + MIR_H + 20, MIR_Z - 20):
        rect(X(20), Z(z) - 0.4, (MIR_D + 40) * k, 0.8, fill="#33373b", stroke="none")
    rect(X(DEPTH + 20), Z(MIR_Z + MIR_H), MIR_D * k, MIR_H * k, fill="none", stroke="#33373b", sw=0.25,
         dash="1 0.7")
    text(X(DEPTH + 260), Z(MIR_Z + MIR_H / 2), "выдвинуто", size=1.8, rot=-90, fill="#33373b")
    dim_h(X(40), X(40 + MIR_D), Z(H) + 7, "480", size=1.8)
    dim_h(X(0), X(DEPTH), fy + 5, "600", ext_from=fy + 0.5, size=1.8)
    dim_v(Z(MIR_Z + MIR_H), Z(MIR_Z), X(-100) - 3, "1405", ext_from=X(40), size=1.8)
    dim_v(Z(MIR_Z), Z(0), X(-100) - 3, "450", size=1.8)
    # схема в плане: 1 – в нише, 2 – выдвинуто, 3 – повёрнуто
    px, py = X(DEPTH + 520) + 6, Z(1500)
    text(px, py - 10, "в плане:", size=1.9, anchor="start", weight="bold")

    def P(x, y):
        return px + x * k, py + y * k

    rect(*P(-100, -60), 100 * k, (LM + 120) * k, fill="url(#wall)", sw=0.2)
    for y in (0, LM):
        line(*P(0, y), *P(DEPTH, y), w=0.35)
    a, b = P(40, (LM - MIR_T) / 2)
    rect(a, b, MIR_D * k, MIR_T * k, fill="#cfdde6", stroke="#33373b", sw=0.3)
    a, b = P(DEPTH + 40, (LM - MIR_T) / 2)
    rect(a, b, MIR_D * k, MIR_T * k, fill="none", stroke="#33373b", sw=0.25, dash="0.8 0.6")
    cx, cy = P(DEPTH + 40 + MIR_D / 2, LM / 2)
    rect(cx - MIR_T * k / 2, cy - MIR_D * k / 2, MIR_T * k, MIR_D * k, fill="none", stroke="#33373b",
         sw=0.25, dash="0.4 0.4")
    for (x, y, n) in ((280, LM / 2, "1"), (DEPTH + 120, LM / 2, "2"), (DEPTH + 340, -150, "3")):
        cxn, cyn = P(x, y)
        e(f'<circle cx="{cxn:.2f}" cy="{cyn:.2f}" r="1.3" fill="#fff" stroke="#33373b" stroke-width="0.2"/>')
        text(cxn, cyn + 0.6, n, size=1.6, weight="bold")
    for i, t in enumerate(("1 — хранится в нише", "2 — выдвинуть на 480", "3 — повернуть к себе")):
        text(px, py + 14 + i * 3.2, t, size=1.8, anchor="start")


def title_block():
    bx, by, bw, bh = 405, 362, 180, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    line(bx, by + 30, bx + bw, by + 30, w=0.3)
    line(bx + 120, by + 14, bx + 120, by + bh, w=0.3)
    text(bx + bw / 2, by + 6.5, "ГАРДЕРОБНАЯ КОМНАТА", size=4.2, weight="bold")
    text(bx + bw / 2, by + 11.5, "Вид сбоку (разрезы А–А, Б–Б), узел зеркала, 3D-виды", size=2.6)
    text(bx + 3, by + 20, "Габариты: 2400 × 1740 × 2640 мм", size=2.6, anchor="start")
    text(bx + 3, by + 26, "Ниша доски 200 × 600, ниша зеркала 120 × 600", size=2.6, anchor="start")
    text(bx + 3, by + 36, "Все размеры в миллиметрах", size=2.6, anchor="start")
    text(bx + 3, by + 42, "Разрезы — масштаб 1:15, 3D — без масштаба", size=2.6, anchor="start")
    text(bx + 150, by + 20.5, "Масштаб", size=2.4)
    text(bx + 150, by + 26.5, "1:15", size=3.6, weight="bold")
    text(bx + 150, by + 36.5, "Лист", size=2.4)
    text(bx + 150, by + 42.5, "2 (А2)", size=3.2, weight="bold")


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)
    image(15, 10, 280, 198, os.path.join(HERE, "3d_front.png"), "3D — ВИД ОТ ВХОДА (зеркало выдвинуто)")
    image(15, 212, 280, 198, os.path.join(HERE, "3d_axo.png"), "3D — АКСОНОМЕТРИЯ (сверху, со стороны входа)")
    section_a(338)
    section_b(500)
    mirror_detail(462, 352)
    notes()
    title_block()
    e('</svg>')
    with open(os.path.join(HERE, "garderobnaya_list2.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


if __name__ == "__main__":
    main()
