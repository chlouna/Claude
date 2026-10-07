"""Génère la vidéo « Guide : crée ton Profil Trucker » (25 s) en deux formats.

    python3 scripts/generer.py

Écrit index.html (16:9, 1920 × 1080) et compositions/vertical.html (9:16, 1080 × 1920).
Le téléphone et ses écrans (profil, modification, camion) sont recréés en HTML au style de
l'app : bandeau Michelin Blue, Inter, cartes blanches. Les positions dans le téléphone sont
en % de l'écran (cqw en largeur, cqh en hauteur).
"""

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DUREE = 25

# --- Illustrations (pas de vraies photos) ---

PORTRAIT = """<svg class="illu" data-layout-allow-overflow viewBox="0 0 240 240" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <rect width="240" height="240" fill="#BFD3F2" />
  <path d="M26 250 Q26 170 120 166 Q214 170 214 250 Z" fill="#FFFF1A" stroke="#061866" stroke-width="6" />
  <path d="M98 160 L142 160 L138 178 L102 178 Z" fill="#E8B48C" stroke="#061866" stroke-width="6" stroke-linejoin="round" />
  <circle cx="120" cy="104" r="58" fill="#E8B48C" stroke="#061866" stroke-width="6" />
  <ellipse cx="102" cy="112" rx="6" ry="8" fill="#061866" />
  <ellipse cx="138" cy="112" rx="6" ry="8" fill="#061866" />
  <path d="M104 134 Q120 146 136 134" fill="none" stroke="#061866" stroke-width="6" stroke-linecap="round" />
  <path d="M62 90 Q66 40 120 38 Q174 40 178 90 Z" fill="#061866" />
  <path d="M56 88 L196 88 Q202 100 186 102 L56 102 Z" fill="#061866" />
</svg>"""

CAMION = """<svg class="illu" data-layout-allow-overflow viewBox="0 0 320 200" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <rect width="320" height="200" fill="#DCE6F7" />
  <circle cx="270" cy="42" r="18" fill="#FFFF1A" />
  <rect y="158" width="320" height="42" fill="#53565A" />
  <path d="M10 180 H50 M80 180 H120 M150 180 H190 M220 180 H260 M290 180 H320" stroke="#FFFFFF" stroke-width="4" />
  <rect x="18" y="62" width="186" height="88" rx="6" fill="#FFFFFF" stroke="#061866" stroke-width="5" />
  <rect x="18" y="116" width="186" height="10" fill="#061866" />
  <path d="M210 150 V92 Q210 80 222 80 H262 Q274 80 280 92 L296 118 V150 Z" fill="#061866" />
  <rect x="244" y="88" width="30" height="26" rx="4" fill="#BFD3F2" />
  <circle cx="58" cy="154" r="15" fill="#111111" /><circle cx="58" cy="154" r="6" fill="#BFD3F2" />
  <circle cx="96" cy="154" r="15" fill="#111111" /><circle cx="96" cy="154" r="6" fill="#BFD3F2" />
  <circle cx="180" cy="154" r="15" fill="#111111" /><circle cx="180" cy="154" r="6" fill="#BFD3F2" />
  <circle cx="266" cy="154" r="15" fill="#111111" /><circle cx="266" cy="154" r="6" fill="#BFD3F2" />
</svg>"""

PAYSAGE = """<svg class="illu" data-layout-allow-overflow viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <rect width="100" height="100" fill="{ciel}" /><circle cx="74" cy="28" r="11" fill="#FFFF1A" />
  <path d="M0 78 L30 46 L52 66 L70 50 L100 76 V100 H0 Z" fill="{sol}" />
</svg>"""

APPAREIL = '<svg class="pictro" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8 H8 L9.5 5.5 H14.5 L16 8 H20 V19 H4 Z" fill="none" stroke="#061866" stroke-width="2" stroke-linejoin="round" /><circle cx="12" cy="13" r="3.5" fill="none" stroke="#061866" stroke-width="2" /></svg>'
COCHE = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="#34C759" /><path d="M6.5 12.5 L10.5 16.5 L17.5 8.5" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" /></svg>'


def lettres(cid, texte):
    """Texte tapé lettre par lettre : chaque caractère est un span révélé par la timeline."""
    spans = "".join(f'<span class="l">{c}</span>' for c in texte)
    return f'<span id="{cid}" class="saisie">{spans}<span class="curseur"></span></span>'


