"""Génère les deux compositions de la vidéo Profil Trucker à partir d'une seule source.

    python3 scripts/generer.py

Écrit index.html (16:9, 1920 × 1080) et compositions/vertical.html (9:16, 1080 × 1920).
Le minutage et les textes sont communs ; seule la mise en page change d'un format à l'autre.
"""

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DUREE = 24

# Visages façon avatars de l'app, avec une casquette de routier.
ROUTIERS = [
    # id, couleur du visage, couleur de la casquette, bouche
    ("r1", "#C9C3F5", "#BFD3F2", "M86 128 Q100 140 114 128"),
    ("r2", "#9FE3D8", "#FFFF1A", "M88 130 L112 130"),
    ("r3", "#F6D38B", "#FFFFFF", "M86 128 Q100 140 114 128"),
]

NOTIFICATIONS = {
    "r1": ("Louna", "vous a envoyé une invitation", None),
    "r2": ("David", "s'est arrêté ici", "Restaurant Chez Marcel, Lyon"),
    "r3": ("Nordin", "a déposé un avis", None),
}


def avatar(visage, casquette, bouche):
    return f"""<svg class="avatar" viewBox="0 0 200 200" aria-hidden="true">
              <circle cx="100" cy="100" r="96" fill="#FFFFFF" />
              <circle cx="100" cy="112" r="70" fill="{visage}" stroke="#061866" stroke-width="5" />
              <path d="M34 92 Q38 34 100 32 Q162 34 166 92 Z" fill="{casquette}" stroke="#061866" stroke-width="5" stroke-linejoin="round" />
              <path d="M30 92 L182 92 Q186 104 172 104 L30 104 Z" fill="#061866" />
              <ellipse cx="80" cy="120" rx="6" ry="9" fill="#061866" />
              <ellipse cx="120" cy="120" rx="6" ry="9" fill="#061866" />
              <path d="{bouche}" fill="none" stroke="#061866" stroke-width="5" stroke-linecap="round" />
            </svg>"""


def routier(rid, visage, casquette, bouche):
    nom, action, detail = NOTIFICATIONS[rid]
    ligne_detail = f'\n                <span class="notif-detail">{detail}</span>' if detail else ""
    return f"""<div id="{rid}" class="routier">
            {avatar(visage, casquette, bouche)}
            <div class="notif">
              <div class="notif-tete">
                <span class="cloche">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a6 6 0 0 0-6 6v4l-2 3h16l-2-3V9a6 6 0 0 0-6-6zm-2 15a2 2 0 0 0 4 0z" fill="#FFFFFF" /></svg>
                </span>
                <span class="notif-app">Truckfly · maintenant</span>
              </div>
              <div class="notif-texte">
                <span><b>{nom}</b> {action}</span>{ligne_detail}
              </div>
            </div>
          </div>"""


CSS_COMMUN = """
      @font-face {
        font-family: "Bib";
        src: url("assets/fonts/BIB-Bold.woff2") format("woff2");
        font-weight: 700;
      }
      @font-face {
        font-family: "Bib";
        src: url("assets/fonts/BIB-Light.woff2") format("woff2");
        font-weight: 300;
      }
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html,
      body {
        width: __W__px;
        height: __H__px;
        overflow: hidden;
        background: #061866;
      }
      #root {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        font-family: "Bib", sans-serif;
      }
      .plein {
        position: absolute;
        inset: 0;
      }
      #fond-couleur {
        position: absolute;
        inset: 0;
        background: #061866;
      }

      /* Intro : des routiers reçoivent des notifications */
      .routier {
        position: absolute;
        display: flex;
        align-items: center;
        gap: 28px;
      }
      .avatar {
        display: block;
        flex: none;
        width: var(--avatar);
        height: var(--avatar);
      }
      .notif {
        width: var(--notif);
        background: #ffffff;
        border-radius: 32px;
        padding: 24px 30px 28px;
        color: #000000;
      }
      .notif-tete {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 10px;
      }
      .cloche {
        display: flex;
        align-items: center;
        justify-content: center;
        width: var(--cloche);
        height: var(--cloche);
        border-radius: 10px;
        background: #061866;
      }
      .cloche svg {
        width: 64%;
        height: 64%;
      }
      .notif-app {
        font-weight: 300;
        font-size: var(--app);
        color: #53565a;
      }
      .notif-texte {
        display: flex;
        flex-direction: column;
        font-weight: 300;
        font-size: var(--message);
        line-height: 1.2;
      }
      .notif-texte b {
        font-weight: 700;
      }
      .notif-detail {
        font-weight: 700;
        color: #061866;
      }

      /* Étapes */
      #textes {
        position: absolute;
      }
      .etape {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        color: #000000;
      }
      .ligne {
        display: block;
        white-space: nowrap;
      }
      .titre {
        font-weight: 700;
        line-height: 1.12;
      }
      .sous {
        font-weight: 300;
        line-height: 1.2;
        margin-top: 16px;
      }
      #t5 {
        align-items: center;
        text-align: center;
        color: #ffffff;
      }
      #t5 .sous {
        white-space: normal;
        text-wrap: balance;
        margin-top: 28px;
      }
      #telephone {
        position: absolute;
      }
      .ecran {
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .cadre {
        position: relative;
        height: 100%;
        aspect-ratio: 460 / 911;
      }
      .cadre img {
        display: block;
        width: 100%;
        height: 100%;
      }
      #repere {
        position: absolute;
        left: 12.6%;
        top: 31.6%;
        width: 74.8%;
        height: 7%;
        border: 6px solid #061866;
        border-radius: 18px;
      }
"""

