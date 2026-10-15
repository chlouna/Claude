"""Newsletter Trucker de novembre 2026, version « charte Michelin Digital Chapter 2 ».
Palette par niveaux (cf. charte) :
  N1 dominantes : Michelin Blue #061866, Glow White #FFFFFF, Off White #F5F3F1 ; accents Velvet Black #000000, Highlight Yellow #FFFF1A (uniquement sur bleu, fonctionnel).
  N2 blue hues (≤ 15 %) : Ice Blue #E4EAF2, Sky Blue #B5D2F4, Electric Blue #1953FF, Indigo Blue #002499, Space Blue #000E38.
  N3 accents (≤ 5 %) : Tangerine #E67245 (pastille « Danger »), Teal #7EDEC8 (coches de la checklist).
Typo : titres Bib Bold en casse de phrase (repli Noto Sans / Arial), texte Noto Sans. Échelle : T1 36/54, T2 32/48, T3 28/42, corps 16/24, S 14/21, annotation 12/18.
python3 newsletters/scripts/trucker_2026_11_charte.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from trucker_2026_11 import T, IMAGES, LIENS, LANGS

SORTIE = Path(__file__).resolve().parent.parent / "trucker" / "2026-11" / "charte"
BLEU, BLANC, OFF, NOIR, JAUNE = "#061866", "#FFFFFF", "#F5F3F1", "#000000", "#FFFF1A"
ICE, SKY, ELEC, INDIGO, SPACE = "#E4EAF2", "#B5D2F4", "#1953FF", "#002499", "#000E38"
TANG, TEAL = "#E67245", "#7EDEC8"
GRIS = "#4A4F5C"
TXT = "font-family:'Noto Sans',Arial,Helvetica,sans-serif;"
TIT = "font-family:'Bib','Noto Sans',Arial,Helvetica,sans-serif;font-weight:700;"


def page(preheader, corps, lang):
    return f"""<!DOCTYPE html>
<html lang="{lang}" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
<title>Le Relais · Michelin Truckfly</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<!--[if mso]><style>table,td,p,a,span,h1,h2,h3{{font-family:Arial,Helvetica,sans-serif !important;}}</style><![endif]-->
<style>
  /* Bib : charger BIB-Bold.woff2 dans Brevo puis remplacer URL-BIB-BOLD. Sans ça, repli Noto Sans Bold. */
  @font-face{{font-family:'Bib';src:url('URL-BIB-BOLD') format('woff2');font-weight:700;font-style:normal;}}
  body{{margin:0;padding:0;width:100%;-webkit-text-size-adjust:100%;}}
  table{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}}
  img{{border:0;display:block;}}
  a[x-apple-data-detectors]{{color:inherit !important;text-decoration:none !important;}}
  @media screen and (max-width:620px){{
    .conteneur{{width:100% !important;}}
    .pad{{padding-left:20px !important;padding-right:20px !important;}}
    .col{{display:block !important;width:100% !important;box-sizing:border-box !important;padding:0 0 12px 0 !important;}}
    .btn-full, .btn-full a{{display:block !important;width:100% !important;box-sizing:border-box !important;text-align:center !important;}}
    .t1{{font-size:32px !important;line-height:48px !important;}}
    .t2{{font-size:30px !important;line-height:40px !important;}}
    .t3{{font-size:24px !important;line-height:34px !important;}}
  }}
</style>
</head>
<body style="margin:0;padding:0;background-color:{OFF};">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:{OFF};opacity:0;">{preheader}&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{OFF};">
<tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" class="conteneur" style="width:600px;max-width:600px;">
<tr><td class="pad" align="right" style="padding:14px 32px;{TXT}font-size:12px;line-height:18px;color:{GRIS};"><a href="{{{{ mirror }}}}" style="color:{GRIS};">Voir dans le navigateur</a></td></tr>
{corps}
</table>
</td></tr></table>
</body></html>
"""


def bouton(texte, lien, fond, couleur, largeur=260):
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" class="btn-full"><tr>
  <td align="center" style="border-radius:8px;background-color:{fond};">
    <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="{lien}" style="height:50px;v-text-anchor:middle;width:{largeur}px;" arcsize="16%" stroke="f" fillcolor="{fond}"><w:anchorlock/><center style="color:{couleur};font-family:Arial,sans-serif;font-size:16px;font-weight:bold;">{texte}</center></v:roundrect><![endif]-->
    <!--[if !mso]><!-- --><a href="{lien}" target="_blank" style="display:inline-block;padding:15px 28px;border-radius:8px;background-color:{fond};{TXT}font-size:16px;line-height:20px;font-weight:700;color:{couleur};text-decoration:none;">{texte}</a><!--<![endif]-->
  </td></tr></table>"""