def tap(tid, x, y):
    return f'<div id="{tid}" class="tap" style="left: {x}%; top: {y}%"><div class="onde"></div><div class="doigt"></div></div>'


def fleche(fid, x, y, cote):
    """Flèche courbe dont la pointe tombe sur (x %, y %) de l'écran, venant de la gauche ou de la droite."""
    if cote == "gauche":
        trace, tete, decal = "M8 10 C 80 6, 150 40, 178 104", "M160 98 L180 108 L182 86", -186
    else:
        trace, tete, decal = "M192 10 C 120 6, 50 40, 22 104", "M40 98 L20 108 L18 86", -14
    return f"""<svg id="{fid}" class="fleche" viewBox="0 0 200 120" style="left: calc({x}% + {decal}px); top: calc({y}% - 112px)" aria-hidden="true">
            <path class="trait" d="{trace}" pathLength="1" />
            <path class="tete" d="{tete}" />
          </svg>"""


def statut():
    return '<div class="statut"><span>10:10</span><span class="reseau">●●● 4G</span></div>'


BARRE_ONGLETS = '<div class="onglets">' + "".join(f"<span>{o}</span>" for o in ("Carte", "GPS", "Communauté", "Amis", "Job")) + "</div>"

BIO = "Routière depuis 12 ans, toujours partante pour un café !"

ECRAN_PROFIL = f"""<div id="ecran-profil" class="ecran-app" data-layout-allow-overflow>
          {statut()}
          <div class="entete">Mon profil</div>
          <div class="carte-blanche" style="left: 4cqw; top: 14cqh; width: 92cqw; height: 24cqh"></div>
          <div class="avatar vide" style="left: 8cqw; top: 17cqh">{APPAREIL}</div>
          <div id="p-photo" class="avatar plein-p" style="left: 8cqw; top: 17cqh">{PORTRAIT}</div>
          <div class="barre vide" style="left: 38cqw; top: 18.6cqh; width: 36cqw; height: 2.4cqh"></div>
          <div class="barre vide" style="left: 38cqw; top: 23cqh; width: 50cqw; height: 1.4cqh"></div>
          <div class="barre vide" style="left: 38cqw; top: 25.6cqh; width: 40cqw; height: 1.4cqh"></div>
          <div id="p-nom" class="nom plein-p" style="left: 38cqw; top: 18.2cqh">Louna Moreau</div>
          <div id="p-bio" class="bio plein-p" style="left: 38cqw; top: 22.4cqh; width: 48cqw">{BIO}</div>
          <div class="bouton plein" style="left: 8cqw; top: 31cqh; width: 40cqw">Modifier le profil</div>
          <div class="bouton creux" style="left: 52cqw; top: 31cqh; width: 40cqw">Partager</div>
          <div class="rubrique" style="left: 5cqw; top: 41cqh">Camion actuel</div>
          <div id="camion-vide" class="carte-pointillee" style="left: 4cqw; top: 45cqh; width: 92cqw; height: 17cqh">
            <span class="cp-titre">Mets ton camion en valeur !</span>
            <span class="cp-texte">Ajoute ton camion pour montrer aux autres chauffeurs avec quoi tu roules.</span>
            <span class="bouton plein cp-bouton">+ Ajouter mon camion</span>
          </div>
          <div id="camion-plein" class="carte-blanche camion-carte" style="left: 4cqw; top: 45cqh; width: 92cqw; height: 11cqh">
            <div class="vignette">{CAMION}</div>
            <span class="nom-camion">Bobby</span>
            <span class="sous-camion">Mon camion</span>
          </div>
          <div class="coche" id="coche-photo" style="left: calc(8cqw + 8.6cqh); top: 25.2cqh">{COCHE}</div>
          <div class="coche" id="coche-nom" style="right: 6cqw; top: 18.4cqh">{COCHE}</div>
          <div class="coche" id="coche-bio" style="right: 6cqw; top: 23.4cqh">{COCHE}</div>
          <div class="coche" id="coche-camion" style="right: 7cqw; top: 48.6cqh">{COCHE}</div>
          {BARRE_ONGLETS}
        </div>"""

