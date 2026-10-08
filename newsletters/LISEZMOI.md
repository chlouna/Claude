# Newsletters Michelin Truckfly

## Le plan d'envoi

| Newsletter | Pour qui | Rythme | Langues |
|---|---|---|---|
| Trucker | Conducteurs qui utilisent l'app | Mensuelle | FR, IT |
| Nouveautés Trucker | Conducteurs qui utilisent l'app | À chaque nouveauté | FR, IT |
| Owner | Établissements présents sur Truckfly | Mensuelle | à préciser |
| B2B | Partenaires et clients pros : nos nouveautés, l'actu du transport | Mensuelle | FR, EN, IT, ES, DE, NL, PL |

## Fichiers

- `template/base.html` : le template commun, à importer dans Brevo (« Coller votre code »).
- `scripts/generer.py` : le contenu de chaque édition, par langue. `python3 newsletters/scripts/generer.py` produit les fichiers HTML.
- `trucker/2026-10/fr.html` et `it.html` : l'édition Trucker d'octobre 2026, prête à coller dans Brevo.
- `assets/` : les images à charger dans Brevo.

## Édition Trucker, octobre 2026

| | FR | IT |
|---|---|---|
| Objet (A) | Le 25 octobre, la nuit te rattrape | Il 25 ottobre il buio arriva prima |
| Objet (B, test A/B) | Ce soir, tu dors où ? | Stasera dove dormi? |
| Preheader | Une heure de jour en moins : nos astuces pour garer ton camion sans stress. | Un'ora di luce in meno: i nostri consigli per parcheggiare il camion senza stress. |
| CTA | Trouver mon spot | Trova il mio posto |

Les rappels hiver diffèrent par pays : Loi Montagne au 1er novembre en France, obligation hivernale au 15 novembre en Italie.

## Avant l'envoi

1. **Lien de l'app** : remplacer `LIEN_APP` dans `scripts/generer.py` par le lien (idéalement un lien profond qui ouvre la carte), puis relancer le script.
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
