"""Build the first pastoral-support companion read sheet."""

from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
from pathlib import Path
import json
import re

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/strategy/pastoral-support-read-sheet-v1.md"
OUTPUT = ROOT / "output/pdf/a-pastor-can-be-known-and-still-unsupported-read-sheet-v1.pdf"
MAP = ROOT / "tmp/pdfs/pastoral-support-read-sheet-v1-content-map.json"

spec = spec_from_file_location("rooted_base", ROOT / "tmp/pdfs/build_rooted_read_sheet_v1.py")
base = module_from_spec(spec)
spec.loader.exec_module(base)

PAPER = HexColor("#F7F1E5")
PAPER_LIGHT = HexColor("#FFFDF7")
FOREST = HexColor("#123F37")
INK = HexColor("#28332F")
MUTED = HexColor("#5C6962")
SAGE = HexColor("#6E8963")
GOLD = HexColor("#D9A12E")
GOLD_DARK = HexColor("#946500")


def style(name, size=10.8, leading=14.0, font="Arial", color=INK, **kwargs):
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        allowWidows=0,
        allowOrphans=0,
        **kwargs,
    )


BODY = style("support-body")
BODY_COMPACT = style("support-body-compact", 10.4, 13.3)
NOTES = style("support-notes", 9.3, 11.35)
SMALL = style("support-small", 8.6, 10.5, color=MUTED)
HEADING = style("support-heading", 15.4, 18.5, "Georgia-Bold", FOREST)
NOTE_HEADING = style("support-note-heading", 13.7, 16.5, "Georgia-Bold", FOREST)
EMPHASIS = style("support-emphasis", 11.4, 14.8, "Georgia-Bold", FOREST)
QUOTE = style("support-quote", 13.1, 17.0, "Georgia-Bold", FOREST)
QUOTE_AUTHOR = style("support-quote-author", 8.9, 11.0, "Arial-Bold", GOLD_DARK)


def clean(text):
    return text.replace("—", "-").replace("–", "-")


def load_sections():
    sections = {}
    text = clean(SOURCE.read_text())
    for part in re.split(r"(?m)^## ", text)[1:]:
        heading, body = part.split("\n", 1)
        sections[heading] = [p.strip() for p in body.strip().split("\n\n") if p.strip() != "---"]
    return sections


class SupportSheet(base.Sheet):
    total_pages = 4
    notes_page = 4

    def page(self, number, title):
        if self.pages:
            self.c.showPage()
        self.nodes = []
        self.pages.append(self.nodes)
        self.mcid = 0

        self.c.addLiteral("/Artifact BMC")
        self.c.setFillColor(PAPER)
        self.c.rect(0, 0, *base.PAGE, fill=1, stroke=0)
        self.c.setStrokeColor(GOLD)
        self.c.setLineWidth(1.35)
        self.c.line(base.LEFT, 728, base.LEFT + 48, 728)
        self.c.setFillColor(MUTED)
        self.c.setFont("Arial", 8.7)
        footer = "PASTORAL SUPPORT  |  READ SHEET" if number < self.notes_page else "PASTORAL SUPPORT  |  PRESENTER NOTES"
        self.c.drawString(base.LEFT, 29, footer)
        self.c.drawRightString(base.PAGE[0] - base.LEFT, 29, f"{number} / {self.total_pages}")
        self.c.addLiteral("EMC")

        if number == 1:
            self.draw(
                "A PASTOR CAN BE KNOWN AND STILL UNSUPPORTED.",
                755,
                style("support-eyebrow", 9.0, 11.5, "Arial-Bold", GOLD_DARK),
                "P",
            )
        else:
            self.c.addLiteral("/Artifact BMC")
            self.c.setFillColor(GOLD_DARK)
            self.c.setFont("Arial-Bold", 9.0)
            self.c.drawString(base.LEFT, 745.7, "A PASTOR CAN BE KNOWN AND STILL UNSUPPORTED.")
            self.c.addLiteral("EMC")

        self.y = 711
        title_size = 22.5 if number == 1 else 20.7
        title_leading = 26.5 if number == 1 else 24.5
        self.draw(title, self.y, style(f"support-title-{number}", title_size, title_leading, "Georgia-Bold", FOREST), "H1" if number == 1 else "H2")
        self.y -= self.last_height + 14

    def heading(self, text, notes=False):
        self.y -= 6
        self.paragraph(text, NOTE_HEADING if notes else HEADING, "H3" if notes else "H2", gap=5)

    def side_quote(self, main_text, quote_text, author):
        top = self.y
        left_width = 310
        right_x = base.LEFT + 332
        right_width = base.WIDTH - 332

        main_h = self.draw(main_text, top, BODY, "P", x=base.LEFT, width=left_width)

        quote_para = Paragraph(base.markup(quote_text), QUOTE)
        _, quote_h = quote_para.wrap(right_width - 26, 1000)
        author_para = Paragraph(base.markup(author), QUOTE_AUTHOR)
        _, author_h = author_para.wrap(right_width - 26, 1000)
        box_h = quote_h + author_h + 34
        box_bottom = top - box_h
        if box_bottom < 57:
            raise ValueError("Side quotation overflows the page")

        self.c.addLiteral("/Artifact BMC")
        self.c.setFillColor(PAPER_LIGHT)
        self.c.roundRect(right_x, box_bottom, right_width, box_h, 10, fill=1, stroke=0)
        self.c.setFillColor(GOLD)
        self.c.rect(right_x, box_bottom, 3.2, box_h, fill=1, stroke=0)
        self.c.addLiteral("EMC")

        quote_top = top - 14
        quote_h_drawn = self.draw(quote_text, quote_top, QUOTE, "BlockQuote", x=right_x + 14, width=right_width - 26)
        author_top = quote_top - quote_h_drawn - 8
        self.draw(author, author_top, QUOTE_AUTHOR, "P", x=right_x + 14, width=right_width - 26)

        self.y = min(top - main_h, box_bottom) - 8

    def quote_strip(self, quote_text, author):
        quote_para = Paragraph(base.markup(quote_text), QUOTE)
        _, quote_h = quote_para.wrap(base.WIDTH - 38, 1000)
        author_para = Paragraph(base.markup(author), QUOTE_AUTHOR)
        _, author_h = author_para.wrap(base.WIDTH - 38, 1000)
        box_h = quote_h + author_h + 32
        box_bottom = self.y - box_h
        if box_bottom < 57:
            raise ValueError("Quotation strip overflows the page")

        self.c.addLiteral("/Artifact BMC")
        self.c.setFillColor(PAPER_LIGHT)
        self.c.roundRect(base.LEFT, box_bottom, base.WIDTH, box_h, 10, fill=1, stroke=0)
        self.c.setFillColor(GOLD)
        self.c.rect(base.LEFT, box_bottom, 3.4, box_h, fill=1, stroke=0)
        self.c.addLiteral("EMC")

        quote_top = self.y - 12
        quote_h_drawn = self.draw(quote_text, quote_top, QUOTE, "BlockQuote", x=base.LEFT + 18, width=base.WIDTH - 36)
        author_top = quote_top - quote_h_drawn - 7
        self.draw(author, author_top, QUOTE_AUTHOR, "P", x=base.LEFT + 18, width=base.WIDTH - 36)
        self.y = box_bottom - 9


