from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import build_formation_gap_pdf as base


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output/pdf/the-formation-gap-v3.pdf"


def draw_stat(pdf, x, top, width, number, color, body):
    number_style = base.style(
        f"stat-{number}", "Georgia-Bold", 34, 37, color, TA_CENTER
    )
    body_style = base.style(
        f"stat-copy-{number}", "Helvetica", 8.8, 11.4, base.INK, TA_CENTER
    )
    next_top = base.draw_paragraph(pdf, number, number_style, x, top, width) - 8
    base.draw_paragraph(pdf, body, body_style, x + 4, next_top, width - 8)


def build_pdf() -> None:
    base.register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    page_width, _ = letter
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle("The Formation Gap")
    pdf.setAuthor("James Akers")
    pdf.setSubject("A Christ-centered, research-informed framework for forming leaders before exhaustion")

    pdf.setFillColor(base.CREAM)
    pdf.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)

    margin = 36
    content_width = page_width - margin * 2

    base.tracking_text(pdf, "THE FORMATION GAP", margin, 758)

    headline_style = base.style(
        "headline-v2", "Georgia-Bold", 20, 24, base.FOREST, TA_LEFT
    )
    base.draw_paragraph(
        pdf,
        "Most Pastors believe ministry should be shared. So why are so many still carrying so much of it alone?",
        headline_style,
        margin,
        735,
        500,
    )

    column_width = 164
    column_x = [36, 224, 412]
    for divider_x in (212, 400):
        pdf.setStrokeColor(HexColor("#C8C7BC"))
        pdf.setLineWidth(0.8)
        pdf.line(divider_x, 570, divider_x, 649)

    draw_stat(
        pdf,
        column_x[0],
        653,
        column_width,
        "96%",
        base.FOREST,
        "of Protestant senior Pastors agree that laypeople sharing responsibility is a mark of church health.",
    )
    draw_stat(
        pdf,
        column_x[1],
        653,
        column_width,
        "41%",
        base.GOLD,
        "of Protestant senior Pastors say their church does a poor job developing new leaders.",
    )
    draw_stat(
        pdf,
        column_x[2],
        653,
        column_width,
        "9%",
        base.GOLD,
        "of Protestant senior Pastors strongly agree their team is good at developing new leaders.",
    )

    band_x = margin
    band_y = 475
    band_h = 80
    pdf.setFillColor(base.FOREST_DARK)
    pdf.roundRect(band_x, band_y, content_width, band_h, 13, fill=1, stroke=0)
    pdf.setFillColor(base.GOLD)
    pdf.roundRect(band_x, band_y, 7, band_h, 4, fill=1, stroke=0)

    answer_style = base.style(
        "answer-v2", "Georgia-Bold", 16.5, 20.5, base.WHITE, TA_LEFT
    )
    answer_support_style = base.style(
        "answer-support-v2", "Helvetica", 9, 11.5, base.SAGE, TA_LEFT
    )
    answer_top = base.draw_paragraph(
        pdf,
        "Jesus called the Twelve to be with Him before He sent them out.",
        answer_style,
        band_x + 25,
        543,
        content_width - 50,
    ) - 7
    base.draw_paragraph(
        pdf,
        "Jesus formed people through shared life before He trusted them to carry the work. <font name='Helvetica-Bold' color='#D5A13A'>MARK 3:14</font>",
        answer_support_style,
        band_x + 25,
        answer_top,
        content_width - 50,
    )

    path = pdf.beginPath()
    path.moveTo(104, 424)
    path.curveTo(185, 446, 229, 450, 306, 431)
    path.curveTo(384, 412, 429, 410, 508, 424)
    pdf.setStrokeColor(base.MOSS)
    pdf.setLineWidth(2)
    pdf.setLineCap(1)
    pdf.drawPath(path, fill=0, stroke=1)

    base.movement(
        pdf,
        104,
        424,
        "WITH HIM",
        "MARK 3:14",
        "They stayed close enough to watch Jesus, ask questions, fail and learn.",
        150,
    )
    base.movement(
        pdf,
        306,
        431,
        "SENT TOGETHER",
        "MARK 6:7",
        "Jesus gave authority and a clear assignment. On this mission, no one went alone.",
        165,
    )
    base.movement(
        pdf,
        508,
        424,
        "BACK WITH HIM",
        "MARK 6:30-31",
        "They told Him what happened. Jesus called them to rest.",
        150,
    )

    pdf.setStrokeColor(base.GOLD)
    pdf.setLineWidth(3)
    pdf.line(margin, 321, margin, 255)

    question_style = base.style(
        "question-v2", "Georgia-Bold", 15.2, 19.2, base.FOREST, TA_LEFT
    )
    base.draw_paragraph(
        pdf,
        "Who is close enough to watch you lead, understand why, carry something real, and come back to talk about it?",
        question_style,
        margin + 17,
        321,
        content_width - 17,
    )

    action_style = base.style(
        "action-v2", "Helvetica-Bold", 10.2, 13.5, base.INK, TA_LEFT
    )
    base.draw_paragraph(
        pdf,
        "Start with one faithful believer already near you. Invite them into one real part of ministry.",
        action_style,
        margin + 17,
        269,
        content_width - 17,
    )

    pdf.setFillColor(base.SAGE)
    pdf.roundRect(margin, 137, content_width, 91, 13, fill=1, stroke=0)

    reminder_style = base.style(
        "reminder-v2", "Georgia-Bold", 11.5, 15, base.FOREST, TA_CENTER
    )
    spirit_style = base.style(
        "spirit-v2", "Helvetica-Bold", 9.2, 12.2, base.FOREST, TA_CENTER
    )
    reminder_bottom = base.draw_paragraph(
        pdf,
        "If we only begin forming people when the Pastor is exhausted,<br/>we started too late. But it is not too late to begin.",
        reminder_style,
        margin + 35,
        210,
        content_width - 70,
    ) - 10
    base.draw_paragraph(
        pdf,
        "The same Holy Spirit that is gifting you, empowering you, teaching you is in them and calling them.",
        spirit_style,
        margin + 35,
        reminder_bottom,
        content_width - 70,
    )

    source_style = base.style(
        "sources-v2", "Helvetica", 7.6, 9.6, base.MUTED, TA_LEFT
    )
    base.draw_paragraph(
        pdf,
        "Sources: Barna Group, 'Pastors Prefer Lay-Led Initiatives to New Church Programs But Struggle to Develop Leaders,' May 6, 2020 (survey of 508 U.S. Protestant senior Pastors, July and August 2019); 'What Relieves Pastoral Burnout - and What Doesn't,' July 6, 2026 (survey of 507 U.S. Protestant senior Pastors, January and February 2026).",
        source_style,
        margin,
        111,
        content_width,
    )

    pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    build_pdf()
