#!/usr/bin/env python3
"""Тумба подвесная под раковину 1260 × 500 × 370 (по эскизу заказчика).
В центре отсек под шланги и сифон, по бокам два выкатных ящика. Лист 1 – виды с размерами, лист 2 – детали."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                       # noqa: E402
from generate import e, line, rect, LED                    # noqa: E402

F = 1.7
_text, _dh, _dv = g.text, g.dim_h, g.dim_v


def text(x, y, s, size=2.6, **kw):
    _text(x, y, s, size=size * F, **kw)


g.text = text


def dim_h(*a, size=2.4, **kw):
    _dh(*a, size=size, **kw)


def dim_v(*a, size=2.4, **kw):
    _dv(*a, size=size, **kw)


T = 16
W, D, H = 1260, 500, 370
SEC = 496                     # секции ящиков в свету
MID = W - 2 * T - 2 * SEC     # 236 – центральная зона (2 перегородки + отсек в свету)
MID_IN = MID - 2 * T          # 204 – отсек в свету
X_P1, X_P2 = T + SEC, T + SEC + MID - T      # перегородки
FAC_W, FAC_H, GAP = 628, 365, 4
BOX_W, BOX_D, BOX_H = 486, 440, 229          # ящик: 454 + 16 + 16, глубина 440
INK = "#1d2a6b"


def frame():
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 594 420" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 594, 420, fill="#fff", stroke="none")
    rect(10, 5, 579, 410, sw=0.6)


def stamp(sub, sheet):
    bx, by, bw, bh = 405, 362, 180, 46
    rect(bx, by, bw, bh, sw=0.5)
    line(bx, by + 14, bx + bw, by + 14, w=0.3)
    line(bx + 120, by + 14, bx + 120, by + bh, w=0.3)
    text(bx + bw / 2, by + 7, "ТУМБА ПОД РАКОВИНУ", size=3.6, weight="bold")
    text(bx + bw / 2, by + 12, sub, size=1.9)
    text(bx + 3, by + 22, f"Габариты {W} × {D} × {H}", size=2.1, anchor="start")
    text(bx + 3, by + 30, "ЛДСП 16, подвесная", size=2.1, anchor="start")
    text(bx + 3, by + 38, "Размеры в мм", size=2.1, anchor="start")
    text(bx + 150, by + 24, "Лист", size=2.0)
    text(bx + 150, by + 34, sheet, size=3.0, weight="bold")


def save(name):
    e('</svg>')
    open(os.path.join(HERE, name), "w", encoding="utf-8").write("\n".join(g.out))


# ===========================================================================
def sheet1():
    frame()
    S = 1 / 4.5
    # --- вид спереди с фасадами
    ox, fy = 40, 125
    X = lambda x: ox + x * S        # noqa: E731
    Z = lambda z: fy - z * S        # noqa: E731
    text(X(W / 2), 30, "ВИД СПЕРЕДИ (фасады)", size=3.2, weight="bold")
    rect(X(0), Z(H), W * S, H * S, fill="#f4efe8", sw=0.4)
    for k in range(2):
        x0 = GAP / 2 + k * (FAC_W + GAP)
        rect(X(x0), Z(H - 2.5), FAC_W * S, FAC_H * S, fill="#fbfaf8", sw=0.45)
        line(X(x0 + FAC_W / 2 - 80), Z(H - 40), X(x0 + FAC_W / 2 + 80), Z(H - 40), w=0.8, color="#333")
    # внутреннее – пунктир
    for x in (X_P1, X_P2):
        rect(X(x), Z(H - T), T * S, (H - 2 * T) * S, fill="none", stroke="#8c7b62", sw=0.25, dash="1.4 0.8")
    rect(X(X_P1 + T + 40), Z(H - 120), 120 * S, 110 * S, fill="none", stroke="#2f6fb0", sw=0.3, dash="1 0.6")
    text(X(W / 2), Z(H - 200), "сифон", size=1.7, fill="#2f6fb0")
    dim_h(X(0), X(W), Z(0) + 12, str(W), ext_from=Z(0) + 0.5)
    for k in range(2):
        x0 = GAP / 2 + k * (FAC_W + GAP)
        dim_h(X(x0), X(x0 + FAC_W), Z(0) + 5, str(FAC_W), ext_from=Z(0) + 0.5, size=2.1)
    dim_v(Z(H), Z(0), X(W) + 6, str(H), ext_from=X(W))
    dim_v(Z(H - 2.5), Z(H - 2.5 - FAC_H), X(0) - 5, str(FAC_H), ext_from=X(0), size=2.1)
    text(X(W / 2), Z(0) + 22, "2 фасада 628 × 365, зазор 4; ящики открываются вместе с фасадом", size=1.9, fill="#444")

    # --- вид спереди без фасадов
    ox2, fy2 = 40, 245
    X2 = lambda x: ox2 + x * S      # noqa: E731
    Z2 = lambda z: fy2 - z * S      # noqa: E731
    text(X2(W / 2), 152, "ВИД СПЕРЕДИ БЕЗ ФАСАДОВ (корпус)", size=3.2, weight="bold")
    rect(X2(0), Z2(H), W * S, H * S, fill="#fbf8f3", sw=0.3)
    for (x0, x1, z0, z1) in ((0, T, 0, H), (W - T, W, 0, H), (T, W - T, 0, T),
                             (T, W - T, H - T, H), (X_P1, X_P1 + T, T, H - T), (X_P2, X_P2 + T, T, H - T)):
        rect(X2(x0), Z2(z1), (x1 - x0) * S, (z1 - z0) * S, fill="#e8dccb", sw=0.3)
    for x0 in (T, X_P2 + T):
        bx = x0 + (SEC - BOX_W) / 2
        rect(X2(bx), Z2(T + 20 + BOX_H), BOX_W * S, BOX_H * S, fill="#f1e9de", sw=0.3)
        text(X2(x0 + SEC / 2), Z2(T + 20 + BOX_H / 2), "ЯЩИК", size=2.2, weight="bold")
        text(X2(x0 + SEC / 2), Z2(T + 20 + BOX_H / 2) + 4, f"{BOX_W} × {BOX_D} × {BOX_H}", size=1.8)
    text(X2(W / 2), Z2(H / 2), "ОТСЕК", size=1.9, weight="bold", fill="#2f6fb0")
    text(X2(W / 2), Z2(H / 2) + 4, "шланги,", size=1.6, fill="#2f6fb0")
    text(X2(W / 2), Z2(H / 2) + 7.5, "сифон", size=1.6, fill="#2f6fb0")
    xs = [0, T, T + SEC, X_P1 + T, X_P2, X_P2 + T, W - T, W]
    for a, b in zip(xs, xs[1:]):
        dim_h(X2(a), X2(b), Z2(0) + 5, str(b - a), ext_from=Z2(0) + 0.5, size=1.9 if b - a > 20 else 1.5)
    dim_h(X2(X_P1), X2(X_P2 + T), Z2(0) + 11, f"{MID} центр. отсек", ext_from=Z2(0) + 0.5, size=2.0)
    dim_h(X2(0), X2(W), Z2(0) + 17, str(W))
    dim_v(Z2(H), Z2(0), X2(W) + 6, str(H), ext_from=X2(W))
    dim_v(Z2(H - T), Z2(T), X2(X_P1 + T + 30), str(H - 2 * T), size=1.9)

    # --- план (разрез под царгами)
    S2 = 1 / 6
    oxp, oyp = 345, 50
    P = lambda x, y: (oxp + x * S2, oyp + y * S2)   # noqa: E731  (y – от стены к фасаду)
    text(oxp + W * S2 / 2, 30, "ПЛАН (разрез, вид сверху)", size=3.2, weight="bold")
    def bx(x0, y0, x1, y1, fill="#e8dccb", **kw):
        a, b = P(x0, y0)
        rect(a, b, (x1 - x0) * S2, (y1 - y0) * S2, fill=fill, sw=0.3, **kw)
    rect(oxp - 4, oyp - 4, W * S2 + 8, 4, fill="url(#wall)", sw=0.2)
    bx(0, 0, W, D, fill="#fbf8f3")
    bx(0, 0, T, D)
    bx(W - T, 0, W, D)
    bx(X_P1, D - 483, X_P1 + T, D)
    bx(X_P2, D - 483, X_P2 + T, D)
    bx(X_P1 + T, D - 483 - T, X_P2, D - 483, fill="#d8ccb8")
    for x0 in (T, X_P2 + T):
        b0 = x0 + (SEC - BOX_W) / 2
        bx(b0, D - BOX_D - 2, b0 + BOX_W, D - 2, fill="#f1e9de")
    for k in range(2):
        bx(GAP / 2 + k * (FAC_W + GAP), D, GAP / 2 + k * (FAC_W + GAP) + FAC_W, D + 18, fill="#fbfaf8")
    cx, cy = P(W / 2, 250)
    e(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{35 * S2:.2f}" fill="#dfe9f3" stroke="#2f6fb0" stroke-width="0.3"/>')
    text(cx, cy + 14, "сифон / шланги", size=1.6, fill="#2f6fb0")
    a, b = P(0, D + 18)
    dim_h(P(0, 0)[0], P(W, 0)[0], b + 8, str(W), ext_from=b)
    dim_v(P(0, 0)[1], P(0, D)[1], P(0, 0)[0] - 5, str(D), ext_from=P(0, 0)[0])
    dim_v(P(0, D - BOX_D - 2)[1], P(0, D - 2)[1], P(T + 40, 0)[0], str(BOX_D), size=1.8)
    dim_v(P(0, D - 483)[1], P(0, D)[1], P(X_P1 - 25, 0)[0], "483", size=1.8)

    # --- разрез сбоку
    oxs, fys = 420, 300
    Y = lambda y: oxs + y * S2      # noqa: E731
    Zs = lambda z: fys - z * S2     # noqa: E731
    text(Y(D / 2), 218, "РАЗРЕЗ ПО ЯЩИКУ (вид сбоку)", size=3.2, weight="bold")
    rect(Y(-12), Zs(H + 60), 12 * S2, (H + 120) * S2, fill="url(#wall)", sw=0.2)
    rect(Y(0), Zs(H), D * S2, H * S2, fill="#fbf8f3", sw=0.3)
    rect(Y(0), Zs(T), D * S2, T * S2, fill="#e8dccb", sw=0.3)
    for y0 in (0, D - 100):
        rect(Y(y0), Zs(H), 100 * S2, T * S2, fill="#e8dccb", sw=0.3)
    rect(Y(D - 2 - BOX_D), Zs(T + 20 + BOX_H), BOX_D * S2, BOX_H * S2, fill="#f1e9de", sw=0.3)
    rect(Y(D), Zs(H - 2.5), 18 * S2, FAC_H * S2, fill="#fbfaf8", sw=0.4)
    dim_h(Y(0), Y(D), Zs(0) + 6, str(D), ext_from=Zs(0) + 0.5)
    dim_h(Y(0), Y(100), Zs(H) - 5, "100", ext_from=Zs(H), size=1.8)
    dim_h(Y(D - 100), Y(D), Zs(H) - 5, "100", ext_from=Zs(H), size=1.8)
    dim_v(Zs(T + 20 + BOX_H), Zs(T + 20), Y(D - BOX_D) - 5, str(BOX_H), size=1.8)
    dim_v(Zs(H), Zs(0), Y(D + 18) + 6, str(H), ext_from=Y(D + 18))
    text(Y(D / 2), Zs(H) - 12, "царги 1228 × 100 (сверху раковина)", size=1.7, fill="#444")

    notes = ["Тумба подвесная: крепится к стене, снизу ножек нет.",
             "Центральный отсек 204 в свету — под шланги и сифон, закрыт от ящиков перегородками 353 × 483.",
             "Ящики: направляющие полного выдвижения 450, коробка 486 × 440 × 229 (ЛДСП 16).",
             "Фасады 628 × 365 крепятся к ящикам и закрывают половину центрального отсека каждый.",
             "Сверху раковина/столешница на двух царгах 1228 × 100."]
    text(40, 300, "ПРИМЕЧАНИЯ", size=3.0, weight="bold", anchor="start")
    for k, s in enumerate(notes):
        text(40, 309 + k * 6.2, f"{k + 1}. {s}", size=2.1, anchor="start")
    stamp("виды, план, разрез", "1 (А2)")
    save("sheet1.svg")


# ===========================================================================
PARTS = [  # (размер, черт кромки), (размер, черт), шт, примечание
    ((1228, 2), (500, 1), 1, "дно"),
    ((1228, 2), (100, 0), 2, "царги"),
    ((370, 2), (500, 2), 2, "боковины"),
    ((353, 2), (483, 1), 2, "перегородки (закрытая сторона)"),
    ((264, 2), (233, 2), 1, "закрытая сторона"),
    ((454, 1), (200, 0), 4, "ящики: перед / зад"),
    ((440, 1), (229, 2), 4, "ящики: бока"),
    ((454, 2), (440, 0), 2, "ящики: дно"),
    ((628, 2), (365, 1), 2, "фасад"),
]


def part_line(x, y, a, b, qty, note, fs=4.2):
    cw = 0.62 * fs * F
    def num(xx, v, n):
        sv = str(v)
        text(xx, y, sv, size=fs, anchor="start", fill=INK)
        for k in range(n):
            line(xx, y + 1.5 + k * 1.3, xx + len(sv) * cw, y + 1.5 + k * 1.3, w=0.4, color=INK)
        return xx + len(sv) * cw
    xx = num(x, *a)
    text(xx + 2, y, "×", size=fs, anchor="start", fill=INK)
    xx = num(xx + 2.8 + cw * 1.2, *b)
    text(xx + 1.5, y, f" — {qty} шт" + (f" — {note}" if note else ""), size=fs, anchor="start", fill=INK)


def sheet2():
    frame()
    text(297, 22, "ТУМБА — ДЕТАЛИ (ЛДСП 16)", size=4.6, weight="bold")
    text(297, 30, "подчёркнутый размер — кромка по этой стороне: одна черта — 1 сторона, две — 2 стороны",
         size=2.1, fill="#444")
    # эскиз в косоугольной проекции
    sc = 0.17
    x, y = 40, 175
    w, h = W * sc, H * sc
    dx, dy = D * sc * 0.35, -D * sc * 0.35
    st = f'fill="none" stroke="{INK}" stroke-width="0.5" stroke-linejoin="round"'
    e(f'<path d="M{x},{y} h{w} v{-h} h{-w} z M{x},{y - h} l{dx},{dy} h{w} l{-dx},{-dy} '
      f'M{x + w},{y} l{dx},{dy} v{-h}" {st}/>')
    for xp in (X_P1, X_P2):
        xx = x + (xp + T / 2) * sc
        line(xx, y, xx, y - h, w=0.45, color=INK)
        line(xx, y - h, xx + dx, y - h + dy, w=0.35, color=INK)
    for x0 in (T, X_P2 + T):
        b0 = x + (x0 + 5) * sc
        rect(b0, y - (T + 20 + BOX_H) * sc, BOX_W * sc, BOX_H * sc, fill="none", stroke=INK, sw=0.35, dash="1.2 0.8")
    text(x + w / 2, y - h / 2, "сифон", size=2.0, fill="#2f6fb0")
    dim_h(x, x + w, y + 7, str(W), ext_from=y + 0.5, size=2.6)
    dim_v(y - h + dy, y + dy, x + w + dx + 6, str(H), ext_from=x + w + dx, size=2.6)
    text(x + w + dx / 2 + 3, y + dy / 2 + 2, str(D), size=2.6, anchor="start", rot=-45)
    for k, s in enumerate(("496", str(MID), "496")):
        xs_ = [T + SEC / 2, W / 2, W - T - SEC / 2][k]
        text(x + xs_ * sc, y - 3, s, size=2.2, fill=INK)
    for k, (a, b, q, n) in enumerate(PARTS):
        part_line(300, 70 + k * 21, a, b, q, n)
    stamp("детали с кромкой", "2 (А2)")
    save("sheet2.svg")


if __name__ == "__main__":
    sheet1()
    sheet2()
