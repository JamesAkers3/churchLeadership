from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from build_v2_visuals import register_fonts


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output" / "pdf" / "rooted-renewed-multiplying-life-v6.pdf"

PAGE = (792.0, 612.0)
PAPER = HexColor("#FBF8EF")
FOREST = HexColor("#173F36")
DARK_FOREST = HexColor("#0D382F")
INK = HexColor("#293630")
MUTED = HexColor("#68736D")
GOLD = HexColor("#D5A13A")
WHITE = HexColor("#FFFDF6")
PALE_SAGE = HexColor("#E7EDDF")
SOIL = HexColor("#A07D59")
SOIL_DARK = HexColor("#664A35")
TRUNK = HexColor("#604631")
LEAF_DARK = HexColor("#35634E")
LEAF_MID = HexColor("#4E7A59")
LEAF_LIGHT = HexColor("#73965F")
BUD = HexColor("#A9C768")
FRUIT = HexColor("#D7A23A")


def paragraph(c, text, x, y_top, width, style):
    p = Paragraph(text, style)
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - height)
    return height


def draw_branch(c, points, width=4.0, color=TRUNK):
    p = c.beginPath()
    p.moveTo(*points[0])
    if len(points) == 4:
        p.curveTo(*points[1], *points[2], *points[3])
    else:
        for point in points[1:]:
            p.lineTo(*point)
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.setLineCap(1)
    c.drawPath(p, fill=0, stroke=1)


def draw_tapered_trunk(c, x, ground, top, lean=0):
    p = c.beginPath()
    p.moveTo(x - 5.5, ground)
    p.curveTo(x - 4, ground + (top - ground) * .34, x + lean - 3, ground + (top - ground) * .70, x + lean - 1.5, top)
    p.lineTo(x + lean + 1.7, top)
    p.curveTo(x + lean + 3, ground + (top - ground) * .70, x + 4, ground + (top - ground) * .34, x + 5.5, ground)
    p.close()
    c.setFillColor(TRUNK)
    c.drawPath(p, fill=1, stroke=0)


def draw_bare_tree(c, x, ground, height, buds=False, lean=0):
    top = ground + height
    draw_tapered_trunk(c, x, ground, top, lean)
    branches = [
        [(x, ground + height * .43), (x - 18, ground + height * .52), (x - 29, ground + height * .66), (x - 37, ground + height * .76)],
        [(x - 22, ground + height * .59), (x - 38, ground + height * .68), (x - 46, ground + height * .76), (x - 52, ground + height * .82)],
        [(x, ground + height * .57), (x + 16, ground + height * .67), (x + 28, ground + height * .76), (x + 39, ground + height * .84)],
        [(x + 21, ground + height * .72), (x + 31, ground + height * .79), (x + 37, ground + height * .87), (x + 44, ground + height * .92)],
        [(x, ground + height * .80), (x - 12, ground + height * .88), (x - 18, ground + height * .93), (x - 23, top)],
    ]
    for idx, branch in enumerate(branches):
        draw_branch(c, branch, 4.8 if idx < 3 else 3.4)

    if buds:
        for bx, by, size in (
            (x - 52, ground + height * .82, 5.0),
            (x - 37, ground + height * .76, 5.5),
            (x + 39, ground + height * .84, 5.4),
            (x + 44, ground + height * .92, 4.7),
            (x - 23, top, 5.2),
            (x, top, 5.6),
        ):
            c.setFillColor(BUD)
            c.ellipse(bx - size, by - size * .65, bx + size, by + size * .65, fill=1, stroke=0)


def draw_roots(c, x, ground, spread=48):
    c.setStrokeColor(Color(SOIL_DARK.red, SOIL_DARK.green, SOIL_DARK.blue, alpha=.78))
    c.setLineCap(1)
    for dx, bend in ((-spread, -12), (-spread * .62, -6), (spread * .62, 7), (spread, 13)):
        p = c.beginPath()
        p.moveTo(x, ground + 1)
        p.curveTo(x + bend * .25, ground - 13, x + dx * .55, ground - 27, x + dx, ground - 43)
        c.setLineWidth(3.4 if abs(dx) < spread else 2.6)
        c.drawPath(p, fill=0, stroke=1)


