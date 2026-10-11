#!/usr/bin/env python3
"""Чертёж подвесного шкафа в прихожей (стена 2–7), лист А3, масштаб 1:20.

Шкаф 1620 × 600 × 2280 мм, висит на 300 мм от чистого пола, до потолка 2580.
Антресоль 500 мм, ниже штанга; во втором отсеке – выдвижные полки для обуви.
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
DT = 18                 # толщина фасада
W = 1620                # ширина шкафа
DEPTH = 600             # глубина с фасадами
CD = DEPTH - DT         # глубина корпуса = 582
CEIL = 2580             # высота помещения (чистый пол – потолок)
ZB = 300                # низ шкафа от пола
ZT = CEIL               # верх шкафа – до потолка
H = ZT - ZB             # высота шкафа = 2280
ANT = 500               # антресоль
ZA = ZT - ANT           # верх полки антресоли = 2080
RAIL = 2000             # штанга
MID = W / 2             # средняя стойка
SHOE = [330, 510, 690, 870]    # выдвижные полки для обуви (низ полки)
SPACER = 25             # проставки под петли для выдвижных полок
DOOR_GAP = 2
WALL = [1620, 100, 100, 900, 115]   # развёртка стены 2–7 по исходному чертежу
CUT = "#7d6c5b"
FACADE = "#ece9e4"
WOOD = "#cdbba6"


class V:
    def __init__(self, ox, fy):
        self.ox, self.fy = ox, fy

    def X(self, x):
        return self.ox + x * S

    def Z(self, z):
        return self.fy - z * S

    def box(self, x0, x1, z0, z1, fill=WOOD, sw=0.2, stroke="#111", dash=None):
        rect(self.X(x0), self.Z(z1), (x1 - x0) * S, (z1 - z0) * S, fill=fill, stroke=stroke, sw=sw, dash=dash)


def hangers(v, x0, x1, z, length):
    n = max(2, int((x1 - x0) / 110))
    step = (x1 - x0) / (n + 1)
    for i in range(1, n + 1):
        cx = v.X(x0 + step * i)
        hw = min(150, step * 0.9) * S
        e(f'<path d="M{cx:.2f},{v.Z(z):.2f} l{-hw / 2:.2f},1.2 l{hw:.2f},0 z" fill="none" stroke="#999" stroke-width="0.15"/>')
        rect(cx - hw / 2, v.Z(z) + 1.2, hw, length * S - 1.2, fill="#ece8e3", stroke="#b5aca2", sw=0.12)


# ---------------------------------------------------------------------------
def view_wall(ox, fy):
    """Фасад: стена 2–7 со шкафом (двери закрыты)."""
    v = V(ox, fy)
    total = sum(WALL)
    text(v.X(total / 2), v.Z(CEIL) - 13, "ФАСАД — СТЕНА 2–7", size=3.4, weight="bold")
    text(v.X(total / 2), v.Z(CEIL) - 9, "двери закрыты", size=2.1)
    # потолок и пол
    rect(v.X(0), v.Z(CEIL + 100), total * S, 100 * S, fill="url(#hatch)", sw=0.25)
    rect(v.X(0), v.Z(0), total * S, 80 * S, fill="url(#hatch)", sw=0.25)
    rect(v.X(0), v.Z(CEIL), total * S, CEIL * S, fill="#f7f5f2", sw=0.35)
    # дверной проём
    d0 = sum(WALL[:3])
    rect(v.X(d0), v.Z(2070), 900 * S, 2070 * S, fill="#fff", stroke="#666", sw=0.25, dash="1.2 0.8")
    line(v.X(d0), v.Z(0), v.X(d0 + 450), v.Z(2070), w=0.15, color="#999", dash="1.2 0.8")
    line(v.X(d0 + 900), v.Z(0), v.X(d0 + 450), v.Z(2070), w=0.15, color="#999", dash="1.2 0.8")
    text(v.X(d0 + 450), v.Z(1000), "дверной проём", size=1.9, fill="#666")
    # простенок 3/4 – 5/6
    rect(v.X(1720), v.Z(CEIL), 100 * S, CEIL * S, fill="url(#hatch)", sw=0.2)
    # шкаф – фасады
    for i in range(4):
        x0, x1 = i * W / 4 + DOOR_GAP / 2, (i + 1) * W / 4 - DOOR_GAP / 2
        v.box(x0, x1, ZB + 2, ZT - 4, fill=FACADE, sw=0.3)
        for k in range(14):              # рисунок «камня»
            rnd = random.Random(i * 100 + k)
            px, pz = rnd.uniform(x0 + 30, x1 - 60), rnd.uniform(ZB + 60, ZT - 120)
            line(v.X(px), v.Z(pz), v.X(px + rnd.uniform(-40, 60)), v.Z(pz + rnd.uniform(-60, 60)), w=0.12, color="#b8b2aa")
    for xh in (W / 4, 3 * W / 4):         # ручки у стыка створок
        for side in (-1, 1):
            xx = xh + side * 30
            rect(v.X(xx) - 0.35, v.Z(1400), 0.7, 900 * S, fill="#3a3632", stroke="none")
    # раскрытие дверей (условно)
    for i, (hinge, far) in enumerate(((0, W / 4), (W / 2, W / 4), (W / 2, 3 * W / 4), (W, 3 * W / 4))):
        line(v.X(hinge), v.Z(ZB + 2), v.X(far), v.Z((ZB + ZT) / 2), w=0.12, color="#888", dash="1 0.8")
        line(v.X(hinge), v.Z(ZT - 4), v.X(far), v.Z((ZB + ZT) / 2), w=0.12, color="#888", dash="1 0.8")
    # пространство под шкафом
    text(v.X(W / 2), v.Z(ZB / 2) + 0.8, "свободно 300 (под шкафом)", size=1.9, fill="#555")
    # размеры
    y1, y2 = v.Z(0) + 10, v.Z(0) + 16
    x = 0
    for w in WALL:
        dim_h(v.X(x), v.X(x + w), y1, str(w), ext_from=v.Z(0) + 4.5, size=2.1)
        x += w
    dim_h(v.X(0), v.X(total), y2, str(total))
    xl = v.X(0) - 5
    dim_v(v.Z(CEIL), v.Z(ZB), xl, str(H), ext_from=v.X(0), size=2.2)
    dim_v(v.Z(ZB), v.Z(0), xl, str(ZB), ext_from=v.X(0), size=2.2)
    dim_v(v.Z(CEIL), v.Z(0), xl - 6, str(CEIL), size=2.2)
    text(v.X(1670), v.Z(1300), "зазор 100", size=1.7, rot=-90, fill="#555")
    for x, s in ((0, "2"), (1720, "3/4"), (1820, "5/6"), (total, "7")):
        text(v.X(x), v.Z(CEIL + 100) - 2, s, size=2.6, weight="bold", fill="#c0392b")
    return v


def view_inside(ox, fy):
    """Внутреннее наполнение (фасады сняты)."""
    v = V(ox, fy)
    text(v.X(W / 2), v.Z(CEIL) - 13, "НАПОЛНЕНИЕ", size=3.4, weight="bold")
    text(v.X(W / 2), v.Z(CEIL) - 9, "фасады условно сняты", size=2.1)
    line(v.X(-150), v.Z(0), v.X(W + 150), v.Z(0), w=0.45)
    line(v.X(-150), v.Z(CEIL), v.X(W + 150), v.Z(CEIL), w=0.3, dash="2 1")
    v.box(0, W, ZB, ZT, fill="#fbfaf8", sw=0.4)
    for x in (0, MID - T / 2, W - T):
        v.box(x, x + T, ZB, ZT)
    for z in (ZB, ZT - T):
        v.box(0, W, z, z + T)
    for x0, x1 in ((T, MID - T / 2), (MID + T / 2, W - T)):
        v.box(x0, x1, ZA - T, ZA)                       # полка антресоли
        rect(v.X(x0 + 60), v.Z(ZA + 280), (x1 - x0 - 120) * S, 280 * S, fill="#e7ddd0", stroke="#aaa", sw=0.12)
    # отсек 1 – длинная одежда
    x0, x1 = T, MID - T / 2
    hangers(v, x0, x1, RAIL, 1400)
    # отсек 2 – одежда + выдвижные полки для обуви
    x0, x1 = MID + T / 2, W - T
    hangers(v, x0, x1, RAIL, 950)
    for xs in (x0, x1 - SPACER):                        # проставки под петли
        v.box(xs, xs + SPACER, ZB + T, SHOE[-1] + 120, fill="#d9cbb8", sw=0.15)
    for z in SHOE:
        sx0, sx1 = x0 + SPACER + 13, x1 - SPACER - 13
        v.box(sx0, sx1, z, z + T, fill="#a89580", sw=0.2)
        v.box(sx0, sx1, z + T, z + 60, fill="none", sw=0.15)            # бортик
        for k in range(3):                                              # пары обуви
            bx = sx0 + 30 + k * 230
            rect(v.X(bx), v.Z(z + T + 110), 190 * S, 110 * S, fill="#4a4440", stroke="none")
    for xr0, xr1 in ((T, MID - T / 2), (MID + T / 2, W - T)):
        y = v.Z(RAIL)
        line(v.X(xr0) + 0.3, y, v.X(xr1) - 0.3, y, w=0.6, color="#555")
        text(v.X(xr0) + 1.2, y - 0.8, "штанга", size=1.6, anchor="start", fill="#444")
    # размеры
    yb = v.Z(0) + 10
    dim_h(v.X(0), v.X(MID), yb, "810", ext_from=v.Z(ZB) + 1)
    dim_h(v.X(MID), v.X(W), yb, "810", ext_from=v.Z(ZB) + 1)
    dim_h(v.X(0), v.X(W), yb + 6, str(W))
    dim_h(v.X(MID + T / 2 + SPACER + 13), v.X(W - T - SPACER - 13), v.Z(SHOE[-1] + 260),
          "≈710", size=1.7)
    leader(v.X(MID + 60), v.Z(SHOE[1] + 30), v.X(MID - 260), v.Z(SHOE[0] + 120),
           "выдвижные\nполки для обуви ×4", anchor="end", size=1.8)
    xr = v.X(W) + 5
    zs = [0, ZB, RAIL, ZA, ZT]
    for a, b in zip(zs, zs[1:]):
        dim_v(v.Z(b), v.Z(a), xr, str(b - a), ext_from=v.X(W), size=2.0)
    dim_v(v.Z(ZT), v.Z(ZA), xr + 6, f"{ANT} антресоль", size=1.9)
    dim_v(v.Z(RAIL), v.Z(0), xr + 12, str(RAIL), size=2.0)
    xl = v.X(0) - 5
    zs = [ZB] + SHOE + [SHOE[-1] + 180]
    for a, b in zip(zs, zs[1:]):
        dim_v(v.Z(b), v.Z(a), xl, str(b - a), ext_from=v.X(0), size=1.7)
    dim_v(v.Z(ZB), v.Z(0), xl, str(ZB), ext_from=v.X(0), size=1.8)
    for x, s in ((MID / 2, "1"), (MID + MID / 2, "2")):
        cx, cy = v.X(x), v.Z(ZT - 150)
        e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.2" fill="#fff" stroke="#111" stroke-width="0.25"/>')
        text(cx, cy + 0.8, s, size=2.2, weight="bold")
    return v


def view_section(ox, fy):
    """Разрез 1–1 по отсеку 2 (вид сбоку)."""
    v = V(ox, fy)                       # x здесь – глубина: 0 стена, 600 фасад
    text(v.X(300), v.Z(CEIL) - 13, "РАЗРЕЗ 1–1", size=3.4, weight="bold")
    text(v.X(300), v.Z(CEIL) - 9, "по отсеку 2", size=2.1)
    rect(v.X(-100), v.Z(CEIL + 100), 100 * S, (CEIL + 180) * S, fill="url(#hatch)", sw=0.25)
    rect(v.X(-100), v.Z(CEIL + 100), (DEPTH + 520) * S, 100 * S, fill="url(#hatch)", sw=0.25)
    rect(v.X(-100), v.Z(0), (DEPTH + 520) * S, 80 * S, fill="url(#hatch)", sw=0.25)
    # корпус в разрезе
    for z in (ZB, ZA - T, ZT - T):
        v.box(0, CD, z, z + T, fill=CUT)
    v.box(0, 4, ZB, ZT, fill="#777")                     # задняя стенка ХДФ
    v.box(CD, DEPTH, ZB + 2, ZT - 4, fill=FACADE, sw=0.3)  # фасад
    rect(v.X(DEPTH), v.Z(1400), 25 * S, 900 * S, fill="#3a3632", stroke="none")
    # навес / монтажная планка
    v.box(4, 24, ZT - 120, ZT - 40, fill="#555")
    # штанга
    e(f'<circle cx="{v.X(CD / 2):.2f}" cy="{v.Z(RAIL):.2f}" r="0.8" fill="#555"/>')
    rect(v.X(CD / 2 - 220), v.Z(RAIL) + 1.2, 440 * S, 950 * S - 1.2, fill="#ece8e3", stroke="#b5aca2", sw=0.12)
    # выдвижные полки: одна выдвинута
    for i, z in enumerate(SHOE):
        off = 400 if i == 1 else 0
        dash = "1 0.7" if off else None
        v.box(40 + off, 540 + off, z, z + T, fill="none" if off else "#a89580", sw=0.25, dash=dash)
        v.box(520 + off, 540 + off, z + T, z + 60, fill="none" if off else "#a89580", sw=0.2, dash=dash)
        line(v.X(20), v.Z(z + 8), v.X(CD - 10 + off), v.Z(z + 8), w=0.2, color="#c9a227")
        rect(v.X(120 + off), v.Z(z + T + 110), 300 * S, 110 * S, fill="#4a4440" if not off else "none",
             stroke="#4a4440", sw=0.15, dash=dash)
    # фасад открыт (пунктир) у выдвинутой полки
    line(v.X(DEPTH), v.Z(ZB + 2), v.X(DEPTH), v.Z(ZT - 4), w=0.1, color="#bbb")
    # размеры
    yb = v.Z(0) + 10
    dim_h(v.X(0), v.X(CD), yb, str(CD), ext_from=v.Z(ZB) + 1, size=2.0)
    dim_h(v.X(CD), v.X(DEPTH), yb, str(DT), ext_from=v.Z(ZB) + 1, size=1.7)
    dim_h(v.X(0), v.X(DEPTH), yb + 6, str(DEPTH))
    dim_h(v.X(40), v.X(540), v.Z(SHOE[0]) + 3, "500", size=1.7)
    dim_h(v.X(540), v.X(940), v.Z(SHOE[1] + 60) - 2, "ход 400", size=1.7)
    leader(v.X(14), v.Z(ZT - 80), v.X(150), v.Z(ZT - 260), "навес / монтажная\nшина к стене", size=1.8)
    leader(v.X(CD / 2), v.Z(RAIL), v.X(150), v.Z(RAIL - 160), "штанга", size=1.8)
    leader(v.X(300), v.Z(SHOE[2] + 8), v.X(660), v.Z(SHOE[2] + 260),
           "направляющие\nполного выдвижения", size=1.8)
    return v


def view_plan(ox, oy):
    """План ниши со шкафом и раскрытием дверей."""
    def P(x, y):
        return ox + x * S, oy + y * S
    text(ox + 910 * S, oy - 9, "ПЛАН", size=3.4, weight="bold")
    rect(*P(-100, -100), 1920 * S, 100 * S, fill="url(#hatch)", sw=0.25)       # стена 2–7
    rect(*P(-100, 0), 100 * S, 1100 * S, fill="url(#hatch)", sw=0.25)          # стена 1–2
    rect(*P(1720, 0), 100 * S, 600 * S, fill="url(#hatch)", sw=0.25)           # стена 3–4
    a, b = P(0, 0)
    rect(a, b, W * S, CD * S, fill="#f4efe8", sw=0.3)
    line(*P(MID, 0), *P(MID, CD), w=0.35)
    line(*P(T, CD / 2), *P(MID - 10, CD / 2), w=0.4, color="#555", dash="2 0.8")
    line(*P(MID + 10, CD / 2), *P(W - T, CD / 2), w=0.4, color="#555", dash="2 0.8")
    for i in range(4):
        a, b = P(i * W / 4 + 1, CD)
        rect(a, b, (W / 4 - 2) * S, DT * S, fill=FACADE, stroke="#111", sw=0.25)
    r = (W / 4) * S
    for hinge, sgn in ((0, 1), (MID, -1), (MID, 1), (W, -1)):
        hx, hy = P(hinge, DEPTH)
        line(hx, hy, hx, hy + r, w=0.25, color="#555")
        sweep = 0 if sgn > 0 else 1
        e(f'<path d="M{hx:.2f},{hy + r:.2f} A{r:.2f},{r:.2f} 0 0 {sweep} {hx + sgn * r:.2f},{hy:.2f}" '
          f'fill="none" stroke="#777" stroke-width="0.18" stroke-dasharray="1 0.7"/>')
    for x, s in ((MID / 2, "1"), (MID + MID / 2, "2")):
        cx, cy = P(x, 200)
        e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="2" fill="#fff" stroke="#111" stroke-width="0.25"/>')
        text(cx, cy + 0.8, s, size=2, weight="bold")
    # линия разреза 1–1
    cx = P(1215, 0)[0]
    line(cx, oy - 7, cx, oy + 950 * S, w=0.3, color="#1f4e8c", dash="5 1 1 1")
    text(cx + 2.5, oy - 6, "1", size=2.6, weight="bold", fill="#1f4e8c")
    text(cx + 2.5, oy + 950 * S + 1.5, "1", size=2.6, weight="bold", fill="#1f4e8c")
    dim_h(*[P(0, 0)[0], P(W, 0)[0]], oy + 1050 * S, str(W), size=2.0)
    dim_h(P(W, 0)[0], P(1720, 0)[0], oy + 1050 * S, "100", size=1.7)
    dim_v(oy, oy + DEPTH * S, ox + 1820 * S + 4, str(DEPTH), ext_from=ox + 1820 * S, size=2.0)
    text(*P(1670, 300), "зазор", size=1.6, rot=-90, fill="#555")


def notes(x, y):
    text(x, y, "ПРИМЕЧАНИЯ", size=3.0, weight="bold", anchor="start")
    rows = [
        "Шкаф подвесной: низ на 300 мм от чистого пола, верх до потолка (2580).",
        "Габарит 1620 × 600 × 2280 мм; корпус ЛДСП 16, глубина корпуса 582,",
        "      фасады 18 мм, 4 распашные двери ≈403 × 2274, по 5 петель на дверь.",
        "Крепление к стене — навесы / монтажная шина, задняя стенка ХДФ.",
        "Отсеки 1 и 2 (по 810): антресоль 500 мм, ниже штанга на Н=2000.",
        "Отсек 1 — длинная одежда (под штангой ≈1680).",
        "Отсек 2 — короткая одежда + 4 выдвижные полки для обуви с бортиком,",
        "      направляющие полного выдвижения 500 мм; проставки 25 мм под петли.",
        "Справа зазор 100 до стены 3–4 (как на исходном чертеже).",
        "Розетки на стене 2–7 (Н=250 и Н=1950, 200 от края шкафа) попадают",
        "      под шкаф и внутрь отсека 2 — уточнить перенос или вырез в задней стенке.",
        "Размеры уточнить по месту после чистовой отделки.",
    ]
    for i, s in enumerate(rows):
        text(x, y + 5.5 + i * 4.1, s, size=2.15, anchor="start")


def title_block():
    bx, by, bw, bh = 290, 252, 120, 38
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 13, bx + bw, by + 13, w=0.3)
    line(bx + 80, by + 13, bx + 80, by + bh, w=0.3)
    text(bx + bw / 2, by + 6, "ШКАФ В ПРИХОЖЕЙ", size=3.8, weight="bold")
    text(bx + bw / 2, by + 10.5, "подвесной, стена 2–7", size=2.3)
    text(bx + 3, by + 19, "1620 × 600 × 2280 мм", size=2.4, anchor="start")
    text(bx + 3, by + 25, "низ шкафа +300 от пола", size=2.4, anchor="start")
    text(bx + 3, by + 31, "Размеры в мм", size=2.4, anchor="start")
    text(bx + 100, by + 20, "Масштаб", size=2.2)
    text(bx + 100, by + 26, "1:20", size=3.4, weight="bold")
    text(bx + 100, by + 33, "Лист 1 (А3)", size=2.2)


def main():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 420, 297, fill="#fff", stroke="none")
    rect(8, 5, 407, 287, sw=0.5)
    fy = 175
    view_wall(34, fy)
    view_inside(205, fy)
    view_section(330, fy)
    view_plan(34, 218)
    notes(150, 214)
    title_block()
    e('</svg>')
    with open(os.path.join(HERE, "shkaf.svg"), "w", encoding="utf-8") as f:
        f.write("\n".join(g.out))


if __name__ == "__main__":
    main()
