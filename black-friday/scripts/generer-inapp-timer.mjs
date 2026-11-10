// Génère le message in-app « dernier jour » en HTML, avec un compte à rebours en direct, dans les 7 langues.
// Chaque fichier est autonome (polices et images intégrées) : black-friday/html-in-app/dernier-jour-timer-<langue>.html
// Usage : node black-friday/scripts/generer-inapp-timer.mjs
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";
import { execFileSync } from "node:child_process";

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || "playwright");
const BF = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SORTIE = path.join(BF, "html-in-app");
fs.mkdirSync(SORTIE, { recursive: true });

// Fin de l'offre : minuit heure locale du pays (heure de Paris partout, sauf Londres pour l'anglais)
const FIN = { fr: "2026-11-30T23:59:59+01:00", en: "2026-11-30T23:59:59+00:00", de: "2026-11-30T23:59:59+01:00",
  it: "2026-11-30T23:59:59+01:00", es: "2026-11-30T23:59:59+01:00", nl: "2026-11-30T23:59:59+01:00", pl: "2026-11-30T23:59:59+01:00" };
// Lien du bouton : à remplacer par le lien profond vers l'abonnement GPS Premium (ou l'action de votre outil in-app)
const LIEN = "LIEN_ABONNEMENT_GPS_PREMIUM";
const TXT = {
  fr: { titre: "Dernier jour : fin dans", u: ["h", "min", "s"], fini: "L'offre est terminée" },
  en: { titre: "Last day: ends in", u: ["hrs", "min", "sec"], fini: "This offer has ended" },
  de: { titre: "Letzter Tag: endet in", u: ["Std.", "Min.", "Sek."], fini: "Das Angebot ist beendet" },
  it: { titre: "Ultimo giorno: termina tra", u: ["ore", "min", "sec"], fini: "L'offerta è terminata" },
  es: { titre: "Último día: termina en", u: ["h", "min", "s"], fini: "La oferta ha terminado" },
  nl: { titre: "Laatste dag: eindigt over", u: ["uur", "min", "sec"], fini: "De actie is afgelopen" },
  pl: { titre: "Ostatni dzień: koniec za", u: ["godz.", "min", "sek."], fini: "Oferta się zakończyła" },
};

const dataUri = (fichier, type) => `data:${type};base64,${fs.readFileSync(fichier).toString("base64")}`;
// Téléphone compressé en WebP pour alléger le HTML
function telWebp(lg) {
  const src = path.join(BF, "assets", lg === "fr" ? "telephone-gps.png" : `telephone-gps-${lg}.png`);
  const out = path.join(SORTIE, `.tel-${lg}.webp`);
  execFileSync("python3", ["-c", `from PIL import Image; Image.open(${JSON.stringify(src)}).save(${JSON.stringify(out)}, "WEBP", quality=82, method=6)`]);
  const uri = dataUri(out, "image/webp"); fs.unlinkSync(out); return uri;
}

