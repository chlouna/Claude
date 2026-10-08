"""Génère les 12 interstitiels Profil Trucker / Social Core de Michelin Truckfly.

    python3 scripts/generer.py

Écrit index.html : les 12 écrans au format téléphone (390 × 844 px), avec de petites animations
d'entrée. scripts/capturer.mjs en tire un PNG par écran (×3, soit 1170 × 2532 px) dans png/.

Charte : Michelin Blue pour les visuels, Bib pour les titres, Inter pour l'interface (police
de l'app). Le jaune n'apparaît que sur fond bleu ; sur fond blanc, le bouton principal est bleu.
"""

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# --- Briques visuelles reprises des vidéos -------------------------------------------------

YEUX = {
    "points": '<ellipse cx="40" cy="44" rx="4.5" ry="7" fill="#061866" /><ellipse cx="60" cy="44" rx="4.5" ry="7" fill="#061866" />',
    "plisses": '<path d="M33 38 L42 44 L33 50 M67 38 L58 44 L67 50" fill="none" stroke="#061866" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />',
}
BADGES = {
    "invitation": '<circle cx="10" cy="9" r="4" fill="#061866" /><path d="M3 21 Q3 14 10 14 Q17 14 17 21 Z" fill="#061866" /><path d="M20 8 V16 M16 12 H24" stroke="#061866" stroke-width="2.6" stroke-linecap="round" />',
    "visite": '<rect x="2" y="7" width="13" height="10" rx="2" fill="#061866" /><path d="M15 10 H20 L23 14 V17 H15 Z" fill="#061866" /><circle cx="7" cy="19" r="2.4" fill="#061866" /><circle cx="19" cy="19" r="2.4" fill="#061866" />',
    "avis": '<path d="M3 5 H21 Q23 5 23 7 V16 Q23 18 21 18 H11 L6 22 V18 H5 Q3 18 3 16 V7 Q3 5 5 5 Z" fill="#061866" />',
    "ami": '<circle cx="13" cy="8" r="5" fill="#061866" /><path d="M3 24 Q3 15 13 15 Q23 15 23 24 Z" fill="#061866" />',
}
PERSONNES = {
    "louna": ("L", "#C9C3F5", "#FFFF1A", "points"),
    "nicolas": ("N", "#A6E8B8", "#061866", "points"),
    "david": ("D", "#F6D38B", "#FFFF1A", "plisses"),
    "vanessa": ("V", "#BFD3F2", "#061866", "points"),
}


def avatar(qui, badge=None, classe="av"):
    lettre, visage, anneau, yeux = PERSONNES[qui]
    pastille = (
        f'<circle cx="88" cy="88" r="20" fill="#DCE6F7" stroke="#FFFFFF" stroke-width="4" />'
        f'<svg x="75" y="75" width="26" height="26" viewBox="0 0 26 26">{BADGES[badge]}</svg>'
        if badge
        else ""
    )
    return (
        f'<svg class="{classe}" viewBox="0 0 112 112" aria-hidden="true">'
        f'<circle cx="50" cy="50" r="44" fill="{visage}" stroke="{anneau}" stroke-width="8" />{YEUX[yeux]}'
        f'<text x="50" y="72" text-anchor="middle" font-family="Inter" font-weight="600" font-size="20" fill="#061866">{lettre}</text>'
        f"{pastille}</svg>"
    )


PORTRAIT = """<svg class="illu" viewBox="0 0 240 240" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <rect width="240" height="240" fill="#BFD3F2" />
  <path d="M26 250 Q26 170 120 166 Q214 170 214 250 Z" fill="#FFFF1A" stroke="#061866" stroke-width="6" />
  <path d="M98 160 L142 160 L138 178 L102 178 Z" fill="#E8B48C" stroke="#061866" stroke-width="6" stroke-linejoin="round" />
  <circle cx="120" cy="104" r="58" fill="#E8B48C" stroke="#061866" stroke-width="6" />
  <ellipse cx="102" cy="112" rx="6" ry="8" fill="#061866" /><ellipse cx="138" cy="112" rx="6" ry="8" fill="#061866" />
  <path d="M104 134 Q120 146 136 134" fill="none" stroke="#061866" stroke-width="6" stroke-linecap="round" />
  <path d="M62 90 Q66 40 120 38 Q174 40 178 90 Z" fill="#061866" />
  <path d="M56 88 L196 88 Q202 100 186 102 L56 102 Z" fill="#061866" />
</svg>"""

