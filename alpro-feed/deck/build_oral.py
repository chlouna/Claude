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



D=ROOT+'deck/'
def img(s,path,x,y,w=None,h=None):
    kw={}
    if w: kw['width']=px(w)
    if h: kw['height']=px(h)
    return s.shapes.add_picture(path,px(x),px(y),**kw)

# 1 COVER
s=prs.slides.add_slide(prs.slide_layouts[6]); bg(s,NAVY)
for (x,y,d) in [(120,120,10),(300,880,14),(860,100,8),(1000,960,10),(700,760,6)]: dot(s,x,y,d,NAVY2 if d>9 else WHITE)
img(s,ROOT+'cal.jpg',1060,0,h=1080)
leaf(s,120,250,70,44,LEAF,-25)
text(s,120,320,900,260,["Le calendrier","de l'Avent Alpro"],size=72,color=WHITE,bold=True,spacing=0.95)
box(s,120,600,140,10,fill=LEAF,radius=0.5)
text(s,120,640,920,60,"Plan de stratégie digitale · Communication multicanal",size=21,color=RGBColor(0xD7,0xE6,0xD0))
text(s,120,710,900,60,"« Votre Noël. Vos envies. Votre Alpro. »",size=30,color=GOLD,italic=True,bold=True)

# 2 VIDEO
s=frame(1,"Notre vidéo")
box(s,260,250,1400,700,fill=NAVY,radius=0.04)
text(s,260,250,1400,700,["▶","Vidéo de 30 secondes","Remplacer ce cadre par la vidéo (point illustré : tunnel de conversion)"],size=30,color=WHITE,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)

# 3 CONTEXTE
s=frame(2,"Alpro et le marché du végétal")
text(s,120,250,1680,80,"Alpro, pionnier du végétal depuis les années 1980. Le marché progresse, mais Noël reste dominé par le chocolat au lait.",size=24,color=MUTED)
for i,(big,small,f) in enumerate([("+ 11 %","croissance du marché français des alternatives végétales en 2025",NAVY),("572 M€","taille du marché français en 2025",GREEN),("5,5 %","part des boissons végétales en volume face au lait animal",WHITE)]):
    x=120+i*580; c=WHITE if f!=WHITE else NAVY
    box(s,x,380,530,450,fill=f,radius=0.1)
    text(s,x+40,430,450,160,big,size=80,color=c,bold=True)
    box(s,x+40,600,80,8,fill=LEAF if f!=WHITE else GOLD,radius=0.5)
    text(s,x+40,640,450,140,small,size=22,color=c if f!=WHITE else MUTED)
text(s,120,880,1680,60,"Source : GFI Europe, 2026.",size=16,color=MUTED)

# 4 IDEE + PROTO
s=frame(3,"Notre idée : 24 jours de découvertes végétales")
img(s,ROOT+'cal.jpg',120,240,h=720)
box(s,700,250,1100,300,fill=NAVY,radius=0.08)
text(s,750,280,1000,250,"« Imagine un calendrier de l'Avent où, au lieu d'un carré de chocolat au lait, tu découvres chaque jour un produit Alpro, avec une recette pour l'utiliser. »",size=26,color=WHITE,italic=True,anchor=MSO_ANCHOR.MIDDLE)
for i,(t,d) in enumerate([("24 cases","mini-produits 100 % végétaux et sans lactose"),("24 recettes","une par case, par QR code"),("1 surprise","la case 25, cachée dans le bouchon")]):
    x=700+i*370
    box(s,x,600,350,200,fill=WHITE,radius=0.12)
    text(s,x+30,630,300,60,t,size=30,color=GREEN,bold=True)
    text(s,x+30,700,300,90,d,size=18,color=MUTED)
text(s,700,850,1100,60,"Prototype présenté en direct",size=22,color=NAVY,bold=True)

