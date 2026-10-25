"""Build the impact-centered pastoral-support companion revision."""

from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
from pathlib import Path
import json

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/strategy/pastoral-support-read-sheet-v7.md"
OUTPUT = ROOT / "output/pdf/a-pastor-can-be-known-and-still-unsupported-read-sheet-v7.pdf"
MAP = ROOT / "tmp/pdfs/pastoral-support-read-sheet-v7-content-map.json"

spec = spec_from_file_location("support_v6", ROOT / "tmp/pdfs/build_pastoral_support_read_sheet_v6.py")
v6 = module_from_spec(spec)
spec.loader.exec_module(v6)
v3 = v6.v3
v1 = v6.v1
base = v6.base

HINGE = ParagraphStyle(
    "support-v7-hinge",
    fontName="Georgia-Bold",
    fontSize=13.0,
    leading=16.0,
    textColor=v1.FOREST,
    allowWidows=0,
    allowOrphans=0,
)
REFERENCE = ParagraphStyle(
    "support-v7-reference",
    fontName="Arial-Bold",
    fontSize=8.5,
    leading=10.5,
    textColor=v1.GOLD_DARK,
    allowWidows=0,
    allowOrphans=0,
)
QUIET_QUOTE = ParagraphStyle(
    "support-v7-quiet-quote",
    fontName="Georgia-Bold",
    fontSize=10.2,
    leading=13.2,
    textColor=v1.FOREST,
    allowWidows=0,
    allowOrphans=0,
)
QUIET_AUTHOR = ParagraphStyle(
    "support-v7-quiet-author",
    fontName="Arial-Bold",
    fontSize=8.1,
    leading=9.8,
    textColor=v1.GOLD_DARK,
    allowWidows=0,
    allowOrphans=0,
)


class V7SupportSheet(v3.V3SupportSheet):
    total_pages = 4
    notes_page = 3

    def reference(self, text):
        self.paragraph(text, REFERENCE, gap=4)

    def quiet_quote(self, quote_text, author):
        top = self.y
        width = base.WIDTH - 26
        quote = Paragraph(base.markup(quote_text), QUIET_QUOTE)
        _, quote_h = quote.wrap(width - 22, 1000)
        byline_h = 0
        if author.strip():
            byline = Paragraph(base.markup(author), QUIET_AUTHOR)
            _, byline_h = byline.wrap(width - 22, 1000)
        total_h = quote_h + byline_h + (21 if author.strip() else 16)
        bottom = top - total_h
        if bottom < 57:
            raise ValueError("Quiet quotation overflows the page")

        self.c.addLiteral("/Artifact BMC")
        self.c.setFillColor(HexColor("#F2E8D2"))
        self.c.rect(base.LEFT, bottom, base.WIDTH, total_h, fill=1, stroke=0)
        self.c.setFillColor(v1.GOLD)
        self.c.rect(base.LEFT, bottom, 3, total_h, fill=1, stroke=0)
        self.c.addLiteral("EMC")

        quote_top = top - 8
        drawn = self.draw(quote_text, quote_top, QUIET_QUOTE, "BlockQuote", x=base.LEFT + 14, width=width - 16)
        if author.strip():
            self.draw(author, quote_top - drawn - 4, QUIET_AUTHOR, "P", x=base.LEFT + 14, width=width - 16)
        self.y = bottom - 7

    def impact_hinge(self, paragraphs):
        top = self.y - 2
        inner_width = base.WIDTH - 34
        measured = []
        content_h = 0
        for text in paragraphs:
            para = Paragraph(base.markup(text), HINGE)
            _, height = para.wrap(inner_width, 1000)
            measured.append((text, height))
            content_h += height
        total_h = content_h + 22 + (len(paragraphs) - 1) * 7
        bottom = top - total_h
        if bottom < 57:
            raise ValueError("Impact hinge overflows the page")

        self.c.addLiteral("/Artifact BMC")
        self.c.setStrokeColor(v1.GOLD)
        self.c.setLineWidth(1.2)
        self.c.line(base.LEFT, top, base.LEFT + base.WIDTH, top)
        self.c.line(base.LEFT, bottom, base.LEFT + base.WIDTH, bottom)
        self.c.addLiteral("EMC")

        cursor = top - 10
        for text, height in measured:
            self.draw(text, cursor, HINGE, "P", x=base.LEFT + 17, width=inner_width)
            cursor -= height + 7
        self.y = bottom - 8


