"""Libellés traduits posés sur les captures de l'app (interstitiel photos, versions hors français).

Chaque zone recouvre un libellé de l'interface d'un aplat de la couleur du fond (relevée dans la
capture) et réécrit le texte traduit en Inter. Le contenu publié par les utilisateurs (avis, noms
de lieux, horaires) reste en français. Coordonnées en pixels de la capture détourée (289 × 571).
"""

from collections import Counter
from functools import lru_cache
from pathlib import Path

from PIL import Image

ICI = Path(__file__).resolve().parent
L, H = 289, 571

BLEU_LIEN = "#1a2a7a"
GRIS = "#9a9aa2"

# Libellés par langue.
TRAD = {
    "en": dict(salut="Hi louna!", enligne="2 friends online", fil="Activity feed", tout="All", amis="Friends",
               activite="Clémentine P. liked a review by <b>F-Y P.</b><br>at:", ilya="6 days ago", sanote="Rating:",
               ouvert="Open", signaler="Report", jaime="Like", aimepar="Liked by", carte="Map", communaute="Community",
               ferme="Closed", ajouter="Add", aller="Go", appeler="Call", favoris="Favorites", voirplus="More",
               motgerant="A word from the manager", cree="Place created by", modifie="Edited last month by",
               categorie="Category", gps="with the GPS", lieux="Places visited", avis="Reviews", note="Average rating",
               toutmoment="That’s all for now"),
    "de": dict(salut="Hallo louna!", enligne="2 Freunde online", fil="Aktivitäten", tout="Alle", amis="Freunde",
               activite="Clémentine P. gefällt eine Bewertung von <b>F-Y P.</b><br>zu:", ilya="vor 6 Tagen", sanote="Bewertung:",
               ouvert="Geöffnet", signaler="Melden", jaime="Gefällt mir", aimepar="Gefällt", carte="Karte", communaute="Community",
               ferme="Geschlossen", ajouter="Hinzufügen", aller="Los", appeler="Anrufen", favoris="Favoriten", voirplus="Mehr",
               motgerant="Worte des Betreibers", cree="Betrieb erstellt von", modifie="Letzten Monat geändert von",
               categorie="Kategorie", gps="mit dem GPS", lieux="Besuchte Orte", avis="Bewertungen", note="Durchschnitt",
               toutmoment="Das ist alles für den Moment"),
    "nl": dict(salut="Hoi louna!", enligne="2 vrienden online", fil="Activiteiten", tout="Alles", amis="Vrienden",
               activite="Clémentine P. vond een review van <b>F-Y P.</b><br>leuk bij:", ilya="6 dagen geleden", sanote="Beoordeling:",
               ouvert="Open", signaler="Melden", jaime="Vind ik leuk", aimepar="Leuk gevonden door", carte="Kaart", communaute="Community",
               ferme="Gesloten", ajouter="Toevoegen", aller="Ga", appeler="Bellen", favoris="Favorieten", voirplus="Meer",
               motgerant="Woord van de uitbater", cree="Locatie aangemaakt door", modifie="Vorige maand gewijzigd door",
               categorie="Categorie", gps="met de GPS", lieux="Bezochte plekken", avis="Reviews", note="Gemiddelde",
               toutmoment="Dat is alles voor nu"),
    "pl": dict(salut="Cześć louna!", enligne="2 znajomych online", fil="Aktywność", tout="Wszystko", amis="Znajomi",
               activite="Clémentine P. polubiła opinię <b>F-Y P.</b><br>o:", ilya="6 dni temu", sanote="Ocena:",
               ouvert="Otwarte", signaler="Zgłoś", jaime="Lubię to", aimepar="Polubione przez", carte="Mapa", communaute="Społeczność",
               ferme="Zamknięte", ajouter="Dodaj", aller="Jedź", appeler="Zadzwoń", favoris="Ulubione", voirplus="Więcej",
               motgerant="Słowo od kierownika", cree="Obiekt dodany przez", modifie="Zmieniono w zeszłym miesiącu przez",
               categorie="Kategoria", gps="z GPS", lieux="Odwiedzone miejsca", avis="Opinie", note="Średnia ocena",
               toutmoment="To na razie wszystko"),
    "it": dict(salut="Ciao louna!", enligne="2 amici online", fil="Attività", tout="Tutti", amis="Amici",
               activite="A Clémentine P. piace una recensione di <b>F-Y P.</b><br>su:", ilya="6 giorni fa", sanote="Voto:",
               ouvert="Aperto", signaler="Segnala", jaime="Mi piace", aimepar="Piace a", carte="Mappa", communaute="Community",
               ferme="Chiuso", ajouter="Aggiungi", aller="Vai", appeler="Chiama", favoris="Preferiti", voirplus="Altro",
               motgerant="La parola del gestore", cree="Locale creato da", modifie="Modificato il mese scorso da",
               categorie="Categoria", gps="con il GPS", lieux="Luoghi visitati", avis="Recensioni", note="Voto medio",
               toutmoment="Per ora è tutto"),
    "es": dict(salut="¡Hola louna!", enligne="2 amigos en línea", fil="Actividad", tout="Todo", amis="Amigos",
               activite="A Clémentine P. le gustó una reseña de <b>F-Y P.</b><br>en:", ilya="hace 6 días", sanote="Su nota:",
               ouvert="Abierto", signaler="Denunciar", jaime="Me gusta", aimepar="Le gusta a", carte="Mapa", communaute="Comunidad",
               ferme="Cerrado", ajouter="Añadir", aller="Ir", appeler="Llamar", favoris="Favoritos", voirplus="Más",
               motgerant="Palabras del gerente", cree="Establecimiento creado por", modifie="Modificado el mes pasado por",
               categorie="Categoría", gps="con el GPS", lieux="Lugares visitados", avis="Reseñas", note="Nota media",
               toutmoment="Eso es todo por ahora"),
}