const navigateur = await chromium.launch();
const page = await navigateur.newPage();
for (const lg of Object.keys(TXT)) {
  const id = `message-in-app-3-dernier-jour-${lg}`;
  await page.goto("file://" + path.join(BF, "campagne.html") + `?solo=${id}`);
  await page.evaluate(() => document.fonts.ready);
  let css = await page.evaluate(() => [...document.querySelectorAll("style")].map(s => s.textContent).join("\n"));
  let html = await page.evaluate(i => document.getElementById(i).outerHTML, id);

  // Polices et images intégrées
  css = css.replace(/url\("assets\/fonts\/([^"]+)"\)/g, (_, f) => `url("${dataUri(path.join(BF, "assets", "fonts", f), "font/woff2")}")`);
  html = html.replace(/src="\.\.\/ma-video\/assets\/logos\/([^"]+)"/, (_, f) => `src="${dataUri(path.join(BF, "..", "ma-video", "assets", "logos", f), "image/png")}"`);
  html = html.replace(/src="assets\/telephone-gps[^"]*"/, `src="${telWebp(lg)}"`);

  // « Dernier jour » remplacé par le compte à rebours
  const t = TXT[lg];
  const timer = `<div class="timer" data-fin="${FIN[lg]}"><p class="timer-titre">${t.titre}</p>
    <div class="cases"><div class="case"><b data-u="h">00</b><small>${t.u[0]}</small></div><i>:</i>
    <div class="case"><b data-u="m">00</b><small>${t.u[1]}</small></div><i>:</i>
    <div class="case"><b data-u="s">00</b><small>${t.u[2]}</small></div></div>
    <p class="timer-fini">${t.fini}</p></div>`;
  html = html.replace(/<p class="compte">[^<]*<\/p>/, timer);
  // Bouton cliquable
  html = html.replace(/<span class="cta ?">([^<]*)<\/span>/, `<a class="cta" href="${LIEN}">$1</a>`);
  // Plein écran : la maquette 390 × 844 s'adapte à l'écran du téléphone
  html = html.replace(/style="--w:390px;--h:844px;--u:[^"]*"/, 'style="--w:100vw;--h:100vh;--u:min(calc(100vw / 36), calc(100vh / 77.9))"');

  const doc = `<!doctype html>
<html lang="${lg}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Black Friday · Dernier jour</title>
<style>
${css}
html, body { margin: 0; padding: 0; background: #0a0a0c; overflow: hidden; }
body { width: 100vw; height: 100vh; }
.kv { margin: 0 auto; }
a.cta { text-decoration: none; }
/* Compte à rebours */
.timer { position: relative; z-index: 3; margin-top: 4.9em; display: flex; flex-direction: column; align-items: center; gap: .8em; }
.timer-titre { font: italic 400 1.45em/1.1 "Texte"; color: var(--blanc); }
.cases { display: flex; align-items: flex-start; gap: .5em; }
.case { display: flex; flex-direction: column; align-items: center; gap: .3em; }
.case b { display: block; min-width: 1.7em; text-align: center; font: 900 italic 2.8em/1 "Titre"; letter-spacing: -.02em;
  color: #111; background: var(--blanc); border-radius: .22em; padding: .14em .12em .1em; font-variant-numeric: tabular-nums; }
.case small { font: italic 600 1em/1 "Texte"; color: var(--gris); }
.cases i { font: 900 italic 2.6em/1.15 "Titre"; color: var(--blanc); }
.timer-fini { display: none; font: 900 italic 2em/1.1 "Titre"; color: var(--blanc); text-align: center; }
.timer.fini .timer-titre, .timer.fini .cases { display: none; }
.timer.fini .timer-fini { display: block; }
.iam.fin .ligne-prix { margin-top: 1.9em; }
.iam.fin .ligne-code { margin-top: 1.9em; }
.iam.fin .tel { top: 49.5em; }
</style>
</head>
<body>
${html}
<script>
(function () {
  var el = document.querySelector(".timer"), fin = new Date(el.getAttribute("data-fin")).getTime();
  var h = el.querySelector('[data-u="h"]'), m = el.querySelector('[data-u="m"]'), s = el.querySelector('[data-u="s"]');
  function deux(n) { return (n < 10 ? "0" : "") + n; }
  function tic() {
    var reste = Math.max(0, Math.floor((fin - Date.now()) / 1000));
    h.textContent = deux(Math.floor(reste / 3600)); m.textContent = deux(Math.floor(reste % 3600 / 60)); s.textContent = deux(reste % 60);
    if (reste === 0) { el.classList.add("fini"); var b = document.querySelector(".cta"); if (b) b.style.display = "none"; clearInterval(t); }
  }
  var t = setInterval(tic, 1000); tic();
})();
</script>
</body>
</html>
`;
  const f = path.join(SORTIE, `dernier-jour-timer-${lg}.html`);
  fs.writeFileSync(f, doc);
  console.log(lg, Math.round(fs.statSync(f).size / 1024) + " Ko");
}
await navigateur.close();
