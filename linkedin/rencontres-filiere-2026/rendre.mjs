// Exporte post.html en PNG 1080 × 1080 (LinkedIn, 1:1).
// Usage : node linkedin/rencontres-filiere-2026/rendre.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const page = await navigateur.newPage({ viewport: { width: 360, height: 360 }, deviceScaleFactor: 3 });
await page.goto("file://" + path.join(ici, "post.html"));
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: path.join(ici, "rencontres-filiere-2026-1080.png") });
await navigateur.close();
