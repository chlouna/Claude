"""Génère la newsletter B2B à partir de template/b2b.html.

Usage : python3 newsletters/scripts/generer_b2b.py
Structure : Édito, Récap du mois, I. Événements, II. Infos Michelin Truckfly,
III. Infos Marché/Légal (UE puis pays, le pays du lecteur en premier), IV. La question des Truckers.
Les textes entre [crochets] sont à compléter : ils ressortent surlignés dans l'aperçu.
"""
import re
from pathlib import Path
from string import Template
from html import escape

RACINE = Path(__file__).resolve().parent.parent
GABARIT = Template((RACINE / "template" / "b2b.html").read_text(encoding="utf-8"))

# À remplacer avant l'envoi (voir LISEZMOI.md).
LIEN_B2B = "https://LIEN-B2B-A-REMPLACER"            # bouton final et logo
LIENS = {
    "voltix": "https://LIEN-VOLTIX-A-REMPLACER",           # stations Voltix dans l'app ou page partenariat
    "rdv": "https://LIEN-RDV-A-REMPLACER",                 # prise de rendez-vous ou e-mail de l'équipe
    "video": "https://LIEN-VIDEO-PROFIL-A-REMPLACER",      # vidéo du Profil Trucker
    "app": "https://LIEN-APP-A-REMPLACER",                 # page de téléchargement de l'app
    "linkedin": "https://LIEN-LINKEDIN-A-REMPLACER",       # page LinkedIn Michelin Truckfly
    "sondage": "https://LIEN-SONDAGE-A-REMPLACER",         # sondage du mois prochain
}
ASSETS = "../../assets"
ADRESSE = "Michelin Truckfly · [adresse postale à compléter]"

FONT = "font-family:'Noto Sans',Arial,Helvetica,sans-serif;"
PAYS_LECTEUR = {"fr": "FR", "it": "IT", "es": "ES", "de": "DE", "nl": "NL", "pl": "PL", "en": None}


def t(texte):
    """Échappe le texte et surligne les [passages à compléter]."""
    texte = escape(texte, quote=False)
    return re.sub(r"\[([^\]]+)\]",
                  r'<span style="background-color:#FFF3A0;color:#000000;">[\1]</span>', texte)


def utm(url, campagne, langue, contenu):
    """Lien Michelin Truckfly suivi. Les sources externes passent par escape() sans UTM."""
    sep = "&amp;" if "?" in url else "?"
    return (f"{escape(url)}{sep}utm_source=brevo&amp;utm_medium=email"
            f"&amp;utm_campaign={campagne}-{langue}&amp;utm_content={contenu}")


def paragraphe(texte, taille=16):
    return (f'      <p class="texte-fonce" style="margin:0 0 14px 0;{FONT}font-size:{taille}px;'
            f'line-height:{round(taille * 1.55)}px;color:#000000;">{t(texte)}</p>')


def lien_texte(libelle, href):
    return (f'<a class="lien" href="{href}" target="_blank" style="color:#061866;font-weight:bold;'
            f'text-decoration:underline;">{t(libelle)}&nbsp;&rarr;</a>')


def bouton(libelle, href, marge="8px 0 0 0"):
    return f"""      <table role="presentation" class="btn-table" cellpadding="0" cellspacing="0" border="0" style="margin:{marge};">
        <tr><td class="btn2-cell" align="center" style="border-radius:24px;background-color:#061866;">
          <!--[if mso]>
          <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="{href}" style="height:48px;v-text-anchor:middle;width:330px;" arcsize="50%" stroke="f" fillcolor="#061866">
            <w:anchorlock/>
            <center style="color:#FFFFFF;font-family:Arial,sans-serif;font-size:16px;font-weight:bold;">{t(libelle)}</center>
          </v:roundrect>
          <![endif]-->
          <!--[if !mso]><!-- -->
          <a class="btn2" href="{href}" target="_blank" style="display:inline-block;padding:14px 28px;border-radius:24px;background-color:#061866;{FONT}font-size:16px;line-height:20px;font-weight:bold;color:#FFFFFF;text-decoration:none;">{t(libelle)}&nbsp;&rarr;</a>
          <!--<![endif]-->
        </td></tr>
      </table>"""


