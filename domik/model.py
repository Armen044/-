#!/usr/bin/env python3
"""Металлический каркас домика из профильной трубы 80×80 (по чертежу domik_chertezh.pdf).

Оси: X — на восток (от наружной грани стены 6), Y — на север (от наружной грани стены 1),
Z — вверх от низа нижней обвязки. Размеры в мм.
Наружные стены: труба внутрь от наружной грани; внутренние — по оси.
Стойки: в углах, на примыканиях, по обе стороны проёмов и промежуточные с шагом ≤ 2000.
Над каждым проёмом — перемычка, под окнами — подоконный ригель.
Домик на сваях: внутренние перегородки — только нижняя обвязка (без стоек, верхней обвязки
и перемычек); нижняя обвязка сплошная, в дверных проёмах не разрезается.
"""
import json
import math
import os

T = 80                 # сечение трубы
H = 3000               # высота каркаса
STEP = 2000            # максимальный шаг стоек
HERE = os.path.dirname(os.path.abspath(__file__))

# линии стен: имя, ориентация ('x' — стена вдоль X, координата c = Y оси), c, от, до (по осям), приоритет
LINES = [
    ("4", "x", 6260, 40, 9360, 0),
    ("1", "x", 40, 40, 5400, 0),
    ("3", "x", -1360, 5400, 9360, 0),
    ("6", "y", 40, 40, 6260, 1),
    ("2", "y", 5400, -1360, 40, 1),       # стена 2 (наружная, выступ)
    ("В4", "y", 5400, 40, 6260, 1),       # П2/3 – П5
    ("5", "y", 9360, -1360, 6260, 1),
    ("В1", "y", 3500, 40, 6260, 1),       # П1а/П1б – П2/3
    ("В2", "x", 3150, 40, 3500, 2),       # П1а – П1б
    ("В3", "x", 4300, 3500, 5400, 2),     # П4 – П2/3
]
# проёмы: линия, от, до (вдоль линии, в свету), низ, верх, вид
OPENINGS = [
    ("1", 850, 2650, 900, 2100, "окно"),
    ("1", 3950, 4950, 0, 2100, "дверь"),
    ("3", 6500, 8300, 0, 2100, "окно в пол"),
    ("5", 3400, 5200, 0, 2300, "витраж"),
    ("6", 3925, 5525, 900, 2300, "окно"),
    ("В4", 2725, 3575, 0, 2100, "дверь"),
    ("В1", 2150, 3000, 0, 2100, "дверь"),
    ("В1", 3300, 4150, 0, 2100, "дверь"),
    ("В3", 4025, 4875, 0, 2100, "дверь"),
]

INTERNAL = {"В1", "В2", "В3", "В4"}   # перегородки: только обвязка под ними
members = []   # dict: kind, line, x0,x1,y0,y1,z0,z1


def add(kind, line, o, c, a, b, z0, z1):
    """Элемент вдоль линии: a..b — вдоль, c — поперечная ось, z0..z1 по высоте."""
    if b - a < 1 or z1 - z0 < 1:
        return
    if o == "x":
        members.append(dict(kind=kind, line=line, x0=a, x1=b, y0=c - T / 2, y1=c + T / 2, z0=z0, z1=z1))
    else:
        members.append(dict(kind=kind, line=line, x0=c - T / 2, x1=c + T / 2, y0=a, y1=b, z0=z0, z1=z1))


def sub(iv, cuts):
    out = [iv]
    for c0, c1 in cuts:
        nxt = []
        for a, b in out:
            if c1 <= a or c0 >= b:
                nxt.append((a, b))
            else:
                if c0 > a:
                    nxt.append((a, c0))
                if c1 < b:
                    nxt.append((c1, b))
        out = nxt
    return out


def cuts_for(line):
    """Участки, занятые трубами линий с более высоким приоритетом (пересекающих эту линию)."""
    name, o, c, a, b, p = line
    res = []
    for n2, o2, c2, a2, b2, p2 in LINES:
        if o2 == o or p2 >= p:
            continue
        if a2 - T / 2 <= c <= b2 + T / 2 and a - T / 2 <= c2 <= b + T / 2:
            res.append((c2 - T / 2, c2 + T / 2))
    return res


# --- обвязки (нижняя и верхняя)
for ln in LINES:
    name, o, c, a, b, p = ln
    base = sub((a - T / 2, b + T / 2), cuts_for(ln))
    for a1, b1 in base:
        if name in INTERNAL:
            add("обвязка под перегородку", name, o, c, a1, b1, 0, T)
        else:
            add("верхняя обвязка", name, o, c, a1, b1, H - T, H)
            add("нижняя обвязка", name, o, c, a1, b1, 0, T)

