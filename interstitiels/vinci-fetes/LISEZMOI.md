# Interstitiel Michelin Truckfly × VINCI Autoroutes · Fêtes de fin d'année

**Offre** : 2 mois de GPS offerts aux **1000 premiers** qui répondent au quiz sécurité.
**Thème** : nos anges gardiens (les patrouilleurs en jaune, un homme et une femme) veillent sur la route pendant les fêtes.
**Budget** : 4 710 €.
**Couleurs** : charte Michelin Truckfly (bleu, jaune) + rouge VINCI Autoroutes `#E20025` (bandeau du haut, badge, écharpes des anges, guirlande, bande du fourgon). Logo officiel : `assets/vinci-autoroutes.png`.

## Parcours

1. L'interstitiel s'affiche dans l'app (CTA « Je participe au quiz »).
2. Au clic, le conducteur arrive sur une autre page, le formulaire Tally : 3 questions sécurité, puis email + téléphone + consentement.
3. On récupère les emails et téléphones pour activer les 2 mois.
4. Le formulaire se ferme seul à 1000 réponses (une seule réponse par email).

Lien d'édition Tally (brouillon, pas encore publié) : https://tally.so/forms/q5L7Y2/edit

Pour savoir d'où vient chaque réponse, ouvrir le lien avec les paramètres `?user_id=…&source=interstitiel`.

Boutons (un par proposition) : A « Je veux mes 2 mois de GPS offerts », B « Je veux gagner 2 mois de GPS », C « Je déballe mes 2 mois de GPS », D « Je veux mes 2 mois de GPS gratuits », avec « Plus tard » en dessous.

## Fichiers

- `index.html` : les 3 propositions au format téléphone (390 × 844), avec de petites animations.
- `png/` : un PNG par proposition en 1170 × 2532, plus `planche.png`.
- Régénérer les PNG : `node interstitiels/vinci-fetes/capturer.mjs`.

| # | Proposition | Titre | CTA |
|---|---|---|---|
| A | Pleine page : les deux anges gardiens au bord de l'autoroute, fourgon de patrouille | Ils veillent sur toi, on t'offre 2 mois de GPS | Je veux mes 2 mois de GPS offerts |
| B | Visuel + feuille blanche, étiquette « 2 mois » | Cette année, le Père Noël porte un gilet jaune | Je veux gagner 2 mois de GPS |
| C | Un cadeau avant l'heure : sapin décoré d'anges en gilet jaune (un en haut du sapin), gros cadeau blanc et rouge sous le sapin avec l'étiquette « 2 mois de GPS offerts » | Sous le sapin, 2 mois de GPS offerts | Je déballe mes 2 mois de GPS |
| D | Pleine page : le Père Noël (manches rouges) et ses deux lutins, tous en gilet jaune de patrouilleur, au bord de l'autoroute | Le Père Noël et ses lutins t'offrent 2 mois de GPS | Je veux mes 2 mois de GPS gratuits |

## Brief VINCI Autoroutes (Lola, d'après le dépliant « Corridor de sécurité »)

- **Accroche** demandée : « Pour leur sécurité et la vôtre, préservez la sécurité de vos anges gardiens pendant les fêtes de fin d'année. »
  Version utilisée (tutoiement de l'app, sans la répétition de « sécurité ») : « Pour leur sécurité et la tienne, protège tes anges gardiens pendant les fêtes de fin d'année. »
- **Pictogrammes + message** en haut de chaque interstitiel, avec les personnages : « À l'approche d'un véhicule d'intervention : JE RALENTIS / JE CHANGE DE VOIE ». Le schéma (voies, flèche du panneau en pointillés, fourgon, voiture qui change de voie) reproduit le modèle du dépliant ; à remplacer par le fichier officiel si VINCI le fournit.
- **Ordre en haut de l'écran** : logos, accroche VINCI, puis le schéma avec « À l'approche d'un véhicule d'intervention : JE RALENTIS / JE CHANGE DE VOIE », puis les personnages. En bas : badge, titre, texte de l'offre, bouton.
- **Amende de 135 €** : question 2 du quiz.
- **Règles de sécurité sur autoroute** : rappelées sur la page de remerciement du formulaire.

## Quiz (3 questions)

1. **Un véhicule d'intervention est arrêté sur la bande d'arrêt d'urgence, gyrophares allumés. Que fais-tu ?**
   - Je garde ma voie et ma vitesse
   - ✅ Je ralentis et je change de voie, ou je m'écarte le plus possible
   - Je klaxonne pour signaler ma présence
2. **Que risques-tu si tu ne respectes pas le corridor de sécurité ?**
   - Rien, c'est une simple recommandation
   - ✅ Une amende de 135 € (depuis septembre 2018, article R412-11-1 du code de la route)
   - Un simple avertissement
3. **Ton camion tombe en panne sur l'autoroute. Quel est le bon réflexe ?**
   - Je reste dans ma cabine, ceinture attachée, en attendant les secours
   - ✅ Feux de détresse, gilet enfilé, je sors et je me mets derrière la glissière
   - Je pose mon triangle de pré-signalisation derrière le camion

**Le saviez-vous ?** (repris du dépliant)
- Après la question 1 : 67 % des conducteurs français n'appliquent pas systématiquement la règle du corridor de sécurité (Baromètre de la conduite responsable, Ipsos pour la Fondation VINCI Autoroutes, 2024).
- Sur la page email : un balisage est une zone d'intervention interdite d'accès ; des aires sont accessibles tous les 15 km environ.

La page de remerciement donne les bonnes réponses et rappelle les règles de sécurité sur autoroute du dépliant : en cas de panne ou d'accident (feux de détresse, bande d'arrêt d'urgence ou refuge, gilet, évacuer, derrière la glissière, borne orange, 112, pas de triangle) et si l'on est témoin d'un accident (rouler jusqu'à la borne d'appel d'urgence).

## À compléter avant diffusion

- Validation du visuel et du logo par VINCI Autoroutes.
- Date de fin de l'offre si VINCI en veut une en plus de la limite des 1000 premiers.
- Mentions légales du jeu (règlement, RGPD) : lien à ajouter dans le formulaire.
- Publier le formulaire Tally et mettre son lien sur le CTA.
