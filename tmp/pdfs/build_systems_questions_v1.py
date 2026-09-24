"""Three-page, print-first church systems conversation worksheet."""

from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path('/Users/jamesakers/Desktop/PERSONAL/James New Endeavor')
OUTPUT = ROOT / 'output/pdf/is-this-still-serving-the-calling-v1.pdf'
FOREST, INK, MUTED = map(HexColor, ['#173F36', '#293630', '#56635D'])
PAPER, SAGE, RULE = map(HexColor, ['#F4F0E3', '#E6EADF', '#A9B0A4'])
LEFT, WIDTH = 42, 528
PLACEMENTS = []


def item(text, font='Human', size=10.2, leading=13.5, color=INK):
    return Paragraph(text, ParagraphStyle('copy', fontName=font, fontSize=size,
                                         leading=leading, textColor=color))


def text(pdf, copy, x, top, width, font='Human', size=10.2, leading=13.5, color=INK):
    p = item(copy, font, size, leading, color)
    _, height = p.wrap(width, 1000)
    p.drawOn(pdf, x, top - height)
    PLACEMENTS.append((pdf.getPageNumber(), copy, x, top - height, width, height))
    return top - height


def page(pdf, title, number):
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, 612, 792, fill=1, stroke=0)
    text(pdf, 'CHRIST AT THE CENTER / LIFE-GIVING SYSTEMS', LEFT, 758, WIDTH,
         'Human-Bold', 8.5, 11, MUTED)
    text(pdf, title, LEFT, 733, WIDTH, 'Book-Bold', 30, 35, FOREST)
    text(pdf, f'{number} / 3', 537, 31, 33, 'Human', 8.5, 10, MUTED)


def line(pdf, x1, x2, y):
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(.45)
    pdf.line(x1, y, x2, y)


def table(pdf, top, widths, headers, rows, minimum, header_height=28):
    pdf.setFillColor(SAGE)
    pdf.rect(LEFT, top-header_height, WIDTH, header_height, fill=1, stroke=0)
    x = LEFT
    for width, header in zip(widths, headers):
        text(pdf, header, x+8, top-7, width-16, 'Human-Bold', 9, 11, FOREST)
        x += width
    cursor = top-header_height
    for row in rows:
        heights = [item(copy).wrap(width-16, 1000)[1] if copy else 0
                   for width, copy in zip(widths, row)]
        height = max(minimum, max(heights)+16)
        x = LEFT
        for width, copy in zip(widths, row):
            if copy:
                text(pdf, copy, x+8, cursor-8, width-16)
            else:
                for y in [cursor-22, cursor-40, cursor-58, cursor-76]:
                    if y > cursor-height+7:
                        line(pdf, x+9, x+width-9, y)
            x += width
        line(pdf, LEFT, LEFT+WIDTH, cursor-height)
        cursor -= height
    line(pdf, LEFT, LEFT+WIDTH, top)
    x = LEFT
    for width in [0]+widths:
        x += width
        line_vertical(pdf, x, cursor, top)
    return cursor


def line_vertical(pdf, x, bottom, top):
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(.45)
    pdf.line(x, bottom, x, top)


def identity(pdf, top, label='Ministry / process / system:'):
    text(pdf, label, LEFT, top, 180, 'Human-Bold', 9.5, 12)
    line(pdf, 174, 570, top-12)