def pastille(texte, fond, couleur):
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 14px 0;"><tr>'
            f'<td style="background-color:{fond};border-radius:20px;padding:5px 14px;{TXT}font-size:13px;line-height:18px;font-weight:700;color:{couleur};">{texte}</td></tr></table>')


def insec(texte):
    return texte.replace(" ?", "&nbsp;?").replace(" !", "&nbsp;!").replace(" :", "&nbsp;:")


def h(texte, couleur, niveau="t3", taille=28, interligne=42, marge="0 0 16px 0"):
    texte = insec(texte)
    return f'<h2 class="{niveau}" style="margin:{marge};{TIT}font-size:{taille}px;line-height:{interligne}px;color:{couleur};">{texte}</h2>'


def p(texte, couleur=NOIR, marge="0 0 16px 0", taille=16, interligne=24):
    return f'<p style="margin:{marge};{TXT}font-size:{taille}px;line-height:{interligne}px;color:{couleur};">{texte}</p>'


def sec(contenu, fond, pad="40px 40px"):
    return f'<tr><td class="pad" style="background-color:{fond};padding:{pad};">\n{contenu}\n</td></tr>'


def ancre(n):
    return f'<tr><td style="font-size:0;line-height:0;"><a name="bloc-{n}" id="bloc-{n}"></a></td></tr>'


def libelle(lang, cle):
    L = {"FR": {"s1": "Loi Montagne", "s2": "Le tuto du mois", "s3": "La communauté", "s4": "Bravo !", "danger": "Hiver"},
         "IT": {"s1": "Loi Montagne", "s2": "Il tutorial del mese", "s3": "La community", "s4": "Bravi!", "danger": "Inverno"},
         "ES": {"s1": "Loi Montagne", "s2": "El tutorial del mes", "s3": "La comunidad", "s4": "¡Enhorabuena!", "danger": "Invierno"}}
    return L[lang][cle]