CAMION = """<svg class="illu" viewBox="0 0 320 200" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
  <rect width="320" height="200" fill="#DCE6F7" />
  <circle cx="270" cy="42" r="18" fill="#FFFF1A" />
  <rect y="158" width="320" height="42" fill="#53565A" />
  <path d="M10 180 H50 M80 180 H120 M150 180 H190 M220 180 H260 M290 180 H320" stroke="#FFFFFF" stroke-width="4" />
  <rect x="18" y="62" width="186" height="88" rx="6" fill="#FFFFFF" stroke="#061866" stroke-width="5" />
  <rect x="18" y="116" width="186" height="10" fill="#061866" />
  <path d="M210 150 V92 Q210 80 222 80 H262 Q274 80 280 92 L296 118 V150 Z" fill="#061866" />
  <rect x="244" y="88" width="30" height="26" rx="4" fill="#BFD3F2" />
  <circle cx="58" cy="154" r="15" fill="#111111" /><circle cx="96" cy="154" r="15" fill="#111111" />
  <circle cx="180" cy="154" r="15" fill="#111111" /><circle cx="266" cy="154" r="15" fill="#111111" />
</svg>"""

PIN = '<svg class="pin" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z" fill="#6E6E73" /></svg>'
COCHE = '<svg class="coche" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="#34C759" /><path d="M6.5 12.5 L10.5 16.5 L17.5 8.5" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" /></svg>'
PLUS = '<span class="plus">+</span>'
HORLOGE = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2.4" /><path d="M12 12 V7 M12 12 L15.5 14" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" /></svg>'
AJOUT = '<svg class="ico" viewBox="0 0 26 26" aria-hidden="true"><circle cx="10" cy="9" r="4" fill="currentColor" /><path d="M3 21 Q3 14 10 14 Q17 14 17 21 Z" fill="currentColor" /><path d="M20 8 V16 M16 12 H24" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" /></svg>'
FLECHE_BAS = '<svg class="fl-bas" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4 V19 M6 13 L12 19 L18 13" fill="none" stroke="#FFFF1A" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" /></svg>'


def carte(av, haut, fort, bas="à l'instant", lieu=None, d=0, extra=""):
    l_haut = f'<span class="gris">{haut}</span>' if haut else ""
    l_lieu = f'<span class="lieu">{PIN}{lieu}</span>' if lieu else ""
    return f"""<div class="carte entre" style="--d: {d}s">
          {av}
          <div class="c-txt">{l_haut}<span class="fort">{fort}</span><span class="c-bas"><span class="gris">{bas}</span>{l_lieu}</span></div>{extra}
        </div>"""


def anneau_progres(pct, couleur="#FFFF1A"):
    return f"""<div class="progres" style="--p: {pct}; --c: {couleur}">
          <svg viewBox="0 0 120 120" aria-hidden="true">
            <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.18)" stroke-width="12" />
            <circle class="arc" cx="60" cy="60" r="50" fill="none" stroke="{couleur}" stroke-width="12" stroke-linecap="round" pathLength="100" />
          </svg>
          <span>{pct}%</span>
        </div>"""


def profil(photo=True, bio=True, camion=True, coches=False, d0=0.0):
    """Carte Profil Trucker qui se complète : photo, puis bio, puis camion."""
    c = lambda: COCHE if coches else ""
    ph = f'<div class="p-photo entre" style="--d: {d0}s">{PORTRAIT}</div>' if photo else '<div class="p-photo vide">' + PLUS + "</div>"
    bi = (
        f'<p class="p-bio entre" style="--d: {d0 + 0.5}s">Conducteur routier 🚛 | Toujours sur la route | À la recherche des meilleurs spots !{c()}</p>'
        if bio
        else '<p class="p-bio vide">+ Ajoute ta bio</p>'
    )
    ca = (
        f'<div class="p-camion entre" style="--d: {d0 + 1.0}s"><div class="vignette">{CAMION}</div><div><b>Le Bolide</b><span>4,00 m · 2,55 m · 16,50 m</span></div>{c()}</div>'
        if camion
        else '<div class="p-camion vide">' + PLUS + " Ajoute ton camion</div>"
    )
    return f"""<div class="profil">
          <div class="p-haut">{ph}<div class="p-nom"><b>Charlie G. <span class="fr"><i></i><i></i><i></i></span></b><span>Membre depuis 2026</span></div>{c() if coches else ""}</div>
          {bi}
          {ca}
        </div>"""


