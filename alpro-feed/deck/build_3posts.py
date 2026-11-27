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



RED=RGBColor(0xC0,0x39,0x2B)
s=frame(8,"Instagram : 3 posts, 3 rôles")
text(s,120,232,1680,50,"Le feed suit un parcours : donner envie, parler à chaque cible, faire acheter.",size=21,color=MUTED,italic=True)
P=[(1,"1. Donner envie","Le calendrier de l'Avent est arrivé !",[("Rareté",RED)],"Bleu marine = confiance. « Est arrivé » en jaune : un événement daté, qui saute aux yeux. Sous-titre « 100 % végétal · sans lactose ».",NAVY),
   (7,"2. Parler à vos 3 cibles","Végé, sportif ou intolérant au lactose ?",[("Cohérence",RGBColor(0x6B,0x4F,0xA0)),("Sympathie",RGBColor(0xD2,0x4F,0x80))],"Une carte par cible : chacun se reconnaît. « Un Noël gourmand, sans compromis » reprend la mission mot pour mot.",GOLD),
   (6,"3. Faire acheter","Il t'attend en magasin",[("Preuve sociale",GREEN),("Rareté",RED)],"Le produit montré en rayon : il existe vraiment. Vert = passage à l'action. « Lien en bio » vers la page de vente.",GREEN)]
for i,(n,role,t,bs,d,c) in enumerate(P):
    x=120+i*575
    box(s,x,300,545,680,fill=WHITE,radius=0.05)
    box(s,x,300,545,62,fill=c,radius=0.2)
    text(s,x+24,300,500,62,role,size=21,color=WHITE,bold=True,anchor=MSO_ANCHOR.MIDDLE)
    s.shapes.add_picture(ROOT+f'feed-posts/post-{n}.png',px(x+137),px(380),width=px(270))
    text(s,x+24,722,500,70,t,size=17,color=NAVY,bold=True,align=PP_ALIGN.CENTER)
    bx=x+24
    for b,bc in bs:
        w=24+len(b)*11
        box(s,bx,808,w,36,fill=bc,radius=0.5)
        text(s,bx,808,w,36,b,size=14,color=WHITE,bold=True,align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        bx+=w+8
    text(s,x+24,856,500,120,d,size=15,color=INK,spacing=1.1)
prs.save(ROOT+'deck/Alpro-slide-3-posts.pptx')
