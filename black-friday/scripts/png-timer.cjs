// Exporte le message « Dernier jour » avec compte à rebours en PNG (1170 × 2532), figé à 12 h de la fin.
// Usage : node black-friday/scripts/png-timer.cjs [heures_restantes]
const { chromium } = require("playwright");
const path = require("path"), fs = require("fs");
const H = Number(process.argv[2] || 12);
const DIR = path.join(__dirname, "..", "html-in-app"), OUT = path.join(__dirname, "..", "png", "campagne", "timer");
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  for (const f of fs.readdirSync(DIR).filter(x => x.startsWith("dernier-jour-timer-") && x.endsWith(".html"))) {
    const lg = f.slice(19, -5), html = fs.readFileSync(path.join(DIR, f), "utf8");
    const fin = new Date(html.match(/data-fin="([^"]+)"/)[1]).getTime();
    const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
    await p.clock.setFixedTime(new Date(fin - H * 3600 * 1000));
    await p.goto("file://" + path.join(DIR, f));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(OUT, `message-in-app-3-dernier-jour-timer-${lg}.png`) });
    await p.close();
  }
  await b.close();
})();
