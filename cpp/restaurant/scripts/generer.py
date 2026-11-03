"""CPP « Restaurant routier » : 1 visuel d'accueil + 5 volets, Google Play (1080 × 1920) et App Store (1284 × 2778).

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
    "accroche": "Les meilleurs restaurants routiers sur votre route",
    "tel_incline": "carte-restaurants.png",
    "tel_haut": "fiche-restaurant.png",
    "tel_bas": "itineraire.png",
    "picto_grand": "resto", "picto_moyen": "resto", "picto_petit1": "carburant", "picto_petit2": "douche",
    "picto_v2_1": "resto", "picto_v2_2": "resto",
}

VOLETS = [
    ("trouvez", "Trouvez", "des restaurants routiers sur votre route, partout en Europe !", "carte-restaurants.png", "vague"),
    ("choisissez", "Choisissez", "votre table grâce aux notes, aux avis et au mot du gérant", "fiche-restaurant.png", "cercle"),
    ("roulez", "Roulez", "jusqu'au restaurant avec notre GPS spécifique poids lourd", "itineraire.png", "vague2"),
    ("partagez", "Partagez", "votre avis sur le repas, le parking et les douches pour aider les autres !", "avis.png", "cercle2"),
    ("decouvrez", "Découvrez", "aussi les parkings, stations-service et lavages poids lourd sur votre route !", "carte-tous.png", "vague3"),
]

if __name__ == "__main__":
    ecrire(RACINE, "CPP Restaurant routier", ACCUEIL, VOLETS)
