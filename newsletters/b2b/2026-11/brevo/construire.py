"""Construit le template Brevo B2B de novembre 2026 en FR, EN, ES, NL, IT à partir du template collé (template_original.yaml)."""
import copy, uuid, yaml, re
from pathlib import Path
ICI = Path(__file__).parent
BLOCS = ICI.parent.parent.parent / "blocs"
y = yaml.safe_load(open(ICI / "template_original.yaml"))
S = y["body"]["content"][0]["content"]
REPLI = '( "EN" in contact.LANG ) or ( ( contact.LANG != "FR" ) and ( contact.LANG != "ES" ) and ( contact.LANG != "NL" ) and ( contact.LANG != "IT" ) )'
LANGS = ["EN", "ES", "NL", "IT"]
COND = {L: (REPLI if L == "EN" else f'( "{L}" in contact.LANG )') for L in LANGS}

def nouveaux_ids(o):
    if isinstance(o, dict):
        if "id" in o: o["id"] = str(uuid.uuid4())
        for v in o.values(): nouveaux_ids(v)
    elif isinstance(o, list):
        for v in o: nouveaux_ids(v)
    return o

def copie(sec, lang, titre):
    s = nouveaux_ids(copy.deepcopy(sec)); s["condition"] = COND[lang]; s["title"] = titre; return s

def pastille(it, txt, larg=None):
    h = f'<p><strong><span style="color: rgb(0, 0, 0);">{txt}</span></strong></p>'
    it["text"] = h; it["content"]["text"] = h
    if larg: it["layout"]["default"]["width"] = larg

def bouton(it, txt, href):
    h = f'<p><strong><span style="color: rgb(0, 0, 0);">{txt}</span></strong></p>'
    it["text"] = h; it["content"]["text"] = h; it["content"]["href"] = href

def paras(lst, couleur="rgb(0, 0, 0)"):
    return '<p><br></p>'.join(f'<p><span style="color: {couleur};">{x}</span></p>' for x in lst)

# ---------- Textes ----------
EDITO = {
 "EN": ("Winter is on its way, let’s be ready", ["Hello,", "As winter sets in, the days get shorter, road conditions get tougher and end of year activity picks up. It is a demanding time for your drivers and your teams alike.", "At MICHELIN Truckfly, we want to help you face it with peace of mind, with reliable information and tools that are useful every day.", "This month, find the essentials: upcoming events, our latest news and the developments that matter in each country.", "Happy reading,"]),
 "ES": ("Llega el invierno, estemos bien preparados", ["Hola:", "Con el invierno, los días se acortan, las condiciones de la carretera se endurecen y la actividad de final de año se intensifica. Es una época exigente para vuestros conductores y para vuestros equipos.", "En MICHELIN Truckfly queremos ayudaros a afrontarla con tranquilidad, con información fiable y herramientas útiles en el día a día.", "Este mes, encontrad lo esencial: los próximos eventos, nuestras novedades y los cambios que importan en cada país.", "¡Buena lectura!"]),
 "NL": ("De winter komt eraan, laten we goed voorbereid zijn", ["Goedendag,", "Met de winter worden de dagen korter, worden de omstandigheden op de weg zwaarder en neemt de drukte aan het eind van het jaar toe. Een veeleisende periode voor uw chauffeurs en voor uw teams.", "Bij MICHELIN Truckfly willen we u helpen deze periode met een gerust hart in te gaan, met betrouwbare informatie en handige tools voor elke dag.", "Deze maand vindt u het belangrijkste: de komende evenementen, ons nieuws en de ontwikkelingen die er in elk land toe doen.", "Veel leesplezier,"]),
 "IT": ("L’inverno si avvicina, restiamo ben preparati", ["Buongiorno,", "Con l’inverno le giornate si accorciano, le condizioni stradali diventano più difficili e l’attività di fine anno si intensifica. È un periodo impegnativo sia per i Suoi autisti sia per il Suo team.", "Con MICHELIN Truckfly vogliamo aiutarLa ad affrontarlo con serenità, con informazioni affidabili e strumenti utili ogni giorno.", "Questo mese trova l’essenziale: i prossimi appuntamenti, le nostre novità e gli sviluppi che contano in ogni Paese.", "Buona lettura,"]),
}
EVT = {
 "EN": ("Events", "Supply Chain Event 2026: tomorrow’s logistics takes shape in Paris", "1 and 2 December 2026 · Paris Expo Porte de Versailles",
        "Every year, the Supply Chain Event brings together logistics and supply chain decision makers. On the programme: more than 110 exhibitors, 40 talks and business meetings to spot the solutions that will make a difference in 2027.",
        "Why is it worth it for you?", ["Discover the latest innovations in transport, warehousing and digital flows", "Attend talks on today’s hot topics: decarbonisation, costs, recruitment", "Meet partners and connect with industry players"], "Discover the show"),
 "ES": ("Eventos", "Supply Chain Event 2026: la logística del mañana se diseña en París", "1 y 2 de diciembre de 2026 · Paris Expo Porte de Versailles",
        "Cada año, el Supply Chain Event reúne a los responsables de la logística y la cadena de suministro. En el programa: más de 110 expositores, 40 conferencias y reuniones de negocio para descubrir las soluciones que marcarán la diferencia en 2027.",
        "¿Por qué te interesa?", ["Descubrir las últimas innovaciones en transporte, almacén y digitalización de flujos", "Asistir a conferencias sobre los temas del momento: descarbonización, costes, contratación", "Conocer a socios y conversar con los actores del sector"], "Descubre el salón"),
 "NL": ("Evenementen", "Supply Chain Event 2026: de logistiek van morgen krijgt vorm in Parijs", "1 en 2 december 2026 · Paris Expo Porte de Versailles",
        "Het Supply Chain Event brengt elk jaar de beslissers uit logistiek en supply chain samen. Op het programma: meer dan 110 exposanten, 40 lezingen en zakelijke afspraken om de oplossingen te ontdekken die in 2027 het verschil maken.",
        "Waarom is het interessant voor u?", ["De nieuwste innovaties ontdekken in transport, opslag en digitalisering van goederenstromen", "Lezingen volgen over actuele thema’s: verduurzaming, kosten, werving", "Partners ontmoeten en in gesprek gaan met spelers uit de sector"], "Ontdek de beurs"),
 "IT": ("Eventi", "Supply Chain Event 2026: a Parigi prende forma la logistica di domani", "1 e 2 dicembre 2026 · Paris Expo Porte de Versailles",
        "Ogni anno il Supply Chain Event riunisce i decisori della logistica e della supply chain. In programma: oltre 110 espositori, 40 conferenze e incontri d’affari per scoprire le soluzioni che faranno la differenza nel 2027.",
        "Perché è interessante per Lei?", ["Scoprire le ultime innovazioni in trasporti, magazzino e digitalizzazione dei flussi", "Seguire conferenze sui temi del momento: decarbonizzazione, costi, reclutamento", "Incontrare partner e confrontarsi con gli operatori del settore"], "Scopri il salone"),
}
PUB = {"EN": ("Hauliers and fleet managers", "Establishments", "Partners and brands"),
       "ES": ("Empresas de transporte y gestores de flota", "Establecimientos", "Socios y marcas"),
       "NL": ("Transportbedrijven en wagenparkbeheerders", "Locaties", "Partners en merken"),
       "IT": ("Aziende di trasporto e gestori di flotte", "Strutture", "Partner e marchi")}
