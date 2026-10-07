"""Génère la vidéo « Guide : crée ton Profil Trucker » (25 s) en deux formats.

    python3 scripts/generer.py

Écrit index.html (16:9, 1920 × 1080) et compositions/vertical.html (9:16, 1080 × 1920).
Les écrans sont les captures de l'app (rognées à 460 × 911 px). Seuls les éléments absents
des captures sont recréés par-dessus, au style de l'app : saisie du numéro, photo de profil,
bio sous la photo, dimensions et carte du camion. Les positions sur les écrans sont en % de la capture.
"""

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DUREE = 25

NUMERO = "06 78 90 00 70"
BIO_AVANT = "Conducteur routier "
BIO_APRES = " | Toujours sur la route | À la recherche des meilleurs spots !"
SURNOM = "Le Bolide"
DIMENSIONS = [("Hauteur", "4,00"), ("Largeur", "2,55"), ("Longueur", "16,50")]

# --- Illustrations (pas de vraies photos) ---

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

PAYSAGE = """<svg class="illu" data-layout-allow-overflow viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <rect width="100" height="100" fill="{ciel}" /><circle cx="74" cy="28" r="11" fill="#FFFF1A" />
  <path d="M0 78 L30 46 L52 66 L70 50 L100 76 V100 H0 Z" fill="{sol}" />
</svg>"""

COCHE = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="#34C759" /><path d="M6.5 12.5 L10.5 16.5 L17.5 8.5" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" /></svg>'
EMOJI_CAMION = '<span class="emoji" role="img" aria-label="camion"></span>'


def lettres(cid, texte, emoji_apres=None):
    """Texte tapé lettre par lettre ; un emoji peut être inséré comme une « lettre »."""
    def spans(t):
        return "".join(f'<span class="l">{c}</span>' for c in t)

    corps = spans(texte)
    if emoji_apres is not None:
        corps += f'<span class="l">{EMOJI_CAMION}</span>' + spans(emoji_apres)
    return f'<span id="{cid}" class="saisie">{corps}<span class="curseur"></span></span>'


def nb_lettres(texte, emoji_apres=None):
    return len(texte) + (1 + len(emoji_apres) if emoji_apres is not None else 0)


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


def ecran(eid, image, contenu=""):
    return f"""<div id="{eid}" class="ecran">
            <div class="cadre">
              <img src="assets/ecrans/{image}.png" alt="" />
              {contenu}
            </div>
          </div>"""


# Zone intérieure de l'écran (hors coque), pour découper les feuilles qui montent du bas
ZONE = 'class="zone-ecran" data-layout-allow-overflow'

def tuiles(prefixe, premiere):
    return "".join(
        f'<div id="{prefixe}-tuile-{i}" class="tuile" style="left: {6 + (i % 3) * 31}%; top: {24 + (i // 3) * 28}%">{contenu}</div>'
        for i, contenu in enumerate(
            [
                premiere,
                PAYSAGE.format(ciel="#DCE6F7", sol="#A6E8B8"),
                PAYSAGE.format(ciel="#F6D38B", sol="#E8B48C"),
                PAYSAGE.format(ciel="#C9C3F5", sol="#53565A"),
                PAYSAGE.format(ciel="#BFD3F2", sol="#061866"),
                PAYSAGE.format(ciel="#FFFFFF", sol="#BFD3F2"),
            ]
        )
    )


def selecteur(prefixe, premiere):
    return f"""<div {ZONE}>
                <div id="{prefixe}-voile" class="voile" data-layout-allow-overlap data-layout-allow-occlusion></div>
                <div id="{prefixe}-selecteur" class="feuille selecteur" data-layout-allow-overlap data-layout-allow-occlusion>
                  <div class="f-titre">Choisir une photo</div>
                  {tuiles(prefixe, premiere)}
                </div>
              </div>"""


