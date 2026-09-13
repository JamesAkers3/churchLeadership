from pathlib import Path
from math import cos, radians, sin

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from build_v2_visuals import (
    CREAM,
    DARK_FOREST,
    FOREST,
    GOLD,
    INK,
    MUTED,
    PAPER,
    TEXT_GOLD,
    WHITE,
    draw_impact,
    draw_lens,
    draw_source,
    kicker,
    register_fonts,
)


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output" / "pdf" / "from-passion-to-impact-v3.pdf"
RUST = HexColor("#B85F3D")
PALE_SAGE = HexColor("#E8EEDF")
PALE_RUST = HexColor("#F2E5DA")
OUTLINE = HexColor("#9AA39D")


def paragraph(c, text, x, y_top, width, style):
    p = Paragraph(text, style)
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - height)
    return height


def panel_header(c, title, equation, y, color):
    c.setFillColor(color)
    c.setFont("Arial-Bold", 9.2)
    c.drawString(59, y, title)
    c.setFont("Arial-Bold", 9.2)
    c.drawRightString(553, y, equation)


def stage(c, x, y, width, title, body, title_color=FOREST):
    style = ParagraphStyle(
        "stage",
        fontName="Arial",
        fontSize=8.5,
        leading=10.8,
        textColor=INK,
        alignment=TA_CENTER,
    )
    html = (
        f'<font name="Arial-Bold" color="{title_color.hexval()}" size="8.8">'
        f"{title}</font><br/>{body}"
    )
    paragraph(c, html, x, y, width, style)


def beam_lines(c, x1, x2, y, color):
    c.setStrokeColor(color)
    c.setLineWidth(3.4)
    for offset in (-15, -5, 5, 15):
        c.line(x1, y + offset, x2, y + offset * 0.62)


def reflector(c, x, y, angle, color=FOREST, length=58, width=6):
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    c.setFillColor(color)
    c.roundRect(-width / 2, -length / 2, width, length, width / 2, fill=1, stroke=0)
    c.restoreState()


def dim_community(c, x, y):
    c.saveState()
    c.setStrokeColor(OUTLINE)
    c.setLineWidth(1.4)
    c.rect(x - 28, y + 5, 25, 27, fill=0, stroke=1)
    roof = c.beginPath()
    roof.moveTo(x - 34, y + 32)
    roof.lineTo(x - 16, y + 48)
    roof.lineTo(x + 2, y + 32)
    c.drawPath(roof, fill=0, stroke=1)
    c.line(x - 16, y + 48, x - 16, y + 58)
    c.line(x - 20, y + 54, x - 12, y + 54)
    for px, py in [(x + 18, y + 16), (x + 35, y + 10), (x + 50, y + 20)]:
        c.circle(px, py + 12, 4, fill=0, stroke=1)
        c.line(px, py + 8, px, py - 3)
    c.restoreState()