INFO = {
 "EN": dict(pill="MICHELIN Truckfly News", apporte="What’s in it for you", btn="Learn more", blog="https://www.truckfly.com/blog/en/", items=[
   ("Drivers ", "like the community’s contributions", ["Photos, comments, recommendations: drivers can now like other drivers’ contributions, straight from the activity feed.", "A way to say thank you and bring the most reliable information to the top."],
    [(0, "The most appreciated information stands out faster: your drivers spot at a glance the parking areas and stops their colleagues rate as reliable."), (1, "Every photo or positive review of the establishment can be liked by the community. The best contributions gain visibility with other drivers.")]),
   ("Profile photos ", "now open full screen", ["One tap on a driver’s photo is all it takes to see it in full. Handy for recognising a colleague you often meet at truck stops."],
    [(0, "Drivers who recognise each other at truck stops and talk more easily: a more human community that breaks the isolation of the road."), (2, "A community that knows each other and comes back to the app every day: an engaged audience, attentive to content that is useful to them.")]),
   ("Every driver ", "chooses their app language", ["The MICHELIN Truckfly language can now be changed directly in the app (Settings &gt; App language), without touching the phone settings."],
    [(0, "Your drivers of every nationality use the app in their own language, even on a shared work phone. Fewer mistakes, more independence, no phone settings to change."), (1, "Truckers from all over Europe use the app in their own language: they find information about the establishment more easily.")]),
   ("New on GPS Premium: ", "the toll alert", ["During navigation, an alert warns the driver when approaching a toll, which also appears on the map. They have time to get into the right lane and get their tag or card ready."],
    [(0, "Fewer last minute braking manoeuvres, the toll tag ready in advance, the right lane chosen in time: more safety and smoother journeys for your drivers equipped with the MICHELIN Truckfly GPS."), (2, "A GPS built for trucks that gets richer every month, for the safety of all road users.")]),
 ]),
 "ES": dict(pill="Noticias MICHELIN Truckfly", apporte="Lo que te aporta", btn="Más información", blog="https://www.truckfly.com/blog/es/", items=[
   ("Los conductores ", "dan like a las aportaciones de la comunidad", ["Fotos, comentarios, recomendaciones: los conductores ya pueden dar like a las aportaciones de los demás, directamente desde el feed de actividad.", "Una forma de dar las gracias y de destacar la información más fiable."],
    [(0, "La información más valorada destaca antes: tus conductores ven de un vistazo los aparcamientos y paradas que sus compañeros consideran fiables."), (1, "Cada foto u opinión positiva sobre el establecimiento puede recibir likes de la comunidad. Las mejores aportaciones ganan visibilidad entre los demás conductores.")]),
   ("Las fotos de perfil ", "se ven a pantalla completa", ["Basta con tocar la foto de un conductor para verla en grande. Muy práctico para reconocer a un compañero con el que te cruzas a menudo en las áreas."],
    [(0, "Conductores que se reconocen en las áreas y se comunican con más facilidad: una comunidad más humana, que rompe el aislamiento de la carretera."), (2, "Una comunidad que se conoce y vuelve a la app cada día: un público comprometido, atento a los contenidos que le son útiles.")]),
   ("Cada conductor ", "elige el idioma de su app", ["El idioma de MICHELIN Truckfly se cambia directamente en la app (Ajustes &gt; Idioma de la aplicación), sin tocar la configuración del teléfono."],
    [(0, "Tus conductores de todas las nacionalidades usan la app en su idioma, incluso en un teléfono de trabajo compartido. Menos errores, más autonomía y ningún ajuste del teléfono que cambiar."), (1, "Los camioneros de toda Europa usan la app en su idioma: encuentran más fácilmente la información sobre el establecimiento.")]),
   ("Novedad GPS Premium: ", "la alerta de peaje", ["Durante la navegación, una alerta avisa al conductor cuando se acerca a un peaje, que también aparece en el mapa. Tiene tiempo de colocarse en el carril correcto y preparar su telepeaje o su tarjeta."],
    [(0, "Menos frenazos de última hora, el telepeaje preparado con antelación, el carril correcto elegido a tiempo: más seguridad y fluidez para tus conductores equipados con el GPS MICHELIN Truckfly."), (2, "Un GPS pensado para camiones que se enriquece cada mes, al servicio de la seguridad de todos los usuarios de la carretera.")]),
 ]),
 "NL": dict(pill="MICHELIN Truckfly Nieuws", apporte="Wat het u oplevert", btn="Meer informatie", blog="https://www.truckfly.com/blog/en/", items=[
   ("Chauffeurs ", "liken de bijdragen van de community", ["Foto’s, reacties, aanbevelingen: chauffeurs kunnen nu de bijdragen van anderen liken, rechtstreeks vanuit de activiteitenfeed.", "Een manier om dank je wel te zeggen en de meest betrouwbare info naar boven te halen."],
    [(0, "De meest gewaardeerde info valt sneller op: uw chauffeurs zien in één oogopslag welke parkings en stops hun collega’s betrouwbaar vinden."), (1, "Elke foto of positieve beoordeling van de locatie kan door de community worden geliket. De beste bijdragen worden beter zichtbaar voor andere chauffeurs.")]),
   ("Profielfoto’s ", "op volledig scherm", ["Eén tik op de foto van een chauffeur volstaat om hem groot te zien. Handig om collega’s op de parkings te herkennen."],
    [(0, "Chauffeurs die elkaar herkennen op de parkings en makkelijker contact maken: een menselijkere community die het isolement van de weg doorbreekt."), (2, "Een community die elkaar kent en elke dag terugkomt in de app: een betrokken publiek dat openstaat voor nuttige content.")]),
   ("Elke chauffeur ", "kiest de taal van zijn app", ["De taal van MICHELIN Truckfly wijzigt u direct in de app (Instellingen &gt; Taal van de app), zonder de instellingen van de telefoon aan te passen."],
    [(0, "Uw chauffeurs van alle nationaliteiten gebruiken de app in hun eigen taal, zelfs op een gedeelde werktelefoon. Minder fouten, meer zelfstandigheid, geen telefooninstellingen te wijzigen."), (1, "Truckers uit heel Europa gebruiken de app in hun eigen taal: zij vinden de informatie over de locatie makkelijker.")]),
   ("Nieuw in GPS Premium: ", "de tolwaarschuwing", ["Tijdens het navigeren waarschuwt een melding de chauffeur bij het naderen van een tolpoort, die ook op de kaart verschijnt. Zo heeft hij tijd om de juiste rijstrook te kiezen en zijn tolbadge of kaart klaar te houden."],
    [(0, "Minder remmen op het laatste moment, de tolbadge op tijd klaar, op tijd de juiste rijstrook: meer veiligheid en een vlottere rit voor uw chauffeurs met de MICHELIN Truckfly GPS."), (2, "Een gps voor vrachtwagens die elke maand beter wordt, ten dienste van de veiligheid van alle weggebruikers.")]),
 ]),
 "IT": dict(pill="Notizie MICHELIN Truckfly", apporte="Cosa Le offre", btn="Scopri di più", blog="https://www.truckfly.com/blog/it/", items=[
   ("Gli autisti ", "mettono like ai contributi della community", ["Foto, commenti, consigli: ora gli autisti possono mettere like ai contributi degli altri, direttamente dal feed delle attività.", "Un modo per dire grazie e far emergere le informazioni più affidabili."],
    [(0, "Le informazioni più apprezzate emergono prima: i Suoi autisti individuano a colpo d’occhio i parcheggi e le soste che i colleghi ritengono affidabili."), (1, "Ogni foto o recensione positiva sulla struttura può ricevere like dalla community. I contributi migliori guadagnano visibilità presso gli altri autisti.")]),
   ("Le foto profilo ", "si aprono a schermo intero", ["Basta un tocco sulla foto di un autista per vederla in grande. Comodo per riconoscere un collega incontrato spesso nelle aree di sosta."],
    [(0, "Autisti che si riconoscono nelle aree di sosta e comunicano più facilmente: una community più umana, che rompe l’isolamento della strada."), (2, "Una community che si conosce e torna nell’app ogni giorno: un pubblico coinvolto, attento ai contenuti che gli sono utili.")]),
   ("Ogni autista ", "sceglie la lingua della sua app", ["La lingua di MICHELIN Truckfly si cambia direttamente nell’app (Impostazioni &gt; Lingua dell’app), senza toccare le impostazioni del telefono."],
    [(0, "I Suoi autisti di ogni nazionalità usano l’app nella loro lingua, anche su un telefono di lavoro condiviso. Meno errori, più autonomia, nessuna impostazione del telefono da modificare."), (1, "I camionisti di tutta Europa usano l’app nella loro lingua: trovano più facilmente le informazioni sulla struttura.")]),
   ("Novità GPS Premium: ", "l’avviso casello", ["Durante la navigazione, un avviso segnala all’autista l’avvicinarsi di un casello, visibile anche sulla mappa. Ha il tempo di posizionarsi sulla corsia giusta e preparare il telepedaggio o la carta."],
    [(0, "Meno frenate dell’ultimo momento, telepedaggio pronto in anticipo, corsia giusta scelta per tempo: più sicurezza e fluidità per i Suoi autisti dotati del GPS MICHELIN Truckfly."), (2, "Un GPS pensato per i camion che si arricchisce ogni mese, al servizio della sicurezza di tutti gli utenti della strada.")]),
 ]),
}
ROADPOL = "https://transportonline.com/news/informazione/roadpol-truck-bus-2026-campagna-novembre/"
MARCHE = {
 "EN": ("Market / Legal Information", "Learn more", [
   ("RoadPol Truck &amp; Bus checks across Europe from 16 to 22 November", ["European traffic police forces in the ROADPOL network are running their last operation of the year on trucks and coaches. Focus: tachograph, driving and rest times.", "Meanwhile, the revision of the weights and dimensions directive is still under negotiation: manufacturers are asking that electric and hydrogen trucks do not lose payload compared with diesel."], "Sources: Transportonline · HGV Ireland", ROADPOL),
   ("UK: 30,000 fewer HGV drivers in one year", ["According to Logistics UK, the UK now has 283,000 HGV drivers, 30,000 fewer than a year earlier. Only 4% are under 25.", "Recruitment is once again a key challenge for hauliers."], "Source: trans.info", "https://trans.info/en/wanted-60-000-drivers-471678")]),
 "ES": ("Info Mercado/Legal", "Más información", [
   ("Controles RoadPol Truck &amp; Bus en Europa del 16 al 22 de noviembre", ["Las policías de tráfico europeas de la red ROADPOL llevan a cabo su última operación del año sobre camiones y autocares. En el punto de mira: tacógrafo, tiempos de conducción y descanso.", "Mientras tanto, la revisión de la directiva de pesos y dimensiones sigue en negociación: los fabricantes piden que los camiones eléctricos y de hidrógeno no pierdan carga útil frente al diésel."], "Fuentes: Transportonline · HGV Ireland", ROADPOL)]),
 "NL": ("Info Markt/Recht", "Meer informatie", [
   ("RoadPol Truck &amp; Bus controles in Europa van 16 tot en met 22 november", ["De Europese verkeerspolitie van het ROADPOL netwerk houdt haar laatste actie van het jaar gericht op vrachtwagens en touringcars. In het vizier: tachograaf, rij en rusttijden.", "Ondertussen wordt nog onderhandeld over de herziening van de richtlijn maten en gewichten: fabrikanten vragen dat elektrische trucks en waterstoftrucks geen laadvermogen verliezen ten opzichte van diesel."], "Bronnen: Transportonline · HGV Ireland", ROADPOL)]),
 "IT": ("Info Mercato/Legale", "Scopri di più", [
   ("Controlli RoadPol Truck &amp; Bus in Europa dal 16 al 22 novembre", ["Le polizie stradali europee della rete ROADPOL svolgono l’ultima campagna dell’anno su camion e autobus. Sotto la lente: tachigrafo, tempi di guida e di riposo.", "Intanto la revisione della direttiva su pesi e dimensioni è ancora in fase di negoziato: i costruttori chiedono che i camion elettrici e a idrogeno non perdano carico utile rispetto al diesel."], "Fonti: Transportonline · HGV Ireland", ROADPOL),
   ("DL 193/2026: sospensione dei canoni di leasing fino a marzo", ["Dal 24 ottobre le imprese di autotrasporto iscritte all’Albo possono chiedere la sospensione dei canoni di leasing sui veicoli, per le rate dal 1° novembre 2026 al 31 marzo 2027. Il decreto deve essere convertito in legge entro il 22 dicembre.", "Il credito d’imposta sul gasolio concesso a fine ottobre va utilizzato entro il 31 dicembre 2026."], "Fonti: Transportonline · TrasportoEuropa", "https://transportonline.com/news/informazione/autotrasporto-carburanti-dl-193-2026-novita/")]),
}
SONDAGE = {
 "EN": ("Results · Previous question", "What would you like the general public to understand about your job?", ["Our working conditions", "Our constraints on the road", "Our role in the economy"], "For 84% of professionals in the MICHELIN Truckfly community, the general public should first understand the reality of the job: working conditions and constraints on the road.",
        "Next month, we’re talking about...", "To reduce risk on the road, the most effective lever in your view is…", "See you in <strong>15 days</strong> to discover the results and answer a new question. See you on the road!"),
 "ES": ("Resultados · Pregunta anterior", "¿Qué te gustaría que el gran público entendiera sobre tu oficio?", ["Nuestras condiciones de trabajo", "Nuestras dificultades en la carretera", "Nuestro papel en la economía"], "Para el 84 % de los profesionales de la comunidad MICHELIN Truckfly, el gran público debería entender primero el día a día del oficio: las condiciones de trabajo y las dificultades en la carretera.",
        "El próximo mes hablamos de...", "Para reducir el riesgo en la carretera, la palanca más eficaz para ti es…", "Nos vemos dentro de <strong>15 días</strong> para descubrir los resultados y responder a una nueva pregunta. ¡Hasta pronto en la carretera!"),
 "NL": ("Resultaten · Vorige vraag", "Wat zou u willen dat het grote publiek begrijpt van uw beroep?", ["Onze arbeidsomstandigheden", "Onze beperkingen op de weg", "Onze rol in de economie"], "Voor 84% van de professionals in de MICHELIN Truckfly community moet het grote publiek vooral de dagelijkse realiteit van het vak begrijpen: de arbeidsomstandigheden en de beperkingen op de weg.",
        "Volgende maand hebben we het over...", "Om het risico op de weg te verkleinen, is volgens u de meest effectieve maatregel…", "Over <strong>15 dagen</strong> ontdekt u de resultaten en kunt u een nieuwe vraag beantwoorden. Tot ziens op de weg!"),
 "IT": ("Risultati · Domanda precedente", "Cosa vorrebbe che il grande pubblico capisse del Suo mestiere?", ["Le nostre condizioni di lavoro", "I nostri vincoli su strada", "Il nostro ruolo nell’economia"], "Per l’84% dei professionisti della community MICHELIN Truckfly, il grande pubblico dovrebbe capire prima di tutto la realtà del mestiere: le condizioni di lavoro e i vincoli su strada.",
        "Il mese prossimo parliamo di...", "Per ridurre il rischio su strada, la leva più efficace secondo Lei è…", "Appuntamento tra <strong>15 giorni</strong> per scoprire i risultati e rispondere a una nuova domanda. Alla prossima, su strada!"),
}


