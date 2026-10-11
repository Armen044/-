"""Геометрия участка 9.5 × 26 м (метры). x — от левого забора, y — от дома к заднему забору."""
from shapely.geometry import Point, Polygon, LineString, box
from shapely.ops import unary_union

W, L = 9.5, 26.0
PIPE = 16.6            # существующая газовая труба (граница декоративной зоны и огорода)
TERR_ROOF = 2.5        # крытая терраса 0…2.5
PATIO = 4.0            # мощёная площадка 2.5…4.0

FIRE_C = (6.2, 12.6)   # центр костровой чаши
FIRE_R = 1.9           # радиус гравийной площадки
FIG_C, FIG_R = (1.9, 14.6), 1.8      # существующий инжир
PLUM_C, PLUM_R = (8.5, 23.2), 1.9    # существующая слива
PATH_HW = 0.5          # полуширина дорожки (плиты 0.6 + гравийная обочина)


def catmull(pts, n=12):
    out = []
    p = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


# осевая дорожки: от террасы вдоль правой посадки, мимо костровой площадки (слева от неё),
# между костром и инжиром — к калитке огорода в центре трубы
PATH_PTS = [(7.0, 3.0), (7.0, 4.0), (7.0, 6.0), (6.6, 8.0), (5.4, 9.6), (4.2, 11.0),
            (3.85, 12.6), (4.05, 14.2), (4.65, 15.7), (4.65, 16.6), (4.65, 17.4)]
PATH_LINE = LineString(catmull(PATH_PTS))

DECO = box(0, PATIO, W, PIPE)
TERRACE = box(0, 0, W, PATIO)
PATH = PATH_LINE.buffer(PATH_HW, cap_style=2).intersection(DECO)
FIRE = Point(FIRE_C).buffer(FIRE_R, 64).difference(PATH)
FIG = Point(FIG_C).buffer(FIG_R, 48)

_c = PATH_LINE.coords
LEFT = Polygon([(0, -1), (_c[0][0], -1)] + list(_c) + [(_c[-1][0], 18), (0, 18)])

LAWN_PTS = [(2.4, 4.6), (4.8, 4.55), (5.8, 4.65), (7.5, 4.8), (8.0, 9.0), (6.0, 11.0), (4.2, 12.9), (3.5, 13.0),
            (2.75, 12.3), (2.1, 11.1), (1.8, 9.6), (2.1, 7.9), (1.75, 6.2), (1.9, 4.9)]
LAWN = (Polygon(catmull(LAWN_PTS + [LAWN_PTS[0]], 10)).buffer(0)
        .intersection(LEFT).difference(PATH).difference(FIG.buffer(0.15)))
LEFT_BED = DECO.intersection(LEFT).difference(PATH).difference(FIRE).difference(LAWN)
RIGHT_BED = DECO.difference(LEFT).difference(PATH).difference(FIRE)

# огород (концепция прежняя)
GARDEN = box(0, PIPE, W, L)
RASP = box(0, PIPE, 1.3, L)
PLUMZ = box(7.8, PIPE, W, L)
BEDS = [box(x0, y0, x0 + 1.8, y0 + 1.2) for x0 in (2.0, 5.5) for y0 in (17.3, 19.0, 20.7, 22.4, 24.1)]
GRAVEL_G = GARDEN.difference(RASP).difference(PLUMZ).difference(unary_union(BEDS))

ZONES = [  # код, название, геометрия
    ("A", "Газон", LAWN),
    ("B", "Костровая зона (гравий, чаша, скамья)", FIRE),
    ("C", "Левая посадка / миксбордер, приствольный круг инжира", LEFT_BED),
    ("D", "Правая посадка: зелёный экран, обрамление костровой зоны", RIGHT_BED),
    ("E", "Дорожка к огороду (плиты в гравии)", PATH),
    ("K", "Терраса: крытая часть и мощёная площадка", TERRACE),
    ("F", "Огород: высокие грядки", unary_union(BEDS)),
    ("G", "Гравийные дорожки и сервисный проход в огороде", GRAVEL_G),
    ("H", "Малинник", RASP),
    ("I", "Зона сливы и сопутствующих посадок", PLUMZ),
]

if __name__ == "__main__":
    tot = 0
    for c, n, g in ZONES:
        print(c, round(g.area, 1), g.geom_type, n)
        tot += g.area
    print("total", round(tot, 2), W * L)
    print("deco", round(DECO.area + TERRACE.area, 1), "garden", GARDEN.area)
    print("fire->right fence", W - FIRE_C[0], "lawn bounds", LAWN.bounds)
