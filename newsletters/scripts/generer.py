"""Génère les newsletters HTML prêtes pour Brevo à partir de template/base.html.

Usage : python3 newsletters/scripts/generer.py
Le contenu de chaque édition est dans le dictionnaire EDITIONS ci-dessous.
"""
from pathlib import Path
from string import Template
from html import escape

RACINE = Path(__file__).resolve().parent.parent
GABARIT = Template((RACINE / "template" / "base.html").read_text(encoding="utf-8"))

# À remplacer avant l'envoi (voir LISEZMOI.md).
LIEN_APP = "https://LIEN-APP-A-REMPLACER"
ASSETS = "../../assets"  # remplacer par l'URL du dossier d'images dans Brevo
ADRESSE = "Michelin Truckfly · [adresse postale à compléter]"

FONT = "font-family:'Noto Sans',Arial,Helvetica,sans-serif;"


def lien(campagne, langue, contenu):
    sep = "&amp;" if "?" in LIEN_APP else "?"
    return (f"{LIEN_APP}{sep}utm_source=brevo&amp;utm_medium=email"
            f"&amp;utm_campaign={campagne}-{langue}&amp;utm_content={contenu}")


def points(liste):
    lignes = []
    for i, texte in enumerate(liste, 1):
        lignes.append(f"""        <tr>
          <td width="36" valign="top" style="padding:0 0 16px 0;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
              <td align="center" valign="middle" width="26" height="26" style="width:26px;height:26px;border-radius:13px;background-color:#061866;{FONT}font-size:13px;line-height:26px;font-weight:bold;color:#FFFFFF;">{i}</td>
            </tr></table>
          </td>
          <td class="texte-fonce" valign="top" style="padding:2px 0 16px 0;{FONT}font-size:17px;line-height:25px;color:#000000;">{escape(texte, quote=False)}</td>
        </tr>""")
    return "\n".join(lignes)


def brefs(liste):
    lignes = []
    for titre, texte in liste:
        lignes.append(f"""            <tr><td class="texte-fonce" style="padding:0 0 16px 0;border-left:3px solid #061866;padding-left:14px;{FONT}font-size:16px;line-height:24px;color:#000000;">
              <strong style="color:inherit;">{escape(titre, quote=False)}</strong><br>{escape(texte, quote=False)}
            </td></tr>""")
    return "\n".join(lignes)


EDITIONS = {
    # ---------- Newsletter Trucker · octobre 2026 ----------
    ("trucker/2026-10", "fr"): dict(
        campagne="trucker-2026-10",
        objet="Depuis dimanche, la nuit te rattrape",
        preheader="Une heure de jour en moins : nos astuces pour garer ton camion sans stress.",
        lien_navigateur="Voir dans le navigateur",
        surtitre="Depuis dimanche, on est à l'heure d'hiver",
        chiffre="−1\u00a0h",
        accroche="de jour en fin de journée. La nuit tombe maintenant vers 17\u00a0h\u00a030.",
        salutation='Salut {{ contact.PRENOM | default : "la route" }},',
        titre="Trouve ta place avant la cohue",
        points=[
            "Moins de jour, c'est plus de camions qui cherchent une place à la même heure.",
            "Choisis ton arrêt du soir dès la pause de midi.",
            "Sur la carte Truckfly, filtre les parkings et lis les avis les plus récents.",
            "Garde toujours un plan B à 30 minutes de route.",
            "Une fois garé, laisse un avis. Le collègue de demain te dira merci.",
        ],
        titre_bref="En bref",
        brefs=[
            ("Ton Profil Trucker t'attend",
             "Photo, bio et ton camion avec ses dimensions. Plus il est complet, plus tes amis te retrouvent."),
            ("Roule avec tes amis",
             "Ajoute-les dans l'app et vois leurs recommandations et leurs arrêts au fil de la journée."),
            ("Loi Montagne dès le 1er novembre",
             "Chaînes ou pneus hiver obligatoires dans les zones de montagne signalées. Vérifie ton équipement avant de partir."),
        ],
        cta_intro="Ce soir, tu dors où\u202f?",
        cta="Trouver mon spot",
        signature="Bonne route,<br><strong>L'équipe Michelin Truckfly</strong>",
        raison="Tu reçois cet e-mail parce que tu utilises l'application Michelin Truckfly.",
        desinscription="Se désinscrire",
    ),
    ("trucker/2026-10", "it"): dict(
        campagne="trucker-2026-10",
        objet="Da domenica il buio arriva prima",
        preheader="Un'ora di luce in meno: i nostri consigli per parcheggiare il camion senza stress.",
        lien_navigateur="Visualizza nel browser",
        surtitre="Da domenica siamo tornati all'ora solare",
        chiffre="−1\u00a0h",
        accroche="di luce a fine giornata. Ora il sole tramonta verso le 17.",
        salutation='Ciao {{ contact.PRENOM | default : "camionista" }},',
        titre="Trova il tuo posto prima della ressa",
        points=[
            "Meno luce vuol dire più camion che cercano posto alla stessa ora.",
            "Scegli la sosta della sera già alla pausa pranzo.",
            "Sulla mappa di Truckfly, filtra i parcheggi e leggi le recensioni più recenti.",
            "Tieni sempre un piano B a 30 minuti di strada.",
            "Una volta parcheggiato, lascia una recensione. Il collega di domani ti ringrazierà.",
        ],
        titre_bref="In breve",
        brefs=[
            ("Il tuo Profilo Trucker ti aspetta",
             "Foto, bio e il tuo camion con le sue misure. Più è completo, più i tuoi amici ti trovano."),
            ("Viaggia con i tuoi amici",
             "Aggiungili nell'app e scopri i loro consigli e le loro soste durante la giornata."),
            ("Dal 15 novembre, obbligo invernale",
             "Pneumatici invernali o catene a bordo sulle strade segnalate. Controlla l'attrezzatura prima di partire."),
        ],
        cta_intro="Stasera dove dormi?",
        cta="Trova il mio posto",
        signature="Buona strada,<br><strong>Il team Michelin Truckfly</strong>",
        raison="Ricevi questa email perché utilizzi l'app Michelin Truckfly.",
        desinscription="Annulla l'iscrizione",
    ),
}


def main():
    for (dossier, langue), e in EDITIONS.items():
        champs = {k: v for k, v in e.items() if k not in ("points", "brefs", "campagne")}
        # Textes simples échappés ; signature, salutation (balise Brevo) et chiffre gardés tels quels.
        for k in ("objet", "preheader", "lien_navigateur", "surtitre", "accroche",
                  "titre", "titre_bref", "cta_intro", "cta", "raison", "desinscription"):
            champs[k] = escape(champs[k], quote=False)
        html = GABARIT.substitute(
            champs,
            lang=langue,
            assets=ASSETS,
            adresse=escape(ADRESSE),
            points=points(e["points"]),
            brefs=brefs(e["brefs"]),
            lien_cta=lien(e["campagne"], langue, "cta"),
            lien_logo=lien(e["campagne"], langue, "logo"),
        )
        sortie = RACINE / dossier / f"{langue}.html"
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text(html, encoding="utf-8")
        print(f"{sortie.relative_to(RACINE)}  objet : {len(e['objet'])} car.")


if __name__ == "__main__":
    main()
