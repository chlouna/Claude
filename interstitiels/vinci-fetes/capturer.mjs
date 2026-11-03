// Capture les 3 propositions en PNG ×3 (1170 × 2532) dans png/, plus planche.png.
// Usage : node interstitiels/vinci-fetes/capturer.mjs
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
import { fileURLToPath } from "node:url";
import path from "node:path";

const racine = path.dirname(fileURLToPath(import.meta.url));
const nav = await chromium.launch();
const page = await nav.newPage({ viewport: { width: 1300, height: 900 }, deviceScaleFactor: 3 });
await page.goto("file://" + path.join(racine, "index.html"));
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => document.body.classList.add("fige", "capture"));
for (const e of await page.$$("section.ecran")) {
  const nom = `${await e.getAttribute("id")}-${await e.getAttribute("data-nom")}.png`;
  await e.screenshot({ path: path.join(racine, "png", nom) });
}
await page.evaluate(() => document.body.classList.remove("capture"));
await (await page.$("body")).screenshot({ path: path.join(racine, "png", "planche.png"), scale: "css" });
await nav.close();
