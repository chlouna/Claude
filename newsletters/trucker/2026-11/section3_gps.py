"""Section 3 : le GPS poids lourds, 5 langues. Faits repris de la page GPS Michelin Truckfly
(86 %, profil du véhicule, alertes communautaires, 135 000 lieux), de l'écran Premium (sans pub, 14 jours d'essai)
et de la B2B de novembre (alerte péage)."""
F = "font-family:Arial,Helvetica,sans-serif;"
NB = "&nbsp;"
S3 = {
 "fr": dict(
  title="3. Les fêtes en GPS poids lourds",
  hook="Le savais-tu" + NB + "?",
  stat="<strong>86" + NB + "% des conducteurs poids lourds</strong> utilisent un GPS pour véhicules légers, qui peut les mettre en danger.",
  intro="Avec les routes chargées et les interdictions des fêtes, ce n’est pas le moment de se tromper de route. Le GPS Michelin Truckfly prend en compte toutes les contraintes de ton camion" + NB + ":",
  cards=[("Une navigation poids lourds", "Gabarit, poids, routes autorisées, restrictions ADR" + NB + ": ton itinéraire est adapté à ton camion."),
         ("Les alertes de la communauté", "Zones de contrôle, accidents, dangers" + NB + ": la plus grande communauté poids lourds d’Europe te prévient en temps réel. Et le trafic en direct t’aide à éviter les bouchons."),
         ("Nouveau" + NB + ": l’alerte péage", "Une alerte te prévient à l’approche d’un péage" + NB + ": tu as le temps de te placer sur la bonne voie et de sortir ton badge."),
         ("+135" + NB + "000 établissements poids lourds", "Restaurants, parkings gratuits ou sécurisés, stations-service" + NB + ": tu sais toujours où t’arrêter."),
         ("Pas de pub au lancement", "Tu ouvres l’appli, tu roules.")],
  end="<strong>Ne tombe plus dans le panneau" + NB + ": teste le GPS 14" + NB + "jours gratuitement.</strong> Et demain, surveille ta boîte mail" + NB + "!",
  src="Source" + NB + ": Michelin Truckfly", btn="J’essaie le GPS", lp="fr"),
 "en": dict(
  title="3. The festive season with a truck GPS",
  hook="Did you know?",
  stat="<strong>86% of HGV drivers</strong> use a GPS made for cars, which can put them in danger.",
  intro="With busy roads and holiday driving bans, this is no time to take a wrong turn. The Michelin Truckfly GPS takes every constraint of your truck into account:",
  cards=[("HGV navigation", "Size, weight, permitted roads, ADR restrictions: your route is adapted to your truck."),
         ("Community alerts", "Police checks, accidents, hazards: Europe’s largest HGV community warns you in real time. And live traffic helps you avoid jams."),
         ("New: the toll alert", "An alert warns you as you approach a toll: you have time to get into the right lane and get your tag ready."),
         ("135,000+ HGV-friendly places", "Restaurants, free or secure parking, fuel stations: you always know where to stop."),
         ("No ads at launch", "Open the app and drive.")],
  end="<strong>Never get caught out again: try the GPS free for 14 days.</strong> And tomorrow, keep an eye on your inbox!",
  src="Source: Michelin Truckfly", btn="Try the GPS", lp="en"),
 "es": dict(
  title="3. Las fiestas con un GPS para camiones",
  hook="¿Lo sabías?",
  stat="<strong>El 86% de los camioneros</strong> usa un GPS para turismos, que puede ponerlos en peligro.",
  intro="Con las carreteras cargadas y las restricciones de las fiestas, no es momento de equivocarse de ruta. El GPS Michelin Truckfly tiene en cuenta todas las limitaciones de tu camión:",
  cards=[("Navegación para camiones", "Gálibo, peso, carreteras permitidas, restricciones ADR: tu ruta se adapta a tu camión."),
         ("Avisos de la comunidad", "Controles, accidentes, peligros: la mayor comunidad de camioneros de Europa te avisa en tiempo real. Y el tráfico en directo te ayuda a evitar atascos."),
         ("Novedad: la alerta de peaje", "Una alerta te avisa cuando te acercas a un peaje: tienes tiempo de colocarte en el carril correcto y preparar tu telepeaje."),
         ("Más de 135.000 establecimientos para camiones", "Restaurantes, aparcamientos gratuitos o vigilados, gasolineras: siempre sabes dónde parar."),
         ("Sin publicidad al abrir la app", "Abres la app y a rodar.")],
  end="<strong>Que no te pillen desprevenido: prueba el GPS gratis durante 14 días.</strong> ¡Y mañana, atento a tu correo!",
  src="Fuente: Michelin Truckfly", btn="Pruebo el GPS", lp="es"),
 "it": dict(
  title="3. Le feste con un GPS per camion",
  hook="Lo sapevi?",
  stat="<strong>L’86% degli autisti di mezzi pesanti</strong> usa un GPS per auto, che può metterli in pericolo.",
  intro="Con strade trafficate e divieti delle feste, non è il momento di sbagliare strada. Il GPS Michelin Truckfly tiene conto di tutti i vincoli del tuo camion:",
  cards=[("Navigazione per mezzi pesanti", "Sagoma, peso, strade consentite, restrizioni ADR: il percorso è adatto al tuo camion."),
         ("Le segnalazioni della community", "Controlli, incidenti, pericoli: la più grande community di camionisti d’Europa ti avvisa in tempo reale. E il traffico in diretta ti aiuta a evitare le code."),
         ("Novità: l’avviso casello", "Un avviso ti segnala l’avvicinarsi di un casello: hai il tempo di metterti sulla corsia giusta e preparare il telepedaggio."),
         ("Oltre 135.000 strutture per mezzi pesanti", "Ristoranti, parcheggi gratuiti o sorvegliati, distributori: sai sempre dove fermarti."),
         ("Niente pubblicità all’avvio", "Apri l’app e parti.")],
  end="<strong>Non farti più cogliere di sorpresa: prova il GPS gratis per 14 giorni.</strong> E domani, tieni d’occhio la tua casella email!",
  src="Fonte: Michelin Truckfly", btn="Provo il GPS", lp="it"),
 "nl": dict(
  title="3. De feestdagen met een vrachtwagen-GPS",
  hook="Wist je dat?",
  stat="<strong>86% van de vrachtwagenchauffeurs</strong> gebruikt een GPS voor personenauto’s, en dat kan gevaarlijk zijn.",
  intro="Met drukke wegen en rijverboden tijdens de feestdagen is dit niet het moment om verkeerd te rijden. De Michelin Truckfly GPS houdt rekening met alle beperkingen van je truck:",
  cards=[("Navigatie voor vrachtwagens", "Afmetingen, gewicht, toegestane wegen, ADR-beperkingen: je route is aangepast aan je truck."),
         ("Meldingen van de community", "Controles, ongevallen, gevaren: de grootste vrachtwagencommunity van Europa waarschuwt je in realtime. En live verkeer helpt je files te vermijden."),
         ("Nieuw: de tolwaarschuwing", "Een melding waarschuwt je bij het naderen van een tolpoort: je hebt tijd om de juiste rijstrook te kiezen en je tolbadge klaar te houden."),
         ("Meer dan 135.000 locaties voor vrachtwagens", "Restaurants, gratis of beveiligde parkings, tankstations: je weet altijd waar je kunt stoppen."),
         ("Geen reclame bij het opstarten", "App open en rijden maar.")],
  end="<strong>Laat je niet meer verrassen: probeer de GPS 14 dagen gratis.</strong> En hou morgen je mailbox in de gaten!",
  src="Bron: Michelin Truckfly", btn="Ik probeer de GPS", lp="nl"),
}


