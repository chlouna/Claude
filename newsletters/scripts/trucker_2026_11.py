"""Newsletter Trucker de novembre 2026 au format « Le Relais », FR / IT / ES avec conditions LANG Brevo.
python3 newsletters/scripts/trucker_2026_11.py
Produit : brevo.html (à coller dans Brevo), apercu-fr.html, apercu-it.html, apercu-es.html (aperçus sans conditions).
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from templates_v2 import page, bouton, ligne, etiquette, titre, texte, F, BLEU, JAUNE, CREME, NOIR, GRIS

SORTIE = Path(__file__).resolve().parent.parent / "trucker" / "2026-11"
IMG = "https://7fn4t.img.bh.d.sendibt3.com/im/sh/"
U = "?u=92pJLo34vnrQ"
IMAGES = {  # images déjà chargées dans Brevo (campagne 619)
    "loi": IMG + "sHxZFukM5YDd.jpg" + U + "tqmwrb6XiprQpQ9VusGVoNI",
    "alerte": IMG + "nIhPFfqllsCM.png" + U + "u6N4w1dFtnCyJjjnUeV1DbY",
    "top": IMG + "J-MiGMgA3s6u.png" + U + "uTkH2fQKAEEHYD7DrJqmKRw",
}
LANGS = ["FR", "IT", "ES"]

T = {
"FR": dict(
    numero="N° [12] · Novembre 2026", sous="Le rendez-vous des routiers de la communauté Michelin Truckfly",
    gps="L'appli gratuite préférée des routiers en Europe. Et pour ceux qui en veulent plus :", gps_lien_txt="un GPS en option !", gps_lien="LIEN-GPS-FR",
    edito_tag="L'ÉDITO", accroche="Tu as bien tes chaînes dans le camion ?", salut="Salut {{ contact.PRENOM | default : \"la route\" }},",
    edito=["Chaque jour, des milliers de conducteurs <strong>roulent, partagent et font vivre la communauté Michelin Truckfly.</strong>",
           "Avec novembre, l'hiver s'installe sur la route : nouvelles obligations en montagne, routes glissantes, conditions qui changent vite… Autant de raisons de bien <strong>préparer tes trajets et de partager les bonnes infos.</strong>",
           "Ce mois-ci, découvre <strong>ce qui devient obligatoire dès le 1er novembre</strong> et comment aider les autres conducteurs face aux dangers de l'hiver. Sans oublier le top contributeur d'octobre… et nos astuces pour prendre sa place !"],
    signe="[Prénom]", role="[rôle] chez Michelin Truckfly",
    prog_tag="AU PROGRAMME",
    prog=["Chaînes, pneus hiver : es-tu en règle ?", "Route glissante, brouillard : préviens les autres", "Deviens le meilleur contributeur", "Le top contributeur d'octobre"],
    s1_tag="1 · LOI MONTAGNE", s1_titre="Chaînes, pneus hiver : es-tu en règle ?",
    s1=["<strong>Le savais-tu ?</strong> Dès ce <strong>dimanche 1er novembre et jusqu'au 31 mars</strong>, la <strong>Loi Montagne</strong> s'applique dans certaines communes de montagne en France. Elles sont signalées par un panneau à l'entrée de la zone."],
    s1_liste_tit="Et les poids lourds sont concernés :",
    s1_liste=["<strong>PL avec remorque ou semi-remorque</strong> : chaînes obligatoires dans le camion pour équiper <strong>au moins deux roues motrices</strong>, même si tu roules en pneus hiver.",
              "<strong>PL sans remorque</strong> : au choix, <strong>chaînes</strong> ou <strong>pneus hiver</strong>."],
    s1_suite=["<strong>Attention aux pneus :</strong> seuls les pneus marqués du <strong>symbole 3PMSF</strong> (la montagne à trois pics avec un flocon) comptent comme équipement hiver. Les autres pneus « neige » ne suffisent pas seuls : il te faut aussi des chaînes.",
              "<strong>Camions étrangers aussi concernés !</strong> Pour l'instant, pas d'amende. Mais sans équipement, les forces de l'ordre peuvent te refuser l'accès à la zone, et ton assurance peut réduire ou refuser ton indemnisation en cas d'accident."],
    check_tit="Ta checklist avant de partir",
    check=["<strong>Vérifie tes pneus</strong> : le symbole 3PMSF est-il bien présent ?", "<strong>Contrôle tes chaînes</strong> : elles sont dans le camion, en bon état, et tu sais les monter."],
    s1_btn="Je prépare mon trajet",
    s2_tag="2 · LE TUTO DU MOIS", s2_titre="Route glissante, brouillard, accident : préviens les autres !",
    s2=["<strong>Brouillard épais, route glissante, accident, bouchon…</strong> Sur la route, une info partagée au bon moment peut éviter bien des galères à un autre conducteur.",
        "Sur Michelin Truckfly, tu peux <strong>signaler une alerte en quelques secondes</strong>, directement depuis la carte. Elle s'affiche alors pour toute la communauté qui roule dans le secteur."],
    pour_signaler="Pour signaler", etapes_signaler=["Ouvre l'appli", "Appuie sur le bouton d'alerte", "Choisis le type de danger : c'est envoyé !"],
    pour_anticiper="Pour anticiper", etapes_anticiper=["Lance ton itinéraire", "Regarde les alertes signalées sur ta route", "Adapte ton trajet si besoin"],
    s2_btn="Je signale une alerte",
    s3_tag="3 · LA COMMUNAUTÉ", s3_titre="Deviens le meilleur contributeur du mois",
    s3=["Sur la route, on fait confiance à ceux qui partagent les bonnes infos. <strong>Un conducteur avec beaucoup de points de contribution, c'est un conducteur fiable</strong> : quand il signale une alerte ou note un arrêt, la communauté sait qu'elle peut compter dessus.",
        "Et la règle est simple : <strong>chaque action vaut 1 point.</strong> Une pause café suffit pour en gagner plusieurs !"],
    regle="1 action = 1 point",
    actions=[("Ajouter une photo", "Parking, entrée, douches…"), ("Laisser un avis", "Note ou commente un arrêt"),
             ("Liker une photo ou une activité", "Encourage les autres conducteurs"), ("Mettre à jour un lieu", "Horaires, services, accès"),
             ("Ajouter un lieu", "Un arrêt pas encore sur l'appli"), ("Signaler une alerte", "Neige, accident, danger…")],
    s3_fin="<strong>Plus tu as de points, plus ta parole compte.</strong> Prêt à grimper au classement ?", s3_btn="Je gagne des points",
    top_tag="4 · BRAVO !", top_titre="Les meilleurs contributeurs du mois d'octobre", top_btn="C'est mon tour !",
    mot_tag="LE MOT DE LA ROUTE",
    mot=["Un grand merci à toute la communauté Michelin Truckfly pour sa fidélité et ses contributions au quotidien.",
         "On se retrouve très bientôt pour de <strong>nouvelles actus, astuces et infos utiles pour tes trajets.</strong>",
         "<strong>D'ici là, prends soin de toi, sois prudent sur la route et bonne route !</strong>"],
    equipe="L'équipe Michelin Truckfly",
    faq_tit="Une question ? Un problème ?", faq="Consulte notre FAQ ou contacte-nous :",
    raison="Tu reçois cet e-mail car tu t'es inscrit à l'application mobile Michelin Truckfly.", desinscription="Se désinscrire",
    alt_loi="Loi Montagne : chaînes et pneus hiver", alt_alerte="Signaler une alerte dans l'app", alt_top="Les meilleurs contributeurs d'octobre",
),
"IT": dict(
    numero="N° [12] · Novembre 2026", sous="L'appuntamento degli autisti della community Michelin Truckfly",
    gps="L'app gratuita preferita dagli autisti di camion in Europa. E per chi vuole di più:", gps_lien_txt="GPS disponibile come opzione!", gps_lien="https://lp.truckfly.com/it/gps-premium",
    edito_tag="L'EDITORIALE", accroche="Hai le catene nel camion?", salut="Ciao {{ contact.PRENOM | default : \"camionista\" }},",
    edito=["Ogni giorno, migliaia di autisti <strong>viaggiano, condividono e fanno vivere la community Michelin Truckfly.</strong>",
           "Con novembre, l'inverno arriva sulla strada: nuovi obblighi in montagna, strade scivolose, condizioni che cambiano in fretta… Tanti buoni motivi per <strong>preparare bene i tuoi viaggi e condividere le info giuste.</strong>",
           "Questo mese scopri <strong>cosa diventa obbligatorio in Francia dal 1° novembre</strong> e come aiutare gli altri autisti contro i pericoli dell'inverno. Senza dimenticare il top contributore di ottobre… e i nostri consigli per prendere il suo posto!"],
    signe="[Nome]", role="[ruolo] in Michelin Truckfly",
    prog_tag="IN QUESTO NUMERO",
    prog=["Catene, pneumatici invernali: sei in regola?", "Strada scivolosa, nebbia: avvisa gli altri", "Diventa il miglior contributore", "Il top contributore di ottobre"],
    s1_tag="1 · LOI MONTAGNE", s1_titre="Catene, pneumatici invernali: sei in regola?",
    s1=["<strong>Lo sapevi?</strong> Viaggi in Francia? Da <strong>domenica 1° novembre fino al 31 marzo</strong>, la <strong>Loi Montagne</strong> (la legge francese sulla montagna) si applica in alcuni comuni di montagna in Francia. Sono segnalati da un cartello all'ingresso della zona."],
    s1_liste_tit="E i mezzi pesanti sono interessati:",
    s1_liste=["<strong>Camion con rimorchio o semirimorchio</strong>: catene obbligatorie a bordo per equipaggiare <strong>almeno due ruote motrici</strong>, anche se monti pneumatici invernali.",
              "<strong>Camion senza rimorchio</strong>: a scelta, <strong>catene</strong> o <strong>pneumatici invernali</strong>."],
    s1_suite=["<strong>Attenzione ai pneumatici:</strong> valgono come equipaggiamento invernale solo i pneumatici con il <strong>simbolo 3PMSF</strong> (la montagna a tre punte con il fiocco di neve). Gli altri pneumatici «da neve» da soli non bastano: servono anche le catene.",
              "<strong>Anche i camion stranieri sono interessati!</strong> Per ora non sono previste multe. Ma senza equipaggiamento le forze dell'ordine possono vietarti l'accesso alla zona e la tua assicurazione può ridurre o rifiutare il risarcimento in caso di incidente."],
    check_tit="La tua checklist prima di partire",
    check=["<strong>Controlla i pneumatici</strong>: c'è il simbolo 3PMSF?", "<strong>Controlla le catene</strong>: sono nel camion, in buono stato, e sai come montarle."],
    s1_btn="Preparo il mio viaggio",
    s2_tag="2 · IL TUTORIAL DEL MESE", s2_titre="Strada scivolosa, nebbia, incidente: avvisa gli altri!",
    s2=["<strong>Nebbia fitta, strada scivolosa, incidente, coda…</strong> Sulla strada, un'info condivisa al momento giusto può evitare tanti problemi a un altro autista.",
        "Su Michelin Truckfly puoi <strong>inviare una segnalazione in pochi secondi</strong>, direttamente dalla mappa. Viene poi mostrata a tutta la community che viaggia nella zona."],
    pour_signaler="Per segnalare", etapes_signaler=["Apri l'app", "Tocca il pulsante di segnalazione", "Scegli il tipo di pericolo: è inviata!"],
    pour_anticiper="Per anticipare", etapes_anticiper=["Avvia il tuo itinerario", "Guarda le segnalazioni sul tuo percorso", "Adatta il viaggio se serve"],
    s2_btn="Invio una segnalazione",
    s3_tag="3 · LA COMMUNITY", s3_titre="Diventa il miglior contributore del mese",
    s3=["Sulla strada, ci si fida di chi condivide le info giuste. <strong>Un autista con tanti punti contributo è un autista affidabile</strong>: quando segnala un pericolo o valuta una sosta, la community sa di poter contare su di lui.",
        "E la regola è semplice: <strong>ogni azione vale 1 punto.</strong> Basta una pausa caffè per guadagnarne diversi!"],
    regle="1 azione = 1 punto",
    actions=[("Aggiungere una foto", "Parcheggio, ingresso, docce…"), ("Lasciare una recensione", "Valuta o commenta una sosta"),
             ("Mettere like a una foto o a un'attività", "Incoraggia gli altri autisti"), ("Aggiornare un luogo", "Orari, servizi, accesso"),
             ("Aggiungere un luogo", "Una sosta non ancora sull'app"), ("Inviare una segnalazione", "Neve, incidente, pericolo…")],
    s3_fin="<strong>Più punti hai, più la tua parola conta.</strong> Pronto a scalare la classifica?", s3_btn="Guadagno punti",
    top_tag="4 · BRAVI!", top_titre="I migliori contributori del mese di ottobre", top_btn="Tocca a me!",
    mot_tag="L'ULTIMA PAROLA",
    mot=["Un grande grazie a tutta la community Michelin Truckfly per la sua fedeltà e i suoi contributi quotidiani.",
         "Ci ritroviamo molto presto con <strong>nuove notizie, consigli e info utili per i tuoi viaggi.</strong>",
         "<strong>Nel frattempo, abbi cura di te, sii prudente e buona strada!</strong>"],
    equipe="Il team Michelin Truckfly",
    faq_tit="Una domanda? Un problema?", faq="Consulta le nostre FAQ o contattaci:",
    raison="Ricevi questa email perché sei registrato sull'app mobile Michelin Truckfly.", desinscription="Annulla l'iscrizione",
    alt_loi="Loi Montagne: catene e pneumatici invernali", alt_alerte="Inviare una segnalazione nell'app", alt_top="I migliori contributori di ottobre",
),
"ES": dict(
    numero="N.º [12] · Noviembre 2026", sous="La cita de los camioneros de la comunidad Michelin Truckfly",
    gps="La app gratuita preferida por los camioneros en Europa. Y para quienes quieren más:", gps_lien_txt="¡GPS disponible como opción!", gps_lien="https://lp.truckfly.com/es/gps-premium",
    edito_tag="EL EDITORIAL", accroche="¿Llevas las cadenas en el camión?", salut="Hola, {{ contact.PRENOM | default : \"camionero\" }}:",
    edito=["Cada día, miles de camioneros <strong>circulan, comparten y dan vida a la comunidad Michelin Truckfly.</strong>",
           "Con noviembre, el invierno llega a la carretera: nuevas obligaciones en montaña, carreteras resbaladizas, condiciones que cambian rápido… Razones de sobra para <strong>preparar bien tus rutas y compartir la información correcta.</strong>",
           "Este mes descubre <strong>qué pasa a ser obligatorio en Francia a partir del 1 de noviembre</strong> y cómo ayudar a otros camioneros frente a los peligros del invierno. Sin olvidar al mejor colaborador de octubre… ¡y nuestros consejos para quitarle el puesto!"],
    signe="[Nombre]", role="[cargo] en Michelin Truckfly",
    prog_tag="EN ESTE NÚMERO",
    prog=["Cadenas, neumáticos de invierno: ¿estás en regla?", "Carretera resbaladiza, niebla: avisa a los demás", "Conviértete en el mejor colaborador", "El mejor colaborador de octubre"],
    s1_tag="1 · LOI MONTAGNE", s1_titre="Cadenas, neumáticos de invierno: ¿estás en regla?",
    s1=["<strong>¿Lo sabías?</strong> ¿Circulas por Francia? Desde el <strong>domingo 1 de noviembre hasta el 31 de marzo</strong>, la <strong>Loi Montagne</strong> (la ley francesa de montaña) se aplica en algunos municipios de montaña de Francia. Están señalizados con un panel a la entrada de la zona."],
    s1_liste_tit="Y los camiones también están afectados:",
    s1_liste=["<strong>Camión con remolque o semirremolque</strong>: cadenas obligatorias a bordo para equipar <strong>al menos dos ruedas motrices</strong>, aunque lleves neumáticos de invierno.",
              "<strong>Camión sin remolque</strong>: a elegir, <strong>cadenas</strong> o <strong>neumáticos de invierno</strong>."],
    s1_suite=["<strong>Ojo con los neumáticos:</strong> solo cuentan como equipamiento de invierno los neumáticos con el <strong>símbolo 3PMSF</strong> (la montaña de tres picos con un copo de nieve). Los demás neumáticos «de nieve» no bastan por sí solos: también necesitas cadenas.",
              "<strong>¡Los camiones extranjeros también están afectados!</strong> De momento no hay multas. Pero sin equipamiento, las fuerzas del orden pueden impedirte el acceso a la zona y tu seguro puede reducir o rechazar la indemnización en caso de accidente."],
    check_tit="Tu checklist antes de salir",
    check=["<strong>Revisa tus neumáticos</strong>: ¿llevan el símbolo 3PMSF?", "<strong>Comprueba tus cadenas</strong>: están en el camión, en buen estado, y sabes montarlas."],
    s1_btn="Preparo mi ruta",
    s2_tag="2 · EL TUTORIAL DEL MES", s2_titre="Carretera resbaladiza, niebla, accidente: ¡avisa a los demás!",
    s2=["<strong>Niebla espesa, carretera resbaladiza, accidente, atasco…</strong> En la carretera, una información compartida en el momento justo puede ahorrarle muchos problemas a otro camionero.",
        "En Michelin Truckfly puedes <strong>enviar un aviso en pocos segundos</strong>, directamente desde el mapa. Se muestra a toda la comunidad que circula por la zona."],
    pour_signaler="Para avisar", etapes_signaler=["Abre la app", "Pulsa el botón de aviso", "Elige el tipo de peligro: ¡enviado!"],
    pour_anticiper="Para anticiparte", etapes_anticiper=["Lanza tu ruta", "Mira los avisos de tu trayecto", "Adapta tu viaje si hace falta"],
    s2_btn="Envío un aviso",
    s3_tag="3 · LA COMUNIDAD", s3_titre="Conviértete en el mejor colaborador del mes",
    s3=["En la carretera, confiamos en quienes comparten buena información. <strong>Un camionero con muchos puntos de contribución es un camionero de confianza</strong>: cuando avisa de un peligro o valora una parada, la comunidad sabe que puede contar con él.",
        "Y la regla es sencilla: <strong>cada acción vale 1 punto.</strong> ¡Con una pausa para el café ya puedes ganar varios!"],
    regle="1 acción = 1 punto",
    actions=[("Añadir una foto", "Parking, entrada, duchas…"), ("Dejar una reseña", "Valora o comenta una parada"),
             ("Dar like a una foto o actividad", "Anima a otros camioneros"), ("Actualizar un lugar", "Horarios, servicios, acceso"),
             ("Añadir un lugar", "Una parada que aún no está en la app"), ("Enviar un aviso", "Nieve, accidente, peligro…")],
    s3_fin="<strong>Cuantos más puntos tienes, más cuenta tu palabra.</strong> ¿Listo para subir en la clasificación?", s3_btn="Gano puntos",
    top_tag="4 · ¡ENHORABUENA!", top_titre="¡Los mejores colaboradores del mes de octubre!", top_btn="¡Me toca!",
    mot_tag="LA ÚLTIMA PALABRA",
    mot=["Muchas gracias a toda la comunidad Michelin Truckfly por su fidelidad y sus contribuciones diarias.",
         "Nos vemos muy pronto con <strong>nuevas noticias, consejos e información útil para tus rutas.</strong>",
         "<strong>Mientras tanto, cuídate, sé prudente en la carretera y ¡buen viaje!</strong>"],
    equipe="El equipo de Michelin Truckfly",
    faq_tit="¿Una pregunta? ¿Un problema?", faq="Consulta nuestra FAQ o contáctanos:",
    raison="Recibes este correo porque estás registrado en la aplicación móvil Michelin Truckfly.", desinscription="Darse de baja",
    alt_loi="Loi Montagne: cadenas y neumáticos de invierno", alt_alerte="Enviar un aviso en la app", alt_top="Los mejores colaboradores de octubre",
),
}

LIENS = {"s1": "LIEN-PREPARER-TRAJET", "s2": "LIEN-SIGNALER-ALERTE", "s3": "LIEN-GAGNER-POINTS", "top": "LIEN-CLASSEMENT"}


def img(cle, alt, lien):
    return (f'<a href="{lien}" target="_blank"><img src="{IMAGES[cle]}" width="520" alt="{alt}" '
            f'style="display:block;width:100%;max-width:520px;height:auto;border-radius:12px;{F}font-size:14px;color:{BLEU};"></a>')


def puces(items, sur_bleu=False):
    c = "#FFFFFF" if sur_bleu else NOIR
    p = JAUNE if sur_bleu else BLEU
    return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 16px 0;">' + "".join(
        f'<tr><td width="22" valign="top" style="padding:0 0 10px 0;{F}font-size:18px;line-height:24px;color:{p};font-weight:bold;">•</td>'
        f'<td valign="top" style="padding:0 0 10px 0;{F}font-size:16px;line-height:24px;color:{c};">{x}</td></tr>' for x in items) + "</table>"


def etapes(titre_e, items):
    lignes = "".join(f'<tr><td width="34" valign="top" style="padding:0 0 10px 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" width="26" height="26" style="width:26px;height:26px;border-radius:13px;background-color:{JAUNE};{F}font-size:13px;line-height:26px;font-weight:bold;color:{BLEU};">{i}</td></tr></table></td><td style="padding:2px 0 10px 0;{F}font-size:15px;line-height:22px;color:#FFFFFF;">{x}</td></tr>'
                     for i, x in enumerate(items, 1))
    return (f'<td class="col" width="50%" valign="top" style="padding:0 8px 0 0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:#0F2479;border-radius:12px;padding:18px 18px 8px 18px;">'
            f'<p style="margin:0 0 12px 0;{F}font-size:15px;line-height:20px;font-weight:bold;color:{JAUNE};">{titre_e}</p>'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{lignes}</table></td></tr></table></td>')


def actions(acts):
    cells = []
    for i in range(0, len(acts), 2):
        row = ""
        for t_, d_ in acts[i:i + 2]:
            row += (f'<td class="col" width="50%" valign="top" style="padding:0 5px 10px 5px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFFFF;border-radius:12px;"><tr>'
                    f'<td width="46" valign="middle" style="padding:12px 0 12px 12px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" width="38" height="28" style="width:38px;height:28px;border-radius:8px;background-color:{JAUNE};{F}font-size:13px;line-height:28px;font-weight:bold;color:{BLEU};">+1</td></tr></table></td>'
                    f'<td valign="middle" style="padding:12px 12px 12px 10px;{F}"><p style="margin:0;font-size:14px;line-height:19px;font-weight:bold;color:{BLEU};">{t_}</p><p style="margin:2px 0 0 0;font-size:12px;line-height:17px;color:{GRIS};">{d_}</p></td>'
                    f'</tr></table></td>')
        cells.append(f"<tr>{row}</tr>")
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFFFF;border-radius:12px;">'
            .replace('style="background-color:#FFFFFF;border-radius:12px;"', 'style="margin:4px 0 16px 0;"') + "".join(cells) + "</table>")


def ancre(n):
    return f'<tr><td style="font-size:0;line-height:0;"><a name="bloc-{n}" id="bloc-{n}"></a></td></tr>'


def blocs(L, t):
    b = []
    # En-tête
    b.append(f"""<tr><td class="pad" style="background-color:{BLEU};padding:24px 40px 22px 40px;{F}">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
    <td valign="middle"><a href="LIEN-APP"><img src="../../assets/logo-truckfly-blanc.png" width="130" height="33" alt="Michelin Truckfly" style="width:130px;height:33px;{F}font-size:16px;font-weight:bold;color:#FFFFFF;"></a></td>
    <td valign="middle" align="right" style="{F}font-size:13px;line-height:18px;color:#FFFFFF;">{t['numero']}</td>
  </tr></table>
  <p style="margin:22px 0 0 0;{F}font-size:40px;line-height:44px;font-weight:bold;color:#FFFFFF;">Le Relais<span style="color:{JAUNE};">.</span></p>
  <p style="margin:4px 0 14px 0;{F}font-size:15px;line-height:21px;color:#C9CEDF;">{t['sous']}</p>
  <p style="margin:0;{F}font-size:12px;line-height:18px;color:#C9CEDF;">{t['gps']} <a href="{t['gps_lien']}" style="color:{JAUNE};font-weight:bold;">{t['gps_lien_txt']}</a></p>
