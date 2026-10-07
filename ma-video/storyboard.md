# Storyboard : Profil Trucker, version 4 (23,2 s)

Message : crée ton Profil Trucker, retrouve tes amis et rejoins la communauté des conducteurs sur Michelin Truckfly.
Diffusion : Instagram en priorité (9:16, 1080 × 1920), plus une version 16:9 (1920 × 1080).
Source : `scripts/generer.py` produit `index.html` et `compositions/vertical.html`.

## Style

- **Titres** en Bib (charte). **Éléments de l'app** (notifications, cartes, bouton « Invité ») en Inter, l'équivalent libre de la police système de l'iPhone, qu'on ne peut pas embarquer.
- **Notifications** au style des cartes du fil d'activité (référence : « Nicolas J. a visité : »). On y trouve l'avatar avec sa pastille, une ligne grise, le lieu en gras, l'heure et une épingle avec la ville.
- **Avatars** au style par défaut de l'app (référence : Abdelatif) : visage de couleur, anneau épais, yeux et initiale. Je n'utilise aucune photo de vrais utilisateurs.
- **Interactions** :
  - un tap = un rond qui se pose, puis une onde ;
  - des flèches courbes qui se dessinent ;
  - un cadre autour des boutons ;
  - le bouton qui passe à « Invité » ;
  - une nouvelle carte qui arrive dans le fil ;
  - un zoom léger.
- Pas de logo, pas d'emoji, pas de musique.

## Déroulé

| # | Minutage | Texte | Ce qui se passe sur le téléphone |
|---|---|---|---|
| Intro | 0 → 5,5 s | Notifications : **Louna vous a envoyé une invitation** · David a visité : **Restaurant Chez Marcel**, Lyon · **Nordin a déposé un avis** | Le fil d'activité est affiché. Les notifications arrivent à 0,3 s, 0,9 s et 1,5 s. Tap sur celle de Louna à 3 s. |
| 1 | 5,5 → 9,7 s | **Crée ton Profil Trucker** / pour que tes amis te retrouvent ! | Le profil de Louna arrive. Tap sur l'avatar à 7,3 s. |
| 2 | 9,7 → 12,7 s | **Personnalise / et partage ton profil** | Cadre et flèche vers les boutons. Tap sur « Modifier le profil » à 10,7 s, puis sur « Partager » à 11,6 s. |
| 3 | 12,7 → 15,1 s | **Retrouve tes amis** | Écran « Trouver des routiers ». Flèche, tap sur « Ajouter » à 13,6 s, le bouton passe à « ✓ Invité ». |
| 4 | 15,1 → 18,7 s | **Suis l'activité de / tes proches au quotidien** | Fil d'activité. Une nouvelle carte arrive (Louna a visité : **AS 24 Calais Eurotunnel**, Coquelles), puis le téléphone zoome légèrement. |
| 5 | 18,7 → 23,2 s | **Ne roule plus seul !** / Rejoins la communauté sur Michelin Truckfly | Fond bleu, texte seul. |

## Écarts par rapport à l'app

- Le gris des textes secondaires est un peu plus foncé que dans l'app (`#6E6E73` au lieu de `#8E8E93`), pour rester lisible en vidéo.
- Le bouton « ✓ Invité » et la carte « Louna a visité : AS 24 Calais Eurotunnel » sont recréés pour la vidéo. Ils ne viennent pas d'une capture.
