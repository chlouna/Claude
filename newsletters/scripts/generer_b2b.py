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
LIEN_B2B = "https://LIEN-B2B-A-REMPLACER"
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
    if "LIEN-" not in url:  # sources externes : pas d'UTM
        return escape(url)
    return (f"{url}?utm_source=brevo&amp;utm_medium=email"
            f"&amp;utm_campaign={campagne}-{langue}&amp;utm_content={contenu}")


def paragraphe(texte, taille=16):
    return (f'      <p class="texte-fonce" style="margin:0 0 14px 0;{FONT}font-size:{taille}px;'
            f'line-height:{round(taille * 1.55)}px;color:#000000;">{t(texte)}</p>')


def lien_texte(libelle, href):
    return (f'<a class="lien" href="{href}" target="_blank" style="color:#061866;font-weight:bold;'
            f'text-decoration:underline;">{t(libelle)}&nbsp;&rarr;</a>')


def entete_section(numero, titre, sous_titre):
    return f"""    <tr><td class="pad carte" style="background-color:#FFFFFF;padding:36px 40px 8px 40px;border-top:6px solid #F5F3F1;{FONT}">
      <p style="margin:0 0 4px 0;font-size:13px;line-height:18px;font-weight:bold;color:#061866;" class="texte-doux">{numero}</p>
      <h2 class="titre texte-fonce" style="margin:0 0 6px 0;font-size:26px;line-height:32px;font-weight:bold;color:#061866;">{t(titre)}</h2>
      <p class="texte-doux" style="margin:0 0 20px 0;font-size:15px;line-height:22px;color:#53565A;">{t(sous_titre)}</p>
    </td></tr>"""


def bloc(contenu, bas=36):
    return f"""    <tr><td class="pad carte" style="background-color:#FFFFFF;padding:0 40px {bas}px 40px;{FONT}">
{contenu}
    </td></tr>"""


def section_evenements(e, langue):
    lignes = []
    for ev in e["evenements"]:
        lignes.append(f"""        <tr>
          <td class="date-col" width="76" valign="top" style="padding:0 0 18px 0;">
            <table role="presentation" width="64" cellpadding="0" cellspacing="0" border="0"><tr>
              <td align="center" style="background-color:#061866;border-radius:10px;padding:10px 4px;{FONT}color:#FFFFFF;">
                <span style="display:block;font-size:20px;line-height:22px;font-weight:bold;">{t(ev['jours'])}</span>
                <span style="display:block;font-size:12px;line-height:16px;">{t(ev['mois'])}</span>
              </td>
            </tr></table>
          </td>
          <td valign="top" style="padding:0 0 18px 12px;{FONT}">
            <p class="texte-fonce" style="margin:0;font-size:17px;line-height:24px;font-weight:bold;color:#000000;">{t(ev['nom'])}</p>
            <p class="texte-doux" style="margin:0 0 4px 0;font-size:14px;line-height:20px;color:#53565A;">{t(ev['lieu'])}</p>
            <p class="texte-fonce" style="margin:0 0 4px 0;font-size:15px;line-height:22px;color:#000000;">{t(ev['texte'])}</p>
            <p style="margin:0;font-size:14px;line-height:20px;">{lien_texte(e['libelle_site'], escape(ev['url']))}</p>
          </td>
        </tr>""")
    tableau = ('      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">\n'
               + "\n".join(lignes) + "\n      </table>")
    note = f'      <p class="texte-doux" style="margin:0;{FONT}font-size:12px;line-height:18px;color:#53565A;">{t(e["note_evenements"])}</p>'
    return entete_section(*e["sections"][0]) + "\n" + bloc(tableau + "\n" + note)


def section_truckfly(e, langue):
    parts = []
    for i, a in enumerate(e["truckfly"]):
        corps = "\n".join(paragraphe(p) for p in a["paragraphes"])
        lien = (f'      <p style="margin:0 0 24px 0;{FONT}font-size:15px;line-height:22px;">'
                f'{lien_texte(a["lien"], utm(LIEN_B2B, e["campagne"], langue, f"truckfly-{i + 1}"))}</p>') if a.get("lien") else ""
        parts.append(f'      <h3 class="texte-fonce" style="margin:0 0 10px 0;{FONT}font-size:19px;line-height:26px;font-weight:bold;color:#000000;">{t(a["titre"])}</h3>\n{corps}\n{lien}')
    return entete_section(*e["sections"][1]) + "\n" + bloc("\n".join(parts), bas=16)


