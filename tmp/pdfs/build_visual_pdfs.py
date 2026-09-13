from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
SOURCE = ROOT / "tmp/pdfs/ql"
OUTPUT = ROOT / "output/pdf"

BACKGROUND = HexColor("#181818")
FOREST = HexColor("#153F36")
FOREST_DEEP = HexColor("#0B3029")
CREAM = HexColor("#F8F4E8")
MUTED = HexColor("#D3D7CF")
GOLD = HexColor("#E6B24A")
GREEN = HexColor("#91B179")
CARD = HexColor("#20352F")


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


def page_size_for(image: Image.Image, width_inches: float = 11.0) -> tuple[float, float]:
    width_points = width_inches * 72
    return width_points, width_points * image.height / image.width


def draw_cropped_image(
    pdf: canvas.Canvas,
    source_path: Path,
    crop_box: tuple[int, int, int, int],
    page_size: tuple[float, float],
) -> None:
    with Image.open(source_path) as source_image:
        cropped = source_image.crop(crop_box).convert("RGB")
        pdf.setFillColor(BACKGROUND)
        pdf.rect(0, 0, page_size[0], page_size[1], fill=1, stroke=0)
        pdf.drawImage(
            ImageReader(cropped),
            0,
            0,
            width=page_size[0],
            height=page_size[1],
            preserveAspectRatio=True,
            mask="auto",
        )


def image_pdf(
    source_name: str,
    output_name: str,
    crop_box: tuple[int, int, int, int],
    title: str,
) -> None:
    source_path = SOURCE / source_name
    with Image.open(source_path) as source_image:
        cropped_size = source_image.crop(crop_box).size
        page_size = page_size_for(Image.new("RGB", cropped_size))

    output_path = OUTPUT / output_name
    pdf = canvas.Canvas(str(output_path), pagesize=page_size, pageCompression=1)
    pdf.setTitle(title)
    pdf.setAuthor("James Akers")
    pdf.setSubject("Christ-centered church health framework")
    draw_cropped_image(pdf, source_path, crop_box, page_size)
    pdf.showPage()
    pdf.save()


def paragraph(
    pdf: canvas.Canvas,
    text: str,
    style: ParagraphStyle,
    x: float,
    y_top: float,
    width: float,
) -> float:
    item = Paragraph(text, style)
    _, height = item.wrap(width, 1000)
    item.drawOn(pdf, x, y_top - height)
    return y_top - height


