"""Builds the redesigned Alpro advent-calendar strategy deck (18 slides, 16:9)."""
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = '/home/user/Claude/alpro-feed/'
NAVY, NAVY2 = RGBColor(0x1D, 0x2A, 0x7A), RGBColor(0x14, 0x1E, 0x5C)
GREEN, LEAF = RGBColor(0x0D, 0x5A, 0x3A), RGBColor(0x7C, 0xC2, 0x42)
CREAM, CREAM2 = RGBColor(0xF7, 0xF0, 0xE4), RGBColor(0xEF, 0xE5, 0xD3)
GOLD, WHITE, INK, MUTED = RGBColor(0xC9, 0xA2, 0x4A), RGBColor(255, 255, 255), RGBColor(0x1B, 0x1F, 0x3B), RGBColor(0x5D, 0x62, 0x80)
PALE_G, PALE_N = RGBColor(0xE3, 0xF1, 0xE6), RGBColor(0xE6, 0xE9, 0xF7)
FONT = 'Nunito'
SCALE = 0.75  # sizes below are given in slide px (1920 wide); 1pt = 2px

prs = Presentation()
prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
W, H = prs.slide_width, prs.slide_height
PX = W / 1920  # design in 1920x1080 px


def px(v):
    return Emu(int(v * PX))


def bg(slide, color):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = color


def box(slide, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12):
    s = slide.shapes.add_shape(shape, px(x), px(y), px(w), px(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1.5)
    s.shadow.inherit = False
    s.text_frame.text = ''
    return s


def text(slide, x, y, w, h, runs, size=20, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, italic=False, spacing=1.1):
    """runs: str, or list of paragraphs; a paragraph is str or list of (txt, dict) runs."""
    tb = slide.shapes.add_textbox(px(x), px(y), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'):
        setattr(tf, m, 0)
    paras = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        parts = para if isinstance(para, list) else [(para, {})]
        for txt, o in parts:
            r = p.add_run()
            r.text = txt
            f = r.font
            f.name = FONT
            f.size = Pt(o.get('size', size) * SCALE)
            f.bold = o.get('bold', bold)
            f.italic = o.get('italic', italic)
            f.color.rgb = o.get('color', color)
    return tb


def dot(slide, x, y, d, color):
    return box(slide, x, y, d, d, fill=color, shape=MSO_SHAPE.OVAL)


def leaf(slide, x, y, w, h, color=LEAF, rot=-20):
    s = box(slide, x, y, w, h, fill=color, shape=MSO_SHAPE.TEAR)
    s.rotation = rot
    return s


def star(slide, x, y, d, color=GOLD):
    return box(slide, x, y, d, d, fill=color, shape=MSO_SHAPE.STAR_5_POINT)


def logo(slide, x=1640, y=950, w=200):
    slide.shapes.add_picture(ROOT + 'logo_t.png', px(x), px(y), width=px(w))


def snow(slide, color=CREAM2):
    for (x, y, d) in [(1780, 70, 14), (1840, 150, 9), (1700, 190, 7), (60, 1000, 10), (130, 960, 7), (1870, 300, 6)]:
        dot(slide, x, y, d, color)


def frame(num, title, title_w=1500):
    """Standard content slide: cream background, numbered pill, title, footer."""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, CREAM)
    snow(s)
    c = dot(s, 90, 70, 92, NAVY)
    tf = c.text_frame
    for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'):
        setattr(tf, m, 0)
    tf.word_wrap = False
    tf.text = str(num)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.runs[0].font.size, p.runs[0].font.bold, p.runs[0].font.name = Pt(24), True, FONT
    p.runs[0].font.color.rgb = WHITE
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    leaf(s, 160, 52, 46, 30, LEAF, -25)
    text(s, 215, 62, 1580, 120, title, size=36, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 215, 190, 120, 8, fill=LEAF, radius=0.5)
    text(s, 90, 1010, 900, 30, "Calendrier de l'Avent Alpro  ·  Plan de stratégie digitale", size=12, color=MUTED)
    text(s, 1500, 1010, 100, 30, str(num + 1), size=12, color=MUTED, align=PP_ALIGN.RIGHT)
    logo(s, 1650, 960, 180)
    return s


def card(s, x, y, w, h, fill, title=None, body=None, tcolor=WHITE, bcolor=None, tsize=24, bsize=17, pad=34):
    box(s, x, y, w, h, fill=fill, radius=0.1)
    bcolor = bcolor or tcolor
    yy = y + pad
    if title:
        text(s, x + pad, yy, w - 2 * pad, 80, title, size=tsize, color=tcolor, bold=True)
    if body:
        text(s, x + pad, yy + (tsize * 2.6 if title else 0), w - 2 * pad, h - 2 * pad, body, size=bsize, color=bcolor)


# ---------- 1. COVER ----------
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s, NAVY)
for (x, y, d) in [(120, 120, 10), (300, 880, 14), (860, 100, 8), (1000, 960, 10), (700, 760, 6), (1250, 140, 12), (520, 300, 6)]:
    dot(s, x, y, d, NAVY2 if d > 9 else WHITE)
