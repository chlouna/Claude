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
# SLIDE 9 USP
s=frame(9,"Pourquoi vos clients vont le choisir")
text(s,120,235,1680,60,"Sept bénéfices, chacun pensé pour une attente précise de vos clients.",size=22,color=MUTED,italic=True)
U=[("Le premier calendrier 100 % végétal","Les intolérants au lactose vivent enfin le rituel de l'Avent."),
   ("Des saveurs exclusives","Pain d'épices, ube : une raison de l'acheter… et de le racheter."),
   ("Une recette pour chaque case","Chaque produit s'accompagne d'un usage concret, par QR code."),
   ("Une offre pour tous les profils","Étudiants, sportifs, familles, jeunes actifs : chacun s'y retrouve."),
   ("Un calendrier plus responsable","Carton recyclable et composition transparente : zéro greenwashing."),
   ("La caution d'un expert du végétal","Une marque de confiance, qu'on achète sans décrypter l'étiquette."),
   ("Une expérience à partager","24 rendez-vous pensés pour être commentés et partagés.")]
for i,(t,d) in enumerate(U):
    row=0 if i<4 else 1; col=i if i<4 else i-4
    x=120+col*425+(212 if row else 0); y=320+row*330
    f=NAVY if i%2==0 else GREEN
    box(s,x,y,395,300,fill=f,radius=0.1)
    dot(s,x+28,y+28,56,WHITE)
    text(s,x+28,y+28,56,56,str(i+1),size=24,color=f,bold=True,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    text(s,x+28,y+105,345,80,t,size=22,color=WHITE,bold=True)
    text(s,x+28,y+195,345,100,d,size=17,color=RGBColor(0xD7,0xE6,0xD0) if f==GREEN else RGBColor(0xC7,0xCD,0xF0))

# SLIDE 10 PROMESSE
s=prs.slides.add_slide(prs.slide_layouts[6]); bg(s,NAVY)
for (x,y,d) in [(150,140,10),(1700,160,14),(1500,900,8),(300,880,12),(900,120,6)]: dot(s,x,y,d,NAVY2)
dot(s,90,70,92,LEAF)
text(s,90,70,92,92,"10",size=30,color=NAVY,bold=True,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
text(s,215,62,1200,110,"La promesse de la campagne",size=40,color=WHITE,bold=True,anchor=MSO_ANCHOR.MIDDLE)
s.shapes.add_picture(ROOT+'cal.jpg',px(1380),px(230),height=px(640))
star(s,620,250,44)
text(s,120,300,1220,280,["« Votre Noël.","Vos envies.","Votre Alpro. »"],size=64,color=WHITE,bold=True,spacing=0.95)
box(s,120,645,200,10,fill=LEAF,radius=0.5)
text(s,120,675,1220,60,"24 jours pour découvrir le végétal autrement.",size=30,color=GOLD,italic=True,bold=True)
box(s,120,760,1200,200,fill=NAVY2,radius=0.12)
text(s,160,760,1120,200,[[("Ce que vos clients retiendront : ",{'bold':True,'color':LEAF}),("chacun vit son Noël à sa façon, intolérant, sportif ou simplement gourmand. Le végétal n'est plus une privation, c'est une nouvelle façon de se faire plaisir.",{})]],size=21,color=WHITE,anchor=MSO_ANCHOR.MIDDLE,spacing=1.15)
text(s,90,1010,900,30,"Calendrier de l'Avent Alpro  ·  Plan de communication",size=12,color=RGBColor(0x9A,0xA3,0xD8))
prs.save(ROOT+'deck/Alpro-slides-USP-promesse.pptx')
