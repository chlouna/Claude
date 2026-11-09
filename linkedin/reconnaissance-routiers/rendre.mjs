// Exporte le carrousel (5 slides 1:1) et la carte unique en PNG 1080 px et 3000 px.
// Usage : node linkedin/reconnaissance-routiers/rendre.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const navigateur = await chromium.launch();
for (const largeur of [1080, 3000]) {
  const page = await navigateur.newPage({ viewport: { width: 1800, height: 760 }, deviceScaleFactor: largeur / 360 });
  await page.goto("file://" + path.join(ici, "carrousel.html"));
  await page.evaluate(() => document.fonts.ready);
  const pano = await page.locator("#panorama").boundingBox();
  for (let i = 0; i < 5; i++) {
    await page.screenshot({ path: path.join(ici, `carrousel-${i + 1}-${largeur}.png`), clip: { x: pano.x + i * 360, y: pano.y, width: 360, height: 360 } });
  }
  await page.locator("#carte").screenshot({ path: path.join(ici, `carte-81-${largeur}.png`) });
  await page.close();
}
await navigateur.close();
