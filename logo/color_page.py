#!/usr/bin/env python3
"""Цветные варианты логотипа «арка-шкаф» (вариант 1): страница-подборка палитр + SVG в export/color/."""
import os

from export_logo import text_path

HERE = os.path.dirname(os.path.abspath(__file__))
# название, фон, заливка шкафа, обводка, линии дверей, ручки, текст, описание
PALETTES = [
    ("Шалфей", "#F1F0EA", "#9CAF88", "#9CAF88", "#EEF2E8", "#C9A66B", "#3E4A3A", "приглушённый зелёный, самый популярный «спокойный» цвет кухонь последних лет"),
    ("Терракота", "#F6EEE7", "#C46A4A", "#C46A4A", "#F5DDD1", "#EDC58E", "#5A2E22", "тёплый глиняный, средиземноморский стиль"),
    ("Пыльная роза", "#F7EFEC", "#C4908C", "#C4908C", "#F8E8E5", "#D9B98A", "#5B3F3D", "как ниша в вашем рабочем месте, детские и спальни"),
    ("Мокко", "#F4EEE8", "#A47864", "#A47864", "#EEDFD5", "#E6CDA3", "#4A3328", "Mocha Mousse, цвет 2025 года по Pantone"),
    ("Глубокий синий", "#EEF0F3", "#1F3A5F", "#1F3A5F", "#8FA6C4", "#C9A66B", "#1F3A5F", "navy с латунью, классика и неоклассика"),
    ("Изумруд", "#EEF3F0", "#2F6B55", "#2F6B55", "#A9CDBE", "#D4B078", "#1E4436", "насыщенный зелёный, премиальные кухни и гардеробные"),
    ("Оливка", "#F2F1E8", "#7A7A4E", "#7A7A4E", "#DCDBC2", "#D2B27C", "#3E3E26", "природный зелёный, эко-стиль, японди"),
    ("Бордо", "#F5EDEE", "#6E2632", "#6E2632", "#D9A8B0", "#D4B078", "#4A1820", "винный, акцентный и дорогой"),
    ("Молочный и латунь", "#E9E4DC", "#F4F0E8", "#8C7B66", "#B9AD9C", "#B8925A", "#5E5244", "светлые фасады с латунной фурнитурой, минимализм"),
    ("Графит и золото", "#2B2C2E", "#3E4044", "#C9A66B", "#6C6E73", "#C9A66B", "#C9A66B", "антрацит с золотом, тёмный интерьер, лофт"),
]


def logo(bg, fill, stroke, line, handle, text, with_bg=True):
    name, w = text_path("RUSTAMYAN", "corm", 30, 7, 200, 342, "middle")
    sub, _ = text_path("МЕБЕЛЬ", "mont", 13, 10, 200, 370, "middle")
    half = max(w / 2, 62) + 28
    vb = (200 - half, 80, 2 * half, 312)
    body = (f'<path fill="{fill}" stroke="{stroke}" stroke-width="3.5" stroke-linejoin="round" d="M140,290 V170 A60,60 0 0 1 260,170 V290 Z"/>'
            f'<path fill="none" stroke="{line}" stroke-width="1.4" d="M149,282 V170 A51,51 0 0 1 251,170 V282 Z"/>'
            f'<path fill="none" stroke="{line}" stroke-width="1.6" d="M200,119 V282"/>'
            f'<path fill="none" stroke="{handle}" stroke-width="3.4" stroke-linecap="round" d="M192,196 V226 M208,196 V226"/>'
            f'<rect fill="{text}" x="152" y="290" width="8" height="7" rx="1.5"/><rect fill="{text}" x="240" y="290" width="8" height="7" rx="1.5"/>'
            f'<path fill="{text}" d="{name}"/><path fill="{text}" d="{sub}"/>')
    rect = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="{bg}"/>' if with_bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}">{rect}{body}</svg>'


if __name__ == "__main__":
    out = os.path.join(HERE, "export", "color")
    os.makedirs(out, exist_ok=True)
    slug = {"Шалфей": "shalfey", "Терракота": "terrakota", "Пыльная роза": "pylnaya-roza", "Мокко": "mokko",
            "Глубокий синий": "siniy", "Изумруд": "izumrud", "Оливка": "olivka", "Бордо": "bordo",
            "Молочный и латунь": "molochnyy-latun", "Графит и золото": "grafit-zoloto"}
    cards = []
    for i, (n, bg, fill, stroke, line, handle, text, desc) in enumerate(PALETTES, 1):
        with open(os.path.join(out, f"rustamyan-mebel-{i:02d}-{slug[n]}.svg"), "w", encoding="utf-8") as fh:
            fh.write(logo(bg, fill, stroke, line, handle, text, with_bg=False))
        sw = "".join(f'<i style="background:{c}" title="{c}"></i>' for c in (fill, handle, text, bg))
        cards.append(f'<figure><div class="tile" style="background:{bg}">{logo(bg, fill, stroke, line, handle, text)}</div>'
                     f'<figcaption><b>{i}. {n}</b><span>{desc}</span><div class="sw">{sw}</div>'
                     f'<code>шкаф {fill} · ручки {handle} · текст {text}</code></figcaption></figure>')
    page = f'''<title>Rustamyan Мебель: цвета</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Montserrat:wght@500;600&display=swap">
<style>
/* подборка палитр: сетка карточек, у каждой свой фон, под ней образцы цвета и коды */
:root{{--page:#F8F6F2;--ink:#2A2420;--muted:#6F6862;--line:#E2DAD0;
  --f-disp:"Cormorant Garamond","Times New Roman",serif;--f-sans:"Montserrat","Segoe UI",Arial,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--page:#1A1715;--ink:#EDE6DE;--muted:#A79E95;--line:#3A332E;color-scheme:dark}}}}
:root[data-theme="dark"]{{--page:#1A1715;--ink:#EDE6DE;--muted:#A79E95;--line:#3A332E;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--page);color:var(--ink);font:15px/1.5 var(--f-sans);padding-inline:16px;padding-block:28px 48px}}
.wrap{{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:28px}}
h1{{font:600 clamp(30px,4.5vw,46px)/1.05 var(--f-disp);margin:0;text-wrap:balance}}
header p{{margin:8px 0 0;color:var(--muted);max-width:70ch}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr));gap:24px}}
figure{{margin:0;display:flex;flex-direction:column;gap:10px;min-width:0}}
.tile{{border-radius:14px;overflow:hidden;border:1px solid var(--line)}}
.tile svg{{display:block;width:100%;height:auto}}
figcaption{{display:flex;flex-direction:column;gap:4px}}
figcaption b{{font-size:16px}}
figcaption span{{color:var(--muted);font-size:13.5px}}
.sw{{display:flex;gap:6px;margin-top:4px}}
.sw i{{width:22px;height:22px;border-radius:50%;border:1px solid var(--line)}}
code{{font:12px ui-monospace,Menlo,monospace;color:var(--muted)}}
</style>
<div class="wrap"><header><h1>Rustamyan · Мебель: арка-шкаф в цвете</h1>
<p>Вариант 1 в десяти популярных дизайнерских цветах мебели. Шкаф залит цветом, ручки латунные или золотые, надпись в тон. Под каждым вариантом образцы и коды цветов.</p></header>
<div class="grid">{"".join(cards)}</div></div>
'''
    with open(os.path.join(HERE, "logo-cveta.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    print("ok", len(cards))
