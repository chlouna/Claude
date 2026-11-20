"""Captures du tuto code promo, une image par langue (FR, EN, ES, IT, NL).
Capture 1 : écran Premium fourni par langue (case code promo corrigée : sans « Soit / Either / O / Cualquiera / Of »).
Capture 2 : écran App Store « Activer l'offre » redessiné net dans chaque langue, sur le cadre de téléphone des captures fournies."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
D = Path(__file__).parent
B = D.parent.parent.parent / "blocs"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
S = 3  # suréchantillonnage

T = {
 "fr": dict(tile=["Utiliser un code", "promotionnel"], title="Activer l’offre", field="Code", btn="Activer",
            cap1="1. Choisis « Utiliser un code promotionnel »", cap2="2. Saisis ton code puis « Activer »"),
 "en": dict(tile=["Use a", "promotional code"], title="Redeem Offer", field="Code", btn="Redeem",
            cap1="1. Choose “Use a promotional code”", cap2="2. Enter your code, then “Redeem”"),
 "es": dict(tile=["Utilizar", "un código"], title="Canjear oferta", field="Código", btn="Canjear",
            cap1="1. Elige «Utilizar un código»", cap2="2. Introduce tu código y pulsa «Canjear»"),
 "it": dict(tile=["Utilizza un codice", "promozionale"], title="Riscatta offerta", field="Codice", btn="Riscatta",
            cap1="1. Scegli «Utilizza un codice promozionale»", cap2="2. Inserisci il codice e tocca «Riscatta»"),
 "nl": dict(tile=["Gebruik een", "promotiecode"], title="Aanbieding inwisselen", field="Code", btn="Inwisselen",
            cap1="1. Kies ‘Gebruik een promotiecode’", cap2="2. Voer je code in en tik op ‘Inwisselen’"),
}

def fit(d, text, font, size, maxw):
    while size > 6:
        f = ImageFont.truetype(font, int(size * S))
        if d.textlength(text, font=f) <= maxw * S: return f
        size -= 0.25
    return ImageFont.truetype(font, int(size * S))

def flat(path):
    src = Image.open(path).convert("RGBA")
    im = Image.new("RGB", src.size, (255, 255, 255)); im.paste(src, (0, 0), src); return im

def premium(lang):
    im = flat(D / f"premium-{lang}.png")
    x0, y0, x1, y1 = (238, 182, 329, 207) if lang in ("it", "fr") else (238, 191, 329, 217)
    bg = im.getpixel((x0 + 2, y0 + 1))
    p = Image.new("RGB", ((x1 - x0) * S, (y1 - y0) * S), bg); d = ImageDraw.Draw(p)
    lines = T[lang]["tile"]
    f = None
    for t in lines:
        g = fit(d, t, REG, 10.5, 86)
        f = g if f is None or g.size < f.size else f
    lh = f.size * 1.18
    top = (p.height - lh * len(lines)) / 2
    for i, t in enumerate(lines):
        tw = d.textlength(t, font=f); d.text(((p.width - tw) / 2, top + i * lh), t, font=f, fill=(50, 50, 50))
    im.paste(p.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))
    return im

def screen_mask(im, ystart=56):
    """Masque de l'écran : remplissage depuis le centre, bloqué par le cadre noir, puis trous comblés ligne par ligne."""
    from PIL import ImageDraw as _D
    w, h = im.size
    bw = im.convert("L").point(lambda v: 255 if v > 60 else 0)
    _D.floodfill(bw, (w // 2, h // 2), 128)
    px = bw.load()
    m = Image.new("L", im.size, 0); mp = m.load()
    for y in range(ystart, h):
        xs = [x for x in range(w) if px[x, y] == 128]
        if len(xs) < 2 or max(xs) - min(xs) < 100: continue
        for x in range(min(xs), max(xs) + 1): mp[x, y] = 255
    return m

ICON = Image.open(D / "appstore-fr-original.jpg").convert("RGB").crop((103, 100, 148, 148))

def appstore(lang):
    base = flat(D / "premium-en.png")
    mask = screen_mask(base)
    w, h = base.size
    c = Image.new("RGB", (w * S, h * S), (255, 255, 255)); d = ImageDraw.Draw(c)
    def R(*v): return [x * S for x in v]
    # fond grisé derrière la feuille iOS, puis feuille blanche
    d.rectangle(R(0, 0, w, 78), fill=(214, 214, 219))
    d.rounded_rectangle(R(20, 72, w - 20, h), radius=14 * S, fill=(255, 255, 255))
    # en-tête App Store
    d.rounded_rectangle(R(44, 88, 64, 108), radius=5 * S, fill=(25, 136, 247))
    fa = ImageFont.truetype(BOLD, 14 * S); d.text(R(49.5, 89.5), "A", font=fa, fill=(255, 255, 255))
    d.text(R(71, 90), "App Store", font=ImageFont.truetype(BOLD, 13 * S), fill=(0, 0, 0))
    d.ellipse(R(302, 86, 324, 108), fill=(238, 238, 240))
    d.line(R(309, 93, 317, 101), fill=(120, 120, 125), width=2 * S); d.line(R(317, 93, 309, 101), fill=(120, 120, 125), width=2 * S)
    # icône de l'appli
    ic = ICON.resize((66 * S, 70 * S), Image.LANCZOS)
    c.paste(ic, (int((w / 2 - 33) * S), 132 * S))
    t = T[lang]
    def center(text, y, font, color):
        tw = d.textlength(text, font=font); d.text(((w * S - tw) / 2, y * S), text, font=font, fill=color)
    center("Michelin Truckfly - GPS", 218, ImageFont.truetype(REG, 12 * S), (120, 120, 125))
    center(t["title"], 240, fit(d, t["title"], BOLD, 24, 270), (0, 0, 0))
    # champ et bouton
    d.rounded_rectangle(R(42, 296, 258, 330), radius=8 * S, fill=(240, 240, 242))
    d.text(R(54, 305), t["field"], font=ImageFont.truetype(REG, 13 * S), fill=(165, 165, 170))
    d.rounded_rectangle(R(264, 296, 322, 330), radius=8 * S, fill=(240, 240, 242))
    fb = fit(d, t["btn"], REG, 12, 52); tw = d.textlength(t["btn"], font=fb)
    d.text(((293 * S - tw / 2), (313 - fb.size / S / 1.7) * S), t["btn"], font=fb, fill=(165, 165, 170))
    # flèche vers le champ
    pts = []
    for i in range(41):
        u = i / 40
        x = (1 - u) ** 2 * 205 + 2 * (1 - u) * u * 95 + u ** 2 * 80
        y = (1 - u) ** 2 * 425 + 2 * (1 - u) * u * 430 + u ** 2 * 352
        pts.append((x * S, y * S))
    d.line(pts, fill=(0, 0, 0), width=4 * S, joint="curve")
    d.polygon(R(80, 340, 66, 366, 94, 362), fill=(0, 0, 0))
    scr = c.resize((w, h), Image.LANCZOS)
    out = base.copy(); out.paste(scr, (0, 0), mask)
    return out

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(" "), [], ""
    for wd in words:
        nxt = (cur + " " + wd).strip()
        if d.textlength(nxt, font=font) <= maxw: cur = nxt
        else: lines.append(cur); cur = wd
    return lines + [cur]

def compose(lang):
    a, b = premium(lang), appstore(lang)
    gap, pad = 40, 30
    W = a.width + b.width + gap + 2 * pad
    f = ImageFont.truetype(BOLD, 22)
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    l1 = wrap(tmp, T[lang]["cap1"], f, a.width); l2 = wrap(tmp, T[lang]["cap2"], f, b.width)
    capH = 24 + 30 * max(len(l1), len(l2)) + 10
    c = Image.new("RGB", (W, a.height + capH), (255, 255, 255)); d = ImageDraw.Draw(c)
    c.paste(a, (pad, 0)); c.paste(b, (pad + a.width + gap, 0))
    for (x, wd), lines in (((pad, a.width), l1), ((pad + a.width + gap, b.width), l2)):
        for i, t in enumerate(lines):
            tw = d.textlength(t, font=f); d.text((x + (wd - tw) / 2, a.height + 14 + i * 30), t, font=f, fill=(6, 24, 102))
    out = B / f"tuto-code-promo-{lang}.jpg"
    c.save(out, quality=85, optimize=True, progressive=True)
    return out

if __name__ == "__main__":
    for lg in T:
        o = compose(lg); print(o.name, o.stat().st_size // 1024, "Ko", Image.open(o).size)
