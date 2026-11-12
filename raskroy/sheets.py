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


def one_sheet(ox, oy, s, title, parts, cut_top):
    """Лист вертикально (2070 × 2800), текстура вдоль 2800. parts – [(ширина, имя|None)] слева направо,
    высота детали h; cut_top – детали сверху листа, иначе снизу."""
    W, H = SH, SW
    X = lambda v: ox + v * s       # noqa: E731
    Y = lambda v: oy + v * s       # noqa: E731
    text(X(W / 2), oy - 8, title, size=2.2, weight="bold")
    rect(X(0), Y(0), W * s, H * s, fill=OFF, sw=0.5)
    grain(X(0), Y(0), W * s, H * s, True)
    h = parts[0][2]
    y0 = 0 if cut_top else H - h
    x = 0
    xs = [0]
    for w, name, _ in parts:
        if name:
            rect(X(x), Y(y0), w * s, h * s, fill=PART, sw=0.5)
            grain(X(x), Y(y0), w * s, h * s, True)
            if w > 1000:
                text(X(x + w / 2), Y(y0 + h / 2), name, size=2.6, weight="bold")
                text(X(x + w / 2), Y(y0 + h / 2) + 6, f"{w} × {h}", size=2.2)
            else:
                text(X(x + w / 2) + 1.2, Y(y0 + h / 2), f"{name}  {w} × {h}", size=1.9, weight="bold", rot=-90)
        else:
            rect(X(x), Y(y0), w * s, h * s, fill=WASTE, sw=0.25)
            if w == 330:
                text(X(x + w / 2) + 1, Y(y0 + h / 2), "330 — стекло", size=1.6, rot=-90, fill="#555")
        x += w
        xs.append(x)
    if W - x > 200:
        rect(X(x), Y(y0), (W - x) * s, h * s, fill=OFF, sw=0.3)
        grain(X(x), Y(y0), (W - x) * s, h * s, True)
        text(X((x + W) / 2), Y(y0 + h / 2), f"остаток {W - x} × {h}", size=2.0, fill="#777")
    else:
        rect(X(x), Y(y0), (W - x) * s, h * s, fill=WASTE, sw=0.25)
    ry0, ry1 = (h, H) if cut_top else (0, H - h)
    text(X(W / 2), Y((ry0 + ry1) / 2), f"остаток {W} × {ry1 - ry0}", size=2.0, fill="#777")
    # стык текстуры
    yj = Y(h) if cut_top else Y(H - h)
    yj = Y(0) if cut_top else Y(H)
    # размеры
    if len(parts) > 1:
        for a_, b_ in zip(xs, xs[1:]):
            yy = Y(y0) - 4 if cut_top else Y(H) + 5
            dim_h(X(a_), X(b_), yy, str(b_ - a_), ext_from=Y(y0) if cut_top else Y(H), size=1.6)
    yb = Y(H) + (5 if cut_top else 12)
    dim_h(X(0), X(x), yb, str(x), ext_from=Y(H), size=2.0)
    dim_h(X(0), X(W), yb + 7, str(W), size=2.2)
    if cut_top:
        dim_v(Y(0), Y(h), X(0) - 5, str(h), ext_from=X(0), size=2.0)
        dim_v(Y(h), Y(H), X(0) - 5, str(H - h), ext_from=X(0), size=2.0)
    else:
        dim_v(Y(0), Y(H - h), X(0) - 5, str(H - h), ext_from=X(0), size=2.0)
        dim_v(Y(H - h), Y(H), X(0) - 5, str(h), ext_from=X(0), size=2.0)
    dim_v(Y(0), Y(H), X(W) + 6, str(H), ext_from=X(W), size=2.2)
    return X, Y


