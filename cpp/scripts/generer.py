"""Génère les captures des Custom Product Pages (CPP) de Michelin Truckfly, une série par business model.

    python3 scripts/generer.py      # écrit index.html (toutes les captures, deux formats)
    node scripts/capturer.mjs       # en tire les PNG dans png/

Formats :
- App Store (CPP)                 : 1290 × 2796 px (iPhone 6,9"), rendu en 430 × 932 × 3
- Google Play (fiche personnalisée) : 1080 × 1920 px (9:16), rendu en 360 × 640 × 3

Charte : Michelin Blue en fond, Bib pour les titres, Inter pour l'interface, jaune par petites
touches sur fond bleu uniquement, casse de phrase partout.
Les écrans de l'app sont recréés (pas de captures réelles) ; noms, avis et chiffres sont des exemples.
"""

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# --- Icônes ---------------------------------------------------------------------------------

ICO = {
    "parking": '<text x="10" y="15" text-anchor="middle" font-family="Inter" font-weight="700" font-size="14" fill="#fff">P</text>',
    "resto": '<path d="M5.5 2.5v6a2 2 0 0 0 1.6 2v7h1.6v-7a2 2 0 0 0 1.6-2v-6H9.1v4.5h-.8V2.5H7.1v4.5h-.8V2.5zM14.5 2.5c-1.6.8-2.2 2.8-2.2 5v3.5h1.6v6.5h1.6v-15z" fill="#fff"/>',
    "douche": '<path d="M10 2.5S4.5 9 4.5 12.6a5.5 5.5 0 0 0 11 0C15.5 9 10 2.5 10 2.5z" fill="#fff"/>',
    "carburant": '<path d="M4 3.5h7.5v14H4z" fill="#fff"/><path d="M11.5 7h2l2 2v5.5a1.3 1.3 0 0 1-2.6 0V11h-1.4" fill="none" stroke="#fff" stroke-width="1.5"/>',
    "lavage": '<circle cx="7" cy="12" r="3.6" fill="#fff"/><circle cx="13.5" cy="8" r="2.6" fill="#fff"/><circle cx="13.5" cy="14.5" r="2" fill="#fff"/>',
    "danger": '<path d="M10 3 L18 17 H2 Z" fill="#fff"/><path d="M10 8v4.5" stroke="#E2477A" stroke-width="2" stroke-linecap="round"/><circle cx="10" cy="14.8" r="1.1" fill="#E2477A"/>',
    "peage": '<path d="M3 17V7h14v10M3 7l7-4 7 4M7 17v-6h6v6" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/>',
    "wifi": '<path d="M3 8a10 10 0 0 1 14 0M5.5 11a6.5 6.5 0 0 1 9 0M8 14a3 3 0 0 1 4 0" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/><circle cx="10" cy="16.5" r="1.2" fill="#fff"/>',
    "cadenas": '<rect x="4.5" y="9" width="11" height="8.5" rx="1.5" fill="#fff"/><path d="M7 9V6.5a3 3 0 0 1 6 0V9" fill="none" stroke="#fff" stroke-width="1.8"/>',
}
COULEUR = {
    "parking": "#4A63E7", "resto": "#E2477A", "douche": "#8E5BD8", "carburant": "#F08A24",
    "lavage": "#1BA6C9", "danger": "#E2477A", "peage": "#061866", "wifi": "#2E9E6A", "cadenas": "#4A63E7",
}


def ico(nom, taille=20):
    return f'<svg width="{taille}" height="{taille}" viewBox="0 0 20 20" aria-hidden="true">{ICO[nom]}</svg>'


def pastille(nom, taille=34, rayon=10):
    return f'<span class="past" style="width:{taille}px;height:{taille}px;border-radius:{rayon}px;background:{COULEUR[nom]}">{ico(nom, round(taille * 0.6))}</span>'


