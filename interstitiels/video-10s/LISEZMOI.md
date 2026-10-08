# Interstitielle vidéo 10 s : Profil Trucker et Social Core

Une vidéo par langue, 1080 × 2338, 30 i/s, 10 s, sans son : `mp4/interstitiel-10s-<langue>.mp4`.

- `generer.py` écrit une page HTML par langue (`fr.html`, `en.html`…), `rendre.mjs` en tire les MP4.
- Régénérer : `python3 interstitiels/video-10s/generer.py`, puis `node interstitiels/video-10s/rendre.mjs` (ou `rendre.mjs fr,de` pour certaines langues).

## Déroulé

| Temps | Ce qui se passe |
|---|---|
| 0–2 s | Logo Michelin Truckfly blanc, puis le titre « Michelin Truckfly devient plus social ! » |
| 2–4 s | Le Profil Trucker de Charlie apparaît : la photo s'ajoute (📸), puis la bio s'écrit (✍️) |
| 4–6 s | Le camion arrive sur le profil (🚛) : photo carrée, surnom, hauteur, largeur et longueur |
| 6–8 s | Le profil se réduit et les cartes des amis arrivent (👥 📍) : invitation de Louna, visite de Nicolas J. à AS 24, arrêt de David au Relais des Cigales |
| 8–10 s | Écran final : « Ne roule plus seul ! », sous-titre, bouton jaune « Créer mon profil » qui pulse, logo en bas |

## Textes à faire valider par les équipes locales

Traductions faites pour cette maquette : à relire par un locuteur natif de chaque pays, notamment le nom de la fonctionnalité (« Profil Trucker »), qui doit correspondre à celui de l'app traduite.

| | Français | Anglais | Allemand | Néerlandais | Polonais | Italien | Espagnol |
|---|---|---|---|---|---|---|---|
| Titre (0–2 s) | Michelin Truckfly devient plus social ! | Michelin Truckfly is getting more social! | Michelin Truckfly wird sozialer! | Michelin Truckfly wordt socialer! | Michelin Truckfly staje się bardziej społecznościowy! | Michelin Truckfly diventa più social! | ¡Michelin Truckfly se vuelve más social! |
| Légende photo | Ajoute ta photo | Add your photo | Füge dein Foto hinzu | Voeg je foto toe | Dodaj swoje zdjęcie | Aggiungi la tua foto | Añade tu foto |
| Légende bio | Personnalise ta bio | Personalise your bio | Personalisiere deine Bio | Personaliseer je bio | Spersonalizuj swój opis | Personalizza la tua bio | Personaliza tu bio |
| Légende camion | Ajoute ton camion | Add your truck | Füge deinen Lkw hinzu | Voeg je truck toe | Dodaj swoją ciężarówkę | Aggiungi il tuo camion | Añade tu camión |
| Légende amis | Retrouve tes amis | Find your friends | Finde deine Freunde | Vind je vrienden | Znajdź znajomych | Ritrova i tuoi amici | Encuentra a tus amigos |
| Légende activité | Découvre leur activité au quotidien | See what they’re up to every day | Entdecke täglich, was sie machen | Ontdek elke dag wat ze doen | Odkrywaj ich codzienną aktywność | Scopri la loro attività ogni giorno | Descubre su actividad cada día |
| Titre final | Ne roule plus seul ! | Never drive alone again! | Fahr nie mehr allein! | Rij nooit meer alleen! | Nie jeźdź już sam! | Non viaggiare più da solo! | ¡No vuelvas a conducir solo! |
| Sous-titre final | Crée ton Profil Trucker sur Michelin Truckfly | Create your Trucker Profile on Michelin Truckfly | Erstelle dein Trucker-Profil auf Michelin Truckfly | Maak je Truckerprofiel aan op Michelin Truckfly | Utwórz swój Profil Truckera w Michelin Truckfly | Crea il tuo Profilo Trucker su Michelin Truckfly | Crea tu Perfil Trucker en Michelin Truckfly |
| Bouton | Créer mon profil | Create my profile | Mein Profil erstellen | Mijn profiel aanmaken | Utwórz mój profil | Crea il mio profilo | Crear mi perfil |
| Bio de Charlie | Conducteur routier 🚛 \| Toujours sur la route \| À la recherche des meilleurs spots ! | Truck driver 🚛 \| Always on the road \| Looking for the best spots! | Lkw-Fahrer 🚛 \| Immer auf der Straße \| Auf der Suche nach den besten Spots! | Vrachtwagenchauffeur 🚛 \| Altijd onderweg \| Op zoek naar de beste plekken! | Kierowca ciężarówki 🚛 \| Zawsze w trasie \| W poszukiwaniu najlepszych miejsc! | Camionista 🚛 \| Sempre in viaggio \| Alla ricerca dei posti migliori! | Camionero 🚛 \| Siempre en la carretera \| ¡Buscando los mejores sitios! |
| Surnom du camion | Le Bolide | The Rocket | Der Blitz | De Bliksem | Błyskawica | Il Fulmine | El Rayo |
| Invitation | Louna vous a envoyé une invitation | Louna sent you an invitation | Louna hat dir eine Einladung geschickt | Louna heeft je een uitnodiging gestuurd | Louna wysłała ci zaproszenie | Louna ti ha inviato un invito | Louna te ha enviado una invitación |
| Visite | Nicolas J. a visité : | Nicolas J. visited: | Nicolas J. hat besucht: | Nicolas J. heeft bezocht: | Nicolas J. odwiedził: | Nicolas J. ha visitato: | Nicolas J. ha visitado: |
| Arrêt | David s’est arrêté ici : | David stopped here: | David hat hier angehalten: | David is hier gestopt: | David zatrzymał się tutaj: | David si è fermato qui: | David ha parado aquí: |

## Choix

- **Casse** : « Michelin Truckfly » et « Ne roule plus seul ! » en casse de phrase, comme demandé et selon la charte. Le logo (image officielle) garde sa typographie.
- **Décimales** : virgule partout sauf en anglais (4.00 m).
- **Surnom du camion** traduit dans chaque langue pour rester parlant. Les noms (Charlie G., Louna, Nicolas J., David) et les lieux (AS 24, Le Relais des Cigales) restent identiques.
- **Drapeau** : Charlie G. garde le drapeau français dans toutes les versions. Il peut être adapté par pays.
- **Notifications** : en français, « vous » comme dans l'app ; tutoiement ailleurs dans la vidéo.