TUILES = "".join(
    f'<div id="tuile-{i}" class="tuile" style="left: {7 + (i % 3) * 30}cqw; top: {62 + (i // 3) * 15}cqh">{contenu}</div>'
    for i, contenu in enumerate(
        [
            PORTRAIT,
            CAMION,
            PAYSAGE.format(ciel="#DCE6F7", sol="#A6E8B8"),
            PAYSAGE.format(ciel="#F6D38B", sol="#E8B48C"),
            PAYSAGE.format(ciel="#C9C3F5", sol="#53565A"),
            PAYSAGE.format(ciel="#BFD3F2", sol="#061866"),
        ]
    )
)

ECRAN_MODIF = f"""<div id="ecran-modif" class="ecran-app" data-layout-allow-overflow>
          {statut()}
          <div class="entete"><span class="retour">‹</span>Modifier le profil</div>
          <div class="avatar grand vide-m" style="left: calc(50cqw - 7cqh); top: 14.5cqh">{APPAREIL}</div>
          <div id="m-photo" class="avatar grand" style="left: calc(50cqw - 7cqh); top: 14.5cqh">{PORTRAIT}</div>
          <div class="lien-photo" style="top: 29.4cqh">Ajouter une photo</div>
          <div class="etiquette" style="top: 34cqh">Prénom</div>
          <div id="champ-prenom" class="champ" style="top: 36.4cqh">{lettres("t-prenom", "Louna")}</div>
          <div class="etiquette" style="top: 43.6cqh">Nom</div>
          <div id="champ-nom" class="champ" style="top: 46cqh">{lettres("t-nom", "Moreau")}</div>
          <div class="etiquette" style="top: 53.2cqh">Biographie</div>
          <div id="champ-bio" class="champ haut" style="top: 55.6cqh">{lettres("t-bio", BIO)}</div>
          <div class="bouton plein large" style="top: 86cqh">Enregistrer</div>
          <div id="voile" class="voile" data-layout-allow-overlap data-layout-allow-occlusion></div>
          <div id="selecteur" class="selecteur" data-layout-allow-overlap data-layout-allow-occlusion>
            <div class="sel-titre" data-layout-allow-overlap data-layout-allow-occlusion>Choisir une photo</div>
            {TUILES}
          </div>
        </div>"""

ECRAN_CAMION = f"""<div id="ecran-camion" class="ecran-app" data-layout-allow-overflow>
          {statut()}
          <div class="entete"><span class="retour">‹</span>Ajouter mon camion</div>
          <div class="etiquette" style="top: 15cqh">Nom du camion</div>
          <div id="champ-camion" class="champ" style="top: 17.4cqh">{lettres("t-camion", "Bobby")}</div>
          <div class="etiquette" style="top: 26cqh">Photo du camion</div>
          <div class="boite-photo" style="top: 28.4cqh">{APPAREIL}<span>Ajouter une photo</span></div>
          <div id="c-photo" class="boite-photo pleine" style="top: 28.4cqh">{CAMION}</div>
          <div class="bouton plein large" style="top: 86cqh">Enregistrer</div>
        </div>"""


