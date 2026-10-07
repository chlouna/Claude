"""Génère les deux compositions de la vidéo « Truckfly pour les établissements » (nouvelle charte).

    python3 scripts/generer.py

Écrit index.html (16:9, 1920 × 1080) et compositions/vertical.html (9:16, 1080 × 1920).
Le minutage, les textes et les interactions sont communs ; seule la mise en page change.

Polices : Bib (charte) pour les titres, Noto Sans (charte) pour l'espace pro recréé.
L'interface est dimensionnée en em à partir de --ui : les repères de clic et les flèches sont
placés dans l'élément qu'ils désignent, ils suivent donc la mise en page des deux formats.
"""

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DUREE = 62.6

B, S, W, O = "#061866", "#000E38", "#FFFFFF", "#F5F3F1"
T1, T2 = "#DCE3F5", "#AEBBE3"  # teintes de Michelin Blue, pour le volume des illustrations


# --- Petits outils de texte -------------------------------------------------------------

def mots(texte, classe=""):
    """Un mot par span, pour les faire arriver un par un."""
    return " ".join(f'<span class="mot {classe}">{m}</span>' for m in texte.split(" "))


def lettres(texte):
    """Une lettre par span, pour l'effet de frappe (display none → inline)."""
    return "".join(f'<span class="ch">{c}</span>' for c in texte)


def compteur(valeur):
    """Chiffres à rouleaux : chaque chiffre défile jusqu'à sa valeur (sans calcul au rendu)."""
    morceaux = []
    for c in valeur:
        if c.isdigit():
            bande = "".join(f"<span>{i % 10}</span>" for i in range(20))
            morceaux.append(f'<span class="chiffre" data-layout-allow-overflow data-v="{c}"><span class="cale">{c}</span><span class="bande">{bande}</span></span>')
        elif c == " ":
            morceaux.append('<span class="espace"></span>')
        else:
            morceaux.append(f"<span>{c}</span>")
    return "".join(morceaux)


CLIC = '<span class="clic"><span class="onde"></span><svg class="pointeur" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 2.5 L5 19 L9.3 15.2 L12.2 21.5 L15 20.2 L12.2 14 L18 14 Z" fill="#FFFFFF" stroke="#061866" stroke-width="1.8" stroke-linejoin="round" /></svg></span>'

FLECHE = '<svg class="fleche" viewBox="0 0 200 120" aria-hidden="true"><path class="trait" d="M8 10 C 80 6, 150 40, 178 104" pathLength="1" /><path class="tete" d="M160 98 L180 108 L182 86" /></svg>'

LOUPE = '<svg class="loupe" viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6.5" fill="none" stroke="#061866" stroke-width="2.6" /><path d="M15 15 L21 21" stroke="#061866" stroke-width="2.8" stroke-linecap="round" /></svg>'

COCHE = '<svg class="coche" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5 L10 17.5 L19 7" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" /></svg>'

ETOILE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5 L14.9 8.6 L21.5 9.4 L16.6 13.9 L17.9 20.5 L12 17.2 L6.1 20.5 L7.4 13.9 L2.5 9.4 L9.1 8.6 Z" fill="#061866" /></svg>'
ETOILE_VIDE = ETOILE.replace('fill="#061866"', 'fill="none" stroke="#061866" stroke-width="1.6"')

# --- Icônes (blanches, 24 × 24) ------------------------------------------------------------

ICONES = {
    "couverts": '<path d="M7 2 V10 M4.5 2 V8 Q4.5 10.5 7 10.5 Q9.5 10.5 9.5 8 V2 M7 10.5 V22 M16 2 Q19.5 4 19.5 10 L16.5 11 V22" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />',
    "pompe": '<path d="M4 21 V4.5 Q4 3 5.5 3 H12.5 Q14 3 14 4.5 V21 M2.5 21 H15.5 M6.5 6 H11.5 V10 H6.5 Z M14 9 H16 Q17.5 9 17.5 10.5 V16.5 Q17.5 18 19 18 Q20.5 18 20.5 16.5 V8 L18 5.5" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />',
    "goutte": '<path d="M12 2.5 Q6 10 6 14.5 A6 6 0 0 0 18 14.5 Q18 10 12 2.5 Z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round" /><path d="M9.5 15 Q9.8 17.2 12 17.6" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" />',
    "cle": '<path d="M14.5 3.5 A5 5 0 0 0 10 10.2 L3.5 16.7 A2 2 0 0 0 6.3 19.5 L12.8 13 A5 5 0 0 0 19.5 8.5 L16.5 11.5 L13.2 10.8 L12.5 7.5 L15.5 4.5 Q15 3.5 14.5 3.5 Z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round" />',
    "douche": '<path d="M5 21 V7 Q5 3 9 3 Q13 3 13 7 V8 M9.5 8 H16.5 M10 11.5 V12.5 M13 11.5 V12.5 M16 11.5 V12.5 M11.5 15 V16 M14.5 15 V16" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" />',
    "parking": '<rect x="3" y="3" width="18" height="18" rx="3.5" fill="none" stroke="{c}" stroke-width="2" /><path d="M9.5 17 V7 H13 Q16 7 16 10 Q16 13 13 13 H9.5" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />',
    "wifi": '<path d="M2.5 9 Q12 1 21.5 9 M5.5 12.5 Q12 7 18.5 12.5 M8.5 16 Q12 13 15.5 16" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" /><circle cx="12" cy="19.3" r="1.5" fill="{c}" />',
    "toilettes": '<circle cx="7" cy="4.5" r="2" fill="{c}" /><circle cx="17" cy="4.5" r="2" fill="{c}" /><path d="M5 8.5 H9 V15 H8 V21 H6 V15 H5 Z M17 8.5 L20 16 H18 V21 H16 V16 H14 Z M12 3 V21" fill="{c}" stroke="{c}" stroke-width="1" stroke-linejoin="round" />',
    "camera": '<path d="M3 8 Q3 6.5 4.5 6.5 H7 L8.5 4 H15.5 L17 6.5 H19.5 Q21 6.5 21 8 V18 Q21 19.5 19.5 19.5 H4.5 Q3 19.5 3 18 Z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round" /><circle cx="12" cy="12.8" r="3.6" fill="none" stroke="{c}" stroke-width="2" />',
    "image": '<rect x="2.5" y="4" width="19" height="16" rx="2.5" fill="none" stroke="{c}" stroke-width="2" /><circle cx="8.5" cy="9.5" r="1.8" fill="{c}" /><path d="M3 18 L9.5 12.5 L13.5 16 L16.5 13.5 L21 17.5" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round" />',
}


def icone(nom, couleur=W, classe="icone"):
    return f'<svg class="{classe}" viewBox="0 0 24 24" aria-hidden="true">{ICONES[nom].format(c=couleur)}</svg>'


# --- Illustrations à plat (viewBox 1200 × 560, le sol est sous l'image) --------------------

def camion(x, y, echelle=1.0, sens=1):
    """Camion vu de côté, cabine à gauche (sens=1) ; (x, y) = point au sol, à l'avant."""
    t = f'translate({x} {y}) scale({echelle * sens} {echelle})'
    return f"""<g transform="{t}">
      <rect x="150" y="-215" width="380" height="172" rx="8" fill="{W}" stroke="{B}" stroke-width="8" />
      <rect x="185" y="-180" width="310" height="22" rx="11" fill="{T1}" />
      <path d="M8 -50 V-150 Q8 -190 48 -190 H140 V-50 Z" fill="{B}" />
      <path d="M26 -110 V-148 Q26 -170 50 -170 H102 V-110 Z" fill="{T1}" />
      <rect x="112" y="-160" width="18" height="70" rx="6" fill="{S}" />
      <rect x="0" y="-52" width="540" height="18" rx="6" fill="{S}" />
      <rect x="0" y="-80" width="22" height="14" rx="4" fill="{W}" />
      {''.join(f'<circle cx="{cx}" cy="-22" r="30" fill="{S}" /><circle cx="{cx}" cy="-22" r="11" fill="{T2}" />' for cx in (70, 390, 462))}
    </g>"""


