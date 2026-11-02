// Capture chaque visuel de index.html en PNG (×3) dans png/<cpp>/<format>/, plus une planche par CPP.
// Usage : node scripts/capturer.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";
const { chromium } = createRequire(import.meta.url)("playwright");

const racine = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const navigateur = await chromium.launch();
const page = await navigateur.newPage({ viewport: { width: 2400, height: 1200 }, deviceScaleFactor: 3 });
await page.goto("file://" + path.join(racine, "index.html"));
await page.evaluate(() => document.fonts.ready);

let n = 0;
for (const shot of await page.$$("section.shot")) {
  const id = await shot.getAttribute("id");
  const cpp = await shot.getAttribute("data-cpp");
  const fmt = await shot.getAttribute("data-fmt");
  const dossier = path.join(racine, "png", cpp, fmt === "ios" ? "app-store" : "google-play");
  fs.mkdirSync(dossier, { recursive: true });
  await shot.screenshot({ path: path.join(dossier, id.replace(`-${fmt}`, "") + ".png") });
  n++;
}
// Planches d'aperçu (taille CSS)
for (const serie of await page.$$(".serie")) {
  const titre = await serie.$eval("h2", (h) => h.textContent);
  const cpp = await serie.$eval("section.shot", (s) => s.dataset.cpp);
  const fmt = titre.includes("Google") ? "google-play" : "app-store";
  await serie.screenshot({ path: path.join(racine, "png", cpp, `planche-${fmt}.png`), scale: "css" });
}
await navigateur.close();
console.log(`${n} PNG dans png/`);
