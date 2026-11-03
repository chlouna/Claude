// Exporte chaque visuel en PNG 1080 × 1920 dans png/google-play/, plus une planche.
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
const { chromium } = createRequire(import.meta.url)("playwright");
const racine = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const nav = await chromium.launch();
const page = await nav.newPage({ viewport: { width: 2000, height: 700 }, deviceScaleFactor: 3 });
await page.goto("file://" + path.join(racine, "scripts", "index.html"));
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: path.join(racine, "png", "planche-google-play.png"), fullPage: true, scale: "css" });
await page.evaluate(() => document.body.classList.add("capture"));
for (const s of await page.$$("section.shot")) {
  await s.screenshot({ path: path.join(racine, "png", "google-play", `parking-${await s.getAttribute("id")}.png`) });
}
await nav.close();
