"""Génère les deux compositions de la vidéo Profil Trucker à partir d'une seule source.

    python3 scripts/generer.py

Écrit index.html (16:9, 1920 × 1080) et compositions/vertical.html (9:16, 1080 × 1920).
Le minutage, les textes et les interactions sont communs ; seule la mise en page change.

Polices : Bib (charte) pour les titres, Inter pour tout ce qui imite l'app (notifications,
cartes, boutons). Inter remplace la police système de l'iPhone, qu'on ne peut pas embarquer.
Les positions sur les écrans sont en % de la capture rognée.
"""

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DUREE = 34.5

# --- Avatars façon app (référence : Abdelatif) : visage de couleur, anneau, yeux, initiale ---

YEUX = {
    "points": '<ellipse cx="40" cy="44" rx="4.5" ry="7" fill="#061866" /><ellipse cx="60" cy="44" rx="4.5" ry="7" fill="#061866" />',
    "plisses": '<path d="M33 38 L42 44 L33 50 M67 38 L58 44 L67 50" fill="none" stroke="#061866" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />',
}

BADGES = {
    "invitation": '<circle cx="10" cy="9" r="4" fill="#061866" /><path d="M3 21 Q3 14 10 14 Q17 14 17 21 Z" fill="#061866" /><path d="M20 8 V16 M16 12 H24" stroke="#061866" stroke-width="2.6" stroke-linecap="round" />',
    "visite": '<rect x="2" y="7" width="13" height="10" rx="2" fill="#061866" /><path d="M15 10 H20 L23 14 V17 H15 Z" fill="#061866" /><circle cx="7" cy="19" r="2.4" fill="#061866" /><circle cx="19" cy="19" r="2.4" fill="#061866" />',
    "avis": '<path d="M3 5 H21 Q23 5 23 7 V16 Q23 18 21 18 H11 L6 22 V18 H5 Q3 18 3 16 V7 Q3 5 5 5 Z" fill="#061866" />',
    "ami": '<circle cx="13" cy="8" r="5" fill="#061866" /><path d="M3 24 Q3 15 13 15 Q23 15 23 24 Z" fill="#061866" />',
}

PERSONNES = {
    # initiale, visage, anneau, yeux
    "louna": ("L", "#C9C3F5", "#FFFF1A", "points"),
    "nicolas": ("N", "#A6E8B8", "#061866", "points"),
    "david": ("D", "#F6D38B", "#FFFF1A", "plisses"),
    "vanessa": ("V", "#BFD3F2", "#061866", "points"),
}


def avatar(qui, badge):
    lettre, visage, anneau, yeux = PERSONNES[qui]
    return f"""<svg class="avatar" viewBox="0 0 112 112" aria-hidden="true">
                <circle cx="50" cy="50" r="44" fill="{visage}" stroke="{anneau}" stroke-width="8" />
                {YEUX[yeux]}
                <text x="50" y="72" text-anchor="middle" font-family="Inter" font-weight="600" font-size="20" fill="#061866">{lettre}</text>
                <circle cx="88" cy="88" r="20" fill="#DCE6F7" stroke="#FFFFFF" stroke-width="4" />
                <svg x="75" y="75" width="26" height="26" viewBox="0 0 26 26">{BADGES[badge]}</svg>
              </svg>"""


PIN = '<svg class="pin" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z" fill="#6E6E73" /></svg>'


def carte(cid, av, haut, fort, bas, lieu=None, extra="", classe=""):
    """Carte au style du fil d'activité (référence : « Nicolas J. a visité : »)."""
    ligne_haut = f'<span class="c-gris">{haut}</span>' if haut else ""
    ligne_lieu = f'<span class="c-lieu">{PIN}{lieu}</span>' if lieu else ""
    return f"""<div id="{cid}" class="carte-app {classe}">
              {av}
              <div class="c-textes">
                {ligne_haut}
                <span class="c-fort">{fort}</span>
                <span class="c-bas"><span class="c-gris">{bas}</span>{ligne_lieu}</span>
              </div>{extra}
            </div>"""


