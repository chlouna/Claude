# Flyer Michelin Truckfly × Delisle Lavage

Une page A4 par station Delisle, à la charte Michelin Truckfly (Michelin Blue, jaune en accent sur fond bleu, Bib + Inter).

## Générer

```bash
npm install
node build.mjs
```

Sortie dans `output/` :
- `flyers-truckfly-delisle.pdf` : toutes les stations, une page chacune
- `stations/flyer-delisle-<ville>.pdf` et `.png` : un fichier par station

## À compléter

- `stations.csv` : une ligne par station (`ville;adresse;lien_qr`). Adresse et lien facultatifs.
  Les 5 villes actuelles viennent d'une recherche web, à vérifier ; il manque 17 stations.
- `config.json` → `lien_qr_par_defaut` : lien du QR code (actuellement truckfly.com, à remplacer par le lien de téléchargement / tracking).
- `assets/logos/delisle.png` (ou .svg) : logo Delisle. Sans fichier, un logo texte s'affiche.
- `assets/photo-camion.jpg` : photo du camion Delisle (facultatif). Si présente, elle passe en fond du bandeau bleu.
