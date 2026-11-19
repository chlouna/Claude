// Exporte ecran.html en PNG (×4) pour composer.py, une version par langue (titre de la barre traduit).
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const TITRES = { fr: "Parking poids lourds", en: "Truck parking", de: "Lkw-Parkplatz", nl: "Vrachtwagenparking",
  pl: "Parking dla ciężarówek", it: "Parcheggio camion", es: "Aparcamiento para camiones" };
const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const page = await navigateur.newPage({ viewport: { width: 263, height: 573 }, deviceScaleFactor: 4 });
await page.goto("file://" + path.join(ici, "ecran.html"));
await page.evaluate(() => document.fonts.ready);
for (const [lang, titre] of Object.entries(TITRES)) {
  await page.evaluate((t) => { document.getElementById("titre").textContent = t; }, titre);
  await page.screenshot({ path: path.join(ici, lang === "fr" ? "ecran.png" : `ecran-${lang}.png`) });
}
await navigateur.close();
