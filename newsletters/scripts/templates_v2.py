"""Génère les templates v2 (Trucker et Owner) : python3 newsletters/scripts/templates_v2.py
Les textes entre [crochets] sont à remplacer à chaque édition. Les liens LIEN-... sont à remplacer.
"""
from pathlib import Path

SORTIE = Path(__file__).resolve().parent.parent / "template" / "v2"
F = "font-family:Arial,Helvetica,sans-serif;"
BLEU, JAUNE, CREME, NOIR, GRIS = "#061866", "#FFFF1A", "#F5F3F1", "#000000", "#53565A"


def page(titre, preheader, corps, lang="fr"):
    return f"""<!DOCTYPE html>
<html lang="{lang}" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
<title>{titre}</title>
<!--[if mso]><style>table,td,div,p,a,span{{font-family:Arial,Helvetica,sans-serif !important;}}</style><![endif]-->
<style>
  body{{margin:0;padding:0;width:100%;-webkit-text-size-adjust:100%;}}
  table{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}}
  img{{border:0;display:block;outline:none;text-decoration:none;}}
  a[x-apple-data-detectors]{{color:inherit !important;text-decoration:none !important;}}
  @media screen and (max-width:620px){{
    .conteneur{{width:100% !important;}}
    .pad{{padding-left:20px !important;padding-right:20px !important;}}
    .col{{display:block !important;width:100% !important;box-sizing:border-box !important;padding:0 0 12px 0 !important;}}
    .btn-full, .btn-full a{{display:block !important;width:100% !important;box-sizing:border-box !important;text-align:center !important;}}
    .h1{{font-size:28px !important;line-height:34px !important;}}
  }}
  @media (prefers-color-scheme:dark){{
    .fond{{background-color:#000E38 !important;}}
    .carte{{background-color:#0B1A4F !important;}}
    .creme{{background-color:#061866 !important;}}
    .t-fonce{{color:#FFFFFF !important;}}
    .t-doux{{color:#C9CEDF !important;}}
  }}
</style>
</head>
<body class="fond" style="margin:0;padding:0;background-color:{CREME};">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:{CREME};opacity:0;">{preheader}&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" class="fond" style="background-color:{CREME};">
<tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" class="conteneur" style="width:600px;max-width:600px;">
<tr><td class="pad t-doux" align="right" style="padding:14px 32px;{F}font-size:12px;color:{GRIS};"><a href="{{{{ mirror }}}}" style="color:{GRIS};">Voir dans le navigateur</a></td></tr>
{corps}
</table>
</td></tr>
</table>
</body>
</html>
"""


def bouton(texte, lien, fond=JAUNE, couleur=BLEU, largeur=300):
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" class="btn-full"><tr>
  <td align="center" style="border-radius:26px;background-color:{fond};">
    <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="{lien}" style="height:52px;v-text-anchor:middle;width:{largeur}px;" arcsize="50%" stroke="f" fillcolor="{fond}"><w:anchorlock/><center style="color:{couleur};font-family:Arial,sans-serif;font-size:17px;font-weight:bold;">{texte}</center></v:roundrect><![endif]-->
    <!--[if !mso]><!-- --><a href="{lien}" target="_blank" style="display:inline-block;padding:15px 32px;border-radius:26px;background-color:{fond};{F}font-size:17px;line-height:22px;font-weight:bold;color:{couleur};text-decoration:none;">{texte}&nbsp;&rarr;</a><!--<![endif]-->
  </td></tr></table>"""


def ligne(contenu, fond="#FFFFFF", pad="32px 40px", classe="carte"):
    return f'<tr><td class="pad {classe}" style="background-color:{fond};padding:{pad};{F}">\n{contenu}\n</td></tr>'


def etiquette(texte, sur_bleu=False):
    c = JAUNE if sur_bleu else BLEU
    return f'<p style="margin:0 0 8px 0;{F}font-size:13px;line-height:18px;font-weight:bold;color:{c};letter-spacing:1px;">{texte}</p>'


def titre(texte, sur_bleu=False, taille=24):
    c = "#FFFFFF" if sur_bleu else BLEU
    classe = "" if sur_bleu else ' class="t-fonce"'
    return f'<h2{classe} style="margin:0 0 12px 0;{F}font-size:{taille}px;line-height:{taille + 7}px;font-weight:bold;color:{c};">{texte}</h2>'


def texte(t, sur_bleu=False, marge="0 0 16px 0"):
    c = "#FFFFFF" if sur_bleu else NOIR
    classe = "" if sur_bleu else ' class="t-fonce"'
    return f'<p{classe} style="margin:{marge};{F}font-size:16px;line-height:24px;color:{c};">{t}</p>'


def image(legende, hauteur=280, lien="#"):
    return f"""<a href="{lien}" target="_blank" style="text-decoration:none;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td align="center" valign="middle" height="{hauteur}" style="height:{hauteur}px;background-color:#DCE2F0;border-radius:12px;{F}font-size:14px;color:{BLEU};">[Image : {legende}]<br><span style="font-size:12px;color:{GRIS};">Remplacer ce bloc par un bloc Image Brevo, cliquable</span></td>