def entete_section(numero, titre, sous_titre, ancre=""):
    return f"""    <tr><td id="{ancre}" class="pad carte" style="background-color:#FFFFFF;padding:36px 40px 8px 40px;border-top:6px solid #F5F3F1;{FONT}">
      <a name="{ancre}"></a><p style="margin:0 0 4px 0;font-size:13px;line-height:18px;font-weight:bold;color:#061866;" class="texte-doux">{numero}</p>
      <h2 class="titre texte-fonce" style="margin:0 0 6px 0;font-size:26px;line-height:32px;font-weight:bold;color:#061866;">{t(titre)}</h2>
      <p class="texte-doux" style="margin:0 0 20px 0;font-size:15px;line-height:22px;color:#53565A;">{t(sous_titre)}</p>
    </td></tr>"""


def bloc(contenu, bas=36):
    return f"""    <tr><td class="pad carte" style="background-color:#FFFFFF;padding:0 40px {bas}px 40px;{FONT}">
{contenu}
    </td></tr>"""


def sous_titre(texte, marge="22px 0 8px 0"):
    return (f'      <h4 class="texte-fonce" style="margin:{marge};{FONT}font-size:17px;line-height:24px;'
            f'font-weight:bold;color:#061866;">{t(texte)}</h4>')


def etiquette(texte):
    return (f'      <p style="margin:0 0 8px 0;{FONT}font-size:12px;line-height:16px;font-weight:bold;color:#53565A;" '
            f'class="texte-doux">{t(texte)}</p>')


def titre_article(texte):
    return (f'      <h3 class="texte-fonce" style="margin:0 0 12px 0;{FONT}font-size:21px;line-height:28px;'
            f'font-weight:bold;color:#000000;">{t(texte)}</h3>')


def chiffres(liste):
    cases = []
    for i, (valeur, legende) in enumerate(liste):
        marge = "padding:0 6px 0 0;" if i == 0 else "padding:0 0 0 6px;"
        cases.append(f"""          <td width="50%" valign="top" style="{marge}">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
              <td style="background-color:#061866;border-radius:12px;padding:16px 18px;{FONT}">
                <p style="margin:0;font-size:26px;line-height:30px;font-weight:bold;color:#FFFF1A;">{t(valeur)}</p>
                <p style="margin:4px 0 0 0;font-size:13px;line-height:18px;color:#FFFFFF;">{t(legende)}</p>
              </td>
            </tr></table>
          </td>""")
    return ('      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 18px 0;"><tr>\n'
            + "\n".join(cases) + "\n      </tr></table>")


def case_date(jours, mois, largeur=64):
    return f"""            <table role="presentation" width="{largeur}" cellpadding="0" cellspacing="0" border="0"><tr>
              <td align="center" style="background-color:#061866;border-radius:10px;padding:10px 4px;{FONT}color:#FFFFFF;">
                <span style="display:block;font-size:20px;line-height:22px;font-weight:bold;">{t(jours)}</span>
                <span style="display:block;font-size:12px;line-height:16px;">{t(mois)}</span>
              </td>
            </tr></table>"""


def section_evenements(e, langue):
    a = e["retour"]
    article = [etiquette(a["etiquette"]), titre_article(a["titre"])]
    article += [paragraphe(p) for p in a["intro"]]
    article.append(chiffres(a["chiffres"]))
    for st, paras in a["blocs"]:
        article.append(sous_titre(st, "4px 0 8px 0"))
        article += [paragraphe(p) for p in paras]
    article.append(paragraphe(a["conclusion"], 15).replace('color:#000000;">', 'color:#000000;font-style:italic;">', 1))
    article.append(bouton(a["bouton"], utm(LIENS["voltix"], e["campagne"], langue, "voltix"), "4px 0 8px 0"))

    r = e["rendez_vous"]
    rdv = f"""      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:10px 0 24px 0;">
        <tr><td class="bref" style="background-color:#F5F3F1;border-radius:12px;padding:22px 22px 8px 22px;{FONT}">
          <p style="margin:0 0 12px 0;font-size:12px;line-height:16px;font-weight:bold;color:#53565A;" class="texte-doux">{t(r['etiquette'])}</p>
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
            <td class="date-col" width="76" valign="top">
{case_date(r['jours'], r['mois'])}
            </td>
            <td valign="top" style="padding-left:12px;{FONT}">
              <p class="texte-fonce" style="margin:0;font-size:19px;line-height:26px;font-weight:bold;color:#000000;">{t(r['nom'])}</p>
              <p class="texte-doux" style="margin:0 0 10px 0;font-size:14px;line-height:20px;color:#53565A;">{t(r['lieu'])}</p>
            </td>
          </tr></table>
{chr(10).join(paragraphe(p, 15) for p in r['textes'])}
          <p style="margin:0 0 14px 0;font-size:14px;line-height:20px;">{lien_texte(r['lien'], escape(r['url']))}</p>
{bouton(r['bouton'], utm(LIENS["rdv"], e["campagne"], langue, "rencontres-filiere"), "0 0 16px 0")}
        </td></tr>
      </table>"""

    lignes = []
    for ev in e["agenda"]:
        lignes.append(f"""        <tr>
          <td width="88" valign="top" style="padding:0 0 12px 0;{FONT}font-size:14px;line-height:21px;font-weight:bold;color:#061866;" class="texte-fonce">{t(ev['date'])}</td>
          <td valign="top" class="texte-fonce" style="padding:0 0 12px 0;{FONT}font-size:14px;line-height:21px;color:#000000;"><a class="lien" href="{escape(ev['url'])}" target="_blank" style="color:#061866;font-weight:bold;">{t(ev['nom'])}</a> · {t(ev['lieu'])}</td>
        </tr>""")
    agenda = (sous_titre(e["titre_agenda"], "0 0 10px 0")
              + '\n      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">\n'
              + "\n".join(lignes) + "\n      </table>"
              + f'\n      <p class="texte-doux" style="margin:4px 0 0 0;{FONT}font-size:12px;line-height:18px;color:#53565A;">{t(e["note_evenements"])}</p>')
    return entete_section(*e["sections"][0], ancre="section-1") + "\n" + bloc("\n".join(article) + "\n" + rdv + "\n" + agenda)