def enseigne(x, y, nom):
    return f"""<g transform="translate({x} {y})">
      <rect x="-60" y="-60" width="120" height="120" rx="28" fill="{B}" />
      <svg x="-38" y="-38" width="76" height="76" viewBox="0 0 24 24">{ICONES[nom].format(c=W)}</svg>
    </g>"""


def arbre(x):
    return f'<g transform="translate({x} 470)"><rect x="-7" y="-120" width="14" height="120" fill="{B}" /><ellipse cx="0" cy="-150" rx="46" ry="70" fill="{T2}" /></g>'


NUAGES = f'<path d="M140 120 Q150 90 185 98 Q200 70 235 85 Q265 80 268 112 Q292 116 290 135 H140 Z" fill="{T1}" /><path d="M930 90 Q940 62 972 70 Q988 46 1018 60 Q1046 56 1048 84 Q1070 88 1068 106 H930 Z" fill="{T1}" />'

RESTAURANT = f"""
    {NUAGES}{arbre(205)}
    <rect x="300" y="200" width="600" height="270" fill="{W}" stroke="{B}" stroke-width="8" />
    <rect x="280" y="168" width="640" height="40" rx="6" fill="{B}" />
    {''.join(f'<rect x="{300 + i * 75}" y="208" width="75" height="62" fill="{B if i % 2 == 0 else W}" />' for i in range(8))}
    {''.join(f'<circle cx="{337.5 + i * 75}" cy="270" r="37.5" fill="{B if i % 2 == 0 else W}" />' for i in range(8))}
    <path d="M300 208 H900" stroke="{B}" stroke-width="8" />
    <rect x="340" y="335" width="150" height="100" rx="6" fill="{T1}" stroke="{B}" stroke-width="7" />
    <rect x="710" y="335" width="150" height="100" rx="6" fill="{T1}" stroke="{B}" stroke-width="7" />
    <path d="M415 335 V435 M785 335 V435" stroke="{B}" stroke-width="6" />
    <rect x="545" y="330" width="110" height="140" rx="6" fill="{T2}" stroke="{B}" stroke-width="7" />
    <circle cx="635" cy="405" r="7" fill="{B}" />
    {enseigne(600, 110, "couverts")}
"""

STATION = f"""
    {NUAGES}
    <rect x="200" y="150" width="800" height="56" rx="10" fill="{B}" />
    <rect x="200" y="206" width="800" height="14" fill="{S}" />
    <rect x="240" y="220" width="26" height="250" fill="{B}" />
    <rect x="934" y="220" width="26" height="250" fill="{B}" />
    {enseigne(600, 90, "pompe")}
    <g transform="translate(330 470)"><rect x="-55" y="-190" width="110" height="190" rx="12" fill="{W}" stroke="{B}" stroke-width="8" /><rect x="-35" y="-165" width="70" height="44" rx="6" fill="{T1}" /><rect x="-35" y="-100" width="70" height="14" rx="7" fill="{T2}" /><path d="M55 -130 Q95 -130 95 -80 V-40" fill="none" stroke="{S}" stroke-width="9" stroke-linecap="round" /></g>
    {camion(430, 470, 0.95)}
"""

LAVAGE = f"""
    {NUAGES}{arbre(150)}{arbre(1060)}
    <rect x="240" y="210" width="44" height="260" fill="{B}" />
    <rect x="916" y="210" width="44" height="260" fill="{B}" />
    <rect x="220" y="150" width="760" height="64" rx="10" fill="{B}" />
    {enseigne(600, 92, "goutte")}
    <g><rect x="306" y="232" width="62" height="238" rx="31" fill="{T2}" />{''.join(f'<path d="M314 {y} H360" stroke="{W}" stroke-width="6" stroke-linecap="round" />' for y in range(262, 460, 30))}</g>
    {camion(380, 470, 0.95)}
    <g><rect x="832" y="232" width="62" height="238" rx="31" fill="{T2}" />{''.join(f'<path d="M840 {y} H886" stroke="{W}" stroke-width="6" stroke-linecap="round" />' for y in range(262, 460, 30))}</g>
    {''.join(f'<path d="M{x} 240 Q{x - 9} 256 {x} 262 Q{x + 9} 256 {x} 240 Z" fill="{T2}" />' for x in (450, 560, 670, 780))}
"""

GARAGE = f"""
    {NUAGES}{arbre(170)}
    <rect x="260" y="190" width="680" height="280" fill="{W}" stroke="{B}" stroke-width="8" />
    <path d="M230 200 L600 110 L970 200 Z" fill="{B}" />
    <rect x="360" y="270" width="480" height="200" fill="{T1}" stroke="{B}" stroke-width="8" />
    {''.join(f'<path d="M364 {y} H836" stroke="{T2}" stroke-width="7" />' for y in range(300, 470, 32))}
    <rect x="360" y="270" width="480" height="62" fill="{S}" />
    {enseigne(600, 40, "cle")}
    {camion(590, 470, 0.95)}
"""

ILLUS = [("restaurant", "Restaurant", RESTAURANT), ("station", "Station-service", STATION), ("lavage", "Station de lavage", LAVAGE), ("garage", "Garage", GARAGE)]


def illustration(contenu, classe="illus", ratio="xMidYMax meet"):
    return f'<svg class="{classe}" viewBox="0 0 1200 560" preserveAspectRatio="{ratio}" aria-hidden="true">{contenu}</svg>'


# Photo de façade pour « Ma photo » : ciel Off White, sol bleu
FACADE = f'<svg class="facade" viewBox="150 60 900 440" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect x="0" y="0" width="1200" height="600" fill="{O}" />{RESTAURANT}<rect x="0" y="470" width="1200" height="130" fill="{B}" /></svg>'

# Photos de la communauté : quatre vignettes illustrées
VIGNETTES = [
    ("Pascal", f'<svg viewBox="0 0 400 260" preserveAspectRatio="xMidYMid slice"><rect width="400" height="260" fill="{T1}" /><circle cx="200" cy="130" r="105" fill="{W}" stroke="{B}" stroke-width="8" /><circle cx="200" cy="130" r="72" fill="none" stroke="{T2}" stroke-width="6" /><path d="M150 150 Q160 95 215 100 Q250 108 240 150 Z" fill="{B}" /><circle cx="235" cy="160" r="16" fill="{T2}" /><circle cx="210" cy="170" r="13" fill="{T2}" /><circle cx="180" cy="168" r="11" fill="{T2}" /><svg x="30" y="60" width="70" height="140" viewBox="0 0 12 24"><path d="M6 1 V23 M2.5 1 V7 Q2.5 9.5 6 9.5 Q9.5 9.5 9.5 7 V1" fill="none" stroke="{B}" stroke-width="1.6" stroke-linecap="round" /></svg><svg x="300" y="60" width="70" height="140" viewBox="0 0 12 24"><path d="M6 23 V1 Q10 4 10 11 L6 12" fill="none" stroke="{B}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" /></svg></svg>'),
    ("Emilie", f'<svg viewBox="0 0 400 260" preserveAspectRatio="xMidYMid slice"><rect width="400" height="260" fill="{O}" /><rect y="190" width="400" height="70" fill="{B}" />{camion(20, 200, 0.42)}{camion(220, 200, 0.42)}<rect x="10" y="40" width="70" height="70" rx="14" fill="{B}" /><svg x="20" y="50" width="50" height="50" viewBox="0 0 24 24">{ICONES["parking"].format(c=W)}</svg></svg>'),
    ("Denis", f'<svg viewBox="0 0 400 260" preserveAspectRatio="xMidYMid slice"><rect width="400" height="260" fill="{T1}" /><rect x="40" y="30" width="150" height="230" fill="{W}" stroke="{B}" stroke-width="8" /><rect x="210" y="30" width="150" height="230" fill="{W}" stroke="{B}" stroke-width="8" /><svg x="70" y="60" width="90" height="90" viewBox="0 0 24 24">{ICONES["douche"].format(c=B)}</svg><svg x="240" y="60" width="90" height="90" viewBox="0 0 24 24">{ICONES["douche"].format(c=B)}</svg></svg>'),
    ("Pascal", f'<svg viewBox="150 60 900 440" preserveAspectRatio="xMidYMid slice"><rect x="0" y="0" width="1200" height="600" fill="{T1}" />{RESTAURANT}<rect x="0" y="470" width="1200" height="130" fill="{B}" /></svg>'),
]


