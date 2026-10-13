#!/usr/bin/env python3
"""Сборка интерактивной 3D-модели (один HTML, three.js встроен) и версии для ссылки."""
import json
import os

import model
from geom import W, D, H

HERE = os.path.dirname(os.path.abspath(__file__))
model.build()
data = {"room": [W, D, H], "boxes": model.boxes, "cyls": model.cyls, "groups": model.groups, "cloth": model.CLOTH,
        "colors": model.COLORS, "edges": model.EDGES, "wood": model.WOOD,
        "sets": [["drawers", "Ящики"], ["trays", "Лотки"], ["doors", "Двери"]],
        "lights": [[W / 2, 300, 2150], [275, 1800, 2150], [W - 275, 1800, 2150], [275, 3500, 2150],
                   [W - 275, 3500, 2150]]}
html = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
three = open(os.path.join(HERE, "..", "garderobnaya", "vendor", "three.min.js"), encoding="utf-8").read()
html = html.replace("/*__SUB__*/", f"{W} × {D} × {H} мм · цоколь 80 · ЛДСП «орех»")
html = html.replace("/*__THREE__*/", three).replace("/*__DATA__*/", json.dumps(data, separators=(",", ":")))
out = os.path.join(HERE, "garderobnaya3_3d.html")
open(out, "w", encoding="utf-8").write(html)
print(out, len(html) // 1024, "KB")
page = html.replace("<script>" + three + "</script>",
                    '<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>')
for tag in ("<!doctype html>", '<html lang="ru">', "</html>", "<head>", "</head>", "<body>", "</body>"):
    page = page.replace(tag + "\n", "").replace(tag, "")
page = "\n".join(l for l in page.split("\n") if not l.startswith("<meta "))
out2 = os.path.join(HERE, "artifact", "garderobnaya3_3d_link.html")
open(out2, "w", encoding="utf-8").write(page)
print(out2, len(page) // 1024, "KB")
