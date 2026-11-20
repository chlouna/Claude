"""Visuel 3 étapes sur le mockup « Fil d'activité » de Louna (FR d'abord)."""
import base64, subprocess, io
from pathlib import Path
from PIL import Image
D = Path(__file__).parent
def load(lg):
    ph = Image.open(D / (f"mockup-fil-{lg}-trad.png" if lg != "fr" else "mockup-fil-fr.png")).convert("RGBA")
    buf = io.BytesIO(); ph.save(buf, "PNG"); return ph, base64.b64encode(buf.getvalue()).decode()
ph, _ = load("fr")
DY = {"fr": 0, "it": 8, "nl": 17, "es": 1, "en": -7}       # décalage vertical du fil selon la langue
LX = {"fr": 248, "it": 245, "nl": 228, "es": 240, "en": 262}  # début du bouton j'aime
S, OX, OY = 1.2, 60, 60          # échelle et position du téléphone
def P(x, y): return OX + x * S, OY + y * S
T = {
 "fr": ("Le bon réflexe pour tes arrêts", [
   ("Avant", "Regarde les photos, les avis et les j’aime", None),
   ("Pendant", "Lis les avis récents&nbsp;: c’est ouvert&nbsp;? il reste de la place&nbsp;?", None),
   ("Après", "Laisse un avis, ajoute une photo et laisse un like&nbsp;!", "<b style=\"color:#ffff1a\">Bonus&nbsp;:</b> tu grimpes dans le top contributeurs&nbsp;!")]),
 "en": ("Smart habits for your stops", [
   ("Before", "Check the photos, the reviews and the likes", None),
   ("During", "Read the latest reviews: is it open? is there still space?", None),
   ("After", "Leave a review, add a photo and drop a like!", "<b style=\"color:#ffff1a\">Bonus:</b> you climb the top contributors ranking!")]),
 "es": ("El buen reflejo para tus paradas", [
   ("Antes", "Mira las fotos, las opiniones y los me gusta", None),
   ("Durante", "Lee las opiniones recientes: ¿está abierto? ¿queda sitio?", None),
   ("Después", "Deja una opinión, añade una foto y da un me gusta", "<b style=\"color:#ffff1a\">Bonus:</b> ¡subes en el top de colaboradores!")]),
 "it": ("Il riflesso giusto per le tue soste", [
   ("Prima", "Guarda le foto, le recensioni e i Mi piace", None),
   ("Durante", "Leggi le recensioni recenti: è aperto? c’è ancora posto?", None),
   ("Dopo", "Lascia una recensione, aggiungi una foto e metti un Mi piace!", "<b style=\"color:#ffff1a\">Bonus:</b> sali nella classifica dei top contributori!")]),
 "nl": ("Slim kiezen waar je stopt", [
   ("Voor", "Bekijk de foto’s, de reviews en de likes", None),
   ("Tijdens", "Lees de nieuwste reviews: is het open? is er nog plek?", None),
   ("Na", "Laat een review achter, voeg een foto toe en geef een like!", "<b style=\"color:#ffff1a\">Bonus:</b> je klimt in de top van de bijdragers!")]),
}
def zones(lg):
    d, lx = DY[lg], LX[lg]
    return [((34, 258 + d, 328, 390 + d), (328, 324 + d)), ((38, 488 + d, 326, 550 + d), (326, 519 + d)), ((lx, 553 + d, 327, 574 + d), (326, 563 + d))]
CALL = [165, 420, 660]   # haut de chaque bulle
CSS = """@font-face{font-family:Bib;font-weight:700;src:url(file:///home/user/Claude/guide-profil/assets/fonts/BIB-Bold.woff2)}
@font-face{font-family:Noto;font-weight:400;src:url(file://%(D)s/fonts/noto-sans-latin-400-normal.woff2)}
@font-face{font-family:Noto;font-weight:600;src:url(file://%(D)s/fonts/noto-sans-latin-600-normal.woff2)}
@font-face{font-family:Noto;font-weight:700;src:url(file://%(D)s/fonts/noto-sans-latin-700-normal.woff2)}
*{margin:0;box-sizing:border-box}body{width:1200px;height:990px;background:#0c165b;font-family:Noto,sans-serif;color:#fff;position:relative;overflow:hidden}
.ph{position:absolute;left:%(OX)spx;top:%(OY)spx;width:%(W)spx}
.title{position:absolute;left:600px;top:66px;font-family:Bib;font-weight:700;font-size:35px;line-height:1.1;color:#ffff1a;white-space:nowrap}
.c{position:absolute;left:600px;width:560px;background:#fff;color:#0c165b;border-radius:28px;padding:22px 30px 24px}
.h{display:flex;align-items:center;gap:16px;font-family:Bib;font-weight:700;font-size:40px}
.n{width:56px;height:56px;border-radius:50%%;background:#ffff1a;display:flex;align-items:center;justify-content:center;font-family:Noto;font-weight:700;font-size:30px}
.b{font-weight:600;font-size:31px;line-height:1.25;margin-top:12px}
.x{display:inline-block;margin-top:14px;background:#061866;color:#fff;font-weight:600;font-size:28px;padding:8px 14px;border-radius:10px}
svg{position:absolute;left:0;top:0}""" % dict(D=D, OX=OX, OY=OY, W=int(ph.width * S))
for lg, (title, steps) in T.items():
    _, b64 = load(lg); ZONES = zones(lg)
    fs = {"es": 31, "it": 32}.get(lg, 35)
    h = f'<img class="ph" src="data:image/png;base64,{b64}"><div class="title" style="font-size:{fs}px">{title}</div>'
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
await p.goto('file://{D}/_m{lg}.html');await p.evaluate(()=>document.fonts.ready);await p.screenshot({{path:'{D}/_m{lg}.png'}});await b.close();}})();"""
    subprocess.run(["node", "-e", js], check=True)
    im = Image.open(D / f"_m{lg}.png").convert("RGB"); out = D / f"etapes-mockup-{lg}.jpg"; q = 88
    while True:
        im.save(out, quality=q, optimize=True, progressive=True)
        if out.stat().st_size < 95_000 or q < 60: break
        q -= 4
    print(lg, out.stat().st_size // 1024, "Ko q", q)