PILL_EDITO = {"DE": "Das Editorial des Monats", "PL": "Editorial miesiąca"}
QBTN = {"DE": "Die Frage der Trucker!", "PL": "Pytanie do Truckerów!"}
RECAP = {
 "DE": ("Der Überblick des Monats", [("Veranstaltungen", "Die nächsten Termine, die Sie nicht verpassen sollten"), ("MICHELIN Truckfly News", "Unsere Neuigkeiten, Updates und Highlights"), ("Markt / Recht", "Entwicklungen und wichtige Informationen aus der Branche"), ("Die Frage der Trucker", "Eine Frage, eine Antwort und die Tipps unserer Community")]),
 "PL": ("Podsumowanie miesiąca", [("Wydarzenia", "Najbliższe terminy, których nie warto przegapić"), ("Aktualności MICHELIN Truckfly", "Nasze nowości, aktualizacje i najważniejsze wydarzenia"), ("Rynek / Przepisy", "Zmiany i informacje, które warto znać w branży"), ("Pytanie do Truckerów", "Jedno pytanie, jedna odpowiedź i porady naszej społeczności")]),
}
EDITO["DE"] = ("Der Winter naht: gut vorbereitet in die kalte Jahreszeit", ["Guten Tag,", "Mit dem Winter werden die Tage kürzer, die Straßenverhältnisse schwieriger und das Jahresendgeschäft nimmt Fahrt auf. Eine anspruchsvolle Zeit für Ihre Fahrer ebenso wie für Ihre Teams.", "Bei MICHELIN Truckfly möchten wir Ihnen helfen, sie gelassen anzugehen, mit verlässlichen Informationen und Tools, die im Alltag wirklich nützen.", "Diesen Monat finden Sie das Wichtigste: kommende Termine, unsere Neuigkeiten und die Entwicklungen, die in jedem Land zählen.", "Viel Spaß beim Lesen,"])
EDITO["PL"] = ("Nadchodzi zima, przygotujmy się dobrze", ["Dzień dobry,", "Wraz z zimą dni stają się krótsze, warunki na drogach trudniejsze, a ruch na koniec roku coraz większy. To wymagający okres zarówno dla Państwa kierowców, jak i zespołów.", "W MICHELIN Truckfly chcemy pomóc Państwu przejść przez niego spokojnie, dzięki rzetelnym informacjom i narzędziom przydatnym na co dzień.", "W tym miesiącu znajdą Państwo najważniejsze informacje: nadchodzące wydarzenia, nasze nowości oraz zmiany, które mają znaczenie w każdym kraju.", "Miłej lektury,"])
EVT["DE"] = ("Veranstaltungen", "Supply Chain Event 2026: In Paris nimmt die Logistik von morgen Gestalt an", "1. und 2. Dezember 2026 · Paris Expo Porte de Versailles",
  "Das Supply Chain Event bringt jedes Jahr die Entscheider aus Logistik und Supply Chain zusammen. Auf dem Programm: über 110 Aussteller, 40 Vorträge und Geschäftstermine, um die Lösungen zu entdecken, die 2027 den Unterschied machen.",
  "Warum lohnt sich der Besuch für Sie?", ["Die neuesten Innovationen in Transport, Lager und Digitalisierung der Warenströme entdecken", "Vorträge zu aktuellen Themen verfolgen: Dekarbonisierung, Kosten, Personalgewinnung", "Partner treffen und sich mit Akteuren der Branche austauschen"], "Messe entdecken")
