// Rend le reel 6.4 « zoom sur les photos de profil » en MP4 (1080 × 1920, 30 i/s, 15 s, sans son).
// Usage : node maj-6-4/reel-zoom/rendre.mjs            → reel-zoom-6-4.mp4
//         node maj-6-4/reel-zoom/rendre.mjs 1,4,7      → aperçus PNG à ces instants, dans apercus/
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { mkdirSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const apercus = process.argv[2] ? process.argv[2].split(",").map(Number) : null;
const duree = 15, ips = 30;

const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const page = await navigateur.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
await page.goto("file://" + path.join(ici, "reel.html"));
await page.evaluate(() => document.fonts.ready);
const regle = (t) => page.evaluate((t) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t; }), t);

if (apercus) {
  mkdirSync(path.join(ici, "apercus"), { recursive: true });
  for (const s of apercus) { await regle(s * 1000); await page.screenshot({ path: path.join(ici, "apercus", `${s}s.png`) }); }
} else {
  const tmp = path.join(ici, ".images");
  rmSync(tmp, { recursive: true, force: true });
  mkdirSync(tmp, { recursive: true });
  for (let i = 0; i < duree * ips; i++) {
    await regle((i / ips) * 1000);
    await page.screenshot({ path: path.join(tmp, `${String(i).padStart(4, "0")}.png`) });
  }
  execFileSync("ffmpeg", ["-y", "-v", "error", "-framerate", String(ips), "-i", path.join(tmp, "%04d.png"),
    "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
    "-movflags", "+faststart", path.join(ici, "reel-zoom-6-4.mp4")]);
  rmSync(tmp, { recursive: true, force: true });
  console.log("reel-zoom-6-4.mp4");
}
await navigateur.close();
