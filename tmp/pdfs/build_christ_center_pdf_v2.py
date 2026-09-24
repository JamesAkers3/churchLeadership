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
SUPPORT_OUTPUT = ROOT / "output/pdf/a-pastor-can-be-known-and-still-unsupported-v2.pdf"
CIRCLES_OUTPUT = ROOT / "output/pdf/christ-at-the-center-1-3-12-v2.pdf"

CREAM = HexColor("#F4F0E3")
PAPER = HexColor("#FBF8EF")
FOREST = HexColor("#173F36")
FOREST_DARK = HexColor("#102F29")
INK = HexColor("#293630")
MUTED = HexColor("#56635D")
GOLD = HexColor("#D5A13A")
MOSS = HexColor("#607D50")
SAGE = HexColor("#C8DABA")
PALE_GOLD = HexColor("#F2E4BB")
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


def stat_column(pdf, x, top, width, label, value, copy, value_color):
    label_style = style(
        f"stat-label-{value}", "Helvetica-Bold", 8.1, 9.5, FOREST, TA_CENTER
    )
    value_style = style(
        f"stat-{value}", "Georgia-Bold", 36, 38, value_color, TA_CENTER
    )
    copy_style = style(
        f"stat-copy-{value}", "Helvetica", 9.3, 11.8, INK, TA_CENTER
    )
    draw_paragraph(pdf, label, label_style, x + 10, top, width - 20)
    draw_paragraph(pdf, value, value_style, x + 10, top - 15, width - 20)
    draw_paragraph(pdf, copy, copy_style, x + 18, top - 58, width - 36)


def base_canvas(path, title, subject):
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path), pagesize=letter, pageCompression=1)
    pdf.setTitle(title)
    pdf.setAuthor("James Akers")
    pdf.setSubject(subject)
    pdf.setFillColor(CREAM)
    pdf.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    return pdf


