#!/usr/bin/env python3
"""Лист 2: вид сбоку (разрез А–А), разрез Б–Б по нише гладильной доски,
объёмные виды (3D). Использует общие функции и размеры из generate.py.
Перед запуском нужно отрендерить 3d_front.png и 3d_axo.png (render3d.js).
"""
import base64
import os

import generate as g
from generate import (S, T, H, D, DEPTH, PLINTH, ANT, RAIL, R1, R2, SIDE,
                      DRAWER_TOP, BOARD_L, BOARD_W, LED, e, text, line, rect,
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
    for i in range(4):                                           # ящики
        zb = PLINTH + T + i * 200
        cutp(DEPTH - 18, DEPTH, zb + 2, zb + 198, fill="#a89580")             # фасад
        rect(U(80), Zf(zb + 150), (DEPTH - 18 - 80) * S, 130 * S, fill="#f6f1ea", stroke="#999", sw=0.15)
        cutp(80, DEPTH - 18, zb + 20, zb + 28)                    # дно ящика
        cutp(80, 92, zb + 28, zb + 150)                           # задняя стенка ящика
        cutp(DEPTH, DEPTH + 12, zb + 125, zb + 137, fill="#c9a227")           # ручка
        line(U(80), Zf(zb + 40), U(DEPTH - 18), Zf(zb + 40), w=0.35, color="#555")   # направляющая
    cutp(0, DEPTH, DRAWER_TOP, DRAWER_TOP + T)
    for z in (1230, 1550, 1870):
        cutp(0, DEPTH - 20, z, z + T)
        rect(U(DEPTH - 40), Zf(z), 18 * S, 10 * S, fill=LED, stroke="#7a5a00", sw=0.15)
        rect(U(120), Zf(z + T + 200), 250 * S, 200 * S, fill="#e3d6c6", stroke="#aaa", sw=0.15)
    cutp(0, DEPTH, ANT, ANT + T)
    rect(U(DEPTH - 22), Zf(ANT), 18 * S, 10 * S, fill=LED, stroke="#7a5a00", sw=0.15)
    rect(U(120), Zf(ANT + T + 260), 400 * S, 260 * S, fill="#e3d6c6", stroke="#aaa", sw=0.15)
    cutp(0, DEPTH, H - T, H)

    # --- размеры
    yb = FY + 9
    dim_h(U(0), U(DEPTH), yb, "600", ext_from=FY + 1)
    dim_h(U(DEPTH), U(D), yb, f"{SIDE} проход вдоль боковых шкафов", ext_from=FY + 1)
    dim_h(U(0), U(D), yb + 7, str(D))
    dim_h(U(80), U(DEPTH - 18), Zf(PLINTH + T + 200) + 3.2, "500 ящик", size=1.8)
    zs = [0, PLINTH, DRAWER_TOP, 1230, 1550, 1870, ANT, H]
    xl = U(-100) - 5
    for a, b in zip(zs, zs[1:]):
        dim_v(Zf(b), Zf(a), xl, str(b - a), ext_from=U(-100), size=2.0)
    dim_v(Zf(H), Zf(0), xl - 6, str(H), ext_from=U(-100))

    # --- выноски
    leader(U(DEPTH - 12), Zf(ANT - 5), U(DEPTH + 120), Zf(ANT) + 7,
           "LED-профиль под антресолью", size=2.0)
    leader(U(DEPTH - 30), Zf(1550 - 5), U(DEPTH + 120), Zf(1550) + 5,
           "LED по краю полок", size=2.0)
    leader(U(300), Zf(PLINTH + T + 640), U(DEPTH + 120), Zf(700),
           "Выкатной ящик: направляющие\n500 мм полного выдвижения", size=2.0)
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
        "Ниша гладильной доски П2 — узкая: модуль 200 мм, внутри 176 мм (ЛДСП 16).",
        "Доска хранится вертикально, БОКОМ (ребром к проходу), толщина в сложенном",
        "      виде ≤ 70–80 мм; длина доски до 1350 мм, ширина до 400 мм.",
        "Держатели доски — 2 шт. на стене (Н≈500 и 1250), утюг на полке Н=1560 (стоя на пятке).",
        "Розетка 220 В в нише на Н≈1720, над полкой утюга.",
        "Секция П1 расширена до 940 мм за счёт сужения ниши.",
        "LED: лента 24 В в алюм. профиле, под антресолью и по переднему краю полок.",
        "Ящики: направляющие полного выдвижения 500 мм с доводчиком, фасады 200 мм.",
        "3D-виды — иллюстрация компоновки; одежда и предметы показаны условно.",
    ]
    for i, s in enumerate(rows):
        text(x, y + 6 + i * 4.6, s, size=2.35, anchor="start")


def title_block():
    bx, by, bw, bh = 405, 362, 180, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    line(bx, by + 30, bx + bw, by + 30, w=0.3)
    line(bx + 120, by + 14, bx + 120, by + bh, w=0.3)
    text(bx + bw / 2, by + 6.5, "ГАРДЕРОБНАЯ КОМНАТА", size=4.2, weight="bold")
    text(bx + bw / 2, by + 11.5, "Вид сбоку (разрезы А–А, Б–Б), объёмные виды", size=2.6)
    text(bx + 3, by + 20, "Габариты: 2400 × 1740 × 2640 мм", size=2.6, anchor="start")
    text(bx + 3, by + 26, "Ниша гладильной доски: 200 × 600 мм", size=2.6, anchor="start")
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
    image(15, 10, 280, 198, os.path.join(HERE, "3d_front.png"), "3D — ВИД ОТ ВХОДА")
    image(15, 212, 280, 198, os.path.join(HERE, "3d_axo.png"), "3D — АКСОНОМЕТРИЯ (сверху, со стороны входа)")
    section_a(338)
    section_b(500)
    notes()
    title_block()
    e('</svg>')
    with open(os.path.join(HERE, "garderobnaya_list2.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


if __name__ == "__main__":
    main()
