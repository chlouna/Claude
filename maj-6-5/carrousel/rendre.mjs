// Exporte les visuels du carrousel en PNG 1080 × 1350 (4:5).
// Usage : node maj-6-5/carrousel/rendre.mjs
import { createRequire } from "node:module";
import { readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
for (const f of readdirSync(ici).filter((f) => /^visuel-\d+\.html$/.test(f)).sort()) {
  const page = await navigateur.newPage({ viewport: { width: 360, height: 450 }, deviceScaleFactor: 3 });
  await page.goto("file://" + path.join(ici, f));
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(ici, `carrousel-6-5-${f.match(/\d+/)[0]}.png`) });
  await page.close();
}
await navigateur.close();