def section_marche(e, langue):
    pays = PAYS_LECTEUR[langue]
    items = sorted(e["marche"], key=lambda m: (m["pays"] != "UE", m["pays"] != pays))
    cartes = []
    for m in items:
        corps = "<br><br>".join(t(p) for p in m["textes"])
        cartes.append(f"""      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 14px 0;">
        <tr><td class="bref" style="background-color:#F5F3F1;border-radius:12px;padding:20px 22px;{FONT}">
          <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
            <td style="background-color:#061866;border-radius:6px;padding:3px 9px;{FONT}font-size:12px;line-height:16px;font-weight:bold;color:#FFFFFF;">{m['pays']}</td>
            <td class="texte-doux" style="padding-left:10px;{FONT}font-size:13px;line-height:16px;font-weight:bold;color:#53565A;">{t(m['nom_pays'])}</td>
          </tr></table>
          <p class="texte-fonce" style="margin:12px 0 8px 0;font-size:17px;line-height:24px;font-weight:bold;color:#000000;">{t(m['titre'])}</p>
          <p class="texte-fonce" style="margin:0 0 8px 0;font-size:15px;line-height:23px;color:#000000;">{corps}</p>
          <p style="margin:0;font-size:13px;line-height:18px;">{lien_texte(e['libelle_source'] + ' : ' + m['source'], escape(m['url']))}</p>
        </td></tr>
      </table>""")
    note = f'      <p class="texte-doux" style="margin:6px 0 0 0;{FONT}font-size:12px;line-height:18px;color:#53565A;">{t(e["note_marche"])}</p>'
    return entete_section(*e["sections"][2]) + "\n" + bloc("\n".join(cartes) + "\n" + note)


def section_question(e, langue):
    q = e["question"]
    conseils = "\n".join(
        f'        <tr><td class="texte-fonce" style="padding:0 0 12px 0;border-left:3px solid #061866;padding-left:14px;{FONT}font-size:15px;line-height:23px;color:#000000;">{t(c)}</td></tr>'
        for c in q["conseils"])
    contenu = f"""      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr><td style="background-color:#061866;border-radius:12px;padding:24px 26px;{FONT}">
          <p style="margin:0 0 6px 0;font-size:13px;line-height:18px;font-weight:bold;color:#FFFF1A;">{t(q['label'])}</p>
          <p style="margin:0;font-size:20px;line-height:28px;font-weight:bold;color:#FFFFFF;">{t(q['question'])}</p>
          <p style="margin:10px 0 0 0;font-size:13px;line-height:18px;color:#FFFFFF;">{t(q['auteur'])}</p>
        </td></tr>
      </table>
      <p class="texte-fonce" style="margin:22px 0 6px 0;{FONT}font-size:17px;line-height:24px;font-weight:bold;color:#061866;">{t(q['titre_reponse'])}</p>
{chr(10).join(paragraphe(p) for p in q['reponse'])}
      <p class="texte-fonce" style="margin:8px 0 12px 0;{FONT}font-size:17px;line-height:24px;font-weight:bold;color:#061866;">{t(q['titre_conseils'])}</p>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{conseils}
      </table>
{paragraphe(q['pour_vous'], 15)}"""
    return entete_section(*e["sections"][3]) + "\n" + bloc(contenu)


def recap(e):
    lignes = []
    for i, (num, texte) in enumerate(zip(["I", "II", "III", "IV"], e["recap"])):
        lignes.append(f"""            <tr>
              <td width="34" valign="top" style="padding:0 0 12px 0;{FONT}font-size:14px;line-height:22px;font-weight:bold;color:#061866;" class="texte-fonce">{num}.</td>
              <td valign="top" class="texte-fonce" style="padding:0 0 12px 0;{FONT}font-size:15px;line-height:22px;color:#000000;"><strong>{t(e['sections'][i][1])}</strong> · {t(texte)}</td>
            </tr>""")
    return "\n".join(lignes)


