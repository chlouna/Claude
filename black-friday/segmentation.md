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

Le segment « Plus tard » est personnalisé uniquement par les push (B et C) : dans l'app, il reçoit le message in-app offre classique.

## Code promo BF50

Le code **BF50** apparaît sur tous les visuels de l'offre (du 27 au 30/11) :
- messages in-app : offre, segment « Préviens-moi », segment « Plus tard », dernier jour ;
- bannière funnel d'achat, avec le rappel « Jusqu'au 30/11 à minuit » ;
- stories du 27, 28, 29 et 30/11, et posts Meta du 27 et du 30/11 ;
- textes des push A, B, C et D (voir plus bas).

Pas de code sur le teasing (20 → 26/11) : l'offre n'y est pas encore dévoilée.
À vérifier : le code doit être actif sur les stores dans les 7 pays, du 27/11 au 30/11 à minuit.

## 2. Le parcours

| Date | Intéressés | Plus tard | Tous les autres |
|---|---|---|---|
| 27/11 matin | Push A + message in-app `2a-interesses` | Push B + message in-app `2-offre` | Message in-app `2-offre` |
| 28 → 29/11 | Message in-app `2-offre` si pas acheté | Message in-app `2-offre` si pas acheté | Message in-app `2-offre` |
| 29/11 | — | Push C si pas acheté | — |
| 30/11 | Push D + message in-app `3-dernier-jour` si pas acheté | Push D + message in-app `3-dernier-jour` si pas acheté | Message in-app `3-dernier-jour` |

Règles : à chaque achat, la personne sort du parcours. Un seul message in-app par ouverture d'app. Pas plus d'une push par jour.

## 3. Textes des push (titre · texte)

Pas d'emoji (règle Truckfly pour les messages GPS). Tutoiement dans toutes les langues. Ton : complice, vocabulaire de la route. Chaque push se termine par le code promo BF50.

### Push A · 27/11 · Intéressés
- **FR** · Promesse tenue · Le GPS Premium est à -50 %. Tu es parmi les premiers à le savoir. Code BF50.
- **EN** · Promise kept · GPS Premium is 50% off. You're among the first to know. Code BF50.
- **DE** · Versprochen ist versprochen · GPS Premium zum halben Preis. Du gehörst zu den Ersten, die es wissen. Code BF50.
- **IT** · Promessa mantenuta · GPS Premium a -50%. Sei tra i primi a saperlo. Codice BF50.
- **ES** · Promesa cumplida · GPS Premium al -50 %. Eres de los primeros en saberlo. Código BF50.
- **NL** · Beloofd is beloofd · GPS Premium voor de halve prijs. Jij hoort het als een van de eersten. Code BF50.
- **PL** · Obietnica dotrzymana · GPS Premium -50%. Wiesz o tym przed innymi. Kod BF50.

### Push B · 27/11 · Plus tard
- **FR** · On te l'a gardée de côté · Le GPS Premium à moitié prix, mais seulement jusqu'au 30/11. Code BF50.
- **EN** · We kept it aside for you · GPS Premium at half price, but only until 30/11. Code BF50.
- **DE** · Wir haben es für dich zurückgelegt · GPS Premium zum halben Preis, aber nur bis 30.11. Code BF50.
- **IT** · Te l'abbiamo tenuta da parte · GPS Premium a metà prezzo, ma solo fino al 30/11. Codice BF50.
- **ES** · Te la hemos guardado · GPS Premium a mitad de precio, solo hasta el 30/11. Código BF50.
- **NL** · We hebben hem voor je apart gehouden · GPS Premium voor de halve prijs, maar alleen t/m 30/11. Code BF50.
- **PL** · Odłożyliśmy ją dla ciebie · GPS Premium za pół ceny, ale tylko do 30.11. Kod BF50.

### Push C · 29/11 · Plus tard, pas encore acheté
- **FR** · Dernière sortie avant la fin · Plus qu'un jour pour le GPS Premium à moitié prix. Code BF50.
- **EN** · Last exit before the end · One day left for GPS Premium at half price. Code BF50.
- **DE** · Letzte Ausfahrt vor dem Ende · Nur noch ein Tag: GPS Premium zum halben Preis. Code BF50.
- **IT** · Ultima uscita prima della fine · Manca un giorno: GPS Premium a metà prezzo. Codice BF50.
- **ES** · Última salida antes del final · Queda un día: GPS Premium a mitad de precio. Código BF50.
- **NL** · Laatste afslag voor het einde · Nog één dag: GPS Premium voor de halve prijs. Code BF50.
- **PL** · Ostatni zjazd przed końcem · Został jeden dzień: GPS Premium za pół ceny. Kod BF50.

### Push D · 30/11 · Tous ceux qui ont cliqué, pas encore acheté
- **FR** · La barrière se ferme à minuit · Dernières heures pour le GPS Premium à 37,99 €/an. Code BF50.
- **EN** · The barrier closes at midnight · Final hours for GPS Premium at £31.99/year. Code BF50.
- **DE** · Um Mitternacht geht die Schranke zu · Letzte Stunden: GPS Premium für 37,99 €/Jahr. Code BF50.
- **IT** · A mezzanotte si chiude la sbarra · Ultime ore: GPS Premium a 37,99 €/anno. Codice BF50.
- **ES** · A medianoche se baja la barrera · Últimas horas: GPS Premium a 37,99 €/año. Código BF50.
- **NL** · Om middernacht gaat de slagboom dicht · Laatste uren: GPS Premium voor € 37,99/jaar. Code BF50.
- **PL** · O północy zamykamy szlaban · Ostatnie godziny: GPS Premium za 166,99 zł/rok. Kod BF50.

## 4. À mesurer

- Taux de clic « Préviens-moi » et « Plus tard » sur le teasing.
- Taux d'achat par segment : Intéressés, Plus tard, Tous les autres.
- Si « Plus tard » convertit bien avec la push C, garder ce schéma pour les prochaines promos.