# --- Les 12 interstitiels -------------------------------------------------------------------

def ecran(num, titre, texte, cta, visuel, nom, plein=False, accroche=None, badge=None):
    acc = f'<p class="accroche">{accroche}</p>' if accroche else ""
    bad = f'<span class="badge">{badge}</span>' if badge else ""
    if plein:
        return f"""<section class="ecran plein" id="i{num:02d}" data-nom="{nom}">
      <div class="statut"><span>9:41</span><span>●●● 4G</span></div>
      <button class="fermer" aria-label="Fermer">×</button>
      <div class="v-plein">{visuel}</div>
      <div class="bas">
        {bad}
        <h1>{titre}</h1>
        <p class="texte">{texte}</p>
        <a class="cta jaune">{cta}</a>
        <a class="plus-tard">Plus tard</a>
      </div>
    </section>"""
    return f"""<section class="ecran" id="i{num:02d}" data-nom="{nom}">
      <div class="statut"><span>9:41</span><span>●●● 4G</span></div>
      <button class="fermer" aria-label="Fermer">×</button>
      <div class="visuel">{visuel}</div>
      <div class="feuille">
        {bad}
        <h1>{titre}</h1>
        <p class="texte">{texte}</p>
        {acc}
        <a class="cta">{cta}</a>
        <a class="plus-tard">Plus tard</a>
      </div>
    </section>"""


def reseau():
    return f"""<div class="reseau">
          <svg class="liens" viewBox="0 0 330 250" aria-hidden="true">
            <path d="M165 60 L70 175 M165 60 L260 175 M70 175 L260 175" pathLength="1" />
          </svg>
          <div class="noeud entre" style="--d: 0s; left: 125px; top: 20px">{avatar("louna", None, "av-xl")}<i class="en-ligne"></i></div>
          <div class="noeud entre" style="--d: 0.25s; left: 30px; top: 135px">{avatar("nicolas", None, "av-xl")}<i class="en-ligne"></i></div>
          <div class="noeud entre" style="--d: 0.5s; left: 220px; top: 135px">{avatar("david", None, "av-xl")}<i class="en-ligne"></i></div>
        </div>"""


ETAT_BTN = lambda cls, contenu, label, d: f"""<div class="etat entre" style="--d: {d}s">
            <div class="ligne-ami">{avatar("vanessa", None, "av-s")}<b>Vanessa Y.</b><span class="btn {cls}">{contenu}</span></div>
            <span class="etat-label">{label}</span>
          </div>"""

