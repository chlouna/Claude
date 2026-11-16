"""Mini tuto en 3 étapes pour accéder à l'espace propriétaire, à partir des captures de Louna."""
import base64, io, subprocess
from pathlib import Path
from PIL import Image
D = Path(__file__).parent
F = Path("/home/user/Claude/newsletters/trucker/2026-11/visuel-etapes/fonts")
src = Image.open(D / "captures-espace.jpg").convert("RGB")
BOX = [(18, 21, 417, 885), (433, 21, 830, 885), (847, 21, 1246, 885)]
def b64(im):
    b = io.BytesIO(); im.save(b, "JPEG", quality=92); return base64.b64encode(b.getvalue()).decode()
caps = ["Connectez-vous à l’appli ou au site",
        "Accédez à votre espace propriétaire",
        "Mettez à jour votre fiche et enregistrez"]
cards = "".join(
    f'<div class="c"><div class="h"><div class="n">{i+1}</div><div class="t">{t}</div></div>'
    f'<img src="data:image/jpeg;base64,{b64(src.crop(b))}"></div>' for i, (t, b) in enumerate(zip(caps, BOX)))
html = f"""<html><head><meta charset="utf-8"><style>
@font-face{{font-family:Bib;font-weight:700;src:url(file:///home/user/Claude/guide-profil/assets/fonts/BIB-Bold.woff2)}}
@font-face{{font-family:Noto;font-weight:600;src:url(file://{F}/noto-sans-latin-600-normal.woff2)}}
*{{margin:0;box-sizing:border-box}}body{{width:1200px;height:900px;background:#f5f3f1;font-family:Noto;display:flex;justify-content:space-between;padding:40px 36px}}
.c{{width:362px;display:flex;flex-direction:column;align-items:center}}
.h{{display:flex;gap:14px;align-items:flex-start;height:96px;width:100%}}
.n{{flex:none;width:52px;height:52px;border-radius:50%;background:#061866;color:#fff;font-family:Bib;font-size:30px;display:flex;align-items:center;justify-content:center}}
.t{{font-weight:600;font-size:27px;line-height:1.25;color:#061866;padding-top:4px}}
img{{width:340px;border-radius:26px;box-shadow:0 8px 24px rgba(6,24,102,.18)}}
</style></head><body>{cards}</body></html>"""
(D / "_t.html").write_text(html)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1200,height:900}}}});
await p.goto('file://{D}/_t.html');await p.evaluate(()=>document.fonts.ready);await p.screenshot({{path:'{D}/_t.png'}});await b.close();}})();"""
subprocess.run(["node", "-e", js], check=True)
im = Image.open(D / "_t.png").convert("RGB"); out = D / "tuto-espace-proprietaire.jpg"; q = 88
while True:
    im.save(out, quality=q, optimize=True, progressive=True)
    if out.stat().st_size < 95_000 or q < 60: break
    q -= 4
print(out.stat().st_size // 1024, "Ko q", q)
for f in ("_t.html", "_t.png"): (D / f).unlink()
