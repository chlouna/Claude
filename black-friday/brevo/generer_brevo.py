# Construit le template Brevo Black Friday (9 langues) : black-friday/brevo/template_black_friday_9_langues.yaml
# En-tête « Afficher dans le navigateur » + images du header et pied de page synchronisé : repris tels quels (source/).
# Usage : python3 black-friday/brevo/generer_brevo.py
import uuid
from pathlib import Path

ICI = Path(__file__).resolve().parent
LANGS = ["FR", "EN", "ES", "IT", "DE", "NL", "PL", "PT", "RO"]
AUTRES = [l for l in LANGS if l != "EN"]
COND_EN = "( \"EN\" in contact.LANG ) or ( " + " and ".join(f"( contact.LANG != \"{l}\" )" for l in AUTRES) + " )"
cond = lambda l: COND_EN if l == "EN" else f"( \"{l}\" in contact.LANG )"
uid = lambda: str(uuid.uuid4())
esc = lambda s: s.replace("'", "&#39;")
LP = "https://lp.truckfly.com/{}/gps-premium?utm_source=brevo&amp;utm_medium=transactional_emails"
IMG = "https://img.mailinblue.com/4222425/images/content_library/original/"

# ---------- Textes du header (bandeau bleu) ----------
HEADER = {
 "FR": ("MICHELIN Truckfly, l'appli gratuite préférée des chauffeurs routiers en Europe.", "Et pour ceux qui en veulent plus :", "Un GPS en option !", "fr"),
 "EN": ("MICHELIN Truckfly, the free app preferred by truck drivers across Europe.", "And for those who want more:", "a GPS option!", "en"),
 "ES": ("MICHELIN Truckfly, la app gratuita preferida por los camioneros en Europa.", "Y para quienes quieren más:", "¡GPS disponible como opción!", "es"),
 "IT": ("MICHELIN Truckfly, l'app gratuita preferita dagli autisti di camion in Europa.", "E per chi vuole di più:", "GPS disponibile come opzione!", "it"),
 "DE": ("MICHELIN Truckfly, die kostenlose App, die bei Lkw-Fahrern in Europa besonders beliebt ist.", "Und für alle, die mehr wollen:", "GPS als Option!", "en"),
 "NL": ("MICHELIN Truckfly, de gratis app die favoriet is bij vrachtwagenchauffeurs in Europa.", "En voor wie meer wil:", "een GPS-optie!", "nl"),
 "PL": ("MICHELIN Truckfly, darmowa aplikacja najchętniej wybierana przez kierowców ciężarówek w Europie.", "A dla tych, którzy chcą więcej:", "opcjonalny GPS!", "en"),
 "PT": ("MICHELIN Truckfly, a aplicação gratuita preferida dos camionistas na Europa.", "E para quem quer mais:", "GPS disponível como opção!", "en"),
 "RO": ("MICHELIN Truckfly, aplicația gratuită preferată de șoferii de camion din Europa.", "Iar pentru cei care vor mai mult:", "GPS opțional!", "en"),
}