CSS_COMMUN = """
      @font-face { font-family: "Bib"; src: url("assets/fonts/BIB-Bold.woff2") format("woff2"); font-weight: 700; }
      @font-face { font-family: "Bib"; src: url("assets/fonts/BIB-Light.woff2") format("woff2"); font-weight: 300; }
      @font-face { font-family: "Inter"; src: url("assets/fonts/Inter-Regular.otf") format("opentype"); font-weight: 400; }
      @font-face { font-family: "Inter"; src: url("assets/fonts/Inter-SemiBold.otf") format("opentype"); font-weight: 600; }
      @font-face { font-family: "Inter"; src: url("assets/fonts/Inter-Bold.otf") format("opentype"); font-weight: 700; }
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html,
      body {
        width: __W__px;
        height: __H__px;
        overflow: hidden;
        background: #061866;
      }
      #root {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        font-family: "Bib", sans-serif;
      }
      .plein-cadre {
        position: absolute;
        inset: 0;
      }
      #fond-couleur {
        position: absolute;
        inset: 0;
        background: #061866;
      }

      /* Textes */
      #textes {
        position: absolute;
      }
      .etape {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        color: #000000;
      }
      .etape.blanc {
        color: #ffffff;
      }
      .ligne {
        display: block;
        white-space: nowrap;
      }
      .titre {
        font-weight: 700;
        line-height: 1.12;
      }
      .leger {
        font-weight: 300;
      }
      .sous {
        font-weight: 300;
        line-height: 1.25;
        margin-top: 18px;
        white-space: normal;
        text-wrap: balance;
      }
      .num {
        display: flex;
        align-items: center;
        justify-content: center;
        width: var(--num);
        height: var(--num);
        border-radius: 50%;
        background: #061866;
        color: #ffffff;
        font-weight: 700;
        font-size: calc(var(--num) * 0.58);
        margin-bottom: 28px;
      }
      .final {
        align-items: center;
        text-align: center;
        color: #ffffff;
      }

      /* Téléphone recréé */
      #telephone {
        position: absolute;
        aspect-ratio: 0.49;
        background: #111111;
        border-radius: 7% / 3.5%;
        padding: 2.4%;
      }
      .tel-int {
        position: relative;
        width: 100%;
        height: 100%;
        container-type: size;
      }
      .tel-ecran {
        position: absolute;
        inset: 0;
        border-radius: 6% / 3%;
        overflow: hidden;
        background: #f5f3f1;
      }
      .calque {
        position: absolute;
        inset: 0;
      }
      .encoche {
        position: absolute;
        left: 33%;
        top: 0;
        width: 34%;
        height: 3.2cqh;
        background: #111111;
        border-radius: 0 0 2cqh 2cqh;
        z-index: 5;
      }
      .ecran-app {
        position: absolute;
        inset: 0;
        background: #f5f3f1;
        font-family: "Inter", sans-serif;
        color: #000000;
      }
      .ecran-app > * {
        position: absolute;
      }
      .statut {
        left: 0;
        right: 0;
        top: 0;
        height: 5cqh;
        background: #061866;
        color: #ffffff;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        padding: 0 7cqw 0.6cqh;
        font-weight: 600;
        font-size: 1.6cqh;
      }
      .reseau {
        font-size: 1.2cqh;
      }
      .entete {
        left: 0;
        right: 0;
        top: 5cqh;
        height: 7cqh;
        background: #061866;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 2.3cqh;
      }
      .retour {
        position: absolute;
        left: 5cqw;
        font-size: 3.4cqh;
        font-weight: 400;
      }
      .carte-blanche {
        background: #ffffff;
        border-radius: 1.6cqh;
      }
      .avatar {
        width: 11cqh;
        height: 11cqh;
        border-radius: 50%;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .avatar.vide,
      .avatar.vide-m {
        background: #e9eef6;
        border: 0.35cqh dashed #8e9bb8;
      }
      .avatar.grand {
        width: 14cqh;
        height: 14cqh;
      }
      #p-photo,
      #m-photo {
        border: 0.45cqh solid #ffff1a;
      }
      .illu {
        display: block;
        width: 100%;
        height: 100%;
      }
      .pictro {
        width: 42%;
        height: 42%;
      }
      .barre {
        background: #e3e6ec;
        border-radius: 0.8cqh;
      }
      .nom {
        font-weight: 700;
        font-size: 2.5cqh;
      }
      .bio {
        font-size: 1.5cqh;
        line-height: 1.3;
        color: #3a3a3c;
      }
      .bouton {
        height: 4.4cqh;
        border-radius: 1cqh;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.6cqh;
      }
      .bouton.plein {
        background: #061866;
        color: #ffffff;
      }
      .bouton.creux {
        border: 0.25cqh solid #061866;
        color: #061866;
        background: #ffffff;
      }
      .bouton.large {
        left: 6cqw;
        width: 88cqw;
        height: 5.4cqh;
        font-size: 1.9cqh;
      }
      .rubrique {
        font-weight: 700;
        font-size: 1.9cqh;
      }
      .carte-pointillee {
        background: #e4edfb;
        border: 0.3cqh dashed #8e9bb8;
        border-radius: 1.6cqh;
        padding: 1.6cqh 5cqw;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 0.8cqh;
      }
      .cp-titre {
        font-weight: 700;
        font-size: 1.9cqh;
      }
      .cp-texte {
        font-size: 1.35cqh;
        color: #3a3a3c;
      }
      .cp-bouton {
        position: static;
        width: 62cqw;
        height: 4.2cqh;
        margin-top: 0.4cqh;
      }
      .camion-carte {
        display: flex;
        align-items: center;
      }
      .vignette {
        position: absolute;
        left: 3cqw;
        top: 1.5cqh;
        width: 11cqh;
        height: 8cqh;
        border-radius: 1cqh;
        overflow: hidden;
      }
      .nom-camion {
        position: absolute;
        left: 34cqw;
        top: 2.6cqh;
        font-weight: 700;
        font-size: 2.2cqh;
      }
      .sous-camion {
        position: absolute;
        left: 34cqw;
        top: 6cqh;
        font-size: 1.5cqh;
        color: #6e6e73;
      }
      .coche {
        width: 3.4cqh;
        height: 3.4cqh;
      }
      .coche svg {
        display: block;
        width: 100%;
        height: 100%;
      }
      .onglets {
        left: 0;
        right: 0;
        bottom: 0;
        height: 8cqh;
        background: #ffffff;
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-size: 1.2cqh;
        color: #6e6e73;
      }
      .lien-photo {
        left: 0;
        right: 0;
        text-align: center;
        font-weight: 700;
        font-size: 1.8cqh;
        color: #061866;
      }
      .etiquette {
        left: 6cqw;
        font-size: 1.5cqh;
        color: #6e6e73;
      }
      .champ {
        left: 6cqw;
        width: 88cqw;
        height: 5.2cqh;
        background: #ffffff;
        border: 0.2cqh solid #d6dae2;
        border-radius: 1cqh;
        padding: 0 3.5cqw;
        display: flex;
        align-items: center;
        font-size: 2cqh;
      }
      .champ.haut {
        display: block;
        height: 12cqh;
        align-items: flex-start;
        padding-top: 1.2cqh;
        line-height: 1.35;
      }
      .saisie {
        display: inline;
      }
      .l {
        display: inline;
      }
      .curseur {
        display: inline-block;
        width: 0.25cqh;
        height: 2.4cqh;
        margin-left: 0.2cqh;
        vertical-align: -0.4cqh;
        background: #061866;
        opacity: 0;
      }
      .voile {
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        background: rgba(6, 24, 102, 0.35);
      }
      .selecteur {
        left: 0;
        right: 0;
        top: 52cqh;
        bottom: 0;
        background: #ffffff;
        border-radius: 2.4cqh 2.4cqh 0 0;
      }
      .sel-titre {
        position: absolute;
        left: 0;
        right: 0;
        top: 3cqh;
        text-align: center;
        font-weight: 700;
        font-size: 2cqh;
      }
      .tuile {
        position: absolute;
        width: 26cqw;
        height: 12cqh;
        border-radius: 1.2cqh;
        overflow: hidden;
        margin-top: -52cqh;
      }
      #tuile-0 {
        outline: 0 solid #061866;
      }
      .boite-photo {
        left: 6cqw;
        width: 88cqw;
        height: 24cqh;
        border-radius: 1.6cqh;
        border: 0.3cqh dashed #8e9bb8;
        background: #e9eef6;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1cqh;
        font-weight: 700;
        font-size: 1.7cqh;
        color: #061866;
      }
      .boite-photo .pictro {
        width: 7cqh;
        height: 7cqh;
      }
      .boite-photo.pleine {
        border: none;
        overflow: hidden;
      }

      /* Interactions */
      .tap {
        position: absolute;
        width: 76px;
        height: 76px;
        margin: -38px 0 0 -38px;
      }
      .tap > div {
        position: absolute;
        inset: 0;
        border-radius: 50%;
        visibility: hidden;
        opacity: 0;
      }
      .doigt {
        background: rgba(255, 255, 255, 0.55);
        border: 5px solid #061866;
      }
      .onde {
        border: 5px solid #061866;
      }
      .fleche {
        position: absolute;
        width: 200px;
        height: 120px;
        overflow: visible;
      }
      .fleche path {
        fill: none;
        stroke: #061866;
        stroke-width: 7;
        stroke-linecap: round;
        stroke-linejoin: round;
      }
      .fleche .trait {
        stroke-dasharray: 1;
      }
"""

