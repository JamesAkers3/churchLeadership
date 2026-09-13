from pathlib import Path
from math import cos, radians, sin

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from build_v2_visuals import (
    DARK_FOREST,
    FOREST,
    FRUIT,
    GOLD,
    INK,
    MOSS,
    MUTED,
    PAPER,
    PETAL,
    SOIL,
    SOIL_DARK,
    TEXT_GOLD,
    TEXT_MOSS,
    WHITE,
    flower,
    kicker,
    leaf,
    register_fonts,
)


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output" / "pdf" / "rooted-renewed-multiplying-life-v3.pdf"
PALE_SAGE = HexColor("#E8EEDF")
SOIL_LIGHT = HexColor("#E8D5B8")


def paragraph(c, text, x, y_top, width, style):
    p = Paragraph(text, style)
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - height)
    return height


def curve(c, start, controls, end, width, color=SOIL_DARK):
    p = c.beginPath()
    p.moveTo(*start)
    p.curveTo(*controls, *end)
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.setLineCap(1)
    c.drawPath(p, fill=0, stroke=1)


def branch(c, x1, y1, x2, y2, width):
    c.setStrokeColor(SOIL_DARK)
    c.setLineWidth(width)
    c.setLineCap(1)
    c.line(x1, y1, x2, y2)


def tree(c, x, ground_y, height, stage):
    scale = height / 170.0
    trunk_top = ground_y + height * 0.60
    crown_top = ground_y + height

    # Tapered trunk.
    trunk = c.beginPath()
    trunk.moveTo(x - 7 * scale, ground_y)
    trunk.curveTo(x - 6 * scale, ground_y + height * .22, x - 2 * scale, ground_y + height * .43, x, trunk_top)
    trunk.curveTo(x + 4 * scale, ground_y + height * .42, x + 7 * scale, ground_y + height * .20, x + 8 * scale, ground_y)
    trunk.close()
    c.setFillColor(SOIL_DARK)
    c.drawPath(trunk, fill=1, stroke=0)

    # Roots remain visible at every season.
    curve(
        c,
        (x - 2 * scale, ground_y + 1),
        (x - 14 * scale, ground_y - 7 * scale, x - 27 * scale, ground_y - 10 * scale),
        (x - 38 * scale, ground_y - 13 * scale),
        2.8 * scale,
    )
    curve(
        c,
        (x + 2 * scale, ground_y + 1),
        (x + 14 * scale, ground_y - 5 * scale, x + 28 * scale, ground_y - 7 * scale),
        (x + 39 * scale, ground_y - 13 * scale),
        2.8 * scale,
    )
    curve(
        c,
        (x, ground_y),
        (x - 2 * scale, ground_y - 10 * scale, x - 4 * scale, ground_y - 18 * scale),
        (x - 6 * scale, ground_y - 26 * scale),
        2.2 * scale,
    )

    # The same branch structure carries every stage.
    branch(c, x, trunk_top, x - 27 * scale, ground_y + height * .79, 4.6 * scale)
    branch(c, x, trunk_top + 5 * scale, x + 30 * scale, ground_y + height * .82, 4.6 * scale)
    branch(c, x - 11 * scale, ground_y + height * .70, x - 36 * scale, ground_y + height * .66, 3.2 * scale)
    branch(c, x + 12 * scale, ground_y + height * .71, x + 39 * scale, ground_y + height * .67, 3.2 * scale)
    branch(c, x - 2 * scale, ground_y + height * .75, x - 4 * scale, crown_top, 3.4 * scale)
    branch(c, x - 26 * scale, ground_y + height * .79, x - 38 * scale, ground_y + height * .91, 2.3 * scale)
    branch(c, x + 29 * scale, ground_y + height * .82, x + 40 * scale, ground_y + height * .94, 2.3 * scale)

    tips = [
        (x - 38 * scale, ground_y + height * .91),
        (x - 36 * scale, ground_y + height * .66),
        (x - 4 * scale, crown_top),
        (x + 40 * scale, ground_y + height * .94),
        (x + 39 * scale, ground_y + height * .67),
    ]

    if stage == 1:
        return

    if stage == 2:
        c.setFillColor(GOLD)
        for tx, ty in tips:
            c.circle(tx, ty, 3.2 * scale, fill=1, stroke=0)
        return

    leaf_positions = [
        (-34, .88, 18), (-30, .70, -18), (-17, .80, 24), (-7, .97, -12),
        (8, .87, 22), (23, .77, -18), (35, .91, 18), (36, .68, -22),
        (-2, .72, 12), (16, .95, -16), (-23, .94, 16), (27, .61, 20),
    ]
    if stage >= 4:
        leaf_positions += [(-42, .77, 12), (43, .80, -12), (-14, .62, -20), (12, .65, 24)]
    if stage >= 5:
        leaf_positions += [(-44, .99, 20), (45, .98, -18), (-35, .58, 12), (38, .58, -16)]

    for i, (dx, frac, angle) in enumerate(leaf_positions):
        color = MOSS if i % 2 == 0 else TEXT_MOSS
        leaf(c, x + dx * scale, ground_y + height * frac, .58 * scale, angle, color)

    if stage == 3:
        for dx, frac in [(-23, .85), (2, .91), (26, .82), (12, .69)]:
            flower(c, x + dx * scale, ground_y + height * frac, .62 * scale)

    if stage >= 4:
        c.setFillColor(FRUIT)
        for dx, frac in [(-22, .82), (7, .89), (27, .73), (-2, .66)]:
            c.circle(x + dx * scale, ground_y + height * frac, 4.5 * scale, fill=1, stroke=0)


