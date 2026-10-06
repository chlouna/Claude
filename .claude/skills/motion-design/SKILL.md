---
name: motion-design
description: >-
  Crée une vidéo animée à la marque de l'utilisateur avec HyperFrames : charte, storyboard validé, contrôle image par image, versions 16:9 et 9:16. Se déclenche sur « vidéo animée », « motion design ».
---

# Créer une vidéo animée à la marque

Skill publié par Loris Gautier, lorisgautier.fr. Il s'appuie sur HyperFrames (HeyGen, licence
Apache 2.0, gratuit) : tu écris la vidéo en HTML et en animations, HyperFrames la rend en MP4.

## Le principe, à respecter

Tu ne vois pas la vidéo pendant que tu l'écris. Tu la vois seulement par des images de contrôle.
La qualité vient donc de trois choses : une charte précise, un storyboard validé avant d'écrire le
moindre code, et un contrôle image par image avant et après le rendu. Une vidéo qui n'est pas passée
par le contrôle ne se livre pas.

Ce skill marche dans Claude Code ou dans l'onglet Code de Claude Desktop, en environnement local.

## 0. Vérifier et préparer le projet

```
npx hyperframes doctor
```

Il faut Node.js 22 ou plus, FFmpeg et Chrome. Si FFmpeg est marqué en échec alors qu'il est
installé, il est souvent cassé par une mise à jour de bibliothèque : sur Mac, `brew upgrade ffmpeg`.
Montre toute commande d'installation à l'utilisateur avant de la lancer.

Pour un nouveau projet :

```
npx hyperframes init NOM-DU-PROJET --non-interactive --example blank
```

Préviens l'utilisateur : cette commande installe les skills HyperFrames dans son dossier de skills,
et dans ceux des autres agents présents sur la machine (Cursor, Codex, Gemini). Elle envoie aussi une
télémétrie anonyme ; `HYPERFRAMES_NO_TELEMETRY=1` la coupe. Lis ensuite le `CLAUDE.md` du projet et
utilise le skill `/hyperframes`, qui oriente vers le bon workflow : `/motion-graphics` pour une
pièce de moins de dix secondes, `/general-video` au-delà.

## 1. La charte

Cherche une `charte.md` dans le projet. Sinon, remplis-la avec l'utilisateur à partir de
`references/charte-modele.md` : couleurs avec leurs codes, polices, logo, ton, mots interdits.
Si l'utilisateur a un site, propose d'en relever les couleurs et les polices.

Les polices doivent être des fichiers du projet, dans `assets/fonts`, chargées par `@font-face`.
Une police qui ne charge pas tombe en silence sur une police système : c'est le défaut le plus
courant, et il se voit seulement au contrôle.

## 2. Le format et le storyboard

Propose le format qui colle à la demande, parmi ceux de `references/formats.md` : annonce,
chiffre clé, trois points, citation, générique de logo. Écris ensuite `storyboard.md` : une ligne
par scène, avec le minutage, le texte exact à l'écran, et ce qui bouge.

Règles du storyboard :

- **Une idée par scène.** Si une scène dit deux choses, coupe-la en deux.
- **Le temps de lecture.** Un texte reste à l'écran au moins 1,5 seconde, plus 0,3 seconde par mot.
- **Les vrais chiffres.** Tu n'inventes jamais un chiffre, un client, un logo ni un témoignage :
  tout vient de l'utilisateur ou de son site.
- **La fin.** La dernière scène porte la marque et l'action attendue, et elle tient au moins
  2 secondes.

Montre le storyboard et attends la validation, sauf si l'utilisateur t'a dit de ne pas l'attendre.

## 3. Construire

Suis le workflow HyperFrames choisi à l'étape 0. Tiens-toi à la charte : ses couleurs, ses polices,
son ton. Un seul style d'animation par vidéo, des transitions courtes, aucun effet que le brief ne
demande pas (confettis, néons, glitch). Le mouvement sert la lecture, il ne la gêne jamais.

## 4. Contrôler avant le rendu

```
npx hyperframes check
npx hyperframes snapshot --at T1,T2,T3
```

Prends une image au milieu de chaque scène, plus la fin. Ouvre chaque image et passe la liste de
`references/controle.md` : textes qui débordent ou se chevauchent, police de secours à la place de
celle de la marque, contraste, orthographe, zones de sécurité du vertical. Corrige, puis recommence
le contrôle jusqu'à ce que la liste soit entièrement propre.

Si une couleur ou une police de la charte pose un problème (contraste, lisibilité), ne la remplace
pas de toi-même : c'est une décision de marque. Propose une alternative à l'utilisateur et attends
sa réponse, ou, s'il t'a dit de ne pas l'attendre, signale l'écart dans le bilan de livraison.

## 5. Rendre les deux formats

La version verticale (1080 × 1920) se recompose : ce n'est jamais un simple recadrage de la version
16:9. Fais-en une composition à part, avec ces règles :

- **Les tailles.** Titres d'au moins 80 pixels, texte courant d'au moins 48 pixels. Sur un téléphone,
  ce qui paraît grand à l'écran de l'ordinateur paraît minuscule.
- **La place.** Le contenu occupe toute la hauteur utile, entre 250 et 1 670 pixels, centré
  verticalement. Un bloc de texte collé en haut avec un grand vide en dessous est un défaut.
- **Une chose à la fois.** Si la version 16:9 affiche plusieurs éléments côte à côte, la verticale
  les montre l'un après l'autre, en grand, plutôt que tous empilés en petit.

```
npx hyperframes render -o renders/NOM-16x9.mp4 --quality delivery
npx hyperframes render -c compositions/vertical.html -o renders/NOM-9x16.mp4 --quality delivery
```

## 6. Contrôler le rendu final

```
node "${CLAUDE_SKILL_DIR}/scripts/planche.mjs" renders/NOM-16x9.mp4
node "${CLAUDE_SKILL_DIR}/scripts/planche.mjs" renders/NOM-9x16.mp4
```

Le script assemble des images réparties sur toute la vidéo en une seule planche. Ouvre chacune des
deux planches et passe-la sur la liste de `references/controle.md`, comme les images de l'étape 4.
La planche verticale est la seule vue de contrôle de la version 9:16 : regarde-la avec la même
exigence. Si une case n'est pas cochée, corrige et rends à nouveau.

## 7. Livrer

Donne les fichiers, leur durée mesurée par le script, et deux ou trois retouches possibles. Musique,
voix off et images de banque se proposent, elles ne s'ajoutent pas d'office : elles posent une
question de droits que l'utilisateur doit trancher.
