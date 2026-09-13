from pathlib import Path
from math import cos, radians, sin

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output" / "pdf"
OUTPUT.mkdir(parents=True, exist_ok=True)

CREAM = HexColor("#F4F0E3")
PAPER = HexColor("#FBF8EF")
FOREST = HexColor("#173F36")
DARK_FOREST = HexColor("#102F29")
INK = HexColor("#293630")
MUTED = HexColor("#68736D")
GOLD = HexColor("#D5A13A")
TEXT_GOLD = HexColor("#8A5C00")
MOSS = HexColor("#789461")
TEXT_MOSS = HexColor("#536A44")
SAGE = HexColor("#DEE8D3")
WHITE = HexColor("#FFFDF6")
SOIL = HexColor("#B78A5B")
SOIL_DARK = HexColor("#74543B")
PETAL = HexColor("#F5E4D3")
FRUIT = HexColor("#B85F3D")


def register_fonts():
    fonts = {
        "Arial": "/System/Library/Fonts/Supplemental/Arial.ttf",
        "Arial-Bold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "Georgia": "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "Georgia-Bold": "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    }
    for name, path in fonts.items():
        pdfmetrics.registerFont(TTFont(name, path))


def draw_paragraph(c, text, x, y_top, width, style):
    p = Paragraph(text, style)
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - height)
    return height


def kicker(c, text, x, y):
    c.setFillColor(TEXT_GOLD)
    c.setFont("Arial-Bold", 9)
    c.drawString(x, y, text.upper())
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.25)
    c.line(x, y - 7, x + 42, y - 7)