def tree_reading_page(pdf: canvas.Canvas, page_size: tuple[float, float]) -> None:
    width, height = page_size
    pdf.setFillColor(BACKGROUND)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    margin = 40
    pdf.setFont("Helvetica-Bold", 11)
    pdf.setFillColor(GREEN)
    pdf.drawString(margin, height - 40, "ROOTED. RENEWED. MULTIPLYING LIFE.")

    pdf.setFont("Georgia-Bold", 28)
    pdf.setFillColor(CREAM)
    pdf.drawString(margin, height - 78, "What the picture is showing us")

    gap = 18
    left_width = width * 0.59
    right_x = margin + left_width + gap
    right_width = width - right_x - margin
    card_top = height - 105
    card_bottom = 40
    card_height = card_top - card_bottom

    pdf.setFillColor(FOREST_DEEP)
    pdf.roundRect(margin, card_bottom, left_width, card_height, 16, fill=1, stroke=0)
    pdf.setStrokeColor(HexColor("#315C51"))
    pdf.setLineWidth(1)
    pdf.roundRect(margin, card_bottom, left_width, card_height, 16, fill=0, stroke=1)

    pdf.setFillColor(HexColor("#FFF7E4"))
    pdf.roundRect(right_x, card_bottom, right_width, card_height, 16, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.roundRect(right_x, card_bottom, 7, card_height, 4, fill=1, stroke=0)

    title_light = ParagraphStyle(
        "title_light",
        fontName="Georgia-Bold",
        fontSize=22,
        leading=26,
        textColor=CREAM,
        alignment=TA_LEFT,
        spaceAfter=12,
    )
    body_light = ParagraphStyle(
        "body_light",
        fontName="Helvetica",
        fontSize=13.2,
        leading=18.5,
        textColor=MUTED,
        alignment=TA_LEFT,
    )
    title_dark = ParagraphStyle(
        "title_dark",
        fontName="Georgia-Bold",
        fontSize=22,
        leading=26,
        textColor=FOREST,
        alignment=TA_LEFT,
        spaceAfter=12,
    )
    heartbeat = ParagraphStyle(
        "heartbeat",
        fontName="Helvetica-Bold",
        fontSize=14.2,
        leading=20.5,
        textColor=FOREST_DEEP,
        alignment=TA_LEFT,
    )
    body_dark = ParagraphStyle(
        "body_dark",
        fontName="Helvetica",
        fontSize=13.1,
        leading=19.2,
        textColor=FOREST,
        alignment=TA_LEFT,
    )
    scripture = ParagraphStyle(
        "scripture",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=FOREST,
        alignment=TA_LEFT,
    )

    left_x = margin + 24
    left_text_width = left_width - 48
    y = card_top - 27
    y = paragraph(pdf, "Reading the tree", title_light, left_x, y, left_text_width) - 13

    bullets = [
        "Roots are the calling, theology, values, and spiritual health that hold everything else.",
        "Buds are the first visible signs that something hidden is waking up.",
        "Flowers and pollinators show the church building real relationships with the community around it.",
        "Fruit and seeds are life change that can travel beyond one moment or ministry.",
        "Saplings are new life and new leadership growing beyond the original tree.",
    ]
    for bullet in bullets:
        y = paragraph(
            pdf,
            f'<font color="#E6B24A">&#8226;</font>&nbsp;&nbsp;{bullet}',
            body_light,
            left_x,
            y,
            left_text_width,
        ) - 12

    right_text_x = right_x + 27
    right_text_width = right_width - 51
    y = card_top - 27
    y = paragraph(pdf, "The Heartbeat", title_dark, right_text_x, y, right_text_width) - 12
    y = paragraph(
        pdf,
        "Systems do not create life. Jesus does. Healthy systems make room for the life He is already growing.",
        heartbeat,
        right_text_x,
        y,
        right_text_width,
    ) - 19
    y = paragraph(
        pdf,
        "A healthy church is rooted in Christ, alive through the Holy Spirit, tended by the Father, and bearing fruit that reaches people with the saving grace of Jesus.",
        body_dark,
        right_text_x,
        y,
        right_text_width,
    ) - 22

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1.5)
    pdf.line(right_text_x, y, right_text_x + right_text_width, y)
    y -= 20
    paragraph(
        pdf,
        "John 15:1–5&nbsp;&nbsp;·&nbsp;&nbsp;John 7:37–39<br/>Matthew 13:23&nbsp;&nbsp;·&nbsp;&nbsp;Mark 4:26–32",
        scripture,
        right_text_x,
        y,
        right_text_width,
    )


def tree_pdf() -> None:
    source_path = SOURCE / "tree-lifecycle-working-concept.html.png"
    crop_box = (20, 20, 1780, 1542)
    with Image.open(source_path) as source_image:
        cropped_size = source_image.crop(crop_box).size
        page_size = page_size_for(Image.new("RGB", cropped_size))

    output_path = OUTPUT / "rooted-renewed-multiplying-life.pdf"
    pdf = canvas.Canvas(str(output_path), pagesize=page_size, pageCompression=1)
    pdf.setTitle("Rooted. Renewed. Multiplying Life.")
    pdf.setAuthor("James Akers")
    pdf.setSubject("A Christ-centered picture of church renewal")

    draw_cropped_image(pdf, source_path, crop_box, page_size)
    pdf.showPage()
    tree_reading_page(pdf, page_size)
    pdf.showPage()
    pdf.save()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    register_fonts()

    tree_pdf()
    image_pdf(
        "christ-centered-leadership-cycle.html.png",
        "christ-at-the-center-1-3-12.pdf",
        (65, 20, 1735, 1490),
        "Christ at the Center: The 1-3-12 Principle",
    )
    image_pdf(
        "jesus-formation-rhythm.html.png",
        "the-way-jesus-formed-people.pdf",
        (245, 20, 1555, 1500),
        "The Way Jesus Formed People",
    )
    image_pdf(
        "from-passion-to-impact-export.html.png",
        "from-passion-to-impact.pdf",
        (15, 15, 1785, 1270),
        "From Passion to Impact",
    )


if __name__ == "__main__":
    main()
