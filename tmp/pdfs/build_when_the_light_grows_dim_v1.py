"""First review PDFs: a Pastor-facing visual and two-page delivery notes."""

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
ASSET = ROOT / 'docs/strategy/assets/when-the-light-grows-dim-support-scene-v1.png'
VISUAL = ROOT / 'output/pdf/when-the-light-grows-dim-v1.pdf'
GUIDE = ROOT / 'output/pdf/when-the-light-grows-dim-talking-sheet-v1.pdf'
PAPER, FOREST, INK, MUTED = map(HexColor, ['#F4F0E3', '#173F36', '#293630', '#56635D'])
LEFT, WIDTH = 42, 528
PLACEMENTS = []


def paragraph(pdf, copy, top, width=WIDTH, x=LEFT, font='Human', size=11,
              leading=15, color=INK):
    p = Paragraph(copy, ParagraphStyle('copy', fontName=font, fontSize=size,
                                      leading=leading, textColor=color))
    _, height = p.wrap(width, 1200)
    p.drawOn(pdf, x, top-height)
    PLACEMENTS.append((pdf._filename, pdf.getPageNumber(), copy, x, top-height, width, height))
    return top-height


def page(pdf, eyebrow, number=None):
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, 612, 792, fill=1, stroke=0)
    paragraph(pdf, eyebrow, 759, font='Human-Bold', size=8.5, leading=11, color=MUTED)
    if number:
        paragraph(pdf, f'{number} / 2', 31, x=538, width=32,
                  size=8.5, leading=10, color=MUTED)


def section(pdf, heading, copy, top, gap=16):
    bottom = paragraph(pdf, heading, top, font='Book-Bold', size=19, leading=23, color=FOREST)
    bottom = paragraph(pdf, copy, bottom-7, size=10.5, leading=14)
    return bottom-gap


def make_pdf(path, title):
    pdf = canvas.Canvas(str(path), pagesize=letter, pageCompression=1)
    pdf.setTitle(title + ' | v1')
    pdf.setAuthor('James Akers')
    pdf.setSubject('Draft for review; pastoral care and church-owned relief, not clinical treatment')
    return pdf


def visual():
    pdf = make_pdf(VISUAL, 'When the Light Grows Dim')
    page(pdf, 'CHRIST AT THE CENTER / PASTORAL CARE')
    paragraph(pdf, 'When the Light Grows Dim', 731,
              font='Book-Bold', size=34, leading=39, color=FOREST)
    bottom = paragraph(pdf,
        'Some Pastors are not losing their passion.<br/>They are losing the capacity to carry it.',
        674, font='Book-Bold', size=24, leading=28, color=FOREST)
    bottom = paragraph(pdf,
        "You can still love Jesus, love people, and believe deeply in your calling<br/>"
        "while being worn down by what you've carried.", bottom-13, size=11, leading=15)

    image_top, image_height = bottom-10, 211
    image = ImageReader(str(ASSET))
    iw, ih = image.getSize()
    scale = min(WIDTH/iw, image_height/ih)
    dw, dh = iw*scale, ih*scale
    pdf.drawImage(image, LEFT+(WIDTH-dw)/2, image_top-image_height+(image_height-dh)/2,
                  width=dw, height=dh, mask='auto')
    bottom = paragraph(pdf,
        "Some things don't end when Sunday is over. Grief and conflict can follow you home. "
        'Even in quiet moments, you may be bracing for the next call.',
        image_top-image_height-13, size=11, leading=15)
    bottom = paragraph(pdf, 'THE HEARTBEAT', bottom-16,
                       font='Human-Bold', size=8.5, leading=11, color=FOREST)
    bottom = paragraph(pdf,
        'When the disciples returned, Jesus heard what they had done and taught. '
        'They had not had time to eat. He invited them to come away and rest.',
        bottom-6, size=10.5, leading=14)
    bottom = paragraph(pdf, 'MARK 6:30-32 / PARAPHRASE', bottom-6,
                       font='Human-Bold', size=8, leading=10, color=MUTED)

    support_top = bottom-18
    supports = [
        ('Make room<br/>to recover.', 'Protect rest with someone else actually covering the work.'),
        ('Bring care<br/>close.', 'Make room for trusted support and qualified professional care.'),
        ('Change what keeps<br/>causing harm.', 'Share responsibility and change harmful expectations.'),
    ]
    ends = []
    for i, (heading, copy) in enumerate(supports):
        x = LEFT+i*180
        end = paragraph(pdf, heading, support_top, x=x, width=168,
                        font='Book-Bold', size=14, leading=16, color=FOREST)
        ends.append(paragraph(pdf, copy, end-6, x=x, width=168, size=10, leading=13))
    bottom = paragraph(pdf, 'You do not have to carry this alone.', min(ends)-18,
                       font='Book-Bold', size=22, leading=26, color=FOREST)
    bottom = paragraph(pdf, 'You can begin privately, with someone you trust.', bottom-5,
                       size=10.5, leading=14)
    paragraph(pdf, 'A conversation about care, not a diagnosis or treatment plan.', bottom-13,
              size=8.5, leading=11, color=MUTED)
    pdf.showPage()
    pdf.save()


