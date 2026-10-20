// Exporte la bulle « 1 · Aimé par Vous » en PNG transparent (×10, avec son ombre).
// Usage : node maj-6-4/post-like/bulle.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const page = await navigateur.newPage({ viewport: { width: 400, height: 200 }, deviceScaleFactor: 10 });
await page.goto("file://" + path.join(ici, "bulle.html"));
await page.evaluate(() => document.fonts.ready);
await (await page.$("body")).screenshot({ path: path.join(ici, "bulle-aime-par-vous.png"), omitBackground: true });
await navigateur.close();
