"""Transforme les captures (cadre iPhone) en téléphones Android génériques pour Google Play.

    python3 commun/android.py <dossier CPP>

Pour chaque image de <CPP>/captures/, écrit la même image dans <CPP>/captures-android/ :
- on garde l'écran de l'app, sans le cadre iPhone (encoche, boutons latéraux) ;
- la barre d'état iOS est remplacée par une barre d'état Android (heure à gauche, icônes à droite,
  petite caméra ronde au centre) ;
- la barre d'accueil iOS en bas est effacée ;
- l'écran est posé dans un cadre noir à bords fins et coins arrondis, sans marque.
Même taille que la capture d'origine, pour ne rien changer à la mise en page.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

CPP = Path(__file__).resolve().parent.parent
POLICE = CPP / "assets" / "fonts" / "Inter-SemiBold.otf"


def sombre(px):
    # cadre iPhone : gris neutres (noir ou gris 85), jamais le bleu de l'en-tête de l'app
    c = [int(v) for v in px[:3]]
    return px[3] > 200 and max(c) < 100 and max(c) - min(c) < 14


def bord_ecran(a, y=None, x=None):
    """Premier pixel de l'écran (ni transparent, ni cadre sombre) en partant du bord."""
    h, w = a.shape[:2]
    if y is not None:
        for xx in range(w // 3):
            px = a[y, xx]
            if px[3] > 200 and not sombre(px):
                return xx
    else:
        for yy in range(h // 4):
            px = a[yy, x]
            if px[3] > 200 and not sombre(px):
                return yy
    raise ValueError("bord de l'écran introuvable")


def couleur(img, x, y):
    return tuple(int(v) for v in img.getpixel((x, y))[:3])


def convertir(chemin, sortie):
    im = Image.open(chemin).convert("RGBA")
    a = np.asarray(im)
    h, w = a.shape[:2]
    def essais(f, valeurs):
        trouves = []
        for v in valeurs:
            try:
                trouves.append(f(v))
            except ValueError:
                pass
        return sorted(trouves)[len(trouves) // 2]  # médiane : ignore les lignes où l'écran est sombre

    gx = essais(lambda y: bord_ecran(a, y=y), [round(h * k) for k in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)])
    gy = essais(lambda x: bord_ecran(a, x=x), [round(w * k) for k in (0.12, 0.2, 0.8, 0.88)])
    marge = 2
    ecran = im.crop((gx + marge, gy + marge, w - gx - marge, h - gy - marge)).convert("RGB")
    ew, eh = ecran.size

    # Barre d'état : hauteur = bas de l'encoche iOS (colonne centrale encore noire)
    yb = 0
    while yb < eh // 6 and max(ecran.getpixel((ew // 2, yb))) < 30:
        yb += 1
    hauteur_barre = max(yb + 3, round(eh * 0.05))
    fond = couleur(ecran, 4, hauteur_barre + 3)
    clair = sum(fond) / 3 > 140
    encre = (30, 30, 30) if clair else (255, 255, 255)
    d = ImageDraw.Draw(ecran)
    d.rectangle((0, 0, ew, hauteur_barre), fill=fond)
    taille = max(8, round(eh * 0.019))
    police = ImageFont.truetype(str(POLICE), taille)
    yt = (hauteur_barre - taille) // 2
    d.text((round(ew * 0.06), yt), "16:46", font=police, fill=encre)
    # icônes Android simples à droite : réseau, wifi, batterie
    xr = ew - round(ew * 0.06)
    hb, lb = taille * 0.95, taille * 0.5
    d.rounded_rectangle((xr - lb, yt + (taille - hb) / 2 + 1, xr, yt + (taille + hb) / 2 + 1), radius=1.5, fill=encre)
    x = xr - lb - taille * 0.55
    for i in range(4):  # réseau
        hh = taille * (0.3 + 0.2 * i)
        d.rectangle((x - taille * 1.2 + i * taille * 0.3, yt + taille + 1 - hh, x - taille * 1.2 + i * taille * 0.3 + taille * 0.18, yt + taille + 1), fill=encre)
    xw = x - taille * 1.55
    d.pieslice((xw - taille * 0.6, yt + 1, xw + taille * 0.6, yt + taille * 1.2 + 1), 225, 315, fill=encre)
    # caméra ronde au centre
    r = max(3, round(ew * 0.018))
    cy = hauteur_barre // 2 + 1
    d.ellipse((ew / 2 - r, cy - r, ew / 2 + r, cy + r), fill=(10, 10, 10))

    # Barre d'accueil iOS en bas : on la recouvre avec la couleur de la barre d'onglets
    bas = round(eh * 0.03)
    d.rectangle((ew * 0.25, eh - bas, ew * 0.75, eh), fill=couleur(ecran, ew // 2, eh - bas - 3))

    # Cadre Android : bords fins réguliers, coins arrondis, un bouton à droite
    cadre = round(w * 0.028)
    W, H = w, h
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(out)
    rayon = round(w * 0.11)
    dc.rounded_rectangle((W - 4, round(H * 0.24), W - 1, round(H * 0.33)), radius=2, fill=(40, 40, 44, 255))  # bouton
    dc.rounded_rectangle((0, 0, W - 4, H - 1), radius=rayon, fill=(18, 18, 20, 255))
    dc.rounded_rectangle((1, 1, W - 5, H - 2), radius=rayon - 1, outline=(70, 70, 76, 255), width=1)
    zone = (cadre, cadre, W - 4 - cadre, H - 1 - cadre)
    ecran = ecran.resize((zone[2] - zone[0], zone[3] - zone[1]), Image.LANCZOS)
    masque = Image.new("L", ecran.size, 0)
    ImageDraw.Draw(masque).rounded_rectangle((0, 0, ecran.size[0] - 1, ecran.size[1] - 1), radius=rayon - cadre, fill=255)
    out.paste(ecran, zone[:2], masque)
    out.save(sortie)


if __name__ == "__main__":
    dossier = Path(sys.argv[1])
    cible = dossier / "captures-android"
    cible.mkdir(exist_ok=True)
    for f in sorted((dossier / "captures").glob("*.png")):
        convertir(f, cible / f.name)
        print("android :", f.name)