EVT["PL"] = ("Wydarzenia", "Supply Chain Event 2026: logistyka jutra nabiera kształtów w Paryżu", "1 i 2 grudnia 2026 · Paris Expo Porte de Versailles",
  "Supply Chain Event co roku gromadzi decydentów z branży logistyki i łańcucha dostaw. W programie: ponad 110 wystawców, 40 wystąpień i spotkania biznesowe, aby poznać rozwiązania, które będą miały znaczenie w 2027 roku.",
  "Dlaczego warto?", ["Poznać najnowsze innowacje w transporcie, magazynowaniu i cyfryzacji przepływów", "Wysłuchać wystąpień na aktualne tematy: dekarbonizacja, koszty, rekrutacja", "Spotkać partnerów i porozmawiać z przedstawicielami branży"], "Poznaj targi")
PUB["DE"] = ("Transportunternehmen und Fuhrparkleiter", "Betriebe", "Partner und Marken")
PUB["PL"] = ("Firmy transportowe i menedżerowie flot", "Obiekty", "Partnerzy i marki")
INFO["DE"] = dict(pill="MICHELIN Truckfly News", apporte="Ihr Vorteil", btn="Mehr erfahren", blog="https://www.truckfly.com/blog/en/", items=[
 ("Fahrer ", "liken die Beiträge der Community", ["Fotos, Kommentare, Empfehlungen: Fahrer können die Beiträge anderer jetzt direkt im Aktivitätsfeed liken.", "Eine Art, Danke zu sagen und die zuverlässigsten Infos sichtbar zu machen."],
  [(0, "Die beliebtesten Infos fallen schneller auf: Ihre Fahrer erkennen auf einen Blick, welche Parkplätze und Stopps ihre Kollegen für zuverlässig halten."), (1, "Jedes Foto und jede positive Bewertung des Betriebs kann von der Community geliked werden. Die besten Beiträge werden für andere Fahrer sichtbarer.")]),
 ("Profilfotos ", "jetzt im Vollbild", ["Ein Tippen auf das Foto eines Fahrers genügt, um es groß anzuzeigen. Praktisch, um Kollegen auf dem Rastplatz wiederzuerkennen."],
  [(0, "Fahrer, die sich auf Rastplätzen wiedererkennen und leichter ins Gespräch kommen: eine menschlichere Community, die die Einsamkeit auf der Straße durchbricht."), (2, "Eine Community, die sich kennt und jeden Tag in die App zurückkehrt: ein engagiertes Publikum, offen für nützliche Inhalte.")]),
 ("Jeder Fahrer ", "wählt die Sprache seiner App", ["Die Sprache von MICHELIN Truckfly lässt sich direkt in der App ändern (Einstellungen &gt; App-Sprache), ohne die Einstellungen des Handys anzutasten."],
  [(0, "Ihre Fahrer aller Nationalitäten nutzen die App in ihrer Sprache, auch auf einem geteilten Diensthandy. Weniger Fehler, mehr Selbstständigkeit, keine Handyeinstellungen zu ändern."), (1, "Lkw-Fahrer aus ganz Europa nutzen die App in ihrer Sprache: Sie finden die Informationen über den Betrieb leichter.")]),
 ("Neu im GPS Premium: ", "der Mauthinweis", ["Während der Navigation warnt ein Hinweis den Fahrer, wenn er sich einer Mautstelle nähert, die auch auf der Karte erscheint. So bleibt Zeit, die richtige Spur zu wählen und die Mautbox oder Karte bereitzuhalten."],
  [(0, "Weniger Bremsmanöver in letzter Sekunde, Mautbox rechtzeitig bereit, die richtige Spur zur rechten Zeit: mehr Sicherheit und flüssigere Fahrten für Ihre Fahrer mit dem MICHELIN Truckfly GPS."), (2, "Ein GPS für Lkw, das jeden Monat besser wird, im Dienst der Sicherheit aller Verkehrsteilnehmer.")]),
])
INFO["PL"] = dict(pill="Aktualności MICHELIN Truckfly", apporte="Co to Państwu daje", btn="Dowiedz się więcej", blog="https://www.truckfly.com/blog/en/", items=[
 ("Kierowcy mogą teraz ", "polubić wpisy społeczności", ["Zdjęcia, komentarze, rekomendacje: kierowcy mogą teraz polubić wpisy innych kierowców bezpośrednio z kanału aktywności.", "To sposób, by podziękować i wyróżnić najbardziej wiarygodne informacje."],
  [(0, "Najbardziej cenione informacje szybciej się wyróżniają: Państwa kierowcy od razu widzą, które parkingi i postoje koledzy uznają za sprawdzone."), (1, "Każde zdjęcie lub pozytywna opinia o obiekcie może zostać polubiona przez społeczność. Najlepsze wpisy zyskują widoczność wśród innych kierowców.")]),
 ("Zdjęcia profilowe ", "na pełnym ekranie", ["Wystarczy dotknąć zdjęcia kierowcy, aby zobaczyć je w dużym rozmiarze. To wygodne, gdy chce się rozpoznać kolegę spotkanego na parkingu."],
  [(0, "Kierowcy, którzy rozpoznają się na parkingach i łatwiej nawiązują kontakt: bardziej ludzka społeczność, która przełamuje samotność w trasie."), (2, "Społeczność, która się zna i codziennie wraca do aplikacji: zaangażowani odbiorcy, otwarci na przydatne treści.")]),
 ("Każdy kierowca ", "wybiera język aplikacji", ["Język MICHELIN Truckfly można zmienić bezpośrednio w aplikacji (Ustawienia &gt; Język aplikacji), bez zmiany ustawień telefonu."],
  [(0, "Państwa kierowcy każdej narodowości korzystają z aplikacji w swoim języku, nawet na wspólnym telefonie służbowym. Mniej błędów, więcej samodzielności, bez zmiany ustawień telefonu."), (1, "Kierowcy z całej Europy korzystają z aplikacji w swoim języku: łatwiej znajdują informacje o obiekcie.")]),
 ("Nowość w GPS Premium: ", "alert o punkcie poboru opłat", ["Podczas nawigacji alert ostrzega kierowcę o zbliżaniu się do punktu poboru opłat, widocznego także na mapie. Kierowca ma czas, by zająć właściwy pas i przygotować urządzenie do opłat lub kartę."],
  [(0, "Mniej gwałtownego hamowania w ostatniej chwili, urządzenie do opłat gotowe wcześniej, właściwy pas wybrany na czas: więcej bezpieczeństwa i płynniejsza jazda dla Państwa kierowców z GPS MICHELIN Truckfly."), (2, "GPS stworzony dla ciężarówek, który co miesiąc zyskuje nowe funkcje, z myślą o bezpieczeństwie wszystkich użytkowników dróg.")]),
])
MARCHE["DE"] = ("Markt / Recht", "Mehr erfahren", [
 ("RoadPol Truck &amp; Bus: Kontrollen in Europa vom 16. bis 22. November", ["Die europäischen Verkehrspolizeien des ROADPOL Netzwerks führen ihre letzte Aktion des Jahres bei Lkw und Bussen durch. Im Fokus: Fahrtenschreiber, Lenk- und Ruhezeiten.", "Parallel wird weiter über die Überarbeitung der Richtlinie zu Maßen und Gewichten verhandelt: Die Hersteller fordern, dass Elektro- und Wasserstoff-Lkw gegenüber dem Diesel keine Nutzlast verlieren."], "Quellen: Transportonline · HGV Ireland", ROADPOL),
 ("Lkw-Maut-Index: Fahrleistung im Oktober gesunken", ["Laut Destatis ist die Fahrleistung mautpflichtiger Lkw auf Autobahnen im Oktober 2026 gegenüber dem Vormonat um 1,6 % gesunken, liegt aber 0,5 % über dem Vorjahresmonat.", "Der Index gilt als Frühindikator für die Konjunktur in der Industrie."], "Quelle: Destatis", "https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/11/PD26_391_421.html")])
