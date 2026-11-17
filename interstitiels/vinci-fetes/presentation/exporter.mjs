// Exporte presentation.html en PDF (12 pages 1280 × 720) et en aperçus PNG.
// Usage : node interstitiels/vinci-fetes/presentation/exporter.mjs
// (APERCU=<dossier> pour choisir où écrire les aperçus PNG)
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
import { fileURLToPath } from "node:url";
import path from "node:path";

const ici = path.dirname(fileURLToPath(import.meta.url));
const nav = await chromium.launch();
const page = await nav.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
await page.goto("file://" + path.join(ici, "presentation.html"));
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: path.join(ici, "Truckfly-VINCI-operation-fetes.pdf"), width: "1280px", height: "720px", printBackground: true });
const slides = await page.$$("section.slide");
const dossier = process.env.APERCU || ici;
for (let i = 0; i < slides.length; i++) {
  await slides[i].screenshot({ path: path.join(dossier, `diapo-${String(i + 1).padStart(2, "0")}.png`) });
}
await nav.close();
console.log(slides.length + " diapositives");