def stage_label(c, x, y, width, title, body, color=FOREST):
    style = ParagraphStyle(
        "stage",
        fontName="Arial",
        fontSize=7.8,
        leading=9.8,
        textColor=INK,
        alignment=TA_CENTER,
    )
    html = f'<font name="Arial-Bold" color="{color.hexval()}" size="8.2">{title}</font><br/>{body}'
    paragraph(c, html, x - width / 2, y, width, style)


def sunlight(c):
    c.setFillColor(Color(0.84, 0.63, 0.23, alpha=.10))
    p = c.beginPath()
    p.moveTo(438, 617)
    p.lineTo(570, 617)
    p.lineTo(570, 343)
    p.lineTo(470, 376)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.circle(548, 586, 17, fill=1, stroke=0)
    c.setStrokeColor(TEXT_GOLD)
    c.setLineWidth(1)
    for angle in range(0, 360, 45):
        a = radians(angle)
        c.line(548 + cos(a) * 22, 586 + sin(a) * 22, 548 + cos(a) * 29, 586 + sin(a) * 29)


def build():
    register_fonts()
    c = canvas.Canvas(
        str(OUTPUT),
        pagesize=LETTER,
        pageCompression=1,
        initialFontName="Arial",
    )
    c.setTitle("Rooted. Renewed. Multiplying Life. - V3")
    c.setSubject("A continuous picture of renewal from rootedness to multiplication")
    c.setAuthor("James Akers")

    width, height = LETTER
    c.setFillColor(PAPER)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    kicker(c, "Rooted. Renewed. Multiplying Life.", 42, 750)
    c.setFillColor(DARK_FOREST)
    c.setFont("Georgia-Bold", 28)
    c.drawString(42, 703, "Bare is not the same as dead.")

    opening = ParagraphStyle(
        "opening",
        fontName="Georgia",
        fontSize=12.3,
        leading=16.5,
        textColor=INK,
        alignment=TA_LEFT,
    )
    paragraph(
        c,
        "Life does not begin when the leaves appear. God was already sustaining it beneath the surface.",
        43,
        678,
        520,
        opening,
    )

    # One continuous landscape makes the movement the main experience.
    c.setFillColor(PALE_SAGE)
    c.roundRect(42, 231, 528, 396, 15, fill=1, stroke=0)
    sunlight(c)

    ground_y = 335
    ground = c.beginPath()
    ground.moveTo(42, ground_y)
    ground.curveTo(160, ground_y + 8, 270, ground_y - 5, 380, ground_y + 4)
    ground.curveTo(470, ground_y + 10, 520, ground_y - 2, 570, ground_y + 3)
    ground.lineTo(570, 268)
    ground.lineTo(42, 268)
    ground.close()
    c.setFillColor(SOIL_LIGHT)
    c.drawPath(ground, fill=1, stroke=0)
    c.setStrokeColor(SOIL)
    c.setLineWidth(1.3)
    c.line(42, ground_y, 570, ground_y)

    positions = [
        (89, 104, 1),
        (188, 128, 2),
        (294, 158, 3),
        (408, 190, 4),
        (505, 222, 5),
    ]
    for x, tree_height, stage_number in positions:
        tree(c, x, ground_y, tree_height, stage_number)

    # Multiplication moves beyond the final tree.
    c.setStrokeColor(TEXT_GOLD)
    c.setLineWidth(1.2)
    c.setDash(3, 3)
    seed_path = c.beginPath()
    seed_path.moveTo(524, 478)
    seed_path.curveTo(560, 459, 565, 413, 550, 374)
    c.drawPath(seed_path, fill=0, stroke=1)
    c.setDash()
    for sx, sy, angle in [(545, 443, -20), (558, 417, -32), (552, 389, -18)]:
        leaf(c, sx, sy, .32, angle, TEXT_GOLD)
    for sx, sh in [(542, 25), (562, 38)]:
        c.setStrokeColor(TEXT_MOSS)
        c.setLineWidth(2)
        c.line(sx, ground_y, sx, ground_y + sh)
        leaf(c, sx - 4, ground_y + sh - 7, .42, 25, MOSS)
        leaf(c, sx + 5, ground_y + sh, .42, -22, TEXT_MOSS)

    # A shared visual foundation reinforces that visible seasons do not create the life.
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.2)
    c.line(68, 288, 544, 288)
    c.setFillColor(TEXT_GOLD)
    c.setFont("Arial-Bold", 7.8)
    c.drawCentredString(width / 2, 276, "ROOTED IN CHRIST")

    stage_label(c, 89, 257, 82, "ROOTED", "life held beneath the surface")
    stage_label(c, 188, 257, 86, "AWAKENING", "the first signs begin to emerge", TEXT_GOLD)
    stage_label(c, 294, 257, 88, "FLOURISHING", "life has room to grow")
    stage_label(c, 408, 257, 84, "FRUITFUL", "others begin to receive it", FRUIT)
    stage_label(c, 517, 257, 94, "MULTIPLYING", "life takes root beyond itself", TEXT_MOSS)

    c.setFillColor(MUTED)
    c.setFont("Arial", 8.7)
    c.drawCentredString(width / 2, 202, "A picture of health - not a scorecard of size, speed, or season.")

    c.setFillColor(DARK_FOREST)
    c.roundRect(42, 62, 528, 105, 12, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 8)
    c.drawString(58, 143, "THE HEARTBEAT")
    heartbeat = ParagraphStyle(
        "heartbeat",
        fontName="Georgia-Bold",
        fontSize=12.6,
        leading=16.5,
        textColor=WHITE,
        alignment=TA_LEFT,
    )
    paragraph(
        c,
        "Systems do not create life. Jesus does. Healthy systems make room for the life He is already growing.",
        58,
        130,
        494,
        heartbeat,
    )
    c.setFillColor(HexColor("#D8E1DB"))
    c.setFont("Arial", 8.2)
    c.drawString(58, 77, "The roots matter even when the branches look bare.")

    c.setFillColor(MUTED)
    c.setFont("Arial", 7.7)
    c.drawCentredString(width / 2, 35, "John 15:1-5  |  John 7:37-39  |  Matthew 13:23  |  Mark 4:26-32")
    c.save()


if __name__ == "__main__":
    build()
