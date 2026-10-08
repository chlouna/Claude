"""Interstitielle vidéo de 15 s « Profil Trucker + Social Core », en 7 langues.

    python3 interstitiels/video-15s/generer.py

Écrit une page par langue (fr.html, en.html, de.html, nl.html, pl.html, it.html, es.html),
au format téléphone 390 × 844. rendre.mjs en tire un MP4 par langue (1080 × 2338, 30 i/s).
Toutes les animations sont en CSS avec des délais absolus : la page entière est une timeline
de 15 s, que le rendu avance image par image.

0–3 s titre · 3–6 s photo, bio · 6–9 s camion · 9–12 s amis, activité · 12–15 s fin.
Les délais sont écrits sur l'ancienne base de 10 s et multipliés par RYTHME (1,5) : tout dure
50 % plus longtemps, pour laisser le temps de lire.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from generer import avatar, PORTRAIT, CAMION, PIN  # noqa: E402  (briques visuelles des interstitiels)

ICI = Path(__file__).resolve().parent
RYTHME = 1.5  # étire la timeline de 10 s à 15 s

TEXTES = {
    "fr": dict(
        titre="Ton profil évolue et devient encore plus communautaire",
        photo="Ajoute ta photo", bio="Personnalise ta bio", camion="Ajoute ton camion",
        amis="Retrouve tes amis", activite="Découvre leur activité au quotidien",
        fin="Ne roule plus seul&nbsp;!", sous="Crée ton Profil Trucker sur Michelin Truckfly", cta="Créer mon profil",
        texte_bio="Conducteur routier | Toujours sur la route | À la recherche des meilleurs spots&nbsp;!",
        membre="Membre depuis 2026", surnom="Le Bolide", dims=("Hauteur", "Largeur", "Longueur"), sep=",",
        invitation="Louna vous a envoyé une invitation", accepter="Accepter",
        visite="Nicolas J. a visité&nbsp;:", arret="David s’est arrêté ici&nbsp;:", instant="à l’instant",
    ),
    "en": dict(
        titre="Your profile is evolving and becoming even more community-driven",
        photo="Add your photo", bio="Personalise your bio", camion="Add your truck",
        amis="Find your friends", activite="See what they’re up to every day",
        fin="Never drive alone again!", sous="Create your Trucker Profile on Michelin Truckfly", cta="Create my profile",
        texte_bio="Truck driver | Always on the road | Looking for the best spots!",
        membre="Member since 2026", surnom="The Rocket", dims=("Height", "Width", "Length"), sep=".",
        invitation="Louna sent you an invitation", accepter="Accept",
        visite="Nicolas J. visited:", arret="David stopped here:", instant="just now",
    ),
    "de": dict(
        titre="Dein Profil entwickelt sich weiter und wird noch gemeinschaftlicher",
        photo="Füge dein Foto hinzu", bio="Personalisiere deine Bio", camion="Füge deinen Lkw hinzu",
        amis="Finde deine Freunde", activite="Entdecke täglich, was sie machen",
        fin="Fahr nie mehr allein!", sous="Erstelle dein Trucker-Profil auf Michelin Truckfly", cta="Mein Profil erstellen",
        texte_bio="Lkw-Fahrer | Immer auf der Straße | Auf der Suche nach den besten Spots!",
        membre="Mitglied seit 2026", surnom="Der Blitz", dims=("Höhe", "Breite", "Länge"), sep=",",
        invitation="Louna hat dir eine Einladung geschickt", accepter="Annehmen",
        visite="Nicolas J. hat besucht:", arret="David hat hier angehalten:", instant="gerade eben",
    ),
    "nl": dict(
        titre="Je profiel evolueert en wordt nog meer community-gericht",
        photo="Voeg je foto toe", bio="Personaliseer je bio", camion="Voeg je truck toe",
        amis="Vind je vrienden", activite="Ontdek elke dag wat ze doen",
        fin="Rij nooit meer alleen!", sous="Maak je Truckerprofiel aan op Michelin Truckfly", cta="Mijn profiel aanmaken",
        texte_bio="Vrachtwagenchauffeur | Altijd onderweg | Op zoek naar de beste plekken!",
        membre="Lid sinds 2026", surnom="De Bliksem", dims=("Hoogte", "Breedte", "Lengte"), sep=",",
        invitation="Louna heeft je een uitnodiging gestuurd", accepter="Accepteren",
        visite="Nicolas J. heeft bezocht:", arret="David is hier gestopt:", instant="zojuist",
    ),
    "pl": dict(
        titre="Twój profil się zmienia i staje się jeszcze bardziej społecznościowy",
        photo="Dodaj swoje zdjęcie", bio="Spersonalizuj swój opis", camion="Dodaj swoją ciężarówkę",
        amis="Znajdź znajomych", activite="Odkrywaj ich codzienną aktywność",
        fin="Nie jeźdź już sam!", sous="Utwórz swój Profil Truckera w Michelin Truckfly", cta="Utwórz mój profil",
        texte_bio="Kierowca ciężarówki | Zawsze w trasie | W poszukiwaniu najlepszych miejsc!",
        membre="Członek od 2026", surnom="Błyskawica", dims=("Wysokość", "Szerokość", "Długość"), sep=",",
        invitation="Louna wysłała ci zaproszenie", accepter="Akceptuj",
        visite="Nicolas J. odwiedził:", arret="David zatrzymał się tutaj:", instant="przed chwilą",
    ),
    "it": dict(
        titre="Il tuo profilo si evolve e diventa ancora più orientato alla community",
        photo="Aggiungi la tua foto", bio="Personalizza la tua bio", camion="Aggiungi il tuo camion",
        amis="Ritrova i tuoi amici", activite="Scopri la loro attività ogni giorno",
        fin="Non viaggiare più da solo!", sous="Crea il tuo Profilo Trucker su Michelin Truckfly", cta="Crea il mio profilo",
        texte_bio="Camionista | Sempre in viaggio | Alla ricerca dei posti migliori!",
        membre="Membro dal 2026", surnom="Il Fulmine", dims=("Altezza", "Larghezza", "Lunghezza"), sep=",",
        invitation="Louna ti ha inviato un invito", accepter="Accetta",
        visite="Nicolas J. ha visitato:", arret="David si è fermato qui:", instant="adesso",
    ),
    "es": dict(
        titre="Tu perfil evoluciona y se vuelve aún más comunitario",
        photo="Añade tu foto", bio="Personaliza tu bio", camion="Añade tu camión",
        amis="Encuentra a tus amigos", activite="Descubre su actividad cada día",
        fin="¡No vuelvas a conducir solo!", sous="Crea tu Perfil Trucker en Michelin Truckfly", cta="Crear mi perfil",
        texte_bio="Camionero | Siempre en la carretera | ¡Buscando los mejores sitios!",
        membre="Miembro desde 2026", surnom="El Rayo", dims=("Altura", "Anchura", "Longitud"), sep=",",
        invitation="Louna te ha enviado una invitación", accepter="Aceptar",
        visite="Nicolas J. ha visitado:", arret="David ha parado aquí:", instant="ahora mismo",
    ),
}

VALEURS = ("4{s}00 m", "2{s}55 m", "16{s}50 m")


def anim(*parts):
    """style="animation: ..." à partir de (nom, durée, délai[, remplissage])."""
    return "animation: " + ", ".join(
        f"{n} {round(d * (1.6 if n == 'balaye' else 1.2), 3)}s {'cubic-bezier(0.2, 0.9, 0.3, 1.15)' if n in ('entre', 'pop') else 'ease'} {round(t * RYTHME, 3)}s {f}"
        for n, d, t, *r in parts
        for f in [r[0] if r else ("both" if n in ("entre", "pop", "balaye") else "forwards")]
    )


def carte(av, haut, fort, bas, d_in, extra=""):
    l_haut = f'<span class="gris">{haut}</span>' if haut else ""
    return f"""<div class="carte" style="{anim(('entre', 0.45, d_in), ('fondu', 0.3, 7.9))}">
          {av}<div class="c-txt">{l_haut}<span class="fort">{fort}</span><span class="gris">{bas}</span></div>{extra}
        </div>"""


def legende(texte, d_in, d_out):
    return f'<p class="legende" style="{anim(("entre", 0.4, d_in), ("sort", 0.3, d_out))}">{texte}</p>'


def page(lang, t):
    dims = "".join(
        f'<div class="dim" style="{anim(("pop", 0.35, 4.75 + 0.2 * i))}"><span>{nom}</span><b>{VALEURS[i].format(s=t["sep"])}</b></div>'
        for i, nom in enumerate(t["dims"])
    )
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=390, height=844" />
<title>Interstitielle Profil Trucker 15 s ({lang})</title>
<style>{CSS}</style>
</head>
<body>
<main class="ecran">
  <!-- 0–3 s : titre -->
  <div class="ouverture" style="{anim(('sort', 0.35, 1.75))}">
    <h1 class="titre" style="{anim(('entre', 0.5, 0.15))}">{t["titre"]}</h1>
  </div>

  <!-- Légendes des scènes -->
  <div class="legendes">
    {legende(t["photo"], 2.05, 2.95)}
    {legende(t["bio"], 3.0, 3.95)}
    {legende(t["camion"], 4.05, 5.95)}
    {legende(t["amis"], 6.05, 6.95)}
    {legende(t["activite"], 7.0, 7.85)}
  </div>

  <!-- 3–9 s : le Profil Trucker se construit -->
  <div class="profil" style="{anim(('entre', 0.45, 1.95), ('monte', 0.5, 6.0), ('fondu', 0.3, 7.9))}">
    <div class="p-haut">
      <div class="p-photo vide"></div>
      <div class="p-photo" style="{anim(('pop', 0.4, 2.3))}">{PORTRAIT}</div>
      <div class="p-nom"><b>Charlie G. <span class="fr"><i></i><i></i><i></i></span></b><span>{t["membre"]}</span></div>
    </div>
    <div class="p-bio">
      <div class="barres" style="{anim(('fondu', 0.2, 3.05))}"><i></i><i></i></div>
      <p style="{anim(('balaye', 0.75, 3.1))}">{t["texte_bio"]}</p>
    </div>
    <div class="p-camion">
      <div class="camion-vide" style="{anim(('fondu', 0.2, 4.2))}">+</div>
      <div class="camion" style="{anim(('entre', 0.45, 4.25))}">
        <div class="carre">{CAMION}</div>
        <div class="camion-txt"><b>{t["surnom"]}</b><div class="dims">{dims}</div></div>
      </div>
    </div>
  </div>

  <!-- 9–12 s : les amis et leur activité -->
  <div class="amis">
    {carte(avatar("louna", "invitation", "av-m"), None, t["invitation"], t["instant"], 6.2, f'<span class="btn">{t["accepter"]}</span>')}
    {carte(avatar("nicolas", "visite", "av-m"), t["visite"], "AS 24", t["instant"], 7.0)}
    {carte(avatar("david", "visite", "av-m"), t["arret"], "Le Relais des Cigales", t["instant"], 7.3)}
  </div>

  <!-- 12–15 s : écran final -->
  <div class="final">
    <h2 style="{anim(('entre', 0.5, 8.15))}">{t["fin"]}</h2>
    <p style="{anim(('entre', 0.45, 8.4))}">{t["sous"]}</p>
    <a class="cta" style="{anim(('pop', 0.45, 8.7), ('pouls', 0.6, 9.3, 'both'))}">{t["cta"]}</a>
    </div>
</main>
</body>
</html>
"""


