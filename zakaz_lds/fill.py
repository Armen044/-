#!/usr/bin/env python3
"""Заполнение бланка заказа распила по списку деталей с фото.
Подчёркивание: 1 черта — кромка 0,4 по одной стороне этого размера, 2 черты — по двум."""
import sys
import openpyxl

src, dst = sys.argv[1], sys.argv[2]
COLOR = "ЛДСП 16"
# (длина, кромка_по_длине 0/1/2, ширина, кромка_по_ширине 0/1/2, кол-во, паз, комментарий)
PARTS = [
    (2544, 1, 530, 0, 10, "", ""),
    (500, 1, 530, 2, 1, "", ""),
    (468, 1, 530, 0, 9, "100+16", "глубина 7мм от кромки"),
    (600, 1, 530, 2, 1, "", ""),
    (568, 1, 530, 0, 9, "100+16", "глубина 7мм от кромки"),
    (568, 1, 50, 0, 7, "", ""),
    (200, 1, 530, 2, 1, "", ""),
    (168, 1, 530, 0, 4, "", ""),
    (1158, 1, 530, 0, 3, "", ""),
    (330, 1, 530, 0, 6, "", ""),
    (1458, 1, 530, 0, 3, "", ""),
    (805, 0, 530, 1, 1, "", ""),
    (705, 1, 530, 1, 1, "", ""),
    (678, 2, 192, 2, 4, "", ""),
    (642, 0, 113, 0, 8, "", ""),
    (440, 2, 142, 2, 8, "", ""),
    (642, 2, 440, 0, 4, "", ""),
    (2390, 0, 65, 0, 2, "", ""),
    (468, 0, 65, 0, 16, "", ""),
    (1190, 0, 65, 0, 6, "", ""),
    (1390, 0, 65, 0, 1, "", ""),
]

wb = openpyxl.load_workbook(src)
ws = wb.active
FIRST, LAST = 3, 77
for r in range(FIRST, LAST + 1):          # очистить старые данные, оформление оставить
    for c in range(1, 13):
        if c == 2:
            continue
        ws.cell(r, c).value = None
for i, (L, eL, Wd, eW, q, groove, note) in enumerate(PARTS):
    r = FIRST + i
    ws.cell(r, 1).value = COLOR
    ws.cell(r, 2).value = 1 if i == 0 else f"=SUM(B{r - 1},1)"
    ws.cell(r, 3).value = L
    ws.cell(r, 4).value = Wd
    ws.cell(r, 5).value = q
    if eL >= 1:
        ws.cell(r, 6).value = 0.4
    if eL >= 2:
        ws.cell(r, 7).value = 0.4
    if eW >= 1:
        ws.cell(r, 8).value = 0.4
    if eW >= 2:
        ws.cell(r, 9).value = 0.4
    if groove:
        ws.cell(r, 10).value = groove
    if note:
        ws.cell(r, 12).value = note
wb.save(dst)
print(len(PARTS), "строк")
