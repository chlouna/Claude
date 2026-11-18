"""Carrousel Instagram / LinkedIn 4:5 des nouveautés GPS de la 6.5 (6 visuels).

    python3 maj-6-5/carrousel/generer.py && node maj-6-5/carrousel/rendre.mjs

Maquette en 360 × 450 px (échelle de la charte, structure 4:5), exportée en 1080 × 1350.
Captures : celles de la newsletter 6.5, détourées dans maj-6-4/tutos/assets (lien « captures »).
"""

from pathlib import Path

ICI = Path(__file__).resolve().parent

# (surtitre, titre, texte, captures)
VISUELS = [
    ("Mise à jour 6.5", "Ton GPS a 4&nbsp;nouveautés", "Fais glisser pour les découvrir →", ["nav-rue.png"]),
    ("Nouveauté 1/4", "Un itinéraire recalculé plus vite",
     "Une sortie ratée&nbsp;? Le GPS recalcule ton itinéraire plus vite, automatiquement.", ["nav-rue.png"]),
    ("Nouveauté 2/4", "Vois ta destination avant d’y arriver",
     "Appuie sur le drapeau d’arrivée, puis sur «&nbsp;Voir dans Street View&nbsp;».", ["streetview.png"]),
    ("Nouveauté 3/4", "Le nom de ta rue toujours affiché",
     "En bas de l’écran, pendant ta navigation. Pratique pour donner ta position.", ["nav-rue.png"]),
    ("Nouveauté 4/4", "Choisis tes alertes",
     "Paramètres → «&nbsp;Alertes en navigation&nbsp;» → coche les alertes à garder.", ["parametres-alertes.png", "alertes-navigation.png"]),
    ("Mise à jour 6.5", "Mets ton appli à jour&nbsp;!", "Et roule plus serein avec Michelin Truckfly.", []),
]

CSS = """
@font-face { font-family: "Bib"; src: url("../../ma-video/assets/fonts/BIB-Bold.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Inter"; src: url("../../ma-video/assets/fonts/Inter-Regular.otf") format("opentype"); font-weight: 400; }
@font-face { font-family: "Inter"; src: url("../../ma-video/assets/fonts/Inter-SemiBold.otf") format("opentype"); font-weight: 600; }
:root { --bleu: #061866; --jaune: #FFFF1A; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 360px; height: 450px; overflow: hidden; background: var(--bleu); }
.v { position: relative; width: 360px; height: 450px; overflow: hidden; color: #fff; font-family: "Inter", sans-serif;
  background: radial-gradient(120% 80% at 70% 10%, #10287f 0%, var(--bleu) 55%, #000e38 100%); }
.v > * { position: absolute; }
.structure { inset: 0; width: 100%; height: 100%; }
.surtitre { right: 48px; top: 54px; font-weight: 600; font-size: 11px; color: var(--jaune); }
.texte { left: 46px; right: 46px; top: 96px; }
h1 { font-family: "Bib", sans-serif; font-weight: 700; font-size: 24px; line-height: 27px; text-wrap: balance; }
p { margin-top: 8px; font-size: 11.5px; line-height: 15.5px; color: rgba(255,255,255,0.9); text-wrap: balance; }
/* Téléphone entier en bas, pour que l'élément montré (bouton, nom de rue) reste visible */
.tels { left: 0; right: 0; bottom: 22px; display: flex; gap: 12px; justify-content: center; }
.tels img { height: 236px; width: auto; filter: drop-shadow(0 10px 22px rgba(0,0,0,0.45)); }
/* Couverture et fin : texte centré */
.seul .texte { top: 150px; text-align: center; }
.seul h1 { font-size: 34px; line-height: 38px; }
.seul p { font-size: 14px; line-height: 19px; margin-top: 14px; }
.couv .texte { text-align: left; }
.couv h1 { font-size: 30px; line-height: 33px; }
.cta { margin-top: 26px; display: inline-flex; padding: 0 18px; height: 40px; align-items: center; border-radius: 10px;
  background: var(--jaune); color: #000; font-weight: 700; font-size: 13px; }
"""


def page(i, surtitre, titre, texte, captures):
    if not captures:
        classe, contenu = "seul", '<a class="cta">Mettre à jour Michelin Truckfly</a>'
    else:
        classe = "couv" if i == 0 else ""
        contenu = ""
    tels = ""
    if captures:
        imgs = "".join(f'<img src="captures/{c}" alt="" />' for c in captures)
        tels = f'<div class="tels{" deux" if len(captures) > 1 else ""}">{imgs}</div>'
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="UTF-8" /><title>Carrousel 6.5 ({i + 1})</title><style>{CSS}</style></head>
<body><main class="v {classe}">
  <img class="structure" src="structure.png" alt="" />
  <p class="surtitre">{surtitre}</p>
  <div class="texte"><h1>{titre}</h1><p>{texte}</p>{contenu}</div>
  {tels}
</main></body></html>
"""


for i, v in enumerate(VISUELS):
    (ICI / f"visuel-{i + 1}.html").write_text(page(i, *v))
print(len(VISUELS), "visuels")
