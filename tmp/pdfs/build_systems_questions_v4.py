"""Approved QA safeguards for shared discernment; preserves v1-v3."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from build_systems_questions_v1 import (
    ROOT, FOREST, INK, MUTED, LEFT, WIDTH, PLACEMENTS,
    page, text, table, identity, line,
)

OUTPUT = ROOT / 'output/pdf/is-this-still-serving-the-calling-v4.pdf'


def build():
    for name, path, index in [
        ('Book-Bold', '/System/Library/Fonts/Supplemental/Baskerville.ttc', 1),
        ('Human', '/System/Library/Fonts/Optima.ttc', 0),
        ('Human-Bold', '/System/Library/Fonts/Optima.ttc', 1),
    ]:
        pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))
    PLACEMENTS.clear()
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle('Is This Still Serving the Calling? | v4')
    pdf.setAuthor('James Akers')
    pdf.setSubject('Five-area life-giving review, shared discernment, and balanced ministry load')

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
        ('Fruit', 'What fruit and cost can we honestly point to, beyond how we feel about this ministry?'),
        ('Honest<br/>examination', 'What am I hoping this review will confirm?<br/>Is our concern with '
         'the ministry\'s purpose or how we carry it?'),
        ('Hidden cost', 'Who is carrying more than we realize? What does this require in time, '
         'money, relationships, and strength?'),
        ('Hard<br/>conversations', 'Whose experience have we not heard? What concern have we avoided naming?'),
    ]
    bottom = table(pdf, 522, [84,252,192], ['What we examine', 'Questions worth asking', 'What we are seeing'],
                   [(f'<font name="Human-Bold">{label}</font>', question, '')
                    for label, question in questions], 50, 31)
    assert bottom >= 58, bottom
    text(pdf, 'Review one ministry in an existing conversation. Make room to disagree, here or privately, '
         'without pressure or penalty.',
         LEFT, bottom-12, WIDTH, size=9.5, leading=12, color=MUTED)
    pdf.showPage()

    page(pdf, 'Is it life giving?', 2)
    text(pdf, '2 / Look at the people this touches.', LEFT, 685, WIDTH,
         'Book-Bold', 22, 26, FOREST)
    text(pdf, 'Systems do not create life. Jesus does. Healthy systems make room '
         'for the life He is already growing.', LEFT, 646, WIDTH,
         'Human-Bold', 11, 15, FOREST)
    text(pdf, 'Name direct or indirect benefit, no clear benefit, or N/A where a group does not apply.',
         LEFT, 622, WIDTH, size=9.5, leading=12, color=MUTED)
    identity(pdf, 602)
    areas = [
        ('Pastor', 'Does this support faithful leadership and shared responsibility, '
         'or require the Pastor to keep rescuing it?'),
        ('Staff/Volunteers', 'Are Staff and volunteers growing and equipped to lead, with the time, authority, '
         'and support the work requires?'),
        ('Local Church', 'Are people being formed, equipped, and entrusted, or simply filling gaps?'),
        ('Community', 'Have we listened? Are people receiving real help, dignity, '
         'and opportunities to encounter Jesus?'),
        ('World (Missions)', 'Does this strengthen prayer, generosity, partnership, '
         'or service beyond our community?'),
    ]
    bottom = table(pdf, 576, [204,108,108,108],
                   ['Who it touches', 'Life and fruit', 'Cost and strain', 'Needed changes'],
                   [(f'<font name="Human-Bold">{label}</font><br/>{question}', '', '', '')
                    for label, question in areas], 77, 35)
    bottom = text(pdf, 'There is no passing score. A focused ministry can be faithful, '
                  'and life-giving does not mean effortless.', LEFT, bottom-17, WIDTH,
                  size=10, leading=13.5)
    bottom = text(pdf, 'Name harm honestly, including within a group. Benefits do not cancel harm. Consider this ministry\'s '
                  'calling and the church\'s work as a whole.', LEFT, bottom-9, WIDTH,
                  size=10, leading=13.5)
    assert bottom >= 49, bottom
    pdf.showPage()

    page(pdf, 'What will we do next?', 3)
    text(pdf, '3 / Choose a faithful next step.', LEFT, 685, WIDTH,
         'Book-Bold', 22, 26, FOREST)
    text(pdf, 'With Scripture open and the Holy Spirit leading, decide together what should continue or change '
         'and how you will carry it. Continuing unchanged is a valid next step; no new assignment is needed.',
         LEFT, 646, WIDTH, size=10.5, leading=14)
    identity(pdf, 601)
    for index, choice in enumerate(['Continue / Strengthen', 'Share', 'Simplify', 'Redesign', 'Pause', 'Release']):
        x = LEFT + (index % 3)*176
        top = 571 - (index//3)*22
        pdf.setStrokeColor(FOREST)
        pdf.setLineWidth(.7)
        pdf.rect(x, top-10, 9, 9, fill=0, stroke=1)
        text(pdf, choice, x+17, top, 151, 'Human-Bold', 10.5, 13, FOREST)
    actions = [
        ('What did we decide, and why?', 46),
        ('What is our one next faithful step?', 54),
        ('Who will carry it? Have we confirmed their willingness and capacity?', 40),
        ('What protected time, authority, training, resources, and support will they need?', 62),
        ('What biblical responsibility must remain, even if we change how we carry it?', 62),
        ('What can we stop, simplify, or share before asking anyone to carry something new?', 48),
        ('How will we know it is helping?<br/><font size="9">Notice both fruit and cost. '
         'Listen to the people involved.</font>', 63),
        ('When will we review it, and who will be there?', 46),
    ]
    cursor = 526
    for prompt, height in actions:
        cursor = table(pdf, cursor, [192,336], ['', ''], [(prompt, '')], height, 0)
    assert cursor >= 78, cursor
    text(pdf, 'You do not have to repair every system at once. Begin with one supported step '
         'toward a healthier, more balanced load, and return to learn together.',
         LEFT, cursor-16, WIDTH, size=10.5, leading=14)
    for number, copy, x, bottom, width, height in PLACEMENTS:
        assert 42 <= x and x+width <= 570, (number, copy)
        assert 20 <= bottom and bottom+height <= 758, (number, copy, bottom)
    pdf.showPage()
    pdf.save()
    print(f'Built {OUTPUT}: 3 pages, {len(PLACEMENTS)} text blocks.')


if __name__ == '__main__':
    build()
