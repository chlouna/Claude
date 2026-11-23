// Rend la vidéo tuto en MP4 1920 × 1080, 30 i/s, à partir de video.html.
// Usage : node tuto-influence/rendre.mjs            → mp4/tuto-marketing-influence.mp4
//         node tuto-influence/rendre.mjs 1,9.5,20   → aperçus PNG à ces instants (en secondes), dans apercus/
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { mkdirSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const apercus = process.argv[2] ? process.argv[2].split(",").map(Number) : null;
const duree = 78, ips = 30;

const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const page = await navigateur.newPage({ viewport: { width: 960, height: 540 }, deviceScaleFactor: 2 });
page.on("pageerror", (e) => { console.error("Erreur page :", e.message); process.exit(1); });
await page.goto("file://" + path.join(ici, "video.html"));
await page.waitForFunction(() => window.PRET === true);
await page.evaluate(() => document.fonts.ready);
const regle = (t) => page.evaluate((t) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t; }), t);

if (apercus) {
  mkdirSync(path.join(ici, "apercus"), { recursive: true });
  for (const s of apercus) { await regle(s * 1000); await page.screenshot({ path: path.join(ici, "apercus", `${s}s.png`) }); }
} else {
  const tmp = path.join(ici, "mp4", ".images");
  rmSync(tmp, { recursive: true, force: true });
  mkdirSync(tmp, { recursive: true });
  for (let i = 0; i < duree * ips; i++) {
    await regle((i / ips) * 1000);
    await page.screenshot({ path: path.join(tmp, `${String(i).padStart(5, "0")}.png`) });
  }
  execFileSync("ffmpeg", ["-y", "-v", "error", "-framerate", String(ips), "-i", path.join(tmp, "%05d.png"),
    "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-movflags", "+faststart",
    path.join(ici, "mp4", "tuto-marketing-influence.mp4")]);
  rmSync(tmp, { recursive: true, force: true });
  console.log("mp4/tuto-marketing-influence.mp4");
}
await navigateur.close();
