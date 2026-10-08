// Rend l'interstitielle de 10 s en MP4, une vidéo par langue (1080 × 2338, 30 i/s), dans mp4/.
// Usage : node interstitiels/video-10s/rendre.mjs [langues, ex. "fr,en"] [instants à capturer en PNG, ex. "1,3,5"]
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { mkdirSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const langues = (process.argv[2] || "fr,en,de,nl,pl,it,es").split(",");
const apercus = process.argv[3] ? process.argv[3].split(",").map(Number) : null; // mode aperçu : PNG seulement
const duree = 10, ips = 30;

const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
for (const lang of langues) {
  const page = await navigateur.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1080 / 390 });
  await page.goto("file://" + path.join(ici, `${lang}.html`));
  await page.evaluate(() => document.fonts.ready);
  const regle = (t) => page.evaluate((t) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t; }), t);

  if (apercus) {
    mkdirSync(path.join(ici, "apercus"), { recursive: true });
    for (const s of apercus) { await regle(s * 1000); await page.screenshot({ path: path.join(ici, "apercus", `${lang}-${s}s.png`) }); }
    await page.close();
    continue;
  }
  const tmp = path.join(ici, "mp4", `.images-${lang}`);
  rmSync(tmp, { recursive: true, force: true });
  mkdirSync(tmp, { recursive: true });
  for (let i = 0; i < duree * ips; i++) {
    await regle((i / ips) * 1000);
    await page.screenshot({ path: path.join(tmp, `${String(i).padStart(4, "0")}.png`) });
  }
  await page.close();
  execFileSync("ffmpeg", ["-y", "-v", "error", "-framerate", String(ips), "-i", path.join(tmp, "%04d.png"),
    "-vf", "scale=1080:2338:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
    "-movflags", "+faststart", path.join(ici, "mp4", `interstitiel-10s-${lang}.mp4`)]);
  rmSync(tmp, { recursive: true, force: true });
  console.log(`interstitiel-10s-${lang}.mp4`);
}
await navigateur.close();
