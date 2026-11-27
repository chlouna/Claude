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



s=frame(8,"Ce que vos clients verront")
text(s,120,232,1680,50,"Instagram, stories, concours, site : une seule identité visuelle sur tous les supports.",size=20,color=MUTED,italic=True)
s.shapes.add_picture(ROOT+'deck/contenus_sans_titre.png',px(260),px(295),width=px(1400))
prs.save(ROOT+'deck/Alpro-slide-contenus.pptx')
