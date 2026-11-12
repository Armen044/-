#!/usr/bin/env python3
"""Карты раскроя двух листов ЛДСП 2800 × 2070 (обшивка инсталляции), по эскизу заказчика.
Лист 1: панель короба 2050 × 1154. Лист 2: фасады 415 × 1782 (4 шт), выкроены подряд
с промежутками 30 и 330, как стоят на объекте, — чтобы рисунок декора шёл непрерывно."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "garderobnaya"))
import generate as g                                       # noqa: E402
from generate import e, line, rect, dim_h, dim_v           # noqa: E402

F = 1.8
_t = g.text


def text(x, y, s, size=2.6, **kw):
    _t(x, y, s, size=size * F, **kw)


g.text = text
SW, SH = 2800, 2070
PART, WASTE, OFF = "#e8d3b8", "url(#hatch)", "#f4f1ec"


def page(title, sub, body):
    g.out.clear()
    e('<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297" '
      f'font-family="{g.FONT}">')
    g.defs()
    rect(0, 0, 420, 297, fill="#fff", stroke="none")
    rect(8, 6, 404, 285, sw=0.6)
    text(210, 20, title, size=3.8, weight="bold")
    text(210, 28, sub, size=1.8, fill="#555")
    body()
    e('</svg>')


def grain(x, y, w, h, vertical):
    """Направление текстуры – тонкие линии по листу."""
    n = 28
    for i in range(1, n):
        if vertical:
            xx = x + w * i / n
            line(xx, y, xx, y + h, w=0.08, color="#c9b79f")
        else:
            yy = y + h * i / n
            line(x, yy, x + w, yy, w=0.08, color="#c9b79f")


def legend(x, y):
    items = [(PART, "деталь"), (OFF, "деловой остаток"), (WASTE, "отход / промежуток")]
    for k, (f, s) in enumerate(items):
        rect(x + k * 55, y - 3, 9, 5, fill=f, sw=0.25)
        text(x + k * 55 + 12, y + 1, s, size=1.7, anchor="start")


def sheet1():
    s = 0.08                      # лист вертикально: 2070 по ширине, 2800 по высоте
    ox, oy = 125, 40
    W, H = SH, SW
    X = lambda v: ox + v * s       # noqa: E731
    Y = lambda v: oy + v * s       # noqa: E731
    rect(X(0), Y(0), W * s, H * s, fill=OFF, sw=0.5)
    grain(X(0), Y(0), W * s, H * s, True)
    rect(X(0), Y(0), 2050 * s, 1154 * s, fill=PART, sw=0.5)
    rect(X(2050), Y(0), 20 * s, 1154 * s, fill=WASTE, sw=0.25)
    text(X(1025), Y(560), "ПАНЕЛЬ КОРОБА", size=2.6, weight="bold")
    text(X(1025), Y(560) + 7, "2050 × 1154 — 1 шт", size=2.4)
    text(X(1035), Y(1154 + 830), "остаток 2070 × 1646", size=2.0, fill="#777")
    dim_h(X(0), X(2050), Y(0) - 5, "2050", ext_from=Y(0), size=2.2)
    dim_h(X(0), X(W), Y(H) + 7, str(W), ext_from=Y(H), size=2.4)
    dim_v(Y(0), Y(1154), X(0) - 5, "1154", ext_from=X(0), size=2.2)
    dim_v(Y(1154), Y(H), X(0) - 5, "1646", ext_from=X(0), size=2.2)
    dim_v(Y(0), Y(H), X(W) + 7, str(H), ext_from=X(W), size=2.4)
    legend(40, 282)
    text(330, 282, "Лист ЛДСП 2800 × 2070 · размеры в мм", size=1.7, anchor="start", fill="#555")


def sheet2():
    s = 0.1                      # лист горизонтально: 2800 × 2070
    ox, oy = 55, 40
    W, H = SW, SH
    X = lambda v: ox + v * s       # noqa: E731
    Y = lambda v: oy + v * s       # noqa: E731
    rect(X(0), Y(0), W * s, H * s, fill=OFF, sw=0.5)
    grain(X(0), Y(0), W * s, H * s, False)
    y0 = H - 1782
    rect(X(0), Y(0), W * s, y0 * s, fill=OFF, sw=0.3)
    seq = [(415, "Ф1"), (30, None), (415, "Ф2"), (330, None), (415, "Ф3"), (30, None), (415, "Ф4")]
    x = 0
    xs = [0]
    for w, name in seq:
        if name:
            rect(X(x), Y(y0), w * s, 1782 * s, fill=PART, sw=0.5)
            text(X(x + w / 2), Y(y0 + 860), name, size=3.2, weight="bold")
            text(X(x + w / 2), Y(y0 + 860) + 7, "415 × 1782", size=1.9)
        else:
            rect(X(x), Y(y0), w * s, 1782 * s, fill=WASTE, sw=0.25)
            if w == 330:
                text(X(x + w / 2), Y(y0 + 900), "330 — место стеклянного фасада", size=1.6, rot=-90, fill="#555")
        x += w
        xs.append(x)
    text(X((x + W) / 2), Y(y0 + 900), f"остаток {W - x} × 1782", size=2.0, fill="#777")
    text(X(W / 2), Y(y0 / 2) + 1.5, f"остаток {W} × {y0}", size=2.0, fill="#777")
    for a, b in zip(xs, xs[1:]):
        dim_h(X(a), X(b), Y(H) + 6, str(b - a), ext_from=Y(H), size=2.0)
    dim_h(X(x), X(W), Y(H) + 6, str(W - x), ext_from=Y(H), size=2.0)
    dim_h(X(0), X(x), Y(H) + 13, str(x), size=2.2)
    dim_h(X(0), X(W), Y(H) + 20, str(W), size=2.4)
    dim_v(Y(0), Y(y0), X(W) + 6, str(y0), ext_from=X(W), size=2.0)
    dim_v(Y(y0), Y(H), X(W) + 6, "1782", ext_from=X(W), size=2.2)
    dim_v(Y(0), Y(H), X(W) + 13, str(H), ext_from=X(W), size=2.4)
    legend(40, 282)
    text(255, 282, "Фасады выкроены подряд — рисунок декора непрерывный", size=1.7, anchor="start", fill="#555")


def main():
    page("ЛИСТ 1 — ПАНЕЛЬ КОРОБА ИНСТАЛЛЯЦИИ", "ЛДСП 2800 × 2070, деталь 2050 × 1154", sheet1)
    open(os.path.join(HERE, "sheet1.svg"), "w", encoding="utf-8").write("\n".join(g.out))
    page("ЛИСТ 2 — ФАСАДЫ ШКАФОВ 860", "ЛДСП 2800 × 2070, 4 фасада 415 × 1782 с промежутками 30 и 330", sheet2)
    open(os.path.join(HERE, "sheet2.svg"), "w", encoding="utf-8").write("\n".join(g.out))


if __name__ == "__main__":
    main()