</tr></table></a>"""


def stats(items, sur_bleu=False):
    cases = []
    for chiffre, legende in items:
        cases.append(f"""<td class="col" width="{100 // len(items)}%" valign="top" style="padding:0 6px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td align="center" valign="middle" height="104" style="height:104px;background-color:{BLEU if not sur_bleu else '#0F2479'};border-radius:12px;padding:0 10px;{F}">
    <p style="margin:0;font-size:28px;line-height:32px;font-weight:bold;color:{JAUNE};">{chiffre}</p>
    <p style="margin:6px 0 0 0;font-size:13px;line-height:18px;color:#FFFFFF;">{legende}</p>
  </td></tr></table></td>""")
    return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>' + "".join(cases) + "</tr></table>"


def sondage(question, reponses, lien, sur_bleu=True):
    btns = "".join(f"""<tr><td style="padding:0 0 10px 0;"><a href="{lien}?reponse={i}" target="_blank" style="display:block;padding:14px 18px;border-radius:10px;background-color:#FFFFFF;{F}font-size:15px;line-height:20px;font-weight:bold;color:{BLEU};text-decoration:none;border:2px solid #FFFFFF;">{r}</a></td></tr>"""
                   for i, r in enumerate(reponses, 1))
    return (etiquette("SONDAGE EXPRESS · 1 CLIC", True) + titre(question, True, 21)
            + texte("{{CONSIGNE}}", True, "0 0 18px 0")
            + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{btns}</table>')


def pied(raison):
    return f"""<tr><td class="pad" style="background-color:{BLEU};padding:28px 40px;{F}" align="center">
  <p style="margin:0 0 6px 0;font-size:15px;line-height:22px;font-weight:bold;color:#FFFFFF;">Suivez Michelin Truckfly</p>
  <p style="margin:0;font-size:14px;line-height:22px;"><a href="LIEN-FACEBOOK" style="color:{JAUNE};font-weight:bold;">Facebook</a> &nbsp;·&nbsp; <a href="LIEN-INSTAGRAM" style="color:{JAUNE};font-weight:bold;">Instagram</a> &nbsp;·&nbsp; <a href="LIEN-LINKEDIN" style="color:{JAUNE};font-weight:bold;">LinkedIn</a></p>
</td></tr>
<tr><td class="pad t-doux" align="center" style="padding:24px 40px 36px 40px;{F}font-size:12px;line-height:18px;color:{GRIS};">
  <p style="margin:0 0 8px 0;">{raison}</p>
  <p style="margin:0 0 8px 0;"><a href="{{{{ unsubscribe }}}}" style="color:{GRIS};">Se désinscrire</a></p>
  <p style="margin:0;">Michelin Truckfly · [adresse postale]</p>
</td></tr>"""


def entete(sous_titre):
    return f"""<tr><td class="pad" style="background-color:{BLEU};padding:24px 40px;{F}">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
    <td valign="middle"><a href="LIEN-APP"><img src="../../assets/logo-truckfly-blanc.png" width="150" height="38" alt="Michelin Truckfly" style="width:150px;height:38px;{F}font-size:18px;font-weight:bold;color:#FFFFFF;"></a></td>
    <td valign="middle" align="right" style="{F}font-size:13px;line-height:18px;color:#FFFFFF;">{sous_titre}</td>
  </tr></table>
