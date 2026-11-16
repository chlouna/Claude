"""v7 : part de la version Brevo de Louna (images gardées). Section 3 (arrêts) raccourcie,
bouton « Je choisis mon arrêt », lien sur le visuel IT, objet de novembre."""
import re, yaml
from pathlib import Path
D = Path(__file__).parent
src = yaml.safe_load(open(D / "template_user_v7.yaml"))
rows = src["body"]["content"][0]["content"]
def lang_of(c): return "EN" if c.startswith('( "EN"') else next(k for k in ("FR", "IT", "ES", "NL") if f'( "{k}"' in c)
def items(r): return r["content"][0]["content"]
def txt(h): return re.sub(r"<[^>]+>|&nbsp;", " ", h or "").strip()
def srcs(o): return re.findall(r"'src': '([^']+)'", str(o))
avant = srcs(src["body"])
NB = "&nbsp;"; W = "rgb(249, 250, 252)"
def p(t): return f'<p class="default"><span style="color: {W};">{t}</span></p>'
BR = '<p class="default"><br></p>'
S = {
 "FR": ("Routes chargées, restos fermés, parkings pleins" + NB + ": pendant les fêtes, trouver un bon arrêt prend du temps.",
        "Avant de t’arrêter, regarde les photos, les avis et les j’aime" + NB + ": les contributions les plus aimées t’indiquent les lieux les plus fiables. Sur place, les avis récents te disent ce qui est ouvert et s’il reste de la place.",
        "Et après ta pause, laisse ton avis" + NB + ": tu aides les collègues et tu grimpes dans le top contributeurs" + NB + "!",
        "À noter" + NB + ": en France, les poids lourds de plus de 7,5" + NB + "t ne roulent pas du jeudi 24 décembre 22" + NB + "h au vendredi 25 décembre 22" + NB + "h, ni du jeudi 31 décembre 22" + NB + "h au vendredi 1er janvier 22" + NB + "h.",
        "Je choisis mon arrêt"),
 "EN": ("Busy roads, closed restaurants, packed car parks: over the holidays, finding a good stop takes time.",
        "Before you stop, check the photos, reviews and likes: the most liked contributions point you to the most reliable places. On site, recent reviews tell you what’s open and if there’s still space.",
        "And after your break, leave a review: you help other drivers and climb the top contributors ranking!",
        "Heading to the continent? In France, trucks over 7.5 t can’t drive on 25 December and 1 January.",
        "Pick my truck stop"),
 "ES": ("Carreteras cargadas, restaurantes cerrados, aparcamientos llenos: en las fiestas, encontrar una buena parada lleva tiempo.",
        "Antes de parar, mira las fotos, las opiniones y los me gusta: las aportaciones con más me gusta te indican los lugares más fiables. Allí, las opiniones recientes te dicen qué está abierto y si queda sitio.",
        "Y después de tu pausa, deja tu opinión: ayudas a los compañeros y subes en el top de colaboradores.",
        "¿Vas a Francia? Allí los camiones de más de 7,5 t no pueden circular del jueves 24 de diciembre a las 22 h al viernes 25 a las 22 h, ni del jueves 31 de diciembre a las 22 h al viernes 1 de enero a las 22 h.",
        "Elijo mi parada"),
 "IT": ("Strade trafficate, ristoranti chiusi, parcheggi pieni: durante le feste, trovare una buona sosta richiede tempo.",
        "Prima di fermarti, guarda le foto, le recensioni e i Mi piace: i contributi più apprezzati ti indicano i posti più affidabili. Sul posto, le recensioni recenti ti dicono cosa è aperto e se c’è ancora posto.",
        "E dopo la pausa, lascia la tua recensione: aiuti i colleghi e sali nella classifica dei top contributori!",
        "Da ricordare: in Italia i mezzi oltre 7,5 t non possono circolare fuori dai centri abitati, dalle 9 alle 22, domenica 6, martedì 8, domenica 13, domenica 20, venerdì 25, sabato 26 e domenica 27 dicembre.",
        "Scelgo la mia sosta"),
 "NL": ("Drukke wegen, gesloten restaurants, volle parkings: tijdens de feestdagen kost een goede stop tijd.",
        "Bekijk voor je stopt de foto’s, reviews en likes: de meest gelikete bijdragen wijzen je de meest betrouwbare plekken aan. Ter plekke zie je in de nieuwste reviews wat er open is en of er nog plek is.",
        "En laat na je pauze een review achter: zo help je andere chauffeurs en klim je in de top van de bijdragers!",
        "Rij je naar Frankrijk? Daar mogen vrachtwagens boven 7,5 t niet rijden op 25 december en 1 januari.",
        "Ik kies mijn stop"),
}
APP = "https://truckflyapp.onelink.me/2ysq/r4vkfd60"
n = 0
for r in rows:
    if not r.get("condition"): continue
    it = items(r); t = it[0].get("content")
    if not (isinstance(t, str) and txt(t).startswith("3.")): continue
    lg = lang_of(r["condition"]); hook, mid, after, note, btn = S[lg]
    it[1]["content"] = p(f"<strong>{hook}</strong>") + BR + p(mid) + BR + p(after) + BR + f'<p class="default"><span style="color: {W}; font-size: 14px;">{note}</span></p>'
    img = it[2]; img["content"]["href"] = APP; img["layout"]["default"]["type"] = "absoluteLink"
    b = it[3]; h = f'<p><strong><span style="color: rgb(0, 0, 0);">{btn}</span></strong></p>'
    b["text"] = h; b["content"]["text"] = h; b["content"]["href"] = APP
    n += 1
assert n == 5, n
NBS = " "
src["subject"] = ('{% if "FR" in contact.LANG %}Demain, c\'est Black Friday' + NBS + '! Et tes trajets de Noël' + NBS + '?'
    '{% elif "ES" in contact.LANG %}¡Mañana es Black Friday! ¿Y tus rutas de Navidad?'
    '{% elif "IT" in contact.LANG %}Domani è Black Friday! E i tuoi viaggi di Natale?'
    '{% elif "NL" in contact.LANG %}Morgen is het Black Friday! En je kerstritten?'
    '{% else %}Black Friday tomorrow! Ready for your Christmas trips?{% endif %}')
assert srcs(src["body"]) == avant, "images modifiées"
dump = yaml.dump(src, allow_unicode=True, sort_keys=False, width=10**9)
ids = re.findall(r"^\s*-?\s*id: (\S+)$", dump, re.M)
assert len(ids) == len(set(ids)) and "MICHELIN" not in dump and "1&nbsp;point" not in dump and "1 punt" not in dump
for f in ("template_final_v7.yaml", "template_final_v7.txt"): (D / f).write_text(dump)
print("OK", len(ids), "ids,", len(avant), "images identiques")
