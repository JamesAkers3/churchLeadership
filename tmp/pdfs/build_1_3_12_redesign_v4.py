"""The approved QA polish; all earlier PDFs remain unchanged."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from build_christ_center_pdf_v2 import (
    CREAM, FOREST, INK, MUTED, PAPER, register_fonts, tracking_text,
)
from build_1_3_12_redesign_v3 import paragraph, PLACEMENTS


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output/pdf/christ-at-the-center-1-3-12-v4.pdf"


def build():
    register_fonts()
    PLACEMENTS.clear()
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle("Who Are You Bringing With You? | Christ at the Center | v4")
    pdf.setAuthor("James Akers")
    pdf.setSubject("A Christ-centered relationship reflection, not prescribed headcounts")
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
        "made mistakes, and learned. He entrusted them with real ministry "
        "while they were still learning.",
        "Helvetica", 11.2, 15.5, INK, left, 630, width, floor=590,
    )
    paragraph(pdf, "MARK 3:14-15 / MARK 6:7, 30-31", "Helvetica-Bold",
              8.5, 11, FOREST, left, 589, width)

    # A gentle common foundation, with the same theological prominence.
    pdf.setFillColor(HexColor("#E1E8D9"))
    pdf.roundRect(left, 468, width, 90, 10, fill=1, stroke=0)
    paragraph(pdf, "Christ at the center.", "Georgia-Bold", 24, 28,
              FOREST, left + 22, 543, width - 44, centered=True)
    paragraph(
        pdf,
        "The Pastor and the people being formed are all disciples of Jesus.<br/>"
        "We remain in Him and depend on the Holy Spirit.",
        "Helvetica", 10.1, 13.5, INK, left + 22, 508, width - 44,
        centered=True, floor=480,
    )
    paragraph(
        pdf, "These are relationships, not ranks or required headcounts.",
        "Helvetica-Bold", 10, 13, FOREST, left, 447, width, centered=True,
    )

    sections = [
        ("1", "Your own walk.",
         "As you lead others, how are you following Jesus?",
         "JOHN 15:5 / 1 TIMOTHY 4:16"),
        ("3", "People you trust.",
         "Who can pray with you, speak honestly, and see beyond the demands of ministry?",
         "MARK 14:32-42 / GALATIANS 6:2"),
        ("12", "People you’re forming.",
         "Who is learning to follow Jesus beside you, and what ministry "
         "could you entrust to them<br/>as they grow?",
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
        paragraph(pdf, scripture, "Helvetica-Bold", 8.5, 11, FOREST,
                  x, 232, column, centered=True, floor=210)

    paragraph(
        pdf,
        "Peter, James, and John belonged to the Twelve.<br/>"
        "Trusted support may also come from outside your church.",
        "Helvetica", 9.5, 13, INK, left + 9, 191, width - 18,
        centered=True, floor=164,
    )

    pdf.setFillColor(PAPER)
    pdf.roundRect(left, 73, width, 72, 10, fill=1, stroke=0)
    paragraph(pdf, "Who could you invite closer?", "Georgia-Bold", 20, 25,
              FOREST, left + 22, 132, width - 44, floor=106)
    paragraph(pdf, "Pray about who to invite closer. Begin with one conversation.",
              "Helvetica", 10.5, 14, INK, left + 22, 98, width - 44, floor=83)

    paragraph(
        pdf,
        "Scripture: John 15:5; 1 Timothy 4:16; Mark 3:14-15; 5:37; 6:7, 30-31; "
        "9:2; 14:32-42; Galatians 6:2; Acts 1:8.",
        "Helvetica", 8.5, 11, MUTED, left, 49, width, floor=27,
    )
    for text, x, bottom, block_width, height in PLACEMENTS:
        assert 42 <= x and x + block_width <= 570, text
        assert 27 <= bottom and bottom + height <= 751, text
    pdf.showPage()
    pdf.save()
    print(f"Built {OUTPUT}; {len(PLACEMENTS)} text blocks within layout bounds.")


if __name__ == "__main__":
    build()
