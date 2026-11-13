"""Mockup GPS (écran itinéraire) traduit en ES, IT, NL ; EN corrigé (« Tous » → « All »).
Base : la version FR fournie. On efface chaque texte et on le réécrit à la même taille."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
D = Path(__file__).parent
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
S = 4
# clé : (zone texte FR, police, alignement, centre x ou None, largeur max, texte FR, couleur forcée ou None, coupe à droite)
E = {
 "pos":   ((105, 38, 168, 55), REG, "l", None, 170, "Ma position", None, None),
 "tous":  ((66, 128, 90, 140), REG, "l", None, 30, "Tous", None, None),
 "resto": ((124, 126, 182, 142), REG, "l", None, 58, "Restaurant", None, None),
 "park":  ((216, 127, 257, 142), REG, "l", None, 46, "Parking", None, None),
 "stat":  ((291, 126, 328, 143), REG, "l", None, 999, "Station", (194, 93, 243), 327),
 "peage": ((231, 244, 304, 259), REG, "c", 267, 72, "Péages ~€10", (255, 255, 255), None),
 "rapide":((36, 449, 158, 465), REG, "l", None, 145, "Itinéraire le plus rapide", None, None),
 "camion":((232, 464, 306, 481), REG, "l", None, 72, "Mon camion", None, None),
 "tard":  ((78, 526, 138, 545), BOLD, "c", 108, 125, "Plus tard", None, None),
 "dem":   ((235, 526, 300, 544), BOLD, "c", 266, 100, "Démarrer", (255, 255, 255), None),
}
T = {
 "es": dict(pos="Mi posición", tous="Todos", resto="Restaurante", park="Parking", stat="Gasolinera", peage="Peajes ~€10",
            rapide="Ruta más rápida", camion="Mi camión", tard="Más tarde", dem="Iniciar"),
 "it": dict(pos="La mia posizione", tous="Tutti", resto="Ristorante", park="Parcheggio", stat="Distributore", peage="Pedaggi ~€10",
            rapide="Percorso più veloce", camion="Il mio camion", tard="Più tardi", dem="Avvia"),
 "nl": dict(pos="Mijn locatie", tous="Alle", resto="Restaurant", park="Parking", stat="Tankstation", peage="Tol ~€10",
            rapide="Snelste route", camion="Mijn truck", tard="Later", dem="Starten"),
}

def load(name):
    im = Image.open(D / name).convert("RGBA")
    return im

def bg_of(rgb, box):
    x0, y0, x1, y1 = box
    cands = [rgb.getpixel((x0 - 1, y0)), rgb.getpixel((x1 + 1, y1)), rgb.getpixel((x0 - 1, y1)), rgb.getpixel((x1 + 1, y0))]
    return max(set(cands), key=cands.count)

def text_color(rgb, box, bg):
    x0, y0, x1, y1 = box
    best, bd = bg, -1
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            p = rgb.getpixel((x, y)); dd = sum(abs(a - b) for a, b in zip(p, bg))
            if dd > bd: best, bd = p, dd
    return best

def size_for(text, font, width):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    s = 6.0
    while s < 40:
        if d.textlength(text, font=ImageFont.truetype(font, int(s * S))) / S >= width: return s
        s += 0.1
    return s

def render(base_name, texts, out):
    im = load(base_name)
    rgb = Image.new("RGB", im.size, (255, 255, 255)); rgb.paste(im, (0, 0), im)
    for k, new in texts.items():
        box, font, al, cx, maxw, fr, col, clip = E[k]
        x0, y0, x1, y1 = box
        bg = (255, 255, 255) if k == "stat" else bg_of(rgb, box)
        color = col or text_color(rgb, box, bg)
        size = size_for(fr, font, x1 - x0 - 2)
        d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        while d0.textlength(new, font=ImageFont.truetype(font, int(size * S))) / S > maxw and size > 6: size -= 0.1
        f = ImageFont.truetype(font, int(size * S))
        tw = d0.textlength(new, font=f) / S
        # zone effacée : le texte FR + la place du nouveau texte
        if al == "l": nx0 = x0
        else: nx0 = cx - tw / 2
        ex0, ex1 = int(min(x0, nx0)) - 1, int(max(x1, nx0 + tw)) + 2
        if clip: ex1 = min(ex1, clip + 1)
        W, H = (ex1 - ex0), (y1 - y0 + 2)
        p = Image.new("RGB", (W * S, H * S), bg); d = ImageDraw.Draw(p)
        asc, desc = f.getmetrics()
        ty = (H * S - (asc + desc * 0.2)) / 2
        d.text(((nx0 - ex0) * S, ty), new, font=f, fill=color)
        rgb.paste(p.resize((W, H), Image.LANCZOS), (ex0, y0 - 1))
    # remet la transparence d'origine
    out_im = rgb.convert("RGBA"); out_im.putalpha(im.getchannel("A"))
    out_im.save(D / out)

if __name__ == "__main__":
    for lg, tx in T.items():
        render("gps-fr.png", tx, f"gps-{lg}.png")
    # EN : seule l'étiquette « Tous » est restée en français
    E["tous"] = ((66, 128, 90, 140), REG, "l", None, 30, "Tous", None, None)
    render("gps-en.png", {"tous": "All"}, "gps-en-corrige.png")
    print("ok")
