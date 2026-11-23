# Tuto vidéo : le métier de responsable marketing d'influence

Vidéo 16:9, 1920 × 1080, 30 i/s, 78 s, sans son : `mp4/tuto-marketing-influence.mp4`.

- `video.html` contient toute la vidéo : personnages 3D cartoon en SVG ombré (Léa et Max), décors, textes et ligne de temps (Web Animations).
- `rendre.mjs` la capture image par image avec Playwright puis l'assemble avec FFmpeg.
- Rendre la vidéo : `node tuto-influence/rendre.mjs`. Aperçus PNG à certains instants : `node tuto-influence/rendre.mjs 4,15,24` (dans `apercus/`).
- Le déroulé scène par scène est dans `storyboard.md`. Polices Fredoka et Nunito (licence OFL) dans `assets/fonts`.

## Vidéos verticales façon « histoire racontée face caméra » (`true-story/`)

- `hugo.html` : Hugo, 29 ans, explique le métier de responsable marketing d'influence (1080 × 1920, 62 s, voix off + musique) → `true-story/mp4/hugo-9x16.mp4`.
- `story.html` : variante où Léa raconte comment elle est devenue responsable marketing d'influence (histoire fictive).
- Le texte se modifie dans le tableau `SCRIPT` en haut du script : une ligne = un sous-titre, `*mots*` = surlignés en jaune, `#` = carte titre. Le minutage se recalcule tout seul.
- Rendre : `node tuto-influence/true-story/rendre.mjs hugo` (ou `story`). Aperçus : `node tuto-influence/true-story/rendre.mjs hugo 5,20,40`.
- Les personnages (Léa, Max, Hugo) sont partagés dans `perso.js`.

### Voix off et musique (Hugo)

- Voix : synthèse locale Kokoro (40 % voix française « siwis » + 60 % voix masculine « nicola »), une piste par sous-titre dans `audio/voix-hugo/`. Les sous-titres et la bouche de Hugo se calent sur la durée de chaque phrase (`hugo-voix.js`).
- Musique : composée et synthétisée par `audio/mixer.py` (pop douce, 104 bpm), donc sans droits tiers ; elle baisse automatiquement sous la voix. Mixage final à -14 LUFS.
- Chaîne complète après un changement de texte :
  1. `python audio/voix.py <dossier des modèles Kokoro> hugo` (python avec `kokoro-onnx` ; modèles `kokoro-v1.0.int8.onnx` renommé `kokoro.onnx` et `voices-v1.0.bin` renommé `voices.bin`, sur les releases GitHub de kokoro-onnx)
  2. `node rendre.mjs hugo` (vidéo muette + minutage)
  3. `python audio/mixer.py hugo` (musique, mixage, MP4 final)
- La prononciation de certains mots se corrige dans le dictionnaire `DIRE` de `audio/voix.py`.
