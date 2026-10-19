#!/usr/bin/env python3
"""Финальный цветной логотип: вариант 9 «Молочный и латунь» — квадратный и горизонтальный, SVG в кривых."""
import os

from color_page import PALETTES, logo
from export_logo import text_path

HERE = os.path.dirname(os.path.abspath(__file__))
_, BG, FILL, STROKE, LINE, HANDLE, TEXT, _ = PALETTES[8]          # 9. Молочный и латунь


def icon():
    return (f'<path fill="{FILL}" stroke="{STROKE}" stroke-width="3.5" stroke-linejoin="round" d="M140,290 V170 A60,60 0 0 1 260,170 V290 Z"/>'
            f'<path fill="none" stroke="{LINE}" stroke-width="1.4" d="M149,282 V170 A51,51 0 0 1 251,170 V282 Z"/>'
            f'<path fill="none" stroke="{LINE}" stroke-width="1.6" d="M200,119 V282"/>'
            f'<path fill="none" stroke="{HANDLE}" stroke-width="3.4" stroke-linecap="round" d="M192,196 V226 M208,196 V226"/>'
            f'<rect fill="{TEXT}" x="152" y="290" width="8" height="7" rx="1.5"/><rect fill="{TEXT}" x="240" y="290" width="8" height="7" rx="1.5"/>')


def horizontal():
    name, w1 = text_path("RUSTAMYAN", "corm", 58, 12, 370, 152)
    sub, w2 = text_path("МЕБЕЛЬ НА ЗАКАЗ", "mont", 16, 14, 374, 192)
    right = 370 + max(w1, w2 + 4)
    vb = (150, 28, right - 150 + 35, 256)
    body = (f'<g transform="translate(40 -60) scale(1.05)">{icon()}</g>'
            f'<path fill="none" stroke="{HANDLE}" stroke-width="1" d="M335,92 V202"/>'
            f'<path fill="{TEXT}" d="{name}"/><path fill="{TEXT}" d="{sub}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}">{body}</svg>'


if __name__ == "__main__":
    out = os.path.join(HERE, "export", "molochnyy-latun")
    os.makedirs(out, exist_ok=True)
    files = {"rustamyan-mebel-molochnyy-latun.svg": logo(BG, FILL, STROKE, LINE, HANDLE, TEXT, with_bg=False),
             "rustamyan-mebel-molochnyy-latun-gorizontalnyy.svg": horizontal()}
    for n, s in files.items():
        with open(os.path.join(out, n), "w", encoding="utf-8") as fh:
            fh.write(s + "\n")
    print("ok", BG)
