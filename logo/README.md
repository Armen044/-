# Логотип Rustamyan · Мебель (арка-шкаф)

`export/`:
- `rustamyan-mebel-1-arka-shkaf.*` — вариант 1 (знак + RUSTAMYAN / МЕБЕЛЬ);
- `rustamyan-mebel-7-gorizontalnyy.*` — вариант 7 (горизонтальный, «МЕБЕЛЬ НА ЗАКАЗ»);
- `.svg` — вектор, надписи в кривых; `.pdf` — вектор для типографии;
- `.png` — 3000 px, прозрачный фон; `-na-kremovom.png` — на кремовом фоне;
- `-svetlyy.*` — светлая версия для тёмного фона.

Цвет: #3A2F27 (тёмно-коричневый), светлая версия #EFE6D8.
Шрифты (OFL): Cormorant Garamond Medium, Montserrat SemiBold — `fonts/`.

Пересборка: `python3 export_logo.py && node render.js`.

## Выбранный цветной вариант: 9 «Молочный и латунь»

`export/molochnyy-latun/` — квадратный и горизонтальный: `.svg` и `.pdf` (вектор, текст в кривых),
`.png` 3000 px на прозрачном фоне, `-na-fone.png` на фоне #E9E4DC.
Цвета: шкаф #F4F0E8, обводка #8C7B66, линии дверей #B9AD9C, ручки #B8925A, текст #5E5244.
Пересборка: `python3 export_color.py && node render_dir.js export/molochnyy-latun "#E9E4DC"`.
