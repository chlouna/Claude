# Génère la voix off de Hugo, une piste WAV par sous-titre, en local.
# Voix : Piper « fr_FR-tom-medium » (voix masculine française, 44,1 kHz), nettoyée par FFmpeg :
# coupe des graves parasites, dé-essage (sifflantes adoucies), compression légère pour une voix régulière.
# Usage : <python avec piper-tts> voix.py <fichier .onnx de la voix> [page=hugo]
# Modèle : github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-fr_FR-tom-medium.tar.bz2
# Écrit audio/voix-<page>/NN.wav et <page>-voix.js (window.VOIX = durées en secondes).
import json, re, sys, pathlib, subprocess, tempfile
import soundfile as sf

ici = pathlib.Path(__file__).resolve().parent
modele = pathlib.Path(sys.argv[1]).resolve()
page = sys.argv[2] if len(sys.argv) > 2 else "hugo"
html = (ici.parent / f"{page}.html").read_text()
bloc = html[html.index("const SCRIPT = ["):]
bloc = bloc[:bloc.index("];") + 1]
lignes = [json.loads("[" + m + "]")[0] for m in re.findall(r"^\s*\[(\".*?\")[,\]]", bloc, re.M)]

# Prononciation : quelques mots que la synthèse lit mal
DIRE = {"brief": "brife", "Max": "Maxe"}
def a_dire(t):
    t = t.lstrip("#").replace("*", "").replace("…", ",").strip(" ,:")
    for k, v in DIRE.items():
        t = re.sub(rf"\b{k}\b", v, t)
    return t if t.endswith(("?", ".", "!")) else t + "."

piper = pathlib.Path(sys.executable).with_name("piper")
FILTRE = "highpass=f=85,deesser=i=0.5:m=0.5:f=0.5,equalizer=f=6500:t=q:w=1.2:g=-3,equalizer=f=2800:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2"
sortie = ici / f"voix-{page}"
sortie.mkdir(exist_ok=True)
durees = []
with tempfile.TemporaryDirectory() as tmp:
    for i, l in enumerate(lignes):
        brut = pathlib.Path(tmp) / f"{i:02d}.wav"
        subprocess.run([str(piper), "-m", str(modele), "-f", str(brut), "--length-scale", "1.04", "--sentence-silence", "0.12"],
                       input=a_dire(l).encode(), check=True, capture_output=True)
        dst = sortie / f"{i:02d}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(brut), "-af", FILTRE, "-ar", "48000", str(dst)], check=True)
        a, sr = sf.read(dst)
        durees.append(round(len(a) / sr, 3))
        print(f"{i:02d} {durees[-1]:5.2f}s  {a_dire(l)}")
(ici.parent / f"{page}-voix.js").write_text(f"window.VOIX = {json.dumps(durees)};\n")
