"""CPP « Parking poids lourds » : 2 visuels d'accueil + 5 volets, Google Play (1080 × 1920) et App Store (1284 × 2778).

    python3 scripts/generer.py && node scripts/capturer.mjs

Mise en page commune dans cpp/commun/panorama.py : décor et pictos en panorama continu,
titres en casse de phrase (charte), logo blanc officiel sur le visuel d'accueil.
"""
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE.parent / "commun"))
from panorama import ecrire  # noqa: E402

ACCUEIL = {
    "accroche": "Le bon parking poids lourd, partout en Europe",
    "tel_incline": "carte-parkings.png",
    "tel_haut": "fiche-reserver.png",
    "tel_bas": "itineraire.png",
    "picto_grand": "parking", "picto_moyen": "parking", "picto_petit1": "carburant", "picto_petit2": "douche",
    "picto_v2_1": "parking", "picto_v2_2": "parking",
}

VOLETS = [
    ("trouvez", "Trouvez", "un parking poids lourd sur votre route, partout en Europe !", "carte-parkings.png", ""),
    ("verifiez", "Vérifiez", "les services avant de vous arrêter : parking gardé, éclairé, prise frigo…", "services.png", ""),
    ("choisissez", "Choisissez", "votre parking grâce aux avis des autres conducteurs", "avis.png", ""),
    ("reservez", "Réservez", "votre place à l'avance dans certains parkings sécurisés !", "fiche-reserver.png", ""),
    ("roulez", "Roulez", "jusqu'à votre parking avec notre GPS spécifique poids lourd", "itineraire.png", ""),
]

if __name__ == "__main__":
    ecrire(RACINE, "CPP Parking poids lourds", ACCUEIL, VOLETS)
