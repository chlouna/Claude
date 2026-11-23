// Rend une vidéo verticale 1080 × 1920, 30 i/s, à partir d'une page du dossier (story = Léa, hugo = Hugo).
// Usage : node tuto-influence/true-story/rendre.mjs hugo            → mp4/hugo-9x16.mp4
//         node tuto-influence/true-story/rendre.mjs hugo 1,8,20     → aperçus PNG dans apercus/
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { mkdirSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const nom = process.argv[2] || "hugo";
const apercus = process.argv[3] ? process.argv[3].split(",").map(Number) : null;
const ips = 30;

const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const page = await navigateur.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
page.on("pageerror", (e) => { console.error("Erreur page :", e.message); process.exit(1); });
await page.goto("file://" + path.join(ici, `${nom}.html`));
await page.waitForFunction(() => window.PRET === true);
await page.evaluate(() => document.fonts.ready);
const duree = await page.evaluate(() => window.DUREE);
const regle = (t) => page.evaluate((t) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t; }), t);

if (apercus) {
  mkdirSync(path.join(ici, "apercus"), { recursive: true });
  for (const s of apercus) { await regle(s * 1000); await page.screenshot({ path: path.join(ici, "apercus", `${nom}-${s}s.png`) }); }
  console.log("durée", duree, "s");
} else {
  const tmp = path.join(ici, "mp4", ".images");
  rmSync(tmp, { recursive: true, force: true });
  mkdirSync(tmp, { recursive: true });
  const n = Math.round(duree * ips);
  for (let i = 0; i < n; i++) {
    await regle((i / ips) * 1000);
    await page.screenshot({ path: path.join(tmp, `${String(i).padStart(5, "0")}.png`) });
  }
  execFileSync("ffmpeg", ["-y", "-v", "error", "-framerate", String(ips), "-i", path.join(tmp, "%05d.png"),
    "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-movflags", "+faststart",
    path.join(ici, "mp4", `${nom}-9x16.mp4`)]);
  rmSync(tmp, { recursive: true, force: true });
  console.log(`mp4/${nom}-9x16.mp4`, duree, "s");
}
await navigateur.close();
