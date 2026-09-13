from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
OUTPUT = ROOT / "output/pdf/the-formation-gap.pdf"

CREAM = HexColor("#F4F0E3")
PAPER = HexColor("#FBF8EF")
FOREST = HexColor("#173F36")
FOREST_DARK = HexColor("#102F29")
INK = HexColor("#293630")
MUTED = HexColor("#68736D")
GOLD = HexColor("#D5A13A")
MOSS = HexColor("#789461")
SAGE = HexColor("#DEE8D3")
WHITE = HexColor("#FFFDF6")


def register_fonts() -> None:
    pdfmetrics.registerFont(
        TTFont("Georgia", "/System/Library/Fonts/Supplemental/Georgia.ttf")
    )
    pdfmetrics.registerFont(
        TTFont(
            "Georgia-Bold", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
        )
    )
    pdfmetrics.registerFontFamily(
        "Georgia",
        normal="Georgia",
        bold="Georgia-Bold",
        italic="Georgia",
        boldItalic="Georgia-Bold",
    )


def style(name, font, size, leading, color, alignment=TA_LEFT, **kwargs):
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=alignment,
        **kwargs,
    )


def draw_paragraph(pdf, text, paragraph_style, x, top, width):
    item = Paragraph(text, paragraph_style)
    _, height = item.wrap(width, 1000)
    item.drawOn(pdf, x, top - height)
    return top - height


def tracking_text(pdf, text, x, y, font="Helvetica-Bold", size=8.5, gap=1.7):
    pdf.setFont(font, size)
    pdf.setFillColor(MOSS)
    cursor = x
    for character in text:
        pdf.drawString(cursor, y, character)
        cursor += pdf.stringWidth(character, font, size) + gap


def movement(pdf, center_x, center_y, title, scripture, description, width):
    pdf.setFillColor(GOLD)
    pdf.circle(center_x, center_y, 7, fill=1, stroke=0)
    pdf.setStrokeColor(MOSS)
    pdf.setLineWidth(1.3)
    pdf.circle(center_x, center_y, 12, fill=0, stroke=1)

    title_style = style(
        f"{title}-title", "Georgia-Bold", 12.5, 15, FOREST, TA_CENTER
    )
    scripture_style = style(
        f"{title}-scripture", "Helvetica-Bold", 8.5, 11, MOSS, TA_CENTER
    )
    description_style = style(
        f"{title}-description", "Helvetica", 9.4, 12.2, INK, TA_CENTER
    )

    left = center_x - width / 2
    top = center_y - 19
    top = draw_paragraph(pdf, title, title_style, left, top, width) - 2
    top = draw_paragraph(pdf, scripture, scripture_style, left, top, width) - 5
    draw_paragraph(pdf, description, description_style, left, top, width)


