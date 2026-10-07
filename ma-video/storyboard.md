# Storyboard : Profil Trucker, version 5 (25,3 s)

Message : crée ton Profil Trucker, ajoute tes amis et découvre leur activité au quotidien. Le Profil Trucker est un espace social pour les conducteurs.
Diffusion : Instagram en priorité (9:16, 1080 × 1920), plus une version 16:9 (1920 × 1080).
Source : `scripts/generer.py` produit `index.html` et `compositions/vertical.html`.

## Style

- **Titres** en Bib (charte). **Éléments de l'app** en Inter, l'équivalent libre de la police système de l'iPhone.
- **Notifications et cartes** au style du fil d'activité (référence : « Nicolas J. a visité : »).
- **Avatars** au style par défaut de l'app (référence : Abdelatif). Je n'utilise aucune photo de vrais utilisateurs.
- **Personnages** : trois conducteurs en buste, avec une casquette, un téléphone en main et une pastille verte « en ligne ».
- Pas de logo, pas d'emoji, pas de musique.

## Déroulé

| # | Minutage | Texte | Animation |
|---|---|---|---|
| Intro | 0 → 6 s | Notifications : **Louna vous a envoyé une invitation** · **Nicolas J. a visité votre profil** · David s'est arrêté ici : **Restaurant Chez Marcel**, Lyon | Louna, Nicolas J. et David apparaissent, en ligne. À chaque notification, un lien se trace entre deux d'entre eux et le téléphone du destinataire vibre. Tap sur « Accepter », qui devient « ✓ Amis », et Louna et Nicolas sautent de joie. Aucun téléphone en arrière-plan. |
| 1 | 6 → 9,8 s | **Crée et personnalise / ton profil** | Profil de Louna. Un cadre entoure les boutons, puis tap sur « Modifier le profil ». Flèche et tap sur le camion (« Poids lourds / Semi »), puis tap sur « Partager ». |
| 2 | 9,8 → 14,2 s | **Ajoute tes amis** | « Trouver des routiers ». Flèche et tap sur « Ajouter », le bouton passe à « ✓ Invité », puis la notification « David a accepté votre invitation » arrive. |
| 3 | 14,2 → 17,8 s | **Découvre leur activité / au quotidien** | Fil d'activité. Une nouvelle carte arrive (Maxime V. a visité : **Cournon**, Cournon-d'Auvergne), une flèche montre où il s'est arrêté, puis tap sur la carte. |
| 4 | 17,8 → 20,6 s | **Visite leurs profils** | Le profil de Maxime V. s'ouvre depuis la carte. Une flèche vise ses statistiques, une autre son dernier arrêt. |
| 5 | 20,6 → 25,3 s | **Ne roule plus seul !** / Crée ton réseau sur Michelin Truckfly | Fond bleu, texte seul. |

## Fonctionnalités sociales montrées

| Fonctionnalité | Où |
|---|---|
| Envoyer et recevoir des invitations, demandes acceptées | Intro, étape 2 |
| Visiter le profil de ses amis | Intro (« a visité votre profil »), étape 4 |
| Voir qui est en ligne | Intro (pastilles vertes) |
| Voir où ses amis se sont arrêtés | Intro (David), étapes 3 et 4 |
| Personnaliser son profil, ajouter son camion, partager son profil | Étape 1 |
| Ajouter ses amis | Étape 2 |
| Suivre l'activité de ses proches | Étape 3 |
| Créer son réseau | Liens entre les personnages dans l'intro, phrase de fin |

## Recréé pour la vidéo, à valider

Ces éléments ne viennent pas d'une capture :
- le bouton « Accepter » / « ✓ Amis » ;
- le bouton « ✓ Invité » ;
- les notifications de l'intro ;
- « David a accepté votre invitation » ;
- la carte « Maxime V. a visité : Cournon » en haut du fil.

Le gris des textes secondaires est un peu plus foncé que dans l'app (`#6E6E73`), pour rester lisible.
