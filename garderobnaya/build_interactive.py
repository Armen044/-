#!/usr/bin/env python3
"""Сборка интерактивной 3D-модели в один самодостаточный HTML-файл
(three.js и данные модели встроены, интернет не нужен)."""
import json
import os

import model3d

HERE = os.path.dirname(os.path.abspath(__file__))

model3d.build(interactive=True)
data = {"boxes": model3d.boxes, "groups": model3d.groups, "cloth": model3d.CLOTH}
with open(os.path.join(HERE, "interactive_template.html"), encoding="utf-8") as f:
    html = f.read()
with open(os.path.join(HERE, "vendor", "three.min.js"), encoding="utf-8") as f:
    three = f.read()
html = html.replace("/*__THREE__*/", three).replace("/*__DATA__*/", json.dumps(data, separators=(",", ":")))
out = os.path.join(HERE, "garderobnaya_3d.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(out, len(html) // 1024, "KB")