# --- Avatars des avis : visage illustré, sans photo ----------------------------------------

def visage(peau, cheveux, forme):
    coiffe = {
        "court": f'<path d="M22 42 Q22 16 50 16 Q78 16 78 42 Q70 30 50 30 Q30 30 22 42 Z" fill="{cheveux}" />',
        "long": f'<path d="M20 70 V44 Q20 14 50 14 Q80 14 80 44 V70 Q74 52 72 40 Q50 34 28 40 Q26 52 20 70 Z" fill="{cheveux}" />',
        "chauve": "",
    }[forme]
    return f"""<svg class="avatar" viewBox="0 0 100 100" aria-hidden="true">
      <circle cx="50" cy="50" r="48" fill="{T1}" />
      <path d="M18 100 Q18 74 50 74 Q82 74 82 100 Z" fill="{B}" />
      <ellipse cx="50" cy="48" rx="25" ry="28" fill="{peau}" />{coiffe}
      <circle cx="41" cy="50" r="3" fill="{S}" /><circle cx="59" cy="50" r="3" fill="{S}" />
      <path d="M42 61 Q50 67 58 61" fill="none" stroke="{S}" stroke-width="3" stroke-linecap="round" />
    </svg>"""


AVIS = [
    ("denis", "Denis", "3 mai", 5, "Super accueil, repas copieux, douche propre, petit déj le matin, rien à redire. Je vous le recommande&nbsp;! Merci à toute l'équipe&nbsp;!", visage("#F2C9A8", S, "chauve")),
    ("pascal", "Pascal", "24 avril", 4, "Restaurant ouvert, menu varié et pas cher. Merci&nbsp;!", visage("#D9A47E", "#3B2A20", "court")),
    ("emilie", "Emilie", "18 avril", 5, "Accueil chaleureux et repas très copieux, c'était parfait&nbsp;!", visage("#F5D5BC", "#7A4A2A", "long")),
]

REPONSE = "Merci beaucoup pour ce commentaire Denis ! À très vite !"


def carte_avis(cle, nom, date, note, texte, av):
    etoiles = "".join(ETOILE if i < note else ETOILE_VIDE for i in range(5))
    reponse = ""
    if cle == "denis":
        reponse = f'<div id="reponse"><span class="rep-titre">Ma réponse</span><span class="rep-texte">{lettres(REPONSE)}<span class="curseur"></span></span></div>'
    bouton = f'<span id="btn-repondre-{cle}" class="btn-ligne">Répondre{CLIC if cle == "denis" else ""}</span>'
    return f"""<div id="avis-{cle}" class="avis">
              {av}
              <div class="avis-corps">
                <div class="avis-tete"><b>{nom}</b><span class="etoiles">{etoiles}</span><span class="gris">{date}</span></div>
                <p>{texte}</p>
                {reponse}
              </div>
              <div class="avis-actions">{bouton}<span class="lien">Signaler</span></div>
            </div>"""


# --- Espace pro recréé ------------------------------------------------------------------

def champ(cid, libelle, valeur, frappe=False, classe=""):
    contenu = f'{lettres(valeur)}<span class="curseur"></span>' if frappe else f'<span class="val">{valeur}</span>'
    return f'<div class="champ {classe}"><span class="libelle">{libelle}</span><span id="{cid}" class="saisie">{contenu}</span></div>'


def enregistrer(bid):
    return f'<div class="actions"><span id="{bid}" class="btn"><span class="btn-txt">Enregistrer</span><span class="btn-ok">✓ Enregistré</span>{CLIC}</span></div>'


SERVICES = [("couverts", "Restaurant routier", True), ("douche", "Douches", True), ("parking", "Parking poids lourds", True), ("wifi", "Wifi", True), ("toilettes", "Toilettes", False), ("camera", "Parking surveillé", False)]

JOURS = ["Lundi", "Mardi", "Mercredi"]

CARTE_PLAN = f"""<div class="plan">
                <svg viewBox="0 0 300 200" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
                  <rect width="300" height="200" fill="{T1}" />
                  <path d="M-10 140 Q90 120 150 70 T310 30 M60 -10 Q80 90 40 210 M180 -10 Q200 110 250 210 M-10 60 H310" fill="none" stroke="{W}" stroke-width="12" />
                  <path d="M-10 140 Q90 120 150 70 T310 30" fill="none" stroke="{T2}" stroke-width="4" />
                </svg>
                <svg id="repere-plan" class="repere" viewBox="0 0 24 32" aria-hidden="true"><path d="M12 1 A10.5 10.5 0 0 0 1.5 11.5 C1.5 19 12 31 12 31 S22.5 19 22.5 11.5 A10.5 10.5 0 0 0 12 1 Z" fill="{B}" /><circle cx="12" cy="11.5" r="4" fill="{W}" /></svg>
              </div>"""

PANES = f"""
            <div id="p1" class="pane">
              <h2>Mon établissement</h2>
              <div class="grille-champs">
                <div class="col">
                  {champ("v-nom", "Nom de l'établissement", "Resto Routier", frappe=True)}
                  {champ("v-adresse", "Adresse", "16 rue de Paris")}
                  <div class="duo">{champ("v-cp", "Code postal", "63130")}{champ("v-ville", "Ville", "Royat")}</div>
                </div>
                <div class="col col-plan">
                  {CARTE_PLAN}
                  {champ("v-tel", "Téléphone", "04 70 00 00 00")}
                </div>
              </div>
              {enregistrer("btn-p1")}
            </div>
            <div id="p2" class="pane">
              <h2>Mes services</h2>
              <div class="services">
                {''.join(f'<div class="service"><span class="case{" a-cocher" if oui else ""}">{COCHE}</span>{icone(nom, B, "icone-service")}<span>{lib}</span></div>' for nom, lib, oui in SERVICES)}
              </div>
              {enregistrer("btn-p2")}
            </div>
            <div id="p3" class="pane">
              <h2>Ma photo</h2>
              <div id="depot">
                <div class="depot-vide">{icone("image", B, "icone-depot")}<span>Glissez votre photo ici</span></div>
                <div id="photo">{FACADE}{CLIC.replace('class="clic"', 'class="clic clic-photo"')}</div>
              </div>
              {enregistrer("btn-p3")}
            </div>
            <div id="p4" class="pane">
              <h2>Mes horaires d'ouverture</h2>
              <div class="horaires">
                {''.join(f'''<div id="j{i}" class="jour">
                  <b>{j}</b>
                  <span class="heure"><span class="libelle">Début</span><span class="saisie"><span class="val">07:00</span></span></span>
                  <span class="heure"><span class="libelle">Fin</span><span class="saisie"><span class="val">23:55</span></span></span>
                  <span class="continue"><span class="case">{COCHE}</span>Journée continue</span>
                  {f'<span id="btn-dupliquer" class="btn-ligne">Dupliquer{CLIC}</span>' if i == 0 else ''}
                </div>''' for i, j in enumerate(JOURS))}
              </div>
            </div>
            <div id="p5" class="pane">
              <h2>Mes commentaires</h2>
              <div class="liste-avis">
                {''.join(carte_avis(*a) for a in AVIS)}
              </div>
            </div>
            <div id="p6" class="pane">
              <h2>Photos de la communauté</h2>
              <div class="galerie">
                {''.join(f'<figure class="vignette">{svg}<figcaption>{icone("camera", B, "icone-legende")}Ajoutée par {qui}</figcaption></figure>' for qui, svg in VIGNETTES)}
              </div>
            </div>"""

