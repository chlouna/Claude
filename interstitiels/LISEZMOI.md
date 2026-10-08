# Interstitiels Profil Trucker et Social Core

Objectif : j'ouvre l'app → je comprends la nouveauté → j'ai envie de créer mon profil.

- `index.html` : les 12 écrans au format téléphone (390 × 844), avec de petites animations d'entrée.
- `png/` : un PNG par écran en 1170 × 2532 (iPhone, ×3), plus `planche.png`.
- `mp4/` : un MP4 animé par écran (1080 × 2338, 30 i/s, 4 s), plus `montage-12-interstitiels.mp4` (48 s).
- Régénérer : `python3 scripts/generer.py`, puis `node scripts/capturer.mjs` (PNG) et `node scripts/animer.mjs` (MP4 ; `node scripts/animer.mjs 4 i04` pour un seul écran).

| # | Fichier | Quand l'afficher | CTA |
|---|---|---|---|
| 1 | `i01-decouverte` | Lancement, première ouverture après la mise à jour | Créer mon Profil Trucker |
| 2 | `i02-profil-trucker` | Utilisateur sans profil | Créer mon profil |
| 3 | `i03-personnalisation` | Profil commencé (≈ 50 %) | Personnaliser mon profil |
| 4 | `i04-ajouter-amis` | Profil créé, aucun ami | Ajouter mes amis |
| 5 | `i05-invitations` | Invitation reçue non lue | Voir mes invitations |
| 6 | `i06-social-core` | Première visite de l'onglet Communauté | Découvrir |
| 7 | `i07-activite-amis` | Au moins un ami actif | Voir l'activité |
| 8 | `i08-recommandations` | Un ami a déposé un avis | Découvrir les recommandations |
| 9 | `i09-camion` | Profil sans camion | Ajouter mon camion |
| 10 | `i10-rappel` | Profil ouvert mais incomplet | Compléter mon profil |
| 11 | `i11-profil-pret` | Juste après un profil complété à 100 % | Ajouter mes amis |
| 12 | `i12-ne-roule-plus-seul` | Grand interstitiel de campagne | Créer mon Profil Trucker |

## Choix de charte

- **Écrans 1 et 12** en pleine page bleue, avec un bouton jaune (comme « Connexion gratuite » dans l'app). Les autres ont un visuel bleu en haut et une feuille blanche en bas, avec un bouton Michelin Blue : la charte réserve le jaune au fond bleu.
- **« Ne roule plus seul ! »** est en casse de phrase, pas en capitales : la charte interdit le texte tout en capitales.
- **Titres** en Bib, **interface** en Inter, comme dans les vidéos. Les emojis (👀, 🚛, 🎉) sont ceux de ton brief.
- **Exemples** : Charlie G., Louna, David, Nicolas J., Vanessa Y. et les dimensions du camion sont des exemples fictifs, repris des vidéos. Les avatars et photos sont des illustrations.
