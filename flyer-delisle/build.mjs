// Génère les flyers Michelin Truckfly × Delisle Lavage : une page A4 par station.
// Usage : node build.mjs            -> output/flyers-truckfly-delisle.pdf + un PDF et un PNG par station
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import QRCode from "qrcode";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright");

const dir = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(dir, "output");
fs.mkdirSync(out, { recursive: true });
const config = JSON.parse(fs.readFileSync(path.join(dir, "config.json"), "utf8"));

// --- Stations (CSV séparé par ;) ---
const lignes = fs.readFileSync(path.join(dir, "stations.csv"), "utf8").split(/\r?\n/).filter(l => l.trim());
const entetes = lignes.shift().split(";").map(s => s.trim());
const stations = lignes.map(l => Object.fromEntries(l.split(";").map((v, i) => [entetes[i], (v || "").trim()]))).filter(s => s.ville);

// --- Éléments facultatifs déposés dans assets/ ---
const trouve = (...noms) => noms.find(n => fs.existsSync(path.join(dir, "assets", n)));
const logoDelisle = trouve("logos/delisle.png", "logos/delisle.svg", "logos/delisle.jpg");
const photo = trouve("photo-camion.jpg", "photo-camion.jpeg", "photo-camion.png", "photo-camion.webp");

const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const slug = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

const ICO = {
  arret: '<svg viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
  gps: '<svg viewBox="0 0 24 24"><path d="M3 11l18-8-8 18-2-8-8-2z"/></svg>',
  avis: '<svg viewBox="0 0 24 24"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>',
  lavage: '<svg viewBox="0 0 24 24"><path d="M12 3s-6 6.5-6 11a6 6 0 0 0 12 0c0-4.5-6-11-6-11z"/></svg>',
  pin: '<svg viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
};
const APPLE = '<svg viewBox="0 0 24 24"><path d="M16.4 12.6c0-2.4 2-3.6 2.1-3.7-1.1-1.7-2.9-1.9-3.5-1.9-1.5-.2-2.9.9-3.7.9-.8 0-1.9-.9-3.2-.8-1.6 0-3.1 1-4 2.4-1.7 3-.4 7.4 1.2 9.8.8 1.2 1.8 2.5 3 2.4 1.2 0 1.7-.8 3.1-.8s1.9.8 3.2.8c1.3 0 2.1-1.2 2.9-2.4.9-1.4 1.3-2.7 1.3-2.8-.1 0-2.4-.9-2.4-3.9zM14 5.4c.7-.8 1.1-1.9 1-3-1 0-2.1.7-2.8 1.5-.6.7-1.2 1.8-1 2.9 1.1.1 2.1-.6 2.8-1.4z"/></svg>';
const PLAY = '<svg viewBox="0 0 24 24"><path d="M4 2.5v19c0 .4.4.6.7.4L20.5 13c.4-.2.4-.8 0-1L4.7 2.1c-.3-.2-.7 0-.7.4z"/></svg>';