def blocs(L, t):
    b = []
    # En-tête : Michelin Blue, logo blanc, nom du rendez-vous
    b.append(sec(f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td valign="middle"><a href="LIEN-APP"><img src="../../../assets/logo-truckfly-blanc.png" width="140" height="35" alt="Michelin Truckfly" style="width:140px;height:35px;{TXT}font-size:16px;font-weight:700;color:{BLANC};"></a></td>
  <td valign="middle" align="right" style="{TXT}font-size:12px;line-height:18px;color:{SKY};">{t['numero']}</td>
</tr></table>
<h1 class="t1" style="margin:28px 0 4px 0;{TIT}font-size:36px;line-height:54px;color:{BLANC};">Le Relais</h1>
{p(t['sous'], SKY, "0 0 18px 0", 14, 21)}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-top:1px solid {INDIGO};padding-top:14px;{TXT}font-size:12px;line-height:18px;color:{BLANC};">{t['gps']} <a href="{t['gps_lien']}" style="color:{JAUNE};font-weight:700;">{t['gps_lien_txt']}</a></td></tr></table>""",
        BLEU, "26px 40px 22px 40px"))
    # Édito : Glow White
    b.append(sec(f"""<h2 class="t2" style="margin:0 0 20px 0;{TIT}font-size:32px;line-height:44px;color:{BLEU};">{insec(t['accroche'])}</h2>
{p(t['salut'])}{''.join(p(x) for x in t['edito'])}
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 0 0;"><tr>
  <td width="54" valign="middle"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" width="44" height="44" style="width:44px;height:44px;border-radius:22px;background-color:{ICE};{TXT}font-size:11px;color:{BLEU};">[photo]</td></tr></table></td>
  <td valign="middle">{p('<strong>' + t['signe'] + '</strong>', NOIR, '0', 15, 21)}{p(t['role'], GRIS, '0', 12, 18)}</td>
</tr></table>""", BLANC, "40px 40px 32px 40px"))
    # Sommaire : Ice Blue (niveau 2)
    lignes = "".join(f'<tr><td width="30" valign="top" style="padding:0 0 10px 0;{TXT}font-size:15px;line-height:22px;font-weight:700;color:{BLEU};">{i}.</td><td style="padding:0 0 10px 0;{TXT}font-size:15px;line-height:22px;"><a href="#bloc-{i}" style="color:{BLEU};font-weight:700;text-decoration:underline;">{x}</a></td></tr>' for i, x in enumerate(t["prog"], 1))
    b.append(sec(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:{ICE};border-radius:12px;padding:20px 22px 10px 22px;">{p("<strong>" + t["prog_tag"].capitalize() + "</strong>", BLEU, "0 0 12px 0", 14, 21)}<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{lignes}</table></td></tr></table>',
                 BLANC, "0 40px 40px 40px"))
    # 1. Loi Montagne : Michelin Blue, checklist Indigo, coches Teal, bouton jaune
    puces = "".join(f'<tr><td width="20" valign="top" style="padding:0 0 10px 0;{TXT}font-size:16px;line-height:24px;color:{SKY};">–</td><td style="padding:0 0 10px 0;{TXT}font-size:16px;line-height:24px;color:{BLANC};">{x}</td></tr>' for x in t["s1_liste"])
    check = "".join(f'<tr><td width="34" valign="top" style="padding:0 0 12px 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" width="24" height="24" style="width:24px;height:24px;border-radius:12px;background-color:{TEAL};{TXT}font-size:14px;line-height:24px;font-weight:700;color:{SPACE};">✓</td></tr></table></td><td style="padding:1px 0 12px 0;{TXT}font-size:15px;line-height:22px;color:{BLANC};">{x}</td></tr>' for x in t["check"])
    b.append(ancre(1))
    b.append(sec(pastille(libelle(L, "s1"), INDIGO, BLANC) + h(t["s1_titre"], BLANC)
        + "".join(p(x, BLANC) for x in t["s1"]) + p("<strong>" + t["s1_liste_tit"] + "</strong>", BLANC, "0 0 10px 0")
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 8px 0;">{puces}</table>'
        + "".join(p(x, BLANC) for x in t["s1_suite"])
        + f'<a href="{LIENS["s1"]}" target="_blank"><img src="{IMAGES["loi"]}" width="520" alt="{t["alt_loi"]}" style="display:block;width:100%;max-width:520px;height:auto;border-radius:12px;{TXT}font-size:14px;color:{SKY};"></a>'
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:22px 0 24px 0;"><tr><td style="background-color:{INDIGO};border-radius:12px;padding:20px 20px 8px 20px;">{p("<strong>" + t["check_tit"] + "</strong>", BLANC, "0 0 14px 0", 17, 24)}<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{check}</table></td></tr></table>'
        + bouton(t["s1_btn"], LIENS["s1"], JAUNE, BLEU), BLEU))
    # 2. Alertes : blanc, étapes Ice Blue, pastille Tangerine (niveau 3)
    def etapes(titre_e, items):
        lig = "".join(f'<tr><td width="34" valign="top" style="padding:0 0 10px 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" width="26" height="26" style="width:26px;height:26px;border-radius:13px;background-color:{BLEU};{TXT}font-size:13px;line-height:26px;font-weight:700;color:{BLANC};">{i}</td></tr></table></td><td style="padding:2px 0 10px 0;{TXT}font-size:15px;line-height:22px;color:{NOIR};">{x}</td></tr>' for i, x in enumerate(items, 1))
        return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:{ICE};border-radius:12px;padding:18px 18px 8px 18px;">{p("<strong>" + titre_e + "</strong>", BLEU, "0 0 12px 0", 16, 22)}<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{lig}</table></td></tr></table>'
    b.append(ancre(2))
    b.append(sec(f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td>{pastille(libelle(L, "s2"), ICE, BLEU)}</td><td style="padding-left:8px;">{pastille(libelle(L, "danger"), TANG, BLANC)}</td></tr></table>'
        + h(t["s2_titre"], BLEU) + "".join(p(x) for x in t["s2"])
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 20px 0;"><tr><td class="col" width="50%" valign="top" style="padding-right:8px;">{etapes(t["pour_signaler"], t["etapes_signaler"])}</td><td class="col" width="50%" valign="top" style="padding-left:8px;">{etapes(t["pour_anticiper"], t["etapes_anticiper"])}</td></tr></table>'
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="padding:0 0 24px 0;"><a href="{LIENS["s2"]}" target="_blank"><img src="{IMAGES["alerte"]}" width="240" alt="{t["alt_alerte"]}" style="display:block;width:240px;max-width:100%;height:auto;border-radius:12px;{TXT}font-size:14px;color:{BLEU};"></a></td></tr></table>'
        + bouton(t["s2_btn"], LIENS["s2"], BLEU, BLANC), BLANC))
    # 3. Contributeur : Michelin Blue, cartes Indigo, +1 jaune (touche sur bleu)
    cartes = ""
    acts = t["actions"]
    for i in range(0, len(acts), 2):
        row = ""
        for ti, de in acts[i:i + 2]:
            row += (f'<td class="col" width="50%" valign="top" style="padding:0 5px 10px 5px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{INDIGO};border-radius:12px;"><tr>'
                    f'<td width="52" valign="middle" style="padding:12px 0 12px 14px;{TXT}font-size:18px;line-height:24px;font-weight:700;color:{JAUNE};">+1</td>'
                    f'<td valign="middle" style="padding:12px 14px 12px 4px;">{p("<strong>" + ti + "</strong>", BLANC, "0", 14, 19)}{p(de, SKY, "2px 0 0 0", 12, 17)}</td></tr></table></td>')
        cartes += f"<tr>{row}</tr>"
    b.append(ancre(3))
    b.append(sec(pastille(libelle(L, "s3"), INDIGO, BLANC) + h(t["s3_titre"], BLANC)
        + "".join(p(x, BLANC) for x in t["s3"])
        + p("<strong>" + t["regle"] + "</strong>", JAUNE, "4px 0 14px 0", 18, 26)
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 14px 0;">{cartes}</table>'
        + p(t["s3_fin"], BLANC, "0 0 22px 0")
        + bouton(t["s3_btn"], LIENS["s3"], JAUNE, BLEU, 240), BLEU))
    # 4. Top contributeurs : Off White
    b.append(ancre(4))
    b.append(sec(pastille(libelle(L, "s4"), ICE, BLEU) + h(t["top_titre"], BLEU)
        + f'<a href="{LIENS["top"]}" target="_blank"><img src="{IMAGES["top"]}" width="520" alt="{t["alt_top"]}" style="display:block;width:100%;max-width:520px;height:auto;border-radius:12px;{TXT}font-size:14px;color:{BLEU};"></a>'
        + '<div style="height:22px;line-height:22px;font-size:0;">&nbsp;</div>'
        + bouton(t["top_btn"], LIENS["top"], BLEU, BLANC, 220), OFF))
    # Mot de la route : blanc, filet Sky Blue
    b.append(sec(h(t["mot_tag"].capitalize(), BLEU, "t3", 24, 36, "0 0 14px 0") + "".join(p(x) for x in t["mot"])
        + p("<strong>" + t["equipe"] + "</strong>", BLEU, "0"), BLANC, "36px 40px 36px 40px"))
    # Pied : Space Blue (ton sur ton)
    b.append(sec(f"""{p('<strong>' + t['faq_tit'] + '</strong>', BLANC, '0 0 6px 0', 16, 22)}
{p(t['faq'] + ' <a href="https://faq.truckfly.com/" style="color:' + SKY + ';font-weight:700;">faq.truckfly.com</a>', BLANC, '0 0 18px 0', 14, 21)}
{p(t['raison'], SKY, '0 0 6px 0', 12, 18)}
{p('<a href="{{ unsubscribe }}" style="color:' + SKY + ';">' + t['desinscription'] + '</a>', SKY, '0', 12, 18)}""", SPACE, "30px 40px 34px 40px"))
    return "\n".join(b)


PRE = {"FR": "L'hiver arrive sur la route. Ce qui change au 1er novembre, les alertes qui t'aident, et comment grimper au classement.",
       "IT": "L'inverno arriva sulla strada. Cosa cambia dal 1° novembre, le segnalazioni che ti aiutano e come scalare la classifica.",
       "ES": "El invierno llega a la carretera. Qué cambia el 1 de noviembre, los avisos que te ayudan y cómo subir en la clasificación."}

if __name__ == "__main__":
    SORTIE.mkdir(parents=True, exist_ok=True)
    tout = "\n".join(f'{{% if ( "{L}" in contact.LANG ) %}}\n{blocs(L, T[L])}\n{{% endif %}}' for L in LANGS)
    (SORTIE / "brevo.html").write_text(page(PRE["FR"], tout, "fr"), encoding="utf-8")
    for L in LANGS:
        apercu = page(PRE[L], blocs(L, T[L]), L.lower()).replace("url('URL-BIB-BOLD')", "url('URL-BIB-BOLD'), url('../../../../guide-profil/assets/fonts/BIB-Bold.woff2')")
        (SORTIE / f"apercu-{L.lower()}.html").write_text(apercu, encoding="utf-8")
    print("ok")