box(s, 1180, -120, 900, 1320, fill=CREAM, shape=MSO_SHAPE.OVAL)
s.shapes.add_picture(ROOT + 'cal.jpg', px(1330), px(110), height=px(860))
leaf(s, 120, 250, 70, 44, LEAF, -25)
text(s, 120, 320, 1050, 260, ["Le calendrier", "de l'Avent Alpro"], size=72, color=WHITE, bold=True, spacing=0.95)
box(s, 120, 600, 140, 10, fill=LEAF, radius=0.5)
text(s, 120, 640, 1000, 60, "Plan de stratégie digitale · Communication multicanal", size=26, color=RGBColor(0xD7, 0xE6, 0xD0))
text(s, 120, 710, 1000, 60, "« Votre Noël. Vos envies. Votre Alpro. »", size=30, color=GOLD, italic=True, bold=True)
star(s, 1150, 220, 40)
star(s, 1240, 880, 28)

# ---------- 2. IDÉE ----------
s = frame(1, "Notre idée : 24 jours de découvertes végétales")
text(s, 120, 260, 800, 50, "Deux constats", size=26, color=GREEN, bold=True)
for i, t in enumerate(["L'essor des modes de vie flexitariens et healthy",
                       "Une offre de Noël dominée par le chocolat au lait, qui exclut les intolérants au lactose"]):
    y = 330 + i * 170
    box(s, 120, y, 800, 140, fill=WHITE, radius=0.18)
    c = dot(s, 150, y + 35, 70, GREEN)
    text(s, 150, y + 35, 70, 70, str(i + 1), size=26, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 250, y + 20, 640, 100, t, size=21, color=INK, anchor=MSO_ANCHOR.MIDDLE)
box(s, 120, 700, 800, 200, fill=PALE_G, radius=0.15)
text(s, 160, 730, 720, 150, [[("Ambition  ", {'bold': True, 'color': GREEN}),
                              ("Transformer l'attente de Noël en un rituel quotidien de découverte, gourmand et responsable.", {'italic': True})]],
     size=22, color=GREEN, anchor=MSO_ANCHOR.MIDDLE)
box(s, 1000, 260, 800, 640, fill=NAVY, radius=0.08)
box(s, 1040, 300, 520, 56, fill=LEAF, radius=0.5)
text(s, 1040, 300, 520, 56, "Comment l'expliquer à un proche", size=19, color=NAVY, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 1050, 390, 700, 480, ["« Imagine un calendrier de l'Avent où, au lieu d'un carré de chocolat au lait, tu découvres chaque jour un produit Alpro, parfois une saveur exclusive comme le pain d'épices ou l'ube, avec une recette pour l'utiliser.",
                              "",
                              "C'est pour tous ceux qui veulent vivre la magie de Noël sans lactose et sans renoncer au plaisir : intolérants, sportifs ou simplement curieux du végétal. »"],
     size=22, color=WHITE, italic=True, spacing=1.2)