# 5 CIBLE
s=frame(4,"Notre cible : 6 personas, Instagram en tête")
P=[("chiara","Chiara, 25 ans","Influenceuse contactée par la marque"),("jade","Jade, 22 ans","TikTok puis drive supermarché"),("chris","Chris, 26 ans","Story d'un pote puis achat en magasin"),("catharina","Catharina, 28 ans","Achat au club de Pilates"),("sam","Sam, 33 ans","Instagram puis Naturalia"),("camille","Camille, 38 ans","Affiche à vélo puis concours")]
for i,(f,n,d) in enumerate(P):
    x=120+(i%3)*360; y=250+(i//3)*340
    img(s,D+'face_'+f+'.png',x+90,y,w=160)
    text(s,x,y+175,340,40,n,size=22,color=NAVY,bold=True,align=PP_ALIGN.CENTER)
    text(s,x,y+215,340,70,d,size=16,color=MUTED,align=PP_ALIGN.CENTER)
box(s,1230,250,570,690,fill=WHITE,radius=0.06)
text(s,1270,275,520,40,"Scoring des canaux de découverte",size=17,color=GREEN,bold=True)
for i,(c,v) in enumerate([("Instagram",6),("TikTok",4),("YouTube",4),("Magasin",4),("Pub print",2),("Site Alpro",0)]):
    y=360+i*92
    text(s,1270,y,200,50,c,size=19,color=NAVY,bold=True,anchor=MSO_ANCHOR.MIDDLE)
    box(s,1470,y+12,240,28,fill=CREAM2,radius=0.5)
    if v: box(s,1470,y+12,240*v/6,28,fill=NAVY if v==6 else GREEN,radius=0.5)
    text(s,1720,y,70,50,f"{v}/6",size=19,color=NAVY,bold=True,anchor=MSO_ANCHOR.MIDDLE)

# 6 PLAN DE COM
s=frame(5,"Comment nos personas nous trouvent")
img(s,ROOT+'scenarios/0-contenus-alpro.png',120,240,w=1180)
for i,(t,d) in enumerate([("Attirer","Instagram, TikTok, influence, concours, affichage"),("Rassurer","landing page : composition, FAQ, 24 cases"),("Faire acheter","store locator, magasin et drive"),("Mots-clés SEO","« calendrier de l'Avent vegan », « sans lactose », « chocolat chaud végétal »")]):
    y=240+i*175
    box(s,1340,y,460,155,fill=NAVY if i%2==0 else GREEN,radius=0.12)
    text(s,1370,y+18,400,40,t,size=22,color=WHITE,bold=True)
    text(s,1370,y+62,400,90,d,size=16,color=WHITE)

# 7 JUSTIF 1 LANDING
s=frame(6,"Justifier un visuel : la landing page")
img(s,D+'landing_top.jpg',120,240,h=720)
J=[("Bouton « Trouver un magasin » ×4","Engagement : l'action est toujours à un clic. Bleu marine = confiance.",NAVY),("Bandeau et badges rouges « Plus que 3 »","Rareté : le rouge est réservé à l'urgence.",RGBColor(0xC0,0x39,0x2B)),("Badges rouge / orange / vert","Code des feux tricolores, compris sans lire.",GOLD),("Case 25 dorée, 24 cases cliquables","Rareté (l'or = précieux) et engagement (le jeu).",GREEN),("FAQ composition et recyclage","Autorité et transparence contre le greenwashing.",NAVY)]
for i,(t,d,c) in enumerate(J):
    y=240+i*145
    dot(s,760,y+18,34,c)
    text(s,820,y,980,45,t,size=21,color=NAVY,bold=True)
    text(s,820,y+48,980,80,d,size=18,color=MUTED)

# 8 JUSTIF 2 CONCOURS
s=frame(7,"Justifier un visuel : le post concours")
for i in range(3): img(s,ROOT+f'concours/slide-{i+1}.png',120+i*400,240,w=370)
J=[("Vert : l'accroche","Réciprocité (on offre) et rareté (« 50 à gagner » en jaune)."),("Crème : la mécanique","« 3 étapes, c'est tout » : engagement, tags = preuve sociale."),("Bleu marine : l'action","Date limite (rareté), bouton blanc au plus fort contraste.")]
for i,(t,d) in enumerate(J):
    y=260+i*230
    box(s,1340,y,460,200,fill=WHITE,radius=0.1)
    text(s,1370,y+25,400,45,t,size=22,color=GREEN,bold=True)
    text(s,1370,y+80,400,110,d,size=18,color=INK)

# 9 SCENARIO JADE
s=frame(8,"Un scénario de contact : Jade, 22 ans")
img(s,ROOT+'scenarios/2-jade.png',240,225,w=1440)

# 10 BIAIS JADE
s=frame(9,"Jade : chaque étape, un biais d'influence")
B=[("TikTok","12,4 K likes","Preuve sociale",RGBColor(0x0D,0x5A,0x3A)),("Site Alpro","« Sans lactose »","Autorité, cohérence",RGBColor(0x4A,0x5A,0x8C)),("Filtre Super U","« Plus que 3 unités »","Rareté",RGBColor(0xC0,0x39,0x2B)),("Drive","Retrait le lendemain","Rareté, cohérence",RGBColor(0x6B,0x4F,0xA0)),("Story 1er déc.","@alpro tagué","Engagement",NAVY)]
for i,(t,d,b,c) in enumerate(B):
    x=120+i*345
    box(s,x,380,320,420,fill=WHITE,radius=0.1)
    dot(s,x+125,410,70,c)
    text(s,x+125,410,70,70,str(i+1),size=28,color=WHITE,bold=True,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    text(s,x+20,510,280,50,t,size=24,color=NAVY,bold=True,align=PP_ALIGN.CENTER)
    text(s,x+20,570,280,60,d,size=18,color=MUTED,align=PP_ALIGN.CENTER)
    box(s,x+30,690,260,60,fill=c,radius=0.5)
    text(s,x+30,690,260,60,b,size=17,color=WHITE,bold=True,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    if i<4: text(s,x+318,570,30,40,"→",size=26,color=MUTED,bold=True)

# 11 MERCI
s=prs.slides.add_slide(prs.slide_layouts[6]); bg(s,CREAM)
box(s,-300,700,900,700,fill=NAVY,shape=MSO_SHAPE.OVAL)
box(s,1450,-350,800,700,fill=GREEN,shape=MSO_SHAPE.OVAL)
for (x,y,d) in [(300,200,40),(1600,820,32),(1380,420,22)]: star(s,x,y,d)
logo(s,810,200,300)
text(s,160,420,1600,150,"Merci ! Vos questions ?",size=80,color=NAVY,bold=True,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
box(s,860,590,200,10,fill=LEAF,radius=0.5)
text(s,160,630,1600,60,"24 jours pour découvrir le végétal autrement.",size=30,color=GREEN,italic=True,bold=True,align=PP_ALIGN.CENTER)
text(s,160,700,1600,60,"Objectif n°1 : 10 000 calendriers vendus au 24 décembre.",size=26,color=MUTED,align=PP_ALIGN.CENTER)

prs.save(ROOT+'deck/Alpro-oral-final.pptx'); print(len(prs.slides))
