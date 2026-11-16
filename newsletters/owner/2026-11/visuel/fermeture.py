"""Capture « Ma fermeture temporaire » : nom de test masqué, dates passées à Noël, export e-mail."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
im = Image.open("capture-fermeture.webp").convert("RGB")
FB = "/home/user/Claude/guide-profil/assets/fonts/Inter-Bold.otf"
FR = "/home/user/Claude/guide-profil/assets/fonts/Inter-Regular.otf"
# 1. Nom de l'établissement de test : flou + nom neutre
box = (10, 200, 450, 270)
im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(14)), box[:2])
d = ImageDraw.Draw(im)
d.text((29, 235), "Votre établissement", font=ImageFont.truetype(FB, 31), fill=(255, 255, 255), anchor="lm")
# 2. Dates de fermeture : vacances de Noël
for x0, txt in ((1424, "24 / 12 / 2026"), (1724, "26 / 12 / 2026")):
    d.rectangle((x0, 396, x0 + 160, 434), fill=(242, 242, 242))
    sz = 25
    while ImageFont.truetype(FR, sz).getlength(txt) > 146: sz -= 1
    d.text((x0 + 6, 415), txt, font=ImageFont.truetype(FR, sz), fill=(30, 30, 30), anchor="lm")
out = im.resize((1200, 630), Image.LANCZOS)
q = 90
while True:
    out.save("capture-fermeture-temporaire.jpg", quality=q, optimize=True, progressive=True)
    import os
    if os.path.getsize("capture-fermeture-temporaire.jpg") < 95_000 or q < 60: break
    q -= 4
print(os.path.getsize("capture-fermeture-temporaire.jpg") // 1024, "Ko q", q)
