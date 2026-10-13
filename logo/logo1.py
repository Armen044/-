#!/usr/bin/env python3
"""Логотип №1 «Арка-монограмма» — Rustamyan Atelier. Лист А4 (альбом): основной знак + варианты."""
SERIF = "Liberation Serif, DejaVu Serif, serif"
SANS = "DejaVu Sans, Liberation Sans, sans-serif"


def logo(cx, cy, s, ink, words=True):
    """Знак: двойная арка + R, под ним RUSTAMYAN / ATELIER. s — масштаб (1 = арка шириной 140)."""
    g = (f'<g transform="translate({cx} {cy}) scale({s})" fill="{ink}" stroke="{ink}">'
         '<path d="M-70 60 V-40 A70 70 0 0 1 70 -40 V60" fill="none" stroke-width="3"/>'
         '<path d="M-58 60 V-38 A58 58 0 0 1 58 -38 V60" fill="none" stroke-width="1"/>'
         f'<text x="0" y="38" font-family="{SERIF}" font-size="110" text-anchor="middle" stroke="none">R</text>')
    if words:
        g += (f'<text x="0" y="120" font-family="{SERIF}" font-size="40" letter-spacing="10" text-anchor="middle" stroke="none">RUSTAMYAN</text>'
              f'<text x="0" y="152" font-family="{SANS}" font-size="16" letter-spacing="6" text-anchor="middle" stroke="none">A T E L I E R</text>')
    return g + '</g>'


W, H = 297, 210  # мм
cards = [("#f3ede3", "#3b2f25", "основной"), ("#2c2a27", "#d8b98a", "на тёмном"),
         ("#ffffff", "#111111", "чёрно-белый"), ("#3b2f25", "#f3ede3", "инверсия")]
parts = [f'<rect width="{W}" height="{H}" fill="#faf8f4"/>',
         f'<rect x="12" y="12" width="{W-24}" height="118" rx="3" fill="#f3ede3"/>',
         logo(W / 2, 64, 0.38, "#3b2f25")]
cw, gap = 62, 7.67
for i, (bg, ink, label) in enumerate(cards):
    x = 12 + i * (cw + gap)
    parts.append(f'<rect x="{x}" y="138" width="{cw}" height="48" rx="2" fill="{bg}" stroke="#e2dccf" stroke-width="0.3"/>')
    parts.append(logo(x + cw / 2, 156, 0.15, ink))
    parts.append(f'<text x="{x}" y="192" font-family="{SANS}" font-size="3.2" fill="#6b645a">{label}</text>')
parts.append(f'<text x="12" y="202" font-family="{SANS}" font-size="3.2" fill="#6b645a">'
             'Цвета: тёмный орех #3B2F25 · лён #F3EDE3 · золото #D8B98A · графит #2C2A27</text>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">'
       + "".join(parts) + '</svg>')
open("rustamyan_logo1.svg", "w").write(svg)
