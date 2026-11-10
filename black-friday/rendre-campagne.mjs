// Exporte la campagne Black Friday : planches + un PNG par visuel dans black-friday/png/campagne/.
// Usage : node black-friday/rendre-campagne.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const sortie = path.join(ici, "png", "campagne");
const url = "file://" + path.join(ici, "campagne.html");
fs.mkdirSync(sortie, { recursive: true });
const navigateur = await chromium.launch();

async function charger(suffixe, largeur, echelle) {
  const page = await navigateur.newPage({ viewport: { width: largeur, height: 900 }, deviceScaleFactor: echelle });
  await page.goto(url + suffixe);
  await page.evaluate(() => document.fonts.ready);
  return page;
}

// Planches
for (const vue of ["app", ...["fr", "en", "de", "it", "es", "nl", "pl"].map(lg => `reseaux-${lg}`)]) {
  const [v, lg] = vue.split("-");
  const page = await charger(`?vue=${v}${lg ? `&lg=${lg}` : ""}`, 3200, 1);
  // Capture limitée à la largeur réelle de la planche (pas d'espace vide à droite)
  const largeur = await page.evaluate(() => Math.ceil(document.getElementById("planche").getBoundingClientRect().right) + 48);
  await page.screenshot({ path: path.join(sortie, `planche-${vue}.png`), fullPage: true, clip: { x: 0, y: 0, width: largeur, height: await page.evaluate(() => document.documentElement.scrollHeight) } });
  await page.close();
}

// Un PNG par visuel
const page0 = await charger("", 2200, 1);
const exports = await page0.evaluate(() => window.EXPORTS);
await page0.close();
for (const [id, echelle, dossier] of exports) {
  fs.mkdirSync(path.join(sortie, dossier), { recursive: true });
  const page = await charger(`?solo=${id}`, 1300, echelle);
  await page.locator(`#${id}`).screenshot({ path: path.join(sortie, dossier, `${id}.png`) });
  await page.close();
  // Bannières à la taille exacte : aussi une version @2x pour les écrans haute définition
  if (echelle === 1 && !id.includes("brevo")) {
    const p2 = await charger(`?solo=${id}`, 1300, 2);
    await p2.locator(`#${id}`).screenshot({ path: path.join(sortie, dossier, `${id}@2x.png`) });
    await p2.close();
  }
}
await navigateur.close();
console.log(`${exports.length} visuels exportés`);
