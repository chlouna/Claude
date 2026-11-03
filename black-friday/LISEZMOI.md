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

## Pistes de fond avec le téléphone GPS

- `fonds.html` : story et post 4:5 avec le téléphone GPS (`assets/telephone-gps.png`), sur 5 fonds : noir, blanc, bleu clair, jaune, Michelin Blue.
- `png/planche-fonds.png` : aperçu des 5 pistes ; `png/fonds/` : un PNG par visuel (story 1080 × 1920, post 1080 × 1350).
- Sur fond clair ou jaune, le titre passe en noir, l'étiquette et le bouton en bleu (ou noir sur jaune).
