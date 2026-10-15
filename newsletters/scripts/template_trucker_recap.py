"""Concept B « Ton mois sur la route » : récap perso (Strava/Spotify), progression et défi (Duolingo),
l'essentiel en 30 s (Morning Brew), impact de la communauté (Waze), quiz en 1 clic.
python3 newsletters/scripts/template_trucker_recap.py → newsletters/template/trucker-recap/
Attributs Brevo nécessaires (à synchroniser depuis l'app) : POINTS_MOIS, AVIS_MOIS, ALERTES_MOIS, VUES_ALERTES, POINTS_NIVEAU_SUIVANT.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from trucker_2026_11_charte import page, bouton, p, BLEU, BLANC, OFF, NOIR, JAUNE, ICE, SKY, INDIGO, SPACE, TEAL, TANG, GRIS, TXT, TIT, insec

SORTIE = Path(__file__).resolve().parent.parent / "template" / "trucker-recap"

# Valeurs d'exemple pour l'aperçu ; dans Brevo, ce sont des attributs de contact.
ATTR = {"PRENOM": ("{{ contact.PRENOM | default : \"\" }}", "Karim"),
        "POINTS": ("{{ contact.POINTS_MOIS | default : \"0\" }}", "14"),
        "AVIS": ("{{ contact.AVIS_MOIS | default : \"0\" }}", "5"),
        "ALERTES": ("{{ contact.ALERTES_MOIS | default : \"0\" }}", "3"),
        "VUES": ("{{ contact.VUES_ALERTES | default : \"0\" }}", "212"),
        "RESTE": ("{{ contact.POINTS_NIVEAU_SUIVANT | default : \"10\" }}", "6")}


def a(cle, apercu):
    return ATTR[cle][1] if apercu else ATTR[cle][0]


def carte(contenu, fond=BLANC, pad="28px 28px", marge="0 0 16px 0"):
    return f'<tr><td class="pad" style="padding:0 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:{marge};"><tr><td style="background-color:{fond};border-radius:20px;padding:{pad};">\n{contenu}\n</td></tr></table></td></tr>'


def sur(texte, couleur):
    return f'<p style="margin:0 0 8px 0;{TXT}font-size:13px;line-height:18px;font-weight:700;color:{couleur};">{texte}</p>'


def titre(texte, couleur, taille=26, ih=34, marge="0 0 12px 0"):
    return f'<h2 class="t3" style="margin:{marge};{TIT}font-size:{taille}px;line-height:{ih}px;color:{couleur};">{insec(texte)}</h2>'


def corps(apercu):
    c = []
    # En-tête compact
    c.append(f"""<tr><td class="pad" style="padding:8px 24px 18px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td valign="middle"><a href="LIEN-APP"><img src="{'../../assets/logo-truckfly-bleu.png' if apercu else 'URL-LOGO-BLEU'}" width="130" height="33" alt="Michelin Truckfly" style="width:130px;height:33px;{TXT}font-size:16px;font-weight:700;color:{BLEU};"></a></td>
  <td valign="middle" align="right" style="{TXT}font-size:13px;line-height:18px;font-weight:700;color:{BLEU};">Novembre 2026</td></tr></table></td></tr>""")
    # 1. Récap perso (Strava / Spotify Wrapped)
    tuiles = "".join(f"""<td class="col" width="33%" valign="top" style="padding:0 5px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color:{INDIGO};border-radius:14px;padding:18px 6px;">
  <p style="margin:0;{TIT}font-size:40px;line-height:44px;color:{BLANC};">{v}</p><p style="margin:4px 0 0 0;{TXT}font-size:13px;line-height:18px;color:{SKY};">{l}</p></td></tr></table></td>"""
                     for v, l in [(a("POINTS", apercu), "points gagnés"), (a("AVIS", apercu), "avis déposés"), (a("ALERTES", apercu), "alertes signalées")])
    c.append(carte(f"""{sur("Ton récap d'octobre", JAUNE)}
<h1 class="t1" style="margin:0 0 6px 0;{TIT}font-size:36px;line-height:44px;color:{BLANC};">Bravo {a("PRENOM", apercu)}, voici ton mois sur la route</h1>
{p("Merci pour tout ce que tu as partagé avec la communauté.", SKY, "0 0 22px 0")}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 22px 0;"><tr>{tuiles}</tr></table>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 22px 0;"><tr><td style="border-top:1px solid {INDIGO};padding-top:18px;">
  <p style="margin:0;{TXT}font-size:16px;line-height:24px;color:{BLANC};">Tes alertes ont été vues par <strong style="color:{JAUNE};">{a("VUES", apercu)} routiers</strong>. Autant de collègues prévenus à temps.</p>