def para(d):
    W = "rgb(255, 255, 255)"
    def p(t): return f'<p><span style="color: {W}; font-size: 16px; font-family: Arial, Helvetica, sans-serif;">{t}</span></p>'
    return "<p><br></p>" + p(f"<strong>{d['hook']}</strong>") + "<p><br></p>" + p(d["stat"]) + "<p><br></p>" + p(d["intro"])

def cards(d):
    rows = ""
    for t, x in d["cards"]:
        rows += f'''
  <tr><td style="padding:12px 16px 12px 14px;border-left:4px solid #FFFF18;background-color:#FFFFFF;border-radius:10px;">
    <p style="margin:0;{F}font-size:15px;line-height:1.35;font-weight:700;color:#061866;">{t}</p>
    <p style="margin:4px 0 0 0;{F}font-size:14px;line-height:1.45;color:#000000;">{x}</p>
  </td></tr>
  <tr><td style="height:8px;font-size:0;line-height:0;">&nbsp;</td></tr>'''
    return f'''<!-- GPS POIDS LOURDS : AVANTAGES -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;">{rows}
  <tr><td style="padding:6px 2px 0 2px;">
    <p style="margin:0 0 8px 0;{F}font-size:16px;line-height:1.5;color:#FFFFFF;">{d["end"]}</p>
    <p style="margin:0;{F}font-size:11px;color:#F9FAFC;">{d["src"]}</p>
  </td></tr>
</table>'''

def title(d):
    return f'<h2 class="default-heading2"><span style="color:rgb(255, 255, 255)">{d["title"]}</span></h2><p><br></p>'