MENU = ["Mon établissement", "Mes services et photos", "Mes horaires d'ouverture", "Mes commentaires"]

FENETRE = f"""<div id="fenetre">
          <div class="barre-nav"><i></i><i></i><i></i><span class="adresse">www.truckfly.com</span></div>
          <div class="entete">
            <img src="{{racine}}assets/logos/truckfly-blanc-rogne.png" alt="Michelin Truckfly" />
            <span class="onglet actif">Mon lieu</span><span class="onglet">Mon compte</span>
            <span class="compte"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="{W}" /><circle cx="12" cy="9.5" r="3.8" fill="{B}" /><path d="M5 19 Q6.5 14.5 12 14.5 Q17.5 14.5 19 19" fill="{B}" /></svg></span>
          </div>
          <div class="corps">
            <div class="menu">
              <div class="vignette-lieu"><div class="vide">{icone("image", B, "icone-vide")}</div><div id="vignette-photo">{FACADE}</div></div>
              {''.join(f'<div id="m{i + 1}" class="item">{lib}</div>' for i, lib in enumerate(MENU))}
            </div>
            <div class="contenu">{PANES}
            </div>
          </div>
        </div>"""

ETIQUETTES = [
    ("l1", "Nom et coordonnées"),
    ("l2", "Services proposés"),
    ("l3", "Photos"),
    ("l4", "Horaires"),
    ("l5", "Retrouvez les commentaires et les photos de la communauté"),
]

STATS = [
    ("st1", "2,3 M", "téléchargements"),
    ("st2", "44", "pays européens"),
    ("st3", "21", "langues disponibles"),
    ("st4", "702 000", "utilisateurs"),
    ("st5", "135 000", "établissements référencés"),
]

# Icônes du téléphone illustré (scène 2) : une grille, celle de Truckfly au centre
GRILLE_APPS = "".join(
    f'<span class="app{" app-truckfly" if i == 4 else ""}">{"<svg viewBox=\"0 0 24 32\"><path d=\"M12 3 A9 9 0 0 0 3 12 C3 18.5 12 29 12 29 S21 18.5 21 12 A9 9 0 0 0 12 3 Z\" fill=\"#FFFFFF\" /><circle cx=\"12\" cy=\"12\" r=\"3.6\" fill=\"#061866\" /></svg>" + CLIC if i == 4 else ""}</span>'
    for i in range(12)
)


def corps(racine):
    return f"""
      <div id="fond" class="plein clip" data-start="0" data-duration="{DUREE}" data-track-index="0">
        <div id="fond-couleur"></div>
      </div>

      <div id="s1" class="plein clip scene" data-start="0" data-duration="3.6" data-track-index="1">
        <div class="bloc-intro">
          <span class="titre mot">Connaissez-vous</span>
          <span class="logo-ligne"><img id="s1-logo" src="{racine}assets/logos/truckfly-blanc-rogne.png" alt="Michelin Truckfly" /><span id="s1-q" class="titre">?</span></span>
          <span id="s1-trait" class="trait-jaune"></span>
        </div>
      </div>

      <div id="s2a" class="plein clip scene" data-start="3.4" data-duration="2.3" data-track-index="1">
        <div id="telephone">
          <div class="ecran-tel">
            <div class="grille-apps">{GRILLE_APPS}</div>
            <div id="app-ouverte"><img src="{racine}assets/logos/truckfly-blanc-rogne.png" alt="" /></div>
          </div>
        </div>
      </div>

      <div id="s2b" class="plein clip scene" data-start="5.5" data-duration="6.2" data-track-index="1">
        <div class="bloc-stats">
          <div class="titre-stats"><span class="titre">{mots("La communauté en chiffres")}</span><span id="s2-trait" class="trait-jaune"></span></div>
          <div class="stats">
            {''.join(f'<div id="{sid}" class="stat"><span class="nombre">{compteur(v)}</span><span class="legende">{lib}</span></div>' for sid, v, lib in STATS)}
          </div>
        </div>
      </div>

      <div id="s3" class="plein clip scene" data-start="11.5" data-duration="5.6" data-track-index="1">
        <div class="bloc-texte">
          <span class="ligne sous">{mots("Saviez-vous que Truckfly existe aussi")}</span>
          <span class="ligne titre">{mots("pour les propriétaires d'établissements&nbsp;?")}</span>
        </div>
      </div>

      <div id="s4" class="plein clip scene" data-start="16.9" data-duration="6.3" data-track-index="1">
        <div id="sol"></div>
        {''.join(f'<div id="i-{cle}" class="illu-bloc">{illustration(svg)}<span class="nom-lieu titre">{nom}</span></div>' for cle, nom, svg in ILLUS)}
      </div>

      <div id="s5" class="plein clip scene" data-start="22.9" data-duration="5.1" data-track-index="1">
        <div class="bloc-texte">
          <span class="ligne sous">{mots("J'ai un établissement sur Truckfly,")}</span>
          <span class="ligne titre">{mots("je mets à jour mes informations&nbsp;!")}</span>
          <span id="s5-url" class="barre-url"><span class="url">{lettres("www.truckfly.com")}<span class="curseur"></span></span>{LOUPE}</span>
        </div>
      </div>

      <div id="s6" class="plein clip scene clair" data-start="27.7" data-duration="6.3" data-track-index="1">
        <div class="bloc-texte">
          <span class="ligne sous">{mots("Mon établissement n'est pas encore sur Truckfly&nbsp;?")}</span>
          <span class="ligne titre">{mots("Je crée mon compte et j'ajoute mon établissement&nbsp;!")}</span>
          <span id="s6-url" class="barre-url"><span class="url">{lettres("www.truckfly.com")}<span class="curseur"></span></span><span id="s6-loupe" class="zone-loupe">{LOUPE}{CLIC}</span></span>
        </div>
      </div>

      <div id="s7" class="plein clip scene" data-start="33.7" data-duration="23.6" data-track-index="1">
        <div class="etiquettes">
          {''.join(f'<div id="{eid}" class="etiquette"><span class="titre">{mots(txt)}</span><span class="trait-jaune"></span></div>' for eid, txt in ETIQUETTES)}
        </div>
        {FENETRE.replace("{racine}", racine)}
      </div>

      <div id="s9" class="plein clip scene" data-start="57.0" data-duration="{round(DUREE - 57.0, 2)}" data-track-index="1">
        <div class="bloc-fin">
          <img id="s9-logo" src="{racine}assets/logos/truckfly-blanc-rogne.png" alt="Michelin Truckfly" />
          <span class="ligne sous">Pour promouvoir mon établissement,</span>
          <span class="ligne sous">connectez-vous sur le site internet.</span>
          <span class="ligne cta">www.truckfly.com</span>
        </div>
      </div>"""


