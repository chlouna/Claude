"""Tutoriels Instagram des nouveautés (likes, photo de profil, langue, alerte péage).

    python3 maj-6-4/tutos/generer.py

Même style que le guide « Crée ton Profil Trucker » (guide-profil/) : intro et fin sur fond
Michelin Blue, étapes sur fond Off White avec pastille numérotée et titre en Bib, taps et zooms
sur les captures de l'app. Écrit une page par vidéo et par format (9x16 : 540 × 960, 16x9 :
960 × 540, rendues ×2). Toutes les animations sont en CSS avec des délais absolus ; rendre.mjs
avance la page image par image et en tire un MP4.

Captures dans assets/ : détourées depuis les images fournies (fond blanc rendu transparent).
"""

from pathlib import Path

from PIL import Image

ICI = Path(__file__).resolve().parent

# Chaque vidéo : durée et scènes. Une scène : (début, fin, fond, numéro, titre, sous-titre, image, actions).
# Actions (positions en % de la capture) : ("tap", x, y, t) · ("zoom", x, y, échelle, t_debut, t_fin)
# · ("langues", t) pour la feuille de choix de langue (recréée).
VIDEOS = {
    "like": dict(duree=15, scenes=[
        (0, 3.6, "bleu", None, "Nouveau&nbsp;: like les contributions", "des autres conducteurs", "like.png", []),
        (3.6, 7.6, "clair", 1, "Ouvre le fil d’activité", None, "like.png", [("tap", 60, 89, 4.7)]),
        (7.6, 11.8, "clair", 2, "Appuie sur «&nbsp;J’aime&nbsp;»", "sous une photo ou un commentaire",
         "like.png", [("zoom", 77, 71, 1.7, 7.9, 11.2), ("tap", 77, 71, 9.0)]),
        (11.8, 15, "bleu", None, "Encourage ceux qui font vivre la communauté&nbsp;!", None, None, []),
    ]),
    "photo-profil": dict(duree=15, scenes=[
        (0, 3.6, "bleu", None, "Nouveau&nbsp;: les photos de profil en grand", None, "photo-profil.png", []),
        (3.6, 8.4, "clair", 1, "Appuie sur une photo de profil", "elle s’affiche en plein écran",
         "photo-profil.png", [("tap", 26, 22, 4.6), ("zoom", 49, 51, 1.4, 5.6, 7.9)]),
        (8.4, 11.8, "clair", 2, "Ajoute la tienne&nbsp;!", "c’est elle que les autres verront en grand",
         "profil-charlie.png", [("tap", 26, 22, 9.5)]),
        (11.8, 15, "bleu", None, "Fais-toi reconnaître sur les aires&nbsp;!", None, None, []),
    ]),
    "langue": dict(duree=16, scenes=[
        (0, 3.3, "bleu", None, "Nouveau&nbsp;: l’appli dans ta langue", None, "parametres.png", []),
        (3.3, 6.3, "clair", 1, "Ouvre les Paramètres", None, "profil-charlie.png", [("tap", 85, 11, 4.4)]),
        (6.3, 9.3, "clair", 2, "Appuie sur «&nbsp;Langue de l’application&nbsp;»", None, "parametres.png", [("tap", 32, 23, 7.4)]),
        (9.3, 12.3, "clair", 3, "Choisis ta langue", None, "parametres.png", [("langues", 9.5)]),
        (12.3, 16, "bleu", None, "Sans toucher aux réglages de ton téléphone&nbsp;!", None, None, []),
    ]),
    "peage": dict(duree=15, scenes=[
        (0, 3.6, "bleu", None, "Nouveau dans le GPS Premium&nbsp;: l’alerte péage", None, "peage.png", []),
        (3.6, 7, "clair", 1, "Lance ta navigation", None, "peage.png", []),
        (7, 11.4, "clair", 2, "Une alerte avant le péage", "et tu le vois sur la carte",
         "peage.png", [("zoom", 50, 84, 1.7, 7.3, 10.9)]),
        (11.4, 15, "bleu", None, "Anticipe&nbsp;: bonne voie, badge prêt&nbsp;!", None, None, []),
    ]),
}

LANGUES = ["Français", "English", "Deutsch", "Nederlands", "Polski", "Italiano", "Español"]
CHOIX = 2  # Deutsch


def anim(*parts):
    """style="animation: ..." à partir de (nom, durée, délai[, remplissage])."""
    return "animation: " + ", ".join(
        f"{n} {d}s {'cubic-bezier(0.2, 0.9, 0.3, 1.1)' if n in ('monte', 'pop', 'feuille') else 'ease-in-out'} {t}s {r[0] if r else 'both'}"
        for n, d, t, *r in parts
    )


