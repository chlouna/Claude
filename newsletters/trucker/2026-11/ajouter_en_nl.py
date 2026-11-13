"""Newsletter Trucker novembre 2026 (envoi jeudi 26/11).
Ajoute EN (UK) et NL, l'encart teasing Black Friday, met les dates à jour."""
from pathlib import Path
import copy, uuid, yaml, sys
sys.path.insert(0, str(Path(__file__).parent))

D = Path(__file__).parent
src = yaml.safe_load(open(D / "template_user.yaml"))
NB = " "
EN_COND = '( "EN" in contact.LANG ) or ( ( contact.LANG != "FR" ) and ( contact.LANG != "ES" ) and ( contact.LANG != "NL" ) and ( contact.LANG != "IT" ) )'
NL_COND = '( "NL" in contact.LANG )'

def walk(o, f):
    if isinstance(o, dict):
        return {k: walk(v, f) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v, f) for v in o]
    return f(o) if isinstance(o, str) else o

def new_ids(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "id": o[k] = str(uuid.uuid4())
            else: new_ids(v)
    elif isinstance(o, list):
        for v in o: new_ids(v)

def repl(s, a, b):
    assert a in s, f"introuvable : {a[:70]}"
    return s.replace(a, b)

rows = src["body"]["content"][0]["content"]
byid = {r["id"]: r for r in rows}
def items(row): return row["content"][0]["content"]

# ---------- Objet ----------
src["subject"] = (
    '{% if "FR" in contact.LANG %}Demain, c\'est Black Friday' + NB + '! Et tes chaînes' + NB + '?'
    '{% elif "ES" in contact.LANG %}¡Mañana es Black Friday! ¿Y tus cadenas?'
    '{% elif "IT" in contact.LANG %}Domani è Black Friday! E le tue catene?'
    '{% elif "NL" in contact.LANG %}Morgen is het Black Friday! En je kettingen?'
    '{% else %}Black Friday tomorrow! Are your chains ready?{% endif %}')

# ---------- Dates : envoi le 26/11, la Loi Montagne est déjà en vigueur ----------
fr_intro, it_intro, es_intro = (items(byid[i])[0] for i in ("9c9a2317-e900-419e-883d-e6f89b5951dd", "dcd388ed-e65b-483f-b936-5579dad62fa0", "3441d09a-f2db-4ff7-b0ac-e0aba1686f27"))
fr_intro["content"] = repl(fr_intro["content"], "ce qui devient obligatoire dès le 1er novembre", "ce qui est obligatoire en montagne depuis le 1er novembre")
fr_intro["content"] = repl(fr_intro["content"], "Avec novembre, l’hiver s’installe", "Avec novembre, l’hiver s’est installé")
fr_intro["content"] += '<p><br></p><p><span style="color: rgb(0, 0, 0);"><strong>Et ne rate pas notre offre Black Friday&nbsp;: elle commence demain&nbsp;!</strong></span></p>'
it_intro["content"] = repl(it_intro["content"], "cosa diventa obbligatorio in Francia dal 1° novembre", "cosa è obbligatorio in Francia dal 1° novembre")
it_intro["content"] += '<p><br></p><p><span style="color: rgb(0, 0, 0);"><strong>E non perderti la nostra offerta Black Friday: inizia domani!</strong></span></p>'
es_intro["content"] = repl(es_intro["content"], "qué pasa a ser obligatorio en Francia a partir del 1 de noviembre", "qué es obligatorio en Francia desde el 1 de noviembre")
es_intro["content"] += '<p><br></p><p><span style="color: rgb(0, 0, 0);"><strong>¡Y no te pierdas nuestra oferta Black Friday: empieza mañana!</strong></span></p>'

p = items(byid["eed65fa8-3d6a-4acf-8c18-d254c651c937"])[1]
p["content"] = repl(p["content"], "Dès ce <strong>dimanche 1er novembre et jusqu’au 31 mars</strong>", "<strong>Depuis le 1er novembre et jusqu’au 31 mars</strong>")
p = items(byid["7c207538-1c0a-4562-9c86-02d754b6f812"])[1]
p["content"] = repl(p["content"], "Da <strong>domenica 1° novembre fino al 31 marzo</strong>", "<strong>Dal 1° novembre e fino al 31 marzo</strong>")
p = items(byid["6dcd0518-5bdc-4943-b8d2-d37ba34c3a39"])[1]
p["content"] = repl(p["content"], "Desde el <strong>domingo 1 de noviembre hasta el 31 de marzo</strong>", "<strong>Desde el 1 de noviembre y hasta el 31 de marzo</strong>")

# ---------- Textes EN / NL ----------
def P(t, color="rgb(0, 0, 0)"): return f'<p><span style="color: {color};">{t}</span></p>'
BR = "<p><br></p>"
W = "rgb(249, 250, 252)"
def PD(t): return f'<p class="default"><span style="color: {W};">{t}</span></p>'
def LI(t, c=W): return f'<li style="color: {c};">{t}</li>'
def UL(*l): return '<ul dir="ltr">' + "".join(l) + "</ul>"
def H2(t, c="rgb(255, 255, 255)"): return f'<p><br></p><h2 class="default-heading2"><span style="color: {c};">{t}</span></h2><p><br></p>'
def H2B(t): return f'<h2 class="default-heading2"><span style="vertical-align:baseline;font-size:32px;color:rgb(0, 0, 0);">{t}</span></h2>'
def BTN(t): return f'<p><strong><span style="color: rgb(0, 0, 0);">{t}</span></strong></p>'
WH = 'style="color: rgb(255, 255, 255); font-size: 16px; font-family: Arial, Helvetica, sans-serif;"'
def TOP(a, b): 
    st = 'style="font-family:arial, helvetica, sans-serif;font-size:32px;margin:0px;text-align:left;word-break:break-word;"'
    return (f'<h2 class="default-heading2" {st}><span style="font-family: Arial, Helvetica, sans-serif; color: rgb(0, 0, 0);">{a}</span></h2>'
            f'<h2 class="default-heading2" {st}><span style="font-family: Arial, Helvetica, sans-serif; color: rgb(0, 0, 0);">{b}</span></h2>')

T = {
 "EN": dict(
  intro=P("Every day, thousands of drivers <strong>drive, share and bring the Michelin Truckfly community to life.</strong>") + BR +
        P("With November, winter has settled on the road: new rules in the mountains, slippery roads, conditions that change fast… All good reasons to <strong>plan your trips well and share the right info.</strong>") + BR +
        P("This month, find out <strong>what has been mandatory in France since 1 November and how to help other drivers face winter hazards. Not forgetting October’s top contributor… and our tips to take their place!</strong>") + BR +
        P("<strong>And don’t miss our Black Friday offer: it starts tomorrow!</strong>"),
  s1t=H2("1. Chains, winter tyres: are you compliant?"),
  s1p=PD("<strong>Did you know?</strong>") + '<p class="default"><br></p>' +
      PD("Driving in France? <strong>Since 1 November and until 31 March</strong>, the <strong>Loi Montagne</strong> (the French mountain law) applies in some mountain areas of France. They are marked by a sign at the entrance to the zone.") + '<p class="default"><br></p>' +
      PD("And HGVs are concerned:") + '<p class="default"><br></p>' +
      UL(LI("<strong>HGV with trailer or semi-trailer</strong>: chains mandatory on board to fit <strong>at least two drive wheels</strong>, even if you run on winter tyres."),
         LI("<strong>HGV without trailer</strong>: your choice, <strong>chains</strong> or <strong>winter tyres</strong>.")) + BR +
      PD("<strong>Watch your tyres:</strong> only tyres with the <strong>3PMSF symbol</strong> (the three-peak mountain with a snowflake) count as winter equipment. Other “snow” tyres are not enough on their own: you also need chains.") + '<p class="default"><br></p>' +
      PD("<strong>Foreign trucks are concerned too!</strong> Without equipment, the police can refuse you access to the zone and your insurer can reduce or refuse compensation in the event of an accident.") + '<p class="default"><br></p>' +
      PD("<strong>Your checklist before you set off:</strong>") +
      UL(LI("<strong>Check your tyres</strong>: is the 3PMSF symbol there?"),
         LI("<strong>Check your chains</strong>: they are in the truck, in good condition, and you know how to fit them.")),
  s1href="https://www.connexionfrance.com/practical/where-in-france-will-snow-tyres-be-mandatory-under-new-november-law/415068",
  s1b=BTN("Plan my trip"),
  s2t=H2B("2. Slippery road, fog, accident: warn the others!"),
  s2p='<p class="default"><br></p>' + P("<strong>Thick fog, slippery road, accident, traffic jam…</strong> On the road, info shared at the right moment can save another driver a lot of trouble.") + BR +
      P("On Michelin Truckfly, you can <strong>report an alert in a few seconds</strong>, straight from the map. It then shows up for the whole community driving in the area.") + BR +
      P("<strong>And the other way round</strong>, check the alerts on your route before you set off: you anticipate hazards and avoid nasty surprises.") + BR +
      UL(LI("<strong>To report</strong>: open the app → tap the alert button → choose the type of hazard → sent!", "rgb(0, 0, 0)"),
         LI("<strong>To anticipate</strong>: start your route → check the alerts reported along it → adjust your trip if needed", "rgb(0, 0, 0)")) + BR,
  s2b=BTN("Report an alert"),
  s3t=H2("3. Become the top contributor of the month").replace("<p><br></p><h2", "<h2", 1),
  s3p=f'<p><br></p><p><span {WH}>On the road, we trust those who share the right info. <strong>A driver with lots of contribution points is a reliable driver</strong>: when they report a hazard or rate a stop, the community knows it can count on them.</span></p><p><br></p><p><span {WH}>And the rule is simple: <strong>every action is worth 1 point.</strong> A coffee break is enough to earn several!</span></p>',
  s3b=BTN("Earn points"),
  topt=TOP("The top contributors", "of October!"), topb=BTN("My turn!"),
  mot='<h2 class="default-heading2"><span style="color: rgb(0, 0, 0);">A word from the road</span></h2>' + BR +
      P("A big thank you to the whole Michelin Truckfly community for your loyalty and your contributions every day.") + BR +
      P("See you very soon for <strong>more news, tips and useful info for your trips.</strong>") + BR +
      P("<strong>Until then, take care of yourself and drive safe!</strong>"),
  phone=[("(ES)", "(EN)"), ("CLASIFICACIÓN DEL MES", "MONTHLY RANKING"), ("1 acción = 1 punto", "1 action = 1 point"),
         ("Cuanto más contribuyes, más confía en ti la comunidad.", "The more you contribute, the more the community trusts you."),
         ("Añadir una foto", "Add a photo"), ("Parking, entrada, duchas…", "Parking, entrance, showers…"),
         ("Dejar una reseña", "Leave a review"), ("Valora o comenta una parada", "Rate or comment on a stop"),
         ("Dar like a una foto o actividad", "Like a photo or activity"), ("Anima a otros camioneros", "Encourage other drivers"),
         ("Actualizar un lugar", "Update a place"), ("Horarios, servicios, acceso", "Opening hours, services, access"),
         ("Añadir un lugar", "Add a place"), ("Una parada que aún no está en la app", "A stop not yet in the app"),
         ("Enviar un aviso", "Send an alert"), ("Nieve, accidente, peligro…", "Snow, accident, danger…"),
         ("El mejor colaborador del mes</strong><br>¡aparece en la próxima newsletter!", "The top contributor of the month</strong><br>features in the next newsletter!"),
         ("Cuantos más puntos tienes, más cuenta tu palabra.", "The more points you have, the more your word counts."),
         ("¿Listo para subir en la clasificación?", "Ready to climb the ranking?")]),
 "NL": dict(
  intro=P("Elke dag zijn duizenden chauffeurs <strong>onderweg, delen ze info en houden ze de Michelin Truckfly community levend.</strong>") + BR +
        P("Met november heeft de winter zijn intrede gedaan op de weg: nieuwe regels in de bergen, gladde wegen, snel wisselende omstandigheden… Genoeg redenen om <strong>je ritten goed voor te bereiden en de juiste info te delen.</strong>") + BR +
        P("Deze maand ontdek je <strong>wat er sinds 1 november verplicht is in Frankrijk en hoe je andere chauffeurs helpt bij wintergevaren. En natuurlijk de topbijdrager van oktober… en onze tips om zijn plek in te nemen!</strong>") + BR +
        P("<strong>En mis onze Black Friday-actie niet: morgen gaat hij van start!</strong>"),
  s1t=H2("1. Kettingen, winterbanden: ben jij in orde?"),
  s1p=PD("<strong>Wist je dat?</strong>") + '<p class="default"><br></p>' +
      PD("Rij je in Frankrijk? <strong>Sinds 1 november en tot 31 maart</strong> geldt de <strong>Loi Montagne</strong> (de Franse bergwet) in bepaalde berggemeenten in Frankrijk. Ze worden aangegeven met een bord bij het begin van de zone.") + '<p class="default"><br></p>' +
      PD("En vrachtwagens vallen er ook onder:") + '<p class="default"><br></p>' +
      UL(LI("<strong>Vrachtwagen met aanhanger of oplegger</strong>: sneeuwkettingen verplicht aan boord om <strong>minstens twee aangedreven wielen</strong> uit te rusten, ook als je op winterbanden rijdt."),
         LI("<strong>Vrachtwagen zonder aanhanger</strong>: naar keuze <strong>sneeuwkettingen</strong> of <strong>winterbanden</strong>.")) + BR +
      PD("<strong>Let op je banden:</strong> alleen banden met het <strong>3PMSF-symbool</strong> (de berg met drie toppen en een sneeuwvlok) tellen als winteruitrusting. Andere ‘sneeuwbanden’ zijn alleen niet genoeg: je hebt ook kettingen nodig.") + '<p class="default"><br></p>' +
      PD("<strong>Ook buitenlandse vrachtwagens vallen eronder!</strong> Zonder uitrusting kan de politie je de toegang tot de zone weigeren en kan je verzekeraar de schadevergoeding verlagen of weigeren bij een ongeval.") + '<p class="default"><br></p>' +
      PD("<strong>Jouw checklist voor vertrek:</strong>") +
      UL(LI("<strong>Controleer je banden</strong>: staat het 3PMSF-symbool erop?"),
         LI("<strong>Controleer je kettingen</strong>: ze liggen in de truck, zijn in goede staat en je weet hoe je ze monteert.")),
  s1href="https://www.france.fr/nl/artikel/winterbanden/",
  s1b=BTN("Ik plan mijn rit"),
  s2t=H2B("2. Gladde weg, mist, ongeval: waarschuw de anderen!"),
  s2p='<p class="default"><br></p>' + P("<strong>Dichte mist, gladde weg, ongeval, file…</strong> Onderweg kan info die op het juiste moment wordt gedeeld een andere chauffeur veel ellende besparen.") + BR +
      P("Op Michelin Truckfly kun je <strong>in een paar seconden een melding doen</strong>, rechtstreeks vanaf de kaart. Die verschijnt dan voor de hele community die in de buurt rijdt.") + BR +
      P("<strong>En andersom</strong>: bekijk voor vertrek de meldingen op je route. Zo zie je gevaren aankomen en voorkom je vervelende verrassingen.") + BR +
      UL(LI("<strong>Melden</strong>: open de app → tik op de meldknop → kies het type gevaar → verstuurd!", "rgb(0, 0, 0)"),
         LI("<strong>Vooruitkijken</strong>: start je route → bekijk de meldingen langs je route → pas je rit aan als het nodig is", "rgb(0, 0, 0)")) + BR,
  s2b=BTN("Ik doe een melding"),
  s3t=H2("3. Word de topbijdrager van de maand").replace("<p><br></p><h2", "<h2", 1),
  s3p=f'<p><br></p><p><span {WH}>Onderweg vertrouwen we op wie de juiste info deelt. <strong>Een chauffeur met veel bijdragepunten is een betrouwbare chauffeur</strong>: als hij een gevaar meldt of een stop beoordeelt, weet de community dat ze op hem kan rekenen.</span></p><p><br></p><p><span {WH}>En de regel is simpel: <strong>elke actie is 1 punt waard.</strong> Met één koffiepauze verdien je er al een paar!</span></p>',
  s3b=BTN("Ik verdien punten"),
  topt=TOP("De topbijdragers", "van oktober!"), topb=BTN("Mijn beurt!"),
  mot='<h2 class="default-heading2"><span style="color: rgb(0, 0, 0);">Een woord van de weg</span></h2>' + BR +
      P("Een dikke dank je wel aan de hele Michelin Truckfly community voor je trouw en je bijdragen, elke dag weer.") + BR +
      P("We zien je heel snel terug met <strong>nieuwe updates, tips en handige info voor je ritten.</strong>") + BR +
      P("<strong>Tot dan: pas goed op jezelf en goede reis!</strong>"),
  phone=[("(ES)", "(NL)"), ("CLASIFICACIÓN DEL MES", "RANGLIJST VAN DE MAAND"), ("1 acción = 1 punto", "1 actie = 1 punt"),
         ("Cuanto más contribuyes, más confía en ti la comunidad.", "Hoe meer je bijdraagt, hoe meer de community je vertrouwt."),
         ("Añadir una foto", "Een foto toevoegen"), ("Parking, entrada, duchas…", "Parking, ingang, douches…"),
         ("Dejar una reseña", "Een review achterlaten"), ("Valora o comenta una parada", "Geef een stop een score of reactie"),
         ("Dar like a una foto o actividad", "Een foto of activiteit liken"), ("Anima a otros camioneros", "Moedig andere chauffeurs aan"),
         ("Actualizar un lugar", "Een locatie bijwerken"), ("Horarios, servicios, acceso", "Openingstijden, diensten, toegang"),
         ("Añadir un lugar", "Een locatie toevoegen"), ("Una parada que aún no está en la app", "Een stop die nog niet in de app staat"),
         ("Enviar un aviso", "Een melding sturen"), ("Nieve, accidente, peligro…", "Sneeuw, ongeval, gevaar…"),
         ("El mejor colaborador del mes</strong><br>¡aparece en la próxima newsletter!", "De topbijdrager van de maand</strong><br>staat in de volgende nieuwsbrief!"),
         ("Cuantos más puntos tienes, más cuenta tu palabra.", "Hoe meer punten je hebt, hoe meer je woord telt."),
         ("¿Listo para subir en la clasificación?", "Klaar om te stijgen in de ranglijst?")]),
}

def clone(es_id, lang, fill):
    r = copy.deepcopy(byid[es_id]); new_ids(r)
    r["condition"] = EN_COND if lang == "EN" else NL_COND
    r["title"] = f"Bannière {lang}"
    fill(items(r), T[lang]); return r

def set_btn(b, html): b["text"] = html; b["content"]["text"] = html

def f_intro(it, t): it[0]["content"] = t["intro"]
def f_s1(it, t):
    it[0]["content"] = t["s1t"]; it[1]["content"] = t["s1p"]
    it[2]["content"]["href"] = t["s1href"]; set_btn(it[3], t["s1b"])
def f_s2(it, t): it[0]["content"] = t["s2t"]; it[1]["content"] = t["s2p"]; set_btn(it[3], t["s2b"])
def f_s3(it, t):
    it[0]["content"] = t["s3t"]; it[1]["content"] = t["s3p"]
    h = it[2]["content"]
    for a, b in t["phone"]: h = repl(h, a, b)
    it[2]["content"] = h; set_btn(it[3], t["s3b"])
def f_top(it, t): it[0]["content"] = t["topt"]; set_btn(it[2], t["topb"])
def f_mot(it, t): it[0]["content"] = t["mot"]

SECTIONS = [("3441d09a-f2db-4ff7-b0ac-e0aba1686f27", f_intro), ("6dcd0518-5bdc-4943-b8d2-d37ba34c3a39", f_s1),
            ("8390fc92-e8ed-4167-8697-4f69704069fb", f_s2), ("4ff1c1ac-67da-4e77-aeed-9859d1a48c68", f_s3),
            ("85668e93-b3f4-4683-b5e2-8a3e5fa9696c", f_top), ("52efe66d-805a-47c3-af88-e7908afce591", f_mot)]

# ---------- Encart teasing Black Friday ----------
BF = {
 "FR": ('( "FR" in contact.LANG )', "Black Friday · du 27 au 30 novembre", "C’est demain&nbsp;!", "Le Black Friday Michelin Truckfly commence demain. Surveille ta boîte mail&nbsp;: ton offre GPS arrive vendredi&nbsp;!", "Découvrir le GPS", "fr"),
 "EN": (EN_COND, "Black Friday · 27 to 30 November", "It starts tomorrow!", "Michelin Truckfly Black Friday starts tomorrow. Keep an eye on your inbox: your GPS offer lands on Friday!", "Discover the GPS", "en"),
 "ES": ('( "ES" in contact.LANG )', "Black Friday · del 27 al 30 de noviembre", "¡Empieza mañana!", "El Black Friday de Michelin Truckfly empieza mañana. Atento a tu correo: ¡tu oferta GPS llega el viernes!", "Descubre el GPS", "es"),
 "IT": ('( "IT" in contact.LANG )', "Black Friday · dal 27 al 30 novembre", "Inizia domani!", "Il Black Friday di Michelin Truckfly inizia domani. Tieni d’occhio la tua casella email: la tua offerta GPS arriva venerdì!", "Scopri il GPS", "it"),
 "NL": (NL_COND, "Black Friday · 27 t/m 30 november", "Morgen gaat het los!", "De Michelin Truckfly Black Friday begint morgen. Hou je mailbox in de gaten: vrijdag staat je GPS-aanbieding klaar!", "Ontdek de GPS", "nl"),
}
def bf_html(label, title, txt, btn, lp):
    return f'''<!-- ENCART TEASING BLACK FRIDAY -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFFFF;padding:8px 20px 8px 20px;">
  <tr><td align="center">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:520px;background-color:#0d1b5e;border-radius:16px;">
      <tr><td align="center" style="padding:28px 24px;font-family:Arial,Helvetica,sans-serif;">
        <p style="margin:0 0 10px 0;font-size:11px;font-weight:700;color:#FFFF18;letter-spacing:2px;text-transform:uppercase;">{label}</p>
        <p style="margin:0 0 12px 0;font-size:28px;line-height:1.2;font-weight:700;color:#FFFF18;">{title}</p>
        <p style="margin:0 0 20px 0;font-size:16px;line-height:1.5;color:#FFFFFF;">{txt}</p>
        <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
          <td align="center" bgcolor="#FFFF18" style="border-radius:10px;">
            <a href="https://lp.truckfly.com/{lp}/gps-premium?utm_source=brevo&amp;utm_medium=transactional_emails" target="_blank" style="display:inline-block;padding:14px 32px;font-family:Arial,Helvetica,sans-serif;font-size:17px;font-weight:700;color:#000000;text-decoration:none;border-radius:10px;">{btn}</a>
          </td></tr></table>
      </td></tr>
    </table>
  </td></tr>
</table>'''
bf_row = copy.deepcopy(byid["4b09a40c-ad49-4f91-b28f-2b37e69aa995"]); new_ids(bf_row)
bf_row["condition"] = ""; bf_row["title"] = "Teasing Black Friday multilangue"
bf_row["content"][0]["content"] = [
    {"condition": c, "id": str(uuid.uuid4()), "title": "HTML", "type": "raw-html",
     "layout": {"320px": {}, "default": {"padding-bottom": "10px", "padding-top": "10px", "width": "100%"}},
     "content": bf_html(l, t, x, b, lp)} for (c, l, t, x, b, lp) in BF.values()]

# Bloc FR section 1 sans condition dans le modèle : visible par toutes les langues
byid["eed65fa8-3d6a-4acf-8c18-d254c651c937"]["condition"] = '( "FR" in contact.LANG )'

for lg, (c, l, t, x, b, lp) in BF.items():
    (D.parent.parent / "blocs" / f"trucker-2026-11-teasing-bf-{lg.lower()}.html").write_text(bf_html(l, t, x, b, lp) + "\n")

# ---------- Insertion ----------
out = []
for r in rows:
    out.append(r)
    for es_id, fill in SECTIONS:
        if r["id"] == es_id:
            out += [clone(es_id, "EN", fill), clone(es_id, "NL", fill)]
            if fill is f_intro: out.append(bf_row)
src["body"]["content"][0]["content"] = out

# ---------- Section 2 : tuto code promo avec les 2 vraies captures ----------
IMG1 = "A_REMPLACER_URL_capture-premium-code-promo-corrigee.png"
IMG2 = "A_REMPLACER_URL_capture-activer-offre.jpg"
S2 = {
 "FR": ("2. Ton code promo activé en 30&nbsp;secondes", "<strong>Demain, c’est le Black Friday</strong> et ton offre arrive par mail. Pour en profiter, il te suffit d’entrer ton code dans l’appli&nbsp;:",
        ["Va dans ton profil, en haut à droite de la carte.", "Appuie sur «&nbsp;Truckfly Premium · aucun abonnement&nbsp;».", "Choisis «&nbsp;Utiliser un code promotionnel&nbsp;».", "Saisis ton code.", "Appuie sur «&nbsp;Activer&nbsp;»."],
        ("Choisis «&nbsp;Utiliser un code promotionnel&nbsp;»", "Saisis ton code puis «&nbsp;Activer&nbsp;»"), "J’ouvre l’appli"),
 "EN": ("2. Your promo code activated in 30 seconds", "<strong>Black Friday starts tomorrow</strong> and your offer is coming by email. To enjoy it, just enter your code in the app:",
        ["Go to your profile, top right of the map.", "Tap “Truckfly Premium · no subscription”.", "Choose “Use a promo code”.", "Enter your code.", "Tap “Redeem”."],
        ("Choose “Use a promo code”", "Enter your code, then “Redeem”"), "Open the app"),
 "ES": ("2. Tu código promocional activado en 30 segundos", "<strong>Mañana empieza el Black Friday</strong> y tu oferta llega por correo. Para aprovecharla, solo tienes que introducir tu código en la app:",
        ["Ve a tu perfil, arriba a la derecha del mapa.", "Pulsa en «Truckfly Premium · sin suscripción».", "Elige «Usar un código promocional».", "Introduce tu código.", "Pulsa en «Activar»."],
        ("Elige «Usar un código promocional»", "Introduce tu código y pulsa «Activar»"), "Abro la app"),
 "IT": ("2. Il tuo codice promo attivato in 30 secondi", "<strong>Domani inizia il Black Friday</strong> e la tua offerta arriva via email. Per approfittarne, basta inserire il codice nell’app:",
        ["Vai nel tuo profilo, in alto a destra della mappa.", "Tocca «Truckfly Premium · nessun abbonamento».", "Scegli «Usa un codice promozionale».", "Inserisci il codice.", "Tocca «Attiva»."],
        ("Scegli «Usa un codice promozionale»", "Inserisci il codice e tocca «Attiva»"), "Apro l’app"),
 "NL": ("2. Je promotiecode geactiveerd in 30 seconden", "<strong>Morgen begint Black Friday</strong> en je aanbieding komt per mail. Om ervan te profiteren, voer je gewoon je code in de app in:",
        ["Ga naar je profiel, rechtsboven op de kaart.", "Tik op ‘Truckfly Premium · geen abonnement’.", "Kies ‘Promotiecode gebruiken’.", "Voer je code in.", "Tik op ‘Activeren’."],
        ("Kies ‘Promotiecode gebruiken’", "Voer je code in en tik op ‘Activeren’"), "Ik open de app"),
}
def captures(cap1, cap2):
    def cell(src, cap, n):
        return (f'<td width="50%" align="center" valign="top" style="padding:0 6px;">'
                f'<img src="{src}" width="220" alt="{cap}" style="display:block;width:100%;max-width:220px;height:auto;border:0;margin:0 auto;">'
                f'<p style="margin:8px 0 0 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.4;font-weight:700;color:#061866;text-align:center;">{n}. {cap}</p></td>')
    return ('<!-- CAPTURES TUTO CODE PROMO -->\n<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:480px;margin:0 auto;"><tr>'
            + cell(IMG1, cap1, 1) + cell(IMG2, cap2, 2) + '</tr></table>')
def lang_of(c):
    return "EN" if c.startswith('( "EN"') else next(k for k in ("FR", "IT", "ES", "NL") if f'( "{k}"' in c)
n2 = 0
for r in src["body"]["content"][0]["content"]:
    it = r["content"][0]["content"]
    if not (isinstance(it[0].get("content"), str) and ">2. " in it[0]["content"]): continue
    lg = lang_of(r.get("condition", ""))
    t, a, steps, caps, btn = S2[lg]
    it[0]["content"] = H2B(t)
    ol = '<ol style="color: rgb(0, 0, 0);">' + "".join(f'<li style="color: rgb(0, 0, 0);">{x}</li>' for x in steps) + "</ol>"
    it[1]["content"] = '<p class="default"><br></p>' + P(a) + ol + BR
    it[2] = {"id": it[2]["id"], "title": "HTML", "type": "raw-html",
             "layout": {"320px": {}, "default": {"padding-bottom": "15px", "padding-top": "15px", "width": "100%"}}, "content": captures(*caps)}
    set_btn(it[3], BTN(btn)); it[3]["content"]["href"] = "https://truckflyapp.onelink.me/2ysq/r4vkfd60"
    n2 += 1
assert n2 == 5, n2

# ---------- Section 1 : interdictions des fêtes, intros et objet ----------
import section1_fetes as s1
INTRO = {
 "FR": ["Chaque jour, des milliers de conducteurs <strong>roulent, partagent et font vivre la communauté Michelin Truckfly.</strong>",
        "Décembre arrive, et avec lui les fêtes&nbsp;: jours fériés, routes chargées, livraisons de dernière minute… Autant de raisons de <strong>bien préparer tes trajets.</strong>",
        "Ce mois-ci, découvre <strong>les jours où tu ne pourras pas rouler pendant les fêtes, comment activer ton code promo en 30&nbsp;secondes, et le top contributeur d’octobre… avec nos astuces pour prendre sa place&nbsp;!</strong>",
        "<strong>Et ne rate pas notre offre Black Friday&nbsp;: elle commence demain&nbsp;!</strong>"],
 "EN": ["Every day, thousands of drivers <strong>drive, share and bring the Michelin Truckfly community to life.</strong>",
        "December is coming, and with it the festive season: public holidays, busy roads, last minute deliveries… All good reasons to <strong>plan your trips well.</strong>",
        "This month, find out <strong>the days you won’t be able to drive over the holidays, how to activate your promo code in 30 seconds, and October’s top contributor… with our tips to take their place!</strong>",
        "<strong>And don’t miss our Black Friday offer: it starts tomorrow!</strong>"],
 "ES": ["Cada día, miles de camioneros <strong>circulan, comparten y dan vida a la comunidad Michelin Truckfly.</strong>",
        "Llega diciembre y, con él, las fiestas: festivos, carreteras cargadas, entregas de última hora… Razones de sobra para <strong>preparar bien tus rutas.</strong>",
        "Este mes descubre <strong>los días en los que no podrás circular durante las fiestas, cómo activar tu código promocional en 30 segundos y al mejor colaborador de octubre… ¡con nuestros consejos para quitarle el puesto!</strong>",
        "<strong>¡Y no te pierdas nuestra oferta Black Friday: empieza mañana!</strong>"],
 "IT": ["Ogni giorno, migliaia di autisti <strong>viaggiano, condividono e fanno vivere la community Michelin Truckfly.</strong>",
        "Arriva dicembre e con lui le feste: giorni festivi, strade trafficate, consegne dell’ultimo minuto… Tanti buoni motivi per <strong>preparare bene i tuoi viaggi.</strong>",
        "Questo mese scopri <strong>i giorni in cui non potrai circolare durante le feste, come attivare il tuo codice promo in 30 secondi e il top contributore di ottobre… con i nostri consigli per prendere il suo posto!</strong>",
        "<strong>E non perderti la nostra offerta Black Friday: inizia domani!</strong>"],
 "NL": ["Elke dag zijn duizenden chauffeurs <strong>onderweg, delen ze info en houden ze de Michelin Truckfly community levend.</strong>",
        "December komt eraan, en daarmee de feestdagen: vrije dagen, drukke wegen, last minute leveringen… Genoeg redenen om <strong>je ritten goed voor te bereiden.</strong>",
        "Deze maand ontdek je <strong>op welke dagen je tijdens de feestdagen niet mag rijden, hoe je je promotiecode in 30 seconden activeert en de topbijdrager van oktober… met onze tips om zijn plek in te nemen!</strong>",
        "<strong>En mis onze Black Friday-actie niet: morgen gaat hij van start!</strong>"],
}
def lang_of(c):
    return "EN" if c.startswith('( "EN"') else next(k for k in ("FR", "IT", "ES", "NL") if f'( "{k}"' in c)
rws = src["body"]["content"][0]["content"]
bfi = next(i for i, r in enumerate(rws) if r.get("title") == "Teasing Black Friday multilangue")
for r in rws[bfi-5:bfi]:
    r["content"][0]["content"][0]["content"] = BR.join(P(x) for x in INTRO[lang_of(r["condition"])])
n1 = 0
for r in rws:
    it = r["content"][0]["content"]
    if not (isinstance(it[0].get("content"), str) and ">1." in it[0]["content"]): continue
    lg = lang_of(r["condition"]); d = s1.S1[lg]
    it[0]["content"] = s1.title(d); it[1]["content"] = s1.para(d)
    it[2] = {"id": it[2]["id"], "title": "HTML", "type": "raw-html",
             "layout": {"320px": {}, "default": {"padding-bottom": "10px", "padding-top": "5px", "width": "100%"}}, "content": s1.box(d)}
    set_btn(it[3], BTN(d["btn"])); it[3]["content"]["href"] = d["href"]
    (D.parent.parent / "blocs" / f"trucker-2026-11-fetes-interdictions-{lg.lower()}.html").write_text(s1.box(d) + "\n")
    n1 += 1
assert n1 == 5, n1
src["subject"] = (
    '{% if "FR" in contact.LANG %}Demain, c\'est Black Friday' + NB + '! Et tes trajets de Noël' + NB + '?'
    '{% elif "ES" in contact.LANG %}¡Mañana es Black Friday! ¿Y tus rutas de Navidad?'
    '{% elif "IT" in contact.LANG %}Domani è Black Friday! E i divieti di Natale?'
    '{% elif "NL" in contact.LANG %}Morgen is het Black Friday! En je kerstritten?'
    '{% else %}Black Friday tomorrow! Ready for the Christmas bans?{% endif %}')

# ---------- Marque, footer FR en « tu », footer NL ----------
src = walk(src, lambda s: s.replace("MICHELIN", "Michelin"))
rows = src["body"]["content"][0]["content"]
foot = rows[-1]["content"][0]["content"]
for it in foot:
    c = it.get("content")
    if not isinstance(c, str): continue
    c = c.replace("Consultez notre FAQ ou contactez-nous :&nbsp;", "Consulte notre FAQ ou contacte-nous&nbsp;:&nbsp;")
    c = c.replace("Une question ? Un problème ?", "Une question&nbsp;? Un problème&nbsp;?")
    c = c.replace("Vous avez reçu cet email car vous vous êtes inscrit à l&#39;application mobile <strong>Michelin Truckfly.</strong>",
                  "Tu reçois cet e-mail car tu es inscrit sur l&#39;appli mobile <strong>Michelin Truckfly</strong>.")
    c = c.replace("in de&nbsp;Michelin&nbsp;Truckfly.</span>", "in de&nbsp;Michelin&nbsp;Truckfly app.</span>")
    it["content"] = c

# ---------- Contrôles ----------
dump = yaml.dump(src, allow_unicode=True, sort_keys=False, width=10**9)
ids = []
def col(o):
    if isinstance(o, dict):
        if "id" in o: ids.append(o["id"])
        for v in o.values(): col(v)
    elif isinstance(o, list):
        for v in o: col(v)
col(src)
assert len(ids) == len(set(ids)), "ids en double"
assert "Loi Montagne" not in dump and "MICHELIN" not in dump and "Dès ce" not in dump and "domenica 1°" not in dump and "domingo 1 de" not in dump
assert "Vous avez reçu" not in dump and "Consultez" not in dump
(D / "template_final.yaml").write_text(dump)
(D / "template_final.txt").write_text(dump)
print("OK", len(rows), "sections,", len(ids), "ids")