def build_support_pdf() -> None:
    pdf = base_canvas(
        SUPPORT_OUTPUT,
        "A Pastor Can Be Known and Still Unsupported",
        "A pastoral reflection on the difference between being known and receiving support",
    )
    page_width, _ = letter
    margin = 36
    content_width = page_width - 2 * margin

    tracking_text(pdf, "PASTORAL SUPPORT / THE RELATIONAL GAP", margin, 758)
    headline = style("support-headline", "Georgia-Bold", 23, 27, FOREST)
    draw_paragraph(
        pdf,
        "A Pastor can be known and still unsupported.",
        headline,
        margin,
        730,
        content_width,
    )
    intro = style("support-intro", "Helvetica", 10.5, 14, INK)
    draw_paragraph(
        pdf,
        "People may recognize the role and appreciate the ministry without seeing what it is costing the person carrying it.",
        intro,
        margin,
        671,
        content_width,
    )

    stat_column(
        pdf,
        margin,
        627,
        252,
        "KNOWN WELL",
        "80%",
        "say someone outside home and church knows them well.",
        FOREST,
    )
    stat_column(
        pdf,
        324,
        627,
        252,
        "SUPPORTED OFTEN",
        "22%",
        "receive spiritual support from peers or a mentor several times a month or more.",
        FOREST,
    )
    pdf.setStrokeColor(MOSS)
    pdf.setLineWidth(0.8)
    pdf.line(page_width / 2, 540, page_width / 2, 625)
    qualifier = style("stat-qualifier", "Helvetica", 8.7, 10.5, MUTED, TA_CENTER)
    draw_paragraph(
        pdf,
        "These are separate survey questions, not one group moving through three stages.",
        qualifier,
        margin,
        529,
        content_width,
    )
    context_stat = style(
        "context-stat", "Helvetica-Bold", 9.8, 12, FOREST, TA_CENTER
    )
    draw_paragraph(
        pdf,
        "<font name='Georgia-Bold' size='15' color='#8A5C00'>65%</font> report feeling lonely or isolated at least sometimes.",
        context_stat,
        margin + 20,
        499,
        content_width - 40,
    )

    pdf.setFillColor(FOREST_DARK)
    pdf.roundRect(margin, 357, content_width, 94, 12, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.rect(margin, 357, 6, 94, fill=1, stroke=0)
    bridge_headline = style(
        "bridge-headline", "Georgia-Bold", 14.5, 18, WHITE
    )
    bridge_body = style("bridge-body", "Helvetica", 9.7, 13, WHITE)
    draw_paragraph(
        pdf,
        "People can know a Pastor well and still miss when the Pastor needs help.",
        bridge_headline,
        margin + 24,
        425,
        content_width - 48,
    )
    draw_paragraph(
        pdf,
        "A Pastor may have people nearby without having a safe place to speak honestly or share the weight.",
        bridge_body,
        margin + 24,
        390,
        content_width - 48,
    )

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(3)
    pdf.line(margin, 273, margin, 334)
    jesus_label = style("jesus-label", "Helvetica-Bold", 8.2, 9.5, FOREST)
    jesus_text = style("jesus-text", "Georgia-Bold", 11.5, 15, FOREST)
    draw_paragraph(
        pdf,
        "JESUS IN GETHSEMANE",
        jesus_label,
        margin + 18,
        321,
        content_width - 40,
    )
    draw_paragraph(
        pdf,
        "Jesus named His sorrow, brought Peter, James and John closer, and asked them to keep watch. They fell asleep—but His willingness to ask was not weakness.",
        jesus_text,
        margin + 18,
        304,
        content_width - 40,
    )
    scripture_ref = style("jesus-scripture", "Helvetica-Bold", 8.2, 9.5, MOSS)
    draw_paragraph(
        pdf,
        "MARK 14:32-37",
        scripture_ref,
        margin + 18,
        274,
        content_width - 40,
    )

    pdf.setFillColor(PAPER)
    pdf.roundRect(margin, 121, content_width, 126, 12, fill=1, stroke=0)
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(3)
    pdf.line(margin + 18, 137, margin + 18, 231)
    question = style("support-question", "Georgia-Bold", 17, 21, FOREST)
    question_body = style("support-question-body", "Helvetica", 10.5, 14, INK)
    next_step = style("support-next-step", "Helvetica-Bold", 9.5, 12, FOREST)
    draw_paragraph(
        pdf,
        "Who knows the soul beneath your role?",
        question,
        margin + 34,
        227,
        content_width - 58,
    )
    draw_paragraph(
        pdf,
        "Who is close enough to see both the fruit and the cost—and present enough to help carry the weight?",
        question_body,
        margin + 34,
        189,
        content_width - 58,
    )
    draw_paragraph(
        pdf,
        "<b>Begin with one safe, honest conversation.</b><br/><font name='Helvetica' size='9'>You do not have to carry this alone or wait for a crisis to ask for support.</font>",
        next_step,
        margin + 34,
        154,
        content_width - 58,
    )

    source = style("support-source", "Helvetica", 7.5, 9.2, MUTED)
    draw_paragraph(
        pdf,
        "Source: Barna Group, '7-Year Trends: Pastors Feel More Loneliness & Less Support,' July 12, 2023. Displayed figures: 2022 survey of 585 U.S. Protestant senior Pastors. The figures are separate measures and should not be read as one scale.",
        source,
        margin,
        91,
        content_width,
    )
    pdf.showPage()
    pdf.save()


def ring_diagram(pdf, center_x, center_y):
    rings = [
        (108, SAGE, MOSS),
        (80, PALE_GOLD, GOLD),
        (55, PAPER, MOSS),
        (32, FOREST_DARK, FOREST_DARK),
    ]
    for radius, fill, stroke in rings:
        pdf.setFillColor(fill)
        pdf.setStrokeColor(stroke)
        pdf.setLineWidth(1.3)
        pdf.circle(center_x, center_y, radius, fill=1, stroke=1)
    number_style = style("ring-number", "Georgia-Bold", 11, 12, FOREST, TA_CENTER)
    draw_paragraph(pdf, "12", number_style, center_x - 20, center_y + 99, 40)
    draw_paragraph(pdf, "3", number_style, center_x + 52, center_y + 7, 32)
    draw_paragraph(pdf, "1", number_style, center_x - 64, center_y + 7, 32)
    center_style = style(
        "ring-center", "Helvetica-Bold", 8.2, 9.5, WHITE, TA_CENTER
    )
    draw_paragraph(pdf, "CHRIST", center_style, center_x - 27, center_y + 5, 54)


def action_block(pdf, top, number, action, body, scripture, height=59):
    x = 310
    width = 266
    marker_style = {
        "CHRIST": (FOREST_DARK, FOREST_DARK, WHITE, "C"),
        "1": (PAPER, MOSS, FOREST, "1"),
        "3": (PALE_GOLD, GOLD, FOREST, "3"),
        "12": (SAGE, MOSS, FOREST, "12"),
    }
    heading = style(
        f"action-heading-{number}", "Georgia-Bold", 10.6, 12.6, FOREST
    )
    body_style = style(f"action-body-{number}", "Helvetica", 8.6, 10.8, INK)
    scripture_style = style(
        f"action-scripture-{number}", "Helvetica-Bold", 7.4, 8.8, MOSS
    )
    if number == "CHRIST":
        text_x = x
        text_width = width
        heading_text = f"CHRIST / {action}"
    else:
        fill, stroke, text_color, marker_text = marker_style[number]
        pdf.setFillColor(fill)
        pdf.setStrokeColor(stroke)
        pdf.setLineWidth(1.2)
        pdf.circle(x + 13, top - 18, 11.5, fill=1, stroke=1)
        marker = style(
            f"action-marker-{number}",
            "Helvetica-Bold",
            7.5,
            8.5,
            text_color,
            TA_CENTER,
        )
        draw_paragraph(pdf, marker_text, marker, x + 1, top - 14, 24)
        text_x = x + 34
        text_width = width - 34
        heading_text = f"{number} / {action}"
    y = draw_paragraph(
        pdf, heading_text, heading, text_x, top - 7, text_width
    ) - 2
    y = draw_paragraph(pdf, body, body_style, text_x, y, text_width) - 1
    draw_paragraph(pdf, scripture, scripture_style, text_x, y, text_width)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.6)
    pdf.line(text_x, top - height, x + width, top - height)