def guide():
    pdf = make_pdf(GUIDE, 'When the Light Grows Dim | Talking Sheet')
    page(pdf, 'WHEN THE LIGHT GROWS DIM / TALKING SHEET', 1)
    paragraph(pdf, 'Opening the conversation', 731,
              font='Book-Bold', size=30, leading=35, color=FOREST)
    top = paragraph(pdf, 'For the person presenting this page. These are notes to adapt, not a script to finish.',
                    679, size=10, leading=13, color=MUTED)-18
    top = section(pdf, 'Begin here',
        '"Pastor, before we talk about what the church needs to do next, I want to make room '
        "for what you've been carrying.<br/><br/>"
        '"There may be things you have walked through that never had room to settle. Sunday '
        'came again. Someone else needed you. You kept going.<br/><br/>'
        '"I don\'t want to assume I know what that has cost you. You don\'t have to explain it '
        'in this room. We can make room for a private conversation with someone you trust. '
        'And the church can begin sharing the weight without asking you to tell every part of your story."', top)
    top = paragraph(pdf,
        '<font name="Human-Bold">Pause.</font> Let people pass or ask to stop. '
        'Offer prayer with permission. Silence is not an invitation to press for disclosure.',
        top, size=10.5, leading=14)-18
    top = section(pdf, 'The Heartbeat',
        '<font name="Human-Bold">Read Mark 6:30-34.</font> The returning apostles reported back; '
        'Jesus invited them to rest. Then the crowd arrived and He responded with compassion. '
        'Preserve both: His care for the disciples and for the people they served. '
        'This is not a clinical recovery plan. Our application is that those carrying ministry need care, too.'
        '<br/><br/>In Gethsemane Jesus voiced His sorrow and asked trusted disciples to remain near '
        '(Matthew 26:36-46). Point to His honesty, not claim He had burnout or PTSD.'
        '<br/><br/>Our primary foundation remains 2 Timothy 1:6-7, read with verse 8: God\'s gift '
        'and power in costly ministry. Do not use the flame language to tell an exhausted Pastor '
        'to push harder or treat distress as weak faith.', top)
    top = section(pdf, 'Ask the church\'s leaders',
        'What have we learned to call normal that keeps asking too much of the Pastor?'
        '<br/><br/>If the Pastor stepped away to receive care, who would actually carry the work?'
        '<br/><br/>What can we remove or share now, rather than wait for a crisis?', top, gap=0)
    assert top >= 48, top
    pdf.showPage()

    page(pdf, 'WHEN THE LIGHT GROWS DIM / TALKING SHEET', 2)
    paragraph(pdf, 'Care and follow-through', 731,
              font='Book-Bold', size=30, leading=35, color=FOREST)
    top = 678
    top = section(pdf, 'Protect choice and privacy',
        'Offer privately: "Would it help to talk about what ministry has been costing you?" '
        'If welcomed: "What would help you feel supported? Who would you feel safe receiving help from?" '
        'People may decline. Explain confidentiality and its safety/reporting limits before sensitive '
        'conversation; never promise absolute secrecy. Do not ask for trauma, symptom, or treatment '
        'disclosures in a public or board meeting. If leaders have contributed to harm, help identify '
        'independent safe support.', top)
    top = section(pdf, 'A first response the church can own',
        'Agree on one immediate relief the Pastor welcomes: remove a nonessential demand, arrange '
        'real coverage, or help connect with agreed professional care. Name who will arrange it, '
        'when it starts, and how interruptions will be handled. Confirm covering Staff/Volunteers '
        'have willingness, capacity, time, and support. Record operational changes, not private '
        'disclosures. Check whether relief actually happened; do not measure healing by productivity.', top)
    top = paragraph(pdf, 'Do not send a wounded Pastor back into an unchanged fire.', top,
                    font='Book-Bold', size=17, leading=20, color=FOREST)-17
    top = section(pdf, 'Know the limits of this conversation',
        'Burnout and PTSD are not interchangeable. Burnout is an occupational phenomenon, not '
        'a medical diagnosis. Persistent distress, disrupted sleep, intrusive memories, avoidance, '
        'or feeling on alert can warrant professional attention; they are not a diagnostic checklist. '
        'Use "trauma-related stress symptoms" only when traumatic exposure is relevant. '
        'Diagnosis and treatment belong with qualified professionals. Prayer must not replace needed care.'
        '<br/><br/>Rest, leave, role changes, and return decisions need individual discernment and '
        'relevant professional guidance. Do not promise quick recovery or let staffing needs '
        'set a healing deadline. The dimming metaphor refers to human capacity, not God becoming absent.', top)
    top = section(pdf, 'If urgent help is needed',
        'In the United States, call or text 988 for suicide risk or an emotional crisis. '
        'For immediate danger call 911. Stop the advisory discussion and help connect with urgent support.',
        top, gap=12)
    top = paragraph(pdf,
        'Before the next chapter, make room for actual care and relief. '
        'No one needs to finish this book to receive help.', top,
        font='Human-Bold', size=10.5, leading=14, color=FOREST)-13
    top = paragraph(pdf,
        'Sources: Mark 6:30-34 (NKJV); Matthew 26:36-46 and 2 Timothy 1:6-8 (NIV). '
        'WHO, "Burn-out an occupational phenomenon"; VA National Center for PTSD, "PTSD Basics"; '
        '988 Lifeline, "What to Expect." Online sources checked September 16, 2026.'
        '<br/>Draft for review. Qualified clinical review is still needed before church use.',
        top, size=8.5, leading=11, color=MUTED)
    assert top >= 44, top
    pdf.showPage()
    pdf.save()


def build():
    for name, path, index in [
        ('Book-Bold', '/System/Library/Fonts/Supplemental/Baskerville.ttc', 1),
        ('Human', '/System/Library/Fonts/Optima.ttc', 0),
        ('Human-Bold', '/System/Library/Fonts/Optima.ttc', 1),
    ]:
        pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))
    visual()
    guide()
    for filename, page_number, copy, x, bottom, width, height in PLACEMENTS:
        assert 42 <= x and x+width <= 570, (filename, copy)
        floor = 20 if copy in ('1 / 2', '2 / 2') else 35
        assert floor <= bottom and bottom+height <= 759, (filename, page_number, copy, bottom)
    print(f'Built {VISUAL}: 1 page.')
    print(f'Built {GUIDE}: 2 pages; {len(PLACEMENTS)} bounded text blocks total.')


if __name__ == '__main__':
    build()
