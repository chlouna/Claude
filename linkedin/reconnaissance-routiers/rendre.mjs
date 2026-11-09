// Exporte chaque visuel en PNG 1080 × 1350 (LinkedIn 4:5) et 3000 × 3750 (export ≥ 3000 px de la charte).
// Usage : node linkedin/reconnaissance-routiers/rendre.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const navigateur = await chromium.launch();
const visuels = [["carte", "carte-81"], ["s1", "carrousel-1"], ["s2", "carrousel-2"], ["s3", "carrousel-3"], ["s4", "carrousel-4"]];
for (const largeur of [1080, 3000]) {
  const page = await navigateur.newPage({ viewport: { width: 360, height: 450 }, deviceScaleFactor: largeur / 360 });
  await page.goto("file://" + path.join(ici, "post.html"));
  await page.evaluate(() => document.fonts.ready);
  for (const [id, nom] of visuels) {
    await page.locator("#" + id).screenshot({ path: path.join(ici, `${nom}-${largeur}.png`) });
  }
  await page.close();
}
await navigateur.close();