def actions_html(actions):
    """Taps et feuille de langues, posés sur la capture (ils suivent le zoom)."""
    html = ""
    for a in actions:
        if a[0] == "tap":
            _, x, y, t = a
            html += f'<i class="tap" style="left:{x}%; top:{y}%; {anim(("tape", 0.9, t))}"></i>'
        elif a[0] == "langues":
            t = a[1]
            lignes = ""
            for i, nom in enumerate(LANGUES):
                coche = ""
                if i == 0:
                    coche = f'<b class="coche" style="{anim(("efface", 0.2, t + 1.5, "forwards"))}">✓</b>'
                elif i == CHOIX:
                    coche = f'<b class="coche" style="{anim(("pop", 0.3, t + 1.5))}">✓</b>'
                lignes += f'<li><span>{nom}</span>{coche}</li>'
            y_choix = 49.5 + 7.2 * (CHOIX + 0.5)  # centre de la ligne choisie, en % de la hauteur
            html += f"""<div class="voile-ecran" style="{anim(("apparait", 0.3, t))}"></div>
        <div class="feuille" style="{anim(("feuille", 0.45, t))}">
          <p class="f-titre">Langue de l’application</p><ul>{lignes}</ul>
        </div>
        <i class="tap" style="left:40%; top:{y_choix}%; {anim(("tape", 0.9, t + 1.0))}"></i>"""
    return html


def scene_html(debut, fin, fond, num, titre, sous, image, actions, derniere):
    # Chaque scène apparaît par-dessus la précédente (pas de fondu sortant, qui laisserait voir le fond).
    style = anim(("apparait", 0.25, debut)) if debut else "opacity: 1;"
    pastille = f'<span class="pastille" style="{anim(("pop", 0.4, debut + 0.1))}">{num}</span>' if num else ""
    sous_html = f'<p class="sous" style="{anim(("monte", 0.5, debut + 0.35))}">{sous}</p>' if sous else ""
    tel = ""
    if image:
        zooms = [a for a in actions if a[0] == "zoom"]
        z_style, origine = "", "50% 50%"
        if zooms:
            _, x, y, s, t1, t2 = zooms[0]
            origine = f"{x}% {y}%"
            z_style = f"--s:{s}; " + anim(("zoome", 0.6, t1, "forwards"), ("dezoome", 0.6, t2, "forwards"))
        l, h = Image.open(ICI / "assets" / image).size
        tel = f"""<div class="tel" style="aspect-ratio: {l} / {h}; {anim(("monte", 0.6, debut + 0.15))}">
        <div class="tel-zoom" style="transform-origin:{origine}; {z_style}">
          <img src="assets/{image}" alt="" />{actions_html(actions)}
        </div>
      </div>"""
    sans_tel = "" if image else " seul"
    return f"""  <section class="scene {fond}{sans_tel}" style="{style}">
    <div class="texte">
      {pastille}<h1 style="{anim(("monte", 0.5, debut + 0.2))}">{titre}</h1>
      {sous_html}
    </div>
    {tel}
  </section>
"""


