"""An editorial, Christ-centered relationship page; preserves all earlier PDFs."""

from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from build_christ_center_pdf_v2 import (
    CREAM, FOREST, INK, MOSS, MUTED, PAPER, WHITE,
    register_fonts, style, tracking_text,
)
from reportlab.platypus import Paragraph


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output/pdf/christ-at-the-center-1-3-12-v3.pdf"
PLACEMENTS = []


def paragraph(pdf, text, font, size, leading, color, x, top, width,
              centered=False, floor=0):
    item = Paragraph(text, style(
        "text", font, size, leading, color,
        alignment=TA_CENTER if centered else 0,
    ))
    _, height = item.wrap(width, 1000)
    bottom = top - height
    assert bottom >= floor, (text, bottom, floor)
    item.drawOn(pdf, x, bottom)
    PLACEMENTS.append((text, x, bottom, width, height))
    return bottom


def build():
    register_fonts()
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle("Who Are You Bringing With You? | Christ at the Center | v3")
    pdf.setAuthor("James Akers")
    pdf.setSubject("1-3-12: a relational reflection, not a prescribed headcount")
    pdf.setFillColor(CREAM)
    pdf.rect(0, 0, 612, 792, fill=1, stroke=0)
    left, width = 42, 528

    tracking_text(pdf, "CHRIST AT THE CENTER / 1-3-12", left, 751,
                  size=8, gap=1.4)
    paragraph(pdf, "Who Are You Bringing<br/>With You?", "Georgia-Bold",
              34, 38, FOREST, left, 728, width, floor=648)
    paragraph(
        pdf,
        "Jesus brought people close. They watched Him, asked questions, "
        "made mistakes, and learned. Then He entrusted them with real ministry.",
        "Helvetica", 11.2, 15.5, INK, left, 630, width, floor=590,
    )
    paragraph(pdf, "MARK 3:14-15 / MARK 6:7, 30-31", "Helvetica-Bold",
              8, 10, MOSS, left, 590, width)

    # One shared foundation; no arrows, ranked rings, or numbered steps.
    pdf.setFillColor(FOREST)
    pdf.roundRect(left, 443, width, 115, 10, fill=1, stroke=0)
    paragraph(pdf, "Christ at the center.", "Georgia-Bold", 24, 28,
              WHITE, left + 22, 533, width - 44, centered=True)
    paragraph(
        pdf,
        "The Pastor and the people being formed are all disciples of Jesus.<br/>"
        "We remain in Him and depend on the Holy Spirit.",
        "Helvetica", 10.1, 13.5, WHITE, left + 22, 495, width - 44,
        centered=True, floor=451,
    )

    sections = [
        ("1", "Your own walk.",
         "Before considering who you lead, how are you following Jesus?",
         "JOHN 15:5 / 1 TIMOTHY 4:16"),
        ("3", "People you trust.",
         "Who can pray with you, speak honestly, and see beyond the demands of ministry?",
         "MARK 14:33-34 / GALATIANS 6:2"),
        ("12", "People you’re forming.",
         "Who is learning beside you, and what are you helping them become ready to carry?",
         "MARK 3:14-15 / MARK 6:7"),
    ]
    gap = 21
    column = (width - gap * 2) / 3
    for index, (number, heading, question, scripture) in enumerate(sections):
        x = left + index * (column + gap)
        paragraph(pdf, number, "Helvetica-Bold", 48, 52, FOREST,
                  x, 417, column, centered=True)
        paragraph(pdf, heading, "Helvetica-Bold", 13.2, 17, FOREST,
                  x, 353, column, centered=True, floor=332)
        paragraph(pdf, question, "Helvetica", 10.5, 14, INK,
                  x + 2, 320, column - 4, centered=True, floor=248)
        paragraph(pdf, scripture, "Helvetica-Bold", 7.2, 9.5, MOSS,
                  x, 243, column, centered=True, floor=219)

    paragraph(
        pdf,
        "Peter, James, and John belonged to the Twelve. The numbers help us "
        "consider our relationships; they are not ranks or required headcounts. "
        "Trusted support may also come from outside your church.",
        "Helvetica", 8.7, 12, MUTED, left + 9, 209, width - 18,
        centered=True, floor=179,
    )

    pdf.setFillColor(PAPER)
    pdf.roundRect(left, 73, width, 91, 10, fill=1, stroke=0)
    paragraph(
        pdf,
        "Who could you invite closer?<br/>What could you begin entrusting to them?",
        "Georgia-Bold", 18, 23, FOREST, left + 22, 150, width - 44,
        floor=102,
    )
    paragraph(pdf, "Pray. Put a name to it. Begin with one conversation.",
              "Helvetica", 10, 13, INK, left + 22, 94, width - 44, floor=80)

    paragraph(
        pdf,
        "Scripture: John 15:5; 1 Timothy 4:16; Mark 3:14-15; 5:37; 6:7, 30-31; "
        "9:2; 14:33-34; Galatians 6:2; Acts 1:8.",
        "Helvetica", 7.5, 10, MUTED, left, 49, width, floor=29,
    )
    pdf.showPage()
    pdf.save()
    for text, x, bottom, block_width, height in PLACEMENTS:
        assert 42 <= x and x + block_width <= 570
        assert 29 <= bottom and bottom + height <= 751
    print(f"Built {OUTPUT}; {len(PLACEMENTS)} text blocks within layout bounds.")


if __name__ == "__main__":
    build()