EDITIONS = {
    ("b2b/2026-10", "fr"): dict(
        campagne="b2b-2026-10",
        objet="Gazole, péages, hiver : ce qui change en Europe",
        preheader="Le récap d'octobre : salons de novembre, Profil Trucker, infos marché pays par pays et la question des truckers.",
        lien_navigateur="Voir dans le navigateur",
        edition="Newsletter pro · Octobre 2026",
        label_edito="L'édito du mois",
        titre_edito="Un automne sous pression, une communauté qui s'organise",
        edito=[
            "Le prix du gazole pèse sur les entreprises de transport. Plusieurs pays réagissent : les Pays-Bas baissent leur péage poids lourds jusqu'à la fin de l'année, l'Italie élargit son crédit d'impôt gazole, l'Espagne impose la clause de révision du prix.",
            "En parallèle, l'hiver arrive. Équipements obligatoires en montagne, nuits plus longues, parkings saturés plus tôt : les conducteurs le sentent dès maintenant.",
            "Chez Michelin Truckfly, nous lançons le Profil Trucker. Les conducteurs se retrouvent, se recommandent les bons arrêts et partagent leur route. Une communauté plus visible, et donc des lieux mieux connus.",
            "Bonne lecture.",
        ],
        signature_edito="[Prénom Nom], [fonction], Michelin Truckfly",
        titre_recap="Le récap du mois",
        recap=[
            "4 salons à noter en novembre et décembre.",
            "Lancement du Profil Trucker et des fonctions communautaires.",
            "Péages, gazole, hiver : 7 points à connaître, de l'UE à la Pologne.",
            "Parkings pleins dès 17 h : comment les conducteurs s'organisent.",
        ],
        sections=[
            ("I.", "Événements", "Les prochains rendez-vous à ne pas manquer"),
            ("II.", "Infos Michelin Truckfly", "Nos actualités, nouveautés et temps forts"),
            ("III.", "Infos Marché/Légal", "Les évolutions et informations à connaître dans le secteur"),
            ("IV.", "La question des Truckers", "Une question, une réponse et les conseils de notre communauté"),
        ],
        libelle_site="Infos et inscription",
        note_evenements="Dates communiquées par les organisateurs, à vérifier sur leur site avant de vous déplacer.",
        evenements=[
            dict(jours="3-5", mois="nov.", nom="TransLogistica Poland", lieu="Varsovie, EXPO XXI · Pologne",
                 texte="Le grand salon polonais du transport routier, de la logistique et de la gestion de flotte. Environ 500 exposants attendus.",
                 url="https://translogistica.pl"),
            dict(jours="4-5", mois="nov.", nom="Expertrans", lieu="Chartres, Parc des expositions Illiade · France",
                 texte="2e édition du salon régional du transport : poids lourds, utilitaires et logistique.",
                 url="https://www.salon-expertrans.fr"),
            dict(jours="11-12", mois="nov.", nom="Logistics & Automation Madrid", lieu="Madrid, IFEMA · Espagne",
                 texte="Transport, entreposage et automatisation de la supply chain.",
                 url="https://www.esmadrid.com/agenda/logistics-automation-madrid-ifema-madrid"),
            dict(jours="1-2", mois="déc.", nom="Supply Chain Event", lieu="Paris, Porte de Versailles · France",
                 texte="Le rendez-vous des décideurs supply chain et transport.",
                 url="https://parisjetaime.com/convention/evenement/supply-chain-e591"),
        ],
        truckfly=[
            dict(titre="Le Profil Trucker est en ligne",
                 paragraphes=[
                     "Chaque conducteur peut désormais créer son profil dans l'app : photo, bio et camion avec ses dimensions.",
                     "Il ajoute ses amis, voit leurs arrêts et leurs recommandations au fil de la journée. Les bons lieux circulent plus vite, de conducteur à conducteur.",
                     "Pour les établissements partenaires, c'est plus de visibilité auprès des routiers qui passent près de chez eux. [Chiffre clé à ajouter : profils créés, avis déposés…]",
                 ],
                 lien="Voir la présentation du Profil Trucker"),
            dict(titre="[Deuxième actu : nouveau partenaire, chiffre du mois, événement Truckfly…]",
                 paragraphes=["[2 ou 3 phrases courtes. Supprimer ce bloc s'il n'y a pas de deuxième actu.]"]),
        ],
        libelle_source="Source",
        note_marche="Informations vérifiées au 8 octobre 2026. Elles ne remplacent pas les textes officiels.",
        marche=[
            dict(pays="UE", nom_pays="Union européenne", titre="Utilitaires : le tachygraphe intelligent est obligatoire à l'international",
                 textes=["Depuis le 1er juillet 2026, les véhicules de 2,5 à 3,5 t qui font du transport international de marchandises doivent avoir un tachygraphe intelligent de 2e génération.",
                         "Les règles de temps de conduite et de repos s'appliquent aussi. Le transport national n'est pas concerné."],
                 source="trans.info", url="https://trans.info/en/f-tachograph-free-van-447001"),
            dict(pays="FR", nom_pays="France", titre="Loi Montagne : équipements d'hiver dès le 1er novembre",
                 textes=["Du 1er novembre au 31 mars, dans les communes listées par arrêté préfectoral. Poids lourd seul : chaînes ou pneus hiver 3PMSF. Avec remorque ou semi-remorque : chaînes pour au moins deux roues motrices, même avec des pneus hiver.",
                         "À noter aussi : interdiction de circuler pour les plus de 7,5 t du mardi 10 novembre à 22 h au mercredi 11 novembre à 22 h."],
                 source="Préfecture du Jura", url="https://www.jura.gouv.fr/contenu/telechargement/28038/217809/file/20231031_CP_Obligation%20%C3%A9quipements%20sp%C3%A9ciaux.pdf"),
            dict(pays="DE", nom_pays="Allemagne", titre="Maut : nouvelles classes CO2 pour les plus de 16 t",
                 textes=["Depuis le 1er juillet 2026, le classement des camions de plus de 16 t dans les classes d'émission CO2 a changé, ce qui modifie le tarif de nombreux véhicules.",
                         "Les camions à zéro émission restent exonérés de péage jusqu'au 30 juin 2031."],
                 source="Toll Collect", url="https://www.toll-collect.de/en/toll_collect/rund_um_die_maut/meldungen/meldungen.html"),
            dict(pays="NL", nom_pays="Pays-Bas", titre="Péage poids lourds : -22,3 % jusqu'au 31 décembre",
                 textes=["Depuis le 1er juillet 2026, un péage au kilomètre (vrachtwagenheffing) remplace l'Eurovignette pour les plus de 3,5 t. Un boîtier embarqué est obligatoire.",
                         "Face à la hausse du gazole, le tarif baisse de 22,3 % du 1er septembre au 31 décembre 2026 : de 0,191 € à 0,148 € par km en moyenne. Retour aux tarifs normaux le 1er janvier 2027."],
                 source="Taxlive (Rijksoverheid)", url="https://www.taxlive.nl/nl/documenten/nieuws/tijdelijke-korting-op-vrachtwagenheffing/"),
            dict(pays="IT", nom_pays="Italie", titre="Crédit d'impôt gazole élargi et obligation hiver au 15 novembre",
                 textes=["Un décret d'octobre élargit le crédit d'impôt « caro gasolio » : il concerne les véhicules de 7,5 t et plus, hors Euro IV et inférieurs.",
                         "Du 15 novembre au 15 avril : pneus hiver ou chaînes à bord sur les routes signalées par l'exploitant."],
                 source="Il Sole 24 Ore", url="https://ntplusfisco.ilsole24ore.com/art/AJKF9UWB"),
            dict(pays="ES", nom_pays="Espagne", titre="Révision du prix selon le gazole : désormais impérative",
                 textes=["Depuis le décret-loi 9/2026 (en vigueur le 16 avril 2026), la clause de révision du prix du transport selon le gazole s'impose dès que le carburant varie de 5 %.",
                         "L'ajustement doit apparaître à part sur la facture."],
                 source="Penningtons Manches Cooper", url="https://www.penningtonslaw.com/insights/novedades-en-la-revision-del-precio-del-transporte-por-carretera-impacto-de-los-rdl-7-2026-y-9-2026/"),
            dict(pays="PL", nom_pays="Pologne", titre="e-TOLL : des tarifs en hausse de 40 % depuis février",
                 textes=["Après l'indexation de janvier, les tarifs e-TOLL des plus de 3,5 t ont augmenté de 40 à 42 % en février 2026 : de 0,34 à 1,07 PLN par km selon le véhicule et la route.",
                         "Les amendes vont de 250 à 1 500 PLN."],
                 source="trans.info", url="https://trans.info/en/poland-truck-toll-rise-446623"),
        ],
        question=dict(
            label="La question du mois",
            question="« En hiver, les parkings sont pleins dès 17 h. Comment être sûr de trouver une place ? »",
            auteur="[Prénom, conducteur depuis X ans, pays]",
            titre_reponse="Notre réponse",
            reponse=[
                "Depuis le passage à l'heure d'hiver, la nuit tombe plus tôt et tout le monde cherche une place en même temps.",
                "La clé : choisir son arrêt du soir dès la pause de midi, vérifier les avis récents sur la carte Truckfly et garder un plan B à 30 minutes de route.",
            ],
            titre_conseils="Les conseils de la communauté",
            conseils=[
                "« [Conseil d'un trucker de la communauté, avec son accord] »",
                "« [Deuxième conseil] »",
                "« [Troisième conseil] »",
            ],
            pour_vous="Pour les chargeurs et les sites de livraison : un chargement qui finit tard peut coûter au conducteur sa place pour la nuit. Des créneaux plus tôt l'hiver, c'est un conducteur plus reposé le lendemain.",
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