def pin(nom, x, y, grand=False):
    t = 46 if grand else 34
    return f'<div class="pin{" grand" if grand else ""}" style="left:{x}px;top:{y}px">{pastille(nom, t, 11 if grand else 9)}</div>'


COCHE = '<svg class="coche" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="#34C759"/><path d="M6.5 12.5 L10.5 16.5 L17.5 8.5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ETOILES = '<span class="etoiles">★★★★<i>★</i></span>'
FLECHE_DROITE = '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M14 42V24a6 6 0 0 1 6-6h16" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/><path d="M30 9l9 9-9 9" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CAMION = """<svg viewBox="0 0 320 170" aria-hidden="true">
  <rect width="320" height="170" rx="14" fill="#DCE6F7"/>
  <rect y="132" width="320" height="38" fill="#C5CFDD"/>
  <rect x="22" y="40" width="186" height="84" rx="6" fill="#fff" stroke="#061866" stroke-width="5"/>
  <rect x="22" y="92" width="186" height="10" fill="#061866"/>
  <path d="M214 124V68q0-12 12-12h38q12 0 18 12l16 26v30z" fill="#061866"/>
  <rect x="246" y="64" width="30" height="24" rx="4" fill="#BFD3F2"/>
  <circle cx="62" cy="128" r="15" fill="#111"/><circle cx="100" cy="128" r="15" fill="#111"/>
  <circle cx="182" cy="128" r="15" fill="#111"/><circle cx="270" cy="128" r="15" fill="#111"/>
</svg>"""


def avatar(lettre, fond):
    return f'<span class="avatar" style="background:{fond}">{lettre}</span>'


# --- Briques d'écran ------------------------------------------------------------------------

def statut(clair=False):
    c = "clair" if clair else ""
    return f'<div class="statut {c}"><b>9:41</b><span><i></i><i></i><i></i><i></i><em></em></span></div>'


def onglets(actif):
    noms = [("carte", "Carte"), ("communaute", "Communauté"), ("gps", "GPS"), ("favoris", "Favoris"), ("profil", "Profil")]
    glyphes = {
        "carte": '<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z M9 4v14 M15 6v14" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
        "communaute": '<circle cx="9" cy="8" r="3.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3 20c0-4 3-6 6-6s6 2 6 6M16 5a3 3 0 0 1 0 6M18 14c2 .6 3 2.6 3 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "gps": '<path d="M12 3l7 17-7-4-7 4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
        "favoris": '<path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
        "profil": '<circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M4 21c0-5 4-7 8-7s8 2 8 7" fill="none" stroke="currentColor" stroke-width="2"/>',
    }
    items = "".join(
        f'<span class="{"actif" if k == actif else ""}"><svg viewBox="0 0 24 24">{glyphes[k]}</svg>{label}</span>'
        for k, label in noms
    )
    return f'<nav class="onglets">{items}</nav>'


def carte_fond(route=None, assombrir=False):
    """Plan de ville stylisé (390 × 844), avec un itinéraire optionnel."""
    routes = {
        "nav": "M195 900 L195 560 Q195 520 235 520 L330 520 Q360 520 360 490 L360 250 Q360 220 330 210 L250 180 L250 -20",
        "apercu": "M60 330 Q120 300 150 250 Q180 190 250 170 Q320 150 340 70",
        "eviter": "M195 900 L195 600 Q195 560 160 540 L80 500 Q55 488 55 450 L55 300 Q55 260 95 250 L300 230 L300 -20",
    }
    trace = ""
    if route:
        d = routes[route]
        trace = f'<path d="{d}" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#3B6CF6" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    voile = '<rect width="390" height="844" fill="#000E38" opacity=".45"/>' if assombrir else ""
    return f"""<svg class="plan" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <rect width="390" height="844" fill="#ECEFF3"/>
  <path d="M-10 700 Q120 640 210 690 T400 660 L400 760 Q300 720 200 770 T-10 790z" fill="#CFE3F5"/>
  <rect x="20" y="70" width="110" height="120" rx="8" fill="#D7EBD3"/>
  <rect x="250" y="590" width="120" height="70" rx="8" fill="#D7EBD3"/>
  <rect x="140" y="330" width="90" height="90" rx="8" fill="#E2E5EA"/>
  <rect x="20" y="380" width="90" height="70" rx="8" fill="#E2E5EA"/>
  <rect x="270" y="300" width="70" height="110" rx="8" fill="#E2E5EA"/>
  <g fill="none" stroke="#fff" stroke-linecap="round">
    <path d="M-10 230 L400 200 M-10 520 L400 520 M195 -10 V900 M55 -10 V900 M360 -10 V900 M-10 380 Q200 360 400 420 M250 -10 V520 M-10 620 L400 570" stroke-width="12"/>
    <path d="M-10 100 Q150 140 400 60 M120 520 V900 M300 520 L330 900 M-10 300 H140" stroke-width="7"/>
  </g>
  <path d="M-10 460 Q150 430 260 470 T400 450" fill="none" stroke="#FFE7A3" stroke-width="14"/>
  {trace}{voile}