def build():
    for name, path, index in [
        ('Book-Bold', '/System/Library/Fonts/Supplemental/Baskerville.ttc', 1),
        ('Human', '/System/Library/Fonts/Optima.ttc', 0),
        ('Human-Bold', '/System/Library/Fonts/Optima.ttc', 1),
    ]:
        pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))
    PLACEMENTS.clear()
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle('Is This Still Serving the Calling? | v1')
    pdf.setAuthor('James Akers')
    pdf.setSubject('Purpose, vision, mission, life-giving reach, and practical systems review')

    page(pdf, 'Is This Still Serving the Calling?', 1)
    text(pdf, '1 / Why are we doing this?', LEFT, 685, WIDTH,
         'Book-Bold', 22, 26, FOREST)
    text(pdf,
         'Pastor, you do not have to carry this conversation alone or arrive with every answer. '
         'Bring the people who do the work and the people affected by it. With Scripture open '
         'and the Holy Spirit leading, ask honestly what should continue, what needs care, '
         'and what needs to change.', LEFT, 646, WIDTH, size=10.5, leading=14)
    identity(pdf, 590)
    text(pdf, 'Church:', LEFT, 569, 70, 'Human-Bold', 9.5, 12)
    line(pdf, 80, 320, 557)
    text(pdf, 'Date:', 345, 569, 60, 'Human-Bold', 9.5, 12)
    line(pdf, 374, 570, 557)
    text(pdf, 'People in this conversation:', LEFT, 548, 160, 'Human-Bold', 9.5, 12)
    line(pdf, 176, 570, 536)
    questions = [
        ('Purpose', 'Why does this exist? What biblical responsibility or real need is it serving?'),
        ('Vision', 'What do we hope will be different in people\'s lives because of this?'),
        ('Mission', 'How does this help us practice our mission - not just repeat our mission statement?'),
        ('Christ at<br/>the center', 'Does the way we do this reflect Jesus\' character and methods? '
         'What in Scripture supports - or challenges - our approach?'),
        ('Fruit', 'What is actually happening? What have the people involved experienced, '
         'beyond attendance or activity?'),
        ('Honest<br/>examination', 'If we were starting today, would we build it this way? Why?'),
        ('Hidden cost', 'Who is carrying more than we realize? What does this require in time, '
         'money, relationships, and strength?'),
        ('Hard<br/>conversations', 'What concern have we avoided naming? What makes it difficult to talk about?'),
    ]
    bottom = table(pdf, 522, [84,252,192], ['What we examine', 'Questions worth asking', 'What we are seeing'],
                   [(f'<font name="Human-Bold">{label}</font>', question, '')
                    for label, question in questions], 50, 31)
    assert bottom >= 58, bottom
    text(pdf, 'Choose one ministry, process, or system to examine at a time.',
         LEFT, bottom-12, WIDTH, size=9.5, leading=12, color=MUTED)
    pdf.showPage()

    page(pdf, 'Is it life giving?', 2)
    text(pdf, '2 / Look at the people this touches.', LEFT, 685, WIDTH,
         'Book-Bold', 22, 26, FOREST)
    text(pdf, 'Systems do not create life. Jesus does. Healthy systems make room '
         'for the life He is already growing.', LEFT, 646, WIDTH,
         'Human-Bold', 11, 15, FOREST)
    identity(pdf, 602)
    areas = [
        ('The Pastor', 'Does this support faithful, shared leadership - or depend on the Pastor continually rescuing it?'),
        ('The congregation', 'Are people being formed, equipped, and entrusted - or repeatedly asked to fill gaps?'),
        ('The community', 'Have we listened to the people we hope to serve? Are we responding to their actual needs?'),
        ('The world through missions', 'How does our church\'s ministry cultivate prayer, generosity, '
         'partnership, and faithful service beyond our community?'),
    ]
    bottom = table(pdf, 576, [204,108,108,108],
                   ['Who it touches', 'Life and fruit', 'Cost and strain', 'Needed changes'],
                   [(f'<font name="Human-Bold">{label}</font><br/>{question}', '', '', '')
                    for label, question in areas], 100, 35)
    bottom = text(pdf, 'Life-giving does not mean effortless. Slow or costly ministry is not automatically failing.',
                  LEFT, bottom-19, WIDTH, size=10, leading=13.5)
    bottom = text(pdf, 'Every system does not need to serve all four directions equally. Consider its particular '
                  'calling, and the church\'s ministry as a whole.', LEFT, bottom-9, WIDTH, size=10, leading=13.5)
    assert bottom >= 49, bottom
    pdf.showPage()

    page(pdf, 'What will we do next?', 3)
    text(pdf, '3 / Choose a faithful next step.', LEFT, 685, WIDTH,
         'Book-Bold', 22, 26, FOREST)
    text(pdf, 'With Scripture open and the Holy Spirit leading, decide together what should change '
         'and how you will carry it. Choose one step you can put into practice and review.',
         LEFT, 646, WIDTH, size=10.5, leading=14)
    identity(pdf, 601)
    for index, choice in enumerate(['Strengthen', 'Share', 'Simplify', 'Redesign', 'Pause', 'Release']):
        x = LEFT + (index % 3)*176
        top = 571 - (index//3)*22
        pdf.setStrokeColor(FOREST)
        pdf.setLineWidth(.7)
        pdf.rect(x, top-10, 9, 9, fill=0, stroke=1)
        text(pdf, choice, x+17, top, 151, 'Human-Bold', 10.5, 13, FOREST)
    actions = [
        ('What did we decide, and why?', 46),
        ('What is our one next faithful step?', 54),
        ('Who will carry it?', 40),
        ('What authority, training, resources, and support will they need?', 62),
        ('What biblical responsibility must remain, even if we change how we carry it?', 62),
        ('Who needs to be heard before we act?', 48),
        ('How will we know it is helping?<br/><font size="9">Notice both fruit and cost. '
         'Listen to the people involved.</font>', 63),
        ('When will we review it, and who will be there?', 46),
    ]
    cursor = 526
    for prompt, height in actions:
        cursor = table(pdf, cursor, [192,336], ['', ''], [(prompt, '')], height, 0)
    assert cursor >= 95, cursor
    text(pdf, 'You do not have to repair every system at once. Begin with what needs your attention, '
         'support the people carrying it, and return to learn together.', LEFT, cursor-20, WIDTH,
         size=10.5, leading=14)
    for number, copy, x, bottom, width, height in PLACEMENTS:
        assert 42 <= x and x+width <= 570, (number, copy)
        assert 20 <= bottom and bottom+height <= 758, (number, copy, bottom)
    pdf.showPage()
    pdf.save()
    print(f'Built {OUTPUT}: 3 pages, {len(PLACEMENTS)} text blocks.')


if __name__ == '__main__':
    build()
