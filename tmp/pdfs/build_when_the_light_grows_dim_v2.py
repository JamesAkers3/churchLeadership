"""Pastor-facing revision: shared experience, receiving care, restrained artwork."""

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
OUTPUT = ROOT / 'output/pdf/when-the-light-grows-dim-v2.pdf'
ASSET = ROOT / 'docs/strategy/assets/when-the-light-grows-dim-support-scene-v1.png'
PAPER, FOREST, INK, MUTED = map(HexColor, ['#F4F0E3', '#173F36', '#293630', '#56635D'])
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


def build():
    for name, path, index in [
        ('Book-Bold', '/System/Library/Fonts/Supplemental/Baskerville.ttc', 1),
        ('Human', '/System/Library/Fonts/Optima.ttc', 0),
        ('Human-Bold', '/System/Library/Fonts/Optima.ttc', 1),
    ]:
        pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    pdf.setTitle('When the Light Grows Dim | v2')
    pdf.setAuthor('James Akers')
    pdf.setSubject('Draft for review; pastoral care, not diagnosis or treatment')
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, 612, 792, fill=1, stroke=0)
    paragraph(pdf, 'CHRIST AT THE CENTER / PASTORAL CARE', 759,
              font='Human-Bold', size=8.5, leading=11, color=MUTED)
    paragraph(pdf, 'When the Light Grows Dim', 731,
              font='Book-Bold', size=34, leading=39, color=FOREST)
    bottom = paragraph(pdf,
        'Some Pastors are not losing their passion.<br/>They are losing the capacity to carry it.',
        674, font='Book-Bold', size=24, leading=28, color=FOREST)

    recognition_top = bottom-18
    bottom = paragraph(pdf,
        "You may be the one everyone calls. The one who steps in when someone else can't."
        '<br/><br/>It can be hard to receive care when you\'re used to being the one who gives it.',
        recognition_top, width=306, size=11.5, leading=15.5)
    image = ImageReader(str(ASSET))
    iw, ih = image.getSize()
    scale = min(198/iw, 80/ih)
    dw, dh = iw*scale, ih*scale
    pdf.drawImage(image, 372+(198-dw)/2,
                  bottom+(recognition_top-bottom-dh)/2,
                  width=dw, height=dh, mask='auto')

    bottom = paragraph(pdf, 'You are not the only one.', bottom-22,
                       font='Book-Bold', size=20, leading=24, color=FOREST)
    row_top = bottom-10
    value_bottom = paragraph(pdf, 'More than', row_top, width=160,
                             font='Human-Bold', size=10, leading=13, color=MUTED)
    value_bottom = paragraph(pdf, '6 in 10', value_bottom-2, width=160,
                             font='Book-Bold', size=34, leading=38, color=FOREST)
    description_bottom = paragraph(pdf,
        'U.S. senior Protestant Pastors report feeling emotionally or mentally exhausted '
        '<font name="Human-Bold">frequently or sometimes.</font>',
        row_top-7, x=222, width=348, size=11.5, leading=15.5)
    bottom = paragraph(pdf,
        'You can love Jesus and still be exhausted. You are not failing because you are hurting. '
        'Receiving care is not a failure of faith.',
        min(value_bottom, description_bottom)-14, size=11, leading=15)

    bottom = paragraph(pdf, 'THE HEARTBEAT', bottom-18,
                       font='Human-Bold', size=8.5, leading=11, color=FOREST)
    bottom = paragraph(pdf,
        'When the disciples returned, Jesus heard what they had done and taught. '
        'They had not had time to eat. He invited them to come away and rest.',
        bottom-6, size=10.5, leading=14)
    bottom = paragraph(pdf, 'MARK 6:30-32 / PARAPHRASE', bottom-6,
                       font='Human-Bold', size=8, leading=10, color=MUTED)

    support_top = bottom-18
    ends = []
    for i, (heading, copy) in enumerate([
        ('Make room<br/>to recover.', 'Protect rest with someone else actually covering the work.'),
        ('Bring care<br/>close.', 'Offer trusted support and qualified professional care when needed.'),
        ('Change what keeps<br/>causing harm.', 'Share responsibility and change harmful expectations.'),
    ]):
        x = LEFT+i*180
        end = paragraph(pdf, heading, support_top, x=x, width=168,
                        font='Book-Bold', size=14, leading=16, color=FOREST)
        ends.append(paragraph(pdf, copy, end-6, x=x, width=168, size=10, leading=13))
    bottom = paragraph(pdf, 'You do not have to carry this alone.', min(ends)-18,
                       font='Book-Bold', size=22, leading=26, color=FOREST)
    bottom = paragraph(pdf, 'You can begin privately, with someone you trust.', bottom-5,
                       size=10.5, leading=14)

    footer_top = bottom-17
    paragraph(pdf,
        'Source: Barna Group with Gloo, "Pastors\' Sense of Calling Is Up - Satisfaction Is Lagging," '
        'May 5, 2026. 2026 survey: 507 U.S. senior Protestant Pastors. Self-reported exhaustion, '
        'not a diagnosis; reported exhaustion has declined over the past decade.'
        '<br/>A conversation about care, not a diagnosis or treatment plan.',
        footer_top, size=8, leading=10, color=MUTED)
    for copy, x, floor, width, height in BLOCKS:
        assert 42 <= x and x+width <= 570, copy
        assert 35 <= floor and floor+height <= 759, (copy, floor)
    pdf.showPage()
    pdf.save()
    print(f'Built {OUTPUT}: one Letter page, {len(BLOCKS)} bounded text blocks.')
    print(f'Illustration: {dw:.1f} x {dh:.1f} points; full original scene, no cropping.')


if __name__ == '__main__':
    build()
