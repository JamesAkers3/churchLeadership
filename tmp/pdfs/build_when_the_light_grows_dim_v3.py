"""Approved layout revision; preserve v2 wording with light, readable boundaries."""

from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path('/Users/jamesakers/Desktop/PERSONAL/James New Endeavor')
OUTPUT = ROOT / 'output/pdf/when-the-light-grows-dim-v3.pdf'
ASSET = ROOT / 'docs/strategy/assets/when-the-light-grows-dim-support-scene-v1.png'
PAPER, FOREST, INK, MUTED, BORDER = map(HexColor,
    ['#F4F0E3', '#173F36', '#293630', '#56635D', '#88988B'])
LEFT, WIDTH = 42, 528
BLOCKS = []


def paragraph(pdf, copy, top, width=WIDTH, x=LEFT, font='Human', size=11,
              leading=15, color=INK):
    p = Paragraph(copy, ParagraphStyle('copy', fontName=font, fontSize=size,
                                      leading=leading, textColor=color))
    _, height = p.wrap(width, 1200)
    p.drawOn(pdf, x, top-height)
    BLOCKS.append((copy, x, top-height, width, height))
    return top-height


def rule(pdf, y):
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.7)
    pdf.line(LEFT, y, LEFT+WIDTH, y)


def build():
    for name, path, index in [
        ('Book-Bold', '/System/Library/Fonts/Supplemental/Baskerville.ttc', 1),
        ('Human', '/System/Library/Fonts/Optima.ttc', 0),
        ('Human-Bold', '/System/Library/Fonts/Optima.ttc', 1),
    ]:
        pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle('When the Light Grows Dim | v3')
    pdf.setAuthor('James Akers')
    pdf.setSubject('Layout review draft; pastoral care, not diagnosis or treatment')
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, 612, 792, fill=1, stroke=0)

    # Recognition: a single opening group with the original small artwork.
    paragraph(pdf, 'CHRIST AT THE CENTER / PASTORAL CARE', 759,
              font='Human-Bold', size=8.5, leading=11, color=MUTED)
    paragraph(pdf, 'When the Light Grows Dim', 731,
              font='Book-Bold', size=34, leading=39, color=FOREST)
    bottom = paragraph(pdf,
        'Some Pastors are not losing their passion.<br/>They are losing the capacity to carry it.',
        674, font='Book-Bold', size=24, leading=28, color=FOREST)
    recognition_top = bottom-12
    bottom = paragraph(pdf,
        "You may be the one everyone calls. The one who steps in when someone else can't."
        '<br/><br/>It can be hard to receive care when you\'re used to being the one who gives it.',
        recognition_top, width=306, size=11, leading=15)
    image = ImageReader(str(ASSET))
    iw, ih = image.getSize()
    scale = min(198/iw, 80/ih)
    dw, dh = iw*scale, ih*scale
    image_bottom = bottom+(recognition_top-bottom-dh)/2
    pdf.drawImage(image, 372+(198-dw)/2, image_bottom,
                  width=dw, height=dh, mask='auto')

    # One fine outline binds the evidence and reassurance, without a filled block.
    panel_top = min(bottom, image_bottom)-16
    panel_start = len(BLOCKS)
    bottom = paragraph(pdf, 'You are not the only one.', panel_top-16,
                       x=60, width=492, font='Book-Bold', size=20, leading=24, color=FOREST)
    row_top = bottom-10
    value_bottom = paragraph(pdf, 'More than', row_top, x=60, width=160,
                             font='Human-Bold', size=10, leading=13, color=MUTED)
    value_bottom = paragraph(pdf, '6 in 10', value_bottom-2, x=60, width=160,
                             font='Book-Bold', size=34, leading=38, color=FOREST)
    description_bottom = paragraph(pdf,
        'U.S. senior Protestant Pastors report feeling emotionally or mentally exhausted '
        '<font name="Human-Bold">frequently or sometimes.</font>',
        row_top-7, x=240, width=312, size=11, leading=15)
    bottom = paragraph(pdf,
        'You can love Jesus and still be exhausted. You are not failing because you are hurting. '
        'Receiving care is not a failure of faith.',
        min(value_bottom, description_bottom)-12, x=60, width=492)
    panel_bottom = bottom-12
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.9)
    pdf.roundRect(LEFT, panel_bottom, WIDTH, panel_top-panel_bottom, 6, stroke=1, fill=0)
    for copy, x, floor, width, height in BLOCKS[panel_start:]:
        assert x >= LEFT+16 and x+width <= LEFT+WIDTH-16, copy
        assert floor >= panel_bottom+11 and floor+height <= panel_top-15, copy

    # Christ's care has its own clear heading and a divider before the response.
    bottom = paragraph(pdf, 'The Heartbeat', panel_bottom-18,
                       font='Book-Bold', size=20, leading=24, color=FOREST)
    bottom = paragraph(pdf,
        'When the disciples returned, Jesus heard what they had done and taught. '
        'They had not had time to eat. He invited them to come away and rest.',
        bottom-7)
    bottom = paragraph(pdf, 'MARK 6:30-32 / PARAPHRASE', bottom-6,
                       font='Human-Bold', size=8, leading=10, color=MUTED)
    rule_y = bottom-14
    rule(pdf, rule_y)

    # Equal columns and consistent dividers, not a ranked recovery sequence.
    support_top = rule_y-14
    ends = []
    for i, (heading, copy) in enumerate([
        ('Make room<br/>to recover.', 'Protect rest with someone else actually covering the work.'),
        ('Bring care<br/>close.', 'Offer trusted support and qualified professional care when needed.'),
        ('Change what keeps<br/>causing harm.', 'Share responsibility and change harmful expectations.'),
    ]):
        x = LEFT+i*184
        end = paragraph(pdf, heading, support_top, x=x, width=160,
                        font='Book-Bold', size=14, leading=16, color=FOREST)
        ends.append(paragraph(pdf, copy, end-6, x=x, width=160, size=11, leading=14))
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.7)
    for x in [214, 398]:
        pdf.line(x, min(ends), x, support_top-2)

    bottom = paragraph(pdf, 'You do not have to carry this alone.', min(ends)-20,
                       font='Book-Bold', size=22, leading=26, color=FOREST)
    bottom = paragraph(pdf, 'You can begin privately, with someone you trust.', bottom-5)
    paragraph(pdf,
        'Source: Barna Group with Gloo, "Pastors\' Sense of Calling Is Up - Satisfaction Is Lagging," '
        'May 5, 2026. 2026 survey: 507 U.S. senior Protestant Pastors. Self-reported exhaustion, '
        'not a diagnosis; reported exhaustion has declined over the past decade.'
        '<br/>A conversation about care, not a diagnosis or treatment plan.',
        bottom-17, size=8, leading=10, color=MUTED)
    for copy, x, floor, width, height in BLOCKS:
        assert 42 <= x and x+width <= 570, copy
        assert 35 <= floor and floor+height <= 759, (copy, floor)
    pdf.showPage()
    pdf.save()
    print(f'Built {OUTPUT}: one Letter page, {len(BLOCKS)} bounded text blocks.')
    print(f'Outlined panel: {panel_top-panel_bottom:.1f} points tall; no fill.')
    print(f'Illustration: {dw:.1f} x {dh:.1f} points; full original scene.')


if __name__ == '__main__':
    build()
