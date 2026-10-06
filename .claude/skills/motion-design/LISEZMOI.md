# Le skill Motion design pour Claude

Ce que vous avez entre les mains : la méthode que Claude suit pour créer une vidéo animée à votre marque. Il part de votre charte (couleurs, polices, logo), vous propose un storyboard scène par scène, construit la vidéo, la contrôle image par image, puis la rend en version horizontale et en version verticale pour LinkedIn, les Reels et les Shorts.

**Rien n'est produit avant que vous ayez validé le storyboard**, et aucun chiffre, client ou témoignage n'est inventé : tout vient de vous.

## Ce qu'il faut avant

- Un abonnement Claude Pro ou supérieur, et l'application Claude Desktop, onglet **Code**, en environnement **Local**. Ce skill ne marche pas dans le chat de claude.ai.
- Node.js 22 ou plus (nodejs.org), FFmpeg et Google Chrome.

Sur Mac :

```
brew install node ffmpeg
```

Sur Windows :

```
winget install OpenJS.NodeJS Gyan.FFmpeg
```

Le moteur de rendu, HyperFrames (HeyGen), est libre et gratuit, sans limite de taille d'entreprise. Il s'installe tout seul au premier projet. Bon à savoir : son installation ajoute ses propres skills dans votre dossier de skills, et dans ceux de Cursor, Codex ou Gemini s'ils sont sur votre machine. Il envoie aussi une télémétrie anonyme, que vous coupez en ajoutant `HYPERFRAMES_NO_TELEMETRY=1` à votre environnement.

## Installation, deux minutes

1. Gardez le fichier `skill-motion-design.zip`.
2. Dans Claude Desktop, onglet Code, écrivez : **installe le skill contenu dans ~/Downloads/skill-motion-design.zip dans ~/.claude/skills**. Le dossier `motion-design` doit finir dans `~/.claude/skills/`.
3. Ouvrez une nouvelle session dans un dossier vide et écrivez : **fais-moi une vidéo animée de 15 secondes pour annoncer [votre offre]**.

## Comment l'utiliser

- Préparez votre charte une fois pour toutes : le modèle est dans `references/charte-modele.md`. Mettez vos polices (fichiers .woff2 ou .ttf) et votre logo dans le dossier du projet.
- Choisissez un des cinq formats : annonce, chiffre clé, trois points, citation, générique de logo.
- Relisez le storyboard : c'est là que se joue la qualité, bien plus que dans les animations.
- Regardez la planche de contrôle que Claude produit à la fin : une image qui résume toute la vidéo.

## Ce que ce skill ne fait pas

Il ne génère pas d'images ni de vidéos réalistes : il anime du texte, des formes, vos visuels et vos chiffres. Il n'ajoute ni musique ni voix off sans votre accord, à cause des droits. Si vous voulez que Claude produise vos vidéos à partir de vos contenus chaque semaine, branché sur vos outils, écrivez-moi sur lorisgautier.fr, l'audit est offert.

Loris Gautier · lorisgautier.fr
