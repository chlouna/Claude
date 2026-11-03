# Black Friday 2026 · GPS Premium -50 %

Offre annuelle à 37,99 € au lieu de 74,99 €, du 27/11 au 30/11/2026.

- `index.html` : la planche (tous les formats et les 3 phases). `index.html?solo=story` affiche un seul format.
- `png/` : un PNG par format à la taille d'export, plus `planche.png`.
- Régénérer : `node black-friday/rendre.mjs`.

| Phase | Dates | Message | CTA |
|---|---|---|---|
| 1 · Teasing | 20 → 26/11 | « -??% », rendez-vous le 27/11 | Activer les notifications |
| 2 · Lancement | 27/11 → 02/12 | -50 %, 37,99 €/an au lieu de 74,99 € | J'en profite |
| 3 · Dernière chance | 29 → 30/11 | Derniers jours, plus que 48 h | J'en profite |

Les textes de chaque phase sont dans l'objet `PHASES` de `index.html`.

Charte : pas de gros texte en jaune. Le jaune est réservé aux petits textes (pastilles), aux boutons et au fond de l'étiquette (texte bleu dessus).

## Pistes de fond avec le téléphone GPS (ancienne charte)

Exception Black Friday : ancienne charte, comme sur le flyer « Le poids lourd des GPS ».

- `fonds.html` : story et post 4:5 avec le téléphone GPS (`assets/telephone-gps.png`), sur 3 fonds : noir, blanc, Michelin Blue. Fond jaune interdit.
- Titres en capitales grasses italiques, dans un cartouche arrondi, avec une ligne fine (sans rond jaune). Texte en italique.
- La date est mise en avant dans un bandeau « DU 27/11 AU 30/11 » à cheval sous le cartouche (jaune sur fond noir et bleu, bleu sur fond blanc).
- Polices : la police MICHELIN n'est pas dans le repo. Elle est remplacée par Archivo Expanded Black Italic (titres) et Open Sans Italic (texte), sous licence libre OFL, dans `assets/fonts/`. Pour passer à la vraie police, déposer le fichier dans `assets/fonts/` et changer l'URL du `@font-face "Titre"` en haut de `fonds.html`.
- `png/planche-fonds.png` : aperçu ; `png/fonds/` : un PNG par visuel (story 1080 × 1920, post 1080 × 1350).

## Plaquette fond noir (version retenue)

- `noir.html` : la plaquette complète. `noir.html?solo=<id>` affiche un seul visuel.
- `png/noir/plaquette-noir.png` : aperçu ; `png/noir/` : un PNG par visuel à la taille d'export.

| Visuel | Quand | Taille |
|---|---|---|
| `story-teasing` | 20/11 · « Ça vous dirait une promo sur le GPS ? » | 1080 × 1920 |
| `story-j1` | 26/11 · Plus qu'un jour (teasing) | 1080 × 1920 |
| `story-jourj` | 27/11 · C'est parti ! | 1080 × 1920 |
| `story-fin3` | 28/11 · Plus que 3 jours | 1080 × 1920 |
| `story-fin1` | 29/11 · Plus qu'un jour | 1080 × 1920 |
| `story-finh` | 30/11 · Plus que quelques heures (fin à minuit) | 1080 × 1920 |
| `post-teasing` | 20 → 26/11 | 1080 × 1350 |
| `post-jourj` | 27/11 | 1080 × 1350 |
| `interstitiel-teasing` | 20 → 26/11 (bouton « M'avertir le 27/11 ») | 1170 × 2532 |
| `interstitiel-offre` | 27/11 → 30/11 | 1170 × 2532 |
| `banniere-web` | 27/11 → 30/11 | 2400 × 800 |
| `banniere-728x90` | 27/11 → 30/11 | 1456 × 180 |

Les textes de chaque phase (teasing, offre, jour J) sont dans l'objet `PHASES` de `noir.html`.

Teasing : pas de prix ni de « ?? ». Accroche « Ça vous dirait une promo sur le GPS ? ». Compte à rebours sur la fin de l'offre jusqu'au 30/11, téléphone dans la pénombre sous un halo, date en bandeau « LE 27/11 ». Bannière in-app retirée.
