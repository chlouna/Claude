// Exporte, pour chaque fin (a, b, c) : le panorama 5400 × 1350, les 5 slides 1080 × 1350.
// La fin « a » est la version par défaut (fichiers sans suffixe) ; b et c ont le suffixe -fin-b / -fin-c.
// Exporte aussi la carte unique « 81 % ». Usage : node linkedin/reconnaissance-routiers/rendre.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const navigateur = await chromium.launch();
for (const fin of ["a", "b", "c"]) {
  const suffixe = fin === "a" ? "" : `-fin-${fin}`;
  const page = await navigateur.newPage({ viewport: { width: 1800, height: 940 }, deviceScaleFactor: 3 });
  await page.goto("file://" + path.join(ici, "carrousel.html") + "?fin=" + fin);
  await page.evaluate(() => document.fonts.ready);
  await page.locator("#panorama").screenshot({ path: path.join(ici, `panorama-5400x1350${suffixe}.png`) });
  const pano = await page.locator("#panorama").boundingBox();
  for (let i = fin === "a" ? 0 : 4; i < 5; i++) {
    await page.screenshot({ path: path.join(ici, `slide-${i + 1}-1080x1350${suffixe}.png`), clip: { x: pano.x + i * 360, y: pano.y, width: 360, height: 450 } });
  }
  if (fin === "a") await page.locator("#carte").screenshot({ path: path.join(ici, "carte-81-1080x1350.png") });
  await page.close();
}
await navigateur.close();