ECRANS = [
    ecran(
        1,
        "MICHELIN Truckfly devient plus social&nbsp;!",
        "Retrouve tes amis, partage ton profil et découvre leur activité au quotidien.",
        "Créer mon Profil Trucker",
        reseau(),
        "decouverte",
        plein=True,
        badge="Nouveau",
    ),
    ecran(
        2,
        "Ton Profil Trucker est là&nbsp;!",
        "Ajoute ta photo, ta bio et ton camion pour créer un profil qui te ressemble.",
        "Créer mon profil",
        profil()
        + """<div class="etapes">
          <span class="entre" style="--d: 0s">① Photo</span><span class="entre" style="--d: 0.5s">② Bio</span><span class="entre" style="--d: 1s">③ Camion</span>
        </div>""",
        "profil-trucker",
        badge="Nouveau",
    ),
    ecran(
        3,
        "Personnalise ton Profil Trucker",
        "Ajoute ton prénom, ta bio, ta photo et ton camion.",
        "Personnaliser mon profil",
        f"""<div class="check">
          <div class="check-tete">{anneau_progres(50, "#061866")}<div><b>Ton Profil Trucker</b><span>2 étapes sur 4</span></div></div>
          <ul>
            <li class="fait entre" style="--d: 0s">{COCHE}Prénom et nom</li>
            <li class="fait entre" style="--d: 0.2s">{COCHE}Bio</li>
            <li class="entre" style="--d: 0.4s">{PLUS}Photo de profil</li>
            <li class="entre" style="--d: 0.6s">{PLUS}Camion</li>
          </ul>
        </div>""",
        "personnalisation",
        accroche="Plus ton profil est complet, plus tes amis pourront te retrouver facilement&nbsp;!",
    ),
    ecran(
        4,
        "Retrouve tes amis sur MICHELIN Truckfly",
        "Envoie-leur une invitation et construis ton réseau de conducteurs.",
        "Ajouter mes amis",
        f"""<div class="etats">
          {ETAT_BTN("plein", AJOUT + "Ajouter", "Tu ajoutes", 0)}
          {FLECHE_BAS.replace('class="fl-bas"', 'class="fl-bas entre" style="--d: 0.3s"')}
          {ETAT_BTN("attente", HORLOGE + "En attente", "Ton invitation attend", 0.5)}
          {FLECHE_BAS.replace('class="fl-bas"', 'class="fl-bas entre" style="--d: 0.8s"')}
          {ETAT_BTN("ami", "✓ Amis", "Invitation acceptée", 1.0)}
        </div>""",
        "ajouter-amis",
    ),
    ecran(
        5,
        "Tu as reçu une invitation&nbsp;?&nbsp;👀",
        "Pense à regarder tes invitations pour ne manquer aucune demande d’ami&nbsp;!",
        "Voir mes invitations",
        f"""<div class="invits entre" style="--d: 0s">
          <div class="invits-tete"><b>Invitations</b></div>
          <div class="invits-sous">En attente <span class="compteur">2</span></div>
          <div class="invit surbrille">{avatar("louna", "invitation", "av-m")}<b>Louna C.</b><span class="btn plein petit">Accepter</span><span class="btn creux petit">Ignorer</span></div>
          <div class="invit">{avatar("david", "invitation", "av-m")}<b>David</b><span class="btn plein petit">Accepter</span><span class="btn creux petit">Ignorer</span></div>
        </div>
        <div class="cloche entre" style="--d: 0.4s">🔔<i>2</i></div>""",
        "invitations",
    ),
    ecran(
        6,
        "Bienvenue dans le Social Core",
        "Découvre ce que font tes amis et reste connecté à ta communauté de conducteurs.",
        "Découvrir",
        """<div class="tuiles">
          <div class="tuile entre" style="--d: 0s"><span class="emo">👥</span><b>Tes amis</b></div>
          <div class="tuile entre" style="--d: 0.3s"><span class="emo">📍</span><b>Leurs activités</b></div>
          <div class="tuile entre" style="--d: 0.6s"><span class="emo pulse">🟢</span><b>Qui est en ligne</b></div>
        </div>""",
        "social-core",
        badge="Nouveau",
    ),
    ecran(
        7,
        "Que font tes amis aujourd’hui&nbsp;?",
        "Découvre leur activité au quotidien et regarde qui est en ligne.",
        "Voir l’activité",
        f"""<div class="pile">
          {carte(avatar("david", "visite", "av-m"), "David s’est arrêté ici :", "Le Relais des Cigales", d=0)}
          {carte(avatar("nicolas", "visite", "av-m"), "Nicolas J. a visité :", "AS 24", d=0.35)}
          {carte(avatar("louna", "invitation", "av-m"), None, "Louna vous a envoyé une invitation", d=0.7)}
        </div>""",
        "activite-amis",
    ),
    ecran(
        8,
        "Partage tes bons plans avec tes amis",
        "Découvre leurs recommandations et partage les tiennes avec la communauté.",
        "Découvrir les recommandations",
        f"""<div class="avis entre" style="--d: 0s">
          <div class="avis-tete">{avatar("david", "avis", "av-m")}<div><span class="gris">David a déposé un avis chez :</span><b>Le Relais des Cigales</b></div></div>
          <div class="etoiles">★★★★★</div>
          <div class="avis-actions"><span>👍 Utile</span><span>💬 Répondre</span></div>
        </div>""",
        "recommandations",
    ),
    ecran(
        9,
        "Et ton camion&nbsp;?&nbsp;🚛",
        "Ajoute son nom, sa photo et ses dimensions à ton Profil Trucker.",
        "Ajouter mon camion",
        f"""<div class="fiche entre" style="--d: 0s">
          <div class="fiche-haut"><div class="carre">{CAMION}</div><div><span class="gris">Nom du camion</span><b>Le Bolide</b></div></div>
          <div class="dims">
            <div class="entre" style="--d: 0.3s"><span>Hauteur</span><b>4,00 m</b></div>
            <div class="entre" style="--d: 0.5s"><span>Largeur</span><b>2,55 m</b></div>
            <div class="entre" style="--d: 0.7s"><span>Longueur</span><b>16,50 m</b></div>
          </div>
        </div>""",
        "camion",
    ),
    ecran(
        10,
        "Ton profil n’attend plus que toi&nbsp;!",
        "Ajoute ta photo, ta bio et ton camion en quelques secondes.",
        "Compléter mon profil",
        f"""<div class="rappel">
          {anneau_progres(25)}
          <div class="manque">
            <span class="entre" style="--d: 0.2s">{PLUS}Photo</span><span class="entre" style="--d: 0.4s">{PLUS}Bio</span><span class="entre" style="--d: 0.6s">{PLUS}Camion</span>
          </div>
        </div>""",
        "rappel",
    ),
    ecran(
        11,
        "Ton profil est prêt&nbsp;!&nbsp;🎉",
        "Maintenant, ajoute tes amis et retrouve ta communauté sur MICHELIN Truckfly.",
        "Ajouter mes amis",
        f"""{profil(coches=True)}
        <div class="complet entre" style="--d: 0.3s">{COCHE}Profil complété à 100 %</div>""",
        "profil-pret",
    ),
    ecran(
        12,
        "Ne roule plus seul&nbsp;!",
        "Crée ton Profil Trucker, retrouve tes amis et découvre leur activité au quotidien.",
        "Créer mon Profil Trucker",
        reseau()
        + f"""<div class="mini-notifs">
          {carte(avatar("louna", "invitation", "av-s"), None, "Louna vous a envoyé une invitation", d=0.8)}
        </div>""",
        "ne-roule-plus-seul",
        plein=True,
    ),
]

