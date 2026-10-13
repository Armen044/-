#!/usr/bin/env python3
"""Логотип №1 «Арка», встроенная в мебель: шкаф и кухня. Лист А4 (альбом), 4 варианта."""
SERIF = "Liberation Serif, DejaVu Serif, serif"
SANS = "DejaVu Sans, Liberation Sans, sans-serif"
INK, BG = "#3b2f25", "#f3ede3"

ARCH = ('<path d="M-70 60 V-40 A70 70 0 0 1 70 -40 V60" fill="none" stroke-width="3"/>')
INNER = ('<path d="M-58 60 V-38 A58 58 0 0 1 58 -38 V60" fill="none" stroke-width="1"/>')


def R(y, size):
    return f'<text x="0" y="{y}" font-family="{SERIF}" font-size="{size}" text-anchor="middle" stroke="none">R</text>'


def handle(x, y1, y2, w=3):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke-width="{w}" stroke-linecap="round"/>'


VARIANTS = [
    ("Шкаф с антресолью",
     "Арка — корпус шкафа: R на антресоли, ниже две двери с ручками.",
     ARCH + INNER
     + '<line x1="-58" y1="-8" x2="58" y2="-8" stroke-width="1.6"/>'
     + '<line x1="0" y1="-8" x2="0" y2="60" stroke-width="1.6"/>'
     + handle(-7, 14, 34) + handle(7, 14, 34)
     + R(-20, 54)
     + '<line x1="-80" y1="60" x2="80" y2="60" stroke-width="3"/>'),
    ("Шкаф-витрина с ящиками",
     "Вверху открытые полки, R стоит на полке; внизу три выдвижных ящика.",
     ARCH + INNER
     + R(-34, 50)
     + '<line x1="-58" y1="-30" x2="58" y2="-30" stroke-width="2"/>'
     + '<line x1="-58" y1="0" x2="58" y2="0" stroke-width="2"/>'
     + '<line x1="-58" y1="20" x2="58" y2="20" stroke-width="1.4"/><line x1="-58" y1="40" x2="58" y2="40" stroke-width="1.4"/>'
     + ''.join(f'<line x1="-9" y1="{y}" x2="9" y2="{y}" stroke-width="2.4" stroke-linecap="round"/>' for y in (10, 30, 50))
     + '<rect x="-46" y="-16" width="8" height="16" stroke="none"/><rect x="-36" y="-12" width="6" height="12" stroke="none"/><circle cx="40" cy="-7" r="7" fill="none" stroke-width="1.2"/>'
     + '<line x1="-80" y1="60" x2="80" y2="60" stroke-width="3"/>'),
    ("Кухня в арочной нише",
     "Столешница, нижние фасады с ручками, над ней R в нише.",
     ARCH + INNER
     + R(-6, 60)
     + '<rect x="-64" y="6" width="128" height="6" stroke="none"/>'
     + ''.join(f'<rect x="{x}" y="16" width="{w}" height="40" fill="none" stroke-width="1.4"/>'
               for x, w in ((-58, 36), (-18, 36), (22, 36)))
     + ''.join(handle(x, 22, 22, 0) + f'<line x1="{x-8}" y1="21" x2="{x+8}" y2="21" stroke-width="2.4" stroke-linecap="round"/>'
               for x in (-40, 0, 40))
     + '<line x1="-80" y1="60" x2="80" y2="60" stroke-width="3"/>'),
    ("Кухня: полки и вытяжка",
     "Вытяжка-купол в арке, полка, столешница, фасады; R на вытяжке.",
     ARCH + INNER
     + '<path d="M-26 -14 L-12 -52 H12 L26 -14 Z" fill="none" stroke-width="1.6"/>'
     + '<line x1="-8" y1="-52" x2="-8" y2="-96" stroke-width="1.2"/><line x1="8" y1="-52" x2="8" y2="-96" stroke-width="1.2"/>'
     + f'<text x="0" y="-22" font-family="{SERIF}" font-size="26" text-anchor="middle" stroke="none">R</text>'
     + '<line x1="-58" y1="-4" x2="-34" y2="-4" stroke-width="2"/><line x1="34" y1="-4" x2="58" y2="-4" stroke-width="2"/>'
     + '<circle cx="-50" cy="-10" r="4" fill="none" stroke-width="1.2"/><rect x="40" y="-16" width="8" height="12" fill="none" stroke-width="1.2"/>'
     + '<rect x="-64" y="8" width="128" height="5" stroke="none"/>'
     + '<line x1="0" y1="13" x2="0" y2="60" stroke-width="1.4"/><line x1="-58" y1="30" x2="58" y2="30" stroke-width="1.4"/>'
     + '<line x1="-36" y1="21" x2="-22" y2="21" stroke-width="2.4" stroke-linecap="round"/><line x1="22" y1="21" x2="36" y2="21" stroke-width="2.4" stroke-linecap="round"/>'
     + '<line x1="-36" y1="42" x2="-22" y2="42" stroke-width="2.4" stroke-linecap="round"/><line x1="22" y1="42" x2="36" y2="42" stroke-width="2.4" stroke-linecap="round"/>'
     + '<line x1="-80" y1="60" x2="80" y2="60" stroke-width="3"/>'),
]


def mark(cx, cy, s, body, ink=INK):
    return (f'<g transform="translate({cx} {cy}) scale({s})" fill="{ink}" stroke="{ink}">{body}'
            f'<text x="0" y="112" font-family="{SERIF}" font-size="40" letter-spacing="10" text-anchor="middle" stroke="none">RUSTAMYAN</text>'
            f'<text x="0" y="142" font-family="{SANS}" font-size="16" letter-spacing="6" text-anchor="middle" stroke="none">A T E L I E R</text></g>')


W, H = 297, 210
p = [f'<rect width="{W}" height="{H}" fill="#faf8f4"/>',
     f'<text x="12" y="17" font-family="{SERIF}" font-size="8" fill="#2a2620">Rustamyan Atelier — арка в мебели</text>',
     f'<text x="12" y="24" font-family="{SANS}" font-size="3.3" fill="#6b645a">Развитие логотипа №1: арка становится шкафом или кухней</text>']
cw, chh = 132, 76
for i, (title, note, body) in enumerate(VARIANTS):
    col, row = i % 2, i // 2
    x, y = 12 + col * (cw + 9), 30 + row * (chh + 15)
    p.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" rx="2.5" fill="{BG}"/>')
    p.append(mark(x + cw / 2, y + 33, 0.235, body))
    p.append(f'<text x="{x}" y="{y + chh + 5}" font-family="{SANS}" font-size="3.6" font-weight="bold" fill="#2a2620">{chr(1040 + i)}. {title}</text>')
    p.append(f'<text x="{x}" y="{y + chh + 9.5}" font-family="{SANS}" font-size="3" fill="#6b645a">{note}</text>')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">' + "".join(p) + '</svg>'
open("rustamyan_logo1_mebel.svg", "w").write(svg)
