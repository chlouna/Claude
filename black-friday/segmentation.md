# Black Friday 2026 · Segmentation app

Objectif : parler différemment à chacun le 27/11, selon sa réponse au message in-app teasing.

## 1. Le teasing crée les segments (20 → 26/11)

Message in-app `message-in-app-1-teasing`, deux boutons :

| Bouton | Segment créé | Ce que ça veut dire |
|---|---|---|
| « Préviens-moi le 27/11 » | **Intéressés** | Veut l'offre, attend le 27 |
| « Plus tard » | **Plus tard** | Pas convaincu, pas fermé |
| Fermé sans cliquer (croix) | Aucun → **Tous les autres** | Neutre |

Dans l'outil de messages in-app : un attribut ou un tag par bouton (ex. `bf26_interesse = true`, `bf26_plus_tard = true`). Si quelqu'un clique les deux sur des jours différents, garder le dernier clic.

Exclure partout ceux qui ont déjà GPS Premium.

## 2. Le parcours

| Date | Intéressés | Plus tard | Tous les autres |
|---|---|---|---|
| 27/11 matin | Push A + message in-app `2a-interesses` | Push B + message in-app `2b-plus-tard` | Message in-app `2-offre` |
| 28 → 29/11 | Message in-app `2-offre` si pas acheté | Message in-app `2-offre` si pas acheté | Message in-app `2-offre` |
| 29/11 | — | Push C si pas acheté | — |
| 30/11 | Push D + message in-app `3-dernier-jour` si pas acheté | Push D + message in-app `3-dernier-jour` si pas acheté | Message in-app `3-dernier-jour` |

Règles : à chaque achat, la personne sort du parcours. Un seul message in-app par ouverture d'app. Pas plus d'une push par jour.

## 3. Textes des push (titre · texte)

Pas d'emoji (règle Truckfly pour les messages GPS). Tutoiement dans toutes les langues. Ton : complice, vocabulaire de la route.

### Push A · 27/11 · Intéressés
- **FR** · Promesse tenue · Le GPS Premium est à -50 %. Tu es parmi les premiers à le savoir.
- **EN** · Promise kept · GPS Premium is 50% off. You're among the first to know.
- **DE** · Versprochen ist versprochen · GPS Premium zum halben Preis. Du gehörst zu den Ersten, die es wissen.
- **IT** · Promessa mantenuta · GPS Premium a -50%. Sei tra i primi a saperlo.
- **ES** · Promesa cumplida · GPS Premium al -50 %. Eres de los primeros en saberlo.
- **NL** · Beloofd is beloofd · GPS Premium voor de halve prijs. Jij hoort het als een van de eersten.
- **PL** · Obietnica dotrzymana · GPS Premium -50%. Wiesz o tym przed innymi.

### Push B · 27/11 · Plus tard
- **FR** · « Plus tard » vient d'arriver · Le GPS Premium à moitié prix, mais seulement jusqu'au 30/11.
- **EN** · “Later” has arrived · GPS Premium at half price, but only until 30/11.
- **DE** · „Später“ ist jetzt · GPS Premium zum halben Preis, aber nur bis 30.11.
- **IT** · «Più tardi» è arrivato · GPS Premium a metà prezzo, ma solo fino al 30/11.
- **ES** · «Más tarde» ya ha llegado · GPS Premium a mitad de precio, solo hasta el 30/11.
- **NL** · ‘Later’ is nu · GPS Premium voor de halve prijs, maar alleen t/m 30/11.
- **PL** · „Później” właśnie nadeszło · GPS Premium za pół ceny, ale tylko do 30.11.

### Push C · 29/11 · Plus tard, pas encore acheté
- **FR** · Dernière sortie avant la fin · Plus qu'un jour pour le GPS Premium à moitié prix.
- **EN** · Last exit before the end · One day left for GPS Premium at half price.
- **DE** · Letzte Ausfahrt vor dem Ende · Nur noch ein Tag: GPS Premium zum halben Preis.
- **IT** · Ultima uscita prima della fine · Manca un giorno: GPS Premium a metà prezzo.
- **ES** · Última salida antes del final · Queda un día: GPS Premium a mitad de precio.
- **NL** · Laatste afslag voor het einde · Nog één dag: GPS Premium voor de halve prijs.
- **PL** · Ostatni zjazd przed końcem · Został jeden dzień: GPS Premium za pół ceny.

### Push D · 30/11 · Tous ceux qui ont cliqué, pas encore acheté
- **FR** · La barrière se ferme à minuit · Dernières heures pour le GPS Premium à 37,99 €/an.
- **EN** · The barrier closes at midnight · Final hours for GPS Premium at £31.99/year.
- **DE** · Um Mitternacht geht die Schranke zu · Letzte Stunden: GPS Premium für 37,99 €/Jahr.
- **IT** · A mezzanotte si chiude la sbarra · Ultime ore: GPS Premium a 37,99 €/anno.
- **ES** · A medianoche se baja la barrera · Últimas horas: GPS Premium a 37,99 €/año.
- **NL** · Om middernacht gaat de slagboom dicht · Laatste uren: GPS Premium voor € 37,99/jaar.
- **PL** · O północy zamykamy szlaban · Ostatnie godziny: GPS Premium za 166,99 zł/rok.

## 4. À mesurer

- Taux de clic « Préviens-moi » et « Plus tard » sur le teasing.
- Taux d'achat par segment : Intéressés, Plus tard, Tous les autres.
- Si « Plus tard » convertit bien avec la push C, garder ce schéma pour les prochaines promos.