CSS = """
@font-face { font-family: "Bib"; src: url("../assets/fonts/BIB-Bold.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Bib"; src: url("../assets/fonts/BIB-Light.woff2") format("woff2"); font-weight: 300; }
@font-face { font-family: "Inter"; src: url("../assets/fonts/Inter-Regular.otf") format("opentype"); font-weight: 400; }
@font-face { font-family: "Inter"; src: url("../assets/fonts/Inter-SemiBold.otf") format("opentype"); font-weight: 600; }
@font-face { font-family: "Inter"; src: url("../assets/fonts/Inter-Bold.otf") format("opentype"); font-weight: 700; }
:root { --bleu: #061866; --jaune: #ffff1a; --gris: #6e6e73; --bleu-clair: #dce6f7; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 390px; height: 844px; overflow: hidden; background: var(--bleu); }
body { font-family: "Inter", "Noto Color Emoji", sans-serif; }
.ecran {
  position: relative; width: 390px; height: 844px; overflow: hidden;
  background: radial-gradient(120% 70% at 50% 10%, #10287f 0%, var(--bleu) 52%, #000e38 100%);
}
.ecran > * { position: absolute; }

/* Ouverture */
.ouverture { left: 24px; right: 24px; top: 0; bottom: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 30px; text-align: center; }
.titre { font-family: "Bib", sans-serif; font-weight: 700; font-size: 34px; line-height: 1.15; color: #fff; text-wrap: balance; }

/* Légendes */
.legendes { left: 22px; right: 22px; top: 52px; height: 110px; }
.legende {
  position: absolute; left: 0; right: 0; top: 0; height: 110px; display: flex; align-items: center; justify-content: center;
  text-align: center; font-family: "Bib", "Noto Color Emoji", sans-serif; font-weight: 700; font-size: 30px; line-height: 1.12; color: #fff; text-wrap: balance;
}

/* Profil Trucker */
.profil {
  left: 24px; right: 24px; top: 190px; background: #fff; border-radius: 22px; padding: 18px;
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.28); transform-origin: 50% 0;
}
.p-haut { position: relative; display: flex; align-items: center; gap: 14px; height: 80px; }
.p-photo { position: absolute; left: 0; top: 2px; width: 76px; height: 76px; border-radius: 50%; overflow: hidden; border: 3px solid var(--bleu); }
.p-photo.vide { border: 2.5px dashed #8e9bb8; background: #eef2f9; }
.illu { display: block; width: 100%; height: 100%; }
.p-nom { margin-left: 90px; display: flex; flex-direction: column; gap: 3px; }
.p-nom b { font-size: 22px; display: flex; align-items: center; gap: 7px; }
.p-nom > span { color: var(--gris); font-size: 13px; }
.fr { display: inline-flex; width: 20px; height: 13px; border-radius: 2px; overflow: hidden; }
.fr i { flex: 1; } .fr i:nth-child(1) { background: #002395; } .fr i:nth-child(2) { background: #fff; outline: 1px solid #eee; } .fr i:nth-child(3) { background: #ed2939; }
.p-bio { position: relative; margin-top: 12px; min-height: 56px; }
.p-bio p { font-size: 14px; line-height: 1.4; color: #3a3a3c; }
.barres { position: absolute; inset: 4px 0 0; display: flex; flex-direction: column; gap: 10px; }
.barres i { display: block; height: 12px; border-radius: 6px; background: #e3e6ec; }
.barres i:last-child { width: 62%; }
.p-camion { position: relative; margin-top: 12px; height: 104px; }
.camion-vide { position: absolute; inset: 0; border: 2.5px dashed #8e9bb8; background: #eef2f9; border-radius: 16px; display: flex; align-items: center; justify-content: center; color: var(--bleu); font-size: 34px; font-weight: 700; }
.camion { position: absolute; inset: 0; display: flex; align-items: center; gap: 12px; padding: 10px; border-radius: 16px; background: #f5f3f1; }
.carre { width: 84px; height: 84px; border-radius: 12px; overflow: hidden; flex: none; background: var(--bleu-clair); }
.camion-txt { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px; }
.camion-txt b { font-family: "Bib", sans-serif; font-size: 20px; }
.dims { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; }
.dim { background: #fff; border: 1.5px solid #d6dae2; border-radius: 9px; padding: 4px 4px; display: flex; flex-direction: column; min-width: 0; }
.dim span { color: var(--gris); font-size: 9px; letter-spacing: -0.2px; white-space: nowrap; }
.dim b { font-size: 13px; white-space: nowrap; }

/* Amis */
.amis { left: 22px; right: 22px; top: 476px; display: flex; flex-direction: column; gap: 10px; }
.carte { display: flex; align-items: center; gap: 12px; background: #fff; border-radius: 16px; padding: 11px 13px; box-shadow: 0 8px 22px rgba(0, 0, 0, 0.22); }
.av-m { width: 50px; height: 50px; flex: none; }
.c-txt { display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0; }
.gris { color: var(--gris); font-size: 12.5px; }
.fort { font-weight: 700; font-size: 14.5px; line-height: 1.25; }
.btn { flex: none; padding: 7px 11px; border-radius: 10px; background: var(--bleu); color: #fff; font-weight: 700; font-size: 12.5px; }

/* Final */
.final { left: 26px; right: 26px; top: 0; bottom: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.final h2 { font-family: "Bib", sans-serif; font-weight: 700; font-size: 44px; line-height: 1.08; color: #fff; text-wrap: balance; }
.final p { margin-top: 16px; font-size: 19px; line-height: 1.4; color: rgba(255, 255, 255, 0.9); text-wrap: balance; }
.cta { margin-top: 30px; width: 100%; height: 58px; border-radius: 14px; background: var(--jaune); color: #000; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; }

/* Animations : délais absolus, la page est une timeline de 10 s × RYTHME */
@keyframes entre { from { opacity: 0; transform: translateY(18px) scale(0.96); } }
@keyframes pop { from { opacity: 0; transform: scale(0.4); } }
@keyframes sort { to { opacity: 0; transform: translateY(-14px); } }
@keyframes fondu { to { opacity: 0; } }
@keyframes balaye { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }
@keyframes monte { to { transform: translateY(-14px) scale(0.84); } }
@keyframes pouls { 50% { transform: scale(1.04); } }
"""

for lang, t in TEXTES.items():
    (ICI / f"{lang}.html").write_text(page(lang, t))
print(len(TEXTES), "pages générées :", ", ".join(TEXTES))
