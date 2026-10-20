// Exporte les posts en PNG : 1080 × 1350 (Instagram) et 3000 × 3750 (export ≥ 3000 px de la charte).
// Usage : node maj-6-4/post-like/rendre.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
// [page, largeur de la maquette en px, nom de sortie]
const posts = [["post.html", 360, "post-like-6-4"], ["post-nouveautes.html", 652, "post-nouveautes-6-4"]];
for (const [fichier, base, nom] of posts) {
  for (const largeur of [1080, 3000]) {
    const page = await navigateur.newPage({ viewport: { width: base, height: base * 1.25 }, deviceScaleFactor: largeur / base });
    await page.goto("file://" + path.join(ici, fichier));
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(ici, `${nom}-${largeur}.png`) });
    await page.close();
  }
}
await navigateur.close();
