// Exporte la planche et chaque format en PNG dans black-friday/png/.
// Usage : node black-friday/rendre.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const sortie = path.join(ici, "png");
fs.mkdirSync(sortie, { recursive: true });
const url = "file://" + path.join(ici, "index.html");
const navigateur = await chromium.launch();

// Planche complète
let page = await navigateur.newPage({ viewport: { width: 1300, height: 800 }, deviceScaleFactor: 2 });
await page.goto(url);
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: path.join(sortie, "planche.png"), fullPage: true });
const formats = await page.evaluate(() => window.FORMATS);
await page.close();

// Un PNG par format, à la taille d'export
for (const [id, echelle] of formats) {
  page = await navigateur.newPage({ viewport: { width: 1300, height: 900 }, deviceScaleFactor: echelle });
  await page.goto(`${url}?solo=${id}`);
  await page.evaluate(() => document.fonts.ready);
  await page.locator(`#${id}`).screenshot({ path: path.join(sortie, `${id}.png`) });
  await page.close();
}
// Pistes de fond (fonds.html)
const urlFonds = "file://" + path.join(ici, "fonds.html");
page = await navigateur.newPage({ viewport: { width: 1100, height: 800 }, deviceScaleFactor: 2 });
await page.goto(urlFonds);
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: path.join(sortie, "planche-fonds.png"), fullPage: true });
const ids = await page.evaluate(() => window.IDS);
await page.close();
fs.mkdirSync(path.join(sortie, "fonds"), { recursive: true });
for (const id of ids) {
  page = await navigateur.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 3 });
  await page.goto(`${urlFonds}?solo=${id}`);
  await page.evaluate(() => document.fonts.ready);
  await page.locator(`#${id}`).screenshot({ path: path.join(sortie, "fonds", `${id}.png`) });
  await page.close();
}
// Plaquette fond noir (noir.html)
const urlNoir = "file://" + path.join(ici, "noir.html");
fs.mkdirSync(path.join(sortie, "noir"), { recursive: true });
page = await navigateur.newPage({ viewport: { width: 1660, height: 800 }, deviceScaleFactor: 2 });
await page.goto(urlNoir);
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: path.join(sortie, "noir", "plaquette-noir.png"), fullPage: true });
const exports = await page.evaluate(() => window.EXPORTS);
await page.close();
for (const [id, echelle] of exports) {
  page = await navigateur.newPage({ viewport: { width: 1300, height: 900 }, deviceScaleFactor: echelle });
  await page.goto(`${urlNoir}?solo=${id}`);
  await page.evaluate(() => document.fonts.ready);
  await page.locator(`#${id}`).screenshot({ path: path.join(sortie, "noir", `${id}.png`) });
  await page.close();
}
await navigateur.close();