SCRIPT = """
      const tl = gsap.timeline({ paused: true });
      const entre = { autoAlpha: 1, y: 0, duration: 0.4, ease: "power2.out" };
      const sort = { autoAlpha: 0, y: -30, duration: 0.3, ease: "power2.in" };

      function fond(couleur, t) {
        tl.to("#fond-couleur", { backgroundColor: couleur, duration: 0.35, ease: "power1.inOut" }, t);
      }
      function montre(cible, t, decalage = 0.08) {
        tl.fromTo(cible, { autoAlpha: 0, y: 40 }, { ...entre, stagger: decalage }, t);
      }
      function cache(cible, t) {
        tl.to(cible, { ...sort, immediateRender: false }, t);
      }
      // Frappe : les lettres apparaissent une à une, le curseur les suit
      function frappe(cible, t, pas = 0.055) {
        tl.fromTo(`${cible} .ch`, { display: "none" }, { display: "inline", duration: 0.001, stagger: pas }, t);
        tl.fromTo(`${cible} .curseur`, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.01 }, t);
      }
      // Clic : le pointeur se pose, une onde part, il reste un instant puis disparaît
      function clic(cible, t) {
        tl.fromTo(`${cible} .pointeur`, { autoAlpha: 0, x: 18, y: 18 }, { autoAlpha: 1, x: 0, y: 0, duration: 0.25, ease: "power2.out" }, t - 0.25);
        tl.fromTo(`${cible} .onde`, { autoAlpha: 0.9, scale: 0.4 }, { autoAlpha: 0, scale: 1.6, duration: 0.5, ease: "power2.out" }, t);
        tl.to(`${cible} .pointeur`, { autoAlpha: 0, duration: 0.2, immediateRender: false }, t + 0.6);
      }
      function enregistre(bouton, t) {
        clic(bouton, t);
        tl.to(`${bouton} .btn-txt`, { autoAlpha: 0, duration: 0.15 }, t + 0.1);
        tl.fromTo(`${bouton} .btn-ok`, { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, t + 0.15);
      }
      function etiquette(id, t, fin) {
        tl.fromTo(`${id} .mot`, { autoAlpha: 0, y: 30 }, { ...entre, stagger: 0.07 }, t);
        tl.fromTo(`${id} .trait-jaune`, { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.out" }, t + 0.3);
        tl.to(id, { autoAlpha: 0, x: -30, duration: 0.3, ease: "power2.in" }, fin);
      }
      function changePane(avant, apres, t) {
        tl.to(avant, { autoAlpha: 0, x: -40, duration: 0.3, ease: "power2.in" }, t);
        tl.fromTo(apres, { autoAlpha: 0, x: 40 }, { autoAlpha: 1, x: 0, duration: 0.35, ease: "power2.out" }, t + 0.25);
      }
      function menu(avant, apres, t) {
        tl.to(`${avant}`, { backgroundColor: "rgba(6,24,102,0)", color: "#000000", duration: 0.25 }, t);
        tl.to(`${apres}`, { backgroundColor: "#061866", color: "#FFFFFF", duration: 0.25 }, t);
      }

      // 1 · Connaissez-vous Truckfly ? (0–3,5 s)
      tl.fromTo("#s1 .mot", { autoAlpha: 0, y: 40 }, entre, 0.25);
      tl.fromTo("#s1-logo", { autoAlpha: 0, scale: 0.9 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: "power2.out" }, 0.8);
      tl.fromTo("#s1-q", { autoAlpha: 0, scale: 0.5 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, 1.3);
      tl.fromTo("#s1-trait", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power2.out" }, 1.5);
      cache("#s1 .bloc-intro", 3.15);
      fond("#F5F3F1", 3.35);

      // 2a · Le téléphone : tap sur l'app Truckfly, elle s'ouvre (3,5–5,6 s)
      tl.fromTo("#telephone", { autoAlpha: 0, y: 160 }, { autoAlpha: 1, y: 0, duration: 0.55, ease: "power2.out" }, 3.45);
      clic(".app-truckfly", 4.35);
      tl.fromTo("#app-ouverte", { autoAlpha: 0, scale: 0.25 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "power2.out" }, 4.5);
      tl.to("#telephone", { autoAlpha: 0, scale: 1.08, duration: 0.3, ease: "power2.in" }, 5.3);
      fond("#061866", 5.35);

      // 2b · La communauté en chiffres (5,6–11,6 s)
      tl.fromTo("#s2b .titre .mot", { autoAlpha: 0, y: 40 }, { ...entre, stagger: 0.08 }, 5.65);
      tl.fromTo("#s2-trait", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power2.out" }, 5.95);
      gsap.utils.toArray("#s2b .stat").forEach((stat, i) => {
        const t = 6.15 + i * 0.35;
        tl.fromTo(stat, { autoAlpha: 0, y: 40 }, entre, t);
        stat.querySelectorAll(".chiffre").forEach((c, j) => {
          const v = Number(c.dataset.v);
          tl.fromTo(c.querySelector(".bande"), { xPercent: -50, yPercent: 0 }, { xPercent: -50, yPercent: -(10 + v) * 5, duration: 1.1 + j * 0.08, ease: "power3.out" }, t);
        });
      });
      cache("#s2b .bloc-stats", 11.3);

      // 3 · Truckfly existe aussi pour les propriétaires d'établissements (11,6–17 s)
      montre("#s3 .sous .mot", 11.65);
      montre("#s3 .titre .mot", 12.35);
      cache("#s3 .bloc-texte", 16.7);
      fond("#F5F3F1", 16.85);

      // 4 · Les établissements : restaurant, station-service, station de lavage, garage (17–23 s)
      tl.fromTo("#sol", { yPercent: 100 }, { yPercent: 0, duration: 0.45, ease: "power2.out" }, 16.95);
      ["#i-restaurant", "#i-station", "#i-lavage", "#i-garage"].forEach((id, i) => {
        const t = 17.05 + i * 1.5;
        tl.fromTo(`${id} .illus`, { autoAlpha: 0, xPercent: 35 }, { autoAlpha: 1, xPercent: 0, duration: 0.45, ease: "power2.out" }, t);
        tl.fromTo(`${id} .nom-lieu`, { autoAlpha: 0, y: 30 }, entre, t + 0.15);
        if (i < 3) {
          tl.to(`${id} .illus`, { autoAlpha: 0, xPercent: -35, duration: 0.35, ease: "power2.in", immediateRender: false }, t + 1.3);
          tl.to(`${id} .nom-lieu`, { autoAlpha: 0, duration: 0.2, immediateRender: false }, t + 1.3);
        }
      });
      tl.to("#i-garage", { autoAlpha: 0, duration: 0.3 }, 22.45);
      tl.to("#sol", { height: "100%", duration: 0.45, ease: "power2.inOut" }, 22.55);
      fond("#061866", 22.95);

      // 5 · J'ai un établissement : je mets à jour mes infos (23–27,8 s)
      montre("#s5 .sous .mot", 23.05);
      montre("#s5 .titre .mot", 23.8);
      tl.fromTo("#s5-url", { autoAlpha: 0, scale: 0.9 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, 24.6);
      frappe("#s5-url", 24.9);
      cache("#s5 .bloc-texte", 27.45);
      fond("#F5F3F1", 27.6);

      // 6 · Pas encore sur Truckfly : je crée mon compte (27,8–33,8 s)
      montre("#s6 .sous .mot", 27.9);
      montre("#s6 .titre .mot", 28.85);
      tl.fromTo("#s6-url", { autoAlpha: 0, scale: 0.9 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, 29.9);
      frappe("#s6-url", 30.2);
      clic("#s6-loupe", 31.6);
      cache("#s6 .bloc-texte", 33.35);
      fond("#061866", 33.5);

      // 7 · L'espace pro (33,8–57 s)
      tl.fromTo("#fenetre", { autoAlpha: 0, y: 120 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "power2.out" }, 33.75);
      tl.set(["#p2", "#p3", "#p4", "#p5", "#p6"], { autoAlpha: 0 }, 0);

      // 7a · Nom et coordonnées (33,8–37,8 s)
      etiquette("#l1", 34.0, 37.55);
      frappe("#v-nom", 34.5);
      tl.to("#v-nom .curseur", { autoAlpha: 0, duration: 0.01 }, 35.3);
      tl.fromTo(["#v-adresse .val", "#v-cp .val", "#v-ville .val", "#v-tel .val"], { autoAlpha: 0, x: -12 }, { autoAlpha: 1, x: 0, duration: 0.25, stagger: 0.22 }, 35.3);
      tl.fromTo("#repere-plan", { autoAlpha: 0, y: -60 }, { autoAlpha: 1, y: 0, duration: 0.5, ease: "bounce.out" }, 35.6);
      enregistre("#btn-p1", 36.75);

      // 7b · Services proposés (37,8–41,8 s)
      menu("#m1", "#m2", 37.75);
      changePane("#p1", "#p2", 37.75);
      etiquette("#l2", 37.95, 41.55);
      gsap.utils.toArray("#p2 .a-cocher").forEach((c, i) => {
        tl.fromTo(c, { backgroundColor: "#FFFFFF" }, { backgroundColor: "#061866", duration: 0.15 }, 38.6 + i * 0.38);
        tl.fromTo(c.querySelector(".coche"), { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)" }, 38.6 + i * 0.38);
      });
      enregistre("#btn-p2", 40.65);

      // 7c · Photos (41,8–45,3 s)
      changePane("#p2", "#p3", 41.75);
      etiquette("#l3", 41.95, 45.05);
      tl.fromTo("#photo", { autoAlpha: 0, x: 260, y: 200, rotation: 6, scale: 0.6 }, { autoAlpha: 1, x: 0, y: 0, rotation: 0, scale: 1, duration: 0.8, ease: "power2.out" }, 42.45);
      tl.fromTo("#photo .pointeur", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.15 }, 42.45);
      tl.to("#photo .pointeur", { autoAlpha: 0, duration: 0.2 }, 43.4);
      tl.fromTo("#vignette-photo", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.35 }, 43.45);
      enregistre("#btn-p3", 44.1);

      // 7d · Horaires (45,3–49,3 s)
      menu("#m2", "#m3", 45.25);
      changePane("#p3", "#p4", 45.25);
      etiquette("#l4", 45.45, 49.05);
      tl.fromTo("#j0 .val", { autoAlpha: 0, x: -10 }, { autoAlpha: 1, x: 0, duration: 0.25, stagger: 0.25 }, 45.85);
      tl.fromTo("#j0 .case", { backgroundColor: "#FFFFFF" }, { backgroundColor: "#061866", duration: 0.15 }, 46.4);
      tl.fromTo("#j0 .coche", { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)" }, 46.4);
      tl.set(["#j1 .val", "#j2 .val", "#j1 .coche", "#j2 .coche"], { autoAlpha: 0 }, 0);
      clic("#btn-dupliquer", 47.0);
      ["#j1", "#j2"].forEach((j, i) => {
        const t = 47.25 + i * 0.35;
        tl.fromTo(`${j} .val`, { autoAlpha: 0, x: -10 }, { autoAlpha: 1, x: 0, duration: 0.25, immediateRender: false }, t);
        tl.fromTo(`${j} .case`, { backgroundColor: "#FFFFFF" }, { backgroundColor: "#061866", duration: 0.15 }, t);
        tl.fromTo(`${j} .coche`, { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)", immediateRender: false }, t);
      });

      // 8 · Commentaires et photos de la communauté (49,3–57 s)
      menu("#m3", "#m4", 49.25);
      changePane("#p4", "#p5", 49.25);
      etiquette("#l5", 49.45, 56.75);
      tl.fromTo(".avis", { autoAlpha: 0, y: 30 }, { ...entre, stagger: 0.2 }, 49.6);
      clic("#btn-repondre-denis", 50.85);
      tl.fromTo("#reponse", { maxHeight: "0em", autoAlpha: 0 }, { maxHeight: "8em", autoAlpha: 1, duration: 0.35, ease: "power2.out" }, 51.0);
      frappe("#reponse", 51.35, 0.038);
      changePane("#p5", "#p6", 54.0);
      tl.fromTo(".vignette", { autoAlpha: 0, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)", stagger: 0.18 }, 54.3);
      tl.to("#fenetre", { autoAlpha: 0, y: 80, duration: 0.35, ease: "power2.in" }, 56.7);

      // 9 · Fin : logo et appel à se connecter (57–62,6 s)
      tl.fromTo("#s9-logo", { autoAlpha: 0, y: 30 }, entre, 57.15);
      montre("#s9 .sous", 57.65, 0.2);
      tl.fromTo("#s9 .cta", { autoAlpha: 0, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, 58.4);
      tl.to("#s9 .cta", { scale: 1.05, duration: 0.35, yoyo: true, repeat: 3, ease: "sine.inOut" }, 59.3);

      window.__timelines = window.__timelines || {};
      window.__timelines["{cid}"] = tl;
      tl.seek(0);
"""

