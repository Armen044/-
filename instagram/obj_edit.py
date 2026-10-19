#!/usr/bin/env python3
"""Обработка фото объекта: кадр 4:5, тон/контраст/резкость -> foto/edit/*.jpg (1080×1350, ТВ-стена 1080×810)."""
import os

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, "foto", "jpg"), os.path.join(HERE, "foto", "edit")
# имя -> (x0, x1, y0) доли кадра; высота = ширина × 1.25 (формат 4:5)
CROPS = {
    "foto-01": (0.065, 0.93, 0.0),    # детская: убрана упаковка слева и пакет справа внизу
    "foto-02": (0.0, 1.0, None),
    "foto-03": (0.15, 0.95, 0.02),    # ниша: без матраса с наклейкой
    "foto-04": (0.0, 1.0, 0.0),
    "foto-05": (0.0, 1.0, None),
    "foto-07": (0.0, 1.0, None),
    "foto-08": (0.0, 1.0, None),
    "foto-09": (0.0, 1.0, 0.0),
    "foto-10": (0.06, 1.0, 0.0),
    "foto-06-detal": (0.60, 1.0, 0.0),  # деталь: правый шкаф с ручками
}


def tone(im):
    im = ImageOps.autocontrast(im, cutoff=0.3, preserve_tone=True)
    im = ImageEnhance.Brightness(im).enhance(1.04)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.05)
    return im


def crop45(im, x0, x1, y0):
    W, H = im.size
    w = int((x1 - x0) * W)
    h = min(int(w * 1.25), H)
    w = int(h / 1.25)
    top = (H - h) // 2 if y0 is None else int(y0 * H)
    top = max(0, min(top, H - h))
    left = int(x0 * W)
    return im.crop((left, top, left + w, top + h))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, (x0, x1, y0) in CROPS.items():
        im = Image.open(os.path.join(SRC, name.replace("-detal", "") + ".jpg")).convert("RGB")
        im = tone(crop45(im, x0, x1, y0)).resize((1080, 1350), Image.LANCZOS)
        im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2)).save(os.path.join(OUT, name + ".jpg"), quality=92)
    im = tone(Image.open(os.path.join(SRC, "foto-06.jpg")).convert("RGB")).resize((1080, 810), Image.LANCZOS)
    im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2)).save(os.path.join(OUT, "foto-06.jpg"), quality=92)
    print("ok")
