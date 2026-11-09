// Exporte : le panorama 5400 × 1350, ses 5 slides en 1080 × 1350, un PDF carrousel LinkedIn,
// et la carte unique « 81 % » en 1080 × 1350. Usage : node linkedin/reconnaissance-routiers/rendre.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const navigateur = await chromium.launch();
const page = await navigateur.newPage({ viewport: { width: 1800, height: 940 }, deviceScaleFactor: 3 });
await page.goto("file://" + path.join(ici, "carrousel.html"));
await page.evaluate(() => document.fonts.ready);
await page.locator("#panorama").screenshot({ path: path.join(ici, "panorama-5400x1350.png") });
const pano = await page.locator("#panorama").boundingBox();
for (let i = 0; i < 5; i++) {
  await page.screenshot({ path: path.join(ici, `slide-${i + 1}-1080x1350.png`), clip: { x: pano.x + i * 360, y: pano.y, width: 360, height: 450 } });
}
await page.locator("#carte").screenshot({ path: path.join(ici, "carte-81-1080x1350.png") });
await navigateur.close();
