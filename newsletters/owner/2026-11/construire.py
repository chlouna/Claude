"""Newsletter owners novembre 2026 : même structure et couleurs qu'octobre (template_user.yaml).
Sujets : fermeture temporaire (fêtes), horaires des fêtes, nouveaux j'aime, fiche des fêtes en 3 points."""
import copy, re, uuid, yaml
from pathlib import Path
D = Path(__file__).parent
src = yaml.safe_load(open(D / "template_user.yaml"))
R = src["body"]["content"][0]["content"]
def it(i): return R[i]["content"][0]["content"]
NB = "&nbsp;"
BLK = 'style="color: rgb(0, 0, 0);"'; WH = 'style="color: rgb(255, 255, 255);"'; BL = 'style="color: rgb(6, 24, 102);"'
def P(t, st=BLK): return f'<p><span {st}>{t}</span></p>'
BR = "<p><br></p>"
FAQ = "https://faq.truckfly.com/hc/fr/categories/360006219672-FAQ-pour-les-propri%C3%A9taires-d-%C3%A9tablissement"
LOGIN = "https://truckfly.com/owner/login?utm_source=brevo&utm_medium=newsletter"
PLACEHOLDER = "https://creative-assets.mailinblue.com/react-editor/placeholder-images/defaultproduct.png"
def btn(b, label, href, color="rgb(0, 0, 0)"):
    h = f'<p><span style="color: {color};"><strong>{label}</strong></span></p>'
    b["text"] = h; b["content"]["text"] = h; b["content"]["href"] = href

# Objet
src["subject"] = "Fermé pendant les fêtes" + " " + "? Prévenez les routiers"

# Header : Michelin Truckfly (jamais en capitales)
for x in it(1):
    if isinstance(x.get("content"), str): x["content"] = x["content"].replace("MICHELIN Truckfly", "Michelin Truckfly")

# Intro
it(3)[1]["content"] = (P("Décembre approche, et avec lui les fêtes de fin d’année. Pour les routiers, c’est une période chargée" + NB + ": ils préparent leurs arrêts à l’avance et vérifient dans l’appli où ils pourront manger, se doucher et dormir.")
    + BR + P("C’est le moment de <strong>leur dire clairement si vous êtes ouvert ou fermé.</strong>")
    + BR + P("Ce mois-ci, nous vous montrons comment le faire en quelques minutes."))

# Au programme (même encadré)
items = ["Fermé pendant les fêtes" + NB + "? La fermeture temporaire", "Le conseil du mois" + NB + ": vos horaires des fêtes",
         "Nouveau" + NB + ": les routiers peuvent liker les avis", "Votre fiche aux couleurs de Noël"]
h = f'<p><span {BL}><strong>Au programme' + NB + ':' + NB + '</strong></span></p><p><span {BL}><strong><br></strong></span></p>'
for n, t in enumerate(items, 1):
    h += f'<p><span {BL}><strong>{n}.' + NB + f'</strong><strong>{t}</strong></span></p>' + (f'<p><span {BL}><br></span></p>' if n < 4 else "")
it(4)[0]["content"] = h

# 1. Fermeture temporaire (section blanche, ex « Profil Trucker »)
s = it(5)
s[0]["content"] = f'<p><span {WH}><strong>Bon à savoir pour les fêtes</strong></span></p>'
s[1]["content"] = f'<h2 class="default-heading2"><span {BL}>Fermé pendant les fêtes' + NB + '? Utilisez la fermeture temporaire</span></h2>'
s[2]["content"] = (P("En fin d’année, certains d’entre vous annoncent leurs dates de congés dans la description de leur fiche ou en laissant un commentaire. Mais un routier pressé ne les voit pas toujours… et risque de trouver porte close.")
    + BR + P("La fonctionnalité <strong>Fermeture temporaire</strong> est faite pour ça" + NB + ": pendant vos dates de fermeture, <strong>le marqueur de votre établissement devient transparent sur la carte</strong> et <strong>un message en rouge apparaît sur votre fiche.</strong> Tout revient à la normale automatiquement dès votre réouverture.")
    + BR + P("<strong>Comment faire" + NB + "?</strong>")
    + '<ol><li ' + BLK + '>Connectez-vous à votre <a href="' + LOGIN + '" target="_blank" style="color: rgb(0, 146, 255); text-decoration: underline;">espace propriétaire</a>.</li>'
    + '<li ' + BLK + '>Cliquez sur «' + NB + 'Mes horaires d’ouverture' + NB + '» dans le menu à gauche.</li>'
    + '<li ' + BLK + '>Dans «' + NB + 'Ma fermeture temporaire' + NB + '», indiquez vos dates de début et de fin, puis enregistrez.</li></ol>'
    + BR + f'<p><span {BLK}>Besoin d’aide' + NB + f'? <a href="{FAQ}" target="_blank" style="color: rgb(0, 146, 255); text-decoration: underline;">Consultez notre FAQ propriétaires</a></span></p>')
s[3]["content"] = (f'<p><strong><span style="background-color: rgb(228, 234, 242); color: rgb(6, 24, 102);">Votre levier' + NB + ':</span></strong>'
    f'<span style="color: rgb(6, 24, 102); background-color: rgb(228, 234, 242);">' + NB + 'déclarez vos dates dès maintenant, pour que les routiers qui préparent leurs trajets de décembre les voient à temps.</span></p>')
