# Reel GPS : signaler les alertes (15 s)

Vidéo : `reel-gps-alertes.mp4` (Reel Instagram, 9:16, 1080 × 1920, 30 i/s, 15 s, sans son).
Régénérer : `node maj-6-4/reel-gps/rendre.mjs` (ou `rendre.mjs 2,5,8` pour des aperçus PNG).

## Déroulé

| Temps | Texte à l'écran | Ce qui se passe |
|---|---|---|
| 0–2,7 s | GPS Michelin Truckfly / **Signale les alertes sur ta route** | Titre et picto d'alerte |
| 2,7–5,6 s | Repère les alertes sur ton trajet | Capture de l'itinéraire ; cercles jaunes sur l'alerte et le contrôle |
| 5,6–8 s | Un souci sur la route ? / Clique sur le bouton jaune | Capture de la navigation ; tap sur le bouton jaune « + » |
| 8–9,6 s | Choisis ton alerte | Le panneau « Que veux-tu signaler ? » monte ; tap sur « Accident » |
| 9,6–11,4 s | Et préviens les autres conducteurs ! | « Alerte envoyée » ; l'alerte apparaît sur la carte |
| 11,6–15 s | **Sur la route, on se prévient !** / bouton « Télécharge Michelin Truckfly » | Le bouton jaune pulse |

## Légende

Un accident, un contrôle, des travaux sur ta route ?

Avec le GPS Michelin Truckfly, tu vois les alertes sur ton trajet avant de partir. Et si tu tombes sur un souci, un clic sur le bouton jaune suffit pour le signaler et prévenir tous les autres conducteurs.

Sur la route, on se prévient !

Télécharge Michelin Truckfly et roule mieux informé.

#Michelin #MichelinTruckfly #GPS #GPSPoidsLourd #Routiers #Trucker #CommunautéRoutière

## À valider

- **Panneau des alertes recréé** : le panneau « Que veux-tu signaler ? », ses 6 types (Contrôle, Accident, Bouchon, Travaux, Danger, Route fermée) et le message « Alerte envoyée » sont dessinés, pas tirés de l'app. Avec une capture du vrai panneau, on le remplace.
- **Captures** : `assets/itineraire.png` et `assets/navigation.png` sont celles fournies.

## Cadrage

Tout est centré horizontalement, avec 56 px de marge de chaque côté (en 540 × 960, soit 112 px en 1080 × 1920). Rien dans les 110 px du haut ni les 210 px du bas, où Instagram affiche son interface.
