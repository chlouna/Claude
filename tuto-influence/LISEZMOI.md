# Tuto vidéo : le métier de responsable marketing d'influence

Vidéo 16:9, 1920 × 1080, 30 i/s, 78 s, sans son : `mp4/tuto-marketing-influence.mp4`.

- `video.html` contient toute la vidéo : personnages 3D cartoon en SVG ombré (Léa et Max), décors, textes et ligne de temps (Web Animations).
- `rendre.mjs` la capture image par image avec Playwright puis l'assemble avec FFmpeg.
- Rendre la vidéo : `node tuto-influence/rendre.mjs`. Aperçus PNG à certains instants : `node tuto-influence/rendre.mjs 4,15,24` (dans `apercus/`).
- Le déroulé scène par scène est dans `storyboard.md`. Polices Fredoka et Nunito (licence OFL) dans `assets/fonts`.