E_INVITE = ecran(
    "e-invite",
    "invite",
    f"""{fleche("fleche-connexion", 18, 82, "gauche")}
              {tap("tap-connexion", 50, 84.3)}""",
)

E_CONNEXION = ecran(
    "e-connexion",
    "connexion",
    f"""{fleche("fleche-email", 18, 58.6, "gauche")}
              {fleche("fleche-mobile", 18, 64.5, "gauche")}
              {tap("tap-mobile", 50, 66.7)}
              <div {ZONE}>
                <div id="feuille-tel" class="feuille" data-layout-allow-overlap data-layout-allow-occlusion>
                  <div class="f-titre">Continuer avec mon mobile</div>
                  <div class="f-etiquette">Numéro de mobile</div>
                  <div class="f-champ">{lettres("t-numero", NUMERO)}</div>
                  <div class="f-bouton">Continuer</div>
                  <div id="connecte" class="f-bouton ok" data-layout-allow-overlap data-layout-allow-occlusion>✓ Connecté</div>
                </div>
              </div>
              {tap("tap-champ-tel", 50, 72)}
              {tap("tap-continuer", 50, 84)}""",
)

DIMS_TEXTE = " · ".join(f"{nom} {valeur} m" for nom, valeur in DIMENSIONS)

E_PROFIL = ecran(
    "e-profil",
    "profil-vide",
    f"""<div id="p-carte" class="p-carte">
                <div class="p-photo">{PORTRAIT}</div>
                <div class="p-nom">Charlie G.</div>
                <div class="p-membre">Membre depuis 2026</div>
                <div id="bio-vide" class="p-bio-vide">+ Ajoute ta bio</div>
                <div id="p-bio" class="p-bio">{BIO_AVANT}{EMOJI_CAMION}{BIO_APRES}</div>
              </div>
              <div id="p-camion" class="p-camion">
                <div class="p-camion-carte">
                  <div class="p-vignette">{CAMION}</div>
                  <div class="p-camion-textes"><b>Camion · « {SURNOM} »</b><span>{DIMS_TEXTE}</span></div>
                </div>
              </div>
              <div class="coche" id="coche-photo" style="left: 27%; top: 15.6%">{COCHE}</div>
              <div class="coche" id="coche-nom" style="left: 84.5%; top: 17.6%">{COCHE}</div>
              <div class="coche" id="coche-bio" style="left: 84.5%; top: 26.6%">{COCHE}</div>
              <div class="coche" id="coche-camion" style="left: 82%; top: 67.4%">{COCHE}</div>
              {fleche("fleche-nom", 40, 19.5, "gauche")}
              {tap("tap-modifier", 31.7, 33.2)}
              {fleche("fleche-photo", 22, 22, "gauche")}
              {tap("tap-avatar", 33, 25.5)}
              {selecteur("p", PORTRAIT)}
              {tap("tap-tuile-p", 22, 66)}
              {tap("tap-bio-ajout", 30, 27.6)}
              <div {ZONE}>
                <div id="feuille-bio" class="feuille" data-layout-allow-overlap data-layout-allow-occlusion>
                  <div class="f-titre">Bio</div>
                  <div class="f-champ haut">{lettres("t-bio", BIO_AVANT, BIO_APRES)}</div>
                  <div class="f-bouton">Enregistrer</div>
                </div>
              </div>
              {tap("tap-enregistrer-bio", 50, 84)}
              {fleche("fleche-bio", 18, 27.5, "gauche")}
              {fleche("fleche-ajout-camion", 34, 81.5, "gauche")}
              {tap("tap-ajout-camion", 55.4, 82.5)}""",
)

E_INFOS = ecran(
    "e-infos",
    "infos",
    f"""<div class="valeur" style="top: 17.6%">{lettres("t-prenom", "Charlie")}</div>
              <div class="valeur" style="top: 25.7%">{lettres("t-nom", "Giraud")}</div>
              {tap("tap-prenom", 50, 18.2)}
              {tap("tap-nom", 50, 26.2)}""",
)