CSS_16x9 = """
      /* 16:9 : texte à gauche, téléphone à droite */
      #root {
        --num: 110px;
      }
      #textes {
        left: 130px;
        top: 0;
        bottom: 0;
        width: 1020px;
      }
      .titre {
        font-size: 88px;
      }
      .leger {
        font-size: 64px;
      }
      .sous {
        font-size: 48px;
        max-width: 980px;
      }
      .final {
        left: -130px;
        width: 1920px;
      }
      .final .titre {
        font-size: 120px;
      }
      #telephone {
        right: 230px;
        top: 70px;
        height: 940px;
      }
"""

CSS_9x16 = """
      /* 9:16 : texte en haut, téléphone en dessous */
      #root {
        --num: 104px;
      }
      #textes {
        left: 30px;
        right: 30px;
        top: 250px;
        height: 400px;
      }
      .etape {
        align-items: center;
        text-align: center;
      }
      .titre {
        font-size: 80px;
      }
      .leger {
        font-size: 60px;
      }
      .sous {
        font-size: 50px;
      }
      .num {
        margin-bottom: 20px;
      }
      .final {
        left: -30px;
        right: -30px;
        top: -250px;
        bottom: auto;
        height: 1920px;
        padding: 0 70px;
      }
      .final .titre {
        font-size: 104px;
      }
      #telephone {
        left: calc(50% - 245px);
        top: 660px;
        height: 1000px;
      }
"""