CSS_16x9 = """
      /* 16:9 : routiers en quinconce, texte à gauche, téléphone à droite */
      #root {
        --avatar: 200px;
        --notif: 700px;
        --cloche: 44px;
        --app: 28px;
        --message: 46px;
      }
      #r1 {
        left: 140px;
        top: 110px;
      }
      #r2 {
        right: 140px;
        top: 400px;
        flex-direction: row-reverse;
      }
      #r3 {
        left: 360px;
        top: 720px;
      }
      #textes {
        left: 130px;
        top: 0;
        bottom: 0;
        width: 1120px;
      }
      .titre {
        font-size: 88px;
      }
      .sous {
        font-size: 56px;
      }
      #t5 {
        left: -130px;
        width: 1920px;
      }
      #t5 .titre {
        font-size: 128px;
      }
      #t5 .sous {
        font-size: 60px;
        max-width: 1500px;
      }
      #telephone {
        right: 110px;
        top: 60px;
        width: 520px;
        height: 880px;
      }
"""

CSS_9x16 = """
      /* 9:16 : routiers empilés, texte en haut, téléphone en dessous */
      #root {
        --avatar: 190px;
        --notif: 730px;
        --cloche: 46px;
        --app: 32px;
        --message: 48px;
      }
      .routier {
        left: 50px;
        right: 50px;
      }
      #r1 {
        top: 360px;
      }
      #r2 {
        top: 880px;
        flex-direction: row-reverse;
      }
      #r3 {
        top: 1400px;
      }
      #textes {
        left: 30px;
        right: 30px;
        top: 250px;
        height: 400px;
      }
      .etape {
        align-items: center;
        text-align: center;
      }
      .titre {
        font-size: 80px;
      }
      .sous {
        font-size: 52px;
      }
      #t5 {
        left: -30px;
        right: -30px;
        top: -250px;
        bottom: auto;
        height: 1920px;
        padding: 0 60px;
      }
      #t5 .titre {
        font-size: 96px;
      }
      #t5 .sous {
        font-size: 56px;
      }
      #telephone {
        left: 0;
        right: 0;
        top: 680px;
        height: 860px;
      }
"""