def draw_leaf(c, x, y, width, height, angle, color):
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    p = c.beginPath()
    p.moveTo(-width / 2, 0)
    p.curveTo(-width * .18, height * .55, width * .24, height * .42, width / 2, 0)
    p.curveTo(width * .20, -height * .50, -width * .20, -height * .42, -width / 2, 0)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def draw_leafy_tree(c, x, ground, height, fruitful=False, scale=1.0, lean=0):
    top = ground + height
    draw_tapered_trunk(c, x, ground, top - 18 * scale, lean)

    endpoints = [
        (-45, .64, -7), (-42, .76, -5), (-31, .87, -3), (-15, .95, -1),
        (2, 1.00, 0), (20, .93, 2), (35, .82, 4), (45, .69, 6),
    ]
    for dx, frac, bend in endpoints:
        sx = x + lean * .55
        sy = ground + height * (.48 if abs(dx) > 38 else .55)
        ex = x + dx * scale + lean
        ey = ground + height * frac
        draw_branch(c, [(sx, sy), (sx + dx * .25, sy + 13), (ex - dx * .20, ey - 8), (ex, ey)], 2.7 * scale)

    colors = (LEAF_DARK, LEAF_MID, LEAF_LIGHT)
    leaves = [
        (-46, .65, -20), (-39, .72, 18), (-45, .79, -8), (-31, .82, 28),
        (-33, .89, -25), (-20, .91, 12), (-14, .98, -12), (-2, 1.02, 20),
        (10, .98, -18), (21, .95, 23), (29, .89, -20), (38, .84, 14),
        (46, .72, -16), (40, .66, 22), (-22, .72, -6), (-8, .78, 17),
        (7, .75, -18), (23, .78, 7), (0, .88, -4), (17, .86, 24),
    ]
    if fruitful:
        leaves += [(-48, .72, 12), (-27, .78, -18), (-9, .91, 26), (28, .73, -9), (43, .79, 20), (9, .82, 8)]

    for idx, (dx, frac, angle) in enumerate(leaves):
        draw_leaf(c, x + dx * scale + lean, ground + height * frac, 15 * scale, 8.5 * scale, angle, colors[idx % 3])

    if fruitful:
        for dx, frac, radius in ((-31, .78, 4.2), (-11, .90, 4.0), (14, .82, 4.4), (34, .75, 4.0), (3, .72, 3.8)):
            c.setFillColor(FRUIT)
            c.circle(x + dx * scale + lean, ground + height * frac, radius * scale, fill=1, stroke=0)


def draw_seedling(c, x, ground, height, color=LEAF_MID):
    c.setStrokeColor(color)
    c.setLineWidth(3.4)
    c.setLineCap(1)
    c.line(x, ground, x, ground + height)
    c.setFillColor(LEAF_LIGHT)
    c.ellipse(x - 12, ground + height - 1, x, ground + height + 7, fill=1, stroke=0)
    c.setFillColor(color)
    c.ellipse(x, ground + height - 4, x + 13, ground + height + 4, fill=1, stroke=0)


def stage(c, title, body, x, y, width):
    c.setFillColor(DARK_FOREST)
    c.setFont("Georgia-Bold", 10.2)
    c.drawCentredString(x + width / 2, y + 41, title)
    style = ParagraphStyle(
        f"stage-{title}",
        fontName="Arial",
        fontSize=8.5,
        leading=10.4,
        textColor=INK,
        alignment=TA_CENTER,
    )
    paragraph(c, body, x, y + 29, width, style)


