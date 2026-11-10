# Message in-app « Dernier jour » avec compte à rebours (HTML)

Un fichier par langue : `dernier-jour-timer-<langue>.html` (FR, EN, DE, IT, ES, NL, PL), environ 350 Ko chacun.
Chaque fichier est autonome : polices, logo et téléphone sont intégrés, aucun appel extérieur.

- **Compte à rebours** : heures, minutes et secondes jusqu'au 30/11/2026 à 23 h 59 min 59 s, heure de Paris (heure de Londres pour l'anglais). Il se calcule sur l'horloge du téléphone et tourne en direct.
- **Après la fin** : le compteur est remplacé par « L'offre est terminée » et le bouton disparaît (au cas où le message reste affiché après minuit).
- **Plein écran** : la maquette s'adapte à la taille de l'écran (`100vw × 100vh`).
- **Bouton « J'en profite »** : c'est un vrai lien. Remplacer `LIEN_ABONNEMENT_GPS_PREMIUM` par le lien profond vers l'abonnement, ou par l'action prévue par l'outil de messages in-app (certains outils demandent un attribut ou un appel JavaScript à la place d'un lien).
- **Bouton de fermeture** : non inclus, il est normalement ajouté par l'outil de messages in-app.

Régénérer : `node black-friday/scripts/generer-inapp-timer.mjs` (après une modification de `campagne.html`).
Les dates de fin et les textes du compteur sont en haut du script (`FIN` et `TXT`).
