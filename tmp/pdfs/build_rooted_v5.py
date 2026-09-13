from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from build_v2_visuals import register_fonts


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
SOURCE_ART = ROOT / "tmp" / "pdfs" / "revision-clean" / "rooted-v1-source-000.png"
OUTPUT = ROOT / "output" / "pdf" / "rooted-renewed-multiplying-life-v5.pdf"

PAGE = (792.0, 612.0)
PAPER = HexColor("#FBF8EF")
FOREST = HexColor("#173F36")
DARK_FOREST = HexColor("#0D382F")
INK = HexColor("#293630")
MUTED = HexColor("#68736D")
GOLD = HexColor("#D5A13A")
WHITE = HexColor("#FFFDF6")


def paragraph(c, text, x, y_top, width, style):
    p = Paragraph(text, style)
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - height)
    return height


def stage(c, number, title, body, x, y, width):
    c.setFillColor(DARK_FOREST)
    c.circle(x + 9, y + 62, 8.5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Arial-Bold", 7)
    c.drawCentredString(x + 9, y + 59.7, str(number))

    c.setFillColor(DARK_FOREST)
    c.setFont("Georgia-Bold", 9.8)
    c.drawString(x, y + 44, title)

    style = ParagraphStyle(
        f"stage-{number}",
        fontName="Arial",
        fontSize=7.5,
        leading=9.1,
        textColor=INK,
        alignment=TA_LEFT,
    )
    paragraph(c, body, x, y + 33, width, style)


def draw_original_landscape(c):
    # Crop only the original V1 tree scene and move it higher on the page.
    # The full source remains untouched; clipping preserves the actual artwork.
    art_x = 16
    art_y = 174
    art_w = 760
    art_h = 302
    scale = 0.435

    clip = c.beginPath()
    clip.roundRect(art_x, art_y, art_w, art_h, 11)
    c.saveState()
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(
        ImageReader(str(SOURCE_ART)),
        13,
        1,
        width=1760 * scale,
        height=1522 * scale,
        mask="auto",
    )
    c.restoreState()
    c.setStrokeColor(HexColor("#B9C3B6"))
    c.setLineWidth(.8)
    c.roundRect(art_x, art_y, art_w, art_h, 11, fill=0, stroke=1)


def build():
    register_fonts()
    c = canvas.Canvas(
        str(OUTPUT),
        pagesize=PAGE,
        pageCompression=1,
        initialFontName="Arial",
    )
    c.setTitle("Rooted. Renewed. Multiplying Life. - V5")
    c.setSubject("A light editorial header paired with the original V1 renewal landscape")
    c.setAuthor("James Akers")

    width, height = PAGE
    c.setFillColor(PAPER)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # V3's lighter title treatment, tightened to give the artwork more room.
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

    # The former oversized header becomes a single, quiet statement band.
    c.setFillColor(FOREST)
    c.roundRect(16, 481, 760, 24, 7, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Arial", 9.2)
    c.drawCentredString(width / 2, 489.2, "Life does not begin when leaves appear. God was already sustaining it beneath the surface.")

    draw_original_landscape(c)

    # Simplified stage language beneath the original progression.
    starts = [22, 176, 330, 484, 638]
    card_width = 130
    stage(c, 1, "Rooted", "The roots are holding more life than anyone can see.", starts[0], 89, card_width)
    stage(c, 2, "Awakening", "New life begins to break through.", starts[1], 89, card_width)
    stage(c, 3, "Flourishing", "Healthy systems make room for people to grow and breathe.", starts[2], 89, card_width)
    stage(c, 4, "Fruitful", "The community begins to experience the fruit.", starts[3], 89, card_width)
    stage(c, 5, "Multiplying", "Life takes root beyond the original tree.", starts[4], 89, 128)

    # Heartbeat remains strong but no longer competes with the illustration.
    c.setFillColor(DARK_FOREST)
    c.roundRect(16, 16, 760, 50, 9, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 7.5)
    c.drawString(29, 48, "THE HEARTBEAT")
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 9.7)
    c.drawString(112, 46.7, "Systems do not create life. Jesus does. Healthy systems make room for the life He is already growing.")
    c.setFillColor(HexColor("#CAD7D1"))
    c.setFont("Arial", 7.1)
    c.drawRightString(763, 26, "John 15:1-5  |  John 7:37-39  |  Matthew 13:23  |  Mark 4:26-32")

    c.save()


if __name__ == "__main__":
    build()