# ---------- Textes des bannières ----------
# Prix affichés en zone euro (FR, ES, IT, DE, NL, PT) ; EN, PL, RO : code BF50 sans prix (prix iOS/Android différents).
# img : bannière Black Friday déjà importée dans Brevo (RO : à importer, voir png/campagne/brevo/ro)
B = {
 "FR": dict(img="6af5777201dbfb6057e2cb09.png", y1="Promo exceptionnelle -50%", y2="sur ton abonnement annuel !", blanc="Profite de ta pause pour activer ton GPS PL.",
   date="Du 27 au 30 novembre", prix='<p style="text-align:center;"><span style="font-family: Arial, Helvetica, sans-serif; color: rgb(255, 255, 26); font-size: 48px;"><strong>37,99€/an&nbsp;</strong></span><span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; color: rgb(255, 255, 255);">au lieu de <s>74,99€/an</s></span></p>',
   bouton="J'en profite à 37,99€/an*", note="*Seulement 5000 codes disponibles", t1="Laisse-toi tenter par le Black Friday !", t2="Ne passe pas à côté de cette opportunité.",
   a=[("Un GPS qui connaît ton camion", "Le GPS MICHELIN Truckfly prend en compte toutes les contraintes de ton camion : <strong>gabarit, poids et restrictions...</strong>"),
      ("Les restrictions, visibles avant d'y être", "Ponts trop bas, tonnages limités : anticipe chaque contrainte directement sur ton itinéraire."),
      ("La route, sous surveillance de tous", "Contrôles, accidents, obstacles : la communauté MICHELIN Truckfly te prévient en temps réel, et tu préviens à ton tour.")]),
 "EN": dict(img="6af5788a6d3f30be82998ef1.png", y1="Exceptional deal -50%", y2="on your annual subscription!", blanc="Make the most of your break to activate your HGV GPS.",
   date="From 27 to 30 November", code="Code BF50", bouton="Get the deal*", note="*Only 5000 codes available", t1="Treat yourself this Black Friday!", t2="Don't miss out on this opportunity.",
   a=[("A GPS that knows your truck", "The MICHELIN Truckfly GPS takes every constraint of your truck into account: <strong>dimensions, weight and restrictions...</strong>"),
      ("Restrictions, visible before you get there", "Low bridges, weight limits: anticipate every constraint right on your route."),
      ("The road, watched over by everyone", "Checks, accidents, obstacles: the MICHELIN Truckfly community warns you in real time, and you warn others in return.")]),
 "ES": dict(img="6af5793a195e7c4d1ccebe3f.png", y1="Oferta excepcional -50%", y2="¡en tu suscripción anual!", blanc="Aprovecha tu pausa para activar tu GPS para camiones.",
   date="Del 27 al 30 de noviembre", prix='<p style="text-align:center;"><span style="font-family: Arial, Helvetica, sans-serif; color: rgb(255, 255, 26); font-size: 48px;"><strong>37,99 €/año&nbsp;</strong></span><span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; color: rgb(255, 255, 255);">en lugar de <s>74,99 €/año</s></span></p>', bouton="Aprovéchalo por 37,99 €/año*", note="*Solo 5000 códigos disponibles", t1="¡Déjate tentar por el Black Friday!", t2="No dejes pasar esta oportunidad.",
   a=[("Un GPS que conoce tu camión", "El GPS de MICHELIN Truckfly tiene en cuenta todas las limitaciones de tu camión: <strong>dimensiones, peso y restricciones...</strong>"),
      ("Las restricciones, visibles antes de llegar", "Puentes demasiado bajos, límites de tonelaje: anticipa cada limitación directamente en tu ruta."),
      ("La carretera, vigilada por todos", "Controles, accidentes, obstáculos: la comunidad MICHELIN Truckfly te avisa en tiempo real, y tú avisas a los demás.")]),
 "IT": dict(img="6af57956195e7c4d1ccebe46.png", y1="Promo eccezionale -50%", y2="sul tuo abbonamento annuale!", blanc="Approfitta della pausa per attivare il tuo GPS per camion.",
   date="Dal 27 al 30 novembre", prix='<p style="text-align:center;"><span style="font-family: Arial, Helvetica, sans-serif; color: rgb(255, 255, 26); font-size: 48px;"><strong>37,99 €/anno&nbsp;</strong></span><span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; color: rgb(255, 255, 255);">invece di <s>74,99 €/anno</s></span></p>', bouton="Approfittane a 37,99 €/anno*", note="*Solo 5000 codici disponibili", t1="Lasciati tentare dal Black Friday!", t2="Non lasciarti sfuggire questa occasione.",
   a=[("Un GPS che conosce il tuo camion", "Il GPS MICHELIN Truckfly tiene conto di tutti i vincoli del tuo camion: <strong>sagoma, peso e restrizioni...</strong>"),
      ("Le restrizioni, visibili prima di arrivarci", "Ponti troppo bassi, limiti di peso: anticipa ogni vincolo direttamente sul tuo percorso."),
      ("La strada, sotto gli occhi di tutti", "Controlli, incidenti, ostacoli: la community MICHELIN Truckfly ti avvisa in tempo reale, e tu avvisi gli altri.")]),
 "DE": dict(img="6af57979041c447ff6e33fcb.png", y1="Sonderaktion -50%", y2="auf dein Jahresabo!", blanc="Nutze deine Pause und aktiviere dein Lkw-Navi.",
   date="Vom 27. bis 30. November", prix='<p style="text-align:center;"><span style="font-family: Arial, Helvetica, sans-serif; color: rgb(255, 255, 26); font-size: 48px;"><strong>37,99 €/Jahr&nbsp;</strong></span><span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; color: rgb(255, 255, 255);">statt <s>74,99 €/Jahr</s></span></p>', bouton="Jetzt für 37,99 €/Jahr sichern*", note="*Nur 5000 Codes verfügbar", t1="Lass dich vom Black Friday verführen!", t2="Lass dir diese Chance nicht entgehen.",
   a=[("Ein Navi, das deinen Lkw kennt", "Das MICHELIN Truckfly Navi berücksichtigt alle Vorgaben deines Lkw: <strong>Abmessungen, Gewicht und Beschränkungen...</strong>"),
      ("Beschränkungen sehen, bevor du da bist", "Zu niedrige Brücken, Gewichtsgrenzen: erkenne jede Einschränkung direkt auf deiner Route."),
      ("Die Straße im Blick aller", "Kontrollen, Unfälle, Hindernisse: die MICHELIN Truckfly Community warnt dich in Echtzeit, und du warnst die anderen.")]),
 "NL": dict(img="6af57992041c447ff6e33fd2.png", y1="Uitzonderlijke actie -50%", y2="op je jaarabonnement!", blanc="Benut je pauze om je vrachtwagen-GPS te activeren.",
   date="Van 27 tot en met 30 november", prix='<p style="text-align:center;"><span style="font-family: Arial, Helvetica, sans-serif; color: rgb(255, 255, 26); font-size: 48px;"><strong>€ 37,99/jaar&nbsp;</strong></span><span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; color: rgb(255, 255, 255);">in plaats van <s>€ 74,99/jaar</s></span></p>', bouton="Profiteer nu voor € 37,99/jaar*", note="*Slechts 5000 codes beschikbaar", t1="Laat je verleiden door Black Friday!", t2="Laat deze kans niet liggen.",
   a=[("Een GPS die je vrachtwagen kent", "De MICHELIN Truckfly GPS houdt rekening met alle beperkingen van je vrachtwagen: <strong>afmetingen, gewicht en restricties...</strong>"),
      ("Restricties zien voordat je er bent", "Te lage bruggen, tonnagebeperkingen: zie elke beperking direct op je route aankomen."),
      ("De weg, in de gaten gehouden door iedereen", "Controles, ongelukken, obstakels: de MICHELIN Truckfly community waarschuwt je in realtime, en jij waarschuwt op jouw beurt.")]),
 "PL": dict(img="6af579af01dbfb6057e2cbd7.png", y1="Wyjątkowa promocja -50%", y2="na roczną subskrypcję!", blanc="Wykorzystaj przerwę, aby aktywować GPS dla ciężarówek.",
   date="Od 27 do 30 listopada", code="Kod BF50", bouton="Skorzystaj*", note="*Dostępnych tylko 5000 kodów", t1="Daj się skusić na Black Friday!", t2="Nie przegap tej okazji.",
   a=[("GPS, który zna Twoją ciężarówkę", "GPS MICHELIN Truckfly uwzględnia wszystkie ograniczenia Twojej ciężarówki: <strong>gabaryty, masę i zakazy...</strong>"),
      ("Ograniczenia widoczne, zanim tam dojedziesz", "Za niskie mosty, limity tonażu: przewiduj każde ograniczenie bezpośrednio na swojej trasie."),
      ("Droga pod okiem wszystkich", "Kontrole, wypadki, przeszkody: społeczność MICHELIN Truckfly ostrzega Cię w czasie rzeczywistym, a Ty ostrzegasz innych.")]),
 "PT": dict(img="6af31ebe0ee2d874fa69e8b8.png", y1="Promoção excecional -50%", y2="na tua subscrição anual!", blanc="Aproveita a tua paragem para ativar o teu GPS para camiões.",
   date="De 27 a 30 de novembro", prix='<p style="text-align:center;"><span style="font-family: Arial, Helvetica, sans-serif; color: rgb(255, 255, 26); font-size: 48px;"><strong>37,99 €/ano&nbsp;</strong></span><span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; color: rgb(255, 255, 255);">em vez de <s>74,99 €/ano</s></span></p>', bouton="Aproveita por 37,99 €/ano*", note="*Apenas 5000 códigos disponíveis", t1="Deixa-te tentar pela Black Friday!", t2="Não percas esta oportunidade.",
   a=[("Um GPS que conhece o teu camião", "O GPS MICHELIN Truckfly tem em conta todas as restrições do teu camião: <strong>dimensões, peso e limitações...</strong>"),
      ("As restrições, visíveis antes de lá chegares", "Pontes demasiado baixas, limites de tonelagem: antecipa cada restrição diretamente no teu itinerário."),
      ("A estrada, sob a vigilância de todos", "Controlos, acidentes, obstáculos: a comunidade MICHELIN Truckfly avisa-te em tempo real, e tu avisas os outros.")]),
 "RO": dict(img="A_IMPORTER_banniere-brevo-2030x889-ro.png", y1="Promoție excepțională -50%", y2="la abonamentul tău anual!", blanc="Profită de pauză ca să-ți activezi GPS-ul pentru camion.",
   date="Între 27 și 30 noiembrie", code="Cod BF50", bouton="Profită acum*", note="*Doar 5000 de coduri disponibile", t1="Lasă-te tentat de Black Friday!", t2="Nu rata această ocazie.",
   a=[("Un GPS care îți cunoaște camionul", "GPS-ul MICHELIN Truckfly ține cont de toate constrângerile camionului tău: <strong>gabarit, greutate și restricții...</strong>"),
      ("Restricțiile, vizibile înainte să ajungi", "Poduri prea joase, limite de tonaj: anticipează fiecare constrângere direct pe traseul tău."),
      ("Drumul, sub ochii tuturor", "Controale, accidente, obstacole: comunitatea MICHELIN Truckfly te anunță în timp real, iar tu îi anunți pe ceilalți.")]),
}