def build():
    v1.SOURCE = SOURCE
    base.SOURCE = SOURCE
    base.OUTPUT = OUTPUT
    base.MAP = MAP
    flags = base.register_fonts()
    sections = v1.load_sections()

    raw = BytesIO()
    c = canvas.Canvas(raw, pagesize=base.PAGE, pageCompression=1, pdfVersion=(1, 4), initialFontName="Arial")
    c.setTitle("A Pastor Can Be Known and Still Unsupported - Read Sheet v7")
    c.setAuthor("James Akers")
    c.setCreator("James Akers")
    c.setSubject("A Christ-centered conversation about pastoral support, shared prayer, and shared responsibility")
    sheet = V7SupportSheet(c)

    opening = sections["Opening the conversation"]
    gethsemane = sections["Jesus named His sorrow"]
    bonhoeffer = sections["Bonhoeffer quotation"]

    sheet.page(1, opening[0])
    sheet.paragraph(opening[1], v1.BODY_COMPACT, gap=5)
    sheet.paragraph(opening[2], v1.BODY_COMPACT, gap=5)
    sheet.paragraph(opening[3], v1.EMPHASIS, gap=4)
    sheet.paragraph(opening[4], v1.BODY_COMPACT, gap=5)
    sheet.heading("Jesus named His sorrow")
    sheet.paragraph(gethsemane[0], v1.BODY_COMPACT, gap=3)
    sheet.reference(gethsemane[1])
    sheet.paragraph(gethsemane[2], v1.EMPHASIS, gap=4)
    sheet.paragraph(gethsemane[3], v1.BODY_COMPACT, gap=4)
    sheet.paragraph(gethsemane[4], v1.BODY_COMPACT, gap=5)
    sheet.quiet_quote(bonhoeffer[0], bonhoeffer[1])

    support = sections["Support changes what someone carries"]
    sheet.heading("Support changes what someone carries")
    sheet.paragraph(support[0], v1.BODY_COMPACT, gap=3)
    sheet.reference(support[1])
    sheet.paragraph(support[2], v1.BODY_COMPACT, gap=3)
    sheet.reference(support[3])

    turning = sections["The turning point"]
    sheet.page(2, "Support changes what someone carries.")
    sheet.impact_hinge(turning)
    sheet.heading("Questions worth sitting with")
    sheet.list(sections["Questions worth sitting with"][0].splitlines(), numbered=True, text_style=v1.BODY_COMPACT, gap=6)
    sheet.heading("Putting this into practice")
    practice = sections["Putting this into practice"]
    sheet.paragraph(practice[0], v1.BODY_COMPACT, gap=5)
    sheet.paragraph(practice[1], v1.BODY_COMPACT, gap=5)
    sheet.paragraph(practice[2], v1.EMPHASIS, gap=6)
    sheet.heading("Moving into the next chapter")
    moving = sections["Moving into the next chapter"]
    sheet.paragraph(moving[0], v1.BODY_COMPACT, gap=2)
    sheet.paragraph(moving[1], v1.EMPHASIS, gap=2)

    sheet.page(3, "Leading the conversation")
    sheet.heading("Before", notes=True)
    sheet.list(sections["Before the conversation"][0].splitlines(), text_style=v1.NOTES, gap=3)
    sheet.heading("During", notes=True)
    sheet.list(sections["During the conversation"][0].splitlines(), text_style=v1.NOTES, gap=3)
    sheet.heading("After", notes=True)
    sheet.list(sections["After the conversation"][0].splitlines(), text_style=v1.NOTES, gap=3)
    sheet.heading("Prayer prompts", notes=True)
    for paragraph in sections["Prayer prompts"]:
        sheet.paragraph(paragraph, v1.NOTES, gap=3)
    sheet.page(4, "Scripture and sources")
    sheet.heading("Scripture and content boundaries", notes=True)
    sheet.list(sections["Scripture and content boundaries"][0].splitlines(), text_style=v1.NOTES, gap=2)
    sheet.heading("Supporting quotation", notes=True)
    supporting = sections["Supporting quotation"]
    sheet.paragraph(supporting[0], v1.NOTES, gap=2)
    sheet.paragraph(supporting[1], v1.SMALL, gap=2)
    sheet.paragraph(supporting[2], v1.SMALL, gap=2)
    sheet.heading("Sources", notes=True)
    sheet.list(sections["Sources"][0].splitlines(), text_style=v1.SMALL, gap=2)
    sheet.heading("Prayer before the next step", notes=True)
    sheet.quiet_quote(sections["Prayer before the next step"][0], "")

    c.save()
    raw.seek(0)
    base.add_structure(raw, sheet)
    MAP.write_text(json.dumps({"font_embedding_flags": flags, "records": sheet.records}, indent=2, ensure_ascii=False) + "\n")
    print(f"Created {OUTPUT.name}: 4 pages; embedding restriction flags {flags}")
    print("Lowest content bottom by page:", [round(min(record["box"][1] for record in sheet.records if record["page"] == page), 1) for page in range(4)])


if __name__ == "__main__":
    build()