def rangee(rid, qui, badge, carte_html, inverse=False):
    """Intro : grand avatar façon app à côté de sa notification, en quinconce."""
    grand = avatar(qui, badge).replace('class="avatar"', 'class="avatar-grand"', 1)
    # halo blanc derrière l'anneau, pour qu'il se détache du fond bleu
    grand = grand.replace('<circle cx="50" cy="50" r="44"', '<circle cx="50" cy="50" r="53" fill="#FFFFFF" />\n                <circle cx="50" cy="50" r="44"', 1)
    sens = " inverse" if inverse else ""
    return f"""<div id="{rid}" class="rangee{sens}">
            {grand}
            {carte_html}
          </div>"""


BOUTON_ACCEPTER = """
              <div class="c-bouton">
                <span id="btn-accepter">Accepter</span>
                <span id="btn-amis">✓ Amis</span>
                <div id="tap-accepter" class="tap" style="left: 50%; top: 50%"><div class="onde"></div><div class="doigt"></div></div>
              </div>"""

NOTIFS_INTRO = "\n          ".join(
    [
        rangee("r1", "nicolas", "visite", carte("n1", "", "Nicolas J. a visité :", "AS 24", "à l'instant", classe="notif")),
        rangee("r2", "david", "avis", carte("n2", "", "David a déposé un avis chez :", "Le Relais des Cigales", "à l'instant", classe="notif"), inverse=True),
        rangee("r3", "louna", "invitation", carte("n3", "", None, "Louna vous a envoyé une invitation", "à l'instant", extra=BOUTON_ACCEPTER, classe="notif")),
    ]
)

TELECHARGER = '<svg class="dl" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 V15 M6.5 10 L12 15.5 L17.5 10 M4 20.5 H20" fill="none" stroke="#061866" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" /></svg>'

HORLOGE = '<svg class="horloge" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5" fill="none" stroke="#061866" stroke-width="2.6" /><path class="aiguille" d="M12 12 V6.5" stroke="#061866" stroke-width="2.6" stroke-linecap="round" /><path d="M12 12 L15.5 14" stroke="#061866" stroke-width="2.6" stroke-linecap="round" /></svg>'

# Ligne « Louna C. » recréée par-dessus la première invitation en attente (capture v3-invitations)
LIGNE_LOUNA = f"""<div id="ligne-louna">
                {avatar("louna", "invitation").replace('class="avatar"', 'class="avatar-ligne"', 1)}
                <span>Louna C.</span>
              </div>"""

# Anneaux verts autour des amis « On the road » (capture v3-accueil-en-ligne)
ANNEAUX = "\n              ".join(
    f'<div class="anneau" style="left: {x}%; top: 27.2%"></div>' for x in (16.7, 35.7, 54.3, 73.3)
)


def tap(tid, x, y):
    return f'<div id="{tid}" class="tap" style="left: {x}%; top: {y}%"><div class="onde"></div><div class="doigt"></div></div>'


