# Téléphones Android pour Google Play

Google Play : pas d'iPhone dans les visuels. Étapes, après `scripts/generer.py` et `scripts/capturer.mjs` :

    python3 commun/android.py restaurant      # captures/ -> captures-android/ (cadre Android)
    python3 commun/android.py parking
    python3 commun/accueil_android.py restaurant assets/photos/accueil-fini-restaurant.webp carte-restaurants.png 767 1521 640 11.0
    python3 commun/accueil_android.py parking assets/photos/accueil-fini-parking.webp carte-parkings.png 545 1414 790 6.4 260 990 505 1062

Les volets Google Play utilisent captures-android/ (réglé dans commun/panorama.py).
