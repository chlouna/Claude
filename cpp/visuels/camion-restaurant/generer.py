"""Visuel 1080 × 1920 : camion devant un restaurant routier, avec le logo, le picto officiel et le téléphone.

    python3 generer.py && node capturer.mjs

- photo.png : photo générée (Canva). Le picto blanc générique de la photo est recouvert
  par le picto restaurant officiel (cpp/assets/icones/restaurant.png), au même endroit.
- Logo blanc officiel en haut à gauche, sur un léger voile bleu pour rester lisible.
- Téléphone incliné avec la carte des restaurants (capture fournie), entier dans l'image.
"""
from pathlib import Path

ICI = Path(__file__).resolve().parent
L, H = 360, 640  # rendu × 3 = 1080 × 1920

# Picto générique de la photo : centre et largeur, en fractions de l'image
PIN_X, PIN_Y, PIN_L = 0.832, 0.468, 0.285

html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Camion restaurant</title><style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #F5F3F1; }}
.visuel {{ position: relative; width: {L}px; height: {H}px; overflow: hidden;
  background: linear-gradient(180deg, rgba(6,24,102,.7) 0%, rgba(6,24,102,.2) 18%, rgba(6,24,102,0) 30%),
  url('photo.png') center / cover no-repeat; }}
.logo {{ position: absolute; left: {0.09 * L:.0f}px; top: {0.055 * H:.0f}px; width: {0.5 * L:.0f}px; }}
.picto {{ position: absolute; left: {PIN_X * L:.1f}px; top: {PIN_Y * H:.1f}px; width: {PIN_L * L / 0.53:.0f}px;
  transform: translate(-50%, -50%); }}
.tel {{ position: absolute; left: {0.66 * L:.0f}px; top: {0.775 * H:.0f}px; height: {0.38 * H:.0f}px;
  transform: translate(-50%, -50%) rotate(12deg); filter: drop-shadow(0 18px 28px rgba(0,0,0,.45)); }}
</style></head><body>
<section class="visuel" id="camion-restaurant">
  <img class="logo" src="../../assets/logos/truckfly-blanc-rogne.png" alt="Michelin Truckfly">
  <img class="picto" src="../../assets/icones/restaurant.png" alt="">
  <img class="tel" src="../../restaurant/captures/carte-restaurants.png" alt="">
</section></body></html>"""

(ICI / "index.html").write_text(html)
print("index.html écrit")
