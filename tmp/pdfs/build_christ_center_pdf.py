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
OUTPUT = ROOT / "output/pdf/christ-at-the-center-1-3-12.pdf"

CREAM = HexColor("#F4F0E3")
PAPER = HexColor("#FBF8EF")
FOREST = HexColor("#173F36")
FOREST_DARK = HexColor("#102F29")
INK = HexColor("#293630")
MUTED = HexColor("#68736D")
GOLD = HexColor("#D5A13A")
MOSS = HexColor("#789461")
SAGE = HexColor("#DEE8D3")
PALE_GOLD = HexColor("#EEE4C5")
WHITE = HexColor("#FFFDF6")
RULE = HexColor("#C8C7BC")


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


def stat(pdf, center_x, top, value, copy, value_color, width=158):
    value_style = style(
        f"stat-{value}", "Georgia-Bold", 32, 34, value_color, TA_CENTER
    )
    copy_style = style(
        f"stat-copy-{value}", "Helvetica", 9.1, 11.5, INK, TA_CENTER
    )
    left = center_x - width / 2
    draw_paragraph(pdf, value, value_style, left, top, width)
    draw_paragraph(pdf, copy, copy_style, left, top - 39, width)


def ring_diagram(pdf, center_x, center_y):
    rings = [
        (91, SAGE, MOSS),
        (64, PALE_GOLD, GOLD),
        (43, PAPER, MOSS),
        (25, FOREST_DARK, FOREST_DARK),
    ]
    for radius, fill, stroke in rings:
        pdf.setFillColor(fill)
        pdf.setStrokeColor(stroke)
        pdf.setLineWidth(1.2)
        pdf.circle(center_x, center_y, radius, fill=1, stroke=1)

    number_style = style(
        "ring-number", "Georgia-Bold", 11, 12, FOREST, TA_CENTER
    )
    draw_paragraph(pdf, "12", number_style, center_x - 16, center_y + 81, 32)
    draw_paragraph(pdf, "3", number_style, center_x - 16, center_y + 58, 32)
    draw_paragraph(pdf, "1", number_style, center_x - 16, center_y + 38, 32)

    center_style = style(
        "ring-center", "Helvetica-Bold", 7.4, 8.5, WHITE, TA_CENTER
    )
    draw_paragraph(pdf, "CHRIST", center_style, center_x - 24, center_y + 4, 48)

def relationship_block(pdf, top, number, heading, body, scripture):
    x = 294
    width = 282
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(2.4)
    pdf.line(x, top - 1, x, top - 54)

    heading_style = style(
        f"relationship-heading-{number}",
        "Georgia-Bold",
        10.9,
        13.4,
        FOREST,
        TA_LEFT,
    )
    body_style = style(
        f"relationship-body-{number}", "Helvetica", 8.9, 11.4, INK, TA_LEFT
    )
    scripture_style = style(
        f"relationship-scripture-{number}",
        "Helvetica-Bold",
        7.4,
        9,
        MOSS,
        TA_LEFT,
    )

    text_x = x + 12
    text_width = width - 12
    next_top = draw_paragraph(
        pdf,
        f"{number} / {heading}",
        heading_style,
        text_x,
        top,
        text_width,
    ) - 3
    next_top = draw_paragraph(pdf, body, body_style, text_x, next_top, text_width) - 2
    draw_paragraph(pdf, scripture, scripture_style, text_x, next_top, text_width)


