"""Section 1 : interdictions de circulation PL pendant les fêtes (décembre 2026), 5 langues.
Sources : Bison Futé (régime général), DM MIT 325/2025 (calendrier 2026), DGT (résolution 2026)."""
F = "font-family:Arial,Helvetica,sans-serif;"
NB = "&nbsp;"

S1 = {
 "FR": dict(
  title="1. Fêtes de fin d’année" + NB + ": les jours où tu ne roules pas",
  hook="Le savais-tu" + NB + "?",
  intro="En décembre, les jours fériés s’ajoutent aux week-ends. En France et en Italie, ça fait plus de jours où les camions de plus de 7,5" + NB + "t n’ont pas le droit de rouler. Le bon réflexe" + NB + ": <strong>planifier tes livraisons et tes pauses dès maintenant.</strong>",
  c=[("France", "plus de 7,5" + NB + "t, tout le réseau", ["Du jeudi 24 décembre 22" + NB + "h au vendredi 25 décembre 22" + NB + "h", "Du jeudi 31 décembre 22" + NB + "h au vendredi 1er janvier 22" + NB + "h", "Et chaque week-end, du samedi 22" + NB + "h au dimanche 22" + NB + "h"]),
     ("Italie", "plus de 7,5" + NB + "t, hors agglomérations, de 9" + NB + "h à 22" + NB + "h", ["Dimanches 6, 13, 20 et 27 décembre", "Mardi 8, vendredi 25 et samedi 26 décembre"]),
     ("Espagne", "", ["Pas d’interdiction générale, mais des restrictions sur certains tronçons. La Catalogne, le Pays basque et la Navarre ont leurs propres règles."])],
  tip="Des interdictions locales peuvent s’ajouter" + NB + ": vérifie avant de partir. Et sur Michelin Truckfly, repère à l’avance les parkings poids lourds sur ta route.",
  src="Sources" + NB + ": Bison Futé · Ministère italien des Transports · DGT",
  btn="Je prépare mon trajet", href="https://www.bison-fute.gouv.fr/regime-general,10852.html"),
 "EN": dict(
  title="1. Festive season: the days you can’t drive",
  hook="Did you know?",
  intro="In December, public holidays come on top of weekends. In France and Italy, that means more days when trucks over 7.5 t are not allowed on the road. Good habit: <strong>plan your deliveries and breaks now.</strong>",
  c=[("France", "over 7.5 t, whole road network", ["From Thursday 24 December 10 pm to Friday 25 December 10 pm", "From Thursday 31 December 10 pm to Friday 1 January 10 pm", "And every weekend, from Saturday 10 pm to Sunday 10 pm"]),
     ("Italy", "over 7.5 t, outside built-up areas, 9 am to 10 pm", ["Sundays 6, 13, 20 and 27 December", "Tuesday 8, Friday 25 and Saturday 26 December"]),
     ("Spain", "", ["No general ban, but restrictions on certain road sections. Catalonia, the Basque Country and Navarre have their own rules."])],
  tip="Local bans may be added: check before you set off. And on Michelin Truckfly, find HGV parking along your route in advance.",
  src="Sources: Bison Futé · Italian Ministry of Transport · DGT",
  btn="Plan my trip", href="https://www.bison-fute.gouv.fr/regime-general,10852,langen.html"),
 "ES": dict(
  title="1. Fiestas de fin de año: los días que no puedes circular",
  hook="¿Lo sabías?",
  intro="En diciembre, los festivos se suman a los fines de semana. En Francia e Italia, eso significa más días en los que los camiones de más de 7,5 t no pueden circular. Buen reflejo: <strong>planifica ya tus entregas y tus pausas.</strong>",
  c=[("España", "", ["No hay prohibición general, sino restricciones en tramos concretos. Cataluña, País Vasco y Navarra tienen sus propias normas."]),
     ("Francia", "más de 7,5 t, toda la red", ["Del jueves 24 de diciembre a las 22 h al viernes 25 a las 22 h", "Del jueves 31 de diciembre a las 22 h al viernes 1 de enero a las 22 h", "Y cada fin de semana, del sábado a las 22 h al domingo a las 22 h"]),
     ("Italia", "más de 7,5 t, fuera de poblado, de 9 h a 22 h", ["Domingos 6, 13, 20 y 27 de diciembre", "Martes 8, viernes 25 y sábado 26 de diciembre"])],
  tip="Pueden añadirse restricciones locales: compruébalo antes de salir. Y en Michelin Truckfly, localiza con antelación los aparcamientos para camiones en tu ruta.",
  src="Fuentes: Bison Futé · Ministerio de Transportes italiano · DGT",
  btn="Preparo mi ruta", href="https://www.dgt.es/comunicacion/notas-de-prensa/20260122-resolucion-medidas-especiales-trafico-2026"),
 "IT": dict(
  title="1. Feste di fine anno: i giorni in cui non puoi circolare",
  hook="Lo sapevi?",
  intro="A dicembre i giorni festivi si aggiungono ai fine settimana. In Francia e in Italia significa più giorni in cui i camion oltre 7,5 t non possono circolare. Il riflesso giusto: <strong>pianifica fin da ora consegne e pause.</strong>",
  c=[("Italia", "oltre 7,5 t, fuori dai centri abitati, dalle 9 alle 22", ["Domeniche 6, 13, 20 e 27 dicembre", "Martedì 8, venerdì 25 e sabato 26 dicembre"]),
     ("Francia", "oltre 7,5 t, su tutta la rete", ["Da giovedì 24 dicembre ore 22 a venerdì 25 ore 22", "Da giovedì 31 dicembre ore 22 a venerdì 1° gennaio ore 22", "E ogni fine settimana, dal sabato ore 22 alla domenica ore 22"]),
     ("Spagna", "", ["Nessun divieto generale, ma restrizioni su alcuni tratti. Catalogna, Paesi Baschi e Navarra hanno regole proprie."])],
  tip="Possono aggiungersi divieti locali: verifica prima di partire. E su Michelin Truckfly, individua in anticipo i parcheggi per camion lungo il percorso.",
  src="Fonti: Ministero delle Infrastrutture e dei Trasporti · Bison Futé · DGT",
  btn="Preparo il mio viaggio", href="https://mit.gov.it/node/21641"),
 "NL": dict(
  title="1. Feestdagen: de dagen dat je niet mag rijden",
  hook="Wist je dat?",
  intro="In december komen de feestdagen bovenop de weekends. In Frankrijk en Italië betekent dat meer dagen waarop vrachtwagens boven 7,5 t niet mogen rijden. Slim: <strong>plan je leveringen en pauzes nu al.</strong>",
  c=[("Frankrijk", "boven 7,5 t, het hele wegennet", ["Van donderdag 24 december 22.00 uur tot vrijdag 25 december 22.00 uur", "Van donderdag 31 december 22.00 uur tot vrijdag 1 januari 22.00 uur", "En elk weekend, van zaterdag 22.00 uur tot zondag 22.00 uur"]),
     ("Italië", "boven 7,5 t, buiten de bebouwde kom, van 9.00 tot 22.00 uur", ["Zondag 6, 13, 20 en 27 december", "Dinsdag 8, vrijdag 25 en zaterdag 26 december"]),
     ("Spanje", "", ["Geen algemeen verbod, wel beperkingen op bepaalde trajecten. Catalonië, Baskenland en Navarra hebben eigen regels."])],
  tip="Er kunnen lokale verboden bijkomen: check dit voor vertrek. En zoek op Michelin Truckfly vooraf de vrachtwagenparkings langs je route.",
  src="Bronnen: Bison Futé · Italiaans ministerie van Transport · DGT",
  btn="Ik plan mijn rit", href="https://www.bison-fute.gouv.fr/regime-general,10852,langen.html"),
}

