"""Part de la version Brevo de Louna (template_user_v2.yaml), garde toutes ses images, et :
1. section 3 (GPS) déclinée en IT, ES, EN, NL sur le modèle FR ;
2. encart Black Friday refait en blocs Brevo natifs, ton message in-app ;
3. bouton FR de la section 3 et accroche FR de la section 2 corrigés."""
import copy, re, uuid, yaml
from pathlib import Path
import section3_gps as s3
D = Path(__file__).parent
src = yaml.safe_load(open(D / "template_user_v2.yaml"))
rows = src["body"]["content"][0]["content"]
EN_COND = '( "EN" in contact.LANG ) or ( ( contact.LANG != "FR" ) and ( contact.LANG != "ES" ) and ( contact.LANG != "NL" ) and ( contact.LANG != "IT" ) )'
COND = {"FR": '( "FR" in contact.LANG )', "IT": '( "IT" in contact.LANG )', "ES": '( "ES" in contact.LANG )', "NL": '( "NL" in contact.LANG )', "EN": EN_COND}

def lang_of(c):
    return "EN" if c.startswith('( "EN"') else next(k for k in ("FR", "IT", "ES", "NL") if f'( "{k}"' in c)
def new_ids(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "id": o[k] = str(uuid.uuid4())
            else: new_ids(v)
    elif isinstance(o, list):
        for v in o: new_ids(v)
def txt(h): return re.sub(r"<[^>]+>|&nbsp;", " ", h or "")
def items(r): return r["content"][0]["content"]
def set_btn(b, label, href):
    h = f'<p><strong><span style="color: rgb(0, 0, 0);">{label}</span></strong></p>'
    b["text"] = h; b["content"]["text"] = h; b["content"]["href"] = href

# ---------- 1. Section 3 ----------
idx3 = [i for i, r in enumerate(rows) if r.get("condition") and isinstance(items(r)[0].get("content"), str)
        and txt(items(r)[0]["content"]).strip().startswith("3.")]
assert len(idx3) == 5, idx3
fr_row = next(rows[i] for i in idx3 if lang_of(rows[i]["condition"]) == "FR")
fr_btn = items(fr_row)[3]
set_btn(fr_btn, "J’essaie le GPS", "https://lp.truckfly.com/fr/gps-premium?utm_source=brevo&utm_medium=transactional_emails")
fr_btn["layout"]["default"]["width"] = "45%"

def para(d):
    W = 'style="color: rgb(255, 255, 255);"'
    def div(x): return f'<div style="font-style: normal; font-weight: 400;"><span {W}>{x}</span></div>'
    br = '<div style="font-style: normal; font-weight: 400;"><span ' + W + '><br></span></div>'
    stat = re.sub(r"</?strong>", "", d["stat"])
    first, rest = d["intro"].split(". ", 1)
    h = div(f"<strong>{d['hook']}</strong>") + br + div(stat) + br + div(f"{first}. <strong>{rest}</strong>")
    for t, x in (d["cards"][0], d["cards"][1], d["cards"][3]):
        h += br + div(f"<strong>{t}&nbsp;: </strong>{x}" if d is s3.S3["fr"] else f"<strong>{t}: </strong>{x}")
    return h

for i in idx3:
    lg = lang_of(rows[i]["condition"])
    if lg == "FR": continue
    d = s3.S3[lg.lower()]
    r = copy.deepcopy(fr_row); new_ids(r)
    r["condition"] = COND[lg]; r["title"] = f"Bannière {lg}"
    it = items(r)
    it[0]["content"] = f'<h2 class="default-heading2"><span style="color:rgb(255, 255, 255);"><strong>{d["title"]}</strong></span></h2><p><br></p>'
    it[1]["content"] = para(d)
    it[2]["content"] = {"src": "https://creative-assets.mailinblue.com/react-editor/placeholder-images/defaultproduct.png"}
    set_btn(it[3], d["btn"], f"https://lp.truckfly.com/{d['lp']}/gps-premium?utm_source=brevo&utm_medium=transactional_emails")
    rows[i] = r

# ---------- 2. Encart Black Friday en blocs Brevo ----------
BF = {
 "FR": ("BLACK FRIDAY · DU 27 AU 30 NOVEMBRE", "⚡ C’est demain&nbsp;! ⚡", "Ton offre GPS arrive vendredi. Reste connecté&nbsp;!", "Découvrir le GPS", "fr"),
 "EN": ("BLACK FRIDAY · 27 TO 30 NOVEMBER", "⚡ It’s tomorrow! ⚡", "Your GPS offer lands on Friday. Stay tuned!", "Discover the GPS", "en"),
 "ES": ("BLACK FRIDAY · DEL 27 AL 30 DE NOVIEMBRE", "⚡ ¡Es mañana! ⚡", "Tu oferta GPS llega el viernes. ¡Estate atento!", "Descubre el GPS", "es"),
 "IT": ("BLACK FRIDAY · DAL 27 AL 30 NOVEMBRE", "⚡ È domani! ⚡", "La tua offerta GPS arriva venerdì. Resta connesso!", "Scopri il GPS", "it"),
 "NL": ("BLACK FRIDAY · 27 T/M 30 NOVEMBER", "⚡ Het is morgen! ⚡", "Je GPS-aanbieding komt vrijdag. Blijf op de hoogte!", "Ontdek de GPS", "nl"),
}
bf = next(r for r in rows if r.get("title") == "Teasing Black Friday multilangue")
bf["layout"]["default"].update({"background-color": "#0d1b5e", "full-width": True, "padding-top": "28px", "padding-bottom": "20px"})
col = bf["content"][0]; col["layout"]["default"]["background-color"] = "#0d1b5e"
proto_btn = fr_btn
new = []
for lg, (lab, title, body, btn, lp) in BF.items():
    t = {"condition": COND[lg], "id": str(uuid.uuid4()), "title": "Text", "type": "text",
         "layout": {"320px": {"width": "100%"}, "default": {"align": "left", "padding-bottom": "5px", "padding-top": "5px",
                    "text-align": "center", "text-valign": "top", "valign": "top", "width": "100%"}},
         "content": (f'<p style="text-align: center;"><span style="color: rgb(255, 255, 24); font-size: 11px;"><strong>{lab}</strong></span></p>'
                     f'<p style="text-align: center;"><br></p>'
                     f'<p style="text-align: center;"><span style="color: rgb(255, 255, 24); font-size: 28px;"><strong>{title}</strong></span></p>'
                     f'<p style="text-align: center;"><br></p>'
                     f'<p style="text-align: center;"><span style="color: rgb(255, 255, 255); font-size: 16px;">{body}</span></p>')}
    b = copy.deepcopy(proto_btn); new_ids(b); b["condition"] = COND[lg]
    set_btn(b, btn, f"https://lp.truckfly.com/{lp}/gps-premium?utm_source=brevo&utm_medium=transactional_emails")
    b["layout"]["default"]["width"] = "50%"
    new += [t, b]
col["content"] = new

# ---------- 3. Accroche FR de la section 2 ----------
n = 0
for r in rows:
    for it in items(r):
        c = it.get("content")
        if isinstance(c, str) and "reste connectés" in c:
            it["content"] = c.replace("<strong>Demain, c’est le Black Friday</strong> reste connectés ! &nbsp;",
                                      "<strong>Demain, c’est le Black Friday, reste connecté&nbsp;!</strong>"); n += 1
assert n == 1, n

# ---------- Objet ----------
NB = " "
src["subject"] = ('{% if "FR" in contact.LANG %}Demain, c\'est Black Friday' + NB + '! Et tes trajets de Noël' + NB + '?'
    '{% elif "ES" in contact.LANG %}¡Mañana es Black Friday! ¿Y tus rutas de Navidad?'
    '{% elif "IT" in contact.LANG %}Domani è Black Friday! E i divieti di Natale?'
    '{% elif "NL" in contact.LANG %}Morgen is het Black Friday! En je kerstritten?'
    '{% else %}Black Friday tomorrow! Ready for the Christmas bans?{% endif %}')

dump = yaml.dump(src, allow_unicode=True, sort_keys=False, width=10**9)
ids = re.findall(r"^\s*-?\s*id: (\S+)$", dump, re.M)
assert len(ids) == len(set(ids)), "ids en double"
assert "Diventa il miglior" not in dump and "Become the top contributor" not in dump and "MICHELIN" not in dump
for f in ("template_final_v2.yaml", "template_final_v2.txt"): (D / f).write_text(dump)
print("OK", len(ids), "ids")
