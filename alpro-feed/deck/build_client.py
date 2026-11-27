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
RED=RGBColor(0xC0,0x39,0x2B)

# 1 COVER
s=prs.slides.add_slide(prs.slide_layouts[6]); bg(s,NAVY)
for (x,y,d) in [(120,120,10),(300,880,14),(860,100,8),(1000,960,10),(700,760,6)]: dot(s,x,y,d,NAVY2 if d>9 else WHITE)
img(s,ROOT+'cal.jpg',1060,0,h=1080)
leaf(s,120,250,70,44,LEAF,-25)
text(s,120,320,900,260,["Le calendrier","de l'Avent Alpro"],size=72,color=WHITE,bold=True,spacing=0.95)
box(s,120,600,140,10,fill=LEAF,radius=0.5)
text(s,120,640,920,60,"Notre plan de communication pour le lancement",size=22,color=RGBColor(0xD7,0xE6,0xD0))
text(s,120,710,920,60,"« Votre Noël. Vos envies. Votre Alpro. »",size=30,color=GOLD,italic=True,bold=True)

# 2 CONTEXTE
s=frame(1,"Le contexte : une place à prendre à Noël")
text(s,120,240,1680,80,"Le végétal progresse, mais Noël reste le moment du chocolat au lait. Vos consommateurs n'ont pas de calendrier pensé pour eux.",size=24,color=MUTED)
for i,(big,small,f) in enumerate([("+ 11 %","de croissance du marché français des alternatives végétales en 2025",NAVY),("572 M€","de marché en France en 2025",GREEN),("5,5 %","seulement des volumes de lait : le végétal reste perçu comme un substitut",WHITE)]):
    x=120+i*580; c=WHITE if f!=WHITE else NAVY
    box(s,x,370,530,400,fill=f,radius=0.1)
    text(s,x+40,410,450,150,big,size=80,color=c,bold=True)
    box(s,x+40,570,80,8,fill=LEAF if f!=WHITE else GOLD,radius=0.5)
    text(s,x+40,605,450,140,small,size=21,color=c if f!=WHITE else MUTED)
box(s,120,810,1680,120,fill=PALE_G,radius=0.3)
text(s,160,810,1600,120,[[("L'opportunité : ",{'bold':True,'color':GREEN}),("faire passer Alpro du rayon « alternative » au rayon « plaisir », sur le moment le plus gourmand de l'année.",{})]],size=22,color=INK,anchor=MSO_ANCHOR.MIDDLE)
text(s,120,950,900,40,"Source : GFI Europe, 2026.",size=14,color=MUTED)

# 3 PROPOSITION
s=frame(2,"Notre proposition : votre premier calendrier de l'Avent")
img(s,ROOT+'cal.jpg',120,240,h=720)
box(s,700,250,1100,250,fill=NAVY,radius=0.08)
text(s,750,250,1000,250,"Chaque jour de décembre, un produit Alpro à découvrir, parfois une saveur exclusive, avec une recette pour l'utiliser.",size=27,color=WHITE,italic=True,anchor=MSO_ANCHOR.MIDDLE)
for i,(t,d) in enumerate([("24 cases","100 % végétales et sans lactose"),("24 recettes","une par case, par QR code"),("1 surprise","la case 25, cachée dans le bouchon")]):
    x=700+i*370
    box(s,x,540,350,190,fill=WHITE,radius=0.12)
    text(s,x+30,565,300,60,t,size=30,color=GREEN,bold=True)
    text(s,x+30,635,300,90,d,size=18,color=MUTED)
box(s,700,770,1100,170,fill=PALE_G,radius=0.2)
text(s,740,770,1020,170,[[("Notre mission : ",{'bold':True,'color':GREEN}),("offrir aux végétariens, aux sportifs et aux intolérants au lactose un Noël gourmand sans compromis, et leur faire adopter le végétal au quotidien.",{})]],size=20,color=INK,anchor=MSO_ANCHOR.MIDDLE)

# 4 CIBLE
s=frame(3,"Vos futurs clients : des urbains connectés de 20 à 40 ans")
P=[("chiara","Chiara, 25 ans","Influenceuse lifestyle"),("jade","Jade, 22 ans","Étudiante, intolérante au lactose"),("chris","Chris, 26 ans","Sportif, musculation"),("catharina","Catharina, 28 ans","Adepte de Pilates"),("sam","Sam, 33 ans","Exigeant, bio et esthète"),("camille","Camille, 38 ans","Maman de deux enfants")]
for i,(f,n,d) in enumerate(P):
    x=120+i*285
    img(s,D+'face_'+f+'.png',x+50,280,w=180)
    text(s,x,480,280,40,n,size=19,color=NAVY,bold=True,align=PP_ALIGN.CENTER)
    text(s,x,525,280,60,d,size=17,color=MUTED,align=PP_ALIGN.CENTER)