MARCHE["PL"] = ("Rynek / Przepisy", "Dowiedz się więcej", [
 ("Kontrole RoadPol Truck &amp; Bus w Europie od 16 do 22 listopada", ["Europejskie policje drogowe z sieci ROADPOL prowadzą ostatnią w tym roku akcję kontrolną ciężarówek i autokarów. Pod lupą: tachograf, czas jazdy i odpoczynku.", "Równolegle trwają negocjacje w sprawie zmiany dyrektywy o masach i wymiarach: producenci chcą, aby ciężarówki elektryczne i wodorowe nie traciły ładowności w porównaniu z dieslem."], "Źródła: Transportonline · HGV Ireland", ROADPOL)])
SONDAGE["DE"] = ("Ergebnisse · Vorherige Frage", "Was sollte die breite Öffentlichkeit Ihrer Meinung nach über Ihren Beruf verstehen?", ["Unsere Arbeitsbedingungen", "Unsere Einschränkungen auf der Straße", "Unsere Rolle in der Wirtschaft"], "Für 84 % der Profis in der MICHELIN Truckfly Community sollte die Öffentlichkeit vor allem den Berufsalltag verstehen: die Arbeitsbedingungen und die Einschränkungen auf der Straße.",
  "Nächsten Monat sprechen wir über...", "Um das Risiko auf der Straße zu verringern, ist der wirksamste Hebel für Sie…", "In <strong>15 Tagen</strong> erfahren Sie die Ergebnisse und können eine neue Frage beantworten. Bis bald auf der Straße!")
