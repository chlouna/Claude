# Storyboard : Profil Trucker, version 9 (25 s)

Message : crée ton Profil Trucker, ajoute tes amis et découvre leur activité au quotidien. Le Profil Trucker est un espace social pour les conducteurs.
Diffusion : Instagram en priorité (9:16, 1080 × 1920), plus une version 16:9 (1920 × 1080).
Source : `scripts/generer.py` produit `index.html` et `compositions/vertical.html`.

## Style

- **Titres** en Bib (charte). **Éléments de l'app** en Inter, l'équivalent libre de la police système de l'iPhone.
- **Notifications et cartes** au style du fil d'activité (référence : « Nicolas J. a visité : »).
- **Avatars** au style par défaut de l'app (référence : Abdelatif). Je n'utilise aucune photo de vrais utilisateurs.
- **Intro** : un grand avatar à côté de chaque notification, en quinconce, avec un halo blanc pour se détacher du fond bleu.
- Pas de logo, pas d'emoji, pas de musique.

## Déroulé

| # | Minutage | Texte | Animation |
|---|---|---|---|
| Intro | 0 → 4,6 s | Notifications : Nicolas J. a visité : **AS 24** · David a déposé un avis chez : **Le Relais des Cigales** · **Louna vous a envoyé une invitation** | Les rangées arrivent à 0,2 s, 0,6 s et 1 s. Tap sur « Accepter », le bouton devient « ✓ Amis » et l'avatar de Louna saute. |
| 1 | 4,6 → 7,6 s | **Crée et personnalise / ton profil** | Profil de Louna. Cadre autour des boutons et tap sur « Modifier le profil ». Flèche et tap sur le camion, puis tap sur « Partager ». |
| 2 | 7,6 → 10,4 s | **Ajoute tes amis** | « Trouver des routiers ». Flèche et tap sur « Ajouter » (Vanessa Y.), le bouton devient « En attente », avec une horloge qui tourne. |
| 3 | 10,4 → 13,4 s | **Invitation acceptée** | Le téléphone de l'ami (onglet Invitations) : la demande de Louna C. arrive. Flèche et tap sur « Accepter », la ligne passe à « ✓ Amis ». |
| 4 | 13,4 → 16 s | **Découvre leur activité / au quotidien** | Accueil « Salut louna ! ». Flèche et tap sur la carte « Nicolas J. a visité : AS 24 Calais Eurotunnel ». |
| 5 | 16 → 18,6 s | **Regarde qui est en ligne** | Même écran. Anneaux verts autour des amis « On the road », « 5 amis en ligne » entouré, flèche vers la rangée. |
| Rappel | 18,6 → 21,4 s | **Pense à regarder tes invitations** / pour ne pas manquer une demande d'ami ! | Fond bleu, texte seul. |
| Fin | 21,4 → 25 s | **Ne roule plus seul !** / bouton « Télécharge Michelin Truckfly » | Fond bleu. Le bouton pulse doucement. |

Durée imposée : 25 s au maximum. Pour la tenir, plusieurs textes restent à l'écran moins longtemps que la règle de lecture (1,5 s + 0,3 s par mot), en particulier la notification de David (3,4 s au lieu de 4,5 s) et le rappel (2,4 s au lieu de 5,1 s).

## Fonctionnalités sociales montrées

| Fonctionnalité | Où |
|---|---|
| Établissements fréquentés et recommandations des proches | Intro, étape 4 |
| Personnaliser son profil, ajouter son camion, partager son profil | Étape 1 |
| Envoyer une invitation, demande en attente, demande acceptée | Intro, étapes 2 et 3, rappel |
| Suivre l'activité de ses proches | Étape 4 |
| Voir qui est en ligne | Étape 5 |

## Recréé pour la vidéo, à valider

Ces éléments ne viennent pas d'une capture :
- les notifications de l'intro (textes fournis) et le bouton « Accepter » / « ✓ Amis » ;
- le bouton « En attente » sur l'écran « Trouver des routiers » ;
- la ligne « Louna C. » à la place de « Valentin T. » sur l'écran Invitations, et son état « ✓ Amis ».

La capture « On the road » contient de vraies photos d'utilisateurs (Clémentine, Nicolas J.). Elle est utilisée à la demande de l'utilisateur.

Le gris des textes secondaires est un peu plus foncé que dans l'app (`#6E6E73`), pour rester lisible.