E_VEHICULE = ecran(
    "e-vehicule",
    "vehicule",
    f"""<div id="photo-camion" class="photo-camion">{CAMION.replace('xMidYMid slice', 'xMidYMid meet')}</div>
              <div class="valeur surnom" style="top: 52.3%">{lettres("t-surnom", SURNOM)}</div>
              <div id="type-camion" class="type-camion"></div>
              <div id="dims" class="dims">
                {"".join(f'<div class="dim" style="left: {i * 34}%"><span class="dim-nom">{nom}</span><div class="dim-champ">{lettres(f"t-dim-{i}", valeur)}<span class="unite">m</span></div></div>' for i, (nom, valeur) in enumerate(DIMENSIONS))}
              </div>
              <div id="enregistrer-actif" class="enregistrer-actif">Enregistrer</div>
              {tap("tap-photo-camion", 50, 40.6)}
              {selecteur("v", CAMION)}
              {tap("tap-tuile-v", 22, 66)}
              {tap("tap-surnom", 50, 53.8)}
              {tap("tap-type", 23.5, 68.4)}
              {tap("tap-dim-0", 20, 79.5)}
              {tap("tap-dim-1", 48, 79.5)}
              {tap("tap-dim-2", 76, 79.5)}
              {tap("tap-enregistrer-camion", 50, 90.2)}""",
)


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

      /* Téléphone : captures de l'app */
      #telephone {
        position: absolute;
      }
      .ecran {
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .cadre {
        position: relative;
        height: 100%;
        aspect-ratio: 460 / 911;
        container-type: size;
      }
      .cadre > img {
        display: block;
        width: 100%;
        height: 100%;
      }
      .cadre > * {
        position: absolute;
      }
      .cadre > img {
        position: static;
      }
      .zone-ecran {
        left: 7.2%;
        top: 2.7%;
        width: 85.6%;
        height: 94.5%;
        border-radius: 5.5cqh;
        overflow: hidden;
        pointer-events: none;
      }
      .illu {
        display: block;
        width: 100%;
        height: 100%;
      }
      .emoji {
        display: inline-block;
        height: 1.1em;
        width: 1.48em;
        vertical-align: -0.2em;
        background: url("assets/emoji/camion.png") center / contain no-repeat;
      }

      /* Éléments recréés au style de l'app (Inter) */
      .feuille {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 50%;
        background: #ffffff;
        border-radius: 2.4cqh 2.4cqh 0 0;
        box-shadow: 0 -1cqh 3cqh rgba(0, 0, 0, 0.18);
        font-family: "Inter", sans-serif;
      }
      .feuille > * {
        position: absolute;
        left: 7%;
        right: 7%;
      }
      .f-titre {
        top: 6%;
        text-align: center;
        font-weight: 700;
        font-size: 2.1cqh;
        color: #000000;
      }
      .f-etiquette {
        top: 21%;
        font-size: 1.6cqh;
        color: #6e6e73;
      }
      .f-champ {
        top: 29%;
        height: 12%;
        border: 0.25cqh solid #061866;
        border-radius: 1cqh;
        padding: 0 4%;
        display: flex;
        align-items: center;
        font-size: 2.2cqh;
        color: #000000;
      }
      .f-champ.haut {
        top: 20%;
        height: 42%;
        display: block;
        padding: 1.6cqh 4%;
        font-size: 1.9cqh;
        line-height: 1.4;
      }
      .f-bouton {
        top: 72%;
        height: 13%;
        border-radius: 1.2cqh;
        background: #061866;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 2cqh;
      }
      .f-bouton.ok {
        background: #34c759;
      }
      .saisie,
      .l {
        display: inline;
      }
      .curseur {
        display: inline-block;
        width: 0.25cqh;
        height: 2.2cqh;
        margin-left: 0.2cqh;
        vertical-align: -0.4cqh;
        background: #061866;
        opacity: 0;
      }
      .valeur {
        left: 11.5%;
        width: 60%;
        height: 2.8%;
        background: #ffffff;
        font-family: "Inter", sans-serif;
        font-size: 1.85cqh;
        color: #6e6e73;
        display: flex;
        align-items: center;
      }
      .valeur.surnom {
        left: 11.5%;
        width: 76%;
        height: 4%;
        background: transparent;
        color: #000000;
        font-size: 2.1cqh;
      }
      .p-carte {
        left: 11.5%;
        top: 15%;
        width: 77%;
        height: 16.2%;
        background: #ffffff;
        font-family: "Inter", sans-serif;
      }
      .p-carte > * {
        position: absolute;
      }
      .p-photo {
        left: 5%;
        top: 4%;
        width: 9.4cqh;
        height: 9.4cqh;
        border-radius: 50%;
        overflow: hidden;
        border: 0.45cqh solid #ffff1a;
      }
      .p-nom {
        left: 42%;
        top: 10%;
        font-weight: 700;
        font-size: 2.5cqh;
        color: #000000;
      }
      .p-membre {
        left: 42%;
        top: 34%;
        font-size: 1.45cqh;
        color: #6e6e73;
      }
      .p-bio-vide,
      .p-bio {
        left: 5%;
        top: 70%;
        width: 88%;
        font-size: 1.35cqh;
        line-height: 1.3;
      }
      .p-bio-vide {
        font-weight: 700;
        color: #061866;
        font-size: 1.5cqh;
      }
      .p-bio {
        color: #3a3a3c;
      }
      .p-camion {
        left: 11%;
        top: 65.6%;
        width: 78.5%;
        height: 20.8%;
        background: #f5f3f1;
      }
      .p-camion-carte {
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        height: 9cqh;
        background: #ffffff;
        border-radius: 1.4cqh;
        display: flex;
        align-items: center;
        gap: 2.4cqh;
        padding: 0 1.4cqh;
        font-family: "Inter", sans-serif;
      }
      .p-vignette {
        width: 9.6cqh;
        height: 6.6cqh;
        border-radius: 1cqh;
        overflow: hidden;
        flex: none;
      }
      .p-camion-textes {
        display: flex;
        flex-direction: column;
        gap: 0.4cqh;
        font-size: 1.3cqh;
        color: #6e6e73;
      }
      .p-camion-textes b {
        font-size: 1.8cqh;
        color: #000000;
      }
      .photo-camion {
        background: #dce6f7;
        left: 9.1%;
        top: 35.3%;
        width: 81.5%;
        height: 10.6%;
        border-radius: 1.4cqh;
        overflow: hidden;
      }
      .type-camion {
        left: 9.4%;
        top: 64.6%;
        width: 26.5%;
        height: 7.6%;
        border: 0.35cqh solid #061866;
        border-radius: 1.2cqh;
        background: rgba(6, 24, 102, 0.08);
      }
      .enregistrer-actif {
        left: 9.1%;
        top: 87.3%;
        width: 81.6%;
        height: 6.1%;
        border-radius: 1.2cqh;
        background: #061866;
        color: #ffffff;
        font-family: "Inter", sans-serif;
        font-weight: 700;
        font-size: 2.1cqh;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .voile {
        position: absolute;
        inset: 0;
        opacity: 0;
        visibility: hidden;
        background: rgba(6, 24, 102, 0.35);
      }
      .selecteur .tuile {
        position: absolute;
        width: 27%;
        height: 24%;
        border-radius: 1.2cqh;
        overflow: hidden;
      }
      #p-tuile-0,
      #v-tuile-0 {
        outline: 0 solid #061866;
      }
      .dims {
        left: 9.1%;
        top: 73.6%;
        width: 81.6%;
        height: 10%;
        font-family: "Inter", sans-serif;
      }
      .dim {
        position: absolute;
        top: 0;
        width: 32%;
        height: 100%;
      }
      .dim-nom {
        position: absolute;
        top: 0;
        left: 0;
        font-weight: 700;
        font-size: 1.5cqh;
        color: #000000;
      }
      .dim-champ {
        position: absolute;
        left: 0;
        right: 0;
        top: 32%;
        height: 50%;
        background: #ffffff;
        border: 0.2cqh solid #d6dae2;
        border-radius: 1cqh;
        padding: 0 8%;
        display: flex;
        align-items: center;
        font-size: 1.9cqh;
        color: #000000;
      }
      .unite {
        margin-left: auto;
        color: #6e6e73;
        font-size: 1.5cqh;
      }
      .coche {
        width: 3.6cqh;
        height: 3.6cqh;
      }
      .coche svg {
        display: block;
        width: 100%;
        height: 100%;
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
        width: 1040px;
      }
      .titre {
        font-size: 88px;
      }
      .leger {
        font-size: 56px;
        margin-top: 12px;
      }
      .sous {
        font-size: 48px;
        max-width: 1000px;
      }
      .final {
        left: -130px;
        width: 1920px;
      }
      .final .titre {
        font-size: 120px;
      }
      #telephone {
        right: 200px;
        top: 50px;
        width: 520px;
        height: 980px;
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
        font-size: 52px;
        margin-top: 10px;
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
        left: 0;
        right: 0;
        top: 660px;
        height: 1000px;
      }
      #t2 .sous {
        font-size: 44px;
      }