CSS_COMMUN = """
@font-face { font-family: "Bib"; src: url("../../ma-video/assets/fonts/BIB-Bold.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Inter"; src: url("../../ma-video/assets/fonts/Inter-Regular.otf") format("opentype"); font-weight: 400; }
@font-face { font-family: "Inter"; src: url("../../ma-video/assets/fonts/Inter-SemiBold.otf") format("opentype"); font-weight: 600; }
@font-face { font-family: "Inter"; src: url("../../ma-video/assets/fonts/Inter-Bold.otf") format("opentype"); font-weight: 700; }
:root { --bleu: #061866; --clair: #F5F3F1; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: var(--w); height: var(--h); overflow: hidden; background: var(--bleu); }
.video { position: relative; width: var(--w); height: var(--h); overflow: hidden; font-family: "Inter", sans-serif; }
.scene { position: absolute; inset: 0; opacity: 0; }
.scene.bleu { background: var(--bleu); color: #fff; }
.scene.clair { background: var(--clair); color: var(--bleu); }
.texte { position: absolute; display: flex; flex-direction: column; }
.pastille { width: var(--pastille); height: var(--pastille); border-radius: 50%; background: var(--bleu); color: #fff;
  display: flex; align-items: center; justify-content: center; font-family: "Bib", sans-serif; font-weight: 700; font-size: calc(var(--pastille) * 0.56); }
h1 { font-family: "Bib", sans-serif; font-weight: 700; font-size: var(--titre); line-height: 1.12; text-wrap: balance; }
.sous { font-size: var(--sous); line-height: 1.3; text-wrap: balance; opacity: 0.9; }
.tel { position: absolute; overflow: hidden; border-radius: 15% / 7.5%; }
.tel-zoom { position: relative; width: 100%; height: 100%; }
.tel img { display: block; width: 100%; height: 100%; filter: drop-shadow(0 14px 28px rgba(0, 0, 0, 0.28)); }
.scene.bleu .tel img { filter: drop-shadow(0 14px 32px rgba(0, 0, 0, 0.5)); }
.tap { position: absolute; width: 13%; aspect-ratio: 1; margin: -6.5% 0 0 -6.5%; border-radius: 50%;
  border: 3px solid var(--bleu); background: rgba(255, 255, 255, 0.35); box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.8); }
/* Feuille de choix de langue (recréée, au style de l'app) */
.tel-zoom { container-type: size; }
.voile-ecran { position: absolute; left: 4.5%; right: 4.5%; top: 2.5%; bottom: 2.5%; border-radius: 9% / 4.5%; background: rgba(0, 0, 0, 0.35); }
.feuille { position: absolute; left: 4.5%; right: 4.5%; bottom: 2.5%; height: 55%; background: #fff; border-radius: 6cqw 6cqw 9% 9% / 6cqw 6cqw 4.5% 4.5%;
  padding: 5cqw 6cqw; color: #000; font-family: "Inter", sans-serif; }
.f-titre { font-weight: 700; font-size: 5cqw; color: var(--bleu); text-align: center; margin-bottom: 2cqw; }
.feuille ul { list-style: none; }
.feuille li { display: flex; justify-content: space-between; align-items: center; height: 7.2cqh; border-bottom: 1px solid #e6e6ea; font-size: 4.4cqw; font-weight: 600; }
.coche { color: var(--bleu); font-size: 5cqw; }


@keyframes apparait { from { opacity: 0; } to { opacity: 1; } }
@keyframes disparait { from { opacity: 1; } to { opacity: 0; } }
@keyframes efface { to { opacity: 0; } }
@keyframes monte { from { opacity: 0; transform: translateY(30px); } }
@keyframes pop { from { opacity: 0; transform: scale(0.3); } }
@keyframes feuille { from { transform: translateY(105%); } }
@keyframes zoome { from { transform: scale(1); } to { transform: scale(var(--s)); } }
@keyframes dezoome { from { transform: scale(var(--s)); } to { transform: scale(1); } }
@keyframes tape {
  0% { opacity: 0; transform: scale(1.7); }
  30% { opacity: 1; transform: scale(1); }
  55% { opacity: 1; transform: scale(0.8); }
  100% { opacity: 0; transform: scale(1); }
}
"""

# Fins sans téléphone : texte centré (après les règles des formats, pour les remplacer).
CSS_SEUL = """
.scene.seul .texte { inset: 0; width: auto; align-items: center; justify-content: center; text-align: center; padding: 0 var(--marge); }
.scene.seul h1 { font-size: var(--titre-fin); }
"""

# Mise en page par format. 9x16 : texte en haut, téléphone en dessous. 16x9 : texte à gauche, téléphone à droite.
FORMATS = {
    "9x16": dict(w=540, h=960, css="""
:root { --w: 540px; --h: 960px; --titre: 42px; --titre-fin: 50px; --sous: 24px; --pastille: 50px; --marge: 50px; }
.texte { left: 36px; right: 36px; top: 70px; align-items: center; text-align: center; gap: 12px; }
.tel { left: 50%; top: 318px; height: 590px; translate: -50% 0; }
.scene.bleu .tel { top: 300px; }
"""),
    "16x9": dict(w=960, h=540, css="""
:root { --w: 960px; --h: 540px; --titre: 40px; --titre-fin: 50px; --sous: 22px; --pastille: 46px; --marge: 120px; }
.texte { left: 80px; width: 470px; top: 0; bottom: 0; justify-content: center; gap: 16px; }
.tel { left: 600px; top: 40px; height: 460px; }
"""),
}


def page(nom, video, fmt):
    f = FORMATS[fmt]
    scenes = video["scenes"]
    corps = "".join(scene_html(*s, derniere=(i == len(scenes) - 1)) for i, s in enumerate(scenes))
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<title>Tutoriel {nom} ({fmt})</title>
<style>{CSS_COMMUN}{f["css"]}{CSS_SEUL}</style>
</head>
<body data-duree="{video["duree"]}" data-w="{f["w"]}" data-h="{f["h"]}">
<main class="video">
{corps}</main>
</body>
</html>
"""


for nom, video in VIDEOS.items():
    for fmt in FORMATS:
        (ICI / f"{nom}-{fmt}.html").write_text(page(nom, video, fmt))
print("pages :", ", ".join(f"{n}-{f}" for n in VIDEOS for f in FORMATS))