box(s,120,650,1680,280,fill=NAVY,radius=0.08)
text(s,170,680,780,230,[[("Où ils nous découvrent",{'bold':True,'color':LEAF,'size':24})],"Instagram pour tous (6 personas sur 6), puis TikTok, YouTube et le magasin.","Aucun ne découvre le calendrier par le site : le site sert à rassurer et à faire acheter."],size=20,color=WHITE,spacing=1.2)
for i,(c,v) in enumerate([("Instagram",6),("TikTok",4),("Magasin",4),("Site Alpro",0)]):
    y=690+i*56
    text(s,1000,y,200,46,c,size=19,color=WHITE,bold=True,anchor=MSO_ANCHOR.MIDDLE)
    box(s,1200,y+11,460,24,fill=NAVY2,radius=0.5)
    if v: box(s,1200,y+11,460*v/6,24,fill=LEAF,radius=0.5)
    text(s,1680,y,90,46,f"{v}/6",size=19,color=WHITE,bold=True,anchor=MSO_ANCHOR.MIDDLE)

# 5 PLAN EN 4 TEMPS
s=frame(4,"Le plan de communication en 4 temps")
ph=[("Mi-sept. à oct.","Teasing","« Quelque chose se prépare » : teaser mystère, compte à rebours, vote sur les saveurs, #VotreAlpro",NAVY),
    ("Novembre","Lancement","Mise en vente, influenceurs, concours Instagram, Bar de Noël en magasin, affichage urbain",GREEN),
    ("1er au 24 déc.","Rituel quotidien","La case du jour et sa recette, unboxing simultané, repost des stories clients",NAVY),
    ("Janvier","Fidélisation","Newsletter bilan, recettes pour continuer, Veganuary, questionnaire",GREEN)]
