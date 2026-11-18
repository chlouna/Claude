// Exporte la banque de textes en PDF A4.
// Usage : node interstitiels/vinci-fetes/textes/exporter.mjs
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
import { fileURLToPath } from "node:url";
import path from "node:path";

const ici = path.dirname(fileURLToPath(import.meta.url));
const nav = await chromium.launch();
const page = await nav.newPage();
await page.goto("file://" + path.join(ici, "textes.html"));
await page.evaluate(() => document.fonts.ready);
await page.pdf({
  path: path.join(ici, "Truckfly-VINCI-banque-de-textes.pdf"),
  format: "A4",
  printBackground: true,
  displayHeaderFooter: true,
  headerTemplate: "<span></span>",
  footerTemplate: '<div style="width:100%;font-size:8px;color:#5a6072;padding:0 15mm;display:flex;justify-content:space-between;font-family:sans-serif"><span>Michelin Truckfly × VINCI Autoroutes · banque de textes</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
  margin: { top: "16mm", bottom: "18mm", left: "15mm", right: "15mm" },
});
await nav.close();