async function page(s) {
  const lien = s.lien_qr || config.lien_qr_par_defaut;
  const qr = await QRCode.toString(lien, { type: "svg", margin: 0, errorCorrectionLevel: "M", color: { dark: "#061866", light: "#FFFFFF" } });
  const delisle = logoDelisle
    ? `<img src="assets/${logoDelisle}" alt="Delisle">`
    : `<div class="txt">Delisle<small>Lavage</small></div>`;
  return `
<section class="page">
  <div class="haut${photo ? " photo" : ""}">
    ${photo ? "" : '<div class="motif"><span></span><span></span><span></span><span></span></div>'}
    <div class="logos">
      <img class="truckfly" src="assets/logos/truckfly-blanc-rogne.png" alt="Michelin Truckfly">
      <span class="croix">×</span>
      <div class="delisle">${delisle}</div>
    </div>
    <div class="accroche">
      <span class="sur-titre">Application gratuite</span>
      <h1>L'appli des routiers, partenaire de ta station de lavage Delisle</h1>
      <p>Michelin Truckfly t'accompagne au quotidien sur la route. Trouve facilement tous les arrêts essentiels : parkings, restaurants, stations de lavage et bien plus encore. Consulte les avis de la communauté et planifie tes trajets en toute sérénité.</p>
    </div>
  </div>
  <img class="tel" src="assets/ecrans/connexion.png" alt="">

  <div class="milieu">
    <h2>La solution tout-en-un dédiée aux conducteurs routiers</h2>
    <ul class="atouts">
      <li><div class="ico">${ICO.arret}</div><div><b>Trouve les meilleurs arrêts</b><span>Parkings, restos, douches, lavages : partout en Europe.</span></div></li>
      <li><div class="ico">${ICO.gps}</div><div><b>Roule avec un GPS poids lourd</b><span>Un itinéraire adapté au gabarit de ton camion.</span></div></li>
      <li><div class="ico">${ICO.lavage}</div><div><b>Repère les 22 stations Delisle</b><span>Toutes les stations de lavage Delisle sur la carte.</span></div></li>
      <li><div class="ico">${ICO.avis}</div><div><b>Partage ton expérience</b><span>Note tes arrêts et aide toute la communauté.</span></div></li>
    </ul>
  </div>

  <div class="bas">
    <div class="gauche">
      <h3>Laisse ton avis,<br><em>ça change tout</em> sur la route !</h3>
      <p>Scanne le QR code, télécharge Michelin Truckfly et note ta station Delisle ${esc(s.ville.startsWith("Station") ? "" : "de " + s.ville)}.</p>
      <div class="stores">
        <div class="store">${PLAY}<div><small>Disponible sur</small><b>Google Play</b></div></div>
        <div class="store">${APPLE}<div><small>Télécharger dans</small><b>l'App Store</b></div></div>
      </div>
    </div>
    <div class="qr"><div class="carre">${qr}</div><div class="legende">Scanne-moi</div></div>
    <div class="station">${ICO.pin.replace("<svg", '<svg class="pin"')}<span class="nom">Delisle Lavage · ${esc(s.ville)}</span>${s.adresse ? `<span class="adr">${esc(s.adresse)}</span>` : ""}</div>
  </div>
</section>`;
}

const doc = (pages) => `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>Flyers Truckfly × Delisle</title><link rel="stylesheet" href="flyer.css">
${photo ? `<style>:root{--photo:url("assets/${photo}")}</style>` : ""}</head><body>${pages.join("\n")}</body></html>`;

const pages = [];
for (const s of stations) pages.push(await page(s));
const htmlPath = path.join(dir, "flyers.html");
fs.writeFileSync(htmlPath, doc(pages));

const browser = await chromium.launch();
const p = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
await p.goto("file://" + htmlPath);
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: path.join(out, config.fichier_pdf), format: "A4", printBackground: true, preferCSSPageSize: true });

// Un PDF + un aperçu PNG par station
fs.mkdirSync(path.join(out, "stations"), { recursive: true });
for (let i = 0; i < stations.length; i++) {
  const f = path.join(dir, `_tmp.html`);
  fs.writeFileSync(f, doc([pages[i]]));
  await p.goto("file://" + f);
  await p.evaluate(() => document.fonts.ready);
  const nom = `flyer-delisle-${slug(stations[i].ville)}`;
  await p.pdf({ path: path.join(out, "stations", nom + ".pdf"), format: "A4", printBackground: true, preferCSSPageSize: true });
  await p.emulateMedia({ media: "print" });
  await p.locator(".page").screenshot({ path: path.join(out, "stations", nom + ".png") });
  await p.emulateMedia({ media: "screen" });
  fs.unlinkSync(f);
}
await browser.close();
console.log(`${stations.length} flyer(s) générés · logo Delisle : ${logoDelisle || "absent (texte)"} · photo : ${photo || "absente"}`);
