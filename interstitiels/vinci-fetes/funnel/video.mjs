// Rend simulation.html en vidéo MP4 1920 × 1080, 30 i/s.
// Usage : node interstitiels/vinci-fetes/funnel/video.mjs
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { mkdirSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const tmp = process.env.IMAGES || path.join(ici, ".images");
rmSync(tmp, { recursive: true, force: true }); mkdirSync(tmp, { recursive: true });
const duree = 21, ips = 30;
const nav = await chromium.launch();
const page = await nav.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await page.goto("file://" + path.join(ici, "simulation.html"));
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => Promise.all([...document.images].map(i => i.decode())));
await page.evaluate(() => window.init());
for (let i = 0; i < duree * ips; i++) {
  await page.evaluate((t) => window.rendu(t), i / ips);
  await page.screenshot({ path: path.join(tmp, `${String(i).padStart(4, "0")}.png`) });
}
await nav.close();
execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(ips), "-i", path.join(tmp, "%04d.png"),
  "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart",
  path.join(ici, "Truckfly-VINCI-simulation-parcours.mp4")]);
rmSync(tmp, { recursive: true, force: true });
console.log("vidéo prête");