def section_truckfly(e, langue):
    p = e["profil"]
    contenu = [etiquette(p["etiquette"]), titre_article(p["titre"])]
    contenu += [paragraphe(x) for x in p["intro"]]

    # Aperçu du fil d'activité, au style de l'app
    fil = []
    for nom, action, lieu, bouton_app in p["exemple_fil"]["lignes"]:
        detail = (f'<br><strong style="color:#061866;">{t(lieu)}</strong>' if lieu else "")
        badge = (f'<td align="right" valign="middle" style="padding-left:8px;"><span style="display:inline-block;background-color:#061866;color:#FFFFFF;border-radius:14px;padding:4px 12px;{FONT}font-size:12px;font-weight:bold;">{t(bouton_app)}</span></td>' if bouton_app else "")
        fil.append(f"""              <tr><td style="padding:10px 0;border-bottom:1px solid #E4E6EE;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
                  <td width="36" valign="middle"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" valign="middle" width="32" height="32" style="width:32px;height:32px;border-radius:16px;background-color:#DCE6F7;{FONT}font-size:13px;font-weight:bold;color:#061866;">{t(nom[0])}</td></tr></table></td>
                  <td valign="middle" style="padding-left:10px;{FONT}font-size:14px;line-height:20px;color:#000000;"><strong>{t(nom)}</strong> {t(action)}{detail}</td>
                  {badge}
                </tr></table>
              </td></tr>""")
    contenu.append(f"""      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 22px 0;">
        <tr><td style="background-color:#061866;border-radius:14px;padding:16px;">
          <p style="margin:0 0 10px 4px;{FONT}font-size:13px;line-height:18px;font-weight:bold;color:#FFFF1A;">{t(p['exemple_fil']['titre'])}</p>
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:#FFFFFF;border-radius:10px;padding:2px 14px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{chr(10).join(fil)}
            </table>
          </td></tr></table>
          <p style="margin:10px 0 0 4px;{FONT}font-size:11px;line-height:16px;color:#C9CEDF;">{t(p['exemple_fil']['legende'])}</p>
        </td></tr>
      </table>""")

    contenu.append(sous_titre(p["titre_fonctions"], "0 0 12px 0"))
    lignes = []
    for i, (titre, texte) in enumerate(p["fonctions"], 1):
        lignes.append(f"""        <tr>
          <td width="38" valign="top" style="padding:0 0 16px 0;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
              <td align="center" valign="middle" width="26" height="26" style="width:26px;height:26px;border-radius:13px;background-color:#061866;{FONT}font-size:13px;line-height:26px;font-weight:bold;color:#FFFFFF;">{i}</td>
            </tr></table>
          </td>
          <td class="texte-fonce" valign="top" style="padding:2px 0 10px 0;{FONT}font-size:15px;line-height:23px;color:#000000;"><strong>{t(titre)}</strong> {t(texte)}</td>
        </tr>""")
    contenu.append('      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 6px 0;">\n'
                   + "\n".join(lignes) + "\n      </table>")

    contenu.append(sous_titre(p["titre_pour_vous"], "4px 0 12px 0"))
    for public, texte in p["pour_vous"]:
        contenu.append(f"""      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 10px 0;">
        <tr><td class="bref" style="background-color:#F5F3F1;border-radius:12px;padding:16px 20px;{FONT}">
          <p class="texte-fonce" style="margin:0 0 4px 0;font-size:15px;line-height:22px;font-weight:bold;color:#061866;">{t(public)}</p>
          <p class="texte-fonce" style="margin:0;font-size:15px;line-height:23px;color:#000000;">{t(texte)}</p>
        </td></tr>
      </table>""")
    contenu.append(paragraphe(p["chiffre"], 15))
    contenu.append(bouton(p["bouton"], utm(LIENS["video"], e["campagne"], langue, "profil-video"), "6px 0 14px 0"))
    contenu.append(f'      <p style="margin:0;{FONT}font-size:15px;line-height:22px;">'
                   f'{lien_texte(p["lien"], utm(LIENS["app"], e["campagne"], langue, "profil-app"))}</p>')
    return entete_section(*e["sections"][1], ancre="section-2") + "\n" + bloc("\n".join(contenu))


