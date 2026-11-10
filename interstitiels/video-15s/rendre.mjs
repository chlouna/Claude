// Rend l'interstitielle de 15 s en MP4, une vidéo par langue (768 × 1152, 30 i/s), dans mp4/.
// Usage : node interstitiels/video-15s/rendre.mjs [langues, ex. "fr,en"] [instants à capturer en PNG, ex. "1,3,5"]
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { mkdirSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const langues = (process.argv[2] || "fr,en,de,nl,pl,it,es").split(",");
const apercus = process.argv[3] ? process.argv[3].split(",").map(Number) : null; // mode aperçu : PNG seulement
const duree = 15, ips = 30;
// HD=1 : version 1080 × 1620 pour Google Ad Manager, qui recompresse la vidéo : débit élevé mais plafonné,
// H.264 niveau 4.0 (lisible par tous les téléphones, contrairement au 1536 × 2304 en niveau 5.0) et piste son muette.
const hd = process.env.HD === "1";
const [lw, lh, suffixe] = hd ? [1080, 1620, "-hd"] : [768, 1152, ""];

const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
for (const lang of langues) {
  const page = await navigateur.newPage({ viewport: { width: 384, height: 576 }, deviceScaleFactor: lw / 384 });
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
    ...(hd ? ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"] : []),
    "-vf", `scale=${lw}:${lh}:flags=lanczos,format=yuv420p`, "-c:v", "libx264", "-crf", hd ? "16" : "18", "-preset", "slow",
    ...(hd ? ["-profile:v", "high", "-level:v", "4.0", "-maxrate", "6M", "-bufsize", "12M", "-c:a", "aac", "-b:a", "64k", "-shortest"] : []),
    "-movflags", "+faststart", path.join(ici, "mp4", `interstitiel-15s-${lang}${suffixe}.mp4`)]);
  rmSync(tmp, { recursive: true, force: true });
  console.log(`interstitiel-15s-${lang}${suffixe}.mp4`);
}
await navigateur.close();