def build_circles_pdf() -> None:
    pdf = base_canvas(
        CIRCLES_OUTPUT,
        "Christ at the Center - 1-3-12",
        "A relational framework for abiding, sharing weight, and forming people to carry the mission",
    )
    page_width, _ = letter
    margin = 36
    content_width = page_width - 2 * margin

    tracking_text(pdf, "CHRIST AT THE CENTER / 1-3-12", margin, 758)
    headline = style("circles-headline", "Georgia-Bold", 21, 25, FOREST)
    draw_paragraph(
        pdf,
        "Christ remains the source, and the weight was never meant to rest on one person.",
        headline,
        margin,
        730,
        content_width,
    )
    intro = style("circles-intro", "Helvetica", 10.4, 14, INK)
    draw_paragraph(
        pdf,
        "Jesus loved the crowds, walked closely with the Twelve, and let three see moments the rest of the Twelve did not.",
        intro,
        margin,
        660,
        content_width,
    )

    ring_diagram(pdf, 164, 458)
    action_block(
        pdf,
        583,
        "CHRIST",
        "THE SOURCE",
        "He holds both the leader and the ministry. Everything begins by remaining in Him.",
        "JOHN 15:5",
    )
    action_block(
        pdf,
        516,
        "1",
        "THE SOUL BENEATH THE ROLE",
        "Your life with Christ matters, not only the work in front of you.",
        "1 TIMOTHY 4:16",
    )
    action_block(
        pdf,
        449,
        "3",
        "TRUSTED SUPPORT",
        "Trusted peers or mentors see the cost, pray, speak truth and help carry what should not be carried alone.",
        "MARK 14:33 / GALATIANS 6:2",
        64,
    )
    action_block(
        pdf,
        382,
        "12",
        "PEOPLE BEING FORMED",
        "People are brought close enough to learn, given something real to carry and helped to grow into what God is calling them to do.",
        "MARK 3:14-15",
        66,
    )

    framework_label = style(
        "framework-label", "Helvetica-Bold", 7.4, 9, FOREST, TA_CENTER
    )
    framework_body = style(
        "framework-body", "Helvetica", 7.4, 9.3, MUTED, TA_CENTER
    )
    draw_paragraph(
        pdf,
        "RELATIONSHIPS, NOT RANK",
        framework_label,
        49,
        334,
        230,
    )
    draw_paragraph(
        pdf,
        "The numbers are a picture, not a rule. Every person has equal value. A Pastor's trusted support may include peers or mentors outside the team being led. Closer relationships still need healthy accountability.",
        framework_body,
        49,
        319,
        230,
    )

    pdf.setFillColor(PAPER)
    pdf.roundRect(margin, 154, content_width, 124, 12, fill=1, stroke=0)
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(3)
    pdf.line(margin + 18, 171, margin + 18, 260)
    cta = style("circles-cta", "Georgia-Bold", 17, 21, FOREST)
    cta_body = style("circles-cta-body", "Helvetica", 10.1, 13.5, INK)
    cta_step = style("circles-cta-step", "Helvetica-Bold", 9.2, 11, FOREST)
    draw_paragraph(
        pdf,
        "Put names to the circles.",
        cta,
        margin + 34,
        253,
        content_width - 58,
    )
    draw_paragraph(
        pdf,
        "Who helps you remain rooted? Who can see the cost? Who are you forming and entrusting?",
        cta_body,
        margin + 34,
        218,
        content_width - 58,
    )
    draw_paragraph(
        pdf,
        "<b>Write down one name. Start there.</b><br/><font name='Helvetica' size='8.8'>If a circle is empty, do not rush to fill it. Pray, then begin with one honest relationship.</font>",
        cta_step,
        margin + 34,
        190,
        content_width - 58,
    )

    source = style("circles-source", "Helvetica", 7.5, 9.2, MUTED)
    draw_paragraph(
        pdf,
        "Scripture: John 15:5; 1 Timothy 4:16; Mark 3:14-15; 5:37; 9:2; 14:33; Galatians 6:2. The pattern is relational; the numbers are not a rule.",
        source,
        margin,
        111,
        content_width,
    )
    pdf.showPage()
    pdf.save()


def build_pdfs() -> None:
    register_fonts()
    build_support_pdf()
    build_circles_pdf()


if __name__ == "__main__":
    build_pdfs()
