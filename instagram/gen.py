#!/usr/bin/env python3
"""Instagram Rustamyan Мебель: аватарки и обложки «Актуального» (SVG), стиль «Молочный и латунь»."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo"))
from color_page import PALETTES  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
_, BG, FILL, STROKE, LINE, BRASS, TEXT, _ = PALETTES[8]
DARK_BG = "#3E3530"


def star(cx, cy, r=8, ri=3.6):
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else ri
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return f'<polygon fill="{BRASS}" stroke="none" points="{" ".join(pts)}"/>'


def ln(d, c=TEXT, w=3.2):
    return f'<path fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" d="{d}"/>'


ARCH = (f'<path fill="{FILL}" stroke="{STROKE}" stroke-width="3.5" stroke-linejoin="round" d="M140,290 V170 A60,60 0 0 1 260,170 V290 Z"/>'
        f'<path fill="none" stroke="{LINE}" stroke-width="1.4" d="M149,282 V170 A51,51 0 0 1 251,170 V282 Z"/>'
        f'<path fill="none" stroke="{LINE}" stroke-width="1.6" d="M200,119 V282"/>'
        f'<path fill="none" stroke="{BRASS}" stroke-width="3.4" stroke-linecap="round" d="M192,196 V226 M208,196 V226"/>'
        f'<rect fill="{TEXT}" x="152" y="290" width="8" height="7" rx="1.5"/><rect fill="{TEXT}" x="240" y="290" width="8" height="7" rx="1.5"/>')

# иконки в квадрате 0..100
ICONS = {
    "pod-klyuch": ("Под ключ", ln("M16,50 L50,20 L84,50 M26,42 V84 H74 V42") + ln("M42,84 V66 A8,8 0 0 1 58,66 V84", BRASS)),
    "kuhni": ("Кухни", ln("M14,14 H86 V36 H14 Z M38,14 V36 M62,14 V36") + ln("M10,56 H90", TEXT, 4) +
              ln("M14,58 V86 H86 V58 M38,58 V86 M62,58 V86") + ln("M22,65 H30 M46,65 H54 M70,65 H78 M43,51 H57", BRASS)),
    "shkafy": ("Шкафы", ln("M30,86 V44 A20,20 0 0 1 70,44 V86 Z M50,24 V86") + ln("M46,52 V62 M54,52 V62", BRASS) +
               ln("M34,86 V90 M66,86 V90")),
    "garderobnye": ("Гардеробные", ln("M12,22 H88", TEXT, 3.6) + "".join(
        ln(f"M{x},22 v6", BRASS) + ln(f"M{x - 11},38 L{x},28 L{x + 11},38 M{x - 11},38 L{x - 9},{L} H{x + 9} L{x + 11},38")
        for x, L in ((27, 80), (50, 72), (73, 84)))),
    "detskie": ("Детские", ln("M14,82 V48 A11,11 0 0 1 36,48 V82 M36,60 H86 V76 H36 M86,76 V82") +
                ln("M40,52 H56 V60 H40 Z") + star(72, 32, 9, 4)),
    "3d": ("3D-проекты", ln("M50,14 L82,32 V68 L50,86 L18,68 V32 Z M18,32 L50,50 L82,32 M50,50 V86") +
           ln("M50,14 L50,50", BRASS, 2)),
    "otzyvy": ("Отзывы", ln("M22,20 H78 Q86,20 86,28 V58 Q86,66 78,66 H46 L30,82 V66 H22 Q14,66 14,58 V28 Q14,20 22,20 Z") +
               star(32, 43, 7, 3.2) + star(50, 43, 7, 3.2) + star(68, 43, 7, 3.2)),
    "zamer": ("Замер", ln("M14,40 Q14,32 22,32 H54 Q62,32 62,40 V72 Q62,80 54,80 H22 Q14,80 14,72 Z") +
              f'<circle cx="38" cy="56" r="11" fill="none" stroke="{TEXT}" stroke-width="3.2"/>' +
              ln("M62,66 H90 V76 H62", BRASS) + ln("M70,66 V71 M78,66 V71 M86,66 V71", BRASS, 2.4)),
    "kontakty": ("Контакты", ln("M32,16 C25,16 18,22 20,32 C25,54 46,76 68,82 C77,84 84,78 84,70 V62 L68,55 L60,64 "
                                "C49,58 42,50 36,40 L45,32 L38,16 Z") + ln("M60,18 Q80,20 82,40 M60,28 Q71,30 72,40", BRASS)),
}


def svg(w, h, bg, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>\n')


def avatar(bg, ring=None):
    # знак-шкаф (200,203 — центр) в круге 1080: высота знака ~620 px
    s = 3.7
    g = f'<g transform="translate({540 - 200 * s} {540 - 205 * s}) scale({s})">{ARCH}</g>'
    r = f'<circle cx="540" cy="540" r="500" fill="none" stroke="{ring}" stroke-width="6"/>' if ring else ""
    return svg(1080, 1080, bg, r + g)


def cover(key):
    _, body = ICONS[key]
    s = 6.4                                   # иконка ~640 px в центре кадра сторис
    g = f'<g transform="translate({540 - 50 * s} {960 - 50 * s}) scale({s})">{body}</g>'
    return svg(1080, 1920, BG, g)


if __name__ == "__main__":
    out = os.path.join(HERE, "export")
    os.makedirs(out, exist_ok=True)
    files = {"avatar-svetlaya.svg": avatar(BG), "avatar-temnaya.svg": avatar(DARK_BG),
             "avatar-s-latunnym-kolcom.svg": avatar(BG, BRASS)}
    for i, k in enumerate(ICONS, 1):
        files[f"aktualnoe-{i:02d}-{k}.svg"] = cover(k)
    for n, s in files.items():
        with open(os.path.join(out, n), "w", encoding="utf-8") as fh:
            fh.write(s)
    print("ok", len(files))
