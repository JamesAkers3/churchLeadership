"""Approved Scripture correction; exact NIV excerpt, other v4 wording retained."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from build_when_the_light_grows_dim_v3 import (
    ROOT, PAPER, FOREST, INK, MUTED, BORDER, LEFT, WIDTH, BLOCKS, paragraph, rule,
)

OUTPUT = ROOT / 'output/pdf/when-the-light-grows-dim-v5.pdf'


def build():
    BLOCKS.clear()
    for name, path, index in [
        ('Book-Bold', '/System/Library/Fonts/Supplemental/Baskerville.ttc', 1),
        ('Human', '/System/Library/Fonts/Optima.ttc', 0),
        ('Human-Bold', '/System/Library/Fonts/Optima.ttc', 1),
    ]:
        pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle('When the Light Grows Dim | v5')
    pdf.setAuthor('James Akers')
    pdf.setSubject('Image-free layout review; pastoral care, not diagnosis or treatment')
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, 612, 792, fill=1, stroke=0)

    # Recognition fills the opening; no blank placeholder for the earlier art.
    paragraph(pdf, 'CHRIST AT THE CENTER / PASTORAL CARE', 759,
              font='Human-Bold', size=8.5, leading=11, color=MUTED)
    paragraph(pdf, 'When the Light Grows Dim', 731,
              font='Book-Bold', size=34, leading=39, color=FOREST)
    bottom = paragraph(pdf,
        'Some Pastors are not losing their passion.<br/>They are losing the capacity to carry it.',
        674, font='Book-Bold', size=26, leading=31, color=FOREST)
    bottom = paragraph(pdf,
        "You may be the one everyone calls. The one who steps in when someone else can't.",
        bottom-15, size=11.5, leading=16)
    bottom = paragraph(pdf,
        "It can be hard to receive care when you're used to being the one who gives it.",
        bottom-8, size=11.5, leading=16)

    # Reassurance is one lightly bounded group, not a crisis headline.
    panel_top = bottom-24
    panel_start = len(BLOCKS)
    bottom = paragraph(pdf, 'You are not the only one.', panel_top-17,
                       x=60, width=492, font='Book-Bold', size=20, leading=24, color=FOREST)
    row_top = bottom-10
    value_bottom = paragraph(pdf, 'More than', row_top, x=60, width=160,
                             font='Human-Bold', size=10, leading=13, color=MUTED)
    value_bottom = paragraph(pdf, '6 in 10', value_bottom-2, x=60, width=160,
                             font='Book-Bold', size=30, leading=34, color=FOREST)
    description_bottom = paragraph(pdf,
        'U.S. senior Protestant Pastors report feeling emotionally or mentally exhausted '
        '<font name="Human-Bold">frequently or sometimes.</font>',
        row_top-7, x=240, width=312, size=11.5, leading=15.5)
    bottom = paragraph(pdf,
        '<font name="Human-Bold">You can love Jesus and still be exhausted.</font> '
        'You are not failing because you are hurting. Receiving care is not a failure of faith.',
        min(value_bottom, description_bottom)-12, x=60, width=492, size=11.5, leading=15.5)
    panel_bottom = bottom-15
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.9)
    pdf.roundRect(LEFT, panel_bottom, WIDTH, panel_top-panel_bottom, 6, stroke=1, fill=0)
    for copy, x, floor, width, height in BLOCKS[panel_start:]:
        assert x >= LEFT+16 and x+width <= LEFT+WIDTH-16, copy
        assert floor >= panel_bottom+14 and floor+height <= panel_top-16, copy

    # Christ's welcome and rest shape the care that follows.
    bottom = paragraph(pdf, 'The Heartbeat', panel_bottom-23,
                       font='Book-Bold', size=20, leading=24, color=FOREST)
    bottom = paragraph(pdf,
        '“Come with me by yourselves to a quiet place and get some rest.”',
        bottom-7, size=11.5, leading=15.5)
    bottom = paragraph(pdf, 'MARK 6:31 / NIV / EXCERPT', bottom-7,
                       font='Human-Bold', size=8, leading=10, color=MUTED)
    rule_y = bottom-16
    rule(pdf, rule_y)

    # Concurrent care: actual coverage, trusted support and changed conditions.
    support_top = rule_y-16
    ends = []
    for i, (heading, copy) in enumerate([
        ('Make room<br/>to recover.', 'Protect rest with someone else actually covering the work.'),
        ('Bring care<br/>close.', 'Offer trusted support and qualified professional care when needed.'),
        ('Change what keeps<br/>causing harm.', 'Share responsibility and change harmful expectations.'),
    ]):
        x = LEFT+i*184
        end = paragraph(pdf, heading, support_top, x=x, width=160,
                        font='Book-Bold', size=14, leading=16, color=FOREST)
        ends.append(paragraph(pdf, copy, end-7, x=x, width=160, size=11, leading=14))
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.7)
    for x in [214, 398]:
        pdf.line(x, min(ends), x, support_top-2)

    bottom = paragraph(pdf, 'You do not have to carry this alone.', min(ends)-23,
                       font='Book-Bold', size=22, leading=26, color=FOREST)
    bottom = paragraph(pdf, 'You can begin privately, with someone you trust.', bottom-5,
                       size=11.5, leading=15.5)
    paragraph(pdf,
        'Source: Barna Group with Gloo, "Pastors\' Sense of Calling Is Up - Satisfaction Is Lagging," '
        'May 5, 2026. 2026 survey: 507 U.S. senior Protestant Pastors. Self-reported exhaustion, '
        'not a diagnosis; reported exhaustion has declined over the past decade.'
        '<br/>A conversation about care, not a diagnosis or treatment plan.',
        bottom-20, size=8, leading=10, color=MUTED)
    for copy, x, floor, width, height in BLOCKS:
        assert 42 <= x and x+width <= 570, copy
        assert 35 <= floor and floor+height <= 759, (copy, floor)
    pdf.showPage()
    pdf.save()
    print(f'Built {OUTPUT}: one Letter page, {len(BLOCKS)} bounded text blocks; no illustration.')
    print(f'Lowest text block: {min(block[2] for block in BLOCKS):.1f} points above page bottom.')


if __name__ == '__main__':
    build()