# ---------- 3. VISION ----------
s = frame(2, "Notre vision : faire passer le végétal au rayon « plaisir »")
stats = [("+ 11 %", "croissance du marché français des alternatives végétales en 2025", NAVY, WHITE),
         ("572 M€", "taille du marché français en 2025", GREEN, WHITE),
         ("5,5 %", "part des boissons végétales en volume face au lait animal", WHITE, NAVY)]
for i, (big, small, f, c) in enumerate(stats):
    x = 120 + i * 580
    box(s, x, 330, 530, 480, fill=f, radius=0.1, line=None)
    dot(s, x + 40, 370, 26, LEAF)
    text(s, x + 40, 430, 450, 160, big, size=80, color=c if f != WHITE else NAVY, bold=True)
    box(s, x + 40, 600, 80, 8, fill=LEAF if f != WHITE else GOLD, radius=0.5)
    text(s, x + 40, 640, 450, 140, small, size=22, color=c if f != WHITE else MUTED)

# ---------- 4. CIBLE ----------
s = frame(3, "Notre cible : des urbains connectés de 20 à 40 ans")
box(s, 120, 250, 980, 56, fill=NAVY, radius=0.5)
text(s, 120, 250, 980, 56, "Cible avec découverte du calendrier · scénario de contact", size=19, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
people = [("Chiara", "25 ans", "Influenceuse contactée par la marque : gifting", NAVY),
          ("Chris", "26 ans", "Story Instagram puis achat en magasin", GREEN),
          ("Camille", "38 ans", "Achat du calendrier grâce à une pub abribus", NAVY),
          ("Jade", "22 ans", "Scroll sur TikTok puis achat drive supermarché", GREEN),
          ("Catharina", "28 ans", "Achat du calendrier au club de Pilates", NAVY),
          ("Sam", "33 ans", "Scroll sur Instagram puis achat chez Naturalia", GREEN)]
for i, (n, a, sc, col) in enumerate(people):
    x, y = 120 + (i % 3) * 580, 360 + (i // 3) * 300
    box(s, x, y, 540, 260, fill=WHITE, radius=0.12)
    dot(s, x + 30, y + 40, 110, col)
    text(s, x + 30, y + 40, 110, 110, n[0], size=46, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 170, y + 45, 340, 50, [[(n, {'bold': True, 'color': NAVY, 'size': 28}), ("  " + a, {'color': GREEN, 'size': 20, 'bold': True})]])
    text(s, x + 170, y + 105, 340, 140, sc, size=19, color=MUTED, italic=True)

# ---------- 5. PERSONAS / SCORING ----------
s = frame(4, "Six personas, un canal de découverte en tête")
chan = [("Instagram", 6), ("TikTok", 4), ("YouTube", 4), ("Point de vente physique", 4), ("Pub print", 2), ("Site internet Alpro", 0)]
text(s, 120, 260, 900, 50, "Scoring : nombre de personas qui découvrent le calendrier par ce canal", size=20, color=GREEN, bold=True)
for i, (c, v) in enumerate(chan):
    y = 330 + i * 100
    text(s, 120, y, 330, 70, c, size=22, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 460, y + 15, 600, 40, fill=CREAM2, radius=0.5)
    if v:
        box(s, 460, y + 15, 600 * v / 6, 40, fill=NAVY if v == 6 else GREEN, radius=0.5)
    text(s, 1080, y, 100, 70, f"{v}/6", size=24, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
box(s, 1240, 300, 560, 580, fill=NAVY, radius=0.1)
star(s, 1290, 340, 44)
text(s, 1290, 420, 470, 440, [[("Instagram arrive en tête (6/6).", {'bold': True, 'size': 30, 'color': WHITE})], "",
                              "Aucun persona ne découvre le calendrier par le site Alpro (0/6) : le site sert à rassurer et à convertir."],
     size=23, color=RGBColor(0xC7, 0xCD, 0xF0), spacing=1.2)

# ---------- 6. SCÉNARIO ----------
s = frame(5, "Notre scénario de contact")
box(s, 120, 260, 1000, 660, fill=NAVY, radius=0.06)
s.shapes.add_picture(ROOT + 'phone.jpg', px(400), px(290), height=px(600))
box(s, 1200, 330, 600, 120, fill=GREEN, radius=0.5)
text(s, 1200, 330, 600, 120, "Jade · 22 ans", size=34, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
steps = ["Scroll sur TikTok", "Achète en drive", "au supermarché"]
box(s, 1200, 500, 600, 380, fill=WHITE, radius=0.1)
text(s, 1250, 540, 500, 300, [[("1  ", {'bold': True, 'color': LEAF, 'size': 34}), ("Scroll sur TikTok", {'bold': True, 'color': NAVY})], "",
                              [("2  ", {'bold': True, 'color': LEAF, 'size': 34}), ("Puis achète en drive au supermarché", {'bold': True, 'color': NAVY})]],
     size=28)

# ---------- 7. MISSION ----------
s = frame(6, "Notre mission : le végétal au quotidien")
box(s, 120, 250, 1680, 190, fill=NAVY, radius=0.15)
text(s, 180, 250, 1560, 190, "Faire entrer le végétal dans le quotidien des consommateurs par une expérience de Noël gourmande, ludique et partageable.",
     size=32, color=WHITE, italic=True, bold=True, anchor=MSO_ANCHOR.MIDDLE)
text(s, 120, 490, 900, 50, "Trois freins que nous levons", size=26, color=GREEN, bold=True)
freins = [("« Le végétal, c'est fade »", "Le calendrier fait goûter avant de convaincre.", LEAF),
          ("« Je ne sais pas l'utiliser »", "Des usages concrets, du latte à la carbonara végétale.", GOLD),
          ("« C'est du greenwashing »", "Une composition affichée en toute transparence.", RGBColor(0x8E, 0x7C, 0xC3))]
for i, (t, b, c) in enumerate(freins):
    x = 120 + i * 570
    box(s, x, 570, 530, 330, fill=WHITE, radius=0.1)
    dot(s, x + 40, 610, 56, c)
    text(s, x + 40, 690, 460, 80, t, size=22, color=NAVY, bold=True)
    text(s, x + 40, 780, 460, 110, b, size=21, color=MUTED)

# ---------- 8. SMART ----------
s = frame(7, "Nos objectifs SMART")
objs = [("1. Vendre la première édition", "10 000", "calendriers vendus", "24 décembre"),
        ("2. Faire découvrir de nouveaux usages", "30 000", "scans des QR codes recettes", "31 décembre"),
        ("3. Développer la visibilité", "1 M", "impressions (Instagram, TikTok, YouTube, influence)", "1er oct. – 31 déc."),
        ("4. Créer une communauté engagée", "10 000", "interactions et 1 000 publications avec le hashtag", "1er nov. – 31 déc."),
        ("5. Recruter des contacts", "8 000", "inscrits newsletter avec consentement", "31 décembre"),
        ("6. Ancrer Alpro dans le quotidien", "20 %", "des acheteurs ayant adopté un nouvel usage", "fin février")]
for i, (t, n, d, e) in enumerate(objs):
    x, y = 120 + (i % 3) * 570, 260 + (i // 3) * 360
    f = GREEN if (i % 3 + i // 3) % 2 == 0 else NAVY
    box(s, x, y, 530, 330, fill=f, radius=0.1)
    text(s, x + 36, y + 30, 460, 40, t, size=19, color=WHITE, bold=True)
    text(s, x + 36, y + 95, 460, 100, n, size=60, color=WHITE, bold=True)
    text(s, x + 36, y + 205, 460, 60, d, size=16, color=RGBColor(0xDD, 0xE6, 0xF5))
    box(s, x + 36, y + 268, 400, 44, fill=WHITE, radius=0.5)
    text(s, x + 36, y + 268, 400, 44, "Échéance : " + e, size=15, color=f, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 9. VALEURS ----------
s = frame(8, "Nos valeurs : là où la marque et la cible se rejoignent")
vals = [("Plaisir", "Prouver que le végétal peut être gourmand", "Se faire plaisir sans se priver pendant les fêtes"),
        ("Innovation", "Proposer des saveurs, recettes et usages inédits", "Découvrir des produits exclusifs, jamais vus en rayon"),
        ("Responsabilité", "Encourager une consommation durable, limiter les emballages", "Consommer en accord avec ses convictions"),
        ("Authenticité", "Communiquer de façon transparente, sans promesse exagérée", "Être rassuré face au greenwashing"),
        ("Bien-être", "Accompagner une alimentation équilibrée", "Prendre soin de soi et de sa digestion"),
        ("Partage", "Créer une communauté autour du rituel de l'Avent", "Cuisiner avec ses proches, partager sur les réseaux")]
for i, (t, a, c) in enumerate(vals):
    x, y = 120 + (i % 3) * 570, 260 + (i // 3) * 360
    box(s, x, y, 530, 330, fill=WHITE, radius=0.1)
    box(s, x, y, 530, 80, fill=NAVY if i % 2 == 0 else GREEN, radius=0.25)
    text(s, x + 36, y, 460, 80, t, size=26, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 36, y + 105, 460, 210, [[("Alpro  ", {'bold': True, 'color': NAVY}), (a, {})], "",
                                        [("Cible  ", {'bold': True, 'color': GREEN}), (c, {})]], size=18, color=INK)

# ---------- 10. USP ----------
s = frame(9, "USPs : sept bénéfices qui nous distinguent")
text(s, 120, 240, 1680, 70, "Le calendrier de l'Avent Alpro se distingue par sept bénéfices, chacun répondant à une attente identifiée dans nos personas.",
     size=22, color=MUTED, italic=True)
usps = ["Le premier calendrier 100 % végétal", "Des exclusivités introuvables en rayon", "Une recette pour chaque case",
        "Une offre qui parle à plusieurs profils", "Un calendrier plus responsable", "La légitimité d'un expert du végétal",
        "Une expérience quotidienne et partageable"]
for i, u in enumerate(usps):
    row = 0 if i < 4 else 1
    col = i if i < 4 else i - 4
    x = 120 + col * 425 + (212 if row else 0)
    y = 360 + row * 300
    box(s, x, y, 395, 260, fill=NAVY if i % 2 == 0 else GREEN, radius=0.12)
    dot(s, x + 30, y + 30, 64, WHITE)
    text(s, x + 30, y + 30, 64, 64, str(i + 1), size=26, color=NAVY if i % 2 == 0 else GREEN, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 30, y + 115, 340, 130, u, size=22, color=WHITE, bold=True)

# ---------- 11. SLOGAN ----------
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s, NAVY)
for (x, y, d) in [(150, 140, 10), (1700, 160, 14), (1500, 900, 8), (300, 880, 12), (900, 120, 6)]:
    dot(s, x, y, d, NAVY2)
dot(s, 90, 70, 92, LEAF)
text(s, 90, 70, 92, 92, "10", size=30, color=NAVY, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 215, 62, 1000, 110, "Notre slogan", size=40, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
star(s, 860, 250, 50)
text(s, 100, 330, 1720, 220, "« Votre Noël. Vos envies. Votre Alpro. »", size=64, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, 860, 570, 200, 10, fill=LEAF, radius=0.5)
text(s, 240, 620, 1440, 60, "Signature : « 24 jours pour découvrir le végétal autrement. »", size=30, color=GOLD, italic=True, bold=True, align=PP_ALIGN.CENTER)
text(s, 340, 720, 1240, 140, "Le consommateur est au centre : chacun vit son Noël à sa façon. Le végétal n'est pas une privation, mais une nouvelle façon de se faire plaisir.",
     size=24, color=RGBColor(0xC7, 0xCD, 0xF0), align=PP_ALIGN.CENTER)
text(s, 90, 1010, 900, 30, "Calendrier de l'Avent Alpro  ·  Plan de stratégie digitale", size=12, color=RGBColor(0x9A, 0xA3, 0xD8))

# ---------- 12. CANAUX ----------
s = frame(11, "Canaux digitaux : classement par ordre d'importance")
rows = [("Instagram", "6/6", "Cœur de la stratégie : esthétique, Reels, stories quotidiennes du 1er au 24 décembre"),
        ("TikTok", "4/6", "Contenu viral et spontané : unboxings, recettes de lattes ou de shakers, avis « non filtrés »"),
        ("Marketing d'influence", "Tous scénarios", "Relais de confiance : créateurs food, lifestyle, fitness et Pilates, clubs de sport partenaires"),
        ("YouTube", "4/6", "Formats longs : recettes détaillées, vlogs, tests nutrition avec un coach"),
        ("Site Alpro et e-mailing", "0/6 découverte", "Rassurer (composition, FAQ), localiser les points de vente, entretenir la relation"),
        ("Paid social (Meta, TikTok Ads)", "Amplification", "Portée en nov.-déc. sur des audiences précises : sans lactose, bio, nutrition sportive")]
for i, (c, sc, r) in enumerate(rows):
    y = 245 + i * 104
    box(s, 120, y, 1680, 92, fill=WHITE, radius=0.3)
    dot(s, 140, y + 16, 60, NAVY if i == 0 else GREEN)
    text(s, 140, y + 16, 60, 60, str(i + 1), size=24, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 230, y, 380, 92, c, size=21, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 620, y + 24, 230, 44, fill=PALE_G, radius=0.5)
    text(s, 620, y + 24, 230, 44, sc, size=15, color=GREEN, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 880, y, 890, 92, r, size=17, color=INK, anchor=MSO_ANCHOR.MIDDLE)
box(s, 120, 880, 1480, 110, fill=PALE_N, radius=0.25)
text(s, 150, 880, 1420, 110, [[("Relais physiques : ", {'bold': True, 'color': NAVY}),
                               ("dégustations en magasin, clubs de Pilates, magasins bio, street marketing, chacun avec un QR code vers le digital.  ", {}),
                               ("SEO : ", {'bold': True, 'color': NAVY}),
                               ("« calendrier de l'Avent vegan », « sans lactose », « chocolat chaud végétal ».", {})]],
     size=16, color=INK, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 13. PRÉSENCE / ÉCHANGE ----------
s = frame(12, "Être présent sur les médias de la cible et dialoguer")
cols = [("Comment être présent", NAVY, [("Instagram", "filtre « Mon décompte de l'Avent Alpro », DA cozy winter"),
                                         ("TikTok", "transparence et ASMR, recettes « Jour 12 : booste ton chocolat chaud »"),
                                         ("YouTube", "une vidéo par semaine en novembre-décembre"),
                                         ("Influence", "unboxing simultané des ambassadeurs le 1er décembre")]),
        ("Comment établir l'échange", GREEN, [("Sondages et boîtes à questions", "« Plutôt team avoine ou team amande ? »"),
                                              ("UGC", "taguer @Alpro à chaque case, repartage des meilleures stories chaque soir"),
                                              ("Modération complice", "ton chaleureux et décalé pour lever les doutes sur le goût ou la composition")])]
for i, (t, c, items) in enumerate(cols):
    x = 120 + i * 860
    box(s, x, 260, 820, 690, fill=WHITE, radius=0.07)
    box(s, x, 260, 820, 100, fill=c, radius=0.3)
    text(s, x + 40, 260, 740, 100, t, size=28, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    paras = []
    for a, b in items:
        paras += [[(a + " : ", {'bold': True, 'color': c}), (b, {})], ""]
    text(s, x + 50, 400, 720, 530, paras[:-1], size=21, color=INK, spacing=1.15)

# ---------- 14. INBOUND ----------
s = frame(13, "Inbound : le ton d'une « amie bien informée »")
box(s, 120, 250, 1680, 140, fill=GREEN, radius=0.3)
text(s, 170, 250, 1580, 140, [[("Pas « tu dois manger végétal », mais ", {}), ("« Et si tu découvrais une nouvelle façon de te faire plaisir ? »", {'bold': True, 'italic': True})]],
     size=27, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
pil = [("Le végétal au quotidien", "Montrer que c'est facile et gourmand", "Recettes, astuces, idées petit-déjeuner"),
       ("La magie de Noël", "Créer l'envie autour du calendrier", "Teasing, compte à rebours, unboxing"),
       ("Bien-être et lifestyle", "S'inscrire dans les habitudes de la cible", "Morning routine, Pilates, goûter, café"),
       ("Communauté et partage", "Faire participer les consommateurs", "Sondages, UGC, challenges, témoignages")]
for i, (t, o, f) in enumerate(pil):
    x = 120 + i * 425
    col = NAVY if i % 2 == 0 else GREEN
    box(s, x, 440, 395, 500, fill=WHITE, radius=0.1)
    dot(s, x + 30, 475, 72, col)
    text(s, x + 30, 475, 72, 72, str(i + 1), size=28, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 30, 575, 340, 90, t, size=24, color=col, bold=True)
    text(s, x + 30, 680, 340, 100, o, size=19, color=MUTED, italic=True)
    box(s, x + 30, 800, 335, 110, fill=CREAM, radius=0.2)
    text(s, x + 50, 800, 300, 110, f, size=17, color=INK, bold=True, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 15. QUESTIONS ----------
s = frame(14, "Répondre aux questions de nos clients potentiels")
qs = [("Qu'y a-t-il dedans ?", "Reel et TikTok « 24 jours, 24 découvertes »"),
      ("Est-ce facile à utiliser ?", "Série « 1 produit Alpro = 3 façons de l'utiliser »"),
      ("Ça correspond à mon mode de vie ?", "Série « Alpro accompagne ta journée », du café de 7 h 30 au dessert de 21 h"),
      ("Est-ce vraiment sain ?", "Carrousel « 5 idées reçues » co-signé par un(e) nutritionniste")]
for i, (q, a) in enumerate(qs):
    y = 250 + i * 160
    box(s, 120, y, 1060, 140, fill=WHITE, radius=0.2)
    box(s, 120, y, 400, 140, fill=NAVY if i % 2 == 0 else GREEN, radius=0.2)
    text(s, 150, y, 340, 140, q, size=21, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 550, y, 600, 140, a, size=19, color=INK, anchor=MSO_ANCHOR.MIDDLE)
text(s, 120, 900, 1060, 60, [[("Faciliter la vie : ", {'bold': True, 'color': GREEN}), ("FAQ, store locator et QR code sur chaque produit vers sa fiche et sa recette.", {'italic': True})]],
     size=18, color=INK)
box(s, 1240, 250, 560, 690, fill=NAVY, radius=0.08)
star(s, 1280, 285, 40)
text(s, 1340, 280, 440, 60, "5 preuves que nous avons la solution", size=24, color=WHITE, bold=True)
proofs = [("Expérience", "dégustations gratuites"), ("Pairs", "unboxings, UGC, témoignages"), ("Expertise", "nutritionnistes et coachs"),
          ("Transparence", "composition par QR code"), ("Dialogue", "réponses rapides aux objections")]
for i, (a, b) in enumerate(proofs):
    y = 400 + i * 104
    dot(s, 1280, y + 10, 22, LEAF)
    text(s, 1320, y, 450, 90, [[(a, {'bold': True, 'color': WHITE, 'size': 22})], b], size=18, color=RGBColor(0xC7, 0xCD, 0xF0))

# ---------- 16. CIALDINI ----------
s = frame(15, "Les principes d'influence de Cialdini")
ci = [("Preuve sociale", "Unboxings d'influenceurs, UGC repartagé, avis et témoignages", GREEN),
      ("Engagement", "Sondages, quiz, challenge « 7 jours végétal »", NAVY),
      ("Sympathie", "Influenceurs proches de la cible, ton chaleureux", GREEN),
      ("Rareté", "Édition limitée, saveurs exclusives, vente nov.-déc. (si réelle)", NAVY)]
for i, (t, b, c) in enumerate(ci):
    x = 120 + i * 425
    box(s, x, 330, 395, 520, fill=c, radius=0.1)
    star(s, x + 36, 370, 50, GOLD if c == NAVY else LEAF)
    text(s, x + 36, 460, 330, 80, t, size=30, color=WHITE, bold=True)
    box(s, x + 36, 560, 80, 8, fill=WHITE, radius=0.5)
    text(s, x + 36, 600, 330, 230, b, size=21, color=WHITE)

# ---------- 17. CALENDRIER ÉDITORIAL ----------
s = frame(16, "Calendrier éditorial : de septembre à janvier")
ph = [("Mi-sept. – oct.", "Faire connaître", "Teasing mystère, compte à rebours, recettes offertes, hashtag"),
      ("Début nov.", "Lancer la vente", "Mise en vente, 1re vague d'influence, dégustations"),
      ("Mi – fin nov.", "Convertir", "FAQ, avis, concours Instagram, Black Friday"),
      ("1er – 7 déc.", "Créer l'habitude", "Unboxing simultané, case du jour, UGC"),
      ("8 – 24 déc.", "Maintenir", "Recettes, challenges, meilleures découvertes"),
      ("Janvier", "Fidéliser", "Newsletter bilan, Veganuary, questionnaire")]
box(s, 200, 393, 1520, 8, fill=LEAF, radius=0.5)
for i, (d, t, b) in enumerate(ph):
    x = 120 + i * 285
    text(s, x, 270, 260, 50, d, size=18, color=MUTED, bold=True, align=PP_ALIGN.CENTER)
    dot(s, x + 90, 357, 80, NAVY if i % 2 == 0 else GREEN)
    text(s, x + 90, 357, 80, 80, str(i + 1), size=28, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, x, 480, 260, 380, fill=WHITE, radius=0.1)
    text(s, x + 24, 505, 212, 110, t, size=21, color=NAVY if i % 2 == 0 else GREEN, bold=True)
    text(s, x + 24, 625, 212, 230, b, size=17, color=INK)
box(s, 120, 890, 1480, 90, fill=PALE_N, radius=0.3)
text(s, 150, 890, 1420, 90, [[("Fréquences : ", {'bold': True, 'color': NAVY}),
                              ("Instagram 4-5 posts/sem. + stories quotidiennes en déc. · TikTok 4 vidéos/sem. · YouTube 1 vidéo/sem. · site 2 articles/mois · newsletter 1-2/sem. en déc.", {})]],
     size=16, color=INK, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 18. MERCI ----------
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s, CREAM)
box(s, -300, 700, 900, 700, fill=NAVY, shape=MSO_SHAPE.OVAL)
box(s, 1450, -350, 800, 700, fill=GREEN, shape=MSO_SHAPE.OVAL)
for (x, y, d) in [(300, 200, 40), (1600, 820, 32), (1380, 420, 22)]:
    star(s, x, y, d)
logo(s, 810, 200, 300)
text(s, 160, 420, 1600, 150, "Merci ! Vos questions ?", size=80, color=NAVY, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, 860, 590, 200, 10, fill=LEAF, radius=0.5)
text(s, 160, 630, 1600, 60, "24 jours pour découvrir le végétal autrement.", size=30, color=GREEN, italic=True, bold=True, align=PP_ALIGN.CENTER)
text(s, 160, 700, 1600, 60, "Objectif n°1 : 10 000 calendriers vendus au 24 décembre.", size=26, color=MUTED, align=PP_ALIGN.CENTER)

prs.save(ROOT + 'deck/Alpro-strategie-digitale-avent.pptx')
print('slides', len(prs.slides))
