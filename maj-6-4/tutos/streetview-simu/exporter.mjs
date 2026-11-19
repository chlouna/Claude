// Exporte ecran.html en PNG (×4) pour composer.py.
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const page = await navigateur.newPage({ viewport: { width: 263, height: 573 }, deviceScaleFactor: 4 });
await page.goto("file://" + path.join(ici, "ecran.html"));
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: path.join(ici, "ecran.png") });
await navigateur.close();