def build_pdf() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    page_width, page_height = letter
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle("Christ at the Center - 1-3-12")
    pdf.setAuthor("James Akers")
    pdf.setSubject(
        "A Christ-centered framework for stewarding proximity, trust and responsibility"
    )

    pdf.setFillColor(CREAM)
    pdf.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    margin = 36
    content_width = page_width - margin * 2

    tracking_text(pdf, "CHRIST AT THE CENTER / 1-3-12", margin, 758)

    headline_style = style(
        "headline", "Georgia-Bold", 22, 26, FOREST, TA_LEFT
    )
    draw_paragraph(
        pdf,
        "Being surrounded is not the same as being carried.",
        headline_style,
        margin,
        733,
        content_width,
    )

    stat(pdf, 119, 672, "80%", "say someone outside home and church knows them well.", FOREST)
    stat(pdf, 306, 672, "65%", "report feeling lonely or isolated at least sometimes.", GOLD)
    stat(
        pdf,
        493,
        672,
        "22%",
        "receive spiritual support from peers or a mentor several times a month or more.",
        FOREST,
    )

    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.7)
    pdf.line(212, 587, 212, 668)
    pdf.line(400, 587, 400, 668)

    pdf.setFillColor(SAGE)
    pdf.roundRect(margin, 548, content_width, 31, 10, fill=1, stroke=0)
    research_bridge = style(
        "research-bridge", "Georgia-Bold", 11.5, 14, FOREST, TA_CENTER
    )
    draw_paragraph(
        pdf,
        "Being known is not always the same as being supported.",
        research_bridge,
        margin + 16,
        569,
        content_width - 32,
    )

    pdf.setFillColor(FOREST_DARK)
    pdf.roundRect(margin, 476, content_width, 57, 13, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.roundRect(margin, 476, 7, 57, 4, fill=1, stroke=0)
    jesus_statement = style(
        "jesus-statement", "Georgia-Bold", 14.2, 18, WHITE, TA_LEFT
    )
    draw_paragraph(
        pdf,
        "Jesus loved everyone fully. He did not give everyone the same access, assignment or responsibility.",
        jesus_statement,
        margin + 25,
        519,
        content_width - 48,
    )

    central_statement = style(
        "central-statement", "Georgia-Bold", 12.5, 15.5, FOREST, TA_CENTER
    )
    draw_paragraph(
        pdf,
        "The crowd may see what the pastor carries. The trusted few must be allowed to see what it costs.",
        central_statement,
        72,
        459,
        page_width - 144,
    )

    ring_diagram(pdf, 158, 327)

    relationship_block(
        pdf,
        414,
        "1",
        "THE SOUL BENEATH THE ROLE",
        "Before anyone sees the pastor, Christ knows the person. Abide before you lead.",
        "JOHN 15:5",
    )
    relationship_block(
        pdf,
        345,
        "3",
        "THE FEW WHO KNOW THE COST",
        "They witnessed Jesus confront death, reveal glory and carry sorrow. They saw moments the crowd did not.",
        "MARK 5:37 / 9:2 / 14:33",
    )
    relationship_block(
        pdf,
        276,
        "12",
        "PEOPLE FORMED TO CARRY THE MISSION",
        "They were with Jesus before they were sent. He shared life, truth and real responsibility.",
        "MARK 3:14-15",
    )

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(3)
    pdf.line(margin, 203, margin, 144)

    question_style = style(
        "question", "Georgia-Bold", 14.8, 18.5, FOREST, TA_LEFT
    )
    draw_paragraph(
        pdf,
        "Who knows the soul beneath your role?",
        question_style,
        margin + 17,
        203,
        content_width - 17,
    )
    application_style = style(
        "application", "Helvetica-Bold", 9.8, 13, INK, TA_LEFT
    )
    draw_paragraph(
        pdf,
        "Who has seen both the fruit and the cost? Who are you intentionally forming to carry the mission, not merely help with the work?",
        application_style,
        margin + 17,
        172,
        content_width - 17,
    )

    pdf.setFillColor(SAGE)
    pdf.roundRect(margin, 82, content_width, 53, 13, fill=1, stroke=0)
    heartbeat_style = style(
        "heartbeat", "Georgia-Bold", 12.3, 15.5, FOREST, TA_CENTER
    )
    draw_paragraph(
        pdf,
        "Different proximity is not favoritism. It is faithful stewardship.",
        heartbeat_style,
        margin + 30,
        116,
        content_width - 60,
    )

    source_style = style("sources", "Helvetica", 6.8, 8.6, MUTED, TA_LEFT)
    draw_paragraph(
        pdf,
        "Source: Barna Group, '7-Year Trends: Pastors Feel More Loneliness and Less Support,' July 12, 2023. The three figures are separate survey measures and should not be read as one scale. 2015 survey: 901 U.S. Protestant senior pastors. 2022 survey: 585 U.S. Protestant senior pastors.",
        source_style,
        margin,
        62,
        content_width,
    )

    pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    build_pdf()
