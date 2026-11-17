"""Ajoute des explications pas à pas (StreetView, alertes, recalcul) sur la version Brevo de Louna, sans toucher aux images."""
import re, yaml
from pathlib import Path
D = Path(__file__).parent
src = yaml.safe_load(open(D / "template_user_v2.yaml"))
R = src["body"]["content"][0]["content"]
NB = "&nbsp;"
B = 'style="color: rgb(0, 0, 0);"'
def P(t): return f'<p><span {B}>{t}</span></p>'
def OL(xs): return '<ol>' + "".join(f'<li {B}>{x}</li>' for x in xs) + '</ol>'
BR = "<p><br></p>"
def lang_of(c): return "EN" if c.startswith('( "EN"') else re.search(r'"(\w\w)"', c).group(1)
def txt(h): return re.sub(r"<[^>]+>|&nbsp;", " ", h or "")
HOW = {"FR": "Comment faire" + NB + "?", "IT": "Come fare?", "ES": "¿Cómo se hace?", "EN": "How does it work?", "NL": "Hoe werkt het?"}
SV = {
 "FR": ("Entrepôt, quai de livraison, parking" + NB + ": avec le nouveau <strong>bouton StreetView</strong>, tu vois à quoi ressemble ta destination avant d’arriver.",
        ["Appuie sur le <strong>drapeau d’arrivée</strong> de ton itinéraire.", "Appuie sur <strong>«" + NB + "Voir en Street View" + NB + "»</strong>.", "<strong>Google Maps s’ouvre directement</strong> sur ta destination."],
        "Fini les tours pour trouver l’entrée" + NB + "!"),
 "IT": ("Magazzino, banchina di carico, parcheggio: con il nuovo <strong>pulsante StreetView</strong> vedi com’è la tua destinazione prima di arrivare.",
        ["Tocca la <strong>bandierina di arrivo</strong> del tuo percorso.", "Tocca <strong>«Vedi in Street View»</strong>.", "<strong>Google Maps si apre direttamente</strong> sulla tua destinazione."],
        "Niente più giri a vuoto per trovare l’ingresso!"),
 "ES": ("Almacén, muelle de carga, parking: con el nuevo <strong>botón StreetView</strong> ves cómo es tu destino antes de llegar.",
        ["Pulsa la <strong>bandera de llegada</strong> de tu ruta.", "Pulsa <strong>«Ver en Street View»</strong>.", "<strong>Google Maps se abre directamente</strong> en tu destino."],
        "¡Se acabaron las vueltas para encontrar la entrada!"),
 "EN": ("Warehouse, loading bay, car park: with the new <strong>StreetView button</strong>, you can see what your destination looks like before you arrive.",
        ["Tap the <strong>finish flag</strong> on your route.", "Tap <strong>“View in Street View”</strong>.", "<strong>Google Maps opens straight</strong> on your destination."],
        "No more driving round in circles to find the entrance!"),
 "NL": ("Magazijn, laadperron, parking: met de nieuwe <strong>StreetView-knop</strong> zie je hoe je bestemming eruitziet voordat je aankomt.",
        ["Tik op de <strong>finishvlag</strong> van je route.", "Tik op <strong>‘Bekijk in Street View’</strong>.", "<strong>Google Maps opent direct</strong> op je bestemming."],
        "Geen rondjes meer rijden om de ingang te vinden!"),
}
AL = {
 "FR": ("Contrôles, accidents, dangers" + NB + ": choisis les alertes que tu veux voir pendant ta navigation.",
        ["Va dans les <strong>paramètres</strong> de l’appli.", "Suis les flèches" + NB + ": <strong>«" + NB + "Alertes" + NB + "»</strong>, puis <strong>«" + NB + "Navigation" + NB + "»</strong>.", "<strong>Coche les alertes que tu veux garder.</strong>"],
        "Les alertes décochées n’apparaîtront plus pendant ta navigation."),
 "IT": ("Controlli, incidenti, pericoli: scegli gli avvisi che vuoi vedere durante la navigazione.",
        ["Vai nelle <strong>impostazioni</strong> dell’app.", "Segui le frecce: <strong>«Avvisi»</strong>, poi <strong>«Navigazione»</strong>.", "<strong>Seleziona gli avvisi che vuoi tenere.</strong>"],
        "Gli avvisi non selezionati non compariranno più durante la navigazione."),
 "ES": ("Controles, accidentes, peligros: elige los avisos que quieres ver durante la navegación.",
        ["Ve a los <strong>ajustes</strong> de la app.", "Sigue las flechas: <strong>«Alertas»</strong> y luego <strong>«Navegación»</strong>.", "<strong>Marca los avisos que quieres mantener.</strong>"],
        "Los avisos desmarcados ya no aparecerán durante tu navegación."),
 "EN": ("Police checks, accidents, hazards: choose which alerts you want to see while navigating.",
        ["Go to the app <strong>settings</strong>.", "Follow the arrows: <strong>“Alerts”</strong>, then <strong>“Navigation”</strong>.", "<strong>Tick the alerts you want to keep.</strong>"],
        "Unticked alerts will no longer appear while you navigate."),
 "NL": ("Controles, ongevallen, gevaren: kies welke meldingen je tijdens het navigeren wilt zien.",
        ["Ga naar de <strong>instellingen</strong> van de app.", "Volg de pijlen: <strong>‘Meldingen’</strong> en dan <strong>‘Navigatie’</strong>.", "<strong>Vink de meldingen aan die je wilt houden.</strong>"],
        "Uitgevinkte meldingen verschijnen niet meer tijdens het navigeren."),
}
RR = {"FR": "Rien à faire" + NB + ": c’est automatique dès que ton appli est à jour.",
      "IT": "Non devi fare nulla: è automatico, basta avere l’app aggiornata.",
      "ES": "No tienes que hacer nada: es automático en cuanto tu app está actualizada.",
      "EN": "Nothing to do: it’s automatic once your app is up to date.",
      "NL": "Je hoeft niets te doen: het gaat automatisch zodra je app up-to-date is."}
