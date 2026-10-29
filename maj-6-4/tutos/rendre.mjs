// Rend les tutoriels en MP4 (30 i/s) dans renders/ : 9x16 en 1080 × 1920, 16x9 en 1920 × 1080.
// Usage : node maj-6-4/tutos/rendre.mjs [pages, ex. "like-9x16,peage-16x9"] [instants à capturer en PNG, ex. "2,5,9"]
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { mkdirSync, rmSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const ici = path.dirname(fileURLToPath(import.meta.url));
const pages = process.argv[2] ? process.argv[2].split(",") : readdirSync(ici).filter((f) => /-(9x16|16x9)\.html$/.test(f)).map((f) => f.replace(".html", ""));
const apercus = process.argv[3] ? process.argv[3].split(",").map(Number) : null;
const ips = 30;

const navigateur = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
for (const nom of pages) {
  const vertical = nom.endsWith("9x16");
  const [w, h] = vertical ? [540, 960] : [960, 540];
  const page = await navigateur.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  await page.goto("file://" + path.join(ici, `${nom}.html`));
  await page.evaluate(() => document.fonts.ready);
  const duree = Number(await page.evaluate(() => document.body.dataset.duree));
  const regle = (t) => page.evaluate((t) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t; }), t);

  if (apercus) {
    mkdirSync(path.join(ici, "apercus"), { recursive: true });
    for (const s of apercus) { await regle(s * 1000); await page.screenshot({ path: path.join(ici, "apercus", `${nom}-${s}s.png`) }); }
    await page.close();
    continue;
  }
  const tmp = path.join(ici, "renders", `.images-${nom}`);
  rmSync(tmp, { recursive: true, force: true });
  mkdirSync(tmp, { recursive: true });
  for (let i = 0; i < duree * ips; i++) {
    await regle((i / ips) * 1000);
    await page.screenshot({ path: path.join(tmp, `${String(i).padStart(4, "0")}.png`) });
  }
  await page.close();
  execFileSync("ffmpeg", ["-y", "-v", "error", "-framerate", String(ips), "-i", path.join(tmp, "%04d.png"),
    "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
    "-movflags", "+faststart", path.join(ici, "renders", `tuto-${nom}.mp4`)]);
  rmSync(tmp, { recursive: true, force: true });
  console.log(`tuto-${nom}.mp4`);
}
await navigateur.close();
