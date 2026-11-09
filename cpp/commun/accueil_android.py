"""Version Google Play d'un visuel d'accueil fini : l'iPhone de l'image est recouvert par un téléphone Android.

    python3 commun/accueil_android.py <dossier CPP> <visuel 1080x1920> <capture> <cx> <cy> <hauteur> <angle> [x0 y0 x1 y1 de la partie du picto qui chevauche le téléphone]

- cx, cy, hauteur, angle : centre, hauteur et inclinaison (degrés, sens horaire) de l'iPhone dans l'image.
- zone (facultatif) : partie du picto de l'image qui chevauche le téléphone ; ses pixels d'origine
  sont remis par-dessus, pour que le picto reste devant.
Écrit <CPP>/png/google-play/<CPP>-01-accueil.png.
"""
import sys
from pathlib import Path

from PIL import Image, ImageFilter

CPP = Path(__file__).resolve().parent.parent
dossier, source, capture = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
cx, cy, hauteur, angle = map(float, sys.argv[4:8])
nom = dossier.name

fond = Image.open(source).convert("RGBA")
tel = Image.open(dossier / "captures-android" / capture).convert("RGBA")
tel = tel.resize((round(tel.width * hauteur / tel.height), round(hauteur)), Image.LANCZOS)
tourne = tel.rotate(-angle, resample=Image.BICUBIC, expand=True)

# ombre portée douce sous le téléphone
ombre = Image.new("RGBA", tourne.size, (0, 0, 0, 0))
ombre.putalpha(tourne.getchannel("A").point(lambda v: v * 0.45))
ombre = ombre.filter(ImageFilter.GaussianBlur(18))
x, y = round(cx - tourne.width / 2), round(cy - tourne.height / 2)
fond.alpha_composite(ombre, (x, y + 14))
fond.alpha_composite(tourne, (x, y))

if len(sys.argv) > 8:
    # Le picto de l'image passe devant le téléphone : on reprend ses pixels d'origine
    # (blanc et bleu du picto) dans la zone donnée (x0 y0 x1 y1), par-dessus le téléphone.
    import numpy as np

    x0, y0, x1, y1 = map(int, sys.argv[8:12])
    orig = np.asarray(Image.open(source).convert("RGB")).astype(int)
    z = orig[y0:y1, x0:x1]
    r, g, b = z[..., 0], z[..., 1], z[..., 2]
    picto = (z.min(axis=2) > 185) | ((b > 190) & (b - r > 60) & (r > 70))
    m = Image.fromarray((picto * 255).astype("uint8")).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1))
    morceau = Image.open(source).convert("RGBA").crop((x0, y0, x1, y1))
    morceau.putalpha(m)
    fond.alpha_composite(morceau, (x0, y0))

fond.convert("RGB").save(dossier / "png" / "google-play" / f"{nom}-01-accueil.png")
print(nom, ": accueil Google Play avec téléphone Android")
