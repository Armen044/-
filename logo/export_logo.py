#!/usr/bin/env python3
"""Логотип Rustamyan · Мебель (арка-шкаф): варианты 1 и 7 в SVG с текстом в кривых.

Шрифты: Cormorant Garamond Medium, Montserrat SemiBold (OFL), лежат в fonts/.
"""
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = {"corm": TTFont(os.path.join(HERE, "fonts", "corm.ttf")),
         "mont": TTFont(os.path.join(HERE, "fonts", "mont.ttf"))}
BROWN, CREAM = "#3A2F27", "#EFE6D8"


def text_path(s, font, size, spacing, x, y, anchor="start"):
    """Строка -> (d, ширина). Межбуквенный интервал как CSS letter-spacing, без хвоста после последней буквы."""
    f = FONTS[font]
    cmap, gs = f.getBestCmap(), f.getGlyphSet()
    k = size / f["head"].unitsPerEm
    adv = [gs[cmap[ord(c)]].width * k for c in s]
    width = sum(adv) + spacing * (len(s) - 1)
    cx = x - width / 2 if anchor == "middle" else x
    pen = SVGPathPen(gs)
    for c, a in zip(s, adv):
        gs[cmap[ord(c)]].draw(TransformPen(pen, (k, 0, 0, -k, cx, y)))
        cx += a + spacing
    return pen.getCommands(), width


def icon(sw=1.0):
    """Арка-шкаф: две двери, ручки, ножки (координаты как на странице концепций)."""
    return (f'<path fill="none" stroke-width="{3.5 * sw}" d="M140,290 V170 A60,60 0 0 1 260,170 V290 Z"/>'
            f'<path fill="none" stroke-width="{1.2 * sw}" d="M149,282 V170 A51,51 0 0 1 251,170 V282 Z"/>'
            f'<path fill="none" stroke-width="{1.6 * sw}" d="M200,119 V282"/>'
            f'<path fill="none" stroke-width="{3 * sw}" d="M192,196 V226 M208,196 V226"/>'
            '<rect stroke="none" x="152" y="290" width="8" height="7" rx="1.5"/>'
            '<rect stroke="none" x="240" y="290" width="8" height="7" rx="1.5"/>')


def svg(viewbox, body, color, w_mm=None):
    x, y, w, h = viewbox
    size = f' width="{w_mm}mm" height="{w_mm * h / w:.2f}mm"' if w_mm else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}"{size}>'
            f'<g fill="{color}" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>\n')


def logo1(color):
    name, w = text_path("RUSTAMYAN", "corm", 30, 7, 200, 342, "middle")
    sub, _ = text_path("МЕБЕЛЬ", "mont", 13, 10, 200, 370, "middle")
    body = icon() + f'<path stroke="none" d="{name}"/><path stroke="none" d="{sub}"/>'
    half = max(w / 2, 62) + 28                      # поля по ширине от самой широкой части
    return svg((200 - half, 80, 2 * half, 312), body, color)


def logo7(color):
    name, w1 = text_path("RUSTAMYAN", "corm", 58, 12, 370, 152)      # блок текста по центру знака
    sub, w2 = text_path("МЕБЕЛЬ НА ЗАКАЗ", "mont", 16, 14, 374, 192)
    body = (f'<g transform="translate(40 -60) scale(1.05)">{icon(1 / 1.05)}</g>'
            '<path fill="none" stroke-width="1" d="M335,92 V202"/>'
            f'<path stroke="none" d="{name}"/><path stroke="none" d="{sub}"/>')
    right = 370 + max(w1, w2 + 4)
    return svg((150, 28, right - 150 + 35, 256), body, color)


if __name__ == "__main__":
    out = os.path.join(HERE, "export")
    os.makedirs(out, exist_ok=True)
    for name, fn in (("rustamyan-mebel-1-arka-shkaf", logo1), ("rustamyan-mebel-7-gorizontalnyy", logo7)):
        for suffix, col in (("", BROWN), ("-svetlyy", CREAM)):
            with open(os.path.join(out, name + suffix + ".svg"), "w", encoding="utf-8") as fh:
                fh.write(fn(col))
    print("ok")
