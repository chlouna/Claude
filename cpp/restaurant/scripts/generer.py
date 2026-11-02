"""CPP « Restaurant routier » : 5 visuels Google Play (1080 × 1920) avec les captures fournies.

    python3 scripts/generer.py && node scripts/capturer.mjs

Format repris des captures store existantes : verbe d'action en titre, phrase en sous-titre,
téléphone au centre. Décor en panorama continu d'un visuel à l'autre. Titres en casse de phrase (charte).
"""
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

VOLETS = [
    ("trouvez", "Trouvez", "des restaurants routiers sur votre route, partout en Europe !", "carte-restaurants.png", "vague"),
    ("choisissez", "Choisissez", "votre table grâce aux notes, aux avis et au mot du gérant", "fiche-restaurant.png", "cercle"),
    ("roulez", "Roulez", "jusqu'au restaurant avec notre GPS spécifique poids lourd", "itineraire.png", "vague2"),
    ("partagez", "Partagez", "votre avis sur le repas, le parking et les douches pour aider les autres !", "avis.png", "cercle2"),
    ("decouvrez", "Découvrez", "aussi les parkings, stations-service et lavages poids lourd sur votre route !", "carte-tous.png", "vague3"),
]

# Décor en panorama : un seul dessin de 5 × 360 px de large, découpé en 5 visuels.
# Le trait jaune et le grand rond blanc passent d'une image à l'autre quand on fait défiler.
LARGEUR = 360
PANORAMA = (
    '<svg class="deco" viewBox="0 0 1800 640" width="1800" height="640">'
    '<path d="M-20 380 C 120 300, 240 300, 360 360 S 600 440, 720 380 S 960 300, 1080 360 S 1320 440, 1440 380 S 1680 300, 1820 340" '
    'fill="none" stroke="#FFFF1A" stroke-width="14" stroke-linecap="round"/>'
    '<circle cx="720" cy="480" r="290" fill="#FFFFFF"/>'
    "</svg>"
)

CSS = """
@font-face { font-family: "Bib"; src: url("../../assets/fonts/BIB-Bold.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-Bold.otf") format("opentype"); font-weight: 700; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #F5F3F1; padding: 24px; display: flex; gap: 16px; flex-wrap: wrap; font-family: "Inter", sans-serif; }
body.capture { padding: 0; gap: 0; }
.shot { position: relative; width: 360px; height: 640px; overflow: hidden; background: #061866; color: #fff; flex: none; }
.deco { position: absolute; top: 0; width: 1800px; height: 640px; }
.textes { position: absolute; top: 46px; left: 0; right: 0; padding: 0 30px; text-align: center; }
h1 { font-family: "Bib"; font-weight: 700; font-size: 34px; line-height: 1.05; }
p { font-family: "Inter"; font-weight: 700; font-size: 15px; line-height: 1.35; margin-top: 12px; }
.tel { position: absolute; left: 50%; top: 178px; height: 420px; transform: translateX(-50%); filter: drop-shadow(0 18px 28px rgba(0,0,0,.35)); }
"""


def page():
    shots = "".join(
        f'<section class="shot" id="{i + 1:02d}-{cle}"><div style="position:absolute;top:0;left:{-i * LARGEUR}px">{PANORAMA}</div><div class="textes"><h1>{titre}</h1><p>{sous}</p></div>'
        f'<img class="tel" src="../captures/{img}" alt=""></section>'
        for i, (cle, titre, sous, img, deco) in enumerate(VOLETS)
    )
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>CPP Restaurant routier</title><style>{CSS}</style></head><body>{shots}</body></html>'


if __name__ == "__main__":
    (RACINE / "scripts" / "index.html").write_text(page())
    print("scripts/index.html écrit :", len(VOLETS), "visuels")