def fleche(fid, x, y, cote):
    """Flèche courbe dont la pointe tombe sur (x %, y %) de l'écran, venant de la gauche ou de la droite."""
    if cote == "gauche":
        trace, tete, decal = "M8 10 C 80 6, 150 40, 178 104", "M160 98 L180 108 L182 86", -186
    else:
        trace, tete, decal = "M192 10 C 120 6, 50 40, 22 104", "M40 98 L20 108 L18 86", -14
    return f"""<svg id="{fid}" class="fleche" viewBox="0 0 200 120" style="left: calc({x}% + {decal}px); top: calc({y}% - 112px)" aria-hidden="true">
                <path class="trait" d="{trace}" pathLength="1" />
                <path class="tete" d="{tete}" />
              </svg>"""


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
      @font-face {
        font-family: "Inter";
        src: url("assets/fonts/Inter-Regular.otf") format("opentype");
        font-weight: 400;
      }
      @font-face {
        font-family: "Inter";
        src: url("assets/fonts/Inter-SemiBold.otf") format("opentype");
        font-weight: 600;
      }
      @font-face {
        font-family: "Inter";
        src: url("assets/fonts/Inter-Bold.otf") format("opentype");
        font-weight: 700;
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

      /* Cartes au style de l'app (Inter) */
      .carte-app {
        display: flex;
        align-items: center;
        gap: var(--c-gap);
        background: #ffffff;
        border-radius: var(--c-rayon);
        padding: var(--c-pad);
        font-family: "Inter", sans-serif;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
      }
      .carte-app .avatar {
        flex: none;
        width: var(--c-avatar);
        height: var(--c-avatar);
      }
      .c-textes {
        flex: 1;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: var(--c-interligne);
      }
      .c-gris {
        color: #6e6e73;
        font-weight: 400;
        font-size: var(--c-petit);
      }
      .c-fort {
        color: #000000;
        font-weight: 700;
        font-size: var(--c-grand);
        line-height: 1.2;
      }
      .c-bas {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.6em;
      }
      .c-lieu {
        display: flex;
        align-items: center;
        gap: 0.2em;
        color: #6e6e73;
        font-size: var(--c-petit);
        white-space: nowrap;
      }
      .pin {
        width: 1em;
        height: 1em;
      }
      .c-bouton {
        position: relative;
        flex: none;
        display: grid;
        font-weight: 700;
        font-size: var(--c-petit);
      }
      .c-bouton > span {
        grid-area: 1 / 1;
        padding: 0.45em 0.9em;
        border-radius: 0.5em;
        text-align: center;
      }
      #btn-accepter {
        background: #061866;
        color: #ffffff;
      }
      #btn-amis {
        background: #e4edfb;
        color: #061866;
      }

      /* Intro : avatars et notifications en quinconce */
      .rangee {
        position: absolute;
        display: flex;
        align-items: center;
        gap: var(--r-gap);
      }
      .rangee.inverse {
        flex-direction: row-reverse;
      }
      .avatar-grand {
        display: block;
        overflow: visible;
        flex: none;
        width: var(--a-grand);
        height: var(--a-grand);
      }
      .notif {
        position: relative;
        flex: 1;
      }
      .notif-tel {
        position: absolute;
      }

      /* Textes */
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
      .final {
        align-items: center;
        text-align: center;
        color: #ffffff;
      }
      .final .sous {
        white-space: normal;
        text-wrap: balance;
        margin-top: 28px;
      }

      /* Téléphone et interactions */
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
        container-type: size;
      }
      .cadre > img {
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
      .tap {
        position: absolute;
        width: 76px;
        height: 76px;
        margin: -38px 0 0 -38px;
      }
      .tap > div {
        position: absolute;
        inset: 0;
        border-radius: 50%;
        visibility: hidden;
        opacity: 0;
      }
      .doigt {
        background: rgba(255, 255, 255, 0.55);
        border: 5px solid #061866;
      }
      .onde {
        border: 5px solid #061866;
      }
      .fleche {
        position: absolute;
        width: 200px;
        height: 120px;
        overflow: visible;
      }
      .fleche path {
        fill: none;
        stroke: #061866;
        stroke-width: 7;
        stroke-linecap: round;
        stroke-linejoin: round;
      }
      .fleche .trait {
        stroke-dasharray: 1;
      }
      #attente {
        position: absolute;
        left: 61.9%;
        top: 33.4%;
        width: 27.6%;
        height: 4.1%;
        border-radius: 1cqh;
        background: #ffffff;
        border: 0.25cqh solid #061866;
        color: #061866;
        font-family: "Inter", sans-serif;
        font-weight: 700;
        font-size: 1.6cqh;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.6cqh;
      }
      .horloge {
        width: 1.9cqh;
        height: 1.9cqh;
      }
      #ligne-louna {
        position: absolute;
        left: 7.2%;
        top: 27.7%;
        width: 44%;
        height: 7.7%;
        background: #d4e7fa;
        display: flex;
        align-items: center;
        gap: 1.4cqh;
        padding-left: 3.5cqh;
        font-family: "Inter", sans-serif;
        font-weight: 700;
        font-size: 2.1cqh;
        color: #000000;
      }
      .avatar-ligne {
        width: 5.6cqh;
        height: 5.6cqh;
        flex: none;
      }
      #ami-ok {
        position: absolute;
        left: 51.5%;
        top: 28.4%;
        width: 39%;
        height: 6.4%;
        background: #d4e7fa;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      #ami-ok span {
        padding: 0.7cqh 2cqh;
        border-radius: 1cqh;
        background: #061866;
        color: #ffffff;
        font-family: "Inter", sans-serif;
        font-weight: 700;
        font-size: 1.9cqh;
      }
      #cadre-en-ligne {
        position: absolute;
        left: 23.5%;
        top: 13.3%;
        width: 31.5%;
        height: 4.6%;
        border-radius: 2.3cqh;
        border: 0.45cqh solid #34c759;
      }
      .cta {
        display: flex;
        align-items: center;
        gap: 0.5em;
        margin-top: var(--cta-marge);
        padding: 0.55em 1.2em;
        border-radius: 999px;
        background: #ffffff;
        color: #061866;
        font-family: "Bib", sans-serif;
        font-weight: 700;
        font-size: var(--cta-taille);
      }
      .dl {
        width: 1.1em;
        height: 1.1em;
      }
      .anneau {
        position: absolute;
        width: 16.5%;
        aspect-ratio: 1;
        margin: -8.25% 0 0 -8.25%;
        border-radius: 50%;
        border: 0.55cqh solid #34c759;
      }
