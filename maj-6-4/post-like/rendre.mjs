// Exporte post.html en PNG : 1080 × 1350 (Instagram) et 3000 × 3750 (export ≥ 3000 px de la charte).
// Usage : node maj-6-4/post-like/rendre.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
for (const largeur of [1080, 3000]) {
  const page = await navigateur.newPage({ viewport: { width: 360, height: 450 }, deviceScaleFactor: largeur / 360 });
  await page.goto("file://" + path.join(ici, "post.html"));
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(ici, `post-like-6-4-${largeur}.png`) });
  await page.close();
}
await navigateur.close();
