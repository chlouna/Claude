"""Section 1 v2 : recentrée chauffeur (où passer son arrêt pendant les fêtes), 5 langues.
Dates : Bison Futé (régime général), DM MIT 325/2025 (calendrier 2026). Appliquée sur template_final_v2."""
import re, yaml
from pathlib import Path
D = Path(__file__).parent
NB = "&nbsp;"
W = "rgb(249, 250, 252)"
S = {
 "FR": dict(title="1. Noël et Nouvel An" + NB + ": où tu vas passer ton arrêt" + NB + "?",
   hook="Le 25 décembre et le 1er janvier, c’est 24" + NB + "h à l’arrêt en France pour les plus de 7,5" + NB + "t. Autant choisir ton aire à l’avance" + NB + "!",
   fr=("France", "plus de 7,5" + NB + "t, tout le réseau", ["Du jeudi 24 décembre 22" + NB + "h au vendredi 25 décembre 22" + NB + "h", "Du jeudi 31 décembre 22" + NB + "h au vendredi 1er janvier 22" + NB + "h", "Et le week-end, comme d’habitude, du samedi 22" + NB + "h au dimanche 22" + NB + "h"]),
   it=("Italie", "plus de 7,5" + NB + "t, hors agglomérations, de 9" + NB + "h à 22" + NB + "h", ["Dimanches 6, 13, 20 et 27 décembre", "Mardi 8, vendredi 25 et samedi 26 décembre", "Du 25 au 27 décembre, ça fait 3 jours d’affilée"]),
   es=("Espagne", "", ["Pas d’interdiction générale" + NB + ": vérifie les restrictions locales avant de partir."]),
   order=("fr", "it", "es"),
   app="<strong>Le bon réflexe" + NB + ":</strong> sur Michelin Truckfly, repère dès maintenant les parkings avec douches et resto sur ta route, et lis les avis récents pour savoir ce qui est ouvert pendant les fêtes.",
   src="Sources" + NB + ": Bison Futé · Ministère italien des Transports", btn="Je trouve mon parking"),
 "EN": dict(title="1. Christmas and New Year: where will you spend your stop?",
   hook="On 25 December and 1 January, trucks over 7.5 t are stopped for 24 hours in France. Better pick your truck stop in advance!",
   fr=("France", "over 7.5 t, whole road network", ["From Thursday 24 December 10 pm to Friday 25 December 10 pm", "From Thursday 31 December 10 pm to Friday 1 January 10 pm", "And at the weekend, as usual, from Saturday 10 pm to Sunday 10 pm"]),
   it=("Italy", "over 7.5 t, outside built-up areas, 9 am to 10 pm", ["Sundays 6, 13, 20 and 27 December", "Tuesday 8, Friday 25 and Saturday 26 December", "From 25 to 27 December, that’s 3 days in a row"]),
   es=("Spain", "", ["No general ban: check local restrictions before you set off."]),
   order=("fr", "it", "es"),
   app="<strong>Good habit:</strong> on Michelin Truckfly, find truck stops with showers and a restaurant along your route now, and read recent reviews to see what’s open over the holidays.",
   src="Sources: Bison Futé · Italian Ministry of Transport", btn="Find my truck stop"),
 "ES": dict(title="1. Navidad y Año Nuevo: ¿dónde vas a pasar tu parada?",
   hook="El 25 de diciembre y el 1 de enero, los camiones de más de 7,5 t paran 24 horas en Francia. ¡Mejor elegir tu área con antelación!",
   fr=("Francia", "más de 7,5 t, toda la red", ["Del jueves 24 de diciembre a las 22 h al viernes 25 a las 22 h", "Del jueves 31 de diciembre a las 22 h al viernes 1 de enero a las 22 h", "Y el fin de semana, como siempre, del sábado a las 22 h al domingo a las 22 h"]),
   it=("Italia", "más de 7,5 t, fuera de poblado, de 9 h a 22 h", ["Domingos 6, 13, 20 y 27 de diciembre", "Martes 8, viernes 25 y sábado 26 de diciembre", "Del 25 al 27 de diciembre, son 3 días seguidos"]),
   es=("España", "", ["No hay prohibición general: revisa las restricciones locales antes de salir."]),
   order=("es", "fr", "it"),
   app="<strong>Buen reflejo:</strong> en Michelin Truckfly, localiza ya los aparcamientos con duchas y restaurante en tu ruta, y lee las opiniones recientes para saber qué está abierto durante las fiestas.",
   src="Fuentes: Bison Futé · Ministerio de Transportes italiano", btn="Busco mi aparcamiento"),
 "IT": dict(title="1. Natale e Capodanno: dove passerai la tua sosta?",
   hook="Il 25 dicembre e il 1° gennaio, in Francia i camion oltre 7,5 t restano fermi 24 ore. Meglio scegliere l’area di sosta in anticipo!",
   fr=("Francia", "oltre 7,5 t, su tutta la rete", ["Da giovedì 24 dicembre ore 22 a venerdì 25 ore 22", "Da giovedì 31 dicembre ore 22 a venerdì 1° gennaio ore 22", "E nel fine settimana, come sempre, dal sabato ore 22 alla domenica ore 22"]),
   it=("Italia", "oltre 7,5 t, fuori dai centri abitati, dalle 9 alle 22", ["Domeniche 6, 13, 20 e 27 dicembre", "Martedì 8, venerdì 25 e sabato 26 dicembre", "Dal 25 al 27 dicembre sono 3 giorni di fila"]),
   es=("Spagna", "", ["Nessun divieto generale: verifica le restrizioni locali prima di partire."]),
   order=("it", "fr", "es"),
   app="<strong>Il riflesso giusto:</strong> su Michelin Truckfly, individua fin da ora i parcheggi con docce e ristorante lungo il percorso, e leggi le recensioni recenti per sapere cosa è aperto durante le feste.",
   src="Fonti: Ministero delle Infrastrutture e dei Trasporti · Bison Futé", btn="Trovo il mio parcheggio"),
 "NL": dict(title="1. Kerst en Oud en Nieuw: waar sta je stil?",
   hook="Op 25 december en 1 januari staan vrachtwagens boven 7,5 t in Frankrijk 24 uur stil. Kies je parking dus op tijd!",
   fr=("Frankrijk", "boven 7,5 t, het hele wegennet", ["Van donderdag 24 december 22.00 uur tot vrijdag 25 december 22.00 uur", "Van donderdag 31 december 22.00 uur tot vrijdag 1 januari 22.00 uur", "En in het weekend, zoals altijd, van zaterdag 22.00 uur tot zondag 22.00 uur"]),
   it=("Italië", "boven 7,5 t, buiten de bebouwde kom, van 9.00 tot 22.00 uur", ["Zondag 6, 13, 20 en 27 december", "Dinsdag 8, vrijdag 25 en zaterdag 26 december", "Van 25 tot en met 27 december is dat 3 dagen achter elkaar"]),
   es=("Spanje", "", ["Geen algemeen verbod: check de lokale beperkingen voor vertrek."]),
   order=("fr", "it", "es"),
   app="<strong>Slim:</strong> zoek nu al op Michelin Truckfly de parkings met douches en restaurant langs je route, en lees de recente reviews om te zien wat er open is tijdens de feestdagen.",
   src="Bronnen: Bison Futé · Italiaans ministerie van Transport", btn="Ik zoek mijn parking"),
}
def p(t): return f'<p class="default"><span style="color: {W};">{t}</span></p>'
BR = '<p class="default"><br></p>'
def para(d):
    h = p(f"<strong>{d['hook']}</strong>") + BR
    for k in d["order"]:
        name, scope, lines = d[k]
        h += p(f"<strong>{name}</strong>" + (f" ({scope})" if scope else ""))
        h += '<ul dir="ltr">' + "".join(f'<li style="color: {W};">{l}</li>' for l in lines) + "</ul>" + BR
    h += p(d["app"]) + BR + f'<p class="default"><span style="color: {W}; font-size: 11px;">{d["src"]}</span></p>'
    return h