def section_marche(e, langue):
    pays = PAYS_LECTEUR[langue]
    items = sorted(e["marche"], key=lambda m: (m["pays"] != "UE", m["pays"] != pays))
    cartes = []
    for m in items:
        corps = "<br><br>".join(t(p) for p in m["textes"])
        sources = " · ".join(lien_texte(nom, escape(url)) for nom, url in m["sources"])
        cartes.append(f"""      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 14px 0;">
        <tr><td class="bref" style="background-color:#F5F3F1;border-radius:12px;padding:20px 22px;{FONT}">
          <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
            <td style="background-color:#061866;border-radius:6px;padding:3px 9px;{FONT}font-size:12px;line-height:16px;font-weight:bold;color:#FFFFFF;">{m['pays']}</td>
            <td class="texte-doux" style="padding-left:10px;{FONT}font-size:13px;line-height:16px;font-weight:bold;color:#53565A;">{t(m['nom_pays'])}</td>
          </tr></table>
          <p class="texte-fonce" style="margin:12px 0 8px 0;font-size:17px;line-height:24px;font-weight:bold;color:#000000;">{t(m['titre'])}</p>
          <p class="texte-fonce" style="margin:0 0 8px 0;font-size:15px;line-height:23px;color:#000000;">{corps}</p>
          <p style="margin:0;font-size:13px;line-height:18px;color:#53565A;" class="texte-doux">{t(e['libelle_source'])} : {sources}</p>
        </td></tr>
      </table>""")
    note = (f'      <p class="texte-doux" style="margin:6px 0 0 0;{FONT}font-size:12px;line-height:18px;color:#53565A;">{t(e["note_marche"])}</p>\n'
            + paragraphe(e["intro_bouton_marche"], 15).replace("margin:0 0 14px 0", "margin:22px 0 4px 0")
            + "\n" + bouton(e["bouton_marche"], utm(LIENS["linkedin"], e["campagne"], langue, "linkedin")))
    return entete_section(*e["sections"][2], ancre="section-3") + "\n" + bloc("\n".join(cartes) + "\n" + note)


def section_question(e, langue):
    q = e["question"]
    barres = []
    for libelle, pct in q["resultats"]:
        barres.append(f"""          <p style="margin:0 0 6px 0;{FONT}font-size:15px;line-height:22px;color:#FFFFFF;"><strong style="color:#FFFF1A;">{pct}&nbsp;%</strong>&nbsp;&nbsp;{t(libelle)}</p>
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 16px 0;"><tr>
            <td width="{pct}%" height="10" style="height:10px;background-color:#FFFF1A;border-radius:5px;font-size:0;line-height:0;">&nbsp;</td>
            <td width="{100 - pct}%" height="10" style="height:10px;background-color:#2A3A85;font-size:0;line-height:0;">&nbsp;</td>
          </tr></table>""")
    contenu = f"""      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr><td style="background-color:#061866;border-radius:12px;padding:24px 26px 10px 26px;{FONT}">
          <p style="margin:0 0 6px 0;font-size:13px;line-height:18px;font-weight:bold;color:#FFFF1A;">{t(q['label'])}</p>
          <p style="margin:0 0 20px 0;font-size:20px;line-height:28px;font-weight:bold;color:#FFFFFF;">{t(q['question'])}</p>
{chr(10).join(barres)}
        </td></tr>
      </table>
{sous_titre(q['titre_retenir'])}
{chr(10).join(paragraphe(p) for p in q['retenir'])}
{paragraphe(q['prochaine'], 15)}
{bouton(q['bouton'], utm(LIENS["sondage"], e["campagne"], langue, "sondage"), "0 0 0 0")}"""
    return entete_section(*e["sections"][3], ancre="section-4") + "\n" + bloc(contenu)