CSS_COMMUN = """
      @font-face { font-family: "Bib"; src: url("{racine}assets/fonts/BIB-Bold.woff2") format("woff2"); font-weight: 700; }
      @font-face { font-family: "Bib"; src: url("{racine}assets/fonts/BIB-Light.woff2") format("woff2"); font-weight: 300; }
      @font-face { font-family: "Noto Sans"; src: url("{racine}assets/fonts/noto-sans-latin-400-normal.woff2") format("woff2"); font-weight: 400; }
      @font-face { font-family: "Noto Sans"; src: url("{racine}assets/fonts/noto-sans-latin-600-normal.woff2") format("woff2"); font-weight: 600; }
      @font-face { font-family: "Noto Sans"; src: url("{racine}assets/fonts/noto-sans-latin-700-normal.woff2") format("woff2"); font-weight: 700; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: {w}px; height: {h}px; overflow: hidden; background: #061866; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Bib", sans-serif; color: #FFFFFF; }
      .plein { position: absolute; inset: 0; }
      #fond-couleur { position: absolute; inset: 0; background: #061866; }
      .scene { display: flex; align-items: center; justify-content: center; }
      .titre { font-weight: 700; line-height: 1.08; }
      .sous { font-weight: 300; line-height: 1.15; }
      .mot { display: inline-block; }
      .ligne { display: block; }
      .clair { color: #061866; }
      .trait-jaune { display: block; height: var(--trait); width: var(--trait-l); background: #FFFF1A; border-radius: 99px; transform-origin: left center; }

      /* 1 · Intro */
      .bloc-intro { display: flex; flex-direction: var(--intro-sens); align-items: center; gap: var(--intro-gap); position: relative; }
      .bloc-intro .titre { font-size: var(--t-intro); }
      .logo-ligne { display: flex; align-items: center; gap: var(--q-gap); }
      #s1-logo { height: var(--logo-intro); width: auto; }
      #s1-q { font-size: var(--t-q); }
      #s1-trait { position: absolute; left: 50%; bottom: calc(var(--trait) * -5); margin-left: calc(var(--trait-l) / -2); }

      /* 2a · Téléphone illustré */
      #telephone { width: var(--tel-l); aspect-ratio: 9 / 18.5; background: #061866; border-radius: calc(var(--tel-l) * 0.14); padding: calc(var(--tel-l) * 0.045); box-shadow: 0 30px 80px rgba(6, 24, 102, 0.25); }
      .ecran-tel { position: relative; width: 100%; height: 100%; background: #FFFFFF; border-radius: calc(var(--tel-l) * 0.1); overflow: hidden; display: flex; align-items: center; justify-content: center; }
      .grille-apps { display: grid; grid-template-columns: repeat(3, 1fr); gap: calc(var(--tel-l) * 0.07); width: 78%; }
      .app { position: relative; aspect-ratio: 1; border-radius: 26%; background: #DCE3F5; display: flex; align-items: center; justify-content: center; }
      .app-truckfly { background: #061866; }
      .app-truckfly svg { width: 46%; height: 60%; }
      #app-ouverte { position: absolute; inset: 0; background: #061866; display: flex; align-items: center; justify-content: center; transform-origin: 50% 46%; }
      #app-ouverte img { width: 74%; height: auto; }

      /* Repères de clic : posés au centre de l'élément visé */
      .clic { position: absolute; left: 50%; top: 50%; width: 0; height: 0; pointer-events: none; }
      .clic .onde { position: absolute; width: var(--clic); height: var(--clic); left: calc(var(--clic) / -2); top: calc(var(--clic) / -2); border-radius: 50%; border: calc(var(--clic) * 0.08) solid #061866; background: rgba(255, 255, 255, 0.45); visibility: hidden; opacity: 0; }
      .pointeur { position: absolute; left: calc(var(--clic) * -0.12); top: calc(var(--clic) * -0.06); width: calc(var(--clic) * 0.9); height: calc(var(--clic) * 0.9); visibility: hidden; opacity: 0; filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.25)); }

      /* 2b · Chiffres */
      .bloc-stats { display: flex; flex-direction: column; gap: var(--stats-gap); }
      .titre-stats .titre { font-size: var(--t-stats); display: block; }
      #s2-trait { margin-top: calc(var(--trait) * 3); }
      .stats { display: grid; grid-template-columns: var(--stats-cols); gap: var(--stats-gap-in); }
      .stat { display: flex; flex-direction: column; gap: 0.1em; }
      .nombre { font-weight: 700; font-size: var(--t-nombre); line-height: 1; display: flex; white-space: nowrap; }
      .chiffre { position: relative; display: inline-block; height: 1em; overflow: hidden; }
      .cale { visibility: hidden; }
      .bande { position: absolute; left: 50%; top: 0; display: flex; flex-direction: column; text-align: center; }
      .bande span { display: block; height: 1em; }
      .espace { display: inline-block; width: 0.22em; }
      .legende { font-weight: 300; font-size: var(--t-legende); }

      /* Textes 3, 5, 6 */
      .bloc-texte { display: flex; flex-direction: column; align-items: center; text-align: center; gap: var(--txt-gap); max-width: var(--txt-l); }
      .bloc-texte .sous { font-size: var(--t-sous); }
      .bloc-texte .titre { font-size: var(--t-titre); }
      .barre-url { display: flex; align-items: center; gap: 0.6em; margin-top: var(--txt-gap); background: #FFFFFF; color: #061866; border-radius: 99px; padding: 0.35em 0.6em 0.35em 1em; font-family: "Noto Sans", sans-serif; font-weight: 600; font-size: var(--t-url); }
      .clair .barre-url { border: 0.08em solid #061866; }
      .url { min-width: 9.2em; white-space: nowrap; }
      .loupe { width: 1.1em; height: 1.1em; }
      .zone-loupe { position: relative; display: flex; --clic: 2.2em; }
      .curseur { display: inline-block; width: 0.07em; height: 1em; margin-left: 0.04em; vertical-align: -0.12em; background: currentColor; visibility: hidden; opacity: 0; }

      /* 4 · Établissements */
      #sol { position: absolute; left: 0; right: 0; bottom: 0; height: var(--sol); background: #061866; }
      .illu-bloc { position: absolute; inset: 0; }
      .illus { position: absolute; left: 50%; bottom: var(--sol); transform: translateX(-50%); width: var(--illu-l); height: var(--illu-h); visibility: hidden; opacity: 0; overflow: visible; }
      .nom-lieu { position: absolute; left: 0; right: 0; bottom: 0; height: var(--sol); display: flex; align-items: center; justify-content: center; font-size: var(--t-lieu); visibility: hidden; opacity: 0; }

      /* 7 · Espace pro recréé (Noto Sans, tailles en em) */
      .etiquettes { position: absolute; left: var(--etq-x); top: var(--etq-y); width: var(--etq-l); height: var(--etq-h); }
      .etiquette { position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; align-items: var(--etq-align); text-align: var(--etq-texte); gap: calc(var(--trait) * 4); }
      .etiquette .titre { font-size: var(--t-etq); }
      .etiquette .mot { visibility: hidden; opacity: 0; }
      #l5 .titre { font-size: var(--t-etq5); }
      #fenetre { position: absolute; left: var(--f-x); top: var(--f-y); width: var(--f-l); height: var(--f-h); font-size: var(--ui); background: #FFFFFF; color: #000000; border-radius: 0.7em; overflow: hidden; font-family: "Noto Sans", sans-serif; display: flex; flex-direction: column; box-shadow: 0 30px 90px rgba(0, 0, 0, 0.35); --clic: 2.6em; }
      .barre-nav { flex: none; height: 2.1em; background: #E9E7E4; display: flex; align-items: center; gap: 0.45em; padding: 0 1em; }
      .barre-nav i { width: 0.7em; height: 0.7em; border-radius: 50%; background: #C9C6C2; }
      .barre-nav .adresse { margin-left: 1.2em; background: #FFFFFF; border-radius: 99px; padding: 0.15em 1em; font-size: 0.8em; color: #53565A; }
      .entete { flex: none; height: 3.1em; background: #061866; display: flex; align-items: center; gap: 1.6em; padding: 0 1.4em; color: #FFFFFF; }
      .entete img { height: 1.6em; width: auto; margin-right: 1em; }
      .onglet { font-size: 0.9em; padding: 0.3em 0; border-bottom: 0.18em solid transparent; }
      .onglet.actif { font-weight: 700; border-color: #FFFF1A; }
      .compte { margin-left: auto; width: 1.8em; height: 1.8em; }
      .compte svg { width: 100%; height: 100%; }
      .corps { flex: 1; display: flex; min-height: 0; }
      .menu { flex: none; width: var(--menu-l); background: #F5F3F1; display: var(--menu-aff); flex-direction: column; }
      .vignette-lieu { position: relative; height: 8.5em; background: #DCE3F5; }
      .vignette-lieu > div { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
      .icone-vide { width: 3em; height: 3em; }
      #vignette-photo { visibility: hidden; opacity: 0; }
      .facade { width: 100%; height: 100%; display: block; }
      .item { font-size: 0.85em; padding: 0.95em 1.3em; border-bottom: 1px solid #E2DFDB; }
      #m1 { background: #061866; color: #FFFFFF; }
      .contenu { flex: 1; position: relative; min-width: 0; }
      .pane { position: absolute; inset: 0; padding: var(--pane-pad); display: flex; flex-direction: column; gap: 1.1em; }
      .pane h2 { font-family: "Bib", sans-serif; font-weight: 700; font-size: 1.55em; color: #061866; }
      .grille-champs { display: grid; grid-template-columns: var(--champs-cols); gap: 1em 1.6em; }
      .col { display: flex; flex-direction: column; gap: 0.9em; min-width: 0; }
      .duo { display: grid; grid-template-columns: 1fr 1.4fr; gap: 1em; }
      .champ { display: flex; flex-direction: column; gap: 0.3em; }
      .libelle { font-size: 0.75em; color: #53565A; font-weight: 600; }
      .saisie { display: block; height: 2.3em; background: #F5F3F1; border: 1px solid #D9D6D2; border-radius: 0.35em; padding: 0 0.7em; line-height: 2.3em; font-size: 0.95em; white-space: nowrap; overflow: hidden; }
      .plan { position: relative; height: var(--plan-h); border-radius: 0.5em; overflow: hidden; }
      .plan > svg:first-child { width: 100%; height: 100%; display: block; }
      .repere { position: absolute; left: 50%; top: 50%; width: 2.2em; height: 2.9em; margin: -2.9em 0 0 -1.1em; visibility: hidden; opacity: 0; }
      .actions { margin-top: auto; display: flex; }
      .btn { position: relative; display: grid; font-weight: 700; font-size: 0.95em; }
      .btn > .btn-txt, .btn > .btn-ok { grid-area: 1 / 1; padding: 0.6em 1.5em; border-radius: 0.4em; text-align: center; }
      .btn-txt { background: #061866; color: #FFFFFF; }
      .btn-ok { background: #E4EAF7; color: #061866; visibility: hidden; opacity: 0; }
      .services { display: grid; grid-template-columns: var(--services-cols); gap: 0.8em 1.6em; }
      .service { display: flex; align-items: center; gap: 0.7em; background: #F5F3F1; border-radius: 0.5em; padding: 0.75em 0.9em; font-size: 0.95em; }
      .case { flex: none; width: 1.3em; height: 1.3em; border: 0.12em solid #061866; border-radius: 0.3em; background: #FFFFFF; display: flex; align-items: center; justify-content: center; }
      .coche { width: 90%; height: 90%; visibility: hidden; opacity: 0; }
      .icone-service { flex: none; width: 1.5em; height: 1.5em; }
      #depot { position: relative; flex: 1; max-height: var(--depot-h); border: 0.14em dashed #061866; border-radius: 0.6em; background: #F5F3F1; }
      .depot-vide { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.6em; color: #53565A; font-size: 0.95em; }
      .icone-depot { width: 3.4em; height: 3.4em; }
      #photo { position: absolute; inset: 0.6em; border-radius: 0.4em; overflow: hidden; visibility: hidden; opacity: 0; box-shadow: 0 10px 30px rgba(6, 24, 102, 0.25); }
      #photo .clic { overflow: visible; }
      .clic-photo { left: 70%; top: 70%; }
      .horaires { display: flex; flex-direction: column; gap: 0.8em; }
      .jour { display: flex; flex-wrap: wrap; align-items: center; gap: 0.7em 1.2em; background: #F5F3F1; border-radius: 0.5em; padding: 0.8em 1em; }
      .jour b { width: 5.4em; color: #061866; }
      .heure { display: flex; align-items: center; gap: 0.5em; }
      .heure .saisie { width: 4.6em; background: #FFFFFF; text-align: center; padding: 0; }
      .heure .libelle { font-size: 0.8em; }
      .continue { display: flex; align-items: center; gap: 0.5em; font-size: 0.9em; }
      .btn-ligne { position: relative; margin-left: auto; border: 0.1em solid #061866; color: #061866; font-weight: 700; border-radius: 0.4em; padding: 0.35em 1em; font-size: 0.85em; white-space: nowrap; }
      .liste-avis { display: flex; flex-direction: column; gap: 0.8em; }
      .avis { display: flex; gap: 1em; align-items: flex-start; border: 1px solid #E2DFDB; border-radius: 0.6em; padding: 0.9em 1em; }
      .avatar { flex: none; width: 3.2em; height: 3.2em; }
      .avis-corps { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 0.3em; }
      .avis-tete { display: flex; align-items: center; gap: 0.6em; }
      .etoiles { display: flex; gap: 0.1em; }
      .etoiles svg { width: 0.95em; height: 0.95em; }
      .gris { color: #53565A; font-size: 0.8em; }
      .avis p { font-size: 0.88em; line-height: 1.4; }
      .avis-actions { flex: none; display: flex; flex-direction: column; align-items: flex-end; gap: 0.5em; }
      .avis-actions .btn-ligne { margin-left: 0; }
      .lien { font-size: 0.8em; color: #53565A; text-decoration: underline; }
      #reponse { overflow: hidden; background: #E4EAF7; border-radius: 0.4em; padding: 0 0.8em; display: flex; flex-direction: column; justify-content: center; gap: 0.15em; visibility: hidden; opacity: 0; }
      #reponse .rep-titre { font-size: 0.72em; font-weight: 700; color: #061866; padding-top: 0.6em; }
      #reponse .rep-texte { font-size: 0.88em; padding-bottom: 0.6em; }
      .galerie { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 1em; min-height: 0; }
      .vignette { display: flex; flex-direction: column; gap: 0.35em; min-height: 0; }
      .vignette > svg { flex: 1; width: 100%; min-height: 0; border-radius: 0.5em; display: block; }
      figcaption { display: flex; align-items: center; gap: 0.4em; font-size: 0.8em; color: #53565A; }
      .icone-legende { width: 1.2em; height: 1.2em; }

      /* 9 · Fin */
      .bloc-fin { display: flex; flex-direction: column; align-items: center; text-align: center; }
      #s9-logo { width: var(--logo-fin); height: auto; margin-bottom: var(--fin-gap); }
      .bloc-fin .sous { font-size: var(--t-fin); }
      .cta { margin-top: var(--fin-gap); background: #FFFFFF; color: #061866; font-weight: 700; font-size: var(--t-cta); padding: 0.4em 1.1em; border-radius: 99px; }
"""

