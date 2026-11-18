// Capture les 4 écrans du parcours (1170 × 2532) et la planche du parcours.
// Usage : node interstitiels/vinci-fetes/funnel/capturer.mjs
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
import { fileURLToPath } from "node:url";
import path from "node:path";

const ici = path.dirname(fileURLToPath(import.meta.url));
const nav = await chromium.launch();
const page = await nav.newPage({ viewport: { width: 1900, height: 1000 }, deviceScaleFactor: 3 });
await page.goto("file://" + path.join(ici, "funnel.html"));
await page.evaluate(() => document.fonts.ready);
await (await page.$(".rang")).screenshot({ path: path.join(ici, "parcours.png"), scale: "css" });
await page.evaluate(() => document.body.classList.add("capture"));
for (const e of await page.$$("section.ecran")) {
  await e.screenshot({ path: path.join(ici, `ecran-${await e.getAttribute("data-nom")}.png`) });
}
await nav.close();
