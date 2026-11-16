"""Visuel 3 étapes Avant / Pendant / Après pour la section des arrêts des fêtes."""
import subprocess, json
from pathlib import Path
from PIL import Image
D = Path(__file__).parent
ICON = {
 "map": '<svg viewBox="0 0 64 64"><path d="M8 14l16-6 16 6 16-6v42l-16 6-16-6-16 6z" fill="none" stroke="#0c165b" stroke-width="5" stroke-linejoin="round"/><path d="M24 8v42M40 14v42" stroke="#0c165b" stroke-width="5"/></svg>',
 "eye": '<svg viewBox="0 0 64 64"><path d="M4 32s10-18 28-18 28 18 28 18-10 18-28 18S4 32 4 32z" fill="none" stroke="#0c165b" stroke-width="5" stroke-linejoin="round"/><circle cx="32" cy="32" r="8" fill="#0c165b"/></svg>',
 "like": '<svg viewBox="0 0 64 64"><path d="M20 28l10-18c4 0 7 3 6 8l-2 8h16c4 0 7 4 6 8l-4 16c-1 4-4 6-8 6H20z" fill="none" stroke="#0c165b" stroke-width="5" stroke-linejoin="round"/><rect x="6" y="28" width="10" height="28" rx="2" fill="#0c165b"/></svg>',
}
T = {
 "fr": ("LE BON RÉFLEXE POUR TES ARRÊTS", [
   ("map", "AVANT", "Regarde tout&nbsp;: photos, avis et j’aime"),
   ("eye", "PENDANT", "Lis les avis récentsLis les avis récents&nbsp;: c’est ouvert&nbsp;? c’est plein&nbsp;?nbsp;: ouvertLis les avis récents&nbsp;: c’est ouvert&nbsp;? c’est plein&nbsp;?nbsp;? pleinLis les avis récents&nbsp;: c’est ouvert&nbsp;? c’est plein&nbsp;?nbsp;?"),
   ("like", "APRÈS", "Laisse un avis, une photo ou un j’aime")]),
}
CSS = """*{margin:0;box-sizing:border-box}body{width:1200px;height:980px;background:#0c165b;font-family:Inter;color:#fff;position:relative;overflow:hidden}
.top{position:absolute;top:56px;left:0;right:0;text-align:center;font-weight:900;font-style:italic;font-size:44px;letter-spacing:1px;color:#ffff1a}
.row{position:absolute;left:70px;right:70px;height:220px;background:rgba(255,255,255,.07);border-radius:36px;display:flex;align-items:center;padding:0 44px}
.ic{width:150px;height:150px;border-radius:50%;background:#ffff1a;flex:none;display:flex;align-items:center;justify-content:center;position:relative}
.ic svg{width:84px;height:84px}
.n{position:absolute;top:-6px;left:-6px;width:52px;height:52px;border-radius:50%;background:#fff;color:#0c165b;font-weight:900;font-size:30px;display:flex;align-items:center;justify-content:center}
.tx{margin-left:44px}.h{font-weight:900;font-style:italic;font-size:56px;color:#ffff1a;line-height:1}
.b{font-weight:600;font-size:40px;line-height:1.2;margin-top:12px}
.ar{position:absolute;left:195px;width:0;height:0;border-left:22px solid transparent;border-right:22px solid transparent;border-top:26px solid #ffff1a}
.dot{position:absolute;width:10px;height:10px;border-radius:50%;background:#fff;opacity:.35}"""
for lg, (top, steps) in T.items():
    h = f'<div class="top">{top}</div>'
    for i, (ic, t, b) in enumerate(steps):
        y = 160 + i * 270
        h += f'<div class="row" style="top:{y}px"><div class="ic"><div class="n">{i+1}</div>{ICON[ic]}</div><div class="tx"><div class="h">{t}</div><div class="b">{b}</div></div></div>'
        if i < 2: h += f'<div class="ar" style="top:{y+232}px"></div>'
    for x, y in [(40,40),(1150,90),(1100,30),(90,120),(1160,940),(30,930),(600,30)]:
        h += f'<div class="dot" style="left:{x}px;top:{y}px"></div>'
    (D / f"_{lg}.html").write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{h}</body></html>')
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:980}});
for(const l of %s){await p.goto('file://%s/_'+l+'.html');await p.screenshot({path:'%s/_'+l+'.png'});}await b.close();})();""" % (json.dumps(list(T)), D, D)
subprocess.run(["node", "-e", js], check=True)
for lg in T:
    im = Image.open(D / f"_{lg}.png").convert("RGB"); out = D / f"etapes-{lg}.jpg"; q = 88
    while True:
        im.save(out, quality=q, optimize=True, progressive=True)
        if out.stat().st_size < 95_000 or q < 60: break
        q -= 4
    print(lg, out.stat().st_size // 1024, "Ko")