def recap(e):
    lignes = []
    for i, (num, texte) in enumerate(zip(["I", "II", "III", "IV"], e["recap"])):
        lignes.append(f"""            <tr>
              <td width="34" valign="top" style="padding:0 0 12px 0;{FONT}font-size:14px;line-height:22px;font-weight:bold;color:#061866;" class="texte-fonce">{num}.</td>
              <td valign="top" class="texte-fonce" style="padding:0 0 12px 0;{FONT}font-size:15px;line-height:22px;color:#000000;"><a class="lien" href="#section-{i + 1}" style="color:#061866;font-weight:bold;text-decoration:underline;">{t(e['sections'][i][1])}</a> · {t(texte)}</td>
            </tr>""")
    return "\n".join(lignes)


EDITIONS = {
    ("b2b/2026-10", "fr"): dict(
        campagne="b2b-2026-10",
        objet="Voltix, Profil Trucker, gazole : l'actu d'octobre",
        preheader="Notre retour de Vierzon, la communauté Truckfly en détail, l'actu marché pays par pays et les résultats de notre sondage.",
        lien_navigateur="Voir dans le navigateur",
        edition="Newsletter pro · Octobre 2026",
        label_edito="L'édito du mois",
        titre_edito="Un secteur en mouvement, nous restons à vos côtés",
        edito=[
            "Bonjour,",
            "L'automne s'annonce chargé pour le transport routier. Prix du gazole, nouvelles règles d'un pays à l'autre, électrification qui s'accélère : le secteur change vite, et vos conducteurs le vivent chaque jour sur la route.",
            "Chez Michelin Truckfly, notre rôle est de les accompagner au plus près, et de vous aider à y voir clair. Ce mois-ci encore, nous avons réuni pour vous l'essentiel : nos temps forts, nos nouveautés et l'actualité qui compte dans chaque pays.",
            "Bonne lecture,",
        ],
        signature_edito="[Prénom Nom], [fonction], Michelin Truckfly",
        titre_recap="Le récap du mois",
        recap=[
            "Retour sur l'inauguration Voltix à Vierzon, et rendez-vous le 22 octobre à Lyon.",
            "Le Profil Trucker côté communauté : amis, activité, recommandations.",
            "UE, France, Allemagne, Pays-Bas, Italie, Espagne : ce qui change ce mois-ci.",
            "Les résultats du sondage sur les 24 Heures Camions.",
        ],
        sections=[
            ("I.", "Événements", "Les prochains rendez-vous à ne pas manquer"),
            ("II.", "Infos Michelin Truckfly", "Nos actualités, nouveautés et temps forts"),
            ("III.", "Infos Marché/Légal", "Les évolutions et informations à connaître dans le secteur"),
            ("IV.", "La question des Truckers", "Une question, une réponse et les conseils de notre communauté"),
        ],
        retour=dict(
            etiquette="Retour sur · Vierzon, 2 octobre 2026",
            titre="Une première station Voltix inaugurée à Vierzon : Michelin Truckfly au rendez-vous !",
            intro=[
                "Une nouvelle étape pour l'électrification du transport routier : Voltix a inauguré à Vierzon sa première station de recharge dédiée aux poids lourds électriques.",
                "Les équipes Michelin Truckfly étaient présentes pour accompagner ce lancement et présenter le rôle de notre application auprès des conducteurs.",
            ],
            chiffres=[("80 % en 30 min", "de recharge, le temps d'une pause réglementaire"),
                      ("50 stations", "Voltix prévues d'ici 2028, intégrées dans Michelin Truckfly")],
            blocs=[
                ("Voltix, c'est quoi ?", [
                    "Filiale de VINCI Concessions, Voltix développe un réseau de stations de recharge conçu pour les camions électriques. La station de Vierzon permet notamment de recharger jusqu'à 80 % de la batterie en 30 minutes, soit le temps d'une pause réglementaire.",
                ]),
                ("50 stations Voltix intégrées dans Michelin Truckfly", [
                    "À mesure du déploiement du réseau, les 50 stations Voltix prévues d'ici 2028 seront intégrées dans Michelin Truckfly, afin que les conducteurs puissent facilement les identifier et les retrouver lors de leurs trajets.",
                    "Cette collaboration avec VINCI Autoroutes illustre une ambition commune : accompagner les évolutions du transport routier et les professionnels qui les vivent au quotidien.",
                ]),
            ],
            bouton="Voir les stations Voltix dans l'app",
            conclusion="GPS poids lourd, établissements adaptés, services communautaires, emploi et demain recharge électrique : Michelin Truckfly continue d'accompagner les transformations du transport routier, au plus près des conducteurs.",
        ),
        rendez_vous=dict(
            etiquette="On y sera",
            jours="22", mois="oct.",
            nom="Les Rencontres de la Filière 2026",
            lieu="Lyon, Matmut Stadium de Gerland · France",
            textes=[
                "Organisée par la Fédération française de carrosserie avant Solutrans 2027, cette journée fait le point sur les grands enjeux du véhicule industriel et urbain.",
                "Au programme, des tables rondes avec des professionnels, des experts et des représentants européens, notamment sur le financement de la transition énergétique et le reconditionnement des véhicules industriels.",
                "Les équipes Michelin Truckfly y assisteront. Vous y serez aussi ? Prenons rendez-vous sur place.",
            ],
            lien="Programme et inscription",
            bouton="Rencontrer notre équipe à Lyon",
            url="https://www.solutrans.fr/en/solutrans-show/industry-meeting",
        ),
        titre_agenda="À l'agenda",
        agenda=[
            dict(date="3-5 nov.", nom="TransLogistica Poland", lieu="Varsovie", url="https://translogistica.pl"),
            dict(date="4-5 nov.", nom="Expertrans", lieu="Chartres", url="https://www.salon-expertrans.fr"),
            dict(date="11-12 nov.", nom="Logistics & Automation", lieu="Madrid", url="https://www.esmadrid.com/agenda/logistics-automation-madrid-ifema-madrid"),
            dict(date="18-19 nov.", nom="RTX Scotland (Road Transport Expo)", lieu="Glasgow", url="https://roadtransportexpo.co.uk"),
            dict(date="1-2 déc.", nom="Supply Chain Event", lieu="Paris", url="https://parisjetaime.com/convention/evenement/supply-chain-e591"),
        ],
        note_evenements="Dates communiquées par les organisateurs, à vérifier sur leur site avant de vous déplacer.",
        profil=dict(
            etiquette="Zoom communauté",
            titre="Profil Trucker : vos conducteurs ne roulent plus seuls",
            intro=[
                "Le mois dernier, nous vous présentions le Profil Trucker : un profil personnalisé, des avis sur les établissements, des arrêts favoris et les profils des autres conducteurs.",
                "Ce mois-ci, place à ce qui en fait le cœur : la communauté. Avec ses fonctions sociales, Michelin Truckfly devient un vrai réseau entre conducteurs. Même seuls dans leur cabine, ils restent connectés à leurs collègues.",
            ],
            exemple_fil=dict(
                titre="Dans l'app : le fil d'activité des amis",
                lignes=[
                    ("Louna", "t'a envoyé une invitation", "", "Accepter"),
                    ("Nicolas J.", "a visité :", "AS 24", ""),
                    ("David", "s'est arrêté ici :", "Le Relais des Cigales", ""),
                ],
                legende="Exemple d'écran, noms fictifs.",
            ),
            titre_fonctions="Comment ça marche",
            fonctions=[
                ("Ajouter ses amis", "et accepter leurs invitations en un geste."),
                ("Voir où ils s'arrêtent", "au fil de la journée : station, relais, parking."),
                ("Profiter de leurs recommandations,", "mises en avant dans l'app."),
            ],
            titre_pour_vous="Ce que ça vous apporte",
            pour_vous=[
                ("Transporteurs et gestionnaires de flotte", "Des conducteurs moins isolés, qui s'entraident et partagent les bons plans de la route : parkings, douches, restaurants. Un outil gratuit qui crée du lien entre vos équipes."),
                ("Établissements", "Le bouche-à-oreille des routiers passe désormais par l'app. Chaque visite et chaque avis peut être vu par les amis du conducteur : une recommandation vaut toutes les publicités."),
                ("Partenaires et marques", "Une communauté engagée, qui revient dans l'app chaque jour. Vos messages touchent les conducteurs là où ils sont : sur la route."),
            ],
            chiffre="[Chiffre clé à ajouter : profils créés, amis ajoutés, avis déposés depuis le lancement…]",
            bouton="Voir le Profil Trucker en vidéo",
            lien="Faire découvrir l'app à vos conducteurs",
        ),
        libelle_source="Sources",
        intro_bouton_marche="Chaque semaine, nous partageons l'essentiel de l'actu transport sur LinkedIn.",
        bouton_marche="Suivre Michelin Truckfly sur LinkedIn",
        note_marche="Informations vérifiées au 8 octobre 2026. Les mesures en discussion peuvent encore évoluer. Elles ne remplacent pas les textes officiels.",
        marche=[
            dict(pays="UE", nom_pays="Union européenne", titre="Eurovignette : jusqu'à -75 % de péage pour les camions à faibles émissions",
                 textes=["Le Parlement européen a voté le 7 octobre la révision de la directive Eurovignette. Elle renforce les réductions de péage pour les poids lourds les moins émetteurs de CO2, jusqu'à 75 %.",
                         "Le Conseil doit encore l'adopter formellement avant son entrée en vigueur."],
                 sources=[("TRM24", "https://www.trm24.fr/parlement-europeen-des-reductions-allant-jusqua-75-des-peages-routiers-pour-les-camions-a-faibles-emissions/")]),
            dict(pays="FR", nom_pays="France", titre="Budget 2027 déposé, mobilisation le 21 octobre",
                 textes=["Le projet de loi de finances 2027 a été déposé le 1er octobre. Il prévoit de revoir le suramortissement pour les camions électriques et de réduire les avantages des camions gaz et B100. Il propose aussi d'augmenter la taxe sur les concessions d'autoroutes les plus rentables.",
                         "Face au prix du gazole, l'OTRE et la FAI appellent les transporteurs à se mobiliser à Paris à partir du 21 octobre.",
                         "Rappel : Loi Montagne dès le 1er novembre, et interdiction de circuler pour les plus de 7,5 t du 10 novembre 22 h au 11 novembre 22 h."],
                 sources=[("Ministère de la Transition écologique", "https://www.ecologie.gouv.fr/presse/plf-2027-teitld-gouvernement-propose-contribution-plus-elevee-exploitants-plus-rentables"),
                          ("OTRE", "https://otre.org/carburants-les-transporteurs-routiers-se-mobiliseront-le-21-octobre-2026-et-suivants")]),
            dict(pays="DE", nom_pays="Allemagne", titre="Gazole : -16,7 centimes par litre jusqu'au 31 décembre",
                 textes=["Depuis le 1er octobre et jusqu'au 31 décembre 2026, la taxe sur l'énergie baisse de 14,04 centimes par litre de gazole, soit jusqu'à 16,7 centimes TTC. La profession juge la mesure insuffisante.",
                         "Le ministère des Transports annonce aussi 100 millions d'euros pour les aires de repos fédérales et de nouvelles places de stationnement poids lourds."],
                 sources=[("VerkehrsRundschau (gazole)", "https://www.verkehrsrundschau.de/nachrichten/transport-logistik/tankrabatt-2026-beschlossen-bis-zu-17-cent-weniger-pro-liter-3909527"),
                          ("VerkehrsRundschau (aires de repos)", "https://www.verkehrsrundschau.de/nachrichten/recht-geld/verkehrsministerium-verspricht-entlastungen-fuer-logistik-3912142")]),
            dict(pays="NL", nom_pays="Pays-Bas", titre="Péage et accises gazole en baisse",
                 textes=["Jusqu'au 31 décembre 2026, le péage poids lourds baisse de 22,3 % (0,148 € au lieu de 0,191 € par km en moyenne), et la taxe de circulation des camions est à zéro.",
                         "Le plan fiscal 2027, présenté le 15 septembre, propose de prolonger la baisse des accises sur le gazole jusqu'au 31 décembre 2027. Le texte doit encore être voté."],
                 sources=[("Taxlive", "https://www.taxlive.nl/nl/documenten/nieuws/tijdelijke-korting-op-vrachtwagenheffing/"),
                          ("Nationale Transportgids", "https://www.nationaletransportgids.nl/wegtransport/prinsjesdag-2026-dit-betekent-het-kabinetsbeleid-voor-de-transportsector/")]),
            dict(pays="IT", nom_pays="Italie", titre="Budget 2027 : le transport demande moins de taxes sur le gazole",
                 textes=["Le projet de budget 2027 est attendu autour du 20 octobre. Unatras réclame moins de taxes sur le gazole, qui pèse 35 % des coûts d'une entreprise de transport. Le gouvernement évoque des aides ciblées.",
                         "Déjà en place : le crédit d'impôt gazole a été élargi début octobre. Et à partir du 15 novembre, pneus hiver ou chaînes à bord sur les routes signalées."],
                 sources=[("ItaliaOggi", "https://www.italiaoggi.it/economia-e-politica/autotrasporto-ugge-fai-e-unatras-nella-finanziaria-meno-tasse-sul-gasolio-e-piu-aiuti-alle-imprese-b26mvz8a"),
                          ("Il Sole 24 Ore", "https://ntplusfisco.ilsole24ore.com/art/AJKF9UWB")]),
            dict(pays="ES", nom_pays="Espagne", titre="Aides au gazole prolongées jusqu'au 31 décembre",
                 textes=["Le décret-loi 25/2026, en vigueur depuis le 1er octobre, prolonge les aides au transport jusqu'à la fin de l'année. La baisse de la taxe sur les hydrocarbures atteint 20 centimes par litre en octobre, puis 13 en novembre et 6 en décembre.",
                         "Avec la carte gazole professionnel, une aide en plus de 5, 12 puis 19 centimes par litre. Pour les véhicules sans gazole professionnel, l'aide par véhicule est à demander avant le 30 octobre."],
                 sources=[("Transporte 3", "https://transporte3.com/noticia/24555-ayudas-al-gasoleo-para-transportistas-asi-funcionaran-hasta-diciembre-de-2026/"),
                          ("Ruta del Transporte", "https://www.rutadeltransporte.com/noticias-transporte/los-transportistas-con-vehiculos-sin-gasoleo-profesional-pueden-pedir-la-segunda-tanda-de-ayudas-hasta-el-30-de-octubre.html")]),
        ],
        question=dict(
            label="Les résultats de notre dernier sondage",
            question="Qu'est-ce qui compte le plus pour vous lors d'un événement comme les 24 Heures Camions du Mans ?",
            resultats=[("Profiter du spectacle et des courses", 40),
                       ("Partager autour de la passion du camion", 38),
                       ("Découvrir les nouveautés du secteur", 21)],
            titre_retenir="Ce qu'on en retient",
            retenir=[
                "Profiter du spectacle et des courses arrive en tête avec 40 % des votes. Partager autour de la passion du camion suit de près avec 38 % des réponses. Enfin, découvrir les nouveautés du secteur représente 21 % des votes.",
                "Pour les routiers, un événement camion est d'abord un moment de passion et de partage. Pour les marques et les exposants, l'expérience et la rencontre comptent autant que la vitrine produit.",
            ],
            prochaine="Ce mois-ci, à vous de jouer : [question du prochain sondage].",
            bouton="Je donne mon avis",
        ),
        cta_intro="Vous voulez apparaître sur la carte des routiers ?",
        cta="Découvrir Michelin Truckfly",
        raison="Vous recevez cet e-mail en tant que partenaire ou client professionnel de Michelin Truckfly.",
        desinscription="Se désinscrire",
    ),
}


