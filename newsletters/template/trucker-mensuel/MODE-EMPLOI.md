# Template Trucker mensuel « Le Relais » : mode d'emploi

Fichiers : `brevo-fr.html` (à importer dans Brevo), `apercu-fr.html` (aperçu). Les textes entre [crochets] sont à remplacer chaque mois.

## Le déroulé fixe (le même chaque mois, pour que les routiers s'y retrouvent)

| Bloc | Contenu | Règle |
|---|---|---|
| En-tête | Le Relais, N° et mois, ligne GPS | Ne change pas, sauf le N° |
| Édito | Accroche-question + 3 phrases + signature | 8 mots max pour l'accroche ; une vraie personne signe |
| Au programme | 4 liens | Reprendre les titres des blocs |
| 1 · Sujet du mois (fond bleu) | Actu, règle, saison | 1 image, 1 checklist de 2 points, 1 bouton |
| 2 · Le tuto du mois | Une fonction de l'app | 2 × 3 étapes, 1 capture ou GIF, 1 bouton |
| 3 · La communauté (fond bleu) | Points de contribution | Bloc fixe, seul le titre peut changer |
| 4 · Bravo ! | Classement du mois précédent | 1 visuel, bouton « C'est mon tour ! » |
| Sondage (optionnel) | 1 question, 3 réponses | Chaque réponse est un lien ; résultats le mois suivant |
| Le mot de la route | Merci + rendez-vous | 3 phrases |

## Règles qui font cliquer
- **Objet** : 50 caractères max, une question ou un bénéfice concret, le mois ou la date si c'est urgent. Tester 2 objets en A/B sur 20 % de la base.
- **Preheader** : complète l'objet, ne le répète pas.
- **Boutons** : verbe à la 1re personne + bénéfice (« Je prépare mon trajet »). Un seul bouton par bloc.
- **Images** : toujours cliquables, avec un texte alternatif, moins de 150 Ko.
- **Longueur** : moins de 2 minutes de lecture. Si un sujet est long, le raccourcir et renvoyer vers une page.

## Charte (Michelin Digital Chapter 2)
- Dominantes : Michelin Blue #061866, Glow White, Off White #F5F3F1.
- Highlight Yellow #FFFF1A : uniquement sur fond bleu, pour les boutons et les « +1 ».
- Blue hues (≤ 15 %) : Ice Blue, Indigo Blue, Sky Blue, Space Blue (pied de page).
- Accents (≤ 5 %) : une pastille Tangerine et les coches Teal, pas plus.
- Titres en Bib Bold, casse de phrase, jamais en capitales. Texte en Noto Sans.

## Chaque mois
1. Copier `MODELE` dans `scripts/template_trucker.py`, remplacer les crochets (ou remplir directement dans Brevo).
2. Traduire en IT (et ES) avec le skill de traduction Brevo, blocs conditionnés par LANG.
3. Remplacer les liens LIEN-…, le logo (URL-LOGO-BLANC) et la police (URL-BIB-BOLD).
4. Vérifier avec le skill brevo-check avant l'envoi.