</td></tr></table>
{bouton("Je partage mon récap", "LIEN-RECAP", JAUNE, BLEU, 240)}""", BLEU, "32px 28px"))
    # 2. Progression (Duolingo)
    c.append(carte(f"""{sur("Ta progression", BLEU)}
{titre("Plus que " + a("RESTE", apercu) + " points pour passer Routier expert", BLEU)}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 8px 0;"><tr>
  <td width="62%" height="14" style="height:14px;background-color:{BLEU};border-radius:7px 0 0 7px;font-size:0;line-height:0;">&nbsp;</td>
  <td width="38%" height="14" style="height:14px;background-color:{ICE};border-radius:0 7px 7px 0;font-size:0;line-height:0;">&nbsp;</td></tr></table>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 18px 0;"><tr>
  <td style="{TXT}font-size:12px;line-height:18px;color:{GRIS};">Routier éclaireur</td><td align="right" style="{TXT}font-size:12px;line-height:18px;color:{GRIS};">Routier expert</td></tr></table>
{p("Le plus rapide : <strong>ajoute 3 photos</strong> d'un arrêt que tu connais bien. Parking, entrée, douches : 1 photo = 1 point.")}
{bouton("Je gagne mes points", "LIEN-POINTS", BLEU, BLANC, 230)}""", BLANC))
    # 3. L'essentiel en 30 secondes (Morning Brew)
    infos = [("Loi Montagne", "Dès le 1er novembre, chaînes ou pneus 3PMSF dans les zones de montagne signalées.", "LIEN-INFO-1"),
             ("Italie", "Pneus hiver ou chaînes à bord sur les routes signalées à partir du 15 novembre.", "LIEN-INFO-2"),
             ("Dans l'app", "Les alertes brouillard et verglas s'affichent sur ton itinéraire avant le départ.", "LIEN-INFO-3")]
    lignes = "".join(f"""<tr><td style="padding:0 0 14px 0;border-bottom:1px solid {ICE};"><p style="margin:0 0 2px 0;{TXT}font-size:12px;line-height:16px;font-weight:700;color:{BLEU};">{t_}</p>
<p style="margin:0;{TXT}font-size:15px;line-height:22px;color:{NOIR};">{d_} <a href="{l_}" style="color:{BLEU};font-weight:700;">Lire</a></p></td></tr><tr><td style="height:14px;line-height:14px;font-size:0;">&nbsp;</td></tr>""" for t_, d_, l_ in infos)
    c.append(carte(f"""{sur("L'essentiel en 30 secondes", BLEU)}{titre("Ce qui change sur la route ce mois-ci", BLEU)}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{lignes}</table>""", BLANC, "28px 28px 14px 28px"))
    # 4. Le défi du mois (Duolingo)
    c.append(carte(f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="74" valign="top"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" width="60" height="60" style="width:60px;height:60px;border-radius:30px;background-color:{BLEU};{TIT}font-size:26px;line-height:60px;color:{JAUNE};">1</td></tr></table></td>
  <td valign="top">{sur("Le défi du mois", BLEU)}{titre("Signale ta première alerte météo", BLEU, 22, 30, "0 0 8px 0")}
  {p("Brouillard, verglas, neige : 10 secondes depuis la carte, et les routiers derrière toi sont prévenus.", NOIR, "0 0 16px 0", 15, 22)}
  {bouton("Je relève le défi", "LIEN-DEFI", BLEU, BLANC, 210)}</td></tr></table>""", ICE))
    # 5. Vu par la communauté (Waze / contenu des routiers)
    c.append(carte(f"""{sur("Vu par la communauté", BLEU)}
<a href="LIEN-PHOTO-DU-MOIS"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" valign="middle" height="260" style="height:260px;background-color:{ICE};border-radius:14px;{TXT}font-size:14px;color:{BLEU};">[Photo d'un routier de la communauté · 1040 × 520 px]</td></tr></table></a>
<p style="margin:14px 0 4px 0;{TXT}font-size:17px;line-height:25px;font-style:italic;color:{NOIR};">« [Le petit mot du routier sur sa photo] »</p>
{p("[Prénom], routier depuis [X] ans · [lieu]", GRIS, "0 0 16px 0", 13, 18)}
<p style="margin:0;{TXT}font-size:15px;line-height:22px;"><a href="LIEN-ENVOYER-PHOTO" style="color:{BLEU};font-weight:700;">Envoie ta photo, elle sera peut-être la prochaine</a></p>""", BLANC))
    # 6. Quiz en 1 clic
    reps = "".join(f'<td class="col" width="50%" style="padding:0 5px;"><a href="LIEN-QUIZ?reponse={k}" style="display:block;padding:16px 10px;border-radius:12px;background-color:{BLANC};{TXT}font-size:17px;line-height:22px;font-weight:700;color:{BLEU};text-align:center;text-decoration:none;">{v}</a></td>' for k, v in [("vrai", "Vrai"), ("faux", "Faux")])
    c.append(carte(f"""{sur("Le quiz de la route", JAUNE)}
{titre("Vrai ou faux : en zone Loi Montagne, des pneus M+S suffisent pour un poids lourd avec semi-remorque.", BLANC, 22, 30, "0 0 18px 0")}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>{reps}</tr></table>
{p("Clique, on te donne la réponse tout de suite.", SKY, "14px 0 0 0", 13, 18)}""", BLEU))
    # Pied
    c.append(f"""<tr><td class="pad" align="center" style="padding:14px 24px 34px 24px;{TXT}font-size:12px;line-height:18px;color:{GRIS};">
  <p style="margin:0 0 6px 0;">Une question ? <a href="https://faq.truckfly.com/" style="color:{BLEU};font-weight:700;">faq.truckfly.com</a></p>
  <p style="margin:0 0 6px 0;">Tu reçois cet e-mail car tu t'es inscrit à l'application mobile Michelin Truckfly.</p>
  <p style="margin:0;"><a href="{{{{ unsubscribe }}}}" style="color:{GRIS};">Se désinscrire</a></p></td></tr>""")
    return "\n".join(c)


if __name__ == "__main__":
    SORTIE.mkdir(parents=True, exist_ok=True)
    pre = "Tes points, tes alertes, ton prochain niveau : ton mois sur la route en un coup d'œil."
    (SORTIE / "brevo-fr.html").write_text(page(pre, corps(False), "fr"), encoding="utf-8")
    ap = page(pre, corps(True), "fr").replace("url('URL-BIB-BOLD')", "url('URL-BIB-BOLD'), url('../../../guide-profil/assets/fonts/BIB-Bold.woff2')")
    (SORTIE / "apercu-fr.html").write_text(ap, encoding="utf-8")
    print("ok")