if __name__ == "__main__":
    src = yaml.safe_load(open(D / "template_final_v2.yaml"))
    rows = src["body"]["content"][0]["content"]
    def lang_of(c): return "EN" if c.startswith('( "EN"') else next(k for k in ("FR", "IT", "ES", "NL") if f'( "{k}"' in c)
    n = 0
    for r in rows:
        it = r["content"][0]["content"]
        t = it[0].get("content")
        if not (r.get("condition") and isinstance(t, str) and re.sub(r"<[^>]+>|&nbsp;", " ", t).strip().startswith("1.")): continue
        d = S[lang_of(r["condition"])]
        it[0]["content"] = f'<p><br></p><h2 class="default-heading2"><span style="color: rgb(255, 255, 255);">{d["title"]}</span></h2><p><br></p>'
        it[1]["content"] = para(d)
        it[2]["content"]["href"] = "https://truckflyapp.onelink.me/2ysq/r4vkfd60"
        b = it[3]; h = f'<p><strong><span style="color: rgb(0, 0, 0);">{d["btn"]}</span></strong></p>'
        b["text"] = h; b["content"]["text"] = h; b["content"]["href"] = "https://truckflyapp.onelink.me/2ysq/r4vkfd60"
        b["layout"]["default"]["width"] = "55%"
        (D / f"section1-{lang_of(r['condition']).lower()}.html").write_text(it[0]["content"] + it[1]["content"] + "\n")
        n += 1
    assert n == 5, n
    dump = yaml.dump(src, allow_unicode=True, sort_keys=False, width=10**9)
    for f in ("template_final_v2.yaml", "template_final_v2.txt"): (D / f).write_text(dump)
    print("OK", n)
