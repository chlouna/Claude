# Génère l'in-app message OneSignal de la proposition D à partir de ../index.html.
# Usage : python3 interstitiels/vinci-fetes/onesignal/generer.py
import base64, io, os, re
from PIL import Image
R=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')+'/'
src=open(R+'index.html').read()

def png_b64(path, h):
    im=Image.open(path).convert('RGBA'); w=round(im.width*h/im.height)
    im=im.resize((w,h), Image.LANCZOS); b=io.BytesIO(); im.save(b,'PNG',optimize=True)
    return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
logo_tf=png_b64(R+'assets/truckfly-blanc-rogne.png', 90)
logo_vinci=png_b64(R+'assets/vinci-autoroutes.png', 102)
bib='data:font/woff2;base64,'+base64.b64encode(open(R+'../assets/fonts/BIB-Bold.woff2','rb').read()).decode()

css=src[src.index('<style>')+7:src.index('</style>')]
css=re.sub(r'@font-face[^}]*\}\n','',css)
css=re.sub(r'\.entete-planche[^\n]*\n','',css)
css=re.sub(r'\.planche[^\n]*\n|\.cartel[^\n]*\n|\.capture[^\n]*\n','',css)
css=re.sub(r'body \{[^}]*\}', '', css, count=1)
defs=src[src.index('<!-- Personnages réutilisés'):src.index('<div class="entete-planche">')]
a=src.index('<!-- D · Pleine page'); b=src.index('</section></div>',a)
sec=src[a:b]
sec=sec[sec.index('<section'):]+'</section>'
sec=sec.replace('<section class="ecran nuit" id="vd" data-nom="pere-noel-lutins">','<section class="ecran nuit card">')
sec=sec.replace('<button class="fermer" aria-label="Fermer">×</button>','<button class="fermer" id="close-x" data-onesignal-unique-label="noel-close-x" aria-label="Fermer">×</button>')
sec=re.sub(r'<a class="cta jaune">([^<]*)</a>', r'<button class="cta jaune" id="quiz" data-onesignal-unique-label="noel-quiz">\1</button>', sec)
sec=sec.replace('<a class="plus-tard">Plus tard</a>','<button class="plus-tard" id="later" data-onesignal-unique-label="noel-later">Plus tard</button>')
sec=sec.replace('src="assets/truckfly-blanc-rogne.png"','src="'+logo_tf+'"').replace('src="assets/vinci-autoroutes.png"','src="'+logo_vinci+'"')
for x in ['id="close-x"','id="quiz"','id="later"','data:image/png']: assert x in sec, x

html=f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Noël – Truckfly x VINCI</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
/* Police des titres Michelin (Bib), intégrée au fichier */
@font-face {{ font-family: "Bib"; src: url("{bib}") format("woff2"); font-weight: 700; font-display: swap; }}
{css}
/* ---------- Ajustements pour l'in-app message OneSignal ---------- */
html, body {{ height: 100%; background: transparent; }}
body {{ font-family: "Inter", system-ui, sans-serif; display: flex; align-items: center; justify-content: center; padding: 16px; }}
.card {{ width: 100%; max-width: 400px; height: min(844px, calc(100vh - 32px)); height: min(844px, calc(100dvh - 32px)); border-radius: 28px; }}
button.fermer, button.cta, button.plus-tard {{ font-family: "Inter", sans-serif; cursor: pointer; border: 0; }}
button.cta {{ width: 100%; }}
button.cta:active {{ transform: scale(.98); }}
button.plus-tard {{ display: block; margin-left: auto; margin-right: auto; background: none; }}
button.cta {{ font-size: 16px; padding: 0 10px; white-space: nowrap; }}
/* Les personnages gardent une taille lisible : la carte défile si l'écran est très petit */
.card {{ overflow-y: auto; }}
.scene {{ min-height: 150px; }}
.v-plein {{ flex: 1 0 auto; }}
/* Petits téléphones : textes un peu plus compacts */
@media (max-height: 760px) {{
  .v-plein {{ padding-top: 52px; gap: 6px; }}
  .duo img {{ height: 24px; }} .logo-vinci {{ height: 42px; }} .duo .logo-vinci img {{ height: 28px; }}
  .bas {{ padding-bottom: 12px; }}
  .badge {{ margin-bottom: 6px; }}
  .accroche-haut {{ font-size: 13px; margin-top: 4px !important; }}
  .c-titre, .c-gestes {{ font-size: 13px; }}
  .corridor .picto {{ width: 46px; height: 54px; }}
  .nuit h1 {{ font-size: 22px; }}
  .texte {{ font-size: 13.5px; margin-top: 6px; }}
  .cta {{ height: 46px; margin-top: 10px; }}
  .plus-tard {{ margin-top: 8px; font-size: 14px; }}
}}
</style>
</head>
<body>
<!-- Active la substitution Liquid (liquidPlayerTags) dans l'IAM -->
<span hidden>{{{{ USER_ID | default: '' }}}}</span>

{defs}
{sec}

<script>
    // Lien public du quiz Tally (à publier avant diffusion)
    const TALLY_URL = "https://tally.so/r/q5L7Y2";

    function buildTallyUrl() {{
      // Tags OneSignal injectés par Liquid (posés côté app via OneSignal.User.addTags)
      const tags = (typeof liquidPlayerTags !== "undefined" && liquidPlayerTags) || {{}};
      const params = new URLSearchParams({{
        user_id: tags.USER_ID || "",   // champ caché « user_id » du formulaire Tally
        source:  "interstitiel-noel",   // champ caché « source » du formulaire Tally
        email:   tags.EMAIL   || "",
        phone:   tags.PHONE   || ""    // tag à créer côté app (n'existe pas encore)
      }});
      return TALLY_URL + "?" + params.toString();
    }}

    document.getElementById("quiz").addEventListener("click", function (e) {{
      OneSignalIamApi.openUrl(e, buildTallyUrl()); // ouvre le lien et ferme l'IAM
    }});

    document.getElementById("later").addEventListener("click", function (e) {{
      OneSignalIamApi.close(e);
    }});

    document.getElementById("close-x").addEventListener("click", function (e) {{
      OneSignalIamApi.close(e);
    }});
</script>
</body>
</html>
'''
open(R+'onesignal/noel-d-pere-noel.html','w').write(html)
print(len(html.encode())//1024,'Ko')
