"""A relational, emotionally grounded page after James' and Tim's feedback."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from build_1_3_12_redesign_v3 import paragraph, PLACEMENTS


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output/pdf/christ-at-the-center-1-3-12-v5.pdf"
PAPER = HexColor("#F4F0E3")
FOREST = HexColor("#173F36")
INK = HexColor("#293630")
OCHRE = HexColor("#85602B")
MUTED = HexColor("#56635D")


def build():
    for name, path, index in [
        ("Book-Bold", "/System/Library/Fonts/Supplemental/Baskerville.ttc", 1),
        ("Human", "/System/Library/Fonts/Optima.ttc", 0),
        ("Human-Bold", "/System/Library/Fonts/Optima.ttc", 1),
    ]:
        pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))
    PLACEMENTS.clear()
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle("Who Are You Bringing With You? | Christ at the Center | v5")
    pdf.setAuthor("James Akers")
    pdf.setSubject("Following Jesus, shared life, and people entrusted with ministry")
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, 612, 792, fill=1, stroke=0)
    left, width, text_left, text_width = 42, 528, 103, 467

    paragraph(pdf, "CHRIST AT THE CENTER / 1-3-12", "Human-Bold", 8.8, 11,
              OCHRE, left, 760, width)
    paragraph(pdf, "Who Are You Bringing<br/>With You?", "Book-Bold", 36, 39,
              FOREST, left, 730, width, floor=650)
    paragraph(
        pdf,
        "Jesus walked closely with the Twelve. Within that shared life, Peter, "
        "James, and John came nearer in moments of power, glory, and sorrow. "
        "He entrusted ministry to people who were still learning.",
        "Human", 11.5, 15.5, INK, left, 632, width, floor=583,
    )

    paragraph(pdf, "Christ at the center.", "Book-Bold", 24, 28,
              FOREST, left, 568, width)
    paragraph(
        pdf,
        "Pastor, we are all disciples of Jesus. We remain in Him "
        "and depend on the Holy Spirit.",
        "Human", 11.5, 15, INK, left, 531, width, floor=500,
    )
    paragraph(pdf, "JOHN 15:5 / ACTS 1:8", "Human-Bold", 8.5, 11,
              MUTED, left, 494, width)

    # Numbers introduce relationships, not statistics or a staffing chart.
    for number, top in [("1", 465), ("3", 358), ("12", 224)]:
        paragraph(pdf, number, "Human-Bold", 32, 36, OCHRE,
                  left, top, 45)

    paragraph(pdf, "Remain in Him.", "Book-Bold", 22, 25,
              FOREST, text_left, 461, text_width, floor=433)
    paragraph(
        pdf,
        "Ministry can fill a day and leave little room to be with Jesus. "
        "Where are you making room to follow Him, without preparing "
        "something for everyone else?",
        "Human", 11.5, 15, INK, text_left, 427, text_width, floor=382,
    )
    paragraph(pdf, "JOHN 15:5 / 1 TIMOTHY 4:16", "Human-Bold", 8.5, 11,
              MUTED, text_left, 372, text_width)

    paragraph(pdf, "Let someone know you.", "Book-Bold", 22, 25,
              FOREST, text_left, 354, text_width)
    paragraph(
        pdf,
        "The crowd may see what the Pastor carries. Let someone you trust "
        "see what it costs.",
        "Book-Bold", 13.5, 17, FOREST, text_left, 320, text_width, floor=285,
    )
    paragraph(pdf, "Who can you invite into an honest conversation?",
              "Human", 11.5, 15, INK, text_left, 278, text_width)
    paragraph(pdf, "MARK 5:37 / 9:2 / 14:32-42 / GALATIANS 6:2",
              "Human-Bold", 8.5, 11, MUTED, text_left, 254, text_width)

    paragraph(pdf, "Bring people close. Entrust real ministry.", "Book-Bold",
              21, 24, FOREST, text_left, 220, text_width, floor=195)
    paragraph(
        pdf,
        "They learned beside Jesus before He sent them together. "
        "Who are you helping follow Him, and what ministry could you "
        "entrust as they grow?",
        "Human", 11.5, 15, INK, text_left, 187, text_width, floor=141,
    )
    paragraph(pdf, "MARK 3:14-15 / MARK 6:7, 30-31", "Human-Bold", 8.5, 11,
              MUTED, text_left, 132, text_width)

    pdf.setStrokeColor(OCHRE)
    pdf.setLineWidth(0.8)
    pdf.line(left, 110, left + width, 110)
    paragraph(pdf, "Who could you invite closer?", "Book-Bold", 23, 27,
              FOREST, left, 98, width, floor=70)
    paragraph(
        pdf,
        "Ask the Holy Spirit which relationship needs your attention.<br/>"
        "Begin with one honest conversation.",
        "Human", 11, 14, INK, left, 62, width, floor=33,
    )
    for text, x, bottom, block_width, height in PLACEMENTS:
        assert 42 <= x and x + block_width <= 570, text
        assert 33 <= bottom and bottom + height <= 760, text
    pdf.showPage()
    pdf.save()
    print(f"Built {OUTPUT}; {len(PLACEMENTS)} bounded text blocks.")


if __name__ == "__main__":
    build()