CSS_16x9 = """
      #root {
        --trait: 10px; --trait-l: 200px;
        --intro-sens: row; --intro-gap: 40px; --q-gap: 36px; --t-intro: 120px; --logo-intro: 150px; --t-q: 150px;
        --tel-l: 380px; --clic: 64px;
        --stats-gap: 70px; --stats-gap-in: 60px 90px; --stats-cols: repeat(3, auto); --t-stats: 96px; --t-nombre: 150px; --t-legende: 44px;
        --txt-gap: 28px; --txt-l: 1760px; --t-sous: 76px; --t-titre: 104px; --t-url: 52px;
        --sol: 300px; --illu-l: 1500px; --illu-h: 700px; --t-lieu: 110px;
        --etq-x: 100px; --etq-y: 140px; --etq-l: 480px; --etq-h: 800px; --etq-align: flex-start; --etq-texte: left; --t-etq: 72px; --t-etq5: 62px;
        --f-x: 630px; --f-y: 100px; --f-l: 1220px; --f-h: 880px; --ui: 24px; --menu-l: 13em; --menu-aff: flex; --pane-pad: 1.5em 1.8em;
        --champs-cols: 1.15fr 1fr; --plan-h: 8.8em; --services-cols: 1fr 1fr; --depot-h: 18em;
        --logo-fin: 720px; --fin-gap: 56px; --t-fin: 72px; --t-cta: 72px;
      }
      #s6 .sous { font-size: 68px; }
      .stats .stat:nth-child(4) { grid-column: 1; }
      .stats .stat:nth-child(5) { grid-column: 2 / span 2; }
"""