def box(d):
    rows = ""
    for name, scope, lines in d["c"]:
        sc = f'<span style="font-weight:400;color:#4A4A4A;"> · {scope}</span>' if scope else ""
        li = "".join(f'<p style="margin:4px 0 0 0;{F}font-size:14px;line-height:1.45;color:#000000;">• {l}</p>' for l in lines)
        rows += f'''
      <tr><td style="padding:12px 16px 12px 14px;border-left:4px solid #FFFF18;background-color:#FFFFFF;border-radius:10px;">
        <p style="margin:0;{F}font-size:15px;line-height:1.35;font-weight:700;color:#061866;">{name}{sc}</p>{li}
      </td></tr>
      <tr><td style="height:8px;font-size:0;line-height:0;">&nbsp;</td></tr>'''
    return f'''<!-- RÉCAP INTERDICTIONS FÊTES -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;">{rows}
  <tr><td style="padding:4px 2px 0 2px;">
    <p style="margin:0 0 8px 0;{F}font-size:14px;line-height:1.5;color:#F9FAFC;">{d["tip"]}</p>
    <p style="margin:0;{F}font-size:11px;color:#F9FAFC;">{d["src"]}</p>
  </td></tr>
</table>'''

def para(d):
    W = "rgb(249, 250, 252)"
    return (f'<p class="default"><strong><span style="color: {W};">{d["hook"]}</span></strong></p><p class="default"><br></p>'
            f'<p class="default"><span style="color: {W};">{d["intro"]}</span></p><p class="default"><br></p>')

def title(d):
    return f'<p><br></p><h2 class="default-heading2"><span style="color: rgb(255, 255, 255);">{d["title"]}</span></h2><p><br></p>'