</td></tr>"""


# ---------------- TRUCKER ----------------
def trucker():
    c = []
    c.append(entete("[Mois] · Ta newsletter"))
    # Hero personnalisé
    c.append(ligne(
        etiquette("SALUT {{ contact.PRENOM | default : \"LA ROUTE\" }} 👋".replace(" 👋", ""), True)
        + f'<h1 class="h1" style="margin:0 0 14px 0;{F}font-size:34px;line-height:40px;font-weight:bold;color:#FFFFFF;">[Titre du mois : une promesse courte, ex. « Trouve ta place avant 17 h »]</h1>'
        + texte("[1 ou 2 phrases qui donnent envie : le bénéfice pour le routier, pas la fonctionnalité.]", True, "0 0 22px 0")
        + bouton("[Action principale]", "LIEN-APP?utm_content=hero"),
        fond=BLEU, pad="36px 40px 40px 40px", classe=""))
    c.append(ligne(image("photo du mois, 1200 × 600, un vrai routier ou un vrai lieu", 280, "LIEN-APP?utm_content=image"), pad="0 40px 0 40px", fond=BLEU, classe=""))
    c.append(f'<tr><td style="background-color:{BLEU};height:32px;line-height:32px;font-size:0;">&nbsp;</td></tr>')
    # Communauté en chiffres
    c.append(ligne(
        etiquette("LA COMMUNAUTÉ CE MOIS-CI") + titre("Grâce à vous, la route est mieux renseignée")
        + stats([("[X]", "avis déposés"), ("[X]", "nouveaux lieux"), ("[X]", "nouveaux Profils Trucker")])
        + texte("Chaque avis aide un collègue à mieux s'arrêter. Merci !", marge="16px 0 0 0"),
        pad="36px 34px 30px 34px"))
    # Spot du mois
    c.append(ligne(
        etiquette("LE SPOT DU MOIS") + titre("[Nom du lieu], [ville]")
        + image("photo du lieu", 220, "LIEN-SPOT")
        + f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:16px 0 0 0;"><tr>
  <td class="creme" style="background-color:{CREME};border-radius:12px;padding:18px 20px;{F}">
    <p style="margin:0 0 6px 0;font-size:16px;line-height:20px;color:{BLEU};font-weight:bold;">★★★★★ <span class="t-fonce" style="color:{NOIR};font-weight:normal;font-size:14px;">[4,8/5 · X avis]</span></p>
    <p class="t-fonce" style="margin:0 0 6px 0;font-size:16px;line-height:24px;color:{NOIR};font-style:italic;">« [Extrait d'un vrai avis de routier] »</p>
    <p class="t-doux" style="margin:0;font-size:13px;line-height:18px;color:{GRIS};">[Prénom], routier depuis [X] ans</p>
  </td></tr></table>"""
        + '<div style="height:18px;line-height:18px;font-size:0;">&nbsp;</div>'
        + bouton("Voir le spot", "LIEN-SPOT", fond=BLEU, couleur="#FFFFFF", largeur=220),
        pad="8px 40px 36px 40px"))
    # Sondage 1 clic
    c.append(ligne(
        sondage("[Question du sondage, ex. « Ton plus gros souci pour te garer le soir ? »]",
                ["[Réponse A]", "[Réponse B]", "[Réponse C]"], "LIEN-SONDAGE")
        .replace("{{CONSIGNE}}", "Clique sur ta réponse, c'est tout. Les résultats arrivent dans la prochaine newsletter."),
        fond=BLEU, pad="36px 40px 30px 40px", classe=""))
    # Astuce
    c.append(ligne(
        etiquette("L'ASTUCE DE LA ROUTE") + titre("[Titre de l'astuce]")
        + texte("[3 phrases max. Concrète, utile tout de suite. Ex. : comment filtrer les parkings sécurisés dans l'app.]")
        + f'<p style="margin:0;{F}font-size:15px;line-height:22px;"><a href="LIEN-ASTUCE" style="color:{BLEU};font-weight:bold;">[Voir comment faire]&nbsp;&rarr;</a></p>',
        pad="36px 40px 32px 40px"))
    # Nouveauté app 2 colonnes
    c.append(ligne(f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td class="col" width="42%" valign="top" style="padding-right:16px;">{image("capture de l'app", 230, "LIEN-NOUVEAUTE")}</td>
  <td class="col" width="58%" valign="middle">
    {etiquette("NOUVEAU DANS L'APP")}{titre("[Nom de la nouveauté]", taille=21)}
    {texte("[Ce que ça change pour toi, en 2 phrases.]")}
    {bouton("[Essayer]", "LIEN-NOUVEAUTE", fond=BLEU, couleur="#FFFFFF", largeur=180)}
  </td></tr></table>""", fond=CREME, pad="32px 40px", classe="creme"))
    c.append(pied("Tu reçois cet e-mail parce que tu utilises l'application Michelin Truckfly."))
    return page("Newsletter Trucker", "[Preheader : complète l'objet, 60 à 90 caractères]", "\n".join(c))


# ---------------- OWNER ----------------
def owner():
    c = []
    c.append(entete("Espace établissements · [Mois]"))
    c.append(ligne(
        etiquette("BONJOUR {{ contact.PRENOM | default : \"\" }}", True)
        + f'<h1 class="h1" style="margin:0 0 14px 0;{F}font-size:32px;line-height:38px;font-weight:bold;color:#FFFFFF;">[Titre du mois, ex. « L\'hiver arrive : soyez le premier choix des routiers »]</h1>'
        + texte("[1 ou 2 phrases : le bénéfice pour l'établissement (plus de visites, plus d'avis, plus de visibilité).]", True, "0 0 22px 0")
        + bouton("Mettre à jour ma fiche", "LIEN-ESPACE-PRO?utm_content=hero", largeur=280),
        fond=BLEU, pad="36px 40px 40px 40px", classe=""))
    # Chiffres
    c.append(ligne(
        etiquette("CE MOIS-CI SUR MICHELIN TRUCKFLY") + titre("Les routiers cherchent des lieux comme le vôtre")
        + stats([("[X]", "recherches de restaurants"), ("[X]", "recherches de parkings"), ("[X]", "avis déposés")])
        + texte("[Une phrase pour relier ces chiffres à l'action : une fiche complète ressort mieux.]", marge="16px 0 0 0"),
        pad="36px 34px 30px 34px"))
    # Checklist fiche
    items = [("Des photos récentes", "extérieur, parking, salle, douches"),
             ("Les horaires à jour", "surtout les jours fériés et la nuit"),
             ("Les services pour les routiers", "parking PL, douches, Wi-Fi, menu routier"),
             ("Une réponse à chaque avis", "même court, un merci compte")]
    lignes = "".join(f"""<tr><td width="34" valign="top" style="padding:0 0 14px 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" width="24" height="24" style="width:24px;height:24px;border-radius:12px;background-color:{BLEU};{F}font-size:14px;line-height:24px;font-weight:bold;color:{JAUNE};">✓</td></tr></table></td>
<td class="t-fonce" valign="top" style="padding:1px 0 14px 0;{F}font-size:16px;line-height:23px;color:{NOIR};"><strong>{a}</strong><br><span class="t-doux" style="color:{GRIS};font-size:14px;">{b}</span></td></tr>""" for a, b in items)
    c.append(ligne(
        etiquette("VOTRE FICHE EN 4 POINTS") + titre("Une fiche complète, c'est plus de routiers à votre porte")
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 10px 0;">{lignes}</table>'
        + bouton("Compléter ma fiche", "LIEN-ESPACE-PRO?utm_content=checklist", fond=BLEU, couleur="#FFFFFF", largeur=260),
        fond=CREME, pad="36px 40px", classe="creme"))
    # Établissement du mois
    c.append(ligne(
        etiquette("ILS EN PARLENT") + titre("[Nom de l'établissement], [ville]")
        + f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td class="col" width="40%" valign="top" style="padding-right:16px;">{image("photo de l'établissement", 200, "LIEN-TEMOIGNAGE")}</td>
  <td class="col" width="60%" valign="top">
    <p class="t-fonce" style="margin:0 0 10px 0;{F}font-size:17px;line-height:25px;color:{NOIR};font-style:italic;">« [Citation du gérant : ce que Michelin Truckfly lui a apporté] »</p>
    <p class="t-doux" style="margin:0 0 14px 0;{F}font-size:13px;line-height:18px;color:{GRIS};">[Prénom Nom], [fonction]</p>
    <p style="margin:0;{F}font-size:15px;line-height:22px;"><a href="LIEN-TEMOIGNAGE" style="color:{BLEU};font-weight:bold;">Lire son témoignage&nbsp;&rarr;</a></p>
  </td></tr></table>""",
        pad="36px 40px"))
    # Conseil
    c.append(ligne(
        etiquette("LE CONSEIL DU MOIS", True) + titre("[Titre du conseil, ex. « Répondre aux avis en 2 minutes »]", True)
        + texte("[3 phrases max, concrètes et applicables tout de suite.]", True, "0 0 20px 0")
        + bouton("[Action liée au conseil]", "LIEN-CONSEIL", largeur=280),
        fond=BLEU, pad="36px 40px", classe=""))
    # Contact
    c.append(ligne(f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td class="col" valign="middle" style="{F}">
    {titre("Une question sur votre fiche ?", taille=20)}
    {texte("Notre équipe vous répond et vous aide à la mettre à jour.", marge="0")}
  </td>
  <td class="col" valign="middle" align="right" width="200">{bouton("Nous écrire", "mailto:[adresse-support]", fond=BLEU, couleur="#FFFFFF", largeur=180)}</td>
</tr></table>""", pad="32px 40px"))
    c.append(pied("Vous recevez cet e-mail car votre établissement est référencé sur Michelin Truckfly."))
    return page("Newsletter Owner", "[Preheader : complète l'objet, 60 à 90 caractères]", "\n".join(c))


if __name__ == "__main__":
    SORTIE.mkdir(parents=True, exist_ok=True)
    (SORTIE / "trucker.html").write_text(trucker(), encoding="utf-8")
    (SORTIE / "owner.html").write_text(owner(), encoding="utf-8")
    print("ok")
