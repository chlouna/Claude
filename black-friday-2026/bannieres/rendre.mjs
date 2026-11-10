// Rend chaque banniere-xx.html en PNG et JPG 2000 × 880.
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
const ici = dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1000, height: 440 }, deviceScaleFactor: 2 });
for (const f of readdirSync(ici).filter(f => /^banniere-..\.html$/.test(f))) {
  await p.goto('file://' + join(ici, f)); await p.evaluate(() => document.fonts.ready);
  const el = await p.$('#b'); const base = join(ici, f.replace('.html', ''));
  await el.screenshot({ path: base + '.png' });
  await el.screenshot({ path: base + '.jpg', type: 'jpeg', quality: 85 });
}
await b.close(); console.log('rendu ok');