def rounded_label(c, text, x, y, width, fill=FOREST, text_color=WHITE):
    c.setFillColor(fill)
    c.roundRect(x, y, width, 22, 11, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont("Arial-Bold", 7.7)
    c.drawCentredString(x + width / 2, y + 7.2, text)


def leaf(c, x, y, scale=1.0, angle=0, color=MOSS):
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    c.setFillColor(color)
    c.setStrokeColor(color)
    p = c.beginPath()
    p.moveTo(-8 * scale, 0)
    p.curveTo(-4 * scale, 7 * scale, 6 * scale, 8 * scale, 10 * scale, 0)
    p.curveTo(5 * scale, -7 * scale, -4 * scale, -6 * scale, -8 * scale, 0)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(Color(1, 1, 1, alpha=0.35))
    c.setLineWidth(0.45)
    c.line(-5 * scale, 0, 7 * scale, 0)
    c.restoreState()


def flower(c, x, y, scale=1.0):
    c.saveState()
    c.setFillColor(PETAL)
    for angle in range(0, 360, 72):
        dx = cos(radians(angle)) * 4.2 * scale
        dy = sin(radians(angle)) * 4.2 * scale
        c.circle(x + dx, y + dy, 3.1 * scale, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.circle(x, y, 2.3 * scale, fill=1, stroke=0)
    c.restoreState()


def curved_branch(c, points, width, color=SOIL_DARK):
    p = c.beginPath()
    p.moveTo(points[0], points[1])
    p.curveTo(*points[2:])
    c.setStrokeColor(color)
    c.setLineCap(1)
    c.setLineWidth(width)
    c.drawPath(p, fill=0, stroke=1)


def draw_tree(c):
    # A subtle halo keeps the illustration editorial and gives the labels a home.
    c.setFillColor(Color(0.87, 0.91, 0.82, alpha=0.50))
    c.circle(306, 395, 165, fill=1, stroke=0)

    # Ground and visible roots.
    ground = c.beginPath()
    ground.moveTo(45, 224)
    ground.curveTo(160, 239, 231, 215, 330, 228)
    ground.curveTo(426, 241, 500, 222, 567, 232)
    ground.lineTo(567, 189)
    ground.lineTo(45, 189)
    ground.close()
    c.setFillColor(HexColor("#E7D5B9"))
    c.drawPath(ground, fill=1, stroke=0)
    c.setStrokeColor(SOIL)
    c.setLineWidth(1.25)
    c.line(45, 225, 567, 225)

    # Trunk: asymmetrical, tapered and curved.
    trunk = c.beginPath()
    trunk.moveTo(277, 223)
    trunk.curveTo(281, 286, 270, 340, 295, 411)
    trunk.curveTo(310, 448, 314, 491, 319, 532)
    trunk.curveTo(328, 488, 329, 448, 322, 408)
    trunk.curveTo(313, 349, 333, 292, 337, 225)
    trunk.close()
    c.setFillColor(SOIL_DARK)
    c.drawPath(trunk, fill=1, stroke=0)

    # Roots visibly hold the whole lifecycle.
    roots = [
        (291, 228, 250, 202, 202, 205, 150, 192),
        (304, 226, 276, 200, 260, 187, 244, 174),
        (319, 226, 350, 199, 389, 201, 430, 181),
        (327, 228, 358, 214, 412, 222, 481, 198),
        (300, 224, 301, 205, 296, 188, 290, 168),
    ]
    for r in roots:
        curved_branch(c, r, 4.5, SOIL_DARK)

    # Main branches: bare on the left, increasingly alive toward the right.
    branches = [
        (302, 427, 259, 470, 204, 488, 139, 502),
        (298, 397, 250, 417, 193, 427, 113, 413),
        (310, 456, 286, 500, 266, 535, 240, 570),
        (313, 438, 349, 480, 386, 508, 447, 526),
        (318, 400, 367, 420, 421, 437, 505, 423),
        (323, 363, 376, 371, 432, 348, 512, 329),
        (321, 475, 357, 523, 397, 551, 433, 575),
    ]
    for i, b in enumerate(branches):
        curved_branch(c, b, 8 if i < 3 else 7)

    # Bare branch tips communicate season, not failure.
    twigs = [
        (205, 488, 183, 514, 166, 529, 145, 548),
        (203, 487, 177, 474, 154, 463, 130, 448),
        (191, 427, 164, 444, 145, 452, 120, 454),
        (191, 427, 164, 406, 145, 390, 132, 372),
        (260, 534, 236, 548, 216, 556, 193, 559),
    ]
    for t in twigs:
        curved_branch(c, t, 3.2)

    # Buds bridge the bare limbs into new life.
    c.setFillColor(GOLD)
    for x, y in [(219, 557), (237, 543), (253, 520), (226, 507), (203, 493)]:
        c.circle(x, y, 3.2, fill=1, stroke=0)

    # Organic leaf canopy, weighted toward the fruitful side.
    leaves = [
        (284, 526, .80, 20, MOSS), (300, 548, .92, -15, TEXT_MOSS),
        (327, 535, 1.0, 12, MOSS), (349, 520, .92, -30, TEXT_MOSS),
        (367, 540, 1.0, 20, MOSS), (391, 555, .90, -12, TEXT_MOSS),
        (415, 538, 1.08, 18, MOSS), (443, 522, .92, -28, TEXT_MOSS),
        (462, 499, 1.0, 30, MOSS), (485, 470, .98, -15, TEXT_MOSS),
        (447, 470, 1.10, 12, MOSS), (416, 485, 1.05, -20, TEXT_MOSS),
        (388, 495, .95, 28, MOSS), (360, 478, 1.0, -8, TEXT_MOSS),
        (339, 456, .90, 24, MOSS), (375, 444, 1.10, -25, TEXT_MOSS),
        (407, 428, .94, 18, MOSS), (443, 418, 1.0, -5, TEXT_MOSS),
        (476, 409, 1.0, 28, MOSS), (497, 385, .86, -30, TEXT_MOSS),
        (454, 377, .96, 12, MOSS), (417, 387, 1.06, -18, TEXT_MOSS),
        (382, 397, .90, 28, MOSS), (348, 408, 1.0, -10, TEXT_MOSS),
        (395, 348, .88, 15, MOSS), (432, 339, 1.03, -22, TEXT_MOSS),
        (469, 326, .92, 22, MOSS), (503, 321, .86, -12, TEXT_MOSS),
    ]
    for args in leaves:
        leaf(c, *args)

    for x, y, s in [(318, 511, .9), (350, 500, .8), (384, 525, .9), (407, 503, .8)]:
        flower(c, x, y, s)

    c.setFillColor(FRUIT)
    for x, y, r in [(423, 458, 6), (461, 441, 6.5), (482, 389, 6), (433, 365, 6.5), (491, 345, 5.5)]:
        c.circle(x, y, r, fill=1, stroke=0)
        c.setStrokeColor(SOIL_DARK)
        c.setLineWidth(.8)
        c.line(x, y + r, x + 2, y + r + 6)
        c.setFillColor(FRUIT)

    # Seed movement and saplings: multiplication beyond the original canopy.
    c.setStrokeColor(GOLD)
    c.setDash(2, 3)
    c.setLineWidth(1)
    path = c.beginPath()
    path.moveTo(494, 343)
    path.curveTo(540, 326, 548, 284, 527, 247)
    c.drawPath(path, fill=0, stroke=1)
    c.setDash()
    for x, y in [(529, 278), (536, 260), (526, 244)]:
        leaf(c, x, y, .38, -30, TEXT_GOLD)

    for x, height in [(470, 34), (516, 50), (550, 27)]:
        c.setStrokeColor(TEXT_MOSS)
        c.setLineWidth(2.3)
        c.line(x, 226, x, 226 + height)
        leaf(c, x - 5, 226 + height - 8, .55, 24, MOSS)
        leaf(c, x + 6, 226 + height - 1, .55, -22, TEXT_MOSS)

    # Stage labels sit with the lived movement rather than in equal scorecard boxes.
    rounded_label(c, "ROOTED", 75, 247, 63, DARK_FOREST)
    rounded_label(c, "AWAKENING", 151, 575, 83, TEXT_GOLD)
    rounded_label(c, "FLOURISHING", 274, 583, 89, FOREST)
    rounded_label(c, "FRUITFUL", 420, 548, 68, FRUIT)
    rounded_label(c, "MULTIPLYING", 475, 292, 91, TEXT_MOSS)


def build_rooted(path):
    c = canvas.Canvas(str(path), pagesize=LETTER, pageCompression=1, initialFontName="Arial")
    width, height = LETTER
    c.setTitle("Rooted. Renewed. Multiplying Life. - V2")
    c.setAuthor("James Akers")
    c.setFillColor(PAPER)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    kicker(c, "Rooted. Renewed. Multiplying Life.", 42, 750)
    c.setFillColor(DARK_FOREST)
    c.setFont("Georgia-Bold", 29)
    c.drawString(42, 700, "Bare is not the same as dead.")
    c.setFillColor(INK)
    c.setFont("Georgia", 12.5)
    c.drawString(44, 676, "What looks dormant may still be deeply rooted in Christ.")

    draw_tree(c)

    c.setFillColor(MUTED)
    c.setFont("Arial", 8.7)
    c.drawCentredString(width / 2, 151, "A picture of health - not a scorecard of size, speed, or season.")

    c.setFillColor(DARK_FOREST)
    c.roundRect(42, 59, 528, 73, 10, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 8)
    c.drawString(58, 111, "THE HEARTBEAT")
    heartbeat = ParagraphStyle(
        "heartbeat", fontName="Georgia-Bold", fontSize=12.3, leading=16,
        textColor=WHITE, alignment=TA_LEFT,
    )
    draw_paragraph(
        c,
        "Systems do not create life. Jesus does. Healthy systems make room for the life He is already growing.",
        58, 101, 492, heartbeat,
    )

    c.setFillColor(MUTED)
    c.setFont("Arial", 7.8)
    c.drawCentredString(width / 2, 35, "John 15:1-5  |  John 7:37-39  |  Matthew 13:23  |  Mark 4:26-32")
    c.save()


def draw_source(c, x, y):
    c.setFillColor(GOLD)
    c.circle(x, y, 27, fill=1, stroke=0)
    c.setStrokeColor(TEXT_GOLD)
    c.setLineWidth(1.5)
    for angle in range(0, 360, 30):
        a = radians(angle)
        c.line(x + cos(a) * 34, y + sin(a) * 34, x + cos(a) * 43, y + sin(a) * 43)


def draw_lens(c, x, y, height=118, cracked=False):
    p = c.beginPath()
    p.moveTo(x, y - height / 2)
    p.curveTo(x + 18, y - height / 3, x + 18, y + height / 3, x, y + height / 2)
    p.curveTo(x - 18, y + height / 3, x - 18, y - height / 3, x, y - height / 2)
    p.close()
    c.setFillColor(HexColor("#D9E7E1"))
    c.setStrokeColor(FOREST)
    c.setLineWidth(2)
    c.drawPath(p, fill=1, stroke=1)
    if cracked:
        c.setStrokeColor(FRUIT)
        c.setLineWidth(1.3)
        c.line(x - 1, y + 35, x + 6, y + 13)
        c.line(x + 6, y + 13, x - 5, y - 5)
        c.line(x - 5, y - 5, x + 7, y - 27)
        c.line(x + 6, y + 13, x + 14, y + 7)


def stage_caption(c, x, y, title, body, width=110, align=TA_CENTER):
    style = ParagraphStyle(
        "stage", fontName="Arial", fontSize=9, leading=11.5,
        textColor=INK, alignment=align,
    )
    html = f'<font name="Arial-Bold" color="#173F36" size="9.1">{title}</font><br/>{body}'
    draw_paragraph(c, html, x, y, width, style)


def draw_impact(c, x, y):
    # Grounded pool of light and a small community, not a growth-chart trophy.
    c.setFillColor(Color(0.84, 0.63, 0.23, alpha=0.18))
    c.ellipse(x - 58, y - 11, x + 58, y + 18, fill=1, stroke=0)
    c.setFillColor(FOREST)
    c.rect(x - 32, y + 8, 28, 30, fill=1, stroke=0)
    roof = c.beginPath()
    roof.moveTo(x - 38, y + 38)
    roof.lineTo(x - 18, y + 55)
    roof.lineTo(x + 2, y + 38)
    roof.close()
    c.drawPath(roof, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(x - 18, y + 55, x - 18, y + 67)
    c.line(x - 23, y + 62, x - 13, y + 62)
    for px, py in [(x + 17, y + 24), (x + 35, y + 18), (x + 52, y + 27)]:
        c.setFillColor(TEXT_MOSS)
        c.circle(px, py + 15, 5, fill=1, stroke=0)
        c.setStrokeColor(TEXT_MOSS)
        c.setLineWidth(3)
        c.line(px, py + 10, px, py - 3)


def build_passion(path):
    c = canvas.Canvas(str(path), pagesize=LETTER, pageCompression=1, initialFontName="Arial")
    width, height = LETTER
    c.setTitle("From Passion to Impact - V2")
    c.setAuthor("James Akers")
    c.setFillColor(PAPER)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    kicker(c, "From Passion to Impact", 42, 750)
    c.setFillColor(DARK_FOREST)
    c.setFont("Georgia-Bold", 26)
    c.drawString(42, 705, "Passion is powerful.")
    opening = ParagraphStyle(
        "opening", fontName="Georgia", fontSize=12.4, leading=17,
        textColor=INK, alignment=TA_LEFT,
    )
    draw_paragraph(
        c,
        "But without vision to focus it and mission to move it, passion becomes scattered energy.",
        43, 680, 500, opening,
    )

    # Main optical journey.
    c.setFillColor(CREAM)
    c.roundRect(42, 345, 528, 270, 14, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("Arial-Bold", 7.7)
    c.drawString(58, 594, "ONE ALIGNED JOURNEY")

    sy = 493
    draw_source(c, 91, sy)

    # Broad energy moves toward vision.
    c.setStrokeColor(Color(0.84, 0.63, 0.23, alpha=0.50))
    c.setLineWidth(4)
    for offset in (-21, -7, 7, 21):
        c.line(126, sy + offset, 190, sy + offset * .60)

    draw_lens(c, 214, sy, 124)

    # Vision focuses energy at the mirror; the beam ends at the reflective face.
    c.setFillColor(Color(0.84, 0.63, 0.23, alpha=0.38))
    focus = c.beginPath()
    focus.moveTo(230, sy - 34)
    focus.lineTo(346, sy - 2)
    focus.lineTo(230, sy + 34)
    focus.close()
    c.drawPath(focus, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.2)
    c.line(230, sy, 346, sy)

    # Mission is a real reflector: the light stops here, changes direction, and lands.
    c.saveState()
    c.translate(356, sy)
    c.rotate(45)
    c.setFillColor(FOREST)
    c.roundRect(-3.5, -43, 7, 86, 3.5, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(-8, -43, -8, 43)
    c.restoreState()

    c.setFillColor(Color(0.84, 0.63, 0.23, alpha=0.32))
    reflected = c.beginPath()
    reflected.moveTo(360, sy - 3)
    reflected.lineTo(485, 395)
    reflected.lineTo(459, 377)
    reflected.close()
    c.drawPath(reflected, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.2)
    c.line(360, sy - 3, 472, 386)
    draw_impact(c, 488, 374)

    stage_caption(c, 49, 421, "PASSION", "creates the energy", 85)
    stage_caption(c, 171, 421, "VISION", "brings it into focus", 95)
    stage_caption(c, 315, 421, "MISSION", "points it somewhere that matters", 100)
    stage_caption(c, 460, 472, "IMPACT", "happens where it lands", 96)

    # Supporting contrast: two small interruptions to the same journey.
    c.setFillColor(DARK_FOREST)
    c.setFont("Georgia-Bold", 12)
    c.drawString(42, 316, "When alignment breaks")

    c.setFillColor(CREAM)
    c.roundRect(42, 213, 252, 88, 10, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(62, 257, 112, 257)
    draw_lens(c, 133, 257, 58, cracked=True)
    c.setStrokeColor(FRUIT)
    c.setLineWidth(1.2)
    c.line(146, 257, 177, 275)
    c.line(146, 257, 180, 240)
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 8)
    c.drawString(194, 270, "DISTORTED VISION")
    small = ParagraphStyle("small", fontName="Arial", fontSize=8.3, leading=10.5, textColor=MUTED)
    draw_paragraph(c, "The passion is still strong, but the lens is sending it off course.", 194, 260, 85, small)

    c.setFillColor(CREAM)
    c.roundRect(306, 213, 264, 88, 10, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(326, 257, 371, 257)
    for x, angle in [(384, 55), (400, 15), (414, -28)]:
        c.saveState()
        c.translate(x, 257)
        c.rotate(angle)
        c.setFillColor(FOREST)
        c.roundRect(-2, -18, 4, 36, 2, fill=1, stroke=0)
        c.restoreState()
    c.setStrokeColor(FRUIT)
    c.setDash(2, 2)
    c.setLineWidth(1.2)
    c.line(414, 257, 447, 281)
    c.line(414, 257, 452, 257)
    c.line(414, 257, 445, 232)
    c.setDash()
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 8)
    c.drawString(465, 270, "COMPETING MISSIONS")
    draw_paragraph(c, "Too many directions can scatter the same passion.", 465, 260, 91, small)

    # The equations are conversation tools, not spiritual arithmetic.
    c.setFillColor(FOREST)
    c.roundRect(42, 158, 528, 36, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Arial-Bold", 10.4)
    c.drawCentredString(width / 2, 172, "PASSION + VISION x MISSION = FOCUSED IMPACT")
    c.setFillColor(HexColor("#EEE7D5"))
    c.roundRect(42, 116, 528, 32, 8, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 9.8)
    c.drawCentredString(width / 2, 128, "PASSION - VISION / MISSION = SCATTERED ENERGY")

    c.setFillColor(DARK_FOREST)
    c.roundRect(42, 48, 528, 52, 9, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 7.6)
    c.drawString(57, 83, "THE HEARTBEAT")
    c.setFillColor(WHITE)
    c.setFont("Georgia", 9.6)
    c.drawString(57, 65, "Jesus knew why He came. He prayed, chose where to go next, and did not let the crowd choose His mission.")
    c.setFillColor(MUTED)
    c.setFont("Arial", 7.6)
    c.drawRightString(554, 33, "Mark 1:35-39")
    c.save()


if __name__ == "__main__":
    register_fonts()
    build_rooted(OUTPUT / "rooted-renewed-multiplying-life-v2.pdf")
    build_passion(OUTPUT / "from-passion-to-impact-v2.pdf")