</td></tr>""")
    # Édito
    b.append(ligne(etiquette(t["edito_tag"])
        + f'<h1 class="h1 t-fonce" style="margin:0 0 16px 0;{F}font-size:30px;line-height:36px;font-weight:bold;color:{BLEU};">{t["accroche"]}</h1>'
        + texte(t["salut"]) + "".join(texte(p) for p in t["edito"])
        + f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 0 0;"><tr>
  <td width="52" valign="middle"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" valign="middle" width="44" height="44" style="width:44px;height:44px;border-radius:22px;background-color:#DCE2F0;{F}font-size:11px;color:{BLEU};">[photo]</td></tr></table></td>
  <td valign="middle" style="{F}"><p class="t-fonce" style="margin:0;font-size:15px;line-height:20px;font-weight:bold;color:{NOIR};">{t['signe']}</p><p class="t-doux" style="margin:0;font-size:13px;line-height:18px;color:{GRIS};">{t['role']}</p></td>
</tr></table>""", pad="36px 40px 28px 40px"))
    # Au programme
    lignes = "".join(f'<tr><td width="28" valign="top" style="padding:0 0 10px 0;{F}font-size:15px;line-height:22px;font-weight:bold;color:{BLEU};">{i}.</td><td style="padding:0 0 10px 0;{F}font-size:15px;line-height:22px;"><a href="#bloc-{i}" style="color:{BLEU};font-weight:bold;">{p}</a></td></tr>' for i, p in enumerate(t["prog"], 1))
    b.append(ligne(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="creme" style="background-color:{CREME};border-radius:12px;padding:20px 22px 10px 22px;">{etiquette(t["prog_tag"])}<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{lignes}</table></td></tr></table>', pad="0 40px 36px 40px"))
    # 1. Loi Montagne
    b.append(ancre(1))
    b.append(ligne(etiquette(t["s1_tag"], True) + titre(t["s1_titre"], True)
        + "".join(texte(p, True) for p in t["s1"]) + texte(f'<strong>{t["s1_liste_tit"]}</strong>', True, "0 0 10px 0")
        + puces(t["s1_liste"], True) + "".join(texte(p, True) for p in t["s1_suite"])
        + img("loi", t["alt_loi"], LIENS["s1"])
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:20px 0 22px 0;"><tr><td style="background-color:{JAUNE};border-radius:12px;padding:18px 20px 6px 20px;{F}"><p style="margin:0 0 10px 0;font-size:16px;line-height:22px;font-weight:bold;color:{BLEU};">✓ {t["check_tit"]}</p>'
        + "".join(f'<p style="margin:0 0 12px 0;font-size:15px;line-height:22px;color:{BLEU};">☐ {x}</p>' for x in t["check"]) + "</td></tr></table>"
        + bouton(t["s1_btn"], LIENS["s1"], largeur=260), fond=BLEU, pad="36px 40px 40px 40px", classe=""))
    # 2. Alertes
    b.append(ancre(2))
    b.append(ligne(etiquette(t["s2_tag"], True) + titre(t["s2_titre"], True)
        + "".join(texte(p, True) for p in t["s2"])
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 20px 0;"><tr>{etapes(t["pour_signaler"], t["etapes_signaler"])}{etapes(t["pour_anticiper"], t["etapes_anticiper"]).replace("padding:0 8px 0 0", "padding:0 0 0 8px")}</tr></table>'
        + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="padding:0 0 22px 0;"><a href="{LIENS["s2"]}" target="_blank"><img src="{IMAGES["alerte"]}" width="240" alt="{t["alt_alerte"]}" style="display:block;width:240px;max-width:100%;height:auto;border-radius:12px;{F}font-size:14px;color:#FFFFFF;"></a></td></tr></table>'
        + bouton(t["s2_btn"], LIENS["s2"], largeur=260), fond="#0B1A4F", pad="36px 40px 40px 40px", classe=""))
    # 3. Contributeur
    b.append(ancre(3))
    b.append(ligne(etiquette(t["s3_tag"]) + titre(t["s3_titre"])
        + "".join(texte(p) for p in t["s3"])
        + f'<p style="margin:6px 0 12px 0;"><span style="display:inline-block;background-color:{BLEU};color:{JAUNE};{F}font-size:14px;font-weight:bold;border-radius:20px;padding:6px 14px;">{t["regle"]}</span></p>'
        + actions(t["actions"]) + texte(t["s3_fin"], marge="4px 0 18px 0")
        + bouton(t["s3_btn"], LIENS["s3"], fond=BLEU, couleur="#FFFFFF", largeur=240), fond=CREME, pad="36px 40px 40px 40px", classe="creme"))
    # 4. Top contributeurs
    b.append(ancre(4))
    b.append(ligne(etiquette(t["top_tag"]) + titre(t["top_titre"])
        + img("top", t["alt_top"], LIENS["top"]) + '<div style="height:20px;line-height:20px;font-size:0;">&nbsp;</div>'
        + bouton(t["top_btn"], LIENS["top"], fond=BLEU, couleur="#FFFFFF", largeur=220), pad="36px 40px 40px 40px"))
    # Mot de la route
    b.append(ligne(etiquette(t["mot_tag"]) + "".join(texte(p) for p in t["mot"])
        + f'<p class="t-fonce" style="margin:0;{F}font-size:16px;line-height:24px;font-weight:bold;color:{BLEU};">{t["equipe"]}</p>',
        fond=CREME, pad="32px 40px 34px 40px", classe="creme"))
    # Pied
    b.append(f"""<tr><td class="pad" style="background-color:{BLEU};padding:28px 40px;{F}" align="center">
  <p style="margin:0 0 6px 0;font-size:16px;line-height:22px;font-weight:bold;color:#FFFFFF;">{t['faq_tit']}</p>
  <p style="margin:0;font-size:14px;line-height:22px;color:#FFFFFF;">{t['faq']} <a href="https://faq.truckfly.com/" style="color:{JAUNE};font-weight:bold;">faq.truckfly.com</a></p>
</td></tr>
<tr><td class="pad t-doux" align="center" style="padding:22px 40px 34px 40px;{F}font-size:12px;line-height:18px;color:{GRIS};">
  <p style="margin:0 0 8px 0;">{t['raison']}</p>
  <p style="margin:0;"><a href="{{{{ unsubscribe }}}}" style="color:{GRIS};">{t['desinscription']}</a></p>
</td></tr>""")
    return "\n".join(b)


def construire(langues, conditions):
    morceaux = []
    for L in langues:
        corps = blocs(L, T[L])
        if conditions:
            corps = f'{{% if ( "{L}" in contact.LANG ) %}}\n{corps}\n{{% endif %}}'
        morceaux.append(corps)
    preheader = ("L'hiver arrive sur la route. Ce qui change au 1er novembre, les alertes qui t'aident, et comment grimper au classement."
                 if langues == ["FR"] or conditions else "")
    if langues == ["IT"]:
        preheader = "L'inverno arriva sulla strada. Cosa cambia dal 1° novembre, le segnalazioni che ti aiutano e come scalare la classifica."
    if langues == ["ES"]:
        preheader = "El invierno llega a la carretera. Qué cambia el 1 de noviembre, los avisos que te ayudan y cómo subir en la clasificación."
    return page("Le Relais · Michelin Truckfly", preheader, "\n".join(morceaux))


if __name__ == "__main__":
    SORTIE.mkdir(parents=True, exist_ok=True)
    (SORTIE / "brevo.html").write_text(construire(LANGS, True), encoding="utf-8")
    for L in LANGS:
        (SORTIE / f"apercu-{L.lower()}.html").write_text(construire([L], False), encoding="utf-8")
    print("ok")
