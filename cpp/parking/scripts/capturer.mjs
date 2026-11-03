// Exporte chaque visuel en PNG : Google Play 1080 × 1920 et App Store 1284 × 2778, plus une planche par format.
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";
const { chromium } = createRequire(import.meta.url)("playwright");
const racine = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const nav = await chromium.launch();
for (const fmt of ["google-play", "app-store"]) {
  const page = await nav.newPage({ viewport: { width: 2400, height: 1000 }, deviceScaleFactor: 3 });
  await page.goto("file://" + path.join(racine, "scripts", `index-${fmt}.html`));
  await page.evaluate(() => document.fonts.ready);
  fs.mkdirSync(path.join(racine, "png", fmt), { recursive: true });
  await page.screenshot({ path: path.join(racine, "png", `planche-${fmt}.png`), fullPage: true, scale: "css" });
  await page.evaluate(() => document.body.classList.add("capture"));
  for (const s of await page.$$("section.shot")) {
    await s.screenshot({ path: path.join(racine, "png", fmt, `parking-${await s.getAttribute("id")}.png`) });
  }
  await page.close();
}
await nav.close();
