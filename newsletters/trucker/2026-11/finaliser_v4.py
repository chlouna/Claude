"""Part de la version Brevo v4 de Louna (images gardées) et :
1. section 2 : IT/ES/EN/NL recopiées sur la structure FR (libellés de l'appli) ;
2. section 1 au format avant / pendant / après ;
3. bannières BF en image : condition EN complète + lien vers la page GPS ;
4. section 3 EN/NL : on remet les visuels GPS déjà uploadés ;
5. objet de novembre."""
import re, yaml
from pathlib import Path
import section1_v2 as s1
D = Path(__file__).parent
src = yaml.safe_load(open(D / "template_user_v4.yaml"))
rows = src["body"]["content"][0]["content"]
EN_COND = '( "EN" in contact.LANG ) or ( ( contact.LANG != "FR" ) and ( contact.LANG != "ES" ) and ( contact.LANG != "NL" ) and ( contact.LANG != "IT" ) )'
def lang_of(c): return "EN" if c.startswith('( "EN"') else next(k for k in ("FR", "IT", "ES", "NL") if f'( "{k}"' in c)
def items(r): return r["content"][0]["content"]
def txt(h): return re.sub(r"<[^>]+>|&nbsp;", " ", h or "").strip()
def srcs(o): return re.findall(r"'src': '([^']+)'", str(o))
avant = srcs(src["body"])

# 1. Section 2
B = 'style="color: rgb(0, 0, 0);"'
def sp(x): return f'<span {B}>{x}</span>'
def s2(hook, profit, how, n, b1, b2, then, steps):
    return ('<p class="default"><br></p>'
        f'<p>{sp(f"<strong>{hook}</strong>")}</p><p>{sp("<br>")}</p>'
        f'<p>{sp(profit)}</p><p><br></p>'
        f'<p class="default"><span {B}><strong>{how}</strong><strong><span style="background-color: rgb(255, 255, 26);"> {n}</span></strong><strong>:</strong></span></p>'
        f'<p class="default">{sp("<br>")}</p>'
        f'<ul><li {B}>{b1}</li><li {B}>{b2}</li></ul><p>{sp("<br>")}</p>'
        f'<p class="default">{sp(f"<strong>{then}</strong>")}</p>'
        '<ol>' + "".join(f'<li {B}>{s}</li>' for s in steps) + '</ol><p><br></p>')
S2 = {
 "IT": s2("Domani è Black Friday, resta connesso!", "Per approfittarne, basta inserire il codice nell’app.",
          "Per aprire la schermata Premium, hai", "2 possibilità",
          "Tocca l’icona del GPS in basso sulla mappa;",
          "oppure vai nel tuo profilo, in alto a sinistra della mappa, e tocca «Premium · prova gratis».",
          "Poi:", ["Scegli «O Utilizza un codice promozionale».", "Inserisci il codice.", "Tocca «Riscatta»."]),
 "ES": s2("Mañana es Black Friday, ¡estate atento!", "Para aprovecharlo, solo tienes que introducir tu código en la app.",
          "Para abrir la pantalla Premium, tienes", "2 opciones",
          "Pulsa el icono del GPS en la parte inferior del mapa;",
          "o ve a tu perfil, arriba a la izquierda del mapa, y pulsa «Premium · pruébalo gratis».",
          "Después:", ["Elige «Cualquiera Utilizar un código».", "Introduce tu código.", "Pulsa «Canjear»."]),
 "EN": s2("Black Friday starts tomorrow, stay tuned!", "To enjoy it, just enter your code in the app.",
          "To open the Premium screen, you have", "2 options",
          "Tap the GPS icon at the bottom of the map;",
          "or go to your profile, top left of the map, then tap “Premium · try for free”.",
          "Then:", ["Choose “Either Use a promotional code”.", "Enter your code.", "Tap “Redeem”."]),
 "NL": s2("Morgen is het Black Friday, blijf op de hoogte!", "Om ervan te profiteren, voer je gewoon je code in de app in.",
          "Om het Premium-scherm te openen, heb je", "2 mogelijkheden",
          "Tik op het gps-icoon onderaan de kaart;",
          "of ga naar je profiel, linksboven op de kaart, en tik op ‘Premium · probeer gratis’.",
          "Daarna:", ["Kies ‘Of Gebruik een promotiecode’.", "Voer je code in.", "Tik op ‘Inwisselen’."]),
}
n2 = n1 = 0
for r in rows:
    if not r.get("condition"): continue
    it = items(r); t = it[0].get("content")
    if not isinstance(t, str): continue
    lg = lang_of(r["condition"]); head = txt(t)
    if head.startswith("2.") and lg != "FR":
        it[1]["content"] = S2[lg]; n2 += 1
    elif head.startswith("1."):
        d = s1.S[lg]
        it[0]["content"] = f'<p><br></p><h2 class="default-heading2"><span style="color: rgb(255, 255, 255);">{d["title"]}</span></h2><p><br></p>'
        it[1]["content"] = s1.para(d)
        it[2]["content"]["href"] = "https://truckflyapp.onelink.me/2ysq/r4vkfd60"
        b = it[3]; h = f'<p><strong><span style="color: rgb(0, 0, 0);">{d["btn"]}</span></strong></p>'
        b["text"] = h; b["content"]["text"] = h; b["content"]["href"] = "https://truckflyapp.onelink.me/2ysq/r4vkfd60"
        b["layout"]["default"]["width"] = "55%"; n1 += 1
