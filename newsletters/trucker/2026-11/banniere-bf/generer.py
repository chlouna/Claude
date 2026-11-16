"""Bannière teasing Black Friday (sans prix ni code), 5 langues, d'après la bannière BF de Louna."""
import base64, subprocess, json
from pathlib import Path
from PIL import Image
D = Path(__file__).parent
M = D.parent / "mockup-gps"
T = {
 "fr": ("DU 27.11 AU 30.11", "C’EST DEMAIN&nbsp;!", "OFFRE GPS", "RESTE CONNECTÉ", "Rendez-vous vendredi dans l’appli", "gps-fr.png"),
 "en": ("27.11 TO 30.11", "IT’S TOMORROW!", "GPS OFFER", "STAY TUNED", "See you on Friday in the app", "gps-en-corrige.png"),
 "es": ("DEL 27.11 AL 30.11", "¡ES MAÑANA!", "OFERTA GPS", "ESTATE ATENTO", "Nos vemos el viernes en la app", "gps-es.png"),
 "it": ("DAL 27.11 AL 30.11", "È DOMANI!", "OFFERTA GPS", "RESTA CONNESSO", "Ci vediamo venerdì nell’app", "gps-it.png"),
 "nl": ("27.11 T/M 30.11", "HET IS MORGEN!", "GPS-AANBIEDING", "BLIJF OP DE HOOGTE", "Tot vrijdag in de app", "gps-nl.png"),
}
CSS = """
*{margin:0;box-sizing:border-box} body{width:1200px;height:600px;background:#000;font-family:Inter;overflow:hidden;position:relative}
.line{position:absolute;left:0;right:0;top:300px;height:2px;background:#fff;opacity:.9}
.bf{position:absolute;left:30px;top:150px;width:370px;height:250px;background:#fff;border-radius:60px;display:flex;align-items:center;justify-content:center}
.bf div{font-weight:900;font-style:italic;font-size:84px;line-height:.92;color:#000;letter-spacing:-2px;text-align:center}
.dates{position:absolute;left:55px;top:385px;background:#ffff1a;padding:14px 28px;border-radius:14px;transform:rotate(-3deg);font-weight:900;font-style:italic;font-size:34px;color:#000;white-space:nowrap}
.tag{position:absolute;left:430px;top:95px;background:#ffff1a;padding:16px 34px 16px 46px;transform:rotate(-5deg);font-weight:900;font-style:italic;font-size:42px;color:#000;clip-path:polygon(22px 0,100% 0,100% 100%,22px 100%,0 50%);white-space:nowrap}
.box{position:absolute;left:430px;top:215px;width:400px;height:150px;background:#fff;border-radius:22px;padding:10px}
.box .in{border:4px dashed #000;border-radius:14px;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center}
.box .k{font-weight:800;font-style:italic;font-size:26px;letter-spacing:3px;color:#333}
.box .q{font-weight:900;font-style:italic;font-size:72px;line-height:1;color:#000;letter-spacing:8px}
.btn{position:absolute;left:430px;top:400px;width:400px;height:84px;background:#ffff1a;border-radius:18px;display:flex;align-items:center;justify-content:center;font-weight:900;font-style:italic;font-size:%BTN%px;color:#000;white-space:nowrap}
.sub{position:absolute;left:430px;top:500px;width:400px;text-align:center;font-style:italic;font-weight:500;font-size:24px;color:#d9d9d9}
.ph{position:absolute;left:868px;top:75px;height:450px;transform:rotate(5deg)}
"""
for lg, (dates, tag, k, btn, sub, img) in T.items():
    b64 = base64.b64encode((M / img).read_bytes()).decode()
    css = CSS.replace("%BTN%", "36" if len(btn) < 16 else "31")
    html = f"""<html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="line"></div>
<div class="bf"><div>BLACK<br>FRIDAY</div></div><div class="dates">{dates}</div>
<div class="tag">⚡ {tag}</div>
<div class="box"><div class="in"><div class="k">{k}</div><div class="q">???</div></div></div>
<div class="btn">{btn}</div><div class="sub">{sub}</div>
<img class="ph" src="data:image/png;base64,{b64}"></body></html>"""
    (D / f"_{lg}.html").write_text(html)
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:600}});
for(const l of %s){await p.goto('file://%s/_'+l+'.html');await p.waitForTimeout(150);await p.screenshot({path:'%s/_'+l+'.png'});}await b.close();})();""" % (json.dumps(list(T)), D, D)
subprocess.run(["node", "-e", js], check=True)
for lg in T:
    im = Image.open(D / f"_{lg}.png").convert("RGB")
    out = D / f"teasing-bf-{lg}.jpg"; q = 88
    while True:
        im.save(out, quality=q, optimize=True, progressive=True)
        if out.stat().st_size < 95_000 or q < 60: break
        q -= 4
    print(lg, out.stat().st_size // 1024, "Ko, q", q)