s[4]["content"] = {"href": LOGIN, "src": PLACEHOLDER}
s[4]["layout"]["default"].update({"canvas-height": "310px", "width": "100%"})
btn(s[5], "Je déclare ma fermeture", LOGIN); s[5]["content"]["title"] = "Espace Propriétaire Michelin Truckfly"

# 2. Conseil du mois (fond bleu)
s = it(6)
s[1]["content"] = f'<h2 class="default-heading2"><span style="color:rgb(255, 255, 255);font-size:24px">Ouvert pendant les fêtes' + NB + '? Faites-le savoir</span></h2>'
W = lambda t: f'<p><span {WH}>{t}</span></p>'
s[2]["content"] = (f'<p class="default"><span {WH}>Si vous restez ouvert pendant les fêtes, c’est un <strong>vrai atout</strong>" + NB + ": les routiers qui cherchent un repas chaud ou une douche le 24 ou le 31 décembre viendront chez vous.</span></p>'.replace('" + NB + "', NB)
    + '<p class="default"><br></p>' + f'<p class="default"><span {WH}><strong>Quelques réflexes' + NB + ':</strong></span></p><p class="default"><br></p>'
    + W("<strong>Vos horaires spéciaux" + NB + ":" + NB + "</strong>indiquez-les pour les 24, 25 et 31 décembre et le 1er janvier") + BR
    + W("<strong>Vos services ouverts" + NB + ":" + NB + "</strong>restaurant, douches, boutique, parking") + BR
    + W("<strong>Répondez aux avis récents" + NB + ":" + NB + "</strong>les routiers les lisent pour savoir ce qui est ouvert"))
btn(s[3], "Je mets à jour mes horaires", LOGIN)

# 3. Nouveau : les j'aime (section blanche, ex « Saison »)
s = it(7)
s[0]["content"] = f'<p><span {WH}><strong>Nouveau</strong></span></p>'
s[1]["content"] = f'<h2 class="default-heading2"><span {BL}>Les routiers peuvent maintenant liker les avis</span></h2>'
s[2]["content"] = (f'<p class="default"><span {BLK}>Sur Michelin Truckfly, les routiers peuvent désormais mettre un <strong>j’aime</strong> sur les avis et les photos de la communauté. Les contributions les plus aimées les aident à repérer <strong>les lieux les plus fiables.</strong></span></p>'
    + '<p class="default"><br></p>'
    + f'<p class="default"><span {BLK}><strong>Pour vous, c’est un nouveau signal de confiance' + NB + ':</strong> des avis détaillés et des photos récentes de votre établissement donnent envie aux routiers de s’arrêter chez vous.</span></p>'
    + '<p class="default"><br></p>'
    + f'<p class="default"><span {BLK}><strong>Votre levier' + NB + ':</strong> invitez vos clients routiers satisfaits à laisser un avis avec une photo.</span></p>')

# 4. Votre fiche des fêtes en 3 points
s = it(9)
s[1]["content"] = f'<h2 class="default-heading2"><span style="color:rgb(6, 24, 102);font-size:24px;">Votre fiche aux couleurs de Noël</span></h2>'
s[2]["content"] = (f'<p class="default"><span {BLK}>Fermé ou ouvert, c’est réglé. Il reste 2 idées pour donner envie aux routiers de s’arrêter chez vous pendant les fêtes.</span></p><p class="default"><br></p>'
    + P("<strong>Vos photos de Noël" + NB + ":" + NB + "</strong>vous décorez votre établissement" + NB + "? Montrez-le" + NB + "! Sapin, guirlandes, salle décorée" + NB + ": de belles photos donnent envie de faire une pause chez vous.") + BR
    + P("<strong>Votre menu des fêtes" + NB + ":" + NB + "</strong>vous proposez un repas spécial pour Noël ou le Nouvel An" + NB + "? Ajoutez-le à votre fiche.") + BR)

# 4 bis. Comment faire + visuel tuto (avant le bouton)
s = it(9)
s[2]["content"] += P("Les informations modifiables dépendent de votre offre" + NB + ": retrouvez le détail dans «" + NB + "👑 nos Packs" + NB + "» une fois connecté.")
img = copy.deepcopy(it(7)[3]); img["id"] = str(uuid.uuid4())
img["content"] = {"href": LOGIN, "src": PLACEHOLDER}
img["layout"]["default"].update({"canvas-height": "450px", "width": "100%"})
s.insert(3, img)

# Mot de fin
it(10)[1]["content"] = (BR + P("À l’approche des fêtes, nous vous souhaitons, à vous et à vos équipes, une très belle fin d’année" + NB + "!")
    + BR + f'<p><span {BLK}>Une question sur votre fiche ou sur la fermeture temporaire&nbsp;? <a href="{FAQ}" target="_blank" style="color: rgb(0, 146, 255); text-decoration: underline;">Notre FAQ propriétaires</a> est faite pour ça. Et si vous ne trouvez pas votre réponse, on est là&nbsp;: répondez simplement à cet e-mail.</span></p>'
    + BR + P("À très vite,") + P("<br><strong>La Team Michelin Truckfly</strong>"))

assert R[8]["title"] == "Yellow Button"
del R[8]   # bouton « J’accède à mon compte » : doublon des boutons de section
dump = yaml.dump(src, allow_unicode=True, sort_keys=False, width=10**9)
assert "MICHELIN" not in dump and "octobre" not in dump.lower() and "11 novembre" not in dump
ids = re.findall(r"^\s*-?\s*id: (\S+)$", dump, re.M); assert len(ids) == len(set(ids))
for f in ("template_final.yaml", "template_final.txt"): (D / f).write_text(dump)
print("OK", len(ids), "ids")