def main():
    for (dossier, langue), e in EDITIONS.items():
        sections = "\n".join([
            section_evenements(e, langue), section_truckfly(e, langue),
            section_marche(e, langue), section_question(e, langue),
        ])
        html = GABARIT.substitute(
            lang=langue, assets=ASSETS, adresse=t(ADRESSE),
            objet=escape(e["objet"], quote=False), preheader=escape(e["preheader"], quote=False),
            lien_navigateur=t(e["lien_navigateur"]), edition=t(e["edition"]),
            label_edito=t(e["label_edito"]), titre_edito=t(e["titre_edito"]),
            edito="\n".join(paragraphe(p) for p in e["edito"]),
            signature_edito=t(e["signature_edito"]),
            titre_recap=t(e["titre_recap"]), recap=recap(e), sections=sections,
            cta_intro=t(e["cta_intro"]), cta=t(e["cta"]),
            lien_cta=utm(LIEN_B2B, e["campagne"], langue, "cta"),
            lien_logo=utm(LIEN_B2B, e["campagne"], langue, "logo"),
            raison=t(e["raison"]), desinscription=t(e["desinscription"]),
        )
        sortie = RACINE / dossier / f"{langue}.html"
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text(html, encoding="utf-8")
        print(f"{sortie.relative_to(RACINE)}  objet : {len(e['objet'])} car.")


if __name__ == "__main__":
    main()