SPAN = 'font-family: Arial, Helvetica, sans-serif;'
def header_bloc(l):
    t1, t2, lien, lp = HEADER[l]
    c = cond(l)
    html = (f'<p style="color: rgb(59, 63, 68); font-family: arial, helvetica, sans-serif; font-size: 16px;"><span style="font-size: 11px; color: rgb(255, 255, 255);">{esc(t1)}&nbsp;</span><br>'
            f'<span style="font-size: 11px; color: rgb(255, 255, 255);">{esc(t2)}&nbsp;<a href="{LP.format(lp)}" type="absoluteLink" target="_blank" rel="noopener noreferrer" style="color: rgb(0, 146, 255); text-decoration: underline;"><strong>{esc(lien)}</strong></a></span></p>')
    return f"""                -
                  condition: '{c}'
                  id: {uid()}
                  title: Text
                  type: text
                  layout:
                    320px:
                      width: 100%
                    default:
                      align: left
                      background-color: '#0c165b'
                      groupPadding: false
                      line-height: '1'
                      padding-bottom: 20px
                      padding-left: 0px
                      padding-top: 0px
                      text-align: center
                      text-valign: top
                      valign: top
                      width: 100%
                  content: '{html}'
"""

def bandeau(l):
    d = B[l]; c = cond(l)
    titre = (f'<h2 class="default-heading2" style="text-align:center;"><span style="{SPAN} color: rgb(255, 255, 26); font-size: 36px;">{esc(d["y1"])}</span></h2>'
             f'<h2 class="default-heading2" style="text-align:center;"><span style="{SPAN} color: rgb(255, 255, 26); font-size: 26px;">{esc(d["y2"])}</span></h2>'
             f'<h2 class="default-heading2"><span style="{SPAN} color: rgb(255, 255, 255);">{esc(d["blanc"])}</span></h2>')
    bas = d.get("prix") or (f'<p style="text-align:center;"><span style="{SPAN} color: rgb(255, 255, 26); font-size: 48px;"><strong>{esc(d["code"])}</strong></span></p>')
    prix = f'<p style="text-align:center;"><span style="{SPAN} font-size: 24px; color: rgb(255, 255, 255);"><strong>{esc(d["date"])}</strong></span></p>' + bas
    bouton = f'<p><span style="{SPAN} font-size: 22px; color: rgb(0, 0, 0);"><strong>{esc(d["bouton"])}</strong></span></p>'
    note = f'<p style="text-align:center;"><span style="{SPAN}"><em>{esc(d["note"])}</em></span></p>'
    fin = (f'<p style="text-align:center;"><span style="{SPAN}font-size:26px;color:rgb(0, 0, 0);"><strong>{esc(d["t1"])}</strong></span><span style="color: rgb(0, 0, 0);"><br></span>'
           f'<span style="{SPAN} font-size: 24px; color: rgb(0, 0, 0);">{esc(d["t2"])}</span></p>')
    av = lambda t, x: (f'<p style="text-align: center;"><strong><span style="font-family: Arial, helvetica, sans-serif; font-size: 16px; color: rgb(0, 0, 0);">{esc(t)}</span></strong></p>'
                       f'<p style="text-align: center;"><span style="font-family: Arial, helvetica, sans-serif; font-size: 16px; color: rgb(0, 0, 0);"><br></span></p>'
                       f'<p style="text-align: center;"><span style="font-family: Arial, helvetica, sans-serif; font-size: 16px; color: rgb(0, 0, 0);">{esc(x)}</span></p>')
    div = f"""                -
                  id: {{}}
                  thumbnail: /assets/img/editor/element_divider.svg
                  title: Diviseur
                  type: divider
                  layout:
                    320px:
                      display: rows
                      padding-bottom: 10px
                      padding-top: 10px
                      width: 100%
                    default:
                      align: center
                      border-color: '#fac96b'
                      border-style: solid
                      border-width: 2px
                      color: '#3b3f44'
                      display: none
                      font-family: 'arial,helvetica,sans-serif'
                      font-size: 16px
                      padding-bottom: 30px
                      padding-top: 30px
                      showHide: true
                      showOnDesktopMobile: mobile
                      width: 100%
"""
    col = lambda img, txt: f"""            -
              id: {uid()}
              isEmpty: false
              stylable: false
              title: 'colonne de grille'
              type: grid-column
              layout:
                320px: {{}}
                default:
                  color: '#314251'
                  font-family: 'arial,helvetica,sans-serif'
                  font-size: 15px
                  padding-left: 0px
                  padding-right: 0px
                  valign: top
              content:
{img}                -
                  id: {uid()}
                  thumbnail: /assets/img/editor/element_text.svg
                  title: Texte
                  type: text
                  layout:
                    320px:
                      text-align: center
                      width: 100%
                    default:
                      align: left
                      color: '#314251'
                      font-family: 'arial,helvetica,sans-serif'
                      font-size: 15px
                      line-height: '1.5'
                      padding-bottom: 15px
                      padding-top: 15px
                      text-align: center
                      text-valign: top
                      valign: top
                      width: 100%
                  content: '{txt}'
""" + div.format(uid())
    image = lambda src, w, h, w320, extra="": f"""                -
                  id: {uid()}
                  thumbnail: /assets/img/editor/element_image.svg
                  title: Image
                  type: image
                  layout:
                    320px:
                      max-width: 320px
                      width: {w320}
                    default:
                      align: center
                      canvas-height: {h}
{extra}                      img-border-radius: 0px
                      opacity: 1
                      padding-bottom: 0px
                      padding-top: 0px
                      type: absoluteLink
                      valign: top
                      width: {w}
                  content:
                    href: 'https://www.truckfly.com/purchase-gps'
                    src: '{IMG}{src}'
"""
    m30 = "                      margin-bottom: 30px\n                      margin-top: 30px\n                      removeMargin: true\n"
    imgs = [image("6aba5d50ed19425e80b928be.png", "100%", "118px", "80%", m30),
            image("69660b7f0c0a6303df64a860.png", "85%", "217px", "75%"),
            image("6aba5cd235e299bb2f779337.png", "95%", "152px", "80%", "                      margin-top: 30px\n                      removeMargin: true\n")]
    ligne = lambda titre_l, extra_layout, contenu, dist="'12'", gutter="30px", stylable="": f"""        -
          align: top
          condition: '{c}'
          dist: {dist}
          gutter: {gutter}
          id: {uid()}
          moduleName: grid-row12
{stylable}          thumbnail: /assets/img/editor/grid_12.svg
          title: '{titre_l}'
          type: grid-row
          layout:
{extra_layout}          content:
{contenu}"""
    lay_noir = lambda pb, pt: f"""            320px:
              display: rows
              padding-left: 15px
              padding-right: 15px
              width: 100%
            default:
              align: center
              background-color: '#000000'
              padding-bottom: {pb}
              padding-top: {pt}
              valign: top
              width: 100%
"""
    r1 = ligne(f"Bannière {l}", lay_noir("10px", "10px"), f"""            -
              id: {uid()}
              isEmpty: false
              title: 'column 1'
              type: grid-column
              layout:
                320px: []
                default:
                  padding-left: 0px
                  padding-right: 0px
                  valign: top
              content:
                -
                  id: {uid()}
                  moduleName: text-title
                  thumbnail: /assets/img/editor/element-title.svg
                  title: Titre
                  type: text
                  layout:
                    320px:
                      width: 100%
                    default:
                      align: left
                      background-color: '#000000'
                      line-height: '2'
                      padding-bottom: 15px
                      padding-left: 30px
                      padding-right: 30px
                      padding-top: 15px
                      text-align: left
                      text-valign: top
                      valign: top
                      width: 100%
                  content: '{titre}'
                -
                  id: {uid()}
                  title: Image
                  type: image
                  layout:
                    320px:
                      max-width: 320px
                      width: 100%
                    default:
                      align: center
                      canvas-height: 250px
                      padding-bottom: 15px
                      padding-top: 15px
                      valign: top
                      width: 100%
                  content:
                    src: '{IMG}{d["img"]}'
""")
    r2 = ligne(f"Bannière {l} {'prix' if d.get('prix') else 'code'}", lay_noir("20px", "20px"), f"""            -
              id: {uid()}
              isEmpty: false
              stylable: false
              title: Column
              type: grid-column
              layout:
                320px: {{}}
                default:
                  padding-left: 0px
                  padding-right: 0px
                  valign: top
              content:
                -
                  id: {uid()}
                  moduleName: text-title
                  thumbnail: /assets/img/editor/element-title.svg
                  title: Titre
                  type: text
                  layout:
                    320px:
                      width: 100%
                    default:
                      align: left
                      background-color: '#000000'
                      padding-top: 15px
                      text-align: left
                      text-valign: top
                      valign: top
                      width: 100%
                  content: '{prix}'
""", stylable="          stylable: false\n")
    r3 = ligne(f"Bannière {l} bouton", """            320px:
              display: rows
              padding-left: 0px
              padding-right: 0px
              width: 100%
            default:
              align: center
              padding-bottom: 10px
              padding-top: 0px
              valign: top
              width: 100%
""", f"""            -
              id: {uid()}
              isEmpty: false
              title: 'column 1'
              type: grid-column
              layout:
                320px: []
                default:
                  item-width: 26px
                  padding-left: 0px
                  padding-right: 0px
                  valign: top
              content:
                -
                  id: {uid()}
                  text: '{bouton}'
                  title: Button
                  type: text-button
                  layout:
                    320px:
                      width: 100%
                    default:
                      align: center
                      background-color: '#ffff1a'
                      border-radius: 12px
                      item-height: 67px
                      margin-bottom: 0px
                      margin-top: 15px
                      padding-bottom: 21px
                      padding-top: 21px
                      text-align: center
                      text-valign: top
                      type: absoluteLink
                      valign: top
                      width: 86%
                  content:
                    href: 'https://www.truckfly.com/add-promo-code?promoCode=BF50'
                    text: '{bouton}'
                    title: ""
                -
                  id: {uid()}
                  moduleName: text-title
                  thumbnail: /assets/img/editor/element-title.svg
                  title: Titre
                  type: text
                  layout:
                    320px:
                      width: 100%
                    default:
                      align: left
                      padding-top: 0px
                      text-align: left
                      text-valign: top
                      valign: top
                      width: 100%
                  content: '{note}'
                -
                  id: {uid()}
                  moduleName: text-title
                  thumbnail: /assets/img/editor/element-title.svg
                  title: Titre
                  type: text
                  layout:
                    320px:
                      width: 100%
                    default:
                      align: left
                      padding-top: 15px
                      text-align: left
                      text-valign: top
                      valign: top
                      width: 100%
                  content: '{fin}'
""", gutter="0px")
    r4 = ligne(f"Bannière {l} avantages", """            320px:
              display: rows
              padding-bottom: 0px
              padding-left: 15px
              padding-right: 15px
              width: 100%
            default:
              align: center
              background-color: '#fdfbfb'
              color: '#314251'
              font-family: 'arial,helvetica,sans-serif'
              font-size: 15px
              padding-bottom: 20px
              padding-top: 20px
              valign: top
              width: 100%
""", "".join(col(imgs[i], av(*d["a"][i])) for i in range(3)), dist="4-4-4")
    return r1 + r2 + r3 + r4

out = (ICI / "source" / "debut.yaml").read_text()
out += "".join(header_bloc(l) for l in LANGS)
out += "".join(bandeau(l) for l in LANGS)
out += (ICI / "source" / "fin.yaml").read_text()
dest = ICI / "template_black_friday_9_langues.yaml"
dest.write_text(out)
print(dest)
