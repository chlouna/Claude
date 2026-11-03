"""Mise en page commune des CPP restaurant et parking : 2 visuels d'accueil + 5 volets, en panorama.

Le décor (rond blanc, trait jaune) et certains éléments (téléphone incliné, pictos) sont placés
sur un seul grand dessin, découpé ensuite en visuels : ils passent d'une image à l'autre.

Formats :
- Google Play : 1080 × 1920 (rendu 360 × 640 × 3)
- App Store   : 1284 × 2778 (rendu 428 × 926 × 3)

Positions exprimées en fractions de la largeur (l) et de la hauteur (h) d'un visuel.
"""

from pathlib import Path

CPP = Path(__file__).resolve().parent.parent

FORMATS = {
    "google-play": {"l": 360, "h": 640, "t": 34, "st": 15, "txt": 46, "tel_haut": 178, "tel_h": 420},
    "app-store": {"l": 428, "h": 926, "t": 42, "st": 18, "txt": 78, "tel_haut": 258, "tel_h": 620},
}

# --- Pictos (repris des visuels store existants) --------------------------------------------

FOURCHETTE = '<path d="M33 30v18a7 7 0 0 0 6 7v20h5V55a7 7 0 0 0 6-7V30h-4v14h-3V30h-4v14h-3V30z M66 30c-5 3-7 9-7 16v10h5v19h5V30z" fill="#fff"/>'
CAMION_MINI = '<path d="M24 58h22V44H24z M46 48h7l5 6v4H46z" fill="#fff"/><circle cx="30" cy="60" r="3" fill="#fff"/><circle cx="52" cy="60" r="3" fill="#fff"/>'


def picto(type_, taille):
    """Picto en forme de punaise, comme sur la carte de l'app."""
    queue = '<path d="M40 92 L50 104 L60 92Z" fill="{c}"/>'
    if type_ == "resto":
        corps = (
            '<rect x="6" y="6" width="88" height="88" rx="18" fill="#fff" stroke="#E2477A" stroke-width="7"/>'
            '<rect x="17" y="17" width="66" height="66" rx="12" fill="#4A63E7"/>'
            '<g transform="translate(6 -4) scale(.9)">' + FOURCHETTE.replace("M33 30", "M60 30").replace("M66 30", "M86 30") + "</g>"
            '<g transform="translate(-2 2)">' + CAMION_MINI + "</g>"
        )
        c = "#E2477A"
    elif type_ == "parking":
        corps = (
            '<rect x="6" y="6" width="88" height="88" rx="18" fill="#fff" stroke="#5B5BD6" stroke-width="7"/>'
            '<text x="50" y="74" text-anchor="middle" font-family="Inter" font-weight="700" font-size="64" fill="#4A4FD8">P</text>'
        )
        c = "#5B5BD6"
    elif type_ == "douche":
        corps = (
            '<rect x="6" y="6" width="88" height="88" rx="18" fill="#fff" stroke="#8E5BD8" stroke-width="7"/>'
            '<rect x="17" y="17" width="66" height="66" rx="12" fill="#8E5BD8"/>'
            '<path d="M50 28S34 47 34 58a16 16 0 0 0 32 0C66 47 50 28 50 28z" fill="#fff"/>'
        )
        c = "#8E5BD8"
    else:  # carburant
        corps = (
            '<rect x="6" y="6" width="88" height="88" rx="18" fill="#fff" stroke="#F08A24" stroke-width="7"/>'
            '<rect x="17" y="17" width="66" height="66" rx="12" fill="#F08A24"/>'
            '<rect x="32" y="30" width="24" height="42" rx="3" fill="#fff"/><path d="M56 40h6l5 5v18a3.5 3.5 0 0 1-7 0v-8h-4" fill="none" stroke="#fff" stroke-width="4"/>'
        )
        c = "#F08A24"
    return (
        f'<svg width="{taille}" height="{taille * 1.06:.0f}" viewBox="0 0 100 106" style="filter:drop-shadow(0 6px 10px rgba(0,0,0,.3))">'
        f'{corps}{queue.format(c=c)}</svg>'
    )


