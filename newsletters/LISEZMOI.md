# Newsletters Michelin Truckfly

## Le plan d'envoi

| Newsletter | Pour qui | Envoi | Langues |
|---|---|---|---|
| B2B | Partenaires et clients pros : nos nouveautés, l'actu du transport | Milieu du mois, vers le 15 | FR, EN, IT, ES, DE, NL, PL |
| Trucker | Conducteurs qui utilisent l'app | Dernier vendredi du mois | FR, IT |
| Owner | Établissements présents sur Truckfly | Dernier vendredi du mois | FR (pour l'instant) |
| Nouveautés Trucker | Conducteurs qui utilisent l'app | Le lundi qui suit le dernier vendredi, quand il y a une nouveauté | FR, IT |

Le calendrier éditorial complet (octobre 2026 à décembre 2027) est dans `calendrier-editorial.xlsx`. Quand une date tombe mal :

- **B2B** : le 15 tombe un samedi → vendredi 14 ; un dimanche → lundi 16 ; un jour férié → jour ouvré suivant.
- **Trucker et Owner** : jour férié, 24 ou 31 décembre → vendredi précédent (18 décembre 2026, 17 décembre 2027).
- **Nouveautés Trucker** : le lundi qui suit l'envoi Trucker ; s'il est férié → mardi (30 mars 2027, 2 novembre 2027).

## Fichiers

- `template/base.html` : le template commun, à importer dans Brevo (« Coller votre code »).
- `scripts/generer.py` : le contenu de chaque édition, par langue. `python3 newsletters/scripts/generer.py` produit les fichiers HTML.
- `trucker/2026-10/fr.html` et `it.html` : l'édition Trucker d'octobre 2026, prête à coller dans Brevo.
- `template/b2b.html` et `scripts/generer_b2b.py` : le template B2B (Édito, Récap du mois, I. Événements, II. Infos Michelin Truckfly, III. Infos Marché/Légal, IV. La question des Truckers). Dans la partie III, l'UE vient en premier, puis le pays du lecteur.
- `b2b/2026-10/fr.html` : l'édition B2B d'octobre 2026 en français. Les passages surlignés en jaune entre [crochets] sont à compléter. Les autres langues viendront après validation du français.
- `assets/` : les images à charger dans Brevo.
- `calendrier-editorial.xlsx` : dates d'envoi, sujets, statuts et échéances. `python3 newsletters/scripts/calendrier.py` le régénère (attention : cela efface ce qui a été saisi dedans).

## Édition Trucker, octobre 2026

| | FR | IT |
|---|---|---|
| Objet (A) | Depuis dimanche, la nuit te rattrape | Da domenica il buio arriva prima |
| Objet (B, test A/B) | Ce soir, tu dors où ? | Stasera dove dormi? |
| Preheader | Une heure de jour en moins : nos astuces pour garer ton camion sans stress. | Un'ora di luce in meno: i nostri consigli per parcheggiare il camion senza stress. |
| CTA | Trouver mon spot | Trova il mio posto |

Envoi le vendredi 30 octobre, donc après le passage à l'heure d'hiver : l'accroche en parle au passé (« depuis dimanche »).

Les rappels hiver diffèrent par pays : Loi Montagne au 1er novembre en France, obligation hivernale au 15 novembre en Italie.

## Avant l'envoi

1. **Liens** : remplacer `LIEN_APP` dans `scripts/generer.py` et `LIEN_B2B` dans `scripts/generer_b2b.py` par le lien (idéalement un lien profond qui ouvre la carte), puis relancer le script.
2. **Images** : charger `assets/logo-truckfly-blanc.png` dans Brevo, puis remplacer `../../assets` par l'URL Brevo (variable `ASSETS`).
3. **Adresse postale** : compléter `ADRESSE` (obligatoire dans le pied de page).
4. **Prénom** : le mail utilise `{{ contact.PRENOM }}`. Si l'attribut s'appelle `FIRSTNAME` dans votre compte, le changer dans `salutation`.
5. **Suivi** : les liens portent déjà leurs UTM. Dans Brevo, désactiver l'ajout automatique des UTM Google Analytics pour éviter les doublons.
6. **Segment** : envoyer `fr.html` au segment `LANGUE = FR` et `it.html` au segment `LANGUE = IT`.
7. **Test** : envoyer un test sur Gmail (mobile), Outlook et Apple Mail.

## Ce qui change par rapport aux anciens templates (pour plus de clics)

- **Une seule action par mail.** Un seul bouton, et le logo mène au même endroit. Moins de choix, plus de clics.
- **Bouton plein écran sur mobile**, 56 px de haut, facile à toucher avec le pouce. Il reste arrondi dans Outlook (code VML).
- **Texte en vrai texte, pas en image.** Le message se lit même quand les images sont bloquées, et le mail passe mieux les filtres anti-spam.
- **Accroche en haut, un chiffre en grand.** On comprend le sujet en 2 secondes.
- **Phrases courtes et listes numérotées** : faciles à lire sur un téléphone, à une pause.
- **Preheader caché mais rempli** : il complète l'objet dans la boîte de réception au lieu d'afficher « Voir dans le navigateur ».
- **Prénom dans la salutation**, avec une valeur par défaut (« Salut la route, ») si le prénom manque.
- **Mode sombre géré** : les couleurs restent lisibles dans Gmail et Apple Mail en mode sombre.
- **Charte Michelin** : Michelin Blue, jaune uniquement sur fond bleu, casse de phrase, pas d'emoji.
- **À tester dans Brevo** : objet A contre objet B sur 20 % de la base, envoi du gagnant après 4 h. Tester aussi l'heure d'envoi (fin de journée en semaine ou dimanche après-midi, quand les conducteurs sont à l'arrêt).
- **À mesurer** : taux de clics (clics ÷ envoyés) et taux de réactivité (clics ÷ ouvertures). Le taux d'ouverture est faussé par Apple Mail et ne suffit plus pour juger un objet.