CSS_9x16 = """
      #root {
        --trait: 12px; --trait-l: 220px;
        --intro-sens: column; --intro-gap: 60px; --q-gap: 40px; --t-intro: 116px; --logo-intro: 200px; --t-q: 200px;
        --tel-l: 560px; --clic: 96px;
        --stats-gap: 56px; --stats-gap-in: 26px; --stats-cols: 1fr; --t-stats: 96px; --t-nombre: 124px; --t-legende: 50px;
        --txt-gap: 36px; --txt-l: 940px; --t-sous: 80px; --t-titre: 104px; --t-url: 60px;
        --sol: 560px; --illu-l: 1680px; --illu-h: 784px; --t-lieu: 100px;
        --etq-x: 70px; --etq-y: 230px; --etq-l: 940px; --etq-h: 360px; --etq-align: center; --etq-texte: center; --t-etq: 104px; --t-etq5: 80px;
        --f-x: 50px; --f-y: 610px; --f-l: 980px; --f-h: 1060px; --ui: 31px; --menu-l: 0; --menu-aff: none; --pane-pad: 1.1em 1.1em;
        --champs-cols: 1fr; --plan-h: 4.2em; --services-cols: 1fr; --depot-h: 13em;
        --logo-fin: 860px; --fin-gap: 80px; --t-fin: 80px; --t-cta: 76px;
      }
      .etiquette .trait-jaune { align-self: center; }
      .bloc-stats, .stat { align-items: center; text-align: center; }
      .titre-stats { display: flex; flex-direction: column; align-items: center; }
      #s2-trait { transform-origin: center; }
      .col-plan .plan { display: none; }
      .pane { gap: 0.9em; }
      .grille-champs .duo { grid-template-columns: 1fr 1.3fr; }
      .liste-avis #avis-emilie { display: none; }
      .avis { flex-wrap: wrap; }
      .avis-actions { flex-direction: row; width: 100%; justify-content: flex-end; align-items: center; gap: 1em; }
      .galerie { grid-template-columns: 1fr 1fr; }
"""


def page(cid, w, h, css_format, racine):
    css = CSS_COMMUN.replace("{racine}", racine).replace("{w}", str(w)).replace("{h}", str(h))
    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={w}, height={h}" />
    <!-- Généré par scripts/generer.py : modifier le générateur, pas ce fichier. -->
    <script src="{racine}assets/vendor/gsap.min.js"></script>
    <style>{css}{css_format}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{cid}" data-start="0" data-duration="{DUREE}" data-width="{w}" data-height="{h}">{corps(racine)}
    </div>
    <script>{SCRIPT.replace("{cid}", cid)}
    </script>
  </body>
</html>
"""


(RACINE / "index.html").write_text(page("main", 1920, 1080, CSS_16x9, ""))
(RACINE / "compositions" / "vertical.html").write_text(page("vertical", 1080, 1920, CSS_9x16, ""))
print("index.html et compositions/vertical.html générés")
