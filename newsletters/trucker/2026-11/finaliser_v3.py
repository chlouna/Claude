"""Part de la dernière version Brevo de Louna (template_user_v3.yaml), garde toutes ses images, et :
1. remet l'encart Black Friday (blocs natifs) après l'intro ;
2. section 1 au format avant / pendant / après (section1_v2.S) ;
3. objet de novembre."""
import copy, re, uuid, yaml
from pathlib import Path
import section1_v2 as s1
from finaliser_v2 import new_ids, lang_of, src as _unused  # noqa (réutilise les helpers)
D = Path(__file__).parent
src = yaml.safe_load(open(D / "template_user_v3.yaml"))
rows = src["body"]["content"][0]["content"]
def items(r): return r["content"][0]["content"]
def txt(h): return re.sub(r"<[^>]+>|&nbsp;", " ", h or "")
def srcs(o):
    return re.findall(r"'src': '([^']+)'", str(o))
avant = srcs(src["body"])

# 1. encart BF
bf = copy.deepcopy(next(r for r in yaml.safe_load(open(D / "template_final_v2.yaml"))["body"]["content"][0]["content"]
                        if r.get("title") == "Teasing Black Friday multilangue"))
new_ids(bf)
nl_intro = next(i for i, r in enumerate(rows) if r.get("condition") == '( "NL" in contact.LANG )')
rows.insert(nl_intro + 1, bf)

# 2. section 1
n = 0
for r in rows:
    if not r.get("condition"): continue
    it = items(r); t = it[0].get("content")
    if not (isinstance(t, str) and txt(t).strip().startswith("1.")): continue
    d = s1.S[lang_of(r["condition"])]
    it[0]["content"] = f'<p><br></p><h2 class="default-heading2"><span style="color: rgb(255, 255, 255);">{d["title"]}</span></h2><p><br></p>'
    it[1]["content"] = s1.para(d)
    it[2]["content"]["href"] = "https://truckflyapp.onelink.me/2ysq/r4vkfd60"
    b = it[3]; h = f'<p><strong><span style="color: rgb(0, 0, 0);">{d["btn"]}</span></strong></p>'
    b["text"] = h; b["content"]["text"] = h; b["content"]["href"] = "https://truckflyapp.onelink.me/2ysq/r4vkfd60"
    b["layout"]["default"]["width"] = "55%"
    n += 1
assert n == 5, n

# 3. objet
NB = " "
src["subject"] = ('{% if "FR" in contact.LANG %}Demain, c\'est Black Friday' + NB + '! Et tes trajets de Noël' + NB + '?'
    '{% elif "ES" in contact.LANG %}¡Mañana es Black Friday! ¿Y tus rutas de Navidad?'
    '{% elif "IT" in contact.LANG %}Domani è Black Friday! E i divieti di Natale?'
    '{% elif "NL" in contact.LANG %}Morgen is het Black Friday! En je kerstritten?'
    '{% else %}Black Friday tomorrow! Ready for the Christmas bans?{% endif %}')

apres = [s for s in srcs(src["body"])]
assert all(s in apres for s in avant), "image perdue"
dump = yaml.dump(src, allow_unicode=True, sort_keys=False, width=10**9)
ids = re.findall(r"^\s*-?\s*id: (\S+)$", dump, re.M)
assert len(ids) == len(set(ids)), "ids en double"
assert "MICHELIN" not in dump and "les jours où tu ne roules pas" not in dump
for f in ("template_final_v3.yaml", "template_final_v3.txt"): (D / f).write_text(dump)
print("OK", len(ids), "ids,", len(rows), "rangées,", len(avant), "images gardées")