"""

SCRIPT = """
      const tl = gsap.timeline({ paused: true });
      const entre = { autoAlpha: 1, y: 0, duration: 0.4, ease: "power2.out", stagger: 0.1 };
      const sort = { autoAlpha: 0, y: -24, duration: 0.25, ease: "power2.in" };
      const arrive = { xPercent: 0, autoAlpha: 1, duration: 0.45, ease: "power2.inOut" };
      const part = { xPercent: -30, autoAlpha: 0, duration: 0.45, ease: "power2.inOut" };

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
      function saisie(id, t, parLettre, n) {
        tl.fromTo(`${id} .curseur`, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t - 0.15);
        tl.fromTo(`${id} .l`, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.01, stagger: parLettre }, t);
        tl.to(`${id} .curseur`, { opacity: 0, duration: 0.01, immediateRender: false }, t + n * parLettre + 0.25);
      }
      function feuilleMonte(id, t) {
        tl.fromTo(id, { yPercent: 105 }, { yPercent: 0, duration: 0.4, ease: "power3.out" }, t);
      }
      function feuilleDescend(id, t) {
        tl.to(id, { yPercent: 105, duration: 0.35, ease: "power2.in" }, t);
      }
      function apparait(id, t) {
        tl.fromTo(id, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.2 }, t);
      }

      // Intro (0–3 s) : l'app en mode invité, puis l'écran de connexion
      texte("#t0", 0.2, 2.8);
      tl.fromTo("#telephone", { autoAlpha: 0, y: 180 }, { autoAlpha: 1, y: 0, duration: 0.7, ease: "power2.out" }, 0.3);
      fleche("#fleche-connexion", 1.3, 2.25);
      tape("#tap-connexion", 1.9);
      tl.fromTo("#e-connexion", { xPercent: 60, autoAlpha: 0 }, arrive, 2.25);
      tl.fromTo("#e-invite", { xPercent: 0, autoAlpha: 1 }, { ...part, immediateRender: false }, 2.25);
      tl.to("#fond-couleur", { backgroundColor: "#F5F3F1", duration: 0.35, ease: "power1.inOut" }, 2.85);

      // 1 · Connecte-toi (3–7,2 s) : e-mail ou mobile, numéro, validation
      texte("#t1", 3.1, 6.95);
      fleche("#fleche-email", 3.2, 4.15);
      fleche("#fleche-mobile", 3.5, 4.15);
      tape("#tap-mobile", 3.9);
      feuilleMonte("#feuille-tel", 4.1);
      tape("#tap-champ-tel", 4.4);
      saisie("#t-numero", 4.55, 0.05, __N_NUMERO__);
      tape("#tap-continuer", 5.45);
      apparait("#connecte", 5.65);
      tl.fromTo("#e-profil", { xPercent: 60, autoAlpha: 0 }, arrive, 6.15);
      tl.fromTo("#e-connexion", { xPercent: 0, autoAlpha: 1 }, { ...part, immediateRender: false }, 6.15);
      fleche("#fleche-nom", 6.55, 6.95);

      // 2 · Complète ton profil (7,2–14,6 s) : prénom, nom, photo, bio sous la photo
      texte("#t2", 7.3, 14.35);
      tape("#tap-modifier", 7.45);
      tl.fromTo("#e-infos", { xPercent: 60, autoAlpha: 0 }, arrive, 7.65);
      tl.fromTo("#e-profil", { xPercent: 0, autoAlpha: 1 }, { ...part, immediateRender: false }, 7.65);
      tape("#tap-prenom", 8.05);
      saisie("#t-prenom", 8.2, 0.05, 7);
      tape("#tap-nom", 8.65);
      saisie("#t-nom", 8.8, 0.05, 6);
      tl.fromTo("#e-profil", { xPercent: -30, autoAlpha: 0 }, { ...arrive, immediateRender: false }, 9.35);
      tl.to("#e-infos", { xPercent: 60, autoAlpha: 0, duration: 0.45, ease: "power2.inOut" }, 9.35);
      fleche("#fleche-photo", 9.7, 10.3);
      tape("#tap-avatar", 10.0);
      tl.fromTo("#p-voile", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.25 }, 10.2);
      feuilleMonte("#p-selecteur", 10.2);
      tape("#tap-tuile-p", 10.65);
      tl.fromTo("#p-tuile-0", { outlineWidth: 0 }, { outlineWidth: "0.6cqh", duration: 0.12 }, 10.75);
      feuilleDescend("#p-selecteur", 10.9);
      tl.to("#p-voile", { autoAlpha: 0, duration: 0.25 }, 10.9);
      apparait("#p-carte", 11.1);
      tl.fromTo("#p-carte .p-photo", { scale: 0.5 }, { scale: 1, duration: 0.4, ease: "back.out(2)" }, 11.1);
      tape("#tap-bio-ajout", 11.55);
      feuilleMonte("#feuille-bio", 11.7);
      saisie("#t-bio", 11.95, 0.013, __N_BIO__);
      tape("#tap-enregistrer-bio", 13.2);
      feuilleDescend("#feuille-bio", 13.4);
      tl.fromTo("#bio-vide", { autoAlpha: 1 }, { autoAlpha: 0, duration: 0.15, immediateRender: false }, 13.5);
      apparait("#p-bio", 13.55);
      fleche("#fleche-bio", 13.75, 14.35);

      // 3 · Ajoute ton camion (14,6–20,4 s) : photo, surnom, type, dimensions
      texte("#t3", 14.7, 20.15);
      fleche("#fleche-ajout-camion", 14.75, 15.35);
      tape("#tap-ajout-camion", 15.05);
      tl.fromTo("#e-vehicule", { xPercent: 60, autoAlpha: 0 }, arrive, 15.3);
      tl.fromTo("#e-profil", { xPercent: 0, autoAlpha: 1 }, { ...part, immediateRender: false }, 15.3);
      tape("#tap-photo-camion", 15.65);
      tl.fromTo("#v-voile", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.25 }, 15.8);
      feuilleMonte("#v-selecteur", 15.8);
      tape("#tap-tuile-v", 16.25);
      tl.fromTo("#v-tuile-0", { outlineWidth: 0 }, { outlineWidth: "0.6cqh", duration: 0.12 }, 16.35);
      feuilleDescend("#v-selecteur", 16.5);
      tl.to("#v-voile", { autoAlpha: 0, duration: 0.25 }, 16.5);
      tl.fromTo("#photo-camion", { autoAlpha: 0, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, 16.65);
      tape("#tap-surnom", 17.0);
      saisie("#t-surnom", 17.1, 0.045, __N_SURNOM__);
      tape("#tap-type", 17.6);
      apparait("#type-camion", 17.75);
      apparait("#dims", 17.8);
      tape("#tap-dim-0", 18.0);
      saisie("#t-dim-0", 18.1, 0.05, 4);
      tape("#tap-dim-1", 18.45);
      saisie("#t-dim-1", 18.55, 0.05, 4);
      tape("#tap-dim-2", 18.9);
      saisie("#t-dim-2", 19.0, 0.05, 5);
      apparait("#enregistrer-actif", 19.3);
      tape("#tap-enregistrer-camion", 19.45);
      apparait("#p-camion", 19.65);
      tl.fromTo("#e-profil", { xPercent: -30, autoAlpha: 0 }, { ...arrive, immediateRender: false }, 19.7);
      tl.to("#e-vehicule", { xPercent: 60, autoAlpha: 0, duration: 0.45, ease: "power2.inOut" }, 19.7);
      tl.fromTo("#p-camion .p-camion-carte", { scale: 0.85 }, { scale: 1, duration: 0.4, ease: "back.out(2)" }, 19.95);

      // Fin A (20,4–23 s) : le profil de Charlie, coché point par point
      texte("#t4", 20.45, 22.75);
      tl.fromTo(".coche", { autoAlpha: 0, scale: 0.3 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)", stagger: 0.15 }, 20.6);
      tl.to("#telephone", { autoAlpha: 0, y: 80, duration: 0.3, ease: "power2.in" }, 22.75);

      // Fin B (23–25 s)
      tl.to("#fond-couleur", { backgroundColor: "#061866", duration: 0.35, ease: "power1.inOut" }, 22.8);
      texte("#t5", 23.05);

      window.__timelines["__ID__"] = tl;
      tl.seek(0);
"""


def page(cid, w, h, css_format):
    css = (CSS_COMMUN + css_format).replace("__W__", str(w)).replace("__H__", str(h))
    script = (
        SCRIPT.replace("__ID__", cid)
        .replace("__N_NUMERO__", str(len(NUMERO)))
        .replace("__N_BIO__", str(nb_lettres(BIO_AVANT, BIO_APRES)))
        .replace("__N_SURNOM__", str(len(SURNOM)))
    )
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

      <div id="ecrans" class="plein-cadre clip" data-start="0" data-duration="23.1" data-track-index="1">
        <div id="telephone">
          {E_INVITE}
          {E_CONNEXION}
          {E_PROFIL}
          {E_INFOS}
          {E_VEHICULE}
        </div>
      </div>

      <div id="textes-clip" class="plein-cadre clip" data-start="0" data-duration="{DUREE}" data-track-index="2">
        <div id="textes">
          <div id="t0" class="etape blanc">
            <span class="ligne titre">Crée ton Profil Trucker</span>
            <span class="ligne titre leger">en 3 étapes et le tour est joué&nbsp;!</span>
          </div>
          <div id="t1" class="etape">
            <div class="num">1</div>
            <span class="ligne titre">Connecte-toi</span>
          </div>
          <div id="t2" class="etape">
            <div class="num">2</div>
            <span class="ligne titre">Complète ton profil</span>
            <span class="ligne sous">Plus ton profil est complet, plus tes amis pourront te retrouver facilement&nbsp;!</span>
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
    <script>{script}    </script>
  </body>
</html>
"""


(RACINE / "index.html").write_text(page("main", 1920, 1080, CSS_16x9))
(RACINE / "compositions" / "vertical.html").write_text(page("vertical", 1080, 1920, CSS_9x16))
print("index.html et compositions/vertical.html générés")
