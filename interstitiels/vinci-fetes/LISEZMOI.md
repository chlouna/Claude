# Interstitiel Michelin Truckfly × VINCI Autoroutes · Fêtes de fin d'année

**Offre** : 2 mois de GPS offerts aux **1000 premiers** qui répondent au quiz sécurité.
**Thème** : nos anges gardiens (les patrouilleurs en jaune, un homme et une femme) veillent sur la route pendant les fêtes.
**Budget** : 4 710 €.
**Couleurs** : charte Michelin Truckfly (bleu, jaune) + rouge VINCI Autoroutes `#E20025` (bandeau du haut, badge, écharpes des anges, guirlande, bande du fourgon). Logo officiel : `assets/vinci-autoroutes.png`.

## Parcours

1. L'interstitiel s'affiche dans l'app (CTA « Je participe au quiz »).
2. Au clic, le conducteur arrive sur une autre page, le formulaire Tally : 2 questions sécurité, puis email + téléphone + consentement.
3. On récupère les emails et téléphones pour activer les 2 mois.
4. Le formulaire se ferme seul à 1000 réponses (une seule réponse par email).

Lien d'édition Tally (brouillon, pas encore publié) : https://tally.so/forms/q5L7Y2/edit

Pour savoir d'où vient chaque réponse, ouvrir le lien avec les paramètres `?user_id=…&source=interstitiel`.

## Fichiers

- `index.html` : les 3 propositions au format téléphone (390 × 844), avec de petites animations.
- `png/` : un PNG par proposition en 1170 × 2532, plus `planche.png`.
- Régénérer les PNG : `node interstitiels/vinci-fetes/capturer.mjs`.

| # | Proposition | Titre | CTA |
|---|---|---|---|
| A | Pleine page : les deux anges gardiens au bord de l'autoroute, fourgon de patrouille | Ils veillent sur toi, on t'offre 2 mois de GPS | Je participe au quiz |
| B | Visuel + feuille blanche, étiquette « 2 mois » | Cette année, le Père Noël porte un gilet jaune | Répondre au quiz |
| C | Un cadeau avant l'heure : sapin décoré d'anges en gilet jaune (un en haut du sapin), gros cadeau blanc et rouge sous le sapin avec l'étiquette « 2 mois de GPS offerts » | Sous le sapin, 2 mois de GPS offerts | Je déballe mon cadeau |

## Quiz (2 questions)

1. **Un véhicule de patrouille est arrêté sur la bande d'arrêt d'urgence, gyrophares allumés. Que fais-tu ?**
   - Je garde ma voie et ma vitesse
   - ✅ Je change de voie pour m'écarter, ou je ralentis fortement si c'est impossible (corridor de sécurité)
   - Je klaxonne pour signaler ma présence
2. **Ton camion tombe en panne sur l'autoroute. Quel est le bon réflexe ?**
   - Je reste dans la cabine en attendant les secours
   - ✅ J'enfile mon gilet, je passe derrière la glissière et j'appelle les secours
   - Je reste devant le camion pour faire signe aux autres

Les bonnes réponses s'affichent sur la page de remerciement. Elles sont à faire valider par VINCI Autoroutes.

## À compléter avant diffusion

- Validation du visuel et du logo par VINCI Autoroutes.
- Date de fin de l'offre si VINCI en veut une en plus de la limite des 1000 premiers.
- Mentions légales du jeu (règlement, RGPD) : lien à ajouter dans le formulaire.
- Publier le formulaire Tally et mettre son lien sur le CTA.
