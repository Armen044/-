#!/usr/bin/env python3
"""Интерактивная 3D-модель гардеробной №2 на шаблоне первой гардеробной."""
import json
import os

import model

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "garderobnaya")

model.build()
data = {"boxes": model.boxes, "groups": model.groups, "cloth": model.CLOTH,
        "colors": model.COLORS, "edges": model.EDGES}
with open(os.path.join(SRC, "interactive_template.html"), encoding="utf-8") as f:
    html = f.read()
with open(os.path.join(SRC, "vendor", "three.min.js"), encoding="utf-8") as f:
    three = f.read()
html = html.replace("глубина шкафов 600 мм", "глубина шкафов 550 мм · обувница Aiden 800")
html = html.replace("/*__THREE__*/", three).replace("/*__DATA__*/", json.dumps(data, separators=(",", ":")))
out = os.path.join(HERE, "garderobnaya2_3d.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(out, len(html) // 1024, "KB")

page = html.replace("<script>" + three + "</script>",
                    '<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>')
for tag in ("<!doctype html>", '<html lang="ru">', "</html>", "<head>", "</head>", "<body>", "</body>"):
    page = page.replace(tag + "\n", "").replace(tag, "")
page = "\n".join(l for l in page.split("\n") if not l.startswith("<meta "))
out2 = os.path.join(HERE, "artifact", "garderobnaya2_3d_link.html")
with open(out2, "w", encoding="utf-8") as f:
    f.write(page)
print(out2, len(page) // 1024, "KB")
