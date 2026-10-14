#!/usr/bin/env python3
"""Сборка интерактивной 3D-модели кухни: HTML с встроенным three.js + версия для ссылки."""
import json
import os

import model3d

HERE = os.path.dirname(os.path.abspath(__file__))
data = model3d.data()
html = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
three = open(os.path.join(HERE, "..", "garderobnaya", "vendor", "three.min.js"), encoding="utf-8").read()
html = html.replace("/*__SUB__*/", "4000 × 1800 × 2630 мм · эмаль белая матовая · шпон дуб · столешница тёмный камень")
html = html.replace("/*__THREE__*/", three).replace("/*__DATA__*/", json.dumps(data, separators=(",", ":")))
out = os.path.join(HERE, "kuhnya2_3d.html")
open(out, "w", encoding="utf-8").write(html)
print(out, len(html) // 1024, "KB")
page = html.replace("<script>" + three + "</script>",
                    '<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>')
for tag in ("<!doctype html>", '<html lang="ru">', "</html>", "<head>", "</head>", "<body>", "</body>"):
    page = page.replace(tag + "\n", "").replace(tag, "")
page = "\n".join(l for l in page.split("\n") if not l.startswith("<meta "))
os.makedirs(os.path.join(HERE, "artifact"), exist_ok=True)
out2 = os.path.join(HERE, "artifact", "kuhnya2_3d_link.html")
open(out2, "w", encoding="utf-8").write(page)
print(out2, len(page) // 1024, "KB")
