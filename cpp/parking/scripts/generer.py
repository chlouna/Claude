"""CPP « Parking poids lourds » : 5 visuels Google Play (1080 × 1920) et App Store (1284 × 2778) avec les captures fournies.

    python3 scripts/generer.py && node scripts/capturer.mjs

Format repris des captures store existantes : verbe d'action en titre, phrase en sous-titre,
téléphone au centre. Décor en panorama continu d'un visuel à l'autre. Titres en casse de phrase (charte).
"""
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

VOLETS = [
    ("trouvez", "Trouvez", "un parking poids lourd sur votre route, partout en Europe !", "carte-parkings.png", ""),
    ("verifiez", "Vérifiez", "les services avant de vous arrêter : parking gardé, éclairé, prise frigo…", "services.png", ""),
    ("choisissez", "Choisissez", "votre parking grâce aux avis des autres conducteurs", "avis.png", ""),
    ("reservez", "Réservez", "votre place à l'avance dans certains parkings sécurisés !", "fiche-reserver.png", ""),
    ("roulez", "Roulez", "jusqu'à votre parking avec notre GPS spécifique poids lourd", "itineraire.png", ""),
]

# Décor en panorama : un seul dessin large de 5 visuels, découpé en 5.
# Le trait jaune et le grand rond blanc passent d'une image à l'autre quand on fait défiler.
FORMATS = {
    # nom : (largeur, hauteur, trait jaune, rond (cx, cy, r), réglages CSS)
    "google-play": (360, 640, "M-20 380 C 120 300, 240 300, 360 360 S 600 440, 720 380 S 960 300, 1080 360 S 1320 440, 1440 380 S 1680 300, 1820 340",
                    (720, 370, 215), "--haut-txt: 46px; --t: 34px; --st: 15px; --tel-haut: 178px; --tel-h: 420px;"),
    "app-store": (428, 926, "M-24 540 C 143 440, 285 440, 428 510 S 713 600, 856 540 S 1141 440, 1284 510 S 1569 600, 1712 540 S 1997 440, 2164 480",
                  (856, 545, 290), "--haut-txt: 78px; --t: 42px; --st: 18px; --tel-haut: 258px; --tel-h: 620px;"),
}

CSS = """
@font-face { font-family: "Bib"; src: url("../../assets/fonts/BIB-Bold.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-Bold.otf") format("opentype"); font-weight: 700; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #F5F3F1; padding: 24px; display: flex; gap: 16px; flex-wrap: wrap; font-family: "Inter", sans-serif; }
body.capture { padding: 0; gap: 0; }
.shot { position: relative; overflow: hidden; background: #061866; color: #fff; flex: none; }
.pano { position: absolute; top: 0; }
.textes { position: absolute; top: var(--haut-txt); left: 0; right: 0; padding: 0 30px; text-align: center; }
h1 { font-family: "Bib"; font-weight: 700; font-size: var(--t); line-height: 1.05; }
p { font-family: "Inter"; font-weight: 700; font-size: var(--st); line-height: 1.35; margin-top: 12px; }
.tel { position: absolute; left: 50%; top: var(--tel-haut); height: var(--tel-h); transform: translateX(-50%); filter: drop-shadow(0 18px 28px rgba(0,0,0,.35)); }
"""


def page(fmt):
    l, h, trait, (cx, cy, r), reglages = FORMATS[fmt]
    n = len(VOLETS)
    pano = (
        f'<svg viewBox="0 0 {l * n} {h}" width="{l * n}" height="{h}">'
        f'<path d="{trait}" fill="none" stroke="#FFFF1A" stroke-width="{round(14 * l / 360)}" stroke-linecap="round"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF"/></svg>'
    )
    shots = "".join(
        f'<section class="shot" id="{i + 1:02d}-{cle}" style="width:{l}px;height:{h}px;{reglages}">'
        f'<div class="pano" style="left:{-i * l}px">{pano}</div><div class="textes"><h1>{titre}</h1><p>{sous}</p></div>'
        f'<img class="tel" src="../captures/{img}" alt=""></section>'
        for i, (cle, titre, sous, img, _) in enumerate(VOLETS)
    )
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>CPP Parking poids lourds</title><style>{CSS}</style></head><body>{shots}</body></html>'


if __name__ == "__main__":
    for fmt in FORMATS:
        (RACINE / "scripts" / f"index-{fmt}.html").write_text(page(fmt))
    print("scripts/index-*.html écrits :", len(VOLETS), "visuels x 2 formats")
