"""Section 1 v2 : recentrée chauffeur (où passer son arrêt pendant les fêtes), 5 langues.
Dates : Bison Futé (régime général), DM MIT 325/2025 (calendrier 2026). Appliquée sur template_final_v2."""
import re, yaml
from pathlib import Path
D = Path(__file__).parent
NB = "&nbsp;"
W = "rgb(249, 250, 252)"
S = {
 "FR": dict(title="1. Noël et Nouvel An" + NB + ": choisis le bon arrêt",
   hook="Routes chargées, restos fermés, parkings pleins" + NB + ": pendant les fêtes, trouver un bon arrêt prend du temps. Voici comment Michelin Truckfly t’aide avant, pendant et après les fêtes.",
   steps=[("Avant", "Prépare tes arrêts sur ta route. Regarde tout" + NB + ": les photos, les avis et maintenant les j’aime. Les contributions les plus aimées t’indiquent les lieux les plus fiables."),
          ("Pendant", "Lis les avis les plus récents pour savoir ce qui est ouvert (douches, resto, boutique) et si le parking est plein."),
          ("Après", "Laisse un avis, ajoute une photo ou like une contribution utile" + NB + ": tu aides le collègue suivant, et chaque action te rapporte 1" + NB + "point.")],
   note="À noter" + NB + ": en France, les poids lourds de plus de 7,5" + NB + "t ne roulent pas du jeudi 24 décembre 22" + NB + "h au vendredi 25 décembre 22" + NB + "h, ni du jeudi 31 décembre 22" + NB + "h au vendredi 1er janvier 22" + NB + "h.",
   btn="Je trouve mon parking"),
 "EN": dict(title="1. Christmas and New Year: pick the right truck stop",
   hook="Busy roads, closed restaurants, packed car parks: over the holidays, finding a good stop takes time. Here’s how Michelin Truckfly helps you before, during and after the holidays.",
   steps=[("Before", "Plan your stops along your route. Look at everything: photos, reviews and now likes. The most liked contributions point you to the most reliable places."),
          ("During", "Read the most recent reviews to see what’s open (showers, restaurant, shop) and how busy the car park is."),
          ("After", "Leave a review, add a photo or like a useful contribution: you help the next driver, and every action earns you 1 point.")],
   note="Heading to the continent? In France, trucks over 7.5 t can’t drive on 25 December and 1 January.",
   btn="Find my truck stop"),
 "ES": dict(title="1. Navidad y Año Nuevo: elige bien tu parada",
   hook="Carreteras cargadas, restaurantes cerrados, aparcamientos llenos: en las fiestas, encontrar una buena parada lleva tiempo. Así te ayuda Michelin Truckfly antes, durante y después de las fiestas.",
   steps=[("Antes", "Prepara tus paradas en tu ruta. Míralo todo: las fotos, las opiniones y ahora los me gusta. Las aportaciones con más me gusta te indican los lugares más fiables."),
          ("Durante", "Lee las opiniones más recientes para saber qué está abierto (duchas, restaurante, tienda) y si el aparcamiento está lleno."),
          ("Después", "Deja una opinión, añade una foto o da me gusta a una aportación útil: ayudas al compañero que viene detrás, y cada acción te da 1 punto.")],
   note="¿Vas a Francia? Allí los camiones de más de 7,5 t no pueden circular del jueves 24 de diciembre a las 22 h al viernes 25 a las 22 h, ni del jueves 31 de diciembre a las 22 h al viernes 1 de enero a las 22 h.",
   btn="Busco mi aparcamiento"),
 "IT": dict(title="1. Natale e Capodanno: scegli la sosta giusta",
   hook="Strade trafficate, ristoranti chiusi, parcheggi pieni: durante le feste, trovare una buona sosta richiede tempo. Ecco come ti aiuta Michelin Truckfly prima, durante e dopo le feste.",
   steps=[("Prima", "Prepara le tue soste lungo il percorso. Guarda tutto: le foto, le recensioni e ora anche i like. I contributi con più like ti indicano i posti più affidabili."),
          ("Durante", "Leggi le recensioni più recenti per sapere cosa è aperto (docce, ristorante, negozio) e se il parcheggio è pieno."),
          ("Dopo", "Lascia una recensione, aggiungi una foto o metti like a un contributo utile: aiuti il collega che arriva dopo, e ogni azione ti fa guadagnare 1 punto.")],
   note="Da ricordare: in Italia i mezzi oltre 7,5 t non possono circolare fuori dai centri abitati, dalle 9 alle 22, domenica 6, martedì 8, domenica 13, domenica 20, venerdì 25, sabato 26 e domenica 27 dicembre.",
   btn="Trovo il mio parcheggio"),
 "NL": dict(title="1. Kerst en Oud en Nieuw: kies de juiste parking",
   hook="Drukke wegen, gesloten restaurants, volle parkings: tijdens de feestdagen kost een goede stop tijd. Zo helpt Michelin Truckfly je voor, tijdens en na de feestdagen.",
   steps=[("Voor", "Plan je stops langs je route. Bekijk alles: foto’s, reviews en nu ook likes. De meest gelikete bijdragen wijzen je de meest betrouwbare plekken aan."),
          ("Tijdens", "Lees de meest recente reviews om te zien wat er open is (douches, restaurant, winkel) en hoe vol de parking is."),
          ("Na", "Laat een review achter, voeg een foto toe of like een nuttige bijdrage: zo help je de volgende chauffeur, en elke actie levert je 1 punt op.")],
   note="Rij je naar Frankrijk? Daar mogen vrachtwagens boven 7,5 t niet rijden op 25 december en 1 januari.",
   btn="Ik zoek mijn parking"),
}
def p(t): return f'<p class="default"><span style="color: {W};">{t}</span></p>'
BR = '<p class="default"><br></p>'
def para(d):
    if "steps" in d:
        h = p(f"<strong>{d['hook']}</strong>") + BR
        for t, x in d["steps"]:
            h += p(f"<strong>{t}</strong>") + p(x) + BR
        return h + f'<p class="default"><span style="color: {W}; font-size: 14px;">{d["note"]}</span></p>'
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
