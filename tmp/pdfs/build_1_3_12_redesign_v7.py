"""Approved sending-language and conversational closing refinement."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from build_1_3_12_redesign_v5 import (
    ROOT, PAPER, FOREST, INK, OCHRE, MUTED, paragraph, PLACEMENTS,
)

OUTPUT = ROOT / "output/pdf/christ-at-the-center-1-3-12-v7.pdf"


def build():
    for name, path, index in [
        ("Book-Bold", "/System/Library/Fonts/Supplemental/Baskerville.ttc", 1),
        ("Human", "/System/Library/Fonts/Optima.ttc", 0),
        ("Human-Bold", "/System/Library/Fonts/Optima.ttc", 1),
    ]:
        pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))
    PLACEMENTS.clear()
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle("Who Are You Bringing With You? | Christ at the Center | v7")
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
    paragraph(pdf, "Christ at the center.", "Book-Bold", 30, 35,
              FOREST, left, 568, width)
    paragraph(
        pdf,
        "Pastor, we are all disciples of Jesus. We remain in Him "
        "and depend on the Holy Spirit.",
        "Human", 11.5, 15, INK, left, 521, width, floor=500,
    )
    paragraph(pdf, "JOHN 15:5 / ACTS 1:8", "Human-Bold", 8.5, 11,
              MUTED, left, 494, width)

    sections = [
        ("1", "Remain in Him.",
         "Ministry can fill a day and leave little room to be with Jesus.",
         "Where are you making room to follow Him, without preparing "
         "something for everyone else?",
         "JOHN 15:5 / 1 TIMOTHY 4:16"),
        ("3", "Let someone know you.",
         "The crowd may see what the Pastor carries. Let someone you trust "
         "see what it costs.",
         "Who can you invite into an honest conversation?",
         "MARK 5:37 / 9:2 / 14:32-42 / GALATIANS 6:2"),
        ("12", "Bring people close. Entrust real ministry.",
         "The disciples learned beside Jesus before He sent them out together.",
         "Who are you helping follow Him, and what ministry could you "
         "entrust as they grow?",
         "MARK 3:14-15 / MARK 6:7, 30-31"),
    ]
    for index, (number, heading, statement, question, scripture) in enumerate(sections):
        top = 461 - index * 120
        paragraph(pdf, number, "Human-Bold", 32, 36, OCHRE,
                  left, top + 4, 45)
        bottom = paragraph(pdf, heading, "Book-Bold", 22, 25,
                           FOREST, text_left, top, text_width)
        bottom = paragraph(pdf, statement, "Human", 11.5, 15,
                           INK, text_left, bottom - 7, text_width)
        bottom = paragraph(pdf, question, "Human-Bold", 11.5, 15,
                           INK, text_left, bottom - 4, text_width)
        bottom = paragraph(pdf, scripture, "Human-Bold", 8.5, 11,
                           MUTED, text_left, bottom - 7, text_width)

    assert bottom > 110, "Relationship sections must clear the closing rule."
    pdf.setStrokeColor(OCHRE)
    pdf.setLineWidth(0.8)
    pdf.line(left, 110, left + width, 110)
    paragraph(pdf, "Who could you invite closer?", "Book-Bold", 23, 27,
              FOREST, left, 98, width, floor=70)
    paragraph(
        pdf,
        "Ask the Holy Spirit who to invite closer, then begin with one honest conversation.",
        "Human", 11, 15, INK, left, 64, width, floor=33,
    )
    for text, x, bottom, block_width, height in PLACEMENTS:
        assert 42 <= x and x + block_width <= 570, text
        assert 33 <= bottom and bottom + height <= 760, text
    pdf.showPage()
    pdf.save()
    print(f"Built {OUTPUT}; {len(PLACEMENTS)} bounded text blocks.")


if __name__ == "__main__":
    build()
