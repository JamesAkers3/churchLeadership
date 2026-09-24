"""Approved hybrid: v3 lead and v4 application, with exact supporting Scripture."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import build_formation_gap_pdf as base
from build_formation_gap_v3 import draw_stat
from build_formation_gap_v4 import QUOTE


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output/pdf/the-formation-gap-v5.pdf"
LEAD = "Jesus called the Twelve to be with Him before He sent them out."


def build_pdf():
    base.register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle("The Formation Gap")
    pdf.setAuthor("James Akers")
    pdf.setSubject("Shared ministry: biblical reflection, exact Scripture and practical application")
    pdf.setFillColor(base.CREAM)
    pdf.rect(0, 0, *letter, fill=1, stroke=0)
    margin, content_width = 36, 540

    base.tracking_text(pdf, "THE FORMATION GAP", margin, 758)
    base.draw_paragraph(
        pdf,
        "Most Pastors believe ministry should be shared. So why are so many still carrying so much of it alone?",
        base.style("headline", "Georgia-Bold", 20, 24, base.FOREST),
        margin, 735, 500,
    )

    for divider_x in (212, 400):
        pdf.setStrokeColor(HexColor("#C8C7BC"))
        pdf.setLineWidth(0.8)
        pdf.line(divider_x, 570, divider_x, 649)
    for x, number, color, copy in (
        (36, "96%", base.FOREST,
         "of Protestant senior Pastors agreed that laypeople sharing responsibility is a mark of church health."),
        (224, "41%", base.GOLD,
         "of Protestant senior Pastors said their church does a poor job developing new leaders."),
        (412, "9%", base.GOLD,
         "of Protestant senior Pastors strongly agreed their team is good at developing new leaders."),
    ):
        draw_stat(pdf, x, 653, 164, number, color, copy)

    pdf.setFillColor(base.FOREST_DARK)
    pdf.roundRect(margin, 475, content_width, 80, 13, fill=1, stroke=0)
    pdf.setFillColor(base.GOLD)
    pdf.roundRect(margin, 475, 7, 80, 4, fill=1, stroke=0)
    lead_bottom = base.draw_paragraph(
        pdf, LEAD,
        base.style("reflection-lead", "Georgia-Bold", 16.5, 20.5, base.WHITE),
        margin + 25, 543, content_width - 50,
    )
    quote_bottom = base.draw_paragraph(
        pdf,
        QUOTE + " <font face='Helvetica-Bold' color='#D5A13A'>MARK 3:14 / NIV</font>",
        base.style("scripture", "Helvetica", 9, 11.5, base.SAGE),
        margin + 25, lead_bottom - 7, content_width - 50,
    )
    assert quote_bottom >= 483, "Scripture panel needs more room."

    base.draw_paragraph(
        pdf, "PUTTING THIS INTO PRACTICE",
        base.style("application-label", "Helvetica-Bold", 8.2, 10, base.MUTED, TA_CENTER),
        margin, 465, content_width,
    )
    path = pdf.beginPath()
    path.moveTo(104, 424)
    path.curveTo(185, 446, 229, 450, 306, 431)
    path.curveTo(384, 412, 429, 410, 508, 424)
    pdf.setStrokeColor(base.MOSS)
    pdf.setLineWidth(2)
    pdf.setLineCap(1)
    pdf.drawPath(path, fill=0, stroke=1)
    for x, y, title, reading, copy, width in (
        (104, 424, "WITH HIM", "READ MARK 3:14",
         "Invite someone to serve beside you. Explain what you're doing and why.", 150),
        (306, 431, "SENT TOGETHER", "READ MARK 6:7-13",
         "Agree on a clear responsibility. Give them room to lead, with support.", 165),
        (508, 424, "BACK WITH HIM", "READ MARK 6:30-31",
         "Make time to listen afterward. Talk about what happened, and make room for rest.", 150),
    ):
        base.movement(pdf, x, y, title, reading, copy, width)

    pdf.setStrokeColor(base.GOLD)
    pdf.setLineWidth(3)
    pdf.line(margin, 321, margin, 255)
    base.draw_paragraph(
        pdf,
        "Who is close enough to watch you lead, understand why, carry something real, and come back to talk about it?",
        base.style("question", "Georgia-Bold", 15.2, 19.2, base.FOREST),
        margin + 17, 321, content_width - 17,
    )
    base.draw_paragraph(
        pdf,
        "Start with one faithful believer already near you. Invite them into one real part of ministry.",
        base.style("action", "Helvetica-Bold", 10.2, 13.5, base.INK),
        margin + 17, 269, content_width - 17,
    )

    pdf.setFillColor(base.SAGE)
    pdf.roundRect(margin, 137, content_width, 91, 13, fill=1, stroke=0)
    reminder_bottom = base.draw_paragraph(
        pdf,
        "If we only begin forming people when the Pastor is exhausted,<br/>we started too late. But it is not too late to begin.",
        base.style("reminder", "Georgia-Bold", 11.5, 15, base.FOREST, TA_CENTER),
        margin + 35, 210, content_width - 70,
    )
    base.draw_paragraph(
        pdf,
        "The same Holy Spirit that is gifting you, empowering you, teaching you is in them and calling them.",
        base.style("spirit", "Helvetica-Bold", 9.2, 12.2, base.FOREST, TA_CENTER),
        margin + 35, reminder_bottom - 10, content_width - 70,
    )

    base.draw_paragraph(
        pdf,
        "Historical research: Barna Group, 'Pastors Prefer Lay-Led Initiatives to New Church Programs But Struggle to Develop Leaders,' May 6, 2020. All three figures: survey of 508 U.S. Protestant senior Pastors, July 25-August 13, 2019. These findings concern shared responsibility and leadership development; they do not measure how much ministry a Pastor carries alone.",
        base.style("source", "Helvetica", 7.6, 9.6, base.MUTED),
        margin, 111, content_width,
    )
    pdf.showPage()
    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