SONDAGE["PL"] = ("Wyniki · Poprzednie pytanie", "Co chcieliby Państwo, aby opinia publiczna zrozumiała w Państwa zawodzie?", ["Nasze warunki pracy", "Nasze ograniczenia na drodze", "Nasza rola w gospodarce"], "Dla 84% profesjonalistów ze społeczności MICHELIN Truckfly opinia publiczna powinna przede wszystkim zrozumieć codzienność zawodu: warunki pracy i ograniczenia na drodze.",
  "W przyszłym miesiącu porozmawiamy o...", "Aby zmniejszyć ryzyko na drodze, najskuteczniejszym rozwiązaniem jest Państwa zdaniem…", "Za <strong>15 dni</strong> poznają Państwo wyniki i odpowiedzą na nowe pytanie. Do zobaczenia na drodze!")

# ---------- Construction ----------
fr_res = (BLOCS / "b2b-2026-11-sondage-resultats.html").read_text()
fr_tea = (BLOCS / "b2b-2026-11-teaser-question.html").read_text()
def resultats(lab, q, opts, concl):
    h = fr_res.replace("Résultats · Question précédente", lab).replace("Qu'aimeriez-vous que le grand public comprenne sur votre métier&nbsp;?", q)
    for a, b in zip(["Nos conditions de travail", "Nos contraintes sur la route", "Notre rôle dans l'économie"], opts): h = h.replace(a, b)
    return re.sub(r"Pour 84&nbsp;%.*?route\.", concl, h, flags=re.S)
