from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

import build_rooted_v6 as base


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
SOURCE_ART = ROOT / "docs" / "strategy" / "assets" / "rooted-botanical-panorama-v1.png"
OUTPUT = ROOT / "output" / "pdf" / "rooted-renewed-multiplying-life-v7.pdf"


def draw_landscape(c):
    x, y, width, height = 31, 198, 730, 243.3
    clip = c.beginPath()
    clip.roundRect(x, y, width, height, 11)
    c.saveState()
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(
        ImageReader(str(SOURCE_ART)),
        x,
        y,
        width=width,
        height=height,
        preserveAspectRatio=False,
        mask="auto",
    )
    c.restoreState()
    c.setStrokeColor(HexColor("#B9C8BE"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, width, height, 11, fill=0, stroke=1)


def build():
    base.register_fonts()
    c = canvas.Canvas(str(OUTPUT), pagesize=base.PAGE, pageCompression=1, initialFontName="Arial")
    c.setTitle("Rooted. Renewed. Multiplying Life. - V7")
    c.setSubject("A Christ-centered botanical picture of renewal, fruit, and multiplication across changing seasons")
    c.setAuthor("James Akers")

    c.setFillColor(base.PAPER)
    c.rect(0, 0, base.PAGE[0], base.PAGE[1], fill=1, stroke=0)

    c.setFillColor(HexColor("#8A5C00"))
    c.setFont("Arial-Bold", 8.4)
    c.drawString(31, 585, "ROOTED. RENEWED. MULTIPLYING LIFE.")
    c.setStrokeColor(base.GOLD)
    c.setLineWidth(1.2)
    c.line(31, 576, 82, 576)

    c.setFillColor(base.DARK_FOREST)
    c.setFont("Georgia-Bold", 27)
    c.drawString(31, 540, "Bare is not the same as dead.")
    c.setFillColor(base.INK)
    c.setFont("Georgia", 11.4)
    c.drawString(32, 514, "What looks dormant may still be deeply rooted in Christ.")

    c.setFillColor(base.FOREST)
    c.roundRect(31, 472, 730, 30, 8, fill=1, stroke=0)
    statement = ParagraphStyle(
        "statement",
        fontName="Arial",
        fontSize=9.3,
        leading=11,
        textColor=base.WHITE,
        alignment=TA_CENTER,
    )
    base.paragraph(
        c,
        "Life does not begin when leaves appear. Where roots remain alive in Christ, God may already be sustaining what has not yet become visible.",
        56,
        492,
        680,
        statement,
    )

    c.setFillColor(base.FOREST)
    c.setFont("Arial-Bold", 8.1)
    c.drawCentredString(396, 455, "A PICTURE OF SEASONS, NOT A SCORECARD")
    draw_landscape(c)

    centers = [96, 246, 396, 546, 696]
    bodies = [
        ("Rooted", "The roots may be holding more life than anyone can see."),
        ("Awakening", "New life begins to break through."),
        ("Flourishing", "Healthy systems make room for people to grow and breathe."),
        ("Fruitful", "The life of Christ becomes visible in people, relationships, and service."),
        ("Multiplying", "Life takes root beyond the original tree."),
    ]
    for center, (title, body) in zip(centers, bodies):
        base.stage(c, title, body, center - 70, 95, 140)

    c.setFillColor(base.DARK_FOREST)
    c.roundRect(31, 16, 730, 55, 9, fill=1, stroke=0)
    c.setFillColor(base.GOLD)
    c.setFont("Arial-Bold", 7.7)
    c.drawString(45, 52, "THE HEARTBEAT")
    c.setFillColor(base.WHITE)
    c.setFont("Georgia-Bold", 9.8)
    c.drawString(128, 50.5, "Systems do not create life. Jesus does. Healthy systems make room for the life He is already growing.")
    c.setFillColor(HexColor("#CAD7D1"))
    c.setFont("Arial", 7.6)
    c.drawRightString(748, 28, "John 15:1-5  |  John 7:37-39  |  Matthew 13:23  |  Mark 4:26-32")

    c.save()


if __name__ == "__main__":
    build()
