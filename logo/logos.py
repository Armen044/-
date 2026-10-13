#!/usr/bin/env python3
"""Концепты логотипа Rustamyan: 6 вариантов на одном листе (SVG -> PNG через render.js)."""
SERIF = "Liberation Serif, DejaVu Serif, serif"
SANS = "DejaVu Sans, Liberation Sans, sans-serif"
CW, CH, GAP = 520, 560, 30
cards = []


def card(i, bg, ink, title, note, body):
    col, row = i % 3, i // 3
    x, y = 40 + col * (CW + GAP), 150 + row * (CH + GAP)
    cards.append(f'''<g transform="translate({x} {y})">
<rect width="{CW}" height="{CH - 90}" rx="14" fill="{bg}"/>
<g transform="translate({CW/2} {(CH-90)/2})" fill="{ink}" stroke="{ink}">{body}</g>
<text x="0" y="{CH - 52}" font-family="{SANS}" font-size="20" font-weight="bold" fill="#2a2620">{i+1}. {title}</text>
<text x="0" y="{CH - 24}" font-family="{SANS}" font-size="15" fill="#6b645a">{note}</text></g>''')


def t(x, y, s, size, font=SERIF, ls=0, weight="normal", anchor="middle", fill=None):
    f = f' fill="{fill}"' if fill else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="{ls}" text-anchor="{anchor}" stroke="none"{f}>{s}</text>')


# 1. Арка-дверной проём с монограммой R — Atelier
card(0, "#f3ede3", "#3b2f25", "Арка-монограмма · Rustamyan Atelier",
     "Арка — проём шкафа / дверь в дом. Премиум, мебель на заказ.",
     '<path d="M-70 60 V-40 A70 70 0 0 1 70 -40 V60" fill="none" stroke-width="3"/>'
     '<path d="M-58 60 V-38 A58 58 0 0 1 58 -38 V60" fill="none" stroke-width="1"/>'
     + t(0, 38, "R", 110) +
     t(0, 120, "RUSTAMYAN", 40, ls=10) + t(0, 152, "A T E L I E R", 16, font=SANS, ls=6))

# 2. Шип «ласточкин хвост» — соединение GR
card(1, "#2c2a27", "#d8b98a", "Ласточкин хвост · GR",
     "Столярное соединение — символ надёжной работы руками.",
     '<rect x="-75" y="-95" width="150" height="150" fill="none" stroke-width="3"/>'
     '<path d="M-75 -20 H-30 L-40 20 H40 L30 -20 H75 V55 H-75Z" stroke="none" opacity="0.9"/>'
     + t(0, -35, "G R", 52, ls=6) + t(0, 110, "RUSTAMYAN", 36, ls=8) +
     t(0, 140, "МЕБЕЛЬ НА ЗАКАЗ", 15, font=SANS, ls=4))

# 3. Годичные кольца дерева с R
rings = "".join(f'<ellipse cx="{d*0.6:.1f}" cy="{-d*0.3:.1f}" rx="{r}" ry="{r*0.9:.1f}" fill="none" stroke-width="{1.2 if k%2 else 2.2}"/>'
                for k, (r, d) in enumerate([(85, 0), (70, 2), (55, 3), (41, 4), (28, 5)]))
card(2, "#e9efe4", "#3d4f36", "Срез дерева · Rustamyan Мебель",
     "Годичные кольца — натуральный массив, тёплая эко-подача.",
     f'<g transform="translate(0 -35)">{rings}<circle cx="4" cy="-2" r="6" stroke="none"/></g>'
     + t(0, 110, "RUSTAMYAN", 38, ls=8) + t(0, 140, "м е б е л ь", 18, font=SANS, ls=3))

# 4. Шкаф-фасады: три двери, ручка = засечка
card(3, "#ffffff", "#1f1f1f", "Фасады шкафа · Rustamyan Interiors",
     "Силуэт двустворчатого шкафа. Минимализм, корпусная мебель.",
     '<rect x="-62" y="-100" width="60" height="130" fill="none" stroke-width="3"/>'
     '<rect x="2" y="-100" width="60" height="130" fill="none" stroke-width="3"/>'
     '<line x1="-12" y1="-50" x2="-12" y2="-20" stroke-width="4"/><line x1="12" y1="-50" x2="12" y2="-20" stroke-width="4"/>'
     + '<line x1="-75" y1="38" x2="75" y2="38" stroke-width="3"/>'
     + t(0, 105, "RUSTAMYAN", 38, font=SANS, ls=9, weight="bold") + t(0, 138, "INTERIORS", 17, font=SANS, ls=10))

# 5. Буква A-крыша в слове (дом)
card(4, "#7a3b2e", "#f6ead8", "Дом в имени · Rustamyan Мебель",
     "Буквы A без перекладины — как крыши домов.",
     t(0, -10, "RUST<tspan font-weight=\"bold\">Λ</tspan>MY<tspan font-weight=\"bold\">Λ</tspan>N", 56, ls=4) +
     '<line x1="-170" y1="20" x2="170" y2="20" stroke-width="1.5"/>'
     + t(0, 60, "М Е Б Е Л Ь", 22, font=SANS, ls=6) + t(0, 120, "семейная мастерская", 18, font=SERIF))

# 6. Печать-герб с восьмиконечной звездой
star = "M0 -38 L9 -9 L38 0 L9 9 L0 38 L-9 9 L-38 0 L-9 -9Z"
card(5, "#1d2a3a", "#c9a96a", "Печать мастера · Rustamyan",
     "Печать со звездой — для бирок и гравировки на изделиях.",
     '<circle r="120" fill="none" stroke-width="3"/><circle r="108" fill="none" stroke-width="1"/>'
     '<circle r="70" fill="none" stroke-width="1"/>'
     f'<path d="{star}" stroke="none"/><path d="{star}" transform="rotate(45) scale(0.7)" stroke="none" opacity="0.7"/>'
     '<path id="arcT" d="M-88 0 A88 88 0 0 1 88 0" fill="none" stroke="none"/>'
     '<path id="arcB" d="M-88 0 A88 88 0 0 0 88 0" fill="none" stroke="none"/>'
     f'<text font-family="{SERIF}" font-size="24" letter-spacing="6" stroke="none"><textPath href="#arcT" startOffset="50%" text-anchor="middle">RUSTAMYAN</textPath></text>'
     f'<text font-family="{SANS}" font-size="14" letter-spacing="4" stroke="none" dy="14"><textPath href="#arcB" startOffset="50%" text-anchor="middle">МЕБЕЛЬ · С 2026</textPath></text>')

W = 40 * 2 + CW * 3 + GAP * 2
H = 150 + CH * 2 + GAP + 20
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<rect width="{W}" height="{H}" fill="#faf8f4"/>'
       f'<text x="40" y="70" font-family="{SERIF}" font-size="40" fill="#2a2620">Rustamyan — концепции логотипа</text>'
       f'<text x="40" y="108" font-family="{SANS}" font-size="18" fill="#6b645a">6 направлений · цвета и шрифты — для примера, финальный вариант дорабатывается</text>'
       + "".join(cards) + '</svg>')
open("rustamyan_logos.svg", "w").write(svg)
