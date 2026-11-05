"""Version App Store (1284 × 2778) d'un visuel d'accueil fini fourni en 1080 × 1920.

    python3 commun/accueil_apple.py <dossier CPP> <visuel 1080x1920> <décalage photo en px>

Le format Apple est plus haut. Pour ne pas laisser de vide au-dessus du logo :
1. on détache l'en-tête du visuel (logo, trait blanc, rond jaune, encadré de l'accroche) ;
2. on comble le ciel derrière (inpainting) et on agrandit la photo pour remplir toute la hauteur ;
3. on replace l'en-tête en haut, à une taille qui garde le logo et l'accroche entiers.
Le décalage photo choisit la partie gardée à l'agrandissement (téléphone et picto entiers).
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

dossier, source, decalage_photo = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
nom = dossier.name
src = np.asarray(Image.open(source).convert("RGB"))
H0, W0 = src.shape[:2]
L, H = 1284, 2778
r, g, b = [src[..., i].astype(int) for i in range(3)]
haut = np.zeros((H0, W0), bool)
haut[:600] = True  # l'en-tête est dans le haut du visuel

# Rond jaune (disque et anneau)
jaune = haut & (r > 190) & (g > 190) & (b < 130)
# Trait blanc : lignes presque entièrement blanches
blanc = (r > 225) & (g > 225) & (b > 225)
lignes = np.where(blanc[:600].mean(axis=1) > 0.6)[0]
trait = np.zeros_like(haut)
for y in lignes:
    trait[y] = blanc[y]
# Encadré de l'accroche : le grand rectangle blanc autour du rond
ys, xs = np.where(jaune)
cx, cy = int(xs.mean()), int(ys.mean())
cadre = np.zeros_like(haut)
x0 = x1 = cx
while x0 > 0 and blanc[cy, x0 - 1] | jaune[cy, x0 - 1] | (src[cy, x0 - 1].sum() < 300):
    x0 -= 1
y0 = y1 = cy
# limites de l'encadré : on cherche la zone blanche/texte autour du centre du rond
col = (blanc | (b > 60) & (r < 80))  # blanc ou texte bleu foncé
bx = np.where(blanc[cy - 5 : cy + 5].mean(axis=0) > 0.5)[0]
bx = bx[(bx > cx - 400) & (bx < cx + 400)]
gx0, gx1 = bx.min(), bx.max()
by = np.where(blanc[:600, gx0 + 5 : gx0 + 15].mean(axis=1) > 0.8)[0]
by = by[(by > cy - 150) & (by < cy + 150)]
gy0, gy1 = by.min(), by.max()
cadre[gy0 : gy1 + 1, gx0 : gx1 + 1] = True
# Logo : blanc pur dans le coin haut gauche
logo = np.zeros_like(haut)
logo[40:230, 40:480] = (r[40:230, 40:480] > 215) & (g[40:230, 40:480] > 215) & (b[40:230, 40:480] > 215)

entete = jaune | trait | cadre | logo
masque = cv2.dilate(entete.astype(np.uint8) * 255, np.ones((7, 7), np.uint8))

# 1-2. Photo sans en-tête, agrandie pour remplir la hauteur Apple
propre = cv2.inpaint(src, masque, 9, cv2.INPAINT_TELEA)
s = H / H0
fond = cv2.resize(propre, (round(W0 * s), H), interpolation=cv2.INTER_LANCZOS4)
fond = fond[:, decalage_photo : decalage_photo + L]

# 3. En-tête replacé en haut
alpha = cv2.GaussianBlur(cv2.dilate(entete.astype(np.uint8) * 255, np.ones((3, 3), np.uint8)), (3, 3), 0)
gauche = np.where(entete.any(axis=0))[0]
gauche, droite = gauche.min(), max(gx1, np.where(logo.any(axis=0))[0].max())
gauche = np.where(logo.any(axis=0))[0].min()
se = min(s, (L - 80) / (droite - gauche))
dx = round((gauche + droite) / 2 * se - L / 2)
haut_logo = np.where(logo.any(axis=1))[0].min()
dy = round(haut_logo * se - 178)  # logo à 178 px du haut (le rond recouvre l'emplacement de l'ancien)
calque = cv2.resize(src, (round(W0 * se), round(H0 * se)), interpolation=cv2.INTER_LANCZOS4)
a = cv2.resize(alpha, (calque.shape[1], calque.shape[0]), interpolation=cv2.INTER_LINEAR)
# En-tête posé sur une toile au format Apple (décalage dx, dy ; dy peut être négatif)
toile = np.zeros((H, L, 3), float)
toile_a = np.zeros((H, L, 1), float)
ys0, xs0 = max(dy, 0), max(dx, 0)
yt0, xt0 = max(-dy, 0), max(-dx, 0)
hh = min(calque.shape[0] - ys0, H - yt0, round(640 * se))
ww = min(calque.shape[1] - xs0, L - xt0)
toile[yt0 : yt0 + hh, xt0 : xt0 + ww] = calque[ys0 : ys0 + hh, xs0 : xs0 + ww]
toile_a[yt0 : yt0 + hh, xt0 : xt0 + ww, 0] = a[ys0 : ys0 + hh, xs0 : xs0 + ww] / 255
out = toile * toile_a + fond.astype(float) * (1 - toile_a)
# Le trait blanc traverse toute la largeur
y_trait = round(lignes.mean() * se) - dy
ep = max(3, round(len(lignes) * se))
out[y_trait - ep // 2 : y_trait - ep // 2 + ep, :] = 255
# On redessine l'en-tête par-dessus le trait (le trait passe derrière le rond et l'encadré)
sans_trait = (jaune | cadre | logo).astype(np.uint8) * 255
a2 = cv2.resize(cv2.GaussianBlur(sans_trait, (3, 3), 0), (calque.shape[1], calque.shape[0]))
toile_a2 = np.zeros((H, L, 1), float)
toile_a2[yt0 : yt0 + hh, xt0 : xt0 + ww, 0] = a2[ys0 : ys0 + hh, xs0 : xs0 + ww] / 255
out = toile * toile_a2 + out * (1 - toile_a2)

Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(dossier / "png" / "app-store" / f"{nom}-01-accueil.png")
Image.fromarray(masque).save(f"/tmp/claude-0/-home-user-Claude/da3bc3ea-8ed9-531e-9bb0-2f2f36f549a7/scratchpad/masque-{nom}.png")
print(nom, "rond", (cx, cy), "encadré", (gx0, gy0, gx1, gy1), "trait", lignes.min(), lignes.max(), "échelle en-tête", round(se, 3))
