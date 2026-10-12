#!/usr/bin/env python3
"""Сборка интерактивной 3D-модели шкафа с ящиками: автономный HTML и версия для ссылки."""
import json
import os

import model

HERE = os.path.dirname(os.path.abspath(__file__))
model.build()
data = {"boxes": model.boxes, "groups": model.groups, "cloth": model.CLOTH,
        "meta": {"comps": model.comps()}}
with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
    html = f.read()
with open(os.path.join(HERE, "..", "garderobnaya", "vendor", "three.min.js"), encoding="utf-8") as f:
    three = f.read()
with open(os.path.join(HERE, "..", "shkaf", "kit.js"), encoding="utf-8") as f:
    kit = f.read()
html = html.replace("/*__DATA__*/", json.dumps(data, separators=(",", ":"))).replace("/*__KIT__*/", kit)

full = html.replace("/*__THREE__*/", three)
with open(os.path.join(HERE, "shkaf3_3d.html"), "w", encoding="utf-8") as f:
    f.write(full)

page = html.replace("<script>/*__THREE__*/</script>",
                    '<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>')
for tag in ("<!doctype html>", '<html lang="ru">', "</html>", "<head>", "</head>", "<body>", "</body>"):
    page = page.replace(tag + "\n", "").replace(tag, "")
page = "\n".join(l for l in page.split("\n") if not l.startswith("<meta "))
os.makedirs(os.path.join(HERE, "artifact"), exist_ok=True)
with open(os.path.join(HERE, "artifact", "shkaf3_3d_link.html"), "w", encoding="utf-8") as f:
    f.write(page)
print("ok", len(full) // 1024, "KB /", len(page) // 1024, "KB")