def teaser(lab, q, fin):
    return (fr_tea.replace("Le mois prochain, on parle de...", lab)
            .replace("Pour réduire le risque sur la route, le levier le plus efficace selon vous, c'est…", q)
            .replace("Rendez-vous dans <strong>15 jours</strong> pour découvrir les résultats et répondre à une nouvelle question. À la prochaine sur la route !", fin))
def cartes(titre, lst):
    h = f'<h4 class="texte-fonce" style="margin:4px 0 12px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:24px;font-weight:bold;color:#061866;">{titre}</h4>\n'
    for t, x in lst:
        h += f'\n<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 10px 0;">\n  <tr><td class="bref" style="background-color:#F5F3F1;border-radius:12px;padding:16px 20px;font-family:Arial,Helvetica,sans-serif;">\n    <p class="texte-fonce" style="margin:0 0 4px 0;font-size:16px;line-height:23px;font-weight:bold;color:#061866;">{t}</p>\n    <p class="texte-fonce" style="margin:0;font-size:16px;line-height:24px;color:#000000;">{x}</p>\n  </td></tr>\n</table>\n'
    return h

ancien = {i: s for i, s in enumerate(S)}
fr = {"edito": S[3], "events": S[14], "infos": S[18], "marche": S[23]}

def edito(L):
    s = copie(fr["edito"], L, f"Bannière {L} · Édito")
    it = s["content"][0]["content"]
    old = {"EN": 4, "ES": 5, "NL": 6, "IT": 7}.get(L)
    pastille(it[0], PILL_EDITO[L] if L in PILL_EDITO else re.sub("<[^>]+>", "", ancien[old]["content"][0]["content"][0]["text"]).replace("&#39;", "’"), "35%")
    t, ps = EDITO[L]
    it[1]["content"] = f'<h1 class="default-heading1"><br></h1><h1 class="default-heading1"><strong><span style="color: rgb(0, 0, 0);">{t}</span></strong></h1>'
    it[2]["content"] = paras(ps)
    if old: it[3]["content"] = copy.deepcopy(ancien[old]["content"][0]["content"][3]["content"])
    return s

def evenements(L):
    s = copie(fr["events"], L, f"Bannière {L} · Événements")
    it = s["content"][0]["content"]
    lab, tit, date, corps, pq, puces, btn = EVT[L]
    pastille(it[0], lab, "30%")
    it[1]["content"] = f'<div><h3 class="default-heading3"><span style="color: rgb(249, 250, 252);"><strong>{tit}</strong></span></h3></div>'
    B = 'style="color: rgb(255, 255, 255);"'
    it[2]["content"] = (f'<p class="default"><br></p><p class="default"><span {B}><strong>{date}</strong></span></p><p class="default"><br></p>'
                        f'<p class="default"><span {B}>{corps}</span></p><p class="default"><br></p><p class="default"><span {B}><strong>{pq}</strong></span></p><p class="default"><br></p>'
                        '<ul>' + "".join(f'<li {B}>{p}</li>' for p in puces) + '</ul>')
    bouton(it[4], btn, "https://www.supplychain-event.com/")
    return s