# --- стойки
posts = {}


JAMBS = []
for _n, _oa, _ob, *_r in OPENINGS:
    if _n in INTERNAL:
        continue
    _o, _c = [(l[1], l[2]) for l in LINES if l[0] == _n][0]
    for _v in (_oa - T / 2, _ob + T / 2):
        JAMBS.append((_v, _c) if _o == "x" else (_c, _v))


def post(x, y, why):
    """Стойка; примыкание ближе 150 мм к стойке проёма не ставится — его роль берёт стойка проёма."""
    k = (round(x), round(y))
    if why != "у проёма" and any(0 < math.hypot(jx - x, jy - y) < 150 for jx, jy in JAMBS):
        return
    for (px, py) in posts:
        if abs(px - k[0]) < T and abs(py - k[1]) < T:
            return
    posts[k] = why


# опорные точки по каждой линии
for ln in LINES:
    name, o, c, a, b, p = ln
    if name in INTERNAL:
        continue
    pts = {a: "угол/примыкание", b: "угол/примыкание"}
    for n2, o2, c2, a2, b2, p2 in LINES:
        if o2 != o and a2 <= c <= b2 and a <= c2 <= b:
            pts.setdefault(c2, "примыкание")
    ops = [(oa, ob) for l, oa, ob, *_ in OPENINGS if l == name]
    for oa, ob in ops:
        pts[oa - T / 2] = "у проёма"
        pts[ob + T / 2] = "у проёма"
    # примыкание рядом со стойкой проёма: на этой же линии заменяется ею,
    # на поперечной линии остаётся только опорой для расчёта шага (стойку даёт проём)
    for v in [v for v, w in pts.items() if w != "у проёма"]:
        x, y = (v, c) if o == "x" else (c, v)
        if any(0 < math.hypot(jx - x, jy - y) < 150 for jx, jy in JAMBS):
            if any(abs(w - v) < 150 and pts[w] == "у проёма" for w in pts):
                del pts[v]
    xs = sorted(pts)
    full = list(xs)
    for s, e in zip(xs, xs[1:]):
        if any(oa - T / 2 <= s and e <= ob + T / 2 for oa, ob in ops):
            continue  # пролёт проёма — без стоек
        n = math.ceil((e - s) / STEP - 1e-9)
        for i in range(1, n):
            full.append(s + (e - s) * i / n)
    for v in sorted(full):
        x, y = (v, c) if o == "x" else (c, v)
        post(x, y, pts.get(v, "промежуточная"))

for (x, y), why in posts.items():
    members.append(dict(kind="стойка", line="", x0=x - T / 2, x1=x + T / 2, y0=y - T / 2, y1=y + T / 2,
                        z0=T, z1=H - T, why=why))

# --- перемычки и подоконные ригели
for name, oa, ob, z0, z1, kind in OPENINGS:
    if name in INTERNAL:
        continue
    o, c = [(l[1], l[2]) for l in LINES if l[0] == name][0]
    add("перемычка", name, o, c, oa, ob, z1, z1 + T)
    if z0 > 0:
        add("подоконный ригель", name, o, c, oa, ob, z0 - T, z0)


def length(m):
    return round(max(m["x1"] - m["x0"], m["y1"] - m["y0"], m["z1"] - m["z0"]))


def check():
    """Трубы не должны пересекаться друг с другом."""
    bad = 0
    for i, a in enumerate(members):
        for b in members[i + 1:]:
            ov = all(min(a[k + "1"], b[k + "1"]) - max(a[k + "0"], b[k + "0"]) > 0.5 for k in "xyz")
            if ov:
                bad += 1
                print("пересечение:", a["kind"], a["line"], b["kind"], b["line"], a, b)
    return bad


def spec():
    rows = {}
    for m in members:
        key = (m["kind"], length(m))
        rows[key] = rows.get(key, 0) + 1
    return rows


if __name__ == "__main__":
    print("пересечений:", check())
    tot = 0
    for (k, L), n in sorted(spec().items()):
        print(f"{k:20s} {L:6d} мм × {n}")
        tot += L * n
    print("всего, м:", tot / 1000, "стоек:", len(posts))
    with open(os.path.join(HERE, "model.js"), "w") as f:
        f.write("window.MODEL = " + json.dumps([[m["x0"], m["x1"], m["y0"], m["y1"], m["z0"], m["z1"], m["kind"]]
                                                 for m in members]) + ";\n")