def draw_landscape(c):
    x0, y0, w, h = 24, 181, 744, 277
    c.setFillColor(PALE_SAGE)
    c.setStrokeColor(HexColor("#B9C8BE"))
    c.setLineWidth(.8)
    c.roundRect(x0, y0, w, h, 12, fill=1, stroke=1)

    c.setFillColor(FOREST)
    c.setFont("Arial-Bold", 8.1)
    c.drawCentredString(396, 438, "A PICTURE OF SEASONS, NOT A SCORECARD")
    ground = 270
    c.setFillColor(SOIL)
    p = c.beginPath()
    p.moveTo(x0, ground)
    p.curveTo(130, ground + 8, 224, ground - 4, 322, ground + 3)
    p.curveTo(430, ground + 11, 522, ground - 5, 620, ground + 2)
    p.curveTo(684, ground + 8, 730, ground + 4, x0 + w, ground + 5)
    p.lineTo(x0 + w, y0)
    p.lineTo(x0, y0)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(Color(SOIL_DARK.red, SOIL_DARK.green, SOIL_DARK.blue, alpha=.16))
    c.setLineWidth(.7)
    for offset in (31, 56):
        contour = c.beginPath()
        contour.moveTo(x0 + 28, ground - offset)
        contour.curveTo(210, ground - offset + 8, 330, ground - offset - 5, 470, ground - offset + 3)
        contour.curveTo(575, ground - offset + 8, 680, ground - offset - 3, x0 + w - 28, ground - offset + 2)
        c.drawPath(contour, fill=0, stroke=1)

    # Rooted
    draw_roots(c, 98, ground, 50)
    draw_bare_tree(c, 98, ground, 132, buds=False, lean=-2)

    # Awakening
    draw_roots(c, 247, ground, 38)
    draw_bare_tree(c, 247, ground, 118, buds=True, lean=3)

    # Flourishing
    draw_roots(c, 396, ground, 33)
    draw_leafy_tree(c, 396, ground, 130, fruitful=False, lean=-2)

    # Fruitful
    draw_roots(c, 545, ground, 34)
    draw_leafy_tree(c, 545, ground, 137, fruitful=True, lean=2)
    c.setFillColor(FRUIT)
    c.ellipse(586, 286, 594, 299, fill=1, stroke=0)

    # Multiplying
    draw_roots(c, 660, ground, 30)
    draw_leafy_tree(c, 660, ground, 127, fruitful=True, scale=.94, lean=-2)
    c.setFillColor(FRUIT)
    c.ellipse(708, 293, 716, 306, fill=1, stroke=0)
    draw_seedling(c, 724, ground, 37)
    draw_seedling(c, 748, ground, 24, color=LEAF_DARK)


def build():
    register_fonts()
    c = canvas.Canvas(str(OUTPUT), pagesize=PAGE, pageCompression=1, initialFontName="Arial")
    c.setTitle("Rooted. Renewed. Multiplying Life. - V6")
    c.setSubject("A Christ-centered picture of renewal, fruit, and multiplication across changing seasons")
    c.setAuthor("James Akers")

    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE[0], PAGE[1], fill=1, stroke=0)

    c.setFillColor(HexColor("#8A5C00"))
    c.setFont("Arial-Bold", 8.4)
    c.drawString(31, 585, "ROOTED. RENEWED. MULTIPLYING LIFE.")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(31, 576, 82, 576)

    c.setFillColor(DARK_FOREST)
    c.setFont("Georgia-Bold", 27)
    c.drawString(31, 540, "Bare is not the same as dead.")
    c.setFillColor(INK)
    c.setFont("Georgia", 11.4)
    c.drawString(32, 514, "What looks dormant may still be deeply rooted in Christ.")

    c.setFillColor(FOREST)
    c.roundRect(24, 472, 744, 30, 8, fill=1, stroke=0)
    statement = ParagraphStyle("statement", fontName="Arial", fontSize=9.3, leading=11, textColor=WHITE, alignment=TA_CENTER)
    paragraph(c, "Life does not begin when leaves appear. Where roots remain alive in Christ, God may already be sustaining what has not yet become visible.", 50, 492, 692, statement)

    draw_landscape(c)

    starts = [28, 177, 326, 475, 624]
    bodies = [
        ("Rooted", "The roots may be holding more life than anyone can see."),
        ("Awakening", "New life begins to break through."),
        ("Flourishing", "Healthy systems make room for people to grow and breathe."),
        ("Fruitful", "The life of Christ becomes visible in people, relationships, and service."),
        ("Multiplying", "Life takes root beyond the original tree."),
    ]
    for start, (title, body) in zip(starts, bodies):
        stage(c, title, body, start, 93, 140)

    c.setFillColor(DARK_FOREST)
    c.roundRect(24, 16, 744, 55, 9, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 7.7)
    c.drawString(38, 52, "THE HEARTBEAT")
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 9.8)
    c.drawString(121, 50.5, "Systems do not create life. Jesus does. Healthy systems make room for the life He is already growing.")
    c.setFillColor(HexColor("#CAD7D1"))
    c.setFont("Arial", 7.6)
    c.drawRightString(755, 28, "John 15:1-5  |  John 7:37-39  |  Matthew 13:23  |  Mark 4:26-32")

    c.save()


if __name__ == "__main__":
    build()
