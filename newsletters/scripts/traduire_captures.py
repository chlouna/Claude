"""Traduit les captures d'écran de l'appli (B2B novembre 2026) en EN et NL en recouvrant les textes FR."""
import sys
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
F = {"b": "/usr/share/fonts/opentype/inter/Inter-Bold.otf", "s": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
     "m": "/usr/share/fonts/opentype/inter/Inter-Medium.otf", "r": "/usr/share/fonts/opentype/inter/Inter-Regular.otf"}
NAVY, DARK, GREY, WHITE, GREEN = (6, 24, 102), (17, 17, 17), (150, 150, 150), (255, 255, 255), (60, 140, 70)

def fond(im, box):
    x0, y0, x1, y1 = box; px = []
    for x in range(x0 - 2, x1 + 3):
        for y in (y0 - 2, y1 + 2): px.append(im.getpixel((min(max(x, 0), im.width - 1), min(max(y, 0), im.height - 1)))[:3])
    for y in range(y0, y1 + 1):
        for x in (x0 - 2, x1 + 2): px.append(im.getpixel((min(max(x, 0), im.width - 1), y))[:3])
    return Counter(px).most_common(1)[0][0]

def rep(im, box, lignes, taille, coul, poids="b", align="l", bg=None, clip=False, maxw=None):
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = box
    c = bg or fond(im, box); d.rectangle(box, fill=c)
    if isinstance(lignes, str): lignes = [lignes]
    t = taille; lim = maxw or (x1 - x0)
    while True:
        f = ImageFont.truetype(F[poids], t)
        if clip or max(d.textlength(l, font=f) for l in lignes) <= lim or t <= 7: break
        t -= 1
    h = (y1 - y0) / len(lignes)
    calque = Image.new("RGBA", im.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(calque)
    for i, l in enumerate(lignes):
        w = dc.textlength(l, font=f); yc = y0 + h * i + h / 2
        x = {"l": x0, "c": (x0 + x1 - w) / 2, "r": x1 - w}[align]
        dc.text((x, yc), l, font=f, fill=coul, anchor="lm")
    if clip:
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rectangle(box, fill=255)
        calque.putalpha(Image.composite(calque.getchannel("A"), Image.new("L", im.size, 0), m))
    im.alpha_composite(calque)

T = {
 "EN": dict(membre="Member since", ami="Friend", edit="Edit", share="Share", camion="My truck", type="HGV / Semi-trailer", surnom='Nickname: "Bobby"',
            retrouvez=["Find your", "trucker friends"], connect=["Connect with the", "truckers you", "already know"], sync="Sync", ajouter="Add",
            sortie="Exit 31.2", peage="Toll in 1.4 km",
            salut="Hi louna!", enligne="7 friends online", fil="Activity feed", tout="All", amis="Friends", avis="Mathieu P. left a review at:", ilya="23 hours ago",
            note="Rating:", ouvert="Open", signaler="Report", jaime="Unlike", aimepar="Liked by", vous="You", retrouvez2=["Find your", "trucker friends"], connect2="Connect with the",
            carte="Map", commu="Community", amis_tab="Friends",
            params="Settings", general="General", langue="App language", unites="Distance units", connexion="Login settings", cookies="Cookie settings",
            affichage="Map display", nuit="Night mode", vue="Map view", nord="Keep north up on the map", zoom="Auto zoom", sat="Satellite view", trafic="Traffic view"),
 "NL": dict(membre="Lid sinds", ami="Vriend", edit="Bewerken", share="Delen", camion="Mijn truck", type="Vrachtwagen / Oplegger", surnom='Bijnaam: "Bobby"',
            retrouvez=["Vind je", "truckvrienden"], connect=["Maak contact met", "truckers die je", "al kent"], sync="Synchroniseren", ajouter="Toevoegen",
            sortie="Afrit 31.2", peage="Tol over 1,4 km",
            salut="Hoi louna!", enligne="7 vrienden online", fil="Activiteitenfeed", tout="Alles", amis="Vrienden", avis="Mathieu P. plaatste een review bij:", ilya="23 uur geleden",
            note="Beoordeling:", ouvert="Open", signaler="Melden", jaime="Niet leuk", aimepar="Geliket door", vous="jou", retrouvez2=["Vind je", "truckvrienden"], connect2="Maak contact met",
            carte="Kaart", commu="Community", amis_tab="Vrienden",
            params="Instellingen", general="Algemeen", langue="Taal van de app", unites="Afstandseenheden", connexion="Inloginstellingen", cookies="Cookie-instellingen",
            affichage="Kaartweergave", nuit="Nachtmodus", vue="Kaartstijl", nord="Noorden boven houden", zoom="Automatisch zoomen", sat="Satellietweergave", trafic="Verkeersweergave"),
}

for L, t in T.items():
    # 1. Profil (photo plein écran)
    im = Image.open(SRC / "4.png").convert("RGBA")
    rep(im, (202, 220, 312, 238), t["membre"], 12, GREY, "r")
    rep(im, (199, 268, 229, 285), t["ami"], 9, GREY, "r")
    rep(im, (99, 313, 139, 334), t["edit"], 12, WHITE, "b", clip=True)
    rep(im, (322, 313, 384, 334), t["share"], 12, NAVY, "b", align="c")
    rep(im, (52, 592, 128, 612), t["camion"], 13, DARK, "b", clip=True)
    rep(im, (154, 649, 345, 676), t["type"], 17, DARK, "r")
    rep(im, (154, 677, 290, 694), t["surnom"], 11, GREY, "r")
    rep(im, (99, 744, 222, 786), t["retrouvez"], 14, WHITE, "b")
    rep(im, (68, 792, 222, 850), t["connect"], 12, WHITE, "r")
    rep(im, (74, 864, 256, 884), t["sync"], 13, NAVY, "b", align="c")
    rep(im, (343, 864, 409, 886), t["ajouter"], 13, WHITE, "b")
    im.save(OUT / f"profil-photo-{L.lower()}.png")
    # 2. GPS, alerte péage
    im = Image.open(SRC / "5.png").convert("RGBA")
    rep(im, (174, 57, 231, 69), t["sortie"], 9, NAVY, "b", align="c", bg=WHITE)
    rep(im, (66, 444, 175, 464), t["peage"], 11, DARK, "b")
    im.save(OUT / f"alerte-peage-{L.lower()}.png")
    # 3. Fil d'activité, likes
    im = Image.open(SRC / "6.png").convert("RGBA")
    rep(im, (80, 68, 200, 93), t["salut"], 17, WHITE, "b")
    rep(im, (91, 93, 180, 109), t["enligne"], 10, (210, 215, 235), "r")
    rep(im, (29, 129, 150, 151), t["fil"], 12, DARK, "b")
    rep(im, (194, 131, 230, 150), t["tout"], 11, WHITE, "b")
    rep(im, (245, 131, 291, 150), t["amis"], 11, NAVY, "b", align="c")
    rep(im, (81, 183, 286, 197), t["avis"], 10, GREY, "r")
    rep(im, (81, 215, 170, 230), t["ilya"], 10, GREY, "r")
    rep(im, (39, 368, 130, 385), t["note"], 10, DARK, "b")
    rep(im, (39, 408, 85, 429), t["ouvert"], 9, GREEN, "r")
    rep(im, (39, 448, 90, 465), t["signaler"], 9, NAVY, "s")
    rep(im, (190, 449, 264, 465), t["jaime"], 8, NAVY, "m", align="r")
    rep(im, (59, 471, 160, 489), t["aimepar"], 10, GREY, "r")
    f = ImageFont.truetype(F["r"], 10); xv = 59 + ImageDraw.Draw(im).textlength(t["aimepar"] + " ", font=f)
    ImageDraw.Draw(im).text((xv, 480), t["vous"], font=ImageFont.truetype(F["b"], 10), fill=DARK, anchor="lm")
    rep(im, (60, 515, 150, 549), t["retrouvez2"], 11, WHITE, "b")
    rep(im, (40, 551, 185, 559), t["connect2"], 10, WHITE, "r", clip=True, bg=NAVY)
    rep(im, (40, 582, 85, 597), t["carte"], 8, GREY, "m", align="c")
    rep(im, (160, 582, 230, 597), t["commu"], 8, NAVY, "s", align="c")
    rep(im, (240, 582, 285, 597), t["amis_tab"], 8, GREY, "m", align="c")
    im.save(OUT / f"fil-likes-{L.lower()}.png")
    # 4. Paramètres, langue
    im = Image.open(SRC / "7.png").convert("RGBA")
    rep(im, (115, 62, 210, 83), t["params"], 11, WHITE, "s", align="c")
    rep(im, (33, 99, 150, 119), t["general"], 16, DARK, "b")
    rep(im, (33, 139, 185, 158), t["langue"], 11, DARK, "s")
    rep(im, (33, 177, 240, 196), t["unites"], 11, DARK, "s")
    rep(im, (33, 214, 240, 233), t["connexion"], 11, DARK, "s")
    rep(im, (33, 251, 240, 269), t["cookies"], 11, DARK, "s")
    rep(im, (33, 309, 260, 333), t["affichage"], 16, DARK, "b")
    rep(im, (33, 357, 185, 376), t["nuit"], 11, DARK, "s")
    rep(im, (33, 407, 215, 426), t["vue"], 11, DARK, "s")
    rep(im, (33, 455, 243, 473), t["nord"], 11, DARK, "s")
    rep(im, (33, 500, 240, 518), t["zoom"], 11, DARK, "s")
    rep(im, (33, 545, 240, 563), t["sat"], 11, DARK, "s")
    rep(im, (33, 589, 240, 607), t["trafic"], 11, DARK, "s")
    im.save(OUT / f"parametres-langue-{L.lower()}.png")
print("ok")
