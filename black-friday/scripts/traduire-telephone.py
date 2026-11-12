# Crée une capture du téléphone GPS par langue, avec « Puis » traduit dans l'encart de guidage.
# Usage : python3 black-friday/scripts/traduire-telephone.py
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ICI = Path(__file__).resolve().parent.parent
SOURCE = ICI / "assets" / "telephone-gps.png"
POLICE = ICI.parent / "interstitiels" / "assets" / "fonts" / "Inter-Bold.otf"
MOTS = {"en": "Then", "de": "Dann", "it": "Poi", "es": "Luego", "nl": "Daarna", "pl": "Potem", "ro": "Apoi"}

# Zone de l'encart « Puis ↑ » dans la capture (en pixels)
TEXTE_X, LIGNE_BASE = 49, 254          # début du mot, ligne de base (bas des capitales)
FOND_X0, FOND_X1, FOND_Y0, FOND_Y1 = 42, 194, 216, 270
FLECHE = (136, 219, 170, 266)           # flèche ↑ à déplacer après le mot
BORD_DROIT, ECART = 190, 22

src = Image.open(SOURCE).convert("RGBA")
fleche = src.crop(FLECHE)
for lg, mot in MOTS.items():
    im = src.copy()
    d = ImageDraw.Draw(im)
    for y in range(FOND_Y0, FOND_Y1):            # le fond a un léger dégradé vertical
        d.line([(FOND_X0, y), (FOND_X1, y)], fill=src.getpixel((36, y)))
    taille = 32
    while True:
        f = ImageFont.truetype(str(POLICE), taille)
        l = d.textlength(mot, font=f)
        if TEXTE_X + l + ECART + fleche.width <= BORD_DROIT or taille <= 20:
            break
        taille -= 1
    d.text((TEXTE_X, LIGNE_BASE), mot, font=f, fill="white", anchor="ls")
    x = round(TEXTE_X + l + ECART)
    im.alpha_composite(fleche, (x - 3, FLECHE[1]))
    im.save(ICI / "assets" / f"telephone-gps-{lg}.png")
    print(lg, mot, taille)
