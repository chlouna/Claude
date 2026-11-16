"""Nouveautés Trucker, envoi lundi 30/11/2026 (mise à jour 6.5.0). Part du template de Louna.
FR, IT, ES (tutoiement). 3 nouveautés GPS + rappel dernier jour du Black Friday (sans prix)."""
import copy, re, uuid, yaml
from pathlib import Path
D = Path(__file__).parent
src = yaml.safe_load(open(D / "template_user.yaml"))
R = src["body"]["content"][0]["content"]
L = ["FR", "IT", "ES", "EN", "NL"]
EN_COND = '( "EN" in contact.LANG ) or ( ( contact.LANG != "FR" ) and ( contact.LANG != "ES" ) and ( contact.LANG != "NL" ) and ( contact.LANG != "IT" ) )'
COND = {"EN": EN_COND, "NL": '( "NL" in contact.LANG )'}
NB = "&nbsp;"
PH = "https://creative-assets.mailinblue.com/react-editor/placeholder-images/defaultproduct.png"
APP = "https://truckflyapp.onelink.me/2ysq/r4vkfd60"
LP = {k: f"https://lp.truckfly.com/{k.lower()}/gps-premium?utm_source=brevo&utm_medium=newsletter" for k in L}
def items(r): return r["content"][-1]["content"]
def new_ids(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "id": o[k] = str(uuid.uuid4())
            else: new_ids(v)
    elif isinstance(o, list):
        for v in o: new_ids(v)
def btn(b, label, href):
    h = f'<p><span style="color: rgb(0, 0, 0);"><strong>{label}</strong></span></p>'
    b["text"] = h; b["content"]["text"] = h; b["content"]["href"] = href
    for k in ("display", "showHide", "showOnDesktopMobile"): b["layout"]["default"].pop(k, None)
    b["layout"]["320px"].pop("display", None)
def P(t): return f'<p><span style="color: rgb(0, 0, 0);">{t}</span></p>'
BR = "<p><br></p>"

T = {
 "FR": dict(
   subject="Nouveau" + " " + ": vois ta destination avant d'y arriver 👀",
   head='Les <span style="color: rgb(6, 24, 102); background-color: rgb(255, 255, 26);">nouvelles fonctionnalités</span> qui arrivent sur ton appli' + NB + ':',
   intro=[ "Ce mois-ci, la mise à jour <strong>6.5.0</strong> de Michelin Truckfly arrive avec <strong>3 nouveautés dans le GPS</strong> pour rouler plus serein.", "Voici tout ce qui change."],
   gps="Les nouveautés du GPS Michelin Truckfly",
   feats=[("Vois ta destination avant d’y arriver" + NB + "!", ["Entrepôt, quai de livraison, parking" + NB + ": avec le nouveau <strong>bouton StreetView</strong>, tu vois à quoi ressemble ta destination avant d’arriver.", "<strong>Fini les tours pour trouver l’entrée" + NB + "!</strong>"]),
          ("Un recalcul d’itinéraire plus efficace", ["Une sortie ratée, un détour imprévu" + NB + "?", "<strong>Le GPS recalcule ton itinéraire plus efficacement</strong> en cas d’écart de route."]),
          ("Les alertes de la communauté, à ta façon", ["Contrôles, accidents, dangers" + NB + ": tu peux maintenant <strong>activer ou désactiver les alertes communautaires</strong> dans les paramètres."])],
   update="Je mets à jour l’appli",
   bf=("⏰ Dernier jour du Black Friday" + NB + "!", "Tu n’as pas encore le GPS Michelin Truckfly" + NB + "? C’est le moment" + NB + ": <strong>l’offre se termine ce soir à minuit.</strong>", "J’en profite")),
 "IT": dict(
   subject="Novità: guarda la tua destinazione prima di arrivarci 👀",
   head='Le <span style="background-color: rgb(255, 255, 26); color: rgb(6, 24, 102);">nuove funzionalità</span> disponibili sulla tua app:',
   intro=["Questo mese l’aggiornamento <strong>6.5.0</strong> di Michelin Truckfly porta <strong>3 novità nel GPS</strong> per guidare più tranquillo.", "Ecco tutto quello che cambia."],
   gps="Le novità del GPS Michelin Truckfly",
   feats=[("Guarda la tua destinazione prima di arrivarci!", ["Magazzino, banchina di carico, parcheggio: con il nuovo <strong>pulsante StreetView</strong> vedi com’è la tua destinazione prima di arrivare.", "<strong>Niente più giri a vuoto per trovare l’ingresso!</strong>"]),
          ("Un ricalcolo del percorso più efficace", ["Un’uscita mancata, una deviazione imprevista?", "<strong>Il GPS ricalcola il tuo percorso in modo più efficace</strong> quando esci dal tragitto."]),
          ("Gli avvisi della community, come vuoi tu", ["Controlli, incidenti, pericoli: ora puoi <strong>attivare o disattivare gli avvisi della community</strong> nelle impostazioni."])],
   update="Aggiorno l’app",
   bf=("⏰ Ultimo giorno del Black Friday!", "Non hai ancora il GPS Michelin Truckfly? È il momento: <strong>l’offerta termina stasera a mezzanotte.</strong>", "Ne approfitto")),
 "ES": dict(
   subject="Novedad: mira tu destino antes de llegar 👀",
   head='Las <span style="color: rgb(6, 24, 102); background-color: rgb(255, 255, 26);">nuevas funciones</span> que llegan a tu app:',
   intro=["Este mes, la actualización <strong>6.5.0</strong> de Michelin Truckfly llega con <strong>3 novedades en el GPS</strong> para que circules más tranquilo.", "Esto es todo lo que cambia."],
   gps="Las novedades del GPS Michelin Truckfly",
   feats=[("¡Mira tu destino antes de llegar!", ["Almacén, muelle de carga, parking: con el nuevo <strong>botón StreetView</strong> ves cómo es tu destino antes de llegar.", "<strong>¡Se acabaron las vueltas para encontrar la entrada!</strong>"]),
          ("Un recálculo de ruta más eficaz", ["¿Una salida perdida, un desvío imprevisto?", "<strong>El GPS recalcula tu ruta de forma más eficaz</strong> cuando te sales del trayecto."]),
          ("Los avisos de la comunidad, a tu manera", ["Controles, accidentes, peligros: ahora puedes <strong>activar o desactivar los avisos de la comunidad</strong> en los ajustes."])],
   update="Actualizo la app",
   bf=("⏰ ¡Último día del Black Friday!", "¿Aún no tienes el GPS Michelin Truckfly? Es el momento: <strong>la oferta termina esta noche a medianoche.</strong>", "Lo aprovecho")),
"EN": dict(
   subject="New: see your destination before you get there 👀",
   head='The <span style="color: rgb(6, 24, 102); background-color: rgb(255, 255, 26);">new features</span> coming to your app:',
   intro=["This month, Michelin Truckfly update <strong>6.5.0</strong> brings <strong>3 new GPS features</strong> to help you drive with peace of mind.", "Here’s everything that’s changing."],
   gps="What’s new in the Michelin Truckfly GPS",
   feats=[("See your destination before you get there!", ["Warehouse, loading bay, car park: with the new <strong>StreetView button</strong>, you can see what your destination looks like before you arrive.", "<strong>No more driving round in circles to find the entrance!</strong>"]),
          ("Smarter rerouting", ["Missed an exit, unexpected detour?", "<strong>The GPS recalculates your route more efficiently</strong> when you go off course."]),
          ("Community alerts, your way", ["Police checks, accidents, hazards: you can now <strong>turn community alerts on or off</strong> in the settings."])],
   update="Update my app",
   bf=("⏰ Last day of Black Friday!", "Don’t have the Michelin Truckfly GPS yet? Now’s the time: <strong>the offer ends tonight at midnight.</strong>", "Grab the offer")),
 "NL": dict(
   subject="Nieuw: bekijk je bestemming voordat je er bent 👀",
   head='De <span style="color: rgb(6, 24, 102); background-color: rgb(255, 255, 26);">nieuwe functies</span> in je app:',
   intro=["Deze maand brengt update <strong>6.5.0</strong> van Michelin Truckfly <strong>3 nieuwe functies in de GPS</strong>, zodat je met een gerust hart rijdt.", "Dit is alles wat er verandert."],
   gps="Nieuw in de Michelin Truckfly GPS",
   feats=[("Bekijk je bestemming voordat je er bent!", ["Magazijn, laadperron, parking: met de nieuwe <strong>StreetView-knop</strong> zie je hoe je bestemming eruitziet voordat je aankomt.", "<strong>Geen rondjes meer rijden om de ingang te vinden!</strong>"]),
          ("Slimmer je route herberekenen", ["Afslag gemist, onverwachte omleiding?", "<strong>De GPS berekent je route efficiënter opnieuw</strong> als je van je route afwijkt."]),
          ("Meldingen van de community, zoals jij wilt", ["Controles, ongevallen, gevaren: je kunt de <strong>meldingen van de community nu aan- of uitzetten</strong> in de instellingen."])],
   update="Ik update de app",
   bf=("⏰ Laatste dag van Black Friday!", "Heb je de Michelin Truckfly GPS nog niet? Dit is het moment: <strong>de actie eindigt vanavond om middernacht.</strong>", "Ik profiteer ervan")),
}

# Groupes de rangées par langue (FR, IT, ES dans le template) + clones EN / NL à partir du FR
BASES = {"banner": 2, "head": 5, "intro": 8, "gps": 21, "f0": 11, "f1": 14, "f2": 17, "bf": 24}
G = {}
for key, b in BASES.items():
    G[key] = {"FR": R[b], "IT": R[b + 1], "ES": R[b + 2]}
    for lg in ("EN", "NL"):
        r = copy.deepcopy(R[b]); new_ids(r); r["condition"] = COND[lg]; r["title"] = f"Bannière {lg}"
        G[key][lg] = r
# Bannière du haut EN / NL : elle reprend le visuel FR (à remplacer si besoin)

# Objet
src["subject"] = ('{% if "FR" in contact.LANG %}' + T["FR"]["subject"] + '{% elif "IT" in contact.LANG %}' + T["IT"]["subject"]
                  + '{% elif "ES" in contact.LANG %}' + T["ES"]["subject"] + '{% elif "NL" in contact.LANG %}' + T["NL"]["subject"]
                  + '{% else %}' + T["EN"]["subject"] + '{% endif %}')

# Marque : Michelin Truckfly (en-tête et pied de page), pied de page FR au tutoiement
for r in (R[1], R[27]):
    for x in items(r):
        if isinstance(x.get("content"), str):
            c = x["content"].replace("MICHELIN Truckfly", "Michelin Truckfly").replace("<strong>MICHELIN</strong> <strong", "<strong>Michelin</strong> <strong").replace("MICHELIN&nbsp;Truckfly", "Michelin&nbsp;Truckfly").replace("MICHELIN <strong", "Michelin <strong")
            c = c.replace("Consultez notre FAQ ou contactez-nous", "Consulte notre FAQ ou contacte-nous")
            c = c.replace("Vous avez reçu cet email car vous vous êtes inscrit à l&#39;application mobile <strong>Michelin Truckfly.</strong>",
                          "Tu reçois cet e-mail car tu es inscrit sur l&#39;appli mobile <strong>Michelin Truckfly</strong>.")
            x["content"] = c

# Titres et intro
for lg in L:
    items(G["head"][lg])[0]["content"] = f'<h2 class="default-heading2"><span style="color: rgb(6, 24, 102);">{T[lg]["head"]}</span></h2>'
    items(G["intro"][lg])[0]["content"] = P(T[lg]["intro"][0]) + BR + P(T[lg]["intro"][1])
    items(G["gps"][lg])[1]["content"] = f'<p><strong>{T[lg]["gps"]}</strong></p>'

# 3 nouveautés : on reprend les blocs « likes / photo / langue » (même mise en page)
for f in range(3):
    for lg in L:
        it = items(G[f"f{f}"][lg]); title, paras = T[lg]["feats"][f]
        it[0]["content"] = f'<h3 class="default-heading3"><span style="font-style:normal;text-decoration:none;font-weight:700;color:rgb(6, 24, 102);">{title}</span></h3>'
        it[1]["content"] = BR.join(P(x) for x in paras)
        it[2]["content"] = {"href": APP, "src": PH}
        if f < 2: it.pop(3)                       # un seul bouton « mise à jour », sous la 3e nouveauté
        else: btn(it[3], T[lg]["update"], APP)

# Rappel Black Friday : on reprend le bloc péage, fond bleu, sans image
for lg in L:
    r = G["bf"][lg]; r["layout"]["default"]["background-color"] = "#061866"
    it = items(r); t, body, b = T[lg]["bf"]
    it[0]["content"] = f'<h3 class="default-heading3" style="text-align: center;"><span style="color: rgb(255, 255, 26);">{t}</span></h3>'
    it[0]["layout"]["default"]["text-align"] = "center"
    it[1]["content"] = f'<p style="text-align: center;"><span style="color: rgb(255, 255, 255);">{body}</span></p>'
    it[1]["layout"]["default"]["text-align"] = "center"
    it.pop(2)
    btn(it[2], b, LP[lg])

# Nouvel ordre : intro → bandeau GPS → 3 nouveautés → séparateur → Black Friday
seq = [R[0], R[1]]
for key in ("banner", "head", "intro", "gps", "f0", "f1", "f2"): seq += [G[key][lg] for lg in L]
seq += [R[20]] + [G["bf"][lg] for lg in L] + [R[27]]
src["body"]["content"][0]["content"] = seq

dump = yaml.dump(src, allow_unicode=True, sort_keys=False, width=10**9)
assert "MICHELIN" not in dump and "vuestros" not in dump and "péage" not in dump.lower()
ids = re.findall(r"^\s*-?\s*id: (\S+)$", dump, re.M); assert len(ids) == len(set(ids))
for fn in ("template_final.yaml", "template_final.txt"): (D / fn).write_text(dump)
print("OK", len(ids), "ids")
