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
OUTPUT = ROOT / "output" / "pdf" / "rooted-renewed-multiplying-life-v4.pdf"

PAGE = (792.0, 684.9)
BLACK = HexColor("#151716")
FOREST = HexColor("#15483D")
DARK_FOREST = HexColor("#0D382F")
CREAM = HexColor("#FBF7EC")
INK = HexColor("#26362F")
MUTED = HexColor("#5F6C66")
GOLD = HexColor("#EDB63D")
PALE_GOLD = HexColor("#F5E2AC")
WHITE = HexColor("#FFFDF6")


def paragraph(c, text, x, y_top, width, style):
    p = Paragraph(text, style)
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - height)
    return height


def stage(c, number, title, body, x, y, width):
    c.setFillColor(DARK_FOREST)
    c.circle(x + 11, y + 77, 10, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Arial-Bold", 7.8)
    c.drawCentredString(x + 11, y + 74.3, str(number))

    c.setFillColor(DARK_FOREST)
    c.setFont("Georgia-Bold", 10.5)
    c.drawString(x, y + 55, title)

    style = ParagraphStyle(
        f"stage-{number}",
        fontName="Arial",
        fontSize=7.8,
        leading=9.7,
        textColor=INK,
        alignment=TA_LEFT,
    )
    paragraph(c, body, x, y + 43, width, style)


def build():
    register_fonts()
    c = canvas.Canvas(
        str(OUTPUT),
        pagesize=PAGE,
        pageCompression=1,
        initialFontName="Arial",
    )
    c.setTitle("Rooted. Renewed. Multiplying Life. - V4")
    c.setSubject("The original renewal landscape with revised Christ-centered language")
    c.setAuthor("James Akers")

    width, height = PAGE

    # Preserve the original V1 illustration at its native page proportions.
    c.drawImage(ImageReader(str(SOURCE_ART)), 0, 0, width=width, height=height, mask="auto")

    # Rebuild the header as live type while leaving the original landscape untouched.
    c.setFillColor(BLACK)
    c.rect(0, 495, width, height - 495, fill=1, stroke=0)
    c.setFillColor(FOREST)
    c.roundRect(5, 506, width - 10, 168, 13, fill=1, stroke=0)
    c.setFillColor(PALE_GOLD)
    c.setFont("Arial-Bold", 8.2)
    c.drawString(23, 648, "ROOTED. RENEWED. MULTIPLYING LIFE.")

    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 27)
    c.drawString(23, 608, "Bare is not the same as dead.")

    c.setFillColor(WHITE)
    c.setFont("Arial-Bold", 11.2)
    c.drawString(23, 575, "What looks dormant may still be deeply rooted in Christ.")
    c.setFillColor(HexColor("#D8E5DF"))
    c.setFont("Arial", 9.8)
    c.drawString(23, 549, "Life does not begin when leaves appear. God was already sustaining it beneath the surface.")

    # Replace the dense five-column copy while keeping the original five-tree scene.
    c.setFillColor(BLACK)
    c.rect(0, 0, width, 180, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.roundRect(5, 10, width - 10, 160, 13, fill=1, stroke=0)

    card_width = 137
    starts = [18, 173, 328, 483, 638]
    stage(c, 1, "Rooted", "The roots are holding more life than anyone can see.", starts[0], 69, card_width)
    stage(c, 2, "Awakening", "New life begins to break through.", starts[1], 69, card_width)
    stage(c, 3, "Flourishing", "Healthy systems make room for people to grow and breathe.", starts[2], 69, card_width)
    stage(c, 4, "Fruitful", "The community begins to experience the fruit.", starts[3], 69, card_width)
    stage(c, 5, "Multiplying", "Life takes root beyond the original tree.", starts[4], 69, 130)

    # A quiet divider gives the Heartbeat its own place without competing with the art.
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(20, 58, width - 20, 58)
    c.setFillColor(DARK_FOREST)
    c.setFont("Arial-Bold", 7.6)
    c.drawString(20, 42, "THE HEARTBEAT")
    c.setFont("Georgia-Bold", 9.6)
    c.drawString(102, 40.5, "Systems do not create life. Jesus does. Healthy systems make room for the life He is already growing.")
    c.setFillColor(MUTED)
    c.setFont("Arial", 7.3)
    c.drawRightString(width - 20, 22, "John 15:1-5  |  John 7:37-39  |  Matthew 13:23  |  Mark 4:26-32")

    c.save()


if __name__ == "__main__":
    build()

