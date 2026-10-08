# Interstitiels Profil Trucker et Social Core

Objectif : j'ouvre l'app → je comprends la nouveauté → j'ai envie de créer mon profil.

- `index.html` : les 9 écrans au format téléphone (390 × 844), avec de petites animations d'entrée.
- `png/` : un PNG par écran en 1170 × 2532 (iPhone, ×3), plus `planche.png` (aperçu de l'ensemble).
- `mp4/` : 1 interstitiel = 1 vidéo, 9 fichiers MP4 séparés (1080 × 2338, 30 i/s, 4 s).
- Régénérer : `python3 scripts/generer.py`, puis `node scripts/capturer.mjs` (PNG) et `node scripts/animer.mjs` (MP4 ; `node scripts/animer.mjs 4 i04` pour un seul écran).

| # | Fichier | Quand l'afficher | CTA |
|---|---|---|---|
| 1 | `i01-decouverte` | Lancement, première ouverture après la mise à jour | Créer mon Profil Trucker |
| 2 | `i02-profil-trucker` | Utilisateur sans profil | Créer mon profil |
| 3 | `i03-personnalisation` | Profil commencé (≈ 50 %) | Personnaliser mon profil |
| 4 | `i04-ajouter-amis` | Profil créé, aucun ami | Ajouter mes amis |
| 5 | `i05-invitations` | Invitation reçue non lue | Voir mes invitations |
| 6 | `i06-activite-amis` | Au moins un ami actif | Voir l'activité |
| 7 | `i07-recommandations` | Un ami a déposé un avis | Découvrir les recommandations |
| 8 | `i08-camion` | Profil sans camion | Ajouter mon camion |
| 9 | `i09-rappel` | Profil ouvert mais incomplet | Compléter mon profil |

## Choix de charte

- **Écran 1** en pleine page bleue, avec un bouton jaune (comme « Connexion gratuite » dans l'app). Les autres ont un visuel bleu en haut et une feuille blanche ajustée au texte en bas, avec un bouton Michelin Blue : la charte réserve le jaune au fond bleu.
- **« Michelin Truckfly »** en casse normale partout.
- **Titres** en Bib, **interface** en Inter, comme dans les vidéos. Pas de barre d'état (heure, réseau) : l'app l'affiche déjà.
- **Exemples** : Charlie G., Louna, David, Nicolas J., Vanessa Y. et les dimensions du camion sont des exemples fictifs, repris des vidéos. Les avatars et photos sont des illustrations.