KEYS = {"sv": ("StreetView", "Street View", "destinazione prima", "destino antes", "destination before", "bestemming voordat", "destination avant"),
        "al": ("alertes de la communauté", "avvisi della community", "avisos de la comunidad", "Community alerts", "Meldingen van de community"),
        "rr": ("recalcul", "ricalcolo", "recálculo", "rerouting", "herberekenen")}
n = {"sv": 0, "al": 0, "rr": 0}
before = re.findall(r"'src': '([^']+)'", str(src["body"]))
for r in R:
    c = r.get("condition")
    if not c: continue
    it = r["content"][-1]["content"]
    if not (it and it[0].get("type") == "text" and "<h3" in (it[0].get("content") or "")): continue
    title = txt(it[0]["content"]); lg = lang_of(c)
    for k, words in KEYS.items():
        if any(w in title for w in words): break
    else: continue
    if k == "sv":
        a, steps, end = SV[lg]; it[1]["content"] = P(a) + BR + P(f"<strong>{HOW[lg]}</strong>") + OL(steps) + BR + P(f"<strong>{end}</strong>")
    elif k == "al":
        a, steps, end = AL[lg]; it[1]["content"] = P(a) + BR + P(f"<strong>{HOW[lg]}</strong>") + OL(steps) + BR + P(end)
    else:
        it[1]["content"] = it[1]["content"] + BR + P(RR[lg])
    n[k] += 1
assert n == {"sv": 5, "al": 5, "rr": 5}, n
assert re.findall(r"'src': '([^']+)'", str(src["body"])) == before
dump = yaml.dump(src, allow_unicode=True, sort_keys=False, width=10**9)
for fn in ("template_final_v2.yaml", "template_final_v2.txt"): (D / fn).write_text(dump)
print("OK", n, len(before), "images identiques")
