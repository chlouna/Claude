// Rend chaque interstitiel de index.html en MP4 animé (1080 × 2338, 30 i/s) dans mp4/,
// 1 interstitiel = 1 fichier. Les animations CSS sont figées puis avancées image par image,
// pour un rendu sans saccade. Usage : node scripts/animer.mjs [durée en s, 4 par défaut]
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { mkdirSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const racine = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const duree = parseFloat(process.argv[2] || "4");
const filtre = process.argv[3] || ""; // ex. "i04" pour ne rendre qu'un écran
const ips = 30;
const images = Math.round(duree * ips);
const tmp = path.join(racine, "mp4", ".images");
rmSync(tmp, { recursive: true, force: true });
mkdirSync(tmp, { recursive: true });

const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const page = await navigateur.newPage({ viewport: { width: 1360, height: 900 }, deviceScaleFactor: 1080 / 390 });
await page.goto("file://" + path.join(racine, "index.html"));
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => document.body.classList.add("capture"));

const ecrans = (await page.$$("section.ecran"));
const tous = [];  // noms de tous les écrans, avant filtrage
for (const e of ecrans) tous.push(`${await e.getAttribute("id")}-${await e.getAttribute("data-nom")}`);
const garde = tous.map((n) => n.startsWith(filtre));
for (let k = ecrans.length - 1; k >= 0; k--) if (!garde[k]) ecrans.splice(k, 1);
const noms = [];
for (const e of ecrans) noms.push(`${await e.getAttribute("id")}-${await e.getAttribute("data-nom")}`);
noms.forEach((n) => mkdirSync(path.join(tmp, n), { recursive: true }));

for (let i = 0; i < images; i++) {
  const t = (i / ips) * 1000;
  await page.evaluate((t) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t; }), t);
  for (let k = 0; k < ecrans.length; k++) {
    await ecrans[k].screenshot({ path: path.join(tmp, noms[k], `${String(i).padStart(4, "0")}.png`) });
  }
}
await navigateur.close();

for (const n of noms) {
  const sortie = path.join(racine, "mp4", `${n}.mp4`);
  execFileSync("ffmpeg", ["-y", "-v", "error", "-framerate", String(ips), "-i", path.join(tmp, n, "%04d.png"),
    "-vf", "scale=1080:2338:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
    "-movflags", "+faststart", sortie]);
}
rmSync(tmp, { recursive: true, force: true });
console.log(`${noms.length} MP4 (${duree} s) dans mp4/`);
