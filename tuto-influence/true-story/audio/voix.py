# Génère la voix off de Hugo, une piste WAV par sous-titre, avec Kokoro (local, hors ligne).
# Voix : 40 % ff_siwis (français) + 60 % im_nicola (timbre masculin).
# Usage : <python avec kokoro-onnx> voix.py <dossier_modeles_kokoro> [page=hugo]
# Écrit audio/voix-<page>/NN.wav et <page>-voix.js (window.VOIX = durées en secondes).
import json, re, sys, pathlib
import soundfile as sf
from kokoro_onnx import Kokoro

ici = pathlib.Path(__file__).resolve().parent
modeles = pathlib.Path(sys.argv[1])
page = sys.argv[2] if len(sys.argv) > 2 else "hugo"
html = (ici.parent / f"{page}.html").read_text()
bloc = html[html.index("const SCRIPT = ["):]
bloc = bloc[:bloc.index("];") + 1]
lignes = [json.loads("[" + m + "]")[0] for m in re.findall(r"^\s*\[(\".*?\")[,\]]", bloc, re.M)]

# Prononciation : quelques mots que la synthèse lit mal
DIRE = {"brief": "brife", "pubs": "peubes", "Max": "Maxe"}
def a_dire(t):
    t = t.lstrip("#").replace("*", "").replace("…", ",").strip(" ,:")
    for k, v in DIRE.items():
        t = re.sub(rf"\b{k}\b", v, t)
    return t if t.endswith(("?", ".", "!")) else t + "."

k = Kokoro(str(modeles / "kokoro.onnx"), str(modeles / "voices.bin"))
style = 0.4 * k.get_voice_style("ff_siwis") + 0.6 * k.get_voice_style("im_nicola")
sortie = ici / f"voix-{page}"
sortie.mkdir(exist_ok=True)
durees = []
for i, l in enumerate(lignes):
    a, sr = k.create(a_dire(l), voice=style, speed=1.08, lang="fr-fr")
    sf.write(sortie / f"{i:02d}.wav", a, sr)
    durees.append(round(len(a) / sr, 3))
    print(f"{i:02d} {durees[-1]:5.2f}s  {a_dire(l)}")
(ici.parent / f"{page}-voix.js").write_text(f"window.VOIX = {json.dumps(durees)};\n")