# --- Construction --------------------------------------------------------------------------

def element(contenu, x, y, f):
    """Élément positionné dans le panorama (x, y en fractions d'un visuel, centre de l'élément)."""
    return f'<div class="el" style="left:{x * f["l"]:.1f}px;top:{y * f["h"]:.1f}px">{contenu}</div>'


def telephone(img, hauteur, f, angle=0):
    return f'<img src="../captures/{img}" style="height:{hauteur * f["h"]:.0f}px;transform:translate(-50%,-50%) rotate({angle}deg)" class="tel-pano" alt="">'


def page(titre_page, accueil, volets, fmt):
    f = FORMATS[fmt]
    l, h = f["l"], f["h"]
    n = 2 + len(volets)

    # Décor : grand rond blanc sur le visuel 2, trait jaune à partir du visuel 3,
    # petit rond blanc entre les volets 2 et 3 (visuels 4 et 5).
    x0 = 2 * l
    k = l / 360
    trait = (
        f"M{x0 - 20 * k:.0f} {0.59 * h:.0f} C {x0 + 120 * k:.0f} {0.47 * h:.0f}, {x0 + 240 * k:.0f} {0.47 * h:.0f}, {x0 + l:.0f} {0.56 * h:.0f} "
        + " ".join(
            f"S {x0 + (j + 1.67) * l:.0f} {(0.69 if j % 2 == 0 else 0.47) * h:.0f}, {x0 + (j + 2) * l:.0f} {(0.59 if j % 2 == 0 else 0.56) * h:.0f}"
            for j in range(0, len(volets) - 1)
        )
        + f" L {n * l + 20:.0f} {0.53 * h:.0f}"
    )
    rond_r = 0.45 * h if fmt == "app-store" else 0.45 * h
    decor = (
        f'<svg class="deco" viewBox="0 0 {n * l} {h}" width="{n * l}" height="{h}">'
        f'<circle cx="{1.25 * l:.0f}" cy="{0.5 * h:.0f}" r="{rond_r:.0f}" fill="#fff"/>'
        f'<path d="{trait}" fill="none" stroke="#FFFF1A" stroke-width="{14 * k:.0f}" stroke-linecap="round"/>'
        f'<circle cx="{4 * l:.0f}" cy="{0.58 * h:.0f}" r="{0.336 * h:.0f}" fill="#fff"/>'
        "</svg>"
    )

    # Éléments qui passent d'un visuel à l'autre (au-dessus du fond du visuel 1)
    a = accueil
    elements = "".join(
        [
            element(telephone(a["tel_incline"], 0.5, f, 18), 0.92, 0.74, f),
            element(picto(a["picto_grand"], 0.2 * l), 0.6, 0.6, f),
            element(picto(a["picto_moyen"], 0.17 * l), 0.36, 0.77, f),
            element(picto(a["picto_petit1"], 0.11 * l), 0.14, 0.53, f),
            element(picto(a["picto_petit2"], 0.1 * l), 0.47, 0.47, f),
            # Visuel 2 : deux téléphones et deux pictos
            element(telephone(a["tel_haut"], 0.4, f), 1.0 + 0.69, 0.32, f),
            element(telephone(a["tel_bas"], 0.4, f), 1.0 + 0.47, 0.8, f),
            element(picto(a["picto_v2_1"], 0.16 * l), 1.0 + 0.24, 0.37, f),
            element(picto(a["picto_v2_2"], 0.16 * l), 1.0 + 0.82, 0.88, f),
        ]
    )

    fond = (
        f'<div class="fond-accueil" style="width:{l}px;height:{h}px">'
        f'<img class="logo" src="../../assets/logos/truckfly-blanc-rogne.png" alt="Michelin Truckfly" style="width:{0.5 * l:.0f}px;left:{0.09 * l:.0f}px;top:{0.065 * h:.0f}px">'
        f'<div class="ligne" style="top:{0.315 * h:.0f}px"></div>'
        f'<div class="soleil" style="left:{0.68 * l:.0f}px;top:{0.315 * h:.0f}px;width:{0.5 * l:.0f}px;height:{0.5 * l:.0f}px"><i></i></div>'
        f'<div class="accroche" style="left:{0.68 * l:.0f}px;top:{0.315 * h:.0f}px;width:{0.46 * l:.0f}px;font-size:{11.5 * k:.1f}px">{a["accroche"]}</div>'
        "</div>"
    )
    pano = f'<div class="pano" style="width:{n * l}px;height:{h}px">{decor}{fond}{elements}</div>'

    textes = [None, None] + [(t, s, img) for (_, t, s, img, _) in volets]
    ids = ["accueil", "accueil-2"] + [c for (c, *_) in volets]
    shots = []
    for i in range(n):
        contenu = ""
        if textes[i]:
            t, s, img = textes[i]
            contenu = f'<div class="textes"><h1>{t}</h1><p>{s}</p></div><img class="tel" src="../captures/{img}" alt="">'
        shots.append(
            f'<section class="shot" id="{i + 1:02d}-{ids[i]}" style="width:{l}px;height:{h}px">'
            f'<div class="decale" style="left:{-i * l}px">{pano}</div>{contenu}</section>'
        )

    css = f"""
@font-face {{ font-family: "Bib"; src: url("../../assets/fonts/BIB-Bold.woff2") format("woff2"); font-weight: 700; }}
@font-face {{ font-family: "Inter"; src: url("../../assets/fonts/Inter-Bold.otf") format("opentype"); font-weight: 700; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #F5F3F1; padding: 24px; display: flex; gap: 16px; flex-wrap: wrap; font-family: "Inter", sans-serif; }}
body.capture {{ padding: 0; gap: 0; }}
.shot {{ position: relative; overflow: hidden; background: #061866; color: #fff; flex: none; }}
.decale, .pano, .deco {{ position: absolute; top: 0; }}
.pano {{ left: 0; }}
.fond-accueil {{ position: absolute; left: 0; top: 0; overflow: hidden;
  background: radial-gradient(120% 70% at 30% 20%, #1B3AA8 0%, #061866 55%, #000E38 100%); }}
.logo {{ position: absolute; }}
.ligne {{ position: absolute; left: 0; right: 0; height: {2.5 * k:.1f}px; background: #fff; }}
.soleil {{ position: absolute; transform: translate(-50%, -50%); border-radius: 50%; border: {2 * k:.1f}px solid #FFFF1A; }}
.soleil i {{ position: absolute; inset: 12%; border-radius: 50%; background: #FFFF1A; }}
.accroche {{ position: absolute; transform: translate(-50%, -50%); background: #fff; color: #061866; font-weight: 700;
  text-align: center; line-height: 1.25; padding: {5 * k:.1f}px {6 * k:.1f}px; }}
.el {{ position: absolute; width: 0; height: 0; }}
.el > svg {{ position: absolute; transform: translate(-50%, -50%); }}
.tel-pano {{ position: absolute; left: 0; top: 0; filter: drop-shadow(0 18px 28px rgba(0,0,0,.35)); }}
.textes {{ position: absolute; top: {f["txt"]}px; left: 0; right: 0; padding: 0 30px; text-align: center; }}
h1 {{ font-family: "Bib"; font-weight: 700; font-size: {f["t"]}px; line-height: 1.05; }}
p {{ font-family: "Inter"; font-weight: 700; font-size: {f["st"]}px; line-height: 1.35; margin-top: 12px; }}
.tel {{ position: absolute; left: 50%; top: {f["tel_haut"]}px; height: {f["tel_h"]}px; transform: translateX(-50%); filter: drop-shadow(0 18px 28px rgba(0,0,0,.35)); }}
"""
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{titre_page}</title><style>{css}</style></head><body>{"".join(shots)}</body></html>'


def ecrire(racine, titre_page, accueil, volets):
    for fmt in FORMATS:
        (racine / "scripts" / f"index-{fmt}.html").write_text(page(titre_page, accueil, volets, fmt))
    print(f"scripts/index-*.html écrits : {2 + len(volets)} visuels × 2 formats")