NOM_LIEN = f' <b style="color:{BLEU_LIEN}; text-decoration: underline">Fabienne B.</b>'
NAV = [("carte", 56, 26, 400, "#8a8a92"), ("communaute", 174, 52, 700, "#0a1a6b"), ("amis", 232, 24, 400, "#8a8a92")]

# Zones par capture : (clé ou modèle, x, y, largeur, hauteur, ancrage, taille de police, graisse, couleur).
# Ancrage : g = gauche, c = centré sur x, d = bord droit en x + largeur, b = bloc sur plusieurs lignes.
ZONES = {
    "fil-photo.png": [
        ("salut", 72, 64, 105, 18, "g", 15.5, 700, "#fff"),
        ("enligne", 82, 85, 75, 10, "g", 8.5, 400, "#fff"),
        ("fil", 26, 117, 76, 15, "g", 12, 700, "#000"),
        ("tout", 171, 116, 34, 17, "c", 9.5, 700, "#0a1a6b"),
        ("✓ {amis}", 231, 115, 56, 19, "c", 9, 700, "#fff"),
        ("activite", 72, 149, 186, 23, "b", 8, 400, GRIS),
        ("ilya", 72, 190, 58, 11, "g", 8.5, 400, GRIS),
        ("sanote", 35, 327, 48, 13, "g", 9.5, 700, "#000"),
        ("ouvert", 35, 368, 36, 11, "g", 9, 400, "#4f8f45"),
        ("<u>{signaler}</u>", 35, 433, 37, 12, "g", 8.5, 700, BLEU_LIEN),
        ("jaime", 205, 433, 29, 11, "d", 8.3, 400, BLEU_LIEN),
        ('{aimepar} <b style="color:#000">Clémentine P.</b>', 53, 452, 108, 13, "g", 8.5, 400, "#b8b8c0"),
        ("bouton", 144, 473),
    ],
    "etablissement-ajouter.png": [
        ("ferme", 31, 137, 30, 11, "g", 9, 400, "#d0453a"),
        ("ajouter", 144, 234, 36, 11, "c", 7.5, 700, "#000"),
        ("aller", 50.5, 339, 22, 12, "c", 8, 700, "#fff"),
        ("appeler", 111.7, 339, 30, 12, "c", 8, 700, "#fff"),
        ("favoris", 172.3, 339, 30, 12, "c", 8, 700, "#fff"),
        ("voirplus", 235.3, 339, 42, 12, "c", 8, 700, "#fff"),
        ("motgerant", 31, 397, 128, 17, "g", 14, 700, "#8a8a95"),
        ("{cree}" + NOM_LIEN, 31, 473, 170, 12, "g", 8.5, 400, GRIS),
        ("{modifie}" + NOM_LIEN, 31, 488, 184, 12, "g", 8.5, 400, GRIS),
        ("categorie", 31, 509, 49, 12, "g", 9, 700, "#000"),
    ],
    "profil-photos.png": [
        ("gps", 58, 77.5, 46, 8, "c", 6.3, 700, "#000"),
        ("lieux", 115, 77.5, 42, 8, "c", 6.3, 400, "#9a9ab0"),
        ("avis", 175, 77.5, 18, 8, "c", 6.3, 400, "#9a9ab0"),
        ("note", 232, 77.5, 46, 8, "c", 6.3, 400, "#9a9ab0"),
        ("toutmoment", 145, 463, 128, 13, "c", 8.5, 400, "#a0a0a8"),
        ("bouton", 144, 465),
    ],
}
for _image in ("fil-photo.png", "profil-photos.png"):
    ZONES[_image] += [(cle, x, 519, w, 12, "c", 7.8, gr, coul) for cle, x, w, gr, coul in NAV]


