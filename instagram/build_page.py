#!/usr/bin/env python3
"""Страница-превью постов: сетка ленты + карточки с текстами для копирования; архив постов."""
import base64
import html
import io
import os
import zipfile

from PIL import Image

from captions import CAPTIONS
from gen import BRASS

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "posts")


def thumb(k):
    im = Image.open(os.path.join(P, k + ".png")).convert("RGB").resize((540, 675))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


keys = list(CAPTIONS)
grid = "".join(f'<img src="{thumb(k)}" alt="Пост {keys.index(k) + 1}">' for k in keys[::-1])
cards = "".join(f'<article><img src="{thumb(k)}" alt=""><div class="txt"><div class="n">Пост {i} · {k}.png</div>'
                f'<pre id="c{i}">{html.escape(t)}</pre><button type="button" data-t="c{i}">Скопировать текст</button></div></article>'
                for i, (k, t) in enumerate(CAPTIONS.items(), 1))
page = f'''<title>Instagram: первые 9 постов</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Montserrat:wght@400;500;600&display=swap">
<style>
/* сверху сетка ленты как в профиле, ниже карточки постов по порядку публикации с текстом для копирования */
:root{{--page:#F8F6F2;--ink:#2A2420;--muted:#6F6862;--line:#E2DAD0;--card:#FFFFFF;--accent:{BRASS};
 --f-disp:"Cormorant Garamond","Times New Roman",serif;--f-sans:"Montserrat","Segoe UI",Arial,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--page:#1A1715;--ink:#EDE6DE;--muted:#A79E95;--line:#3A332E;--card:#24201D;color-scheme:dark}}}}
:root[data-theme="dark"]{{--page:#1A1715;--ink:#EDE6DE;--muted:#A79E95;--line:#3A332E;--card:#24201D;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--page);color:var(--ink);font:15px/1.5 var(--f-sans);padding-inline:16px;padding-block:28px 48px}}
.wrap{{max-width:1000px;margin:0 auto;display:flex;flex-direction:column;gap:28px}}
h1{{font:600 clamp(28px,4vw,42px)/1.1 var(--f-disp);margin:0}}
h2{{font:600 14px var(--f-sans);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0}}
p{{margin:0;max-width:66ch;color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:3px;max-width:540px}}
.grid img{{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}}
article{{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:24px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px}}
@media (max-width:700px){{article{{grid-template-columns:1fr}}}}
article>img{{width:100%;border-radius:6px}}
.txt{{display:flex;flex-direction:column;gap:10px;min-width:0}}
.n{{font:600 22px var(--f-disp)}}
pre{{margin:0;font:14px/1.5 var(--f-sans);white-space:pre-wrap;overflow-wrap:anywhere}}
button{{align-self:flex-start;font:600 13px var(--f-sans);background:var(--accent);color:#fff;border:0;border-radius:6px;padding:8px 14px;cursor:pointer}}
button:focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}
.list{{display:flex;flex-direction:column;gap:12px}}
</style>
<div class="wrap">
<header><h1>Instagram: первые 9 постов</h1>
<p>Картинки 1080 × 1350 (формат 4:5) лежат в архиве. Публикуйте строго по порядку с 1 по 9: так лента сложится, как на сетке ниже. Пост 1 окажется справа внизу, пост 9 слева вверху.</p></header>
<section><h2>Как будет выглядеть лента</h2><div class="grid" style="margin-top:12px">{grid}</div></section>
<section class="list"><h2>Посты и тексты по порядку публикации</h2>{cards}</section>
</div>
<script>
document.querySelectorAll('button[data-t]').forEach(b=>b.addEventListener('click',()=>{{
 const el=document.getElementById(b.dataset.t);
 navigator.clipboard.writeText(el.textContent).then(()=>{{b.textContent='Скопировано'}}).catch(()=>{{
  const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Текст выделен — скопируйте'}});
}}));
</script>'''
with open(os.path.join(HERE, "instagram-posty.html"), "w", encoding="utf-8") as fh:
    fh.write(page)
with open(os.path.join(P, "podpisi.md"), "w", encoding="utf-8") as f:
    f.write("# Первые 9 постов: порядок публикации и тексты\n\n")
    for i, (k, t) in enumerate(CAPTIONS.items(), 1):
        f.write(f"## {i}. {k}.png\n\n```\n{t}\n```\n\n")
with zipfile.ZipFile(os.path.join(HERE, "instagram-posty-1-9.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    for k in keys:
        z.write(os.path.join(P, k + ".png"), k + ".png")
    z.write(os.path.join(P, "podpisi.md"), "podpisi.md")
print("ok")
