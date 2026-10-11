# Гардеробная 2400 × 1740 × 2640

- `garderobnaya.pdf` — 2 листа А2:
  1. план, развёртка левой / задней / правой стены (1:15);
  2. вид сбоку (разрез А–А), разрез Б–Б по нише гладильной доски (1:15), 3D-виды.
- `garderobnaya.png`, `garderobnaya_list2.png` — те же листы картинкой.

Пересборка:

```
python3 generate.py      # лист 1 (SVG)
python3 model3d.py       # 3D-модель -> model.js
node render3d.js         # 3d_front.png, 3d_axo.png
python3 sheet2.py        # лист 2 (SVG)
node render.js           # PNG + общий PDF
```