CSS = """
@font-face { font-family: "Bib"; src: url("assets/fonts/BIB-Bold.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Bib"; src: url("assets/fonts/BIB-Light.woff2") format("woff2"); font-weight: 300; }
@font-face { font-family: "Inter"; src: url("assets/fonts/Inter-Regular.otf") format("opentype"); font-weight: 400; }
@font-face { font-family: "Inter"; src: url("assets/fonts/Inter-SemiBold.otf") format("opentype"); font-weight: 600; }
@font-face { font-family: "Inter"; src: url("assets/fonts/Inter-Bold.otf") format("opentype"); font-weight: 700; }
:root {
  --bleu: #061866;
  --bleu-nuit: #000e38;
  --jaune: #ffff1a;
  --blanc-casse: #f5f3f1;
  --bleu-clair: #dce6f7;
  --gris: #6e6e73;
  --vert: #34c759;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #e9e7e4;
  font-family: "Inter", "Noto Color Emoji", sans-serif;
  color: #000;
  padding: 40px 16px 80px;
}
.entete-planche { max-width: 1320px; margin: 0 auto 28px; font-family: "Bib", sans-serif; }
.entete-planche h2 { font-size: 32px; color: var(--bleu); }
.entete-planche p { font-family: "Inter", sans-serif; color: #3a3a3c; margin-top: 6px; }
.planche {
  max-width: 1320px; margin: 0 auto;
  display: grid; grid-template-columns: repeat(auto-fill, 390px); gap: 32px 24px; justify-content: center;
}
.cartel { font-size: 13px; color: #3a3a3c; margin-bottom: 8px; font-weight: 600; }
.ecran {
  position: relative; width: 390px; height: 844px; overflow: hidden;
  border-radius: 40px; background: var(--bleu); color: #000;
  box-shadow: 0 20px 50px rgba(6, 24, 102, 0.22);
}
.capture .ecran { border-radius: 0; box-shadow: none; }
.statut {
  position: absolute; left: 0; right: 0; top: 0; height: 48px; padding: 16px 28px 0;
  display: flex; justify-content: space-between; color: #fff; font-weight: 600; font-size: 15px; z-index: 3;
}
.fermer {
  position: absolute; right: 18px; top: 56px; z-index: 3; width: 34px; height: 34px; border-radius: 50%;
  border: 0; background: rgba(255, 255, 255, 0.16); color: #fff; font-size: 24px; line-height: 34px;
}
.visuel {
  position: absolute; left: 0; right: 0; top: 0; height: 470px;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px;
  padding: 96px 24px 54px;
  background: radial-gradient(120% 70% at 50% 0%, #10287f 0%, var(--bleu) 55%, var(--bleu-nuit) 100%);
}
.feuille {
  position: absolute; left: 0; right: 0; bottom: 0; min-height: 404px;
  background: #fff; border-radius: 28px 28px 0 0; padding: 30px 26px 30px;
  display: flex; flex-direction: column;
}
h1 { font-family: "Bib", "Noto Color Emoji", sans-serif; font-weight: 700; font-size: 30px; line-height: 1.12; color: #000; }
.texte { font-size: 16.5px; line-height: 1.45; color: #3a3a3c; margin-top: 12px; }
.accroche {
  margin-top: 14px; padding: 12px 14px; border-radius: 14px; background: var(--bleu-clair);
  color: var(--bleu); font-weight: 600; font-size: 14.5px; line-height: 1.4;
}
.badge {
  align-self: flex-start; margin-bottom: 12px; padding: 5px 12px; border-radius: 999px;
  background: var(--bleu); color: #fff; font-weight: 700; font-size: 12.5px;
}
.cta {
  margin-top: auto; height: 56px; border-radius: 14px; background: var(--bleu); color: #fff;
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 17px; text-decoration: none;
}
.cta.jaune { background: var(--jaune); color: #000; margin-top: 26px; }
.plus-tard { margin-top: 12px; text-align: center; color: var(--gris); font-size: 15px; font-weight: 600; text-decoration: none; }
.plein .plus-tard { color: rgba(255, 255, 255, 0.75); }

/* Écrans pleine page bleue (1 et 12) */
.plein { background: radial-gradient(110% 60% at 50% 18%, #10287f 0%, var(--bleu) 50%, var(--bleu-nuit) 100%); }
.v-plein { position: absolute; left: 0; right: 0; top: 96px; height: 380px; display: flex; flex-direction: column; align-items: center; }
.bas { position: absolute; left: 0; right: 0; bottom: 0; padding: 0 26px 34px; display: flex; flex-direction: column; }
.plein h1 { color: #fff; font-size: 36px; }
.plein .texte { color: rgba(255, 255, 255, 0.86); }
.plein .badge { background: var(--jaune); color: #000; }

/* Réseau d'avatars */
.reseau { position: relative; width: 330px; height: 250px; }
.liens { position: absolute; inset: 0; }
.liens path { fill: none; stroke: rgba(255, 255, 255, 0.35); stroke-width: 3; stroke-dasharray: 1; animation: trace 1.2s ease 0.6s both; }
.noeud { position: absolute; width: 84px; height: 84px; }
.av-xl { width: 84px; height: 84px; display: block; }
.noeud::before { content: ""; position: absolute; inset: -6px; border-radius: 50%; background: #fff; z-index: -1; }
.en-ligne { position: absolute; right: 2px; top: 2px; width: 20px; height: 20px; border-radius: 50%; background: var(--vert); border: 3px solid #fff; animation: pouls 1.8s ease-in-out 1.4s infinite; }
.mini-notifs { width: 330px; margin-top: 14px; }

/* Cartes au style du fil d'activité */
.carte {
  display: flex; align-items: center; gap: 12px; width: 100%;
  background: #fff; border-radius: 16px; padding: 12px 14px; box-shadow: 0 8px 22px rgba(0, 0, 0, 0.16);
}
.av-m { width: 52px; height: 52px; flex: none; }
.av-s { width: 40px; height: 40px; flex: none; }
.c-txt { display: flex; flex-direction: column; gap: 2px; min-width: 0; flex: 1; }
.gris { color: var(--gris); font-size: 13px; }
.fort { font-weight: 700; font-size: 15px; line-height: 1.25; }
.c-bas { display: flex; justify-content: space-between; align-items: center; }
.lieu { display: flex; align-items: center; gap: 2px; color: var(--gris); font-size: 13px; }
.pin { width: 13px; height: 13px; }
.pile { width: 100%; display: flex; flex-direction: column; gap: 12px; }

/* Profil Trucker */
.profil { width: 320px; background: #fff; border-radius: 20px; padding: 16px; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.2); }
.p-haut { display: flex; align-items: center; gap: 14px; position: relative; }
.p-haut > .coche { position: absolute; right: 0; top: 4px; }
.p-photo { width: 66px; height: 66px; border-radius: 50%; overflow: hidden; border: 3px solid var(--bleu); flex: none; }
.p-photo.vide { border: 2px dashed #8e9bb8; background: #eef2f9; display: flex; align-items: center; justify-content: center; }
.illu { display: block; width: 100%; height: 100%; }
.p-nom { display: flex; flex-direction: column; gap: 2px; }
.p-nom b { font-size: 20px; display: flex; align-items: center; gap: 6px; }
.p-nom > span { color: var(--gris); font-size: 12.5px; }
.fr { display: inline-flex; width: 18px; height: 12px; border-radius: 2px; overflow: hidden; }
.fr i { flex: 1; } .fr i:nth-child(1) { background: #002395; } .fr i:nth-child(2) { background: #fff; outline: 1px solid #eee; } .fr i:nth-child(3) { background: #ed2939; }
.p-bio { margin-top: 12px; font-size: 12.5px; line-height: 1.4; color: #3a3a3c; display: flex; gap: 8px; align-items: flex-start; }
.p-bio.vide { color: var(--bleu); font-weight: 700; }
.p-camion { margin-top: 12px; display: flex; align-items: center; gap: 12px; padding: 10px; border-radius: 14px; background: var(--blanc-casse); }
.p-camion > div:not(.vignette) { display: flex; flex-direction: column; flex: 1; }
.p-camion b { font-size: 15px; } .p-camion span { color: var(--gris); font-size: 12px; }
.p-camion.vide { color: var(--bleu); font-weight: 700; font-size: 14px; border: 2px dashed #8e9bb8; background: #eef2f9; }
.vignette, .carre { width: 52px; height: 52px; border-radius: 10px; overflow: hidden; flex: none; background: var(--bleu-clair); }
.coche { width: 22px; height: 22px; flex: none; }
.plus { display: inline-flex; width: 22px; height: 22px; border-radius: 50%; align-items: center; justify-content: center; background: var(--bleu-clair); color: var(--bleu); font-weight: 700; font-size: 16px; flex: none; }
.etapes { display: flex; gap: 8px; }
.etapes span { padding: 7px 12px; border-radius: 999px; background: rgba(255, 255, 255, 0.12); color: #fff; font-weight: 600; font-size: 13px; }
.etapes span:nth-child(odd) { color: var(--jaune); }
.complet { display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 999px; background: #fff; font-weight: 700; font-size: 14px; color: #000; }

/* Checklist et progression */
.check { width: 320px; background: #fff; border-radius: 20px; padding: 18px; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.2); }
.check-tete { display: flex; align-items: center; gap: 14px; margin-bottom: 10px; }
.check-tete b { display: block; font-size: 17px; } .check-tete span { color: var(--gris); font-size: 13px; }
.check .progres { width: 64px; height: 64px; }
.check .progres circle:first-child { stroke: #e6e9f0; }
.check .progres span { color: var(--bleu); font-size: 15px; }
.check ul { list-style: none; display: flex; flex-direction: column; }
.check li { display: flex; align-items: center; gap: 10px; padding: 11px 2px; border-top: 1px solid #eceef2; font-weight: 600; font-size: 15px; }
.check li:not(.fait) { color: var(--bleu); }
.progres { position: relative; width: 150px; height: 150px; flex: none; }
.progres svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.progres .arc { stroke-dasharray: var(--p) 100; animation: remplit 1.2s ease 0.2s both; }
.progres span { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: "Bib", sans-serif; font-weight: 700; font-size: 34px; color: #fff; }
.rappel { display: flex; flex-direction: column; align-items: center; gap: 20px; }
.manque { display: flex; gap: 8px; }
.manque span { display: flex; align-items: center; gap: 6px; padding: 8px 14px 8px 8px; border-radius: 999px; background: #fff; font-weight: 700; font-size: 14px; color: var(--bleu); }

/* États du bouton d'ajout */
.etats { width: 100%; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.etat { width: 320px; display: flex; flex-direction: column; align-items: center; gap: 6px; }
.ligne-ami { width: 100%; display: flex; align-items: center; gap: 10px; background: #fff; border-radius: 14px; padding: 9px 12px; }
.ligne-ami b { flex: 1; font-size: 15px; }
.etat-label { color: rgba(255, 255, 255, 0.85); font-size: 12.5px; font-weight: 600; }
.etat:last-child .etat-label { color: var(--jaune); }
.fl-bas { width: 22px; height: 22px; }
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 12px; border-radius: 10px; font-weight: 700; font-size: 13.5px; white-space: nowrap; }
.btn.plein { background: var(--bleu); color: #fff; }
.btn.attente { background: #fff; color: var(--bleu); border: 2px solid var(--bleu); }
.btn.ami { background: var(--bleu-clair); color: var(--bleu); }
.btn.creux { background: #fff; color: var(--bleu); border: 1.5px solid var(--bleu); }
.btn.petit { padding: 6px 10px; font-size: 12.5px; }
.ico { width: 16px; height: 16px; }

/* Invitations */
.invits { width: 330px; background: var(--blanc-casse); border-radius: 20px; overflow: hidden; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.25); }
.invits-tete { background: var(--bleu); color: #fff; text-align: center; padding: 14px; font-size: 18px; border-bottom: 1px solid rgba(255,255,255,0.15); }
.invits-sous { display: flex; align-items: center; gap: 8px; padding: 12px 14px 6px; font-weight: 700; font-size: 15px; }
.compteur { display: inline-flex; width: 22px; height: 22px; border-radius: 50%; background: var(--jaune); align-items: center; justify-content: center; font-size: 12.5px; }
.invit { display: flex; align-items: center; gap: 8px; padding: 10px 14px; }
.invit b { flex: 1; font-size: 14.5px; }
.invit.surbrille { background: #d4e7fa; }
.cloche { position: absolute; right: 34px; top: 104px; font-size: 34px; }
.cloche i { position: absolute; right: -6px; top: -4px; width: 22px; height: 22px; border-radius: 50%; background: var(--jaune); color: #000; font-style: normal; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; }

/* Social Core */
.tuiles { display: flex; flex-direction: column; gap: 12px; width: 300px; }
.tuile { display: flex; align-items: center; gap: 14px; padding: 14px 16px; border-radius: 18px; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.18); color: #fff; }
.tuile b { font-size: 18px; }
.emo { width: 50px; height: 50px; border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center; font-size: 26px; flex: none; }

/* Avis */
.avis { width: 330px; background: #fff; border-radius: 20px; padding: 16px; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.25); }
.avis-tete { display: flex; align-items: center; gap: 12px; }
.avis-tete > div { display: flex; flex-direction: column; gap: 2px; }
.avis-tete b { font-size: 17px; }
.etoiles { margin-top: 12px; color: var(--bleu); font-size: 24px; letter-spacing: 3px; }
.avis-actions { margin-top: 12px; padding-top: 10px; border-top: 1px solid #eceef2; display: flex; gap: 18px; color: var(--bleu); font-weight: 600; font-size: 14px; }

/* Fiche camion */
.fiche { width: 330px; background: #fff; border-radius: 20px; padding: 16px; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.25); }
.fiche-haut { display: flex; align-items: center; gap: 14px; }
.fiche-haut .carre { width: 92px; height: 92px; border-radius: 14px; }
.fiche-haut > div:last-child { display: flex; flex-direction: column; gap: 2px; }
.fiche-haut b { font-size: 22px; font-family: "Bib", sans-serif; }
.dims { margin-top: 14px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.dims div { border: 1.5px solid #d6dae2; border-radius: 12px; padding: 8px 10px; display: flex; flex-direction: column; }
.dims span { color: var(--gris); font-size: 12px; } .dims b { font-size: 16px; }

/* Animations d'entrée (désactivées pour les captures PNG) */
.entre { animation: entre 0.55s cubic-bezier(0.2, 0.9, 0.3, 1.2) both; animation-delay: calc(var(--d, 0s) + 0.25s); }
.pulse { animation: pouls 1.8s ease-in-out infinite; }
@keyframes entre { from { opacity: 0; transform: translateY(14px) scale(0.96); } }
@keyframes trace { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }
@keyframes remplit { from { stroke-dasharray: 0 100; } }
@keyframes pouls { 50% { transform: scale(1.15); } }
.fige *, .fige *::before { animation: none !important; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
"""


def page():
    cartes = "\n".join(
        f'<div><div class="cartel">{i + 1:02d} · {e.split(chr(34) + " data-nom=" + chr(34))[1].split(chr(34))[0]}</div>{e}</div>'
        for i, e in enumerate(ECRANS)
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Interstitiels Profil Trucker</title>
<style>{CSS}</style>
</head>
<body>
  <header class="entete-planche">
    <h2>Interstitiels Profil Trucker et Social Core</h2>
    <p>12 écrans à l'ouverture de l'app · j'ouvre l'app → je comprends la nouveauté → j'ai envie de créer mon profil.</p>
  </header>
  <main class="planche">
{cartes}
  </main>
</body>
</html>
"""


(RACINE / "index.html").write_text(page())
print("index.html généré :", len(ECRANS), "interstitiels")
