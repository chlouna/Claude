"""Captures du tuto code promo traduites (FR, EN, ES, IT, NL), en une image par langue.
Capture 1 : écran Premium, flouté sauf la case code promo (aucun prix lisible).
Capture 2 : écran App Store « Activer l'offre », titre, champ et bouton traduits."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
D = Path(__file__).parent
B = D.parent.parent.parent / "blocs"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

T = {
 "fr": dict(tile=["Utiliser un code", "promotionnel"], title="Activer l’offre", field="Code", btn=["Acti", "ver"],
            cap=["1. Choisis « Utiliser un", "code promotionnel »"], cap2=["2. Saisis ton code", "puis « Activer »"]),
 "en": dict(tile=["Use a promo", "code"], title="Redeem Offer", field="Code", btn=["Re", "deem"],
            cap=["1. Choose “Use a", "promo code”"], cap2=["2. Enter your code,", "then “Redeem”"]),
 "es": dict(tile=["Usar un código", "promocional"], title="Canjear oferta", field="Código", btn=["Can", "jear"],
            cap=["1. Elige «Usar un", "código promocional»"], cap2=["2. Introduce tu código", "y pulsa «Canjear»"]),
 "it": dict(tile=["Usa un codice", "promozionale"], title="Riscatta offerta", field="Codice", btn=["Ris", "catta"],
            cap=["1. Scegli «Usa un", "codice promozionale»"], cap2=["2. Inserisci il codice", "e tocca «Riscatta»"]),
 "nl": dict(tile=["Promotiecode", "gebruiken"], title="Aanbieding inwisselen", field="Code", btn=["Inwis", "selen"],
            cap=["1. Kies ‘Promotiecode", "gebruiken’"], cap2=["2. Voer je code in en", "tik op ‘Inwisselen’"]),
}

def patch(im, box, bg, lines, font, size, color, S=6, maxw=None, dy=0):
    x0, y0, x1, y1 = box
    w, h = (x1 - x0) * S, (y1 - y0) * S
    p = Image.new("RGB", (w, h), bg); d = ImageDraw.Draw(p)
    fs = size
    while True:
        f = ImageFont.truetype(font, int(fs * S))
        if max(d.textlength(t, font=f) for t in lines) <= (maxw or (x1 - x0)) * S or fs < 4: break
        fs -= 0.2
    lh = fs * 1.2 * S
    top = (h - lh * len(lines)) / 2 + dy * S
    for i, t in enumerate(lines):
        tw = d.textlength(t, font=f); d.text(((w - tw) / 2, top + i * lh), t, font=f, fill=color)
    im.paste(p.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))

def premium(lang):
    src = Image.open(B / "capture-premium-code-promo-corrigee.png").convert("RGBA")
    im = Image.new("RGB", src.size, (255, 255, 255)); im.paste(src, (0, 0), src)
    # flou de l'écran sauf la case code promo et la flèche
    keep = [(139, 63, 199, 131), (155, 126, 200, 150), (186, 148, 218, 168)]
    zone = (18, 58, 201, 398)
    bl = im.crop(zone).filter(ImageFilter.GaussianBlur(3.2))
    wash = Image.new("RGB", bl.size, (255, 255, 255)); bl = Image.blend(bl, wash, 0.35)
    orig = im.copy(); im.paste(bl, zone[:2])
    for k in keep: im.paste(orig.crop(k), k[:2])
    patch(im, (143, 106, 195, 126), (255, 255, 255), T[lang]["tile"], REG, 6.6, (55, 55, 55), maxw=50)
    return im

def appstore(lang):
    im = Image.open(B / "capture-activer-offre.jpg").convert("RGB")
    t = T[lang]
    patch(im, (40, 176, 214, 199), im.getpixel((45, 178)), [t["title"]], BOLD, 15.5, (0, 0, 0), maxw=168)
    patch(im, (36, 214, 100, 231), im.getpixel((37, 214)), [t["field"]], REG, 7.2, (170, 170, 170), maxw=60)
    # aligne le texte du champ à gauche
    fld = im.getpixel((37, 214))
    sub = Image.new("RGB", (64 * 6, 17 * 6), fld); d = ImageDraw.Draw(sub)
    d.text((3 * 6, 2.2 * 6), t["field"], font=ImageFont.truetype(REG, int(7.2 * 6)), fill=(170, 170, 170))
    im.paste(sub.resize((64, 17), Image.LANCZOS), (36, 214))
    patch(im, (193, 211, 219, 235), im.getpixel((194, 212)), t["btn"], REG, 6.4, (175, 175, 175), maxw=24)
    return im

def compose(lang):
    a, b = premium(lang), appstore(lang)
    H = 760
    a = a.resize((round(a.width * H / a.height), H), Image.LANCZOS)
    b = b.resize((round(b.width * H / b.height), H), Image.LANCZOS)
    gap, pad, capH = 40, 30, 110
    W = a.width + b.width + gap + 2 * pad
    c = Image.new("RGB", (W, H + capH + pad), (255, 255, 255)); d = ImageDraw.Draw(c)
    c.paste(a, (pad, 0)); c.paste(b, (pad + a.width + gap, 0))
    f = ImageFont.truetype(BOLD, 26)
    for (x, w), lines in (((pad, a.width), T[lang]["cap"]), ((pad + a.width + gap, b.width), T[lang]["cap2"])):
        for i, t in enumerate(lines):
            tw = d.textlength(t, font=f); d.text((x + (w - tw) / 2, H + 18 + i * 34), t, font=f, fill=(6, 24, 102))
    out = B / f"tuto-code-promo-{lang}.jpg"
    c.save(out, quality=82, optimize=True, progressive=True)
    return out

if __name__ == "__main__":
    for lg in T:
        o = compose(lg); print(o.name, c := o.stat().st_size // 1024, "Ko", Image.open(o).size)
