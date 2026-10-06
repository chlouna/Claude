// Planche de contrôle d'une vidéo rendue : extrait des images réparties sur toute la durée
// et les assemble en une seule image, pour que Claude vérifie le rendu final d'un coup d'œil.
// Usage : node planche.mjs renders/video.mp4 [nombre d'images, 8 par défaut]
// Sortie : renders/video-planche.png, et la liste des instants capturés.
import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";

const [, , video, nombreTexte] = process.argv;
if (!video || !existsSync(video)) {
  console.error("Usage : node planche.mjs CHEMIN/VIDEO.mp4 [nombre d'images]");
  process.exit(1);
}
const nombre = Math.max(2, Math.min(24, parseInt(nombreTexte || "8", 10)));

function sonde(champs) {
  const sortie = execFileSync("ffprobe", ["-v", "error", "-select_streams", "v:0",
    "-show_entries", champs, "-of", "json", video], { encoding: "utf8" });
  return JSON.parse(sortie);
}

const flux = sonde("stream=width,height").streams[0];
const duree = parseFloat(sonde("format=duration").format.duration);
const vertical = flux.height > flux.width;
const colonnes = vertical ? Math.min(nombre, 6) : Math.min(nombre, 4);
const lignes = Math.ceil(nombre / colonnes);
const sortie = video.replace(/\.[a-z0-9]+$/i, "") + "-planche.png";

// une image au milieu de chaque tranche, pour ne pas tomber pile sur un fondu de début ou de fin
const instants = Array.from({ length: nombre }, (_, i) => ((i + 0.5) * duree) / nombre);
const filtre = `select='${instants.map((t) => `lt(prev_pts*TB\\,${t.toFixed(3)})*gte(pts*TB\\,${t.toFixed(3)})`).join("+")}',scale=-2:360,tile=${colonnes}x${lignes}:padding=8:color=white`;

execFileSync("ffmpeg", ["-y", "-hide_banner", "-loglevel", "error", "-i", video,
  "-vf", filtre, "-frames:v", "1", "-fps_mode", "vfr", sortie]);

console.log(`Vidéo : ${flux.width} x ${flux.height}, ${duree.toFixed(2)} s`);
console.log(`Planche : ${sortie} (${nombre} images, de gauche à droite puis de haut en bas)`);
console.log("Instants : " + instants.map((t) => t.toFixed(1) + " s").join(", "));
