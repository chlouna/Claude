"""CPP « Restaurant routier » : 5 visuels Google Play (1080 × 1920) avec les captures fournies.

    python3 scripts/generer.py && node scripts/capturer.mjs

Format repris des captures store existantes : verbe d'action en titre, phrase en sous-titre,
téléphone au centre, courbe jaune ou grand cercle blanc. Titres en casse de phrase (charte).
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

DECOR = {
    "vague": '<svg class="deco" viewBox="0 0 360 640" preserveAspectRatio="none"><path d="M-20 360 Q90 300 180 350 T380 300" fill="none" stroke="#FFFF1A" stroke-width="14" stroke-linecap="round"/></svg>',
    "vague2": '<svg class="deco" viewBox="0 0 360 640" preserveAspectRatio="none"><path d="M-20 300 Q120 420 200 360 T380 330" fill="none" stroke="#FFFF1A" stroke-width="14" stroke-linecap="round"/></svg>',
    "vague3": '<svg class="deco" viewBox="0 0 360 640" preserveAspectRatio="none"><path d="M-20 420 Q100 330 190 380 T380 340" fill="none" stroke="#FFFF1A" stroke-width="14" stroke-linecap="round"/></svg>',
    "cercle": '<svg class="deco" viewBox="0 0 360 640"><circle cx="330" cy="430" r="230" fill="#FFFFFF"/></svg>',
    "cercle2": '<svg class="deco" viewBox="0 0 360 640"><circle cx="20" cy="440" r="230" fill="#FFFFFF"/></svg>',
}

CSS = """
@font-face { font-family: "Bib"; src: url("../../assets/fonts/BIB-Bold.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Inter"; src: url("../../assets/fonts/Inter-Bold.otf") format("opentype"); font-weight: 700; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #F5F3F1; padding: 24px; display: flex; gap: 16px; flex-wrap: wrap; font-family: "Inter", sans-serif; }
body.capture { padding: 0; gap: 0; }
.shot { position: relative; width: 360px; height: 640px; overflow: hidden; background: #061866; color: #fff; flex: none; }
.deco { position: absolute; inset: 0; width: 100%; height: 100%; }
.textes { position: absolute; top: 46px; left: 0; right: 0; padding: 0 30px; text-align: center; }
h1 { font-family: "Bib"; font-weight: 700; font-size: 34px; line-height: 1.05; }
p { font-family: "Inter"; font-weight: 700; font-size: 15px; line-height: 1.35; margin-top: 12px; }
.tel { position: absolute; left: 50%; top: 178px; height: 420px; transform: translateX(-50%); filter: drop-shadow(0 18px 28px rgba(0,0,0,.35)); }
"""


def page():
    shots = "".join(
        f'<section class="shot" id="{i + 1:02d}-{cle}">{DECOR[deco]}<div class="textes"><h1>{titre}</h1><p>{sous}</p></div>'
        f'<img class="tel" src="../captures/{img}" alt=""></section>'
        for i, (cle, titre, sous, img, deco) in enumerate(VOLETS)
    )
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>CPP Restaurant routier</title><style>{CSS}</style></head><body>{shots}</body></html>'


if __name__ == "__main__":
    (RACINE / "scripts" / "index.html").write_text(page())
    print("scripts/index.html écrit :", len(VOLETS), "visuels")