box(s,200,400,1520,8,fill=LEAF,radius=0.5)
for i,(d,t,b,c) in enumerate(ph):
    x=120+i*430
    text(s,x,270,400,50,d,size=20,color=MUTED,bold=True,align=PP_ALIGN.CENTER)
    dot(s,x+160,360,88,c)
    text(s,x+160,360,88,88,str(i+1),size=32,color=WHITE,bold=True,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    box(s,x,490,400,400,fill=WHITE,radius=0.1)
    text(s,x+30,515,340,60,t,size=28,color=c,bold=True)
    text(s,x+30,590,340,290,b,size=20,color=INK,spacing=1.2)
text(s,120,920,1680,60,[[("Canaux : ",{'bold':True,'color':NAVY}),("Instagram en cœur de stratégie, puis TikTok, influence, YouTube, site et e-mailing, publicité ciblée.",{})]],size=19,color=INK)

# 6 CONTENUS
s=frame(5,"Ce que vos clients verront")
img(s,ROOT+'scenarios/0-contenus-alpro.png',240,225,w=1440)

# 7 VIDEO
s=frame(6,"Un contenu type : la recette du jour en vidéo")
try:
    s.shapes.add_movie(ROOT+'videos/video-recette-iced-latte.mp4',px(260),px(240),px(1170),px(658),poster_frame_image=D+'poster_video.jpg',mime_type='video/mp4')
except Exception as e:
    img(s,D+'poster_video.jpg',260,240,w=1170); print('movie fallback',e)
box(s,1470,240,330,658,fill=NAVY,radius=0.08)
text(s,1500,270,270,600,[[("Pourquoi ce format",{'bold':True,'color':LEAF,'size':22})],"","Une recette simple, filmée dans une cuisine chaleureuse : le végétal devient un plaisir du quotidien.","","Sympathie : ambiance cocooning.","Autorité : la marque montre comment utiliser ses produits."],size=17,color=WHITE,spacing=1.15)

# 8 FEED
s=frame(7,"Instagram, le cœur du dispositif")
img(s,ROOT+'profil-alpro-noel.png',120,230,h=760)
J=[("Ligne 1 : donner envie","L'annonce, la recette en 3 étapes, le secret de la case 25.",NAVY),("Ligne 2 : faire agir","« On l'ouvre ensemble ? », le goûter de Noël, « Il t'attend en magasin ».",GREEN),("Ligne 3 : parler à vos 3 cibles","Végétariens, sportifs (shaker post-séance), intolérants (« Sans lactose. Sans compromis. »).",GOLD),("Une DA reconnaissable","Bleu marine = confiance, vert = végétal et action, jaune = nouveauté, or = exclusif.",NAVY)]
for i,(t,d,c) in enumerate(J):
    y=240+i*185
    box(s,520,y,1280,165,fill=WHITE,radius=0.15)
    box(s,520,y,14,165,fill=c,radius=0)
    text(s,570,y+20,1200,45,t,size=24,color=NAVY,bold=True)
    text(s,570,y+75,1200,80,d,size=19,color=MUTED)

# 9 LANDING
s=frame(8,"La page de vente : rassurer et faire acheter")
img(s,D+'landing_top.jpg',120,240,h=720)
J=[("Bouton « Trouver un magasin » ×4","Engagement : l'achat est toujours à un clic. Bleu marine = confiance.",NAVY),("« Plus que 3 unités ! » en rouge","Rareté : le rouge est réservé à l'urgence.",RED),("Badges rouge, orange, vert","Le code des feux tricolores, compris sans lire.",GOLD),("Case 25 dorée, 24 cases cliquables","Rareté (l'or = précieux) et engagement (le jeu).",GREEN),("FAQ composition et recyclage","Autorité et transparence contre le greenwashing.",NAVY)]
for i,(t,d,c) in enumerate(J):
    y=240+i*145
    dot(s,760,y+18,34,c)
    text(s,820,y,980,45,t,size=21,color=NAVY,bold=True)
    text(s,820,y+48,980,80,d,size=18,color=MUTED)

# 10 ACTIVATION 1
s=frame(9,"Activation 1 : le concours « Gagne ton calendrier »")
for i in range(3): img(s,ROOT+f'concours/slide-{i+1}.png',120+i*390,240,w=360)
box(s,1320,240,480,450,fill=NAVY,radius=0.08)
text(s,1360,270,410,400,[[("Mi-novembre · 50 calendriers",{'bold':True,'color':LEAF,'size':22})],"","S'abonner, taguer 2 amis, partager en story.","","Ce que vous y gagnez : des abonnés, et une cible qui ne vous suivait pas encore."],size=19,color=WHITE,spacing=1.15)
box(s,1320,720,480,170,fill=WHITE,radius=0.12)
text(s,1350,735,420,150,"Réciprocité (on offre), rareté (50 lots, date limite), engagement et preuve sociale (tags, stories).",size=17,color=INK,anchor=MSO_ANCHOR.MIDDLE)

# 11 ACTIVATION 2
s=frame(10,"Activation 2 : le Bar de Noël Alpro en magasin")
img(s,ROOT+'bar_stand.jpg',120,240,h=640)
box(s,1120,240,680,640,fill=NAVY,radius=0.06)
text(s,1160,270,600,590,[[("Les week-ends de novembre",{'bold':True,'color':LEAF,'size':22})],"Hypermarchés urbains et magasins bio.","",[("Faire goûter avant de convaincre : ",{'bold':True}),("dégustation offerte de boissons chaudes de Noël.",{})],"",[("Achat immédiat : ",{'bold':True}),("le présentoir est sur le stand.",{})],"",[("Un contact gagné : ",{'bold':True}),("QR code recette du jour et newsletter.",{})]],size=19,color=WHITE,spacing=1.15)
text(s,120,905,1680,60,"Lève la peur que le végétal soit fade · réciprocité, sympathie, achat d'impulsion",size=19,color=GREEN,bold=True)

# 12 PARCOURS JADE
s=frame(11,"Un parcours client : Jade, 22 ans, intolérante au lactose")
img(s,ROOT+'scenarios/2-jade.png',240,225,w=1440)

# 13 OBJECTIFS
s=frame(12,"Ce que la campagne vous apporte")
K=[("10 000","calendriers vendus","au 24 décembre",NAVY),("1 M","d'impressions","oct. à déc.",GREEN),("30 000","scans de recettes","au 31 décembre",NAVY),("8 000","contacts newsletter","au 31 décembre",GREEN),("10 000","interactions et 1 000 posts #VotreAlpro","nov. à déc.",NAVY),("20 %","des acheteurs adoptent un nouvel usage","fin février",GREEN)]
for i,(n,d,e,c) in enumerate(K):
    x=120+(i%3)*570; y=250+(i//3)*350
    box(s,x,y,530,320,fill=c,radius=0.1)
    text(s,x+36,y+40,460,110,n,size=66,color=WHITE,bold=True)
    text(s,x+36,y+160,460,80,d,size=21,color=WHITE)
    text(s,x+36,y+255,460,40,e,size=16,color=RGBColor(0xC7,0xCD,0xF0))

# 14 MERCI
s=prs.slides.add_slide(prs.slide_layouts[6]); bg(s,CREAM)
box(s,-300,700,900,700,fill=NAVY,shape=MSO_SHAPE.OVAL)
box(s,1450,-350,800,700,fill=GREEN,shape=MSO_SHAPE.OVAL)
for (x,y,d) in [(300,200,40),(1600,820,32),(1380,420,22)]: star(s,x,y,d)
logo(s,810,200,300)
text(s,160,420,1600,150,"Merci ! Vos questions ?",size=80,color=NAVY,bold=True,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
box(s,860,590,200,10,fill=LEAF,radius=0.5)
text(s,160,630,1600,60,"24 jours pour découvrir le végétal autrement.",size=30,color=GREEN,italic=True,bold=True,align=PP_ALIGN.CENTER)
text(s,160,700,1600,60,"Analyses, personas et données détaillées : voir le dossier et ses annexes.",size=22,color=MUTED,align=PP_ALIGN.CENTER)

prs.save(ROOT+'deck/Alpro-presentation-client.pptx'); print(len(prs.slides))