def aligned_journey(c):
    c.setFillColor(PALE_SAGE)
    c.roundRect(42, 422, 528, 201, 14, fill=1, stroke=0)
    panel_header(
        c,
        "FOCUSED IMPACT",
        "PASSION + VISION x MISSION = FOCUSED IMPACT",
        595,
        FOREST,
    )

    y = 520
    draw_source(c, 93, y)
    beam_lines(c, 127, 181, y, Color(0.84, 0.63, 0.23, alpha=0.55))
    draw_lens(c, 205, y, 92)

    c.setFillColor(Color(0.84, 0.63, 0.23, alpha=0.35))
    focused = c.beginPath()
    focused.moveTo(219, y - 28)
    focused.lineTo(329, y)
    focused.lineTo(219, y + 28)
    focused.close()
    c.drawPath(focused, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(219, y, 329, y)

    reflector(c, 341, y, 45, FOREST, 68, 7)
    c.setFillColor(Color(0.84, 0.63, 0.23, alpha=0.31))
    landing = c.beginPath()
    landing.moveTo(345, y - 2)
    landing.lineTo(480, 452)
    landing.lineTo(459, 435)
    landing.close()
    c.drawPath(landing, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(345, y - 2, 469, 445)
    draw_impact(c, 490, 433)

    stage(c, 55, 459, 76, "PASSION", "creates the energy")
    stage(c, 161, 459, 88, "VISION", "brings it into focus")
    stage(c, 291, 459, 100, "MISSION", "points it somewhere that matters")
    stage(c, 451, 512, 100, "IMPACT", "happens where it lands")


def scattered_journey(c):
    c.setFillColor(PALE_RUST)
    c.roundRect(42, 192, 528, 211, 14, fill=1, stroke=0)
    panel_header(
        c,
        "SCATTERED ENERGY",
        "PASSION - VISION / MISSION = SCATTERED ENERGY",
        375,
        RUST,
    )

    y = 300
    draw_source(c, 93, y)
    beam_lines(c, 127, 181, y, Color(0.84, 0.63, 0.23, alpha=0.55))
    draw_lens(c, 205, y, 92, cracked=True)

    # The cracked lens sends the same energy in several directions.
    c.setStrokeColor(RUST)
    c.setLineWidth(1.8)
    distorted = [(219, 300, 319, 329), (219, 300, 333, 300), (219, 300, 319, 270)]
    for x1, y1, x2, y2 in distorted:
        c.line(x1, y1, x2, y2)

    # Competing reflectors divide the direction again.
    reflector(c, 331, 329, 54, FOREST, 48, 5)
    reflector(c, 345, 300, 12, FOREST, 48, 5)
    reflector(c, 331, 270, -38, FOREST, 48, 5)

    c.setStrokeColor(RUST)
    c.setLineWidth(1.5)
    c.setDash(4, 3)
    c.line(338, 329, 445, 364)
    c.line(350, 300, 458, 303)
    c.line(338, 270, 438, 228)
    c.setDash()

    # The community is present but no focused beam reaches it.
    dim_community(c, 493, 255)

    stage(c, 55, 238, 76, "PASSION", "the energy is still there", RUST)
    stage(c, 154, 238, 102, "DISTORTED VISION", "sends it off course", RUST)
    stage(c, 286, 238, 110, "COMPETING MISSIONS", "divide the direction", RUST)
    stage(c, 446, 238, 105, "SCATTERED ENERGY", "loses strength before it lands", RUST)


def build():
    register_fonts()
    c = canvas.Canvas(
        str(OUTPUT),
        pagesize=LETTER,
        pageCompression=1,
        initialFontName="Arial",
    )
    c.setTitle("From Passion to Impact - V3")
    c.setSubject("Two complete visual journeys: focused impact and scattered energy")
    c.setAuthor("James Akers")

    c.setFillColor(PAPER)
    c.rect(0, 0, LETTER[0], LETTER[1], fill=1, stroke=0)

    kicker(c, "From Passion to Impact", 42, 751)
    c.setFillColor(DARK_FOREST)
    c.setFont("Georgia-Bold", 26)
    c.drawString(42, 707, "Passion is powerful.")
    opening = ParagraphStyle(
        "opening",
        fontName="Georgia",
        fontSize=12.2,
        leading=16.5,
        textColor=INK,
        alignment=TA_LEFT,
    )
    paragraph(
        c,
        "But without vision to focus it and mission to move it, passion becomes scattered energy.",
        43,
        682,
        520,
        opening,
    )

    aligned_journey(c)
    scattered_journey(c)

    c.setFillColor(DARK_FOREST)
    c.roundRect(42, 61, 528, 100, 12, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 8)
    c.drawString(58, 139, "THE HEARTBEAT")
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 12.2)
    c.drawString(58, 113, "Passion creates the energy. Vision brings it into focus.")
    c.drawString(58, 93, "Mission points it somewhere that matters. Impact happens where it lands.")
    c.setFillColor(HexColor("#D8E1DB"))
    c.setFont("Arial", 8.4)
    c.drawString(58, 75, "Jesus knew why He came. He prayed, chose where to go next, and did not let the crowd choose His mission.")

    c.setFillColor(MUTED)
    c.setFont("Arial", 7.8)
    c.drawRightString(554, 35, "Mark 1:35-39")
    c.save()


if __name__ == "__main__":
    build()
