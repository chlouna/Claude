// Capture chaque interstitiel de index.html en PNG (×3 : 1170 × 2532 px) dans png/,
// plus une planche de tous les écrans. Usage : node scripts/capturer.mjs
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
import { fileURLToPath } from "node:url";
import path from "node:path";

const racine = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const page = await navigateur.newPage({ viewport: { width: 1360, height: 900 }, deviceScaleFactor: 3 });
await page.goto("file://" + path.join(racine, "index.html"));
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => document.body.classList.add("fige", "capture"));

const ecrans = await page.$$("section.ecran");
for (const ecran of ecrans) {
  const id = await ecran.getAttribute("id");
  const nom = await ecran.getAttribute("data-nom");
  await ecran.screenshot({ path: path.join(racine, "png", `${id}-${nom}.png`) });
}
await page.evaluate(() => document.body.classList.remove("capture"));
const planche = await page.$("body");
await page.setViewportSize({ width: 1360, height: 900 });
await planche.screenshot({ path: path.join(racine, "png", "planche.png"), scale: "css" });
await navigateur.close();
console.log(`${ecrans.length} PNG + planche dans png/`);