SCRIPT = """
      const tl = gsap.timeline({ paused: true });
      const entre = { autoAlpha: 1, y: 0, duration: 0.4, ease: "power2.out", stagger: 0.1 };
      const sort = { autoAlpha: 0, y: -24, duration: 0.25, ease: "power2.in" };
      const glisse = { duration: 0.4, ease: "power2.inOut" };

      function texte(id, debut, fin) {
        tl.fromTo(`${id} > *`, { autoAlpha: 0, y: 40 }, entre, debut);
        if (fin !== undefined) tl.to(id, sort, fin);
      }
      function tape(id, t) {
        tl.fromTo(`${id} .doigt`, { autoAlpha: 0, scale: 1.5 }, { autoAlpha: 1, scale: 1, duration: 0.15, ease: "power2.out" }, t);
        tl.fromTo(`${id} .onde`, { autoAlpha: 0.9, scale: 0.7 }, { autoAlpha: 0, scale: 2.3, duration: 0.5, ease: "power2.out", immediateRender: false }, t + 0.12);
        tl.to(`${id} .doigt`, { autoAlpha: 0, scale: 0.8, duration: 0.18, ease: "power2.in", immediateRender: false }, t + 0.4);
      }
      function fleche(id, t, fin) {
        tl.fromTo(`${id} .trait`, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, t);
        tl.fromTo(`${id} .tete`, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.12 }, t + 0.34);
        tl.to(id, { autoAlpha: 0, duration: 0.2 }, fin);
      }
      // Saisie lettre par lettre, avec le curseur qui clignote pendant la frappe
      function saisie(id, t, parLettre, n) {
        tl.fromTo(`${id} .curseur`, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t - 0.15);
        tl.fromTo(`${id} .l`, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.01, stagger: parLettre }, t);
        tl.to(`${id} .curseur`, { opacity: 0, duration: 0.01, immediateRender: false }, t + n * parLettre + 0.25);
      }
      const ecranEntre = (id, t) => tl.fromTo(id, { xPercent: 100, autoAlpha: 0 }, { xPercent: 0, autoAlpha: 1, ...glisse }, t);
      const ecranSort = (id, t) => tl.to(id, { xPercent: 100, autoAlpha: 0, ...glisse }, t);
      // L'écran profil glisse à gauche (et s'efface) quand un autre écran le recouvre
      const profilPart = (t, premier) => tl.fromTo("#ecran-profil", { xPercent: 0, autoAlpha: 1 }, { xPercent: -100, autoAlpha: 0, ...glisse, immediateRender: premier }, t);
      const profilRevient = (t) => tl.fromTo("#ecran-profil", { xPercent: -100, autoAlpha: 0 }, { xPercent: 0, autoAlpha: 1, ...glisse, immediateRender: false }, t);

      // Intro (0–4,2 s) : profil vide, puis « 3 étapes »
      texte("#t0", 0.2, 2.25);
      tl.fromTo("#telephone", { autoAlpha: 0, y: 180 }, { autoAlpha: 1, y: 0, duration: 0.7, ease: "power2.out" }, 0.5);
      texte("#t0b", 2.4, 3.95);
      tl.to("#fond-couleur", { backgroundColor: "#F5F3F1", duration: 0.35, ease: "power1.inOut" }, 3.95);

      // 1 · Complète ton profil (4,2–9,2 s) : prénom, nom, biographie
      texte("#t1", 4.3, 8.95);
      tape("#tap-modifier", 4.55);
      ecranEntre("#ecran-modif", 4.8);
      profilPart(4.8, false);
      tl.fromTo("#telephone", { scale: 1 }, { scale: __ZOOM__, duration: 0.6, ease: "power2.inOut", transformOrigin: "50% 55%", immediateRender: false }, 5.0);
      tape("#tap-prenom", 5.25);
      saisie("#t-prenom", 5.45, 0.07, __N_PRENOM__);
      tape("#tap-nom", 6.0);
      saisie("#t-nom", 6.2, 0.07, __N_NOM__);
      tape("#tap-bio", 6.85);
      saisie("#t-bio", 7.05, 0.022, __N_BIO__);
      tl.to("#telephone", { scale: 1, duration: 0.5, ease: "power2.inOut" }, 8.7);

      // 2 · Ajoute ta photo de profil (9,2–13,4 s) : sélecteur, photo choisie, enregistrer
      texte("#t2", 9.25, 13.15);
      fleche("#fleche-photo", 9.35, 10.0);
      tape("#tap-photo", 9.75);
      tl.fromTo("#voile", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, 10.0);
      tl.fromTo("#selecteur", { yPercent: 100 }, { yPercent: 0, duration: 0.4, ease: "power3.out" }, 10.0);
      tape("#tap-tuile", 10.75);
      tl.fromTo("#tuile-0", { outlineWidth: 0 }, { outlineWidth: "0.6cqh", duration: 0.15 }, 10.9);
      tl.to("#selecteur", { yPercent: 100, duration: 0.35, ease: "power2.in" }, 11.15);
      tl.to("#voile", { autoAlpha: 0, duration: 0.3 }, 11.15);
      tl.fromTo("#m-photo", { autoAlpha: 0, scale: 0.6 }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 11.4);
      fleche("#fleche-photo-ok", 11.6, 12.4);
      tape("#tap-enregistrer", 12.35);
      // Retour au profil, désormais rempli (nom, bio, photo)
      tl.fromTo(".plein-p", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.01 }, 12.55);
      tl.fromTo("#ecran-profil .vide, #ecran-profil .barre", { autoAlpha: 1 }, { autoAlpha: 0, duration: 0.01, immediateRender: false }, 12.55);
      profilRevient(12.6);
      ecranSort("#ecran-modif", 12.6);

      // 3 · Ajoute ton camion (13,4–18 s) : nom du camion, photo, carte sur le profil
      texte("#t3", 13.45, 17.75);
      fleche("#fleche-camion", 13.55, 14.15);
      tape("#tap-ajout-camion", 14.0);
      ecranEntre("#ecran-camion", 14.25);
      profilPart(14.25, false);
      tape("#tap-nom-camion", 14.75);
      saisie("#t-camion", 14.95, 0.08, __N_CAMION__);
      tape("#tap-photo-camion", 15.6);
      tl.fromTo("#c-photo", { autoAlpha: 0, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, 15.85);
      tape("#tap-enregistrer-camion", 16.45);
      tl.fromTo("#camion-plein", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.01 }, 16.65);
      tl.fromTo("#camion-vide", { autoAlpha: 1 }, { autoAlpha: 0, duration: 0.01, immediateRender: false }, 16.65);
      profilRevient(16.7);
      ecranSort("#ecran-camion", 16.7);
      tl.fromTo("#camion-plein", { scale: 0.9 }, { scale: 1, duration: 0.4, ease: "back.out(2)", immediateRender: false }, 17.0);

      // Fin A (18–21,6 s) : profil complet, coché point par point
      texte("#t4", 18.0, 21.45);
      tl.fromTo(".coche", { autoAlpha: 0, scale: 0.3 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)", stagger: 0.2 }, 18.25);
      tl.to("#telephone", { autoAlpha: 0, y: 80, duration: 0.3, ease: "power2.in" }, 21.45);

      // Fin B (21,6–25 s)
      tl.to("#fond-couleur", { backgroundColor: "#061866", duration: 0.35, ease: "power1.inOut" }, 21.5);
      texte("#t5", 21.75);

      window.__timelines["__ID__"] = tl;
      tl.seek(0);
"""