"""

CSS_16x9 = """
      /* 16:9 : notifications en quinconce ; puis texte à gauche, téléphone à droite */
      #root {
        --c-gap: 26px;
        --c-rayon: 28px;
        --c-pad: 24px 32px;
        --c-avatar: 112px;
        --c-interligne: 6px;
        --c-petit: 30px;
        --c-grand: 36px;
      }
      #root {
        --a-grand: 170px;
        --cta-taille: 56px;
        --cta-marge: 48px;
        --r-gap: 28px;
      }
      .rangee {
        width: 1040px;
      }
      #r1 {
        left: 150px;
        top: 150px;
      }
      #r2 {
        right: 150px;
        top: 410px;
      }
      #r3 {
        left: 330px;
        top: 680px;
      }
      .notif-tel {
        right: 50px;
        top: 790px;
        width: 720px;
      }
      #textes {
        left: 130px;
        top: 0;
        bottom: 0;
        width: 1000px;
      }
      .titre {
        font-size: 88px;
      }
      .final {
        left: -130px;
        width: 1920px;
      }
      .final .titre {
        font-size: 128px;
      }
      .final .sous {
        font-size: 60px;
        max-width: 1500px;
      }
      #telephone {
        right: 210px;
        top: 60px;
        width: 520px;
        height: 880px;
      }
      .final .titre-rappel {
        font-size: 96px;
      }
