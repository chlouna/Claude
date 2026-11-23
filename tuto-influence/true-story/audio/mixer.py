# Compose la musique de fond (originale, synthétisée ici), place la voix off sur la ligne de temps,
# baisse la musique sous la voix, puis assemble le son avec la vidéo muette.
# Usage : <python avec numpy + soundfile> mixer.py [page=hugo]
# Entrées : mp4/<page>-9x16-muet.mp4, mp4/<page>-temps.json (écrit par rendre.mjs), audio/voix-<page>/NN.wav
# Sortie  : mp4/<page>-9x16.mp4
import json, subprocess, sys, pathlib
import numpy as np, soundfile as sf

ici = pathlib.Path(__file__).resolve().parent
racine = ici.parent
page = sys.argv[1] if len(sys.argv) > 1 else "hugo"
temps = json.loads((racine / "mp4" / f"{page}-temps.json").read_text())
SR = 48000
T = temps["duree"]
N = int(T * SR)

# ---------- Musique : pop douce et entraînante, 104 bpm, Do – Sol – La m – Fa ----------
rng = np.random.default_rng(7)
bpm = 104; temps_s = 60 / bpm; mesure = 4 * temps_s
def note(f, dur, kind="pluck"):
    t = np.arange(int(dur * SR)) / SR
    if kind == "pluck":   # piano électrique : sinus + harmoniques, attaque rapide, déclin
        w = np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*2*f*t) + 0.12*np.sin(2*np.pi*3*f*t)
        env = np.minimum(1, t / 0.005) * np.exp(-t * 3.2)
    elif kind == "basse":
        w = np.sin(2*np.pi*f*t) + 0.25*np.sin(2*np.pi*2*f*t)
        env = np.minimum(1, t / 0.01) * np.exp(-t * 1.6)
    elif kind == "nappe":
        w = sum(np.sin(2*np.pi*f*d*t) for d in (0.997, 1.0, 1.003)) / 3
        env = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4)
    return w * env
def kick():
    t = np.arange(int(0.25 * SR)) / SR
    return np.sin(2*np.pi*(50 + 90*np.exp(-t*30))*t) * np.exp(-t*14)
def bruit(dur, dec, hp=True):
    n = rng.standard_normal(int(dur * SR))
    if hp: n = np.diff(n, prepend=0)  # passe-haut simple
    return n * np.exp(-np.arange(len(n)) / SR * dec)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
ACC = [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]]  # Do, Sol, La m, Fa
BASSE = [36, 43, 45, 41]
mus = np.zeros((N + SR * 2, 2))
def pose(sig, t0, gain, pan=0.0):
    i = int(t0 * SR); j = min(len(mus), i + len(sig))
    if j <= i: return
    s = sig[: j - i] * gain
    mus[i:j, 0] += s * (1 - pan); mus[i:j, 1] += s * (1 + pan)
m = 0
while m * mesure < T + 1:
    a = m % 4; t0 = m * mesure
    for n in ACC[a]: pose(note(hz(n), mesure, "nappe"), t0, 0.035)
    if m >= 1:  # accords pincés sur les contretemps
        for b in range(4):
            for j, n in enumerate(ACC[a][1:]): pose(note(hz(n + 12), 0.5, "pluck"), t0 + (b + 0.5) * temps_s + j * 0.012, 0.05, pan=0.3 * (j - 1))
        for b, n in enumerate([BASSE[a], BASSE[a], BASSE[a] + 12, BASSE[a]]): pose(note(hz(n), temps_s * 0.95, "basse"), t0 + b * temps_s, 0.22)
    if m >= 2:  # batterie légère
        for b in range(4):
            if b in (0, 2): pose(kick(), t0 + b * temps_s, 0.45)
            if b in (1, 3): pose(bruit(0.18, 22, hp=False) * 0.6 + bruit(0.18, 30), t0 + b * temps_s, 0.06)
            for h in (0, 0.5): pose(bruit(0.05, 70), t0 + (b + h) * temps_s, 0.03, pan=0.2)
    m += 1
mus = mus[:N]
# fondu d'entrée et de sortie
f = np.ones(N); fi, fo = int(0.8 * SR), int(2.5 * SR)
f[:fi] = np.linspace(0, 1, fi); f[-fo:] = np.linspace(1, 0, fo)
mus *= f[:, None]
mus /= np.max(np.abs(mus)) + 1e-9

# ---------- Voix off ----------
voix = np.zeros(N)
actif = np.zeros(N)
for i, t0 in enumerate(temps["debuts_voix"]):
    a, sr = sf.read(ici / f"voix-{page}" / f"{i:02d}.wav")
    if a.ndim > 1: a = a.mean(1)
    a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)  # 24 kHz → 48 kHz
    k = int(t0 * SR); j = min(N, k + len(a))
    voix[k:j] += a[: j - k]; actif[k:j] = 1
voix /= np.max(np.abs(voix)) + 1e-9
# ---------- Mixage : la musique descend sous la voix (enveloppe lissée) ----------
lisse = int(0.25 * SR)
env = np.convolve(actif, np.ones(lisse) / lisse, mode="same")
gain_mus = 0.28 - 0.21 * np.clip(env, 0, 1)    # 0,28 seule, 0,07 sous la voix
mix = mus * gain_mus[:, None] + (0.85 * voix)[:, None]
mix /= max(1.0, np.max(np.abs(mix)) / 0.97)
wav = racine / "mp4" / f"{page}-son.wav"
sf.write(wav, mix, SR)
sf.write(racine / "mp4" / f"{page}-musique.wav", mus * 0.5, SR)
# ---------- Assemblage : loudness réseaux sociaux (-14 LUFS), vidéo copiée telle quelle ----------
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(racine / "mp4" / f"{page}-9x16-muet.mp4"), "-i", str(wav),
    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
    "-movflags", "+faststart", str(racine / "mp4" / f"{page}-9x16.mp4")], check=True)
print(f"mp4/{page}-9x16.mp4")