</svg>"""


def camion_pos(x, y, angle=0):
    return f'<div class="moi" style="left:{x}px;top:{y}px;transform:rotate({angle}deg)"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#061866" stroke="#fff" stroke-width="4"/><path d="M20 9l8 20-8-5-8 5z" fill="#fff"/></svg></div>'


def bandeau_nav(dist, rue):
    return f'<div class="bandeau-nav"><span class="fleche">{FLECHE_DROITE}</span><div><b>{dist}</b><span>{rue}</span></div></div>'


def barre_eta(heure, detail):
    return f"""<div class="eta"><div><b>{heure}</b><span>{detail}</span></div><span class="eta-btn">Arrêts</span><span class="eta-x">×</span></div>"""


def ecran_nav(alerte=None, chip=None, route="nav", vitesse="80"):
    al = ""
    if alerte:
        icone, titre, texte = alerte
        al = f'<div class="alerte">{pastille(icone, 44, 12)}<div><b>{titre}</b><span>{texte}</span></div></div>'
    ch = f'<div class="chip-carte" style="{chip[1]}">{chip[0]}</div>' if chip else ""
    pos = (182, 640) if route != "eviter" else (182, 660)
    return f"""{carte_fond(route)}{statut()}
      {bandeau_nav("300 m", "Rue des Transporteurs")}{al}{ch}
      {camion_pos(*pos)}
      <div class="vitesse">{vitesse}</div>
      {barre_eta("14:32", "3 h 48 · 312 km")}"""


def entete(titre, retour=True, action=""):
    r = '<span class="retour">‹</span>' if retour else ""
    return f'<div class="entete">{statut(True)}<div class="entete-l">{r}<b>{titre}</b><span class="act">{action}</span></div></div>'


def champ(label, valeur, coche=False):
    return f'<div class="champ"><span>{label}</span><b>{valeur}</b>{COCHE if coche else ""}</div>'


def interrupteur(label, on):
    return f'<div class="champ"><span>{label}</span><i class="inter {"on" if on else ""}"></i></div>'


def ligne_arret(icone, nom, detail, info, extra=""):
    return f'<div class="arret">{pastille(icone, 40, 11)}<div><b>{nom}</b><span>{detail}</span>{extra}</div><em>{info}</em></div>'


def photo_lieu(variante=0):
    ciel = ["#BFD3F2", "#F6D38B"][variante]
    return f"""<svg viewBox="0 0 390 230" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <rect width="390" height="230" fill="{ciel}"/>
  <rect y="170" width="390" height="60" fill="#8A929E"/>
  <path d="M0 200 H390" stroke="#fff" stroke-width="3" stroke-dasharray="26 20"/>
  <rect x="40" y="80" width="200" height="92" fill="#F5F3F1" stroke="#061866" stroke-width="4"/>
  <path d="M30 84 L140 40 L250 84Z" fill="#E2477A" stroke="#061866" stroke-width="4" stroke-linejoin="round"/>
  <rect x="70" y="112" width="40" height="30" fill="#BFD3F2" stroke="#061866" stroke-width="3"/>
  <rect x="160" y="112" width="40" height="60" fill="#061866"/>
  <rect x="96" y="56" width="88" height="20" rx="4" fill="#061866"/>
  <text x="140" y="71" text-anchor="middle" font-family="Inter" font-weight="700" font-size="12" fill="#FFFF1A">RELAIS</text>
  <rect x="262" y="104" width="112" height="56" rx="5" fill="#fff" stroke="#061866" stroke-width="4"/>
  <path d="M374 160v-40q0-8 8-8h8v48z" fill="#061866"/>
  <circle cx="290" cy="164" r="9" fill="#111"/><circle cx="350" cy="164" r="9" fill="#111"/>
