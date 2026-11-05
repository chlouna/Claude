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

Pas d'emoji (règle Truckfly pour les messages GPS). Tutoiement dans toutes les langues.

### Push A · 27/11 · Intéressés
- **FR** · Black Friday : c'est parti · On t'avait promis de te prévenir : le GPS Premium est à -50 % jusqu'au 30/11.
- **EN** · Black Friday is on · As promised: GPS Premium is 50% off until 30/11.
- **DE** · Black Friday ist da · Wie versprochen: GPS Premium bis 30.11. zum halben Preis.
- **IT** · Il Black Friday è iniziato · Come promesso: GPS Premium a -50% fino al 30/11.
- **ES** · Ya está aquí el Black Friday · Te lo prometimos: GPS Premium al -50 % hasta el 30/11.
- **NL** · Black Friday is begonnen · Zoals beloofd: GPS Premium t/m 30/11 voor de halve prijs.
- **PL** · Black Friday wystartował · Tak jak obiecaliśmy: GPS Premium -50% do 30.11.

### Push B · 27/11 · Plus tard
- **FR** · Tu avais dit « plus tard » · C'est maintenant : le GPS Premium est à moitié prix jusqu'au 30/11.
- **EN** · You said “later” · Well, it's now: GPS Premium is half price until 30/11.
- **DE** · Du hast „später“ gesagt · Jetzt ist es so weit: GPS Premium bis 30.11. zum halben Preis.
- **IT** · Avevi detto «più tardi» · È il momento: GPS Premium a metà prezzo fino al 30/11.
- **ES** · Dijiste «más tarde» · Es ahora: GPS Premium a mitad de precio hasta el 30/11.
- **NL** · Je zei ‘later’ · Nou, het is nu: GPS Premium t/m 30/11 voor de halve prijs.
- **PL** · „Później” właśnie nadeszło · GPS Premium za pół ceny do 30.11.

### Push C · 29/11 · Plus tard, pas encore acheté
- **FR** · Plus qu'un jour · Demain soir, le GPS Premium repasse à 74,99 €.
- **EN** · Only one day left · Tomorrow night, GPS Premium goes back to £63.98.
- **DE** · Nur noch ein Tag · Morgen Abend kostet GPS Premium wieder 74,99 €.
- **IT** · Manca solo un giorno · Domani sera GPS Premium torna a 74,99 €.
- **ES** · Solo queda un día · Mañana por la noche, GPS Premium vuelve a 74,99 €.
- **NL** · Nog maar één dag · Morgenavond kost GPS Premium weer € 74,99.
- **PL** · Został tylko jeden dzień · Jutro wieczorem GPS Premium wraca do 333,98 zł.

### Push D · 30/11 · Tous ceux qui ont cliqué, pas encore acheté
- **FR** · Dernier jour · Le GPS Premium à 37,99 €/an, c'est jusqu'à minuit.
- **EN** · Last day · GPS Premium at £31.99/year, until midnight.
- **DE** · Letzter Tag · GPS Premium für 37,99 €/Jahr, nur bis Mitternacht.
- **IT** · Ultimo giorno · GPS Premium a 37,99 €/anno, fino a mezzanotte.
- **ES** · Último día · GPS Premium a 37,99 €/año, hasta medianoche.
- **NL** · Laatste dag · GPS Premium voor € 37,99/jaar, tot middernacht.
- **PL** · Ostatni dzień · GPS Premium za 166,99 zł/rok, tylko do północy.

## 4. À mesurer

- Taux de clic « Préviens-moi » et « Plus tard » sur le teasing.
- Taux d'achat par segment : Intéressés, Plus tard, Tous les autres.
- Si « Plus tard » convertit bien avec la push C, garder ce schéma pour les prochaines promos.