@lru_cache(maxsize=None)
def _image(nom):
    return Image.open(ICI / "assets" / nom).convert("RGB")


def couleur_fond(nom, x, y, w, h):
    """Couleur dominante de la zone : le fond, le texte n'y occupe qu'une minorité de pixels."""
    im = _image(nom)
    x0, y0 = max(int(x), 0), max(int(y), 0)
    pixels = [im.getpixel((i, j)) for i in range(x0, min(int(x + w), L)) for j in range(y0, min(int(y + h), H))]
    r, g, b = Counter((p[0] // 8 * 8, p[1] // 8 * 8, p[2] // 8 * 8) for p in pixels).most_common(1)[0][0]
    return f"rgb({r + 4}, {g + 4}, {b + 4})"


def pc(v, total):
    return f"{v / total * 100:.3f}%"


def calques(image, lang):
    """HTML des libellés traduits pour une capture, ou chaîne vide (français ou capture sans zone)."""
    if lang not in TRAD or image not in ZONES:
        return ""
    t = TRAD[lang]
    html = ""
    for zone in ZONES[image]:
        if zone[0] == "bouton":  # bouton « remonter » de l'app, redessiné par-dessus le texte traduit
            _, x, y = zone
            html += (f'<span class="trad-bouton" style="left:{pc(x, L)}; top:{pc(y, H)}">'
                     '<svg viewBox="0 0 24 24"><path d="M6 15l6-6 6 6" fill="none" stroke="#0a1a6b" stroke-width="3" '
                     'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')
            continue
        cle, x, y, w, h, ancre, taille, graisse, couleur = zone
        texte = cle.format(**t) if "{" in cle else t[cle]
        fond = couleur_fond(image, x - (w / 2 if ancre == "c" else 0), y, w, h)
        if ancre == "c":
            pos = f"left:{pc(x, L)}; translate:-50% 0; justify-content:center;"
        elif ancre == "d":
            pos = f"right:{pc(L - x - w, L)}; justify-content:flex-end;"
        else:
            pos = f"left:{pc(x, L)};"
        bloc = " bloc" if ancre == "b" else ""
        largeur = f"width:{pc(w, L)};" if ancre == "b" else f"min-width:{pc(w, L)};"
        html += (f'<span class="trad{bloc}" style="{pos} top:{pc(y, H)}; {largeur} min-height:{pc(h, H)}; '
                 f'background:{fond}; color:{couleur}; font-size:{taille / L * 100:.3f}cqw; font-weight:{graisse}"><span>{texte}</span></span>')
    return html


CSS = """
.trad { position: absolute; display: flex; align-items: center; white-space: nowrap; line-height: 1.15;
  font-family: "Inter", sans-serif; padding: 0 0.4cqw; }
.trad.bloc { display: block; white-space: normal; line-height: 1.3; padding: 0; }
.trad b { font-weight: 700; }
.trad-bouton { position: absolute; width: 8.6cqw; height: 8.6cqw; translate: -50% -50%; border-radius: 50%; background: #fff;
  box-shadow: 0 0.6cqw 2cqw rgba(0, 0, 0, 0.18); display: flex; align-items: center; justify-content: center; }
.trad-bouton svg { width: 55%; height: 55%; }
"""