def infos(L):
    d = INFO[L]; s = copie(fr["infos"], L, f"Bannière {L} · Infos MICHELIN Truckfly")
    it = s["content"][0]["content"]
    pastille(it[0], d["pill"])
    for k, (a, b, txt, cs) in enumerate(d["items"]):
        t, x, img, html, btn = it[1 + 5 * k: 6 + 5 * k]
        t["content"] = f'<h2 class="default-heading2"><span style="color: rgb(0, 0, 0);"><strong>{a}</strong><strong><span style="background-color: rgb(255, 255, 26);">{b}</span></strong></span></h2>'
        x["content"] = paras(txt)
        lien = "https://lp.truckfly.com/en/gps-premium" if k == 3 else d["blog"]
        img["content"]["href"] = lien
        html["content"] = cartes(d["apporte"], [(PUB[L][i], c) for i, c in cs])
        bouton(btn, d["btn"], lien)
    return s

def marche(L):
    lab, btn, cartes_m = MARCHE[L]; s = copie(fr["marche"], L, f"Bannière {L} · Marché/Légal")
    it = s["content"][0]["content"]
    pastille(it[0], lab, "40%")
    if len(cartes_m) == 1: del it[4:]
    W = "rgb(249, 250, 252)"
    for k, (tit, ps, src, href) in enumerate(cartes_m):
        t, x, b = (it[1], it[2], it[3]) if k == 0 else (it[5], it[6], it[7])
        t["content"] = f'<p><strong><span style="color: rgb(255, 255, 255); font-size: 32px;">{tit}</span></strong></p>'
        x["content"] = paras(ps, W) + f'<p><br></p><p><span style="color: {W}; font-size: 11px;">{src}</span></p>'
        bouton(b, btn, href)
    return s

new = []
for i, s in enumerate(S):
    if i in (4, 5, 6, 7, 15, 16, 17, 19, 20, 21, 22, 24, 25, 26, 27): continue  # anciennes sections remplacées
    new.append(s)
    if i == 3: new += [edito(L) for L in LANGS]
    if i == 9: s["condition"] = REPLI; s["content"][0]["content"][1]["content"] = (
        '<p><span style="color: rgb(0, 0, 0); font-size: 20px;"><strong>I. Events</strong></span></p><p><span style="color: rgb(0, 0, 0);">The upcoming dates not to miss</span></p><p><br></p>'
        '<p><span style="color: rgb(0, 0, 0); font-size: 20px;"><strong>II. MICHELIN Truckfly News</strong></span></p><p><span style="color: rgb(0, 0, 0);">Our news, updates and highlights</span></p><p><br></p>'
        '<p><span style="color: rgb(0, 0, 0); font-size: 20px;"><strong>III. Market / Legal Information</strong></span></p><p><span style="color: rgb(0, 0, 0);">Updates and key information to know about the industry</span></p><p><br></p>'
        '<p><span style="color: rgb(0, 0, 0); font-size: 20px;"><strong>IV. The Truckers’ Question</strong></span></p><p><span style="color: rgb(0, 0, 0);">One question, one answer and advice from our community</span></p>')
    if i == 12:
        for L in ():
            r = copie(S[10], L, f"Bannière {L} · Récap"); pastille(r["content"][0]["content"][0], RECAP[L][0], "35%")
            r["content"][0]["content"][1]["content"] = "<p><br></p>".join(
                f'<p><span style="color: rgb(0, 0, 0); font-size: 20px;"><strong>{n}. {a}</strong></span></p><p><span style="color: rgb(0, 0, 0);">{b}</span></p>'
                for n, (a, b) in zip(["I", "II", "III", "IV"], RECAP[L][1]))
            new.append(r)
    if i == 14: new += [evenements(L) for L in LANGS]
    if i == 18: new += [infos(L) for L in LANGS]
    if i == 23: new += [marche(L) for L in LANGS]
    if i == 29:
        items = s["content"][0]["content"]
        def lang_of(c):
            for L in ["FR", "EN", "ES", "NL", "IT"]:
                if f'"{L}"' in (c or ""): return L
        for it in items:
            L = lang_of(it.get("condition"))
            if not L or it["type"] != "raw-html": 
                if L == "EN": it["condition"] = REPLI
                continue
            res = "SONDAGE" in it["content"]
            if L == "FR": it["content"] = fr_res if res else fr_tea
            else:
                lab, q, opts, concl, tlab, tq, fin = SONDAGE[L]
                it["content"] = resultats(lab, q, opts, concl) if res else teaser(tlab, tq, fin)
                if L == "EN": it["condition"] = REPLI
        es = [it for it in items if it.get("condition") == '( "ES" in contact.LANG )']
        for L in ():
            for it in es:
                c = nouveaux_ids(copy.deepcopy(it)); c["condition"] = COND[L]
                if c["type"] == "text-button":
                    h = f"<p><strong>{QBTN[L]}</strong></p>"; c["text"] = h; c["content"]["text"] = h
                else:
                    lab, q, opts, concl, tlab, tq, fin = SONDAGE[L]
                    c["content"] = resultats(lab, q, opts, concl) if "SONDAGE" in c["content"] else teaser(tlab, tq, fin)
                items.insert(len(items) - 1, c)
y["body"]["content"][0]["content"] = new

out = yaml.dump(y, allow_unicode=True, sort_keys=False, width=10**9, default_flow_style=False)
(ICI / "template_FR_EN_ES_NL_IT.yaml").write_text(out)

# ---------- Vérifications ----------
z = yaml.safe_load(out); ids = []
def walk(o):
    if isinstance(o, dict):
        if "id" in o: ids.append(o["id"])
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(z)
print("ids", len(ids), "uniques", len(set(ids)))
for s in z["body"]["content"][0]["content"]: print("-", s.get("title"), "|", s.get("condition"))
print("caractères", len(out))
