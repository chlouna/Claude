# Black Friday 2026 · GPS Premium -50 %

Offre annuelle à 37,99 € au lieu de 74,99 €, du 27/11 au 04/12/2026.

- `index.html` : la planche (tous les formats et les 3 phases). `index.html?solo=story` affiche un seul format.
- `png/` : un PNG par format à la taille d'export, plus `planche.png`.
- Régénérer : `node black-friday/rendre.mjs`.

| Phase | Dates | Message | CTA |
|---|---|---|---|
| 1 · Teasing | 20 → 26/11 | « -??% », rendez-vous le 27/11 | Activer les notifications |
| 2 · Lancement | 27/11 → 02/12 | -50 %, 37,99 €/an au lieu de 74,99 € | J'en profite |
| 3 · Dernière chance | 03 → 04/12 | Derniers jours, plus que 48 h | J'en profite |

Les textes de chaque phase sont dans l'objet `PHASES` de `index.html`.

Charte : pas de gros texte en jaune. Le jaune est réservé aux petits textes (pastilles), aux boutons et au fond de l'étiquette (texte bleu dessus).

## Pistes de fond avec le téléphone GPS (ancienne charte)

Exception Black Friday : ancienne charte, comme sur le flyer « Le poids lourd des GPS ».

- `fonds.html` : story et post 4:5 avec le téléphone GPS (`assets/telephone-gps.png`), sur 3 fonds : noir, blanc, Michelin Blue. Fond jaune interdit.
- Titres en capitales grasses italiques, dans un cartouche arrondi, avec un rond jaune et une ligne fine. Texte en italique.
- La date est mise en avant dans un bandeau « DU 27/11 AU 04/12 » à cheval sous le cartouche (jaune sur fond noir et bleu, bleu sur fond blanc).
- Polices : la police MICHELIN n'est pas dans le repo. Elle est remplacée par Archivo Expanded Black Italic (titres) et Open Sans Italic (texte), sous licence libre OFL, dans `assets/fonts/`. Pour passer à la vraie police, déposer le fichier dans `assets/fonts/` et changer l'URL du `@font-face "Titre"` en haut de `fonds.html`.
- `png/planche-fonds.png` : aperçu ; `png/fonds/` : un PNG par visuel (story 1080 × 1920, post 1080 × 1350).
