// Exporte le visuel en PNG 1080 × 1920 (camion-restaurant.png).
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
const { chromium } = createRequire(import.meta.url)("playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const nav = await chromium.launch();
const page = await nav.newPage({ viewport: { width: 400, height: 700 }, deviceScaleFactor: 3 });
await page.goto("file://" + path.join(ici, "index.html"));
await page.waitForLoadState("networkidle");
await (await page.$("#camion-restaurant")).screenshot({ path: path.join(ici, "camion-restaurant.png") });
await nav.close();
