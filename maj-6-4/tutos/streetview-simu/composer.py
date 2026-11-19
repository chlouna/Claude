"""Pose l'écran recréé (ecran.html, exporté en ecran.png) dans le cadre du téléphone de la capture Street View.

    node maj-6-4/tutos/streetview-simu/exporter.mjs && python3 maj-6-4/tutos/streetview-simu/composer.py

Écrit ../assets/streetview-simu.png, à la même taille que streetview.png (le cadre est agrandi ×4 pour la netteté).
"""
from pathlib import Path
from PIL import Image

ICI = Path(__file__).resolve().parent
K = 4
cadre = Image.open(ICI.parent / "assets" / "streetview.png").convert("RGBA")
w, h = cadre.size
grand = cadre.resize((w * K, h * K), Image.LANCZOS)
x0, y0, x1, y1 = 21, 16, 287, 591  # zone de l'écran dans la capture
# Masque : l'écran (rectangle arrondi) moins l'encoche, mesurés sur la capture.
from PIL import ImageDraw
masque = Image.new("L", (w * K, h * K), 0)
d = ImageDraw.Draw(masque)
d.rounded_rectangle((x0 * K, 16 * K, x1 * K, y1 * K), radius=30 * K, fill=255)
d.rounded_rectangle((78 * K, 0, 228 * K, 38 * K), radius=10 * K, fill=0)
zone = masque.crop((x0 * K, y0 * K, x1 * K, y1 * K))
for lang in ("fr", "en", "de", "nl", "pl", "it", "es"):
    source = "ecran.png" if lang == "fr" else f"ecran-{lang}.png"
    ecran = Image.open(ICI / source).convert("RGBA").resize(((x1 - x0) * K, (y1 - y0) * K), Image.LANCZOS)
    image = grand.copy()
    image.paste(ecran, (x0 * K, y0 * K), zone)
    sortie = "streetview-simu.png" if lang == "fr" else f"streetview-simu-{lang}.png"
    image.save(ICI.parent / "assets" / sortie)
    print(sortie, image.size)