SCRIPT = """
      const tl = gsap.timeline({ paused: true });
      const entre = { autoAlpha: 1, y: 0, duration: 0.4, ease: "power2.out", stagger: 0.12 };
      const sort = { autoAlpha: 0, y: -24, duration: 0.25, ease: "power2.in" };
      const arrive = { xPercent: 0, autoAlpha: 1, duration: 0.5, ease: "power2.inOut" };
      const part = { xPercent: -30, autoAlpha: 0, duration: 0.5, ease: "power2.inOut", immediateRender: false };

      function texte(id, debut, fin) {
        tl.fromTo(`${id} .ligne`, { autoAlpha: 0, y: 40 }, entre, debut);
        if (fin !== undefined) tl.to(id, sort, fin);
      }

      // Intro (0–6 s) : chaque routier apparaît, puis sa notification glisse
      [["#r1", 0.3], ["#r2", 1.3], ["#r3", 2.3]].forEach(([id, t]) => {
        tl.fromTo(`${id} .avatar`, { autoAlpha: 0, scale: 0.6 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, t);
        tl.fromTo(`${id} .notif`, { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: "power2.out" }, t + 0.25);
      });
      tl.to(".routier", { autoAlpha: 0, y: -30, duration: 0.3, ease: "power2.in", stagger: 0.06 }, 5.5);
      tl.to("#fond-couleur", { backgroundColor: "#F5F3F1", duration: 0.4, ease: "power1.inOut" }, 5.75);

      // Étapes (6–10,2 · 10,2–13,2 · 13,2–15,6 · 15,6–19,2) puis fin (19,2–24)
      texte("#t1", 6.3, 9.95);
      texte("#t2", 10.3, 12.95);
      texte("#t3", 13.3, 15.35);
      texte("#t4", 15.7, 18.9);
      texte("#t5", 19.35);

      // Téléphone : le profil apparaît progressivement
      tl.fromTo("#telephone", { autoAlpha: 0, y: 160 }, { autoAlpha: 1, y: 0, duration: 0.8, ease: "power2.out" }, 6.15);
      // Personnalise et partage : repère sur les deux boutons
      tl.fromTo("#repere", { autoAlpha: 0, scale: 1.08 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "power2.out" }, 10.7);
      tl.to("#repere", { autoAlpha: 0, duration: 0.25 }, 12.95);
      // Retrouve tes amis
      tl.fromTo("#e2", { xPercent: 60, autoAlpha: 0 }, arrive, 13.0);
      tl.fromTo("#e1", { xPercent: 0, autoAlpha: 1 }, part, 13.0);
      // Activité des proches
      tl.fromTo("#e3", { xPercent: 60, autoAlpha: 0 }, arrive, 15.4);
      tl.fromTo("#e2", { xPercent: 0, autoAlpha: 1 }, { ...part, immediateRender: false }, 15.4);
      tl.to("#telephone", { autoAlpha: 0, y: 80, duration: 0.3, ease: "power2.in" }, 18.9);

      // Fin : retour au fond bleu
      tl.to("#fond-couleur", { backgroundColor: "#061866", duration: 0.4, ease: "power1.inOut" }, 18.95);

      window.__timelines["__ID__"] = tl;
      tl.seek(0);
"""


def page(cid, w, h, css_format):
    routiers = "\n          ".join(routier(*r) for r in ROUTIERS)
    css = (CSS_COMMUN + css_format).replace("__W__", str(w)).replace("__H__", str(h))
    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={w}, height={h}" />
    <!-- Généré par scripts/generer.py : modifier le générateur, pas ce fichier. -->
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{css}    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="{cid}"
      data-start="0"
      data-duration="{DUREE}"
      data-width="{w}"
      data-height="{h}"
    >
      <div id="fond" class="plein clip" data-start="0" data-duration="{DUREE}" data-track-index="0">
        <div id="fond-couleur"></div>
      </div>

      <div id="intro" class="plein clip" data-start="0" data-duration="6" data-track-index="1">
        <div id="routiers" class="plein">
          {routiers}
        </div>
      </div>

      <div id="ecrans" class="plein clip" data-start="6" data-duration="13.2" data-track-index="2">
        <div id="telephone">
          <div id="e1" class="ecran">
            <div class="cadre">
              <img src="assets/ecrans/v2-profil.png" alt="" />
              <div id="repere"></div>
            </div>
          </div>
          <div id="e2" class="ecran">
            <div class="cadre"><img src="assets/ecrans/v2-trouver-routiers.png" alt="" /></div>
          </div>
          <div id="e3" class="ecran">
            <div class="cadre"><img src="assets/ecrans/v2-fil-activite.png" alt="" /></div>
          </div>
        </div>
      </div>

      <div id="textes-clip" class="plein clip" data-start="6" data-duration="{DUREE - 6}" data-track-index="3">
        <div id="textes">
          <div id="t1" class="etape">
            <span class="ligne titre">Crée ton Profil Trucker</span>
            <span class="ligne sous">pour que tes amis te retrouvent&nbsp;!</span>
          </div>
          <div id="t2" class="etape">
            <span class="ligne titre">Personnalise</span>
            <span class="ligne titre">et partage ton profil</span>
          </div>
          <div id="t3" class="etape">
            <span class="ligne titre">Retrouve tes amis</span>
          </div>
          <div id="t4" class="etape">
            <span class="ligne titre">Suis l'activité de</span>
            <span class="ligne titre">tes proches au quotidien</span>
          </div>
          <div id="t5" class="etape" data-layout-allow-overflow>
            <span class="ligne titre">Ne roule plus seul&nbsp;!</span>
            <span class="ligne sous">Rejoins la communauté sur Michelin Truckfly</span>
          </div>
        </div>
      </div>
    </div>
    <script>{SCRIPT.replace("__ID__", cid)}    </script>
  </body>
</html>
"""


(RACINE / "index.html").write_text(page("main", 1920, 1080, CSS_16x9))
(RACINE / "compositions" / "vertical.html").write_text(page("vertical", 1080, 1920, CSS_9x16))
print("index.html et compositions/vertical.html générés")
