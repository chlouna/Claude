# Custom Product Pages Michelin Truckfly

Une CPP (App Store) / fiche Play Store personnalisée (Google Play) par business model, avec 5 captures chacune.

1. App gratuite et communauté
2. Établissements (restaurants, parkings, stations, lavages)
3. GPS Premium

- `png/<cpp>/app-store/` : 5 PNG en 1284 × 2778
- `png/<cpp>/google-play/` : 5 PNG en 1080 × 1920 (9:16)
- `png/<cpp>/planche-*.png` : aperçu de la série
- `index.html` : toutes les captures en HTML
- Régénérer : `python3 scripts/generer.py`, puis `node scripts/capturer.mjs`

Ton : vouvoiement partout.
Écrans de l'app recréés (pas de captures réelles). Les noms, avis et chiffres de statistiques sont des exemples, à remplacer avant publication s'ils doivent être réels.

Limites des stores : texte promotionnel App Store 170 caractères ; Google Play : nom 30, description courte 80, description complète 4 000.

---

## 1. App gratuite et communauté (publicité)

- **Cible** : tous les routiers, acquisition large (réseaux sociaux, influence, salons).
- **Lien profond conseillé** : carte des lieux.
- **Mots-clés Google Play** : parking poids lourd, aire routier, relais routier, douche routier

| # | Titre | Sous-titre |
|---|---|---|
| 1 | Trouvez où vous arrêter | Parkings, restos et douches poids lourds partout en Europe |
| 2 | Des avis laissés par des routiers | Pour choisir votre arrêt en confiance |
| 3 | Prévenez les autres en un geste | Accidents, contrôles, dangers en temps réel |
| 4 | Votre communauté de routiers | Suivez vos amis et leurs bons plans |
| 5 | Gratuit, dans votre langue | Plus de 700 000 conducteurs dans 44 pays |

**Texte promotionnel App Store** :
Parkings, restos et douches poids lourds, avis de routiers et alertes en temps réel. Gratuit, dans 44 pays et dans votre langue.

**Description courte Google Play** :
Parkings, restos, douches poids lourds et alertes de routiers. Gratuit.

**Description complète Google Play** :
Rejoignez plus de 700 000 conducteurs routiers sur Michelin Truckfly.
• Trouvez les parkings, restos, douches, stations et lavages poids lourds dans 44 pays
• Lisez les avis des autres routiers avant de vous arrêter
• Signalez un accident, un contrôle ou un danger en un geste
• Créez votre Profil Trucker, ajoutez vos amis et suivez leurs bons plans
• L'app dans votre langue
Gratuit.

---

## 2. Établissements (restaurants, parkings, stations, lavages)

- **Cible** : gérants de relais routiers, restaurants, parkings, stations, lavages. Campagnes B2B (LinkedIn, newsletter owners, prospection).
- **Lien profond conseillé** : revendiquer / gérer ma fiche établissement.
- **Mots-clés Google Play** : relais routier visibilité, fiche établissement routiers

| # | Titre | Sous-titre |
|---|---|---|
| 1 | Faites venir les poids lourds chez vous | Votre établissement visible par 700 000 conducteurs |
| 2 | Votre fiche à jour en 2 minutes | Horaires, places, services, photos |
| 3 | Répondez aux avis | Montrez aux routiers que vous les écoutez |
| 4 | Suivez vos visites | Vues, itinéraires lancés, appels |
| 5 | Mettez en avant vos offres | Sur la carte, au moment où ils cherchent un arrêt |

**Texte promotionnel App Store** :
Rendez votre établissement visible par plus de 700 000 routiers : fiche à jour, réponses aux avis, statistiques et offres mises en avant.

**Description courte Google Play** :
Gérez la fiche de votre établissement et attirez les routiers.

**Description complète Google Play** :
Restaurant, parking, station ou lavage : Michelin Truckfly met votre établissement sous les yeux de plus de 700 000 conducteurs routiers.
• Mettez à jour vos horaires, places poids lourds, services et photos
• Répondez aux avis des conducteurs
• Suivez les vues de votre fiche, les itinéraires lancés et les appels
• Mettez en avant vos offres sur la carte

---

## 3. GPS Premium (abonnement)

- **Cible** : routiers qui cherchent un GPS poids lourd. Campagnes Apple Search Ads / Google App Campaigns sur « GPS camion », « GPS poids lourd ».
- **Lien profond conseillé** : écran d'abonnement Premium.
- **Mots-clés Google Play** : gps camion, gps poids lourd, navigation camion, itinéraire poids lourd

| # | Titre | Sous-titre |
|---|---|---|
| 1 | Le GPS pensé pour votre camion | Navigation poids lourd dans 44 pays |
| 2 | Un itinéraire selon votre gabarit | Hauteur, largeur, poids : évitez les mauvaises surprises |
| 3 | Le péage ? Vous le voyez venir | Une alerte avant d'y arriver |
| 4 | Vos arrêts sur votre route | Parkings, restos et douches poids lourds |
| 5 | Passez à Premium | Et roulez sans publicité |

**Texte promotionnel App Store** :
Le GPS poids lourd de Michelin : un itinéraire adapté à votre gabarit, l'alerte péage et vos arrêts sur la route. Sans publicité.

**Description courte Google Play** :
GPS poids lourd : itinéraire selon votre gabarit, alerte péage, sans pub.

**Description complète Google Play** :
Michelin Truckfly Premium, c'est le GPS pensé pour votre camion.
• Un itinéraire calculé selon votre hauteur, votre largeur, votre longueur et votre poids
• Une alerte à l'approche des péages, pour préparer votre badge
• Les parkings, restos et douches poids lourds sur votre itinéraire
• 44 pays européens
• Sans publicité
Renseignez votre camion, lancez votre trajet et roulez sereinement.

---

## À valider

- Ce qui existe vraiment dans l'offre établissements : statistiques, réponses aux avis, offres mises en avant.
- Les fonctions Premium citées : sans publicité, alerte péage, itinéraire selon le gabarit.
- Les chiffres : 700 000 conducteurs et 44 pays (repris du skill blog : 702 000 utilisateurs, 44 pays).
- La CPP « Entreprises de transport (B2B) » est mise de côté pour l'instant (dans l'historique git).