def build_pdf() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    page_width, page_height = letter
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle("The Formation Gap")
    pdf.setAuthor("James Akers")
    pdf.setSubject("A Christ-centered, research-informed framework for forming leaders")

    pdf.setFillColor(CREAM)
    pdf.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    margin = 36
    content_width = page_width - margin * 2

    tracking_text(pdf, "THE FORMATION GAP", margin, 758)

    headline_style = style(
        "headline", "Georgia-Bold", 20, 24, FOREST, TA_LEFT
    )
    draw_paragraph(
        pdf,
        "Most pastors believe ministry should be shared. So why are so many still carrying so much of it alone?",
        headline_style,
        margin,
        735,
        500,
    )

    pdf.setStrokeColor(HexColor("#C8C7BC"))
    pdf.setLineWidth(0.8)
    pdf.line(page_width / 2, 570, page_width / 2, 654)

    stat_style = style("stat", "Georgia-Bold", 36, 38, FOREST)
    stat_gold_style = style("stat-gold", "Georgia-Bold", 36, 38, GOLD)
    stat_copy = style("stat-copy", "Helvetica", 10.2, 13.2, INK)
    stat_conclusion = style(
        "stat-conclusion", "Helvetica-Bold", 11.2, 16, FOREST, TA_CENTER
    )

    draw_paragraph(pdf, "96%", stat_style, margin, 654, 225)
    draw_paragraph(
        pdf,
        "say laypeople taking responsibility is a mark of a healthier church.",
        stat_copy,
        margin,
        604,
        225,
    )

    right_x = 326
    draw_paragraph(pdf, "41%", stat_gold_style, right_x, 654, 225)
    draw_paragraph(
        pdf,
        "say their church is doing a poor job developing new leaders.",
        stat_copy,
        right_x,
        604,
        225,
    )
    draw_paragraph(
        pdf,
        'Only <font face="Georgia-Bold" size="15" color="#D5A13A">9%</font> of pastors strongly agree their team is good at developing new leaders.',
        stat_conclusion,
        margin,
        568,
        content_width,
    )

    band_x = margin
    band_y = 462
    band_h = 80
    pdf.setFillColor(FOREST_DARK)
    pdf.roundRect(band_x, band_y, content_width, band_h, 13, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.roundRect(band_x, band_y, 7, band_h, 4, fill=1, stroke=0)

    realization_style = style(
        "realization", "Georgia-Bold", 16.5, 20.5, WHITE, TA_LEFT
    )
    research_style = style(
        "research", "Helvetica", 8.8, 11.5, SAGE, TA_LEFT
    )
    band_text_x = band_x + 25
    band_text_w = content_width - 48
    band_top = draw_paragraph(
        pdf,
        "If the first time we think about delegation is when the pastor is exhausted, we waited too long.",
        realization_style,
        band_text_x,
        536,
        band_text_w,
    ) - 7
    draw_paragraph(
        pdf,
        "In 2026, pastors said delegation was one of the most helpful steps they could take. They also named it one of the hardest.",
        research_style,
        band_text_x,
        band_top,
        band_text_w,
    )

    jesus_heading = style(
        "jesus-heading", "Georgia-Bold", 16.5, 20.5, FOREST, TA_CENTER
    )
    draw_paragraph(
        pdf,
        "Jesus called the Twelve to be with Him before He sent them out.",
        jesus_heading,
        70,
        451,
        page_width - 140,
    )

    path = pdf.beginPath()
    path.moveTo(104, 394)
    path.curveTo(185, 416, 229, 420, 306, 401)
    path.curveTo(384, 382, 429, 380, 508, 394)
    pdf.setStrokeColor(MOSS)
    pdf.setLineWidth(2)
    pdf.setLineCap(1)
    pdf.drawPath(path, fill=0, stroke=1)

    movement(
        pdf,
        104,
        394,
        "WITH HIM",
        "MARK 3:14",
        "They stayed close enough to watch Jesus, ask questions, fail and learn.",
        150,
    )
    movement(
        pdf,
        306,
        401,
        "SENT TOGETHER",
        "MARK 6:7",
        "Jesus gave authority and a clear assignment. No one went alone.",
        165,
    )
    movement(
        pdf,
        508,
        394,
        "BACK WITH HIM",
        "MARK 6:30-31",
        "They told Him what happened. Jesus called them to rest.",
        150,
    )

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(3)
    pdf.line(margin, 302, margin, 241)

    question_style = style(
        "question", "Georgia-Bold", 15.5, 19.5, FOREST, TA_LEFT
    )
    draw_paragraph(
        pdf,
        "Who is close enough to watch you lead, understand why, carry something real, and come back to talk about it?",
        question_style,
        margin + 17,
        302,
        content_width - 17,
    )

    action_style = style(
        "action", "Helvetica-Bold", 10.5, 14, INK, TA_LEFT
    )
    draw_paragraph(
        pdf,
        "You do not have to fix the whole system this week. Start with one person already near you. Invite them into one real part of ministry.",
        action_style,
        margin + 17,
        252,
        content_width - 17,
    )

    pdf.setFillColor(SAGE)
    pdf.roundRect(margin, 137, content_width, 74, 13, fill=1, stroke=0)

    heartbeat_style = style(
        "heartbeat", "Georgia-Bold", 12.2, 16.2, FOREST, TA_CENTER
    )
    draw_paragraph(
        pdf,
        "The same Holy Spirit that is gifting you, empowering you, teaching you is in them and calling them.",
        heartbeat_style,
        margin + 28,
        189,
        content_width - 56,
    )

    source_style = style(
        "sources", "Helvetica", 7.6, 9.6, MUTED, TA_LEFT
    )
    draw_paragraph(
        pdf,
        "Sources: Barna Group, 'Pastors Prefer Lay-Led Initiatives to New Church Programs But Struggle to Develop Leaders,' May 6, 2020 (survey of 508 U.S. Protestant senior pastors, July and August 2019); 'What Relieves Pastoral Burnout - and What Doesn't,' July 6, 2026 (survey of 507 U.S. Protestant senior pastors, January and February 2026).",
        source_style,
        margin,
        111,
        content_width,
    )

    pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    build_pdf()
