"""Visuel 3 étapes sur le mockup « Fil d'activité » de Louna (FR d'abord)."""
import base64, subprocess, io
from pathlib import Path
from PIL import Image
D = Path(__file__).parent
ph = Image.open(D / "mockup-fil.png").convert("RGBA")
buf = io.BytesIO(); ph.save(buf, "PNG"); b64 = base64.b64encode(buf.getvalue()).decode()
S, OX, OY = 1.2, 60, 60          # échelle et position du téléphone
def P(x, y): return OX + x * S, OY + y * S
T = {
 "fr": ("LE BON RÉFLEXE<br>POUR TES ARRÊTS", [
   ("AVANT", "Regarde les photos, les avis et les j’aime", None),
   ("PENDANT", "Lis les avis récents&nbsp;: c’est ouvert&nbsp;? il reste de la place&nbsp;?", None),
   ("APRÈS", "Laisse un avis, ajoute une photo et like", "Tu grimpes dans le top contributeurs&nbsp;!")]),
}
ZONES = [((34, 258, 328, 390), (328, 324)), ((38, 488, 326, 550), (326, 519)), ((248, 553, 327, 574), (326, 563))]
CALL = [165, 420, 660]   # haut de chaque bulle
CSS = """*{margin:0;box-sizing:border-box}body{width:1200px;height:990px;background:#0c165b;font-family:Inter;color:#fff;position:relative;overflow:hidden}
.ph{position:absolute;left:%dpx;top:%dpx;width:%dpx}
.title{position:absolute;left:600px;top:34px;font-weight:900;font-style:italic;font-size:40px;line-height:1.1;color:#ffff1a}
.c{position:absolute;left:600px;width:560px;background:#fff;color:#0c165b;border-radius:28px;padding:22px 30px 24px}
.h{display:flex;align-items:center;gap:16px;font-weight:900;font-style:italic;font-size:40px}
.n{width:56px;height:56px;border-radius:50%%;background:#ffff1a;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:32px}
.b{font-weight:600;font-size:31px;line-height:1.25;margin-top:12px}
.x{display:inline-block;margin-top:14px;background:#ffff1a;font-weight:800;font-size:28px;padding:8px 14px;border-radius:10px}
svg{position:absolute;left:0;top:0}""" % (OX, OY, int(ph.width * S))
for lg, (title, steps) in T.items():
    h = f'<img class="ph" src="data:image/png;base64,{b64}"><div class="title">{title}</div>'
    svg = '<svg width="1200" height="990">'
    for i, ((t, b, extra), ((x1, y1, x2, y2), tgt), top) in enumerate(zip(steps, ZONES, CALL)):
        a, bb = P(x1, y1), P(x2, y2)
        svg += f'<rect x="{a[0]-4}" y="{a[1]-4}" width="{bb[0]-a[0]+8}" height="{bb[1]-a[1]+8}" rx="12" fill="none" stroke="#ffff1a" stroke-width="6"/>'
        tx, ty = P(*tgt); sx, sy = 600, top + 52
        svg += (f'<path d="M{sx} {sy} C {sx-60} {sy}, {tx+70} {ty}, {tx+14} {ty}" fill="none" stroke="#ffff1a" stroke-width="6"/>'
                f'<path d="M{tx+4} {ty} l20 -12 v24 z" fill="#ffff1a"/>')
        h += (f'<div class="c" style="top:{top}px"><div class="h"><div class="n">{i+1}</div>{t}</div><div class="b">{b}</div>'
              + (f'<div class="x">{extra}</div>' if extra else "") + '</div>')
    h += svg + '</svg>'
    (D / f"_m{lg}.html").write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{h}</body></html>')
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1200,height:990}}}});
await p.goto('file://{D}/_m{lg}.html');await p.screenshot({{path:'{D}/_m{lg}.png'}});await b.close();}})();"""
    subprocess.run(["node", "-e", js], check=True)
    im = Image.open(D / f"_m{lg}.png").convert("RGB"); out = D / f"etapes-mockup-{lg}.jpg"; q = 88
    while True:
        im.save(out, quality=q, optimize=True, progressive=True)
        if out.stat().st_size < 95_000 or q < 60: break
        q -= 4
    print(lg, out.stat().st_size // 1024, "Ko q", q)