def page(cid, w, h, css_format, zoom):
    css = (CSS_COMMUN + css_format).replace("__W__", str(w)).replace("__H__", str(h))
    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={w}, height={h}" />
    <!-- Généré par scripts/generer.py : modifier le générateur, pas ce fichier. -->
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{css}    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="{cid}"
      data-start="0"
      data-duration="{DUREE}"
      data-width="{w}"
      data-height="{h}"
    >
      <div id="fond" class="plein-cadre clip" data-start="0" data-duration="{DUREE}" data-track-index="0">
        <div id="fond-couleur"></div>
      </div>

      <div id="ecrans" class="plein-cadre clip" data-start="0" data-duration="21.8" data-track-index="1">
        <div id="telephone">
          <div class="tel-int">
            <div class="tel-ecran">
              {ECRAN_PROFIL}
              {ECRAN_MODIF}
              {ECRAN_CAMION}
              <div class="encoche"></div>
            </div>
            <div class="calque">
              {tap("tap-modifier", 28, 33.2)}
              {tap("tap-prenom", 40, 39)}
              {tap("tap-nom", 40, 48.6)}
              {tap("tap-bio", 40, 61.6)}
              {fleche("fleche-photo", 40, 18, "gauche")}
              {tap("tap-photo", 50, 21.5)}
              {tap("tap-tuile", 20, 68)}
              {fleche("fleche-photo-ok", 40, 18, "gauche")}
              {tap("tap-enregistrer", 50, 88.7)}
              {fleche("fleche-camion", 22, 57, "gauche")}
              {tap("tap-ajout-camion", 50, 58.6)}
              {tap("tap-nom-camion", 40, 20)}
              {tap("tap-photo-camion", 50, 40.4)}
              {tap("tap-enregistrer-camion", 50, 88.7)}
            </div>
          </div>
        </div>
      </div>

      <div id="textes-clip" class="plein-cadre clip" data-start="0" data-duration="{DUREE}" data-track-index="2">
        <div id="textes">
          <div id="t0" class="etape blanc">
            <span class="ligne titre leger">Guide&nbsp;:</span>
            <span class="ligne titre">crée ton</span>
            <span class="ligne titre">Profil Trucker&nbsp;!</span>
          </div>
          <div id="t0b" class="etape blanc">
            <span class="ligne titre">3 étapes</span>
            <span class="ligne titre">et le tour est joué&nbsp;!</span>
          </div>
          <div id="t1" class="etape">
            <div class="num">1</div>
            <span class="ligne titre">Complète ton profil</span>
          </div>
          <div id="t2" class="etape">
            <div class="num">2</div>
            <span class="ligne titre">Ajoute ta photo</span>
            <span class="ligne titre">de profil</span>
          </div>
          <div id="t3" class="etape">
            <div class="num">3</div>
            <span class="ligne titre">Ajoute ton camion</span>
          </div>
          <div id="t4" class="etape">
            <span class="ligne titre">Et le tour est joué&nbsp;!</span>
            <span class="ligne sous">Plus ton profil est complet et personnalisé, plus tes amis pourront te retrouver facilement&nbsp;!</span>
          </div>
          <div id="t5" class="etape final" data-layout-allow-overflow>
            <span class="ligne titre">Alors, à toi</span>
            <span class="ligne titre">de jouer&nbsp;!</span>
          </div>
        </div>
      </div>
    </div>
    <script>{SCRIPT.replace("__ID__", cid).replace("__ZOOM__", zoom).replace("__N_PRENOM__", "5").replace("__N_NOM__", "6").replace("__N_BIO__", str(len(BIO))).replace("__N_CAMION__", "5")}    </script>
  </body>
</html>
"""


(RACINE / "index.html").write_text(page("main", 1920, 1080, CSS_16x9, "1.06"))
(RACINE / "compositions" / "vertical.html").write_text(page("vertical", 1080, 1920, CSS_9x16, "1.12"))
print("index.html et compositions/vertical.html générés")
