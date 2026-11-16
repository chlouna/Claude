"""Remplace le texte de l'avis (FR) par sa traduction sur chaque mockup du fil d'activité."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
D = Path(__file__).parent
FONT = "/home/user/Claude/guide-profil/assets/fonts/Inter-Regular.otf"
AVIS = {
 "en": "A first for me. Very warm welcome. Parking spotless, good meal, showers and toilets spotless. I’ll gladly come back.",
 "es": "Primera vez aquí. Muy buena acogida, parking impecable, buena comida, duchas y aseos impecables. ¡Volveré!",
 "it": "Prima volta per me. Ottima accoglienza, parcheggio impeccabile, buon pasto, doccia e servizi impeccabili. Tornerò!",
 "nl": "Eerste keer voor mij. Goed onthaal, parking piekfijn, lekker eten, douche en sanitair piekfijn. Ik kom graag terug.",
}
TOP = {"en": 490, "es": 498, "it": 505, "nl": 514}   # haut de la 1re ligne
X0, X1, PITCH, SIZE, K = 45, 312, 18.5, 13.2, 4
COL = (122, 122, 128, 255)
for lg, txt in AVIS.items():
    im = Image.open(D / f"mockup-fil-{lg}.png").convert("RGBA")
    a = np.asarray(im).copy()
    top = TOP[lg]
    bg = a[top - 4, 60].copy()
    a[top - 3: top + int(2 * PITCH) + 14, 42:326] = bg
    im = Image.fromarray(a)
    f = ImageFont.truetype(FONT, int(SIZE * K))
    words, lines, cur = txt.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) / K <= X1 - X0: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    assert len(lines) <= 3, (lg, lines)
    W, H = (X1 - X0 + 20) * K, int(3 * PITCH + 10) * K
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
    for i, l in enumerate(lines):
        dr.text((0, (9.6 + i * PITCH) * K), l, font=f, fill=COL, anchor="ls")
    lay = lay.resize((W // K, H // K), Image.LANCZOS)
    im.alpha_composite(lay, (X0, top))
    im.save(D / f"mockup-fil-{lg}-trad.png")
    print(lg, lines)