def both():
    s = 0.068
    oy = 52
    # лист 2 – фасады снизу листа; лист 1 – панель короба сверху листа:
    # нижний край фасадов и верхний край панели – соседние участки декора
    fronts = [(415, "Ф1", 1782), (30, None, 1782), (415, "Ф2", 1782), (330, None, 1782),
              (415, "Ф3", 1782), (30, None, 1782), (415, "Ф4", 1782)]
    X2, Y2 = one_sheet(62, oy, s, "ЛИСТ 2 — фасады (вырезаются СНИЗУ листа)", fronts, cut_top=False)
    X1, Y1 = one_sheet(262, oy, s, "ЛИСТ 1 — панель короба (вырезается СВЕРХУ листа)",
                       [(2050, "ПАНЕЛЬ КОРОБА", 1154)], cut_top=True)
    # стрелка совпадения текстуры
    ya, yb = Y2(SW), Y1(0)
    xa, xb = X2(SH) + 16, X1(0) - 10
    e(f'<path d="M{xa:.2f},{ya - 20:.2f} C{xa + 18:.2f},{ya - 20:.2f} {xb - 18:.2f},{yb + 20:.2f} {xb:.2f},{yb + 20:.2f}" '
      f'fill="none" stroke="#c0392b" stroke-width="0.5" marker-end="url(#arr)"/>')
    text((xa + xb) / 2 + 3, (ya + yb) / 2 - 2, "стык текстуры:", size=1.8, fill="#c0392b", weight="bold")
    text((xa + xb) / 2 + 3, (ya + yb) / 2 + 3.5, "низ фасадов →", size=1.7, fill="#c0392b")
    text((xa + xb) / 2 + 3, (ya + yb) / 2 + 8, "верх панели", size=1.7, fill="#c0392b")
    legend(48, 286)
    text(240, 286, "Листы из одной пачки, текстура вдоль 2800 · размеры в мм, без учёта пропила",
         size=1.6, anchor="start", fill="#555")


def both2():
    """Правый шкаф 433: фасад и видимая боковина 210, верхняя часть 1782 и нижняя 1154."""
    s = 0.068
    oy = 52
    up = [(430, "Фасад", 1782), (210, "Бок", 1782)]
    low = [(433, "Фасад", 1154), (210, "Бок", 1154)]
    X4, Y4 = one_sheet(62, oy, s, "ЛИСТ 4 — верх правого шкафа (вырезается СНИЗУ)", up, cut_top=False)
    X3, Y3 = one_sheet(262, oy, s, "ЛИСТ 3 — низ правого шкафа (вырезается СВЕРХУ)", low, cut_top=True)
    ya, yb = Y4(SW), Y3(0)
    xa, xb = X4(SH) + 16, X3(0) - 10
    e(f'<path d="M{xa:.2f},{ya - 20:.2f} C{xa + 18:.2f},{ya - 20:.2f} {xb - 18:.2f},{yb + 20:.2f} {xb:.2f},{yb + 20:.2f}" '
      f'fill="none" stroke="#c0392b" stroke-width="0.5" marker-end="url(#arr)"/>')
    text((xa + xb) / 2 + 3, (ya + yb) / 2 - 2, "стык текстуры:", size=1.8, fill="#c0392b", weight="bold")
    text((xa + xb) / 2 + 3, (ya + yb) / 2 + 3.5, "низ верхних →", size=1.7, fill="#c0392b")
    text((xa + xb) / 2 + 3, (ya + yb) / 2 + 8, "верх нижних", size=1.7, fill="#c0392b")
    legend(48, 286)
    text(240, 286, "Листы из одной пачки, текстура вдоль 2800 · размеры в мм, без учёта пропила",
         size=1.6, anchor="start", fill="#555")


def main():
    page("РАСКРОЙ ЛДСП 2800 × 2070 — ОБШИВКА ИНСТАЛЛЯЦИИ",
         "декор дерево: фасады над коробом, текстура совпадает по стыку", both)
    open(os.path.join(HERE, "sheet1.svg"), "w", encoding="utf-8").write("\n".join(g.out))
    page("РАСКРОЙ ЛДСП 2800 × 2070 — ПРАВЫЙ ШКАФ 433",
         "фасад и боковина: верхняя часть 1782 над нижней 1154, текстура совпадает по стыку", both2)
    open(os.path.join(HERE, "sheet2.svg"), "w", encoding="utf-8").write("\n".join(g.out))


if __name__ == "__main__":
    main()