def build():
    base.SOURCE = SOURCE
    base.OUTPUT = OUTPUT
    base.MAP = MAP
    flags = base.register_fonts()
    sections = load_sections()

    raw = BytesIO()
    c = canvas.Canvas(raw, pagesize=base.PAGE, pageCompression=1, pdfVersion=(1, 4), initialFontName="Arial")
    c.setTitle("A Pastor Can Be Known and Still Unsupported - Read Sheet v1")
    c.setAuthor("James Akers")
    c.setCreator("James Akers")
    c.setSubject("A Christ-centered conversation about pastoral support and shared responsibility")
    sheet = SupportSheet(c)

    opening = sections["Opening the conversation"]
    sheet.page(1, opening[0])
    sheet.paragraph(opening[1], BODY, gap=6)
    sheet.paragraph(opening[2], BODY, gap=6)
    sheet.paragraph(opening[3], EMPHASIS, gap=5)

    sheet.heading("Jesus invited people closer")
    gethsemane = sections["Jesus invited people closer"]
    sheet.paragraph(gethsemane[0], BODY, gap=5)
    sheet.paragraph(gethsemane[1], BODY, gap=6)
    bonhoeffer = sections["Bonhoeffer quotation"]
    sheet.side_quote(gethsemane[2], bonhoeffer[0], bonhoeffer[1])

    sheet.page(2, "The weight can be shared without diminishing the calling.")
    for paragraph in sections["The weight can be shared without diminishing the calling"]:
        paragraph_style = EMPHASIS if paragraph.startswith("**The calling") else BODY
        sheet.paragraph(paragraph, paragraph_style, gap=6)
    sheet.heading("Compassion takes different forms")
    compassion = sections["Compassion takes different forms"]
    sheet.paragraph(compassion[0], EMPHASIS, gap=6)
    sheet.paragraph(compassion[1], BODY, gap=7)
    stanley = sections["Andy Stanley quotation"]
    # Let the warning land as a deliberate closing reflection rather than another paragraph.
    sheet.y = min(sheet.y, 210)
    sheet.quote_strip(stanley[0], stanley[1])

    sheet.page(3, "Care becomes real when someone carries part of the weight.")
    sheet.paragraph(compassion[2], BODY, gap=6)
    sheet.paragraph(compassion[3], EMPHASIS, gap=7)
    sheet.heading("Questions worth sitting with")
    sheet.list(sections["Questions worth sitting with"][0].splitlines(), numbered=True, text_style=BODY_COMPACT, gap=5)
    sheet.heading("Putting this into practice")
    for paragraph in sections["Putting this into practice"]:
        paragraph_style = EMPHASIS if paragraph.startswith("Caring for") else BODY_COMPACT
        sheet.paragraph(paragraph, paragraph_style, gap=5)
    sheet.heading("Moving into the next chapter")
    for paragraph in sections["Moving into the next chapter"]:
        sheet.paragraph(paragraph, EMPHASIS if paragraph.startswith("That brings") else BODY_COMPACT, gap=4)

    sheet.page(4, "Presenter notes")
    sheet.list(sections["Notes for the presenter"][0].splitlines(), text_style=NOTES, gap=3)
    sheet.heading("Scripture and content boundaries", notes=True)
    sheet.list(sections["Scripture and content boundaries"][0].splitlines(), text_style=NOTES, gap=3)
    sheet.heading("Sources", notes=True)
    sheet.list(sections["Sources"][0].splitlines(), text_style=SMALL, gap=2)

    c.save()
    raw.seek(0)
    base.add_structure(raw, sheet)
    MAP.write_text(json.dumps({"font_embedding_flags": flags, "records": sheet.records}, indent=2, ensure_ascii=False) + "\n")
    print(f"Created {OUTPUT.name}: 4 pages; embedding restriction flags {flags}")
    print("Lowest content bottom by page:", [round(min(record["box"][1] for record in sheet.records if record["page"] == page), 1) for page in range(4)])


if __name__ == "__main__":
    build()
