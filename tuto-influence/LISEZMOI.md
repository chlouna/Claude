# Tuto vidéo : le métier de responsable marketing d'influence

Vidéo 16:9, 1920 × 1080, 30 i/s, 78 s, sans son : `mp4/tuto-marketing-influence.mp4`.

- `video.html` contient toute la vidéo : personnages 3D cartoon en SVG ombré (Léa et Max), décors, textes et ligne de temps (Web Animations).
- `rendre.mjs` la capture image par image avec Playwright puis l'assemble avec FFmpeg.
- Rendre la vidéo : `node tuto-influence/rendre.mjs`. Aperçus PNG à certains instants : `node tuto-influence/rendre.mjs 4,15,24` (dans `apercus/`).
- Le déroulé scène par scène est dans `storyboard.md`. Polices Fredoka et Nunito (licence OFL) dans `assets/fonts`.

## Vidéos verticales façon « histoire racontée face caméra » (`true-story/`)

- `hugo.html` : Hugo, 29 ans, explique le métier de responsable marketing d'influence (1080 × 1920, ~79 s, sans son) → `true-story/mp4/hugo-9x16.mp4`.
- `story.html` : variante où Léa raconte comment elle est devenue responsable marketing d'influence (histoire fictive).
- Le texte se modifie dans le tableau `SCRIPT` en haut du script : une ligne = un sous-titre, `*mots*` = surlignés en jaune, `#` = carte titre. Le minutage se recalcule tout seul.
- Rendre : `node tuto-influence/true-story/rendre.mjs hugo` (ou `story`). Aperçus : `node tuto-influence/true-story/rendre.mjs hugo 5,20,40`.
- Les personnages (Léa, Max, Hugo) sont partagés dans `perso.js`.