</svg>"""


def services(liste):
    return '<div class="services">' + "".join(f"<span>{pastille(i, 40, 12)}<em>{t}</em></span>" for i, t in liste) + "</div>"


def avis(nom, lettre, fond, texte, quand="il y a 2 jours", likes=None, reponse=None):
    lk = f'<div class="like">♥ J\'aime · <b>{likes}</b></div>' if likes is not None else ""
    rp = f'<div class="reponse"><b>Réponse de l\'établissement</b><p>{reponse}</p></div>' if reponse else ""
    return f"""<div class="avis">
        <div class="avis-tete">{avatar(lettre, fond)}<div><b>{nom}</b><span>{quand}</span></div>{ETOILES}</div>
        <p>{texte}</p>{lk}{rp}
      </div>"""


def fiche_lieu(proprio=False):
    badge = '<span class="verifie">' + COCHE + "Géré par l'établissement</span>" if proprio else ""
    return f"""<div class="photo-lieu">{photo_lieu(0)}{statut()}</div>
      <div class="fiche">
        <div class="poignee"></div>
        {badge}
        <h2>Relais de la Bascule</h2>
        <p class="sous-fiche">Restaurant · Parking poids lourds · A6, sortie 24</p>
        <div class="note"><b>4,5</b>{ETOILES}<span>(128 avis)</span><em class="ouvert">Ouvert · 5:00–23:00</em></div>
        {services([("parking", "40 places"), ("douche", "Douches"), ("resto", "Restaurant"), ("wifi", "Wi-Fi")])}
        <div class="boutons"><span class="btn plein">Itinéraire</span><span class="btn">Appeler</span></div>
        {avis("Mathieu P.", "M", "#A6E8B8", "Super accueil, parking éclairé et douches propres. Je recommande !")}
      </div>"""


# --- Écrans par business model --------------------------------------------------------------

def e_gabarit(titre="Mon camion", vehicules=None):
    if vehicules:
        lignes = "".join(
            f'<div class="vehicule{" sel" if i == 0 else ""}"><div class="v-ill">{CAMION}</div><div><b>{n}</b><span>{d}</span></div>{COCHE if i == 0 else ""}</div>'
            for i, (n, d) in enumerate(vehicules)
        )
        return f"""{entete(titre, action="+")}<div class="corps">
        <p class="rubrique">Véhicules de la flotte</p>{lignes}
        <p class="rubrique">Chaque profil a son itinéraire</p>
        {champ("Hauteur · largeur", "4,00 m · 2,55 m")}{champ("Poids total", "44 t")}{interrupteur("Matières dangereuses (ADR)", True)}
      </div>"""
    return f"""{entete(titre)}<div class="corps">
        <div class="grand-camion">{CAMION}</div>
        {champ("Hauteur", "4,00 m")}{champ("Largeur", "2,55 m")}{champ("Longueur", "16,50 m")}
        {champ("Poids total", "44 t")}{champ("Poids par essieu", "11,5 t")}
        {interrupteur("Matières dangereuses (ADR)", False)}
        <span class="btn plein large">Calculer l'itinéraire</span>
      </div>"""


def e_arrets(titre="Sur ton itinéraire", securise=False):
    lignes = [
        ligne_arret("parking", "Aire de Saint-Ambreuil", "Parking poids lourds · 60 places", "42 km<br>15:10",
                    '<span class="dispo">Places disponibles</span>' if securise else ""),
        ligne_arret("resto", "Relais de la Bascule", "Restaurant · Douches", "88 km<br>15:52"),
        ligne_arret("cadenas" if securise else "douche", "Truck Parking Mâcon Nord" if securise else "Station Total Mâcon",
                    "Parking sécurisé · Gardien 24 h/24" if securise else "Douches · Carburant", "131 km<br>16:31",
                    '<span class="dispo">Places disponibles</span>' if securise else ""),
        ligne_arret("lavage", "Station de lavage PL", "Lavage poids lourds", "176 km<br>17:12"),
    ]
    return f"""<div class="mini-carte">{carte_fond("apercu")}{statut()}
        {pin("parking", 104, 270)}{pin("resto", 160, 214)}{pin("cadenas" if securise else "douche", 238, 150)}{pin("lavage", 300, 96)}
        {camion_pos(44, 314, 40)}</div>
      <div class="fiche liste">
        <div class="poignee"></div>
        <h2>{titre}</h2>
        <div class="filtres"><span class="on">Tout</span><span>Parkings</span><span>Restos</span><span>Douches</span></div>
        {"".join(lignes)}
      </div>"""


def e_offre(titre, sous, avantages, cta, b2b=False):
    lis = "".join(f"<li>{COCHE}<span>{a}</span></li>" for a in avantages)
    return f"""<div class="offre">{statut(True)}<span class="eta-x blanc">×</span>
        <div class="offre-tete"><span class="badge-j">{"Entreprises" if b2b else "Premium"}</span><h2>{titre}</h2><p>{sous}</p></div>
        <ul>{lis}</ul>
        <span class="btn jaune large">{cta}</span>
        <p class="petit">{"Réponse de notre équipe sous 48 h" if b2b else "Abonnement géré depuis ton store"}</p>
      </div>"""


def e_explorer():
    pins = [("parking", 70, 190), ("resto", 140, 250), ("douche", 290, 190), ("carburant", 210, 260),
            ("parking", 300, 330), ("resto", 40, 300), ("lavage", 120, 420), ("parking", 250, 440),
            ("carburant", 330, 520), ("resto", 60, 520), ("douche", 180, 360)]
    return f"""{carte_fond()}{statut()}
      <div class="recherche"><svg viewBox="0 0 24 24"><circle cx="10" cy="10" r="6.5" fill="none" stroke="#6E6E73" stroke-width="2.4"/><path d="M15 15l5 5" stroke="#6E6E73" stroke-width="2.4" stroke-linecap="round"/></svg>Rechercher un lieu, une ville…</div>
      <div class="chips"><span class="on">{ico("parking", 14)}Parkings</span><span>Restaurants</span><span>Douches</span><span>Lavage</span></div>
      {"".join(pin(*p) for p in pins)}{pin("resto", 186, 196, True)}
      <div class="mini-fiche">{pastille("resto", 52, 14)}<div><b>Relais de la Bascule</b><span>Restaurant · Parking PL · 2,4 km</span><span class="note-s">4,5 {ETOILES} (128)</span></div></div>
      {onglets("carte")}"""


def e_signaler():
    items = [("danger", "Accident"), ("peage", "Contrôle"), ("carburant", "Bouchon"), ("danger", "Danger"),
             ("parking", "Parking complet"), ("lavage", "Météo")]
    cases = "".join(f"<span>{pastille(i, 62, 31)}<em>{t}</em></span>" for i, t in items)
    return f"""{carte_fond("nav", assombrir=True)}{statut(True)}{camion_pos(182, 440)}
      <div class="fiche signaler"><div class="poignee"></div><h2>Signaler</h2><p class="sous-fiche">Préviens les conducteurs autour de toi</p>
        <div class="grille">{cases}</div>
        <div class="merci">{COCHE}<span>Merci ! <b>214 conducteurs</b> ont été prévenus.</span></div>
      </div>"""


def e_communaute():
    return f"""{entete("Communauté", retour=False)}<div class="corps gris-fond">
        <div class="filtres"><span class="on">Amis</span><span>Autour de moi</span><span>Mes alertes</span></div>
        <div class="post"><div class="avis-tete">{avatar("V", "#BFD3F2")}<div><b>Vanessa Y.</b><span>a signalé un danger · A7 · il y a 5 min</span></div></div>
          <div class="post-alerte">{pastille("danger", 36, 18)}<span>Objet sur la voie de droite, km 214</span></div><div class="like">♥ J'aime · <b>23</b></div></div>
        {avis("Mathieu P.", "M", "#A6E8B8", "Parking calme la nuit, resto ouvert tôt. Parfait avant de reprendre la route.", "a donné son avis sur Relais de la Bascule", likes=12)}
        <div class="post"><div class="avis-tete">{avatar("C", "#F6D38B")}<div><b>Charlie G.</b><span>a ajouté son camion · il y a 1 h</span></div></div>
          <div class="post-camion">{CAMION}</div></div>
      </div>{onglets("communaute")}"""


def e_langues():
    langues = ["Français", "Deutsch", "Español", "Italiano", "Polski", "Português", "Română", "Nederlands", "Čeština"]
    li = "".join(f'<div class="champ"><span>{l}</span>{COCHE if i == 0 else ""}</div>' for i, l in enumerate(langues))
    return f"""{entete("Langue de l'application")}<div class="corps"><p class="rubrique">Choisis ta langue</p>{li}</div>"""


def e_edition():
    photos = "".join(f'<span class="ph">{photo_lieu(i % 2)}</span>' for i in range(2)) + '<span class="ph plus">+</span>'
    return f"""{entete("Ma fiche établissement", action="Enregistrer")}<div class="corps">
        <p class="rubrique">Photos</p><div class="photos">{photos}</div>
        <p class="rubrique">Informations</p>
        {champ("Horaires", "Lun–sam · 5:00–23:00")}{champ("Places poids lourds", "40")}{champ("Téléphone", "03 85 00 00 00")}
        <p class="rubrique">Services</p>
        {interrupteur("Douches", True)}{interrupteur("Restaurant", True)}{interrupteur("Wi-Fi", True)}{interrupteur("Parking sécurisé", False)}
      </div>"""


def e_reponse():
    return f"""{entete("Avis sur votre établissement")}<div class="corps gris-fond">
        <div class="resume"><b>4,5</b><div>{ETOILES}<span>128 avis</span></div></div>
        {avis("Mathieu P.", "M", "#A6E8B8", "Super accueil, parking éclairé et douches propres. Je recommande !",
              reponse="Merci Mathieu ! Au plaisir de vous revoir sur l'A6.")}
        {avis("Nicolas J.", "N", "#C9C3F5", "Bon repas, mais le parking était complet vers 21 h.", "il y a 5 jours")}
        <div class="saisie">Répondre à Nicolas J.…<span class="btn plein petit">Envoyer</span></div>
      </div>"""


def e_stats():
    barres = [38, 52, 46, 61, 70, 58, 84]
    jours = ["L", "M", "M", "J", "V", "S", "D"]
    b = "".join(f'<span><i style="height:{h}%"></i><em>{j}</em></span>' for h, j in zip(barres, jours))
    return f"""{entete("Statistiques", action="30 j")}<div class="corps gris-fond">
        <div class="kpis">
          <div class="kpi"><span>Vues de la fiche</span><b>3 420</b><em>+18 %</em></div>
          <div class="kpi"><span>Itinéraires lancés</span><b>412</b><em>+9 %</em></div>
          <div class="kpi"><span>Appels</span><b>58</b><em>+4 %</em></div>
          <div class="kpi"><span>Nouveaux avis</span><b>17</b><em>+6</em></div>
        </div>
        <div class="graphe"><b>Visites par jour</b><div class="barres">{b}</div></div>
      </div>"""


def e_mise_en_avant():
    return f"""{carte_fond()}{statut()}
      {pin("parking", 70, 170)}{pin("carburant", 290, 160)}{pin("douche", 300, 330)}{pin("resto", 40, 310)}{pin("lavage", 250, 450)}
      {pin("resto", 172, 250, True)}
      <div class="bulle-offre">Café offert aux routiers</div>
      <div class="fiche promo"><div class="poignee"></div>
        <span class="tag-promo">Offre de l'établissement</span>
        <h2>Relais de la Bascule</h2><p class="sous-fiche">Restaurant · 2,4 km · Ouvert</p>
        <div class="offre-carte">{pastille("resto", 48, 14)}<div><b>Café offert aux routiers</b><span>Tous les matins de 5:00 à 9:00, sur présentation de l'app</span></div></div>
        <div class="boutons"><span class="btn plein">Itinéraire</span><span class="btn">Voir la fiche</span></div>
      </div>"""


# --- Les CPP --------------------------------------------------------------------------------

AVANTAGES_PREMIUM = ["GPS poids lourd en 44 pays", "Itinéraire adapté à ton gabarit", "Alerte à l'approche des péages",
                     "Arrêts poids lourds sur ta route", "Sans publicité"]
AVANTAGES_B2B = ["GPS poids lourd pour chaque conducteur", "Profils de véhicules : gabarit, poids, ADR",
                 "Alertes communautaires en temps réel", "Parkings et arrêts poids lourds en Europe", "Accompagnement dédié"]

CPP = [
    {
        "id": "gps-premium",
        "nom": "GPS Premium (abonnement)",
        "captures": [
            ("Le GPS pensé pour <em>ton camion</em>", "Navigation poids lourd dans 44 pays", ecran_nav()),
            ("Un itinéraire selon <em>ton gabarit</em>", "Hauteur, largeur, poids : on évite les mauvaises surprises", e_gabarit()),
            ("Le péage ? <em>Tu le vois venir</em>", "Une alerte avant d'y arriver", ecran_nav(alerte=("peage", "Péage dans 2 km", "Prépare ton badge"))),
            ("Tes arrêts <em>sur ta route</em>", "Parkings, restos et douches poids lourds", e_arrets()),
            ("Passe à <em>Premium</em>", "Et roule sans publicité", e_offre("Michelin Truckfly Premium", "Tout ce qu'il faut pour rouler sereinement", AVANTAGES_PREMIUM, "Passer à Premium")),
        ],
    },
    {
        "id": "communaute",
        "nom": "App gratuite et communauté (publicité)",
        "captures": [
            ("Trouve où t'arrêter, <em>partout en Europe</em>", "Parkings, restos, douches, lavages poids lourds", e_explorer()),
            ("Des avis laissés <em>par des routiers</em>", "Pour choisir ton arrêt en confiance", fiche_lieu()),
            ("Préviens les autres <em>en un geste</em>", "Accidents, contrôles, dangers en temps réel", e_signaler()),
            ("Ta communauté <em>de routiers</em>", "Suis tes amis et leurs bons plans", e_communaute()),
            ("Gratuit, <em>dans ta langue</em>", "Plus de 700 000 conducteurs dans 44 pays", e_langues()),
        ],
    },
    {
        "id": "etablissements",
        "nom": "Établissements (owners)",
        "captures": [
            ("Faites venir <em>les poids lourds</em> chez vous", "Votre établissement visible par 700 000 conducteurs", fiche_lieu(proprio=True)),
            ("Votre fiche à jour <em>en 2 minutes</em>", "Horaires, places, services, photos", e_edition()),
            ("Répondez <em>aux avis</em>", "Montrez aux routiers que vous les écoutez", e_reponse()),
            ("Suivez <em>vos visites</em>", "Vues, itinéraires lancés, appels", e_stats()),
            ("Mettez en avant <em>vos offres</em>", "Sur la carte, au moment où ils cherchent un arrêt", e_mise_en_avant()),
        ],
    },
    {
        "id": "entreprises",
        "nom": "Entreprises de transport (B2B)",
        "captures": [
            ("Le GPS poids lourd <em>pour votre flotte</em>", "Michelin Truckfly pour les entreprises", ecran_nav(chip=("Pont 3,50 m évité", "left:96px;top:390px"), route="eviter")),
            ("Un profil <em>par véhicule</em>", "Gabarit, poids, matières dangereuses", e_gabarit("Ma flotte", [("Semi-remorque", "4,00 m · 16,50 m · 44 t"), ("Porteur", "3,60 m · 9,80 m · 19 t"), ("Citerne ADR", "3,90 m · 12,00 m · 40 t")])),
            ("Moins d'imprévus <em>sur la route</em>", "Péages, dangers, bouchons signalés à l'avance", ecran_nav(alerte=("danger", "Danger signalé à 4 km", "Objet sur la voie de droite"))),
            ("Des pauses <em>mieux préparées</em>", "Parkings sécurisés et services sur l'itinéraire", e_arrets("Pauses sur l'itinéraire", securise=True)),
            ("Équipez <em>vos conducteurs</em>", "Une offre adaptée à la taille de votre flotte", e_offre("Michelin Truckfly pour les entreprises", "Le GPS et la communauté au service de vos conducteurs", AVANTAGES_B2B, "Contacter l'équipe", b2b=True)),
        ],
    },
]

# --- Mise en page ---------------------------------------------------------------------------

VAGUES = [
    "M-40 620 Q140 520 260 600 T520 560",
    "M-40 540 Q100 680 250 600 T520 650",
    "M-40 700 Q160 560 300 640 T520 520",
    "M-40 580 Q180 700 280 580 T520 620",
    "M-40 650 Q120 540 240 620 T520 580",
]


def capture(cpp, i, titre, sous, ecran, fmt):
    vague = VAGUES[i % len(VAGUES)]
    return f"""<section class="shot {fmt}" id="{cpp['id']}-{i + 1:02d}-{fmt}" data-cpp="{cpp['id']}" data-fmt="{fmt}">
    <svg class="vague" viewBox="0 0 480 1000" preserveAspectRatio="none" aria-hidden="true"><path d="{vague}" fill="none" stroke="#FFFF1A" stroke-width="16" stroke-linecap="round"/></svg>
    <div class="textes"><h1>{titre}</h1><p>{sous}</p></div>
    <div class="tel"><div class="ecran">{ecran}</div></div>
  </section>"""


CSS = (RACINE / "scripts" / "style.css").read_text()


def page():
    blocs = []
    for cpp in CPP:
        for fmt, label in (("ios", "App Store · 1290 × 2796"), ("play", "Google Play · 1080 × 1920")):
            shots = "".join(capture(cpp, i, *c, fmt) for i, c in enumerate(cpp["captures"]))
            blocs.append(f'<div class="serie"><h2>{cpp["nom"]} <small>{label}</small></h2><div class="rangee">{shots}</div></div>')
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>CPP Michelin Truckfly</title><style>{CSS}</style></head>
<body>
<header class="entete-planche"><h1>Custom Product Pages · Michelin Truckfly</h1><p>Une série de 5 captures par business model, aux formats App Store et Google Play. Écrans recréés, noms et chiffres d'exemple.</p></header>
{"".join(blocs)}
</body></html>"""


if __name__ == "__main__":
    (RACINE / "index.html").write_text(page())
    print("index.html écrit :", sum(len(c["captures"]) for c in CPP) * 2, "captures")