assert n2 == 4 and n1 == 5, (n2, n1)

# 3. Bannières BF (rangées avec une seule image)
nb = 0
for r in rows:
    it = items(r)
    if r.get("condition") and len(it) == 1 and it[0]["type"] == "image" and "6afab" in it[0]["content"]["src"]:
        if r["condition"] == '( "EN" in contact.LANG )': r["condition"] = EN_COND
        lg = lang_of(r["condition"]).lower()
        it[0]["content"]["href"] = f"https://lp.truckfly.com/{lg}/gps-premium?utm_source=brevo&utm_medium=transactional_emails"
        it[0]["layout"]["default"]["type"] = "absoluteLink"; nb += 1
assert nb == 5, nb

# 4. Section 3 EN / NL : visuels GPS déjà uploadés (version précédente)
GPS = {"EN": "https://img.mailinblue.com/4222425/images/content_library/original/6af70cc09315e0271c3b3403.png",
       "NL": "https://img.mailinblue.com/4222425/images/content_library/original/6af70cebfb8879568609c3e7.png"}
for r in rows:
    it = items(r)
    if r.get("condition") and isinstance(it[0].get("content"), str) and txt(it[0]["content"]).startswith("3."):
        lg = lang_of(r["condition"])
        if lg in GPS and "placeholder" in it[2]["content"]["src"]:
            it[2]["content"]["src"] = GPS[lg]; it[2]["layout"]["default"]["canvas-height"] = "359px"

# 5. Objet
NB = " "
src["subject"] = ('{% if "FR" in contact.LANG %}Demain, c\'est Black Friday' + NB + '! Et tes trajets de Noël' + NB + '?'
    '{% elif "ES" in contact.LANG %}¡Mañana es Black Friday! ¿Y tus rutas de Navidad?'
    '{% elif "IT" in contact.LANG %}Domani è Black Friday! E i tuoi viaggi di Natale?'
    '{% elif "NL" in contact.LANG %}Morgen is het Black Friday! En je kerstritten?'
    '{% else %}Black Friday tomorrow! Ready for your Christmas trips?{% endif %}')

apres = srcs(src["body"])
assert all(s in apres for s in avant if "placeholder" not in s), "image perdue"
dump = yaml.dump(src, allow_unicode=True, sort_keys=False, width=10**9)
ids = re.findall(r"^\s*-?\s*id: (\S+)$", dump, re.M)
assert len(ids) == len(set(ids)) and "MICHELIN" not in dump
for f in ("template_final_v4.yaml", "template_final_v4.txt"): (D / f).write_text(dump)
print("OK", len(ids), "ids")
