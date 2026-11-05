# Reel GPS : signaler les alertes (15 s)

Vidéo : `reel-gps-alertes.mp4` (Reel Instagram, 9:16, 1080 × 1920, 30 i/s, 15 s, sans son).
Régénérer : `node maj-6-4/reel-gps/rendre.mjs` (ou `rendre.mjs 2,5,8` pour des aperçus PNG).

## Déroulé

| Temps | Texte à l'écran | Ce qui se passe |
|---|---|---|
| 0–2,7 s | **Un souci sur la route ? Signale-le !** | Titre et picto d'alerte |
| 2,7–5,3 s | Clique sur le bouton jaune | Capture de la navigation (25 km/h) ; tap sur le bouton jaune « + » |
| 5,3–8,3 s | Choisis ton alerte | Le panneau « Signaler » monte ; tap sur « Accident » |
| 8,3–11,4 s | Et préviens les autres conducteurs ! | « Alerte envoyée » ; l'alerte apparaît sur la carte |
| 11,6–15 s | **Sur la route, on se prévient !** / bouton « Télécharge Michelin Truckfly » | Le bouton jaune pulse |

## Légende

Un accident, un contrôle, des travaux sur ta route ?

Avec le GPS Michelin Truckfly, tu vois les alertes sur ton trajet avant de partir. Et si tu tombes sur un souci, un clic sur le bouton jaune suffit pour le signaler et prévenir tous les autres conducteurs.

Sur la route, on se prévient !

Télécharge Michelin Truckfly et roule mieux informé.

#Michelin #MichelinTruckfly #GPS #GPSPoidsLourd #Routiers #Trucker #CommunautéRoutière

## À valider

- **Panneau « Signaler »** : repris de la capture fournie (`assets/reference-signaler.png`) : titre, « N’appuyez qu’une fois en sécurité » et les 6 alertes (Accident, Danger, Problème de carte, Zone de contrôle, Embouteillage, Zone peu sûre). La capture fait 145 × 286 px, trop petite pour la vidéo : le panneau est redessiné en net et les pictos sont simplifiés.
- **Vitesse** : 25 km/h affiché à la place de la vitesse de la capture.
- **« Alerte envoyée »** : message dessiné, pas tiré de l'app.

## Cadrage

Tout est centré horizontalement. Les légendes commencent à 184 px du haut et les écrans vont de 372 à 1 652 px (en 1080 × 1920), pour remplir la hauteur sans coller aux bords.
