# Storyboard : Truckfly pour les établissements (64,6 s)

Message : les propriétaires et gestionnaires d'établissements peuvent créer leur établissement sur Michelin Truckfly, mettre à jour leurs informations et suivre ce que la communauté publie sur leur fiche.
Référence : « Truckfly : Comment promouvoir ou faire connaître votre établissement » (ancienne charte, rouge, 60 s). Même déroulé, refait à la nouvelle charte (`charte.md`).
Diffusion : 16:9 (1920 × 1080) et 9:16 (1080 × 1920), recomposée à part.
Source : `scripts/generer.py` produit `index.html` et `compositions/vertical.html`. Rendus dans `renders/`.
Vouvoiement : la vidéo s'adresse à des professionnels (l'original vouvoie).

## Style

- Fonds Michelin Blue `#061866` et Off White `#F5F3F1`, en alternance. Accent Highlight Yellow `#FFFF1A` uniquement sur fond bleu (soulignés, curseur, flèches, tap).
- Titres en Bib Bold / Light, en casse de phrase. Interface en Noto Sans (charte).
- Intro avec les vraies captures de l'app (écran d'ouverture avec le Bibendum, carte). La carte contient la photo de profil d'un utilisateur et des logos de marques partenaires : capture fournie par l'utilisateur.
- Illustrations à plat (façade, vignettes) en bleu, blanc, Space Blue `#000E38` et deux teintes claires de Michelin Blue.
- Un seul style d'animation : les éléments montent avec un léger fondu (0,4 s), les mots du titre arrivent un par un. Des taps et des flèches jaunes guident le regard dans l'interface.
- Logo blanc sur bleu, logo couleur sur Off White. Pas de musique ni de voix off (à proposer).

## Déroulé

| # | Minutage | Texte à l'écran | Animation |
|---|---|---|---|
| 1 | 0 → 3,5 s | **Connaissez-vous** [logo Michelin Truckfly] **?** | Fond bleu. Les mots arrivent un par un, puis le logo blanc et le point d'interrogation, avec un soulignement jaune. |
| 2 | 3,5 → 5,8 s | Écran d'ouverture de l'app : logo et Bibendum | Capture fournie (`assets/ecrans/app-ouverture.png`). Le téléphone monte, puis passe en arrière-plan, atténué. |
| 3 | 5,8 → 11,3 s | **Saviez-vous que Michelin Truckfly existe aussi / pour les propriétaires d'établissements ?** | Interstitiel lisible, par-dessus le téléphone atténué. Mots un par un. |
| 4 | 11,3 → 18 s | Repères **Restaurant** · **Parking** · **Station-service** · **Station de lavage** · **Garage** | Le téléphone revient au premier plan, l'écran d'ouverture laisse place à la carte de l'app (`assets/ecrans/app-carte.png`). La carte s'éclaircit, puis les cinq repères tombent l'un après l'autre avec leur étiquette. En 16:9, la liste des types se construit à gauche en même temps. |
| 5 | 18,3 → 24,3 s | **La communauté en chiffres** · **2,3 M** téléchargements · **44** pays européens · **21** langues disponibles · **702 000** utilisateurs · **135 000** établissements référencés | Fond bleu, les chiffres défilent jusqu'à leur valeur. |
| 6 | 24,3 → 29,6 s | **Vous avez un établissement sur Michelin Truckfly ?** → **Mettez à jour vos informations !** | Fond bleu, puis « www.truckfly.com » se tape dans une barre d'adresse. |
| 7 | 29,6 → 35,8 s | **Pas encore présent sur Michelin Truckfly ?** → **Créez votre compte et ajoutez votre établissement !** | Fond Off White, même barre d'adresse, clic sur la loupe. |
| 8a | 35,8 → 39,8 s | Étiquette **Nom et coordonnées** | Espace pro recréé (menu : Mon établissement, Mes services et photos, Mes horaires d'ouverture, Mes commentaires). Les champs Nom, Adresse, Email et Téléphone se remplissent. Le repère de la carte tombe, tap sur « Enregistrer ». |
| 8b | 39,8 → 43,8 s | Étiquette **Services proposés** | Onglet « Mes services et photos ». Cases cochées (Restaurant routier, Douches, Parking poids lourds, Wifi). Flèche jaune, tap sur « Enregistrer ». |
| 8c | 43,8 → 47,3 s | Étiquette **Photos** | Zone « Ma photo » : l'illustration de la façade y glisse et se dépose. Tap sur « Enregistrer ». |
| 8d | 47,3 → 51,3 s | Étiquette **Horaires** | Onglet « Mes horaires d'ouverture » : lundi, mardi et mercredi se remplissent (« Journée continue » cochée). Tap sur « Dupliquer ». |
| 9 | 51,3 → 59 s | **Retrouvez les commentaires et les photos de la communauté** | Onglet « Mes commentaires » : trois avis (Denis, Pascal, Emilie, comme dans l'original). Tap sur « Répondre », la réponse « Merci beaucoup pour ce commentaire Denis ! À très vite ! » se tape. Puis une rangée de photos de la communauté (illustrations) défile. |
| 10 | 59 → 64,6 s | [logo Michelin Truckfly] **Pour promouvoir mon établissement, / connectez-vous sur le site internet.** · bouton **www.truckfly.com** | Fond bleu, logo blanc. Le bouton blanc pulse doucement. Dernière image fixe pendant 2 s. |

## Recréé pour la vidéo, à valider

- L'espace pro (scènes 8 et 9) est **recréé à la nouvelle charte** d'après l'original. La page www.truckfly.com/owner/signup n'était pas accessible depuis l'environnement de travail : à remplacer par des captures de l'interface actuelle si besoin.
- Les noms, avis et horaires de démonstration (Resto Routier, Denis, Pascal, Emilie…) reprennent ceux de l'original.
- Chiffres : les cinq de l'encart « La communauté en chiffres » fourni par l'utilisateur.
- Adresse affichée : www.truckfly.com, comme dans l'original.

## Versions traduites (16:9 seulement)

Anglais, allemand, espagnol, italien, néerlandais et polonais : `LANGUE=xx python3 scripts/generer.py` écrit `compositions/paysage-xx.html`, rendue dans `renders/truckfly-etablissements-xx-16x9.mp4`. Les textes sont dans `scripts/traductions.py`.

- Registre : vouvoiement en allemand (Sie), espagnol (usted), italien (Lei) et néerlandais (u) ; « you » en anglais ; tutoiement en polonais, l'usage courant des applications.
- Nombres au format de chaque langue (2.3M / 702,000 en anglais, 2,3 Mio. / 702.000 en allemand…).
- Les captures de l'app (écran d'ouverture, carte) restent en français : à remplacer par les captures de chaque langue si disponibles.
- Traductions à faire relire par une personne de langue maternelle avant diffusion.