"""

CSS_9x16 = """
      /* 9:16 : notifications en quinconce ; puis texte en haut, téléphone en dessous */
      #root {
        --c-gap: 30px;
        --c-rayon: 32px;
        --c-pad: 30px 36px;
        --c-avatar: 136px;
        --c-interligne: 8px;
        --c-petit: 40px;
        --c-grand: 48px;
      }
      #root {
        --a-grand: 190px;
        --cta-taille: 46px;
        --cta-marge: 56px;
        --r-gap: 26px;
      }
      .rangee,
      .notif-tel {
        left: 50px;
        right: 50px;
      }
      #r1 {
        top: 380px;
      }
      #r2 {
        top: 830px;
      }
      #r3 {
        top: 1280px;
      }
      .notif-tel {
        top: 1390px;
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
      .final {
        left: -30px;
        right: -30px;
        top: -250px;
        bottom: auto;
        height: 1920px;
        padding: 0 60px;
      }
      .final .titre {
        font-size: 96px;
      }
      .final .sous {
        font-size: 56px;
      }
      #telephone {
        left: 0;
        right: 0;
        top: 680px;
        height: 860px;
      }
      .final .titre-rappel {
        font-size: 88px;
        white-space: normal;
        text-wrap: balance;
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
      // Tap : le doigt se pose, une onde part, le doigt se lève
      function tape(id, t) {
        tl.fromTo(`${id} .doigt`, { autoAlpha: 0, scale: 1.5 }, { autoAlpha: 1, scale: 1, duration: 0.18, ease: "power2.out" }, t);
        tl.fromTo(`${id} .onde`, { autoAlpha: 0.9, scale: 0.7 }, { autoAlpha: 0, scale: 2.3, duration: 0.55, ease: "power2.out", immediateRender: false }, t + 0.15);
        tl.to(`${id} .doigt`, { autoAlpha: 0, scale: 0.8, duration: 0.2, ease: "power2.in", immediateRender: false }, t + 0.45);
      }
      // Flèche : le trait se dessine, puis la pointe apparaît
      function fleche(id, t, fin) {
        tl.fromTo(`${id} .trait`, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.45, ease: "power2.out" }, t);
        tl.fromTo(`${id} .tete`, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.15 }, t + 0.38);
        tl.to(id, { autoAlpha: 0, duration: 0.25 }, fin);
      }


      // Intro (0–6 s) : les notifications des amis arrivent une à une
      [["#r1", 0.3], ["#r2", 0.9], ["#r3", 1.5]].forEach(([id, t]) => {
        tl.fromTo(`${id} .avatar-grand`, { autoAlpha: 0, scale: 0.6 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, t);
        tl.fromTo(`${id} .notif`, { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: "power2.out" }, t + 0.2);
      });
      // L'invitation de Louna est acceptée
      tape("#tap-accepter", 3.3);
      tl.fromTo("#btn-amis", { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 3.5);
      tl.to("#btn-accepter", { autoAlpha: 0, duration: 0.15 }, 3.5);
      tl.to("#r3 .avatar-grand", { y: -16, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }, 3.6);
      tl.to(".rangee", { autoAlpha: 0, y: -30, duration: 0.3, ease: "power2.in", stagger: 0.06 }, 5.6);
      tl.to("#fond-couleur", { backgroundColor: "#F5F3F1", duration: 0.4, ease: "power1.inOut" }, 5.75);

      // 1 · Crée et personnalise ton profil (6–9,8 s)
      tl.fromTo("#telephone", { autoAlpha: 0, y: 160 }, { autoAlpha: 1, y: 0, duration: 0.7, ease: "power2.out" }, 5.85);
      texte("#t1", 6.2, 9.55);
      tl.fromTo("#repere", { autoAlpha: 0, scale: 1.08 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "power2.out" }, 6.5);
      tape("#tap-modifier", 6.9);
      fleche("#fleche-camion", 7.6, 9.5);
      tape("#tap-camion", 8.1);
      tape("#tap-partager", 8.85);
      tl.to("#repere", { autoAlpha: 0, duration: 0.25 }, 9.5);

      // 2 · Ajoute tes amis (9,8–13,4 s) : Ajouter → tap → En attente
      tl.fromTo("#e2", { xPercent: 60, autoAlpha: 0 }, arrive, 9.6);
      tl.fromTo("#e1", { xPercent: 0, autoAlpha: 1 }, part, 9.6);
      texte("#t2", 10.0, 13.15);
      fleche("#fleche-ajouter", 10.2, 13.15);
      tape("#tap-ajouter", 10.75);
      tl.fromTo("#attente", { autoAlpha: 0, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 10.95);
      tl.fromTo("#attente .aiguille", { rotation: 0 }, { rotation: 360, svgOrigin: "12 12", duration: 2, ease: "none" }, 11.05);
      tl.to("#attente", { scale: 1.08, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }, 11.4);

      // 3 · Téléphone de l'ami (13,4–18,4 s) : invitation reçue → tap sur Accepter → invitation acceptée
      tl.fromTo("#e5", { xPercent: 60, autoAlpha: 0 }, arrive, 13.2);
      tl.fromTo("#e2", { xPercent: 0, autoAlpha: 1 }, { ...part, immediateRender: false }, 13.2);
      tl.fromTo("#ligne-louna", { autoAlpha: 0, x: -30 }, { autoAlpha: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, 13.75);
      texte("#t3", 13.6, 15.75);
      fleche("#fleche-accepter", 14.4, 18.15);
      tape("#tap-accepter-tel", 15.55);
      tl.fromTo("#ami-ok", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.2 }, 15.75);
      tl.fromTo("#ami-ok span", { scale: 0.7 }, { scale: 1, duration: 0.35, ease: "back.out(2.5)" }, 15.75);
      texte("#t4", 16.0, 18.15);

      // 4 · Découvre leur activité au quotidien (18,4–21,8 s) : accueil, carte de Nicolas J.
      tl.fromTo("#e6", { xPercent: 60, autoAlpha: 0 }, arrive, 18.2);
      tl.fromTo("#e5", { xPercent: 0, autoAlpha: 1 }, { ...part, immediateRender: false }, 18.2);
      texte("#t5", 18.6, 21.55);
      fleche("#fleche-activite", 19.0, 21.55);
      tape("#tap-activite", 19.9);

      // 5 · Regarde qui est en ligne (21,8–25 s) : anneaux verts, « 5 amis en ligne » entouré
      texte("#t6", 22.0, 24.75);
      tl.fromTo(".anneau", { autoAlpha: 0, scale: 1.35 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "back.out(2)", stagger: 0.15 }, 22.2);
      tl.fromTo("#cadre-en-ligne", { autoAlpha: 0, scale: 1.15 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 22.2);
      tl.to(".anneau", { scale: 1.1, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }, 23.0);
      fleche("#fleche-en-ligne", 22.7, 24.75);
      tl.to([".anneau", "#cadre-en-ligne"], { autoAlpha: 0, duration: 0.25 }, 24.75);
      tl.to("#telephone", { autoAlpha: 0, y: 80, duration: 0.3, ease: "power2.in" }, 24.75);

      // Rappel (25–30,5 s), puis fin (30,5–34,5 s) avec le bouton de téléchargement
      tl.to("#fond-couleur", { backgroundColor: "#061866", duration: 0.4, ease: "power1.inOut" }, 24.8);
      texte("#t7", 25.15, 30.25);
      texte("#t8", 30.6);
      tl.to("#t8 .cta", { scale: 1.06, duration: 0.35, yoyo: true, repeat: 3, ease: "sine.inOut" }, 31.6);

      window.__timelines["__ID__"] = tl;
      tl.seek(0);
"""


def page(cid, w, h, css_format):
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
        <div class="plein">
          {NOTIFS_INTRO}
        </div>
      </div>

      <div id="ecrans" class="plein clip" data-start="5.8" data-duration="19.2" data-track-index="2">
        <div id="telephone">
          <div id="e1" class="ecran">
            <div class="cadre">
              <img src="assets/ecrans/v2-profil.png" alt="" />
              <div id="repere"></div>
              {fleche("fleche-camion", 14, 70, "gauche")}
              {tap("tap-modifier", 31, 35.2)}
              {tap("tap-camion", 50, 72.4)}
              {tap("tap-partager", 68, 35.2)}
            </div>
          </div>
          <div id="e2" class="ecran">
            <div class="cadre">
              <img src="assets/ecrans/v2-trouver-routiers.png" alt="" />
              <div id="attente">{HORLOGE}En attente</div>
              {fleche("fleche-ajouter", 89, 33.5, "droite")}
              {fleche("fleche-attente", 89, 33.5, "droite")}
              {tap("tap-ajouter", 75.5, 35.4)}
            </div>
          </div>
          <div id="e5" class="ecran">
            <div class="cadre">
              <img src="assets/ecrans/v3-invitations.png" alt="" />
              {LIGNE_LOUNA}
              <div id="ami-ok"><span>✓ Amis</span></div>
              {fleche("fleche-accepter", 66, 29.8, "droite")}
              {tap("tap-accepter-tel", 60.8, 31.6)}
            </div>
          </div>
          <div id="e6" class="ecran">
            <div class="cadre">
              <img src="assets/ecrans/v3-accueil-en-ligne.png" alt="" />
              {ANNEAUX}
              {fleche("fleche-activite", 13, 46, "gauche")}
              <div id="cadre-en-ligne"></div>
              {fleche("fleche-en-ligne", 8.5, 25.5, "gauche")}
              {tap("tap-activite", 50, 48)}
            </div>
          </div>
        </div>
      </div>

      <div id="textes-clip" class="plein clip" data-start="6" data-duration="{round(DUREE - 6, 2)}" data-track-index="3">
        <div id="textes">
          <div id="t1" class="etape">
            <span class="ligne titre">Crée et personnalise</span>
            <span class="ligne titre">ton profil</span>
          </div>
          <div id="t2" class="etape">
            <span class="ligne titre">Ajoute tes amis</span>
          </div>
          <div id="t3" class="etape">
            <span class="ligne titre">Invitation reçue</span>
          </div>
          <div id="t4" class="etape">
            <span class="ligne titre">Invitation acceptée</span>
          </div>
          <div id="t5" class="etape">
            <span class="ligne titre">Découvre leur activité</span>
            <span class="ligne titre">au quotidien</span>
          </div>
          <div id="t6" class="etape">
            <span class="ligne titre">Regarde qui est en ligne</span>
          </div>
          <div id="t7" class="etape final" data-layout-allow-overflow>
            <span class="ligne titre titre-rappel">Pense à regarder tes invitations</span>
            <span class="ligne sous">pour ne pas manquer une demande d'ami&nbsp;!</span>
          </div>
          <div id="t8" class="etape final" data-layout-allow-overflow>
            <span class="ligne titre">Ne roule plus seul&nbsp;!</span>
            <span class="ligne cta">{TELECHARGER}Télécharge Michelin Truckfly</span>
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
