"""Remplace le visuel 01 (accueil) par un visuel d'accueil fini fourni en 1080 × 1920.

    python3 commun/accueil_fini.py <dossier CPP> <visuel 1080x1920> [bord gauche du logo en px]

À lancer après scripts/capturer.mjs.
- Google Play (1080 × 1920) : le visuel tel quel.
- App Store (1284 × 2778) : le visuel agrandi et recadré pour garder le logo à gauche et l'accroche
  à droite avec une marge de 40 px ; la hauteur manquante est complétée en haut par le ciel étiré et flouté.
"""
import sys
from pathlib import Path

from PIL import Image, ImageFilter

dossier, source = Path(sys.argv[1]), Path(sys.argv[2])
nom = dossier.name
im = Image.open(source).convert("RGB")
assert im.size == (1080, 1920), im.size

# Google Play
im.save(dossier / "png" / "google-play" / f"{nom}-01-accueil.png")

# App Store
L, H, marge = 1284, 2778, 40
gauche, droite = (int(sys.argv[3]) if len(sys.argv) > 3 else 70), 997  # logo … bord droit de l'accroche
s = min(1.36, (L - 2 * marge) / (droite - gauche))
grand = im.resize((round(1080 * s), round(1920 * s)), Image.LANCZOS)
decalage = round((gauche + droite) / 2 * s - L / 2)
grand = grand.crop((decalage, 0, decalage + L, grand.height))
manque = H - grand.height
ciel = grand.crop((0, 0, L, 40)).resize((L, manque + 40), Image.BICUBIC).filter(ImageFilter.GaussianBlur(12))
apple = Image.new("RGB", (L, H))
apple.paste(ciel, (0, 0))
# fondu entre le ciel ajouté et l'image
fondu = Image.linear_gradient("L").resize((L, 80))
apple.paste(grand, (0, manque))
apple.paste(ciel.crop((0, manque, L, manque + 40)).resize((L, 80)), (0, manque), Image.eval(fondu, lambda v: 255 - v))
apple.save(dossier / "png" / "app-store" / f"{nom}-01-accueil.png")
print(f"{nom} : accueil remplacé (Google Play et App Store)")
