"""Newsletter Owner d'octobre 2026 (envoi le vendredi 30), FR, charte Michelin Digital Chapter 2.
python3 newsletters/scripts/owner_2026_10.py → newsletters/owner/2026-10/
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from trucker_2026_11_charte import (page, bouton, pastille, h, p, sec, image, insec,
                                    BLEU, BLANC, OFF, NOIR, JAUNE, ICE, SKY, INDIGO, SPACE, TEAL, GRIS, TXT, TIT)

SORTIE = Path(__file__).resolve().parent.parent / "owner" / "2026-10"


def checklist(items, sur_bleu):
    coul = BLANC if sur_bleu else NOIR
    return "".join(
        f'<tr><td width="34" valign="top" style="padding:0 0 12px 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" width="24" height="24" style="width:24px;height:24px;border-radius:12px;background-color:{TEAL};{TXT}font-size:14px;line-height:24px;font-weight:700;color:{SPACE};">✓</td></tr></table></td>'
        f'<td style="padding:1px 0 12px 0;{TXT}font-size:15px;line-height:22px;color:{coul};"><strong>{a}</strong><br><span style="color:{SKY if sur_bleu else GRIS};font-size:14px;">{b}</span></td></tr>' for a, b in items)


def corps(apercu):
    logo = "../../assets/logo-truckfly-blanc.png" if apercu else "URL-LOGO-BLANC"
    b = []
    # En-tête
    b.append(sec(f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td valign="middle"><a href="LIEN-ESPACE-PRO"><img src="{logo}" width="140" height="35" alt="Michelin Truckfly" style="width:140px;height:35px;{TXT}font-size:16px;font-weight:700;color:{BLANC};"></a></td>
  <td valign="middle" align="right" style="{TXT}font-size:12px;line-height:18px;color:{SKY};">Octobre 2026</td></tr></table>
<h1 class="t1" style="margin:28px 0 4px 0;{TIT}font-size:36px;line-height:54px;color:{BLANC};">L'Escale</h1>
{p("La lettre des établissements partenaires de Michelin Truckfly", SKY, "0", 14, 21)}""", BLEU, "26px 40px 26px 40px"))
    # Édito
    b.append(sec(f"""<h2 class="t2" style="margin:0 0 20px 0;{TIT}font-size:32px;line-height:44px;color:{BLEU};">{insec("Cet hiver, les routiers vont chercher où s'arrêter plus tôt")}</h2>
{p("Bonjour {{ contact.PRENOM | default : \"à toute l’équipe\" }},")}
{p("Depuis le passage à l'heure d'hiver, la nuit tombe vers 17 h 30. Les routiers choisissent leur arrêt du soir plus tôt dans la journée, et les places de parking poids lourds se remplissent plus vite.")}
{p("C'est le moment où <strong>une fiche à jour fait la différence</strong> : horaires d'hiver, places disponibles, douches, repas chaud. Ce mois-ci, nous vous donnons les clés pour être le premier choix des routiers cet hiver.")}
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 0 0;"><tr>
  <td width="54" valign="middle"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" width="44" height="44" style="width:44px;height:44px;border-radius:22px;background-color:{ICE};{TXT}font-size:11px;color:{BLEU};">[photo]</td></tr></table></td>
  <td valign="middle">{p('<strong>[Prénom Nom]</strong>', NOIR, '0', 15, 21)}{p('[rôle] chez Michelin Truckfly', GRIS, '0', 12, 18)}</td></tr></table>""", BLANC, "40px 40px 32px 40px"))
    # Sommaire
    prog = ["L'hiver arrive : ce que cherchent les routiers", "Nouveau : les routiers se recommandent entre amis", "Votre fiche d'hiver en 4 points", "Le conseil du mois : répondre aux avis"]
    lignes = "".join(f'<tr><td width="30" valign="top" style="padding:0 0 10px 0;{TXT}font-size:15px;line-height:22px;font-weight:700;color:{BLEU};">{i}.</td><td style="padding:0 0 10px 0;{TXT}font-size:15px;line-height:22px;"><a href="#bloc-{i}" style="color:{BLEU};font-weight:700;">{x}</a></td></tr>' for i, x in enumerate(prog, 1))
    b.append(sec(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:{ICE};border-radius:12px;padding:20px 22px 10px 22px;">{p("<strong>Au programme</strong>", BLEU, "0 0 12px 0", 14, 21)}<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{lignes}</table></td></tr></table>', BLANC, "0 40px 40px 40px"))
    # 1. Hiver (bleu)
    besoins = [("Une place de parking poids lourd sûre et éclairée", "dès la fin d'après-midi"),
               ("Des douches chaudes et propres", "après une longue journée au froid"),
               ("Un repas chaud, même tard", "indiquez vos horaires de service"),
               ("Des infos fiables avant de venir", "horaires d'hiver, fermetures, accès")]
    b.append(f'<tr><td style="font-size:0;line-height:0;"><a name="bloc-1" id="bloc-1"></a></td></tr>')
    b.append(sec(pastille("Saison", INDIGO, BLANC) + h("L'hiver arrive : ce que cherchent les routiers", BLANC)
        + p("Nuits plus longues, routes glissantes, équipements obligatoires en montagne dès le 1er novembre : en hiver, les routiers planifient davantage leurs arrêts. Ils regardent l'app avant de choisir où dormir et où manger.", BLANC)
        + p("<strong>Ce qu'ils recherchent en priorité :</strong>", BLANC, "0 0 12px 0")
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 10px 0;">{checklist(besoins, True)}</table>'
        + image("[Photo d'un établissement partenaire en hiver · 1040 × 520 px]", "Un établissement partenaire accueille des routiers en hiver", "LIEN-ESPACE-PRO")
        + '<div style="height:24px;line-height:24px;font-size:0;">&nbsp;</div>'
        + bouton("Je mets mes horaires d'hiver", "LIEN-ESPACE-PRO?utm_content=hiver", JAUNE, BLEU, 300), BLEU))
    # 2. Nouveauté : recommandations entre amis
    b.append(f'<tr><td style="font-size:0;line-height:0;"><a name="bloc-2" id="bloc-2"></a></td></tr>')
    b.append(sec(pastille("Nouveau sur Michelin Truckfly", ICE, BLEU) + h("Les routiers se recommandent désormais entre amis", BLEU)
        + p("Avec le <strong>Profil Trucker</strong>, les conducteurs ajoutent leurs collègues en amis. Ils voient où leurs amis se sont arrêtés et les avis qu'ils déposent, mis en avant dans l'app.")
        + p("Pour vous, c'est le <strong>bouche-à-oreille des routiers, en version numérique</strong> : chaque visite et chaque avis positif peut donner envie à d'autres conducteurs de s'arrêter chez vous.")
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 22px 0;"><tr><td style="background-color:{ICE};border-radius:12px;padding:18px 20px;">'
        + p("<strong>Votre levier :</strong> invitez vos clients routiers à laisser un avis sur Michelin Truckfly. [Kit affiche avec QR code à télécharger, si disponible.]", BLEU, "0", 15, 22) + '</td></tr></table>'
        + bouton("Je découvre le Profil Trucker", "LIEN-PROFIL-TRUCKER", BLEU, BLANC, 300), BLANC))
    # 3. Fiche d'hiver en 4 points (Off White)
    fiche = [("Vos horaires d'hiver", "jours fériés compris (1er et 11 novembre, fêtes de fin d'année)"),
             ("Des photos récentes", "parking, entrée, douches, salle : la nuit aussi, si c'est éclairé"),
             ("Vos services poids lourds", "nombre de places, douches, Wi-Fi, menu routier, accès 44 t"),
             ("Une réponse à chaque avis", "même courte : un merci compte pour les routiers")]
    b.append(f'<tr><td style="font-size:0;line-height:0;"><a name="bloc-3" id="bloc-3"></a></td></tr>')
    b.append(sec(pastille("Votre fiche", ICE, BLEU) + h("Votre fiche d'hiver en 4 points", BLEU)
        + p("Une fiche complète inspire confiance et ressort mieux auprès des routiers qui cherchent où s'arrêter.")
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 14px 0;">{checklist(fiche, False)}</table>'
        + bouton("Je complète ma fiche", "LIEN-ESPACE-PRO?utm_content=fiche", BLEU, BLANC, 260), OFF))
    # 4. Conseil du mois (bleu)
    b.append(f'<tr><td style="font-size:0;line-height:0;"><a name="bloc-4" id="bloc-4"></a></td></tr>')
    b.append(sec(pastille("Le conseil du mois", INDIGO, BLANC) + h("Répondre aux avis en 2 minutes", BLANC)
        + p("Un routier qui lit vos réponses voit un établissement attentif. Quelques règles simples :", BLANC)
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 10px 0;">{checklist([("Remerciez", "même pour un avis court"), ("Restez factuel", "si l’avis est négatif, expliquez ce que vous avez changé"), ("Invitez à revenir", "une phrase suffit : « Au plaisir de vous revoir sur la route ! »")], True)}</table>'
        + bouton("Je réponds aux avis", "LIEN-AVIS", JAUNE, BLEU, 240), BLEU))
    # Témoignage
    b.append(sec(pastille("Ils en parlent", ICE, BLEU) + h("[Nom de l'établissement], [ville]", BLEU)
        + f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td class="col" width="42%" valign="top" style="padding-right:16px;">{image("[Photo de l'établissement]", "Établissement partenaire", "LIEN-TEMOIGNAGE", 220, 200)}</td>
  <td class="col" width="58%" valign="top">{p("« [Citation du gérant : ce que Michelin Truckfly lui apporte, en 2 phrases.] »", NOIR, "0 0 10px 0", 17, 25)}{p("[Prénom Nom], [fonction]", GRIS, "0 0 14px 0", 13, 18)}
  <p style="margin:0;{TXT}font-size:15px;line-height:22px;"><a href="LIEN-TEMOIGNAGE" style="color:{BLEU};font-weight:700;">Lire son témoignage</a></p></td></tr></table>""", BLANC))
    # Contact
    b.append(sec(f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td class="col" valign="middle">{h("Une question sur votre fiche ?", BLEU, "t3", 22, 30, "0 0 6px 0")}{p("Notre équipe vous aide à la mettre à jour.", NOIR, "0")}</td>
  <td class="col" valign="middle" align="right" width="200">{bouton("Nous écrire", "mailto:[adresse-support]", BLEU, BLANC, 180)}</td></tr></table>""", OFF, "32px 40px"))
    # Pied
    b.append(sec(f"""{p('<a href="https://faq.truckfly.com/" style="color:' + SKY + ';font-weight:700;">FAQ Michelin Truckfly</a>', BLANC, '0 0 14px 0', 14, 21)}
{p("Vous recevez cet e-mail car votre établissement est référencé sur Michelin Truckfly.", SKY, '0 0 6px 0', 12, 18)}
{p('<a href="{{ unsubscribe }}" style="color:' + SKY + ';">Se désinscrire</a> · Michelin Truckfly, [adresse postale]', SKY, '0', 12, 18)}""", SPACE, "28px 40px 32px 40px"))
    return "\n".join(b)


if __name__ == "__main__":
    SORTIE.mkdir(parents=True, exist_ok=True)
    pre = "Nuits plus longues, parkings pleins plus tôt : 4 réglages simples pour être le premier choix des routiers cet hiver."
    (SORTIE / "brevo-fr.html").write_text(page(pre, corps(False), "fr"), encoding="utf-8")
    ap = page(pre, corps(True), "fr").replace("url('URL-BIB-BOLD')", "url('URL-BIB-BOLD'), url('../../../guide-profil/assets/fonts/BIB-Bold.woff2')")
    (SORTIE / "apercu-fr.html").write_text(ap, encoding="utf-8")
    print("ok")
