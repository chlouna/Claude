"""Ordre de vente : bannière BF, GPS (1), code promo (2), arrêts des fêtes (3). Part de template_final_v5."""
import re, yaml
from pathlib import Path
D = Path(__file__).parent
src = yaml.safe_load(open(D / "template_final_v5.yaml"))
rows = src["body"]["content"][0]["content"]
def items(r): return r["content"][0]["content"]
def head(r):
    c = items(r)[0].get("content") if r.get("condition") else None
    return re.sub(r"<[^>]+>|&nbsp;", " ", c).strip()[:2] if isinstance(c, str) else ""
idx = {k: [i for i, r in enumerate(rows) if head(r) == k] for k in ("1.", "2.", "3.")}
assert all(len(v) == 5 for v in idx.values()), idx
start = idx["1."][0]
assert idx["1."] + idx["2."] + idx["3."] == list(range(start, start + 15))
s1, s2, s3 = ([rows[i] for i in idx[k]] for k in ("1.", "2.", "3."))
def renum(r, old, new):
    t = items(r)[0]; t["content"] = re.sub(r"(>|^)(\s*)" + re.escape(old) + r"(\s)", r"\g<1>\g<2>" + new + r"\3", t["content"], count=1)
    assert new in t["content"], t["content"][:120]
for r in s3: renum(r, "3.", "1.")
for r in s1: renum(r, "1.", "3.")
rows[start:start + 15] = s3 + s2 + s1
# intro dans le même ordre
NB = "&nbsp;"
INTRO = {
 "Ce mois-ci, découvre ": "pourquoi un GPS poids lourds change tout, comment activer ton code promo en 30" + NB + "secondes, comment bien choisir tes arrêts pendant les fêtes, et les meilleurs contributeurs de novembre" + NB + "!",
 "Questo mese scopri ": "perché un GPS per camion fa la differenza, come attivare il tuo codice promo in 30 secondi, come scegliere bene le tue soste durante le feste e i migliori contributori di novembre!",
 "Este mes descubre ": "por qué un GPS para camiones lo cambia todo, cómo activar tu código promocional en 30 segundos, cómo elegir bien tus paradas en las fiestas y a los mejores colaboradores de noviembre.",
 "This month, find out ": "why a truck GPS makes all the difference, how to activate your promo code in 30 seconds, how to pick the right stops over the holidays, and November’s top contributors!",
 "Deze maand ontdek je ": "waarom een vrachtwagen-GPS het verschil maakt, hoe je je promotiecode in 30 seconden activeert, hoe je tijdens de feestdagen de juiste stops kiest en de topbijdragers van november!",
}
n = 0
for r in rows:
    for it in items(r):
        c = it.get("content")
        if not isinstance(c, str): continue
        for lead, body in INTRO.items():
            new = re.sub(re.escape(lead) + r"<strong>.*?</strong>", lambda m: f"{lead}<strong>{body}</strong>", c, count=1)
            if new != c: it["content"] = c = new; n += 1
assert n == 5, n
dump = yaml.dump(src, allow_unicode=True, sort_keys=False, width=10**9)
for f in ("template_final_v6.yaml", "template_final_v6.txt"): (D / f).write_text(dump)
print("OK", [head(r) + r["condition"][4:6] for r in rows[start:start + 15]])
